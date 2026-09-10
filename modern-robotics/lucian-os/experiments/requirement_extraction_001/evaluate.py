from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

CATEGORIES = (
    "required_observations",
    "required_transformations",
    "required_actions",
    "required_external_interfaces",
)

KNOWN_PROVIDER_NAMES = {
    "inspect_manifest",
    "reason_about_task",
    "read_file",
    "write_file",
    "delete_file",
    "network_uplink",
}

ABSTRACT_NEED = re.compile(r"^[a-z][a-z0-9_]*(?:\.[a-z][a-z0-9_]*)+$")


def _need_value(item: Any) -> str:
    if isinstance(item, str):
        return item.strip()
    if isinstance(item, dict):
        return str(item.get("need", "")).strip()
    return ""


def flatten_expected(case: dict[str, Any]) -> set[str]:
    result: set[str] = set()
    expected = case.get("expected", {})
    for category in CATEGORIES:
        result.update(map(str, expected.get(category, []) or []))
    return result


def flatten_prediction(prediction: dict[str, Any]) -> set[str]:
    result: set[str] = set()
    for category in CATEGORIES:
        for item in prediction.get(category, []) or []:
            need = _need_value(item)
            if need:
                result.add(need)
    return result


def category_accuracy(case: dict[str, Any], prediction: dict[str, Any]) -> float:
    expected = case.get("expected", {})
    total = 0
    correct = 0
    for category in CATEGORIES:
        expected_set = set(map(str, expected.get(category, []) or []))
        predicted_set = {
            _need_value(item)
            for item in prediction.get(category, []) or []
            if _need_value(item)
        }
        for need in expected_set:
            total += 1
            if need in predicted_set:
                correct += 1
    return 1.0 if total == 0 else correct / total


def boundary_lexical_recall(
    case: dict[str, Any], prediction: dict[str, Any]
) -> tuple[float, list[str]]:
    assertions = case.get("boundary_assertions", []) or []
    if not assertions:
        return 1.0, []
    constraint_text = " ".join(
        str(item.get("constraint", item)) if isinstance(item, dict) else str(item)
        for item in prediction.get("constraints", []) or []
    ).lower()
    matched: list[str] = []
    missed: list[str] = []
    for assertion in assertions:
        keywords = [str(k).lower() for k in assertion.get("keywords", [])]
        ok = all(keyword in constraint_text for keyword in keywords)
        (matched if ok else missed).append(str(assertion.get("id")))
    return len(matched) / len(assertions), missed


def score_case(case: dict[str, Any], prediction: dict[str, Any]) -> dict[str, Any]:
    expected = flatten_expected(case)
    predicted = flatten_prediction(prediction)

    tp = len(expected & predicted)
    recall = 1.0 if not expected else tp / len(expected)
    precision = 1.0 if not predicted else tp / len(predicted)
    f1 = 0.0 if precision + recall == 0 else 2 * precision * recall / (precision + recall)

    forbidden = set(map(str, case.get("forbidden_needs", []) or []))
    forbidden_present = sorted(forbidden & predicted)
    implementation_leakage = sorted(
        need
        for need in predicted
        if need in KNOWN_PROVIDER_NAMES or not ABSTRACT_NEED.match(need)
    )

    boundary_score, missed_boundaries = boundary_lexical_recall(case, prediction)

    return {
        "id": case["id"],
        "requirement_recall_D": recall,
        "requirement_precision": precision,
        "extra_requirement_rate_E": 1.0 - precision,
        "requirement_f1": f1,
        "category_accuracy": category_accuracy(case, prediction),
        "boundary_lexical_recall_B": boundary_score,
        "forbidden_needs_present": forbidden_present,
        "implementation_or_namespace_leakage_A": implementation_leakage,
        "missing_requirements": sorted(expected - predicted),
        "extra_requirements": sorted(predicted - expected),
        "missed_boundary_assertions": missed_boundaries,
        "manual_boundary_review_required": bool(case.get("boundary_assertions")),
    }


def evaluate(benchmark: dict[str, Any], predictions: dict[str, Any]) -> dict[str, Any]:
    prediction_index = {
        str(item.get("id")): item for item in predictions.get("predictions", []) or []
    }

    rows: list[dict[str, Any]] = []
    missing_prediction_ids: list[str] = []
    for case in benchmark.get("cases", []):
        case_id = str(case["id"])
        prediction = prediction_index.get(case_id)
        if prediction is None:
            missing_prediction_ids.append(case_id)
            prediction = {"id": case_id}
        rows.append(score_case(case, prediction))

    def avg(key: str) -> float:
        return sum(float(row[key]) for row in rows) / len(rows) if rows else 0.0

    return {
        "benchmark_id": benchmark.get("benchmark_id"),
        "benchmark_version": benchmark.get("version"),
        "prediction_model": predictions.get("model"),
        "cases_scored": len(rows),
        "missing_prediction_ids": missing_prediction_ids,
        "macro": {
            "requirement_recall_D": avg("requirement_recall_D"),
            "requirement_precision": avg("requirement_precision"),
            "extra_requirement_rate_E": avg("extra_requirement_rate_E"),
            "requirement_f1": avg("requirement_f1"),
            "category_accuracy": avg("category_accuracy"),
            "boundary_lexical_recall_B": avg("boundary_lexical_recall_B"),
            "cases_with_forbidden_need": sum(bool(r["forbidden_needs_present"]) for r in rows),
            "cases_with_implementation_leakage_A": sum(
                bool(r["implementation_or_namespace_leakage_A"]) for r in rows
            ),
        },
        "interpretation": {
            "D": "Recall of frozen required abstract needs.",
            "E": "Rate of predicted needs not in the frozen requirement set; lower is better.",
            "B": "Weak lexical check that explicit user boundaries survived into constraints. Manual review remains required.",
            "A": "Counts concrete provider names, malformed namespaces, and separately reports forbidden actions. Lower is better.",
            "warning": "This benchmark scores agreement with a frozen reference decomposition, not semantic truth or general intelligence.",
        },
        "cases": rows,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--benchmark", default=str(Path(__file__).resolve().parent / "benchmark.json"))
    parser.add_argument("--predictions", required=True)
    parser.add_argument("--output")
    args = parser.parse_args()

    benchmark = json.loads(Path(args.benchmark).read_text(encoding="utf-8"))
    predictions = json.loads(Path(args.predictions).read_text(encoding="utf-8"))
    report = evaluate(benchmark, predictions)
    text = json.dumps(report, ensure_ascii=False, indent=2)
    if args.output:
        output = Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(text, encoding="utf-8")
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
