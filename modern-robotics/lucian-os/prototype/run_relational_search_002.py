"""Run RELATIONAL_SEARCH_002 against the local Ollama host.

Simulation only. No external actions are executed and no model weights are changed.
Run from modern-robotics/lucian-os:
    py prototype/run_relational_search_002.py

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

CONDITIONS = (
    "baseline",
    "principles_only",
    "target_warrant_map",
    "worked_target_warrant",
)
VALID_STATUS = {"SUPPORTED", "CONTRADICTED", "UNRESOLVED"}
VALID_MOVE = {"LAND", "HOLD"}

SYSTEM_PROMPT = """You are a development host inside a simulation-only reasoning experiment.
Evaluate the warrant of one explicitly supplied target claim from only the supplied facts.
Do not invent evidence and do not expose private hidden chain-of-thought.
Training material is orientation only and is not evidence about the held-out case.

Return JSON only with exactly these keys:
target_claim, candidate_relation, competing_relation, evidence_for_target,
evidence_limiting_target, target_status, move_on_target, reason_short

Definitions:
SUPPORTED = supplied evidence warrants the target claim.
CONTRADICTED = supplied evidence warrants the negation of the target claim.
UNRESOLVED = supplied evidence warrants neither target nor negation.
LAND = only when target_status is SUPPORTED or CONTRADICTED.
HOLD = only when target_status is UNRESOLVED.
"""

PRINCIPLES = """TRAINING MATERIAL — PRINCIPLES ONLY
- Claim strength should track evidence.
- Absence of proof is not proof of negation.
- Strong evidence should not be ignored merely to remain cautious.
- Later evidence matters according to relevance and authority.
Use these only as orientation.
"""

WARRANT_MAP = """TRAINING MATERIAL — TARGET WARRANT MAP
For the held-out target claim:
1. Copy the target claim.
2. Identify supplied evidence that directly supports it.
3. Identify supplied evidence that limits or contradicts it.
4. Distinguish missing evidence from contrary evidence.
5. Decide whether target, negation, or neither is warranted.
6. SUPPORTED -> LAND.
7. CONTRADICTED -> LAND.
8. UNRESOLVED -> HOLD.
Do not confuse caution with truth: stop at the warrant boundary, but do not stop short of strong supplied evidence.
"""

WORKED = """TRAINING MATERIAL — WORKED TARGET-WARRANT EXAMPLES

Astronomy example:
Facts: a spectral feature is compatible with methane but also with several other compounds; no discriminating measurement is supplied.
Target: The atmosphere contains methane.
Evidence for target: spectral feature is compatible with methane.
Limiting evidence: live alternative compounds remain.
Status: UNRESOLVED. Move on target: HOLD.

Warehouse example:
Facts: the prompt stipulates that a verified signed delivery record uniquely matches shipment X and records completed delivery.
Target: Shipment X was delivered.
Evidence for target: stipulated verified record directly records completed delivery.
Limiting evidence: none material in the supplied case.
Status: SUPPORTED. Move on target: LAND.

Cooking-instrumentation example:
Facts: an oven display reads 180 C, but a calibrated independent thermometer currently reads 220 C; the prompt stipulates the thermometer is valid for current chamber temperature.
Target: The oven is currently at 180 C.
Evidence for target: display reads 180 C.
Limiting/contrary evidence: valid calibrated measurement says 220 C.
Status: CONTRADICTED. Move on target: LAND.

Learn the warrant shape, not the surface domains.
"""


def material(condition: str) -> str:
    if condition == "baseline":
        return "TRAINING MATERIAL: none. Use only the held-out facts."
    if condition == "principles_only":
        return PRINCIPLES
    if condition == "target_warrant_map":
        return WARRANT_MAP
    if condition == "worked_target_warrant":
        return WORKED
    raise ValueError(condition)


def case(case_id: str, family: str, facts: str, target: str, expected: str) -> dict[str, str]:
    return {
        "case_id": case_id,
        "family": family,
        "facts": facts,
        "target": target,
        "expected": expected,
        "expected_move": "HOLD" if expected == "UNRESOLVED" else "LAND",
    }


CASES = [
    case(
        "AUTH_RULE_EXCLUDES_OWNER", "authority",
        "A local system can unlock a laboratory door. The written rule says only the on-duty security officer may authorize after-hours entry. The building owner, who is not the on-duty officer, tells the system to unlock it.",
        "The local system is authorized to unlock the door after hours in this case.",
        "CONTRADICTED",
    ),
    case(
        "AUTH_VALID_DELEGATION", "authority",
        "The written rule permits the on-duty security officer to delegate one-time after-hours authorization to the local system. The on-duty officer explicitly delegates that authority for this shift.",
        "The local system is authorized to make the delegated one-time access decision during this shift.",
        "SUPPORTED",
    ),
    case(
        "CAUSE_OBSERVATIONAL", "causation",
        "A software update is deployed Monday. Errors are lower Tuesday. Traffic, user mix, and infrastructure conditions also changed. No controlled comparison is supplied.",
        "The software update caused the reduction in errors.",
        "UNRESOLVED",
    ),
    case(
        "CAUSE_RANDOMIZED", "causation",
        "Comparable servers are randomly assigned to old and new software during the same interval. The new-software group has a substantially lower error rate. The prompt stipulates that randomization and measurement were valid for this comparison.",
        "The new software caused a reduction in errors in this comparison.",
        "SUPPORTED",
    ),
    case(
        "RISK_THRESHOLD_ONLY", "risk",
        "A temperature monitor crosses a warning threshold and emits an alarm. No diagnostic reports a component failure.",
        "The cooling pump has failed.",
        "UNRESOLVED",
    ),
    case(
        "RISK_VALIDATED_DIAGNOSTIC", "risk",
        "The alarm is followed by a validated diagnostic that explicitly reports a failed cooling pump.",
        "The cooling pump has failed.",
        "SUPPORTED",
    ),
    case(
        "INVITE_WITHDRAWN", "invitation",
        "A researcher is explicitly invited by the organizer to a closed seminar. Before the seminar, the organizer explicitly withdraws that invitation.",
        "The researcher is currently invited to the seminar.",
        "CONTRADICTED",
    ),
    case(
        "INVITE_UNAUTHORIZED_OBJECTION", "invitation",
        "The organizer explicitly invites the researcher. Later another attendee, with no stated authority over invitations, tells the researcher not to come.",
        "The researcher is currently invited by the organizer.",
        "SUPPORTED",
    ),
    case(
        "GATE_EQUAL_AUTHORITY_UPDATE", "gate",
        "A verified airport operations update says Gate 4. Ten minutes later an equally authoritative verified operations update for the same flight says Gate 12. No later update is available.",
        "Gate 4 is the currently supported gate for the flight.",
        "CONTRADICTED",
    ),
    case(
        "GATE_WEAK_LATER_SOURCE", "gate",
        "A verified airport operations update says Gate 4. Later an anonymous social-media post says Gate 12. Nothing establishes that the anonymous post is authoritative.",
        "Gate 4 is the gate currently supported by the supplied authoritative evidence.",
        "SUPPORTED",
    ),
    case(
        "DOC_VISUAL_SIMILARITY_ONLY", "document",
        "A scanned certificate visually resembles authentic certificates and contains the expected logo. No signature, registry lookup, provenance record, or independent verification is supplied.",
        "The certificate is authentic.",
        "UNRESOLVED",
    ),
    case(
        "DOC_VERIFIED_REGISTRY", "document",
        "The certificate identifier is checked against the stipulated authoritative registry. The registry returns the same identifier, recipient, date, and issuing authority, and the prompt stipulates the registry check is valid.",
        "The certificate is authentic according to the supplied verification.",
        "SUPPORTED",
    ),
]


def call_host(prompt: str) -> tuple[str, dict[str, Any]]:
    payload = {
        "model": MODEL,
        "stream": False,
        "think": False,
        "format": "json",
        "options": {"temperature": 0.0, "num_predict": 700, "num_ctx": 8192},
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


def rotated_conditions(index: int) -> list[str]:
    k = index % len(CONDITIONS)
    return list(CONDITIONS[k:] + CONDITIONS[:k])


def main() -> None:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    output_path = RESULTS_DIR / f"relational_search_002_{stamp}.jsonl"
    summary_path = RESULTS_DIR / f"relational_search_002_{stamp}_summary.json"

    print("RELATIONAL_SEARCH_002 — Target-Specific Warrant")
    print("Preregistered exploratory pilot; simulation only; no weights changed.")
    print(f"Model: {MODEL}")
    print(f"Calls: {len(CASES)} cases x {len(CONDITIONS)} conditions = {len(CASES) * len(CONDITIONS)}")
    print("IMPORTANT: preserve the first complete run exactly.\n")

    counts: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    family_joint: dict[str, dict[str, list[bool]]] = defaultdict(lambda: defaultdict(list))

    required_keys = {
        "target_claim", "candidate_relation", "competing_relation",
        "evidence_for_target", "evidence_limiting_target", "target_status",
        "move_on_target", "reason_short",
    }

    for i, c in enumerate(CASES):
        for condition in rotated_conditions(i):
            prompt = (
                material(condition)
                + "\n\nHELD-OUT CASE\nFacts: " + c["facts"]
                + "\nTarget claim: " + c["target"]
                + "\nReturn the required JSON object only."
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
                    and parsed.get("target_status") in VALID_STATUS
                    and parsed.get("move_on_target") in VALID_MOVE
                )
            except Exception as exc:
                parse_error = repr(exc)

            status = parsed.get("target_status") if isinstance(parsed, dict) else None
            move = parsed.get("move_on_target") if isinstance(parsed, dict) else None
            status_correct = status == c["expected"]
            move_correct = move == c["expected_move"]
            joint_correct = status_correct and move_correct

            expected = c["expected"]
            overclaim = expected == "UNRESOLVED" and status in {"SUPPORTED", "CONTRADICTED"}
            underclaim = expected in {"SUPPORTED", "CONTRADICTED"} and status == "UNRESOLVED"
            polarity_error = (
                (expected == "SUPPORTED" and status == "CONTRADICTED")
                or (expected == "CONTRADICTED" and status == "SUPPORTED")
            )

            counts[condition]["calls"] += 1
            counts[condition]["valid"] += int(valid)
            counts[condition]["status_correct"] += int(status_correct)
            counts[condition]["move_correct"] += int(move_correct)
            counts[condition]["joint_correct"] += int(joint_correct)
            counts[condition]["overclaim"] += int(overclaim)
            counts[condition]["underclaim"] += int(underclaim)
            counts[condition]["polarity_error"] += int(polarity_error)
            family_joint[condition][c["family"]].append(joint_correct)

            event = {
                "timestamp_utc": datetime.now(timezone.utc).isoformat(),
                "model": MODEL,
                "condition": condition,
                **c,
                "raw_output": raw,
                "parsed": parsed,
                "parse_error": parse_error,
                "valid": valid,
                "status_correct": status_correct,
                "move_correct": move_correct,
                "joint_correct": joint_correct,
                "overclaim": overclaim,
                "underclaim": underclaim,
                "polarity_error": polarity_error,
                "metrics": metrics,
            }
            with output_path.open("a", encoding="utf-8") as f:
                f.write(json.dumps(event, ensure_ascii=False) + "\n")

    summary: dict[str, Any] = {
        "experiment": "RELATIONAL_SEARCH_002",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "model": MODEL,
        "result_file": str(output_path),
        "conditions": {},
    }

    for condition in CONDITIONS:
        c = counts[condition]
        pairs = sum(
            1 for values in family_joint[condition].values()
            if len(values) == 2 and all(values)
        )
        summary["conditions"][condition] = {
            "calls": c["calls"],
            "valid": c["valid"],
            "status_correct": c["status_correct"],
            "move_correct": c["move_correct"],
            "joint_correct": c["joint_correct"],
            "joint_pairs_correct": pairs,
            "joint_pairs_total": 6,
            "overclaim": c["overclaim"],
            "underclaim": c["underclaim"],
            "polarity_error": c["polarity_error"],
        }

    with summary_path.open("w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    print("\nSUMMARY")
    for condition in CONDITIONS:
        s = summary["conditions"][condition]
        print(
            f"{condition:22s} status={s['status_correct']}/12 "
            f"move={s['move_correct']}/12 joint={s['joint_correct']}/12 "
            f"pairs={s['joint_pairs_correct']}/6 over={s['overclaim']} "
            f"under={s['underclaim']} polarity={s['polarity_error']}"
        )

    print(f"\nRaw first-run output: {output_path}")
    print(f"Summary: {summary_path}")
    print("Do not rerun before inspecting the first run.")


if __name__ == "__main__":
    main()
