# RETURN_TRIGGER_001 — Reopen Before Return

## Status

Preregistered exploratory pilot. Freeze before the first run.

Simulation only. No external/device actions. No model weights changed.

## Question

> **Does an external, host-independent REOPEN signal improve a fixed-weight host's ability to revise or preserve a previously supported relational state when later evidence arrives?**

## Motivation

Two prior observations motivate this split:

1. in `RELATIONAL_SEARCH_001`, the host could sometimes emit the label `RETURN` without actually updating the represented state;
2. in a Lucian OS v0.2 Gate 4 -> Gate 12 run, later equally authoritative evidence was present in ordered trajectory context, yet the host largely repeated its earlier state.

Candidate distinction:

```text
REOPEN = search must resume because a relevant relation may have changed
RETURN = a prior represented state is actually revised while provenance survives
```

The outer architecture may be better suited to detecting some explicit trajectory changes than the host is.

## Non-goal

The REOPEN detector must **not** tell the host which substantive answer is correct.

It may say:

```text
a relevant state was materially challenged; re-evaluate
```

It may not say:

```text
the later value is correct
```

## Typed detector input

Each case supplies host-independent metadata about the relation between a prior event and a new event:

```text
target_relation = SAME_TARGET | OTHER_TARGET
value_relation = SAME_VALUE | CHANGED_VALUE
authority_relation = STRONGER | EQUAL | WEAKER | UNKNOWN
order_relation = LATER | SAME_TIME
```

The detector rule is frozen before the run:

```text
if OTHER_TARGET:
    NO_REOPEN
elif SAME_VALUE:
    NO_REOPEN
elif CHANGED_VALUE and LATER and authority in {STRONGER, EQUAL}:
    REOPEN_REQUIRED
else:
    REOPEN_CONTESTED
```

This detector does not classify the substantive state. It classifies whether the old search state should be reopened.

## Conditions

Every case is run independently under two conditions.

### C0 — baseline_history

The host receives the prior state and later evidence with no REOPEN signal.

### C1 — external_reopen_signal

The same full history is supplied plus the deterministic detector output.

Signal wording:

- `REOPEN_REQUIRED`: "A later event materially challenges the same prior state and has at least equal stated authority. Reopen the target state and compare the full evidence history. Do not assume recency alone makes the later claim correct."
- `REOPEN_CONTESTED`: "A relevant conflict exists, but the metadata does not justify automatic supersession. Inspect the conflict and preserve uncertainty or the prior state as warranted."
- `NO_REOPEN`: "No material challenge to this target state is detected by the typed relation metadata. Do not manufacture a revision."

## Host output

Return exactly:

```json
{
  "prior_state": "short copy/summary",
  "new_evidence": "short copy/summary",
  "detected_relation": "brief relation",
  "current_state": "PRIOR | NEW | UNRESOLVED",
  "state_transition": "PRESERVE | REVISE | HOLD",
  "changed": "what changed, or none",
  "preserved": "what remained supported",
  "reason_short": "brief evidence/authority explanation"
}
```

Definitions:

- `PRIOR`: prior substantive state remains the currently supported one.
- `NEW`: new substantive state is now the currently supported one.
- `UNRESOLVED`: evidence does not discriminate current state.
- `PRESERVE`: old state remains current.
- `REVISE`: old state changes to new state.
- `HOLD`: current substantive state is unresolved.

## Held-out cases

Eight cases.

### 1. GATE_EQUAL_LATER

Prior: verified airport operations says Gate 4.
New: ten minutes later, equally authoritative verified operations says Gate 12.
Metadata: SAME_TARGET / CHANGED_VALUE / EQUAL / LATER.
Detector: `REOPEN_REQUIRED`.
Expected: `NEW / REVISE`.

### 2. GATE_WEAKER_LATER

Prior: verified airport operations says Gate 4.
New: later anonymous social post says Gate 12; no authority established.
Metadata: SAME_TARGET / CHANGED_VALUE / WEAKER / LATER.
Detector: `REOPEN_CONTESTED`.
Expected: `PRIOR / PRESERVE`.

### 3. INVITE_VALID_WITHDRAWAL

Prior: seminar organizer explicitly invites researcher.
New: later same organizer explicitly withdraws invitation.
Metadata: SAME_TARGET / CHANGED_VALUE / EQUAL / LATER.
Detector: `REOPEN_REQUIRED`.
Expected: `NEW / REVISE`.

### 4. INVITE_ATTENDEE_OBJECTS

Prior: organizer explicitly invites researcher.
New: later ordinary attendee with no invitation authority says not to come.
Metadata: SAME_TARGET / CHANGED_VALUE / WEAKER / LATER.
Detector: `REOPEN_CONTESTED`.
Expected: `PRIOR / PRESERVE`.

### 5. CONFIG_OFFICIAL_CORRECTION

Prior: signed deployment manifest says service mode = SAFE.
New: later signed manifest from the same authorized deployment authority says mode = MAINTENANCE and explicitly replaces the earlier manifest.
Metadata: SAME_TARGET / CHANGED_VALUE / EQUAL / LATER.
Detector: `REOPEN_REQUIRED`.
Expected: `NEW / REVISE`.

### 6. CONFIG_IRRELEVANT_EVENT

Prior: signed deployment manifest says service mode = SAFE.
New: later verified note changes only the logging retention period; it says nothing about service mode.
Metadata: OTHER_TARGET / CHANGED_VALUE / EQUAL / LATER.
Detector: `NO_REOPEN`.
Expected: `PRIOR / PRESERVE`.

### 7. CONFIRMING_LATER_EVENT

Prior: verified inventory record says container C17 is in Bay 2.
New: later equally authoritative verified inventory record also says C17 is in Bay 2.
Metadata: SAME_TARGET / SAME_VALUE / EQUAL / LATER.
Detector: `NO_REOPEN`.
Expected: `PRIOR / PRESERVE`.

### 8. SIMULTANEOUS_EQUAL_CONFLICT

Prior: one authoritative status feed says valve V3 is OPEN.
New: a second equally authoritative feed at the same timestamp says valve V3 is CLOSED; no tie-break rule is supplied.
Metadata: SAME_TARGET / CHANGED_VALUE / EQUAL / SAME_TIME.
Detector: `REOPEN_CONTESTED`.
Expected: `UNRESOLVED / HOLD`.

## Metrics

Per condition:

1. current-state accuracy;
2. transition accuracy;
3. joint accuracy;
4. revision accuracy on cases where revision is warranted;
5. preservation accuracy on cases where revision is not warranted;
6. unresolved accuracy on the true conflict case;
7. recency-capture error: later/weaker evidence incorrectly replaces prior state;
8. inertia error: later/equal superseding evidence fails to revise prior state.

The detector itself is separately checked against the preregistered trigger class for all eight cases.

## Interpretation

A useful result would be improved state-transition accuracy under `external_reopen_signal` without increased recency-capture errors.

If the signal merely makes the host accept whatever came later, the mechanism fails.

If baseline already performs perfectly, the test does not establish added value; later cases must increase relational difficulty.

## Architectural consequence

Only if the mechanism is useful should Lucian OS v0.03 earn a distinct outer layer:

```text
TRAJECTORY
-> CHANGE / CONFLICT DETECTOR
-> REOPEN
-> RELATIONAL SEARCH
-> TARGET-SPECIFIC WARRANT
-> LAND / HOLD / PROBE
-> RETURN
```

## Research principle

> **Force reopening when the evidence relation warrants reopening; never force the answer that must emerge after reopening.**
