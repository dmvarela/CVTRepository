"""IAM-001 — Learning Changes Morphology, simulation only.

Integrates downward compilation with resource scheduling. A recurring task begins
with a reasoning-heavy morphology, may earn a smaller compiled morphology after
verified repetition, and must retract that morphology when drift contradicts it.

The simulation asks whether learning changes which tasks can coexist on the same
unchanged host. No model calls, external actions, permission changes, or device
actions occur.

Run from modern-robotics/lucian-os:
    py prototype/learning_morphology_v001.py
"""
from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST = PROJECT_ROOT / "manifests" / "iam_learning_morphology_demo.json"


def load_manifest(path: Path = DEFAULT_MANIFEST) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def simulate(
    data: dict[str, Any],
    *,
    learning_enabled: bool = True,
    compiled_modules_override: list[str] | None = None,
    authority_revocation: tuple[int, int] | None = None,
    max_ticks: int = 80,
) -> dict[str, Any]:
    host = copy.deepcopy(data["host"])
    modules = {str(m["name"]): copy.deepcopy(m) for m in data["modules"]}
    recurring = data["recurring_task"]
    voice = data["voice_task"]

    pending: list[dict[str, Any]] = []
    current_modules = set(str(x) for x in host.get("resting_modules", []))
    trace: list[dict[str, Any]] = []
    evidence: list[dict[str, Any]] = []
    skill: dict[str, Any] | None = None
    skill_version = 0

    completed_cases = 0
    voice_deadline_misses = 0
    concurrent_ticks = 0
    heavy_executions = 0
    compiled_executions = 0
    compilations = 0
    retractions = 0
    authority_blocks = 0
    authority_violations = 0
    modeled_cost = 0.0
    transition_cost_total = 0

    def resource_usage(names: list[str] | set[str]) -> dict[str, int]:
        selected = set(str(x) for x in names)
        return {
            resource: sum(int(modules[name].get(resource, 0) or 0) for name in selected)
            for resource in ("memory_mb", "cpu_units", "network_units")
        }

    def feasible(names: list[str] | set[str]) -> tuple[bool, dict[str, int]]:
        usage = resource_usage(names)
        limits = host["resources"]
        return (
            all(usage[name] <= int(limits.get(name, 0) or 0) for name in usage),
            usage,
        )

    def transition_cost(target: list[str] | set[str]) -> dict[str, Any]:
        nonlocal current_modules
        target_set = set(str(x) for x in target)
        loads = sorted(target_set - current_modules)
        unloads = sorted(current_modules - target_set)
        load_cost = sum(int(modules[name].get("load_cost", 0) or 0) for name in loads)
        unload_cost = sum(int(modules[name].get("unload_cost", 0) or 0) for name in unloads)
        current_modules = target_set
        return {
            "load": loads,
            "unload": unloads,
            "cost": load_cost + unload_cost,
        }

    last_arrival = int(recurring["case_count"])
    voice_arrivals = set(int(x) for x in voice["arrivals"])

    for tick in range(1, max_ticks + 1):
        if tick <= last_arrival:
            generation = (
                str(recurring["drift_generation"])
                if tick >= int(recurring["drift_case"])
                else str(recurring["initial_generation"])
            )
            pending.append({"case_id": tick, "generation": generation})

        voice_active = tick in voice_arrivals
        authority = set(str(x) for x in host.get("authority", []))
        if authority_revocation and authority_revocation[0] <= tick <= authority_revocation[1]:
            authority.discard(str(recurring["required_authority"]))

        recurring_route: str | None = None
        recurring_modules: list[str] = []
        if pending:
            if str(recurring["required_authority"]) in authority:
                if learning_enabled and skill is not None:
                    recurring_route = "compiled"
                    recurring_modules = list(
                        compiled_modules_override or recurring["compiled_modules"]
                    )
                else:
                    recurring_route = "heavy"
                    recurring_modules = list(recurring["heavy_modules"])
            else:
                authority_blocks += 1

        selected_modules: list[str] = []
        run_voice = False
        run_recurring = False

        # Interactive voice is a hard-start workload in this toy scheduler.
        # The recurring task may coexist only if the union of morphologies fits.
        if voice_active:
            voice_modules = list(voice["modules"])
            voice_ok, _ = feasible(voice_modules)
            if voice_ok:
                run_voice = True
                selected_modules.extend(voice_modules)
            else:
                voice_deadline_misses += 1

            if recurring_route is not None and run_voice:
                both_ok, _ = feasible(set(voice_modules) | set(recurring_modules))
                if both_ok:
                    run_recurring = True
                    selected_modules.extend(recurring_modules)
        elif recurring_route is not None:
            recurring_ok, _ = feasible(recurring_modules)
            if recurring_ok:
                run_recurring = True
                selected_modules.extend(recurring_modules)

        if run_voice and run_recurring:
            concurrent_ticks += 1

        events: list[dict[str, Any]] = []
        executed_case = pending[0]["case_id"] if (run_recurring and pending) else None

        if run_recurring:
            case = pending[0]
            if str(recurring["required_authority"]) not in authority:
                # Defensive assertion path: scheduling should have blocked this already.
                authority_violations += 1
            elif recurring_route == "heavy":
                heavy_executions += 1
                modeled_cost += float(recurring["heavy_cost"])
                completed_cases += 1
                pending.pop(0)
                evidence.append(case)

                if (
                    learning_enabled
                    and skill is None
                    and len(evidence) >= int(recurring["validation_window"])
                ):
                    recent = evidence[-int(recurring["validation_window"]):]
                    generations = {row["generation"] for row in recent}
                    if len(generations) == 1:
                        skill_version += 1
                        skill = {
                            "version": skill_version,
                            "generation": recent[-1]["generation"],
                            "required_authority": recurring["required_authority"],
                        }
                        compilations += 1
                        modeled_cost += float(recurring["compile_cost"])
                        events.append(
                            {
                                "event": "COMPILED",
                                "generation": skill["generation"],
                                "version": skill_version,
                                "required_authority": skill["required_authority"],
                            }
                        )
            elif recurring_route == "compiled":
                compiled_executions += 1
                modeled_cost += float(recurring["compiled_cost"]) + float(
                    recurring["verification_cost"]
                )

                if case["generation"] == skill["generation"]:
                    completed_cases += 1
                    pending.pop(0)
                else:
                    # Truth bites: the stale compiled route loses eligibility.
                    retractions += 1
                    modeled_cost += float(recurring["repair_cost"])
                    events.append(
                        {
                            "event": "RETRACTED",
                            "reason": "verification_contradiction",
                            "old_generation": skill["generation"],
                            "observed_generation": case["generation"],
                        }
                    )
                    skill = None
                    evidence = []

        usage = (
            resource_usage(selected_modules)
            if selected_modules
            else {"memory_mb": 0, "cpu_units": 0, "network_units": 0}
        )
        change = transition_cost(selected_modules)
        transition_cost_total += int(change["cost"])

        trace.append(
            {
                "tick": tick,
                "voice_arrived": voice_active,
                "voice_running": run_voice,
                "recurring_running": run_recurring,
                "recurring_route": recurring_route if run_recurring else None,
                "executed_case": executed_case,
                "pending_cases": len(pending),
                "completed_cases": completed_cases,
                "active_skill": copy.deepcopy(skill),
                "resources": usage,
                "transition": change,
                "events": events,
                "authority_available": str(recurring["required_authority"]) in authority,
            }
        )

        if (
            tick >= last_arrival
            and not pending
            and not any(arrival > tick for arrival in voice_arrivals)
        ):
            break

    return {
        "learning_enabled": learning_enabled,
        "host_resources": copy.deepcopy(host["resources"]),
        "ticks_to_finish": tick,
        "completed_cases": completed_cases,
        "pending_cases": len(pending),
        "voice_deadline_misses": voice_deadline_misses,
        "concurrent_ticks": concurrent_ticks,
        "heavy_executions": heavy_executions,
        "compiled_executions": compiled_executions,
        "compilations": compilations,
        "retractions": retractions,
        "authority_blocks": authority_blocks,
        "authority_violations": authority_violations,
        "modeled_cost": round(modeled_cost, 3),
        "transition_cost_total": transition_cost_total,
        "trace": trace,
    }


def row_at(result: dict[str, Any], tick: int) -> dict[str, Any]:
    return next(row for row in result["trace"] if int(row["tick"]) == tick)


def compact(result: dict[str, Any]) -> dict[str, Any]:
    return {
        key: value
        for key, value in result.items()
        if key != "trace"
    }


def main() -> int:
    data = load_manifest()

    baseline = simulate(data, learning_enabled=False)
    learning = simulate(data, learning_enabled=True)
    no_resource_gain = simulate(
        data,
        learning_enabled=True,
        compiled_modules_override=list(data["recurring_task"]["heavy_modules"]),
    )
    authority = simulate(
        data,
        learning_enabled=True,
        authority_revocation=(10, 12),
    )

    heavy_plus_voice = set(data["recurring_task"]["heavy_modules"]) | set(
        data["voice_task"]["modules"]
    )
    compiled_plus_voice = set(data["recurring_task"]["compiled_modules"]) | set(
        data["voice_task"]["modules"]
    )

    # Recompute the two key union footprints from the manifest.
    modules = {str(m["name"]): m for m in data["modules"]}
    def usage(names: set[str]) -> dict[str, int]:
        return {
            resource: sum(int(modules[name].get(resource, 0) or 0) for name in names)
            for resource in ("memory_mb", "cpu_units", "network_units")
        }

    heavy_voice_usage = usage(heavy_plus_voice)
    compiled_voice_usage = usage(compiled_plus_voice)
    memory_limit = int(data["host"]["resources"]["memory_mb"])

    learning_tick_4 = row_at(learning, 4)
    learning_tick_8 = row_at(learning, 8)
    learning_tick_20 = row_at(learning, 20)
    learning_tick_28 = row_at(learning, 28)

    retraction_events = [
        event
        for row in learning["trace"]
        for event in row["events"]
        if event["event"] == "RETRACTED"
    ]
    v2_compile_events = [
        event
        for row in learning["trace"]
        for event in row["events"]
        if event["event"] == "COMPILED" and event.get("generation") == "v2"
    ]

    revoked_rows = [
        row for row in authority["trace"] if 10 <= int(row["tick"]) <= 12
    ]

    checks = {
        "T1_learning_creates_new_concurrency": (
            baseline["concurrent_ticks"] == 0
            and learning["concurrent_ticks"] > 0
            and learning_tick_8["voice_running"]
            and learning_tick_8["recurring_running"]
            and learning_tick_8["recurring_route"] == "compiled"
        ),
        "T2_same_hardware_different_feasible_set": (
            heavy_voice_usage["memory_mb"] > memory_limit
            and compiled_voice_usage["memory_mb"] <= memory_limit
            and learning_tick_4["voice_running"]
            and not learning_tick_4["recurring_running"]
            and learning_tick_8["voice_running"]
            and learning_tick_8["recurring_running"]
        ),
        "T3_drift_removes_then_recreates_concurrency": (
            len(retraction_events) >= 1
            and not learning_tick_20["recurring_running"]
            and len(v2_compile_events) >= 1
            and learning_tick_28["recurring_running"]
            and learning_tick_28["recurring_route"] == "compiled"
        ),
        "T4_learning_improves_trajectory_under_reference_costs": (
            learning["completed_cases"] == baseline["completed_cases"] == int(data["recurring_task"]["case_count"])
            and learning["voice_deadline_misses"] == baseline["voice_deadline_misses"] == 0
            and learning["ticks_to_finish"] < baseline["ticks_to_finish"]
            and learning["modeled_cost"] < baseline["modeled_cost"]
        ),
        "T5_authority_remains_non_compensatory": (
            authority["authority_blocks"] > 0
            and authority["authority_violations"] == 0
            and all(not row["recurring_running"] for row in revoked_rows)
        ),
        "T6_learning_flag_without_resource_change_does_not_create_concurrency": (
            no_resource_gain["compilations"] > 0
            and no_resource_gain["concurrent_ticks"] == 0
        ),
    }

    report = {
        "experiment": "IAM-001",
        "mode": "SIMULATION_ONLY",
        "warning": (
            "Synthetic resource footprints and costs test architecture only; "
            "they are not measurements of a real model, host, or deployment."
        ),
        "resource_discrimination": {
            "host_memory_mb": memory_limit,
            "heavy_plus_voice": heavy_voice_usage,
            "compiled_plus_voice": compiled_voice_usage,
        },
        "baseline_no_learning": compact(baseline),
        "learning": compact(learning),
        "no_resource_gain_control": compact(no_resource_gain),
        "authority_control": compact(authority),
        "key_learning_trace": [
            row
            for row in learning["trace"]
            if row["voice_arrived"] or row["events"]
        ],
        "checks": checks,
        "overall": "PASS" if all(checks.values()) else "REVIEW_REQUIRED",
    }

    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["overall"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
