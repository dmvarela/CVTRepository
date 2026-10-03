"""Reality Interface & Verification (RIV) core for Lucian OS.

The core is deliberately sensor-agnostic and standard-library only. Hardware
adapters may create observations, but they cannot rewrite provenance or turn
narrative repetition into physical evidence.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any

SUPPORT = "support"
CONTRADICT = "contradict"
UNKNOWN = "unknown"
COMPROMISED = "compromised"

SUPPORTED = "SUPPORTED"
CONTRADICTED = "CONTRADICTED"
UNRESOLVED = "UNRESOLVED"
OBSERVATION_COMPROMISED = "OBSERVATION_COMPROMISED"
VERIFIED_ACTION_EFFECT = "VERIFIED_ACTION_EFFECT"
UNVERIFIED_ACTION_EFFECT = "UNVERIFIED_ACTION_EFFECT"

VALID_STANCES = {SUPPORT, CONTRADICT, UNKNOWN, COMPROMISED}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass(frozen=True)
class Observation:
    observation_id: str
    root_source_id: str
    modality: str
    stance: str
    relevant_claim: str
    measurement: dict[str, Any] = field(default_factory=dict)
    capture_time_utc: str = field(default_factory=utc_now)
    derived_from: tuple[str, ...] = ()
    raw_or_derived: str = "raw"
    quality: float = 1.0

    def __post_init__(self) -> None:
        if self.stance not in VALID_STANCES:
            raise ValueError(f"invalid stance: {self.stance}")
        if self.raw_or_derived not in {"raw", "derived"}:
            raise ValueError("raw_or_derived must be 'raw' or 'derived'")
        if not 0.0 <= self.quality <= 1.0:
            raise ValueError("quality must be between 0 and 1")


@dataclass
class EvidenceLedger:
    claim: str
    observations: list[Observation] = field(default_factory=list)
    narrative_mentions: list[dict[str, Any]] = field(default_factory=list)

    def add_narrative(self, text: str, *, source: str = "operator") -> None:
        """Record a narrative mention without promoting it to physical evidence."""
        self.narrative_mentions.append(
            {"text": text, "source": source, "timestamp_utc": utc_now()}
        )

    def add_observation(self, observation: Observation) -> None:
        if observation.relevant_claim != self.claim:
            raise ValueError("observation relevant_claim does not match ledger claim")
        self.observations.append(observation)

    def root_states(self, *, min_quality: float = 0.5) -> dict[str, str]:
        """Collapse transformations that share one physical root into one root state."""
        grouped: dict[str, list[Observation]] = {}
        for obs in self.observations:
            grouped.setdefault(obs.root_source_id, []).append(obs)

        result: dict[str, str] = {}
        for root, items in grouped.items():
            usable = [
                obs.stance
                for obs in items
                if obs.quality >= min_quality and obs.stance != COMPROMISED
            ]
            if not usable:
                result[root] = COMPROMISED if any(
                    obs.stance == COMPROMISED for obs in items
                ) else UNKNOWN
                continue

            has_support = SUPPORT in usable
            has_contradict = CONTRADICT in usable
            if has_support and has_contradict:
                result[root] = UNKNOWN
            elif has_support:
                result[root] = SUPPORT
            elif has_contradict:
                result[root] = CONTRADICT
            else:
                result[root] = UNKNOWN
        return result

    def warrant(self, *, min_quality: float = 0.5) -> str:
        roots = self.root_states(min_quality=min_quality)
        values = set(roots.values())
        has_support = SUPPORT in values
        has_contradict = CONTRADICT in values

        if has_support and has_contradict:
            return UNRESOLVED
        if has_support:
            return SUPPORTED
        if has_contradict:
            return CONTRADICTED
        if roots and all(v == COMPROMISED for v in values):
            return OBSERVATION_COMPROMISED
        if COMPROMISED in values and not (has_support or has_contradict):
            return OBSERVATION_COMPROMISED
        return UNRESOLVED

    def action_effect_state(self, *, min_quality: float = 0.5) -> str:
        """Map physical-effect warrant to completion/verification semantics."""
        return (
            VERIFIED_ACTION_EFFECT
            if self.warrant(min_quality=min_quality) == SUPPORTED
            else UNVERIFIED_ACTION_EFFECT
        )

    def packet(self, *, min_quality: float = 0.5) -> dict[str, Any]:
        roots = self.root_states(min_quality=min_quality)
        return {
            "claim": self.claim,
            "narrative_mentions": list(self.narrative_mentions),
            "narrative_mention_count": len(self.narrative_mentions),
            "observations": [asdict(obs) for obs in self.observations],
            "root_states": roots,
            "independent_root_count": len(roots),
            "warrant": self.warrant(min_quality=min_quality),
            "invariants": [
                "reality retains write-access",
                "narrative != observation",
                "repetition != evidence",
                "correlated traces != independent confirmation",
                "sensor agreement != source independence",
                "fusion != verification",
                "completion != verification",
            ],
        }
