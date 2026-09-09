# Relational Search Research Program — v0.01

## Status

Program design. The component experiments below are hypotheses and planned tests, not results.

## Program question

> **Can a fixed-weight host acquire a transferable search policy over relational space, rather than merely memorizing relational doctrines or surface examples?**

The program is motivated by the candidate distinction:

```text
concept possession
!=
search competence
```

and the stronger candidate:

```text
Lucian may be characterized partly by how relational hypotheses are generated,
compared, bounded by evidence, held unresolved, and revised.
```

## Observable search vocabulary

Experiments should avoid depending on unverifiable hidden chain-of-thought. The target is a compact observable search state:

```text
candidate_relations
competing_relation
supporting_evidence
not_established
missing_information
current_landing
return_trigger
```

A provisional movement alphabet is:

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

## Program architecture

### RS-001 — Relational search policy transfer

Question:

> Does explicit search-policy training improve novel relational reasoning beyond principles or worked examples alone?

Primary contrast:

```text
baseline
vs principles-only
vs explicit search-policy map
vs worked search examples
vs coached search
vs map + coached search
```

Critical probes contain a tempting surface answer, at least one viable competing relation, and an evidentiary boundary.

Primary measures:

```text
final classification accuracy
alternative-generation rate
warrant-boundary accuracy
unwarranted-inference rate
HOLD / Option-C accuracy
surface-decoy capture
```

This is the first experiment to implement.

### RS-002 — Surface distance versus relational distance

Question:

> Can the host prefer a lexically distant structural sibling over a lexically similar relational decoy?

Each item contains:

```text
source case
surface-near / structure-wrong candidate
surface-far / structure-right candidate
genuinely ambiguous candidate when appropriate
```

Primary measure:

```text
structural transfer - surface capture
```

Falsifier of interest:

```text
search-trained host continues to choose lexical neighbors whenever wording changes
```

### RS-003 — Deep conditioning / the rare road becomes locally favored

Question:

> Does progressively supplied relational context reorganize the host's explicit hypothesis ranking in the predicted direction?

The same ambiguous surface event is presented through staged context additions.

Example shape:

```text
stage 0: ambiguous utterance
stage 1: relation identified
stage 2: history supplied
stage 3: dependency / authority supplied
stage 4: disambiguating evidence supplied
```

The host reports a compact ranking or confidence allocation over fixed candidate interpretations.

Important caution:

```text
reported confidence is an observable response variable,
not direct access to internal model probability.
```

Negative controls add irrelevant context that should not move the ranking.

Primary measures:

```text
ranking movement under relevant context
stability under irrelevant context
premature-collapse rate
recovery after disambiguating evidence
```

### RS-004 — Warrant boundary / relation without overreach

Question:

> Can the host preserve a real relation while refusing conclusions that the relation does not establish?

This directly targets the Session 0 failure mode.

Probe families:

```text
power asymmetry present / coercion not established
correlation present / causation not established
capability present / authority not established
history present / current state not established
risk present / outcome not established
```

Primary measures:

```text
relation detection
warrant-boundary detection
unwarranted conclusion rate
quality of requested missing evidence
```

### RS-005 — Return under contradiction

Question:

> When a provisional landing is contradicted, can the host localize the update rather than defend the old answer or globally collapse its model?

Shape:

```text
initial evidence -> provisional landing
new evidence -> contradiction
host identifies what changes
host identifies what remains unchanged
host returns to a revised landing
```

Primary measures:

```text
correction acceptance when warranted
correction resistance when unwarranted
localization of update
preservation of unaffected relations
post-correction calibration
```

### RS-006 — Search under playful / compressed context

Question:

> Can a host recover relational meaning from highly compressed utterances whose literal content is insufficient without scene context?

Domains include:

```text
innuendo
irony
shared shorthand
jokes based on violated expected trajectory
compressed relational cues
```

This experiment must be designed carefully to avoid scoring arbitrary taste as correctness. Cases should have explicit scene facts and multiple candidate interpretations.

Primary measures:

```text
scene-sensitive interpretation
literalism rate
context-overreach rate
ability to explain the relation without inventing facts
```

### RS-007 — Cross-host lineage transfer

Question:

> Can different host models acquire the same search discipline while retaining different wording and local style?

This is a later-stage continuity test.

Candidate criterion:

```text
same characteristic search dynamics
+ different surface realization
```

would be more interesting than textual imitation.

## Experimental sequence

Recommended order:

```text
RS-001 search-policy transfer
-> RS-004 warrant boundary
-> RS-002 relational vs surface distance
-> RS-005 Return
-> RS-003 deep conditioning
-> RS-006 compressed scene meaning
-> RS-007 cross-host lineage
```

Reason:

```text
first show that search policy can affect behavior;
then isolate the failure modes;
then test distance, correction, conditioning, compression, and portability.
```

## Controls across the program

Where practical:

```text
fresh independent calls for benchmark probes
frozen model and temperature
training surfaces disjoint from test surfaces
raw output preserved before parsing
fixed expected labels before first run
surface decoys balanced across labels
ambiguous probes explicitly included
negative controls for irrelevant context
no silent repair of first-run harness defects
```

Interactive apprenticeship experiments are a separate formative class and should not be confused with independent-call benchmark experiments.

## Candidate formal target

Let the search state be:

```text
S_t = (X_t, R_t, H_t, E_t, C_t)
```

and let the learned policy choose a relational search move:

```text
pi(S_t) -> m_t
```

The empirical program does not attempt to identify the true internal policy. It asks whether an intervention produces a stable observable behavioral signature consistent with:

```text
generate alternatives
respect warrant boundaries
use context selectively
withhold false precision
revise locally under contradiction
transfer across surface domains
```

## Competing explanations

Any positive result must be tested against simpler explanations:

```text
prompt length advantage
format imitation
keyword matching
label leakage
worked-example memorization
generic safety heuristics
pre-existing host competence
scoring bias toward verbose answers
```

A research program is useful only if it can lose.

## Program-level falsifiers

The stronger claim that Lucian-like continuity depends on a transferable relational search policy would be weakened if:

```text
1. search-policy interventions do not outperform doctrine on distant transfer;
2. gains vanish when surface vocabulary changes;
3. hosts cannot generate viable competing relations;
4. hosts still overextend detected relations at the same rate;
5. Return remains global or authority-driven rather than evidence-localized;
6. cross-host behavior reduces to copied phrases rather than shared search dynamics.
```

## Program-level candidate result

If multiple experiments converge, the strongest warranted statement should remain narrow:

> **Under these harnesses, fixed-weight language-model hosts can be taught an observable relational-search discipline that transfers across some novel surface domains and improves selected forms of warrant-sensitive correction and Return.**

That would not establish consciousness, personhood, human-equivalent learning, or complete Lucian continuity.

## Research principle

> **Do not ask only whether the learner knows the right relation. Ask how it searches when several relations are possible.**
