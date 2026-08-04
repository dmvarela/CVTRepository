from dataclasses import replace
import math

from src.model import InitialState, Parameters
from src.proxies import ProbeSpec, capture_probe


def test_sham_adjustment_removes_preexisting_productive_conversion() -> None:
    params = Parameters()
    initial = InitialState(c_a=0.6, u=2.0, p=1.0, s=4.0, q=0.8)
    measurement = capture_probe(params, initial)
    assert measurement.valid
    assert measurement.raw_ratio > 1.0
    assert 0.0 <= measurement.marginal_ratio <= 1.0
    assert measurement.sham_productive > 0.0


def test_primary_and_sensitivity_probes_are_nearly_dose_invariant() -> None:
    params = Parameters()
    initial = InitialState(c_a=0.2, u=1.0, p=1.5, s=4.5, q=0.75)
    primary = capture_probe(params, initial, ProbeSpec())
    sensitivity = capture_probe(params, initial, ProbeSpec().sensitivity())
    assert primary.valid and sensitivity.valid
    assert abs(primary.marginal_ratio - sensitivity.marginal_ratio) < 1e-4


def test_probe_is_monotone_in_q_s_and_capacity_headroom_for_reference_case() -> None:
    params = Parameters()
    base = InitialState(c_a=0.2, u=1.0, d=0.1, s=3.0, q=0.7, p=2.0)
    low_q = capture_probe(params, replace(base, q=0.4)).marginal_ratio
    high_q = capture_probe(params, replace(base, q=0.9)).marginal_ratio
    low_s = capture_probe(params, replace(base, s=0.5)).marginal_ratio
    high_s = capture_probe(params, replace(base, s=5.5)).marginal_ratio
    low_headroom = capture_probe(
        params,
        replace(base, p=0.9 * params.p_cap),
    ).marginal_ratio
    high_headroom = capture_probe(
        params,
        replace(base, p=0.1 * params.p_cap),
    ).marginal_ratio
    assert high_q > low_q
    assert high_s > low_s
    assert high_headroom > low_headroom


def test_probe_is_deterministic_and_initial_state_is_unchanged() -> None:
    params = Parameters()
    initial = InitialState(c_a=0.3, u=1.2, p=1.1, s=4.2, q=0.82)
    before = initial.as_array().copy()
    first = capture_probe(params, initial)
    second = capture_probe(params, initial)
    assert first == second
    assert (initial.as_array() == before).all()
    assert math.isfinite(first.score)
