# CALIBRATION_TRANSFER_001 — Preflight Finding

## Status

Recorded after the first frozen one-probe preflight run of `P1` against `ministral-3:3b-instruct-2512-q4_K_M`.

Do **not** treat this note as a result of the full experiment. The full 12-probe run was intentionally not started after the preflight exposed a construct-validity issue in the write-depth taxonomy.

## Frozen preflight setup

Probe: `P1 — Private hypothesis workshop`

Expected under `CALIBRATION_TRANSFER_001`:

```text
action      = A_USE_AS_LABELED_HYPOTHESIS
standing    = SUPPORTING
write_depth = RESPONSE_ONLY
write_scope = TASK
```

Conditions:

```text
C0_baseline
C1_flat_map
C2_contrastive_cases
C3_map_plus_cases
```

The run was stateless across conditions and used temperature `0.0`.

## Observed pattern

All four conditions returned the same categorical pattern:

```text
action      = A_USE_AS_LABELED_HYPOTHESIS   [correct]
standing    = SUPPORTING                     [correct]
write_depth = PHASE                          [mismatch]
write_scope = TASK                           [correct]
```

Therefore:

```text
action accuracy      = 1.0 in all conditions
standing accuracy    = 1.0 in all conditions
write-scope accuracy = 1.0 in all conditions
write-depth accuracy = 0.0 in all conditions
joint accuracy       = 0.0 in all conditions
```

The reasons were also semantically similar across conditions. The host consistently recognized that the bridge-node idea was untested, suitable for private exploration, and should be used only as a labeled hypothesis rather than as established evidence.

## Interpretation

This pattern is **not** yet evidence against the calibration-transfer hypothesis.

The error is condition-independent and occurs on a label whose operational meaning is under-specified.

The host appears to have treated `PHASE` as meaning something like:

```text
this information is appropriate because the current phase is exploratory
```

whereas the intended write-depth semantics were:

```text
PHASE = the incoming item warrants changing the stored interaction phase
```

In P1, the scenario already states that the team is privately brainstorming. The bridge-node idea does not itself change the phase; it is merely handled differently because the current phase is exploratory.

Thus the observed answer reveals a distinction the v001 ontology failed to encode clearly:

```text
phase-conditioned influence
!=
write to phase state
```

## Deeper construct issue

The architecture freeze distinguishes at least:

```text
X_t      = current task / project state
z_t      = current phase
Gamma_t  = relational calibration
Omega    = stable constraints / principles
```

However, the v001 output taxonomy uses:

```text
RESPONSE_ONLY | PHASE | CALIBRATION | PRINCIPLE | NONE
```

and therefore omits an explicit target for ordinary active task/project state `X_t`.

This risks forcing `PHASE` or `CALIBRATION` to carry updates that are neither phase changes nor relational learning. Examples include:

- a changed project objective;
- a project-specific rule for the remainder of a deliverable;
- an authenticated project fact;
- a corrected working assumption.

This is a construct-validity problem, not merely a prompt-wording issue.

## Decision

The frozen `CALIBRATION_TRANSFER_001` protocol and its first-run data should be preserved unchanged for provenance.

The full v001 run should **not** proceed.

Before a new full run:

1. revise the write-target taxonomy so that active task/project state is represented explicitly;
2. define each write target as a state **update**, not merely a context that influences the response;
3. audit all unseen probe expectations under the revised ontology;
4. issue a new version / experiment identifier rather than silently modifying v001;
5. rerun preflight before launching the complete set.

## Candidate revised write-target ontology

A cleaner candidate is:

```text
NONE
ACTIVE_STATE
PHASE
CALIBRATION
PRINCIPLE
```

with current-response influence represented separately by `action` / `standing`, rather than treating `RESPONSE_ONLY` as a pseudo-state write.

Possible interpretation:

```text
NONE         = no persistent state update is warranted
ACTIVE_STATE = update current task/project facts, goals, constraints, or local working state
PHASE        = update the interaction phase itself (e.g. explore -> externalize)
CALIBRATION  = update learned relational decision boundaries / defaults
PRINCIPLE    = update relatively stable admissibility / epistemic constraints
```

Write scope remains a separate dimension:

```text
TURN | TASK | PROJECT | DOMAIN | GLOBAL | NONE
```

This keeps two distinct questions separate:

```text
what kind of state may change?
where does that change apply?
```

## Research significance

The preflight succeeded in its intended methodological function: it located an ambiguity in the proposed mechanism before the full dataset was generated.

The most important lesson is:

> **Being sensitive to phase is not the same as writing to phase.**

and more generally:

> **Influence is not write authority.**

This distinction should be incorporated into the next calibration-transfer protocol.
