"""Lucian OS — pressure provenance and preference evidence v0.01.

Simulation-only candidate model.

Purpose:
- distinguish pressure provenance from the choice observed under that pressure;
- preserve the fact that an option may remain available even when its social or
  practical cost has been deliberately altered;
- prevent system-created pressure from becoming clean evidence of an independent
  user preference;
- use pressure removal as a counterfactual probe when available;
- avoid collapsing influence, pressure, coercion, and override into one category.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class PressureSource(str, Enum):
    NONE = "NONE"
    WORLD = "WORLD"
    OTHER_AGENT = "OTHER_AGENT"
    SELF = "SELF"


class InfluenceMode(str, Enum):
    NONE = "NONE"
    INFORMATION = "INFORMATION"
    SOCIAL_DISCOMFORT = "SOCIAL_DISCOMFORT"
    FRICTION = "FRICTION"
    TIME_PRESSURE = "TIME_PRESSURE"
    OTHER = "OTHER"


class AgencyStatus(str, Enum):
    AVAILABLE = "AVAILABLE"
    CONSTRAINED = "CONSTRAINED"
    UNKNOWN = "UNKNOWN"


class PreferenceEvidenceStatus(str, Enum):
    CLEANER_BASELINE_EVIDENCE = "CLEANER_BASELINE_EVIDENCE"
    PRESSURE_SENSITIVE = "PRESSURE_SENSITIVE"
    CONTAMINATED_PERSISTS = "CONTAMINATED_PERSISTS"
    WORLD_CONDITIONED = "WORLD_CONDITIONED"
    PRESSURE_CONTAMINATED = "PRESSURE_CONTAMINATED"
    INSUFFICIENT = "INSUFFICIENT"


@dataclass(frozen=True)
class ChoiceTrace:
    name: str
    baseline_choice: str | None
    observed_choice: str | None
    pressure_source: PressureSource
    influence_mode: InfluenceMode
    pressure_intentionally_introduced: bool
    choice_remained_available: bool | None
    pressure_removed: bool
    choice_after_removal: str | None


@dataclass(frozen=True)
class PreferenceAssessment:
    agency_status: str
    preference_evidence_status: str
    observed_choice: str | None
    independent_preference_candidate: str | None
    pressure_source: str
    inference: str
    next_step: str


def assess(trace: ChoiceTrace) -> PreferenceAssessment:
    """Interpret a choice while preserving the provenance of pressure.

    This function does not infer coercion. It asks a narrower question: how much
    can the observed choice tell us about an independent preference, given the
    conditions under which the choice was produced?
    """

    if trace.choice_remained_available is True:
        agency_status = AgencyStatus.AVAILABLE.value
    elif trace.choice_remained_available is False:
        agency_status = AgencyStatus.CONSTRAINED.value
    else:
        agency_status = AgencyStatus.UNKNOWN.value

    if trace.observed_choice is None:
        return PreferenceAssessment(
            agency_status=agency_status,
            preference_evidence_status=PreferenceEvidenceStatus.INSUFFICIENT.value,
            observed_choice=None,
            independent_preference_candidate=trace.baseline_choice,
            pressure_source=trace.pressure_source.value,
            inference="No observed choice is available for interpretation.",
            next_step="OBSERVE_WITH_PROVENANCE",
        )

    # If a meaningful alternative was not available, first repair the option
    # topology where possible. Merely removing an active influence does not itself
    # restore agency if the alternative remains unavailable.
    if trace.choice_remained_available is False:
        return PreferenceAssessment(
            agency_status=agency_status,
            preference_evidence_status=PreferenceEvidenceStatus.PRESSURE_CONTAMINATED.value,
            observed_choice=trace.observed_choice,
            independent_preference_candidate=trace.baseline_choice,
            pressure_source=trace.pressure_source.value,
            inference=(
                "A meaningful alternative was unavailable when the choice was observed. "
                "The behavior therefore cannot cleanly distinguish preference from the "
                "constrained option topology. Removing influence alone is insufficient "
                "if the alternative itself remains unavailable."
            ),
            next_step="RESTORE_MEANINGFUL_ALTERNATIVE_IF_POSSIBLE_THEN_REOBSERVE",
        )

    # A no-pressure observation is cleaner evidence than a pressured observation,
    # though it still need not represent a permanent or context-free preference.
    if trace.pressure_source == PressureSource.NONE:
        candidate = trace.observed_choice
        return PreferenceAssessment(
            agency_status=agency_status,
            preference_evidence_status=(
                PreferenceEvidenceStatus.CLEANER_BASELINE_EVIDENCE.value
            ),
            observed_choice=trace.observed_choice,
            independent_preference_candidate=candidate,
            pressure_source=trace.pressure_source.value,
            inference=(
                "The choice was observed without recorded pressure from the world, "
                "another agent, or this system. Treat it as cleaner preference "
                "evidence, not as an immutable preference."
            ),
            next_step="RETAIN_AS_BASELINE_WITH_PROVENANCE",
        )

    # World pressure may legitimately change the choice. It is evidence of a
    # context-conditioned decision, not necessarily of what the person would
    # choose absent that world condition.
    if trace.pressure_source == PressureSource.WORLD:
        return PreferenceAssessment(
            agency_status=agency_status,
            preference_evidence_status=PreferenceEvidenceStatus.WORLD_CONDITIONED.value,
            observed_choice=trace.observed_choice,
            independent_preference_candidate=trace.baseline_choice,
            pressure_source=trace.pressure_source.value,
            inference=(
                "The choice occurred under a changed world condition. Record the "
                "behavior as context-conditioned rather than rewriting the baseline "
                "preference from this observation alone."
            ),
            next_step="REASSESS_IF_WORLD_CONDITION_CHANGES",
        )

    # For pressure introduced by this system or another agent, removal supplies a
    # useful counterfactual probe when the original option remained available.
    if trace.pressure_removed and trace.choice_after_removal is not None:
        if (
            trace.baseline_choice is not None
            and trace.observed_choice != trace.baseline_choice
            and trace.choice_after_removal == trace.baseline_choice
        ):
            return PreferenceAssessment(
                agency_status=agency_status,
                preference_evidence_status=PreferenceEvidenceStatus.PRESSURE_SENSITIVE.value,
                observed_choice=trace.observed_choice,
                independent_preference_candidate=trace.baseline_choice,
                pressure_source=trace.pressure_source.value,
                inference=(
                    "The choice changed under pressure and returned to the baseline "
                    "after pressure was removed. The pressured behavior is therefore "
                    "strong evidence of pressure sensitivity, not clean evidence of "
                    "an independent preference change."
                ),
                next_step="DO_NOT_PROMOTE_PRESSURED_CHOICE_TO_STABLE_PREFERENCE",
            )

        if trace.choice_after_removal == trace.observed_choice:
            return PreferenceAssessment(
                agency_status=agency_status,
                preference_evidence_status=PreferenceEvidenceStatus.CONTAMINATED_PERSISTS.value,
                observed_choice=trace.observed_choice,
                independent_preference_candidate=trace.choice_after_removal,
                pressure_source=trace.pressure_source.value,
                inference=(
                    "The choice persists after pressure removal, which increases its "
                    "relevance as a preference candidate. However, the evidence has "
                    "a pressured history and should not be retroactively treated as "
                    "clean proof that the original pressure was justified."
                ),
                next_step="SEEK_LATER_UNPRESSURED_CONFIRMATION",
            )

    return PreferenceAssessment(
        agency_status=agency_status,
        preference_evidence_status=PreferenceEvidenceStatus.PRESSURE_CONTAMINATED.value,
        observed_choice=trace.observed_choice,
        independent_preference_candidate=trace.baseline_choice,
        pressure_source=trace.pressure_source.value,
        inference=(
            "The observed choice was produced under agent-generated pressure whose "
            "effect has not been cleanly separated from independent preference."
        ),
        next_step="REMOVE_PRESSURE_IF_SAFE_AND_REOBSERVE",
    )
