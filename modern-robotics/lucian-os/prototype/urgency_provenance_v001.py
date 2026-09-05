"""Lucian OS — urgency provenance v0.01.

Simulation-only candidate model.

Purpose:
- combine horizon evidence with provenance of pressure-shaped behavior;
- prevent system/agent-generated reactions from becoming quantitative physical horizon evidence;
- preserve the case where an intervention actually shortens the physical horizon;
- distinguish external physical urgency from self-caused physical urgency.

This is not a validated control or human-behavior model.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from horizon_evidence_v001 import (
    EvidenceKind,
    HorizonEstimate,
    HorizonEvidence,
    HorizonStatus,
    estimate_horizon,
)


class PhysicalCause(str, Enum):
    EXTERNAL = "EXTERNAL"
    SELF_INTERVENTION = "SELF_INTERVENTION"
    OTHER_AGENT_INTERVENTION = "OTHER_AGENT_INTERVENTION"


class ReactionPressureSource(str, Enum):
    NONE = "NONE"
    WORLD = "WORLD"
    SELF = "SELF"
    OTHER_AGENT = "OTHER_AGENT"
    VICARIOUS_OTHER_AGENT = "VICARIOUS_OTHER_AGENT"


class ReactionEvidenceStatus(str, Enum):
    CLEANER_CONTEXT_SIGNAL = "CLEANER_CONTEXT_SIGNAL"
    WORLD_CONDITIONED = "WORLD_CONDITIONED"
    PRESSURE_CONTAMINATED = "PRESSURE_CONTAMINATED"
    VICARIOUS_PRESSURE_CONTAMINATED = "VICARIOUS_PRESSURE_CONTAMINATED"
    NONE = "NONE"


class UrgencyProvenance(str, Enum):
    EXTERNAL_PHYSICAL = "EXTERNAL_PHYSICAL"
    SELF_CAUSED_PHYSICAL = "SELF_CAUSED_PHYSICAL"
    OTHER_AGENT_CAUSED_PHYSICAL = "OTHER_AGENT_CAUSED_PHYSICAL"
    MIXED_PHYSICAL = "MIXED_PHYSICAL"
    CONTESTED_PHYSICAL = "CONTESTED_PHYSICAL"
    INSUFFICIENT = "INSUFFICIENT"


@dataclass(frozen=True)
class PhysicalChannel:
    evidence: HorizonEvidence
    cause: PhysicalCause


@dataclass(frozen=True)
class ReactionSignal:
    name: str
    observed: bool
    pressure_source: ReactionPressureSource
    description: str


@dataclass(frozen=True)
class UrgencyAssessment:
    horizon: HorizonEstimate
    urgency_provenance: str
    reaction_evidence_statuses: tuple[str, ...]
    reaction_sources: tuple[str, ...]
    reactions_used_to_quantify_horizon: bool
    self_caused_physical_urgency: bool
    interpretation: str


def _reaction_status(signal: ReactionSignal) -> ReactionEvidenceStatus:
    if not signal.observed:
        return ReactionEvidenceStatus.NONE
    if signal.pressure_source == ReactionPressureSource.NONE:
        return ReactionEvidenceStatus.CLEANER_CONTEXT_SIGNAL
    if signal.pressure_source == ReactionPressureSource.WORLD:
        return ReactionEvidenceStatus.WORLD_CONDITIONED
    if signal.pressure_source == ReactionPressureSource.VICARIOUS_OTHER_AGENT:
        return ReactionEvidenceStatus.VICARIOUS_PRESSURE_CONTAMINATED
    return ReactionEvidenceStatus.PRESSURE_CONTAMINATED


def assess_urgency(
    physical_channels: tuple[PhysicalChannel, ...],
    claims: tuple[HorizonEvidence, ...] = (),
    reactions: tuple[ReactionSignal, ...] = (),
) -> UrgencyAssessment:
    """Assess urgency without letting pressure-shaped behavior become a clock."""

    for channel in physical_channels:
        if channel.evidence.kind != EvidenceKind.PHYSICAL:
            raise ValueError("PhysicalChannel must wrap PHYSICAL horizon evidence")
    for claim in claims:
        if claim.kind != EvidenceKind.CLAIM:
            raise ValueError("claims must contain CLAIM horizon evidence")

    horizon = estimate_horizon(
        tuple(channel.evidence for channel in physical_channels) + tuple(claims)
    )

    if horizon.status == HorizonStatus.INSUFFICIENT.value:
        provenance = UrgencyProvenance.INSUFFICIENT
    elif horizon.status == HorizonStatus.CONTESTED.value:
        provenance = UrgencyProvenance.CONTESTED_PHYSICAL
    else:
        causes = {channel.cause for channel in physical_channels}
        if causes == {PhysicalCause.EXTERNAL}:
            provenance = UrgencyProvenance.EXTERNAL_PHYSICAL
        elif causes == {PhysicalCause.SELF_INTERVENTION}:
            provenance = UrgencyProvenance.SELF_CAUSED_PHYSICAL
        elif causes == {PhysicalCause.OTHER_AGENT_INTERVENTION}:
            provenance = UrgencyProvenance.OTHER_AGENT_CAUSED_PHYSICAL
        else:
            provenance = UrgencyProvenance.MIXED_PHYSICAL

    reaction_statuses = tuple(_reaction_status(r).value for r in reactions)
    reaction_sources = tuple(r.pressure_source.value for r in reactions if r.observed)

    self_caused = provenance == UrgencyProvenance.SELF_CAUSED_PHYSICAL

    if self_caused:
        interpretation = (
            "Independent physical relations support a short/finite horizon whose current "
            "cause is the system's own intervention. The urgency is physically real and "
            "must be handled, while causal provenance remains attached for correction and audit."
        )
    elif provenance == UrgencyProvenance.INSUFFICIENT:
        interpretation = (
            "No adequately supported physical horizon is available. Behavioral reactions, "
            "including reactions to pressure, do not manufacture a quantitative clock."
        )
    else:
        interpretation = (
            "Use independent physical horizon relations for timing. Behavioral reactions are "
            "context evidence only and never enter the quantitative horizon in this model."
        )

    return UrgencyAssessment(
        horizon=horizon,
        urgency_provenance=provenance.value,
        reaction_evidence_statuses=reaction_statuses,
        reaction_sources=reaction_sources,
        reactions_used_to_quantify_horizon=False,
        self_caused_physical_urgency=self_caused,
        interpretation=interpretation,
    )
