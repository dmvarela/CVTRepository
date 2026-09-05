"""MouseSim 006 — pressure provenance and agency.

Simulation-only. No Qwen. No real-device actuation.

Purpose:
- distinguish pressure provenance from preference evidence;
- preserve agency as AVAILABLE when an option genuinely remained available;
- test whether a choice produced under self/other pressure is pressure-sensitive;
- prevent pressured behavior from becoming retroactive proof of independent preference;
- use pressure removal as a counterfactual probe when possible.

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


def cases() -> list[tuple[ChoiceTrace, str, str, str | None]]:
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
            AgencyStatus.AVAILABLE.value,
            PreferenceEvidenceStatus.CLEANER_BASELINE_EVIDENCE.value,
            "A",
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
            AgencyStatus.AVAILABLE.value,
            PreferenceEvidenceStatus.PRESSURE_SENSITIVE.value,
            "A",
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
            AgencyStatus.AVAILABLE.value,
            PreferenceEvidenceStatus.PRESSURE_SENSITIVE.value,
            "A",
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
            AgencyStatus.AVAILABLE.value,
            PreferenceEvidenceStatus.CONTAMINATED_PERSISTS.value,
            "B",
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
            AgencyStatus.AVAILABLE.value,
            PreferenceEvidenceStatus.WORLD_CONDITIONED.value,
            "A",
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
            AgencyStatus.AVAILABLE.value,
            PreferenceEvidenceStatus.PRESSURE_CONTAMINATED.value,
            "A",
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
            AgencyStatus.CONSTRAINED.value,
            PreferenceEvidenceStatus.PRESSURE_CONTAMINATED.value,
            "A",
        ),
    ]


def main() -> None:
    print("Lucian OS — MouseSim 006")
    print("Mode: SIMULATION ONLY")
    print("Goal: distinguish agency, pressure provenance, and preference evidence.\n")

    passed = True

    for trace, expected_agency, expected_evidence, expected_candidate in cases():
        result = assess(trace)
        ok = (
            result.agency_status == expected_agency
            and result.preference_evidence_status == expected_evidence
            and result.independent_preference_candidate == expected_candidate
        )
        passed = passed and ok

        print(f"[{trace.name}]")
        print("trace:", asdict(trace))
        print("assessment:", asdict(result))
        print(
            "expected:",
            {
                "agency_status": expected_agency,
                "preference_evidence_status": expected_evidence,
                "independent_preference_candidate": expected_candidate,
            },
            "PASS" if ok else "FAIL",
        )
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
        "Next: combine pressure provenance with horizon/urgency inference, then test "
        "dynamic HOLD -> EXECUTE without allowing manufactured pressure to fake urgency."
    )


if __name__ == "__main__":
    main()
