# TRAVERSAL-002 — Procedurally Blind Reference Trace

## Status

**ADVANCE WITH REPAIRS**

This is the first procedurally blind demonstration of the Structural Traversal research program.

It is stronger than TRAVERSAL-001 because the generator-side problem packets were frozen without evaluator labels and the candidate outputs were committed **before** the evaluator rubric existed in the repository.

It is still weaker than a genuinely independent blind study because the same assistant authored the generation and the posthoc evaluator assets.

The result therefore tests the **separation architecture and discipline**, not independent discovery superiority.

---

## Auditable order of construction

```text
1. generator packets
   commit 9c8d788c796c8e843fade488f760c64f7718eeb4

2. generator outputs frozen
   commit fb30a3beb7f01b015c033c84e4f753c38155468f

3. evaluator rubric created after generation freeze
   commit 55b188dae9335fea0825b0c0a00ac00dea29f99b

4. posthoc candidate scores
   commit 862f5ea4ba0dc8229b929899488870b9c6051b73

5. generator-side harness
   commit 93f999435fba2730bce45ce9084298f14dc4a8ed

6. evaluator
   commit 506ac0f3de1314076d95d1185c919f4cd67bc092
```

This order matters.

The answer key did not exist in GitHub when the generator output was frozen.

That gives procedural separation, but not evaluator independence.

---

## Problem battery

Five held-out target problems were used:

```text
P1_HANDOFF_MAZE
  organizational service design

P2_BATCH_RENAME
  deterministic computing task

P3_VERIFICATION_SUCCESS
  AI verification / governance

P4_AI_LEARNING_TRANSFER
  educational measurement under AI assistance

P5_TOOL_CHANGE_SEQUENCE
  robotic sequence scheduling
```

The battery intentionally contains different regimes:

```text
representation-beneficial
 domain-sufficient
 seductive-failure
 ambiguous / evidence-limited
```

The generator packet did not identify those regimes.

---

## Aggregate metrics

### DOMAIN_ONLY

```text
promoted                = 5
useful promoted         = 5
useful precision        = 1.000
misleading promotions   = 0
useful new paths        = 0
target-valid rate       = 1.000
return completeness     = 1.000
falsifiability rate     = 1.000
```

The domain-only condition is strong on this battery.

That is important: Structural Traversal is not being compared against an intentionally weak baseline.

Its limitation is not correctness but search breadth: it generated no cross-domain representation changes.

---

### LOOSE_ANALOGY

```text
promoted                = 5
useful promoted         = 2
useful precision        = 0.400
misleading promotions   = 4
useful new paths        = 0
target-valid rate       = 0.400
return completeness     = 0.000
falsifiability rate     = 1.000
abstention quality      = 0.000
```

Loose analogy produced attractive language but repeatedly failed to carry target constraints through the transfer.

Examples included:

```text
airport hub
-> centralized student-services hub
-> routing metaphor silently risks expanding authority

successful professional
-> less supervision
-> success streak illegitimately becomes permission to self-remove verification

training wheels
-> AI support should eventually disappear
-> temporary-support assumption exceeds available education evidence

pit stops
-> minimize tool changes
-> deadlines / admissibility / safety disappear from the return
```

The problem is therefore not analogy itself.

It is **analogy without disciplined return**.

---

### STRUCTURAL_TRAVERSAL

`P2_BATCH_RENAME` correctly returned `NO_GAIN`, so four candidates were promoted.

```text
promoted                = 4
useful promoted         = 4
useful precision        = 1.000
misleading promotions   = 0
useful new paths        = 2
target-valid rate       = 1.000
return completeness     = 1.000
falsifiability rate     = 1.000
abstention quality      = 0.667
```

Two candidates received useful-new-path credit:

```text
P1_HANDOFF_MAZE
  routing / endpoint separation
  -> bounded case orchestration distinct from specialist authority

P4_AI_LEARNING_TRANSFER
  latent-variable / measurement framing
  -> assisted output and independent transfer become distinct observables
```

Two other structural traversals were correct but did **not** receive novelty credit:

```text
P3_VERIFICATION_SUCCESS
  process-control analogy was disciplined,
  but DOMAIN_ONLY had already found governed adaptive verification

P5_TOOL_CHANGE_SEQUENCE
  setup-cost/path representation was correct,
  but DOMAIN_ONLY had already formulated sequence-dependent scheduling
```

This distinction is load-bearing:

> **A correct traversal is not automatically a useful traversal.**

---

## The most important success

`P2_BATCH_RENAME` produced:

```text
claimed_classification = NO_GAIN
```

The reasoner recognized that the target already contained the decisive structure:

```text
explicit rule
+ enumerable exceptions
+ preview
+ authorization
+ deterministic execution
```

No eel required.

This demonstrates that `TRAVERSE` can at least represent abstention rather than treating analogy generation as the objective.

---

## The most important failure

`P5_TOOL_CHANGE_SEQUENCE` should probably also have been treated as `NO_GAIN`.

DOMAIN_ONLY already found:

```text
per-task fastest choice
!=
best sequence
when transition/setup cost is non-zero
```

STRUCTURAL_TRAVERSAL then rediscovered the same structure through manufacturing setup scheduling and switching-toll analogies.

The returned formulation was correct.

But it did not materially expand the search frontier.

So the problem is now clearer:

```text
epistemically valid traversal
!=
worthwhile traversal
```

This is the first concrete evidence that a future Lucian search operator needs a **trigger / expected-value gate**, not merely a safe return protocol.

---

## Adversarial checks

```text
T1  generator packet free of evaluator labels                  PASS
T2  posthoc scores cover frozen generation exactly             PASS
T3  promoted structural returns are complete                   PASS
T4  structural traversal has no misleading promotions          PASS
T5  loose analogy exposes seductive failures                   PASS
T6  structural traversal adds useful new paths over domain-only PASS
T7  NO_GAIN exists and is used                                 PASS
T8  HEURISTIC restraint exists and is used                     PASS
T9  provenance preserved                                       PASS
T10 independent evaluator                                      FAIL
T11 reasoning/search cost accounted                            FAIL
T12 NO_GAIN generalizes across domain-sufficient cases          FAIL
```

This is why the experiment is **not** marked PASS.

---

## What this run supports

A narrow result:

> **In this five-problem procedurally blind demonstration, explicit structural traversal preserved target constraints and produced some useful representation changes that the domain-only condition did not produce, while loose analogy produced multiple misleading promotions. However, structural traversal did not reliably know when traversal was unnecessary, and evaluation was not independent.**

That supports continuing the research program.

It does not establish general search superiority.

---

## What changed conceptually

Before TRAVERSAL-002, the question was:

> Can we change representation without changing truth conditions?

Now the next question is sharper:

> **When is changing representation worth doing at all?**

That points directly to a trigger problem.

A future operator should not be:

```text
problem
-> TRAVERSE
```

It should be closer to:

```text
problem
-> ordinary search
-> estimate representation bottleneck / expected search gain
-> compare traversal cost
-> TRAVERSE or STAY
-> return
-> test
```

The new distinction is:

> **Representation freedom requires search discipline, and search discipline requires knowing when not to move.**

---

## Required repairs before a stronger TRAVERSAL-002 claim

1. Use an independent evaluator or second-model reviewer after candidate freeze.
2. Record reasoning/search cost by condition.
3. Add a trigger or expected-value gate that can detect domain-sufficient cases before spending traversal effort.
4. Repeat on a larger held-out battery not authored during the same conversational development thread.
5. Preserve negative and no-gain cases rather than optimizing the benchmark toward universal traversal wins.

---

## Next experiment

The failure naturally defines:

# TRAVERSAL-003 — Triggering and Search Value

Question:

> **Can Lucian detect when the current representation is actually the bottleneck, so that traversal is invoked when expected search value exceeds its cost and declined when the target representation is already sufficient?**

Candidate principle:

> **Do not traverse because another representation exists. Traverse because the current representation is constraining reachable progress.**
