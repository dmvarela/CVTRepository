from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.optimize import minimize
from scipy.special import expit, logit
from sklearn.metrics import average_precision_score, brier_score_loss, log_loss, roc_auc_score

C_VARIANTS = {
    "primary_micro_probe": "g_c_probe_sham_adjusted_primary",
    "dose_2_5x_micro_probe": "g_c_probe_sham_adjusted_2_5x_dose",
    "direct_structural_composite": "g_c_direct_structural_composite",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fit_map(z: np.ndarray, y: np.ndarray, positive: bool = True, l2: float = 1e-6) -> tuple[float, float]:
    z = np.asarray(z, float)
    y = np.asarray(y, float)
    p0 = float(np.clip(y.mean(), 1e-8, 1 - 1e-8))

    def objective_and_grad(v: np.ndarray) -> tuple[float, np.ndarray]:
        a, b = v
        eta = a + b * z
        p = expit(eta)
        residual = p - y
        objective = np.sum(np.logaddexp(0, eta) - y * eta) + 0.5 * l2 * (a * a + b * b)
        gradient = np.array([residual.sum() + l2 * a, np.dot(residual, z) + l2 * b])
        return float(objective), gradient

    result = minimize(
        lambda v: objective_and_grad(v)[0],
        [logit(p0), 1.0],
        jac=lambda v: objective_and_grad(v)[1],
        method="L-BFGS-B",
        bounds=[(None, None), (0, None)] if positive else None,
    )
    if not result.success:
        raise RuntimeError(str(result.message))
    return float(result.x[0]), float(result.x[1])


def metrics(y: np.ndarray, p: np.ndarray) -> dict[str, object]:
    y = np.asarray(y, int)
    p = np.asarray(p, float)
    z = logit(np.clip(p, 1e-8, 1 - 1e-8))
    calibration_intercept, calibration_slope = fit_map(z, y, positive=False, l2=1e-8)
    order = np.argsort(p)
    chunks = np.array_split(order, 10)
    ece = sum(len(chunk) / len(y) * abs(p[chunk].mean() - y[chunk].mean()) for chunk in chunks)

    def threshold_summary(threshold: float) -> dict[str, object]:
        mask = p >= threshold
        count = int(mask.sum())
        coverage = float(mask.mean())
        false_safe_rate = float(np.mean(y[mask] == 0)) if count else None
        return {
            "count": count,
            "coverage": coverage,
            "false_safe_rate": false_safe_rate,
            "informative": bool(count >= 50 and coverage >= 0.05),
        }

    return {
        "brier": float(brier_score_loss(y, p)),
        "log_loss": float(log_loss(y, p, labels=[0, 1])),
        "auroc": float(roc_auc_score(y, p)),
        "average_precision": float(average_precision_score(y, p)),
        "calibration_intercept": calibration_intercept,
        "calibration_slope": calibration_slope,
        "ece": float(ece),
        "high": threshold_summary(0.8),
        "ordinary": threshold_summary(0.5),
    }


def run(data_dir: Path, output_dir: Path) -> dict[str, object]:
    output_dir.mkdir(parents=True, exist_ok=True)
    training = pd.read_csv(data_dir / "training.csv")
    validation = pd.read_csv(data_dir / "validation.csv")
    calibration = training[training.training_subset == "calibration"].reset_index(drop=True)

    result: dict[str, object] = {
        "stage": "3.2.5",
        "method": (
            "fair refit of locked CVT-2-minimum scorer with each prespecified C alternative; "
            "calibration refit uses calibration subset only; validation evaluated once from the "
            "already-opened validation partition; final test unused"
        ),
        "training_sha256": sha256(data_dir / "training.csv"),
        "validation_sha256": sha256(data_dir / "validation.csv"),
        "variants": {},
        "final_test_generated": False,
        "final_test_opened": False,
        "confirmatory_test_authorized": False,
    }

    for label, c_column in C_VARIANTS.items():
        columns = ["g_b", "g_q", c_column, "g_s"]
        calibration_score = calibration[columns].min(axis=1).to_numpy(float)
        intercept, slope = fit_map(calibration_score, calibration.hosted.to_numpy(int), positive=True)
        validation_score = validation[columns].min(axis=1).to_numpy(float)
        prediction = expit(intercept + slope * validation_score)
        variant_metrics = metrics(validation.hosted.to_numpy(int), prediction)
        result["variants"][label] = {
            "c_column": c_column,
            "score": "minimum(g_b,g_q,c,g_s)",
            "calibration_intercept": intercept,
            "calibration_slope": slope,
            **variant_metrics,
        }

    primary_brier = result["variants"]["primary_micro_probe"]["brier"]
    for variant in result["variants"].values():
        variant["brier_minus_primary"] = float(variant["brier"] - primary_brier)
    result["ranking_by_brier"] = sorted(
        [[name, data["brier"]] for name, data in result["variants"].items()],
        key=lambda row: row[1],
    )

    (output_dir / "capture_proxy_sensitivity_refit.json").write_text(json.dumps(result, indent=2))
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", default="results/stage3_1")
    parser.add_argument("--output", default="results/stage3_2_5")
    args = parser.parse_args()
    print(json.dumps(run(Path(args.data), Path(args.output)), indent=2))


if __name__ == "__main__":
    main()
