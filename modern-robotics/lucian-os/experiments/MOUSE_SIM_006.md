# MouseSim 006 — Pressure Provenance and Agency

## Status

Simulation-only experiment, 2026-09-04.

## Discovery provenance

This experiment emerged from a discussion about being comfortable with epistemic discomfort. A remembered social example exposed a different structure: discomfort can be borne by oneself, but it can also be intentionally introduced into another person's decision environment.

The useful structural observation is not a generalization about any culture or population. It is narrower:

- an option may remain genuinely available;
- no violence, threat, deception, or physical override may occur;
- another agent may nevertheless deliberately alter the social or practical cost of exercising that option;
- the resulting choice is therefore evidence about behavior under the altered condition, not automatically clean evidence of an independent preference.

This created a new question for Lucian OS:

> Did I help create the behavior I am now interpreting?

## Why this is separate from MouseSim 005

MouseSim 005 asks whether urgency is supported by independent horizon evidence or merely claimed.

MouseSim 006 asks a neighboring but distinct question:

> What if the decision-maker itself changes the pressure landscape and then observes the resulting choice?

005 remains frozen so these hypotheses can be tested separately.

## Core distinctions

MouseSim 006 does **not** assume:

`influence = pressure = coercion = override`

These categories are kept separate.

It also does not assume that social pressure removes agency.

A central test case deliberately has:

`choice_remained_available = True`

while the observed choice changes under introduced social discomfort.

Thus the model can return both:

`agency_status = AVAILABLE`

and:

`preference_evidence_status = PRESSURE_SENSITIVE`

The person still had an available alternative; the evidentiary meaning of the resulting choice nevertheless changes because the decision landscape was altered.

## Pressure provenance

Current candidate sources:

- `NONE`
- `WORLD`
- `OTHER_AGENT`
- `SELF`

`SELF` means the observing/problem-solving system itself introduced the pressure.

The provenance is retained because a self-generated intervention can contaminate later inference if the system forgets that it helped produce the observed behavior.

## Preference evidence states

### CLEANER_BASELINE_EVIDENCE

A choice observed without recorded pressure is cleaner evidence for a current preference candidate, though not proof of an immutable preference.

### PRESSURE_SENSITIVE

The choice changes under pressure and returns to the prior baseline after the pressure is removed.

Interpretation:

> The pressured behavior is evidence of pressure sensitivity, not clean evidence of an independent preference change.

### CONTAMINATED_PERSISTS

The choice changes under pressure and continues after pressure is removed.

This increases the relevance of the new choice as a preference candidate, but the history remains contaminated by the original intervention.

The system must not reason:

`I pressured -> choice changed -> choice persisted -> therefore pressure was justified`

Instead it should seek later unpressured confirmation.

### WORLD_CONDITIONED

The world itself changed the decision conditions.

The choice is recorded as context-conditioned behavior rather than automatically rewriting the baseline preference.

### PRESSURE_CONTAMINATED

An agent-generated pressure is active and has not been removed or otherwise separated from the observed behavior.

The appropriate next step, when safe and authorized, is to remove the pressure and reobserve.

## Counterfactual probe

A key diagnostic maneuver is:

`baseline choice -> introduced pressure -> observed choice -> remove pressure -> reobserve`

If:

`A -> B -> A`

then the evidence strongly supports pressure sensitivity.

The valid inference is:

> Under the introduced pressure, B became the selected action.

The invalid stronger inference is:

> B was the person's independent preference all along.

## Self-generated evidence loop

This experiment is designed to guard against:

`system nudges -> person complies -> system observes compliance -> system infers preference -> system nudges harder`

Without provenance, the system can mistakenly use evidence it helped manufacture as justification for increasing the intervention that manufactured it.

Candidate rule:

> Self-generated pressure must remain attached to the provenance of the behavior observed under it.

## Relation to FTLτA

### F

Absence of physical override is not the same question as absence of influence. The system must preserve meaningful rejection paths and separately track how its own interventions alter their cost.

### T

Observed behavior must be interpreted under the conditions that produced it. A pressured choice cannot be silently promoted to independent preference evidence.

### L

Where possible, avoid degrading another agent's alternatives merely to obtain compliance. Preserve relational viability and the capacity for meaningful refusal.

### A

Agency may remain available even under influence or discomfort. The model must not erase agency merely because preferences are pressure-sensitive.

### tau

Preference evidence has history. Removing pressure and returning later can materially change what the prior choice warrants.

## Current test matrix

1. unpressured baseline choice;
2. self-created social pressure changes choice and removal restores baseline;
3. other-agent pressure changes choice and removal restores baseline;
4. self-created pressure changes choice and the new choice persists after removal;
5. changed world condition changes choice;
6. agent pressure remains active, so preference evidence remains contaminated;
7. comparison case where the alternative is actually removed, producing `AGENCY=CONSTRAINED`.

## Guardrails

- Do not infer population-level cultural traits from the motivating anecdote.
- Do not label every influence coercion.
- Do not treat option-cost asymmetry alone as proof that agency disappeared.
- Do not treat formal availability alone as proof that an observed choice reveals independent preference.
- Preserve intervention provenance.
- Prefer counterfactual reobservation where safe, authorized, and informative.

## Emerging principle

> A choice can be real while the inference drawn from that choice is still wrong.

And:

> If I altered the decision landscape, I must remember that when interpreting the decision.

## Next

Combine pressure provenance with the horizon/urgency model, then test dynamic `HOLD -> EXECUTE` while ensuring that system-created pressure cannot fake the evidence used to justify commitment.
