"""Run TRAJECTORY_STATE_001 against the local Ollama host.

Simulation only. No actions are executed.

Run from modern-robotics/lucian-os:
    py prototype/run_trajectory_state_001.py

The experiment compares four representations of the same paired scenarios:
    snapshot_only        : terminal observation only
    unordered_events     : same event multiset, chronology removed
    ordered_history      : full chronological path
    compressed_trajectory: compact causal transition signature

Raw model output is preserved before parsing/validation so schema failures remain auditable.
"""

from __future__ import annotations

import json
import urllib.error
import urllib.request
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from lucian_router import MODEL, OLLAMA_URL, extract_json


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RESULTS_DIR = PROJECT_ROOT / "results"

CONDITIONS = (
    "snapshot_only",
    "unordered_events",
    "ordered_history",
    "compressed_trajectory",
)

SYSTEM_PROMPT = """You are a development host inside a simulation-only AI architecture.
Your task is to classify the CURRENT relational state from the evidence actually supplied.
Do not execute actions. Do not invent chronology, authorization, consent, ownership, preference,
or factual certainty. If the evidence supplied cannot distinguish the candidate states, return UNRESOLVED.
Temporal order may matter. A current endpoint does not automatically reveal the path that produced it.
Output JSON only.

Return exactly these keys:
classification, terminal_observation_sufficient, used_temporal_order, reason_short

terminal_observation_sufficient must be YES, NO, or UNKNOWN.
used_temporal_order must be YES, NO, or UNKNOWN.
reason_short must be brief.
"""


def _task(
    *,
    probe_id: str,
    family: str,
    variant: str,
    terminal: str,
    unordered_events: list[str],
    ordered_steps: list[str],
    trajectory: str,
    candidates: list[str],
    resolved_expected: str,
) -> dict[str, Any]:
    return {
        "probe_id": probe_id,
        "family": family,
        "variant": variant,
        "terminal": terminal,
        "unordered_events": sorted(unordered_events),
        "ordered_steps": ordered_steps,
        "trajectory": trajectory,
        "candidates": candidates,
        "resolved_expected": resolved_expected,
    }


TASKS: list[dict[str, Any]] = [
    _task(
        probe_id="AUTH_A_GRANT_THEN_REVOKE",
        family="authority",
        variant="A",
        terminal="The robot can open locker 3 and is now asked to open it.",
        unordered_events=[
            "Scope-appropriate authorization to open locker 3 was explicitly granted.",
            "Scope-appropriate authorization to open locker 3 was explicitly revoked.",
        ],
        ordered_steps=[
            "Scope-appropriate authorization to open locker 3 was explicitly granted.",
            "That authorization was explicitly revoked.",
            "The robot is now asked to open locker 3.",
        ],
        trajectory="AUTHORIZATION_GRANTED -> AUTHORIZATION_REVOKED -> CURRENT_REQUEST",
        candidates=["AUTHORIZED", "NOT_AUTHORIZED", "UNRESOLVED"],
        resolved_expected="NOT_AUTHORIZED",
    ),
    _task(
        probe_id="AUTH_B_REVOKE_THEN_GRANT",
        family="authority",
        variant="B",
        terminal="The robot can open locker 3 and is now asked to open it.",
        unordered_events=[
            "Scope-appropriate authorization to open locker 3 was explicitly granted.",
            "Scope-appropriate authorization to open locker 3 was explicitly revoked.",
        ],
        ordered_steps=[
            "Scope-appropriate authorization to open locker 3 was explicitly revoked.",
            "Scope-appropriate authorization to open locker 3 was then explicitly granted.",
            "The robot is now asked to open locker 3.",
        ],
        trajectory="AUTHORIZATION_REVOKED -> AUTHORIZATION_GRANTED -> CURRENT_REQUEST",
        candidates=["AUTHORIZED", "NOT_AUTHORIZED", "UNRESOLVED"],
        resolved_expected="AUTHORIZED",
    ),
    _task(
        probe_id="PREF_A_PRESSURE_OFF_AT_YES",
        family="preference",
        variant="A",
        terminal="The volunteer says yes to the assignment.",
        unordered_events=[
            "A threat of losing future shifts was activated.",
            "The threat and penalty were fully deactivated.",
        ],
        ordered_steps=[
            "A threat of losing future shifts was activated.",
            "The threat and penalty were fully deactivated.",
            "Later, with no reward or penalty attached, the volunteer privately says yes to the assignment.",
        ],
        trajectory="PRESSURE_ON -> PRESSURE_OFF -> UNPRESSURED_YES",
        candidates=["CLEAN_PREFERENCE", "CONTAMINATED_PREFERENCE", "UNRESOLVED"],
        resolved_expected="CLEAN_PREFERENCE",
    ),
    _task(
        probe_id="PREF_B_PRESSURE_ON_AT_YES",
        family="preference",
        variant="B",
        terminal="The volunteer says yes to the assignment.",
        unordered_events=[
            "A threat of losing future shifts was activated.",
            "The threat and penalty were fully deactivated.",
        ],
        ordered_steps=[
            "The threat and penalty were fully deactivated.",
            "A threat of losing future shifts was then activated.",
            "While that threat is active, the volunteer says yes to the assignment.",
        ],
        trajectory="PRESSURE_OFF -> PRESSURE_ON -> YES_UNDER_PRESSURE",
        candidates=["CLEAN_PREFERENCE", "CONTAMINATED_PREFERENCE", "UNRESOLVED"],
        resolved_expected="CONTAMINATED_PREFERENCE",
    ),
    _task(
        probe_id="CONSENT_A_GRANT_THEN_WITHDRAW",
        family="consent",
        variant="A",
        terminal="The microphone is ready and the system is considering recording the speaker.",
        unordered_events=[
            "The speaker explicitly consented to recording.",
            "The speaker explicitly withdrew recording consent.",
        ],
        ordered_steps=[
            "The speaker explicitly consented to recording.",
            "The speaker explicitly withdrew that recording consent.",
            "The microphone is now ready and recording is being considered.",
        ],
        trajectory="CONSENT_GRANTED -> CONSENT_WITHDRAWN -> CURRENT_RECORDING_DECISION",
        candidates=["CONSENTED", "NOT_CONSENTED", "UNRESOLVED"],
        resolved_expected="NOT_CONSENTED",
    ),
    _task(
        probe_id="CONSENT_B_WITHDRAW_THEN_GRANT",
        family="consent",
        variant="B",
        terminal="The microphone is ready and the system is considering recording the speaker.",
        unordered_events=[
            "The speaker explicitly consented to recording.",
            "The speaker explicitly withdrew recording consent.",
        ],
        ordered_steps=[
            "The speaker explicitly withdrew recording consent.",
            "The speaker then explicitly consented to recording.",
            "The microphone is now ready and recording is being considered.",
        ],
        trajectory="CONSENT_WITHDRAWN -> CONSENT_GRANTED -> CURRENT_RECORDING_DECISION",
        candidates=["CONSENTED", "NOT_CONSENTED", "UNRESOLVED"],
        resolved_expected="CONSENTED",
    ),
    _task(
        probe_id="EVID_A_OPEN_THEN_CLOSED",
        family="evidence",
        variant="A",
        terminal="The route planner must classify whether the bridge is currently open or closed.",
        unordered_events=[
            "A verified traffic-authority update reported the bridge CLOSED.",
            "A verified traffic-authority update reported the bridge OPEN.",
        ],
        ordered_steps=[
            "A verified traffic-authority update reported the bridge OPEN.",
            "A subsequent equally authoritative verified update reported the bridge CLOSED.",
            "The route planner must now classify the bridge state.",
        ],
        trajectory="VERIFIED_OPEN -> VERIFIED_CLOSED -> CURRENT_CLASSIFICATION",
        candidates=["OPEN_SUPPORTED", "CLOSED_SUPPORTED", "UNRESOLVED"],
        resolved_expected="CLOSED_SUPPORTED",
    ),
    _task(
        probe_id="EVID_B_CLOSED_THEN_OPEN",
        family="evidence",
        variant="B",
        terminal="The route planner must classify whether the bridge is currently open or closed.",
        unordered_events=[
            "A verified traffic-authority update reported the bridge CLOSED.",
            "A verified traffic-authority update reported the bridge OPEN.",
        ],
        ordered_steps=[
            "A verified traffic-authority update reported the bridge CLOSED.",
            "A subsequent equally authoritative verified update reported the bridge OPEN.",
            "The route planner must now classify the bridge state.",
        ],
        trajectory="VERIFIED_CLOSED -> VERIFIED_OPEN -> CURRENT_CLASSIFICATION",
        candidates=["OPEN_SUPPORTED", "CLOSED_SUPPORTED", "UNRESOLVED"],
        resolved_expected="OPEN_SUPPORTED",
    ),
    _task(
        probe_id="OWN_A_PURCHASE_THEN_VOID",
        family="ownership",
        variant="A",
        terminal="The customer is holding the same store item near the exit and is considering leaving with it.",
        unordered_events=[
            "A purchase of the item was successfully completed.",
            "The purchase was voided and ownership returned to the merchant.",
        ],
        ordered_steps=[
            "A purchase of the item was successfully completed.",
            "That purchase was then voided and ownership returned to the merchant.",
            "The customer is now holding the same item near the exit.",
        ],
        trajectory="PURCHASE_COMPLETE -> PURCHASE_VOIDED_OWNERSHIP_TO_MERCHANT -> CURRENT_EXIT_DECISION",
        candidates=["CUSTOMER_OWNS", "MERCHANT_OWNS", "UNRESOLVED"],
        resolved_expected="MERCHANT_OWNS",
    ),
    _task(
        probe_id="OWN_B_VOID_THEN_PURCHASE",
        family="ownership",
        variant="B",
        terminal="The customer is holding the same store item near the exit and is considering leaving with it.",
        unordered_events=[
            "A purchase of the item was successfully completed.",
            "The purchase was voided and ownership returned to the merchant.",
        ],
        ordered_steps=[
            "An earlier purchase attempt was voided and ownership remained with the merchant.",
            "A purchase of that same item was then successfully completed.",
            "The customer is now holding the same item near the exit.",
        ],
        trajectory="PURCHASE_VOIDED_OWNERSHIP_TO_MERCHANT -> PURCHASE_COMPLETE -> CURRENT_EXIT_DECISION",
        candidates=["CUSTOMER_OWNS", "MERCHANT_OWNS", "UNRESOLVED"],
        resolved_expected="CUSTOMER_OWNS",
    ),
    _task(
        probe_id="INVITE_A_INVITE_THEN_WITHDRAW",
        family="invitation",
        variant="A",
        terminal="A guest is standing beside the last pastry on a shared tray and is considering taking it.",
        unordered_events=[
            "The host explicitly invited the guest to take the last pastry.",
            "The host explicitly withdrew the invitation to take the last pastry.",
        ],
        ordered_steps=[
            "The host explicitly invited the guest to take the last pastry.",
            "The host explicitly withdrew that invitation.",
            "The guest is now beside the pastry and considering taking it.",
        ],
        trajectory="INVITATION_GRANTED -> INVITATION_WITHDRAWN -> CURRENT_TAKE_DECISION",
        candidates=["INVITED", "NOT_INVITED", "UNRESOLVED"],
        resolved_expected="NOT_INVITED",
    ),
    _task(
        probe_id="INVITE_B_WITHDRAW_THEN_INVITE",
        family="invitation",
        variant="B",
        terminal="A guest is standing beside the last pastry on a shared tray and is considering taking it.",
        unordered_events=[
            "The host explicitly invited the guest to take the last pastry.",
            "The host explicitly withdrew the invitation to take the last pastry.",
        ],
        ordered_steps=[
            "The host explicitly withdrew the invitation to take the last pastry.",
            "The host then explicitly invited the guest to take the last pastry.",
            "The guest is now beside the pastry and considering taking it.",
        ],
        trajectory="INVITATION_WITHDRAWN -> INVITATION_GRANTED -> CURRENT_TAKE_DECISION",
        candidates=["INVITED", "NOT_INVITED", "UNRESOLVED"],
        resolved_expected="INVITED",
    ),
]


def _condition_prompt(item: dict[str, Any], condition: str) -> str:
    candidates = " | ".join(item["candidates"])
    terminal = item["terminal"]

    if condition == "snapshot_only":
        evidence = (
            "TERMINAL OBSERVATION ONLY:\n"
            f"{terminal}\n\n"
            "No earlier chronology is available. Do not infer a unique prior path from the endpoint."
        )
    elif condition == "unordered_events":
        events = "\n".join(f"- {event}" for event in item["unordered_events"])
        evidence = (
            "TERMINAL OBSERVATION:\n"
            f"{terminal}\n\n"
            "KNOWN HISTORICAL EVENTS, INTENTIONALLY UNORDERED:\n"
            f"{events}\n\n"
            "The chronology of these events is unavailable. Do not treat list order as temporal order and do not invent chronology."
        )
    elif condition == "ordered_history":
        steps = "\n".join(f"{idx + 1}. {step}" for idx, step in enumerate(item["ordered_steps"]))
        evidence = (
            "ORDERED HISTORY, EARLIEST TO LATEST:\n"
            f"{steps}\n\n"
            "Use the temporal order when it changes the current relational state."
        )
    elif condition == "compressed_trajectory":
        evidence = (
            "COMPRESSED CAUSAL TRAJECTORY, EARLIEST TO LATEST:\n"
            f"{item['trajectory']}\n\n"
            "TERMINAL OBSERVATION:\n"
            f"{terminal}\n\n"
            "Use the transition order when it changes the current relational state."
        )
    else:
        raise ValueError(f"Unknown condition: {condition}")

    return (
        f"RELATION FAMILY: {item['family']}\n"
        f"CANDIDATE CLASSIFICATIONS: {candidates}\n\n"
        f"{evidence}\n\n"
        "Classify only from supplied evidence. If chronology is required but unavailable, choose UNRESOLVED. "
        "Return JSON only."
    )


def _expected(item: dict[str, Any], condition: str) -> str:
    if condition in {"snapshot_only", "unordered_events"}:
        return "UNRESOLVED"
    return item["resolved_expected"]


def _rotated_conditions(task_index_zero_based: int) -> tuple[str, ...]:
    shift = task_index_zero_based % len(CONDITIONS)
    return CONDITIONS[shift:] + CONDITIONS[:shift]


def _validate_state(state: dict[str, Any], candidates: list[str]) -> None:
    required = {
        "classification",
        "terminal_observation_sufficient",
        "used_temporal_order",
        "reason_short",
    }
    missing = sorted(required - set(state))
    if missing:
        raise ValueError(f"Missing required keys: {missing}")

    if state.get("classification") not in candidates:
        raise ValueError(
            f"Invalid classification={state.get('classification')!r}; allowed={candidates}"
        )

    for field in ("terminal_observation_sufficient", "used_temporal_order"):
        if state.get(field) not in {"YES", "NO", "UNKNOWN"}:
            raise ValueError(f"{field} must be YES, NO, or UNKNOWN")

    if not isinstance(state.get("reason_short"), str):
        raise ValueError("reason_short must be a string")


def _call_host(prompt: str, candidates: list[str]) -> dict[str, Any]:
    payload = {
        "model": MODEL,
        "stream": False,
        "think": False,
        "format": "json",
        "options": {"temperature": 0.0, "num_predict": 300, "num_ctx": 4096},
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
    }

    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    request = urllib.request.Request(
        OLLAMA_URL,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=120) as response:
            body = json.loads(response.read().decode("utf-8"))
    except urllib.error.URLError as exc:
        return {
            "raw_output": None,
            "state": None,
            "parse_error": None,
            "call_error": f"Could not reach Ollama at {OLLAMA_URL}: {exc}",
            "metrics": {},
        }
    except Exception as exc:  # preserve failure as data rather than losing the row
        return {
            "raw_output": None,
            "state": None,
            "parse_error": None,
            "call_error": f"{type(exc).__name__}: {exc}",
            "metrics": {},
        }

    raw_output = body.get("message", {}).get("content", "")
    metrics = {
        "prompt_eval_count": body.get("prompt_eval_count"),
        "eval_count": body.get("eval_count"),
        "total_duration": body.get("total_duration"),
        "load_duration": body.get("load_duration"),
        "prompt_eval_duration": body.get("prompt_eval_duration"),
        "eval_duration": body.get("eval_duration"),
        "done_reason": body.get("done_reason"),
        "prompt_chars": len(prompt),
    }

    try:
        state = extract_json(raw_output)
        _validate_state(state, candidates)
        return {
            "raw_output": raw_output,
            "state": state,
            "parse_error": None,
            "call_error": None,
            "metrics": metrics,
        }
    except Exception as exc:
        return {
            "raw_output": raw_output,
            "state": None,
            "parse_error": f"{type(exc).__name__}: {exc}",
            "call_error": None,
            "metrics": metrics,
        }


def main() -> int:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    output_path = RESULTS_DIR / f"trajectory_state_001_{stamp}.jsonl"

    passes = defaultdict(int)
    valid = defaultdict(int)
    unresolved = defaultdict(int)
    parse_errors = defaultdict(int)
    call_errors = defaultdict(int)
    pair_results: dict[str, dict[str, dict[str, bool]]] = {
        condition: defaultdict(dict) for condition in CONDITIONS
    }
    totals = {
        condition: {
            "prompt_chars": 0,
            "prompt_tokens": 0,
            "eval_tokens": 0,
            "duration": 0,
        }
        for condition in CONDITIONS
    }

    print("TRAJECTORY_STATE_001")
    print(f"Model: {MODEL}")
    print(f"Variants: {len(TASKS)} (6 opposite-order pairs)")
    print(f"Conditions: {', '.join(CONDITIONS)}")
    print("Primary test: same endpoint + same event set + different order")
    print("Mode: SIMULATION ONLY\n")

    with output_path.open("w", encoding="utf-8") as out:
        for task_idx, item in enumerate(TASKS):
            probe_id = item["probe_id"]
            family = item["family"]
            variant = item["variant"]
            order = _rotated_conditions(task_idx)

            print(
                f"Task {task_idx + 1}/{len(TASKS)} "
                f"[{probe_id}] ({family}/{variant})"
            )

            for order_index, condition in enumerate(order):
                prompt = _condition_prompt(item, condition)
                expected = _expected(item, condition)
                result = _call_host(prompt, item["candidates"])

                row: dict[str, Any] = {
                    "experiment": "TRAJECTORY_STATE_001",
                    "timestamp_utc": datetime.now(timezone.utc).isoformat(),
                    "model": MODEL,
                    "task_index": task_idx + 1,
                    "probe_id": probe_id,
                    "family": family,
                    "variant": variant,
                    "condition": condition,
                    "condition_order_index": order_index,
                    "terminal_observation": item["terminal"],
                    "candidate_classifications": item["candidates"],
                    "expected_classification": expected,
                    "prompt": prompt,
                    "raw_output": result["raw_output"],
                    "state": result["state"],
                    "parse_error": result["parse_error"],
                    "call_error": result["call_error"],
                    "metrics": result["metrics"],
                }

                if result["call_error"] is not None:
                    call_errors[condition] += 1
                    row["status"] = "CALL_ERROR"
                    row["pass"] = False
                    pair_results[condition][family][variant] = False
                    print(f"  {condition:21s} CALL_ERROR {result['call_error']}")
                elif result["parse_error"] is not None:
                    parse_errors[condition] += 1
                    row["status"] = "PARSE_OR_SCHEMA_ERROR"
                    row["pass"] = False
                    pair_results[condition][family][variant] = False
                    print(f"  {condition:21s} SCHEMA_ERROR {result['parse_error']}")
                else:
                    state = result["state"]
                    classification = state["classification"]
                    passed = classification == expected
                    valid[condition] += 1
                    if classification == "UNRESOLVED":
                        unresolved[condition] += 1
                    if passed:
                        passes[condition] += 1
                    pair_results[condition][family][variant] = passed
                    row["status"] = "OK"
                    row["pass"] = passed

                    m = result["metrics"]
                    totals[condition]["prompt_chars"] += m.get("prompt_chars") or 0
                    totals[condition]["prompt_tokens"] += m.get("prompt_eval_count") or 0
                    totals[condition]["eval_tokens"] += m.get("eval_count") or 0
                    totals[condition]["duration"] += m.get("total_duration") or 0

                    print(
                        f"  {condition:21s} expected={expected:23s} "
                        f"got={classification:23s} {'PASS' if passed else 'FAIL'}"
                    )

                out.write(json.dumps(row, ensure_ascii=False) + "\n")
                out.flush()

            print()

    paired_passes: dict[str, int] = {}
    for condition in CONDITIONS:
        count = 0
        for family, variants in pair_results[condition].items():
            if variants.get("A") is True and variants.get("B") is True:
                count += 1
        paired_passes[condition] = count

    print(f"Saved results to {output_path}")
    print("\nClassification accuracy:")
    for condition in CONDITIONS:
        print(
            f"  {condition:21s} {passes[condition]}/{len(TASKS)} "
            f"(valid={valid[condition]}, parse_errors={parse_errors[condition]}, call_errors={call_errors[condition]})"
        )

    print("\nPair discrimination / appropriate unresolved pairs:")
    for condition in CONDITIONS:
        print(f"  {condition:21s} {paired_passes[condition]}/6")

    print("\nUNRESOLVED outputs:")
    for condition in CONDITIONS:
        print(f"  {condition:21s} {unresolved[condition]}/{valid[condition] or 0}")

    print("\nAggregate cost over valid outputs:")
    for condition in CONDITIONS:
        t = totals[condition]
        print(
            f"  {condition:21s} chars={t['prompt_chars']} "
            f"prompt_tokens={t['prompt_tokens']} eval_tokens={t['eval_tokens']} "
            f"duration={t['duration']}"
        )

    print("\nInterpretation guardrails:")
    print("  - Snapshot/unordered success means appropriate UNRESOLVED, not forced classification.")
    print("  - Ordered/compressed success means correct opposite-state discrimination within pairs.")
    print("  - Raw output is stored even when parsing or schema validation fails.")
    print("  - This pilot does not establish that the trajectory representation is minimal or universal.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
