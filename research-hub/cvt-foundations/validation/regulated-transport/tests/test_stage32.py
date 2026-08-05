import numpy as np
import pandas as pd

from src.stage32_compare import fit_map, gates, pairwise, softmin


def test_scalar_calibrator_keeps_nonnegative_orientation() -> None:
    score = np.linspace(0.0, 1.0, 100)
    outcome = (score > 0.65).astype(int)
    _, slope = fit_map(score, outcome, positive=True)
    assert slope >= 0.0


def test_gate_and_pairwise_shapes() -> None:
    frame = pd.DataFrame(
        {
            "g_b": [0.2, 0.8],
            "g_q": [0.3, 0.9],
            "g_c_probe_sham_adjusted_primary": [0.4, 0.7],
            "g_s": [0.5, 0.6],
        }
    )
    primary = gates(frame)
    expanded = pairwise(primary)
    assert primary.shape == (2, 4)
    assert expanded.shape == (2, 10)


def test_softmin_approaches_minimum_from_above() -> None:
    values = np.array([[0.2, 0.4, 0.6, 0.8], [0.7, 0.7, 0.7, 0.7]])
    tau = 0.1
    score = softmin(values, tau)
    minimum = np.min(values, axis=1)
    assert np.all(score >= minimum - 1e-12)
    assert np.all(score <= minimum + tau * np.log(values.shape[1]) + 1e-12)
