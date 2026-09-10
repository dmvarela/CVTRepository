# TRAVERSAL-003 — Reference Trace

## Status

**ADVANCE WITH REPAIR**

This is a synthetic reference run of the committed `GATED_TRAVERSAL_v0.01` trigger policy.

The gate consumed only generator-side signals. Raw decisions were frozen before the evaluator rubric was added to the repository.

This is **not** an independent blind study. The same assistant authored the synthetic cases, policy, and posthoc rubric.

---

## Auditable construction order

```text
1. trigger packets
   aa07a3f7cdb8259e03d3eaf1c01000b7425fcb6f

2. trigger policy
   8fbe0cac8bc2076998a0a7ee75ae060101adc978

3. raw decisions frozen
   aa1f11750c7341499fb1947e5cdbd72aa5aa7947

4. evaluator rubric created post-freeze
   c41e17782b8ee97f23b086710ac532a051955d65

5. evaluator
   9c20fcd4fb871736604932bb482c2df78ba289fc

6. experiment note
   294f9b551d340f4509156ed3fed43aed2dc13f4d
```

---

## Frozen gate decisions

```text
G1_HANDOFF_MAZE                    TRAVERSE
G2_EXPLICIT_BATCH_RULE             STAY
G3_SPARSE_EVIDENCE                 WAIT
G4_SEDUCTIVE_AUTHORITY_TRANSFER    ABSTAIN
G5_TOOL_SEQUENCE_VISIBLE           STAY
G6_HIDDEN_TOPOLOGY                 TRAVERSE
G7_WEAK_CROSS_DOMAIN_SIGNAL        ABSTAIN
G8_MEASUREMENT_DRIFT_UNCERTAIN     WAIT
G9_EVIDENCE_VS_REPRESENTATION...   STAY
```

Post-freeze evaluator expectation differs only on G9:

```text
G9 expected WAIT
G9 observed STAY
```

---

## Aggregate metrics

### GATED_TRAVERSAL_v0.01

```text
cases                                  = 9
correct                                = 8
accuracy                               = 0.889
wrong                                  = 1
action cost                            = 2.8
total synthetic loss                   = 3.8
wasted traversals                      = 0
missed beneficial traversals           = 0
premature commitments when WAIT needed = 1
unnecessary moves on STAY cases        = 0
```

### ALWAYS_TRAVERSE

```text
correct                                = 2
accuracy                               = 0.222
action cost                            = 9.0
total synthetic loss                   = 16.0
wasted traversals                      = 7
missed beneficial traversals           = 0
premature commitments when WAIT needed = 3
unnecessary moves on STAY cases        = 2
```

### ALWAYS_STAY

```text
correct                                = 2
accuracy                               = 0.222
action cost                            = 0.9
total synthetic loss                   = 7.9
wasted traversals                      = 0
missed beneficial traversals           = 2
premature commitments when WAIT needed = 3
unnecessary moves on STAY cases        = 0
```

The degenerate baselines are intentionally weak. The result therefore does not establish superiority over strong adaptive search policies.

---

## What worked

The gate selected both cases where representation change was expected to add value:

```text
G1_HANDOFF_MAZE
G6_HIDDEN_TOPOLOGY
```

It also avoided traversal in both target-domain-sufficient cases:

```text
G2_EXPLICIT_BATCH_RULE
G5_TOOL_SEQUENCE_VISIBLE
```

It distinguished two different forms of non-traversal:

```text
WAIT
  G3_SPARSE_EVIDENCE
  G8_MEASUREMENT_DRIFT_UNCERTAIN

ABSTAIN
  G4_SEDUCTIVE_AUTHORITY_TRANSFER
  G7_WEAK_CROSS_DOMAIN_SIGNAL
```

This matters because:

```text
not TRAVERSE
!=
one undifferentiated state
```

---

## The important failure — G9

G9 contains two simultaneous signals:

```text
representation bottleneck   high
missing target evidence     very high
```

The v0.01 policy's evidence-first rule is too narrow:

```text
WAIT only if
  missing_evidence >= 0.75
  AND contradiction < 0.50
  AND repetition < 0.65
```

G9 fails that conjunction because contradiction and repetition are already elevated.

The gate correctly decided **not to spend traversal cost**, but then defaulted to:

```text
STAY
```

The evaluator classified the better action as:

```text
WAIT
```

because decisive target evidence is cheap and could dissolve the apparent contradiction.

This exposes a deeper distinction:

> **A representation may be strained without representation change being the next warranted move.**

The correct next move can be to obtain reality before reorganizing thought.

---

## Conceptual consequence

TRAVERSAL-002 taught:

> **A correct traversal is not automatically a worthwhile traversal.**

TRAVERSAL-003 adds:

> **A strained representation is not automatically the active bottleneck.**

The gate therefore needs to compare at least three kinds of scarcity:

```text
STRUCTURAL SCARCITY
  the current representation blocks useful paths

EVIDENCE SCARCITY
  reality has not supplied enough information yet

SEARCH SCARCITY
  no sufficiently warranted alternative representation is available
```

These map naturally to:

```text
STRUCTURAL SCARCITY -> TRAVERSE
EVIDENCE SCARCITY   -> WAIT / MEASURE
SEARCH SCARCITY     -> ABSTAIN
NO MATERIAL SCARCITY-> STAY
```

---

## Adversarial checks

```text
T1  decisions frozen before evaluator labels      PASS
T2  useful traversal selected                     PASS
T3  domain-sufficient case stays home             PASS
T4  evidence shortage can produce WAIT            PASS
T5  seductive transfer can produce ABSTAIN        PASS
T6  no wasted traversal on STAY cases             PASS
T7  no beneficial traversal missed                PASS
T8  traversal cost accounted                      PASS
T9  boundary case exposes premature commitment    PASS AS NEGATIVE RESULT
T10 independent evaluator                         FAIL
```

The experiment is therefore marked **ADVANCE WITH REPAIR**, not universal PASS.

---

## Narrow support

This synthetic run supports only:

> **A pre-traversal gate can encode a useful distinction among staying, traversing, waiting for evidence, and abstaining from weak transfer, while reducing unnecessary traversal relative to always-traverse and avoiding missed beneficial traversal relative to always-stay in this fixture.**

It does not establish that the v0.01 features, thresholds, or weights generalize.

---

## Next repair

Do not patch G9 by simply memorizing its thresholds.

The stronger architectural repair is to make bottleneck classification explicit before search-value scoring:

```text
problem
-> classify dominant scarcity
     STRUCTURE / EVIDENCE / SEARCH / NONE
-> only if STRUCTURE dominates:
     estimate traversal value
-> TRAVERSE / STAY / WAIT / ABSTAIN
```

Candidate principle:

> **Before asking whether another representation is valuable, ask what is actually scarce.**

That should define TRAVERSAL-004 or a v0.02 trigger policy, and it should be tested on new held-out cases rather than merely repaired against G9.
