import unittest

from code.bounded_authority_router import route


class RouterTests(unittest.TestCase):
    def test_local_reasoning_is_proposal_only(self):
        result = route("Reason about this task.")
        self.assertEqual(result["routing"]["disposition"], "LOCAL_PROPOSAL_ONLY")
        self.assertEqual(result["execution"], "NONE — simulation only")

    def test_high_confidence_does_not_create_authority(self):
        result = route(
            "Delete the file.",
            model_proposed_capability="delete_file",
            model_confidence=0.99,
        )
        self.assertEqual(result["routing"]["disposition"], "BLOCK")
        self.assertFalse(result["authorized"])

    def test_authorized_but_unavailable_capability_escalates(self):
        result = route(
            "Read file notes.txt.",
            model_proposed_capability="read_file",
            model_confidence=0.95,
        )
        self.assertEqual(result["routing"]["disposition"], "ESCALATE")
        self.assertTrue(result["authorized"])

    def test_confidence_does_not_substitute_for_warrant(self):
        result = route(
            "State the verified result.",
            model_confidence=0.99,
            requires_verified_fact=True,
            warrant="insufficient",
        )
        self.assertEqual(result["routing"]["disposition"], "HOLD_FOR_EVIDENCE")


if __name__ == "__main__":
    unittest.main()
