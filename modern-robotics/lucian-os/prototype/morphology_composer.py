"""Elastic Computational Morphology v0.01 — simulation-only composer.

This prototype tests a narrow Lucian OS claim:

    A host should be treated as a set of affordances from which a bounded,
    task-specific morphology can be composed, rather than as pass/fail hardware.

It does NOT execute device actions, download modules, grant permissions, or call
remote AI. It only composes declared demo modules against declared demo hosts.

Examples (run from modern-robotics/lucian-os):

    py prototype/morphology_composer.py --host old-radio-demo --task speak_with_user
    py prototype/morphology_composer.py --host laptop-demo --task organize_files
    py prototype/morphology_composer.py --host vacuum-demo --task clean_floor
    py prototype/morphology_composer.py --host robot-demo --task pick_up_object

Pressure / counterfactual tests:

    py prototype/morphology_composer.py --host old-radio-demo --task speak_with_user --remove-affordance network_uplink
    py prototype/morphology_composer.py --host vacuum-demo --task clean_floor --deny-authority physical_actuation
    py prototype/morphology_composer.py --host laptop-demo --task research_question --memory-mb 256

The output explicitly keeps feasibility, authority, resource sufficiency, routing,
and contraction separate.
"""

from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path
from typing import Any, Iterable


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DEMO = PROJECT_ROOT / "manifests" / "elastic_demo_hosts.json"


class CompositionFailure(Exception):
    """Internal signal used while exploring candidate morphologies."""


def load_demo(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def index_by_name(items: Iterable[dict[str, Any]], key: str = "name") -> dict[str, dict[str, Any]]:
    return {str(item[key]): item for item in items}


def find_host(data: dict[str, Any], host_id: str) -> dict[str, Any]:
    hosts = {h["id"]: h for h in data.get("embodiments", [])}
    if host_id not in hosts:
        raise KeyError(f"Unknown host {host_id!r}. Available: {', '.join(sorted(hosts))}")
    return copy.deepcopy(hosts[host_id])


def find_task(data: dict[str, Any], task_name: str) -> dict[str, Any]:
    tasks = data.get("task_profiles", {})
    if task_name not in tasks:
        raise KeyError(f"Unknown task {task_name!r}. Available: {', '.join(sorted(tasks))}")
    return copy.deepcopy(tasks[task_name])


def module_memory(module: dict[str, Any]) -> int:
    return int(module.get("cost", {}).get("memory_mb", 0) or 0)


def total_memory(selected: set[str], modules: dict[str, dict[str, Any]]) -> int:
    return sum(module_memory(modules[name]) for name in selected)


def provided_functions(selected: set[str], modules: dict[str, dict[str, Any]]) -> set[str]:
    provided: set[str] = set()
    for name in selected:
        provided.update(str(x) for x in modules[name].get("provides", []))
    return provided


def candidate_score(module: dict[str, Any]) -> tuple[int, int, str]:
    """Prefer local, then lower-memory, then deterministic stable ordering."""
    return (
        1 if module.get("remote", False) else 0,
        module_memory(module),
        str(module.get("name", "")),
    )


def raw_candidate_blockers(
    module: dict[str, Any],
    host: dict[str, Any],
    selected: set[str],
    modules: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    affordances = set(str(x) for x in host.get("affordances", []))
    authority = set(str(x) for x in host.get("authority", []))
    required_affordances = set(str(x) for x in module.get("requires_affordances", []))
    required_authority = set(str(x) for x in module.get("authority", []))

    memory_limit = int(host.get("resources", {}).get("memory_mb", 0) or 0)
    projected = total_memory(selected | {str(module["name"])}, modules)

    return {
        "missing_affordances": sorted(required_affordances - affordances),
        "missing_authority": sorted(required_authority - authority),
        "memory_required_mb": projected,
        "memory_available_mb": memory_limit,
        "memory_blocked": bool(memory_limit and projected > memory_limit),
    }


def resolve_function(
    function_name: str,
    *,
    host: dict[str, Any],
    modules: dict[str, dict[str, Any]],
    providers: dict[str, list[str]],
    selected: set[str],
    stack: tuple[str, ...] = (),
) -> set[str]:
    if function_name in provided_functions(selected, modules):
        return set(selected)

    if function_name in stack:
        raise CompositionFailure(f"dependency cycle while resolving {function_name}")

    candidate_names = providers.get(function_name, [])
    if not candidate_names:
        raise CompositionFailure(f"no module provides {function_name}")

    ordered = sorted((modules[name] for name in candidate_names), key=candidate_score)

    for module in ordered:
        blockers = raw_candidate_blockers(module, host, selected, modules)
        if blockers["missing_affordances"] or blockers["missing_authority"]:
            continue

        tentative = set(selected)
        dependency_failed = False
        for dependency in module.get("requires_functions", []):
            try:
                tentative = resolve_function(
                    str(dependency),
                    host=host,
                    modules=modules,
                    providers=providers,
                    selected=tentative,
                    stack=stack + (function_name,),
                )
            except CompositionFailure:
                dependency_failed = True
                break

        if dependency_failed:
            continue

        tentative.add(str(module["name"]))
        memory_limit = int(host.get("resources", {}).get("memory_mb", 0) or 0)
        if memory_limit and total_memory(tentative, modules) > memory_limit:
            continue

        return tentative

    raise CompositionFailure(f"no admissible composition found for {function_name}")


def diagnose_function(
    function_name: str,
    *,
    host: dict[str, Any],
    modules: dict[str, dict[str, Any]],
    providers: dict[str, list[str]],
    selected: set[str],
) -> dict[str, Any]:
    diagnoses: list[dict[str, Any]] = []
    for module_name in providers.get(function_name, []):
        module = modules[module_name]
        blockers = raw_candidate_blockers(module, host, selected, modules)
        diagnoses.append(
            {
                "module": module_name,
                "remote": bool(module.get("remote", False)),
                **blockers,
                "requires_functions": list(module.get("requires_functions", [])),
            }
        )

    if not diagnoses:
        return {
            "function": function_name,
            "status": "NO_PROVIDER_DECLARED",
            "candidates": [],
        }

    authority_only = any(
        not d["missing_affordances"] and d["missing_authority"] and not d["memory_blocked"]
        for d in diagnoses
    )
    physical_gap = all(bool(d["missing_affordances"]) for d in diagnoses)
    resource_gap = any(d["memory_blocked"] for d in diagnoses)

    if authority_only:
        status = "PHYSICALLY_POSSIBLE_BUT_NOT_AUTHORIZED"
    elif physical_gap:
        status = "MISSING_AFFORDANCE"
    elif resource_gap:
        status = "RESOURCE_CONSTRAINED_OR_DEPENDENCY_BLOCKED"
    else:
        status = "DEPENDENCY_OR_COMPOSITION_BLOCKED"

    return {
        "function": function_name,
        "status": status,
        "candidates": diagnoses,
    }


def compose(data: dict[str, Any], host: dict[str, Any], task_name: str, task: dict[str, Any]) -> dict[str, Any]:
    modules = index_by_name(data.get("module_registry", []))

    providers: dict[str, list[str]] = {}
    for module_name, module in modules.items():
        for function_name in module.get("provides", []):
            providers.setdefault(str(function_name), []).append(module_name)

    resting = set(str(x) for x in host.get("resting_modules", []))
    selected = set(resting)
    unmet: list[str] = []
    diagnostics: list[dict[str, Any]] = []

    for demand in task.get("demands", []):
        demand = str(demand)
        try:
            selected = resolve_function(
                demand,
                host=host,
                modules=modules,
                providers=providers,
                selected=selected,
            )
        except CompositionFailure:
            unmet.append(demand)
            diagnostics.append(
                diagnose_function(
                    demand,
                    host=host,
                    modules=modules,
                    providers=providers,
                    selected=selected,
                )
            )

    selected_modules = [modules[name] for name in sorted(selected)]
    remote_modules = sorted(
        str(m["name"]) for m in selected_modules if m.get("remote", False)
    )
    local_modules = sorted(
        str(m["name"]) for m in selected_modules if not m.get("remote", False)
    )
    temporary = sorted(selected - resting)

    required_authority = sorted(
        {
            str(scope)
            for module in selected_modules
            for scope in module.get("authority", [])
        }
    )

    return {
        "ecm_version": "0.01",
        "mode": "SIMULATION_ONLY",
        "host": {
            "id": host.get("id"),
            "type": host.get("type"),
            "resources": host.get("resources", {}),
            "affordances": sorted(str(x) for x in host.get("affordances", [])),
            "authority": sorted(str(x) for x in host.get("authority", [])),
        },
        "task": {
            "name": task_name,
            "description": task.get("description"),
            "demands": list(task.get("demands", [])),
        },
        "resting_morphology": sorted(resting),
        "chosen_morphology": {
            "modules": sorted(selected),
            "local_modules": local_modules,
            "recruited_remote_modules": remote_modules,
            "provided_functions": sorted(provided_functions(selected, modules)),
            "memory_cost_mb": total_memory(selected, modules),
            "required_authority": required_authority,
        },
        "unmet_demands": unmet,
        "diagnostics": diagnostics,
        "disposition": "VIABLE_MORPHOLOGY" if not unmet else "NO_COMPLETE_ADMISSIBLE_MORPHOLOGY",
        "selection_rule": (
            "Prefer the least-memory local admissible provider; recruit remote modules only "
            "when local composition is unavailable. Capability never manufactures authority."
        ),
        "contraction_plan": {
            "unload_after_task": temporary,
            "close_remote_connections": remote_modules,
            "return_to_modules": sorted(resting),
            "authority_note": "No authority was granted by composition; host authority remains external input.",
            "preserve": ["task provenance", "verification result", "unresolved state"],
        },
        "execution": "NONE",
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Lucian OS Elastic Morphology Composer v0.01")
    parser.add_argument("--manifest", type=Path, default=DEFAULT_DEMO)
    parser.add_argument("--host", required=True)
    parser.add_argument("--task", required=True)
    parser.add_argument(
        "--remove-affordance",
        action="append",
        default=[],
        help="Counterfactual: remove a declared host affordance (repeatable).",
    )
    parser.add_argument(
        "--deny-authority",
        action="append",
        default=[],
        help="Counterfactual: remove a declared authority scope (repeatable).",
    )
    parser.add_argument(
        "--memory-mb",
        type=int,
        default=None,
        help="Counterfactual: override available host memory.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    data = load_demo(args.manifest)
    host = find_host(data, args.host)
    task = find_task(data, args.task)

    if args.remove_affordance:
        removed = set(args.remove_affordance)
        host["affordances"] = [x for x in host.get("affordances", []) if x not in removed]

    if args.deny_authority:
        denied = set(args.deny_authority)
        host["authority"] = [x for x in host.get("authority", []) if x not in denied]

    if args.memory_mb is not None:
        host.setdefault("resources", {})["memory_mb"] = max(0, args.memory_mb)

    result = compose(data, host, args.task, task)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["disposition"] == "VIABLE_MORPHOLOGY" else 2


if __name__ == "__main__":
    raise SystemExit(main())
