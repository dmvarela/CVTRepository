import json
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.model_selection import StratifiedKFold

from src.stage32_runner import (
    _design_hash_digest,
    _identity_digest,
    _outcome_digest,
    _rounded_gate_digest,
    _sha256_file,
    threshold_tune_bounded,
    verify_portable_seal,
)

GATE_COLUMNS = [
    "g_b",
    "g_q",
    "g_c_probe_sham_adjusted_primary",
    "g_s",
    "g_c_probe_sham_adjusted_2_5x_dose",
    "g_c_direct_structural_composite",
]


def _frame(partition: str) -> pd.DataFrame:
    rows = 3
    frame = pd.DataFrame(
        {
            "partition": [partition] * rows,
            "partition_index": np.arange(rows),
            "row_id": [f"{partition}-{index}" for index in range(rows)],
            "design_hash": [f"design-{partition}-{index}" for index in range(rows)],
            "forcing_family": ["constant", "pulse", "ramp"],
            "forcing_stratum": ["low", "middle", "high"],
            "target_reached": [False, True, True],
            "viable": [True, True, False],
            "hosted": [False, True, False],
            "failure_reason": ["target_not_reached", "hosted", "damage_violation"],
            "probe_valid": [True] * rows,
            "sensitivity_probe_valid": [True] * rows,
            "solver_success": [True] * rows,
            "accounting_valid": [True] * rows,
            "bounds_valid": [True] * rows,
            "productive_pool_monotone": [True] * rows,
            "g_b": [0.2, 0.6, 0.9],
            "g_q": [0.5, 0.7, 0.8],
            "g_c_probe_sham_adjusted_primary": [0.1, 0.4, 0.7],
            "g_s": [0.3, 0.8, 0.6],
            "g_c_probe_sham_adjusted_2_5x_dose": [0.11, 0.41, 0.71],
            "g_c_direct_structural_composite": [0.4, 0.5, 0.6],
        }
    )
    if partition == "training":
        frame["training_subset"] = ["fit", "fit", "calibration"]
    return frame


def test_portable_seal_accepts_frozen_evidence(tmp_path: Path) -> None:
    data_dir = tmp_path / "data"
    output_dir = tmp_path / "output"
    data_dir.mkdir()
    (data_dir / "stage31_manifest.json").write_text(
        json.dumps(
            {
                "test_partition_generated": False,
                "test_partition_opened": False,
            }
        ),
        encoding="utf-8",
    )

    partitions = {}
    for partition in ("training", "validation"):
        frame = _frame(partition)
        path = data_dir / f"{partition}.csv"
        frame.to_csv(path, index=False)
        partitions[partition] = {
            "rows": len(frame),
            "file_sha256": _sha256_file(path),
            "design_hash_sha256": _design_hash_digest(frame),
            "identity_digest": _identity_digest(frame),
            "outcome_digest": _outcome_digest(frame),
            "rounded_gate_digest": _rounded_gate_digest(frame, GATE_COLUMNS, 5),
            "hosted_count": int(frame.hosted.sum()),
            "target_reached_count": int(frame.target_reached.sum()),
            "viable_count": int(frame.viable.sum()),
            "failure_reason_counts": {
                str(key): int(value)
                for key, value in frame.failure_reason.value_counts().sort_index().items()
            },
        }

    seal_path = tmp_path / "seal.json"
    seal_path.write_text(
        json.dumps(
            {
                "version": "test",
                "source_workflow_run": 1,
                "source_artifact_id": 2,
                "source_artifact_digest": "sha256:test",
                "gate_columns": GATE_COLUMNS,
                "gate_round_decimals": 5,
                "partitions": partitions,
            }
        ),
        encoding="utf-8",
    )

    report = verify_portable_seal(data_dir, seal_path, output_dir)
    assert report["passed"] is True
    assert set(report["actual_hashes"]) == {"training.csv", "validation.csv"}
    assert (output_dir / "portable_seal_report.json").exists()


def test_bounded_threshold_search_returns_frozen_grid_candidate() -> None:
    rng = np.random.default_rng(20260805)
    x = rng.uniform(0.0, 1.0, size=(120, 4))
    y = ((x[:, 0] > 0.45) & (x[:, 1] > 0.40)).astype(int)
    folds = list(
        StratifiedKFold(3, shuffle=True, random_state=7).split(
            np.zeros(len(y)),
            y,
        )
    )
    thresholds, score, count = threshold_tune_bounded(
        x,
        y,
        folds,
        chunk_size=32,
    )
    assert thresholds.shape == (4,)
    assert np.isfinite(score)
    assert count == 9**4
