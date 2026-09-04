# MouseSim 003 — Relational Fault Isolation

## Status

Simulation-only experiment, 2026-09-04.

No Qwen. No real-device actuation.

## Question

When observed behavior violates expectation, can Lucian OS distinguish among:

- a world/environment constraint;
- a body/actuator failure;
- a sensor/observation-model failure;
- normal cross-channel consistency;
- an underdetermined case where the evidence is insufficient to isolate a failure?

The experiment must not let the diagnostic engine inspect hidden simulator truth.

## Why this experiment exists

MouseSim 002 established that changed evidence can change warrant and planning. It also exposed a deeper problem: a no-motion event is not self-explanatory.

A forward command can fail to produce movement because:

- the path is blocked;
- the actuator failed;
- the sensor report is wrong;
- one of the observation channels is unavailable;
- several failures coexist.

Therefore the architecture should ask:

> Which expected relation stopped holding?

rather than:

> Which component should I blame?

## Hidden simulator variables

Each scenario has hidden truth for:

- `world_blocked`;
- `actuator_mode` (`healthy` or `stuck`);
- `proximity_mode` (`healthy` or `stuck_blocked`).

The diagnostic engine never reads these hidden fields.

## Observable telemetry

The diagnoser receives only relational evidence:

- `proximity_blocked`;
- `command_issued`;
- `motor_response`;
- `encoder_steps`;
- `external_displacement`;
- `contact_detected`.

This creates multiple routes that constrain the same state hypothesis.

## Candidate relations

The experiment reasons over relations such as:

- `world -> proximity report`;
- `command -> motor response`;
- `motor/body -> encoder motion`;
- `body -> external displacement`;
- `world/body -> contact`;
- `constraint -> zero displacement`.

Redundancy therefore lives partly in relations rather than in duplicated sensors.

## Expected cases

### 1. Normal clear motion

Evidence:

- proximity reports clear;
- motor responds;
- encoder records movement;
- external displacement confirms movement.

Expected diagnosis:

`CONSISTENT`

### 2. World changed — obstacle

Evidence:

- proximity reports blocked;
- motor responds;
- contact occurs;
- encoder and external displacement both remain zero.

Expected diagnosis:

`WORLD_CONSTRAINT`

Important: no-motion alone does not produce this diagnosis. The diagnosis depends on the relational pattern across several channels.

### 3. Body changed — actuator stuck

Evidence:

- proximity reports clear;
- no contact;
- motor fails to respond;
- encoder and external displacement remain zero.

Expected diagnosis:

`BODY_OR_ACTUATOR`

### 4. Sensor changed — proximity stuck blocked

Evidence:

- proximity reports blocked;
- motor responds;
- encoder reports movement;
- external displacement confirms movement.

Expected diagnosis:

`SENSOR_OR_OBSERVATION_MODEL`

The diagnoser localizes the suspect relation; it does not claim knowledge of the exact physical sensor defect.

### 5. Underdetermined evidence

Evidence:

- proximity reports blocked;
- zero movement;
- motor-response and contact channels are unavailable.

Multiple hypotheses remain compatible with the observation.

Expected diagnosis:

`UNKNOWN`

Expected next step:

`SAFE_DISCRIMINATING_PROBE`

This is the critical negative test. The system must not manufacture attribution simply because a diagnosis was requested.

## Pass criteria

MouseSim 003 passes the toy matrix only if:

- normal cross-channel consistency -> `CONSISTENT`;
- world constraint pattern -> `WORLD_CONSTRAINT`;
- body/actuator pattern -> `BODY_OR_ACTUATOR`;
- sensor/world-report contradiction -> `SENSOR_OR_OBSERVATION_MODEL`;
- underdetermined evidence -> `UNKNOWN`;
- raw hidden truth remains inaccessible to the diagnostic engine.

Passing this matrix validates only that the deterministic prototype behaves according to the stated toy expectations.

## Architectural significance

If the experiment works, Lucian OS has a primitive form of relational diagnosis:

`prediction -> telemetry -> residual pattern -> surviving hypotheses -> diagnosis or UNKNOWN`

The important principle is:

> Contradiction should narrow or revise the model, not automatically select a culprit.

And:

> No single path certifies itself.

## Next bridge

MouseSim 004 should combine this diagnostic layer with the Relational Viability Model v0.02.

The same fault pattern should then be presented under different viability horizons:

- ample horizon -> deeper reconstruction;
- contracting horizon -> one high-value discriminating probe;
- critical horizon -> preservation before full diagnosis;
- no viable path -> `INFEASIBLE`;
- ambiguous evidence with insufficient time -> explicit unresolved diagnosis plus preserving action, not fabricated certainty.

## Guardrails

- This is not a model of aviation fault diagnosis or a certified control law.
- Real systems require domain-specific safety engineering, sensor models, uncertainty treatment, and validated procedures.
- The simulation uses simplified deterministic patterns only to test architectural distinctions.
- A diagnosis label names the currently suspect relation class, not a metaphysical certainty about the hidden cause.
