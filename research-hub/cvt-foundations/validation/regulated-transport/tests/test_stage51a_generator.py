import copy
import unittest
from collections import Counter
from pathlib import Path

from src.stage51a_generator import (
    Stage51AError,
    _params_initial,
    apply_history,
    audit_configuration,
    balanced_cell,
    derive_seed,
    design_smoke_rows,
    load_json,
    smoke_record,
    stage5_row_id,
)


ROOT = Path(__file__).parents[1]
PROTOCOL_PATH = ROOT / "config" / "stage5_relational_routing_protocol.json"
CONFIG_PATH = ROOT / "config" / "stage51a_generator_implementation.json"


def fixtures():
    return load_json(PROTOCOL_PATH), load_json(CONFIG_PATH)


class Stage51AGeneratorTests(unittest.TestCase):
    def test_configuration_audit_passes_without_execution_authority(self) -> None:
        protocol, config = fixtures()
        report = audit_configuration(protocol, config)
        self.assertEqual(report["status"], "pass")
        self.assertFalse(report["full_partition_generation_authorized"])
        self.assertFalse(report["final_test_opened"])

    def test_canonical_protocol_hash_change_is_rejected(self) -> None:
        protocol, config = fixtures()
        changed = copy.deepcopy(protocol)
        changed["objective"] = changed["objective"] + " changed"
        with self.assertRaises(Stage51AError):
            audit_configuration(changed, config)

    def test_full_generation_authority_is_rejected_in_stage51a(self) -> None:
        protocol, config = fixtures()
        changed = copy.deepcopy(config)
        changed["authorization"][
            "full_development_partition_generation_authorized"
        ] = True
        with self.assertRaises(Stage51AError):
            audit_configuration(protocol, changed)

    def test_seed_derivation_and_row_ids_are_deterministic(self) -> None:
        namespace = "cvt-regulated-transport-stage5-v1-development-fit"
        first = derive_seed(namespace, "development_fit", 7)
        second = derive_seed(namespace, "development_fit", 7)
        self.assertEqual(first, second)
        self.assertEqual(
            stage5_row_id(namespace, "development_fit", 7),
            stage5_row_id(namespace, "development_fit", 7),
        )
        self.assertTrue(
            stage5_row_id(namespace, "development_fit", 7).startswith(
                "s5-development_fit-"
            )
        )

    def test_partition_namespaces_and_derived_seeds_are_disjoint(self) -> None:
        _, config = fixtures()
        seeds = {
            derive_seed(spec["seed_namespace"], name, 0)
            for name, spec in config["planned_partitions"].items()
        }
        self.assertEqual(len(seeds), 5)
        self.assertTrue(
            seeds.isdisjoint(
                set(config["seed_and_identity"]["stage3_master_seeds_forbidden"])
            )
        )

    def test_twelve_row_cell_prefix_has_balanced_marginals(self) -> None:
        cells = [balanced_cell(index) for index in range(12)]
        self.assertEqual(set(Counter(cell[0] for cell in cells).values()), {3})
        self.assertEqual(set(Counter(cell[1] for cell in cells).values()), {4})
        self.assertEqual(set(Counter(cell[2] for cell in cells).values()), {4})
        self.assertNotIn("repeated_pulse", {cell[0] for cell in cells})

    def test_design_contract_rejects_more_than_twelve_rows(self) -> None:
        protocol, config = fixtures()
        with self.assertRaises(Stage51AError):
            design_smoke_rows(protocol, config, rows=13)

    def test_design_contract_rejects_validation_smoke(self) -> None:
        protocol, config = fixtures()
        with self.assertRaises(Stage51AError):
            design_smoke_rows(
                protocol,
                config,
                partition="fresh_validation",
                rows=1,
            )

    def test_design_rows_use_new_identity_and_unique_hashes(self) -> None:
        protocol, config = fixtures()
        rows = design_smoke_rows(protocol, config, rows=12)
        self.assertEqual(len({row["row_id"] for row in rows}), 12)
        self.assertEqual(len({row["design_hash"] for row in rows}), 12)
        self.assertTrue(all(row["row_id"].startswith("s5-") for row in rows))
        self.assertTrue(
            all(
                not row["row_id"].startswith(("training-", "validation-", "test-"))
                for row in rows
            )
        )

    def test_equal_feature_contracts_contain_31_unique_columns(self) -> None:
        _, config = fixtures()
        relational = config["relational_columns"]
        native = config["native_columns"]
        self.assertEqual((len(relational), len(set(relational))), (31, 31))
        self.assertEqual((len(native), len(set(native))), (31, 31))
        self.assertTrue(set(config["probe_design"]["summary_formulas"]).issubset(relational))

    def test_history_clone_returns_new_precontact_state(self) -> None:
        protocol, config = fixtures()
        row = design_smoke_rows(protocol, config, rows=2)[1]
        self.assertEqual(row["history_class"], "subthreshold_prior_exposure")
        params, initial = _params_initial(row)
        history = apply_history(row, params, initial, config)
        self.assertTrue(history.solver_success)
        self.assertGreater(history.prior_scheduled_dose, 0.0)
        self.assertFalse((history.state.as_array() == initial.as_array()).all())

    def test_recovered_history_uses_sample_aligned_output_grid(self) -> None:
        protocol, config = fixtures()
        row = design_smoke_rows(protocol, config, rows=3)[2]
        self.assertEqual(row["history_class"], "prior_exposure_then_recovery")
        params, initial = _params_initial(row)
        history = apply_history(row, params, initial, config)
        self.assertTrue(history.solver_success)
        self.assertGreater(history.time_since_prior_exposure, 0.0)
        self.assertGreaterEqual(history.precontact_recovery_fraction, 0.0)
        self.assertLessEqual(history.precontact_recovery_fraction, 1.0)

    def test_one_row_native_smoke_is_isolated_and_finite(self) -> None:
        protocol, config = fixtures()
        row = design_smoke_rows(protocol, config, rows=1)[0]
        record = smoke_record(row, config)
        self.assertTrue(record["main_solver_success"])
        self.assertTrue(record["accounting_valid"])
        self.assertTrue(record["bounds_valid"])
        self.assertEqual(record["probe_invalid"], 0)
        self.assertEqual(record["probe_isolation_max_abs_state_difference"], 0.0)
        self.assertEqual(record["relational_feature_count"], 31)
        self.assertEqual(record["native_feature_count"], 31)
        self.assertTrue(record["relational_features_finite"])
        self.assertTrue(record["native_features_finite"])


if __name__ == "__main__":
    unittest.main()

