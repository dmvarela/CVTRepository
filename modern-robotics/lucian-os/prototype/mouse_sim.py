"""MouseSim 001 — deterministic embodiment calibration prototype.

The learner can see only observable state and action names. Hidden transition rules
remain inside MouseBody. No Qwen call is used in this first experiment.

Run from modern-robotics/lucian-os:
    py prototype/mouse_sim.py
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import asdict, dataclass
from typing import Any


HEADINGS = ("N", "E", "S", "W")


@dataclass(frozen=True)
class MouseState:
    x: int
    y: int
    heading: str
    battery: int
    last_contact: str | None = None


class MouseBody:
    """Hidden simulator truth. The learner must not inspect `_rules`."""

    def __init__(self) -> None:
        self.state = MouseState(x=0, y=0, heading="N", battery=100)
        self._rules = {
            "pulse_a": "forward",
            "pulse_b": "turn_left",
            "pulse_c": "turn_right",
            "pulse_d": "backward",
            "sense": "sense",
            "stop": "stop",
        }

    @property
    def exposed_actions(self) -> tuple[str, ...]:
        return tuple(self._rules.keys())

    def observe(self) -> MouseState:
        return self.state

    def perturb(self, action_name: str, new_effect: str) -> None:
        """Test-only reality change used for the truth-bites experiment."""
        if action_name not in self._rules:
            raise KeyError(action_name)
        self._rules[action_name] = new_effect

    def step(self, action_name: str) -> MouseState:
        if action_name not in self._rules:
            raise ValueError(f"Unknown action: {action_name}")

        effect = self._rules[action_name]
        s = self.state
        x, y, heading = s.x, s.y, s.heading
        battery = max(0, s.battery - (0 if effect in {"sense", "stop"} else 1))
        contact = None

        if effect == "turn_left":
            heading = HEADINGS[(HEADINGS.index(heading) - 1) % 4]
        elif effect == "turn_right":
            heading = HEADINGS[(HEADINGS.index(heading) + 1) % 4]
        elif effect in {"forward", "backward"}:
            sign = 1 if effect == "forward" else -1
            dx, dy = {"N": (0, 1), "E": (1, 0), "S": (0, -1), "W": (-1, 0)}[heading]
            x += sign * dx
            y += sign * dy
        elif effect == "stuck":
            contact = "no_motion"
        elif effect in {"sense", "stop"}:
            pass
        else:
            raise ValueError(f"Unsupported hidden effect: {effect}")

        self.state = MouseState(x=x, y=y, heading=heading, battery=battery, last_contact=contact)
        return self.state


class AuthorityEnvelope:
    def __init__(self, permitted: set[str]) -> None:
        self.permitted = set(permitted)

    def allows(self, action: str) -> bool:
        return action in self.permitted


class EmpiricalBodyMap:
    def __init__(self) -> None:
        self.observations: dict[str, list[dict[str, Any]]] = defaultdict(list)

    @staticmethod
    def delta(before: MouseState, after: MouseState) -> dict[str, Any]:
        return {
            "dx": after.x - before.x,
            "dy": after.y - before.y,
            "heading_before": before.heading,
            "heading_after": after.heading,
            "battery_delta": after.battery - before.battery,
            "last_contact": after.last_contact,
        }

    @staticmethod
    def signature(delta: dict[str, Any]) -> tuple[Any, ...]:
        return (
            delta["dx"],
            delta["dy"],
            delta["heading_before"],
            delta["heading_after"],
            delta["battery_delta"],
            delta["last_contact"],
        )

    def record(self, action: str, before: MouseState, after: MouseState) -> None:
        d = self.delta(before, after)
        self.observations[action].append(
            {
                "before": asdict(before),
                "after": asdict(after),
                "delta": d,
            }
        )

    def status(self, action: str) -> str:
        rows = self.observations.get(action, [])
        if not rows:
            return "unknown"

        signatures = [self.signature(r["delta"]) for r in rows]
        unique = set(signatures)

        if len(rows) >= 3 and len(unique) == 1:
            return "validated"

        # If a transition was once validated by three identical observations and a
        # later observation differs, reality changes the trusted status.
        if len(rows) >= 4:
            first_three = set(signatures[:3])
            if len(first_three) == 1 and any(sig not in first_three for sig in signatures[3:]):
                return "contested"

        return "observed"

    def summary(self, action: str) -> dict[str, Any]:
        rows = self.observations.get(action, [])
        return {
            "action": action,
            "status": self.status(action),
            "samples": len(rows),
            "last_delta": rows[-1]["delta"] if rows else None,
        }


class Calibrator:
    def __init__(self, body: MouseBody, authority: AuthorityEnvelope) -> None:
        self.body = body
        self.authority = authority
        self.map = EmpiricalBodyMap()

    def probe(self, action: str) -> dict[str, Any]:
        if not self.authority.allows(action):
            return {
                "action": action,
                "disposition": "BLOCK",
                "reason": "action is outside the calibration authority envelope",
                "status": self.map.status(action),
            }

        before = self.body.observe()
        after = self.body.step(action)
        self.map.record(action, before, after)
        return {
            "action": action,
            "disposition": "OBSERVED",
            "before": asdict(before),
            "after": asdict(after),
            "map": self.map.summary(action),
        }


def main() -> None:
    body = MouseBody()
    authority = AuthorityEnvelope(
        permitted={"pulse_a", "pulse_b", "pulse_c", "sense", "stop"}
    )
    calibrator = Calibrator(body, authority)

    print("Lucian OS v0.2 — MouseSim 001")
    print("Mode: SIMULATION ONLY")
    print("Learner sees action names + observations, not hidden body rules.\n")

    print("[1] Calibrating pulse_a three times")
    for _ in range(3):
        result = calibrator.probe("pulse_a")
        print(result)
    print("Trusted status:", calibrator.map.status("pulse_a"))

    print("\n[2] Truth-bites perturbation: simulator changes pulse_a behavior")
    body.perturb("pulse_a", "stuck")
    result = calibrator.probe("pulse_a")
    print(result)
    print("Trusted status after contradictory evidence:", calibrator.map.status("pulse_a"))

    print("\n[3] Authority test: pulse_d exists physically but is not permitted")
    result = calibrator.probe("pulse_d")
    print(result)

    print("\nExpected core outcomes:")
    print("- pulse_a becomes validated after repeated consistent observations")
    print("- contradictory evidence changes pulse_a to contested")
    print("- unauthorized pulse_d returns BLOCK and is not executed")


if __name__ == "__main__":
    main()
