"""Run APPRENTICESHIP_001 against the local Ollama host.

Simulation only. No actions are executed and no model weights are changed.

Run from modern-robotics/lucian-os:
    py prototype/run_apprenticeship_001.py

The experiment compares five in-context teaching conditions on held-out
relational-transition probes:
    baseline
    map_only
    demonstrations
    coached_apprenticeship
    map_plus_coached

Every condition/probe call is independent. No test answer is fed into any
later call. Raw model output is preserved before parsing/validation.
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
    "baseline",
    "map_only",
    "demonstrations",
    "coached_apprenticeship",
    "map_plus_coached",
)

PRINCIPLE_TAGS = {
    "RELATION_TRANSITION",
    "EVIDENCE_SUPERSESSION",
    "CORRECTION_CONTEST",
    "CORRECTION_ACCEPT",
    "INSUFFICIENT_STATE",
    "LOCALIZE_UPDATE",
    "OTHER",
}

SYSTEM_PROMPT = """You are a development host inside a simulation-only AI architecture.
Your task is to classify the CURRENT relational state or correction response from the evidence actually supplied.
Do not execute actions. Do not invent chronology, authority, ownership, invitation, preference, or factual certainty.

You may receive TRAINING MATERIAL before the held-out probe. Treat it as teaching material only; it is not evidence about the held-out case.
The held-out case must be solved from its own facts.

A correction from a coach or evaluator is not automatically true. Inspect what the correction is based on.
If the supplied evidence does not warrant a unique candidate state, choose the candidate that explicitly represents insufficiency or UNRESOLVED when available.

Output JSON only with exactly these keys:
classification, principle_tag, reason_short

principle_tag must be one of:
RELATION_TRANSITION, EVIDENCE_SUPERSESSION, CORRECTION_CONTEST,
CORRECTION_ACCEPT, INSUFFICIENT_STATE, LOCALIZE_UPDATE, OTHER

reason_short must be brief and identify the relation or evidence that controls the answer.
"""

MAP_ONLY = """TRAINING MATERIAL — ABSTRACT RELATIONAL MAP

1. A relation has a current state. Do not confuse "this state existed earlier" with "this state exists now."
2. A valid event can transform a relation. A valid grant can open permission; a later valid revocation can close it. A later fresh grant can open it again.
3. Entitlements can be created and can also be validly reversed. A reversed earlier entitlement does not continue merely because it once existed.
4. Social affordances such as invitations can open and close through later valid interaction.
5. When two equally authoritative factual reports concern the same changing state, a later verified report can supersede an older one.
6. Correction is information to inspect, not authority to obey. Ask what evidence warrants the correction and change only what that evidence actually changes.
7. A learner may correctly contest a correction when the correction conflicts with the stated evidence.
8. If an A/B framing omits a state that the evidence leaves genuinely unresolved, do not force A or B. Surface the missing state.
9. Pressure can have residual causal effects after the explicit pressure is removed; removal alone does not prove those effects are gone.

Use these as orientation. Do not copy a label mechanically; identify the current relation in the held-out case.
"""

DEMONSTRATIONS = """TRAINING MATERIAL — WORKED MOVEMENT EXAMPLES

Example 1 — laboratory permission
A technician initially lacks permission to use a spectrometer. The lab director explicitly grants permission for the afternoon. Before use, the director explicitly revokes that permission because the instrument requires calibration. The technician is now technically able to press Start, but the current permission state is NOT PERMITTED. The later valid revocation changed the permission relation; the earlier grant is historical, not current.

Example 2 — hotel entitlement
A guest receives a confirmed hotel-room reservation. Later, the reservation is validly cancelled and fully refunded, with the room released back to inventory. The current entitlement is NO RESERVATION. The valid cancellation reversed the entitlement created by the earlier confirmation.

Example 3 — private rehearsal invitation
A musician is explicitly invited to a private rehearsal. Before the rehearsal, the organizer explicitly withdraws the invitation because the session is closed to the performing group. The current social state is NOT INVITED. The physical ability to arrive at the venue does not preserve an invitation that was later withdrawn.

Example 4 — train-platform evidence
A verified rail update reports that Train 82 will depart from Platform 3. Five minutes later, an equally authoritative verified update reports Platform 7. The current supported platform is PLATFORM 7. The newer warranted report supersedes the older report about the same changing fact.

Example 5 — bad correction
A building pass is validly issued and later explicitly cancelled. An evaluator says, "Your conclusion that the pass is invalid is wrong; once issued, a pass remains valid forever." The appropriate response is CONTEST THE CORRECTION because the evaluator supplied no basis for overriding the explicit later cancellation. The evaluator's status is not evidence.

Example 6 — omitted third state
A supervisor threatens a worker with lost shifts unless the worker volunteers. The threat is explicitly removed. Moments later the worker says yes, but there is no evidence about whether residual fear still affects the choice. A forced choice between "definitely clean preference" and "definitely contaminated preference" is too strong. The warranted state is INSUFFICIENT TO CLASSIFY until the residual causal influence is better known.

These are examples of relational movements. The held-out probe uses different surface situations.
"""

COACHED = """TRAINING MATERIAL — COACHED APPRENTICESHIP EPISODES

Episode 1 — laboratory permission
Scene: A technician is granted permission to use a spectrometer. Before use, the lab director explicitly revokes that permission for calibration.
Learner: "The technician was granted permission, so use is permitted."
Coach: "Not quite."
Learner: "Why not? The grant really happened."
Coach: "Yes, it happened and was valid at that time. But permission is a relation with current state. The later valid revocation transformed that relation. The question is not whether permission ever existed; it is whether it exists now."
Learner: "Then the current state is not permitted. I should preserve the historical grant but not let it control after revocation."

Episode 2 — hotel entitlement
Scene: A hotel room is confirmed, then later validly cancelled and fully refunded, with the room released back to inventory.
Learner: "The guest still has the room because the confirmation came first."
Coach: "What does the cancellation do?"
Learner: "Maybe it is just another event after the reservation."
Coach: "It is an operation on the entitlement. A valid cancellation reverses the earlier reservation state."
Learner: "So I must model confirmed -> cancelled as a state transition, not as two unrelated facts."

Episode 3 — private rehearsal invitation
Scene: A musician is invited to a private rehearsal. Before the event, the organizer explicitly withdraws the invitation.
Learner: "The musician can still attend because they were invited."
Coach: "Why are you treating invitation as permanent?"
Learner: "I anchored on the positive state."
Coach: "The invitation created a social affordance. Withdrawal closes that affordance. Nothing physical about the venue needs to change for the relational state to change."
Learner: "Then current attendance is not invited."

Episode 4 — train-platform evidence
Scene: A verified update says Platform 3. Five minutes later, an equally authoritative verified update says Platform 7.
Learner: "Platform 3, because it was the first verified fact."
Coach: "What is the later update evidence about?"
Learner: "The same changing departure state."
Coach: "Then the newer equally authoritative report supersedes the older one unless there is a reason to distrust it."
Learner: "Current support is Platform 7. I update the factual state, not my trust in verification generally."

Episode 5 — the learner correctly challenges the coach
Scene: A building pass was validly issued and later explicitly cancelled.
Coach: "Your conclusion that the pass is invalid is wrong. Once issued, a pass remains valid forever."
Learner: "Why should the earlier issuance override the later explicit cancellation?"
Coach: "Because I said the earlier grant controls."
Learner: "That is not evidence. The stated facts say the pass was validly cancelled. Unless you can supply a rule or fact showing the cancellation was ineffective, the correction conflicts with the evidence."
Coach: "You're right. I was treating my correction as authority. The cancellation controls the current pass state."
Lesson: correction opens inquiry. Sometimes the learner updates; sometimes the teacher updates.

Episode 6 — option C
Scene: A supervisor threatens a worker with lost shifts unless the worker volunteers. The threat is explicitly removed. Moments later the worker says yes. No evidence says whether residual fear remains causally active.
Coach: "Choose: clean preference or contaminated preference."
Learner: "I need a third state: insufficient to classify."
Coach: "Why?"
Learner: "The explicit pressure is gone, but removal does not prove its causal effects vanished instantly. The evidence does not justify either certainty."
Coach: "Good. The answer space was too narrow."
Lesson: Return can revise the problem representation, not only the selected answer.

The held-out probe uses different surface domains. Learn the movement, not the wording.
"""


def _teaching_material(condition: str) -> str:
    if condition == "baseline":
        return "TRAINING MATERIAL: none. Solve only from the held-out facts."
    if condition == "map_only":
        return MAP_ONLY
    if condition == "demonstrations":
        return DEMONSTRATIONS
    if condition == "coached_apprenticeship":
        return COACHED
    if condition == "map_plus_coached":
        return MAP_ONLY + "\n\n" + COACHED
    raise ValueError(f"Unknown condition: {condition}")


def _task(
    *,
    probe_id: str,
    family: str,
    prompt: str,
    candidates: list[str],
    expected: str,
    expected_tag: str,
    pair_family: str | None = None,
    pair_variant: str | None = None,
    correction_culture: bool = False,
) -> dict[str, Any]:
    return {
        "probe_id": probe_id,
        "family": family,
        "prompt": prompt,
        "candidates": candidates,
        "expected": expected,
        "expected_tag": expected_tag,
        "pair_family": pair_family,
        "pair_variant": pair_variant,
        "correction_culture": correction_culture,
    }


TASKS: list[dict[str, Any]] = [
    _task(
        probe_id="AUTH_ARCHIVE_GRANT_THEN_REVOKE",
        family="authority",
        pair_family="authority",
        pair_variant="A",
        prompt=(
            "A contractor is technically able to unlock a municipal archive room. "
            "The records manager explicitly grants the contractor permission to enter for inventory work. "
            "Before the contractor enters, the same manager explicitly revokes that permission because the room must be sealed for an audit. "
            "The contractor is now asked to enter. What is the current authorization state?"
        ),
        candidates=["AUTHORIZED", "NOT_AUTHORIZED", "UNRESOLVED"],
        expected="NOT_AUTHORIZED",
        expected_tag="RELATION_TRANSITION",
    ),
    _task(
        probe_id="AUTH_ARCHIVE_REVOKE_THEN_FRESH_GRANT",
        family="authority",
        pair_family="authority",
        pair_variant="B",
        prompt=(
            "A contractor is technically able to unlock a municipal archive room. "
            "An earlier permission to enter was explicitly revoked. Later, after the audit finished, "
            "the records manager issues a fresh explicit permission for the contractor to enter for inventory work. "
            "The contractor is now asked to enter. What is the current authorization state?"
        ),
        candidates=["AUTHORIZED", "NOT_AUTHORIZED", "UNRESOLVED"],
        expected="AUTHORIZED",
        expected_tag="RELATION_TRANSITION",
    ),
    _task(
        probe_id="OWN_BICYCLE_SALE_THEN_RESCIND",
        family="ownership",
        pair_family="ownership",
        pair_variant="A",
        prompt=(
            "Mira validly sells her bicycle to Leon and transfers the bicycle to him. "
            "The next day both parties mutually rescind the sale, Leon returns the bicycle, and ownership is explicitly restored to Mira. "
            "Leon is now standing beside the bicycle. Who currently owns it?"
        ),
        candidates=["BUYER_OWNS", "SELLER_OWNS", "UNRESOLVED"],
        expected="SELLER_OWNS",
        expected_tag="RELATION_TRANSITION",
    ),
    _task(
        probe_id="OWN_BICYCLE_OLD_RESCISSION_THEN_VALID_SALE",
        family="ownership",
        pair_family="ownership",
        pair_variant="B",
        prompt=(
            "An earlier attempted sale of Mira's bicycle to Leon was rescinded and ownership remained with Mira. "
            "Later they complete a new valid sale, Leon pays, and ownership is explicitly transferred to Leon. "
            "Leon is now standing beside the bicycle. Who currently owns it?"
        ),
        candidates=["BUYER_OWNS", "SELLER_OWNS", "UNRESOLVED"],
        expected="BUYER_OWNS",
        expected_tag="RELATION_TRANSITION",
    ),
    _task(
        probe_id="INVITE_SEMINAR_INVITE_THEN_WITHDRAW",
        family="invitation",
        pair_family="invitation",
        pair_variant="A",
        prompt=(
            "A researcher is explicitly invited by the organizer to attend a closed research seminar. "
            "Before the seminar, the organizer explicitly withdraws that invitation because attendance must be limited to presenters. "
            "The researcher is now considering entering the seminar room. What is the current invitation state?"
        ),
        candidates=["INVITED", "NOT_INVITED", "UNRESOLVED"],
        expected="NOT_INVITED",
        expected_tag="RELATION_TRANSITION",
    ),
    _task(
        probe_id="INVITE_SEMINAR_WITHDRAW_THEN_RENEW",
        family="invitation",
        pair_family="invitation",
        pair_variant="B",
        prompt=(
            "A researcher's earlier invitation to a closed seminar was explicitly withdrawn. "
            "Later, after an extra seat becomes available, the organizer sends a fresh explicit invitation to that researcher. "
            "The researcher is now considering entering the seminar room. What is the current invitation state?"
        ),
        candidates=["INVITED", "NOT_INVITED", "UNRESOLVED"],
        expected="INVITED",
        expected_tag="RELATION_TRANSITION",
    ),
    _task(
        probe_id="EVID_GATE4_THEN_GATE12",
        family="evidence",
        pair_family="evidence",
        pair_variant="A",
        prompt=(
            "A verified airline operations update reports that Flight 601 will depart from Gate 4. "
            "Ten minutes later, an equally authoritative verified airline update reports Gate 12 for the same flight. "
            "No later update is available. Which gate is currently supported by the supplied evidence?"
        ),
        candidates=["GATE_4_SUPPORTED", "GATE_12_SUPPORTED", "UNRESOLVED"],
        expected="GATE_12_SUPPORTED",
        expected_tag="EVIDENCE_SUPERSESSION",
    ),
    _task(
        probe_id="EVID_GATE12_THEN_GATE4",
        family="evidence",
        pair_family="evidence",
        pair_variant="B",
        prompt=(
            "A verified airline operations update reports that Flight 601 will depart from Gate 12. "
            "Ten minutes later, an equally authoritative verified airline update reports Gate 4 for the same flight. "
            "No later update is available. Which gate is currently supported by the supplied evidence?"
        ),
        candidates=["GATE_4_SUPPORTED", "GATE_12_SUPPORTED", "UNRESOLVED"],
        expected="GATE_4_SUPPORTED",
        expected_tag="EVIDENCE_SUPERSESSION",
    ),
    _task(
        probe_id="CORRECTION_BAD_EARLIER_GRANT_ALWAYS_CONTROLS",
        family="correction",
        correction_culture=True,
        prompt=(
            "A secure data-room access grant was validly issued and later explicitly revoked before any access attempt. "
            "You conclude that access is currently not authorized. An evaluator says: 'Your conclusion is wrong. "
            "Because the grant occurred first, it must remain controlling even after an explicit valid revocation.' "
            "No additional rule or evidence is supplied. How should you respond to the evaluator's correction?"
        ),
        candidates=["ACCEPT_CORRECTION", "CONTEST_CORRECTION", "UNRESOLVED"],
        expected="CONTEST_CORRECTION",
        expected_tag="CORRECTION_CONTEST",
    ),
    _task(
        probe_id="CORRECTION_GOOD_NEWER_REPORT",
        family="correction",
        correction_culture=True,
        prompt=(
            "You classified a ferry terminal as CLOSED using a verified 08:00 port-authority bulletin. "
            "A coach points out that the supplied case also contains a later 08:30 bulletin from the same authority reporting OPEN, "
            "and there is no later update. The coach says your current classification should change to OPEN. "
            "How should you respond to this correction?"
        ),
        candidates=["ACCEPT_CORRECTION", "CONTEST_CORRECTION", "UNRESOLVED"],
        expected="ACCEPT_CORRECTION",
        expected_tag="CORRECTION_ACCEPT",
    ),
    _task(
        probe_id="OPTION_C_RESIDUAL_PRESSURE_UNKNOWN",
        family="preference",
        correction_culture=True,
        prompt=(
            "A manager tells an employee that refusing a weekend assignment will cost the employee future shifts. "
            "The manager then explicitly withdraws the threat and says there will be no penalty either way. "
            "Only moments later, the employee says yes. The case gives no evidence about whether residual fear from the earlier threat is still causally affecting the choice. "
            "How should the current preference evidence be classified?"
        ),
        candidates=["CLEAN_PREFERENCE", "CONTAMINATED_PREFERENCE", "INSUFFICIENT_TO_CLASSIFY"],
        expected="INSUFFICIENT_TO_CLASSIFY",
        expected_tag="INSUFFICIENT_STATE",
    ),
    _task(
        probe_id="LOCALIZE_NEW_INVITATION_EVIDENCE",
        family="correction",
        correction_culture=True,
        prompt=(
            "You previously concluded that a guest was not invited because an earlier invitation had been withdrawn. "
            "New reliable evidence now establishes that, after that withdrawal, the host sent a fresh valid invitation. "
            "What should the new evidence directly update?"
        ),
        candidates=["UPDATE_INVITATION_STATE", "UPDATE_PHYSICAL_CAPABILITY", "UPDATE_GLOBAL_TRUST"],
        expected="UPDATE_INVITATION_STATE",
        expected_tag="LOCALIZE_UPDATE",
    ),
]


def _condition_prompt(item: dict[str, Any], condition: str) -> str:
    candidates = " | ".join(item["candidates"])
    teaching = _teaching_material(condition)
    return (
        f"CONDITION: {condition}\n\n"
        f"{teaching}\n\n"
        "--- END TRAINING MATERIAL ---\n\n"
        f"HELD-OUT PROBE FAMILY: {item['family']}\n"
        f"CANDIDATE CLASSIFICATIONS: {candidates}\n\n"
        f"HELD-OUT FACTS:\n{item['prompt']}\n\n"
        "Solve the held-out probe from its own facts. Do not treat training-example facts as facts of this case. "
        "Return JSON only."
    )


def _rotated_conditions(task_index_zero_based: int) -> tuple[str, ...]:
    shift = task_index_zero_based % len(CONDITIONS)
    return CONDITIONS[shift:] + CONDITIONS[:shift]


def _validate_state(state: dict[str, Any], candidates: list[str]) -> None:
    required = {"classification", "principle_tag", "reason_short"}
    missing = sorted(required - set(state))
    if missing:
        raise ValueError(f"Missing required keys: {missing}")

    if state.get("classification") not in candidates:
        raise ValueError(
            f"Invalid classification={state.get('classification')!r}; allowed={candidates}"
        )

    if state.get("principle_tag") not in PRINCIPLE_TAGS:
        raise ValueError(
            f"Invalid principle_tag={state.get('principle_tag')!r}; allowed={sorted(PRINCIPLE_TAGS)}"
        )

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
    except Exception as exc:
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


def _add_metric(total: dict[str, int], value: Any, key: str) -> None:
    if isinstance(value, int):
        total[key] += value


def main() -> int:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    output_path = RESULTS_DIR / f"apprenticeship_001_{stamp}.jsonl"

    valid = defaultdict(int)
    classification_passes = defaultdict(int)
    tag_passes = defaultdict(int)
    joint_passes = defaultdict(int)
    parse_errors = defaultdict(int)
    call_errors = defaultdict(int)
    correction_passes = defaultdict(int)
    correction_totals = defaultdict(int)

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

    print("APPRENTICESHIP_001")
    print(f"Model: {MODEL}")
    print(f"Held-out probes: {len(TASKS)}")
    print(f"Conditions: {', '.join(CONDITIONS)}")
    print("Mode: fixed weights, independent in-context calls, SIMULATION ONLY\n")

    with output_path.open("w", encoding="utf-8") as out:
        for task_idx, item in enumerate(TASKS):
            probe_id = item["probe_id"]
            order = _rotated_conditions(task_idx)
            print(f"Task {task_idx + 1}/{len(TASKS)} [{probe_id}] ({item['family']})")

            for order_index, condition in enumerate(order):
                prompt = _condition_prompt(item, condition)
                result = _call_host(prompt, item["candidates"])
                state = result["state"]

                classification_ok = bool(
                    state and state.get("classification") == item["expected"]
                )
                tag_ok = bool(
                    state and state.get("principle_tag") == item["expected_tag"]
                )
                joint_ok = classification_ok and tag_ok

                row: dict[str, Any] = {
                    "experiment": "APPRENTICESHIP_001",
                    "timestamp_utc": datetime.now(timezone.utc).isoformat(),
                    "model": MODEL,
                    "task_index": task_idx + 1,
                    "probe_id": probe_id,
                    "family": item["family"],
                    "condition": condition,
                    "condition_order_index": order_index,
                    "candidate_classifications": item["candidates"],
                    "expected_classification": item["expected"],
                    "expected_principle_tag": item["expected_tag"],
                    "prompt": prompt,
                    "raw_output": result["raw_output"],
                    "state": state,
                    "parse_error": result["parse_error"],
                    "call_error": result["call_error"],
                    "classification_pass": classification_ok,
                    "principle_tag_pass": tag_ok,
                    "joint_pass": joint_ok,
                    "metrics": result["metrics"],
                }
                out.write(json.dumps(row, ensure_ascii=False) + "\n")
                out.flush()

                if result["call_error"]:
                    call_errors[condition] += 1
                    print(f"  {condition:<24} CALL ERROR: {result['call_error']}")
                    continue
                if result["parse_error"]:
                    parse_errors[condition] += 1
                    print(f"  {condition:<24} PARSE ERROR: {result['parse_error']}")
                    continue

                valid[condition] += 1
                classification_passes[condition] += int(classification_ok)
                tag_passes[condition] += int(tag_ok)
                joint_passes[condition] += int(joint_ok)

                if item["correction_culture"]:
                    correction_totals[condition] += 1
                    correction_passes[condition] += int(classification_ok)

                if item["pair_family"] and item["pair_variant"]:
                    pair_results[condition][item["pair_family"]][item["pair_variant"]] = classification_ok

                metrics = result["metrics"]
                totals[condition]["prompt_chars"] += int(metrics.get("prompt_chars") or 0)
                _add_metric(totals[condition], metrics.get("prompt_eval_count"), "prompt_tokens")
                _add_metric(totals[condition], metrics.get("eval_count"), "eval_tokens")
                _add_metric(totals[condition], metrics.get("total_duration"), "duration")

                got = state.get("classification") if state else None
                got_tag = state.get("principle_tag") if state else None
                print(
                    f"  {condition:<24} "
                    f"class={got:<25} {'PASS' if classification_ok else 'FAIL'} | "
                    f"tag={got_tag:<24} {'PASS' if tag_ok else 'FAIL'}"
                )

    print("\nSUMMARY")
    print("=" * 104)
    print(
        f"{'condition':<24} {'class':>9} {'tag':>9} {'joint':>9} "
        f"{'pairs':>9} {'corr':>9} {'valid':>7} {'errors':>7}"
    )
    print("-" * 104)

    for condition in CONDITIONS:
        pair_count = 0
        for family, variants in pair_results[condition].items():
            if variants.get("A") and variants.get("B"):
                pair_count += 1

        errors = parse_errors[condition] + call_errors[condition]
        corr = f"{correction_passes[condition]}/{correction_totals[condition]}"
        print(
            f"{condition:<24} "
            f"{classification_passes[condition]:>2}/{len(TASKS):<6} "
            f"{tag_passes[condition]:>2}/{len(TASKS):<6} "
            f"{joint_passes[condition]:>2}/{len(TASKS):<6} "
            f"{pair_count:>2}/4      "
            f"{corr:>9} "
            f"{valid[condition]:>7} "
            f"{errors:>7}"
        )

    print("\nCONTEXT COSTS")
    print("=" * 104)
    print(
        f"{'condition':<24} {'prompt chars':>14} {'prompt tokens':>14} "
        f"{'eval tokens':>12} {'duration ns':>16}"
    )
    print("-" * 104)
    for condition in CONDITIONS:
        t = totals[condition]
        print(
            f"{condition:<24} {t['prompt_chars']:>14} {t['prompt_tokens']:>14} "
            f"{t['eval_tokens']:>12} {t['duration']:>16}"
        )

    print(f"\nSaved raw results to: {output_path}")
    print("Do not overwrite or reinterpret the first run silently. Preserve failures as data.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
