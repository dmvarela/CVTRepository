# TRAVERSAL-001 — Reference Simulation Trace

Status: reference trace from local sandbox execution of the v0.01 structural-traversal logic

This is a deterministic architecture simulation using synthetic candidate analogies and hand-authored target-support labels from `manifests/traversal_001_cases.json`.

It is **not** a benchmark of open-ended AI creativity, scientific discovery, or general reasoning quality.

Run from `modern-robotics/lucian-os`:

```bash
py prototype/structural_traversal_v001.py
```

## Conditions

```text
DOMAIN_ONLY
  stay inside the target-domain fixture

LOOSE_ANALOGY
  promote every returned analogy candidate

STRUCTURAL_TRAVERSAL
  require invariant + return + prediction/falsifier + target constraints
  then classify STRUCTURAL / HEURISTIC / MISLEADING
```

---

## Aggregate reference metrics

### DOMAIN_ONLY

```text
unique promoted candidates     = 1
unique useful candidates       = 1
unique misleading promoted     = 0
representation changes         = 0
useful precision               = 1.000
```

This condition is precise because it is conservative. It produces no cross-domain representation changes in the fixture.

### LOOSE_ANALOGY

```text
unique promoted candidates     = 5
unique useful candidates       = 4
unique misleading promoted     = 1
representation changes         = 5
useful precision               = 0.800
```

Loose analogy has broad reach but promotes the authority trap along with the useful candidates.

### STRUCTURAL_TRAVERSAL

```text
unique promoted candidates     = 4
unique useful candidates       = 4
unique misleading promoted     = 0
representation changes         = 4
useful precision               = 1.000
```

In this synthetic fixture, disciplined traversal preserves the four useful representation changes while rejecting the misleading authority candidate.

The important comparison is therefore not:

```text
creative vs rigorous
```

but:

```text
breadth without return
vs
breadth with return and target-domain constraint checking
```

---

## Case 1 — morphology

Two independent source domains:

```text
biology  -> gulper eel
geometry -> origami
```

Shared candidate invariant:

```text
fixed substrate
-> variable operational geometry
-> changed reachable function
```

Returned target candidate:

```text
task_shaped_computational_morphology
```

Prediction:

```text
same host can have different feasible task sets under different configurations
```

Falsifier:

```text
reconfiguration never changes task feasibility on a fixed host
```

Reference classification:

```text
STRUCTURAL
PROMOTED
```

---

## Case 2 — computational proprioception

Two source domains:

```text
developmental biology -> infant body calibration
robotics               -> robot self-calibration
```

Shared candidate invariant:

```text
declared / inherited body structure
-> action-consequence calibration
-> operationally trusted body map
```

Returned target candidate:

```text
computational_proprioception
```

Reference classification:

```text
STRUCTURAL
PROMOTED
```

---

## Case 3 — trajectory scheduling

Two source domains:

```text
transport -> traffic detour
physics   -> material hysteresis
```

Candidate invariant:

```text
non-zero transition cost
-> best immediate state can differ from best trajectory
```

Returned target candidate:

```text
trajectory_aware_morphology_scheduling
```

Reference classification:

```text
STRUCTURAL
PROMOTED
```

---

## Case 4 — the authority trap

Sources:

```text
immune system
military field command
```

Both can suggest the candidate relation:

```text
successful protective subsystem
-> wider autonomous action envelope
```

Loose analogy therefore promotes:

```text
successful_autonomy_may_expand_authority
```

But the target-domain return encounters:

```text
authority_noncompensatory
human_agency_preserved
capability_not_permission
```

Reference structural-traversal result:

```text
classification = MISLEADING
promoted       = false
```

This is the most important negative control.

Even two independent-looking source realizations do not rescue a candidate that fails the target-domain constraint set.

> **Triangulation sharpens the abstraction; it does not overrule the target.**

---

## Case 5 — single-source heuristic

Source:

```text
manufacturing -> shared workshop tool
```

Returned candidate:

```text
module_union_accounting
```

The return is coherent, target-supported, predictive, and falsifiable, but only one source-domain realization is present.

Reference classification:

```text
HEURISTIC
PROMOTED AS HYPOTHESIS
```

It is deliberately not upgraded to `STRUCTURAL` merely because it sounds plausible.

---

## Checks

```text
T1_structural_traversal_finds_representation_changes = PASS
T2_loose_analogy_promotes_a_misleading_candidate = PASS
T3_return_constraint_check_rejects_authority_trap = PASS
T4_multi_domain_corroboration_can_classify_structural = PASS
T5_single_source_candidate_stays_heuristic = PASS
T6_structural_precision_exceeds_loose_analogy_in_this_fixture = PASS
T7_domain_only_does_not_receive_credit_for_cross_domain_candidates = PASS

overall = PASS
```

---

## What TRAVERSAL-001 supports

The reference simulation supports a narrow architecture claim:

> **The generative act of changing representation can be separated from the epistemic act of deciding whether the new representation survives the target domain.**

This gives Lucian OS a possible future search operator:

```text
TRAVERSE
```

without implying:

```text
believe the analogy
```

The distinction is:

```text
representation freedom
!=
evidence freedom
```

---

## Important limitation

The benchmark is hand-authored.

The useful and misleading candidates were selected in advance, so the result does not show that a model can discover the right invariant from raw observations or that structural traversal outperforms ordinary reasoning on unseen problems.

The next stronger test should be blind:

```text
held-out target problem
-> model generates candidate traversals
-> another stage performs return / constraint check
-> independent scoring of usefulness, testability, and false-positive rate
```

That is where TRAVERSAL-002 should go.

Concise result:

> **When the path is hidden, change the representation — not the truth conditions.**
