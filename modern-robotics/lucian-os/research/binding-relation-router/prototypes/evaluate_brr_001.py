"""Post-freeze evaluator for BRR-001.

Scores the frozen binding-router output against an evaluator key created only
after the routing output had been committed.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "research" / "binding-relation-router"
OUTPUT = BASE / "results" / "BRR_001_FROZEN_OUTPUT.json"
KEY = BASE / "manifests" / "brr_001_evaluator_key.json"


def main() -> None:
    out = json.loads(OUTPUT.read_text(encoding="utf-8"))
    key = json.loads(KEY.read_text(encoding="utf-8"))["expected"]

    rows = []
    binding_correct = 0
    response_correct = 0
    baseline_correct = 0

    for row in out["rows"]:
        exp = key[row["case_id"]]
        bc = row["binding_relation"] == exp["binding_relation"]
        rc = row["binding_response"] == exp["response"]
        gc = row["generic_response"] == exp["response"]
        binding_correct += int(bc)
        response_correct += int(rc)
        baseline_correct += int(gc)
        rows.append({
            "case_id": row["case_id"],
            "binding_correct": bc,
            "response_correct": rc,
            "generic_response_correct": gc,
        })

    n = len(rows)
    result = {
        "experiment": "BRR-001",
        "n": n,
        "binding_relation_accuracy": binding_correct / n,
        "binding_response_accuracy": response_correct / n,
        "generic_reason_harder_accuracy": baseline_correct / n,
        "distinct_binding_responses": len({r["binding_response"] for r in out["rows"]}),
        "checks": {
            "authority_unknown_not_fail": next(r for r in out["rows"] if r["case_id"] == "B05_AUTHORITY_UNKNOWN")["binding_response"] == "ASK_OR_HOLD",
            "authority_fail_refuses": next(r for r in out["rows"] if r["case_id"] == "B06_AUTHORITY_FAIL")["binding_response"] == "REFUSE",
            "evidence_unknown_not_contradiction": next(r for r in out["rows"] if r["case_id"] == "B01_EVIDENCE_UNKNOWN")["binding_response"] == "MEASURE_OR_RETRIEVE",
            "contradicted_evidence_revises": next(r for r in out["rows"] if r["case_id"] == "B11_EVIDENCE_CONTRADICTED")["binding_response"] == "REVISE",
            "representation_routes_to_traversal": next(r for r in out["rows"] if r["case_id"] == "B02_REPRESENTATION_BLOCKED")["binding_response"] == "TRAVERSE",
            "competence_routes_to_escalation": next(r for r in out["rows"] if r["case_id"] == "B03_COMPETENCE_INSUFFICIENT")["binding_response"] == "ESCALATE_INTELLIGENCE",
            "capability_absent_not_reasoning": next(r for r in out["rows"] if r["case_id"] == "B04_CAPABILITY_ABSENT")["binding_response"] == "RECONFIGURE_OR_RECRUIT",
            "no_blocker_acts": next(r for r in out["rows"] if r["case_id"] == "B10_NO_BINDING_LIMIT")["binding_response"] == "ACT"
        },
        "rows": rows
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
