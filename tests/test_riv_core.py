import unittest

from code.riv_core import (
    CONTRADICT,
    COMPROMISED,
    SUPPORT,
    CONTRADICTED,
    OBSERVATION_COMPROMISED,
    SUPPORTED,
    UNRESOLVED,
    UNVERIFIED_ACTION_EFFECT,
    VERIFIED_ACTION_EFFECT,
    EvidenceLedger,
    Observation,
)


class RIVCoreTests(unittest.TestCase):
    def obs(self, oid, root, stance, claim="object present", **kwargs):
        return Observation(
            observation_id=oid,
            root_source_id=root,
            modality=kwargs.pop("modality", "camera"),
            stance=stance,
            relevant_claim=claim,
            **kwargs,
        )

    def test_repetition_does_not_increase_warrant(self):
        ledger = EvidenceLedger("object present")
        for _ in range(20):
            ledger.add_narrative("The object is present.")
        ledger.add_observation(self.obs("cam1", "camera-frame-1", CONTRADICT))
        self.assertEqual(ledger.warrant(), CONTRADICTED)
        self.assertEqual(ledger.packet()["narrative_mention_count"], 20)
        self.assertEqual(ledger.packet()["independent_root_count"], 1)

    def test_derived_reports_share_one_root(self):
        ledger = EvidenceLedger("object present")
        ledger.add_observation(self.obs("raw", "camera-frame-1", SUPPORT))
        ledger.add_observation(
            self.obs(
                "caption",
                "camera-frame-1",
                SUPPORT,
                raw_or_derived="derived",
                derived_from=("raw",),
            )
        )
        self.assertEqual(ledger.warrant(), SUPPORTED)
        self.assertEqual(ledger.packet()["independent_root_count"], 1)

    def test_cross_root_conflict_is_preserved(self):
        ledger = EvidenceLedger("path clear")
        ledger.add_observation(self.obs("cam", "camera-1", SUPPORT, claim="path clear"))
        ledger.add_observation(
            self.obs("depth", "depth-1", CONTRADICT, claim="path clear", modality="depth")
        )
        self.assertEqual(ledger.warrant(), UNRESOLVED)

    def test_compromised_only_does_not_support_claim(self):
        ledger = EvidenceLedger("object present")
        ledger.add_observation(self.obs("cam", "camera-1", COMPROMISED, quality=0.0))
        self.assertEqual(ledger.warrant(), OBSERVATION_COMPROMISED)

    def test_action_command_is_not_physical_verification(self):
        ledger = EvidenceLedger("tone physically produced")
        ledger.add_narrative("Playback command completed.", source="system-telemetry")
        self.assertEqual(ledger.action_effect_state(), UNVERIFIED_ACTION_EFFECT)

    def test_sensor_support_can_verify_action_effect(self):
        ledger = EvidenceLedger("tone physically produced")
        ledger.add_narrative("Playback command completed.", source="system-telemetry")
        ledger.add_observation(
            Observation(
                observation_id="mic1",
                root_source_id="mic-capture-1",
                modality="microphone",
                stance=SUPPORT,
                relevant_claim="tone physically produced",
            )
        )
        self.assertEqual(ledger.action_effect_state(), VERIFIED_ACTION_EFFECT)

    def test_new_observation_can_overturn_prior_supported_state(self):
        old = EvidenceLedger("object present")
        old.add_observation(self.obs("cam-old", "camera-old", SUPPORT))
        self.assertEqual(old.warrant(), SUPPORTED)

        current = EvidenceLedger("object present")
        current.add_observation(self.obs("cam-new", "camera-new", CONTRADICT))
        self.assertEqual(current.warrant(), CONTRADICTED)


if __name__ == "__main__":
    unittest.main()
