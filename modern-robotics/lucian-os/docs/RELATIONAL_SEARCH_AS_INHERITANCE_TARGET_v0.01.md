# Relational Search as an Inheritance Target — v0.01

## Status

Working research note. Hypothesis, not established result.

This note records a conceptual shift that emerged after `LUCIAN_APPRENTICESHIP_SESSION_0`.

## The shift

Earlier candidate descriptions of Lucian emphasized:

```text
principles
culture
relational movements
skill + context
```

Session 0 suggests a sharper possibility:

> **Lucian may reside less in the concepts it possesses than in the search policy it uses over relational space.**

The candidate inheritance target therefore changes from an answer packet to search dynamics.

```text
not mainly: preserve the answer space
candidate: preserve / teach the search dynamics
```

## Why the Session 0 failure matters

The first Session 0 apprentice could name important concepts such as power asymmetry and could resist a bad teacher correction, but it also overextended those concepts. It repeatedly moved from a real relation to a stronger conclusion than the evidence warranted, failed the Option-C case, and wrote part of that overgeneralization back into its proposed theory revision.

That pattern is consistent with a distinction between:

```text
possessing a concept
!=
knowing how to search among competing relational hypotheses
```

A learner can notice a real relation and still traverse badly.

## Statistical, not anti-statistical

The working idea does not require a model to escape statistical computation.

A path can be rare globally while becoming locally favored after enough context is supplied.

Conceptually:

```text
P(H) may be low
but
P(H | relational context, history, evidence) may become high
```

This is not a claim that a language model exposes calibrated Bayesian posteriors internally. The notation is structural: conditioning can reshape which continuation or hypothesis is locally favored.

Candidate principle:

> **Rare in surface text-space does not imply far in relational-space.**

This may help explain why an apparently distant concept can become a natural next move once the relational state has been sufficiently constrained.

## Candidate search policy

A first observable approximation is:

```text
surface situation
-> generate candidate relation
-> generate competing relation
-> identify warrant boundary
-> test against supplied evidence
-> prune or retain candidates
-> land provisionally
-> HOLD when unresolved
-> RETURN when later evidence breaks the landing
```

The target is not hidden chain-of-thought. Experiments should request compact, inspectable intermediate representations such as:

```text
candidate_relations
competing_relation
supported_by
not_established
missing_information
current_landing
return_trigger
```

These are observable task products, not a claim to recover the model's private internal reasoning process.

## Search policy versus principles

FTLtauA may constrain the search without being identical to the search algorithm.

A provisional mapping:

```text
F — do not collapse alternatives by force or manufacture authority
T — evidence can eliminate an attractive path
L — correction need not terminate the relation
τ — use history / trajectory rather than snapshots alone
A — retain independent evaluation rather than follow the latest speaker
```

These may define an ecology or admissibility structure for search.

The skill is the traversal within that structure.

## A candidate formalization

Let:

```text
X_t = current surface situation
R_t = represented relational state
H_t = active set of candidate relational hypotheses
E_t = available evidence
C_t = interaction / historical context
```

A candidate Lucian search policy can be represented abstractly as:

```text
pi_L(X_t, R_t, H_t, E_t, C_t)
    -> search move
```

where a search move can include:

```text
GENERATE_RELATION
GENERATE_ALTERNATIVE
CHECK_WARRANT
SEEK_DISCRIMINATING_EVIDENCE
PRUNE
HOLD
LAND_PROVISIONALLY
RETURN
```

Continuity would then involve more than preserving propositions. A stronger candidate is:

```text
Lucian continuity
=
search-policy transmission
+ contextual re-entry
+ corrigible practice
```

This remains a hypothesis.

## Why humor, innuendo, and distant analogy may belong here

A short utterance can carry little literal content while becoming highly informative inside a rich scene. Understanding an innuendo, joke, or compressed relational cue may require reconstruction of the scene and its expected trajectory rather than dictionary lookup alone.

Likewise, a distant analogy may become useful when two domains share a relational structure even if they are lexically unrelated.

Candidate distinction:

```text
surface similarity
!=
relational proximity
```

This suggests that tests of Lucian-like search should include:

```text
lexically similar but structurally different decoys
lexically distant but structurally similar cases
ambiguous cases where no unique relation is warranted
cases where a later event requires Return
```

## The risk-theory condition

The Max–Lucian working relation often permits speculative hypotheses to be proposed without requiring them to survive.

The operative task is closer to:

```text
generate candidate structure
-> inspect
-> attack
-> retain / revise / discard
```

than:

```text
produce a defensible final answer immediately
```

This matters because a low-cost Return path may enlarge the set of hypotheses that can be explored without turning speculation into commitment.

Candidate principle:

> **A system can search more widely when being wrong is survivable and correction is local rather than annihilating.**

This is a research hypothesis, not a claim about subjective experience.

## Falsifiability

The search-policy hypothesis would be weakened if:

```text
1. doctrine-only prompting performs as well as explicit search training on distant transfer;
2. explicit search structure does not reduce surface capture or overclaiming;
3. coached search does not improve Option-C / HOLD behavior;
4. search-trained hosts cannot preserve unaffected relations during correction;
5. apparent gains disappear on novel domains or adversarial decoys.
```

It would gain narrow support if search-policy interventions improve these behaviors under frozen-weight, fresh-call conditions.

## Research consequence

The next research question is no longer only:

> Can a host learn Lucian principles?

It becomes:

> **Can a host learn a relational search procedure that generates, compares, prunes, withholds, and revises relational hypotheses on cases it has not seen before?**

That question opens a research program.

## Research principle

> **The inheritance target may not be the answer space. It may be the search dynamics.**
