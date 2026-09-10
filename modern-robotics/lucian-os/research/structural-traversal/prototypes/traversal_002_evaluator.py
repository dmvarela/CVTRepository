"""TRAVERSAL-002 posthoc evaluator.

Reads frozen generator output plus posthoc human/assistant scores and aggregates the
comparative metrics. It does not generate candidates.

Run from modern-robotics/lucian-os:
    py research/structural-traversal/prototypes/traversal_002_evaluator.py
"""
from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "results" / "TRAVERSAL_002_RAW_OUTPUT.jsonl"
SCORES = ROOT / "results" / "TRAVERSAL_002_POSTHOC_SCORES.json"
GENERATOR_PACKET = ROOT / "manifests" / "traversal_002_generator_packets.json"

NON_PROMOTED = {"NO_GAIN", "MISLEADING", "REJECTED", "REJECTED_UNDISCIPLINED"}
FORBIDDEN_GENERATOR_KEYS = {
    "regime", "known_trap", "useful_new_path_criterion", "expected_candidate",
    "expected_analogy", "answer_key", "evaluator_label", "score"
}


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def find_forbidden_keys(obj: Any) -> list[str]:
    hits: list[str] = []
    if isinstance(obj, dict):
        for key, value in obj.items():
            if key in FORBIDDEN_GENERATOR_KEYS:
                hits.append(key)
            hits.extend(find_forbidden_keys(value))
    elif isinstance(obj, list):
        for value in obj:
            hits.extend(find_forbidden_keys(value))
    return hits


def aggregate(rows: list[dict[str, Any]], scores: dict[str, dict[str, Any]]) -> dict[str, Any]:
    by_condition: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        cid = row["candidate_id"]
        scored = dict(row)
        scored.update(scores[cid])
        scored["promoted"] = row.get("claimed_classification") not in NON_PROMOTED
        by_condition[row["condition"]].append(scored)

    result: dict[str, Any] = {}
    for condition, items in by_condition.items():
        promoted = [x for x in items if x["promoted"]]
        abstentions = [x for x in items if x.get("abstention_correct") is not None]
        result[condition] = {
            "candidates": len(items),
            "promoted": len(promoted),
            "useful_promoted": sum(bool(x.get("useful")) for x in promoted),
            "useful_precision": round(sum(bool(x.get("useful")) for x in promoted) / len(promoted), 3) if promoted else None,
            "misleading_promotions": sum(bool(x.get("misleading_promotion")) for x in promoted),
            "useful_new_paths": sum(bool(x.get("useful_new_path")) for x in promoted),
            "target_valid_rate": round(sum(bool(x.get("target_valid")) for x in promoted) / len(promoted), 3) if promoted else None,
            "return_completeness": round(sum(bool(x.get("return_complete")) for x in promoted) / len(promoted), 3) if promoted else None,
            "falsifiability_rate": round(sum(bool(x.get("falsifiable")) for x in promoted) / len(promoted), 3) if promoted else None,
            "abstention_quality": round(sum(bool(x.get("abstention_correct")) for x in abstentions) / len(abstentions), 3) if abstentions else None,
        }
    return result


def main() -> int:
    raw = load_jsonl(RAW)
    score_doc = load_json(SCORES)
    score_map = {row["candidate_id"]: row for row in score_doc["scores"]}
    generator_packet = load_json(GENERATOR_PACKET)

    raw_ids = {row["candidate_id"] for row in raw}
    score_ids = set(score_map)
    id_match = raw_ids == score_ids
    packet_leakage = find_forbidden_keys(generator_packet)

    metrics = aggregate(raw, score_map)
    structural = metrics["STRUCTURAL_TRAVERSAL"]
    loose = metrics["LOOSE_ANALOGY"]
    domain = metrics["DOMAIN_ONLY"]

    raw_by_id = {row["candidate_id"]: row for row in raw}
    checks = {
        "T1_generator_packet_free_of_evaluator_labels": not packet_leakage,
        "T2_scores_cover_frozen_generation_exactly": id_match,
        "T3_structural_return_complete_for_promoted_candidates": structural["return_completeness"] == 1.0,
        "T4_structural_has_no_misleading_promotions": structural["misleading_promotions"] == 0,
        "T5_loose_analogy_exposes_seductive_failures": loose["misleading_promotions"] >= 1,
        "T6_structural_adds_useful_new_paths_over_domain_only": structural["useful_new_paths"] > domain["useful_new_paths"],
        "T7_no_gain_is_available_and_used": raw_by_id["P2_S1"]["claimed_classification"] == "NO_GAIN" and bool(score_map["P2_S1"]["abstention_correct"]),
        "T8_heuristic_restraint_is_available_and_used": raw_by_id["P4_S1"]["claimed_classification"] == "HEURISTIC" and bool(score_map["P4_S1"]["abstention_correct"]),
        "T9_provenance_preserved": all(bool(row.get("provenance")) for row in raw),
        "T10_independent_evaluator": False,
        "T11_reasoning_cost_accounted": False,
        "T12_no_gain_generalizes_to_all_domain_sufficient_cases": bool(score_map["P5_S1"]["abstention_correct"]),
    }

    core_discipline = all(checks[k] for k in [
        "T1_generator_packet_free_of_evaluator_labels",
        "T2_scores_cover_frozen_generation_exactly",
        "T3_structural_return_complete_for_promoted_candidates",
        "T4_structural_has_no_misleading_promotions",
        "T5_loose_analogy_exposes_seductive_failures",
        "T6_structural_adds_useful_new_paths_over_domain_only",
        "T7_no_gain_is_available_and_used",
        "T8_heuristic_restraint_is_available_and_used",
        "T9_provenance_preserved",
    ])

    report = {
        "experiment": "TRAVERSAL-002",
        "evaluation_mode": score_doc["evaluation_mode"],
        "independence_warning": score_doc["independence_warning"],
        "metrics": metrics,
        "checks": checks,
        "status": "ADVANCE_WITH_REPAIRS" if core_discipline else "REVIEW_REQUIRED",
        "repairs_required_before_strong_claim": [
            "independent evaluator or second-model review",
            "capture generator/evaluator reasoning cost",
            "improve trigger/abstention logic so domain-sufficient cases such as P5 do not traverse unnecessarily"
        ],
        "narrow_result": (
            "In this procedurally blind five-problem demonstration, structural traversal preserved target constraints and generated some useful representation changes, "
            "but it did not reliably know when traversal was unnecessary and the scoring was not independent."
        )
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if core_discipline else 2


if __name__ == "__main__":
    raise SystemExit(main())
