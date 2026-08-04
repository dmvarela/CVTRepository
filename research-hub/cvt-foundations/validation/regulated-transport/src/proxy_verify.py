from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import spearmanr

from .model import InitialState, Parameters, SimulationConfig
from .proxies import compute
from .schedules import Forcing, constant, pulse, ramp, repeated_pulse, shock_tail

SEED = 20260804
FAMILIES = ("constant", "pulse", "repeated_pulse", "ramp", "shock_tail")


def _schedule(name: str, amplitude: float, permeability: float):
    forcing = Forcing(amplitude, permeability)
    return {
        "constant": constant(forcing),
        "pulse": pulse(forcing, duration=3.0),
        "repeated_pulse": repeated_pulse(forcing),
        "ramp": ramp(forcing),
        "shock_tail": shock_tail(forcing),
    }[name]


def sample_rows(n: int = 300) -> pd.DataFrame:
    rng = np.random.default_rng(SEED)
    rows: list[dict[str, float | int | str]] = []
    for index in range(n):
        params = Parameters(
            p_cap=rng.uniform(5.0, 12.0),
            u_max=rng.uniform(2.0, 8.0),
            s_max=rng.uniform(3.0, 10.0),
            k_p=rng.uniform(0.4, 1.5),
            k_b=rng.uniform(0.2, 1.2),
            k_rel=rng.uniform(0.05, 0.5),
            k_e=rng.uniform(0.1, 1.0),
            h=rng.uniform(0.0, 1.0),
        )
        initial = InitialState(
            c_a=rng.uniform(0.0, 0.8),
            p=rng.uniform(0.0, 0.5 * params.p_cap),
            u=rng.uniform(0.0, 0.8 * params.u_max),
            d=rng.uniform(0.0, 0.35),
            s=rng.uniform(0.05, 1.0) * params.s_max,
            q=rng.uniform(0.35, 1.0),
        )
        family = FAMILIES[index % len(FAMILIES)]
        amplitude = rng.uniform(0.2, 8.0)
        permeability = rng.uniform(0.05, 1.5)
        proxies = compute(
            _schedule(family, amplitude, permeability),
            params,
            initial,
            SimulationConfig(),
        )
        rows.append(
            {
                "id": index,
                "family": family,
                "amplitude": amplitude,
                "permeability": permeability,
                "q0": initial.q,
                "s_fraction": initial.s / params.s_max,
                "p_headroom": 1.0 - initial.p / params.p_cap,
                "c_a0": initial.c_a,
                "u_fraction": initial.u / params.u_max,
                "d0": initial.d,
                **asdict(proxies),
            }
        )
    return pd.DataFrame(rows)


def variance_inflation_factors(data: pd.DataFrame, columns: list[str]) -> dict[str, float]:
    matrix = data[columns].to_numpy(float)
    result: dict[str, float] = {}
    for index, column in enumerate(columns):
        target = matrix[:, index]
        predictors = np.delete(matrix, index, axis=1)
        predictors = np.column_stack([np.ones(len(predictors)), predictors])
        beta = np.linalg.lstsq(predictors, target, rcond=None)[0]
        fitted = predictors @ beta
        residual_sum = float(np.sum((target - fitted) ** 2))
        total_sum = float(np.sum((target - np.mean(target)) ** 2))
        r_squared = 1.0 - residual_sum / total_sum if total_sum > 0.0 else 1.0
        result[column] = float(np.inf if r_squared >= 1.0 else 1.0 / (1.0 - r_squared))
    return result


def verify(output_dir: str | Path) -> dict[str, object]:
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    data = sample_rows()
    data.to_csv(output / "proxy_development.csv", index=False)

    columns = ["g_b", "g_q", "g_c_direct", "g_c_probe", "g_s"]
    correlation = data[columns].corr(method="spearman")
    correlation.to_csv(output / "proxy_spearman.csv")

    vifs = variance_inflation_factors(data, columns)
    (output / "proxy_vif.json").write_text(json.dumps(vifs, indent=2), encoding="utf-8")

    direct_probe = float(spearmanr(data.g_c_direct, data.g_c_probe).statistic)
    off_diagonal = correlation.to_numpy() - np.eye(len(columns))
    summary: dict[str, object] = {
        "n": len(data),
        "seed": SEED,
        "direct_probe_spearman": direct_probe,
        "max_abs_pairwise_spearman": float(np.max(np.abs(off_diagonal))),
        "vif": vifs,
        "near_duplicate_pairs": [
            (left, right, float(abs(correlation.loc[left, right])))
            for left_index, left in enumerate(columns)
            for right in columns[left_index + 1 :]
            if abs(correlation.loc[left, right]) >= 0.9
        ],
        "test_partition_opened": False,
        "outcome_used_in_proxy_construction": False,
    }
    (output / "proxy_summary.json").write_text(
        json.dumps(summary, indent=2),
        encoding="utf-8",
    )
    return summary


if __name__ == "__main__":
    print(json.dumps(verify("results/stage2"), indent=2))
