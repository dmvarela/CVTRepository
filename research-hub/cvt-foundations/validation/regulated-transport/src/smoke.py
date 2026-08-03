from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from .accounting import accounting
from .model import InitialState, Parameters, SimulationConfig, simulate, with_sensitivity
from .outcomes import evaluate
from .schedules import Forcing, constant, pulse, ramp, repeated_pulse, shock_tail


def scenarios():
    base = Parameters()
    initial = InitialState(s=4.5, q=0.9)
    cfg = SimulationConfig()
    return [
        ("zero", constant(Forcing(0.0, 0.0)), base, initial, cfg),
        ("low_constant", constant(Forcing(1.5, 0.25)), base, initial, cfg),
        ("moderate_constant", constant(Forcing(4.0, 0.55)), base, initial, cfg),
        ("high_constant", constant(Forcing(9.0, 1.2)), base, initial, cfg),
        ("short_pulse", pulse(Forcing(8.0, 1.0), duration=3.0), base, initial, cfg),
        ("repeated_pulse", repeated_pulse(Forcing(6.0, 0.8)), base, initial, cfg),
        ("ramp", ramp(Forcing(7.0, 0.9)), base, initial, cfg),
        ("shock_tail", shock_tail(Forcing(10.0, 1.1)), base, initial, cfg),
        ("high_no_flux_damage", constant(Forcing(9.0, 1.2)), with_sensitivity(base, remove_flux_damage=True), initial, cfg),
        ("high_no_q_flux", constant(Forcing(9.0, 1.2)), with_sensitivity(base, remove_q_flux=True), initial, cfg),
    ]


def run(output: Path) -> pd.DataFrame:
    rows = []
    for name, schedule, params, initial, config in scenarios():
        result = simulate(schedule, params, initial, config)
        acc = accounting(result)
        outcome = evaluate(result)
        rows.append({
            "scenario": name,
            "solver_success": result.solver_success,
            "projection_count": result.projection_count,
            "accounting_valid": acc.valid,
            "accounting_residual": acc.residual,
            "delivered": acc.delivered,
            "productive": acc.productive,
            "rejected": acc.rejected,
            "buffer_terminal": result.u[-1],
            "free_terminal": result.c_a[-1],
            "target_reached": outcome.target_reached,
            "viable": outcome.viable,
            "hosted": outcome.hosted,
            "peak_damage": outcome.peak_damage,
            "minimum_integrity": outcome.minimum_integrity,
            "terminal_reserve": outcome.terminal_reserve,
        })
    frame = pd.DataFrame(rows)
    output.parent.mkdir(parents=True, exist_ok=True)
    frame.to_csv(output, index=False)
    return frame


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path("results/smoke_summary.csv"))
    args = parser.parse_args()
    print(run(args.output).to_string(index=False))


if __name__ == "__main__":
    main()
