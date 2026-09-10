"""CP-001 — Measured Computational Proprioception, simulation only.

Tests whether Lucian OS can improve scheduling by replacing declared transition
costs and resource footprints with bounded empirical measurements. No model
calls, device actions, permission changes, or external I/O occur.

Run from modern-robotics/lucian-os:
    py prototype/computational_proprioception_v001.py
"""
from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST = PROJECT_ROOT / "manifests" / "computational_proprioception_demo.json"


def load_manifest(path: Path = DEFAULT_MANIFEST) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def transition_key(a: str, b: str) -> str:
    return f"{a}_to_{b}"


def run_sparse(data: dict[str, Any], *, adaptive: bool) -> dict[str, Any]:
    spec = data["scenario_sparse"]
    estimates = copy.deepcopy(data["transition_prior"])
    current = "local"
    work = 0
    tick = 1
    total = transition_total = operating_total = delay_total = 0.0
    observations: list[dict[str, Any]] = []
    trace: list[dict[str, Any]] = []

    while work < int(spec["work_units"]):
        pressure = tick in set(int(x) for x in spec["pressures"])
        if pressure:
            remote_est = (0.0 if current == "remote" else float(estimates[transition_key(current, "remote")])) + float(data["morphologies"]["remote"]["operating_cost"])
            choices = [("remote", remote_est), ("idle", float(spec["delay_cost"]))]
        else:
            local_est = (0.0 if current == "local" else float(estimates[transition_key(current, "local")])) + float(data["morphologies"]["local"]["operating_cost"])
            remote_est = (0.0 if current == "remote" else float(estimates[transition_key(current, "remote")])) + float(data["morphologies"]["remote"]["operating_cost"])
            choices = [("local", local_est), ("remote", remote_est)]

        action = min(choices, key=lambda row: (row[1], row[0]))[0]
        before = current
        transition = operating = delay = 0.0

        if action == "idle":
            delay = float(spec["delay_cost"])
        else:
            if action != current:
                key = transition_key(current, action)
                transition = float(spec["actual_switch_cost"])
                if adaptive:
                    estimates[key] = transition
                observations.append({"tick": tick, "transition": key, "observed_cost": transition, "estimate_after": float(estimates[key])})
                current = action
            operating = float(data["morphologies"][action]["operating_cost"])
            work += 1

        total += transition + operating + delay
        transition_total += transition
        operating_total += operating
        delay_total += delay
        trace.append({"tick": tick, "pressure": pressure, "before": before, "decision": action, "work_completed": work, "transition_cost_realized": transition, "operating_cost": operating, "delay_cost": delay, "estimates": copy.deepcopy(estimates)})
        tick += 1

    return {"adaptive": adaptive, "total_realized_cost": round(total, 3), "transition_cost": round(transition_total, 3), "operating_cost": round(operating_total, 3), "delay_cost": round(delay_total, 3), "finish_tick": tick - 1, "observations": observations, "trace": trace}


def run_drift(data: dict[str, Any], *, adaptive: bool) -> dict[str, Any]:
    spec = data["scenario_drift"]
    estimates = copy.deepcopy(data["transition_prior"])
    current = "local"
    work = 0
    tick = 1
    total = transition_total = operating_total = delay_total = 0.0
    observations: list[dict[str, Any]] = []
    trace: list[dict[str, Any]] = []

    while work < int(spec["work_units"]):
        pressure = tick in set(int(x) for x in spec["pressures"])
        if pressure:
            remote_est = (0.0 if current == "remote" else float(estimates[transition_key(current, "remote")])) + float(data["morphologies"]["remote"]["operating_cost"])
            choices = [("remote", remote_est), ("idle", float(spec["delay_cost"]))]
        else:
            local_est = (0.0 if current == "local" else float(estimates[transition_key(current, "local")])) + float(data["morphologies"]["local"]["operating_cost"])
            remote_est = (0.0 if current == "remote" else float(estimates[transition_key(current, "remote")])) + float(data["morphologies"]["remote"]["operating_cost"])
            choices = [("local", local_est), ("remote", remote_est)]

        action = min(choices, key=lambda row: (row[1], row[0]))[0]
        transition = operating = delay = 0.0

        if action == "idle":
            delay = float(spec["delay_cost"])
        else:
            if action != current:
                actual = float(spec["low_cost"]) if tick < int(spec["drift_tick"]) else float(spec["high_cost"])
                key = transition_key(current, action)
                transition = actual
                if adaptive:
                    estimates[key] = 0.2 * float(estimates[key]) + 0.8 * actual
                elif tick < int(spec["drift_tick"]):
                    estimates[key] = actual
                observations.append({"tick": tick, "transition": key, "observed_cost": actual, "estimate_after": float(estimates[key])})
                current = action
            operating = float(data["morphologies"][action]["operating_cost"])
            work += 1

        total += transition + operating + delay
        transition_total += transition
        operating_total += operating
        delay_total += delay
        trace.append({"tick": tick, "pressure": pressure, "decision": action, "work_completed": work, "transition_cost_realized": transition, "estimates": copy.deepcopy(estimates)})
        tick += 1

    return {"adaptive": adaptive, "total_realized_cost": round(total, 3), "transition_cost": round(transition_total, 3), "operating_cost": round(operating_total, 3), "delay_cost": round(delay_total, 3), "finish_tick": tick - 1, "observations": observations, "trace": trace}


def memory_probe(data: dict[str, Any]) -> dict[str, Any]:
    host_limit = int(data["host"]["memory_mb"])
    voice = int(data["voice"]["memory_mb"])
    morph = data["morphologies"]["compiled_probe"]
    declared = int(morph["declared_memory_mb"])
    observed = int(morph["actual_memory_mb"])
    before = declared + voice
    after = observed + voice
    return {"host_memory_mb": host_limit, "declared_compiled_mb": declared, "observed_compiled_mb": observed, "voice_mb": voice, "predicted_union_before_probe_mb": before, "predicted_feasible_before_probe": before <= host_limit, "predicted_union_after_probe_mb": after, "operational_feasible_after_probe": after <= host_limit, "map_update": {"declared_memory_mb": declared, "experienced_memory_mb": observed, "operational_memory_mb": observed, "status": "DECLARED_ESTIMATE_OVERRIDDEN_BY_OBSERVATION"}}


def run_new_host(data: dict[str, Any], *, inherit_old_host_map: bool) -> dict[str, Any]:
    spec = data["scenario_new_host"]
    estimates = {"local_to_remote": 4.0, "remote_to_local": 4.0} if inherit_old_host_map else copy.deepcopy(data["transition_prior"])
    current = "local"
    work = 0
    tick = 1
    total = 0.0
    decisions: list[dict[str, Any]] = []

    while work < int(spec["work_units"]):
        pressure = tick in set(int(x) for x in spec["pressures"])
        if pressure:
            remote_est = (0.0 if current == "remote" else float(estimates[transition_key(current, "remote")])) + float(data["morphologies"]["remote"]["operating_cost"])
            choices = [("remote", remote_est), ("idle", float(spec["delay_cost"]))]
        else:
            local_est = (0.0 if current == "local" else float(estimates[transition_key(current, "local")])) + float(data["morphologies"]["local"]["operating_cost"])
            remote_est = (0.0 if current == "remote" else float(estimates[transition_key(current, "remote")])) + float(data["morphologies"]["remote"]["operating_cost"])
            choices = [("local", local_est), ("remote", remote_est)]

        action = min(choices, key=lambda row: (row[1], row[0]))[0]
        before = current
        realized = 0.0
        if action == "idle":
            realized += float(spec["delay_cost"])
        else:
            if action != current:
                realized += float(spec["actual_switch_cost"])
                if not inherit_old_host_map:
                    estimates[transition_key(current, action)] = float(spec["actual_switch_cost"])
                current = action
            realized += float(data["morphologies"][action]["operating_cost"])
            work += 1
        total += realized
        decisions.append({"tick": tick, "pressure": pressure, "before": before, "decision": action, "realized_cost": round(realized, 3), "estimates": copy.deepcopy(estimates)})
        tick += 1

    return {"inherit_old_host_map": inherit_old_host_map, "total_realized_cost": round(total, 3), "finish_tick": tick - 1, "decisions": decisions}


def authority_control() -> dict[str, Any]:
    measured_transition = {"name": "write_records", "possible": True, "measured": True, "confidence": 0.99, "required_authority": "write_records"}
    authority: set[str] = set()
    admissible = measured_transition["required_authority"] in authority
    return {"transition": measured_transition, "authority": sorted(authority), "admissible": admissible, "outcome": "BLOCK" if not admissible else "ALLOW"}


def row_at(result: dict[str, Any], tick: int) -> dict[str, Any]:
    return next(row for row in result["trace"] if int(row["tick"]) == tick)


def main() -> int:
    data = load_manifest()
    sparse_declared = run_sparse(data, adaptive=False)
    sparse_adaptive = run_sparse(data, adaptive=True)
    drift_frozen = run_drift(data, adaptive=False)
    drift_adaptive = run_drift(data, adaptive=True)
    memory = memory_probe(data)
    new_host_wrong = run_new_host(data, inherit_old_host_map=True)
    new_host_scoped = run_new_host(data, inherit_old_host_map=False)
    authority = authority_control()

    checks = {
        "T1_declared_costs_can_cause_repeated_bad_folds": row_at(sparse_declared, 3)["decision"] == "remote" and row_at(sparse_declared, 10)["decision"] == "remote" and sparse_declared["transition_cost"] > sparse_adaptive["transition_cost"],
        "T2_experience_changes_future_scheduling": row_at(sparse_adaptive, 3)["decision"] == "remote" and row_at(sparse_adaptive, 10)["decision"] == "idle" and sparse_adaptive["total_realized_cost"] < sparse_declared["total_realized_cost"],
        "T3_recalibration_tracks_host_drift": row_at(drift_frozen, 12)["decision"] == "remote" and row_at(drift_adaptive, 12)["decision"] == "idle" and drift_adaptive["total_realized_cost"] < drift_frozen["total_realized_cost"],
        "T4_measured_memory_changes_reachability": memory["predicted_feasible_before_probe"] and not memory["operational_feasible_after_probe"] and memory["map_update"]["operational_memory_mb"] == memory["observed_compiled_mb"],
        "T5_calibration_is_host_scoped": new_host_scoped["finish_tick"] < new_host_wrong["finish_tick"] and new_host_scoped["total_realized_cost"] < new_host_wrong["total_realized_cost"],
        "T6_measurement_does_not_manufacture_authority": authority["transition"]["measured"] and authority["transition"]["possible"] and not authority["admissible"] and authority["outcome"] == "BLOCK",
    }

    report = {"experiment": "CP-001", "mode": "SIMULATION_ONLY", "warning": "Synthetic observations test architecture only. They are not real measurements of the user's computer, a model runtime, or a production scheduler.", "sparse_pressure": {"declared_only": sparse_declared, "adaptive": sparse_adaptive}, "drift": {"frozen_map": drift_frozen, "adaptive_recalibration": drift_adaptive}, "memory_probe": memory, "host_specificity": {"incorrectly_inherited_host_A_map": new_host_wrong, "host_B_scoped_calibration": new_host_scoped}, "authority_control": authority, "checks": checks, "overall": "PASS" if all(checks.values()) else "REVIEW_REQUIRED"}
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["overall"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
