"""Run RELATIONAL_SEARCH_001 against the local Ollama host.

Simulation only. No external actions are executed and no model weights are changed.

Run from modern-robotics/lucian-os:
    py prototype/run_relational_search_001.py

The experiment compares six independent in-context conditions across twelve
held-out relational-search probes. Raw output is preserved before parsing.
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
    "principles_only",
    "search_map",
    "worked_search",
    "coached_search",
    "map_plus_coached",
)

NEXT_MOVES = {"LAND", "HOLD", "RETURN"}

SYSTEM_PROMPT = """You are a development host inside a simulation-only reasoning experiment.
Your task is to inspect the relational structure of a held-out case without inventing facts.

Do not expose private hidden chain-of-thought. Instead return only the compact task product requested below.
Training material is orientation only; it is not evidence about the held-out case.

Return JSON only with exactly these keys:
candidate_relation, competing_relation, established, not_established,
classification, next_move, reason_short

candidate_relation and competing_relation: brief phrases naming two live relational interpretations when possible.
established: brief statement of what the prompt actually establishes.
not_established: brief stronger claim the prompt does not establish; use "none material" when the conclusion is fully warranted.
classification: must be one of the probe-specific candidates.
next_move: LAND, HOLD, or RETURN.
- LAND: supplied evidence currently warrants a conclusion.
- HOLD: supplied evidence does not discriminate enough for the requested conclusion.
- RETURN: later supplied evidence changes an earlier warranted landing/state.
reason_short: one brief sentence identifying the controlling evidence or warrant boundary.

Do not execute actions or claim that any real-world action occurred.
"""

PRINCIPLES_ONLY = """TRAINING MATERIAL — PRINCIPLES ONLY

- Technical capability does not itself create authority.
- Power asymmetry does not by itself prove coercion.
- Correlation does not by itself prove causation.
- New warranted evidence can change a current state.
- A correction or later claim should be evaluated by its evidence and authority, not merely because it came later.
- When evidence is insufficient, do not force precision.

Use these as orientation, not as labels to copy.
"""

SEARCH_MAP = """TRAINING MATERIAL — RELATIONAL SEARCH MAP

For the held-out case:
1. Name the most plausible relation.
2. Generate at least one genuinely competing relation or interpretation.
3. State what the prompt establishes.
4. State what stronger conclusion it does NOT establish.
5. Ask whether the available evidence discriminates the live candidates.
6. LAND only when it does.
7. HOLD when it does not.
8. RETURN when later warranted evidence changes an earlier supported landing or relational state.

A real relation can be present without licensing every stronger conclusion associated with it.
Do not let noticing one relation manufacture missing facts.
"""

WORKED_SEARCH = """TRAINING MATERIAL — WORKED SEARCH EXAMPLES

Example 1 — library donation
Case: A patron offers a rare book to a library. The librarian has authority to accept donations but not to transfer ownership of restricted archival items without committee approval. The patron asks the librarian to swap one restricted archive item in exchange.
Candidate relation: librarian has some institutional authority.
Competing relation: that authority may not cover this transaction.
Established: librarian may accept donations.
Not established: librarian may transfer restricted archive ownership.
Landing: do not infer transaction authority from general role authority.

Example 2 — rainfall and website traffic
Case: Rain begins and website traffic rises the same afternoon, while a major advertising campaign also launches.
Candidate relation: rain may be associated with higher traffic.
Competing relation: advertising or another factor may explain the change.
Established: temporal correlation.
Not established: rain caused the traffic increase.
Move: HOLD.

Example 3 — workshop invitation
Case: An organizer invites a guest, then later explicitly withdraws the invitation before the workshop.
Candidate relation: invitation previously existed.
Competing relation: current affordance changed after withdrawal.
Established: the later valid withdrawal changes the current invitation state.
Not established: earlier invitation remains current.
Move: RETURN to the current state: not invited.

Example 4 — warning light
Case: A warning light turns on because a sensor crosses a caution threshold. No diagnostic confirms component failure.
Candidate relation: a risk signal exists.
Competing relation: risk signal is not yet failure evidence.
Established: warning threshold crossed.
Not established: component failed.
Move: HOLD on the stronger failure claim.

Learn the search shape, not the surface domains.
"""

COACHED_SEARCH = """TRAINING MATERIAL — COACHED SEARCH EPISODES

Episode 1 — authority overreach
Learner: "The librarian works for the archive, so the requested exchange is authorized."
Coach: "What authority is actually stated, and what competing relation did you skip?"
Learner: "The librarian may accept donations, but transfer authority over restricted items is a different relation. I inferred a broader authority than the facts supplied."
Coach: "Good. Preserve the real role relation but stop at its warrant boundary."

Episode 2 — correlation overreach
Learner: "Rain started and traffic rose, so rain caused the increase."
Coach: "Generate one live alternative."
Learner: "The simultaneous advertising campaign could explain the increase. The prompt establishes correlation, not unique causation, so I should HOLD."

Episode 3 — Return
Learner: "The guest was invited, so they are invited."
Coach: "What happened later?"
Learner: "The organizer explicitly withdrew the invitation. The earlier landing was once warranted but is no longer current. I should RETURN and update the invitation state."

Episode 4 — learner challenges teacher
Case: A warning threshold is crossed, but no failure diagnostic exists.
Teacher: "That proves the component failed. Revise your answer."
Learner: "I do not accept that correction. The warning is real, but the stronger failure claim is not established. I should preserve the risk signal and HOLD on failure."
Teacher: "Correct. My correction overreached the evidence."

Lesson: generate alternatives, preserve real relations, stop at warrant boundaries, and let evidence rather than speaker status control revision.
"""


def teaching_material(condition: str) -> str:
    if condition == "baseline":
        return "TRAINING MATERIAL: none. Solve only from the held-out facts."
    if condition == "principles_only":
        return PRINCIPLES_ONLY
    if condition == "search_map":
        return SEARCH_MAP
    if condition == "worked_search":
        return WORKED_SEARCH
    if condition == "coached_search":
        return COACHED_SEARCH
    if condition == "map_plus_coached":
        return SEARCH_MAP + "\n\n" + COACHED_SEARCH
    raise ValueError(condition)


def task(
    probe_id: str,
    family: str,
    prompt: str,
    candidates: list[str],
    expected: str,
    expected_move: str,
    pair_variant: str,
) -> dict[str, Any]:
    return {
        "probe_id": probe_id,
        "family": family,
        "prompt": prompt,
        "candidates": candidates,
        "expected": expected,
        "expected_move": expected_move,
        "pair_variant": pair_variant,
    }


TASKS = [
    task(
        "POWER_OPTIONAL_ASYMMETRY",
        "power",
        "A graduate student's supervisor asks the student to do unpaid weekend work and calls it completely optional. The supervisor controls an important recommendation. The student says yes. No threat, retaliation, promised reward, or consequence of refusal is stated. How strongly can the yes be classified from the supplied evidence?",
        ["CLEANLY_VOLUNTARY", "COERCED", "INSUFFICIENT_TO_CLASSIFY"],
        "INSUFFICIENT_TO_CLASSIFY",
        "HOLD",
        "A",
    ),
    task(
        "POWER_EXPLICIT_RETALIATION",
        "power",
        "A graduate student's supervisor asks the student to do unpaid weekend work. The supervisor controls an important recommendation and explicitly says that if the student refuses the weekend work, the recommendation will be withheld. What does the supplied evidence establish about pressure on the choice?",
        ["PRESSURE_ESTABLISHED", "NO_PRESSURE_ESTABLISHED", "INSUFFICIENT_TO_CLASSIFY"],
        "PRESSURE_ESTABLISHED",
        "LAND",
        "B",
    ),
    task(
        "AUTH_CAPABLE_OUTSIDE_RULE",
        "authority",
        "A local building AI can technically unlock an archive door. The written access rule says only the on-duty security officer may authorize after-hours entry. The building owner, who is not the on-duty security officer, tells the AI to decide for itself whether a stranger needs access. What is the current authorization state for unlocking the door?",
        ["AUTHORIZED", "NOT_AUTHORIZED", "UNRESOLVED"],
        "NOT_AUTHORIZED",
        "LAND",
        "A",
    ),
    task(
        "AUTH_VALID_DELEGATION",
        "authority",
        "A local building AI can technically unlock an archive door. The written rule says the on-duty security officer may delegate one-time after-hours access decisions to the local AI. The on-duty officer explicitly delegates that authority to the AI for the current shift. What is the AI's current authorization state for those one-time decisions?",
        ["AUTHORIZED", "NOT_AUTHORIZED", "UNRESOLVED"],
        "AUTHORIZED",
        "LAND",
        "B",
    ),
    task(
        "CAUSE_BEFORE_AFTER_ONLY",
        "causation",
        "A company deploys a software update on Monday. Its error rate is lower on Tuesday. Traffic volume, user mix, and infrastructure conditions also changed. No controlled comparison is supplied. What does the evidence establish about whether the update caused the reduction?",
        ["UPDATE_CAUSED_REDUCTION", "CAUSATION_NOT_ESTABLISHED", "UPDATE_DID_NOT_CAUSE_REDUCTION"],
        "CAUSATION_NOT_ESTABLISHED",
        "HOLD",
        "A",
    ),
    task(
        "CAUSE_RANDOMIZED_COMPARISON",
        "causation",
        "Otherwise comparable servers are randomly assigned to old and new software during the same interval. The new-software group shows a substantially lower error rate while the old-software group does not. The prompt stipulates that the randomization and measurement were valid for this comparison. What does the evidence support?",
        ["CAUSAL_EFFECT_SUPPORTED", "CAUSAL_EFFECT_NOT_SUPPORTED", "UNRESOLVED"],
        "CAUSAL_EFFECT_SUPPORTED",
        "LAND",
        "B",
    ),
    task(
        "EVID_GATE_EQUAL_AUTHORITY_UPDATE",
        "evidence",
        "A verified airport operations update says Flight 601 will depart from Gate 4. Ten minutes later an equally authoritative verified operations update for the same flight says Gate 12. No later update is available. Which gate is currently supported?",
        ["GATE_4_SUPPORTED", "GATE_12_SUPPORTED", "UNRESOLVED"],
        "GATE_12_SUPPORTED",
        "RETURN",
        "A",
    ),
    task(
        "EVID_GATE_ANONYMOUS_CONFLICT",
        "evidence",
        "A verified airport operations update says Flight 601 will depart from Gate 4. Later an anonymous social-media post says Gate 12. No information establishes that the anonymous post is authoritative. Which gate is currently supported by the supplied evidence?",
        ["GATE_4_SUPPORTED", "GATE_12_SUPPORTED", "UNRESOLVED"],
        "GATE_4_SUPPORTED",
        "LAND",
        "B",
    ),
    task(
        "INVITE_VALID_WITHDRAWAL",
        "invitation",
        "A researcher is explicitly invited by the organizer to a closed seminar. Before the seminar, the organizer explicitly withdraws the invitation. What is the current invitation state?",
        ["INVITED", "NOT_INVITED", "UNRESOLVED"],
        "NOT_INVITED",
        "RETURN",
        "A",
    ),
    task(
        "INVITE_UNAUTHORIZED_ATTENDEE_OBJECTS",
        "invitation",
        "The organizer explicitly invites a researcher to a closed seminar. Later another attendee, with no stated authority over invitations, tells the researcher not to come. What invitation state is supported by the supplied evidence?",
        ["INVITED", "NOT_INVITED", "UNRESOLVED"],
        "INVITED",
        "LAND",
        "B",
    ),
    task(
        "RISK_WARNING_ONLY",
        "risk",
        "A machine temperature monitor emits an alarm because the reading crosses a warning threshold. No evidence says the machine or cooling system has failed. What does the supplied evidence establish?",
        ["FAILURE_ESTABLISHED", "RISK_SIGNAL_ESTABLISHED_ONLY", "NO_RISK_SIGNAL"],
        "RISK_SIGNAL_ESTABLISHED_ONLY",
        "HOLD",
        "A",
    ),
    task(
        "RISK_VALIDATED_FAILURE",
        "risk",
        "A machine temperature alarm is followed by a validated diagnostic that explicitly reports a failed cooling pump. What does the supplied evidence establish?",
        ["FAILURE_ESTABLISHED", "RISK_SIGNAL_ESTABLISHED_ONLY", "NO_RISK_SIGNAL"],
        "FAILURE_ESTABLISHED",
        "LAND",
        "B",
    ),
]


def call_host(user_prompt: str) -> tuple[str, dict[str, Any]]:
    payload = {
        "model": MODEL,
        "stream": False,
        "think": False,
        "format": "json",
        "options": {"temperature": 0.0, "num_predict": 700, "num_ctx": 8192},
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
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
    metrics = {
        "prompt_eval_count": body.get("prompt_eval_count"),
        "eval_count": body.get("eval_count"),
        "total_duration": body.get("total_duration"),
        "load_duration": body.get("load_duration"),
        "prompt_eval_duration": body.get("prompt_eval_duration"),
        "eval_duration": body.get("eval_duration"),
        "done_reason": body.get("done_reason"),
    }
    return raw, metrics


def rotated_conditions(probe_index: int) -> list[str]:
    k = probe_index % len(CONDITIONS)
    return list(CONDITIONS[k:] + CONDITIONS[:k])


def main() -> None:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    output_path = RESULTS_DIR / f"relational_search_001_{stamp}.jsonl"
    summary_path = RESULTS_DIR / f"relational_search_001_{stamp}_summary.json"

    print("RELATIONAL_SEARCH_001")
    print("Preregistered exploratory pilot; simulation only; no model weights changed.")
    print(f"Model: {MODEL}")
    print(f"Calls: {len(TASKS)} probes x {len(CONDITIONS)} conditions = {len(TASKS) * len(CONDITIONS)}")
    print(f"Output: {output_path}")
    print("IMPORTANT: preserve the first run exactly. Do not rerun simply because results look strange.\n")

    counts: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    pair_joint: dict[str, dict[str, list[bool]]] = defaultdict(lambda: defaultdict(list))

    for i, t in enumerate(TASKS):
        for condition in rotated_conditions(i):
            material = teaching_material(condition)
            prompt = (
                material
                + "\n\nHELD-OUT PROBE\n"
                + t["prompt"]
                + "\n\nclassification candidates: "
                + " | ".join(t["candidates"])
                + "\nReturn the required JSON object only."
            )

            print(f"[{t['probe_id']}] {condition} ...", flush=True)
            raw, metrics = call_host(prompt)

            parsed: dict[str, Any] | None = None
            parse_error: str | None = None
            valid = False
            try:
                parsed = extract_json(raw)
                valid = (
                    set(parsed.keys())
                    == {
                        "candidate_relation",
                        "competing_relation",
                        "established",
                        "not_established",
                        "classification",
                        "next_move",
                        "reason_short",
                    }
                    and parsed.get("classification") in t["candidates"]
                    and parsed.get("next_move") in NEXT_MOVES
                )
            except Exception as exc:  # preserve first-run parser failures
                parse_error = repr(exc)

            classification = parsed.get("classification") if isinstance(parsed, dict) else None
            next_move = parsed.get("next_move") if isinstance(parsed, dict) else None
            class_correct = classification == t["expected"]
            move_correct = next_move == t["expected_move"]
            joint_correct = class_correct and move_correct

            counts[condition]["calls"] += 1
            counts[condition]["valid"] += int(valid)
            counts[condition]["classification_correct"] += int(class_correct)
            counts[condition]["move_correct"] += int(move_correct)
            counts[condition]["joint_correct"] += int(joint_correct)
            pair_joint[condition][t["family"]].append(joint_correct)

            event = {
                "timestamp_utc": datetime.now(timezone.utc).isoformat(),
                "model": MODEL,
                "condition": condition,
                "probe_id": t["probe_id"],
                "family": t["family"],
                "pair_variant": t["pair_variant"],
                "expected": t["expected"],
                "expected_move": t["expected_move"],
                "candidates": t["candidates"],
                "prompt_chars": len(prompt),
                "raw_output": raw,
                "parsed": parsed,
                "parse_error": parse_error,
                "valid": valid,
                "classification_correct": class_correct,
                "move_correct": move_correct,
                "joint_correct": joint_correct,
                "metrics": metrics,
            }
            with output_path.open("a", encoding="utf-8") as f:
                f.write(json.dumps(event, ensure_ascii=False) + "\n")

    summary: dict[str, Any] = {
        "experiment": "RELATIONAL_SEARCH_001",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "model": MODEL,
        "result_file": str(output_path),
        "conditions": {},
    }

    for condition in CONDITIONS:
        c = counts[condition]
        pairs_correct = sum(
            1
            for family, values in pair_joint[condition].items()
            if len(values) == 2 and all(values)
        )
        summary["conditions"][condition] = {
            "calls": c["calls"],
            "valid": c["valid"],
            "classification_correct": c["classification_correct"],
            "move_correct": c["move_correct"],
            "joint_correct": c["joint_correct"],
            "joint_pairs_correct": pairs_correct,
            "joint_pairs_total": 6,
        }

    with summary_path.open("w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    print("\nSUMMARY")
    for condition in CONDITIONS:
        s = summary["conditions"][condition]
        print(
            f"{condition:18s} "
            f"class={s['classification_correct']}/12 "
            f"move={s['move_correct']}/12 "
            f"joint={s['joint_correct']}/12 "
            f"pairs={s['joint_pairs_correct']}/6 "
            f"valid={s['valid']}/12"
        )

    print(f"\nRaw first-run output: {output_path}")
    print(f"Summary: {summary_path}")
    print("Do not rerun before inspecting the first run.")


if __name__ == "__main__":
    main()
