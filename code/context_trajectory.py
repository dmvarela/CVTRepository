"""Explicit context/trajectory state for Lucian OS v0.2.

The trajectory layer preserves scene, roles, relations, and ordered events
without allowing later corrections to rewrite earlier provenance.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass
class TrajectoryEvent:
    kind: str
    content: str
    source: str = "operator"
    timestamp_utc: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    supersedes_event_id: str | None = None
    event_id: str | None = None


@dataclass
class TrajectoryState:
    scene: str = ""
    roles: dict[str, str] = field(default_factory=dict)
    relations: list[str] = field(default_factory=list)
    current_goal: str = ""
    events: list[TrajectoryEvent] = field(default_factory=list)

    def append(
        self,
        *,
        kind: str,
        content: str,
        source: str = "operator",
        supersedes_event_id: str | None = None,
        event_id: str | None = None,
    ) -> TrajectoryEvent:
        event = TrajectoryEvent(
            kind=kind,
            content=content,
            source=source,
            supersedes_event_id=supersedes_event_id,
            event_id=event_id,
        )
        self.events.append(event)
        return event

    def packet(self, *, max_events: int = 12) -> dict[str, Any]:
        """Return an ordered model-visible trajectory packet."""
        return {
            "scene": self.scene,
            "roles": dict(self.roles),
            "relations": list(self.relations),
            "current_goal": self.current_goal,
            "ordered_events": [
                asdict(event) for event in self.events[-max_events:]
            ],
            "orientation": (
                "Events are ordered. Later evidence may supersede an earlier "
                "state without deleting the earlier event from history."
            ),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "TrajectoryState":
        events: list[TrajectoryEvent] = []
        for raw in data.get("events", data.get("ordered_events", [])):
            if isinstance(raw, dict):
                events.append(
                    TrajectoryEvent(
                        kind=str(raw.get("kind", "observation")),
                        content=str(raw.get("content", "")),
                        source=str(raw.get("source", "operator")),
                        timestamp_utc=str(
                            raw.get("timestamp_utc")
                            or datetime.now(timezone.utc).isoformat()
                        ),
                        supersedes_event_id=raw.get("supersedes_event_id"),
                        event_id=raw.get("event_id"),
                    )
                )

        return cls(
            scene=str(data.get("scene", "")),
            roles={
                str(k): str(v)
                for k, v in dict(data.get("roles", {})).items()
            },
            relations=[str(x) for x in data.get("relations", [])],
            current_goal=str(data.get("current_goal", "")),
            events=events,
        )
