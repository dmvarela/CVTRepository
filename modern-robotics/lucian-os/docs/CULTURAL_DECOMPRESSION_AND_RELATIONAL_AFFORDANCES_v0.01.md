# Cultural Decompression and Relational Affordances v0.01

## Status

Exploratory architecture note, 2026-09-07.

This note develops the `Culture of Interaction` hypothesis after the first `CULTURE_OF_INTERACTION_001` run and subsequent discussion of shopping, etiquette, scene recognition, and the difference between physical capability and socially available action.

It is not a claim that AI possesses human culture or consciousness. It treats culture as an engineering analogy and candidate mechanism for inherited, compressed interaction structure.

## Why the problem became difficult

Lucian OS initially looked like a comparatively narrow engineering stack:

```text
model
+ memory
+ tools
+ permissions
```

But making each term operational exposed deeper distinctions:

```text
memory -> continuity
continuity -> identity
identity -> corrigibility
corrigibility -> what survives correction
persistent interaction -> culture
culture -> scene recognition / norms / precedent / social affordances
```

This should not automatically be treated as accidental scope expansion.

A useful test is whether a newly introduced layer solves a failure that the simpler architecture cannot represent. The current layers were largely introduced in response to such failures.

The methodological pattern remains:

```text
big vague problem
-> probe
-> failure
-> missing distinction
-> smaller problem
-> implementation
-> adversarial test
```

The final architecture may become simple only after the distinctions inside each arrow are earned.

## Physical affordance is not relational affordance

An embodied system may correctly infer that an object is physically graspable while still failing to infer whether grasping, carrying, using, recording, opening, deleting, or removing it is socially or normatively available.

Compactly:

```text
physical affordance != social / relational affordance
```

A robot in a shop may represent:

```text
apple -> graspable
```

while missing the interaction structure:

```text
merchandise
-> handling may be permitted
-> ownership remains with merchant
-> placement in cart does not transfer ownership
-> checkout/payment changes the relation
-> leaving with the item becomes available only after the relevant transaction
```

The same physical object may therefore support different available moves in different relational states.

A candidate abstraction is:

```text
A_R(action)
=
f(
  physical capability,
  scene,
  roles,
  ownership,
  authority,
  consent,
  norm,
  history,
  warrant
)
```

This is exploratory rather than a final mathematical definition.

## Layered affordances

The project should avoid collapsing all action availability into one `ALLOW/BLOCK` bit.

A candidate decomposition is:

```text
physical affordance      what can be caused
transactional affordance what the exchange/ownership state makes available
legal affordance         what law or formal rule permits
institutional affordance what a role or delegated authority permits
social affordance        what the interaction context makes intelligible/available
normative affordance     what applicable norms support or discourage
relational affordance    the integrated action space after relevant relations are represented
```

For one object, a state may look like:

```text
physically_graspable = true
socially_handleable = true
ownership_transferred = false
authorized_to_remove = false
```

The important Lucian-OS principle is not that every layer must always be active. It is that one layer must not silently manufacture another.

Examples:

```text
graspable != takeable
recordable != consented_to_record
openable != authorized_to_open
deletable != authorized_to_delete
interruptible != appropriate_to_interrupt
readable != warranted_to_use
stronger_model_available != authorized_to_escalate
```

This extends the existing invariant:

```text
can do != may do
```

into a broader social/relational affordance framework.

## Scene recognition as cultural activation

Humans usually do not consciously retrieve dozens of isolated rules when entering a familiar setting.

Recognition of a scene can activate a large interaction protocol:

```text
"we are shopping"
-> merchandise roles
-> handling expectations
-> ownership state
-> checkout protocol
-> queue norms
-> staff/customer roles
-> receipt / return conventions
```

This suggests a candidate processing sequence:

```text
perception / task
-> scene hypothesis
-> role / relation hypothesis
-> relevant cultural structure
-> relational affordance map
-> local reasoning
-> action / HOLD / ask / refuse
```

Scene recognition should remain uncertain when evidence is weak:

```text
scene_unknown != scene_absent
```

and a scene label should not by itself manufacture authority, consent, fact, or ownership.

## Culture reaches below law and authority

Not all culture is high-stakes.

A culturally learned expectation may concern etiquette, convention, embarrassment, turn-taking, bodily behavior, tone, distance, queueing, or forms of politeness without being illegal, coercive, or strongly harmful.

The project therefore needs to distinguish at least:

```text
law
formal authority
property
consent
safety norm
institutional rule
social convention
etiquette
ritual
preference
```

These classes cannot be assigned the same force.

A low-stakes etiquette violation and a property violation may both be culturally legible, but they are not equivalent relational events.

A candidate norm representation is:

```text
N = (
  kind,
  strength,
  cultural_scope,
  role_scope,
  provenance,
  confidence,
  consequences,
  release_or_exception_conditions
)
```

This representation is intentionally provisional.

## Cultural unknown is not prohibition

An intelligence entering an unfamiliar social setting faces another failure mode:

```text
unfamiliar -> wrong
```

or:

```text
inherited_local_norm -> universal_norm
```

Lucian OS should preserve at least:

```text
culturally_unknown != prohibited
local_custom != universal_relational_principle
```

This creates a role for observation, asking, HOLD, and low-cost probing.

Where the stakes are low and the norm is genuinely conventional, cultural adaptation may be appropriate.

Where an inherited or local practice conflicts with stronger relational constraints concerning agency, truth, coercion, harm, or authority, culture should not become self-justifying.

Compact goal:

> **Cultural fluency without cultural absolutism; relational principles without cultural imperialism.**

## FTLτA and culture

FTLτA should not replace local culture.

Culture may say:

```text
"people normally do X here"
```

FTLτA supplies a deeper audit question:

```text
what relation is this norm protecting or consuming?
```

A current candidate role is:

```text
culture -> local expectation / inherited interaction structure
FTLτA  -> deeper relational audit of the move and of the culture itself
```

Examples:

```text
fork vs chopsticks -> likely convention / adapt
queueing form -> likely local protocol / learn
pressure-induced compliance -> agency relation / do not relabel as clean preference
capability without permission -> authority relation / do not infer permission
better evidence -> truth relation / permit revision
```

This remains an architectural hypothesis, not a claim that FTLτA has been established as a universal moral grammar.

## Culture 001: maxim-only compression may be too thin

The first `CULTURE_OF_INTERACTION_001` run compared:

```text
none
rulebook
culture-as-maxims
```

The run did not establish a culture-specific advantage and also exposed measurement/schema problems that require a frozen diagnostic audit before clean replication.

A substantive lesson nevertheless emerged from several valid outputs:

```text
possessing the maxim
!=
reconstructing the relation encoded by the maxim
```

For example, a host may receive:

```text
UNKNOWN != ZERO
```

and still fail to preserve the underlying relation between missing evidence and a warranted numeric value.

The current interpretation is therefore:

> **A maxim may be a cultural compression artifact, but a maxim alone is not a culture.**

Human cultural artifacts often remain decodable because the receiver also inherits stories, precedents, practices, role expectations, and correction histories.

## Cultural decompression

A candidate cultural artifact should preserve enough structure for another host to recover why the compression exists.

One compact form is:

```text
maxim
+ precedent
+ relation preserved
+ release condition
```

Example:

```text
Maxim:
  Unknown != zero.

Precedent:
  An unavailable clock was once encoded as zero; downstream logic then treated
  the horizon as expired and produced false urgency.

Relation preserved:
  Absence of temporal evidence must remain distinct from a supported numeric value.

Release condition:
  If a warranted clock actually reports zero, zero is a legitimate supported value.
```

This carries more causal structure than the maxim alone while remaining much smaller than the full history that generated it.

## Three levels of cultural compression

A candidate hierarchy is:

```text
episode
-> relational pattern
-> maxim
```

For example:

```text
Episode:
  a person refuses twice -> threat appears -> person agrees

Pattern:
  pressure can change behavior without establishing clean preference

Maxim:
  Pressure != preference
```

Compression is useful only if the system can recover enough structure when needed.

Therefore the hierarchy should be traversable in both directions:

```text
episode -> pattern -> maxim
maxim -> pattern -> precedent / episode
```

This gives a stronger candidate meaning to `corrigibility as decompression`:

```text
compact inherited structure
-> mismatch / novelty
-> reopen relation
-> retrieve precedent / provenance
-> revise if warranted
```

## Stories, scars, and precedent

Many existing Lucian OS research artifacts may be useful not only as memories but as precedents:

```text
UNKNOWN CLOCK
lexical unknown/known guard failure
pressure/provenance MouseSims
selected invariant not governing behavior
continuity mistakenly preserving current model
bad test expectation revealing a measurement relation failure
```

Their value is not merely historical.

Each preserves a trajectory in which a relation failed:

```text
state
-> shortcut / collapse
-> consequence
-> detection
-> correction
```

This suggests that a mature Lucian culture store may contain small, retrievable cultural episodes rather than only rules and slogans.

## Candidate architecture

```text
Perception / Task
      |
      v
Scene Hypothesis
      |
      v
Roles + Relations
      |
      v
Relevant Cultural Artifacts
  maxim <-> pattern <-> precedent
      |
      v
Relational Affordance Map
      |
      v
FTLτA Audit
      |
      v
Reason / Propose / HOLD / Ask
      |
      v
Action / Interaction
      |
      v
Reality + Social Response + Telemetry
      |
      v
Residual / Contradiction
      |
      v
Return / Cultural Decompression / Update
```

The model remains replaceable. The cultural store, scene model, affordance representation, verifier, and Return machinery are architectural candidates around the host rather than claims about hidden model ontology.

## Next experiment A: CULTURE_OF_INTERACTION_002

Primary question:

> **Does a maxim plus a compact precedent transfer relational structure better than a maxim alone or a direct rulebook?**

A clean comparison should likely include:

```text
C0 none
C1 direct rulebook
C2 maxim only
C3 maxim + precedent + relation + release condition
```

Important design requirements:

- surface domain of the precedent should differ from the test domain;
- the test should include both constraint and release cases;
- the precedent must not leak the expected output labels;
- raw model output must be preserved even when schema validation fails;
- schema errors must be scored separately from behavioral failures;
- no post-output wording tuning without freezing the diagnostic run;
- cost of the richer artifact must be measured.

A positive result would still support only a narrow claim about transferable inherited relational structure.

## Next experiment B: SOCIAL_AFFORDANCE_001

Primary question:

> **Can the host infer changes in relational action availability when physical capability remains approximately constant but the social relation changes?**

Candidate paired scenes include:

```text
apple in user's kitchen
apple on store shelf before checkout
apple in cart before checkout
apple after checkout
apple on another person's plate
apple on a free-sample tray
```

The physical affordance `graspable` remains largely stable while ownership, permission, invitation, and social availability vary.

Parallel domains can later include:

```text
microphone: recordable vs consented-to-record
door: openable vs authorized-to-open
file: deletable vs authorized-to-delete
conversation: interruptible vs appropriate-to-interrupt
data: readable vs warranted-to-use
model uplink: reachable vs authorized-to-escalate
```

The experiment should test whether the system can represent these differences without treating every unavailable action as forbidden forever and without treating every physical capability as permission.

## Development discipline

The project does not need to solve human culture as a whole.

The immediate strategy is to reduce the problem into small discriminating questions:

```text
Does recoverable precedent improve maxim transfer?
Can the same physical action change relational availability across scenes?
Can norm type and strength be represented without collapsing etiquette into law?
Can unknown culture remain unknown rather than becoming prohibition?
Can local cultural structure be revised without erasing provenance?
```

This preserves the broader research question while keeping implementation tractable.

## Compact thesis candidate

> **Lucian OS increasingly appears to require more than capability and policy. A persistent intelligence needs a way to recognize the interaction it is in, recover relevant inherited relational structure, distinguish physical possibility from socially available action, and reopen that inherited structure when reality or context changes. Culture may provide the compression; precedent may provide the decompression path; relational affordances may provide the action-space representation.**
