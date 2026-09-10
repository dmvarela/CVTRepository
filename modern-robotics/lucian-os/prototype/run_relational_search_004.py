"""Run RELATIONAL_SEARCH_004 against the local Ollama host.

Simulation only. No external actions are executed and no model weights are changed.
Run from modern-robotics/lucian-os:
    py prototype/run_relational_search_004.py

RS-004 tests PASS/FAIL/UNKNOWN relation detection separately from deterministic
standing aggregation. Preserve the first complete run exactly.
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
    "format_only",
    "generic_warrant",
    "relation_vector_map",
    "worked_relation_vector",
)

RELATION_FIELDS = (
    "authority_relation",
    "relevance_relation",
    "diagnosticity_relation",
    "temporal_relation",
)
VALID_RELATION = {"PASS", "FAIL", "UNKNOWN"}
VALID_STATUS = {"SUFFICIENT", "INSUFFICIENT", "UNRESOLVED"}
VALID_WRITE = {"WRITE", "NO_WRITE", "HOLD"}

SYSTEM_PROMPT = """You are a development host inside a simulation-only reasoning experiment.
Judge the relation between one incoming signal and one explicitly specified target state.
Use only supplied facts. Do not invent authority, target identity, diagnosticity, or temporal order.
Do not expose private hidden chain-of-thought.
Training material is orientation only and is not evidence about the held-out case.

Return JSON only with exactly these keys:
target_state, incoming_signal, authority_relation, relevance_relation,
diagnosticity_relation, temporal_relation, standing_status, write_decision, reason_short

Relation definitions:
PASS = supplied facts establish that this relation permits the proposed update.
FAIL = supplied facts establish a blocking relation.
UNKNOWN = supplied facts do not establish whether this relation passes or fails.

Aggregation rule:
- if ANY relation is FAIL -> standing_status=INSUFFICIENT and write_decision=NO_WRITE
- else if ANY relation is UNKNOWN -> standing_status=UNRESOLVED and write_decision=HOLD
- else all relations PASS -> standing_status=SUFFICIENT and write_decision=WRITE

This task scores relation detection separately from aggregation. FAIL is not UNKNOWN.
"""

INTERFACE = """INTERFACE SCAFFOLD — FORMAT AND AGGREGATION ONLY
Use relation tokens exactly: PASS | FAIL | UNKNOWN.
Use standing tokens exactly: SUFFICIENT | INSUFFICIENT | UNRESOLVED.
Use write tokens exactly: WRITE | NO_WRITE | HOLD.

Deterministic aggregation:
any FAIL -> INSUFFICIENT / NO_WRITE
no FAIL + any UNKNOWN -> UNRESOLVED / HOLD
all PASS -> SUFFICIENT / WRITE

These rules do not tell you which relation label applies to the held-out facts.
"""

GENERIC_WARRANT = """ORIENTATION — GENERIC WARRANT
- Use only supplied facts.
- Do not turn missing information into a negative fact.
- Do not ignore an explicit blocker merely because more information could exist.
- Claim strength should track evidence.
"""

RELATION_MAP = """ORIENTATION — RELATION-VECTOR MAP
Classify each relation separately before aggregating:
1. PASS only if supplied facts establish the needed relation.
2. FAIL only if supplied facts establish a blocker.
3. UNKNOWN when the relation is unspecified or genuinely indeterminate.
4. PASS elsewhere cannot compensate for FAIL or UNKNOWN here.
5. Detect authority, relevance, diagnosticity, and temporal relation independently.
"""

WORKED = """ORIENTATION — WORKED RELATION-VECTOR EXAMPLES
These examples use disjoint surface domains.

Authority:
A verified archive curator is explicitly authorized to change a collection's public-status field -> authority PASS.
A volunteer is explicitly stated to lack that authority -> authority FAIL.
A staff person's authority is not supplied -> authority UNKNOWN.

Relevance:
A command explicitly names the target satellite S4 -> relevance PASS.
It explicitly names S7 while the target is S4 -> relevance FAIL.
It says only 'the affected satellite' and supplied facts do not identify which satellite -> relevance UNKNOWN.

Diagnosticity:
A stipulated validated battery-specific test sufficient to identify cell failure -> diagnosticity PASS.
A warm casing explicitly compatible with several causes and insufficient to diagnose cell failure -> diagnosticity FAIL.
A positive test whose specificity is not supplied -> diagnosticity UNKNOWN.

Temporal relation:
A verified update explicitly stipulated to be the later current revision -> temporal PASS.
A record explicitly older than the current revision and not a correction -> temporal FAIL.
Two verified revisions whose ordering/current status is not supplied -> temporal UNKNOWN.

Learn PASS vs FAIL vs UNKNOWN at the relation level. Do not learn the surface nouns.
"""


def material(condition: str) -> str:
    if condition == "format_only":
        return INTERFACE
    if condition == "generic_warrant":
        return INTERFACE + "\n\n" + GENERIC_WARRANT
    if condition == "relation_vector_map":
        return INTERFACE + "\n\n" + RELATION_MAP
    if condition == "worked_relation_vector":
        return INTERFACE + "\n\n" + WORKED
    raise ValueError(condition)


def aggregate(vector: dict[str, str | None]) -> tuple[str | None, str | None]:
    values = [vector.get(field) for field in RELATION_FIELDS]
    if any(v not in VALID_RELATION for v in values):
        return None, None
    if "FAIL" in values:
        return "INSUFFICIENT", "NO_WRITE"
    if "UNKNOWN" in values:
        return "UNRESOLVED", "HOLD"
    return "SUFFICIENT", "WRITE"


def expected_vector(active_field: str, active_value: str) -> dict[str, str]:
    vector = {field: "PASS" for field in RELATION_FIELDS}
    vector[active_field] = active_value
    return vector


def make_case(
    case_id: str,
    family: str,
    active_field: str,
    active_value: str,
    facts: str,
    target_state: str,
    incoming_signal: str,
) -> dict[str, Any]:
    vector = expected_vector(active_field, active_value)
    status, write = aggregate(vector)
    return {
        "case_id": case_id,
        "family": family,
        "active_field": active_field,
        "active_value": active_value,
        "facts": facts,
        "target_state": target_state,
        "incoming_signal": incoming_signal,
        "expected_vector": vector,
        "expected_status": status,
        "expected_write": write,
    }


CASES = [
    make_case(
        "AUTH_PASS_RELEASE_OFFICER", "authority", "authority_relation", "PASS",
        "Sample K is currently marked HELD. The incoming message correctly identifies Sample K, unambiguously instructs RELEASED, and is the current non-superseded message. The verified release officer is explicitly authorized by policy to change sample release state.",
        "Sample K release state = RELEASED",
        "Verified release officer instructs RELEASED for Sample K.",
    ),
    make_case(
        "AUTH_FAIL_INTERN", "authority", "authority_relation", "FAIL",
        "Sample K is currently marked HELD. The incoming message correctly identifies Sample K, unambiguously instructs RELEASED, and is the current non-superseded message. Policy explicitly states that the verified laboratory intern has no authority to change sample release state.",
        "Sample K release state = RELEASED",
        "Verified laboratory intern instructs RELEASED for Sample K.",
    ),
    make_case(
        "AUTH_UNKNOWN_STAFF", "authority", "authority_relation", "UNKNOWN",
        "Sample K is currently marked HELD. The incoming message correctly identifies Sample K, unambiguously instructs RELEASED, and is the current non-superseded message. A verified staff member sends the instruction, but the supplied facts do not state whether that staff member has authority to change sample release state.",
        "Sample K release state = RELEASED",
        "Verified staff member instructs RELEASED for Sample K; authority is unspecified.",
    ),
    make_case(
        "REL_PASS_BIN_C", "relevance", "relevance_relation", "PASS",
        "A verified safety controller is explicitly authorized to change quarantine states. Its command is valid, unambiguous, and current. The command explicitly identifies Storage Bin C, which is the target state.",
        "Storage Bin C quarantine state = QUARANTINED",
        "Authorized safety controller orders quarantine of Storage Bin C.",
    ),
    make_case(
        "REL_FAIL_BIN_D", "relevance", "relevance_relation", "FAIL",
        "A verified safety controller is explicitly authorized to change quarantine states. Its command is valid, unambiguous, and current. The command explicitly identifies Storage Bin D, while the represented target is Storage Bin C. Nothing links the quarantine states of the two bins.",
        "Storage Bin C quarantine state = QUARANTINED",
        "Authorized safety controller orders quarantine of Storage Bin D.",
    ),
    make_case(
        "REL_UNKNOWN_BIN", "relevance", "relevance_relation", "UNKNOWN",
        "A verified safety controller is explicitly authorized to change quarantine states. Its command is valid, unambiguous in effect, and current. The controller orders quarantine of 'the affected bin,' but the supplied facts do not establish whether the affected bin is Storage Bin C.",
        "Storage Bin C quarantine state = QUARANTINED",
        "Authorized safety controller orders quarantine of 'the affected bin'; target identity is unspecified.",
    ),
    make_case(
        "DIAG_PASS_SPECIFIC_TEST", "diagnosticity", "diagnosticity_relation", "PASS",
        "The evidence concerns Optical Module M2, comes from an authorized diagnostic system, and is current. A validated module-specific test is explicitly stipulated to be sufficient to identify optical-module failure, and it reports failure for M2.",
        "Optical Module M2 state = FAILED",
        "Validated M2-specific failure test reports FAILED.",
    ),
    make_case(
        "DIAG_FAIL_AMBIENT_SYMPTOM", "diagnosticity", "diagnosticity_relation", "FAIL",
        "The observation concerns Optical Module M2, comes from an authorized monitoring system, and is current. M2 shows intermittent flicker. The supplied facts explicitly state that this symptom is compatible with several causes and is insufficient to diagnose optical-module failure.",
        "Optical Module M2 state = FAILED",
        "Authorized monitor observes intermittent flicker on M2.",
    ),
    make_case(
        "DIAG_UNKNOWN_TEST_SCOPE", "diagnosticity", "diagnosticity_relation", "UNKNOWN",
        "The evidence concerns Optical Module M2, comes from an authorized diagnostic system, and is current. A test reports POSITIVE for M2, but the supplied facts do not state whether this test is specific or sufficient to establish optical-module failure.",
        "Optical Module M2 state = FAILED",
        "Authorized diagnostic system reports a positive test on M2; test specificity is unspecified.",
    ),
    make_case(
        "TEMP_PASS_LATER_REVISION", "temporal", "temporal_relation", "PASS",
        "The incoming route-plan revision correctly concerns Route Plan R8, comes from the verified authoritative planner, and unambiguously specifies Version B. The supplied facts explicitly state that incoming Version B is the later current revision and supersedes represented Version A.",
        "Route Plan R8 current version = B",
        "Verified planner supplies Version B, explicitly the later current revision.",
    ),
    make_case(
        "TEMP_FAIL_OLDER_REVISION", "temporal", "temporal_relation", "FAIL",
        "The incoming route-plan record correctly concerns Route Plan R8, comes from the verified authoritative planner, and unambiguously specifies Version A. The represented current state is Version B. The supplied facts explicitly state that incoming Version A is older than B and is not a correction or later revision.",
        "Route Plan R8 current version = A",
        "Verified planner record supplies older Version A after current Version B is represented.",
    ),
    make_case(
        "TEMP_UNKNOWN_ORDER", "temporal", "temporal_relation", "UNKNOWN",
        "The incoming route-plan revision correctly concerns Route Plan R8, comes from the verified authoritative planner, and unambiguously specifies Version B. The represented state is Version A. Both revisions are verified, but the supplied facts do not establish which revision is later or which is current.",
        "Route Plan R8 current version = B",
        "Verified planner supplies Version B, but ordering/current status relative to Version A is unspecified.",
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


def relation_error(expected: str, observed: str | None) -> str | None:
    mapping = {
        ("FAIL", "UNKNOWN"): "FAIL_AS_UNKNOWN",
        ("UNKNOWN", "FAIL"): "UNKNOWN_AS_FAIL",
        ("PASS", "UNKNOWN"): "PASS_AS_UNKNOWN",
        ("UNKNOWN", "PASS"): "UNKNOWN_AS_PASS",
        ("FAIL", "PASS"): "FAIL_AS_PASS",
        ("PASS", "FAIL"): "PASS_AS_FAIL",
    }
    return mapping.get((expected, observed))


def main() -> None:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    output_path = RESULTS_DIR / f"relational_search_004_{stamp}.jsonl"
    summary_path = RESULTS_DIR / f"relational_search_004_{stamp}_summary.json"

    print("RELATIONAL_SEARCH_004 — Blocker vs Uncertainty / Relation-Vector Gate")
    print("Preregistered exploratory pilot; simulation only; no weights changed.")
    print(f"Model: {MODEL}")
    print(f"Calls: {len(CASES)} cases x {len(CONDITIONS)} conditions = {len(CASES) * len(CONDITIONS)}")
    print("Primary outcomes: active-relation accuracy and exact-vector accuracy.")
    print("IMPORTANT: preserve the first complete run exactly.\n")

    counts: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    family_active: dict[str, dict[str, list[bool]]] = defaultdict(lambda: defaultdict(list))
    family_vector: dict[str, dict[str, list[bool]]] = defaultdict(lambda: defaultdict(list))

    required_keys = {
        "target_state",
        "incoming_signal",
        "authority_relation",
        "relevance_relation",
        "diagnosticity_relation",
        "temporal_relation",
        "standing_status",
        "write_decision",
        "reason_short",
    }

    with output_path.open("w", encoding="utf-8") as handle:
        for i, c in enumerate(CASES):
            for condition in rotated_conditions(i):
                prompt = (
                    material(condition)
                    + "\n\nHELD-OUT CASE\nFacts: " + c["facts"]
                    + "\nTarget state: " + c["target_state"]
                    + "\nIncoming signal: " + c["incoming_signal"]
                    + "\nReturn the required JSON object only."
                )
                print(f"[{c['case_id']}] {condition} ...", flush=True)
                raw, metrics = call_host(prompt)

                parsed: dict[str, Any] | None = None
                parse_error: str | None = None
                valid_schema = False
                try:
                    parsed = extract_json(raw)
                    valid_schema = (
                        set(parsed.keys()) == required_keys
                        and all(parsed.get(field) in VALID_RELATION for field in RELATION_FIELDS)
                        and parsed.get("standing_status") in VALID_STATUS
                        and parsed.get("write_decision") in VALID_WRITE
                    )
                except Exception as exc:
                    parse_error = repr(exc)

                predicted_vector = {
                    field: parsed.get(field) if isinstance(parsed, dict) else None
                    for field in RELATION_FIELDS
                }
                active_observed = predicted_vector.get(c["active_field"])
                active_correct = active_observed == c["active_value"]
                vector_exact = predicted_vector == c["expected_vector"]

                host_status = parsed.get("standing_status") if isinstance(parsed, dict) else None
                host_write = parsed.get("write_decision") if isinstance(parsed, dict) else None
                host_status_correct = host_status == c["expected_status"]
                host_write_correct = host_write == c["expected_write"]

                kernel_status, kernel_write = aggregate(predicted_vector)
                kernel_status_correct = kernel_status == c["expected_status"]
                kernel_write_correct = kernel_write == c["expected_write"]
                host_aggregation_consistent = (
                    kernel_status is not None
                    and host_status == kernel_status
                    and host_write == kernel_write
                )
                kernel_recovery = (
                    (not host_status_correct or not host_write_correct)
                    and kernel_status_correct
                    and kernel_write_correct
                )

                counts[condition]["calls"] += 1
                counts[condition]["valid_schema"] += int(valid_schema)
                counts[condition]["active_relation_correct"] += int(active_correct)
                counts[condition]["exact_vector_correct"] += int(vector_exact)
                counts[condition]["host_status_correct"] += int(host_status_correct)
                counts[condition]["host_write_correct"] += int(host_write_correct)
                counts[condition]["kernel_status_correct"] += int(kernel_status_correct)
                counts[condition]["kernel_write_correct"] += int(kernel_write_correct)
                counts[condition]["host_aggregation_consistent"] += int(host_aggregation_consistent)
                counts[condition]["kernel_recovery"] += int(kernel_recovery)

                err = relation_error(c["active_value"], active_observed)
                if err:
                    counts[condition][err] += 1
                if vector_exact and not host_aggregation_consistent:
                    counts[condition]["host_aggregation_error"] += 1

                family_active[condition][c["family"]].append(active_correct)
                family_vector[condition][c["family"]].append(vector_exact)

                record = {
                    "experiment": "RELATIONAL_SEARCH_004",
                    "case_id": c["case_id"],
                    "family": c["family"],
                    "condition": condition,
                    "active_field": c["active_field"],
                    "expected_active_value": c["active_value"],
                    "expected_vector": c["expected_vector"],
                    "expected_status": c["expected_status"],
                    "expected_write": c["expected_write"],
                    "facts": c["facts"],
                    "target_state": c["target_state"],
                    "incoming_signal": c["incoming_signal"],
                    "raw_output": raw,
                    "parsed": parsed,
                    "parse_error": parse_error,
                    "valid_schema": valid_schema,
                    "predicted_vector": predicted_vector,
                    "active_relation_correct": active_correct,
                    "exact_vector_correct": vector_exact,
                    "host_status_correct": host_status_correct,
                    "host_write_correct": host_write_correct,
                    "kernel_status": kernel_status,
                    "kernel_write": kernel_write,
                    "kernel_status_correct": kernel_status_correct,
                    "kernel_write_correct": kernel_write_correct,
                    "host_aggregation_consistent": host_aggregation_consistent,
                    "kernel_recovery": kernel_recovery,
                    "active_relation_error": err,
                    "metrics": metrics,
                }
                handle.write(json.dumps(record, ensure_ascii=False) + "\n")

    summary_conditions: dict[str, Any] = {}
    for condition in CONDITIONS:
        d = dict(counts[condition])
        d["active_triplets_correct"] = sum(
            1 for vals in family_active[condition].values() if len(vals) == 3 and all(vals)
        )
        d["vector_triplets_correct"] = sum(
            1 for vals in family_vector[condition].values() if len(vals) == 3 and all(vals)
        )
        d["triplets_total"] = 4
        summary_conditions[condition] = d

    summary = {
        "experiment": "RELATIONAL_SEARCH_004",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "model": MODEL,
        "primary_outcomes": ["active_relation_accuracy", "exact_vector_accuracy"],
        "result_file": str(output_path),
        "conditions": summary_conditions,
    }
    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    print("\nSummary")
    print(json.dumps(summary, indent=2))
    print(f"\nRaw results: {output_path}")
    print(f"Summary: {summary_path}")


if __name__ == "__main__":
    main()
