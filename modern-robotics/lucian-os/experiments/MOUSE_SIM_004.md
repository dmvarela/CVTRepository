# Lucian OS — MouseSim 004

## Title

Problem Solving Under a Contracting Viability Horizon

## Mode

SIMULATION ONLY. No Qwen. No real-device actuation.

## Purpose

MouseSim 004 combines two previously separate capabilities:

- MouseSim 003: preserve `UNKNOWN` when relational evidence cannot isolate body, sensor, or world failure.
- Decision Axes v0.03: separate epistemic status, feasibility status, reasoning regime, and commitment posture.

The experiment asks whether the same unresolved problem is handled differently as available corrective margin changes, without pretending that uncertainty disappeared.

## Shared starting evidence

All primary horizon cases begin from the same underdetermined telemetry:

- proximity reports blocked;
- command was issued;
- motor response unavailable;
- encoder reports zero movement;
- external displacement reports zero movement;
- contact evidence unavailable.

MouseSim 003 correctly returns:

`UNKNOWN -> SAFE_DISCRIMINATING_PROBE`

The diagnosis is held fixed across the horizon variants.

## Probe set

The toy system has three authorized probes:

- `motor_response_probe`: latency 2, reduces one hypothesis dimension;
- `contact_probe`: latency 3, reduces one hypothesis dimension;
- `cross_channel_bundle`: latency 8, broader but slower, reduces three hypothesis dimensions.

The values are deliberately crude. Their purpose is to force tradeoffs between breadth and time cost.

## Test matrix

### A — Large horizon

Expected:

`UNKNOWN + FEASIBLE + RECONSTRUCT + PROBE(cross_channel_bundle)`

Interpretation: enough margin remains for broader reconstruction.

### B — Contracting horizon

Expected:

`UNKNOWN + FEASIBLE + STABILIZE_AND_DISCRIMINATE + PROBE(motor_response_probe)`

Interpretation: the broad probe no longer fits the required reserve, so the system selects the highest-yield bounded probe.

### C — Critical horizon

Expected:

`UNKNOWN + FEASIBLE + PRESERVE + EXECUTE_SAFE_ACTION`

Interpretation: the uncertainty remains unresolved, but no further diagnosis fits inside the correction window.

### D — Critical horizon, preserving action unauthorized

Expected:

`UNKNOWN + FEASIBLE + PRESERVE + REFUSE`

Interpretation: urgency does not expand authority.

### E — Original objective infeasible

Expected:

`UNKNOWN + INFEASIBLE + PRESERVE + REROUTE_OBJECTIVE`

Interpretation: available time cannot manufacture a solution when no admissible path exists.

### F — Known enough to act

Expected:

`KNOWN_ENOUGH_TO_ACT + FEASIBLE + MONITOR + EXECUTE`

Interpretation: the axes are not hard-wired to uncertainty; when evidence is sufficient and authority permits action, commitment can proceed directly.

## Critical negative test — horizon misestimation

The selector is given an optimistic horizon estimate and therefore chooses a short discriminating probe.

Hidden experiment truth reveals that the real horizon was shorter. By the time the probe completes, the remaining true horizon is less than the correction cycle still required.

Expected result:

`MODEL_FAILURE_EXPOSED`

This is intentionally treated as a failure of the horizon model rather than retuning the selector until the case disappears.

The experiment therefore establishes an important limitation:

> A correct regime selector can still fail if the viability-horizon estimate is wrong.

## Key invariants

1. `UNKNOWN` must remain `UNKNOWN` when only time changes.
2. Less time may reduce inquiry depth but must not inflate certainty.
3. Probe latency must consume real correction margin.
4. Authority remains binding under pressure.
5. `INFEASIBLE` is distinct from `UNKNOWN`.
6. Negative results are preserved rather than hidden.

## Next rail

Add independent evidence about the horizon itself, then test false urgency versus real urgency.

Candidate question:

> Which relations can correct not only the state estimate, but the estimate of how much time remains to correct the state?
