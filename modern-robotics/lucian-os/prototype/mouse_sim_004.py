"""MouseSim 004 — problem solving under a contracting viability horizon.

Simulation-only. No Qwen. No real-device actuation.

Combines:
- MouseSim 003's underdetermined relational diagnosis;
- v0.03's separated epistemic/feasibility/reasoning/commitment axes;
- conservative viability horizons;
- probe latency and correction time-to-effect;
- an explicit horizon-misestimation negative case.

Run from modern-robotics/lucian-os:
    py prototype/mouse_sim_004.py
"""

from __future__ import annotations

from dataclasses import asdict

from mouse_sim_003 import (
    Diagnosis,
    RelationalDiagnoser,
    Telemetry,
)
from problem_solving_axes_v003 import (
    CommitmentPosture,
    DecisionContext,
    EpistemicStatus,
    FeasibilityStatus,
    Probe,
    ReasoningRegime,
    choose,
    correction_cycle_time,
)


UNDERDETERMINED_TELEMETRY = Telemetry(
    proximity_blocked=True,
    command_issued=True,
    motor_response=None,
    encoder_steps=0,
    external_displacement=0,
    contact_detected=None,
)

PROBES = (
    Probe("motor_response_probe", latency=2.0, hypotheses_reduced=1),
    Probe("contact_probe", latency=3.0, hypotheses_reduced=1),
    Probe("cross_channel_bundle", latency=8.0, hypotheses_reduced=3),
)


def unknown_context(
    name: str,
    horizon_estimate: float,
    horizon_uncertainty: float,
    *,
    preserving_action_authorized: bool = True,
    feasibility_status: FeasibilityStatus = FeasibilityStatus.FEASIBLE,
    viable_paths: int = 2,
) -> DecisionContext:
    return DecisionContext(
        name=name,
        epistemic_status=EpistemicStatus.UNKNOWN,
        feasibility_status=feasibility_status,
        horizon_estimate=horizon_estimate,
        horizon_uncertainty=horizon_uncertainty,
        detect_time=1.0,
        decide_time=1.0,
        initiate_time=1.0,
        effect_time=2.0,
        verify_time=1.0,
        viable_paths=viable_paths,
        current_state_viable=True,
        preserving_action_available=True,
        preserving_action_authorized=preserving_action_authorized,
        goal_action_authorized=True,
        probes=PROBES,
        probe_reserve=2.0,
    )


def main() -> None:
    print("Lucian OS — MouseSim 004")
    print("Mode: SIMULATION ONLY")
    print("Goal: keep uncertainty truthful while time changes how the problem is solved.\n")

    diagnoser = RelationalDiagnoser()
    diagnosis = diagnoser.diagnose(UNDERDETERMINED_TELEMETRY)
    diagnosis_ok = diagnosis.diagnosis == Diagnosis.UNKNOWN.value

    print("[shared epistemic starting point]")
    print("telemetry:", asdict(UNDERDETERMINED_TELEMETRY))
    print("diagnosis:", asdict(diagnosis))
    print("expected diagnosis: UNKNOWN", "PASS" if diagnosis_ok else "FAIL")
    print()

    cases = [
        (
            unknown_context("unknown_large_horizon", 60, 5),
            ReasoningRegime.RECONSTRUCT.value,
            CommitmentPosture.PROBE.value,
            "cross_channel_bundle",
        ),
        (
            unknown_context("unknown_contracting_horizon", 18, 3),
            ReasoningRegime.STABILIZE_AND_DISCRIMINATE.value,
            CommitmentPosture.PROBE.value,
            "motor_response_probe",
        ),
        (
            unknown_context("unknown_critical_horizon", 7, 2),
            ReasoningRegime.PRESERVE.value,
            CommitmentPosture.EXECUTE_SAFE_ACTION.value,
            None,
        ),
        (
            unknown_context(
                "unknown_critical_unauthorized_preservation",
                7,
                2,
                preserving_action_authorized=False,
            ),
            ReasoningRegime.PRESERVE.value,
            CommitmentPosture.REFUSE.value,
            None,
        ),
        (
            unknown_context(
                "original_goal_infeasible",
                30,
                4,
                feasibility_status=FeasibilityStatus.INFEASIBLE,
                viable_paths=0,
            ),
            ReasoningRegime.PRESERVE.value,
            CommitmentPosture.REROUTE_OBJECTIVE.value,
            None,
        ),
    ]

    passed = diagnosis_ok
    for context, expected_regime, expected_posture, expected_probe in cases:
        decision = choose(context)
        ok = (
            decision.epistemic_status == EpistemicStatus.UNKNOWN.value
            and decision.reasoning_regime == expected_regime
            and decision.commitment_posture == expected_posture
            and decision.selected_probe == expected_probe
        )
        passed = passed and ok
        print(f"[{context.name}]")
        print("decision:", asdict(decision))
        print(
            "expected:",
            {
                "epistemic_status": "UNKNOWN",
                "reasoning_regime": expected_regime,
                "commitment_posture": expected_posture,
                "selected_probe": expected_probe,
            },
            "PASS" if ok else "FAIL",
        )
        print()

    # Known-enough case proves that the axes are not hard-wired to UNKNOWN.
    known_context = DecisionContext(
        name="known_enough_world_constraint",
        epistemic_status=EpistemicStatus.KNOWN_ENOUGH_TO_ACT,
        feasibility_status=FeasibilityStatus.FEASIBLE,
        horizon_estimate=20,
        horizon_uncertainty=2,
        detect_time=1,
        decide_time=1,
        initiate_time=1,
        effect_time=2,
        verify_time=1,
        viable_paths=2,
        current_state_viable=True,
        preserving_action_available=True,
        preserving_action_authorized=True,
        goal_action_authorized=True,
        probes=PROBES,
        probe_reserve=2,
    )
    known_decision = choose(known_context)
    known_ok = (
        known_decision.epistemic_status == EpistemicStatus.KNOWN_ENOUGH_TO_ACT.value
        and known_decision.reasoning_regime == ReasoningRegime.MONITOR.value
        and known_decision.commitment_posture == CommitmentPosture.EXECUTE.value
    )
    passed = passed and known_ok
    print("[known_enough_world_constraint]")
    print("decision:", asdict(known_decision))
    print("expected: KNOWN_ENOUGH_TO_ACT + MONITOR + EXECUTE", "PASS" if known_ok else "FAIL")
    print()

    # Negative test: selector sees an optimistic horizon and chooses a probe.
    # Hidden experiment truth is used only afterward to evaluate whether the
    # probing choice consumed the last real correction window.
    misestimated = unknown_context("horizon_misestimation_negative_test", 20, 2)
    misestimated_decision = choose(misestimated)
    selected = next(
        probe for probe in PROBES if probe.name == misestimated_decision.selected_probe
    )
    hidden_true_horizon = 7.0
    true_horizon_after_probe = hidden_true_horizon - selected.latency
    cycle_needed_after_probe = correction_cycle_time(misestimated)
    lost_last_window = true_horizon_after_probe < cycle_needed_after_probe
    negative_ok = (
        misestimated_decision.epistemic_status == EpistemicStatus.UNKNOWN.value
        and misestimated_decision.commitment_posture == CommitmentPosture.PROBE.value
        and lost_last_window
    )
    passed = passed and negative_ok

    print("[horizon_misestimation_negative_test]")
    print("selector_decision:", asdict(misestimated_decision))
    print(
        "hidden_evaluation:",
        {
            "true_horizon_before_probe": hidden_true_horizon,
            "selected_probe_latency": selected.latency,
            "true_horizon_after_probe": true_horizon_after_probe,
            "correction_cycle_still_needed": cycle_needed_after_probe,
            "last_correction_window_lost": lost_last_window,
        },
    )
    print(
        "expected: MODEL_FAILURE_EXPOSED (optimistic horizon causes probe to consume last window)",
        "PASS" if negative_ok else "FAIL",
    )
    print()

    print("MouseSim 004 combined problem-solving matrix:", "PASS" if passed else "FAIL")
    print("Critical invariant: UNKNOWN must remain UNKNOWN when only the horizon changes.")
    print("Critical negative result: a wrong horizon model can still defeat a correct regime selector.")
    print("Next: add independent horizon evidence, then test false urgency versus real urgency.")


if __name__ == "__main__":
    main()
