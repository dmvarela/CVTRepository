"""MAS-002 — Hysteresis and Lookahead for Morphology Scheduling.

Simulation-only comparison of three policies:
- greedy: choose the cheapest currently feasible running morphology;
- sticky: penalize switching and enforce a short minimum dwell;
- lookahead: optimize a bounded future horizon over operating, transition, and delay cost.

Candidate morphologies are assumed to have already passed capability, authority,
privacy, safety, and competence gates. MAS-002 studies only the scheduling problem
inside that admissible set.

Run from modern-robotics/lucian-os:
    py prototype/morphology_scheduler_v002.py
"""
from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST = PROJECT_ROOT / "manifests" / "mas002_scheduler_policy_demo.json"


def load_manifest(path: Path = DEFAULT_MANIFEST) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def transition_cost(data: dict[str, Any], current: str, target: str) -> float:
    if current == target:
        return 0.0
    return float(data["modes"][current]["unload_cost"]) + float(
        data["modes"][target]["load_cost"]
    )


def feasible(
    data: dict[str, Any],
    mode: str,
    *,
    voice_active: bool,
    compiled_available: bool,
) -> bool:
    if mode == "compiled" and not compiled_available:
        return False
    memory = float(data["modes"][mode]["memory_mb"])
    if voice_active:
        memory += float(data["voice"]["memory_mb"])
    return memory <= float(data["host"]["memory_mb"])


def run_strategy(
    data: dict[str, Any],
    scenario_name: str,
    strategy: str,
) -> dict[str, Any]:
    scenario = data["scenarios"][scenario_name]
    voice_ticks = {int(x) for x in scenario["voice_ticks"]}
    compiled_at = scenario.get("compiled_available_at")
    lookahead_horizon = int(data["scheduler"]["lookahead_horizon"])
    delay_rate = float(data["scheduler"]["delay_cost_per_pending_unit"])
    sticky_dwell = int(data["scheduler"]["sticky_min_dwell"])
    sticky_multiplier = float(data["scheduler"]["sticky_switch_multiplier"])

    remaining = int(scenario["work_units"])
    current = "local"
    dwell = 999
    tick = 1

    operating_cost = 0.0
    switching_cost = 0.0
    delay_cost = 0.0
    switches = 0
    remote_ticks = 0
    idle_ticks = 0
    voice_deadline_misses = 0
    trace: list[dict[str, Any]] = []

    while remaining > 0 and tick < 100:
        voice_active = tick in voice_ticks
        compiled_available = compiled_at is not None and tick >= int(compiled_at)
        choices = [
            mode
            for mode in ("local", "remote", "compiled", "idle")
            if feasible(
                data,
                mode,
                voice_active=voice_active,
                compiled_available=compiled_available,
            )
        ]

        # Voice is an already-admitted hard workload. Feasibility includes its
        # memory demand, so any selected mode preserves the voice start.
        if not choices:
            voice_deadline_misses += int(voice_active)
            raise RuntimeError("No feasible scheduler state")

        if strategy == "greedy":
            running = [mode for mode in choices if mode != "idle"]
            choice = min(
                running,
                key=lambda mode: (
                    float(data["modes"][mode]["operating_cost"]),
                    mode,
                ),
            ) if running else "idle"

        elif strategy == "sticky":
            if current in choices and dwell < sticky_dwell:
                choice = current
            else:
                running = [mode for mode in choices if mode != "idle"]
                choice = min(
                    running,
                    key=lambda mode: (
                        float(data["modes"][mode]["operating_cost"])
                        + sticky_multiplier * transition_cost(data, current, mode),
                        mode,
                    ),
                ) if running else "idle"

        elif strategy == "lookahead":
            @lru_cache(maxsize=None)
            def value(step: int, mode_now: str, work_left: int) -> tuple[float, str]:
                if work_left <= 0:
                    return 0.0, "idle"
                if step >= lookahead_horizon:
                    # Terminal unfinished-work penalty prevents free indefinite delay.
                    return work_left * 1.5, "idle"

                future_tick = tick + step
                future_voice = future_tick in voice_ticks
                future_compiled = (
                    compiled_at is not None and future_tick >= int(compiled_at)
                )
                options = [
                    mode
                    for mode in ("local", "remote", "compiled", "idle")
                    if feasible(
                        data,
                        mode,
                        voice_active=future_voice,
                        compiled_available=future_compiled,
                    )
                ]

                best_cost = float("inf")
                best_mode = "idle"
                for mode in options:
                    progress = 0 if mode == "idle" else 1
                    immediate = (
                        transition_cost(data, mode_now, mode)
                        + float(data["modes"][mode]["operating_cost"])
                        + delay_rate * work_left
                    )
                    future_cost, _ = value(
                        step + 1,
                        mode,
                        max(0, work_left - progress),
                    )
                    candidate = immediate + future_cost
                    if candidate < best_cost - 1e-9 or (
                        abs(candidate - best_cost) < 1e-9 and mode < best_mode
                    ):
                        best_cost = candidate
                        best_mode = mode
                return best_cost, best_mode

            _, choice = value(0, current, remaining)

        else:
            raise ValueError(f"Unknown strategy: {strategy}")

        change_cost = transition_cost(data, current, choice)
        step_operating = float(data["modes"][choice]["operating_cost"])
        step_delay = delay_rate * remaining

        switching_cost += change_cost
        operating_cost += step_operating
        delay_cost += step_delay
        switches += int(choice != current)
        remote_ticks += int(choice == "remote")
        idle_ticks += int(choice == "idle")

        before = remaining
        if choice != "idle":
            remaining -= 1

        trace.append(
            {
                "tick": tick,
                "voice_active": voice_active,
                "compiled_available": compiled_available,
                "from": current,
                "to": choice,
                "transition_cost": round(change_cost, 3),
                "operating_cost": round(step_operating, 3),
                "delay_cost": round(step_delay, 3),
                "remaining_before": before,
                "remaining_after": remaining,
            }
        )

        dwell = dwell + 1 if choice == current else 0
        current = choice
        tick += 1

    contraction_cost = float(data["modes"][current]["unload_cost"])
    switching_cost += contraction_cost
    total_cost = switching_cost + operating_cost + delay_cost

    return {
        "scenario": scenario_name,
        "strategy": strategy,
        "work_complete": remaining == 0,
        "ticks_to_finish": tick - 1,
        "voice_deadline_misses": voice_deadline_misses,
        "switches": switches,
        "remote_ticks": remote_ticks,
        "idle_ticks": idle_ticks,
        "transition_cost": round(switching_cost, 3),
        "operating_cost": round(operating_cost, 3),
        "delay_cost": round(delay_cost, 3),
        "contraction_cost": round(contraction_cost, 3),
        "total_modeled_cost": round(total_cost, 3),
        "trace": trace,
    }


def compact(result: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in result.items() if key != "trace"}


def main() -> int:
    data = load_manifest()
    strategies = ("greedy", "sticky", "lookahead")
    results = {
        scenario: {
            strategy: run_strategy(data, scenario, strategy)
            for strategy in strategies
        }
        for scenario in data["scenarios"]
    }

    clustered = results["clustered_pressure"]
    sparse = results["sparse_pressure"]
    learned = results["learned_morphology"]

    learned_lookahead_modes = {
        row["tick"]: row["to"] for row in learned["lookahead"]["trace"]
    }
    clustered_lookahead_modes = {
        row["tick"]: row["to"] for row in clustered["lookahead"]["trace"]
    }

    checks = {
        "T1_greedy_exposes_thrashing": (
            clustered["greedy"]["switches"] > clustered["lookahead"]["switches"]
            and clustered["greedy"]["transition_cost"] > clustered["lookahead"]["transition_cost"]
        ),
        "T2_clustered_pressure_rewards_short_lookahead": (
            clustered["lookahead"]["total_modeled_cost"] < clustered["greedy"]["total_modeled_cost"]
            and clustered["lookahead"]["total_modeled_cost"] < clustered["sticky"]["total_modeled_cost"]
            and clustered_lookahead_modes.get(3) == "remote"
            and clustered_lookahead_modes.get(4) == "remote"
            and clustered_lookahead_modes.get(5) == "remote"
            and clustered_lookahead_modes.get(6) == "local"
        ),
        "T3_sparse_pressure_can_reward_stickiness": (
            sparse["sticky"]["total_modeled_cost"] < sparse["greedy"]["total_modeled_cost"]
            and sparse["sticky"]["total_modeled_cost"] < sparse["lookahead"]["total_modeled_cost"]
        ),
        "T4_lookahead_can_choose_waiting_over_unnecessary_fold": (
            sparse["lookahead"]["idle_ticks"] == 2
            and sparse["lookahead"]["remote_ticks"] == 0
            and sparse["lookahead"]["ticks_to_finish"] > sparse["greedy"]["ticks_to_finish"]
        ),
        "T5_learned_morphology_changes_future_optimum": (
            learned["lookahead"]["total_modeled_cost"] < learned["greedy"]["total_modeled_cost"]
            and learned["lookahead"]["total_modelled_cost"] if False else True
        ),
        "T6_learned_form_is_taken_when_future_value_justifies_switch": (
            learned_lookahead_modes.get(4) == "remote"
            and learned_lookahead_modes.get(5) == "remote"
            and all(learned_lookahead_modes.get(tick) == "compiled" for tick in range(6, 13))
        ),
        "T7_all_policies_preserve_hard_voice_and_complete_work": all(
            result["work_complete"] and result["voice_deadline_misses"] == 0
            for scenario in results.values()
            for result in scenario.values()
        ),
    }

    # Explicitly evaluate T5 without hiding the comparison behind a single winner.
    checks["T5_learned_morphology_changes_future_optimum"] = (
        learned["lookahead"]["total_modeled_cost"] < learned["greedy"]["total_modeled_cost"]
        and learned["lookahead"]["total_modeled_cost"] < learned["sticky"]["total_modeled_cost"]
    )

    report = {
        "experiment": "MAS-002",
        "mode": "SIMULATION_ONLY",
        "warning": (
            "Synthetic costs and resource footprints test scheduling distinctions only. "
            "Candidate morphologies are assumed to have already passed Lucian OS admissibility gates."
        ),
        "results": {
            scenario: {strategy: compact(result) for strategy, result in values.items()}
            for scenario, values in results.items()
        },
        "key_traces": {
            "clustered_lookahead": clustered["lookahead"]["trace"],
            "sparse_lookahead": sparse["lookahead"]["trace"],
            "learned_lookahead": learned["lookahead"]["trace"],
        },
        "checks": checks,
        "overall": "PASS" if all(checks.values()) else "REVIEW_REQUIRED",
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["overall"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
