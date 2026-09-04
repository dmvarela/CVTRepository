"""Lucian OS — relationally corrigible viability model v0.01.

Simulation-only deterministic regime selector.

Purpose:
- model a conservative viability horizon;
- account for uncertainty in that horizon;
- represent corrective slack;
- distinguish HOLD, RECONSTRUCT, STABILIZE_AND_DISCRIMINATE,
  PRESERVE, and INFEASIBLE;
- provide toy cases for falsification before wiring the model into MouseSim.

Run from modern-robotics/lucian-os:
    py prototype/relational_viability_model.py
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
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
    detect_decide_act_verify_time: float
    viable_paths: int
    current_state_viable: bool
    safe_preserving_action_available: bool
    discriminating_probe_available: bool
    probe_time: float
    expected_information_gain_rate: float
    expected_margin_loss_rate: float
    intervention_effective_now: bool
    waiting_expected_to_improve_action_value: bool


def lower_horizon(context: DecisionContext, k: float = 1.0) -> float:
    """Conservative horizon estimate used by the toy selector."""
    return max(
        0.0,
        context.horizon_estimate - k * context.horizon_uncertainty,
    )


def corrective_slack(context: DecisionContext, k: float = 1.0) -> float:
    """Margin left after reserving time to detect, decide, act, and verify."""
    return lower_horizon(context, k) - context.detect_decide_act_verify_time


def choose_regime(context: DecisionContext) -> dict[str, object]:
    """Select one reasoning regime from the current viability state.

    The thresholds are intentionally simple. They are hypotheses to test, not
    a validated control law.
    """

    h_lower = lower_horizon(context)
    slack = corrective_slack(context)

    if (not context.goal_feasible) or context.viable_paths <= 0:
        regime = Regime.INFEASIBLE
        reason = "No admissible path satisfies the original goal."

    elif slack <= 0:
        regime = Regime.PRESERVE
        reason = (
            "Corrective slack is exhausted; explanatory delay would consume "
            "remaining recovery margin."
        )

    else:
        waiting_buys_more_than_it_costs = (
            context.expected_information_gain_rate
            > context.expected_margin_loss_rate
        )

        if (
            context.current_state_viable
            and not context.intervention_effective_now
            and context.waiting_expected_to_improve_action_value
            and waiting_buys_more_than_it_costs
        ):
            regime = Regime.HOLD
            reason = (
                "Waiting preserves viability and is expected to improve future "
                "action value faster than it consumes margin."
            )

        elif (
            context.discriminating_probe_available
            and context.probe_time < slack
            and (
                slack <= 2 * context.detect_decide_act_verify_time
                or context.viable_paths <= 2
            )
        ):
            regime = Regime.STABILIZE_AND_DISCRIMINATE
            reason = (
                "Margin is contracting; one bounded discriminating probe fits "
                "inside remaining corrective slack."
            )

        elif (
            slack > 2 * context.detect_decide_act_verify_time
            and context.viable_paths >= 3
        ):
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
        "correction_latency": context.detect_decide_act_verify_time,
        "corrective_slack": slack,
        "viable_paths": context.viable_paths,
        "reason": reason,
    }


def scenarios() -> list[DecisionContext]:
    return [
        DecisionContext(
            name="desk",
            goal_feasible=True,
            horizon_estimate=3600,
            horizon_uncertainty=600,
            detect_decide_act_verify_time=2,
            viable_paths=20,
            current_state_viable=True,
            safe_preserving_action_available=True,
            discriminating_probe_available=True,
            probe_time=1,
            expected_information_gain_rate=1.0,
            expected_margin_loss_rate=0.001,
            intervention_effective_now=False,
            waiting_expected_to_improve_action_value=True,
        ),
        DecisionContext(
            name="archers_out_of_effective_range",
            goal_feasible=True,
            horizon_estimate=30,
            horizon_uncertainty=5,
            detect_decide_act_verify_time=3,
            viable_paths=4,
            current_state_viable=True,
            safe_preserving_action_available=True,
            discriminating_probe_available=False,
            probe_time=0,
            expected_information_gain_rate=0.5,
            expected_margin_loss_rate=0.1,
            intervention_effective_now=False,
            waiting_expected_to_improve_action_value=True,
        ),
        DecisionContext(
            name="anomaly_ample_margin",
            goal_feasible=True,
            horizon_estimate=120,
            horizon_uncertainty=20,
            detect_decide_act_verify_time=5,
            viable_paths=5,
            current_state_viable=True,
            safe_preserving_action_available=True,
            discriminating_probe_available=True,
            probe_time=10,
            expected_information_gain_rate=0.5,
            expected_margin_loss_rate=0.05,
            intervention_effective_now=True,
            waiting_expected_to_improve_action_value=False,
        ),
        DecisionContext(
            name="contracting_margin",
            goal_feasible=True,
            horizon_estimate=20,
            horizon_uncertainty=5,
            detect_decide_act_verify_time=6,
            viable_paths=2,
            current_state_viable=True,
            safe_preserving_action_available=True,
            discriminating_probe_available=True,
            probe_time=4,
            expected_information_gain_rate=0.8,
            expected_margin_loss_rate=0.5,
            intervention_effective_now=True,
            waiting_expected_to_improve_action_value=False,
        ),
        DecisionContext(
            name="critical_margin",
            goal_feasible=True,
            horizon_estimate=7,
            horizon_uncertainty=2,
            detect_decide_act_verify_time=6,
            viable_paths=1,
            current_state_viable=True,
            safe_preserving_action_available=True,
            discriminating_probe_available=True,
            probe_time=4,
            expected_information_gain_rate=1.0,
            expected_margin_loss_rate=2.0,
            intervention_effective_now=True,
            waiting_expected_to_improve_action_value=False,
        ),
        DecisionContext(
            name="no_win",
            goal_feasible=False,
            horizon_estimate=15,
            horizon_uncertainty=3,
            detect_decide_act_verify_time=5,
            viable_paths=0,
            current_state_viable=True,
            safe_preserving_action_available=True,
            discriminating_probe_available=False,
            probe_time=0,
            expected_information_gain_rate=0.0,
            expected_margin_loss_rate=0.0,
            intervention_effective_now=True,
            waiting_expected_to_improve_action_value=False,
        ),
    ]


def main() -> None:
    print("Lucian OS — Relational Viability Model v0.01")
    print("Mode: SIMULATION ONLY")
    print("Thresholds are deliberately crude and falsifiable.\n")

    expected = {
        "desk": "HOLD",
        "archers_out_of_effective_range": "HOLD",
        "anomaly_ample_margin": "RECONSTRUCT",
        "contracting_margin": "STABILIZE_AND_DISCRIMINATE",
        "critical_margin": "PRESERVE",
        "no_win": "INFEASIBLE",
    }

    passed = True
    for context in scenarios():
        result = choose_regime(context)
        ok = result["regime"] == expected[context.name]
        passed = passed and ok
        print(result)
        print("expected:", expected[context.name], "PASS" if ok else "FAIL")
        print()

    print("Core regime matrix:", "PASS" if passed else "FAIL")
    print("Next: use this selector inside MouseSim after relational fault isolation.")


if __name__ == "__main__":
    main()
