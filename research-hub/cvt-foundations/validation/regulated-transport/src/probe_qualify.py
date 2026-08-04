from __future__ import annotations

import argparse
import itertools
import json
from dataclasses import asdict, replace
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import spearmanr

from .model import InitialState, Parameters
from .proxies import ProbeSpec, capture_probe

SEED = 20260804
PRIMARY = ProbeSpec()
SENSITIVITY = PRIMARY.sensitivity()


def development_cases(n: int, seed: int = SEED) -> list[tuple[int, Parameters, InitialState]]:
    rng = np.random.default_rng(seed)
    cases: list[tuple[int, Parameters, InitialState]] = []
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
        cases.append((index, params, initial))
    return cases


def measurement_row(
    index: int,
    label: str,
    params: Parameters,
    initial: InitialState,
    spec: ProbeSpec,
) -> dict[str, object]:
    measurement = capture_probe(params, initial, spec)
    return {
        "id": index,
        "probe": label,
        "q0": initial.q,
        "s_fraction": initial.s / params.s_max,
        "capacity_headroom": 1.0 - initial.p / params.p_cap,
        "c_a0": initial.c_a,
        "u_fraction": initial.u / params.u_max,
        "d0": initial.d,
        "delivered_fraction_pcap": measurement.delivered / params.p_cap,
        "incremental_p_fraction_pcap": measurement.incremental_p / params.p_cap,
        "incremental_s_fraction_smax": measurement.incremental_s / params.s_max,
        **asdict(measurement),
    }


def candidate_sweep(cases: list[tuple[int, Parameters, InitialState]]) -> pd.DataFrame:
    specs = [
        ProbeSpec(
            c_b=2.0,
            permeability=permeability,
            pulse_duration=pulse,
            readout_horizon=readout,
        )
        for permeability, pulse, readout in itertools.product(
            (0.05, 0.10, 0.25),
            (0.05, 0.10),
            (0.5, 1.0),
        )
    ]
    rows: list[dict[str, object]] = []
    for spec in specs:
        label = (
            f"cb{spec.c_b:g}_pi{spec.permeability:g}_"
            f"pulse{spec.pulse_duration:g}_read{spec.readout_horizon:g}"
        )
        measurements = [
            measurement_row(index, label, params, initial, spec)
            for index, params, initial in cases
        ]
        data = pd.DataFrame(measurements)
        finite = data[np.isfinite(data.marginal_ratio)]
        rows.append(
            {
                "probe": label,
                "n": len(data),
                "valid_fraction": float(data.valid.mean()),
                "delivered_fraction_p95": float(
                    data.delivered_fraction_pcap.quantile(0.95)
                ),
                "marginal_ratio_median": float(finite.marginal_ratio.median()),
                "marginal_ratio_iqr": float(
                    finite.marginal_ratio.quantile(0.75)
                    - finite.marginal_ratio.quantile(0.25)
                ),
                "raw_ratio_fraction_gt_one": float((finite.raw_ratio > 1.0).mean()),
                "incremental_p_fraction_p95": float(
                    finite.incremental_p_fraction_pcap.abs().quantile(0.95)
                ),
                "incremental_damage_p95": float(
                    finite.incremental_d.abs().quantile(0.95)
                ),
                "incremental_reserve_fraction_p95": float(
                    finite.incremental_s_fraction_smax.abs().quantile(0.95)
                ),
                "incremental_integrity_p95": float(
                    finite.incremental_q.abs().quantile(0.95)
                ),
            }
        )
    return pd.DataFrame(rows)


def primary_audit(
    cases: list[tuple[int, Parameters, InitialState]],
) -> tuple[pd.DataFrame, dict[str, object]]:
    rows: list[dict[str, object]] = []
    for index, params, initial in cases:
        rows.append(measurement_row(index, "primary", params, initial, PRIMARY))
        rows.append(
            measurement_row(index, "sensitivity", params, initial, SENSITIVITY)
        )
    data = pd.DataFrame(rows)
    pivot = data.pivot(index="id", columns="probe", values="marginal_ratio")
    summary: dict[str, object] = {
        "n_cases": len(cases),
        "seed": SEED,
        "primary_spec": asdict(PRIMARY),
        "sensitivity_spec": asdict(SENSITIVITY),
        "primary_sensitivity_spearman": float(
            spearmanr(pivot.primary, pivot.sensitivity, nan_policy="omit").statistic
        ),
        "primary_sensitivity_max_abs_difference": float(
            np.nanmax(np.abs(pivot.primary - pivot.sensitivity))
        ),
        "test_partition_opened": False,
        "outcome_used": False,
    }
    for label, group in data.groupby("probe"):
        finite = group[np.isfinite(group.marginal_ratio)]
        summary[label] = {
            "valid_fraction": float(group.valid.mean()),
            "delivered_floor_margin_min": float(
                np.min(finite.delivered / finite.delivered_floor)
            ),
            "delivered_fraction_p95": float(
                finite.delivered_fraction_pcap.quantile(0.95)
            ),
            "marginal_ratio_median": float(finite.marginal_ratio.median()),
            "marginal_ratio_iqr": float(
                finite.marginal_ratio.quantile(0.75)
                - finite.marginal_ratio.quantile(0.25)
            ),
            "fraction_negative": float((finite.marginal_ratio < 0.0).mean()),
            "fraction_gt_one": float((finite.marginal_ratio > 1.0).mean()),
            "raw_ratio_fraction_gt_one": float((finite.raw_ratio > 1.0).mean()),
            "raw_ratio_median": float(finite.raw_ratio.median()),
            "rho_q": float(spearmanr(finite.marginal_ratio, finite.q0).statistic),
            "rho_s": float(
                spearmanr(finite.marginal_ratio, finite.s_fraction).statistic
            ),
            "rho_headroom": float(
                spearmanr(
                    finite.marginal_ratio,
                    finite.capacity_headroom,
                ).statistic
            ),
            "incremental_p_fraction_p95": float(
                finite.incremental_p_fraction_pcap.abs().quantile(0.95)
            ),
            "incremental_damage_p95": float(
                finite.incremental_d.abs().quantile(0.95)
            ),
            "incremental_reserve_fraction_p95": float(
                finite.incremental_s_fraction_smax.abs().quantile(0.95)
            ),
            "incremental_integrity_p95": float(
                finite.incremental_q.abs().quantile(0.95)
            ),
        }
    return data, summary


def monotonicity_audit(
    cases: list[tuple[int, Parameters, InitialState]],
) -> dict[str, object]:
    grids = {
        "q": np.linspace(0.35, 1.0, 6),
        "s": np.linspace(0.05, 0.95, 6),
        "headroom": np.linspace(0.10, 0.95, 6),
    }
    summary: dict[str, object] = {}
    for variable, grid in grids.items():
        nondecreasing = 0
        strictly_increasing = 0
        worst_step = 0.0
        for _, params, initial in cases:
            values: list[float] = []
            for value in grid:
                if variable == "q":
                    perturbed = replace(initial, q=float(value))
                elif variable == "s":
                    perturbed = replace(
                        initial,
                        s=float(value * params.s_max),
                    )
                else:
                    perturbed = replace(
                        initial,
                        p=float((1.0 - value) * params.p_cap),
                    )
                values.append(
                    capture_probe(params, perturbed, PRIMARY).marginal_ratio
                )
            differences = np.diff(values)
            worst_step = min(worst_step, float(np.min(differences)))
            nondecreasing += int(np.all(differences >= -1e-7))
            strictly_increasing += int(np.all(differences > 0.0))
        summary[variable] = {
            "nondecreasing_fraction": nondecreasing / len(cases),
            "strictly_increasing_fraction": strictly_increasing / len(cases),
            "worst_step": worst_step,
        }

    descriptive_grids = {
        "c_a_descriptive": np.linspace(0.0, 0.8, 6),
        "u_descriptive": np.linspace(0.0, 0.8, 6),
    }
    for variable, grid in descriptive_grids.items():
        correlations: list[float] = []
        for _, params, initial in cases:
            values: list[float] = []
            for value in grid:
                if variable == "c_a_descriptive":
                    perturbed = replace(initial, c_a=float(value))
                else:
                    perturbed = replace(initial, u=float(value * params.u_max))
                values.append(
                    capture_probe(params, perturbed, PRIMARY).marginal_ratio
                )
            correlations.append(float(np.corrcoef(grid, values)[0, 1]))
        correlation_array = np.asarray(correlations)
        summary[variable] = {
            "median_linear_correlation": float(np.nanmedian(correlation_array)),
            "positive_fraction": float(np.mean(correlation_array > 0.0)),
        }

    repeatability: list[tuple[float, float, float]] = []
    for _, params, initial in cases[:20]:
        reference = capture_probe(params, initial, PRIMARY)
        repeated = capture_probe(params, initial, PRIMARY)
        bdf = capture_probe(params, initial, PRIMARY, method="BDF")
        tight = capture_probe(
            params,
            initial,
            PRIMARY,
            rtol=1e-10,
            atol=1e-12,
        )
        repeatability.append(
            (
                abs(reference.marginal_ratio - repeated.marginal_ratio),
                abs(reference.marginal_ratio - bdf.marginal_ratio),
                abs(reference.marginal_ratio - tight.marginal_ratio),
            )
        )
    differences = np.asarray(repeatability)
    summary["repeatability"] = {
        "exact_repeat_max_abs": float(differences[:, 0].max()),
        "bdf_max_abs": float(differences[:, 1].max()),
        "tight_tolerance_max_abs": float(differences[:, 2].max()),
    }
    summary["test_partition_opened"] = False
    return summary


def run(output_dir: str | Path, *, quick: bool = False) -> dict[str, object]:
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    candidate_cases = development_cases(10 if quick else 50)
    primary_cases = development_cases(20 if quick else 300)
    monotonic_cases = development_cases(5 if quick else 30, seed=SEED + 1)

    candidates = candidate_sweep(candidate_cases)
    candidates.to_csv(output / "probe_candidate_summary.csv", index=False)

    primary_data, primary_summary = primary_audit(primary_cases)
    primary_data.to_csv(output / "probe_primary_development.csv", index=False)
    (output / "probe_primary_summary.json").write_text(
        json.dumps(primary_summary, indent=2),
        encoding="utf-8",
    )

    monotonic_summary = monotonicity_audit(monotonic_cases)
    (output / "probe_monotonicity_summary.json").write_text(
        json.dumps(monotonic_summary, indent=2),
        encoding="utf-8",
    )
    return {
        "primary": primary_summary,
        "monotonicity": monotonic_summary,
        "candidate_count": len(candidates),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="results/stage2_5")
    parser.add_argument("--quick", action="store_true")
    args = parser.parse_args()
    print(json.dumps(run(args.output, quick=args.quick), indent=2))


if __name__ == "__main__":
    main()
