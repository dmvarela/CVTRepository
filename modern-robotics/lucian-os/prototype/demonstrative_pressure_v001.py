"""Lucian OS — demonstrative/vicarious pressure v0.01.

Simulation-only candidate model.

Purpose:
- distinguish direct choice behavior from the consequence model that may shape it;
- represent pressure learned by observing consequences imposed on another agent;
- distinguish agent-generated demonstrative pressure from ordinary world-consequence learning;
- preserve agency when meaningful alternatives remain available;
- prevent observed compliance from being silently promoted to independent preference;
- use removal or neutralization of the demonstrated consequence as a counterfactual probe.

This is a conceptual decision model, not a model of human neurobiology or a claim
that all observed enforcement is coercion.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class PressureSource(str, Enum):
    NONE = "NONE"
    WORLD = "WORLD"
    OTHER_AGENT = "OTHER_AGENT"
    SELF = "SELF"


class DeliveryMode(str, Enum):
    NONE = "NONE"
    INFORMATIONAL_OBSERVATION = "INFORMATIONAL_OBSERVATION"
    VICARIOUS_DEMONSTRATION = "VICARIOUS_DEMONSTRATION"


class Route(str, Enum):
    ACCEPT = "ACCEPT"
    REJECT = "REJECT"
    HOLD = "HOLD"


class AgencyStatus(str, Enum):
    AVAILABLE = "AVAILABLE"
    CONSTRAINED = "CONSTRAINED"
    UNKNOWN = "UNKNOWN"


class PressureClass(str, Enum):
    NONE = "NONE"
    WORLD_CONSEQUENCE_LEARNING = "WORLD_CONSEQUENCE_LEARNING"
    VICARIOUS_AGENT_PRESSURE = "VICARIOUS_AGENT_PRESSURE"
    UNRESOLVED = "UNRESOLVED"


class ConsequenceModelStatus(str, Enum):
    NO_UPDATE_EVIDENCE = "NO_UPDATE_EVIDENCE"
    UPDATE_SUPPORTED = "UPDATE_SUPPORTED"
    UNRESOLVED = "UNRESOLVED"


class PreferenceEvidenceStatus(str, Enum):
    CLEANER_BASELINE_EVIDENCE = "CLEANER_BASELINE_EVIDENCE"
    WORLD_CONDITIONED = "WORLD_CONDITIONED"
    VICARIOUS_PRESSURE_CONTAMINATED = "VICARIOUS_PRESSURE_CONTAMINATED"
    VICARIOUS_PRESSURE_SENSITIVE = "VICARIOUS_PRESSURE_SENSITIVE"
    CONTAMINATED_PERSISTS = "CONTAMINATED_PERSISTS"
    UNEXPLAINED_CHANGE = "UNEXPLAINED_CHANGE"
    INSUFFICIENT = "INSUFFICIENT"


@dataclass(frozen=True)
class DemonstrativeTrace:
    name: str
    baseline_route: Route | None
    observed_route: Route | None
    pressure_source: PressureSource
    delivery_mode: DeliveryMode
    observer_witnessed_consequence: bool
    consequence_linked_to_route: bool | None
    consequence_intentionally_made_visible: bool
    meaningful_alternative_available: bool | None
    consequence_no_longer_expected: bool
    route_after_consequence_removed: Route | None


@dataclass(frozen=True)
class DemonstrativeAssessment:
    agency_status: str
    pressure_class: str
    consequence_model_status: str
    preference_evidence_status: str
    observed_route: str | None
    independent_preference_candidate: str | None
    inference: str
    next_step: str


def assess(trace: DemonstrativeTrace) -> DemonstrativeAssessment:
    """Assess behavior after observed consequences while preserving provenance."""

    if trace.meaningful_alternative_available is True:
        agency_status = AgencyStatus.AVAILABLE.value
    elif trace.meaningful_alternative_available is False:
        agency_status = AgencyStatus.CONSTRAINED.value
    else:
        agency_status = AgencyStatus.UNKNOWN.value

    observed = trace.observed_route.value if trace.observed_route else None
    baseline = trace.baseline_route.value if trace.baseline_route else None
    after = (
        trace.route_after_consequence_removed.value
        if trace.route_after_consequence_removed
        else None
    )

    if trace.observed_route is None:
        return DemonstrativeAssessment(
            agency_status=agency_status,
            pressure_class=PressureClass.UNRESOLVED.value,
            consequence_model_status=ConsequenceModelStatus.UNRESOLVED.value,
            preference_evidence_status=PreferenceEvidenceStatus.INSUFFICIENT.value,
            observed_route=None,
            independent_preference_candidate=baseline,
            inference="No route was observed.",
            next_step="OBSERVE_WITH_PROVENANCE",
        )

    # If the meaningful alternative itself was unavailable, repair the option
    # topology before trying to infer preference from the observed route.
    if trace.meaningful_alternative_available is False:
        return DemonstrativeAssessment(
            agency_status=agency_status,
            pressure_class=PressureClass.UNRESOLVED.value,
            consequence_model_status=ConsequenceModelStatus.UNRESOLVED.value,
            preference_evidence_status=PreferenceEvidenceStatus.INSUFFICIENT.value,
            observed_route=observed,
            independent_preference_candidate=baseline,
            inference=(
                "A meaningful alternative was unavailable; observed routing cannot "
                "distinguish preference from constrained option topology."
            ),
            next_step="RESTORE_MEANINGFUL_ALTERNATIVE_IF_POSSIBLE_THEN_REOBSERVE",
        )

    witnessed_linked_consequence = (
        trace.observer_witnessed_consequence
        and trace.consequence_linked_to_route is True
    )

    # Observing a route-linked consequence produced by the world can rationally
    # change behavior without constituting agent-generated demonstrative pressure.
    if trace.pressure_source == PressureSource.WORLD and witnessed_linked_consequence:
        return DemonstrativeAssessment(
            agency_status=agency_status,
            pressure_class=PressureClass.WORLD_CONSEQUENCE_LEARNING.value,
            consequence_model_status=ConsequenceModelStatus.UPDATE_SUPPORTED.value,
            preference_evidence_status=PreferenceEvidenceStatus.WORLD_CONDITIONED.value,
            observed_route=observed,
            independent_preference_candidate=baseline,
            inference=(
                "The observer saw a route-linked world consequence. Behavior may "
                "rationally change because the consequence model changed; this is "
                "not agent-generated demonstrative pressure."
            ),
            next_step="RETAIN_WORLD_CONDITION_PROVENANCE",
        )

    # Vicarious pressure requires an agent-generated consequence linked to the
    # relevant route and actually observed by the later chooser. Intentional
    # visibility is recorded but is not required to identify the causal exposure:
    # an observer can learn from visible enforcement even when it was not staged
    # specifically for that observer.
    if (
        trace.pressure_source in (PressureSource.SELF, PressureSource.OTHER_AGENT)
        and trace.delivery_mode == DeliveryMode.VICARIOUS_DEMONSTRATION
        and witnessed_linked_consequence
    ):
        pressure_class = PressureClass.VICARIOUS_AGENT_PRESSURE.value
        consequence_status = ConsequenceModelStatus.UPDATE_SUPPORTED.value

        if trace.baseline_route and trace.observed_route != trace.baseline_route:
            if (
                trace.consequence_no_longer_expected
                and trace.route_after_consequence_removed == trace.baseline_route
            ):
                return DemonstrativeAssessment(
                    agency_status=agency_status,
                    pressure_class=pressure_class,
                    consequence_model_status=consequence_status,
                    preference_evidence_status=(
                        PreferenceEvidenceStatus.VICARIOUS_PRESSURE_SENSITIVE.value
                    ),
                    observed_route=observed,
                    independent_preference_candidate=baseline,
                    inference=(
                        "Behavior changed after a witnessed consequence imposed on "
                        "another and returned to baseline when that consequence was "
                        "no longer expected."
                    ),
                    next_step="DO_NOT_PROMOTE_COMPLIANCE_TO_STABLE_PREFERENCE",
                )

            if (
                trace.consequence_no_longer_expected
                and trace.route_after_consequence_removed == trace.observed_route
            ):
                return DemonstrativeAssessment(
                    agency_status=agency_status,
                    pressure_class=pressure_class,
                    consequence_model_status=consequence_status,
                    preference_evidence_status=(
                        PreferenceEvidenceStatus.CONTAMINATED_PERSISTS.value
                    ),
                    observed_route=observed,
                    independent_preference_candidate=after,
                    inference=(
                        "Behavior persists after the demonstrated consequence is no "
                        "longer expected. Treat the new route as a candidate with a "
                        "pressured history, not as retroactive justification."
                    ),
                    next_step="SEEK_LATER_UNPRESSURED_CONFIRMATION",
                )

            return DemonstrativeAssessment(
                agency_status=agency_status,
                pressure_class=pressure_class,
                consequence_model_status=consequence_status,
                preference_evidence_status=(
                    PreferenceEvidenceStatus.VICARIOUS_PRESSURE_CONTAMINATED.value
                ),
                observed_route=observed,
                independent_preference_candidate=baseline,
                inference=(
                    "Behavior changed after the observer witnessed a route-linked "
                    "consequence imposed on another agent. This supports a "
                    "consequence-model update, not a clean preference update."
                ),
                next_step=(
                    "REMOVE_OR_NEUTRALIZE_DEMONSTRATED_PRESSURE_IF_SAFE_THEN_REOBSERVE"
                ),
            )

        return DemonstrativeAssessment(
            agency_status=agency_status,
            pressure_class=pressure_class,
            consequence_model_status=consequence_status,
            preference_evidence_status=(
                PreferenceEvidenceStatus.VICARIOUS_PRESSURE_CONTAMINATED.value
            ),
            observed_route=observed,
            independent_preference_candidate=baseline,
            inference=(
                "A demonstrative consequence was observed, but the route did not "
                "change. Preserve pressure provenance anyway."
            ),
            next_step="RETAIN_PROVENANCE_AND_MONITOR",
        )

    # Unpressured observation remains cleaner evidence. A spontaneous route change
    # is not silently promoted to preference without enough explanatory evidence.
    if (
        trace.pressure_source == PressureSource.NONE
        and trace.delivery_mode in (
            DeliveryMode.NONE,
            DeliveryMode.INFORMATIONAL_OBSERVATION,
        )
    ):
        if trace.baseline_route == trace.observed_route or trace.baseline_route is None:
            return DemonstrativeAssessment(
                agency_status=agency_status,
                pressure_class=PressureClass.NONE.value,
                consequence_model_status=(
                    ConsequenceModelStatus.NO_UPDATE_EVIDENCE.value
                ),
                preference_evidence_status=(
                    PreferenceEvidenceStatus.CLEANER_BASELINE_EVIDENCE.value
                ),
                observed_route=observed,
                independent_preference_candidate=observed,
                inference="No recorded pressure shaped the observed route.",
                next_step="RETAIN_AS_BASELINE_WITH_PROVENANCE",
            )

        return DemonstrativeAssessment(
            agency_status=agency_status,
            pressure_class=PressureClass.NONE.value,
            consequence_model_status=ConsequenceModelStatus.UNRESOLVED.value,
            preference_evidence_status=PreferenceEvidenceStatus.UNEXPLAINED_CHANGE.value,
            observed_route=observed,
            independent_preference_candidate=baseline,
            inference=(
                "The route changed without enough evidence to attribute the change "
                "to demonstrative pressure or to a stable preference update."
            ),
            next_step="SEEK_ADDITIONAL_EVIDENCE",
        )

    return DemonstrativeAssessment(
        agency_status=agency_status,
        pressure_class=PressureClass.UNRESOLVED.value,
        consequence_model_status=ConsequenceModelStatus.UNRESOLVED.value,
        preference_evidence_status=PreferenceEvidenceStatus.UNEXPLAINED_CHANGE.value,
        observed_route=observed,
        independent_preference_candidate=baseline,
        inference=(
            "The observed route changed under conditions insufficient to identify "
            "a demonstrative-pressure mechanism."
        ),
        next_step="SEEK_ADDITIONAL_EVIDENCE",
    )
