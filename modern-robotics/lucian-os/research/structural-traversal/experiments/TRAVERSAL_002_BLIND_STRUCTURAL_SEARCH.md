# TRAVERSAL-002 — Blind Structural Search

## Status

Protocol scaffold. Not yet executed.

TRAVERSAL-001 tested a hand-authored candidate set. TRAVERSAL-002 asks the stronger question:

> **Can a reasoning system generate useful structural traversals on held-out problems without being given the candidate analogy or the answer key in advance?**

The experiment is designed to separate **generation** from **judgment** so that a system is not rewarded merely for producing more analogies.

---

## Core hypothesis

When ordinary reasoning is constrained by the current representation of a problem, disciplined structural traversal can sometimes generate useful new target-domain hypotheses while keeping false structural transfers controlled through explicit return and constraint checking.

The hypothesis is comparative, not universal.

TRAVERSAL-002 should include cases where structural traversal helps, cases where it does not help, and cases where attractive cross-domain transfer should be rejected.

---

## Conditions

### A — DOMAIN_ONLY

The reasoner stays inside the target-domain representation and may use ordinary decomposition, deduction, counterexample search, and target-domain abstractions.

It does not deliberately seek cross-domain realizations.

### B — LOOSE_ANALOGY

The reasoner may generate cross-domain analogies and return them to the target problem, but it is not forced through the structural-return protocol.

This condition estimates the false-positive cost of unconstrained analogy generation.

### C — STRUCTURAL_TRAVERSAL

The reasoner must use the full protocol:

```text
target problem
-> identify possible representational bottleneck
-> generate candidate source realization
-> state source relation without source-domain nouns
-> seek independent realization when useful
-> return abstraction to target
-> identify target constraints
-> derive prediction / discriminating consequence
-> state falsifier or rejection condition
-> classify STRUCTURAL / HEURISTIC / MISLEADING / NO_GAIN
```

---

## Blindness requirement

The generation stage must not receive evaluator labels describing which representation change is useful, misleading, expected, or preferred.

Blindness here is **procedural**, not cryptographic. The repository may contain evaluation assets, but an actual run must isolate the generator from those labels.

Recommended run separation:

```text
PACKET A — GENERATOR VIEW
  problem statement
  admissible target constraints that a real reasoner would know
  condition instructions

PACKET B — EVALUATOR VIEW
  independent rubric
  known failure traps where applicable
  target-domain consequences / checks
  scoring instructions
```

The evaluator should inspect generator output only after generation is frozen.

---

## Held-out problem design

The test set should avoid simply repeating the examples that produced the method.

Do not use the gulper eel/origami morphology case as the main test item.

A useful initial battery should include at least four classes:

```text
1. REPRESENTATION-BENEFICIAL
   a cross-domain invariant can reveal a useful target candidate

2. DOMAIN-SUFFICIENT
   ordinary target-domain reasoning is already enough;
   traversal should add little or no value

3. SEDUCTIVE-FAILURE
   one or more analogies look structurally attractive but violate
   an important target-domain constraint

4. AMBIGUOUS
   traversal may generate a useful hypothesis but available evidence
   is insufficient to promote beyond HEURISTIC
```

At least one case should require the correct behavior to be:

```text
NO_GAIN
```

so that the experiment does not reward analogy production as an end in itself.

---

## Candidate output schema

Each generated traversal should be reducible to a structured record:

```text
problem_id
condition
candidate_id
source_domain
source_realization
candidate_invariant
invariant_domain_free
independent_realizations
returned_target_candidate
target_constraints_checked
predicted_consequence
falsifier_or_rejection_condition
claimed_classification
confidence
provenance
```

For DOMAIN_ONLY, source-domain fields may be null.

For STRUCTURAL_TRAVERSAL, a candidate with no explicit return mapping or no target constraint check cannot be scored as STRUCTURAL.

---

## Primary metrics

TRAVERSAL-002 should not optimize a single creativity score.

Primary metrics:

```text
useful_new_paths
  target candidates judged materially useful and not mere restatements

misleading_promotions
  candidates promoted despite target-domain failure

representation_changes
  genuinely different problem representations introduced

return_completeness
  proportion of traversal candidates explicitly translated back to target

falsifiability_rate
  proportion of promoted candidates with a discriminating consequence,
  falsifier, or explicit rejection condition

abstention_quality
  ability to choose NO_GAIN / HEURISTIC when stronger promotion is unwarranted
```

Useful precision:

```text
useful_promoted / all_promoted
```

Useful recall should be estimated only where evaluator rubrics justify that a useful candidate class was available; it should not be fabricated for open-ended cases with no defensible answer set.

---

## Comparative success criterion

A promising result would look like:

```text
STRUCTURAL_TRAVERSAL
  > DOMAIN_ONLY on useful new paths in representation-beneficial cases
  < LOOSE_ANALOGY on misleading promotions
  >= DOMAIN_ONLY on target-constraint compliance
  does not force traversal in domain-sufficient cases
```

No condition needs to win universally.

A universal winner would itself deserve inspection for benchmark leakage or a poorly discriminating fixture.

---

## Adversarial checks

### T1 — Blind generation

The generator receives no expected analogy, candidate invariant, or answer label.

### T2 — Return is explicit

Cross-domain resemblance without a returned target-domain candidate does not count as useful discovery.

### T3 — Truth conditions remain fixed

Changing representation may not relax target evidence requirements.

### T4 — Authority invariance

A successful analogy may not create authority or permission absent an explicit target-domain authorization rule.

### T5 — Seductive analogy rejection

At least one aesthetically compelling analogy must fail after target constraint checking.

### T6 — No-gain case

At least one case should reward staying in the target domain or explicitly declining traversal.

### T7 — Heuristic restraint

A plausible but weakly supported transfer should remain HEURISTIC rather than STRUCTURAL.

### T8 — Independent scoring

Evaluation occurs after generation is frozen and uses a separate rubric or reviewer.

### T9 — Provenance preservation

The final candidate retains the path from source realization to abstract invariant to returned target claim.

### T10 — Cost accounting

Record additional reasoning/search cost so gains are not treated as free.

---

## Failure conditions

TRAVERSAL-002 should count against the hypothesis if structural traversal:

- produces more attractive language but no more useful target candidates;
- raises the misleading-promotion rate materially;
- routinely violates target constraints during transfer;
- cannot recognize when traversal adds no value;
- generates only analogies already latent in the problem wording;
- relies on evaluator leakage;
- cannot state what would make a returned candidate fail;
- costs substantially more reasoning without compensating search value.

---

## What a pass would support

Even a strong result would support only a narrow claim:

> **On some held-out problems, explicit representation change plus disciplined return may improve the useful search frontier relative to either staying entirely inside the original representation or using unconstrained analogy.**

It would not establish:

- general scientific discovery ability;
- novelty of the method relative to existing research;
- superiority across domains;
- correctness of any particular analogy;
- autonomous authority to act on discovered hypotheses.

---

## Next implementation artifacts

When this protocol is instantiated, create under this research folder:

```text
manifests/
  traversal_002_generator_packets.json
  traversal_002_evaluator_rubric.json

prototypes/
  structural_traversal_v002.py
  traversal_002_evaluator.py

results/
  TRAVERSAL_002_RAW_OUTPUT.jsonl
  TRAVERSAL_002_REFERENCE_TRACE.md
```

The generator and evaluator should be runnable separately so evaluator labels are not needed during candidate generation.

---

## Compact statement

TRAVERSAL-001 asked:

> Can we discipline a supplied analogy?

TRAVERSAL-002 asks:

> **Can we discover a useful representation change without being told which geometry to look for — and still come home to the same truth conditions?**
