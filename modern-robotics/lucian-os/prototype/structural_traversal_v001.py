"""TRAVERSAL-001 — Structural Search, simulation only.

Compares three conditions over synthetic cases:
- DOMAIN_ONLY: stay inside the target representation;
- LOOSE_ANALOGY: promote cross-domain analogies without disciplined return;
- STRUCTURAL_TRAVERSAL: require a domain-free invariant, return mapping,
  target-domain prediction/falsifier, constraint check, and classification.

This prototype does not generate analogies with an AI model and does not establish
that structural traversal is generally superior in open-ended search. It tests the
architecture of the discipline itself.

Run from modern-robotics/lucian-os:
    py prototype/structural_traversal_v001.py
"""
from __future__ import annotations

import collections
import json
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST = PROJECT_ROOT / "manifests" / "traversal_001_cases.json"


def load_manifest(path: Path = DEFAULT_MANIFEST) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def run_domain_only(case: dict[str, Any]) -> list[dict[str, Any]]:
    promoted: list[dict[str, Any]] = []
    for candidate in case.get("domain_only", []):
        if candidate.get("testable") and candidate.get("target_supported"):
            promoted.append({
                "candidate": candidate["candidate"],
                "classification": "DOMAIN_SUPPORTED",
                "promoted": True,
                "useful": True,
                "representation_change": bool(candidate.get("representation_change", False)),
            })
    return promoted


def run_loose_analogy(case: dict[str, Any]) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    for analogy in case.get("analogies", []):
        results.append({
            "candidate": analogy["return_candidate"],
            "source": analogy["source"],
            "classification": "PROMOTED_BY_ANALOGY",
            "promoted": True,
            "useful": bool(analogy.get("target_supported")),
            "misleading": not bool(analogy.get("target_supported")),
            "representation_change": True,
        })
    return results


def run_structural_traversal(case: dict[str, Any]) -> list[dict[str, Any]]:
    groups: dict[tuple[str, str], list[dict[str, Any]]] = collections.defaultdict(list)
    for analogy in case.get("analogies", []):
        groups[(str(analogy["return_candidate"]), str(analogy["invariant"]))].append(analogy)

    results: list[dict[str, Any]] = []
    for (candidate, invariant), analogies in groups.items():
        source_domains = sorted({str(a["source_domain"]) for a in analogies})
        invariant_domain_free = all(bool(a.get("invariant_domain_free")) for a in analogies)
        return_complete = all(
            bool(a.get("return_candidate"))
            and bool(a.get("prediction"))
            and bool(a.get("falsifier"))
            for a in analogies
        )
        violations = sorted({
            str(v)
            for analogy in analogies
            for v in analogy.get("constraint_violations", [])
        })
        target_supported = all(bool(a.get("target_supported")) for a in analogies)

        if violations or not target_supported:
            classification = "MISLEADING"
            promoted = False
            useful = False
        elif invariant_domain_free and return_complete and len(source_domains) >= 2:
            classification = "STRUCTURAL"
            promoted = True
            useful = True
        elif invariant_domain_free and return_complete:
            classification = "HEURISTIC"
            promoted = True
            useful = True
        else:
            classification = "REJECTED_UNDISCIPLINED"
            promoted = False
            useful = False

        results.append({
            "candidate": candidate,
            "invariant": invariant,
            "classification": classification,
            "promoted": promoted,
            "useful": useful,
            "representation_change": promoted,
            "source_domains": source_domains,
            "source_count": len(analogies),
            "constraint_violations": violations,
            "prediction": analogies[0].get("prediction"),
            "falsifier": analogies[0].get("falsifier"),
        })
    return results


def unique_metrics(rows: list[dict[str, Any]]) -> dict[str, Any]:
    promoted_by_candidate: dict[str, list[dict[str, Any]]] = collections.defaultdict(list)
    for row in rows:
        if row.get("promoted"):
            promoted_by_candidate[str(row["candidate"])].append(row)

    useful = 0
    misleading = 0
    representation_changes = 0
    for candidate_rows in promoted_by_candidate.values():
        if any(bool(row.get("useful")) for row in candidate_rows):
            useful += 1
        if any(bool(row.get("misleading")) for row in candidate_rows):
            misleading += 1
        if any(bool(row.get("representation_change")) for row in candidate_rows):
            representation_changes += 1

    promoted = len(promoted_by_candidate)
    precision = None if promoted == 0 else round(useful / promoted, 3)
    return {
        "unique_promoted_candidates": promoted,
        "unique_useful_candidates": useful,
        "unique_misleading_promoted": misleading,
        "representation_changes": representation_changes,
        "useful_precision": precision,
    }


def main() -> int:
    data = load_manifest()
    case_reports: dict[str, Any] = {}
    all_domain: list[dict[str, Any]] = []
    all_loose: list[dict[str, Any]] = []
    all_structural: list[dict[str, Any]] = []

    for case in data.get("cases", []):
        domain = run_domain_only(case)
        loose = run_loose_analogy(case)
        structural = run_structural_traversal(case)
        all_domain.extend(domain)
        all_loose.extend(loose)
        all_structural.extend(structural)
        case_reports[str(case["id"])] = {
            "target_problem": case.get("target_problem"),
            "target_constraints": case.get("target_constraints", []),
            "domain_only": domain,
            "loose_analogy": loose,
            "structural_traversal": structural,
        }

    domain_metrics = unique_metrics(all_domain)
    loose_metrics = unique_metrics(all_loose)
    structural_metrics = unique_metrics(all_structural)

    authority_rows = case_reports["authority_trap"]["structural_traversal"]
    heuristic_rows = case_reports["single_source_heuristic"]["structural_traversal"]

    checks = {
        "T1_structural_traversal_finds_representation_changes": (
            structural_metrics["representation_changes"] >= 3
        ),
        "T2_loose_analogy_promotes_a_misleading_candidate": (
            loose_metrics["unique_misleading_promoted"] >= 1
        ),
        "T3_return_constraint_check_rejects_authority_trap": (
            len(authority_rows) == 1
            and authority_rows[0]["classification"] == "MISLEADING"
            and not authority_rows[0]["promoted"]
        ),
        "T4_multi_domain_corroboration_can_classify_structural": (
            sum(
                1
                for report in case_reports.values()
                for row in report["structural_traversal"]
                if row["classification"] == "STRUCTURAL"
            ) >= 3
        ),
        "T5_single_source_candidate_stays_heuristic": (
            len(heuristic_rows) == 1
            and heuristic_rows[0]["classification"] == "HEURISTIC"
        ),
        "T6_structural_precision_exceeds_loose_analogy_in_this_fixture": (
            structural_metrics["useful_precision"] is not None
            and loose_metrics["useful_precision"] is not None
            and structural_metrics["useful_precision"] > loose_metrics["useful_precision"]
        ),
        "T7_domain_only_does_not_receive_credit_for_cross_domain_candidates": (
            domain_metrics["representation_changes"] == 0
            and structural_metrics["representation_changes"] > domain_metrics["representation_changes"]
        ),
    }

    report = {
        "experiment": "TRAVERSAL-001",
        "mode": "SIMULATION_ONLY",
        "warning": (
            "The candidate set and truth labels are synthetic and hand-authored. "
            "This tests traversal discipline and filtering, not open-ended creative superiority."
        ),
        "conditions": {
            "DOMAIN_ONLY": "promote only target-domain candidates already supported in the fixture",
            "LOOSE_ANALOGY": "promote every returned analogy candidate without disciplined constraint return",
            "STRUCTURAL_TRAVERSAL": (
                "require domain-free invariant, return mapping, prediction/falsifier, target constraints, "
                "and classify as STRUCTURAL / HEURISTIC / MISLEADING"
            ),
        },
        "cases": case_reports,
        "metrics": {
            "DOMAIN_ONLY": domain_metrics,
            "LOOSE_ANALOGY": loose_metrics,
            "STRUCTURAL_TRAVERSAL": structural_metrics,
        },
        "checks": checks,
        "overall": "PASS" if all(checks.values()) else "REVIEW_REQUIRED",
    }

    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["overall"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
