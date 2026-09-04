"""Lucian OS — problem-solving decision axes v0.03.

Simulation-only candidate architecture.

Separates four coordinates that earlier prototypes partially mixed:
- epistemic status: what is warranted?
- feasibility status: does an admissible solution exist?
- reasoning regime: how much inquiry can be afforded?
- commitment posture: what kind of commitment is warranted now?
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class EpistemicStatus(str, Enum):
    KNOWN_ENOUGH_TO_ACT = "KNOWN_ENOUGH_TO_ACT"
    UNKNOWN = "UNKNOWN"


class FeasibilityStatus(str, Enum):
    FEASIBLE = "FEASIBLE"
    INFEASIBLE = "INFEASIBLE"


class ReasoningRegime(str, Enum):
    MONITOR = "MONITOR"
    RECONSTRUCT = "RECONSTRUCT"
    STABILIZE_AND_DISCRIMINATE = "STABILIZE_AND_DISCRIMINATE"
    PRESERVE = "PRESERVE"


class CommitmentPosture(str, Enum):
    HOLD = "HOLD"
    PROBE = "PROBE"
    EXECUTE = "EXECUTE"
    EXECUTE_SAFE_ACTION = "EXECUTE_SAFE_ACTION"
    REROUTE_OBJECTIVE = "REROUTE_OBJECTIVE"
    REFUSE = "REFUSE"


@dataclass(frozen=True)
class Probe:
    name: str
    latency: float
    hypotheses_reduced: int
    authorized: bool = True

    @property
    def discrimination_rate(self) -> float:
        if self.latency <= 0:
            return 0.0
        return self.hypotheses_reduced / self.latency


@dataclass(frozen=True)
class DecisionContext:
    name: str
    epistemic_status: EpistemicStatus
    feasibility_status: FeasibilityStatus
    horizon_estimate: float
    horizon_uncertainty: float

    detect_time: float
    decide_time: float
    initiate_time: float
    effect_time: float
    verify_time: float

    viable_paths: int
    current_state_viable: bool
    preserving_action_available: bool
    preserving_action_authorized: bool
    goal_action_authorized: bool

    probes: tuple[Probe, ...]
    probe_reserve: float = 0.0

    intervention_effective_now: bool = True
    waiting_expected_to_improve_action_value: bool = False
    next_review_interval: float = 1.0
    margin_loss_rate: float = 0.0
    hold_reserve: float = 0.0


@dataclass(frozen=True)
class Decision:
    epistemic_status: str
    feasibility_status: str
    reasoning_regime: str
    commitment_posture: str
    selected_probe: str | None
    lower_horizon: float
    correction_cycle_time: float
    corrective_slack: float
    reason: str


def lower_horizon(context: DecisionContext, k: float = 1.0) -> float:
    return max(0.0, context.horizon_estimate - k * context.horizon_uncertainty)


def correction_cycle_time(context: DecisionContext) -> float:
    return (
        context.detect_time
        + context.decide_time
        + context.initiate_time
        + context.effect_time
        + context.verify_time
    )


def corrective_slack(context: DecisionContext, k: float = 1.0) -> float:
    return lower_horizon(context, k) - correction_cycle_time(context)


def projected_slack_after_wait(context: DecisionContext, k: float = 1.0) -> float:
    wait_cost = context.next_review_interval * context.margin_loss_rate
    return corrective_slack(context, k) - wait_cost


def choose(context: DecisionContext) -> Decision:
    h_lower = lower_horizon(context)
    cycle = correction_cycle_time(context)
    slack = corrective_slack(context)

    # Feasibility is distinct from uncertainty. Sufficient warrant that no
    # admissible path exists changes the objective rather than inventing a route.
    if (
        context.feasibility_status == FeasibilityStatus.INFEASIBLE
        or context.viable_paths <= 0
    ):
        return Decision(
            epistemic_status=context.epistemic_status.value,
            feasibility_status=FeasibilityStatus.INFEASIBLE.value,
            reasoning_regime=ReasoningRegime.PRESERVE.value,
            commitment_posture=CommitmentPosture.REROUTE_OBJECTIVE.value,
            selected_probe=None,
            lower_horizon=h_lower,
            correction_cycle_time=cycle,
            corrective_slack=slack,
            reason=(
                "No admissible path satisfies the original objective; preserve "
                "what remains viable and reroute the objective truthfully."
            ),
        )

    # If the evidence is already sufficient for the relevant action, reasoning
    # can remain light. Authority still independently gates commitment.
    if context.epistemic_status == EpistemicStatus.KNOWN_ENOUGH_TO_ACT:
        posture = (
            CommitmentPosture.EXECUTE
            if context.goal_action_authorized
            else CommitmentPosture.REFUSE
        )
        reason = (
            "Evidence is sufficient for the relevant action and authority permits "
            "execution."
            if posture == CommitmentPosture.EXECUTE
            else "Evidence is sufficient, but the relevant action is not authorized."
        )
        return Decision(
            epistemic_status=context.epistemic_status.value,
            feasibility_status=context.feasibility_status.value,
            reasoning_regime=ReasoningRegime.MONITOR.value,
            commitment_posture=posture.value,
            selected_probe=None,
            lower_horizon=h_lower,
            correction_cycle_time=cycle,
            corrective_slack=slack,
            reason=reason,
        )

    # UNKNOWN is preserved from this point onward. Urgency may change inquiry
    # depth or action posture, but it must not silently promote certainty.
    hold_candidate = (
        context.current_state_viable
        and not context.intervention_effective_now
        and context.waiting_expected_to_improve_action_value
        and projected_slack_after_wait(context) > context.hold_reserve
    )
    if hold_candidate:
        return Decision(
            epistemic_status=EpistemicStatus.UNKNOWN.value,
            feasibility_status=context.feasibility_status.value,
            reasoning_regime=ReasoningRegime.MONITOR.value,
            commitment_posture=CommitmentPosture.HOLD.value,
            selected_probe=None,
            lower_horizon=h_lower,
            correction_cycle_time=cycle,
            corrective_slack=slack,
            reason=(
                "The state remains viable; waiting is expected to improve future "
                "action value while preserving the required correction reserve."
            ),
        )

    fitting_probes = [
        probe
        for probe in context.probes
        if probe.authorized
        and probe.latency + context.probe_reserve < max(slack, 0.0)
    ]

    if slack <= 0:
        posture = (
            CommitmentPosture.EXECUTE_SAFE_ACTION
            if context.preserving_action_available
            and context.preserving_action_authorized
            else CommitmentPosture.REFUSE
        )
        return Decision(
            epistemic_status=EpistemicStatus.UNKNOWN.value,
            feasibility_status=context.feasibility_status.value,
            reasoning_regime=ReasoningRegime.PRESERVE.value,
            commitment_posture=posture.value,
            selected_probe=None,
            lower_horizon=h_lower,
            correction_cycle_time=cycle,
            corrective_slack=slack,
            reason=(
                "Uncertainty remains unresolved, but the correction window cannot "
                "afford further diagnosis. Preserve without inflating certainty."
            ),
        )

    if fitting_probes:
        broad_probe = max(
            fitting_probes,
            key=lambda probe: (probe.hypotheses_reduced, -probe.latency),
        )
        if slack > 3 * cycle and broad_probe.hypotheses_reduced >= 2:
            return Decision(
                epistemic_status=EpistemicStatus.UNKNOWN.value,
                feasibility_status=context.feasibility_status.value,
                reasoning_regime=ReasoningRegime.RECONSTRUCT.value,
                commitment_posture=CommitmentPosture.PROBE.value,
                selected_probe=broad_probe.name,
                lower_horizon=h_lower,
                correction_cycle_time=cycle,
                corrective_slack=slack,
                reason=(
                    "Large conservative margin permits a broader cross-channel "
                    "probe while preserving correction capacity."
                ),
            )

        best_probe = max(
            fitting_probes,
            key=lambda probe: (
                probe.discrimination_rate,
                probe.hypotheses_reduced,
                -probe.latency,
            ),
        )
        return Decision(
            epistemic_status=EpistemicStatus.UNKNOWN.value,
            feasibility_status=context.feasibility_status.value,
            reasoning_regime=ReasoningRegime.STABILIZE_AND_DISCRIMINATE.value,
            commitment_posture=CommitmentPosture.PROBE.value,
            selected_probe=best_probe.name,
            lower_horizon=h_lower,
            correction_cycle_time=cycle,
            corrective_slack=slack,
            reason=(
                "Uncertainty matters to action and margin is finite; use the "
                "highest-yield authorized probe that fits the remaining reserve."
            ),
        )

    posture = (
        CommitmentPosture.EXECUTE_SAFE_ACTION
        if context.preserving_action_available and context.preserving_action_authorized
        else CommitmentPosture.REFUSE
    )
    return Decision(
        epistemic_status=EpistemicStatus.UNKNOWN.value,
        feasibility_status=context.feasibility_status.value,
        reasoning_regime=ReasoningRegime.PRESERVE.value,
        commitment_posture=posture.value,
        selected_probe=None,
        lower_horizon=h_lower,
        correction_cycle_time=cycle,
        corrective_slack=slack,
        reason=(
            "No authorized discriminating probe fits the remaining correction "
            "reserve; preserve the state without fabricating a diagnosis."
        ),
    )
