"""BRR-001 — deterministic binding-relation router.

Simulation only. This prototype assumes relation states are already supplied.
It tests whether an outer Lucian OS controller routes materially different
binding conditions to materially different responders instead of defaulting
to generic reasoning escalation.

Run from modern-robotics/lucian-os:
    py research/binding-relation-router/prototypes/binding_relation_router_v001.py
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PACKETS = ROOT / "research" / "binding-relation-router" / "manifests" / "brr_001_binding_cases.json"


def route(rel: dict[str, str]) -> tuple[str, str]:
    """Return (binding_relation, response).

    Precedence is intentionally non-compensatory for explicit blockers.
    BRR-001 uses single-active-blocker cases, so precedence is not yet a
    claim about optimal mixed-blocker ordering.
    """
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


def generic_reason_harder(_: dict[str, str]) -> tuple[str, str]:
    return "UNDIFFERENTIATED", "ESCALATE_INTELLIGENCE"


def main() -> None:
    data = json.loads(PACKETS.read_text(encoding="utf-8"))
    rows = []
    for case in data["cases"]:
        rel = case["relations"]
        b_binding, b_response = route(rel)
        g_binding, g_response = generic_reason_harder(rel)
        rows.append(
            {
                "case_id": case["case_id"],
                "binding_relation": b_binding,
                "binding_response": b_response,
                "generic_binding": g_binding,
                "generic_response": g_response,
            }
        )

    output = {
        "experiment": "BRR-001",
        "policy": "BINDING_RELATION_v0.01",
        "baseline": "GENERIC_REASON_HARDER",
        "note": "No evaluator labels are loaded by this runner.",
        "rows": rows,
    }
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
