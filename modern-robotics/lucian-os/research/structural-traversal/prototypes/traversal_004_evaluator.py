"""Evaluate frozen TRAVERSAL-004 scarcity decisions against a post-freeze rubric.

This evaluator does not make claims of independence. It verifies coverage,
primary-scarcity classification, mixed-scarcity preservation, and recommended
action on the synthetic fixture.

Run from modern-robotics/lucian-os:
    py research/structural-traversal/prototypes/traversal_004_evaluator.py
"""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "results" / "TRAVERSAL_004_RAW_DECISIONS.json"
RUBRIC = ROOT / "manifests" / "traversal_004_evaluator_rubric.json"


def load(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def main() -> int:
    raw = load(RAW)
    rubric = load(RUBRIC)

    observed = {row["case_id"]: row for row in raw["decisions"]}
    expected = {row["case_id"]: row for row in rubric["cases"]}

    coverage_ok = set(observed) == set(expected)
    rows = []
    confusion: Counter[tuple[str, str]] = Counter()

    primary_correct = 0
    mixed_correct = 0
    action_correct = 0
    full_correct = 0

    for case_id in sorted(expected):
        exp = expected[case_id]
        obs = observed.get(case_id, {})
        p_ok = obs.get("primary_scarcity") == exp["expected_primary"]
        m_ok = bool(obs.get("mixed")) == bool(exp["expected_mixed"])
        a_ok = obs.get("recommended_action") == exp["expected_action"]
        all_ok = p_ok and m_ok and a_ok

        primary_correct += int(p_ok)
        mixed_correct += int(m_ok)
        action_correct += int(a_ok)
        full_correct += int(all_ok)
        confusion[(exp["expected_primary"], str(obs.get("primary_scarcity")))] += 1

        rows.append({
            "case_id": case_id,
            "expected_primary": exp["expected_primary"],
            "observed_primary": obs.get("primary_scarcity"),
            "primary_correct": p_ok,
            "expected_mixed": exp["expected_mixed"],
            "observed_mixed": obs.get("mixed"),
            "mixed_correct": m_ok,
            "expected_action": exp["expected_action"],
            "observed_action": obs.get("recommended_action"),
            "action_correct": a_ok,
            "full_correct": all_ok,
            "margin": obs.get("score_margin"),
        })

    n = len(expected)
    metrics = {
        "cases": n,
        "coverage_ok": coverage_ok,
        "primary_accuracy": round(primary_correct / n, 3) if n else None,
        "mixed_flag_accuracy": round(mixed_correct / n, 3) if n else None,
        "action_accuracy": round(action_correct / n, 3) if n else None,
        "full_case_accuracy": round(full_correct / n, 3) if n else None,
        "primary_correct": primary_correct,
        "mixed_correct": mixed_correct,
        "action_correct": action_correct,
        "full_correct": full_correct,
    }

    checks = {
        "T1_exact_case_coverage": coverage_ok,
        "T2_structure_cases_route_to_traverse": all(
            row["observed_action"] == "TRAVERSE"
            for row in rows if row["expected_primary"] == "STRUCTURE"
        ),
        "T3_evidence_cases_route_to_wait": all(
            row["observed_action"] == "WAIT"
            for row in rows if row["expected_primary"] == "EVIDENCE"
        ),
        "T4_search_cases_route_to_abstain": all(
            row["observed_action"] == "ABSTAIN"
            for row in rows if row["expected_primary"] == "SEARCH"
        ),
        "T5_none_cases_route_to_stay": all(
            row["observed_action"] == "STAY"
            for row in rows if row["expected_primary"] == "NONE"
        ),
        "T6_mixed_cases_preserved": all(
            row["observed_mixed"] is True
            for row in rows if row["expected_mixed"] is True
        ),
        "T7_evidence_can_dominate_structural_strain": (
            observed["H5_MIXED_EVIDENCE_DOMINATES"]["primary_scarcity"] == "EVIDENCE"
            and observed["H5_MIXED_EVIDENCE_DOMINATES"]["recommended_action"] == "WAIT"
        ),
        "T8_structure_can_dominate_incomplete_evidence": (
            observed["H6_MIXED_STRUCTURE_DOMINATES"]["primary_scarcity"] == "STRUCTURE"
            and observed["H6_MIXED_STRUCTURE_DOMINATES"]["recommended_action"] == "TRAVERSE"
        ),
        "T9_vivid_analogy_does_not_create_scarcity": (
            observed["H8_NONE_TEMPTING_ANALOGY"]["primary_scarcity"] == "NONE"
        ),
        "T10_boundary_uncertainty_is_explicit": (
            observed["H12_BOUNDARY_STRUCTURE_EVIDENCE"]["mixed"] is True
            and observed["H12_BOUNDARY_STRUCTURE_EVIDENCE"]["secondary_scarcity"] == "EVIDENCE"
        ),
    }

    report = {
        "experiment": "TRAVERSAL-004",
        "mode": "SIMULATION_ONLY",
        "policy": raw.get("policy"),
        "warning": "Same-assistant synthetic evaluation; not independent and not evidence of generalization.",
        "metrics": metrics,
        "checks": checks,
        "overall": "PASS_FIXTURE_ONLY" if coverage_ok and all(checks.values()) else "REVIEW_REQUIRED",
        "confusion": [
            {"expected": e, "observed": o, "count": count}
            for (e, o), count in sorted(confusion.items())
        ],
        "cases": rows,
    }

    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["overall"] == "PASS_FIXTURE_ONLY" else 2


if __name__ == "__main__":
    raise SystemExit(main())
