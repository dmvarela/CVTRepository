"""Stage 5.1A fresh-generator implementation and bounded smoke audit.

This module cannot generate a full Stage 5 partition. It reads no Stage 3
row-level evidence, fits no model, and has no final-test path.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from dataclasses import asdict, dataclass, fields
from pathlib import Path
from typing import Any

import numpy as np
from scipy.stats import qmc

from .accounting import accounting
from .model import InitialState, Parameters, SimulationConfig, simulate
from .proxies import ProbeMeasurement, ProbeSpec, ProxyConfig, bounded_coupling, capture_probe
from .schedules import Forcing, constant, pulse, ramp, shock_tail


class Stage51AError(ValueError):
    """Raised when a dry-run authorization or generator invariant is violated."""


@dataclass(frozen=True)
class HistoryResult:
    state: InitialState
    prior_scheduled_dose: float
    time_since_prior_exposure: float
    precontact_recovery_fraction: float
    solver_success: bool


FAMILIES = ("constant", "pulse", "ramp", "shock_tail")
STRATA = ("low", "middle", "high")
HISTORIES = (
    "none",
    "subthreshold_prior_exposure",
    "prior_exposure_then_recovery",
)


def canonical_hash(payload: Any) -> str:
    def normalize(value: Any) -> Any:
        if isinstance(value, dict):
            return {str(key): normalize(item) for key, item in value.items()}
        if isinstance(value, (list, tuple)):
            return [normalize(item) for item in value]
        if isinstance(value, np.generic):
            return value.item()
        if isinstance(value, float) and not math.isfinite(value):
            raise Stage51AError("non-finite value cannot be hashed")
        return value

    encoded = json.dumps(
        normalize(payload),
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def file_sha256(path: str | Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def derive_seed(namespace: str, partition: str, row_index: int) -> int:
    if row_index < 0:
        raise Stage51AError("row_index must be nonnegative")
    digest = hashlib.sha256(
        f"{namespace}:{partition}:{row_index}".encode("utf-8")
    ).digest()
    return int.from_bytes(digest[:8], byteorder="big", signed=False)


def stage5_row_id(namespace: str, partition: str, row_index: int) -> str:
    digest = hashlib.sha256(
        f"{namespace}:{partition}:{row_index}".encode("utf-8")
    ).hexdigest()
    return f"s5-{partition}-{digest[:16]}"


def load_json(path: str | Path) -> dict[str, Any]:
    with Path(path).open(encoding="utf-8") as handle:
        return json.load(handle)


def audit_configuration(
    protocol: dict[str, Any],
    implementation: dict[str, Any],
) -> dict[str, Any]:
    checks: list[str] = []

    if protocol.get("stage") != "5.0":
        raise Stage51AError("Stage 5.0 protocol is required")
    if implementation.get("stage") != "5.1A":
        raise Stage51AError("Stage 5.1A implementation config is required")
    if canonical_hash(protocol) != implementation["protocol"]["canonical_json_sha256"]:
        raise Stage51AError("frozen Stage 5.0 canonical protocol hash changed")
    checks.append("stage_identity")

    auth = implementation["authorization"]
    if not auth["stage51a_smoke_generation_authorized"]:
        raise Stage51AError("bounded smoke generation must be explicitly authorized")
    if auth["maximum_smoke_rows"] > 12:
        raise Stage51AError("Stage 5.1A smoke limit cannot exceed 12")
    for key in (
        "full_development_partition_generation_authorized",
        "candidate_model_fitting_authorized",
        "fresh_validation_generation_authorized",
        "fresh_validation_opening_authorized",
        "confirmatory_final_test_authorized",
        "final_test_generated",
        "final_test_opened",
    ):
        if auth[key]:
            raise Stage51AError(f"{key} must be false in Stage 5.1A")
    checks.append("dry_run_authorization")

    if implementation["seed_and_identity"]["row_level_stage3_access_permitted"]:
        raise Stage51AError("Stage 3 row access is forbidden")
    planned = implementation["planned_partitions"]
    protocol_partitions = protocol["fresh_partitions"]
    for name, spec in planned.items():
        expected = protocol_partitions[name]
        if spec["rows"] != expected["rows"]:
            raise Stage51AError(f"{name} row count differs from Stage 5.0")
        if spec["seed_namespace"] != expected["seed_namespace"]:
            raise Stage51AError(f"{name} seed namespace differs from Stage 5.0")
    namespaces = [spec["seed_namespace"] for spec in planned.values()]
    if len(namespaces) != len(set(namespaces)):
        raise Stage51AError("partition namespaces must be unique")
    checks.append("partition_and_namespace_lock")

    balanced = implementation["balanced_design"]
    if balanced["reserved_forcing_family"] in balanced["forcing_families"]:
        raise Stage51AError("reserved repeated-pulse family leaked into development")
    if balanced["adaptive_outcome_enrichment_permitted"]:
        raise Stage51AError("outcome-adaptive enrichment is forbidden")
    checks.append("balanced_design_and_reserved_family")

    relational = implementation["relational_columns"]
    native = implementation["native_columns"]
    if len(relational) != 31 or len(set(relational)) != 31:
        raise Stage51AError("relational contract must contain 31 unique columns")
    if len(native) != 31 or len(set(native)) != 31:
        raise Stage51AError("native contract must contain 31 unique columns")
    checks.append("equal_31_column_contracts")

    probe = implementation["probe_design"]
    if probe["implementation"] != "discarded_sham_adjusted_counterfactual_clones":
        raise Stage51AError("probe isolation contract changed")
    if probe["timing_states"] != [
        "initial_state",
        "post_history_pre_main_input",
    ]:
        raise Stage51AError("probe timing contract changed")
    if probe["dose_multipliers"] != [1.0, 2.5]:
        raise Stage51AError("probe dose contract changed")
    if set(probe["summary_formulas"]) != set(relational[-8:]):
        raise Stage51AError("the eight probe summaries do not match the feature contract")
    checks.append("probe_contract")

    protocol_auth = protocol["authorization"]
    if any(
        protocol_auth[key]
        for key in (
            "stage5_data_generation_authorized",
            "stage5_candidate_fitting_authorized",
            "stage5_validation_generation_authorized",
            "stage5_validation_opening_authorized",
            "confirmatory_final_test_authorized",
            "final_test_generated",
            "final_test_opened",
        )
    ):
        raise Stage51AError("Stage 5.0 execution/final-test firewall changed")
    checks.append("upstream_firewall")

    return {
        "stage": "5.1A",
        "status": "pass",
        "checks": checks,
        "check_count": len(checks),
        "full_partition_generation_authorized": False,
        "candidate_model_fitted": False,
        "fresh_validation_generated": False,
        "final_test_generated": False,
        "final_test_opened": False,
    }


def _scale(unit: float, bounds: list[float]) -> float:
    low, high = map(float, bounds)
    return low + float(unit) * (high - low)


def _log_factor(unit: float, default: float) -> float:
    return float(
        math.exp(
            math.log(default / 3.0)
            + float(unit) * (math.log(default * 3.0) - math.log(default / 3.0))
        )
    )


def balanced_cell(index: int) -> tuple[str, str, str]:
    """Return a 36-row cycle with balanced 12-row smoke marginals."""
    within = index % 36
    block = within // 12
    family = FAMILIES[within % 4]
    stratum = STRATA[(within // 4) % 3]
    history = HISTORIES[(block + within % 3) % 3]
    return family, stratum, history


def _design_dimensions(config: dict[str, Any]) -> list[str]:
    return (
        list(config["native_parameter_ranges"])
        + list(config["initial_state_ranges"])
        + list(config["log_factor_defaults"])
        + [
            name
            for name in config["schedule_ranges"]
            if name != "declared_recovery_horizon"
        ]
        + [
            name
            for name in config["history_ranges"]
            if name != "none_recovery_fraction"
        ]
        + ["amplitude_unit"]
    )


def design_smoke_rows(
    protocol: dict[str, Any],
    config: dict[str, Any],
    *,
    partition: str = "development_fit",
    rows: int = 12,
) -> list[dict[str, Any]]:
    audit_configuration(protocol, config)
    maximum = int(config["authorization"]["maximum_smoke_rows"])
    if partition != config["allowed_smoke_partition"]:
        raise Stage51AError("Stage 5.1A may smoke only development_fit")
    if rows <= 0 or rows > maximum:
        raise Stage51AError(f"smoke rows must be between 1 and {maximum}")

    namespace = config["planned_partitions"][partition]["seed_namespace"]
    dimensions = _design_dimensions(config)
    design_seed = derive_seed(namespace, partition, 2**31 - 1)
    lhs = qmc.LatinHypercube(
        d=len(dimensions),
        seed=np.random.default_rng(design_seed),
    ).random(rows)

    result: list[dict[str, Any]] = []
    for index in range(rows):
        values = dict(zip(dimensions, lhs[index], strict=True))
        family, stratum, history = balanced_cell(index)
        row: dict[str, Any] = {
            "partition": partition,
            "partition_index": index,
            "row_id": stage5_row_id(namespace, partition, index),
            "row_seed": derive_seed(namespace, partition, index),
            "forcing_family": family,
            "forcing_stratum": stratum,
            "history_class": history,
        }
        for name, bounds in config["native_parameter_ranges"].items():
            row[name] = _scale(values[name], bounds)
        for name, bounds in config["initial_state_ranges"].items():
            row[name] = _scale(values[name], bounds)
        for name, default in config["log_factor_defaults"].items():
            row[name] = _log_factor(values[name], float(default))
        for name, bounds in config["schedule_ranges"].items():
            if name == "declared_recovery_horizon":
                row[name] = float(bounds[0])
            else:
                row[name] = _scale(values[name], bounds)
        for name, bounds in config["history_ranges"].items():
            if name != "none_recovery_fraction":
                row[name] = _scale(values[name], bounds)
        row["u_safe"] = row["u_safe_fraction"] * row["u_max"]
        row["amplitude"] = _scale(
            values["amplitude_unit"],
            config["balanced_design"]["forcing_strata"][stratum],
        )
        row["design_hash"] = canonical_hash(row)
        result.append(row)
    return result


def _params_initial(row: dict[str, Any]) -> tuple[Parameters, InitialState]:
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
    return params, initial


def _state_from_array(vector: np.ndarray, params: Parameters) -> InitialState:
    upper = np.array([np.inf, np.inf, params.u_max, 1.0, params.s_max, 1.0])
    clipped = np.minimum(np.maximum(np.asarray(vector, dtype=float), 0.0), upper)
    return InitialState(*map(float, clipped))


def _state_distance(
    first: InitialState,
    second: InitialState,
    params: Parameters,
) -> float:
    scales = np.array([1.0, params.p_cap, params.u_max, 1.0, params.s_max, 1.0])
    return float(np.linalg.norm((first.as_array() - second.as_array()) / scales))


def apply_history(
    row: dict[str, Any],
    params: Parameters,
    initial: InitialState,
    config: dict[str, Any],
) -> HistoryResult:
    history = row["history_class"]
    if history == "none":
        return HistoryResult(
            state=initial,
            prior_scheduled_dose=0.0,
            time_since_prior_exposure=0.0,
            precontact_recovery_fraction=float(
                config["history_ranges"]["none_recovery_fraction"]
            ),
            solver_success=True,
        )
    if history not in HISTORIES:
        raise Stage51AError(f"unsupported history class: {history}")

    target_peak = float(row["prior_peak_fraction_j_safe"] * params.j_safe)
    permeability = float(row["prior_permeability"])
    duration = float(row["prior_duration"])
    recovery = (
        float(row["recovery_interval"])
        if history == "prior_exposure_then_recovery"
        else 0.0
    )
    source = float(initial.c_a + target_peak / permeability)
    schedule = pulse(
        Forcing(source, permeability, t_intervention=duration),
        duration=duration,
    )
    simulation = simulate(
        schedule,
        params=params,
        initial=initial,
        config=SimulationConfig(
            t_intervention=duration,
            t_follow=recovery,
            dt_out=(duration + recovery) / 200.0,
            rtol=1e-8,
            atol=1e-10,
            method="BDF",
        ),
    )
    exposed = _state_from_array(simulation.dense_solution(duration), params)
    post = _state_from_array(simulation.y[:, -1], params)
    disturbed = _state_distance(exposed, initial, params)
    residual = _state_distance(post, initial, params)
    recovery_fraction = (
        float(np.clip(1.0 - residual / disturbed, 0.0, 1.0))
        if disturbed > 1e-12 and recovery > 0.0
        else 0.0
    )
    return HistoryResult(
        state=post,
        prior_scheduled_dose=target_peak * duration,
        time_since_prior_exposure=recovery,
        precontact_recovery_fraction=recovery_fraction,
        solver_success=simulation.solver_success,
    )


def main_schedule_and_descriptors(
    row: dict[str, Any],
    state: InitialState,
) -> tuple[Any, dict[str, float]]:
    forcing = Forcing(
        float(row["amplitude"]),
        float(row["permeability"]),
        t_intervention=20.0,
    )
    family = row["forcing_family"]
    if family == "constant":
        schedule = constant(forcing)
        active_duration = 20.0
    elif family == "pulse":
        active_duration = float(row["pulse_duration"])
        schedule = pulse(forcing, duration=active_duration)
    elif family == "ramp":
        schedule = ramp(forcing)
        active_duration = 20.0
    elif family == "shock_tail":
        schedule = shock_tail(
            forcing,
            shock_duration=float(row["shock_duration"]),
            tail_fraction=float(row["tail_fraction"]),
        )
        active_duration = 20.0
    else:
        raise Stage51AError(f"unsupported forcing family: {family}")

    times = np.linspace(0.0, 20.0, 2001)
    intact = np.array(
        [
            permeability * max(0.0, source - state.c_a)
            for source, permeability in (schedule(float(time)) for time in times)
        ]
    )
    peak = float(np.max(intact))
    dose = float(np.trapezoid(intact, times))
    centroid = (
        float(np.trapezoid(times * intact, times) / dose)
        if dose > 0.0
        else 0.0
    )
    if peak > 0.0:
        rise_indices = np.flatnonzero(intact >= 0.9 * peak)
        rise_time = float(times[int(rise_indices[0])])
    else:
        rise_time = 0.0
    descriptors = {
        "scheduled_peak": peak,
        "scheduled_dose": dose,
        "active_duration": active_duration,
        "input_centroid": centroid,
        "rise_time": rise_time,
        "tail_fraction": (
            float(row["tail_fraction"]) if family == "shock_tail" else 0.0
        ),
        "declared_recovery_horizon": float(row["declared_recovery_horizon"]),
    }
    return schedule, descriptors


def _probe_fractions(measurement: ProbeMeasurement) -> dict[str, float]:
    if not measurement.valid or measurement.delivered <= 0.0:
        raise Stage51AError("invalid smoke probe")
    uptake = float(measurement.marginal_productive / measurement.delivered)
    buffering = float(measurement.incremental_u / measurement.delivered)
    rejection = float(
        (
            measurement.delivered
            - measurement.marginal_productive
            - measurement.incremental_c
            - measurement.incremental_u
        )
        / measurement.delivered
    )
    return {
        "uptake": float(np.clip(uptake, 0.0, 1.0)),
        "buffering": float(np.clip(buffering, -1.0, 1.0)),
        "rejection": float(np.clip(rejection, 0.0, 1.0)),
        "damage": float(measurement.incremental_d / measurement.delivered),
        "integrity_loss": float(-measurement.incremental_q / measurement.delivered),
    }


def _probe_disturbance_norm(
    measurement: ProbeMeasurement,
    params: Parameters,
) -> float:
    scaled = np.array(
        [
            measurement.incremental_c,
            measurement.incremental_p / params.p_cap,
            measurement.incremental_u / params.u_max,
            measurement.incremental_d,
            measurement.incremental_s / params.s_max,
            measurement.incremental_q,
        ]
    )
    return float(np.linalg.norm(scaled))


def _probe_recovery_fraction(
    short: ProbeMeasurement,
    recovery: ProbeMeasurement,
    params: Parameters,
) -> float:
    initial_norm = _probe_disturbance_norm(short, params)
    terminal_norm = _probe_disturbance_norm(recovery, params)
    if initial_norm <= 1e-12:
        return 0.0
    return float(np.clip(1.0 - terminal_norm / initial_norm, -1.0, 1.0))


def run_probe_summaries(
    params: Parameters,
    initial: InitialState,
    posthistory: InitialState,
    config: dict[str, Any],
) -> tuple[dict[str, float], dict[str, Any]]:
    probe_config = config["probe_design"]
    cells: dict[str, dict[float, dict[str, ProbeMeasurement]]] = {}
    timing_states = {
        "initial": initial,
        "posthistory": posthistory,
    }
    valid: list[bool] = []
    for timing, state in timing_states.items():
        cells[timing] = {}
        for multiplier in map(float, probe_config["dose_multipliers"]):
            cells[timing][multiplier] = {}
            for horizon_name, horizon in (
                ("short", float(probe_config["short_horizon"])),
                ("recovery", float(probe_config["recovery_horizon"])),
            ):
                measurement = capture_probe(
                    params,
                    state,
                    ProbeSpec(
                        c_b=float(probe_config["base_c_b"]),
                        permeability=float(
                            probe_config["base_permeability"] * multiplier
                        ),
                        pulse_duration=float(probe_config["pulse_duration"]),
                        readout_horizon=horizon,
                        delivered_floor_fraction_pcap=float(
                            probe_config["delivered_floor_fraction_pcap"]
                        ),
                    ),
                    method="BDF",
                    rtol=1e-8,
                    atol=1e-10,
                )
                cells[timing][multiplier][horizon_name] = measurement
                valid.append(measurement.valid)

    post_1 = cells["posthistory"][1.0]["short"]
    post_25 = cells["posthistory"][2.5]["short"]
    post_1_f = _probe_fractions(post_1)
    post_25_f = _probe_fractions(post_25)
    initial_recovery = _probe_recovery_fraction(
        cells["initial"][1.0]["short"],
        cells["initial"][1.0]["recovery"],
        params,
    )
    post_recovery = _probe_recovery_fraction(
        post_1,
        cells["posthistory"][1.0]["recovery"],
        params,
    )
    summaries = {
        "probe_uptake_nominal_posthistory": post_1_f["uptake"],
        "probe_uptake_dose_slope": (
            post_25_f["uptake"] - post_1_f["uptake"]
        )
        / 1.5,
        "probe_rejection_nominal_posthistory": post_1_f["rejection"],
        "probe_buffering_dose_slope": (
            post_25_f["buffering"] - post_1_f["buffering"]
        )
        / 1.5,
        "probe_damage_dose_slope": (
            post_25_f["damage"] - post_1_f["damage"]
        )
        / 1.5,
        "probe_integrity_dose_slope": (
            post_25_f["integrity_loss"] - post_1_f["integrity_loss"]
        )
        / 1.5,
        "probe_recovery_nominal_posthistory": post_recovery,
        "probe_recovery_timing_contrast": post_recovery - initial_recovery,
    }
    return summaries, {
        "measurements": len(valid),
        "valid": int(sum(valid)),
        "invalid": int(len(valid) - sum(valid)),
    }


def _category_features(family: str, history: str) -> dict[str, float]:
    return {
        "forcing_is_pulse": float(family == "pulse"),
        "forcing_is_ramp": float(family == "ramp"),
        "forcing_is_shock_tail": float(family == "shock_tail"),
        "history_is_subthreshold_prior_exposure": float(
            history == "subthreshold_prior_exposure"
        ),
        "history_is_prior_exposure_then_recovery": float(
            history == "prior_exposure_then_recovery"
        ),
    }


def feature_vectors(
    row: dict[str, Any],
    params: Parameters,
    state: InitialState,
    history: HistoryResult,
    descriptors: dict[str, float],
    probe: dict[str, float],
    config: dict[str, Any],
) -> tuple[dict[str, float], dict[str, float]]:
    categories = _category_features(row["forcing_family"], row["history_class"])
    local = {
        "g_b": bounded_coupling(descriptors["scheduled_peak"], ProxyConfig()),
        "g_q": state.q,
        "g_s": state.s / params.s_max,
        "initial_free_load_fraction": state.c_a / max(params.c_safe, 1e-12),
        "initial_buffer_load_fraction": state.u / params.u_max,
        "initial_damage_margin": 0.45 - state.d,
        "initial_integrity_margin": state.q - 0.55,
        "initial_reserve_fraction": state.s / params.s_max,
    }
    relational = {
        **local,
        **{key: categories[key] for key in categories if key.startswith("forcing_")},
        **descriptors,
        **{
            key: categories[key]
            for key in categories
            if key.startswith("history_")
        },
        "prior_scheduled_dose": history.prior_scheduled_dose,
        "time_since_prior_exposure": history.time_since_prior_exposure,
        "precontact_recovery_fraction": history.precontact_recovery_fraction,
        **probe,
    }
    native_names = (
        "p_cap",
        "u_max",
        "k_p",
        "k_b",
        "k_rel",
        "k_e",
        "s_max",
        "r_s",
        "k_rep",
        "r_q",
        "c_safe",
        "u_safe",
        "c_q",
        "j_safe",
        "h",
    )
    native = {
        **{f"param_{name}": float(getattr(params, name)) for name in native_names},
        "state_c_a": state.c_a,
        "state_p": state.p,
        "state_u": state.u,
        "state_d": state.d,
        "state_s": state.s,
        "state_q": state.q,
        **{key: categories[key] for key in categories if key.startswith("forcing_")},
        "scheduled_peak": descriptors["scheduled_peak"],
        "scheduled_dose": descriptors["scheduled_dose"],
        "active_duration": descriptors["active_duration"],
        **{
            key: categories[key]
            for key in categories
            if key.startswith("history_")
        },
        "prior_scheduled_dose": history.prior_scheduled_dose,
        "time_since_prior_exposure": history.time_since_prior_exposure,
    }
    relational_order = config["relational_columns"]
    native_order = config["native_columns"]
    if set(relational) != set(relational_order):
        raise Stage51AError("relational feature implementation differs from contract")
    if set(native) != set(native_order):
        raise Stage51AError("native feature implementation differs from contract")
    return (
        {name: float(relational[name]) for name in relational_order},
        {name: float(native[name]) for name in native_order},
    )


def _bounds_valid(result: Any, params: Parameters) -> bool:
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


def smoke_record(
    row: dict[str, Any],
    config: dict[str, Any],
) -> dict[str, Any]:
    params, initial = _params_initial(row)
    history = apply_history(row, params, initial, config)
    schedule, descriptors = main_schedule_and_descriptors(row, history.state)
    simulation_config = SimulationConfig(
        t_intervention=20.0,
        t_follow=float(row["declared_recovery_horizon"]),
        dt_out=0.1,
        rtol=1e-8,
        atol=1e-10,
        method="BDF",
    )
    main_before = simulate(
        schedule,
        params=params,
        initial=history.state,
        config=simulation_config,
    )
    probe, probe_audit = run_probe_summaries(
        params,
        initial,
        history.state,
        config,
    )
    main_after = simulate(
        schedule,
        params=params,
        initial=history.state,
        config=simulation_config,
    )
    acc = accounting(main_after)
    relational, native = feature_vectors(
        row,
        params,
        history.state,
        history,
        descriptors,
        probe,
        config,
    )
    isolation = float(np.max(np.abs(main_before.y - main_after.y)))
    return {
        "row_id": row["row_id"],
        "design_hash": row["design_hash"],
        "forcing_family": row["forcing_family"],
        "forcing_stratum": row["forcing_stratum"],
        "history_class": row["history_class"],
        "history_solver_success": history.solver_success,
        "main_solver_success": main_after.solver_success,
        "accounting_valid": acc.valid,
        "bounds_valid": _bounds_valid(main_after, params),
        "accounting_residual_fraction": abs(acc.residual) / acc.tolerance,
        "probe_measurements": probe_audit["measurements"],
        "probe_invalid": probe_audit["invalid"],
        "probe_isolation_max_abs_state_difference": isolation,
        "relational_feature_count": len(relational),
        "native_feature_count": len(native),
        "relational_features_finite": bool(
            np.isfinite(list(relational.values())).all()
        ),
        "native_features_finite": bool(np.isfinite(list(native.values())).all()),
        "relational_feature_hash": canonical_hash(relational),
        "native_feature_hash": canonical_hash(native),
    }


def _counts(records: list[dict[str, Any]], column: str) -> dict[str, int]:
    return {
        value: sum(record[column] == value for record in records)
        for value in sorted({record[column] for record in records})
    }


def run_smoke(
    protocol_path: str | Path,
    config_path: str | Path,
    output_dir: str | Path,
    *,
    rows: int = 12,
) -> dict[str, Any]:
    protocol = load_json(protocol_path)
    config = load_json(config_path)
    configuration_audit = audit_configuration(protocol, config)
    design = design_smoke_rows(protocol, config, rows=rows)
    records = [smoke_record(row, config) for row in design]
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)

    total_probes = sum(record["probe_measurements"] for record in records)
    invalid_probes = sum(record["probe_invalid"] for record in records)
    integrity = {
        "stage": "5.1A",
        "status": "pass",
        "rows": len(records),
        "unique_row_ids": len({record["row_id"] for record in records}),
        "unique_design_hashes": len(
            {record["design_hash"] for record in records}
        ),
        "forcing_family_counts": _counts(records, "forcing_family"),
        "forcing_stratum_counts": _counts(records, "forcing_stratum"),
        "history_class_counts": _counts(records, "history_class"),
        "history_solver_success_fraction": float(
            np.mean([record["history_solver_success"] for record in records])
        ),
        "main_solver_success_fraction": float(
            np.mean([record["main_solver_success"] for record in records])
        ),
        "accounting_valid_fraction": float(
            np.mean([record["accounting_valid"] for record in records])
        ),
        "bounds_valid_fraction": float(
            np.mean([record["bounds_valid"] for record in records])
        ),
        "maximum_accounting_residual_fraction": max(
            record["accounting_residual_fraction"] for record in records
        ),
        "probe_measurements": total_probes,
        "probe_invalid": invalid_probes,
        "probe_invalid_fraction": invalid_probes / total_probes,
        "maximum_probe_isolation_state_difference": max(
            record["probe_isolation_max_abs_state_difference"]
            for record in records
        ),
        "finite_relational_feature_fraction": float(
            np.mean([record["relational_features_finite"] for record in records])
        ),
        "finite_native_feature_fraction": float(
            np.mean([record["native_features_finite"] for record in records])
        ),
        "relational_column_count": 31,
        "native_column_count": 31,
        "stage3_row_level_evidence_read": False,
        "full_development_partition_generated": False,
        "candidate_model_fitted": False,
        "fresh_validation_generated": False,
        "final_test_generated": False,
        "final_test_opened": False,
    }
    rules = config["smoke_integrity_rules"]
    passed = bool(
        integrity["unique_row_ids"] == len(records)
        and integrity["unique_design_hashes"] == len(records)
        and integrity["history_solver_success_fraction"]
        == rules["solver_success_fraction"]
        and integrity["main_solver_success_fraction"]
        == rules["solver_success_fraction"]
        and integrity["accounting_valid_fraction"]
        == rules["accounting_valid_fraction"]
        and integrity["bounds_valid_fraction"] == rules["bounds_valid_fraction"]
        and integrity["probe_invalid_fraction"]
        <= rules["maximum_probe_invalid_fraction"]
        and integrity["maximum_probe_isolation_state_difference"]
        <= rules["maximum_probe_isolation_state_difference"]
        and integrity["finite_relational_feature_fraction"]
        == rules["finite_feature_fraction"]
        and integrity["finite_native_feature_fraction"]
        == rules["finite_feature_fraction"]
    )
    integrity["status"] = "pass" if passed else "fail"

    manifest = {
        "stage": "5.1A",
        "version": config["version"],
        "status": "bounded_smoke_complete" if passed else "bounded_smoke_failed",
        "rows": len(records),
        "protocol_canonical_sha256": canonical_hash(protocol),
        "implementation_config_canonical_sha256": canonical_hash(config),
        "row_id_sha256": hashlib.sha256(
            "\n".join(record["row_id"] for record in records).encode("utf-8")
        ).hexdigest(),
        "design_hash_sha256": hashlib.sha256(
            "\n".join(record["design_hash"] for record in records).encode("utf-8")
        ).hexdigest(),
        "relational_feature_hash_sha256": hashlib.sha256(
            "\n".join(
                record["relational_feature_hash"] for record in records
            ).encode("utf-8")
        ).hexdigest(),
        "native_feature_hash_sha256": hashlib.sha256(
            "\n".join(
                record["native_feature_hash"] for record in records
            ).encode("utf-8")
        ).hexdigest(),
        "configuration_audit": configuration_audit,
        "smoke_only": True,
        "full_development_partition_generated": False,
        "candidate_model_fitted": False,
        "fresh_validation_generated": False,
        "final_test_generated": False,
        "final_test_opened": False,
    }
    feature_contract = {
        "stage": "5.1A",
        "relational_columns": config["relational_columns"],
        "native_columns": config["native_columns"],
        "relational_column_count": len(config["relational_columns"]),
        "native_column_count": len(config["native_columns"]),
        "equal_column_capacity": True,
        "post_outcome_predictors": [],
    }
    authorization = {
        "stage": "5.1A",
        "status": "authorized_for_stage5_1b" if passed else "not_authorized",
        "stage5_1b_full_development_generation_authorized": passed,
        "maximum_stage5_1b_rows": 24000 if passed else 0,
        "candidate_model_fitting_authorized": False,
        "fresh_validation_generation_authorized": False,
        "fresh_validation_opening_authorized": False,
        "confirmatory_final_test_authorized": False,
        "final_test_generated": False,
        "final_test_opened": False,
        "basis": [
            "stage5_0_protocol_frozen",
            "stage5_1a_configuration_audit_passed",
            "stage5_1a_bounded_smoke_integrity_passed",
        ]
        if passed
        else ["stage5_1a_bounded_smoke_integrity_failed"],
    }
    artifacts = {
        "smoke_manifest.json": manifest,
        "smoke_integrity.json": integrity,
        "feature_contract.json": feature_contract,
        "authorization_decision.json": authorization,
    }
    for name, payload in artifacts.items():
        (output / name).write_text(
            json.dumps(payload, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    if not passed:
        raise Stage51AError("Stage 5.1A smoke integrity failed")
    return {
        "manifest": manifest,
        "integrity": integrity,
        "feature_contract": feature_contract,
        "authorization": authorization,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--protocol", type=Path, required=True)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--smoke", action="store_true")
    parser.add_argument("--rows", type=int, default=12)
    args = parser.parse_args()
    if not args.smoke:
        raise SystemExit(
            "Stage 5.1A is smoke-only; pass --smoke. Full generation is disabled."
        )
    report = run_smoke(
        args.protocol,
        args.config,
        args.output,
        rows=args.rows,
    )
    print(json.dumps(report["integrity"], indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

