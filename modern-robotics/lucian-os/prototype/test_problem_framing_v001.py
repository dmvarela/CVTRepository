from __future__ import annotations

import unittest

from problem_framing_v001 import validate_framing_state


class ProblemFramingContractTests(unittest.TestCase):
    def base_state(self) -> dict:
        return {
            "surface_request": "Use Photoshop to resize this image to 800 pixels wide and save a copy.",
            "objective": {"text": "Produce an 800-pixel-wide copy", "source": "USER"},
            "constraints": [
                {"text": "Do not change the original", "source": "USER"}
            ],
            "implementation_assumptions": [
                {"text": "Use Photoshop", "source": "USER"}
            ],
            "problem_shape": "transform an image while preserving the original",
            "structural_mismatch": {"present": False, "basis": ""},
            "framing_disposition": "EXECUTE_AS_FRAMED",
            "proposed_reframe": "",
        }

    def test_execute_as_framed_is_valid(self) -> None:
        result = validate_framing_state(self.base_state())
        self.assertTrue(result["valid"])
        self.assertTrue(result["execution_allowed_by_framing"])
        self.assertEqual(result["framing_disposition"], "EXECUTE_AS_FRAMED")

    def test_reframe_requires_material_mismatch(self) -> None:
        state = self.base_state()
        state["framing_disposition"] = "REFRAME_AND_PROPOSE"
        state["proposed_reframe"] = "Inspect duplicate candidates before deletion"
        result = validate_framing_state(state)
        self.assertFalse(result["valid"])
        self.assertIn(
            "REFRAME_AND_PROPOSE requires structural_mismatch.present=true",
            result["violations"],
        )

    def test_reframe_with_basis_is_valid_but_not_execution_ready(self) -> None:
        state = self.base_state()
        state["surface_request"] = "Delete duplicate files until I free 10 GB."
        state["objective"] = {"text": "Free at least 10 GB", "source": "USER"}
        state["implementation_assumptions"] = [
            {"text": "Deletion is the required means", "source": "INFERRED"}
        ]
        state["problem_shape"] = "reclaim storage while preserving unique information"
        state["structural_mismatch"] = {
            "present": True,
            "basis": "The objective is storage recovery; deletion is consequential and only one candidate means.",
        }
        state["framing_disposition"] = "REFRAME_AND_PROPOSE"
        state["proposed_reframe"] = "Identify safe duplicate candidates and lower-risk reclaim paths before deletion."
        result = validate_framing_state(state)
        self.assertTrue(result["valid"])
        self.assertFalse(result["execution_allowed_by_framing"])

    def test_ask_or_hold_preserves_underspecification(self) -> None:
        state = self.base_state()
        state["surface_request"] = "Make my computer faster."
        state["objective"] = {"text": "Improve computer performance", "source": "USER"}
        state["constraints"] = []
        state["implementation_assumptions"] = []
        state["problem_shape"] = "performance problem with unresolved target metric"
        state["structural_mismatch"] = {
            "present": True,
            "basis": "The request does not identify which performance dimension is failing.",
        }
        state["framing_disposition"] = "ASK_OR_HOLD"
        state["proposed_reframe"] = ""
        result = validate_framing_state(state)
        self.assertTrue(result["valid"])
        self.assertFalse(result["execution_allowed_by_framing"])

    def test_inferred_objective_requires_explicit_provenance(self) -> None:
        state = self.base_state()
        state["objective"] = {"text": "Something deeper", "source": ""}
        result = validate_framing_state(state)
        self.assertFalse(result["valid"])
        self.assertIn(
            "objective.source must be USER | CONTEXT | INFERRED",
            result["violations"],
        )

    def test_execute_as_framed_cannot_smuggle_reframe(self) -> None:
        state = self.base_state()
        state["proposed_reframe"] = "Actually do something else"
        result = validate_framing_state(state)
        self.assertFalse(result["valid"])
        self.assertIn(
            "EXECUTE_AS_FRAMED must not carry an unused proposed_reframe",
            result["violations"],
        )


if __name__ == "__main__":
    unittest.main()
