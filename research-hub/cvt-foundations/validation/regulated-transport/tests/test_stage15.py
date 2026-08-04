from __future__ import annotations

import numpy as np

from src.accounting import accounting
from src.model import SimulationConfig, simulate
from src.schedules import Forcing, pulse, repeated_pulse
from src.verify_stage15 import cross_solver_table, randomized_property_table


def test_all_forcing_breakpoints_close_accounting() -> None:
    cases = [
        pulse(Forcing(8.0, 0.7), duration=2.731),
        repeated_pulse(
            Forcing(6.0, 0.55),
            duration=2.417,
            starts=(0.0, 6.3, 13.1),
        ),
    ]
    for schedule in cases:
        result = simulate(schedule)
        assert accounting(result).valid


def test_cross_solver_agreement() -> None:
    table = cross_solver_table()
    assert table.lsoda_accounting_valid.all()
    assert table.bdf_accounting_valid.all()
    assert table.max_scaled_trajectory_difference.max() < 1e-4
    assert table.max_scaled_terminal_difference.max() < 1e-5


def test_randomized_properties() -> None:
    table = randomized_property_table(n_runs=40)
    assert table.solver_success.all()
    assert table.accounting_valid.all()
    assert table.bounds_valid.all()
    assert table.productive_pool_monotone.all()
    assert table.residual_fraction_of_tolerance.max() < 1.0
