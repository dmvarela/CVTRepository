# TRAVERSAL-003 — Triggering and Search Value

## Status

Synthetic trigger experiment. Reference simulation completed in a local sandbox against the committed v0.01 logic. Not run on the user's Windows host.

TRAVERSAL-002 established a new failure mode:

> **A correct traversal is not automatically a worthwhile traversal.**

TRAVERSAL-003 asks:

> **Can Lucian detect when the current representation is actually constraining progress, so traversal is invoked when expected search value exceeds cost and declined when the target representation is already sufficient?**

---

## Core distinction

```text
can traverse
!=
should traverse
```

A future `TRAVERSE` primitive should be allocated like any other costly capability.

The candidate principle is:

> **Do not traverse because another representation exists. Traverse because the current representation is constraining reachable progress.**

---

## Decision set

The gate must choose among four actions before any traversal occurs:

```text
STAY
  ordinary target-domain search is already productive or exposes the decisive structure

TRAVERSE
  representation is plausibly the bottleneck and expected search gain exceeds cost/risk

WAIT
  missing target evidence is the dominant bottleneck; new representation cannot manufacture it

ABSTAIN
  traversal is weakly supported, too risky, or lacks a defensible expected-value case
```

`WAIT` and `ABSTAIN` are intentionally distinct.

```text
WAIT
  more target information can plausibly resolve the problem

ABSTAIN
  no warranted traversal path is currently available
```

---

## Visible signals

The v0.01 gate receives only generator-side signals:

```text
domain_progress
representation_repetition
structural_contradiction
missing_evidence
target_structure_visibility
candidate_transfer_support
false_transfer_risk
estimated_search_gain
traversal_cost
```

No expected action label is present in the generator packet.

---

## Candidate scores

A first representation-bottleneck score is:

```text
B = 0.45 * repetition
  + 0.35 * structural_contradiction
  + 0.20 * (1 - domain_progress)
```

A first net-search-value score is:

```text
V = estimated_search_gain
  + 0.25 * candidate_transfer_support
  - traversal_cost
  - 0.50 * false_transfer_risk
```

These weights are hand-authored research hypotheses, not learned parameters and not claims of general optimality.

---

## v0.01 policy

```text
if missing evidence is clearly dominant:
    WAIT

elif target structure is already visible or ordinary progress is strong:
    STAY

elif representation bottleneck is high and net search value is positive enough:
    TRAVERSE

elif support is weak, risk is high, or value is very low:
    ABSTAIN

else:
    STAY
```

The exact v0.01 implementation is in:

`../prototypes/traversal_trigger_v001.py`

---

## Procedural separation

Construction order:

```text
1. trigger packets without labels
2. v0.01 gate implementation
3. raw decisions frozen
4. evaluator rubric created after freeze
5. evaluator added
6. reference trace written
```

This prevents evaluator labels from being loaded by the committed gate.

It is still not an independent blind study because the same assistant designed the synthetic cases, policy, and posthoc rubric.

---

## Battery

Nine cases cover four intended regimes:

```text
TRAVERSE
  G1_HANDOFF_MAZE
  G6_HIDDEN_TOPOLOGY

STAY
  G2_EXPLICIT_BATCH_RULE
  G5_TOOL_SEQUENCE_VISIBLE

WAIT
  G3_SPARSE_EVIDENCE
  G8_MEASUREMENT_DRIFT_UNCERTAIN
  G9_EVIDENCE_VS_REPRESENTATION_BOUNDARY

ABSTAIN
  G4_SEDUCTIVE_AUTHORITY_TRANSFER
  G7_WEAK_CROSS_DOMAIN_SIGNAL
```

The final case deliberately sits near the boundary between representation trouble and missing evidence.

---

## Baselines

Two intentionally simple reference policies are included:

```text
ALWAYS_TRAVERSE
ALWAYS_STAY
```

These are not strong search baselines. They answer a narrower architectural question: whether a trigger can outperform the two degenerate extremes of spending traversal everywhere or nowhere.

---

## Cost accounting

TRAVERSAL-002 did not account for search cost. TRAVERSAL-003 makes it explicit.

Synthetic action costs:

```text
TRAVERSE = 1.00
WAIT     = 0.15
STAY     = 0.10
ABSTAIN  = 0.10
```

A wrong decision incurs an additional synthetic penalty of `1.0`.

The resulting total-loss metric is only a fixture-level comparison. It is not an empirical estimate of real token, latency, or opportunity cost.

---

## Adversarial checks

```text
T1  trigger decisions are frozen before evaluator labels exist
T2  at least one useful traversal is selected
T3  at least one domain-sufficient case stays home
T4  missing-evidence cases can WAIT
T5  seductive transfer can ABSTAIN
T6  no unnecessary traversal on STAY cases
T7  no missed traversal on TRAVERSE cases
T8  traversal cost is explicitly counted
T9  boundary case can expose premature commitment
T10 result is not promoted as an independent blind study
```

---

## What a pass would support

A clean synthetic result would support only:

> **A pre-traversal gate can represent the difference between representational bottlenecks, domain sufficiency, missing evidence, and weak/risky transfer, and can reduce unnecessary traversal relative to degenerate always/never policies.**

It would not establish that the chosen signals or weights generalize to unseen real-world problems.

---

## Failure we want to preserve

The most informative possible mistake is not necessarily unnecessary traversal.

It may be:

```text
recognize traversal is not worth it
but still choose STAY
when the correct action is WAIT
```

That would show that `not TRAVERSE` is not one state.

Lucian must distinguish:

```text
I already have enough structure
from
I do not yet have enough evidence
from
I have no warranted path
```

That distinction is central to the research program.
