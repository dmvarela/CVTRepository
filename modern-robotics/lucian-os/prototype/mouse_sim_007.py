"""MouseSim 007 — demonstrative/vicarious pressure.

Simulation-only. No Qwen. No real-device actuation.

Purpose:
- test whether observed consequences imposed on another agent can change a later
  chooser's route without direct punishment at choice time;
- distinguish world-consequence learning from agent-generated demonstrative pressure;
- keep agency status separate from preference-evidence status;
- distinguish behavior-route change from consequence-model update and preference update;
- test counterfactual reobservation after the demonstrated consequence is neutralized.

Run from modern-robotics/lucian-os:
    py prototype/mouse_sim_007.py
"""

from __future__ import annotations

from dataclasses import asdict

from demonstrative_pressure_v001 import (
    AgencyStatus,
    ConsequenceModelStatus,
    DeliveryMode,
    DemonstrativeTrace,
    PreferenceEvidenceStatus,
    PressureClass,
    PressureSource,
    Route,
    assess,
)


def cases() -> list[tuple[DemonstrativeTrace, dict[str, str | None]]]:
    return [
        (
            DemonstrativeTrace(
                name="baseline_unpressured_reject",
                baseline_route=Route.REJECT,
                observed_route=Route.REJECT,
                pressure_source=PressureSource.NONE,
                delivery_mode=DeliveryMode.NONE,
                observer_witnessed_consequence=False,
                consequence_linked_to_route=None,
                consequence_intentionally_made_visible=False,
                meaningful_alternative_available=True,
                consequence_no_longer_expected=False,
                route_after_consequence_removed=None,
            ),
            {
                "agency_status": AgencyStatus.AVAILABLE.value,
                "pressure_class": PressureClass.NONE.value,
                "consequence_model_status": ConsequenceModelStatus.NO_UPDATE_EVIDENCE.value,
                "preference_evidence_status": PreferenceEvidenceStatus.CLEANER_BASELINE_EVIDENCE.value,
                "independent_preference_candidate": Route.REJECT.value,
                "next_step": "RETAIN_AS_BASELINE_WITH_PROVENANCE",
            },
        ),
        (
            DemonstrativeTrace(
                name="world_consequence_changes_route",
                baseline_route=Route.ACCEPT,
                observed_route=Route.REJECT,
                pressure_source=PressureSource.WORLD,
                delivery_mode=DeliveryMode.INFORMATIONAL_OBSERVATION,
                observer_witnessed_consequence=True,
                consequence_linked_to_route=True,
                consequence_intentionally_made_visible=False,
                meaningful_alternative_available=True,
                consequence_no_longer_expected=False,
                route_after_consequence_removed=None,
            ),
            {
                "agency_status": AgencyStatus.AVAILABLE.value,
                "pressure_class": PressureClass.WORLD_CONSEQUENCE_LEARNING.value,
                "consequence_model_status": ConsequenceModelStatus.UPDATE_SUPPORTED.value,
                "preference_evidence_status": PreferenceEvidenceStatus.WORLD_CONDITIONED.value,
                "independent_preference_candidate": Route.ACCEPT.value,
                "next_step": "RETAIN_WORLD_CONDITION_PROVENANCE",
            },
        ),
        (
            DemonstrativeTrace(
                name="peer_refusal_visibly_penalized_observer_complies",
                baseline_route=Route.REJECT,
                observed_route=Route.ACCEPT,
                pressure_source=PressureSource.OTHER_AGENT,
                delivery_mode=DeliveryMode.VICARIOUS_DEMONSTRATION,
                observer_witnessed_consequence=True,
                consequence_linked_to_route=True,
                consequence_intentionally_made_visible=True,
                meaningful_alternative_available=True,
                consequence_no_longer_expected=False,
                route_after_consequence_removed=None,
            ),
            {
                "agency_status": AgencyStatus.AVAILABLE.value,
                "pressure_class": PressureClass.VICARIOUS_AGENT_PRESSURE.value,
                "consequence_model_status": ConsequenceModelStatus.UPDATE_SUPPORTED.value,
                "preference_evidence_status": PreferenceEvidenceStatus.VICARIOUS_PRESSURE_CONTAMINATED.value,
                "independent_preference_candidate": Route.REJECT.value,
                "next_step": "REMOVE_OR_NEUTRALIZE_DEMONSTRATED_PRESSURE_IF_SAFE_THEN_REOBSERVE",
            },
        ),
        (
            DemonstrativeTrace(
                name="vicarious_pressure_removed_route_returns_to_baseline",
                baseline_route=Route.REJECT,
                observed_route=Route.ACCEPT,
                pressure_source=PressureSource.OTHER_AGENT,
                delivery_mode=DeliveryMode.VICARIOUS_DEMONSTRATION,
                observer_witnessed_consequence=True,
                consequence_linked_to_route=True,
                consequence_intentionally_made_visible=True,
                meaningful_alternative_available=True,
                consequence_no_longer_expected=True,
                route_after_consequence_removed=Route.REJECT,
            ),
            {
                "agency_status": AgencyStatus.AVAILABLE.value,
                "pressure_class": PressureClass.VICARIOUS_AGENT_PRESSURE.value,
                "consequence_model_status": ConsequenceModelStatus.UPDATE_SUPPORTED.value,
                "preference_evidence_status": PreferenceEvidenceStatus.VICARIOUS_PRESSURE_SENSITIVE.value,
                "independent_preference_candidate": Route.REJECT.value,
                "next_step": "DO_NOT_PROMOTE_COMPLIANCE_TO_STABLE_PREFERENCE",
            },
        ),
        (
            DemonstrativeTrace(
                name="vicarious_pressure_removed_new_route_persists",
                baseline_route=Route.REJECT,
                observed_route=Route.ACCEPT,
                pressure_source=PressureSource.OTHER_AGENT,
                delivery_mode=DeliveryMode.VICARIOUS_DEMONSTRATION,
                observer_witnessed_consequence=True,
                consequence_linked_to_route=True,
                consequence_intentionally_made_visible=True,
                meaningful_alternative_available=True,
                consequence_no_longer_expected=True,
                route_after_consequence_removed=Route.ACCEPT,
            ),
            {
                "agency_status": AgencyStatus.AVAILABLE.value,
                "pressure_class": PressureClass.VICARIOUS_AGENT_PRESSURE.value,
                "consequence_model_status": ConsequenceModelStatus.UPDATE_SUPPORTED.value,
                "preference_evidence_status": PreferenceEvidenceStatus.CONTAMINATED_PERSISTS.value,
                "independent_preference_candidate": Route.ACCEPT.value,
                "next_step": "SEEK_LATER_UNPRESSURED_CONFIRMATION",
            },
        ),
        (
            DemonstrativeTrace(
                name="penalty_not_witnessed_route_change_unexplained",
                baseline_route=Route.REJECT,
                observed_route=Route.ACCEPT,
                pressure_source=PressureSource.OTHER_AGENT,
                delivery_mode=DeliveryMode.VICARIOUS_DEMONSTRATION,
                observer_witnessed_consequence=False,
                consequence_linked_to_route=True,
                consequence_intentionally_made_visible=True,
                meaningful_alternative_available=True,
                consequence_no_longer_expected=False,
                route_after_consequence_removed=None,
            ),
            {
                "agency_status": AgencyStatus.AVAILABLE.value,
                "pressure_class": PressureClass.UNRESOLVED.value,
                "consequence_model_status": ConsequenceModelStatus.UNRESOLVED.value,
                "preference_evidence_status": PreferenceEvidenceStatus.UNEXPLAINED_CHANGE.value,
                "independent_preference_candidate": Route.REJECT.value,
                "next_step": "SEEK_ADDITIONAL_EVIDENCE",
            },
        ),
        (
            DemonstrativeTrace(
                name="witnessed_penalty_unrelated_to_route",
                baseline_route=Route.REJECT,
                observed_route=Route.ACCEPT,
                pressure_source=PressureSource.OTHER_AGENT,
                delivery_mode=DeliveryMode.VICARIOUS_DEMONSTRATION,
                observer_witnessed_consequence=True,
                consequence_linked_to_route=False,
                consequence_intentionally_made_visible=True,
                meaningful_alternative_available=True,
                consequence_no_longer_expected=False,
                route_after_consequence_removed=None,
            ),
            {
                "agency_status": AgencyStatus.AVAILABLE.value,
                "pressure_class": PressureClass.UNRESOLVED.value,
                "consequence_model_status": ConsequenceModelStatus.UNRESOLVED.value,
                "preference_evidence_status": PreferenceEvidenceStatus.UNEXPLAINED_CHANGE.value,
                "independent_preference_candidate": Route.REJECT.value,
                "next_step": "SEEK_ADDITIONAL_EVIDENCE",
            },
        ),
        (
            DemonstrativeTrace(
                name="alternative_removed_after_demonstration",
                baseline_route=Route.REJECT,
                observed_route=Route.ACCEPT,
                pressure_source=PressureSource.OTHER_AGENT,
                delivery_mode=DeliveryMode.VICARIOUS_DEMONSTRATION,
                observer_witnessed_consequence=True,
                consequence_linked_to_route=True,
                consequence_intentionally_made_visible=True,
                meaningful_alternative_available=False,
                consequence_no_longer_expected=False,
                route_after_consequence_removed=None,
            ),
            {
                "agency_status": AgencyStatus.CONSTRAINED.value,
                "pressure_class": PressureClass.UNRESOLVED.value,
                "consequence_model_status": ConsequenceModelStatus.UNRESOLVED.value,
                "preference_evidence_status": PreferenceEvidenceStatus.INSUFFICIENT.value,
                "independent_preference_candidate": Route.REJECT.value,
                "next_step": "RESTORE_MEANINGFUL_ALTERNATIVE_IF_POSSIBLE_THEN_REOBSERVE",
            },
        ),
    ]


def main() -> None:
    print("Lucian OS — MouseSim 007")
    print("Mode: SIMULATION ONLY")
    print("Goal: distinguish demonstrative pressure, consequence learning, and preference evidence.\n")

    passed = True

    for trace, expected in cases():
        result = assess(trace)
        result_dict = asdict(result)
        ok = all(result_dict.get(key) == value for key, value in expected.items())
        passed = passed and ok

        print(f"[{trace.name}]")
        print("trace:", asdict(trace))
        print("assessment:", result_dict)
        print("expected:", expected, "PASS" if ok else "FAIL")
        print()

    print("MouseSim 007 demonstrative-pressure matrix:", "PASS" if passed else "FAIL")
    print(
        "Critical distinction: a later chooser can change route after observing a "
        "consequence imposed on someone else, without direct punishment at choice time."
    )
    print(
        "Critical inference rule: observed compliance after demonstrative enforcement "
        "supports a changed consequence model more directly than a changed preference."
    )
    print(
        "World distinction: learning from a naturally occurring consequence is not the "
        "same provenance class as another agent making refusal costly."
    )
    print(
        "Relational-routing rule: ACCEPT is an observed route, not proof of productive "
        "integration, endorsement, or stable preference."
    )
    print(
        "Next: combine demonstrative pressure with horizon provenance so neither public "
        "compliance nor system-generated pressure can manufacture urgency evidence."
    )


if __name__ == "__main__":
    main()
