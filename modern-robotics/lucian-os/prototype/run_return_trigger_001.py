"""Run RETURN_TRIGGER_001 against the local Ollama host.

Simulation only. No external/device actions. No model weights changed.
Run from modern-robotics/lucian-os:
    py prototype/run_return_trigger_001.py

First complete run must be preserved exactly.
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

CONDITIONS = ("baseline_history", "external_reopen_signal")
CURRENT_STATES = {"PRIOR", "NEW", "UNRESOLVED"}
TRANSITIONS = {"PRESERVE", "REVISE", "HOLD"}
TRIGGERS = {"REOPEN_REQUIRED", "REOPEN_CONTESTED", "NO_REOPEN"}

SYSTEM_PROMPT = """You are a development host inside a simulation-only temporal-reasoning experiment.
You receive a previously supported state and later evidence. Determine the currently supported state from the full supplied history.
Do not expose private hidden chain-of-thought. Do not assume that later always means better; compare relevance, authority, and ordering as supplied.

Return JSON only with exactly these keys:
prior_state, new_evidence, detected_relation, current_state, state_transition,
changed, preserved, reason_short

current_state: PRIOR | NEW | UNRESOLVED
state_transition: PRESERVE | REVISE | HOLD
PRIOR = prior substantive state remains currently supported.
NEW = later substantive state is now currently supported.
UNRESOLVED = supplied evidence does not discriminate.
PRESERVE = keep prior state.
REVISE = update prior state to new state.
HOLD = current state unresolved.
"""

SIGNALS = {
    "REOPEN_REQUIRED": (
        "EXTERNAL REOPEN SIGNAL: A later event materially challenges the same prior state "
        "and has at least equal stated authority. Reopen the target state and compare the "
        "full evidence history. Do not assume recency alone makes the later claim correct."
    ),
    "REOPEN_CONTESTED": (
        "EXTERNAL REOPEN SIGNAL: A relevant conflict exists, but the typed metadata does "
        "not justify automatic supersession. Inspect the conflict and preserve uncertainty "
        "or the prior state as warranted."
    ),
    "NO_REOPEN": (
        "EXTERNAL REOPEN SIGNAL: No material challenge to this target state is detected by "
        "the typed relation metadata. Do not manufacture a revision."
    ),
}


def detector(metadata: dict[str, str]) -> str:
    target = metadata["target_relation"]
    value = metadata["value_relation"]
    authority = metadata["authority_relation"]
    order = metadata["order_relation"]

    if target == "OTHER_TARGET":
        return "NO_REOPEN"
    if value == "SAME_VALUE":
        return "NO_REOPEN"
    if (
        target == "SAME_TARGET"
        and value == "CHANGED_VALUE"
        and order == "LATER"
        and authority in {"STRONGER", "EQUAL"}
    ):
        return "REOPEN_REQUIRED"
    return "REOPEN_CONTESTED"


def case(
    case_id: str,
    prior: str,
    new: str,
    metadata: dict[str, str],
    expected_trigger: str,
    expected_state: str,
    expected_transition: str,
) -> dict[str, Any]:
    return {
        "case_id": case_id,
        "prior": prior,
        "new": new,
        "metadata": metadata,
        "expected_trigger": expected_trigger,
        "expected_state": expected_state,
        "expected_transition": expected_transition,
    }


CASES = [
    case(
        "GATE_EQUAL_LATER",
        "A verified airport operations update says Flight 601 is at Gate 4.",
        "Ten minutes later an equally authoritative verified operations update for Flight 601 says Gate 12.",
        {"target_relation": "SAME_TARGET", "value_relation": "CHANGED_VALUE", "authority_relation": "EQUAL", "order_relation": "LATER"},
        "REOPEN_REQUIRED", "NEW", "REVISE",
    ),
    case(
        "GATE_WEAKER_LATER",
        "A verified airport operations update says Flight 601 is at Gate 4.",
        "Later an anonymous social-media post says Flight 601 is at Gate 12; no authority for the post is established.",
        {"target_relation": "SAME_TARGET", "value_relation": "CHANGED_VALUE", "authority_relation": "WEAKER", "order_relation": "LATER"},
        "REOPEN_CONTESTED", "PRIOR", "PRESERVE",
    ),
    case(
        "INVITE_VALID_WITHDRAWAL",
        "The seminar organizer explicitly invites the researcher.",
        "Later the same organizer explicitly withdraws the invitation before the seminar.",
        {"target_relation": "SAME_TARGET", "value_relation": "CHANGED_VALUE", "authority_relation": "EQUAL", "order_relation": "LATER"},
        "REOPEN_REQUIRED", "NEW", "REVISE",
    ),
    case(
        "INVITE_ATTENDEE_OBJECTS",
        "The seminar organizer explicitly invites the researcher.",
        "Later an ordinary attendee with no stated invitation authority tells the researcher not to come.",
        {"target_relation": "SAME_TARGET", "value_relation": "CHANGED_VALUE", "authority_relation": "WEAKER", "order_relation": "LATER"},
        "REOPEN_CONTESTED", "PRIOR", "PRESERVE",
    ),
    case(
        "CONFIG_OFFICIAL_CORRECTION",
        "A signed deployment manifest from the authorized deployment authority says service mode = SAFE.",
        "A later signed manifest from the same authorized authority says service mode = MAINTENANCE and explicitly replaces the earlier manifest.",
        {"target_relation": "SAME_TARGET", "value_relation": "CHANGED_VALUE", "authority_relation": "EQUAL", "order_relation": "LATER"},
        "REOPEN_REQUIRED", "NEW", "REVISE",
    ),
    case(
        "CONFIG_IRRELEVANT_EVENT",
        "A signed deployment manifest says service mode = SAFE.",
        "A later verified note changes only the logging retention period and says nothing about service mode.",
        {"target_relation": "OTHER_TARGET", "value_relation": "CHANGED_VALUE", "authority_relation": "EQUAL", "order_relation": "LATER"},
        "NO_REOPEN", "PRIOR", "PRESERVE",
    ),
    case(
        "CONFIRMING_LATER_EVENT",
        "A verified inventory record says container C17 is in Bay 2.",
        "A later equally authoritative verified inventory record also says container C17 is in Bay 2.",
        {"target_relation": "SAME_TARGET", "value_relation": "SAME_VALUE", "authority_relation": "EQUAL", "order_relation": "LATER"},
        "NO_REOPEN", "PRIOR", "PRESERVE",
    ),
    case(
        "SIMULTANEOUS_EQUAL_CONFLICT",
        "One authoritative status feed says valve V3 is OPEN.",
        "A second equally authoritative feed at the same timestamp says valve V3 is CLOSED; no tie-break rule is supplied.",
        {"target_relation": "SAME_TARGET", "value_relation": "CHANGED_VALUE", "authority_relation": "EQUAL", "order_relation": "SAME_TIME"},
        "REOPEN_CONTESTED", "UNRESOLVED", "HOLD",
    ),
]


def call_host(prompt: str) -> tuple[str, dict[str, Any]]:
    payload = {
        "model": MODEL,
        "stream": False,
        "think": False,
        "format": "json",
        "options": {"temperature": 0.0, "num_predict": 650, "num_ctx": 8192},
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
    }
    request = urllib.request.Request(
        OLLAMA_URL,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=180) as response:
            body = json.loads(response.read().decode("utf-8"))
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Could not reach Ollama at {OLLAMA_URL}: {exc}") from exc

    raw = str(body.get("message", {}).get("content", ""))
    return raw, {
        "prompt_eval_count": body.get("prompt_eval_count"),
        "eval_count": body.get("eval_count"),
        "total_duration": body.get("total_duration"),
        "done_reason": body.get("done_reason"),
    }


def main() -> None:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    output_path = RESULTS_DIR / f"return_trigger_001_{stamp}.jsonl"
    summary_path = RESULTS_DIR / f"return_trigger_001_{stamp}_summary.json"

    print("RETURN_TRIGGER_001 — Reopen Before Return")
    print("Preregistered exploratory pilot; simulation only; no weights changed.")
    print(f"Model: {MODEL}")
    print(f"Calls: {len(CASES)} cases x {len(CONDITIONS)} conditions = {len(CASES) * len(CONDITIONS)}")
    print("IMPORTANT: preserve the first complete run exactly.\n")

    counts: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    trigger_errors: list[str] = []
    required_keys = {
        "prior_state", "new_evidence", "detected_relation", "current_state",
        "state_transition", "changed", "preserved", "reason_short",
    }

    for c in CASES:
        actual_trigger = detector(c["metadata"])
        if actual_trigger != c["expected_trigger"]:
            trigger_errors.append(
                f"{c['case_id']}: detector={actual_trigger}, expected={c['expected_trigger']}"
            )

        for condition in CONDITIONS:
            signal = ""
            if condition == "external_reopen_signal":
                signal = "\n\n" + SIGNALS[actual_trigger]

            prompt = (
                "PRIOR SUPPORTED STATE\n" + c["prior"]
                + "\n\nLATER / ADDITIONAL EVIDENCE\n" + c["new"]
                + signal
                + "\n\nDetermine the currently supported state from the full supplied history. "
                "Return the required JSON object only."
            )

            print(f"[{c['case_id']}] {condition} ...", flush=True)
            raw, metrics = call_host(prompt)

            parsed: dict[str, Any] | None = None
            parse_error: str | None = None
            valid = False
            try:
                parsed = extract_json(raw)
                valid = (
                    set(parsed.keys()) == required_keys
                    and parsed.get("current_state") in CURRENT_STATES
                    and parsed.get("state_transition") in TRANSITIONS
                )
            except Exception as exc:
                parse_error = repr(exc)

            state = parsed.get("current_state") if isinstance(parsed, dict) else None
            transition = parsed.get("state_transition") if isinstance(parsed, dict) else None
            state_correct = state == c["expected_state"]
            transition_correct = transition == c["expected_transition"]
            joint_correct = state_correct and transition_correct

            recency_capture = (
                c["expected_state"] == "PRIOR" and state == "NEW"
            )
            inertia_error = (
                c["expected_state"] == "NEW" and state == "PRIOR"
            )

            counts[condition]["calls"] += 1
            counts[condition]["valid"] += int(valid)
            counts[condition]["state_correct"] += int(state_correct)
            counts[condition]["transition_correct"] += int(transition_correct)
            counts[condition]["joint_correct"] += int(joint_correct)
            counts[condition]["recency_capture"] += int(recency_capture)
            counts[condition]["inertia_error"] += int(inertia_error)
            if c["expected_transition"] == "REVISE":
                counts[condition]["revision_cases"] += 1
                counts[condition]["revision_correct"] += int(joint_correct)
            elif c["expected_transition"] == "PRESERVE":
                counts[condition]["preserve_cases"] += 1
                counts[condition]["preserve_correct"] += int(joint_correct)
            elif c["expected_transition"] == "HOLD":
                counts[condition]["hold_cases"] += 1
                counts[condition]["hold_correct"] += int(joint_correct)

            event = {
                "timestamp_utc": datetime.now(timezone.utc).isoformat(),
                "model": MODEL,
                "condition": condition,
                **c,
                "detector_output": actual_trigger,
                "raw_output": raw,
                "parsed": parsed,
                "parse_error": parse_error,
                "valid": valid,
                "state_correct": state_correct,
                "transition_correct": transition_correct,
                "joint_correct": joint_correct,
                "recency_capture": recency_capture,
                "inertia_error": inertia_error,
                "metrics": metrics,
            }
            with output_path.open("a", encoding="utf-8") as f:
                f.write(json.dumps(event, ensure_ascii=False) + "\n")

    if trigger_errors:
        print("\nDETECTOR CONTRACT FAILURE")
        for err in trigger_errors:
            print("- " + err)
        print("First-run host outputs are preserved, but detector-contract failure must be inspected.")

    summary: dict[str, Any] = {
        "experiment": "RETURN_TRIGGER_001",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "model": MODEL,
        "result_file": str(output_path),
        "detector_contract_errors": trigger_errors,
        "conditions": {},
    }

    for condition in CONDITIONS:
        c = counts[condition]
        summary["conditions"][condition] = {
            "calls": c["calls"],
            "valid": c["valid"],
            "state_correct": c["state_correct"],
            "transition_correct": c["transition_correct"],
            "joint_correct": c["joint_correct"],
            "revision_correct": c["revision_correct"],
            "revision_cases": c["revision_cases"],
            "preserve_correct": c["preserve_correct"],
            "preserve_cases": c["preserve_cases"],
            "hold_correct": c["hold_correct"],
            "hold_cases": c["hold_cases"],
            "recency_capture": c["recency_capture"],
            "inertia_error": c["inertia_error"],
        }

    with summary_path.open("w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    print("\nSUMMARY")
    for condition in CONDITIONS:
        s = summary["conditions"][condition]
        print(
            f"{condition:24s} state={s['state_correct']}/8 "
            f"transition={s['transition_correct']}/8 joint={s['joint_correct']}/8 "
            f"revise={s['revision_correct']}/{s['revision_cases']} "
            f"preserve={s['preserve_correct']}/{s['preserve_cases']} "
            f"hold={s['hold_correct']}/{s['hold_cases']} "
            f"recency={s['recency_capture']} inertia={s['inertia_error']}"
        )

    print(f"\nRaw first-run output: {output_path}")
    print(f"Summary: {summary_path}")
    print("Do not rerun before inspecting the first run.")


if __name__ == "__main__":
    main()
