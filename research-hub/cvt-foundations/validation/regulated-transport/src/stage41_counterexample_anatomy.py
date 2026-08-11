from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any, Iterable

import numpy as np
import pandas as pd


LOCKED_VALIDATION_SHA256 = "e7e49a9bfa99d61664f850fa2e78c86e31c580d4fcfcfff786a3ff360660aad4"
LOCKED_PREDICTIONS_SHA256 = "2889eae1387498de9547a293e2a28a4ee314f79528bb9137cb2843f33b8cecd2"
GATES = {
    "B": "g_b",
    "Q": "g_q",
    "C": "g_c_probe_sham_adjusted_primary",
    "S": "g_s",
}
CAPTURE = [
    "g_c_probe_sham_adjusted_primary",
    "g_c_probe_sham_adjusted_2_5x_dose",
    "g_c_direct_structural_composite",
]
MARGINS = [
    "productive_headroom",
    "buffer_headroom",
    "damage_margin",
    "integrity_margin",
    "reserve_fraction",
    "free_load_margin",
]
SCHEDULE = [
    "peak_source_concentration",
    "peak_permeability",
    "active_duration",
    "pulse_count",
    "scheduled_peak_intact_flux",
    "scheduled_intact_dose",
]
ROUTING = [
    "delivered",
    "productive_total",
    "rejected",
    "productive_at_intervention",
    "peak_damage",
    "minimum_integrity",
    "peak_free_load",
    "terminal_reserve",
    "terminal_reserve_fraction",
]
CVT_MODEL = "CVT-2-minimum"
NATIVE_MODEL = "BL-6-full-native-gradient-boosting"
CLASS_ORDER = [
    "hosted_failed_gate",
    "hosted_all_gates_pass",
    "nonhosted_all_gates_pass",
    "nonhosted_failed_gate",
]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _required(frame: pd.DataFrame, columns: Iterable[str], source: str) -> None:
    missing = sorted(set(columns) - set(frame.columns))
    if missing:
        raise ValueError(f"{source} is missing required columns: {missing}")


def _json_number(value: Any) -> Any:
    if isinstance(value, (np.integer,)):
        return int(value)
    if isinstance(value, (np.floating, float)):
        return None if not np.isfinite(value) else float(value)
    return value


def _records(frame: pd.DataFrame, columns: list[str]) -> list[dict[str, Any]]:
    return [
        {key: _json_number(value) for key, value in row.items()}
        for row in frame.loc[:, columns].to_dict(orient="records")
    ]


def classify(frame: pd.DataFrame, thresholds: dict[str, float]) -> pd.DataFrame:
    result = frame.copy()
    for label, column in GATES.items():
        result[f"gate_{label}_pass"] = result[column] >= thresholds[label]
        result[f"gate_{label}_margin"] = result[column] - thresholds[label]
    pass_columns = [f"gate_{label}_pass" for label in GATES]
    result["all_gates_pass"] = result[pass_columns].all(axis=1)
    result["failed_gate_count"] = (~result[pass_columns]).sum(axis=1).astype(int)
    result["failed_gate_pattern"] = result.apply(
        lambda row: "+".join(label for label in GATES if not row[f"gate_{label}_pass"]) or "none",
        axis=1,
    )
    result["primary_class"] = np.select(
        [
            (result.hosted == 1) & ~result.all_gates_pass,
            (result.hosted == 1) & result.all_gates_pass,
            (result.hosted == 0) & result.all_gates_pass,
            (result.hosted == 0) & ~result.all_gates_pass,
        ],
        CLASS_ORDER,
        default="invalid",
    )
    if (result.primary_class == "invalid").any():
        raise ValueError("Every row must have binary hosted status and exactly one anatomy class")
    return result


def attach_predictions(evidence: pd.DataFrame, predictions: pd.DataFrame) -> pd.DataFrame:
    _required(predictions, ["row_id", "hosted", "forcing_family", CVT_MODEL, NATIVE_MODEL], "predictions")
    if predictions.row_id.duplicated().any() or evidence.row_id.duplicated().any():
        raise ValueError("row_id must be unique in evidence and predictions")
    keep = predictions[["row_id", "hosted", "forcing_family", CVT_MODEL, NATIVE_MODEL]].rename(
        columns={
            "hosted": "prediction_hosted",
            "forcing_family": "prediction_forcing_family",
            CVT_MODEL: "cvt_probability",
            NATIVE_MODEL: "native_gb_probability",
        }
    )
    joined = evidence.merge(keep, on="row_id", how="left", validate="one_to_one")
    if joined.cvt_probability.isna().any() or len(joined) != len(predictions):
        raise ValueError("Evidence and prediction row IDs do not match exactly")
    if not (joined.hosted == joined.prediction_hosted).all():
        raise ValueError("Hosted outcome differs between evidence and predictions")
    if not (joined.forcing_family == joined.prediction_forcing_family).all():
        raise ValueError("Forcing family differs between evidence and predictions")
    joined = joined.drop(columns=["prediction_hosted", "prediction_forcing_family"])
    y = joined.hosted.astype(float)
    joined["cvt_brier_contribution"] = (joined.cvt_probability - y) ** 2
    joined["native_brier_contribution"] = (joined.native_gb_probability - y) ** 2
    joined["cvt_minus_native_brier"] = joined.cvt_brier_contribution - joined.native_brier_contribution
    joined["cvt_underprediction_if_hosted"] = np.where(joined.hosted == 1, 1 - joined.cvt_probability, 0.0)
    joined["cvt_overprediction_if_nonhosted"] = np.where(joined.hosted == 0, joined.cvt_probability, 0.0)
    joined["native_underprediction_if_hosted"] = np.where(joined.hosted == 1, 1 - joined.native_gb_probability, 0.0)
    joined["native_overprediction_if_nonhosted"] = np.where(joined.hosted == 0, joined.native_gb_probability, 0.0)
    joined["probability_error_direction"] = np.where(
        joined.hosted == 1, "underpredict_hosted", "overpredict_nonhosted"
    )
    joined["cvt_classification_error"] = ((joined.cvt_probability >= 0.5).astype(int) != joined.hosted).astype(int)
    joined["native_classification_error"] = ((joined.native_gb_probability >= 0.5).astype(int) != joined.hosted).astype(int)
    joined["classification_error_partition"] = np.select(
        [
            (joined.cvt_classification_error == 1) & (joined.native_classification_error == 0),
            (joined.cvt_classification_error == 0) & (joined.native_classification_error == 1),
            (joined.cvt_classification_error == 1) & (joined.native_classification_error == 1),
        ],
        ["cvt_only", "native_only", "shared"],
        default="neither",
    )
    joined["lower_brier_model"] = np.select(
        [joined.cvt_minus_native_brier > 1e-15, joined.cvt_minus_native_brier < -1e-15],
        ["native", "cvt"],
        default="tie",
    )
    return joined


def attach_nearest_controls(frame: pd.DataFrame) -> pd.DataFrame:
    result = frame.copy()
    result["nearest_control_row_id"] = ""
    result["nearest_control_class"] = ""
    result["nearest_control_gate_distance"] = np.nan
    contrasts = {
        "hosted_failed_gate": "nonhosted_failed_gate",
        "nonhosted_all_gates_pass": "hosted_all_gates_pass",
    }
    gate_columns = list(GATES.values())
    for query_class, control_class in contrasts.items():
        query = result[result.primary_class == query_class].sort_values("row_id")
        control = result[result.primary_class == control_class].sort_values("row_id")
        if query.empty or control.empty:
            continue
        q_values = query[gate_columns].to_numpy(float)
        c_values = control[gate_columns].to_numpy(float)
        for start in range(0, len(query), 256):
            stop = min(start + 256, len(query))
            squared = ((q_values[start:stop, None, :] - c_values[None, :, :]) ** 2).sum(axis=2)
            nearest = squared.argmin(axis=1)
            indices = query.index[start:stop]
            result.loc[indices, "nearest_control_row_id"] = control.iloc[nearest].row_id.to_numpy()
            result.loc[indices, "nearest_control_class"] = control_class
            result.loc[indices, "nearest_control_gate_distance"] = np.sqrt(squared[np.arange(stop - start), nearest])
    return result


def numeric_summary(frame: pd.DataFrame, columns: list[str]) -> dict[str, Any]:
    output: dict[str, Any] = {}
    for column in columns:
        values = frame[column].dropna().astype(float)
        output[column] = {
            "count": int(len(values)),
            "mean": _json_number(values.mean()),
            "median": _json_number(values.median()),
            "q25": _json_number(values.quantile(0.25)),
            "q75": _json_number(values.quantile(0.75)),
            "min": _json_number(values.min()),
            "max": _json_number(values.max()),
        }
    return output


def count_table(frame: pd.DataFrame, row: str, column: str) -> dict[str, dict[str, int]]:
    table = pd.crosstab(frame[row], frame[column])
    return {
        str(index): {str(key): int(value) for key, value in values.items()}
        for index, values in table.to_dict(orient="index").items()
    }


def contrast_deltas(frame: pd.DataFrame, left: str, right: str, columns: list[str]) -> dict[str, Any]:
    a = frame[frame.primary_class == left]
    b = frame[frame.primary_class == right]
    return {
        column: {
            "left_mean": _json_number(a[column].mean()),
            "right_mean": _json_number(b[column].mean()),
            "mean_difference_left_minus_right": _json_number(a[column].mean() - b[column].mean()),
            "left_median": _json_number(a[column].median()),
            "right_median": _json_number(b[column].median()),
            "median_difference_left_minus_right": _json_number(a[column].median() - b[column].median()),
        }
        for column in columns
    }


def build_summary(
    frame: pd.DataFrame,
    thresholds: dict[str, float],
    source_hashes: dict[str, str],
) -> dict[str, Any]:
    total = len(frame)
    class_counts = {name: int((frame.primary_class == name).sum()) for name in CLASS_ORDER}
    by_class_stats = {}
    stats_columns = list(GATES.values()) + MARGINS + SCHEDULE + CAPTURE + ROUTING + [
        "cvt_probability",
        "native_gb_probability",
        "cvt_brier_contribution",
        "native_brier_contribution",
        "cvt_minus_native_brier",
    ]
    for name in CLASS_ORDER:
        part = frame[frame.primary_class == name]
        by_class_stats[name] = numeric_summary(part, stats_columns)

    family_concentration: dict[str, Any] = {}
    overall_contradiction_rate = float(frame.primary_class.isin([CLASS_ORDER[0], CLASS_ORDER[2]]).mean())
    for family, part in frame.groupby("forcing_family", sort=True):
        hosted = part[part.hosted == 1]
        nonhosted = part[part.hosted == 0]
        contradiction_rate = float(part.primary_class.isin([CLASS_ORDER[0], CLASS_ORDER[2]]).mean())
        family_concentration[str(family)] = {
            "rows": int(len(part)),
            "contradiction_count": int(part.primary_class.isin([CLASS_ORDER[0], CLASS_ORDER[2]]).sum()),
            "contradiction_rate": contradiction_rate,
            "contradiction_rate_lift_vs_overall": contradiction_rate / overall_contradiction_rate,
            "hosted_failed_gate_share_of_hosted": _json_number((hosted.primary_class == CLASS_ORDER[0]).mean()),
            "nonhosted_all_gates_pass_share_of_nonhosted": _json_number((nonhosted.primary_class == CLASS_ORDER[2]).mean()),
        }

    model_error_by_class: dict[str, Any] = {}
    for name in CLASS_ORDER:
        part = frame[frame.primary_class == name]
        model_error_by_class[name] = {
            "rows": int(len(part)),
            "cvt_mean_probability": _json_number(part.cvt_probability.mean()),
            "native_mean_probability": _json_number(part.native_gb_probability.mean()),
            "cvt_mean_brier_contribution": _json_number(part.cvt_brier_contribution.mean()),
            "native_mean_brier_contribution": _json_number(part.native_brier_contribution.mean()),
            "cvt_minus_native_mean_brier": _json_number(part.cvt_minus_native_brier.mean()),
            "cvt_classification_errors": int(part.cvt_classification_error.sum()),
            "native_classification_errors": int(part.native_classification_error.sum()),
            "cvt_mean_underprediction_if_hosted": _json_number(part.cvt_underprediction_if_hosted.mean()),
            "cvt_mean_overprediction_if_nonhosted": _json_number(part.cvt_overprediction_if_nonhosted.mean()),
            "native_mean_underprediction_if_hosted": _json_number(part.native_underprediction_if_hosted.mean()),
            "native_mean_overprediction_if_nonhosted": _json_number(part.native_overprediction_if_nonhosted.mean()),
            "classification_error_partition": {str(k): int(v) for k, v in part.classification_error_partition.value_counts().items()},
            "lower_brier_model": {str(k): int(v) for k, v in part.lower_brier_model.value_counts().items()},
        }

    example_columns = [
        "row_id",
        "primary_class",
        "forcing_family",
        "forcing_stratum",
        "failed_gate_pattern",
        "failure_reason",
        "cvt_probability",
        "native_gb_probability",
        "cvt_minus_native_brier",
        "nearest_control_row_id",
        "nearest_control_gate_distance",
    ]
    examples: dict[str, Any] = {}
    for name in [CLASS_ORDER[0], CLASS_ORDER[2]]:
        part = frame[frame.primary_class == name]
        examples[name] = {
            "nearest_in_gate_space": _records(part.nsmallest(5, "nearest_control_gate_distance"), example_columns),
            "largest_cvt_error": _records(part.nlargest(5, "cvt_brier_contribution"), example_columns),
            "largest_native_advantage": _records(part.nlargest(5, "cvt_minus_native_brier"), example_columns),
            "largest_cvt_advantage": _records(part.nsmallest(5, "cvt_minus_native_brier"), example_columns),
        }

    return {
        "stage": "4.1",
        "status": "exploratory_counterexample_anatomy",
        "confirmatory_claim": False,
        "confirmatory_test_authorized": False,
        "final_test_generated": False,
        "final_test_opened": False,
        "source_hashes": source_hashes,
        "gate_thresholds": thresholds,
        "rows": total,
        "class_counts": class_counts,
        "class_rates": {key: value / total for key, value in class_counts.items()},
        "class_by_forcing_family": count_table(frame, "primary_class", "forcing_family"),
        "class_by_forcing_stratum": count_table(frame, "primary_class", "forcing_stratum"),
        "forcing_family_concentration": family_concentration,
        "failed_gate_patterns_by_class": count_table(frame, "primary_class", "failed_gate_pattern"),
        "failure_reason_by_class": count_table(frame, "primary_class", "failure_reason"),
        "statistics_by_class": by_class_stats,
        "contrasts": {
            "hosted_failed_gate_vs_nonhosted_failed_gate": contrast_deltas(
                frame, CLASS_ORDER[0], CLASS_ORDER[3], MARGINS + SCHEDULE + ROUTING
            ),
            "nonhosted_all_gates_pass_vs_hosted_all_gates_pass": contrast_deltas(
                frame, CLASS_ORDER[2], CLASS_ORDER[1], MARGINS + SCHEDULE + ROUTING
            ),
        },
        "model_error_by_class": model_error_by_class,
        "examples": examples,
    }


def build_hypotheses(summary: dict[str, Any]) -> dict[str, Any]:
    patterns = summary["failed_gate_patterns_by_class"]["hosted_failed_gate"]
    leading_pattern, leading_count = max(patterns.items(), key=lambda item: (item[1], item[0]))
    capture_involved = sum(count for pattern, count in patterns.items() if "C" in pattern.split("+"))
    hosted_failed_total = summary["class_counts"]["hosted_failed_gate"]
    reasons = summary["failure_reason_by_class"]["nonhosted_all_gates_pass"]
    leading_reason, leading_reason_count = max(reasons.items(), key=lambda item: (item[1], item[0]))
    all_pass_contrast = summary["contrasts"]["nonhosted_all_gates_pass_vs_hosted_all_gates_pass"]
    family = max(
        summary["forcing_family_concentration"].items(),
        key=lambda item: item[1]["nonhosted_all_gates_pass_share_of_nonhosted"],
    )
    error = summary["model_error_by_class"]
    return {
        "stage": "4.1",
        "status": "exploratory_hypotheses_only",
        "suitable_for_final_test": False,
        "requires_fresh_development_partition": True,
        "final_test_generated": False,
        "final_test_opened": False,
        "hypotheses": [
            {
                "id": "RR-H1",
                "claim": "A failed local gate can be survivable when the realized routing configuration preserves damage, integrity, and reserve margins.",
                "anatomy_signal": {
                    "most_common_hosted_failed_gate_pattern": leading_pattern,
                    "count": leading_count,
                    "capture_gate_involved_count": capture_involved,
                    "capture_gate_involved_share": capture_involved / hosted_failed_total,
                },
                "alternative_explanations": ["threshold miscalibration", "proxy measurement error", "simulation-specific compensation"],
                "fresh_test": "Preregister interactions between failed-gate identity and pre-contact margin configuration on a new development partition.",
            },
            {
                "id": "RR-H2",
                "claim": "Passing all four local gates is insufficient: most all-pass failures did not reach the transformation target, while a smaller subset lost viability through damage or integrity failure.",
                "anatomy_signal": {
                    "dominant_failure_reason": leading_reason,
                    "dominant_failure_reason_count": leading_reason_count,
                    "dominant_failure_reason_share": leading_reason_count / summary["class_counts"]["nonhosted_all_gates_pass"],
                    "family_with_highest_all_pass_failure_share": family[0],
                    "share_of_nonhosted": family[1]["nonhosted_all_gates_pass_share_of_nonhosted"],
                    "scheduled_dose_mean_difference_failed_minus_hosted_all_pass": all_pass_contrast["scheduled_intact_dose"]["mean_difference_left_minus_right"],
                },
                "alternative_explanations": ["forcing-family imbalance", "unmeasured history", "gate thresholds fitted to the wrong contrast"],
                "fresh_test": "Cross a fresh schedule field with dose, active duration, and recovery horizon before fitting revised candidates.",
            },
            {
                "id": "RR-H3",
                "claim": "Capture readiness should be modeled as an input-conditioned response relation rather than a coequal stored gate.",
                "anatomy_signal": {
                    "capture_proxy_context": "Primary and 2.5x micro-probes were nearly identical in Stage 3.2.5, while the direct structural composite was worse after fair calibration.",
                    "working_form": "C = C(B, Q, S, input, current_load, history)",
                },
                "alternative_explanations": ["micro-probe lacks dynamic range", "direct composite is misspecified"],
                "fresh_test": "Design multiple probe timings and doses on a new development partition and preregister response-surface candidates.",
            },
            {
                "id": "RR-H4",
                "claim": "The native gradient booster gains most on hosted cases, while rare confident nonhosted errors can erase its average advantage within the nonhosted anatomy classes.",
                "anatomy_signal": {
                    name: values["cvt_minus_native_mean_brier"] for name, values in error.items()
                },
                "alternative_explanations": ["higher native model capacity", "calibration differences", "simulation equations favor native inputs"],
                "fresh_test": "Freeze an interaction-limited relational CVT candidate and compare it with capacity-matched native baselines on fresh development data.",
            },
            {
                "id": "RR-H5",
                "claim": "A revised CVT candidate should represent routing channels explicitly: productive uptake, rejection, buffering, damage, and recovery.",
                "anatomy_signal": "The Stage 4.1 class contrasts report realized routing quantities separately rather than collapsing them into gate possession.",
                "alternative_explanations": ["post-outcome routing variables are descriptive only and cannot be used as predictors"],
                "fresh_test": "Define pre-outcome estimators for routing propensities before using them in any new candidate.",
            },
        ],
    }


def _markdown_table(headers: list[str], rows: list[list[Any]]) -> str:
    lines = ["| " + " | ".join(headers) + " |", "|" + "|".join(["---"] * len(headers)) + "|"]
    lines.extend("| " + " | ".join(str(value) for value in row) + " |" for row in rows)
    return "\n".join(lines)


def build_review(summary: dict[str, Any], hypotheses: dict[str, Any]) -> str:
    counts = summary["class_counts"]
    family_rows = []
    for family, values in summary["forcing_family_concentration"].items():
        family_rows.append([
            family,
            values["rows"],
            values["contradiction_count"],
            f"{values['contradiction_rate']:.3f}",
            f"{values['hosted_failed_gate_share_of_hosted']:.3f}",
            f"{values['nonhosted_all_gates_pass_share_of_nonhosted']:.3f}",
        ])
    pattern_rows = sorted(
        (
            item
            for item in summary["failed_gate_patterns_by_class"]["hosted_failed_gate"].items()
            if item[1] > 0
        ),
        key=lambda item: (-item[1], item[0]),
    )
    reason_rows = sorted(
        (
            item
            for item in summary["failure_reason_by_class"]["nonhosted_all_gates_pass"].items()
            if item[1] > 0
        ),
        key=lambda item: (-item[1], item[0]),
    )
    error_rows = []
    for name in CLASS_ORDER:
        values = summary["model_error_by_class"][name]
        error_rows.append([
            name,
            values["rows"],
            f"{values['cvt_mean_probability']:.4f}",
            f"{values['native_mean_probability']:.4f}",
            f"{values['cvt_mean_brier_contribution']:.4f}",
            f"{values['native_mean_brier_contribution']:.4f}",
        ])
    all_pass_contrast = summary["contrasts"]["nonhosted_all_gates_pass_vs_hosted_all_gates_pass"]
    failed_contrast = summary["contrasts"]["hosted_failed_gate_vs_nonhosted_failed_gate"]
    return f"""# CVT Regulated-Transport Validation â€” Stage 4.1 Counterexample Anatomy

**Status:** exploratory architecture repair after a failed validation geometry  
**Evidence boundary:** already-opened Stage 3.1 validation evidence, locked Stage 3.2 predictions, and Stage 3.2.5 closure only  
**Final-test status:** ungenerated, unopened, and not authorized

## Result

Stage 4.1 reproduces the two load-bearing contradictions exactly: **{counts['hosted_failed_gate']}** hosted cases failed at least one frozen gate, and **{counts['nonhosted_all_gates_pass']}** nonhosted cases passed all four. The clean controls contain {counts['hosted_all_gates_pass']} hosted all-pass cases and {counts['nonhosted_failed_gate']} nonhosted failed-gate cases. These are exploratory descriptions of the already-opened validation partition, not a new validation claim.

## Forcing-family concentration

{_markdown_table(['family', 'rows', 'contradictions', 'contradiction rate', 'failed-gate share of hosted', 'all-pass share of nonhosted'], family_rows)}

The table separates raw counts from within-family rates. Concentration is therefore interpreted as a schedule clue, not as evidence that a forcing family is intrinsically causal.

## Survivable failed-gate patterns

{_markdown_table(['failed-gate pattern', 'hosted count'], [[key, value] for key, value in pattern_rows])}

The dominant pattern identifies where the literal hard-intersection reading breaks most often. A surviving failed gate should not be read as irrelevant: it may indicate compensation, a poorly placed threshold, or a proxy that does not represent the relevant relation under contact.

## All-gates-pass failure reasons

{_markdown_table(['recorded failure reason', 'count'], [[key, value] for key, value in reason_rows])}

The all-pass failures show that local adequacy is not sufficient. Their schedule and realized-routing profiles must be read together; post-outcome routing quantities here are anatomy labels, not admissible inputs for a future predictor.

## CVT versus native gradient-boosting errors

{_markdown_table(['class', 'n', 'mean CVT p', 'mean native p', 'CVT mean Brier', 'native mean Brier'], error_rows)}

The native model's advantage is class-dependent rather than uniform. That pattern is consistent with omitted interactions, but it is also compatible with ordinary capacity differences and with a simulated world whose native equations favor native features.

In particular, the native model sharply reduces mean error on hosted rows, including the failed-gate contradictions. The locked CVT model assigns every hosted validation row a probability below 0.5. Within the nonhosted classes, the native model is closer on most individual rows but a small number of high-probability false positives raise its class-mean Brier contribution above CVT's. This is a probability-error comparison, not a new decision threshold claim.

## Margin and schedule contrasts

Among all-pass rows, failed minus hosted mean damage margin is {all_pass_contrast['damage_margin']['mean_difference_left_minus_right']:.4f}, integrity margin is {all_pass_contrast['integrity_margin']['mean_difference_left_minus_right']:.4f}, reserve fraction is {all_pass_contrast['reserve_fraction']['mean_difference_left_minus_right']:.4f}, scheduled peak intact flux is {all_pass_contrast['scheduled_peak_intact_flux']['mean_difference_left_minus_right']:.4f}, and scheduled intact dose is {all_pass_contrast['scheduled_intact_dose']['mean_difference_left_minus_right']:.4f}.

Among failed-gate rows, hosted minus nonhosted mean damage margin is {failed_contrast['damage_margin']['mean_difference_left_minus_right']:.4f}, integrity margin is {failed_contrast['integrity_margin']['mean_difference_left_minus_right']:.4f}, reserve fraction is {failed_contrast['reserve_fraction']['mean_difference_left_minus_right']:.4f}, scheduled peak intact flux is {failed_contrast['scheduled_peak_intact_flux']['mean_difference_left_minus_right']:.4f}, and scheduled intact dose is {failed_contrast['scheduled_intact_dose']['mean_difference_left_minus_right']:.4f}.

These contrasts support a relational reading: the same gate status can terminate differently under different margin, timing, and routing configurations. They do not establish a replacement equation.

The all-pass failures are not primarily overload cases. Of the {counts['nonhosted_all_gates_pass']} cases, {summary['failure_reason_by_class']['nonhosted_all_gates_pass'].get('target_not_reached', 0)} fail because the transformation target is not reached, with the remainder split between recorded damage and integrity violations. Their scheduled intact dose is lower on average than in hosted all-pass controls. Gate adequacy therefore appears insufficient both for producing enough transformation and for protecting viability once contact occurs.

## Relational-routing hypotheses

The companion `relational_routing_hypotheses.json` records {len(hypotheses['hypotheses'])} hypotheses. Every hypothesis is marked exploratory, includes rival explanations, and requires a fresh development partition before candidate selection. The current final test is not an admissible development resource.

## Reproducibility and boundary audit

- Validation evidence SHA-256: `{summary['source_hashes']['validation_csv']}`
- Locked predictions SHA-256: `{summary['source_hashes']['validation_predictions_csv']}`
- Exactly {summary['rows']} de-identified validation row IDs appear in `counterexample_anatomy.csv`.
- No final-test generator, partition, outcome, or prediction was read or materialized.
- `confirmatory_test_authorized = false`
- `final_test_generated = false`
- `final_test_opened = false`

## Decision

Proceed only to a Stage 4.2 architecture decision. If relational routing is developed further, Stage 5 must begin with a fresh development partition and a new preregistration. Stage 4.1 does not authorize the preserved final test.
"""


def output_columns() -> list[str]:
    # Keep the row-level artifact compact and de-identified. Boolean pass flags,
    # threshold margins, individual loss terms, and post-outcome routing values
    # remain exactly derivable or are summarized in counterexample_summary.json.
    return [
        "row_id",
        "hosted",
        "target_reached",
        "viable",
        "failure_reason",
        "forcing_family",
        "forcing_stratum",
        "primary_class",
        "failed_gate_pattern",
        *list(GATES.values()),
        "g_c_probe_sham_adjusted_2_5x_dose",
        "g_c_direct_structural_composite",
        *MARGINS,
        *SCHEDULE,
        "cvt_probability",
        "native_gb_probability",
        "cvt_minus_native_brier",
        "nearest_control_row_id",
        "nearest_control_gate_distance",
    ]


def run(
    validation_path: Path,
    predictions_path: Path,
    selection_path: Path,
    authorization_path: Path,
    output_dir: Path,
    review_path: Path,
) -> dict[str, Any]:
    source_hashes = {
        "validation_csv": sha256(validation_path),
        "validation_predictions_csv": sha256(predictions_path),
        "selection_json": sha256(selection_path),
        "authorization_decision_json": sha256(authorization_path),
    }
    if source_hashes["validation_csv"] != LOCKED_VALIDATION_SHA256:
        raise ValueError("Validation evidence does not match the locked Stage 3.1 SHA-256")
    if source_hashes["validation_predictions_csv"] != LOCKED_PREDICTIONS_SHA256:
        raise ValueError("Predictions do not match the locked Stage 3.2 SHA-256")

    selection = json.loads(selection_path.read_text(encoding="utf-8"))
    authorization = json.loads(authorization_path.read_text(encoding="utf-8"))
    if any(
        [
            authorization.get("confirmatory_test_authorized"),
            authorization.get("final_test_generated"),
            authorization.get("final_test_opened"),
        ]
    ):
        raise ValueError("Stage 3.2.5 boundary does not authorize Stage 4.1")
    thresholds = dict(zip(GATES, selection["counterexamples"]["thresholds"], strict=True))
    evidence = pd.read_csv(validation_path)
    predictions = pd.read_csv(predictions_path)
    _required(
        evidence,
        [
            "row_id",
            "hosted",
            "target_reached",
            "viable",
            "failure_reason",
            "forcing_family",
            "forcing_stratum",
            *GATES.values(),
            *CAPTURE,
            *MARGINS,
            *SCHEDULE,
            *ROUTING,
        ],
        "validation evidence",
    )
    if len(evidence) != 4000 or set(evidence.partition.unique()) != {"validation"}:
        raise ValueError("Stage 4.1 requires the locked 4,000-row validation partition")
    frame = attach_predictions(classify(evidence, thresholds), predictions)
    frame.failure_reason = frame.failure_reason.fillna("none_recorded").astype(str)
    frame = attach_nearest_controls(frame)
    if int((frame.primary_class == CLASS_ORDER[0]).sum()) != selection["counterexamples"]["hosted_with_failed_gate"]:
        raise ValueError("Hosted failed-gate count does not reproduce the Stage 3.2 lock")
    if int((frame.primary_class == CLASS_ORDER[2]).sum()) != selection["counterexamples"]["nonhosted_all_gates_pass"]:
        raise ValueError("Nonhosted all-pass count does not reproduce the Stage 3.2 lock")

    summary = build_summary(frame, thresholds, source_hashes)
    hypotheses = build_hypotheses(summary)
    output_dir.mkdir(parents=True, exist_ok=True)
    review_path.parent.mkdir(parents=True, exist_ok=True)
    anatomy_path = output_dir / "counterexample_anatomy.csv"
    summary_path = output_dir / "counterexample_summary.json"
    hypotheses_path = output_dir / "relational_routing_hypotheses.json"
    export = frame.loc[:, output_columns()].copy()
    for column in ["hosted", "target_reached", "viable"]:
        export[column] = export[column].astype(int)
    export.to_csv(anatomy_path, index=False, float_format="%.6g")
    summary["output_hashes"] = {"counterexample_anatomy_csv": sha256(anatomy_path)}
    summary_path.write_text(json.dumps(summary, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    hypotheses_path.write_text(json.dumps(hypotheses, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    review_path.write_text(build_review(summary, hypotheses), encoding="utf-8")
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description="Execute the frozen Stage 4.1 counterexample anatomy")
    parser.add_argument("--validation", type=Path, required=True)
    parser.add_argument("--predictions", type=Path, required=True)
    parser.add_argument("--selection", type=Path, required=True)
    parser.add_argument("--authorization", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--review", type=Path, required=True)
    args = parser.parse_args()
    summary = run(
        args.validation,
        args.predictions,
        args.selection,
        args.authorization,
        args.output,
        args.review,
    )
    print(json.dumps({"rows": summary["rows"], "class_counts": summary["class_counts"]}, indent=2))


if __name__ == "__main__":
    main()

