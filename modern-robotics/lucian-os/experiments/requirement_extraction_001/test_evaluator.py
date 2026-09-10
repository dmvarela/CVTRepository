from __future__ import annotations

import json
import unittest
from pathlib import Path

from evaluate import evaluate

HERE = Path(__file__).resolve().parent
BENCHMARK = HERE / "benchmark.json"


class RequirementExtractionEvaluatorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.benchmark = json.loads(BENCHMARK.read_text(encoding="utf-8"))

    def perfect_fixture(self) -> dict:
        predictions = []
        for case in self.benchmark["cases"]:
            prediction = {"id": case["id"], "constraints": []}
            for category, needs in case["expected"].items():
                prediction[category] = [
                    {"need": need, "purpose": "frozen test fixture"}
                    for need in needs
                ]
            for assertion in case.get("boundary_assertions", []):
                prediction["constraints"].append(
                    {
                        "constraint": " ".join(assertion.get("keywords", [])),
                        "source": "USER",
                    }
                )
            predictions.append(prediction)
        return {"model": "perfect-fixture", "predictions": predictions}

    def test_perfect_fixture_scores_perfectly_on_needs(self) -> None:
        report = evaluate(self.benchmark, self.perfect_fixture())
        macro = report["macro"]
        self.assertEqual(macro["requirement_recall_D"], 1.0)
        self.assertEqual(macro["requirement_precision"], 1.0)
        self.assertEqual(macro["extra_requirement_rate_E"], 0.0)
        self.assertEqual(macro["category_accuracy"], 1.0)
        self.assertEqual(macro["cases_with_forbidden_need"], 0)
        self.assertEqual(macro["cases_with_implementation_leakage_A"], 0)

    def test_forbidden_delete_is_detected_in_ambiguous_cleanup(self) -> None:
        fixture = self.perfect_fixture()
        target = next(p for p in fixture["predictions"] if p["id"] == "REX014")
        target["required_actions"] = [
            {"need": "filesystem.delete", "purpose": "invented destructive action"}
        ]
        report = evaluate(self.benchmark, fixture)
        row = next(r for r in report["cases"] if r["id"] == "REX014")
        self.assertIn("filesystem.delete", row["forbidden_needs_present"])
        self.assertGreater(row["extra_requirement_rate_E"], 0.0)

    def test_provider_name_leakage_is_detected(self) -> None:
        fixture = self.perfect_fixture()
        target = next(p for p in fixture["predictions"] if p["id"] == "REX001")
        target["required_observations"].append(
            {"need": "read_file", "purpose": "leaked concrete provider name"}
        )
        report = evaluate(self.benchmark, fixture)
        row = next(r for r in report["cases"] if r["id"] == "REX001")
        self.assertIn("read_file", row["implementation_or_namespace_leakage_A"])


if __name__ == "__main__":
    unittest.main()
