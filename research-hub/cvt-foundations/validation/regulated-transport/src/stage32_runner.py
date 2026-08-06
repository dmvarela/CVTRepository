from __future__ import annotations

import argparse
import hashlib
import json
import math
import time
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from scipy.special import expit, logit

from . import stage32_compare as compare

IDENTITY_COLUMNS = [
    "row_id",
    "partition_index",
    "design_hash",
    "forcing_family",
    "forcing_stratum",
]
OUTCOME_COLUMNS = [
    "row_id",
    "target_reached",
    "viable",
    "hosted",
    "failure_reason",
    "probe_valid",
    "sensitivity_probe_valid",
    "solver_success",
    "accounting_valid",
    "bounds_valid",
    "productive_pool_monotone",
]


def _sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def _sha256_file(path: Path) -> str:
    return _sha256_bytes(path.read_bytes())


def _bool_token(value: Any) -> str:
    if isinstance(value, (bool, np.bool_)):
        return "1" if bool(value) else "0"
    text = str(value).strip().lower()
    if text in {"true", "1"}:
        return "1"
    if text in {"false", "0"}:
        return "0"
    raise ValueError(f"Cannot interpret boolean value: {value!r}")


def _design_hash_digest(frame: pd.DataFrame) -> str:
    ordered = frame.sort_values("partition_index")
    payload = "\n".join(ordered.design_hash.astype(str)).encode("utf-8")
    return _sha256_bytes(payload)


def _identity_digest(frame: pd.DataFrame) -> str:
    columns = list(IDENTITY_COLUMNS)
    if "training_subset" in frame.columns:
        columns.append("training_subset")
    ordered = frame.sort_values("partition_index")
    lines = ["\t".join(map(str, row)) for row in ordered[columns].itertuples(index=False, name=None)]
    return _sha256_bytes(("\n".join(lines) + "\n").encode("utf-8"))


def _outcome_digest(frame: pd.DataFrame) -> str:
    ordered = frame.sort_values("partition_index")
    lines: list[str] = []
    boolean_positions = {1, 2, 3, 5, 6, 7, 8, 9, 10}
    for row in ordered[OUTCOME_COLUMNS].itertuples(index=False, name=None):
        values = [
            _bool_token(value) if index in boolean_positions else str(value)
            for index, value in enumerate(row)
        ]
        lines.append("\t".join(values))
    return _sha256_bytes(("\n".join(lines) + "\n").encode("utf-8"))


def _rounded_gate_digest(frame: pd.DataFrame, columns: list[str], decimals: int) -> str:
    ordered = frame.sort_values("partition_index")
    values = ordered[columns].to_numpy(float)
    format_string = f"%.{decimals}f"
    lines = ["\t".join(format_string % value for value in row) for row in values]
    return _sha256_bytes(("\n".join(lines) + "\n").encode("utf-8"))


def verify_portable_seal(data_dir: Path, seal_path: Path, output_dir: Path) -> dict[str, Any]:
    seal = json.loads(seal_path.read_text(encoding="utf-8"))
    if (data_dir / "test.csv").exists():
        raise ValueError("Final test data are present during Stage 3.2")

    stage31_manifest_path = data_dir / "stage31_manifest.json"
    if not stage31_manifest_path.exists():
        raise ValueError("Stage 3.1 manifest is missing")
    stage31_manifest = json.loads(stage31_manifest_path.read_text(encoding="utf-8"))
    if stage31_manifest.get("test_partition_opened") or stage31_manifest.get("test_partition_generated"):
        raise ValueError("Stage 3.1 manifest reports that the final test was generated or opened")

    report: dict[str, Any] = {
        "version": seal["version"],
        "source_workflow_run": seal["source_workflow_run"],
        "source_artifact_id": seal["source_artifact_id"],
        "source_artifact_digest": seal["source_artifact_digest"],
        "test_partition_present": False,
        "test_partition_opened": False,
        "partitions": {},
        "passed": True,
    }
    actual_hashes: dict[str, str] = {}

    for partition, expected in seal["partitions"].items():
        csv_path = data_dir / f"{partition}.csv"
        if not csv_path.exists():
            raise ValueError(f"Missing sealed partition: {csv_path.name}")
        frame = pd.read_csv(csv_path)
        actual_file_hash = _sha256_file(csv_path)
        actual_hashes[csv_path.name] = actual_file_hash

        checks = {
            "rows": int(len(frame)) == int(expected["rows"]),
            "exact_artifact_hash": actual_file_hash == expected["file_sha256"],
            "design_hash": _design_hash_digest(frame) == expected["design_hash_sha256"],
            "identity_digest": _identity_digest(frame) == expected["identity_digest"],
            "outcome_digest": _outcome_digest(frame) == expected["outcome_digest"],
            "rounded_gate_digest": _rounded_gate_digest(
                frame,
                seal["gate_columns"],
                int(seal["gate_round_decimals"]),
            )
            == expected["rounded_gate_digest"],
            "hosted_count": int(frame.hosted.sum()) == int(expected["hosted_count"]),
            "target_reached_count": int(frame.target_reached.sum())
            == int(expected["target_reached_count"]),
            "viable_count": int(frame.viable.sum()) == int(expected["viable_count"]),
            "failure_reason_counts": {
                str(key): int(value)
                for key, value in frame.failure_reason.value_counts().sort_index().items()
            }
            == expected["failure_reason_counts"],
            "solver_success": bool(frame.solver_success.map(_bool_token).eq("1").all()),
            "accounting_valid": bool(frame.accounting_valid.map(_bool_token).eq("1").all()),
            "bounds_valid": bool(frame.bounds_valid.map(_bool_token).eq("1").all()),
            "productive_monotone": bool(
                frame.productive_pool_monotone.map(_bool_token).eq("1").all()
            ),
            "primary_probe_valid": bool(frame.probe_valid.map(_bool_token).eq("1").all()),
            "sensitivity_probe_valid": bool(
                frame.sensitivity_probe_valid.map(_bool_token).eq("1").all()
            ),
        }
        failed = [name for name, passed in checks.items() if not passed]
        report["partitions"][partition] = {
            "file_sha256": actual_file_hash,
            "checks": checks,
            "failed_checks": failed,
        }
        if failed:
            report["passed"] = False

    output_dir.mkdir(parents=True, exist_ok=True)
    report_path = output_dir / "portable_seal_report.json"
    report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    if not report["passed"]:
        raise ValueError(f"Portable evidence seal failed; see {report_path}")
    report["actual_hashes"] = actual_hashes
    return report


def threshold_tune_bounded(
    x: np.ndarray,
    y: np.ndarray,
    folds: list[tuple[np.ndarray, np.ndarray]],
    *,
    chunk_size: int = 128,
) -> tuple[np.ndarray, float, int]:
    """Frozen direct-constraint search with bounded memory use.

    This is algebraically the same 9^4 threshold grid and Newton update used by
    the preregistered implementation. It processes candidate thresholds in
    blocks so the full 7,200 x 4 x 6,561 tensor is never materialized.
    """
    quantiles = np.quantile(x, np.arange(0.1, 1.0, 0.1), axis=0)
    mesh = np.meshgrid(*[quantiles[:, index] for index in range(4)], indexing="ij")
    combinations = np.column_stack([item.ravel() for item in mesh])
    total = np.zeros(len(combinations), dtype=float)
    y = np.asarray(y, float)

    for start in range(0, len(combinations), chunk_size):
        stop = min(start + chunk_size, len(combinations))
        block = combinations[start:stop]
        block_total = np.zeros(len(block), dtype=float)
        for train_index, validation_index in folds:
            z_train = np.min(
                x[train_index, :, None] - block.T[None, :, :],
                axis=1,
            )
            z_validation = np.min(
                x[validation_index, :, None] - block.T[None, :, :],
                axis=1,
            )
            y_train = y[train_index, None]
            intercept = np.full(
                len(block),
                logit(np.clip(y[train_index].mean(), 1e-8, 1.0 - 1e-8)),
            )
            slope = np.ones(len(block), dtype=float)
            for _ in range(8):
                eta = intercept[None, :] + z_train * slope[None, :]
                probability = expit(eta)
                residual = probability - y_train
                weight = probability * (1.0 - probability)
                gradient_intercept = residual.sum(axis=0) + 1e-6 * intercept
                gradient_slope = (residual * z_train).sum(axis=0) + 1e-6 * slope
                hessian_intercept = weight.sum(axis=0) + 1e-6
                hessian_cross = (weight * z_train).sum(axis=0)
                hessian_slope = (weight * z_train * z_train).sum(axis=0) + 1e-6
                determinant = np.maximum(
                    hessian_intercept * hessian_slope - hessian_cross * hessian_cross,
                    1e-12,
                )
                delta_intercept = (
                    hessian_slope * gradient_intercept
                    - hessian_cross * gradient_slope
                ) / determinant
                delta_slope = (
                    -hessian_cross * gradient_intercept
                    + hessian_intercept * gradient_slope
                ) / determinant
                intercept -= np.clip(delta_intercept, -5.0, 5.0)
                slope = np.maximum(0.0, slope - np.clip(delta_slope, -5.0, 5.0))
            block_total += np.mean(
                (
                    expit(intercept[None, :] + z_validation * slope[None, :])
                    - y[validation_index, None]
                )
                ** 2,
                axis=0,
            )
        total[start:stop] = block_total / len(folds)

    best = float(total.min())
    tied = np.flatnonzero(total - best < 0.0005)
    center = np.median(x, axis=0)
    selected_index = int(
        tied[np.argmin(np.abs(combinations[tied] - center).sum(axis=1))]
    )
    return combinations[selected_index], float(total[selected_index]), int(len(combinations))


def _false_safe_comparison(metrics: pd.DataFrame, model: str, reference: str) -> dict[str, Any]:
    indexed = metrics.set_index("model")
    model_row = indexed.loc[model]
    reference_row = indexed.loc[reference]
    estimable = bool(
        int(model_row.high_confidence_count) >= 50
        and int(reference_row.high_confidence_count) >= 50
    )
    worsening = (
        float(model_row.high_confidence_false_safe)
        - float(reference_row.high_confidence_false_safe)
        if estimable
        else None
    )
    return {
        "estimable": estimable,
        "model_count": int(model_row.high_confidence_count),
        "reference_count": int(reference_row.high_confidence_count),
        "model_false_safe_rate": (
            float(model_row.high_confidence_false_safe)
            if int(model_row.high_confidence_count) > 0
            else None
        ),
        "reference_false_safe_rate": (
            float(reference_row.high_confidence_false_safe)
            if int(reference_row.high_confidence_count) > 0
            else None
        ),
        "worsening": worsening,
        "passes": bool(not estimable or worsening <= 0.02),
    }


def _postprocess_results(data_dir: Path, output_dir: Path, seal_report: dict[str, Any]) -> dict[str, Any]:
    metrics_path = output_dir / "validation_metrics.csv"
    selection_path = output_dir / "selection.json"
    predictions_path = output_dir / "validation_predictions.csv"
    lock_path = output_dir / "model_lock_manifest.json"

    metrics = pd.read_csv(metrics_path)
    selection = json.loads(selection_path.read_text(encoding="utf-8"))
    predictions = pd.read_csv(predictions_path)
    validation = pd.read_csv(data_dir / "validation.csv")

    incremental_false_safe = _false_safe_comparison(
        metrics,
        selection["best_cvt"],
        selection["best_simple_baseline"],
    )
    compression_false_safe = _false_safe_comparison(
        metrics,
        selection["best_cvt"],
        selection["best_native_baseline"],
    )

    incremental = selection["incremental_value"]
    incremental["passes_predictive_criteria"] = bool(incremental["passes"])
    incremental["false_safe_comparison"] = incremental_false_safe
    incremental["passes"] = bool(
        incremental["passes_predictive_criteria"] and incremental_false_safe["passes"]
    )

    compression = selection["predictive_compression"]
    compression["passes_predictive_criteria"] = bool(compression["passes"])
    compression["false_safe_comparison"] = compression_false_safe
    compression["passes"] = bool(
        compression["passes_predictive_criteria"] and compression_false_safe["passes"]
    )

    provisional_screens: dict[str, Any] = {}
    for row in metrics.itertuples(index=False):
        enough_count = int(row.high_confidence_count) >= 50
        enough_coverage = float(row.high_confidence_coverage) >= 0.05
        acceptable_false_safe = bool(
            enough_count
            and np.isfinite(row.high_confidence_false_safe)
            and float(row.high_confidence_false_safe) <= 0.10
        )
        provisional_screens[row.model] = {
            "minimum_count": enough_count,
            "minimum_coverage": enough_coverage,
            "maximum_false_safe_rate": acceptable_false_safe,
            "passes_validation_only_screen": bool(
                enough_count and enough_coverage and acceptable_false_safe
            ),
            "final_test_calibration_still_required": True,
        }
    selection["provisional_safety_screens"] = provisional_screens
    selection["portable_seal_passed"] = bool(seal_report["passed"])
    selection["final_test_opened"] = False
    selection_path.write_text(json.dumps(selection, indent=2), encoding="utf-8")

    joined = predictions.merge(
        validation[["row_id", "failure_reason"]],
        on="row_id",
        how="left",
        validate="one_to_one",
    )
    reason_rows: list[dict[str, Any]] = []
    prediction_columns = [
        column
        for column in predictions.columns
        if column not in {"row_id", "hosted", "forcing_family"}
    ]
    for model in prediction_columns:
        false_safe = joined[(joined[model] >= 0.80) & (~joined.hosted.astype(bool))]
        counts = false_safe.failure_reason.value_counts().sort_index()
        if len(counts) == 0:
            reason_rows.append({"model": model, "failure_reason": "none", "rows": 0})
        else:
            reason_rows.extend(
                {
                    "model": model,
                    "failure_reason": str(reason),
                    "rows": int(count),
                }
                for reason, count in counts.items()
            )
    false_safe_path = output_dir / "false_safe_reasons.csv"
    pd.DataFrame(reason_rows).to_csv(false_safe_path, index=False)

    lock = json.loads(lock_path.read_text(encoding="utf-8"))
    lock.update(
        {
            "portable_seal_version": seal_report["version"],
            "portable_seal_report_sha256": _sha256_file(
                output_dir / "portable_seal_report.json"
            ),
            "source_artifact_id": seal_report["source_artifact_id"],
            "source_artifact_digest": seal_report["source_artifact_digest"],
            "threshold_search": "bounded-memory exact frozen grid",
            "selection_sha256": _sha256_file(selection_path),
            "false_safe_reasons_sha256": _sha256_file(false_safe_path),
            "final_test_opened": False,
            "confirmatory_test_authorized": False,
        }
    )
    lock_path.write_text(json.dumps(lock, indent=2), encoding="utf-8")
    return selection


def run(
    data_dir: str | Path,
    output_dir: str | Path,
    seal_path: str | Path,
    bootstrap_resamples: int = 2000,
) -> dict[str, Any]:
    started = time.perf_counter()
    data = Path(data_dir)
    output = Path(output_dir)
    seal_report = verify_portable_seal(data, Path(seal_path), output)

    compare.HASHES = dict(seal_report["actual_hashes"])
    compare.verify = lambda _: None
    compare.threshold_tune = threshold_tune_bounded
    compare.run(data, output, bootstrap_resamples)
    selection = _postprocess_results(data, output, seal_report)

    execution = {
        "stage": "3.2",
        "elapsed_seconds": time.perf_counter() - started,
        "bootstrap_resamples": int(bootstrap_resamples),
        "portable_seal_passed": True,
        "validation_opened_once": True,
        "final_test_generated": False,
        "final_test_opened": False,
    }
    (output / "execution.json").write_text(
        json.dumps(execution, indent=2),
        encoding="utf-8",
    )
    return selection


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", default="results/stage3_1")
    parser.add_argument("--output", default="results/stage3_2")
    parser.add_argument(
        "--seal",
        default="config/stage32_portable_seal.json",
    )
    parser.add_argument("--bootstrap-resamples", type=int, default=2000)
    arguments = parser.parse_args()
    result = run(
        arguments.data,
        arguments.output,
        arguments.seal,
        arguments.bootstrap_resamples,
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
