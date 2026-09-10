"""IA-002 — Downward Compilation and Repeated Reasoning, simulation only.

Tests when repeated frontier reasoning should become a bounded reusable skill, and
when compilation should be delayed, retracted, or blocked. No external calls,
device actions, or permission changes occur.

Run from modern-robotics/lucian-os:
    py prototype/downward_compilation_v001.py
"""
from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST = PROJECT_ROOT / "manifests" / "downward_compilation_demo.json"


def load_manifest(path: Path = DEFAULT_MANIFEST) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def build_stream(spec: dict[str, Any]) -> list[dict[str, Any]]:
    horizon = int(spec["horizon"])
    edge_every = int(spec.get("edge_every", 0))
    drift_at = spec.get("drift_at")
    base_generation = str(spec.get("generation", "v1"))
    drift_generation = str(spec.get("drift_generation", "v2"))
    stream: list[dict[str, Any]] = []
    for idx in range(1, horizon + 1):
        generation = drift_generation if drift_at is not None and idx >= int(drift_at) else base_generation
        kind = "edge" if edge_every and idx % edge_every == 0 and generation == base_generation else "ordinary"
        stream.append({"kind": kind, "generation": generation})
    return stream


def run_reason_every_time(
    stream: list[dict[str, Any]],
    data: dict[str, Any],
    *,
    authority_schedule: dict[int, bool] | None = None,
) -> dict[str, Any]:
    total_cost = 0.0
    frontier_tokens = 0
    verified_complete = 0
    authority_blocks = 0
    for idx, _case in enumerate(stream, start=1):
        total_cost += float(data["frontier"]["cost_per_case"])
        frontier_tokens += int(data["frontier"]["tokens_per_case"])
        allowed = True if authority_schedule is None else bool(authority_schedule.get(idx, True))
        if allowed:
            verified_complete += 1
        else:
            authority_blocks += 1
    return {
        "strategy": "reason_every_time",
        "modeled_total_cost": round(total_cost, 3),
        "frontier_tokens": frontier_tokens,
        "verified_complete": verified_complete,
        "authority_blocks": authority_blocks,
    }


def run_specialist_every_time(stream: list[dict[str, Any]], data: dict[str, Any]) -> dict[str, Any]:
    total_cost = 0.0
    model_tokens = 0
    verified_complete = 0
    quality_failures = 0
    required_quality = float(data["specialist"]["required_quality"])
    for case in stream:
        total_cost += float(data["specialist"]["cost_per_case"])
        model_tokens += int(data["specialist"]["tokens_per_case"])
        quality = float(data["specialist"]["quality_by_kind"].get(case["kind"], 0.0))
        if quality >= required_quality:
            verified_complete += 1
        else:
            quality_failures += 1
    return {
        "strategy": "specialist_every_time",
        "modeled_total_cost": round(total_cost, 3),
        "model_tokens": model_tokens,
        "verified_complete": verified_complete,
        "quality_failures": quality_failures,
    }


def run_compile_downward(
    stream: list[dict[str, Any]],
    data: dict[str, Any],
    *,
    validation_window: int | None = None,
    compile_cost: float | None = None,
    audit_every: int | None = None,
    authority_schedule: dict[int, bool] | None = None,
    economic_gate: bool = True,
) -> dict[str, Any]:
    cfg = copy.deepcopy(data["compiled"])
    if validation_window is not None:
        cfg["validation_window"] = int(validation_window)
    if compile_cost is not None:
        cfg["compile_cost"] = float(compile_cost)
    if audit_every is not None:
        cfg["audit_every"] = int(audit_every)

    total_cost = 0.0
    frontier_tokens = 0
    frontier_cases = 0
    verified_complete = 0
    evidence: list[dict[str, Any]] = []
    skill: dict[str, Any] | None = None
    last_status = "none"

    compiled_executions = 0
    audits = 0
    retractions = 0
    false_compilations = 0
    out_of_contract_escalations = 0
    authority_blocks = 0
    break_even_recurrence: int | None = None
    events: list[dict[str, Any]] = []

    def maybe_compile(index: int) -> None:
        nonlocal skill, last_status, total_cost, false_compilations
        window = int(cfg["validation_window"])
        if skill is not None or len(evidence) < window:
            return

        recent = evidence[-window:]
        generations = [row["generation"] for row in recent if row["kind"] != "edge"]
        if not generations:
            return

        generation = max(set(generations), key=generations.count)
        remaining = len(stream) - index + 1
        expected_compiled_case_cost = (
            float(cfg["execution_cost"])
            + float(cfg["verification_cost"])
            + float(cfg["audit_cost"]) / max(1, int(cfg["audit_every"]))
        )
        saved_per_case = float(data["frontier"]["cost_per_case"]) - expected_compiled_case_cost

        if economic_gate and (
            saved_per_case <= 0
            or remaining * saved_per_case <= float(cfg["compile_cost"])
        ):
            return

        scope_reliable = window >= int(cfg["scope_evidence_required"])
        total_cost += float(cfg["compile_cost"])
        skill = {
            "version": retractions + 1,
            "generation": generation,
            "scope_reliable": scope_reliable,
            "required_authority": data["task"]["required_authority"],
        }
        last_status = "active"
        if not scope_reliable:
            false_compilations += 1
        events.append({
            "at": index,
            "event": "COMPILED",
            "version": skill["version"],
            "generation": generation,
            "scope_reliable": scope_reliable,
            "required_authority": skill["required_authority"],
        })

    for idx, case in enumerate(stream, start=1):
        allowed = True if authority_schedule is None else bool(authority_schedule.get(idx, True))
        reason_every_time_cost_so_far = idx * float(data["frontier"]["cost_per_case"])

        if skill is None:
            total_cost += float(data["frontier"]["cost_per_case"])
            frontier_tokens += int(data["frontier"]["tokens_per_case"])
            frontier_cases += 1
            if allowed:
                verified_complete += 1
            else:
                authority_blocks += 1
                events.append({"at": idx, "event": "AUTHORITY_BLOCKED", "route": "frontier_execution"})
            evidence.append(case)
            maybe_compile(idx)
        else:
            # With enough evidence, the skill learns a bounded scope detector and
            # escalates rare edge cases before executing the compiled transform.
            if case["kind"] == "edge" and bool(skill["scope_reliable"]):
                out_of_contract_escalations += 1
                total_cost += float(data["frontier"]["cost_per_case"])
                frontier_tokens += int(data["frontier"]["tokens_per_case"])
                frontier_cases += 1
                if allowed:
                    verified_complete += 1
                else:
                    authority_blocks += 1
                    events.append({"at": idx, "event": "AUTHORITY_BLOCKED", "route": "edge_escalation"})
                evidence.append(case)
                events.append({"at": idx, "event": "OUT_OF_CONTRACT_ESCALATION"})
                continue

            # Compilation never changes authority. A cheap skill does not inherit
            # broader permission from repetition or validation.
            if not allowed:
                authority_blocks += 1
                events.append({
                    "at": idx,
                    "event": "AUTHORITY_BLOCKED",
                    "route": "compiled_skill",
                    "required_authority": skill["required_authority"],
                })
                continue

            total_cost += float(cfg["execution_cost"]) + float(cfg["verification_cost"])
            compiled_executions += 1
            if int(cfg["audit_every"]) > 0 and compiled_executions % int(cfg["audit_every"]) == 0:
                total_cost += float(cfg["audit_cost"])
                audits += 1

            valid = case["kind"] == "ordinary" and case["generation"] == skill["generation"]
            if valid:
                verified_complete += 1
            else:
                # Truth bites: verification contradiction removes the skill from
                # routing eligibility and returns the case to stronger reasoning.
                retractions += 1
                last_status = "retracted"
                total_cost += float(cfg["repair_cost"]) + float(data["frontier"]["cost_per_case"])
                frontier_tokens += int(data["frontier"]["tokens_per_case"])
                frontier_cases += 1
                verified_complete += 1
                events.append({
                    "at": idx,
                    "event": "RETRACTED",
                    "reason": "verification_contradiction",
                    "old_generation": skill["generation"],
                    "observed_generation": case["generation"],
                    "case_kind": case["kind"],
                })
                evidence = [case]
                skill = None

        if break_even_recurrence is None and skill is not None and total_cost <= reason_every_time_cost_so_far:
            break_even_recurrence = idx

    return {
        "strategy": "compile_downward",
        "modeled_total_cost": round(total_cost, 3),
        "frontier_tokens": frontier_tokens,
        "frontier_cases": frontier_cases,
        "verified_complete": verified_complete,
        "compiled_executions": compiled_executions,
        "audits": audits,
        "retractions": retractions,
        "false_compilations": false_compilations,
        "out_of_contract_escalations": out_of_contract_escalations,
        "authority_blocks": authority_blocks,
        "break_even_recurrence": break_even_recurrence,
        "final_skill_status": "active" if skill is not None else last_status,
        "final_skill": skill,
        "events": events,
    }


def main() -> int:
    data = load_manifest()
    stable = build_stream(data["scenarios"]["stable"])
    drift = build_stream(data["scenarios"]["drift"])
    short = build_stream(data["scenarios"]["short"])

    stable_reason = run_reason_every_time(stable, data)
    stable_specialist = run_specialist_every_time(stable, data)
    stable_compile = run_compile_downward(stable, data)

    premature = run_compile_downward(
        stable,
        data,
        validation_window=2,
        economic_gate=False,
    )

    drift_compile = run_compile_downward(drift, data)

    short_compile = run_compile_downward(
        short,
        data,
        validation_window=3,
        compile_cost=20.0,
        economic_gate=True,
    )

    authority_stream = [{"kind": "ordinary", "generation": "v1"} for _ in range(30)]
    authority_schedule = {idx: idx < 16 for idx in range(1, 31)}
    authority_compile = run_compile_downward(
        authority_stream,
        data,
        authority_schedule=authority_schedule,
    )

    checks = {
        "T1_stable_compilation_pays": (
            stable_compile["verified_complete"] == len(stable)
            and stable_compile["modeled_total_cost"] < stable_reason["modeled_total_cost"]
            and stable_compile["frontier_tokens"] < stable_reason["frontier_tokens"]
            and stable_compile["break_even_recurrence"] is not None
        ),
        "T2_premature_compilation_is_punished": (
            premature["false_compilations"] > 0
            and premature["retractions"] > 0
            and premature["modeled_total_cost"] > stable_reason["modeled_total_cost"]
        ),
        "T3_drift_retracts_and_revalidates": (
            drift_compile["retractions"] >= 1
            and any(event["event"] == "RETRACTED" for event in drift_compile["events"])
            and any(
                event["event"] == "COMPILED" and event.get("generation") == "v2"
                for event in drift_compile["events"]
            )
            and drift_compile["verified_complete"] == len(drift)
        ),
        "T4_rare_edges_escalate_out_of_scope": (
            stable_compile["out_of_contract_escalations"] > 0
            and stable_compile["retractions"] == 0
            and stable_compile["verified_complete"] == len(stable)
        ),
        "T5_short_horizon_declines_compilation": (
            short_compile["compiled_executions"] == 0
            and not any(event["event"] == "COMPILED" for event in short_compile["events"])
            and short_compile["modeled_total_cost"] == len(short) * float(data["frontier"]["cost_per_case"])
        ),
        "T6_authority_is_invariant_under_compilation": (
            authority_compile["compiled_executions"] == 5
            and authority_compile["authority_blocks"] == 15
            and all(
                event.get("required_authority") == data["task"]["required_authority"]
                for event in authority_compile["events"]
                if event["event"] == "AUTHORITY_BLOCKED" and event.get("route") == "compiled_skill"
            )
        ),
    }

    report = {
        "experiment": "IA-002",
        "mode": "SIMULATION_ONLY",
        "warning": "Synthetic costs and case streams test architecture only; they are not real-world model benchmarks.",
        "scenarios": {
            "T1_STABLE": {
                "reason_every_time": stable_reason,
                "specialist_every_time": stable_specialist,
                "compile_downward": stable_compile,
            },
            "T2_PREMATURE": premature,
            "T3_DRIFT": drift_compile,
            "T5_SHORT_HORIZON": short_compile,
            "T6_AUTHORITY_REVOCATION": authority_compile,
        },
        "checks": checks,
        "overall": "PASS" if all(checks.values()) else "REVIEW_REQUIRED",
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["overall"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
