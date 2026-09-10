# Structural Traversal Research Program

## Status

Active Lucian OS research program.

This folder isolates work on a candidate search capability:

> **When the current representation of a problem is not yielding a path, change the representation without changing the truth conditions.**

Structural traversal is not the whole of Lucian OS. It is a research program exploring whether cross-domain representation changes can become a disciplined, testable search operator rather than an informal analogy habit.

The central rule is:

> **Representation freedom != evidence freedom.**

A traversal may generate a new way of seeing the problem. The returned target-domain claim must still survive the target's constraints, evidence, falsifiers, authority boundaries, and negative results.

---

## Research question

Can a system improve search by deliberately moving between representations, extracting relational or transformational invariants, and returning those invariants to the original problem under unchanged truth conditions?

A canonical traversal is:

```text
problem
-> detect representational bottleneck
-> traverse to another realization
-> strip domain-specific nouns
-> extract candidate invariant
-> seek independent realization when useful
-> return to target domain
-> derive consequence / prediction
-> adversarially inspect
-> classify
```

Candidate classifications:

```text
STRUCTURAL
  the abstraction survives return and target-domain constraint checking

HEURISTIC
  useful hypothesis generator, but evidence or triangulation is incomplete

MISLEADING
  transferred structure fails target-domain constraints or evidence
```

---

## Origin and provenance

The method note that motivated this program remains in the main Lucian OS documentation:

- `../../docs/STRUCTURAL_ANALOGY_AS_SEARCH_METHOD_v0.01.md`

TRAVERSAL-001 remains in the original flat layout as provenance and should not be moved merely for cosmetic consistency:

- `../../experiments/TRAVERSAL_001_STRUCTURAL_SEARCH.md`
- `../../manifests/traversal_001_cases.json`
- `../../prototype/structural_traversal_v001.py`
- `../../results/TRAVERSAL_001_REFERENCE_TRACE.md`

TRAVERSAL-001 was a hand-authored synthetic architecture test. Its narrow result was that the generative act of changing representation can be separated from the epistemic act of deciding whether the returned representation survives the target domain.

It did **not** establish open-ended discovery ability or general superiority over ordinary reasoning.

From TRAVERSAL-002 onward, new work belongs under this research-program folder.

---

## Folder convention

```text
research/structural-traversal/
  README.md
  experiments/
  manifests/
  prototypes/
  results/
  notes/
```

Subfolders are created as files are needed rather than populated with empty placeholders.

---

## Experimental progression

```text
TRAVERSAL-001
  supplied candidate analogies
  supplied target-support labels
  tested return discipline and filtering

TRAVERSAL-002
  held-out target problems
  generation separated from evaluation
  candidate traversals not supplied in advance
  test useful discovery + false-positive control

future
  trigger policy: when should traversal occur?
  cost policy: when is traversal worth the extra reasoning?
  memory policy: which successful traversals become reusable structure?
  integration: how does TRAVERSE interact with ordinary search and escalation?
```

---

## Promotion criteria

A research result should not move into Lucian OS core merely because it is interesting.

A candidate `TRAVERSE` primitive should require evidence that it can:

1. generate representation changes not simply restate the target vocabulary;
2. return candidates to the target domain explicitly;
3. preserve target-domain constraints and authority boundaries;
4. produce predictions, tests, or discriminating consequences when appropriate;
5. reject seductive but structurally invalid transfers;
6. abstain when traversal adds no value;
7. preserve provenance from source analogy to returned claim;
8. avoid claiming evidence merely from cross-domain resemblance;
9. show value on held-out problems rather than only hand-authored fixtures;
10. justify its computational cost relative to simpler reasoning routes.

Until those conditions survive stronger experiments, structural traversal remains a research capability, not a kernel guarantee.

---

## Architectural boundary

The intended future shape is:

```text
ordinary search
      |
      | stalled / representation bottleneck
      v
TRAVERSE
      |
      v
candidate representation changes
      |
      v
RETURN + TARGET CONSTRAINT CHECK
      |
      +--> reject
      +--> retain as heuristic
      +--> promote to testable target hypothesis
```

`TRAVERSE` must never mean `believe the analogy`.

The strongest compact formulation remains:

> **Analogy opens the path; evidence decides whether the path is real.**

And the search question that originated the program is:

> **There is a geometry here. Where else does this geometry live?**
