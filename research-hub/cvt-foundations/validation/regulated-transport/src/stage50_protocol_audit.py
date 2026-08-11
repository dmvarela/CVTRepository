"""Audit the frozen Stage 5.0 relational-routing protocol.

This module reads only the protocol document. It does not load Stage 3 rows,
generate Stage 5 evidence, fit a model, or access the final test.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


class ProtocolError(ValueError):
    """Raised when a Stage 5.0 firewall or preregistration invariant fails."""


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ProtocolError(message)


def audit_protocol(protocol: dict[str, Any]) -> dict[str, Any]:
    checks: list[str] = []

    _require(protocol.get("stage") == "5.0", "stage must be 5.0")
    checks.append("stage_identity")
    _require(
        protocol.get("status") == "protocol_frozen_execution_not_authorized",
        "Stage 5.0 must remain protocol-only",
    )
    checks.append("protocol_only_status")

    authorization = protocol["authorization"]
    _require(authorization["protocol_design_complete"] is True, "protocol must be complete")
    for key in (
        "stage5_data_generation_authorized",
        "stage5_candidate_fitting_authorized",
        "stage5_validation_generation_authorized",
        "stage5_validation_opening_authorized",
        "confirmatory_final_test_authorized",
        "final_test_generated",
        "final_test_opened",
    ):
        _require(authorization[key] is False, f"{key} must be false at Stage 5.0")
    checks.append("execution_and_final_test_firewall")

    firewall = protocol["evidence_firewall"]
    _require(firewall["row_level_stage3_access_from_stage5_code"] is False, "Stage 3 rows are sealed from Stage 5 code")
    _require(firewall["final_test_generator_changes_permitted"] is False, "final-test generator must remain unchanged")
    forbidden = set(firewall["forbidden_for_stage5_fitting_selection_calibration_or_validation"])
    _require(
        {"stage3_training_rows", "stage3_validation_rows", "stage3_validation_predictions", "final_test_rows"}.issubset(forbidden),
        "forbidden evidence list is incomplete",
    )
    checks.append("evidence_firewall")

    partitions = protocol["fresh_partitions"]
    names = (
        "development_fit",
        "development_tune",
        "development_calibration",
        "development_selection",
        "fresh_validation",
    )
    namespaces = [partitions[name]["seed_namespace"] for name in names]
    _require(len(namespaces) == len(set(namespaces)), "fresh partition seed namespaces must be unique")
    _require(all(partitions[name]["rows"] > 0 for name in names), "fresh partitions must have positive size")
    _require(partitions["row_id_overlap_permitted"] is False, "row overlap must be forbidden")
    _require(partitions["stage3_seed_reuse_permitted"] is False, "Stage 3 seed reuse must be forbidden")
    _require(partitions["adaptive_outcome_enrichment_permitted"] is False, "outcome-adaptive enrichment must be forbidden")
    _require(partitions["fresh_validation"]["generate_only_after_candidate_lock"] is True, "fresh validation must follow candidate lock")
    _require(partitions["fresh_validation"]["single_opening"] is True, "fresh validation must be single-opening")
    _require(partitions["excluded_reserved_family"] not in partitions["forcing_families"], "reserved forcing family leaked into Stage 5")
    checks.append("fresh_partition_independence")

    predictors = protocol["pre_outcome_predictors"]
    _require(predictors["post_outcome_variables_allowed_as_predictors"] is False, "post-outcome predictors must be forbidden")
    _require(set(predictors["groups"]) == {"local_state", "scheduled_input", "declared_history", "counterfactual_probe_response"}, "predictor groups changed")
    probe = predictors["probe_design"]
    _require("counterfactual_clones" in probe["implementation"], "probes must not alter the evaluated trajectory")
    _require(len(probe["timing_states"]) >= 2 and len(probe["dose_multipliers"]) >= 2, "probe timing and dose must both vary")
    column_counts = predictors["frozen_encoded_column_counts"]
    _require(column_counts["total"] == sum(column_counts[name] for name in predictors["groups"]), "encoded predictor count is inconsistent")
    checks.append("pre_outcome_predictor_boundary")

    endpoints = protocol["post_outcome_endpoints"]
    _require(endpoints["primary"] == "hosted", "primary outcome must remain hosted")
    _require(set(endpoints["separate_binary_failures"]) == {"target_not_reached", "damage_violation", "integrity_violation"}, "failure endpoints must remain separate")
    _require("never_primary_predictors" in endpoints["routing_response_role"], "post-outcome routing responses cannot become predictors")
    checks.append("outcome_separation")

    _require(len(protocol["prespecified_interactions"]) == 12, "the interaction set must contain exactly 12 frozen terms")
    models = protocol["models"]
    baselines = models["baselines"]
    _require("CM-1-native-logistic" in baselines and "CM-2-native-gradient-boosting" in baselines, "both capacity-matched native baselines are required")
    _require(baselines["CM-1-native-logistic"]["maximum_input_columns"] == models["maximum_relational_input_columns"], "logistic input capacities must match")
    _require(baselines["CM-1-native-logistic"]["maximum_fitted_terms"] == models["maximum_relational_fitted_terms"], "logistic term capacities must match")
    _require(baselines["CM-2-native-gradient-boosting"]["maximum_input_columns"] == models["maximum_relational_input_columns"], "boosting input capacities must match")
    _require(column_counts["total"] <= models["maximum_relational_input_columns"], "relational columns exceed the frozen budget")
    _require(sum(baselines["CM-1-native-logistic"]["frozen_input_groups"].values()) == column_counts["total"], "native and relational encoded column counts must match")
    _require("BL-6-full-native-gradient-boosting" in baselines, "full native gradient-boosting benchmark is required")
    checks.append("candidate_and_capacity_matching")

    fit = protocol["fit_select_calibrate"]
    _require(fit["primary_metric"] == "brier", "Brier score must remain primary")
    _require(fit["winner_lock_required_before_fresh_validation_generation"] is True, "winner lock must precede validation generation")
    _require(fit["development_calibration_role"] == "platt_calibration_only", "calibration partition role changed")
    checks.append("fit_selection_calibration_roles")

    gates = protocol["fresh_validation_gates"]
    _require(gates["all_required_for_final_test_authorization"] is True, "all fresh-validation gates must be required")
    _require(gates["incremental_value_vs_transport"]["minimum_absolute_brier_improvement"] >= 0.005, "incremental threshold was weakened")
    _require(gates["relational_value_vs_additive_ablation"]["minimum_absolute_brier_improvement"] >= 0.005, "relational threshold was weakened")
    _require(gates["capacity_matched_value"]["paired_95_percent_ci_must_exclude_zero"] is True, "capacity-matched CI gate is required")
    _require(gates["compression_vs_full_native_gradient_boosting"]["maximum_feature_fraction"] <= 1 / 3 + 1e-9, "compression feature threshold was weakened")
    checks.append("fresh_validation_thresholds")

    stops = protocol["integrity_and_stop_rules"]
    _require(stops["threshold_changes_after_fresh_validation_opening_permitted"] is False, "post-opening threshold changes must be forbidden")
    _require(stops["additional_candidate_search_after_fresh_validation_opening_confirmatory"] is False, "post-opening candidate search cannot be confirmatory")
    _require("keep_final_test_sealed" in stops["failed_validation_gate_action"], "failed validation must keep final test sealed")
    checks.append("stopping_rules")

    claims = protocol["claims_boundary"]
    _require(claims["stage5_0_is_preregistration_not_evidence"] is True, "Stage 5.0 cannot be evidence")
    _require(claims["relational_routing_validated"] is False and claims["cvt_confirmed"] is False, "validation claims are premature")
    checks.append("claims_boundary")

    return {
        "stage": "5.0",
        "status": "pass",
        "checks_passed": checks,
        "check_count": len(checks),
        "data_generated": False,
        "models_fitted": False,
        "final_test_generated": False,
        "final_test_opened": False,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--protocol", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    with args.protocol.open(encoding="utf-8") as handle:
        report = audit_protocol(json.load(handle))

    rendered = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")


if __name__ == "__main__":
    main()

