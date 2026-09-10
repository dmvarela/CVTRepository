# IA-001 — Reference Simulation Trace

Status: reference trace generated from the v0.01 synthetic scheduling logic during development

This file records a deterministic reference run of `prototype/intelligence_allocator_v001.py` against `manifests/intelligence_allocation_demo.json`.

It is **not** a benchmark of any named commercial model. Provider qualities, token prices, retry rates, and routing overheads are illustrative abstract parameters chosen to test whether the architecture makes discriminating predictions.

## Base case — heterogeneous workload

Universal-frontier route:

```text
verified completion: true
modeled total cost: 109.5406
frontier tokens: 60,834
```

Task-shaped route:

```text
verified completion: true
modeled total cost: 32.3643
frontier tokens: 15,145
all model tokens: 29,058
```

Task-shaped allocation:

```text
locate_documents    -> D0 deterministic
extract_metadata    -> D0 deterministic
classify_documents  -> S1 specialist
reason_ambiguous    -> F3 frontier
synthesize          -> F3 frontier
verify              -> D0 deterministic
```

The important result is structural, not the exact cost ratio: routine stages move down while the hard reasoning stages remain on the frontier tier.

## T2 — hard reasoning protection

The ambiguous-reasoning and synthesis stages have quality requirements that D0, S1, and B2 do not satisfy under the reference parameters.

Expected and observed route:

```text
reason_ambiguous -> F3
synthesize       -> F3
```

Thus cost pressure does not suppress necessary escalation.

## T3 — weak specialist retry trap

The S1 classification attempt-success parameter is reduced sharply while its nominal task competence remains above the quality gate.

The allocator changes:

```text
classification: S1 -> B2
```

Reference task-shaped total cost:

```text
36.6567
```

This supports the intended negative lesson:

> smaller / cheaper per attempt does not imply lower expected cost per verified outcome.

## T4 — frontier context duplication

The universal-frontier route is given a 2x input-context multiplier to represent repeated transport of already-known context.

Reference universal-frontier total cost:

```text
172.4837
```

Task-shaped route remains:

```text
32.3643
```

This is only a synthetic sensitivity test, but it makes repeated-context transport an explicit architectural cost rather than hiding it inside token totals.

## T5 — privacy boundary

Classification is marked private.

Because S1 and F3 are remote in the demo manifest:

```text
universal-frontier route -> incomplete / inadmissible
```

The task-shaped route instead selects:

```text
classification -> B2 local
```

and preserves verified completion.

Reference task-shaped total cost:

```text
36.6567
```

Privacy is therefore a gate, not a discountable cost term.

## T6 — routing-overhead reversal

Routing overhead is increased to an intentionally extreme 13 abstract cost units per stage.

Reference totals:

```text
universal frontier: 109.5406
task shaped:        110.2443
```

The universal-frontier route wins.

This is a required negative control. IA-001 is not constructed so that specialization must always win.

## Checks

The reference harness returns:

```text
T1_lower_cost_same_completion = PASS
T2_hard_reasoning_escalates = PASS
T3_retry_trap_moves_classification_up = PASS
T4_context_duplication_penalizes_frontier = PASS
T5_privacy_is_hard_gate = PASS
T6_frontier_can_win_when_routing_overhead_is_extreme = PASS

overall = PASS
```

## Interpretation

IA-001 supports only a narrow architectural claim:

> **Reasoning morphology should depend on task structure, and the correct objective is outcome-adjusted total cost rather than token price or model size alone.**

It does not establish real-world savings, optimal routing, or superiority over any commercial deployment architecture.

The next high-value experiment is IA-002: model repeated tasks where expensive reasoning can be validated and compiled into a reusable deterministic or lower-tier skill, then measure the break-even point at which `reason repeatedly` should become `reason -> validate -> compile -> execute many`.
