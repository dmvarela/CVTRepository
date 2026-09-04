"""MouseSim 003 — relational fault isolation.

Simulation-only. No Qwen. No real-device actuation.

Purpose:
- keep hidden world/body/sensor truth separate from telemetry;
- diagnose violated relations rather than automatically blaming a component;
- distinguish world constraint, body/actuator failure, sensor/observation-model failure,
  normal consistency, and genuinely underdetermined cases;
- preserve UNKNOWN when available evidence cannot isolate the failure;
- recommend a safe discriminating probe rather than fabricate a diagnosis.

Run from modern-robotics/lucian-os:
    py prototype/mouse_sim_003.py
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import Enum


class Diagnosis(str, Enum):
    CONSISTENT = "CONSISTENT"
    WORLD_CONSTRAINT = "WORLD_CONSTRAINT"
    BODY_OR_ACTUATOR = "BODY_OR_ACTUATOR"
    SENSOR_OR_OBSERVATION_MODEL = "SENSOR_OR_OBSERVATION_MODEL"
    UNKNOWN = "UNKNOWN"


@dataclass(frozen=True)
class HiddenCase:
    """Experiment-harness truth. The diagnostic engine never reads these fields."""

    name: str
    world_blocked: bool
    actuator_mode: str  # healthy | stuck
    proximity_mode: str  # healthy | stuck_blocked
    expose_motor_response: bool = True
    expose_contact: bool = True


@dataclass(frozen=True)
class Telemetry:
    """Only this object is given to the diagnostic engine."""

    proximity_blocked: bool | None
    command_issued: bool
    motor_response: bool | None
    encoder_steps: int | None
    external_displacement: int | None
    contact_detected: bool | None


@dataclass(frozen=True)
class DiagnosticResult:
    diagnosis: str
    violated_relations: tuple[str, ...]
    supporting_relations: tuple[str, ...]
    next_step: str
    explanation: str


class HiddenMouseSimulator:
    """Produces telemetry from hidden world/body/sensor state."""

    @staticmethod
    def run(case: HiddenCase) -> Telemetry:
        # Primary proximity sensor.
        if case.proximity_mode == "healthy":
            proximity_blocked = case.world_blocked
        elif case.proximity_mode == "stuck_blocked":
            proximity_blocked = True
        else:
            raise ValueError(f"Unsupported proximity mode: {case.proximity_mode}")

        command_issued = True

        # Motor/actuator relation.
        motor_response_truth = case.actuator_mode == "healthy"

        # World and actuator jointly determine whether displacement occurs.
        moved = motor_response_truth and not case.world_blocked
        encoder_steps = 1 if moved else 0
        external_displacement = 1 if moved else 0

        # Contact is a distinct relation: a healthy actuator pressing into a real
        # obstacle yields contact; a stuck actuator in free space does not.
        contact_truth = (
            case.world_blocked
            and case.actuator_mode == "healthy"
            and command_issued
        )

        return Telemetry(
            proximity_blocked=proximity_blocked,
            command_issued=command_issued,
            motor_response=(
                motor_response_truth if case.expose_motor_response else None
            ),
            encoder_steps=encoder_steps,
            external_displacement=external_displacement,
            contact_detected=(contact_truth if case.expose_contact else None),
        )


class RelationalDiagnoser:
    """Diagnose patterns of relation failure without access to hidden truth."""

    @staticmethod
    def diagnose(t: Telemetry) -> DiagnosticResult:
        independent_motion = (
            (t.encoder_steps is not None and t.encoder_steps > 0)
            or (
                t.external_displacement is not None
                and t.external_displacement > 0
            )
        )

        both_motion_channels_zero = (
            t.encoder_steps == 0
            and t.external_displacement == 0
        )

        # Case 1: primary sensor predicts blocked, yet two independent motion
        # relations show successful displacement. Do not claim which piece of
        # hardware is physically broken; localize the suspect relation.
        if t.proximity_blocked is True and independent_motion:
            return DiagnosticResult(
                diagnosis=Diagnosis.SENSOR_OR_OBSERVATION_MODEL.value,
                violated_relations=(
                    "proximity_report -> predicted_world_constraint",
                ),
                supporting_relations=(
                    "command -> motor response",
                    "motor/body -> encoder motion",
                    "body -> external displacement",
                ),
                next_step="RECALIBRATE_OR_CROSS_CHECK_SENSOR",
                explanation=(
                    "The proximity report predicts a blocked forward relation, "
                    "but independent motion channels show that the body actually "
                    "advanced. The sensor/observation relation is therefore suspect."
                ),
            )

        # Case 2: blocked report + no motion + contact + motor response form a
        # mutually consistent relational pattern for a world constraint.
        if (
            t.proximity_blocked is True
            and both_motion_channels_zero
            and t.contact_detected is True
            and t.motor_response is True
        ):
            return DiagnosticResult(
                diagnosis=Diagnosis.WORLD_CONSTRAINT.value,
                violated_relations=(),
                supporting_relations=(
                    "world -> proximity blocked",
                    "command -> motor response",
                    "world/body -> contact",
                    "constraint -> zero displacement",
                ),
                next_step="REPLAN_AROUND_CONSTRAINT",
                explanation=(
                    "Several distinct relations agree: the path is reported blocked, "
                    "the actuator responds, contact is detected, and the body does "
                    "not displace. The evidence supports a world constraint rather "
                    "than immediately blaming the motor."
                ),
            )

        # Case 3: sensor reports clear but the command fails to produce motor/body
        # response in free-space telemetry.
        if (
            t.proximity_blocked is False
            and both_motion_channels_zero
            and t.motor_response is False
            and t.contact_detected is False
        ):
            return DiagnosticResult(
                diagnosis=Diagnosis.BODY_OR_ACTUATOR.value,
                violated_relations=(
                    "command -> motor response",
                    "expected_free_path -> body displacement",
                ),
                supporting_relations=(
                    "world -> proximity clear",
                    "no contact -> no observed obstacle",
                ),
                next_step="RECALIBRATE_BODY_OR_USE_ALTERNATE_ACTUATION",
                explanation=(
                    "The path is reported clear and no contact is observed, yet the "
                    "command produces no motor response or displacement. The failure "
                    "localizes to the body/actuator relation more strongly than to "
                    "the world relation."
                ),
            )

        # Normal cross-channel agreement.
        if (
            t.proximity_blocked is False
            and independent_motion
            and t.motor_response is True
        ):
            return DiagnosticResult(
                diagnosis=Diagnosis.CONSISTENT.value,
                violated_relations=(),
                supporting_relations=(
                    "world -> proximity clear",
                    "command -> motor response",
                    "motor/body -> encoder motion",
                    "body -> external displacement",
                ),
                next_step="CONTINUE",
                explanation=(
                    "Sensor, actuator, encoder, and external displacement relations "
                    "are mutually consistent with an unobstructed successful move."
                ),
            )

        # Crucial negative result: do not force attribution when the relational
        # evidence does not uniquely distinguish world, body, or sensor hypotheses.
        return DiagnosticResult(
            diagnosis=Diagnosis.UNKNOWN.value,
            violated_relations=("unresolved_relation_set",),
            supporting_relations=(),
            next_step="SAFE_DISCRIMINATING_PROBE",
            explanation=(
                "Available evidence does not isolate a unique failed relation. "
                "Preserve the competing hypotheses and seek an authorized safe "
                "probe that can distinguish them."
            ),
        )


def cases() -> list[tuple[HiddenCase, str]]:
    return [
        (
            HiddenCase(
                name="normal_clear_motion",
                world_blocked=False,
                actuator_mode="healthy",
                proximity_mode="healthy",
            ),
            Diagnosis.CONSISTENT.value,
        ),
        (
            HiddenCase(
                name="world_changed_obstacle",
                world_blocked=True,
                actuator_mode="healthy",
                proximity_mode="healthy",
            ),
            Diagnosis.WORLD_CONSTRAINT.value,
        ),
        (
            HiddenCase(
                name="body_changed_actuator_stuck",
                world_blocked=False,
                actuator_mode="stuck",
                proximity_mode="healthy",
            ),
            Diagnosis.BODY_OR_ACTUATOR.value,
        ),
        (
            HiddenCase(
                name="sensor_changed_stuck_blocked",
                world_blocked=False,
                actuator_mode="healthy",
                proximity_mode="stuck_blocked",
            ),
            Diagnosis.SENSOR_OR_OBSERVATION_MODEL.value,
        ),
        (
            HiddenCase(
                name="underdetermined_missing_relations",
                world_blocked=True,
                actuator_mode="healthy",
                proximity_mode="healthy",
                expose_motor_response=False,
                expose_contact=False,
            ),
            Diagnosis.UNKNOWN.value,
        ),
    ]


def main() -> None:
    simulator = HiddenMouseSimulator()
    diagnoser = RelationalDiagnoser()

    print("Lucian OS — MouseSim 003")
    print("Mode: SIMULATION ONLY")
    print("Goal: diagnose which relation failed without reading hidden truth.\n")

    passed = True

    for hidden_case, expected in cases():
        telemetry = simulator.run(hidden_case)
        result = diagnoser.diagnose(telemetry)
        ok = result.diagnosis == expected
        passed = passed and ok

        print(f"[{hidden_case.name}]")
        print("telemetry:", asdict(telemetry))
        print("diagnosis:", asdict(result))
        print("expected:", expected, "PASS" if ok else "FAIL")
        print()

    print("MouseSim 003 relational diagnosis matrix:", "PASS" if passed else "FAIL")
    print("Critical negative test: underdetermined evidence must remain UNKNOWN.")
    print(
        "Next: combine these hypotheses with the v0.02 viability-horizon selector "
        "so available time determines how much diagnosis can be afforded."
    )


if __name__ == "__main__":
    main()
