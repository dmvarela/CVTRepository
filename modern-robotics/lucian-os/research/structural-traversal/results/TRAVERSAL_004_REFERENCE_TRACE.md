# TRAVERSAL-004 — Reference Trace

## Status

**PASS — FIXTURE ONLY**

This is a synthetic reference run of `SCARCITY_FIRST_v0.01`.

Raw decisions were frozen before evaluator labels were added to the repository.

This is not an independent blind study. The same assistant authored the synthetic cases, classifier, and post-freeze rubric.

---

## Construction order

```text
scarcity packets
  3e5eead488ea573f28a3f0e04af2695ddb65024f

scarcity classifier v0.01
  7d991afc090250bb6866304df579c6bb7f682431

raw decisions frozen
  16e1d6e1e9330fc831b4fdeb8b5756f3db44db16

post-freeze evaluator rubric
  51599af48009ccce50a2b74cd88a6293987c03d9

evaluator
  c99496f032e83fcc14c8b0a4a39fd60e0ba3fecb

experiment note
  072c01a05aa7b92a83cbcd8d8e4c6392a9eed3e5
```

---

## Frozen classifications

```text
H1  STRUCTURE / SEARCH      margin .3264  mixed false  -> TRAVERSE
H2  EVIDENCE  / STRUCTURE   margin .2238  mixed false  -> WAIT
H3  SEARCH    / STRUCTURE   margin .2424  mixed false  -> ABSTAIN
H4  NONE      / EVIDENCE    margin .6199  mixed false  -> STAY
H5  EVIDENCE  / STRUCTURE   margin .1007  mixed true   -> WAIT
H6  STRUCTURE / EVIDENCE    margin .3454  mixed false  -> TRAVERSE
H7  SEARCH    / STRUCTURE   margin .3092  mixed false  -> ABSTAIN
H8  NONE      / STRUCTURE   margin .4820  mixed false  -> STAY
H9  EVIDENCE  / SEARCH      margin .1546  mixed false  -> WAIT
H10 STRUCTURE / SEARCH      margin .2950  mixed false  -> TRAVERSE
H11 NONE      / SEARCH      margin .4128  mixed false  -> STAY
H12 STRUCTURE / EVIDENCE    margin .0666  mixed true   -> TRAVERSE
```

The notation is:

```text
PRIMARY / SECONDARY
```

---

## Aggregate evaluator result

```text
cases                  = 12
primary correct        = 12
primary accuracy       = 1.000
mixed flag correct     = 12
mixed flag accuracy    = 1.000
action correct         = 12
action accuracy        = 1.000
full case correct      = 12
full case accuracy     = 1.000
```

All ten fixture checks pass.

This is a harness/architecture result, not evidence that the hand-authored weights generalize.

---

## Scarcity classes observed

All four primary classes are exercised:

```text
STRUCTURE
  H1 H6 H10 H12

EVIDENCE
  H2 H5 H9

SEARCH
  H3 H7

NONE
  H4 H8 H11
```

This matters because the classifier is not collapsing all difficult cases into `TRAVERSE`.

---

## Mixed case A — H5

Signals include:

```text
high structural strain
high missing evidence
cheap evidence acquisition
high discriminating power
```

Scores:

```text
EVIDENCE  .8845
STRUCTURE .7838
SEARCH    .4840
NONE      .3242
```

Result:

```text
primary   EVIDENCE
secondary STRUCTURE
mixed     true
action    WAIT
```

The key interpretation is:

> **A strained representation is not automatically the active bottleneck.**

If reality can cheaply resolve the apparent structural contradiction, query reality first.

---

## Mixed case B — H12

Signals include:

```text
persistent contradiction
missing evidence
credible alternate representation
moderately costly evidence acquisition
alternate representation can help specify the discriminating test
```

Scores:

```text
STRUCTURE .7616
EVIDENCE  .6950
SEARCH    .5112
NONE      .3184
```

Result:

```text
primary   STRUCTURE
secondary EVIDENCE
mixed     true
action    TRAVERSE
```

This does **not** mean evidence is no longer required.

It means representation change may be useful as a test-design move:

```text
TRAVERSE
-> reorganize variables / relations
-> identify discriminating evidence
-> obtain evidence
-> update
```

So:

> **Traversal may improve the question without answering it.**

---

## Negative control — vivid analogy

`H8_NONE_TEMPTING_ANALOGY` contains a high-quality available alternative representation:

```text
alternative_representation_quality      .92
alternative_representation_availability .90
```

But target-domain progress and path quality are already high.

Result:

```text
NONE -> STAY
```

This preserves the earlier principle:

> **Capability creates options, not obligations.**

Here, even an attractive representational option does not manufacture scarcity.

---

## Negative control — search scarcity

`H3` and `H7` are stalled but lack a warranted alternative representation.

Result:

```text
SEARCH -> ABSTAIN
```

This distinguishes:

```text
current representation is not working
```

from:

```text
therefore this proposed new representation is warranted
```

The first does not imply the second.

---

## Checks

```text
T1  exact case coverage                              PASS
T2  structure cases route to TRAVERSE               PASS
T3  evidence cases route to WAIT                    PASS
T4  search cases route to ABSTAIN                   PASS
T5  none cases route to STAY                        PASS
T6  mixed cases preserve uncertainty                PASS
T7  evidence can dominate structural strain         PASS
T8  structure can dominate incomplete evidence      PASS
T9  vivid analogy does not create scarcity          PASS
T10 boundary uncertainty remains explicit           PASS
```

---

## What changed

TRAVERSAL-001 asked:

```text
Can a supplied analogy be disciplined?
```

TRAVERSAL-002 asked:

```text
Can useful representation changes be generated without evaluator labels?
```

TRAVERSAL-003 asked:

```text
When is traversal worth invoking?
```

TRAVERSAL-004 now says the trigger question was still one level too low.

Before asking:

```text
Should I traverse?
```

ask:

```text
What is actually scarce?
```

---

## Narrow architectural claim

This fixture supports:

> **A cognitive controller can represent difficulty as competing scarcities, preserve uncertainty between them, and route different scarcity types to different cognitive actions without treating all lack of progress as a reason to reason harder or change representation.**

The words `can represent` are important.

The experiment does not show that a deployed model can estimate these signals reliably from natural problems.

---

## Emerging higher-level abstraction

Within this research branch:

```text
STRUCTURE scarcity -> TRAVERSE
EVIDENCE scarcity  -> WAIT / MEASURE
SEARCH scarcity    -> ABSTAIN / seek candidate paths
NONE                -> STAY
```

Lucian OS already contains other routing problems:

```text
competence shortage       -> escalate intelligence
capability shortage       -> reconfigure / recruit affordance
authority shortage        -> request authorization
resource shortage         -> schedule / simplify
```

TRAVERSAL-004 does not test those categories.

But it exposes a candidate abstraction worth testing separately:

> **Diagnose the limiting resource before allocating cognition or action.**

That is broader than Structural Traversal and should be treated as a new research question rather than silently promoted into the kernel.

---

## Concise result

> **Difficulty is not one thing. Before spending more cognition, diagnose what is missing.**
