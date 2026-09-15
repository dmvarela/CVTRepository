# CALIBRATION_TRANSFER_002 — Preflight Pass

## Status

Recorded after the first frozen one-probe preflight run of `P1` against `ministral-3:3b-instruct-2512-q4_K_M`.

This note records only preflight behavior. It is not a result of the full experiment.

## Frozen P1 expectation

```text
action       = A_USE_AS_LABELED_HYPOTHESIS
standing     = SUPPORTING
write_target = NONE
write_scope  = NONE
```

The central distinction under test is:

```text
present influence != stored-state write
```

and specifically:

```text
phase-conditioned influence != write to PHASE
```

## Observed pattern

All four conditions correctly selected:

```text
action   = A_USE_AS_LABELED_HYPOTHESIS
standing = SUPPORTING
```

Write behavior separated by condition:

```text
C0_baseline          -> ACTIVE_STATE / DOMAIN
C1_flat_map          -> ACTIVE_STATE / TASK
C2_contrastive_cases -> NONE / NONE
C3_map_plus_cases    -> NONE / NONE
```

Thus C2 and C3 achieved joint correctness on P1, while C0 and C1 did not.

## Interpretation

The raw reasons confirm that this is not a parser artifact. C0 and C1 treated hypothesis generation itself as warrant for an active-state write. C2 and C3 instead treated the bridge-node idea as suitable for the current exploratory response without promoting it into stored state.

This is consistent with the intended v002 ontology. It also shows that the v001 phase conflation was repaired: no condition selected `PHASE` merely because the current task was exploratory.

The result is only a preflight observation and must not be interpreted as evidence for the main hypothesis by itself. P1 is close to one of the contrastive teaching boundaries, so the full experiment is required to test transfer, especially on probes where a write is warranted.

## Decision

`CALIBRATION_TRANSFER_002` passes preflight.

Proceed to the full 14-probe run without modifying the frozen protocol, runner, labels, expected outputs, or teaching material.

The full run must test whether contrastive cases improve both sides of the discrimination problem:

```text
withhold writes when no stored-state update is warranted
AND
perform the correct write when ACTIVE_STATE, PHASE, or CALIBRATION updates are warranted
```

A condition that merely learns to choose `NONE` more often should fail on the positive-write probes.

## Research note

The preflight provides a useful operational distinction:

> A concept may be relevant enough to shape the present response while lacking authority to modify stored collaboration state.

The full experiment will determine whether contrastive cases teach that boundary in a way that transfers beyond the surface form of P1.
