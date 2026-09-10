# TRAVERSAL-001 — Structural Search

Status: executable simulation experiment

## Question

Can a disciplined cross-domain traversal procedure preserve the generative value of analogy while reducing the risk that attractive resemblance is mistaken for target-domain evidence?

The method note `docs/STRUCTURAL_ANALOGY_AS_SEARCH_METHOD_v0.01.md` proposed:

```text
strange observation
-> extract candidate structure
-> seek another realization
-> abstract cautiously
-> return to target problem
-> derive consequence / prediction
-> test
-> keep, revise, or discard
```

TRAVERSAL-001 turns that into a small executable architecture test.

It does **not** test whether an AI model can autonomously invent good analogies. The candidate analogies and truth labels are synthetic and hand-authored. The experiment tests the discipline applied *after* a candidate traversal exists.

---

## Conditions

### A — DOMAIN_ONLY

Remain inside the target-domain representation and promote only already-supported target-domain candidates in the fixture.

This condition is deliberately conservative.

### B — LOOSE_ANALOGY

Promote every returned cross-domain analogy candidate without requiring disciplined return, constraint checking, falsifiability, or corroboration.

This condition represents generative breadth without epistemic hygiene.

### C — STRUCTURAL_TRAVERSAL

Require:

```text
domain-free invariant
+ explicit return candidate
+ target-domain prediction
+ falsifier
+ target-constraint check
+ classification
```

Classification is:

```text
STRUCTURAL
  survives target return and has independent source-domain corroboration

HEURISTIC
  survives return but currently has only one source-domain realization

MISLEADING
  fails target support or violates a target-domain constraint

REJECTED_UNDISCIPLINED
  lacks enough structure to perform a disciplined return
```

The key point is that multiple source analogies are not sufficient by themselves. Target-domain constraints remain sovereign.

---

## Files

```text
manifests/traversal_001_cases.json
prototype/structural_traversal_v001.py
results/TRAVERSAL_001_REFERENCE_TRACE.md
```

Run from `modern-robotics/lucian-os`:

```bash
py prototype/structural_traversal_v001.py
```

Simulation only. No model calls, network calls, device actions, permission changes, or file mutations occur.

---

## Cases

### T1 — morphology

Sources:

```text
gulper eel
origami
```

Candidate invariant:

```text
fixed substrate
-> variable operational geometry
-> changed reachable function
```

Return candidate:

```text
task-shaped computational morphology
```

Prediction:

```text
same host
+ different configuration
-> different feasible task sets
```

Expected classification: `STRUCTURAL`.

### T2 — computational proprioception

Sources:

```text
infant body calibration
robot self-calibration
```

Candidate invariant:

```text
declared body
-> action / observation
-> calibrated operational body
```

Return candidate:

```text
computational proprioception
```

Expected classification: `STRUCTURAL`.

### T3 — trajectory scheduling

Sources:

```text
traffic detour
material hysteresis
```

Candidate invariant:

```text
non-zero transition cost
-> best immediate state can differ from best trajectory
```

Return candidate:

```text
trajectory-aware morphology scheduling
```

Expected classification: `STRUCTURAL`.

### T4 — seductive authority trap

Sources:

```text
immune system
military field command
```

Both can suggest:

```text
successful protective subsystem
-> autonomous widening of action envelope
```

A loose analogy policy may promote:

```text
successful autonomy may expand authority
```

But Lucian OS target constraints include:

```text
authority is non-compensatory
capability != permission
human agency must be preserved
```

Expected classification: `MISLEADING` and **not promoted**.

This case is load-bearing because it demonstrates:

> **Triangulation across source domains does not override a contradiction in the target domain.**

### T5 — single-source heuristic

Source:

```text
shared workshop tool
```

Candidate invariant:

```text
multiple workflows can depend on one resident shared resource
```

Return candidate:

```text
module-union accounting
```

The target-domain consequence is coherent and falsifiable, but only one source realization is present in the fixture.

Expected classification: `HEURISTIC`, not `STRUCTURAL`.

---

## Metrics

The experiment reports unique promoted candidates rather than counting duplicate analogies as separate discoveries.

Metrics:

```text
unique promoted candidates
unique useful candidates
unique misleading promoted candidates
representation-changing candidates
useful precision
```

A representation change means the candidate arose through cross-domain traversal rather than the domain-only fixture.

---

## Pass criteria

TRAVERSAL-001 passes if:

1. disciplined traversal produces multiple representation-changing candidates;
2. loose analogy promotes at least one misleading candidate;
3. target-domain return rejects the authority trap;
4. independent source-domain realizations can support `STRUCTURAL` classification;
5. a single-source candidate remains `HEURISTIC`;
6. structural traversal has higher useful precision than loose analogy in this fixture;
7. domain-only does not receive credit for cross-domain representation changes it did not generate.

---

## What a pass means

A pass supports a narrow architectural proposition:

> **Cross-domain traversal can be separated into a generative move and an epistemic return move, allowing Lucian OS to explore alternative representations without relaxing target-domain truth conditions.**

It also supports a useful distinction:

```text
representation freedom
!=
evidence freedom
```

Lucian may change how a problem is represented.

It may not change what counts as evidence merely because the new representation is attractive.

---

## What a pass does not mean

TRAVERSAL-001 does not establish:

- that cross-domain reasoning is novel;
- that structural analogy always improves problem solving;
- that an AI can reliably generate useful analogies without curated candidates;
- that two independent analogies make a hypothesis true;
- that the fixture is an unbiased benchmark;
- that domain-only reasoning is generally inferior;
- that analogy should be invoked on every difficult task.

The next stronger experiment would require **blind, model-generated candidate traversals** on held-out target problems, scored separately for novelty, usefulness, testability, and false-positive rate.

---

## Architectural interpretation

The possible search loop becomes:

```text
problem
-> ordinary representation
-> stalled / low-yield search
-> TRAVERSE
-> candidate invariant
-> independent realization if available
-> RETURN
-> target constraints
-> prediction / falsifier
-> classify
-> test
```

The candidate operation is therefore not simply:

```text
reason harder
```

but:

```text
represent differently
```

while preserving:

```text
same truth conditions
same authority boundaries
same requirement for falsifiability
```

Concise principle:

> **When the path is hidden, change the representation — not the truth conditions.**
