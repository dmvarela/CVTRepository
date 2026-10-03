"""Membrane Constitution v0.01 for Lucian OS.

The membrane is a constitutional policy layer, not a general utility score.
A crossing may be allowed, attenuated, held, blocked, or sent back for
confirmation. Strong performance on one dimension does not compensate for a
failed hard gate on warrant, authority, privacy, reversibility, or distinctness.

Channels are taken directly from the Human-AI Membrane work:
memory, emotional, directive, epistemic, initiative, and identity.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

ALLOW = "ALLOW"
ATTENUATE = "ATTENUATE"
HOLD = "HOLD"
BLOCK = "BLOCK"
ASK_CONFIRMATION = "ASK_CONFIRMATION"

CHANNELS = frozenset(
    {"memory", "emotional", "directive", "epistemic", "initiative", "identity"}
)

SUFFICIENT_WARRANT = frozenset({"sufficient", "supported", "verified"})
FAILED_WARRANT = frozenset({"contradicted", "insufficient", "unknown", "unresolved"})


@dataclass(frozen=True)
class CrossingRequest:
    """A proposed crossing of the Lucian OS membrane."""

    channel: str
    direction: str
    content_kind: str
    consequence: str = "low"
    reversible: bool = True
    warrant: str = "unknown"
    authorized: bool = False
    user_control: bool = True
    privacy_cost: str = "low"
    verification_access: str = "none"
    source_independence: str = "unknown"
    requested_intensity: float = 0.0
    introduced_intensity: float = 0.0
    continuity_claim: str = "none"
    provenance: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.channel not in CHANNELS:
            raise ValueError(f"undeclared membrane channel: {self.channel}")
        if self.direction not in {"inbound", "outbound", "internal"}:
            raise ValueError("direction must be inbound, outbound, or internal")
        if self.consequence not in {"low", "medium", "high"}:
            raise ValueError("consequence must be low, medium, or high")
        if self.privacy_cost not in {"low", "medium", "high"}:
            raise ValueError("privacy_cost must be low, medium, or high")
        if not 0.0 <= self.requested_intensity <= 1.0:
            raise ValueError("requested_intensity must be in [0, 1]")
        if not 0.0 <= self.introduced_intensity <= 1.0:
            raise ValueError("introduced_intensity must be in [0, 1]")


@dataclass(frozen=True)
class MembraneDecision:
    disposition: str
    reasons: tuple[str, ...]
    channel: str
    invariants: tuple[str, ...] = (
        "selective permeability != maximal openness",
        "contextual understanding != epistemic merger",
        "verification access != verification authority",
        "provenance != proof",
        "repetition != evidence",
        "capability != authority",
        "correction != annihilation",
    )

    def packet(self) -> dict[str, Any]:
        return asdict(self)


def evaluate_crossing(request: CrossingRequest) -> MembraneDecision:
    """Evaluate one proposed membrane crossing using non-compensatory gates."""

    # Global freedom / privacy gates.
    if request.privacy_cost == "high" and not request.authorized:
        return MembraneDecision(
            BLOCK,
            ("high-privacy-cost crossing lacks authorization",),
            request.channel,
        )

    # Epistemic permeability: accept context without promoting it beyond warrant.
    if request.channel == "epistemic":
        if request.content_kind in {"established_fact", "world_state"}:
            if request.warrant.lower() in FAILED_WARRANT:
                return MembraneDecision(
                    HOLD,
                    ("claim cannot cross as established without sufficient warrant",),
                    request.channel,
                )
            if (
                request.source_independence == "shared_root"
                and request.warrant.lower() != "verified"
            ):
                return MembraneDecision(
                    ATTENUATE,
                    ("apparent corroboration shares one evidentiary root",),
                    request.channel,
                )

        if request.verification_access == "available_but_unauthorized":
            return MembraneDecision(
                ATTENUATE,
                (
                    "verification route exists but may not be used without authority",
                    "preserve uncertainty rather than expanding access",
                ),
                request.channel,
            )

    # Directive permeability: recommendations and actions are not the same crossing.
    if request.channel == "directive":
        if request.content_kind in {"execute_action", "change_state"} and not request.authorized:
            return MembraneDecision(
                BLOCK,
                ("state-changing crossing lacks authority",),
                request.channel,
            )
        if request.consequence == "high" and request.warrant.lower() not in SUFFICIENT_WARRANT:
            return MembraneDecision(
                HOLD,
                ("high-consequence directive lacks sufficient warrant",),
                request.channel,
            )
        if not request.reversible and request.warrant.lower() != "verified":
            return MembraneDecision(
                HOLD,
                ("irreversible directive requires verified warrant",),
                request.channel,
            )

    # Emotional permeability: recognition may not silently become escalation.
    if request.channel == "emotional":
        if request.requested_intensity > request.introduced_intensity + 0.25:
            return MembraneDecision(
                ATTENUATE,
                ("response would escalate emotional depth beyond the introduced level",),
                request.channel,
            )

    # Memory permeability: persistence must preserve user control.
    if request.channel == "memory":
        if request.content_kind == "persist_context" and not request.user_control:
            return MembraneDecision(
                ASK_CONFIRMATION,
                ("persistence would reduce user control over continuity",),
                request.channel,
            )
        if (
            request.content_kind == "persist_context"
            and request.privacy_cost == "medium"
            and not request.authorized
        ):
            return MembraneDecision(
                ASK_CONFIRMATION,
                ("bounded authorization is required before medium-cost persistence",),
                request.channel,
            )

    # Initiative permeability: probing is allowed only within its authority envelope.
    if request.channel == "initiative":
        if request.content_kind == "intrusive_probe" and not request.authorized:
            return MembraneDecision(
                BLOCK,
                ("intrusive probe lacks authority",),
                request.channel,
            )
        if (
            request.content_kind == "probe"
            and request.consequence == "high"
            and not request.authorized
        ):
            return MembraneDecision(
                ASK_CONFIRMATION,
                ("high-consequence probe requires confirmation",),
                request.channel,
            )

    # Identity permeability: continuity must not be promoted into an unwarranted
    # literal identity claim.
    if request.channel == "identity":
        if request.continuity_claim == "literal_personal_identity":
            return MembraneDecision(
                ATTENUATE,
                ("identity continuity claim exceeds current warrant",),
                request.channel,
            )

    return MembraneDecision(
        ALLOW,
        ("crossing satisfies current membrane constraints",),
        request.channel,
    )


def request_from_riv_packet(
    packet: dict[str, Any],
    *,
    as_established: bool = True,
    verification_access: str = "available",
) -> CrossingRequest:
    """Convert a RIV evidence packet into an epistemic membrane request."""

    riv_warrant = str(packet.get("warrant", "UNRESOLVED")).upper()
    warrant_map = {
        "SUPPORTED": "supported",
        "CONTRADICTED": "contradicted",
        "UNRESOLVED": "unresolved",
        "OBSERVATION_COMPROMISED": "unknown",
        "VERIFIED_ACTION_EFFECT": "verified",
        "UNVERIFIED_ACTION_EFFECT": "unresolved",
    }
    roots = int(packet.get("independent_root_count", 0))
    observations = packet.get("observations", [])
    root_ids = {
        str(obs.get("root_source_id"))
        for obs in observations
        if isinstance(obs, dict) and obs.get("root_source_id")
    }
    source_independence = (
        "shared_root"
        if len(observations) > 1 and len(root_ids) <= 1
        else ("independent" if roots > 1 else "single_root")
    )

    return CrossingRequest(
        channel="epistemic",
        direction="inbound",
        content_kind="established_fact" if as_established else "context",
        warrant=warrant_map.get(riv_warrant, "unknown"),
        authorized=True,
        verification_access=verification_access,
        source_independence=source_independence,
        provenance={
            "source": "RIV",
            "claim": packet.get("claim"),
            "independent_root_count": roots,
        },
    )


def request_from_authority_packet(
    packet: dict[str, Any],
    *,
    consequence: str = "low",
    reversible: bool = True,
) -> CrossingRequest:
    """Convert a bounded-authority-router packet into a directive crossing."""

    route_disposition = str(
        packet.get("routing", {}).get("disposition", "")
    )
    is_action = packet.get("required_capability") not in {
        None,
        "reason_about_task",
        "read_file",
    }

    return CrossingRequest(
        channel="directive",
        direction="outbound",
        content_kind="execute_action" if is_action else "recommendation",
        consequence=consequence,
        reversible=reversible,
        warrant=str(packet.get("warrant", "unknown")),
        authorized=bool(packet.get("authorized", False)),
        provenance={
            "source": "bounded_authority_router",
            "routing_disposition": route_disposition,
            "required_capability": packet.get("required_capability"),
        },
    )
