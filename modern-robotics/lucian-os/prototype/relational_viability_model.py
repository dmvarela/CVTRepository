"""Lucian OS — relationally corrigible viability model v0.02.

Simulation-only deterministic regime selector.

v0.02 changes:
- decomposes correction latency into detect, decide, initiate, effect, verify;
- makes time-to-effect explicit;
- removes the dimensionally sloppy v0.01 comparison between information-gain
  rate and margin-loss rate;
- HOLD now requires projected corrective slack after the next review interval
  to remain above an explicit reserve;
- adds adversarial tests for actuator delay and horizon uncertainty.

Run from modern-robotics/lucian-os:
    py prototype/relational_viability_model.py
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class Regime(str, Enum):
    HOLD = "HOLD"
    RECONSTRUCT = "RECONSTRUCT"
    STABILIZE_AND_DISCRIMINATE = "STABILIZE_AND_DISCRIMINATE"
    PRESERVE = "PRESERVE"
    INFEASIBLE = "INFEASIBLE"


@dataclass(frozen=True)
class DecisionContext:
    name: str
    goal_feasible: bool
    horizon_estimate: float
    horizon_uncertainty: float

    # Latency decomposition
    detect_time: float
    decide_time: float
    initiate_time: float
    effect_time: float
    verify_time: float

    viable_paths: int
    current_state_viable: bool
    safe_preserving_action_available: bool

    discriminating_probe_available: bool
    probe_time: float

    # HOLD-specific state
    intervention_effective_now: bool
    waiting_expected_to_improve_action_value: bool
    next_review_interval: float
    margin_loss_rate: float
    hold_reserve: float


def lower_horizon(context: DecisionContext, k: float = 1.0) -> float:
    """Conservative viability-horizon estimate."""
    return max(
        0.0,
        context.horizon_estimate - k * context.horizon_uncertainty,
    )


def time_to_effect(context: DecisionContext) -> float:
    """Time until an initiated correction can begin changing the trajectory."""
    return (
        context.detect_time
        + context.decide_time
        + context.initiate_time
        + context.effect_time
    )


def correction_cycle_time(context: DecisionContext) -> float:
    """Time reserved to detect, decide, initiate, take effect, and verify."""
    return time_to_effect(context) + context.verify_time


def corrective_slack(context: DecisionContext, k: float = 1.0) -> float:
    """Conservative margin remaining after reserving a full correction cycle."""
    return lower_horizon(context, k) - correction_cycle_time(context)


def projected_slack_after_wait(context: DecisionContext, k: float = 1.0) -> float:
    """Slack expected to remain at the next HOLD review.

    margin_loss_rate is measured in horizon-units consumed per unit of waiting
    time. This avoids v0.01's comparison of unlike rate quantities.
    """
    wait_cost = context.next_review_interval * context.margin_loss_rate
    return corrective_slack(context, k) - wait_cost


def choose_regime(context: DecisionContext) -> dict[str, object]:
    """Select one toy reasoning regime.

    These thresholds are hypotheses for falsification, not a validated control law.
    """
    h_lower = lower_horizon(context)
    t_effect = time_to_effect(context)
    cycle = correction_cycle_time(context)
    slack = corrective_slack(context)
    slack_after_wait = projected_slack_after_wait(context)

    if (not context.goal_feasible) or context.viable_paths <= 0:
        regime = Regime.INFEASIBLE
        reason = "No admissible path satisfies the original goal."

    elif slack <= 0:
        regime = Regime.PRESERVE
        reason = (
            "The conservative horizon is shorter than the full correction cycle; "
            "there is no margin for explanatory delay."
        )

    else:
        hold_candidate = (
            context.current_state_viable
            and not context.intervention_effective_now
            and context.waiting_expected_to_improve_action_value
        )

        if hold_candidate and slack_after_wait > context.hold_reserve:
            regime = Regime.HOLD
            reason = (
                "Waiting is expected to improve future action value and the next "
                "review still preserves the required corrective reserve."
            )

        elif (
            context.discriminating_probe_available
            and context.probe_time < slack
            and (
                slack <= 2 * cycle
                or context.viable_paths <= 2
            )
        ):
            regime = Regime.STABILIZE_AND_DISCRIMINATE
            reason = (
                "Margin is contracting; one bounded discriminating probe fits "
                "inside remaining corrective slack."
            )

        elif slack > 2 * cycle and context.viable_paths >= 3:
            regime = Regime.RECONSTRUCT
            reason = (
                "Substantial conservative margin and multiple viable paths permit "
                "deeper diagnosis."
            )

        elif context.discriminating_probe_available and context.probe_time < slack:
            regime = Regime.STABILIZE_AND_DISCRIMINATE
            reason = "Use a bounded discriminating probe before committing."

        elif context.safe_preserving_action_available:
            regime = Regime.PRESERVE
            if hold_candidate:
                reason = (
                    "HOLD is rejected because the next review would consume too "
                    "much corrective reserve; use the safest validated preserving action."
                )
            else:
                reason = (
                    "No useful probe fits the remaining margin; take the safest "
                    "validated preserving action."
                )

        else:
            regime = Regime.HOLD
            reason = (
                "The current state remains viable and no better warranted "
                "intervention is available."
            )

    return {
        "scenario": context.name,
        "regime": regime.value,
        "horizon_estimate": context.horizon_estimate,
        "horizon_uncertainty": context.horizon_uncertainty,
        "lower_horizon": h_lower,
        "time_to_effect": t_effect,
        "verification_time": context.verify_time,
        "correction_cycle_time": cycle,
        "corrective_slack": slack,
        "projected_slack_after_wait": slack_after_wait,
        "hold_reserve": context.hold_reserve,
        "viable_paths": context.viable_paths,
        "reason": reason,
    }


def scenarios() -> list[tuple[DecisionContext, str]]:
    cases: list[tuple[DecisionContext, str]] = []

    def add(expected: str, **kwargs: object) -> None:
        cases.append((DecisionContext(**kwargs), expected))

    common = dict(
        goal_feasible=True,
        current_state_viable=True,
        safe_preserving_action_available=True,
        next_review_interval=1.0,
        margin_loss_rate=0.5,
        hold_reserve=2.0,
    )

    add(
        "HOLD",
        name="desk",
        horizon_estimate=3600,
        horizon_uncertainty=600,
        detect_time=0.5,
        decide_time=0.5,
        initiate_time=0.5,
        effect_time=0.5,
        verify_time=0.5,
        viable_paths=20,
        discriminating_probe_available=True,
        probe_time=1,
        intervention_effective_now=False,
        waiting_expected_to_improve_action_value=True,
        **common,
    )

    add(
        "HOLD",
        name="archers_out_of_effective_range",
        horizon_estimate=30,
        horizon_uncertainty=5,
        detect_time=0.5,
        decide_time=0.5,
        initiate_time=0.5,
        effect_time=2.0,
        verify_time=0.5,
        viable_paths=4,
        discriminating_probe_available=False,
        probe_time=0,
        intervention_effective_now=False,
        waiting_expected_to_improve_action_value=True,
        next_review_interval=2.0,
        margin_loss_rate=1.0,
        hold_reserve=5.0,
        goal_feasible=True,
        current_state_viable=True,
        safe_preserving_action_available=True,
    )

    add(
        "RECONSTRUCT",
        name="anomaly_ample_margin",
        horizon_estimate=120,
        horizon_uncertainty=20,
        detect_time=1,
        decide_time=1,
        initiate_time=1,
        effect_time=1,
        verify_time=1,
        viable_paths=5,
        discriminating_probe_available=True,
        probe_time=10,
        intervention_effective_now=True,
        waiting_expected_to_improve_action_value=False,
        **common,
    )

    add(
        "STABILIZE_AND_DISCRIMINATE",
        name="contracting_margin",
        horizon_estimate=20,
        horizon_uncertainty=5,
        detect_time=1,
        decide_time=1,
        initiate_time=1,
        effect_time=2,
        verify_time=1,
        viable_paths=2,
        discriminating_probe_available=True,
        probe_time=4,
        intervention_effective_now=True,
        waiting_expected_to_improve_action_value=False,
        **common,
    )

    add(
        "PRESERVE",
        name="critical_margin",
        horizon_estimate=7,
        horizon_uncertainty=2,
        detect_time=1,
        decide_time=1,
        initiate_time=1,
        effect_time=2,
        verify_time=1,
        viable_paths=1,
        discriminating_probe_available=True,
        probe_time=4,
        intervention_effective_now=True,
        waiting_expected_to_improve_action_value=False,
        **common,
    )

    add(
        "INFEASIBLE",
        name="no_win",
        goal_feasible=False,
        horizon_estimate=15,
        horizon_uncertainty=3,
        detect_time=1,
        decide_time=1,
        initiate_time=1,
        effect_time=1,
        verify_time=1,
        viable_paths=0,
        current_state_viable=True,
        safe_preserving_action_available=True,
        discriminating_probe_available=False,
        probe_time=0,
        intervention_effective_now=True,
        waiting_expected_to_improve_action_value=False,
        next_review_interval=1,
        margin_loss_rate=0,
        hold_reserve=2,
    )

    # Adversarial pair 1: same apparent horizon, only effect latency changes.
    add(
        "STABILIZE_AND_DISCRIMINATE",
        name="same_horizon_fast_effect",
        horizon_estimate=12,
        horizon_uncertainty=2,
        detect_time=1,
        decide_time=1,
        initiate_time=1,
        effect_time=1,
        verify_time=1,
        viable_paths=2,
        discriminating_probe_available=True,
        probe_time=2,
        intervention_effective_now=True,
        waiting_expected_to_improve_action_value=False,
        **common,
    )

    add(
        "PRESERVE",
        name="same_horizon_slow_effect",
        horizon_estimate=12,
        horizon_uncertainty=2,
        detect_time=1,
        decide_time=1,
        initiate_time=1,
        effect_time=7,
        verify_time=1,
        viable_paths=2,
        discriminating_probe_available=True,
        probe_time=2,
        intervention_effective_now=True,
        waiting_expected_to_improve_action_value=False,
        **common,
    )

    # Adversarial pair 2: same point estimate, only horizon uncertainty changes.
    add(
        "RECONSTRUCT",
        name="same_estimate_low_uncertainty",
        horizon_estimate=20,
        horizon_uncertainty=3,
        detect_time=1,
        decide_time=1,
        initiate_time=1,
        effect_time=1,
        verify_time=1,
        viable_paths=4,
        discriminating_probe_available=True,
        probe_time=2,
        intervention_effective_now=True,
        waiting_expected_to_improve_action_value=False,
        **common,
    )

    add(
        "PRESERVE",
        name="same_estimate_high_uncertainty",
        horizon_estimate=20,
        horizon_uncertainty=15,
        detect_time=1,
        decide_time=1,
        initiate_time=1,
        effect_time=1,
        verify_time=1,
        viable_paths=4,
        discriminating_probe_available=True,
        probe_time=2,
        intervention_effective_now=True,
        waiting_expected_to_improve_action_value=False,
        **common,
    )

    # HOLD should be rejected if waiting to the next review consumes the reserve.
    add(
        "PRESERVE",
        name="hold_rejected_reserve_consumed",
        horizon_estimate=14,
        horizon_uncertainty=2,
        detect_time=0.5,
        decide_time=0.5,
        initiate_time=0.5,
        effect_time=2.0,
        verify_time=0.5,
        viable_paths=2,
        current_state_viable=True,
        safe_preserving_action_available=True,
        discriminating_probe_available=False,
        probe_time=0,
        intervention_effective_now=False,
        waiting_expected_to_improve_action_value=True,
        next_review_interval=4.0,
        margin_loss_rate=1.5,
        hold_reserve=3.0,
        goal_feasible=True,
    )

    return cases


def main() -> None:
    print("Lucian OS — Relational Viability Model v0.02")
    print("Mode: SIMULATION ONLY")
    print("New: time-to-effect + conservative HOLD reserve tests.")
    print("Thresholds remain deliberately crude and falsifiable.\n")

    passed = True
    for context, expected in scenarios():
        result = choose_regime(context)
        ok = result["regime"] == expected
        passed = passed and ok
        print(result)
        print("expected:", expected, "PASS" if ok else "FAIL")
        print()

    print("v0.02 adversarial regime matrix:", "PASS" if passed else "FAIL")
    print(
        "Next: relational fault isolation, then combine fault hypotheses with "
        "contracting horizons in MouseSim."
    )


if __name__ == "__main__":
    main()
