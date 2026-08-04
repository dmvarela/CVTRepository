from __future__ import annotations

from dataclasses import asdict
from pathlib import Path

import numpy as np
import pandas as pd

from .accounting import accounting
from .model import InitialState, Parameters, SimulationConfig, simulate
from .schedules import Forcing, constant, pulse, ramp, repeated_pulse, shock_tail

MASTER_SEED = 20260804


def representative_scenarios():
    return {
        "moderate_constant": constant(Forcing(4.0, 0.35)),
        "high_constant": constant(Forcing(8.0, 0.70)),
        "short_pulse": pulse(Forcing(8.0, 0.70), duration=3.0),
        "repeated_pulse": repeated_pulse(Forcing(6.0, 0.55)),
        "ramp": ramp(Forcing(8.0, 0.60)),
        "shock_tail": shock_tail(Forcing(10.0, 0.80)),
    }


def cross_solver_table() -> pd.DataFrame:
    rows = []
    for name, schedule in representative_scenarios().items():
        lsoda = simulate(schedule, config=SimulationConfig(method="LSODA"))
        bdf = simulate(schedule, config=SimulationConfig(method="BDF"))
        scale = np.maximum(1.0, np.max(np.abs(lsoda.y), axis=1))
        trajectory_difference = float(
            np.max(np.abs(lsoda.y - bdf.y) / scale[:, None])
        )
        terminal_difference = float(
            np.max(np.abs(lsoda.y[:, -1] - bdf.y[:, -1]) / scale)
        )
        rows.append(
            {
                "scenario": name,
                "max_scaled_trajectory_difference": trajectory_difference,
                "max_scaled_terminal_difference": terminal_difference,
                "lsoda_projection_count": lsoda.projection_count,
                "bdf_projection_count": bdf.projection_count,
                "lsoda_accounting_valid": accounting(lsoda).valid,
                "bdf_accounting_valid": accounting(bdf).valid,
            }
        )
    return pd.DataFrame(rows)


def _sample_case(rng: np.random.Generator, run_id: int):
    params = Parameters(
        p_cap=rng.uniform(5.0, 12.0),
        u_max=rng.uniform(2.0, 8.0),
        k_p=rng.uniform(0.4, 1.5),
        k_b=rng.uniform(0.2, 1.2),
        k_rel=rng.uniform(0.05, 0.5),
        k_e=rng.uniform(0.1, 1.0),
        s_max=rng.uniform(3.0, 10.0),
        r_s=rng.uniform(0.01, 0.15),
        k_rep=rng.uniform(0.05, 0.5),
        r_q=rng.uniform(0.01, 0.15),
        c_safe=rng.uniform(0.5, 2.0),
        u_safe=rng.uniform(1.5, 5.5),
        c_q=rng.uniform(1.0, 3.0),
        j_safe=rng.uniform(0.5, 3.0),
        h=rng.uniform(0.0, 1.0),
    )
    initial = InitialState(
        c_a=rng.uniform(0.0, 0.5),
        u=rng.uniform(0.0, 0.8 * params.u_max),
        d=rng.uniform(0.0, 0.35),
        s=rng.uniform(0.05, 1.0) * params.s_max,
        q=rng.uniform(0.35, 1.0),
    )
    forcing = Forcing(rng.uniform(0.5, 10.0), rng.uniform(0.05, 1.0))
    family = run_id % 5
    if family == 0:
        schedule = constant(forcing)
        family_name = "constant"
    elif family == 1:
        schedule = pulse(forcing, duration=rng.uniform(2.0, 5.0))
        family_name = "pulse"
    elif family == 2:
        schedule = repeated_pulse(forcing, duration=rng.uniform(1.5, 4.0))
        family_name = "repeated_pulse"
    elif family == 3:
        schedule = ramp(forcing)
        family_name = "ramp"
    else:
        schedule = shock_tail(
            forcing,
            shock_duration=rng.uniform(1.0, 3.0),
            tail_fraction=rng.uniform(0.2, 0.6),
        )
        family_name = "shock_tail"
    return params, initial, schedule, family_name


def randomized_property_table(n_runs: int = 120) -> pd.DataFrame:
    rng = np.random.default_rng(MASTER_SEED)
    rows = []
    for run_id in range(n_runs):
        params, initial, schedule, family_name = _sample_case(rng, run_id)
        result = simulate(schedule, params=params, initial=initial)
        acc = accounting(result)
        bounds_valid = bool(
            result.c_a.min() >= -1e-10
            and result.u.min() >= -1e-10
            and result.u.max() <= params.u_max + 1e-8
            and result.d.min() >= -1e-10
            and result.d.max() <= 1.0 + 1e-8
            and result.s.min() >= -1e-10
            and result.s.max() <= params.s_max + 1e-8
            and result.q.min() >= -1e-10
            and result.q.max() <= 1.0 + 1e-8
        )
        rows.append(
            {
                "run_id": run_id,
                "family": family_name,
                "solver_success": result.solver_success,
                "accounting_valid": acc.valid,
                "accounting_residual": acc.residual,
                "accounting_tolerance": acc.tolerance,
                "residual_fraction_of_tolerance": abs(acc.residual) / acc.tolerance,
                "bounds_valid": bounds_valid,
                "productive_pool_monotone": bool(np.all(np.diff(result.p) >= -1e-9)),
                "projection_count": result.projection_count,
            }
        )
    return pd.DataFrame(rows)


def main(output_dir: str = "results/stage15") -> None:
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    cross = cross_solver_table()
    random_table = randomized_property_table()
    cross.to_csv(output / "cross_solver.csv", index=False)
    random_table.to_csv(output / "randomized_properties.csv", index=False)
    summary = pd.DataFrame(
        [
            {
                "randomized_runs": len(random_table),
                "successful_integrations": int(random_table.solver_success.sum()),
                "accounting_passes": int(random_table.accounting_valid.sum()),
                "bound_passes": int(random_table.bounds_valid.sum()),
                "monotonicity_passes": int(random_table.productive_pool_monotone.sum()),
                "projection_positive_runs": int((random_table.projection_count > 0).sum()),
                "projection_over_500_runs": int((random_table.projection_count > 500).sum()),
                "maximum_residual_fraction_of_tolerance": float(
                    random_table.residual_fraction_of_tolerance.max()
                ),
                "maximum_cross_solver_trajectory_difference": float(
                    cross.max_scaled_trajectory_difference.max()
                ),
                "maximum_cross_solver_terminal_difference": float(
                    cross.max_scaled_terminal_difference.max()
                ),
            }
        ]
    )
    summary.to_csv(output / "summary.csv", index=False)


if __name__ == "__main__":
    main()
