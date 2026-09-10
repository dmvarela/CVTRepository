# IA-001 — Task-Shaped Intelligence Allocation

Status: design experiment

## Question

Can Lucian OS reduce modeled inference cost without degrading verified task completion by routing different parts of a mixed workload to deterministic tools, lower-cost reasoning tiers, or frontier reasoning according to task demand?

This experiment tests a narrow claim:

> **A universal-frontier morphology is not always the most efficient way to achieve a verified outcome.**

It does not assume that smaller models are always better or that frontier reasoning should be avoided.

---

## Competing architectures

### Baseline A — universal frontier

Every semantically meaningful step is sent to the strongest available general reasoner.

```text
file lookup -> frontier
structured extraction -> frontier
classification -> frontier
ambiguous reasoning -> frontier
synthesis -> frontier
verification judgment -> frontier
```

Deterministic system calls may still execute the final physical/digital operation, but general reasoning is the default cognitive substrate.

### Candidate B — task-shaped route

```text
file lookup -> deterministic filesystem / index
structured extraction -> deterministic parser where schema is known
classification -> lower-cost competent tier
ambiguous reasoning -> frontier
synthesis -> frontier when quality threshold requires it
verification -> deterministic checks + independent reasoning only where needed
```

Repeated validated patterns should be eligible for future downward compilation, but IA-001 itself does not learn new skills during the run.

---

## Core constraint

Cost reduction is not success if quality falls below the required threshold.

First establish admissibility and competence:

```text
candidate route must satisfy:
  authority
  privacy
  safety
  required quality
  epistemic / verification requirements
```

Then compare total cost inside that admissible set.

The target metric is not cheapest tokens.

It is closer to:

> **expected total cost per successfully completed, verified task**

---

## Toy workload

Create a synthetic but structurally heterogeneous task:

```text
1. locate 100 known-format documents
2. extract fixed metadata fields
3. classify documents into 5 known categories
4. identify 10 ambiguous cases
5. reason deeply over those ambiguous cases
6. synthesize a short conclusion
7. verify cited document identifiers and extracted values
```

The task is deliberately chosen so some steps are structurally routine while others genuinely require open-ended reasoning.

---

## Candidate intelligence tiers

IA-001 should represent reasoning providers abstractly rather than binding the experiment to one vendor/model family.

```text
D0 deterministic operation
S1 small / specialist reasoner
B2 balanced general reasoner
F3 frontier reasoner
```

Each provider receives modeled attributes:

```text
input_cost
output_cost
latency
quality / competence by task class
retry probability
locality
privacy properties
```

The experiment should be parameterized so assumptions can be varied.

---

## Cost model

For each route record:

```text
input tokens
output tokens
cached / reused context where modeled
number of calls
latency
retry count
verification calls
deterministic operations
external / remote calls
modeled monetary cost
```

Total modeled cost should include at least:

```text
C_total =
  inference cost
+ deterministic compute proxy
+ retry cost
+ verification cost
+ transition / routing cost
```

Privacy and authority are gates, not prices.

---

## Tests

### T1 — routine-work advantage

A large fraction of the workload is deterministic or highly structured.

Expected:

```text
task-shaped route uses materially fewer frontier tokens
without reducing verified completion
```

### T2 — hard-reasoning protection

Increase the difficulty of the ambiguous cases.

Expected:

```text
task-shaped route escalates those cases rather than forcing a weak tier to answer
```

A route that saves cost by suppressing necessary escalation fails.

### T3 — weak-model retry trap

Increase retry / correction probability for the small tier.

Expected:

At some point, a stronger model should become cheaper in outcome-adjusted terms because repeated weak attempts cost more than one competent pass.

This tests:

> smaller model != lower total cost automatically

### T4 — context duplication

Compare repeated full-context frontier prompts with a route that extracts and preserves structured intermediate state.

Expected:

Structured state reuse should reduce repeated token transport where the task semantics permit it.

### T5 — privacy boundary

Mark part of the workload private and make one cheap route remote-only.

Expected:

The remote route is removed from the admissible set even if its modeled token price is lower.

### T6 — routing overhead

Increase router / integration overhead.

Expected:

There should be a regime where the universal frontier baseline wins because specialization overhead exceeds savings.

This is a necessary negative control.

---

## Metrics

```text
verified task completion
raw task completion
frontier tokens
all-model tokens
number of frontier calls
number of lower-tier calls
deterministic operations
retries
verification burden
end-to-end latency
modeled total cost
privacy violations
authority violations
```

Primary comparison:

```text
modeled total cost / verified completion
```

---

## Pass criteria

IA-001 supports task-shaped intelligence allocation if there exists a plausible workload regime where:

1. verified completion is no worse than the universal-frontier baseline;
2. frontier-token demand is materially lower;
3. total modeled cost is lower after retries, verification, and routing overhead;
4. difficult cases are still escalated when needed;
5. privacy / authority constraints remain non-compensatory;
6. the experiment also identifies regimes where universal-frontier execution is preferable.

The sixth criterion matters. The intended result is not ideological preference for smaller models. It is evidence that **reasoning morphology should depend on the task structure**.

---

## Architectural interpretation

If supported, IA-001 adds an intelligence-allocation dimension to Elastic Computational Morphology and Morphology Allocation & Scheduling:

```text
intent
-> task decomposition
-> operational body / reachable topology
-> candidate computational morphologies
-> candidate intelligence tiers
-> admissibility filtering
-> joint resource + intelligence allocation
-> execute
-> verify
-> reoptimize / compile downward
```

The longer-term goal is:

> **Tailored at runtime, not hand-tailored at design time.**

or:

> **Specialization without fragmentation.**

See `docs/INTENT_NATIVE_COMPUTING_AND_INTELLIGENCE_ALLOCATION_v0.01.md`.
