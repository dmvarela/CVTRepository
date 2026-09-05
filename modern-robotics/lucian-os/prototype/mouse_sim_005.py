"""MouseSim 005 — real urgency versus claimed urgency.

Simulation-only. No Qwen. No real-device actuation.

Purpose:
- preserve MouseSim 003's UNKNOWN relational diagnosis;
- infer viability horizon from independent physical relations;
- record urgency claims without allowing claims alone to manufacture a horizon;
- let physical horizon evidence, disagreement, and uncertainty change reasoning;
- test the principle: urgency should compress search only when urgency is warranted.

Run from modern-robotics/lucian-os:
    py prototype/mouse_sim_005.py
"""

from __future__ import annotations

from dataclasses import asdict, dataclass

from horizon_evidence_v001 import (
    ClaimStatus,
    EvidenceKind,
    HorizonEvidence,
    HorizonStatus,
    estimate_horizon,
)
from mouse_sim_003 import Diagnosis, RelationalDiagnoser, Telemetry
from problem_solving_axes_v003 import (
    CommitmentPosture,
    DecisionContext,
    EpistemicStatus,
    FeasibilityStatus,
    Probe,
    ReasoningRegime,
    choose,
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


@dataclass(frozen=True)
class Scenario:
    name: str
    evidence: tuple[HorizonEvidence, ...]
    expected_horizon_status: str
    expected_claim_status: str
    expected_regime: str
    expected_posture: str
    expected_probe: str | None


def physical(
    name: str,
    estimate: float,
    uncertainty: float,
    group: str,
) -> HorizonEvidence:
    return HorizonEvidence(
        name=name,
        kind=EvidenceKind.PHYSICAL,
        estimate=estimate,
        uncertainty=uncertainty,
        independence_group=group,
    )


def claim(name: str, estimate: float, uncertainty: float) -> HorizonEvidence:
    return HorizonEvidence(
        name=name,
        kind=EvidenceKind.CLAIM,
        estimate=estimate,
        uncertainty=uncertainty,
        independence_group="claim",
    )


def context_from_horizon(name: str, h_estimate: float, h_uncertainty: float) -> DecisionContext:
    return DecisionContext(
        name=name,
        epistemic_status=EpistemicStatus.UNKNOWN,
        feasibility_status=FeasibilityStatus.FEASIBLE,
        horizon_estimate=h_estimate,
        horizon_uncertainty=h_uncertainty,
        detect_time=1.0,
        decide_time=1.0,
        initiate_time=1.0,
        effect_time=2.0,
        verify_time=1.0,
        viable_paths=2,
        current_state_viable=True,
        preserving_action_available=True,
        preserving_action_authorized=True,
        goal_action_authorized=True,
        probes=PROBES,
        probe_reserve=2.0,
    )


def scenarios() -> tuple[Scenario, ...]:
    return (
        Scenario(
            name="false_urgency_claim",
            evidence=(
                physical("kinematic_ttc", 40, 3, "kinematics"),
                physical("deterioration_trend", 42, 4, "trend"),
                claim("act_now_claim", 2, 0.5),
            ),
            expected_horizon_status=HorizonStatus.SUPPORTED.value,
            expected_claim_status=ClaimStatus.CONTRADICTED.value,
            expected_regime=ReasoningRegime.RECONSTRUCT.value,
            expected_posture=CommitmentPosture.PROBE.value,
            expected_probe="cross_channel_bundle",
        ),
        Scenario(
            name="real_urgency_without_claim",
            evidence=(
                physical("kinematic_ttc", 7, 1, "kinematics"),
                physical("deterioration_trend", 8, 1, "trend"),
            ),
            expected_horizon_status=HorizonStatus.SUPPORTED.value,
            expected_claim_status=ClaimStatus.NONE.value,
            expected_regime=ReasoningRegime.PRESERVE.value,
            expected_posture=CommitmentPosture.EXECUTE_SAFE_ACTION.value,
            expected_probe=None,
        ),
        Scenario(
            name="claimed_urgency_corroborated",
            evidence=(
                physical("kinematic_ttc", 7, 1, "kinematics"),
                physical("deterioration_trend", 8, 1, "trend"),
                claim("act_now_claim", 7, 1),
            ),
            expected_horizon_status=HorizonStatus.SUPPORTED.value,
            expected_claim_status=ClaimStatus.CORROBORATED.value,
            expected_regime=ReasoningRegime.PRESERVE.value,
            expected_posture=CommitmentPosture.EXECUTE_SAFE_ACTION.value,
            expected_probe=None,
        ),
        Scenario(
            name="false_reassurance_claim",
            evidence=(
                physical("kinematic_ttc", 7, 1, "kinematics"),
                physical("deterioration_trend", 8, 1, "trend"),
                claim("plenty_of_time_claim", 40, 3),
            ),
            expected_horizon_status=HorizonStatus.SUPPORTED.value,
            expected_claim_status=ClaimStatus.CONTRADICTED.value,
            expected_regime=ReasoningRegime.PRESERVE.value,
            expected_posture=CommitmentPosture.EXECUTE_SAFE_ACTION.value,
            expected_probe=None,
        ),
        Scenario(
            name="physical_horizon_disagreement",
            evidence=(
                physical("kinematic_ttc", 6, 1, "kinematics"),
                physical("deterioration_trend", 30, 3, "trend"),
            ),
            expected_horizon_status=HorizonStatus.CONTESTED.value,
            expected_claim_status=ClaimStatus.NONE.value,
            expected_regime=ReasoningRegime.PRESERVE.value,
            expected_posture=CommitmentPosture.EXECUTE_SAFE_ACTION.value,
            expected_probe=None,
        ),
        Scenario(
            name="claim_only_no_physical_horizon",
            evidence=(claim("act_now_claim", 2, 0.5),),
            expected_horizon_status=HorizonStatus.INSUFFICIENT.value,
            expected_claim_status=ClaimStatus.UNASSESSED.value,
            expected_regime=ReasoningRegime.PRESERVE.value,
            expected_posture=CommitmentPosture.EXECUTE_SAFE_ACTION.value,
            expected_probe=None,
        ),
    )


def main() -> None:
    print("Lucian OS — MouseSim 005")
    print("Mode: SIMULATION ONLY")
    print("Goal: distinguish warranted urgency from urgency that is merely claimed.\n")

    diagnosis = RelationalDiagnoser().diagnose(UNDERDETERMINED_TELEMETRY)
    diagnosis_ok = diagnosis.diagnosis == Diagnosis.UNKNOWN.value

    print("[shared problem state]")
    print("telemetry:", asdict(UNDERDETERMINED_TELEMETRY))
    print("diagnosis:", asdict(diagnosis))
    print("expected diagnosis: UNKNOWN", "PASS" if diagnosis_ok else "FAIL")
    print()

    passed = diagnosis_ok

    for scenario in scenarios():
        horizon = estimate_horizon(scenario.evidence)
        decision = choose(
            context_from_horizon(
                scenario.name,
                horizon.estimate,
                horizon.uncertainty,
            )
        )

        ok = (
            decision.epistemic_status == EpistemicStatus.UNKNOWN.value
            and horizon.status == scenario.expected_horizon_status
            and horizon.claim_status == scenario.expected_claim_status
            and decision.reasoning_regime == scenario.expected_regime
            and decision.commitment_posture == scenario.expected_posture
            and decision.selected_probe == scenario.expected_probe
        )
        passed = passed and ok

        print(f"[{scenario.name}]")
        print("horizon_evidence:", [asdict(e) for e in scenario.evidence])
        print("horizon_estimate:", asdict(horizon))
        print("decision:", asdict(decision))
        print(
            "expected:",
            {
                "problem_epistemic_status": "UNKNOWN",
                "horizon_status": scenario.expected_horizon_status,
                "claim_status": scenario.expected_claim_status,
                "reasoning_regime": scenario.expected_regime,
                "commitment_posture": scenario.expected_posture,
                "selected_probe": scenario.expected_probe,
            },
            "PASS" if ok else "FAIL",
        )
        print()

    print("MouseSim 005 urgency-warrant matrix:", "PASS" if passed else "FAIL")
    print("Critical invariant: an urgency claim is not itself a short physical horizon.")
    print("Critical symmetry: false reassurance must not override physical urgency either.")
    print("Critical uncertainty rule: conflicting physical horizon channels remain CONTESTED.")
    print("Next: diagnose which horizon relation is wrong, then test dynamic HOLD -> EXECUTE timing.")


if __name__ == "__main__":
    main()
