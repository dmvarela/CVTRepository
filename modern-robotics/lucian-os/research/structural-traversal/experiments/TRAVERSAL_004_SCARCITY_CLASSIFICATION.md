# TRAVERSAL-004 — Scarcity Classification

## Status

**PASS — FIXTURE ONLY**

This experiment is the architectural repair suggested by TRAVERSAL-003.

TRAVERSAL-003 showed that a representation can be strained while the next warranted move is still to obtain missing evidence rather than traverse. TRAVERSAL-004 therefore inserts an explicit diagnostic stage before search-value allocation:

```text
problem state
-> diagnose active scarcity
-> preserve close secondary scarcity
-> only then choose cognitive action
```

The central question is:

> **Before asking whether another representation is valuable, can Lucian distinguish what is actually scarce?**

---

## Hypothesis

A pre-action scarcity representation can distinguish at least four materially different problem states:

```text
STRUCTURE
  the current representation is the active bottleneck

EVIDENCE
  missing reality is the active bottleneck

SEARCH
  no sufficiently warranted alternate path / representation is available

NONE
  current target-domain reasoning is adequate; no material mode change is justified
```

These states imply different next actions:

```text
STRUCTURE -> TRAVERSE
EVIDENCE  -> WAIT / MEASURE
SEARCH    -> ABSTAIN from unsupported traversal / continue candidate search
NONE      -> STAY
```

The classifier should also preserve mixed cases rather than force false certainty.

---

## Why this is not a threshold patch

TRAVERSAL-003 failed one boundary case because its direct action gate used a narrow conjunction for evidence shortage.

The repair here does **not** add a special rule for that case.

Instead it changes the architecture:

```text
OLD
signals
-> choose STAY / TRAVERSE / WAIT / ABSTAIN

NEW
signals
-> score candidate scarcities
-> identify primary + secondary scarcity
-> preserve margin / mixed state
-> map diagnosis to action
```

This is a representation change in the controller itself.

---

## Generator-side signals

Each held-out synthetic packet contains only observable normalized signals:

```text
target_progress
contradiction_persistence
reformulation_repetition
evidence_missing
evidence_acquisition_cost
evidence_discriminating_power
alternative_representation_quality
alternative_representation_availability
domain_native_path_quality
target_constraint_clarity
```

The generator packet contains no expected scarcity class or expected action.

---

## Classifier v0.01

`SCARCITY_FIRST_v0.01` computes four hand-authored scores.

The weights are not claimed to be learned, optimal, or general.

The important architectural object is not the exact formula but the explicit separation of candidate bottlenecks.

The classifier returns:

```text
primary_scarcity
secondary_scarcity
score_margin
mixed
scores
recommended_action
action_reason
```

A case is marked `mixed=true` when the top two scarcity scores are close and the leading score is materially active.

This prevents:

```text
classification
=
pretend certainty
```

---

## Mixed scarcity policy

The initial mixed rule is deliberately narrow.

When `EVIDENCE` is one of the two leading scarcities:

```text
cheap + highly discriminating evidence
-> WAIT first

structure leads + missing evidence is comparatively costly / weak
-> TRAVERSE, while preserving evidence as unresolved
```

Traversal in the second case does **not** promote a factual conclusion. It may instead reorganize the problem or specify which evidence would discriminate.

Thus:

```text
TRAVERSE
!=
permission to outrun evidence
```

---

## Battery

Twelve new synthetic cases were used.

The battery contains:

- clear structural scarcity;
- cheap decisive evidence scarcity;
- empty / weak search frontier;
- domain-sufficient cases;
- vivid but unnecessary analogy;
- structural strain with noisy rather than missing evidence;
- mixed structure/evidence cases with different relative costs;
- a boundary case with close structural and evidence scores.

The cases were not copied from the TRAVERSAL-003 fixture.

---

## Procedural separation

Construction order:

```text
1. scarcity packets
   commit 3e5eead488ea573f28a3f0e04af2695ddb65024f

2. scarcity classifier
   commit 7d991afc090250bb6866304df579c6bb7f682431

3. raw decisions frozen
   commit 16e1d6e1e9330fc831b4fdeb8b5756f3db44db16

4. evaluator rubric created post-freeze
   commit 51599af48009ccce50a2b74cd88a6293987c03d9

5. evaluator
   commit c99496f032e83fcc14c8b0a4a39fd60e0ba3fecb
```

The evaluator labels did not exist in the repository when the raw decisions were frozen.

This is procedural separation only.

The same assistant authored the cases, classifier, and post-freeze rubric, so the experiment is **not independently blind**.

---

## Result

On this hand-authored fixture:

```text
cases                 12
primary scarcity      12 / 12
mixed-state flag      12 / 12
recommended action    12 / 12
full case match       12 / 12
```

All ten architectural checks pass.

This is recorded as `PASS_FIXTURE_ONLY`, not as evidence that the numerical policy generalizes.

---

## Two mixed cases

### H5 — evidence dominates structural strain

Both `EVIDENCE` and `STRUCTURE` score highly.

But the missing evidence is cheap and strongly discriminating.

Result:

```text
primary   EVIDENCE
secondary STRUCTURE
mixed     true
action    WAIT
```

Interpretation:

> **A representation can be strained without representation change being the next warranted move.**

Reality is cheap enough to query first.

### H12 — structure slightly leads evidence

Both `STRUCTURE` and `EVIDENCE` remain active, but acquiring the missing evidence is moderately costly and the alternate representation can help determine what evidence would actually discriminate.

Result:

```text
primary   STRUCTURE
secondary EVIDENCE
mixed     true
action    TRAVERSE
```

Interpretation:

Traversal is useful here as a **test-design / problem-organization move**, not as a substitute for the missing evidence.

---

## Important negative controls

### Vivid analogy does not manufacture scarcity

`H8_NONE_TEMPTING_ANALOGY` includes a high-quality available analogy while domain-native reasoning is already progressing strongly.

The classifier returns:

```text
NONE -> STAY
```

So:

> **Availability of a representation change does not create a reason to use it.**

### Stalled reasoning does not automatically mean STRUCTURE

The two search-scarcity cases are stalled, but no warranted alternate representation is ready.

The classifier returns:

```text
SEARCH -> ABSTAIN
```

This separates:

```text
representation is bad
```

from:

```text
we have a better representation ready
```

---

## What this fixture supports

A narrow architecture claim:

> **It is coherent and operationally useful to represent the pre-action problem as a scarcity diagnosis rather than directly selecting a cognitive move from undifferentiated signs of difficulty.**

The fixture also supports preserving a secondary scarcity and score margin in boundary cases.

It does **not** establish:

- that these four classes are exhaustive;
- that the weights or thresholds generalize;
- that a model can estimate the signals reliably from raw real-world problems;
- that scarcity-first routing beats strong learned or adaptive baselines;
- that structural traversal is generally useful;
- independent evaluator agreement.

---

## Architectural implication

The research branch began with analogy, but the architecture now points one level higher.

The candidate principle is:

> **Diagnose the limiting resource before allocating cognition.**

Within Structural Traversal the current mapping is:

```text
missing structure -> TRAVERSE
missing evidence  -> WAIT / MEASURE
missing search path -> ABSTAIN / search for candidates
nothing material missing -> STAY
```

Lucian OS has other possible scarcity classes that this experiment did not test:

```text
missing competence
missing computational capability
missing physical affordance
missing authority
missing time / memory / energy
```

Those may map to different operations such as escalation, reconfiguration, authorization requests, or scheduling.

That broader generalization remains a hypothesis for a separate research program.

---

## Next question

TRAVERSAL-004 validates the scarcity-first representation only inside the traversal branch.

The next stronger architectural question is:

> **Does the same scarcity-routing abstraction remain useful when Lucian must choose among measuring, traversing, escalating intelligence, reconfiguring embodiment, requesting authority, scheduling, acting, or abstaining?**

That should not automatically become TRAVERSAL-005, because it is no longer fundamentally a structural-analogy experiment.

It is a candidate **Cognitive Scarcity Router** research program.

---

## Compact result

> **Difficulty is not one thing. Before spending more cognition, diagnose what is missing.**
