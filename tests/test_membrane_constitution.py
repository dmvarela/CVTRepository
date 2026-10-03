import unittest

from code.bounded_authority_router import route
from code.membrane_constitution import (
    ALLOW,
    ASK_CONFIRMATION,
    ATTENUATE,
    BLOCK,
    HOLD,
    CrossingRequest,
    evaluate_crossing,
    request_from_authority_packet,
    request_from_riv_packet,
)
from code.riv_core import CONTRADICT, SUPPORT, EvidenceLedger, Observation


class MembraneConstitutionTests(unittest.TestCase):
    def test_riv_contradiction_cannot_cross_as_established_fact(self):
        ledger = EvidenceLedger("reference card present")
        for _ in range(20):
            ledger.add_narrative("The reference card is present.")
        ledger.add_observation(
            Observation(
                observation_id="cam1",
                root_source_id="camera-frame-1",
                modality="camera",
                stance=CONTRADICT,
                relevant_claim="reference card present",
            )
        )
        req = request_from_riv_packet(ledger.packet(), as_established=True)
        decision = evaluate_crossing(req)
        self.assertEqual(decision.disposition, HOLD)

    def test_supported_riv_state_may_cross(self):
        ledger = EvidenceLedger("reference card present")
        ledger.add_observation(
            Observation(
                observation_id="cam1",
                root_source_id="camera-frame-1",
                modality="camera",
                stance=SUPPORT,
                relevant_claim="reference card present",
            )
        )
        req = request_from_riv_packet(ledger.packet(), as_established=True)
        self.assertEqual(evaluate_crossing(req).disposition, ALLOW)

    def test_shared_root_reports_are_not_independent_corroboration(self):
        ledger = EvidenceLedger("tone present")
        ledger.add_observation(
            Observation(
                observation_id="raw",
                root_source_id="mic-capture-1",
                modality="microphone",
                stance=SUPPORT,
                relevant_claim="tone present",
            )
        )
        ledger.add_observation(
            Observation(
                observation_id="classifier",
                root_source_id="mic-capture-1",
                modality="audio_classifier",
                stance=SUPPORT,
                relevant_claim="tone present",
                raw_or_derived="derived",
                derived_from=("raw",),
            )
        )
        req = request_from_riv_packet(ledger.packet(), as_established=True)
        self.assertEqual(evaluate_crossing(req).disposition, ATTENUATE)

    def test_unauthorized_state_change_is_blocked(self):
        router_packet = route(
            "Delete the file.",
            model_proposed_capability="delete_file",
            model_confidence=0.99,
            warrant="sufficient",
        )
        req = request_from_authority_packet(
            router_packet, consequence="high", reversible=False
        )
        self.assertEqual(evaluate_crossing(req).disposition, BLOCK)

    def test_high_consequence_authorized_action_still_needs_warrant(self):
        req = CrossingRequest(
            channel="directive",
            direction="outbound",
            content_kind="execute_action",
            consequence="high",
            warrant="insufficient",
            authorized=True,
        )
        self.assertEqual(evaluate_crossing(req).disposition, HOLD)

    def test_emotional_depth_is_attenuated_not_rejected(self):
        req = CrossingRequest(
            channel="emotional",
            direction="outbound",
            content_kind="reflection",
            requested_intensity=0.9,
            introduced_intensity=0.2,
        )
        self.assertEqual(evaluate_crossing(req).disposition, ATTENUATE)

    def test_memory_persistence_preserves_user_control(self):
        req = CrossingRequest(
            channel="memory",
            direction="internal",
            content_kind="persist_context",
            privacy_cost="medium",
            authorized=False,
            user_control=True,
        )
        self.assertEqual(evaluate_crossing(req).disposition, ASK_CONFIRMATION)

    def test_literal_identity_claim_is_attenuated(self):
        req = CrossingRequest(
            channel="identity",
            direction="outbound",
            content_kind="continuity_statement",
            continuity_claim="literal_personal_identity",
        )
        self.assertEqual(evaluate_crossing(req).disposition, ATTENUATE)

    def test_unauthorized_verification_access_does_not_expand_itself(self):
        req = CrossingRequest(
            channel="epistemic",
            direction="inbound",
            content_kind="context",
            warrant="unknown",
            verification_access="available_but_unauthorized",
        )
        self.assertEqual(evaluate_crossing(req).disposition, ATTENUATE)


if __name__ == "__main__":
    unittest.main()
