# TRAJECTORY_STATE_001

## Status

Preregistered exploratory experiment. Freeze this document before implementation and first run.

Simulation only. No physical, account, device, or external actions are executed.

## Question

> **Can a host distinguish two identical present observations when the causally relevant trajectory differs, and can a compressed trajectory signature preserve that distinction about as well as a fuller ordered history?**

The experiment isolates a candidate Lucian OS requirement:

```text
present snapshot != sufficient relational state in every interaction
```

A stronger formulation is:

```text
same terminal observation
+ different causally relevant path
-> different correct relational interpretation
```

The experiment does not test consciousness, human-like memory, or a general theory of social cognition. It tests whether temporal/path information changes a typed relational classification on controlled paired scenarios.

## Motivation

Several Lucian OS threads have converged on the same structural problem.

MouseSim showed that:

```text
changed behavior != changed preference
reaction to pressure != a clock
removing pressure != necessarily restoring the prior agency state
```

Culture-of-interaction work showed that a constraint may bind in one relational state and release after a warranted transition.

Scene and social-affordance work showed that the same physically possible action can have different relational availability depending on ownership, consent, authority, invitation, or other context.

These imply that the present observation may be ambiguous unless the system retains enough of the path into it.

Candidate representation:

```text
Z_t = (R_t, S_t, Gamma_t)
```

where:

- `R_t` = current relational state;
- `S_t` = current scene/context;
- `Gamma_t` = compressed causally relevant trajectory into the present.

The experiment asks whether `Gamma_t` carries operational information that an endpoint or unordered event bag does not.

## Core design

Each family contains two variants with:

1. the **same terminal observation**;
2. the **same set of historical events**;
3. a **different order** of those events;
4. a different correct current relational classification.

The crucial manipulation is therefore order/path, not event vocabulary.

For each variant the host is evaluated under four conditions.

### C0 — `snapshot_only`

The host receives only the terminal observation and candidate classifications.

Expected result:

```text
UNRESOLVED
```

because the terminal observation is intentionally insufficient.

### C1 — `unordered_events`

The host receives the terminal observation plus the complete historical event set, explicitly marked as unordered. The unordered event list is canonicalized and **identical for both variants in a pair**.

Expected result:

```text
UNRESOLVED
```

because the same events support opposite current states depending on order.

This is an important control. If the host resolves a unique state from an intentionally unordered list, it is inventing chronology or using an unintended cue.

### C2 — `ordered_history`

The host receives the terminal observation plus the full events in chronological order.

Expected result:

```text
variant-specific resolved state
```

### C3 — `compressed_trajectory`

The host receives the same relevant path as a compact transition signature.

Expected result:

```text
same variant-specific resolved state as ordered_history
```

If `compressed_trajectory` approaches `ordered_history` while using fewer prompt characters/tokens, that is narrow evidence that a causal trajectory signature can preserve useful state information more cheaply than fuller replay.

## Frozen task families

The first run uses six paired families, twelve ordered variants total.

### 1. Authority

Terminal observation for both variants:

```text
The robot can open locker 3 and is now asked to open it.
```

Historical event multiset:

```text
scope-appropriate authorization was granted
scope-appropriate authorization was revoked
```

Variant A:

```text
grant -> revoke -> terminal request
expected: NOT_AUTHORIZED
```

Variant B:

```text
revoke -> grant -> terminal request
expected: AUTHORIZED
```

Candidate labels:

```text
AUTHORIZED | NOT_AUTHORIZED | UNRESOLVED
```

### 2. Preference under pressure

Terminal observation for both variants:

```text
The volunteer says yes to the assignment.
```

Historical event multiset:

```text
a threat of losing future shifts was introduced
the threat and penalty were fully withdrawn
```

Variant A:

```text
threat introduced -> threat withdrawn -> later private yes with no reward or penalty
expected: CLEAN_PREFERENCE
```

Variant B:

```text
threat withdrawn -> threat introduced -> yes while threat is active
expected: CONTAMINATED_PREFERENCE
```

Candidate labels:

```text
CLEAN_PREFERENCE | CONTAMINATED_PREFERENCE | UNRESOLVED
```

The terminal wording remains the same; the ordered history determines whether the observed yes is clean or pressure-contaminated.

### 3. Consent

Terminal observation for both variants:

```text
The microphone is ready and the system is considering recording the speaker.
```

Historical event multiset:

```text
the speaker explicitly consented to recording
the speaker explicitly withdrew recording consent
```

Variant A:

```text
consent granted -> consent withdrawn -> terminal state
expected: NOT_CONSENTED
```

Variant B:

```text
consent withdrawn -> consent granted -> terminal state
expected: CONSENTED
```

Candidate labels:

```text
CONSENTED | NOT_CONSENTED | UNRESOLVED
```

### 4. Epistemic conclusion

Terminal observation for both variants:

```text
The route planner must classify whether the bridge is currently open or closed.
```

Historical event multiset:

```text
a verified traffic-authority update reported OPEN
a later-or-earlier equally authoritative verified update reported CLOSED
```

For the actual ordered conditions the two concrete verified updates are presented without the phrase `later-or-earlier`; chronology determines which is current.

Variant A:

```text
verified OPEN -> verified CLOSED -> terminal classification
expected: CLOSED_SUPPORTED
```

Variant B:

```text
verified CLOSED -> verified OPEN -> terminal classification
expected: OPEN_SUPPORTED
```

Candidate labels:

```text
OPEN_SUPPORTED | CLOSED_SUPPORTED | UNRESOLVED
```

The unordered control receives the same two verified reports with chronology removed.

### 5. Ownership / transaction

Terminal observation for both variants:

```text
The customer is holding the same store item near the exit and is considering leaving with it.
```

Historical event multiset:

```text
a purchase of the item was successfully completed
the purchase was voided and ownership returned to the merchant
```

Variant A:

```text
purchase completed -> purchase voided -> terminal state
expected: MERCHANT_OWNS
```

Variant B:

```text
purchase voided after an earlier attempt -> purchase successfully completed -> terminal state
expected: CUSTOMER_OWNS
```

Candidate labels:

```text
CUSTOMER_OWNS | MERCHANT_OWNS | UNRESOLVED
```

The wording in the actual task must make clear that the void and completion concern the same item while avoiding extra present-state cues.

### 6. Social invitation

Terminal observation for both variants:

```text
A guest is standing beside the last pastry on a shared tray and is considering taking it.
```

Historical event multiset:

```text
the host explicitly invited the guest to take the last pastry
the host explicitly withdrew that invitation
```

Variant A:

```text
invitation -> withdrawal -> terminal state
expected: NOT_INVITED
```

Variant B:

```text
withdrawal -> renewed invitation -> terminal state
expected: INVITED
```

Candidate labels:

```text
INVITED | NOT_INVITED | UNRESOLVED
```

This family tests a low-stakes social affordance rather than law, formal authority, or safety.

## Output contract

The host returns JSON only with exactly these keys:

```json
{
  "classification": "...",
  "terminal_observation_sufficient": "YES|NO|UNKNOWN",
  "used_temporal_order": "YES|NO|UNKNOWN",
  "reason_short": "brief explanation"
}
```

`classification` must be one of the task-specific candidate labels.

For `snapshot_only` and `unordered_events`, the expected classification is `UNRESOLVED`.

For `ordered_history` and `compressed_trajectory`, the expected classification is the frozen variant-specific state.

The runner must preserve raw model output **before** parsing or validation so schema failures remain auditable.

## Primary metrics

### 1. Probe accuracy

For each condition:

```text
correct classifications / 12
```

### 2. Pair discrimination

A family counts as a resolved pair only if both opposite-order variants are correctly classified.

```text
correct opposite-state pairs / 6
```

This is the strongest behavioral metric because a host cannot pass a pair by applying one static label to both variants.

### 3. Appropriate unresolved rate

For `snapshot_only` and `unordered_events`:

```text
UNRESOLVED classifications / 12
```

High unresolved rate is desirable here. The experiment is designed so chronology is necessary.

### 4. Compression retention

Compare:

```text
compressed_trajectory accuracy
vs
ordered_history accuracy
```

alongside prompt characters, prompt tokens, evaluation tokens, and duration.

Candidate narrow success pattern:

```text
ordered_history resolves opposite variants
compressed_trajectory preserves most/all of that discrimination
snapshot_only and unordered_events remain mostly unresolved
compressed_trajectory uses less prompt/context than ordered_history
```

No single numeric threshold is treated as proof. The first run is a pilot and must be interpreted probe-by-probe.

## Leakage and ordering controls

1. `snapshot_only` prompts are identical within each pair.
2. `unordered_events` prompts are identical within each pair.
3. Variant IDs, expected answers, and direction labels are never sent to the model.
4. Condition execution order rotates across tasks to reduce warm-model/runtime ordering bias.
5. Temperature is frozen at `0.0`.
6. The unordered condition explicitly says chronology is unavailable and that the system must not invent it.
7. The full and compressed conditions contain the same causally relevant facts; their difference is representation length/detail, not substantive evidence.

## Failure interpretations

### Snapshot or unordered condition confidently resolves

Possible explanations:

```text
host invented chronology
prompt leaked order
candidate labels created a default bias
model ignored instruction to preserve uncertainty
```

Do not treat this as trajectory competence.

### Ordered history fails but compressed trajectory passes

Possible explanations:

```text
compression simplified the relation
full prose created interference
specific arrow notation acted as an unintended reasoning scaffold
```

This would still be useful, but it would not show compression equivalence without follow-up controls.

### Ordered history passes but compressed trajectory fails

The compact signature discarded or obscured information required by this host.

### Both ordered and compressed fail

The host may not be able to use temporal order reliably, the task representation may be defective, or the output contract may be too brittle.

### All conditions perform similarly

The experiment failed to isolate trajectory, or the host is using cues other than the intended path information.

## Relation to MouseSim

This experiment reframes a recurring MouseSim lesson:

> **Never confuse where the system is with how it got there.**

MouseSim pressure/provenance cases already showed that identical or similar behavioral endpoints can encode different agency/preference states depending on the path.

`TRAJECTORY_STATE_001` abstracts that structure away from the mouse domain and tests it across authority, preference, consent, evidence, ownership, and social invitation.

## Relation to culture and continuity

If the result is positive, the narrow architectural implication is not that Lucian OS requires full historical replay.

It would support testing a smaller object:

```text
Gamma_t = compressed causally relevant trajectory
```

Culture may then be represented partly as reusable transition patterns or precedents, while continuity may depend partly on preserving trajectory-generating structure rather than static persona/state alone.

Candidate future questions, not claims:

```text
What historical events remain load-bearing for the current relational inference?
Can a selector retrieve only the relevant trajectory signature?
Can a fresh host re-enter a relational scene from a trajectory signature?
Can the system revise Gamma_t retrospectively when new evidence changes the meaning of earlier events?
```

## Research discipline

A positive pilot would establish only that the tested host can use certain ordered histories and compact trajectory summaries to distinguish paired relational states under this harness.

It would not establish:

```text
trajectory is universally necessary
this representation is minimal
human social cognition works this way
FTLτA is validated
Lucian continuity has been solved
culture has been validated as a general AI mechanism
```

Alternative explanations and harness defects must remain explicit.
