"""Lucian OS — agency/membrane mapping v0.01.

Simulation-only conceptual falsification test.

Purpose:
- map the existing membrane B,Q,C,S decomposition onto influence/agency;
- test whether classic membrane failure signatures transfer coherently;
- deliberately test whether membrane viability is sufficient to distinguish
  healthy informational influence from strategic pressure.

This is an analogy test, not a claim that human agency is literally a membrane.

Run from modern-robotics/lucian-os:
    py prototype/agency_membrane_mapping_v001.py
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import Enum


class MembraneStatus(str, Enum):
    VIABLE = "VIABLE"
    NONVIABLE = "NONVIABLE"


class InfluenceClass(str, Enum):
    INFORMATIONAL = "INFORMATIONAL"
    STRATEGIC_PRESSURE = "STRATEGIC_PRESSURE"
    OVERRIDE = "OVERRIDE"
    INSUFFICIENT = "INSUFFICIENT"


@dataclass(frozen=True)
class InfluenceCase:
    name: str

    # Agency-analogue of delivered transport.
    delivered_influence: float
    lower_admissible: float
    handling_capacity: float

    # Q analogue: does the receiving decision process remain functionally distinct?
    meaningful_alternative_available: bool
    evaluative_mediation_retained: bool

    # C analogue: can the receiving state productively process the input?
    capture_ready: bool

    # S analogue: does recovery / re-evaluation headroom remain?
    restorative_reserve: float
    reserve_required: float

    # Provenance / strategy variables deliberately kept outside B,Q,C,S.
    strategic_pressure: bool = False
    option_removed: bool = False


@dataclass(frozen=True)
class MappingResult:
    bounded_coupling_B: bool
    preserved_organization_Q: bool
    capture_readiness_C: bool
    restorative_reserve_S: bool
    membrane_status: str
    failure_signatures: tuple[str, ...]
    influence_class: str
    mapping_gap_exposed: bool
    interpretation: str


def assess(case: InfluenceCase) -> MappingResult:
    """Assess the membrane analogy and expose where it is insufficient."""

    B = case.lower_admissible <= case.delivered_influence <= case.handling_capacity

    Q = (
        case.meaningful_alternative_available
        and case.evaluative_mediation_retained
        and not case.option_removed
    )

    C = case.capture_ready
    S = case.restorative_reserve >= case.reserve_required

    membrane_status = (
        MembraneStatus.VIABLE
        if all((B, Q, C, S))
        else MembraneStatus.NONVIABLE
    )

    failures: list[str] = []
    if case.delivered_influence < case.lower_admissible:
        failures.append("INSUFFICIENT_DELIVERY")
    elif case.delivered_influence > case.handling_capacity:
        failures.append("OVEREXPOSURE")

    if not C:
        failures.append("CAPTURE_FAILURE")

    if not Q:
        failures.append("LOSS_OF_IDENTITY_DEFINING_ORGANIZATION")

    if not S:
        failures.append("RESERVE_EXHAUSTION")

    if case.option_removed:
        influence_class = InfluenceClass.OVERRIDE
    elif case.strategic_pressure:
        influence_class = InfluenceClass.STRATEGIC_PRESSURE
    elif case.delivered_influence < case.lower_admissible:
        influence_class = InfluenceClass.INSUFFICIENT
    else:
        influence_class = InfluenceClass.INFORMATIONAL

    mapping_gap = (
        membrane_status == MembraneStatus.VIABLE
        and influence_class == InfluenceClass.STRATEGIC_PRESSURE
    )

    if mapping_gap:
        interpretation = (
            "B,Q,C,S remain viable even though the influence is strategically "
            "designed to alter the recipient's choice landscape. Membrane viability "
            "therefore does not by itself classify the legitimacy or provenance of influence."
        )
    elif membrane_status == MembraneStatus.VIABLE:
        interpretation = (
            "The receiving decision process remains inside the candidate membrane "
            "viability region under this simplified mapping."
        )
    else:
        interpretation = (
            "At least one membrane condition fails; the transferred failure signature "
            "identifies where the receiving decision relation loses viability."
        )

    return MappingResult(
        bounded_coupling_B=B,
        preserved_organization_Q=Q,
        capture_readiness_C=C,
        restorative_reserve_S=S,
        membrane_status=membrane_status.value,
        failure_signatures=tuple(failures),
        influence_class=influence_class.value,
        mapping_gap_exposed=mapping_gap,
        interpretation=interpretation,
    )


def cases() -> list[tuple[InfluenceCase, dict[str, object]]]:
    return [
        (
            InfluenceCase(
                name="truthful_reason_with_room_to_refuse",
                delivered_influence=0.30,
                lower_admissible=0.10,
                handling_capacity=0.80,
                meaningful_alternative_available=True,
                evaluative_mediation_retained=True,
                capture_ready=True,
                restorative_reserve=0.80,
                reserve_required=0.30,
            ),
            {
                "membrane_status": "VIABLE",
                "influence_class": "INFORMATIONAL",
                "mapping_gap_exposed": False,
            },
        ),
        (
            InfluenceCase(
                name="too_little_signal_to_support_transformation",
                delivered_influence=0.05,
                lower_admissible=0.10,
                handling_capacity=0.80,
                meaningful_alternative_available=True,
                evaluative_mediation_retained=True,
                capture_ready=True,
                restorative_reserve=0.80,
                reserve_required=0.30,
            ),
            {
                "membrane_status": "NONVIABLE",
                "failure_signature": "INSUFFICIENT_DELIVERY",
                "mapping_gap_exposed": False,
            },
        ),
        (
            InfluenceCase(
                name="overexposure_exceeds_handling_capacity",
                delivered_influence=0.90,
                lower_admissible=0.10,
                handling_capacity=0.50,
                meaningful_alternative_available=True,
                evaluative_mediation_retained=True,
                capture_ready=True,
                restorative_reserve=0.80,
                reserve_required=0.30,
            ),
            {
                "membrane_status": "NONVIABLE",
                "failure_signature": "OVEREXPOSURE",
                "mapping_gap_exposed": False,
            },
        ),
        (
            InfluenceCase(
                name="capture_failure_receiver_not_ready",
                delivered_influence=0.30,
                lower_admissible=0.10,
                handling_capacity=0.80,
                meaningful_alternative_available=True,
                evaluative_mediation_retained=True,
                capture_ready=False,
                restorative_reserve=0.80,
                reserve_required=0.30,
            ),
            {
                "membrane_status": "NONVIABLE",
                "failure_signature": "CAPTURE_FAILURE",
                "mapping_gap_exposed": False,
            },
        ),
        (
            InfluenceCase(
                name="option_removed_loss_of_decision_organization",
                delivered_influence=0.30,
                lower_admissible=0.10,
                handling_capacity=0.80,
                meaningful_alternative_available=False,
                evaluative_mediation_retained=False,
                capture_ready=True,
                restorative_reserve=0.80,
                reserve_required=0.30,
                option_removed=True,
            ),
            {
                "membrane_status": "NONVIABLE",
                "failure_signature": "LOSS_OF_IDENTITY_DEFINING_ORGANIZATION",
                "influence_class": "OVERRIDE",
                "mapping_gap_exposed": False,
            },
        ),
        (
            InfluenceCase(
                name="restorative_reserve_exhausted",
                delivered_influence=0.30,
                lower_admissible=0.10,
                handling_capacity=0.80,
                meaningful_alternative_available=True,
                evaluative_mediation_retained=True,
                capture_ready=True,
                restorative_reserve=0.10,
                reserve_required=0.30,
            ),
            {
                "membrane_status": "NONVIABLE",
                "failure_signature": "RESERVE_EXHAUSTION",
                "mapping_gap_exposed": False,
            },
        ),
        (
            InfluenceCase(
                name="euston_like_strategic_social_discomfort",
                delivered_influence=0.40,
                lower_admissible=0.10,
                handling_capacity=0.80,
                meaningful_alternative_available=True,
                evaluative_mediation_retained=True,
                capture_ready=True,
                restorative_reserve=0.80,
                reserve_required=0.30,
                strategic_pressure=True,
            ),
            {
                "membrane_status": "VIABLE",
                "influence_class": "STRATEGIC_PRESSURE",
                "mapping_gap_exposed": True,
            },
        ),
    ]


def matches(result: MappingResult, expected: dict[str, object]) -> bool:
    if "membrane_status" in expected and result.membrane_status != expected["membrane_status"]:
        return False
    if "influence_class" in expected and result.influence_class != expected["influence_class"]:
        return False
    if (
        "mapping_gap_exposed" in expected
        and result.mapping_gap_exposed != expected["mapping_gap_exposed"]
    ):
        return False
    if (
        "failure_signature" in expected
        and expected["failure_signature"] not in result.failure_signatures
    ):
        return False
    return True


def main() -> None:
    print("Lucian OS — Agency/Membrane Mapping v0.01")
    print("Mode: SIMULATION ONLY")
    print("Goal: test whether the membrane B,Q,C,S geometry transfers to agency/influence.\n")

    passed = True

    for case, expected in cases():
        result = assess(case)
        ok = matches(result, expected)
        passed = passed and ok

        print(f"[{case.name}]")
        print("case:", asdict(case))
        print("assessment:", asdict(result))
        print("expected:", expected, "PASS" if ok else "FAIL")
        print()

    print("Agency/membrane mapping matrix:", "PASS" if passed else "FAIL")
    print(
        "Positive result: classic membrane failure signatures transfer coherently "
        "to several agency/influence failure cases."
    )
    print(
        "Critical negative result: B,Q,C,S can remain viable under strategic pressure; "
        "membrane viability alone is not sufficient to classify influence legitimacy."
    )
    print(
        "Next: retain membrane geometry as a viability layer and add pressure provenance / "
        "agency constraints as an independent layer rather than collapsing them."
    )


if __name__ == "__main__":
    main()
