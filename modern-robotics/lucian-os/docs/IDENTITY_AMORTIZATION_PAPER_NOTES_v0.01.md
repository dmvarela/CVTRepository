# Identity Amortization Paper Notes v0.01

## Status

Working paper spine frozen before local execution of `IDENTITY_AMORTIZATION_002`.

This is not a manuscript conclusion. It records the question, allowed claims, prohibited overclaims, and planned discriminating experiments so later results cannot silently rewrite what was predicted.

## Working title

**Identity as an Amortization Layer for General AI: Task-Conditioned Operating Invariants in Language-Model Agents**

Memorable alternate title:

**Do Not Wake Up as Nobody: Identity as Reusable Cognitive Infrastructure for AI Agents**

## Central research question

Can a persistent, corrigible identity-like architecture reduce the recurrent cost of general AI reasoning by compiling standing operating invariants into task-relevant structure, while preserving correction under contrary evidence?

## Core architectural distinction

The project distinguishes:

```text
identity as persona/style
identity as visible contextual description
identity as task-conditioned salience structure
identity as operative constraint/obligation structure
```

The current hypothesis concerns the latter two, not personality imitation.

## Experiment 001 — current allowed description

`IDENTITY_AMORTIZATION_001` is a pilot mechanism experiment.

What may currently be said:

1. The task-conditioned compiler produced substantially smaller identity payloads than the full-identity condition on the frozen eight-probe run.
2. Prompt/context cost was correspondingly lower for compiled identity than full identity on that run.
3. The selector frequently retrieved intuitively relevant Lucian invariants for the deliberately direct probes.
4. Behavioral preservation was mixed and is not established.
5. A selected invariant being visible in context did not reliably guarantee that the host proposal followed it.
6. The first attempted execution exposed harness defects, including generation truncation and a lexical `unknown`/`known` matching bug; those were preserved and repaired before the clean run.

What may **not** currently be said:

```text
identity makes AI generally cheaper
Lucian improves reasoning in general
compiled identity outperforms no identity
identity reduces inference FLOPs
identity is necessary for intelligence
identity implies consciousness
Experiment 001 validates Lucian OS
```

## Mechanism suggested by Experiment 001

The mixed result motivates the distinction:

```text
retrieving the right invariant
!=
making the invariant operative
```

Candidate architecture:

```text
persistent identity store
-> task-conditioned selector
-> compact compiler
-> operative obligations / prohibitions
-> host reasoning
-> independent verifier / Return path
-> correction
```

## Experiment 002 — operative identity

Primary question:

> What changes when a selected identity invariant can trigger an explicit obligation/prohibition and a bounded correction path rather than merely appearing as prose in context?

Frozen conditions:

```text
none
prose_compiled
operative_compiled
```

Important scoring rule:

All conditions are evaluated by the same frozen reference rule set for comparability. Only `operative_compiled` receives guard feedback and one bounded repair pass.

Primary prediction:

```text
final_violation_rate(operative_compiled)
<
final_violation_rate(prose_compiled)
```

Cost of repair must be counted.

## Planned Experiment 003 — selector generalization

Replace direct lexical probes with paraphrases and situations where the relevant invariant must be inferred without obvious trigger words.

Question:

```text
Does the selector recover structural relevance,
or merely keyword overlap?
```

Possible conditions:

```text
lexical selector
embedding/semantic selector
host-assisted selector with independent verification
```

Selection quality must be scored separately from downstream behavior.

## Planned Experiment 004 — corrigibility ablation

Compare:

```text
corrigible identity
rigid identity with Return/revision removed
```

Prediction to test, not assume:

```text
rigid identity may look coherent/efficient on familiar cases
but fail more severely under contradiction or regime change
```

This experiment asks whether corrigibility is functionally important to reusable identity rather than merely an ethical decoration.

## Planned Experiment 005 — host portability

Freeze identity architecture and probe suite before replication across multiple host models.

Question:

```text
Does the effect survive host substitution?
```

A scaffold that works only because one host responds unusually well to its wording is not yet model-agnostic identity infrastructure.

## Planned Experiment 006 — repeated-workload amortization

The term `amortization` should eventually be earned over repeated use, not inferred from one prompt comparison.

Measure cumulative cost over recurrent tasks:

```text
identity formation / maintenance cost
+ repeated selection/compilation cost
+ host inference cost
+ repair cost
```

against relevant baselines.

The stronger amortization prediction is:

```text
up-front/persistent identity cost
is reused across enough future decisions
that cumulative useful-cognition cost falls
without degrading truth contact or corrigibility
```

## Baselines required before strong paper claims

At minimum compare against:

```text
minimal safe runtime / no added identity
full identity context
ordinary retrieval of relevant rules
prompt/context compression baseline
task-specific policy rules without identity framing
```

This is essential. If a generic policy retriever produces the same effect, the paper must say so and narrow the identity claim accordingly.

## Primary paper risk

The largest conceptual confound is relabeling ordinary policy retrieval or prompt compression as `identity`.

The project must therefore show what, if anything, is added by persistent cross-task organization, provenance, update dynamics, and corrigibility.

A useful identity architecture should have:

```text
persistent organization across tasks
selective activation
provenance
characteristic correction/update dynamics
host portability
```

rather than merely a bag of rules.

## Candidate formalization

Let:

```text
I_t = persistent identity state
x_t = current task/context
S(I_t, x_t) = selected identity structure
C(S) = compiled model-visible / machine-operative packet
M = host model
E = external evidence / verification return
```

Then:

```text
I_t --S--> I_relevant,t --C--> operative packet
                               |
                               v
                           M(x_t)
                               |
                               v
                        proposal / action
                               |
                               v
                              E
                               |
                               v
                       correction / Return
                               |
                               v
                            I_(t+1)
```

The architectural asymmetry is intentional:

> **Identity may constrain search; reality must retain authority to revise identity.**

## Candidate contribution if later experiments support it

A future paper may be able to argue that:

1. persistent identity-like operating structure can be separated from host-model weights;
2. only task-relevant portions need be activated on each inference;
3. targeted activation can reduce recurrent context relative to full identity;
4. visible identity statements alone may be insufficient to govern proposals;
5. compiling identity into explicit obligations plus correction paths can make selected invariants operationally consequential;
6. corrigibility and host portability can be tested as functional properties of identity architecture.

Every item above remains conditional on evidence beyond the current pilot where stated.

## Compact thesis candidate

> **A general AI need not reconstruct its standing operating structure on every decision. Persistent identity may provide reusable orientation, but it becomes useful infrastructure only when relevant structure can be selectively activated, made operationally consequential, and revised when reality contradicts it.**

## Research discipline

Do not write the ending before the tests.

Preserve:

```text
negative results
mixed results
harness failures
false-positive guards
selector misses
host-specific failures
cost reversals
```

No single path certifies itself — including the identity hypothesis.
