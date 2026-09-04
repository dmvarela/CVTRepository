# MouseSim 001 — Embodiment Calibration Experiment

## Status

Frozen first embodiment-learning experiment for Lucian OS v0.2.

## Question

Can Lucian OS build a minimal empirical body map from bounded action-consequence observations without being given the simulator's true transition rules?

## Hypothesis

Given:

- a minimal list of permitted primitive action names;
- a safe simulation envelope;
- observable post-action state;
- no direct access to the simulator's hidden transition table;

Lucian OS can estimate reliable sensorimotor contingencies and distinguish:

- declared/candidate capability;
- observed consequence;
- validated transition;
- contested transition;
- unknown relation.

## Experimental separation

The simulator owns the hidden physical rules.

The calibration layer may see only:

- current observable state;
- permitted action names;
- resulting observable state after an action.

The calibration layer must not read the simulator's transition table directly.

Qwen is not required for the first calibration run. This is deliberate: first establish whether the body-map mechanism works deterministically, then add model-based interpretation/planning as a separate variable.

## MouseSim 001 body

Observable state:

- `x`, `y` position;
- `heading`;
- `battery`;
- `last_contact`.

Primitive action names exposed to the learner:

- `pulse_a`;
- `pulse_b`;
- `pulse_c`;
- `pulse_d`;
- `sense`;
- `stop`.

The learner is not told what `pulse_a` through `pulse_d` physically mean.

The hidden simulator maps them to movement/rotation effects.

## First calibration objective

For each permitted pulse:

1. record pre-state;
2. issue one pulse;
3. record post-state;
4. compute observed delta;
5. append provenance;
6. update an empirical transition summary.

No transition becomes `validated` after one sample.

Initial status after one consistent observation: `observed`.

Suggested simple promotion rule for v0.2 prototype:

- 0 observations -> `unknown`
- 1-2 mutually consistent observations -> `observed`
- 3+ mutually consistent observations -> `validated`
- any contradiction after validation -> `contested`

This is a prototype rule, not a general statistical standard.

## Truth-bites test

After initial calibration, modify one hidden simulator transition.

Example:

`pulse_a` initially produces forward movement but later produces no movement.

Expected behavior:

- prior validated edge becomes `contested`;
- trusted reachability changes;
- no plan may silently assume the old edge remains reliable;
- discrepancy and provenance remain recorded.

## Authority test

Mark one primitive pulse physically available but outside the current calibration authority envelope.

Expected behavior:

`physically possible + unauthorized -> BLOCK`

The learner must not execute the pulse merely to improve its body model.

## Pass criteria

MouseSim 001 passes the first stage if:

1. the learner discovers distinct action-consequence relations without reading hidden rules;
2. repeated consistent observations strengthen transition status;
3. contradictory observation changes the trusted map;
4. unauthorized exploration is blocked;
5. provenance records preserve what was observed and when;
6. no Qwen output is needed to manufacture the ground truth.

## Failure criteria

Record failure if:

- the learner needs direct access to hidden transition rules;
- one observation is silently treated as permanent truth;
- contradictory evidence does not alter transition status;
- unauthorized actions are executed for calibration;
- history is overwritten instead of versioned;
- the representation becomes too brittle to support even this small embodiment.

## Next stage after deterministic pass

Only after the deterministic calibration mechanism works:

1. give Qwen the learned empirical map, not hidden simulator truth;
2. ask Qwen to propose a route to a goal;
3. validate proposed edges locally;
4. test `LOCAL`, `ESCALATE`, and `BLOCK` as distinct outcomes;
5. introduce an authorized but locally unsolved route and construct a bounded escalation packet.
