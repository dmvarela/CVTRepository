"""Offline contract tests for Lucian OS v0.3 search-to-capability composition.

No Ollama call. No device or network action.
Run from modern-robotics/lucian-os:
    py prototype/test_lucian_os_v003.py
"""

from __future__ import annotations

import json
import unittest
from pathlib import Path

from lucian_os_v003 import compose_search_state
from problem_requirements_v003 import (
    flatten_requirements,
    validate_problem_requirements,
)
from relational_search_engine_v003 import validate_search_state_v003

PROJECT_ROOT = Path(__file__).resolve().parents[1]
MANIFEST = PROJECT_ROOT / "manifests" / "windows_dev_host_composition_lab.json"


def base_state() -> dict:
    return {
        "candidate_relations": ["task requires source inspection"],
        "competing_relations": [],
        "established": ["user requested a file comparison"],
        "not_established": ["the file contents are not yet known"],
        "missing_information": ["file contents"],
        "warrant_status": "INSUFFICIENT",
        "posture": "PROBE",
        "provisional_landing": None,
        "required_observations": [
            {"need": "filesystem.read", "purpose": "inspect the source file"}
        ],
        "required_transformations": [
            {"need": "reason.task", "purpose": "compare the observed contents"}
        ],
        "required_actions": [],
        "required_external_interfaces": [],
        "constraints": [
            {"constraint": "do not modify the source", "source": "USER"}
        ],
        "proposed_next_step": "Read the source, then compare.",
        "return_localization": None,
    }


class V003ContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))

    def test_valid_requirement_contract(self) -> None:
        check = validate_problem_requirements(base_state())
        self.assertTrue(check["valid"], check)

    def test_need_must_be_abstract_namespace(self) -> None:
        state = base_state()
        state["required_observations"][0]["need"] = "read_file"
        check = validate_problem_requirements(state)
        self.assertFalse(check["valid"])
        self.assertTrue(
            any("dotted abstract namespace" in v for v in check["violations"])
        )

    def test_search_contract_includes_requirements(self) -> None:
        check = validate_search_state_v003(base_state())
        self.assertTrue(check["valid"], check)

    def test_requirement_order_is_preserved_across_categories(self) -> None:
        reqs = flatten_requirements(base_state())
        self.assertEqual(
            [r["requirement"] for r in reqs],
            ["filesystem.read", "reason.task"],
        )

    def test_provider_discovery_is_separate_from_need(self) -> None:
        result = compose_search_state(
            search_state=base_state(),
            manifest=self.manifest,
        )
        steps = result["composition"]["composition"]
        self.assertEqual(steps[0]["requirement"], "filesystem.read")
        self.assertEqual(steps[0]["selected_capability"], "read_file")
        self.assertEqual(steps[1]["requirement"], "reason.task")
        self.assertEqual(steps[1]["selected_capability"], "reason_about_task")

    def test_authority_does_not_propagate(self) -> None:
        state = base_state()
        state["required_actions"] = [
            {"need": "filesystem.write", "purpose": "save a derived copy"}
        ]
        result = compose_search_state(search_state=state, manifest=self.manifest)
        self.assertEqual(result["disposition"], "REFUSE")
        statuses = [
            step["gate"]["status"]
            for step in result["composition"]["composition"]
        ]
        self.assertIn("AUTHORITY_BLOCKED", statuses)

    def test_missing_provider_is_unsatisfiable(self) -> None:
        state = base_state()
        state["required_transformations"] = [
            {"need": "document.summarize", "purpose": "summarize the document"}
        ]
        result = compose_search_state(search_state=state, manifest=self.manifest)
        self.assertEqual(result["disposition"], "UNSATISFIABLE")

    def test_invalid_search_product_holds_before_composition(self) -> None:
        state = base_state()
        state["required_observations"][0]["need"] = "read_file"
        result = compose_search_state(search_state=state, manifest=self.manifest)
        self.assertEqual(result["disposition"], "HOLD_INVALID_SEARCH_PRODUCT")
        self.assertIsNone(result["composition"])


if __name__ == "__main__":
    unittest.main()
