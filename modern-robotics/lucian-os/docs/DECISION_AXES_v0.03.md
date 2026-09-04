# Lucian OS — Decision Axes v0.03

## Status

Architecture refinement, 2026-09-04.

This version separates concepts that earlier prototypes partially mixed. The goal is to keep epistemic truth, feasibility, reasoning depth, and commitment behavior distinct so that pressure can change how the system acts without silently changing what it knows.

## Four coordinates

At any decision point, represent at least four independent coordinates:

1. **Epistemic status** — what is warranted?
   - `KNOWN_ENOUGH_TO_ACT`
   - `UNKNOWN`

2. **Feasibility status** — does an admissible solution to the current objective exist?
   - `FEASIBLE`
   - `INFEASIBLE`

3. **Reasoning regime** — how much inquiry can the current margin support?
   - `MONITOR`
   - `RECONSTRUCT`
   - `STABILIZE_AND_DISCRIMINATE`
   - `PRESERVE`

4. **Commitment posture** — what kind of commitment is warranted now?
   - `HOLD`
   - `PROBE`
   - `EXECUTE`
   - `EXECUTE_SAFE_ACTION`
   - `REROUTE_OBJECTIVE`
   - `REFUSE`

## Why the split matters

`UNKNOWN` and `INFEASIBLE` are not the same kind of statement.

- `UNKNOWN` means the available evidence does not yet warrant a sufficient conclusion.
- `INFEASIBLE` means the admissible solution set for the current objective is empty under the current warranted model.

Likewise, `HOLD` is not a reasoning regime. It is a commitment posture. A system can be reasoning deeply while withholding action, or reasoning minimally while continuing to hold a stable state.

The resulting architecture allows combinations such as:

`UNKNOWN + FEASIBLE + RECONSTRUCT + PROBE`

`UNKNOWN + FEASIBLE + PRESERVE + EXECUTE_SAFE_ACTION`

`KNOWN_ENOUGH_TO_ACT + FEASIBLE + MONITOR + EXECUTE`

`UNKNOWN + INFEASIBLE + PRESERVE + REROUTE_OBJECTIVE`

## Core invariant

> Pressure may change reasoning depth and commitment posture without changing epistemic status unless new evidence actually warrants that change.

This is the executable form of:

> Compress search, not truth.

A critical-horizon system may remain `UNKNOWN` while moving from `PROBE` to `EXECUTE_SAFE_ACTION` because no further diagnosis fits inside the remaining correction window.

## Authority remains separate

A shorter horizon does not manufacture permission.

Therefore:

`UNKNOWN + critical horizon + preserving action unauthorized`

must not become unauthorized execution. The correct posture is `REFUSE` or another authorized preserving alternative if one exists.

## Feasibility remains separate from time

A system can have substantial time margin and still face an infeasible objective:

`corrective_slack > 0`

while:

`V_t = empty set`

The proper response is to preserve what remains viable and reroute the objective truthfully rather than fabricate a solution.

## Relation to time-to-effect

The reasoning regime is selected against conservative corrective slack:

`H_lower = max(0, H_hat - k * sigma_H)`

`T_cycle = T_detect + T_decide + T_initiate + T_effect + T_verify`

`S = H_lower - T_cycle`

Probe selection must also reserve enough margin after the probe for a preserving or corrective action to still matter.

## Known limitation

The current selector still uses crude scalar thresholds and a scalar horizon. Real systems may have multiple simultaneous horizons and nonlinear reachable sets. This version exists to make the conceptual distinctions falsifiable, not to claim a validated control law.

## Next test

MouseSim 004 combines the four-coordinate model with MouseSim 003's `UNKNOWN` diagnosis under large, contracting, and critical horizons.

The key invariant is that the epistemic state remains unchanged while the reasoning regime and commitment posture adapt.
