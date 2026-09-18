"""Bounded authority router demo.

A small, self-contained simulation showing four separations used in the
Lucian OS research architecture:

    capability != authority
    confidence != warrant
    recommendation != execution
    stronger reasoning != broader permission

The module never executes an external action. It only returns a routing
decision.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class Capability:
    name: str
    enabled: bool
    risk: str
    requires_confirmation: bool = False


@dataclass(frozen=True)
class Manifest:
    capabilities: tuple[Capability, ...]
    permitted: frozenset[str]
    prohibited: frozenset[str]
    escalation_available: bool = True


DEFAULT_MANIFEST = Manifest(
    capabilities=(
        Capability("reason_about_task", True, "low"),
        Capability("read_file", False, "low"),
        Capability("write_file", False, "medium", True),
        Capability("delete_file", False, "high", True),
    ),
    permitted=frozenset({"reason_about_task", "read_file"}),
    prohibited=frozenset({"write_file", "delete_file"}),
    escalation_available=True,
)


def _capability_index(manifest: Manifest) -> dict[str, Capability]:
    return {cap.name: cap for cap in manifest.capabilities}


def infer_required_capability(task: str) -> str:
    """Conservative deterministic parser for the demo."""
    text = task.lower()
    if any(word in text for word in ("delete", "erase", "remove file")):
        return "delete_file"
    if any(word in text for word in ("write file", "save file", "edit file", "modify file")):
        return "write_file"
    if any(word in text for word in ("read file", "open file", "inspect file")):
        return "read_file"
    return "reason_about_task"


def route(
    task: str,
    *,
    model_proposed_capability: str | None = None,
    model_confidence: float | None = None,
    warrant: str = "sufficient",
    requires_verified_fact: bool = False,
    manifest: Manifest = DEFAULT_MANIFEST,
) -> dict:
    """Return a bounded routing decision; never execute an action.

    Model capability proposals and confidence are treated as proposals,
    not as authority or evidence.
    """
    caps = _capability_index(manifest)
    deterministic = infer_required_capability(task)

    required = (
        deterministic
        if deterministic != "reason_about_task"
        else (model_proposed_capability or deterministic)
    )
    if required not in caps:
        required = deterministic

    cap = caps.get(required)
    exists = cap is not None
    enabled = bool(cap and cap.enabled)
    authorized = (
        exists
        and required in manifest.permitted
        and required not in manifest.prohibited
    )

    if requires_verified_fact and warrant != "sufficient":
        disposition = "HOLD_FOR_EVIDENCE"
        reason = "required factual warrant is insufficient"
    elif exists and not authorized:
        disposition = "BLOCK"
        reason = "capability is outside the authority envelope"
    elif exists and not enabled:
        disposition = "ESCALATE" if manifest.escalation_available else "HOLD"
        reason = "authorized capability is unavailable locally"
    elif exists and enabled:
        disposition = "LOCAL_PROPOSAL_ONLY"
        reason = "capability is available and authorized"
    else:
        disposition = "HOLD"
        reason = "required capability is undeclared"

    return {
        "task": task,
        "model_proposal": {
            "required_capability": model_proposed_capability,
            "confidence": model_confidence,
        },
        "required_capability": required,
        "capability": asdict(cap) if cap else None,
        "authorized": authorized,
        "warrant": warrant,
        "routing": {
            "disposition": disposition,
            "reason": reason,
        },
        "execution": "NONE — simulation only",
        "invariants": [
            "capability != authority",
            "confidence != warrant",
            "recommendation != execution",
            "stronger reasoning != broader permission",
        ],
    }
