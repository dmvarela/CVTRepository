import numpy as np

from src.accounting import accounting
from src.model import InitialState, Parameters, SimulationConfig, simulate
from src.schedules import Forcing, constant, repeated_pulse


def test_zero_forcing_preserves_transport_mass_and_no_productive_growth():
    result = simulate(constant(Forcing(0.0, 0.0)))
    acc = accounting(result)
    assert result.solver_success
    assert acc.valid
    assert acc.delivered == 0.0
    assert np.isclose(result.p[-1], result.p[0], atol=1e-10)
    assert np.all(result.c_a >= -1e-12)
    assert np.all(result.u >= -1e-12)


def test_mass_accounting_closes_under_constant_forcing():
    result = simulate(constant(Forcing(5.0, 0.7)))
    acc = accounting(result)
    assert result.solver_success
    assert acc.valid, (acc.residual, acc.tolerance)


def test_states_respect_hard_bounds():
    params = Parameters()
    result = simulate(constant(Forcing(12.0, 1.5)), params, InitialState(s=0.4, q=0.45, d=0.2))
    assert np.all(result.c_a >= -1e-10)
    assert np.all(result.p >= -1e-10)
    assert np.all((result.u >= -1e-10) & (result.u <= params.u_max + 1e-10))
    assert np.all((result.d >= -1e-10) & (result.d <= 1.0 + 1e-10))
    assert np.all((result.s >= -1e-10) & (result.s <= params.s_max + 1e-10))
    assert np.all((result.q >= -1e-10) & (result.q <= 1.0 + 1e-10))


def test_productive_pool_is_monotone():
    result = simulate(repeated_pulse(Forcing(6.0, 0.8)))
    assert np.all(np.diff(result.p) >= -1e-9)


def test_reproducibility_is_exact_for_deterministic_run():
    schedule = constant(Forcing(4.0, 0.5))
    first = simulate(schedule)
    second = simulate(schedule)
    assert np.array_equal(first.t, second.t)
    assert np.allclose(first.y, second.y, rtol=0.0, atol=0.0)


def test_output_step_refinement_is_stable():
    schedule = constant(Forcing(6.0, 0.8))
    coarse = simulate(schedule, config=SimulationConfig(dt_out=0.1))
    fine = simulate(schedule, config=SimulationConfig(dt_out=0.025))
    assert np.allclose(coarse.y[:, -1], fine.y[:, -1], rtol=2e-4, atol=2e-6)
