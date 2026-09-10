"""IA-001 — Task-Shaped Intelligence Allocation, simulation only.

Compares a universal-frontier baseline with a task-shaped route over a synthetic
mixed workload. Provider costs are abstract and vendor-neutral. Privacy is a
hard gate, not a price. No model/API calls or external actions occur.

Run from modern-robotics/lucian-os:
    py prototype/intelligence_allocator_v001.py
"""
from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST = PROJECT_ROOT / "manifests" / "intelligence_allocation_demo.json"


def load_manifest(path: Path = DEFAULT_MANIFEST) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def profile(data: dict[str, Any], provider: str, task_class: str, mods: dict[str, Any] | None = None) -> dict[str, float] | None:
    record = copy.deepcopy(data["providers"][provider].get("profiles", {}).get(task_class))
    if not record:
        return None
    mods = mods or {}
    success_mult = mods.get("attempt_success_multiplier", {}).get(provider, {}).get(task_class, 1.0)
    quality_mult = mods.get("quality_multiplier", {}).get(provider, {}).get(task_class, 1.0)
    record["attempt_success"] = max(0.05, min(0.999, float(record["attempt_success"]) * success_mult))
    record["quality"] = max(0.0, min(0.999, float(record["quality"]) * quality_mult))
    return record


def base_call_cost(data: dict[str, Any], provider: str, stage: dict[str, Any], context_multiplier: float = 1.0) -> tuple[float, float, float]:
    p = data["providers"][provider]
    input_tokens = float(stage["input_tokens_per_unit"] * stage["units"]) * context_multiplier
    output_tokens = float(stage["output_tokens_per_unit"] * stage["units"])
    fixed = float(p.get("fixed_cost_per_call", 0.0)) * stage["units"]
    cost = fixed + input_tokens / 1000.0 * float(p["input_cost_per_1k"]) + output_tokens / 1000.0 * float(p["output_cost_per_1k"])
    return cost, input_tokens, output_tokens


def admissible(data: dict[str, Any], provider: str, stage: dict[str, Any], privacy: str, mods: dict[str, Any] | None) -> tuple[bool, dict[str, float] | None, str]:
    p = data["providers"][provider]
    pr = profile(data, provider, str(stage["task_class"]), mods)
    if not pr:
        return False, None, "UNSUPPORTED_TASK_CLASS"
    if float(pr["quality"]) < float(stage["min_quality"]):
        return False, pr, "INSUFFICIENT_QUALITY"
    if privacy == "private" and p.get("locality") == "remote":
        return False, pr, "PRIVACY_BLOCKED"
    return True, pr, "ADMISSIBLE"


def expected_stage_cost(data: dict[str, Any], provider: str, stage: dict[str, Any], privacy: str, mods: dict[str, Any] | None = None, context_multiplier: float = 1.0) -> dict[str, Any] | None:
    ok, pr, reason = admissible(data, provider, stage, privacy, mods)
    if not ok or pr is None:
        return None
    base, input_tokens, output_tokens = base_call_cost(data, provider, stage, context_multiplier)
    expected_attempts = 1.0 / float(pr["attempt_success"])
    return {
        "provider": provider,
        "quality": round(float(pr["quality"]), 4),
        "expected_attempts": expected_attempts,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "expected_cost": base * expected_attempts,
        "reason": reason,
    }


def choose_task_shaped(data: dict[str, Any], stage: dict[str, Any], privacy: str, mods: dict[str, Any] | None = None) -> dict[str, Any] | None:
    candidates: list[dict[str, Any]] = []
    for provider in data["providers"]:
        candidate = expected_stage_cost(data, provider, stage, privacy, mods)
        if candidate:
            candidates.append(candidate)
    if not candidates:
        return None
    return min(candidates, key=lambda x: (x["expected_cost"], x["provider"]))


def run_route(
    data: dict[str, Any],
    route: str,
    *,
    mods: dict[str, Any] | None = None,
    privacy_overrides: dict[str, str] | None = None,
    routing_overhead_per_stage: float | None = None,
    frontier_context_multiplier: float = 1.0,
) -> dict[str, Any]:
    privacy_overrides = privacy_overrides or {}
    routing_overhead = float(data["routing_overhead_per_stage"] if routing_overhead_per_stage is None else routing_overhead_per_stage)
    total_cost = 0.0
    frontier_tokens = 0.0
    all_model_tokens = 0.0
    deterministic_operations = 0
    expected_model_calls = 0.0
    complete = True
    stages: list[dict[str, Any]] = []

    for stage in data["stages"]:
        privacy = privacy_overrides.get(str(stage["name"]), str(stage["privacy"]))
        if route == "frontier":
            selected = expected_stage_cost(data, "F3", stage, privacy, mods, frontier_context_multiplier)
            if selected is None:
                complete = False
                stages.append({"stage": stage["name"], "provider": None, "status": "NO_ADMISSIBLE_FRONTIER_ROUTE", "privacy": privacy})
                continue
        elif route == "task_shaped":
            selected = choose_task_shaped(data, stage, privacy, mods)
            if selected is None:
                complete = False
                stages.append({"stage": stage["name"], "provider": None, "status": "NO_COMPETENT_ADMISSIBLE_PROVIDER", "privacy": privacy})
                continue
            selected["expected_cost"] += routing_overhead
        else:
            raise ValueError(f"Unknown route: {route}")

        provider = str(selected["provider"])
        attempts = float(selected["expected_attempts"])
        token_total = (float(selected["input_tokens"]) + float(selected["output_tokens"])) * attempts
        total_cost += float(selected["expected_cost"])

        if provider == "D0":
            deterministic_operations += int(stage["units"])
        else:
            expected_model_calls += float(stage["units"]) * attempts
            all_model_tokens += token_total
        if provider == "F3":
            frontier_tokens += token_total

        stages.append({
            "stage": stage["name"],
            "provider": provider,
            "privacy": privacy,
            "quality": selected["quality"],
            "expected_attempts": round(attempts, 3),
            "expected_cost": round(float(selected["expected_cost"]), 4),
        })

    return {
        "route": route,
        "verified_completion": complete,
        "modeled_total_cost": round(total_cost, 4),
        "frontier_tokens": round(frontier_tokens),
        "all_model_tokens": round(all_model_tokens),
        "expected_model_calls": round(expected_model_calls, 1),
        "deterministic_operations": deterministic_operations,
        "stages": stages,
    }


def scenario(data: dict[str, Any], name: str, **kwargs: Any) -> dict[str, Any]:
    frontier = run_route(data, "frontier", **kwargs)
    shaped = run_route(data, "task_shaped", **kwargs)
    return {
        "scenario": name,
        "frontier": frontier,
        "task_shaped": shaped,
        "cost_difference_task_shaped_minus_frontier": round(shaped["modeled_total_cost"] - frontier["modeled_total_cost"], 4),
    }


def main() -> int:
    data = load_manifest()
    scenarios = [
        scenario(data, "T1_BASE_ROUTINE_WORK"),
        scenario(data, "T3_WEAK_SPECIALIST_RETRY_TRAP", mods={"attempt_success_multiplier": {"S1": {"classification": 0.22}}}),
        scenario(data, "T4_FRONTIER_CONTEXT_DUPLICATION", frontier_context_multiplier=2.0),
        scenario(data, "T5_PRIVATE_CLASSIFICATION", privacy_overrides={"classify_documents": "private"}),
        scenario(data, "T6_ROUTING_OVERHEAD_REVERSAL", routing_overhead_per_stage=13.0),
    ]

    # T2 is embedded in the base workload: ambiguous reasoning and synthesis have
    # quality thresholds that D0/S1/B2 do not meet, so task-shaped routing must
    # escalate those stages to F3 rather than suppress the hard work.
    base = scenarios[0]["task_shaped"]
    stage_provider = {row["stage"]: row.get("provider") for row in base["stages"]}
    t2_pass = stage_provider.get("reason_ambiguous") == "F3" and stage_provider.get("synthesize") == "F3"

    checks = {
        "T1_lower_cost_same_completion": (
            scenarios[0]["task_shaped"]["verified_completion"]
            and scenarios[0]["frontier"]["verified_completion"]
            and scenarios[0]["task_shaped"]["modeled_total_cost"] < scenarios[0]["frontier"]["modeled_total_cost"]
        ),
        "T2_hard_reasoning_escalates": t2_pass,
        "T3_retry_trap_moves_classification_up": any(
            row["stage"] == "classify_documents" and row.get("provider") == "B2"
            for row in scenarios[1]["task_shaped"]["stages"]
        ),
        "T4_context_duplication_penalizes_frontier": scenarios[2]["frontier"]["modeled_total_cost"] > scenarios[0]["frontier"]["modeled_total_cost"],
        "T5_privacy_is_hard_gate": (
            not scenarios[3]["frontier"]["verified_completion"]
            and scenarios[3]["task_shaped"]["verified_completion"]
            and any(row["stage"] == "classify_documents" and row.get("provider") == "B2" for row in scenarios[3]["task_shaped"]["stages"])
        ),
        "T6_frontier_can_win_when_routing_overhead_is_extreme": scenarios[4]["frontier"]["modeled_total_cost"] < scenarios[4]["task_shaped"]["modeled_total_cost"],
    }

    report = {
        "experiment": "IA-001",
        "mode": "SIMULATION_ONLY",
        "cost_units": data["cost_units"],
        "warning": "Synthetic provider qualities and costs are illustrative parameters, not measurements of named commercial models.",
        "scenarios": scenarios,
        "checks": checks,
        "overall": "PASS" if all(checks.values()) else "REVIEW_REQUIRED",
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["overall"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
