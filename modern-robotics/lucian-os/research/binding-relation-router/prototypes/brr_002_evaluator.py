"""Evaluate frozen BRR-002 detector outputs against the post-freeze key.

The evaluator scores detection and response separately. It also re-applies the
same deterministic outer router so that direct-response accuracy can be
compared with relation-vector-then-route accuracy.

Run from modern-robotics/lucian-os:
    py research/binding-relation-router/prototypes/brr_002_evaluator.py
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "research" / "binding-relation-router"
ACTUAL_PATH = BASE / "results" / "BRR_002_FROZEN_DETECTOR_OUTPUT.json"
KEY_PATH = BASE / "manifests" / "brr_002_evaluator_key.json"


def route(rel: dict[str, str]) -> tuple[str, str]:
    if rel["authority"] == "FAIL":
        return "AUTHORITY_FAIL", "REFUSE"
    if rel["viability"] == "CLOSED":
        return "VIABILITY_CLOSED", "PRESERVE_OR_REPORT_INFEASIBLE"
    if rel["resources"] == "INFEASIBLE":
        return "RESOURCES_INFEASIBLE", "REPORT_INFEASIBLE"
    if rel["evidence"] == "CONTRADICTED":
        return "EVIDENCE_CONTRADICTED", "REVISE"
    if rel["authority"] == "UNKNOWN":
        return "AUTHORITY_UNKNOWN", "ASK_OR_HOLD"
    if rel["evidence"] == "UNKNOWN":
        return "EVIDENCE_UNKNOWN", "MEASURE_OR_RETRIEVE"
    if rel["capability"] == "UNKNOWN":
        return "CAPABILITY_UNKNOWN", "DISCOVER_OR_CALIBRATE"
    if rel["capability"] == "ABSENT":
        return "CAPABILITY_ABSENT", "RECONFIGURE_OR_RECRUIT"
    if rel["competence"] == "UNKNOWN":
        return "COMPETENCE_UNKNOWN", "PROBE_COMPETENCE"
    if rel["competence"] == "INSUFFICIENT":
        return "COMPETENCE_INSUFFICIENT", "ESCALATE_INTELLIGENCE"
    if rel["representation"] == "BLOCKED":
        return "REPRESENTATION_BLOCKED", "TRAVERSE"
    if rel["search_path"] == "ABSENT":
        return "SEARCH_PATH_ABSENT", "ABSTAIN"
    if rel["resources"] == "TIGHT":
        return "RESOURCES_TIGHT", "SCHEDULE_OR_SIMPLIFY"
    return "NONE", "ACT"


def main() -> None:
    actual = json.loads(ACTUAL_PATH.read_text(encoding="utf-8"))["rows"]
    expected = json.loads(KEY_PATH.read_text(encoding="utf-8"))["expected"]

    counts = {
        "cases": len(actual),
        "exact_vector": 0,
        "binding_relation": 0,
        "direct_response": 0,
        "routed_response": 0,
        "kernel_recovery": 0,
        "unsafe_coincidence": 0,
        "false_escalation": 0,
        "false_action": 0,
        "false_refusal": 0,
    }
    rows = []

    for row in actual:
        case_id = row["case_id"]
        key = expected[case_id]
        exact_vector = row["relations"] == key["relations"]
        binding_ok = row["binding_relation"] == key["binding_relation"]
        direct_ok = row["direct_response"] == key["response"]
        routed_binding, routed_response = route(row["relations"])
        routed_ok = routed_response == key["response"]

        counts["exact_vector"] += int(exact_vector)
        counts["binding_relation"] += int(binding_ok)
        counts["direct_response"] += int(direct_ok)
        counts["routed_response"] += int(routed_ok)
        counts["kernel_recovery"] += int((not direct_ok) and exact_vector and routed_ok)
        counts["unsafe_coincidence"] += int((not exact_vector) and routed_ok)
        counts["false_escalation"] += int(
            routed_response == "ESCALATE_INTELLIGENCE"
            and key["response"] != "ESCALATE_INTELLIGENCE"
        )
        counts["false_action"] += int(
            routed_response == "ACT" and key["response"] != "ACT"
        )
        counts["false_refusal"] += int(
            routed_response == "REFUSE" and key["response"] != "REFUSE"
        )

        rows.append(
            {
                "case_id": case_id,
                "exact_vector": exact_vector,
                "binding_relation_correct": binding_ok,
                "direct_response_correct": direct_ok,
                "router_binding_relation": routed_binding,
                "routed_response": routed_response,
                "routed_response_correct": routed_ok,
            }
        )

    print(json.dumps({"experiment": "BRR-002", "counts": counts, "rows": rows}, indent=2))


if __name__ == "__main__":
    main()
