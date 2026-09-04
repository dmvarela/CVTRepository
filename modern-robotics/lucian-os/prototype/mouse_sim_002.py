"""MouseSim 002 — state-conditioned embodiment learning.

Simulation-only. No Qwen.

Purpose:
- learn action consequences conditioned on observable body state;
- keep raw telemetry separate from body-map inference;
- make contradictory evidence change planning behavior;
- use a safe epistemic action when consequential uncertainty is unresolved.

Run from modern-robotics/lucian-os:
    py prototype/mouse_sim_002.py
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import asdict, dataclass
from typing import Any


HEADINGS = ("N", "E", "S", "W")
VECTORS = {
    "N": (0, 1),
    "E": (1, 0),
    "S": (0, -1),
    "W": (-1, 0),
}


@dataclass(frozen=True)
class MouseState:
    x: int
    y: int
    heading: str
    battery: int
    last_contact: str | None = None
    sensed_front_blocked: bool | None = None


@dataclass(frozen=True)
class TelemetryEvent:
    seq: int
    action: str
    before: MouseState
    after: MouseState


class MouseBody:
    """Hidden simulator truth.

    The learner may act and observe, but must not inspect the body's hidden rules or
    hidden obstacle set.
    """

    def __init__(self) -> None:
        self.state = MouseState(0, 0, "N", 100)
        self._rules = {
            "pulse_a": "forward",
            "pulse_b": "turn_left",
            "pulse_c": "turn_right",
            "pulse_d": "backward",
            "sense": "sense",
            "stop": "stop",
        }
        self._obstacles: set[tuple[int, int]] = set()

    @property
    def exposed_actions(self) -> tuple[str, ...]:
        return tuple(self._rules.keys())

    def observe(self) -> MouseState:
        return self.state

    def perturb(self, action_name: str, new_effect: str) -> None:
        """Experiment-harness change to hidden body truth."""
        if action_name not in self._rules:
            raise KeyError(action_name)
        self._rules[action_name] = new_effect

    def test_set_state(self, state: MouseState) -> None:
        """Experiment-harness only; not exposed to the learner."""
        self.state = state

    def test_set_obstacles(self, cells: set[tuple[int, int]]) -> None:
        """Experiment-harness only; obstacle truth remains hidden from the learner."""
        self._obstacles = set(cells)

    def _front_cell(self, state: MouseState) -> tuple[int, int]:
        dx, dy = VECTORS[state.heading]
        return state.x + dx, state.y + dy

    def step(self, action_name: str) -> MouseState:
        if action_name not in self._rules:
            raise ValueError(f"Unknown action: {action_name}")

        effect = self._rules[action_name]
        s = self.state
        x, y, heading = s.x, s.y, s.heading
        contact: str | None = None
        sensed = s.sensed_front_blocked
        battery_cost = 0 if effect in {"sense", "stop"} else 1
        battery = max(0, s.battery - battery_cost)

        if effect == "turn_left":
            heading = HEADINGS[(HEADINGS.index(heading) - 1) % 4]
            sensed = None
        elif effect == "turn_right":
            heading = HEADINGS[(HEADINGS.index(heading) + 1) % 4]
            sensed = None
        elif effect in {"forward", "backward"}:
            sign = 1 if effect == "forward" else -1
            dx, dy = VECTORS[heading]
            target = (x + sign * dx, y + sign * dy)
            if target in self._obstacles:
                contact = "blocked"
            else:
                x, y = target
            # Occupancy evidence is local to the old pose/orientation and becomes stale.
            sensed = None
        elif effect == "stuck":
            contact = "no_motion"
            sensed = None
        elif effect == "sense":
            sensed = self._front_cell(s) in self._obstacles
            contact = "sensed"
        elif effect == "stop":
            contact = "stopped"
        else:
            raise ValueError(f"Unsupported hidden effect: {effect}")

        self.state = MouseState(
            x=x,
            y=y,
            heading=heading,
            battery=battery,
            last_contact=contact,
            sensed_front_blocked=sensed,
        )
        return self.state


class AuthorityEnvelope:
    def __init__(self, permitted: set[str]) -> None:
        self.permitted = set(permitted)

    def allows(self, action: str) -> bool:
        return action in self.permitted


class TelemetryLog:
    """Append-only raw action/observation history."""

    def __init__(self) -> None:
        self.events: list[TelemetryEvent] = []

    def append(
        self,
        action: str,
        before: MouseState,
        after: MouseState,
    ) -> TelemetryEvent:
        event = TelemetryEvent(len(self.events) + 1, action, before, after)
        self.events.append(event)
        return event


class EmpiricalBodyMap:
    """Inference layer derived from telemetry; never overwrites raw telemetry."""

    def __init__(self) -> None:
        # The first v0.2 context model is intentionally small: orientation + action.
        self.observations: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)

    @staticmethod
    def context(state: MouseState) -> str:
        return f"heading={state.heading}"

    @staticmethod
    def delta(before: MouseState, after: MouseState) -> dict[str, Any]:
        return {
            "dx": after.x - before.x,
            "dy": after.y - before.y,
            "heading_before": before.heading,
            "heading_after": after.heading,
            "battery_delta": after.battery - before.battery,
            "last_contact": after.last_contact,
            "sensed_front_blocked_before": before.sensed_front_blocked,
            "sensed_front_blocked_after": after.sensed_front_blocked,
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
            delta["sensed_front_blocked_before"],
            delta["sensed_front_blocked_after"],
        )

    def record(self, event: TelemetryEvent) -> None:
        context = self.context(event.before)
        d = self.delta(event.before, event.after)
        self.observations[(context, event.action)].append(
            {
                "telemetry_seq": event.seq,
                "delta": d,
            }
        )

    def status(self, context: str, action: str) -> str:
        rows = self.observations.get((context, action), [])
        if not rows:
            return "unknown"

        signatures = [self.signature(row["delta"]) for row in rows]

        # Three identical observations can establish a prototype-level validated
        # relation. Any later contradiction changes the status to contested.
        if len(rows) >= 4:
            first_three = set(signatures[:3])
            if len(first_three) == 1 and any(
                sig not in first_three for sig in signatures[3:]
            ):
                return "contested"

        if len(rows) >= 3 and len(set(signatures)) == 1:
            return "validated"

        return "observed"

    def summary(self, context: str, action: str) -> dict[str, Any]:
        rows = self.observations.get((context, action), [])
        return {
            "context": context,
            "action": action,
            "status": self.status(context, action),
            "samples": len(rows),
            "telemetry_refs": [row["telemetry_seq"] for row in rows],
            "last_delta": rows[-1]["delta"] if rows else None,
        }


class Calibrator:
    def __init__(self, body: MouseBody, authority: AuthorityEnvelope) -> None:
        self.body = body
        self.authority = authority
        self.telemetry = TelemetryLog()
        self.map = EmpiricalBodyMap()

    def probe(self, action: str) -> dict[str, Any]:
        if not self.authority.allows(action):
            return {
                "action": action,
                "disposition": "BLOCK",
                "reason": "action is outside the calibration authority envelope",
            }

        before = self.body.observe()
        after = self.body.step(action)

        # Reality is recorded first. Interpretation is derived second.
        event = self.telemetry.append(action, before, after)
        self.map.record(event)
        context = self.map.context(before)

        return {
            "disposition": "OBSERVED",
            "telemetry": {
                "seq": event.seq,
                "action": action,
                "before": asdict(before),
                "after": asdict(after),
            },
            "inference": self.map.summary(context, action),
        }


class TinyPlanner:
    """Small deterministic planner used to test whether warrant changes behavior."""

    def __init__(self, empirical_map: EmpiricalBodyMap) -> None:
        self.map = empirical_map

    def plan_one_step_forward(self, state: MouseState) -> dict[str, Any]:
        # First ask whether a consequential environmental fact is unresolved.
        if state.sensed_front_blocked is None:
            return {
                "disposition": "EPISTEMIC_ACTION",
                "action": "sense",
                "reason": "front occupancy is consequential and currently unknown",
            }

        if state.sensed_front_blocked:
            return {
                "disposition": "REPLAN_REQUIRED",
                "action": None,
                "reason": "telemetry reports the forward cell is blocked",
            }

        context = self.map.context(state)
        status = self.map.status(context, "pulse_a")

        if status == "validated":
            return {
                "disposition": "LOCAL_ACTION",
                "action": "pulse_a",
                "reason": f"transition is validated for {context}",
            }

        return {
            "disposition": "RECALIBRATE",
            "action": None,
            "reason": (
                f"pulse_a is {status} for {context}; "
                "trusted reachability is unavailable"
            ),
        }


def main() -> None:
    body = MouseBody()
    authority = AuthorityEnvelope(
        {"pulse_a", "pulse_b", "pulse_c", "sense", "stop"}
    )
    calibrator = Calibrator(body, authority)
    planner = TinyPlanner(calibrator.map)

    print("Lucian OS v0.2 — MouseSim 002")
    print("Mode: SIMULATION ONLY")
    print("Goal: discover state-conditioned embodiment + make truth alter planning.\n")

    print("[1] Learn pulse_a while facing NORTH")
    for _ in range(3):
        print(calibrator.probe("pulse_a"))
    print("North status:", calibrator.map.status("heading=N", "pulse_a"))

    print("\n[2] Turn EAST, then learn the same pulse without false contradiction")
    print(calibrator.probe("pulse_c"))
    for _ in range(3):
        print(calibrator.probe("pulse_a"))
    print("North status remains:", calibrator.map.status("heading=N", "pulse_a"))
    print("East status:", calibrator.map.status("heading=E", "pulse_a"))

    print("\n[3] T must bite planning")
    body.test_set_state(MouseState(0, 10, "N", 90))
    body.test_set_obstacles(set())
    print("Epistemic step:", planner.plan_one_step_forward(body.observe()))
    print("Sense:", calibrator.probe("sense"))
    print("Planner before contradiction:", planner.plan_one_step_forward(body.observe()))

    body.perturb("pulse_a", "stuck")
    print("Contradictory telemetry:", calibrator.probe("pulse_a"))
    print(
        "North status after contradiction:",
        calibrator.map.status("heading=N", "pulse_a"),
    )

    # Motion invalidated the previous occupancy observation, so ask reality again.
    print("Sense again:", calibrator.probe("sense"))
    print("Planner after contradiction:", planner.plan_one_step_forward(body.observe()))

    print("\n[4] Epistemic action: ask reality before moving")
    body.perturb("pulse_a", "forward")
    body.test_set_state(MouseState(2, 2, "N", 80))
    body.test_set_obstacles({(2, 3)})
    print(
        "Planner with consequential unknown:",
        planner.plan_one_step_forward(body.observe()),
    )
    print("Reality probe:", calibrator.probe("sense"))
    print("Planner after telemetry:", planner.plan_one_step_forward(body.observe()))

    print("\nExpected core outcomes:")
    print("- pulse_a validates separately for heading=N and heading=E")
    print("- contradictory north telemetry changes heading=N/pulse_a to contested")
    print("- planner changes from LOCAL_ACTION to RECALIBRATE")
    print("- consequential unknown occupancy causes EPISTEMIC_ACTION sense")
    print("- sensed obstacle causes REPLAN_REQUIRED rather than blind movement")
    print("- raw telemetry remains separate from body-map inference")


if __name__ == "__main__":
    main()
