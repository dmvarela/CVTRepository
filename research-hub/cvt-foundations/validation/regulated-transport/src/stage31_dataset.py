from __future__ import annotations

import argparse
import hashlib
import json
import math
import signal
from contextlib import contextmanager
from dataclasses import asdict, fields
from multiprocessing import Pool
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import scipy
from scipy.stats import qmc

from .accounting import accounting, accounting_refined
from .model import InitialState, Parameters, SimulationConfig, simulate
from .outcomes import Thresholds, evaluate
from .probe_pair import capture_probe_pair_combined
from .proxies import ProbeSpec, ProxyConfig, bounded_coupling, capture_direct, scheduled_peak
from .schedules import Forcing, constant, pulse, ramp, shock_tail


class Stage31Timeout(RuntimeError):
    pass


@contextmanager
def _time_limit(seconds: float):
    if not hasattr(signal, "setitimer"):
        yield
        return
    previous_handler = signal.getsignal(signal.SIGALRM)

    def handler(signum, frame):
        del signum, frame
        raise Stage31Timeout(f"operation exceeded {seconds} seconds")

    signal.signal(signal.SIGALRM, handler)
    signal.setitimer(signal.ITIMER_REAL, seconds)
    try:
        yield
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0.0)
        signal.signal(signal.SIGALRM, previous_handler)


VERSION = "stage3.1-data-1.0"
MASTER_SEED = 20260803
PARTITIONS = {"training": 12000, "validation": 4000}
PARTITION_SEEDS = {"training": MASTER_SEED, "validation": MASTER_SEED + 1}
FAMILIES = ("constant", "pulse", "ramp", "shock_tail")
FORCING_STRATA = ("low", "middle", "high")

UNIFORM_RANGES: dict[str, tuple[float, float]] = {
    "p_cap": (5.0, 12.0),
    "u_max": (2.0, 8.0),
    "k_p": (0.4, 1.5),
    "k_b": (0.2, 1.2),
    "k_rel": (0.05, 0.5),
    "k_e": (0.1, 1.0),
    "s_max": (3.0, 10.0),
    "r_s": (0.01, 0.15),
    "k_rep": (0.05, 0.5),
    "r_q": (0.01, 0.15),
    "c_safe": (0.5, 2.0),
    "u_safe_fraction": (0.35, 0.90),
    "c_q": (1.0, 3.0),
    "j_safe": (0.5, 3.0),
    "h": (0.0, 1.0),
    "c_a0": (0.0, 0.8),
    "p_fraction0": (0.0, 0.5),
    "u_fraction0": (0.0, 0.8),
    "d0": (0.0, 0.35),
    "s_fraction0": (0.05, 1.0),
    "q0": (0.35, 1.0),
    "permeability": (0.05, 1.0),
    "pulse_duration": (2.0, 5.0),
    "shock_duration": (1.0, 3.0),
    "tail_fraction": (0.2, 0.6),
}

LOG_FACTOR_DEFAULTS: dict[str, float] = {
    "k_s": 1.0,
    "k_q": 0.5,
    "s_export": 1.5,
    "k_rep_half": 1.0,
    "k_qs": 1.0,
    "k_d1": 0.10,
    "k_d2": 0.08,
    "k_d3": 0.04,
    "a_p": 0.06,
    "a_e": 0.04,
    "a_b": 0.03,
    "a_r": 0.08,
    "b_d": 0.12,
    "b_l": 0.08,
}

AMPLITUDE_RANGES = {
    "low": (0.5, 2.5),
    "middle": (2.5, 6.0),
    "high": (6.0, 10.0),
}

DESIGN_DIMENSIONS = tuple(UNIFORM_RANGES) + tuple(LOG_FACTOR_DEFAULTS) + ("amplitude_unit",)


def _scale(value: float, low: float, high: float) -> float:
    return low + value * (high - low)


def _log_factor(value: float, default: float) -> float:
    low = math.log(default / 3.0)
    high = math.log(default * 3.0)
    return math.exp(_scale(value, low, high))


def _canonical_hash(payload: dict[str, Any]) -> str:
    encoded = json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _schedule_and_descriptors(row: dict[str, Any], initial: InitialState):
    amplitude = float(row["amplitude"])
    permeability = float(row["permeability"])
    forcing = Forcing(amplitude, permeability)
    family = str(row["forcing_family"])
    pulse_duration = float(row["pulse_duration"])
    shock_duration = float(row["shock_duration"])
    tail_fraction = float(row["tail_fraction"])

    if family == "constant":
        schedule = constant(forcing)
        active_duration = 20.0
        pulse_count = 1
        dose = 20.0 * permeability * max(0.0, amplitude - initial.c_a)
    elif family == "pulse":
        schedule = pulse(forcing, duration=pulse_duration)
        active_duration = pulse_duration
        pulse_count = 1
        dose = pulse_duration * permeability * max(0.0, amplitude - initial.c_a)
    elif family == "ramp":
        schedule = ramp(forcing)
        active_duration = 20.0
        pulse_count = 1
        if amplitude <= initial.c_a:
            dose = 0.0
        else:
            onset = 20.0 * initial.c_a / amplitude
            dose = permeability * (
                amplitude * (20.0**2 - onset**2) / 40.0
                - initial.c_a * (20.0 - onset)
            )
    elif family == "shock_tail":
        schedule = shock_tail(
            forcing,
            shock_duration=shock_duration,
            tail_fraction=tail_fraction,
        )
        active_duration = 20.0
        pulse_count = 1
        shock_flux = permeability * max(0.0, amplitude - initial.c_a)
        tail_flux = permeability * max(0.0, amplitude * tail_fraction - initial.c_a)
        dose = shock_duration * shock_flux + (20.0 - shock_duration) * tail_flux
    else:
        raise ValueError(f"Unsupported Stage 3.1 family: {family}")

    peak_intact_flux = permeability * max(0.0, amplitude - initial.c_a)
    descriptors = {
        "peak_source_concentration": amplitude,
        "peak_permeability": permeability,
        "active_duration": active_duration,
        "pulse_count": pulse_count,
        "scheduled_peak_intact_flux": peak_intact_flux,
        "scheduled_intact_dose": float(max(0.0, dose)),
    }
    return schedule, descriptors


def design_rows(partition: str, n: int | None = None) -> list[dict[str, Any]]:
    if partition not in PARTITIONS:
        raise ValueError(
            "Stage 3.1 may generate only training or validation; final test is inaccessible"
        )
    count = PARTITIONS[partition] if n is None else int(n)
    if count <= 0:
        raise ValueError("count must be positive")
    seed = PARTITION_SEEDS[partition]
    lhs = qmc.LatinHypercube(d=len(DESIGN_DIMENSIONS), seed=seed).random(count)
    rng = np.random.default_rng(seed + 1000)
    cells = np.array(
        [
            (family, stratum)
            for family in FAMILIES
            for stratum in FORCING_STRATA
        ],
        dtype=object,
    )
    repetitions = math.ceil(count / len(cells))
    assignments = np.tile(cells, (repetitions, 1))[:count]
    rng.shuffle(assignments, axis=0)

    rows: list[dict[str, Any]] = []
    for index in range(count):
        values = dict(zip(DESIGN_DIMENSIONS, lhs[index], strict=True))
        row: dict[str, Any] = {
            "partition": partition,
            "partition_index": index,
            "row_id": f"{partition}-{index:05d}",
            "forcing_family": str(assignments[index, 0]),
            "forcing_stratum": str(assignments[index, 1]),
        }
        for name, (low, high) in UNIFORM_RANGES.items():
            row[name] = _scale(float(values[name]), low, high)
        for name, default in LOG_FACTOR_DEFAULTS.items():
            row[name] = _log_factor(float(values[name]), default)
        row["u_safe"] = row["u_safe_fraction"] * row["u_max"]
        amp_low, amp_high = AMPLITUDE_RANGES[row["forcing_stratum"]]
        row["amplitude"] = _scale(
            float(values["amplitude_unit"]),
            amp_low,
            amp_high,
        )
        row["design_hash"] = _canonical_hash(
            {key: value for key, value in row.items() if key != "design_hash"}
        )
        rows.append(row)
    return rows


def _bounds_valid(result, params: Parameters) -> bool:
    return bool(
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


def _failure_reason(result, outcome, thresholds: Thresholds) -> str:
    if outcome.hosted:
        return "hosted"
    if not outcome.target_reached:
        return "target_not_reached"
    if float(np.max(result.d)) > thresholds.d_max:
        return "damage_violation"
    if float(np.min(result.q)) < thresholds.q_min:
        return "integrity_violation"
    if float(np.max(result.c_a)) > thresholds.c_max:
        return "free_load_violation"
    if float(np.max(result.u)) > result.params.u_max + 1e-9:
        return "buffer_bound_violation"
    if float(result.s[-1]) < thresholds.s_terminal_fraction * result.params.s_max:
        return "terminal_reserve_violation"
    return "other_nonhosting"


def simulate_design(row: dict[str, Any]) -> dict[str, Any]:
    parameter_values = {
        field.name: row[field.name]
        for field in fields(Parameters)
        if field.name in row
    }
    params = Parameters(**parameter_values)
    initial = InitialState(
        c_a=float(row["c_a0"]),
        p=float(row["p_fraction0"] * params.p_cap),
        u=float(row["u_fraction0"] * params.u_max),
        d=float(row["d0"]),
        s=float(row["s_fraction0"] * params.s_max),
        q=float(row["q0"]),
    )
    schedule, descriptors = _schedule_and_descriptors(row, initial)

    solver_retry_level = 0
    config = SimulationConfig(method="BDF", rtol=1e-8, atol=1e-10)
    try:
        with _time_limit(5.0):
            result = simulate(schedule, params=params, initial=initial, config=config)
    except Stage31Timeout:
        solver_retry_level = 1
        config = SimulationConfig(method="RK45", rtol=1e-8, atol=1e-10)
        with _time_limit(5.0):
            result = simulate(schedule, params=params, initial=initial, config=config)

    accounting_timeout_fallback = False
    try:
        with _time_limit(3.0):
            acc = accounting(result)
    except Stage31Timeout:
        accounting_timeout_fallback = True
        with _time_limit(5.0):
            acc = accounting_refined(result)

    if not acc.valid:
        solver_retry_level = max(solver_retry_level, 2)
        config = SimulationConfig(method="DOP853", rtol=1e-10, atol=1e-12)
        with _time_limit(5.0):
            result = simulate(schedule, params=params, initial=initial, config=config)
        with _time_limit(5.0):
            acc = accounting_refined(result)

    outcome = evaluate(result)
    proxy_config = ProxyConfig(probe=ProbeSpec())
    peak = scheduled_peak(schedule, initial, config.t_intervention)
    probe_solver = "BDF"
    probe_timeout_fallback = False
    try:
        with _time_limit(3.0):
            primary_probe, sensitivity_probe = capture_probe_pair_combined(
                params,
                initial,
                ProbeSpec(),
                ProbeSpec().sensitivity(),
                method=probe_solver,
            )
    except Stage31Timeout:
        probe_timeout_fallback = True
        probe_solver = "RK45"
        with _time_limit(3.0):
            primary_probe, sensitivity_probe = capture_probe_pair_combined(
                params,
                initial,
                ProbeSpec(),
                ProbeSpec().sensitivity(),
                method=probe_solver,
            )

    g_b = bounded_coupling(peak, proxy_config)
    thresholds = Thresholds()
    record: dict[str, Any] = dict(row)
    record.update(descriptors)
    record.update(
        {
            f"param_{name}": getattr(params, name)
            for name in (field.name for field in fields(Parameters))
        }
    )
    record.update(
        {
            "initial_c_a": initial.c_a,
            "initial_p": initial.p,
            "initial_p_fraction": initial.p / params.p_cap,
            "initial_u": initial.u,
            "initial_u_fraction": initial.u / params.u_max,
            "initial_d": initial.d,
            "initial_s": initial.s,
            "initial_s_fraction": initial.s / params.s_max,
            "initial_q": initial.q,
            "productive_headroom": 1.0 - initial.p / params.p_cap,
            "buffer_headroom": 1.0 - initial.u / params.u_max,
            "damage_margin": thresholds.d_max - initial.d,
            "integrity_margin": initial.q - thresholds.q_min,
            "reserve_fraction": initial.s / params.s_max,
            "free_load_margin": thresholds.c_max - initial.c_a,
            "g_b": g_b,
            "g_q": initial.q,
            "g_c_probe_sham_adjusted_primary": primary_probe.score,
            "g_c_probe_sham_adjusted_2_5x_dose": sensitivity_probe.score,
            "g_c_direct_structural_composite": capture_direct(params, initial),
            "g_s": initial.s / params.s_max,
            "probe_valid": primary_probe.valid,
            "probe_delivered": primary_probe.delivered,
            "probe_delivered_floor": primary_probe.delivered_floor,
            "probe_marginal_productive": primary_probe.marginal_productive,
            "probe_raw_ratio": primary_probe.raw_ratio,
            "probe_marginal_ratio": primary_probe.marginal_ratio,
            "sensitivity_probe_valid": sensitivity_probe.valid,
            "solver_success": result.solver_success,
            "generation_solver": config.method,
            "solver_retry_level": solver_retry_level,
            "accounting_timeout_fallback": accounting_timeout_fallback,
            "probe_solver": probe_solver,
            "probe_timeout_fallback": probe_timeout_fallback,
            "bounds_valid": _bounds_valid(result, params),
            "productive_pool_monotone": bool(np.all(np.diff(result.p) >= -1e-9)),
            "projection_count": result.projection_count,
            "accounting_valid": acc.valid,
            "accounting_refined": acc.refined,
            "accounting_residual": acc.residual,
            "accounting_tolerance": acc.tolerance,
            "accounting_residual_fraction": abs(acc.residual) / acc.tolerance,
            "delivered": acc.delivered,
            "productive_total": acc.productive,
            "rejected": acc.rejected,
            "target_reached": outcome.target_reached,
            "viable": outcome.viable,
            "hosted": outcome.hosted,
            "productive_at_intervention": outcome.productive_at_intervention,
            "peak_damage": outcome.peak_damage,
            "minimum_integrity": outcome.minimum_integrity,
            "peak_free_load": outcome.peak_free_load,
            "terminal_reserve": outcome.terminal_reserve,
            "terminal_reserve_fraction": outcome.terminal_reserve / params.s_max,
            "failure_reason": _failure_reason(result, outcome, thresholds),
        }
    )
    normalized = {
        key: (value.item() if isinstance(value, np.generic) else value)
        for key, value in record.items()
        if key != "row_digest"
    }
    record["row_digest"] = _canonical_hash(normalized)
    return record


def _assign_training_subsets(data: pd.DataFrame) -> pd.DataFrame:
    if set(data.partition.unique()) != {"training"}:
        return data
    ordered = data.assign(
        _subset_hash=data.row_id.map(
            lambda value: hashlib.sha256(value.encode()).hexdigest()
        )
    ).sort_values("_subset_hash")
    fit_count = int(round(0.75 * len(data)))
    subset = pd.Series("calibration", index=ordered.index)
    subset.iloc[:fit_count] = "fit"
    result = data.copy()
    result["training_subset"] = subset.reindex(result.index)
    return result


def generate_partition(
    partition: str,
    output_dir: str | Path,
    *,
    n: int | None = None,
    workers: int = 1,
    batch_size: int = 500,
) -> tuple[pd.DataFrame, dict[str, Any]]:
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    design = design_rows(partition, n=n)
    chunk_dir = output / ".stage31_chunks"
    chunk_dir.mkdir(parents=True, exist_ok=True)
    frames: list[pd.DataFrame] = []
    for start_index in range(0, len(design), batch_size):
        end_index = min(start_index + batch_size, len(design))
        chunk_path = (
            chunk_dir
            / f"{partition}_{start_index:05d}_{end_index:05d}.csv"
        )
        if chunk_path.exists():
            frame = pd.read_csv(chunk_path)
        else:
            batch = design[start_index:end_index]
            if workers > 1:
                with Pool(processes=workers, maxtasksperchild=100) as pool:
                    records = list(pool.imap(simulate_design, batch, chunksize=4))
            else:
                records = [simulate_design(row) for row in batch]
            frame = pd.DataFrame(records).sort_values("partition_index")
            frame.to_csv(chunk_path, index=False, float_format="%.17g")
        frames.append(frame)

    data = (
        pd.concat(frames, ignore_index=True)
        .sort_values("partition_index")
        .reset_index(drop=True)
    )
    if partition == "training":
        data = _assign_training_subsets(data)
    path = output / f"{partition}.csv"
    data.to_csv(path, index=False, float_format="%.17g")
    manifest = {
        "version": VERSION,
        "partition": partition,
        "rows": len(data),
        "seed": PARTITION_SEEDS[partition],
        "file": path.name,
        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "design_hash_sha256": hashlib.sha256(
            "\n".join(data.design_hash).encode()
        ).hexdigest(),
        "row_digest_sha256": hashlib.sha256(
            "\n".join(data.row_digest).encode()
        ).hexdigest(),
        "test_partition_opened": False,
        "candidate_model_fitted": False,
    }
    (output / f"{partition}_manifest.json").write_text(
        json.dumps(manifest, indent=2),
        encoding="utf-8",
    )
    return data, manifest


def _cross_solver_audit(
    data: pd.DataFrame,
    sample_fraction: float = 0.01,
) -> dict[str, Any]:
    n = max(1, int(round(sample_fraction * len(data))))
    sample = (
        data.assign(
            _audit_hash=data.row_id.map(
                lambda value: hashlib.sha256((value + "-solver").encode()).hexdigest()
            )
        )
        .sort_values("_audit_hash")
        .head(n)
    )
    terminal_differences: list[float] = []
    outcome_mismatches = 0
    for _, stored in sample.iterrows():
        raw = {name: stored[name] for name in UNIFORM_RANGES if name in stored}
        raw.update({name: stored[name] for name in LOG_FACTOR_DEFAULTS})
        raw.update(
            {
                "amplitude": stored.amplitude,
                "forcing_family": stored.forcing_family,
                "forcing_stratum": stored.forcing_stratum,
                "pulse_duration": stored.pulse_duration,
                "shock_duration": stored.shock_duration,
                "tail_fraction": stored.tail_fraction,
            }
        )
        parameter_values = {
            field.name: stored[f"param_{field.name}"]
            for field in fields(Parameters)
        }
        params = Parameters(**parameter_values)
        initial = InitialState(
            stored.initial_c_a,
            stored.initial_p,
            stored.initial_u,
            stored.initial_d,
            stored.initial_s,
            stored.initial_q,
        )
        schedule, _ = _schedule_and_descriptors(raw, initial)
        bdf = simulate(
            schedule,
            params=params,
            initial=initial,
            config=SimulationConfig(method="BDF", rtol=1e-8, atol=1e-10),
        )
        rk45 = simulate(
            schedule,
            params=params,
            initial=initial,
            config=SimulationConfig(method="RK45", rtol=1e-8, atol=1e-10),
        )
        scale = np.maximum(
            1.0,
            np.maximum(np.abs(bdf.y[:, -1]), np.abs(rk45.y[:, -1])),
        )
        terminal_differences.append(
            float(
                np.max(
                    np.abs(bdf.y[:, -1] - rk45.y[:, -1]) / scale
                )
            )
        )
        outcome_mismatches += int(
            evaluate(bdf).hosted != evaluate(rk45).hosted
        )
    return {
        "sample_count": n,
        "sample_fraction": n / len(data),
        "maximum_scaled_terminal_difference": max(terminal_differences),
        "hosted_outcome_mismatches": outcome_mismatches,
    }


def integrity_review(
    training: pd.DataFrame,
    validation: pd.DataFrame,
    output_dir: str | Path,
) -> dict[str, Any]:
    output = Path(output_dir)
    overlap = set(training.design_hash).intersection(validation.design_hash)
    all_data = pd.concat([training, validation], ignore_index=True)
    family_tables = {}
    for partition, frame in (("training", training), ("validation", validation)):
        table = (
            frame.groupby(
                ["forcing_family", "forcing_stratum"],
                observed=True,
            )
            .agg(
                rows=("row_id", "size"),
                hosted=("hosted", "sum"),
                hosted_fraction=("hosted", "mean"),
                probe_invalid_fraction=(
                    "probe_valid",
                    lambda values: 1.0 - float(np.mean(values)),
                ),
            )
            .reset_index()
        )
        table.to_csv(output / f"{partition}_balance.csv", index=False)
        family_tables[partition] = table.to_dict(orient="records")

    reason_table = (
        all_data.groupby(
            ["partition", "failure_reason"],
            observed=True,
        )
        .size()
        .rename("rows")
        .reset_index()
    )
    reason_table.to_csv(output / "failure_reasons.csv", index=False)

    summary: dict[str, Any] = {
        "version": VERSION,
        "test_partition_opened": False,
        "candidate_model_fitted": False,
        "training_rows": len(training),
        "validation_rows": len(validation),
        "training_unique_row_ids": int(training.row_id.nunique()),
        "validation_unique_row_ids": int(validation.row_id.nunique()),
        "training_validation_design_overlap": len(overlap),
        "solver_success_fraction": float(all_data.solver_success.mean()),
        "accounting_valid_fraction": float(all_data.accounting_valid.mean()),
        "bounds_valid_fraction": float(all_data.bounds_valid.mean()),
        "productive_monotone_fraction": float(
            all_data.productive_pool_monotone.mean()
        ),
        "maximum_accounting_residual_fraction": float(
            all_data.accounting_residual_fraction.max()
        ),
        "accounting_refinement_fraction": float(
            all_data.accounting_refined.mean()
        ),
        "primary_probe_invalid_fraction_training": float(
            1.0 - training.probe_valid.mean()
        ),
        "primary_probe_invalid_fraction_validation": float(
            1.0 - validation.probe_valid.mean()
        ),
        "sensitivity_probe_invalid_fraction_training": float(
            1.0 - training.sensitivity_probe_valid.mean()
        ),
        "sensitivity_probe_invalid_fraction_validation": float(
            1.0 - validation.sensitivity_probe_valid.mean()
        ),
        "hosted_fraction_training": float(training.hosted.mean()),
        "hosted_fraction_validation": float(validation.hosted.mean()),
        "training_fit_rows": int(
            (training.training_subset == "fit").sum()
        )
        if "training_subset" in training
        else None,
        "training_calibration_rows": int(
            (training.training_subset == "calibration").sum()
        )
        if "training_subset" in training
        else None,
        "projection_positive_fraction": float(
            (all_data.projection_count > 0).mean()
        ),
        "projection_over_500_fraction": float(
            (all_data.projection_count > 500).mean()
        ),
        "numerical_retry_fraction": float(
            (all_data.solver_retry_level > 0).mean()
        ),
        "numerical_second_retry_fraction": float(
            (all_data.solver_retry_level > 1).mean()
        ),
        "accounting_timeout_fallback_fraction": float(
            all_data.accounting_timeout_fallback.mean()
        ),
        "probe_timeout_fallback_fraction": float(
            all_data.probe_timeout_fallback.mean()
        ),
        "cross_solver_training": _cross_solver_audit(training),
        "generation_solver": "BDF",
        "audit_solver": "RK45",
        "cross_solver_validation": _cross_solver_audit(validation),
        "family_stratum_balance": family_tables,
    }
    summary["probe_stop_rule_triggered"] = bool(
        summary["primary_probe_invalid_fraction_training"] > 0.01
        or summary["primary_probe_invalid_fraction_validation"] > 0.01
    )
    summary["minimum_class_count_training"] = int(
        min(training.hosted.sum(), (~training.hosted.astype(bool)).sum())
    )
    summary["minimum_class_count_validation"] = int(
        min(validation.hosted.sum(), (~validation.hosted.astype(bool)).sum())
    )
    summary["fitting_ready"] = bool(
        summary["training_validation_design_overlap"] == 0
        and summary["solver_success_fraction"] == 1.0
        and summary["accounting_valid_fraction"] == 1.0
        and summary["bounds_valid_fraction"] == 1.0
        and summary["productive_monotone_fraction"] == 1.0
        and not summary["probe_stop_rule_triggered"]
        and summary["minimum_class_count_training"] >= 200
        and summary["minimum_class_count_validation"] >= 50
        and summary["cross_solver_training"]["hosted_outcome_mismatches"] == 0
        and summary["cross_solver_validation"]["hosted_outcome_mismatches"] == 0
    )
    (output / "integrity_summary.json").write_text(
        json.dumps(summary, indent=2),
        encoding="utf-8",
    )
    return summary


def run(
    output_dir: str | Path,
    *,
    training_n: int | None = None,
    validation_n: int | None = None,
    workers: int = 1,
) -> dict[str, Any]:
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    training, train_manifest = generate_partition(
        "training",
        output,
        n=training_n,
        workers=workers,
    )
    validation, validation_manifest = generate_partition(
        "validation",
        output,
        n=validation_n,
        workers=workers,
    )
    summary = integrity_review(training, validation, output)
    combined_manifest = {
        "version": VERSION,
        "master_seed": MASTER_SEED,
        "partitions": {
            "training": train_manifest,
            "validation": validation_manifest,
        },
        "test_partition_generated": False,
        "test_partition_opened": False,
        "candidate_model_fitted": False,
        "environment": {
            "python": __import__("sys").version.split()[0],
            "numpy": np.__version__,
            "pandas": pd.__version__,
            "scipy": scipy.__version__,
        },
        "design": {
            "families": list(FAMILIES),
            "forcing_strata": AMPLITUDE_RANGES,
            "uniform_ranges": UNIFORM_RANGES,
            "log_factor_defaults": LOG_FACTOR_DEFAULTS,
            "probe_primary": asdict(ProbeSpec()),
            "probe_sensitivity": asdict(ProbeSpec().sensitivity()),
        },
    }
    (output / "stage31_manifest.json").write_text(
        json.dumps(combined_manifest, indent=2),
        encoding="utf-8",
    )
    return summary


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="results/stage3_1")
    parser.add_argument("--workers", type=int, default=1)
    parser.add_argument("--quick", action="store_true")
    args = parser.parse_args()
    summary = run(
        args.output,
        training_n=240 if args.quick else None,
        validation_n=80 if args.quick else None,
        workers=args.workers,
    )
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
