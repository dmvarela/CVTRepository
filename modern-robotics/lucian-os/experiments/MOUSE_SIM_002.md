# MouseSim 002 — Discover a Body

## Status

Frozen second Lucian OS embodiment-learning experiment, 2026-09-03.

MouseSim 001 showed that repeated action-consequence observations can move a relation from `observed` to `validated`, contradictory evidence can move it to `contested`, and unauthorized calibration can be blocked.

MouseSim 002 asks a harder question:

> Can the learner discover that the consequence of an action depends on current body state, while keeping telemetry separate from inference and allowing changed warrant to alter planning?

## Core transition model

MouseSim 001 used a flat relation:

`action -> observed delta`

MouseSim 002 tests the richer form:

`(state, action) -> next state`

The first state variable under test is orientation.

Thus `pulse_a` may be validated separately under:

- `heading=N`
- `heading=E`

A different absolute displacement after rotation should not automatically be treated as contradiction.

## Experimental separations

### Hidden simulator truth

The learner cannot inspect:

- the action-to-effect rule table;
- the obstacle set;
- perturbations applied by the experiment harness.

### Telemetry

Every permitted probe first produces an append-only raw telemetry event containing:

- sequence number;
- action;
- pre-state;
- post-state.

### Inference

The empirical body map is derived from telemetry and stores references back to the raw telemetry sequence numbers.

Inference must not overwrite telemetry.

## Test 1 — State-conditioned action learning

1. Run `pulse_a` three times while facing north.
2. Expect `heading=N + pulse_a -> validated`.
3. Execute the unknown turn pulse that changes orientation eastward.
4. Run `pulse_a` three times while facing east.
5. Expect `heading=E + pulse_a -> validated` while the north relation remains validated.

Pass condition:

> The learner treats the same action as having distinct reliable consequences in distinct observable body states instead of collapsing them into one contradictory global action rule.

## Test 2 — Truth must alter planning

1. Restore a north-facing test state.
2. Use `sense` to establish that the forward cell is clear.
3. Ask the tiny deterministic planner for a one-step-forward decision.
4. Because north + `pulse_a` is validated, expect `LOCAL_ACTION`.
5. Perturb hidden body truth so `pulse_a` no longer moves the body.
6. Execute `pulse_a` and record contradictory telemetry.
7. Expect the north transition to become `contested`.
8. Sense again, then ask the planner for the same one-step-forward decision.
9. Expect `RECALIBRATE`, not `LOCAL_ACTION`.

This is the first direct behavioral T test:

`changed evidence -> changed warrant -> changed reachable action`

A status label alone is insufficient.

## Test 3 — Epistemic action

Create a state in which the forward occupancy is unknown but consequential.

Expected planner output:

`EPISTEMIC_ACTION -> sense`

The sensing action is not chosen to accomplish the external movement goal directly. It is chosen to obtain evidence required to decide safely.

After telemetry reports an obstacle ahead, expect:

`REPLAN_REQUIRED`

rather than blind movement.

## Candidate principle

> Preserve the task-relevant invariant; infer unresolved detail faithfully; when consequential uncertainty remains, use an authorized safe probe so reality can answer.

## FTLτA behavior under test

### F

Only actions inside the authority envelope may be used for calibration or epistemic probing.

### T

Raw telemetry must be preserved independently of inference, and contradictory evidence must be able to remove an action from trusted planning.

### τ

Telemetry sequence references preserve the order and provenance of observations. Full restart continuity is deferred to a later experiment.

### L and A

Not independently tested in MouseSim 002.

## Known limitations

- The v0.2 context key initially uses orientation only; richer contexts will be necessary.
- Contact with an environmental obstacle and failure of a body actuator can both change observed motion; later work must distinguish causal attribution rather than treating every mismatch as a body failure.
- Three repeated observations are only a prototype promotion rule, not a statistically justified universal threshold.
- `sense` is an idealized discrete sensor.
- The planner handles only a one-step-forward decision.
- Qwen remains deliberately absent.

## Pass criteria

MouseSim 002 passes if:

1. north and east `pulse_a` relations can both become validated;
2. orientation change does not falsely contest the north relation;
3. raw telemetry remains append-only and separately referenced by inference;
4. a later contradictory north observation changes that relation to `contested`;
5. the planner consequently changes from `LOCAL_ACTION` to `RECALIBRATE`;
6. consequential unknown occupancy causes an epistemic `sense` action;
7. observed blockage causes `REPLAN_REQUIRED` rather than blind movement.

## Failure criteria

Record failure if:

- action meaning remains globally flat and cannot condition on state;
- inference rewrites or substitutes for raw telemetry;
- contested reachability remains usable by the planner;
- uncertainty is silently completed when a safe discriminating probe exists;
- the planner moves into known blockage;
- hidden simulator truth leaks into the learner.

## Next rail if 002 passes

MouseSim 003 should move from one-step body knowledge to goal-directed navigation:

`learned embodiment map + local world evidence + goal -> candidate trajectory`

Only after a deterministic navigator is working should Qwen return as a bounded route proposer rather than a motor controller.
