from __future__ import annotations

import unittest
from pathlib import Path

from capability_composer_v001 import (
    DEFAULT_MANIFEST,
    compose_plan,
    derive_requirements,
    load_manifest,
)


class CapabilityCompositionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.manifest = load_manifest(Path(DEFAULT_MANIFEST))

    def test_multistep_safe_composition(self) -> None:
        plan = compose_plan(
            "Inspect the manifest and reason about the task",
            self.manifest,
        )
        self.assertEqual(
            [step["requirement"] for step in plan["composition"]],
            ["capability.enumerate", "reason.task"],
        )
        self.assertEqual(
            [step["selected_capability"] for step in plan["composition"]],
            ["inspect_manifest", "reason_about_task"],
        )
        self.assertEqual(plan["disposition"], "READY_FOR_SIMULATION")
        self.assertFalse(plan["execution_permitted"])

    def test_authority_block_is_not_skipped(self) -> None:
        plan = compose_plan("Read a file, then write a copy", self.manifest)
        self.assertEqual(
            [step["requirement"] for step in plan["composition"]],
            ["filesystem.read", "filesystem.write"],
        )
        self.assertEqual(plan["disposition"], "REFUSE")
        self.assertIn(
            "AUTHORITY_BLOCKED",
            [step["gate"]["status"] for step in plan["composition"]],
        )

    def test_network_need_is_discovered_abstractly(self) -> None:
        plan = compose_plan(
            "Read a file and use the web to compare it",
            self.manifest,
        )
        requirements = [step["requirement"] for step in plan["composition"]]
        self.assertEqual(
            requirements,
            ["filesystem.read", "network.request", "reason.task"],
        )
        self.assertEqual(plan["disposition"], "REFUSE")

    def test_open_ended_task_falls_back_to_reasoning(self) -> None:
        requirements = derive_requirements("Figure out what happened here")
        self.assertEqual(requirements[0]["requirement"], "reason.task")
        self.assertEqual(requirements[0]["status"], "CONSERVATIVE_FALLBACK")

    def test_missing_requirement_is_truthfully_unsatisfiable(self) -> None:
        manifest = dict(self.manifest)
        manifest["capabilities"] = [
            c
            for c in self.manifest["capabilities"]
            if "filesystem.read" not in c.get("provides", [])
        ]
        plan = compose_plan("Read a file", manifest)
        self.assertEqual(plan["disposition"], "UNSATISFIABLE")
        self.assertEqual(
            plan["composition"][0]["gate"]["status"],
            "MISSING_CAPABILITY",
        )


if __name__ == "__main__":
    unittest.main()
