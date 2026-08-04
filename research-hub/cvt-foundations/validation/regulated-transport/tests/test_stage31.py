from pathlib import Path

import pandas as pd
import pytest

from src.stage31_dataset import design_rows, run


def test_final_test_generation_is_inaccessible() -> None:
    with pytest.raises(ValueError):
        design_rows("test", 10)


def test_design_is_deterministic_and_disjoint() -> None:
    first = design_rows("training", 24)
    second = design_rows("training", 24)
    validation = design_rows("validation", 24)
    assert first == second
    assert {row["design_hash"] for row in first}.isdisjoint(
        {row["design_hash"] for row in validation}
    )


def test_quick_generation_and_integrity(tmp_path: Path) -> None:
    summary = run(tmp_path, training_n=24, validation_n=12, workers=1)
    assert summary["test_partition_opened"] is False
    assert summary["candidate_model_fitted"] is False
    assert summary["training_validation_design_overlap"] == 0
    assert summary["solver_success_fraction"] == 1.0
    assert summary["accounting_valid_fraction"] == 1.0
    assert (tmp_path / "stage31_manifest.json").exists()
    assert len(pd.read_csv(tmp_path / "training.csv")) == 24


def test_combined_probe_matches_reference() -> None:
    from src.model import InitialState, Parameters
    from src.probe_pair import capture_probe_pair_combined
    from src.proxies import ProbeSpec, capture_probe

    params = Parameters()
    initial = InitialState(c_a=0.2, p=0.3, u=0.4, d=0.1, s=4.0, q=0.8)
    primary, sensitivity = capture_probe_pair_combined(params, initial)
    primary_reference = capture_probe(params, initial, ProbeSpec(), method="BDF")
    sensitivity_reference = capture_probe(
        params,
        initial,
        ProbeSpec().sensitivity(),
        method="BDF",
    )
    assert abs(primary.score - primary_reference.score) < 1e-5
    assert abs(sensitivity.score - sensitivity_reference.score) < 1e-5
