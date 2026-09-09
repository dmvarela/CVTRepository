"""Lucian OS Morphology Allocation & Scheduling v0.01.

Simulation only.

Purpose:
- consume tasks that already expose candidate morphologies;
- reject candidates that violate authority or privacy;
- account for shared modules by set union rather than duplicate task cost;
- choose feasible coexisting task/morphology assignments under resource limits;
- preserve hard interactive start commitments before soft optimization;
- record morphology transition cost and final contraction cost;
- expose the current myopic scheduler's thrashing / lookahead limitations.

Run from modern-robotics/lucian-os:

    py prototype/morphology_scheduler_v001.py

No device actions, network calls, permission changes, or remote model calls occur.
"""

from __future__ import annotations

import copy
import itertools
import json
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST = PROJECT_ROOT / "manifests" / "morphology_scheduler_demo.json"


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def index_modules(data: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {str(module["name"]): module for module in data.get("modules", [])}


def candidate_admissibility(
    task: dict[str, Any],
    candidate: dict[str, Any],
    host: dict[str, Any],
    modules: dict[str, dict[str, Any]],
) -> tuple[bool, list[str]]:
    authority = set(str(x) for x in host.get("authority", []))
    required_authority: set[str] = set()
    uses_remote = False
    reasons: list[str] = []

    for module_name in candidate.get("modules", []):
        module = modules[str(module_name)]
        required_authority.update(str(x) for x in module.get("authority", []))
        uses_remote = uses_remote or bool(module.get("remote", False))

    missing_authority = sorted(required_authority - authority)
    if missing_authority:
        reasons.append(f"missing authority: {missing_authority}")

    deny_remote_for = set(
        str(x)
        for x in host.get("privacy_policy", {}).get("deny_remote_for", [])
    )
    if uses_remote and str(task.get("privacy", "public")) in deny_remote_for:
        reasons.append("remote morphology prohibited by task privacy class")

    return (not reasons), reasons


def resource_usage(
    module_names: set[str],
    modules: dict[str, dict[str, Any]],
) -> dict[str, int]:
    usage = {"memory_mb": 0, "cpu_units": 0, "network_units": 0}
    for module_name in module_names:
        module = modules[module_name]
        for resource_name in usage:
            usage[resource_name] += int(module.get(resource_name, 0) or 0)
    return usage


def transition_cost(
    current: set[str],
    target: set[str],
    modules: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    loads = sorted(target - current)
    unloads = sorted(current - target)
    load_cost = sum(int(modules[name].get("load_cost", 0) or 0) for name in loads)
    unload_cost = sum(int(modules[name].get("unload_cost", 0) or 0) for name in unloads)
    return {
        "load": loads,
        "unload": unloads,
        "load_cost": load_cost,
        "unload_cost": unload_cost,
        "total": load_cost + unload_cost,
    }


def assignment_resources(
    assignment: dict[str, dict[str, Any] | None],
    host: dict[str, Any],
    modules: dict[str, dict[str, Any]],
) -> tuple[bool, set[str], dict[str, int], int]:
    selected_modules: set[str] = set()
    external_cost = 0

    for candidate in assignment.values():
        if candidate is None:
            continue
        selected_modules.update(str(x) for x in candidate.get("modules", []))
        external_cost += int(candidate.get("external_cost", 0) or 0)

    usage = resource_usage(selected_modules, modules)
    limits = host.get("resources", {})
    feasible = all(
        usage[name] <= int(limits.get(name, 0) or 0)
        for name in usage
    )
    return feasible, selected_modules, usage, external_cost


def enumerate_feasible_assignments(
    active_tasks: list[dict[str, Any]],
    host: dict[str, Any],
    modules: dict[str, dict[str, Any]],
) -> list[tuple[dict[str, dict[str, Any] | None], set[str], dict[str, int], int]]:
    option_sets: list[tuple[dict[str, Any], list[dict[str, Any] | None]]] = []

    for task in active_tasks:
        options: list[dict[str, Any] | None] = [None]
        for candidate in task.get("candidates", []):
            admissible, _ = candidate_admissibility(task, candidate, host, modules)
            if admissible:
                options.append(candidate)
        option_sets.append((task, options))

    results = []
    for picks in itertools.product(*(options for _, options in option_sets)):
        assignment = {
            str(option_sets[index][0]["id"]): picks[index]
            for index in range(len(option_sets))
        }
        feasible, selected_modules, usage, external_cost = assignment_resources(
            assignment,
            host,
            modules,
        )
        if feasible:
            results.append((assignment, selected_modules, usage, external_cost))

    return results


def assignment_rank(
    *,
    tick: int,
    active_tasks: list[dict[str, Any]],
    states: dict[str, dict[str, Any]],
    assignment: dict[str, dict[str, Any] | None],
    selected_modules: set[str],
    usage: dict[str, int],
    external_cost: int,
    current_modules: set[str],
    modules: dict[str, dict[str, Any]],
) -> tuple[tuple[Any, ...], dict[str, Any]]:
    hard_start_violations = 0
    interactive_service = 0
    useful_service = 0.0

    for task in active_tasks:
        task_id = str(task["id"])
        candidate = assignment[task_id]
        state = states[task_id]

        if task.get("latency_class") == "interactive" and state["started_at"] is None:
            max_delay = int(task.get("max_start_delay", 999999))
            if tick - int(task.get("arrival", 0)) >= max_delay and candidate is None:
                hard_start_violations += 1
            if candidate is not None:
                interactive_service += 1

        if candidate is not None:
            age = max(0, tick - int(task.get("arrival", 0)))
            useful_service += float(task.get("priority", 1)) + (0.1 * age)

    change = transition_cost(current_modules, selected_modules, modules)

    # Lexicographic ordering. Hard constraints were already filtered before this.
    # Here we preserve interactive commitments, then maximize service, then prefer
    # lower external cost and lower reconfiguration cost.
    rank = (
        -hard_start_violations,
        interactive_service,
        useful_service,
        -external_cost,
        -change["total"],
        -usage["memory_mb"],
    )

    detail = {
        "hard_start_violations": hard_start_violations,
        "interactive_service": interactive_service,
        "useful_service": useful_service,
        "external_cost": external_cost,
        "transition": change,
    }
    return rank, detail


def candidate_audit(
    data: dict[str, Any],
    host: dict[str, Any],
) -> list[dict[str, Any]]:
    modules = index_modules(data)
    audit: list[dict[str, Any]] = []
    for task in data.get("tasks", []):
        for candidate in task.get("candidates", []):
            admissible, reasons = candidate_admissibility(task, candidate, host, modules)
            audit.append(
                {
                    "task": task.get("id"),
                    "candidate": candidate.get("name"),
                    "admissible": admissible,
                    "reasons": reasons,
                }
            )
    return audit


def run_schedule(
    data: dict[str, Any],
    *,
    memory_override: int | None = None,
    max_ticks: int = 12,
) -> dict[str, Any]:
    host = copy.deepcopy(data["host"])
    if memory_override is not None:
        host["resources"]["memory_mb"] = max(0, int(memory_override))

    modules = index_modules(data)
    tasks = {str(task["id"]): copy.deepcopy(task) for task in data.get("tasks", [])}
    states = {
        task_id: {
            "remaining": int(task["work_ticks"]),
            "started_at": None,
            "completed_at": None,
            "wait_ticks": 0,
        }
        for task_id, task in tasks.items()
    }

    current_modules = set(str(x) for x in host.get("resting_modules", []))
    trace: list[dict[str, Any]] = []

    for tick in range(max_ticks):
        active_tasks = [
            task
            for task in tasks.values()
            if int(task.get("arrival", 0)) <= tick and states[str(task["id"])]["remaining"] > 0
        ]

        if not active_tasks:
            if all(state["remaining"] <= 0 for state in states.values()):
                break
            trace.append(
                {
                    "tick": tick,
                    "running": [],
                    "morphologies": {},
                    "modules": sorted(current_modules),
                    "note": "no arrived unfinished task",
                }
            )
            continue

        feasible = enumerate_feasible_assignments(active_tasks, host, modules)
        ranked: list[tuple[tuple[Any, ...], dict[str, Any], dict[str, Any], set[str], dict[str, int]]] = []

        for assignment, selected_modules, usage, external_cost in feasible:
            rank, rank_detail = assignment_rank(
                tick=tick,
                active_tasks=active_tasks,
                states=states,
                assignment=assignment,
                selected_modules=selected_modules,
                usage=usage,
                external_cost=external_cost,
                current_modules=current_modules,
                modules=modules,
            )
            ranked.append((rank, rank_detail, assignment, selected_modules, usage))

        ranked.sort(key=lambda row: row[0], reverse=True)
        rank, rank_detail, assignment, selected_modules, usage = ranked[0]

        running: list[str] = []
        morphologies: dict[str, str] = {}
        for task in active_tasks:
            task_id = str(task["id"])
            candidate = assignment[task_id]
            if candidate is None:
                states[task_id]["wait_ticks"] += 1
                continue

            if states[task_id]["started_at"] is None:
                states[task_id]["started_at"] = tick

            states[task_id]["remaining"] -= 1
            if states[task_id]["remaining"] == 0:
                states[task_id]["completed_at"] = tick + 1

            running.append(task_id)
            morphologies[task_id] = str(candidate["name"])

        trace.append(
            {
                "tick": tick,
                "running": running,
                "morphologies": morphologies,
                "modules": sorted(selected_modules),
                "resources": usage,
                "rank": list(rank),
                "rank_detail": rank_detail,
            }
        )
        current_modules = set(selected_modules)

    resting = set(str(x) for x in host.get("resting_modules", []))
    contraction = transition_cost(current_modules, resting, modules)

    return {
        "architecture": "morphology-allocation-scheduler-v0.01",
        "mode": "SIMULATION_ONLY",
        "host": host,
        "candidate_audit": candidate_audit(data, host),
        "trace": trace,
        "task_states": states,
        "final_contraction": contraction,
        "all_tasks_complete": all(state["remaining"] <= 0 for state in states.values()),
        "known_limitation": (
            "The scheduler is one-step/myopic. Temporary pressure can cause morphology switching "
            "that a lookahead or hysteresis policy might avoid."
        ),
    }


def summarize(result: dict[str, Any]) -> dict[str, Any]:
    return {
        "memory_mb": result["host"]["resources"]["memory_mb"],
        "all_tasks_complete": result["all_tasks_complete"],
        "task_states": result["task_states"],
        "trace": [
            {
                "tick": row["tick"],
                "running": row.get("running", []),
                "morphologies": row.get("morphologies", {}),
                "modules": row.get("modules", []),
                "resources": row.get("resources"),
                "transition": row.get("rank_detail", {}).get("transition"),
            }
            for row in result["trace"]
        ],
        "final_contraction": result["final_contraction"],
    }


def main() -> int:
    data = load_json(DEFAULT_MANIFEST)

    base = run_schedule(data, memory_override=768)
    pressure = run_schedule(data, memory_override=700)
    privacy_pressure = run_schedule(data, memory_override=620, max_ticks=10)

    remote_index_audit = [
        row
        for row in privacy_pressure["candidate_audit"]
        if row["task"] == "index" and row["candidate"] == "remote_index"
    ]

    report = {
        "experiment": "MAS-001",
        "mode": "SIMULATION_ONLY",
        "base_768mb": summarize(base),
        "pressure_700mb": summarize(pressure),
        "privacy_pressure_620mb": summarize(privacy_pressure),
        "privacy_control": remote_index_audit,
        "interpretation": {
            "base": (
                "The research and voice tasks can coexist by sharing local_reasoner; "
                "background indexing waits until CPU becomes available."
            ),
            "pressure": (
                "Temporary memory pressure can trigger an alternative research morphology "
                "while preserving the interactive local voice morphology."
            ),
            "privacy": (
                "When memory is too small for the private indexing morphology, the scheduler "
                "must not use the remote indexing candidate because privacy is a hard constraint."
            ),
            "warning": (
                "A myopic scheduler may switch a task away from and then back to a morphology. "
                "MAS-002 should test lookahead / hysteresis rather than hiding this behavior."
            ),
        },
    }

    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
