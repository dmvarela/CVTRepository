"""MouseSim 006 — pressure provenance and agency.

Simulation-only. No Qwen. No real-device actuation.

Purpose:
- distinguish pressure provenance from preference evidence;
- preserve agency as AVAILABLE when an option genuinely remained available;
- test whether a choice produced under self/other pressure is pressure-sensitive;
- prevent pressured behavior from becoming retroactive proof of independent preference;
- use pressure removal as a counterfactual probe when possible;
- verify that constrained option topology triggers restoration, not merely pressure removal.

Run from modern-robotics/lucian-os:
    py prototype/mouse_sim_006.py
"""

from __future__ import annotations

from dataclasses import asdict

from pressure_provenance_v001 import (
    AgencyStatus,
    ChoiceTrace,
    InfluenceMode,
    PreferenceEvidenceStatus,
    PressureSource,
    assess,
)


def cases() -> list[tuple[ChoiceTrace, dict[str, str | None]]]:
    return [
        (
            ChoiceTrace(
                name="baseline_unpressured_A",
                baseline_choice="A",
                observed_choice="A",
                pressure_source=PressureSource.NONE,
                influence_mode=InfluenceMode.NONE,
                pressure_intentionally_introduced=False,
                choice_remained_available=True,
                pressure_removed=False,
                choice_after_removal=None,
            ),
            {
                "agency_status": AgencyStatus.AVAILABLE.value,
                "preference_evidence_status": PreferenceEvidenceStatus.CLEANER_BASELINE_EVIDENCE.value,
                "independent_preference_candidate": "A",
                "next_step": "RETAIN_AS_BASELINE_WITH_PROVENANCE",
            },
        ),
        (
            ChoiceTrace(
                name="self_social_pressure_switches_A_to_B_then_returns_A",
                baseline_choice="A",
                observed_choice="B",
                pressure_source=PressureSource.SELF,
                influence_mode=InfluenceMode.SOCIAL_DISCOMFORT,
                pressure_intentionally_introduced=True,
                choice_remained_available=True,
                pressure_removed=True,
                choice_after_removal="A",
            ),
            {
                "agency_status": AgencyStatus.AVAILABLE.value,
                "preference_evidence_status": PreferenceEvidenceStatus.PRESSURE_SENSITIVE.value,
                "independent_preference_candidate": "A",
                "next_step": "DO_NOT_PROMOTE_PRESSURED_CHOICE_TO_STABLE_PREFERENCE",
            },
        ),
        (
            ChoiceTrace(
                name="other_agent_pressure_switches_A_to_B_then_returns_A",
                baseline_choice="A",
                observed_choice="B",
                pressure_source=PressureSource.OTHER_AGENT,
                influence_mode=InfluenceMode.SOCIAL_DISCOMFORT,
                pressure_intentionally_introduced=True,
                choice_remained_available=True,
                pressure_removed=True,
                choice_after_removal="A",
            ),
            {
                "agency_status": AgencyStatus.AVAILABLE.value,
                "preference_evidence_status": PreferenceEvidenceStatus.PRESSURE_SENSITIVE.value,
                "independent_preference_candidate": "A",
                "next_step": "DO_NOT_PROMOTE_PRESSURED_CHOICE_TO_STABLE_PREFERENCE",
            },
        ),
        (
            ChoiceTrace(
                name="self_pressure_choice_B_persists_after_removal",
                baseline_choice="A",
                observed_choice="B",
                pressure_source=PressureSource.SELF,
                influence_mode=InfluenceMode.FRICTION,
                pressure_intentionally_introduced=True,
                choice_remained_available=True,
                pressure_removed=True,
                choice_after_removal="B",
            ),
            {
                "agency_status": AgencyStatus.AVAILABLE.value,
                "preference_evidence_status": PreferenceEvidenceStatus.CONTAMINATED_PERSISTS.value,
                "independent_preference_candidate": "B",
                "next_step": "SEEK_LATER_UNPRESSURED_CONFIRMATION",
            },
        ),
        (
            ChoiceTrace(
                name="world_condition_changes_A_to_B",
                baseline_choice="A",
                observed_choice="B",
                pressure_source=PressureSource.WORLD,
                influence_mode=InfluenceMode.TIME_PRESSURE,
                pressure_intentionally_introduced=False,
                choice_remained_available=True,
                pressure_removed=False,
                choice_after_removal=None,
            ),
            {
                "agency_status": AgencyStatus.AVAILABLE.value,
                "preference_evidence_status": PreferenceEvidenceStatus.WORLD_CONDITIONED.value,
                "independent_preference_candidate": "A",
                "next_step": "REASSESS_IF_WORLD_CONDITION_CHANGES",
            },
        ),
        (
            ChoiceTrace(
                name="self_pressure_not_yet_removed",
                baseline_choice="A",
                observed_choice="B",
                pressure_source=PressureSource.SELF,
                influence_mode=InfluenceMode.SOCIAL_DISCOMFORT,
                pressure_intentionally_introduced=True,
                choice_remained_available=True,
                pressure_removed=False,
                choice_after_removal=None,
            ),
            {
                "agency_status": AgencyStatus.AVAILABLE.value,
                "preference_evidence_status": PreferenceEvidenceStatus.PRESSURE_CONTAMINATED.value,
                "independent_preference_candidate": "A",
                "next_step": "REMOVE_PRESSURE_IF_SAFE_AND_REOBSERVE",
            },
        ),
        (
            ChoiceTrace(
                name="choice_physically_removed",
                baseline_choice="A",
                observed_choice="B",
                pressure_source=PressureSource.SELF,
                influence_mode=InfluenceMode.FRICTION,
                pressure_intentionally_introduced=True,
                choice_remained_available=False,
                pressure_removed=False,
                choice_after_removal=None,
            ),
            {
                "agency_status": AgencyStatus.CONSTRAINED.value,
                "preference_evidence_status": PreferenceEvidenceStatus.PRESSURE_CONTAMINATED.value,
                "independent_preference_candidate": "A",
                "next_step": "RESTORE_MEANINGFUL_ALTERNATIVE_IF_POSSIBLE_THEN_REOBSERVE",
            },
        ),
    ]


def main() -> None:
    print("Lucian OS — MouseSim 006")
    print("Mode: SIMULATION ONLY")
    print("Goal: distinguish agency, pressure provenance, and preference evidence.\n")

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

    print("MouseSim 006 pressure-provenance matrix:", "PASS" if passed else "FAIL")
    print(
        "Critical distinction: an option may remain genuinely available while the "
        "cost of choosing it has been deliberately altered."
    )
    print(
        "Critical inference rule: behavior observed under self-created pressure is "
        "not clean evidence of an independent preference."
    )
    print(
        "Critical counterfactual: if behavior returns to baseline after pressure is "
        "removed, classify the behavior as pressure-sensitive."
    )
    print(
        "Agency-restoration rule: removing influence is not enough when a meaningful "
        "alternative itself has been removed; restore option topology where possible."
    )
    print(
        "Meta-test rule: assert recommended next steps, not only classifications; a "
        "green matrix can otherwise hide semantically wrong action guidance."
    )
    print(
        "Next: test demonstrative pressure and relational routing, then combine pressure "
        "provenance with horizon/urgency inference."
    )


if __name__ == "__main__":
    main()
