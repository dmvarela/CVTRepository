import copy
import json
import unittest
from pathlib import Path

from src.stage50_protocol_audit import ProtocolError, audit_protocol


PROTOCOL = Path(__file__).parents[1] / "config" / "stage5_relational_routing_protocol.json"


def load_protocol() -> dict:
    with PROTOCOL.open(encoding="utf-8") as handle:
        return json.load(handle)


class Stage50ProtocolAuditTests(unittest.TestCase):
    def test_frozen_protocol_passes_all_invariants(self) -> None:
        report = audit_protocol(load_protocol())
        self.assertEqual(report["status"], "pass")
        self.assertGreaterEqual(report["check_count"], 10)
        self.assertFalse(report["data_generated"])
        self.assertFalse(report["models_fitted"])
        self.assertFalse(report["final_test_opened"])

    def test_stage3_row_access_is_rejected(self) -> None:
        protocol = load_protocol()
        protocol["evidence_firewall"]["row_level_stage3_access_from_stage5_code"] = True
        with self.assertRaises(ProtocolError):
            audit_protocol(protocol)

    def test_final_test_access_is_rejected(self) -> None:
        protocol = load_protocol()
        protocol["authorization"]["final_test_opened"] = True
        with self.assertRaises(ProtocolError):
            audit_protocol(protocol)

    def test_post_outcome_predictor_is_rejected(self) -> None:
        protocol = load_protocol()
        protocol["pre_outcome_predictors"]["post_outcome_variables_allowed_as_predictors"] = True
        with self.assertRaises(ProtocolError):
            audit_protocol(protocol)

    def test_seed_namespace_overlap_is_rejected(self) -> None:
        protocol = load_protocol()
        partitions = protocol["fresh_partitions"]
        partitions["fresh_validation"]["seed_namespace"] = partitions["development_fit"]["seed_namespace"]
        with self.assertRaises(ProtocolError):
            audit_protocol(protocol)

    def test_missing_capacity_matched_baseline_is_rejected(self) -> None:
        protocol = load_protocol()
        del protocol["models"]["baselines"]["CM-2-native-gradient-boosting"]
        with self.assertRaises(ProtocolError):
            audit_protocol(protocol)

    def test_predictor_budget_overrun_is_rejected(self) -> None:
        protocol = load_protocol()
        protocol["pre_outcome_predictors"]["frozen_encoded_column_counts"]["counterfactual_probe_response"] = 10
        protocol["pre_outcome_predictors"]["frozen_encoded_column_counts"]["total"] = 33
        with self.assertRaises(ProtocolError):
            audit_protocol(protocol)

    def test_weakened_incremental_threshold_is_rejected(self) -> None:
        protocol = copy.deepcopy(load_protocol())
        protocol["fresh_validation_gates"]["incremental_value_vs_transport"]["minimum_absolute_brier_improvement"] = 0.001
        with self.assertRaises(ProtocolError):
            audit_protocol(protocol)


if __name__ == "__main__":
    unittest.main()

