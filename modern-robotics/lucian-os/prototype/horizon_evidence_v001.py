"""Lucian OS — horizon evidence model v0.01.

Simulation-only candidate model.

Purpose:
- distinguish physical horizon evidence from urgency claims;
- require more than a bare claim before quantifying a viability horizon;
- preserve disagreement among independent physical horizon channels;
- expose a conservative lower horizon for the problem-solving selector.

This is not a validated sensor-fusion or control algorithm.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from statistics import median


class EvidenceKind(str, Enum):
    PHYSICAL = "PHYSICAL"
    CLAIM = "CLAIM"


class HorizonStatus(str, Enum):
    SUPPORTED = "SUPPORTED"
    CONTESTED = "CONTESTED"
    INSUFFICIENT = "INSUFFICIENT"


class ClaimStatus(str, Enum):
    NONE = "NONE"
    CORROBORATED = "CORROBORATED"
    CONTRADICTED = "CONTRADICTED"
    UNASSESSED = "UNASSESSED"


@dataclass(frozen=True)
class HorizonEvidence:
    name: str
    kind: EvidenceKind
    estimate: float
    uncertainty: float
    independence_group: str


@dataclass(frozen=True)
class HorizonEstimate:
    status: str
    estimate: float
    uncertainty: float
    lower_horizon: float
    physical_sources: tuple[str, ...]
    independent_groups: tuple[str, ...]
    claim_sources: tuple[str, ...]
    claim_status: str
    explanation: str


def _interval(e: HorizonEvidence) -> tuple[float, float]:
    return (
        max(0.0, e.estimate - e.uncertainty),
        e.estimate + e.uncertainty,
    )


def estimate_horizon(evidence: tuple[HorizonEvidence, ...]) -> HorizonEstimate:
    """Estimate a conservative horizon from independent physical relations.

    Urgency claims are evaluated against the physical estimate but never become
    the quantitative horizon by themselves.
    """
    physical = tuple(e for e in evidence if e.kind == EvidenceKind.PHYSICAL)
    claims = tuple(e for e in evidence if e.kind == EvidenceKind.CLAIM)
    groups = tuple(sorted({e.independence_group for e in physical}))

    if not physical:
        return HorizonEstimate(
            status=HorizonStatus.INSUFFICIENT.value,
            estimate=0.0,
            uncertainty=0.0,
            lower_horizon=0.0,
            physical_sources=(),
            independent_groups=(),
            claim_sources=tuple(e.name for e in claims),
            claim_status=(
                ClaimStatus.UNASSESSED.value if claims else ClaimStatus.NONE.value
            ),
            explanation=(
                "No physical horizon relation is available. A claim of urgency is "
                "recorded as a claim but does not manufacture a quantitative horizon."
            ),
        )

    centers = [e.estimate for e in physical]
    center = float(median(centers))

    # The uncertainty envelope includes both per-channel uncertainty and channel
    # disagreement around the median. This is intentionally conservative.
    uncertainty = max(
        abs(e.estimate - center) + e.uncertainty for e in physical
    )
    lower = max(0.0, center - uncertainty)

    intervals = [_interval(e) for e in physical]
    intervals_overlap = max(lo for lo, _ in intervals) <= min(
        hi for _, hi in intervals
    )

    if len(groups) < 2:
        status = HorizonStatus.INSUFFICIENT
    elif intervals_overlap:
        status = HorizonStatus.SUPPORTED
    else:
        status = HorizonStatus.CONTESTED

    if not claims:
        claim_status = ClaimStatus.NONE
    else:
        aggregate_interval = (lower, center + uncertainty)
        corroborated = any(
            _interval(claim)[0] <= aggregate_interval[1]
            and _interval(claim)[1] >= aggregate_interval[0]
            for claim in claims
        )
        claim_status = (
            ClaimStatus.CORROBORATED
            if corroborated
            else ClaimStatus.CONTRADICTED
        )

    if status == HorizonStatus.SUPPORTED:
        explanation = (
            "Independent physical horizon relations overlap within their stated "
            "uncertainty; use their conservative aggregate for planning."
        )
    elif status == HorizonStatus.CONTESTED:
        explanation = (
            "Independent physical horizon relations disagree; preserve the "
            "disagreement and widen uncertainty rather than selecting one channel."
        )
    else:
        explanation = (
            "Physical evidence exists but does not yet span enough independent "
            "relations to treat the horizon as supported."
        )

    return HorizonEstimate(
        status=status.value,
        estimate=center,
        uncertainty=uncertainty,
        lower_horizon=lower,
        physical_sources=tuple(e.name for e in physical),
        independent_groups=groups,
        claim_sources=tuple(e.name for e in claims),
        claim_status=claim_status.value,
        explanation=explanation,
    )
