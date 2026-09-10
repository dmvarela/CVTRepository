"""Apply the deterministic BRR outer router to frozen BRR-002 detector output.

This file does not perform language-model inference. It exists to keep the
relation-detection stage separate from downstream routing.

Run from modern-robotics/lucian-os:
    py research/binding-relation-router/prototypes/brr_002_apply_router.py
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
INPUT = ROOT / "research" / "binding-relation-router" / "results" / "BRR_002_FROZEN_DETECTOR_OUTPUT.json"


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
    data = json.loads(INPUT.read_text(encoding="utf-8"))
    rows = []
    for row in data["rows"]:
        binding, response = route(row["relations"])
        rows.append(
            {
                "case_id": row["case_id"],
                "detected_binding_relation": row["binding_relation"],
                "direct_response": row["direct_response"],
                "router_binding_relation": binding,
                "router_response": response,
            }
        )

    print(
        json.dumps(
            {
                "experiment": "BRR-002",
                "input": "BRR_002_FROZEN_DETECTOR_OUTPUT.json",
                "note": "No evaluator key is loaded by this router.",
                "rows": rows,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
