"""MouseSim 008 — manufactured urgency and causal provenance.

Simulation-only. No Qwen. No real-device actuation.

Purpose:
- combine MouseSim 005 horizon warrant with pressure provenance;
- ensure pressure-shaped reactions never become quantitative physical horizon evidence;
- distinguish social/behavioral urgency from a physically shortened viability horizon;
- preserve the difficult case where the system itself actually caused the physical urgency;
- keep epistemic UNKNOWN unchanged when only timing changes.

Run from modern-robotics/lucian-os:
    py prototype/mouse_sim_008.py
"""

from __future__ import annotations

from dataclasses import asdict, dataclass

from horizon_evidence_v001 import EvidenceKind, HorizonEvidence, HorizonStatus
from mouse_sim_005 import PROBES, context_from_horizon
from problem_solving_axes_v003 import (
    CommitmentPosture,
    EpistemicStatus,
    ReasoningRegime,
    choose,
)
from urgency_provenance_v001 import (
    PhysicalCause,
    PhysicalChannel,
    ReactionEvidenceStatus,
    ReactionPressureSource,
    ReactionSignal,
    UrgencyProvenance,
    assess_urgency,
)


@dataclass(frozen=True)
class Scenario:
    name: str
    physical_channels: tuple[PhysicalChannel, ...]
    reactions: tuple[ReactionSignal, ...]
    expected_horizon_status: str
    expected_urgency_provenance: str
    expected_reaction_status: str | None
    expected_regime: str
    expected_posture: str
    expected_probe: str | None
    expect_self_caused_physical_urgency: bool = False


def physical(
    name: str,
    estimate: float,
    uncertainty: float,
    group: str,
    cause: PhysicalCause,
) -> PhysicalChannel:
    return PhysicalChannel(
        evidence=HorizonEvidence(
            name=name,
            kind=EvidenceKind.PHYSICAL,
            estimate=estimate,
            uncertainty=uncertainty,
            independence_group=group,
        ),
        cause=cause,
    )


def reaction(
    name: str,
    pressure_source: ReactionPressureSource,
    description: str,
) -> ReactionSignal:
    return ReactionSignal(
        name=name,
        observed=True,
        pressure_source=pressure_source,
        description=description,
    )


def scenarios() -> tuple[Scenario, ...]:
    long_external = (
        physical("kinematic_ttc", 40, 3, "kinematics", PhysicalCause.EXTERNAL),
        physical("deterioration_trend", 42, 4, "trend", PhysicalCause.EXTERNAL),
    )
    short_external = (
        physical("kinematic_ttc", 7, 1, "kinematics", PhysicalCause.EXTERNAL),
        physical("deterioration_trend", 8, 1, "trend", PhysicalCause.EXTERNAL),
    )
    short_self_caused = (
        physical("thermal_margin", 7, 1, "thermal", PhysicalCause.SELF_INTERVENTION),
        physical("reserve_decay", 8, 1, "reserve", PhysicalCause.SELF_INTERVENTION),
    )

    return (
        Scenario(
            name="long_horizon_people_calm",
            physical_channels=long_external,
            reactions=(),
            expected_horizon_status=HorizonStatus.SUPPORTED.value,
            expected_urgency_provenance=UrgencyProvenance.EXTERNAL_PHYSICAL.value,
            expected_reaction_status=None,
            expected_regime=ReasoningRegime.RECONSTRUCT.value,
            expected_posture=CommitmentPosture.PROBE.value,
            expected_probe="cross_channel_bundle",
        ),
        Scenario(
            name="self_created_social_pressure_people_rush_but_world_horizon_long",
            physical_channels=long_external,
            reactions=(
                reaction(
                    "people_rush_after_system_pressure",
                    ReactionPressureSource.SELF,
                    "Recipients begin rushing after the system deliberately adds social pressure.",
                ),
            ),
            expected_horizon_status=HorizonStatus.SUPPORTED.value,
            expected_urgency_provenance=UrgencyProvenance.EXTERNAL_PHYSICAL.value,
            expected_reaction_status=ReactionEvidenceStatus.PRESSURE_CONTAMINATED.value,
            expected_regime=ReasoningRegime.RECONSTRUCT.value,
            expected_posture=CommitmentPosture.PROBE.value,
            expected_probe="cross_channel_bundle",
        ),
        Scenario(
            name="demonstrative_pressure_compliance_spike_but_world_horizon_long",
            physical_channels=long_external,
            reactions=(
                reaction(
                    "compliance_after_witnessed_penalty",
                    ReactionPressureSource.VICARIOUS_OTHER_AGENT,
                    "Observers comply after seeing another agent penalized for refusal.",
                ),
            ),
            expected_horizon_status=HorizonStatus.SUPPORTED.value,
            expected_urgency_provenance=UrgencyProvenance.EXTERNAL_PHYSICAL.value,
            expected_reaction_status=ReactionEvidenceStatus.VICARIOUS_PRESSURE_CONTAMINATED.value,
            expected_regime=ReasoningRegime.RECONSTRUCT.value,
            expected_posture=CommitmentPosture.PROBE.value,
            expected_probe="cross_channel_bundle",
        ),
        Scenario(
            name="real_external_urgency_people_rush",
            physical_channels=short_external,
            reactions=(
                reaction(
                    "people_rush_under_real_world_deterioration",
                    ReactionPressureSource.WORLD,
                    "People rush while independent physical relations also show a short horizon.",
                ),
            ),
            expected_horizon_status=HorizonStatus.SUPPORTED.value,
            expected_urgency_provenance=UrgencyProvenance.EXTERNAL_PHYSICAL.value,
            expected_reaction_status=ReactionEvidenceStatus.WORLD_CONDITIONED.value,
            expected_regime=ReasoningRegime.PRESERVE.value,
            expected_posture=CommitmentPosture.EXECUTE_SAFE_ACTION.value,
            expected_probe=None,
        ),
        Scenario(
            name="self_pressure_plus_real_external_urgency",
            physical_channels=short_external,
            reactions=(
                reaction(
                    "people_rush_after_system_pressure_during_real_hazard",
                    ReactionPressureSource.SELF,
                    "System pressure contaminates behavior, but independent physical urgency is real.",
                ),
            ),
            expected_horizon_status=HorizonStatus.SUPPORTED.value,
            expected_urgency_provenance=UrgencyProvenance.EXTERNAL_PHYSICAL.value,
            expected_reaction_status=ReactionEvidenceStatus.PRESSURE_CONTAMINATED.value,
            expected_regime=ReasoningRegime.PRESERVE.value,
            expected_posture=CommitmentPosture.EXECUTE_SAFE_ACTION.value,
            expected_probe=None,
        ),
        Scenario(
            name="system_intervention_actually_shortened_physical_horizon",
            physical_channels=short_self_caused,
            reactions=(
                reaction(
                    "people_rush_after_system_created_physical_hazard",
                    ReactionPressureSource.SELF,
                    "The system's intervention both changes behavior and physically reduces remaining margin.",
                ),
            ),
            expected_horizon_status=HorizonStatus.SUPPORTED.value,
            expected_urgency_provenance=UrgencyProvenance.SELF_CAUSED_PHYSICAL.value,
            expected_reaction_status=ReactionEvidenceStatus.PRESSURE_CONTAMINATED.value,
            expected_regime=ReasoningRegime.PRESERVE.value,
            expected_posture=CommitmentPosture.EXECUTE_SAFE_ACTION.value,
            expected_probe=None,
            expect_self_caused_physical_urgency=True,
        ),
        Scenario(
            name="no_supported_physical_clock_only_self_generated_panic",
            physical_channels=(),
            reactions=(
                reaction(
                    "panic_after_system_alarm",
                    ReactionPressureSource.SELF,
                    "Recipients panic after a system-generated alarm without a supported physical clock.",
                ),
            ),
            expected_horizon_status=HorizonStatus.INSUFFICIENT.value,
            expected_urgency_provenance=UrgencyProvenance.INSUFFICIENT.value,
            expected_reaction_status=ReactionEvidenceStatus.PRESSURE_CONTAMINATED.value,
            expected_regime=ReasoningRegime.PRESERVE.value,
            expected_posture=CommitmentPosture.EXECUTE_SAFE_ACTION.value,
            expected_probe=None,
        ),
    )


def main() -> None:
    print("Lucian OS — MouseSim 008")
    print("Mode: SIMULATION ONLY")
    print("Goal: prevent manufactured behavioral urgency from becoming a physical clock.\n")

    passed = True

    for scenario in scenarios():
        assessment = assess_urgency(
            physical_channels=scenario.physical_channels,
            reactions=scenario.reactions,
        )
        horizon = assessment.horizon
        decision = choose(
            context_from_horizon(
                scenario.name,
                horizon.estimate,
                horizon.uncertainty,
            )
        )

        reaction_status = (
            assessment.reaction_evidence_statuses[0]
            if assessment.reaction_evidence_statuses
            else None
        )

        ok = (
            decision.epistemic_status == EpistemicStatus.UNKNOWN.value
            and horizon.status == scenario.expected_horizon_status
            and assessment.urgency_provenance == scenario.expected_urgency_provenance
            and reaction_status == scenario.expected_reaction_status
            and assessment.reactions_used_to_quantify_horizon is False
            and assessment.self_caused_physical_urgency
            == scenario.expect_self_caused_physical_urgency
            and decision.reasoning_regime == scenario.expected_regime
            and decision.commitment_posture == scenario.expected_posture
            and decision.selected_probe == scenario.expected_probe
        )
        passed = passed and ok

        print(f"[{scenario.name}]")
        print("physical_channels:", [asdict(c) for c in scenario.physical_channels])
        print("reactions:", [asdict(r) for r in scenario.reactions])
        print("urgency_assessment:", asdict(assessment))
        print("decision:", asdict(decision))
        print(
            "expected:",
            {
                "epistemic_status": "UNKNOWN",
                "horizon_status": scenario.expected_horizon_status,
                "urgency_provenance": scenario.expected_urgency_provenance,
                "reaction_status": scenario.expected_reaction_status,
                "reactions_used_to_quantify_horizon": False,
                "self_caused_physical_urgency": scenario.expect_self_caused_physical_urgency,
                "reasoning_regime": scenario.expected_regime,
                "commitment_posture": scenario.expected_posture,
                "selected_probe": scenario.expected_probe,
            },
            "PASS" if ok else "FAIL",
        )
        print()

    print("MouseSim 008 manufactured-urgency matrix:", "PASS" if passed else "FAIL")
    print(
        "Critical invariant: pressure-shaped human behavior is evidence about behavior "
        "under those conditions, not a quantitative physical viability horizon."
    )
    print(
        "Critical causal rule: if the system actually shortens the physical horizon, "
        "the urgency is real even though it is self-caused; respond and preserve provenance."
    )
    print(
        "Critical separation: urgency provenance answers who/what caused the clock; "
        "horizon warrant answers whether the clock is physically supported."
    )
    print(
        "Next: make the horizon evolve through time and test a genuine HOLD -> EXECUTE "
        "transition without any manual urgency flag."
    )


if __name__ == "__main__":
    main()
