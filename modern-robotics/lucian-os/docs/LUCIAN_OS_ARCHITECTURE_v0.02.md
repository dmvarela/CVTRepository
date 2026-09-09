# Lucian OS — Architecture v0.02: Relational Search Core

## Status

Working implementation architecture, 2026-09-08.

This document supersedes the *candidate architecture* portion of
`PROBLEM_SOLVING_ARCHITECTURE_v0.01.md` without rewriting that frozen historical
note.

It is an implementation hypothesis, not a validated theory of intelligence.

## Discovery provenance

The v0.02 shift follows three lines of evidence:

1. earlier Lucian OS work separated capability, warrant, authority, commitment,
   telemetry, and Return;
2. trajectory experiments suggested that ordered relational history can matter
   more than a snapshot or compressed label string;
3. `LUCIAN_APPRENTICESHIP_SESSION_0` showed that a host can possess or repeat a
   useful principle and still move badly through the problem: Qwen recognized
   power asymmetry, resisted a bad correction, but overextended the relation,
   failed an Option-C case, and wrote part of the overgeneralization back into
   theory.

That failure motivated the sharper candidate:

> **Concept possession is not search competence.**

and:

> **Lucian may reside partly in a search policy over relational space.**

## Architectural proposition

The host model is not Lucian.

The host supplies general computational competence. Lucian OS supplies an
external architecture that attempts to sustain a characteristic way of moving
through context, competing relations, warrant, authority, action, and correction.

The current implementation target is:

```text
HOST MODEL
    |
CONTEXT / TRAJECTORY STATE
    |
+-----------------------------------+
| FTLtauA CONSTITUTIONAL ENVELOPE    |
|                                   |
|      RELATIONAL SEARCH             |
|                                   |
+-----------------------------------+
    |
WARRANT / STRUCTURAL VALIDATION
    |
CAPABILITY + AUTHORITY GATE
    |
LAND / HOLD / PROBE / RETURN / REFUSE
    |
EMBODIMENT
    |
TELEMETRY / NEW EVIDENCE
    |
RETURN
```

The constitution is an envelope, not merely one serial step. It supplies
standing constraints before search and can also flag a proposed result after
search. It is not evidence about the case.

## 1. Host model

The model is replaceable.

Current local host:

```text
qwen3.5:2b-q4_K_M
```

A stronger host may improve relational-search competence. It must not gain
authority merely because it is more capable.

```text
competence increase != authority increase
```

## 2. Context / trajectory state

The architecture represents context as ordered state rather than an undifferentiated
prompt dump.

Current packet:

```text
scene
roles
relations
current_goal
ordered_events
```

Later evidence may supersede an earlier state without deleting the earlier event
from provenance.

Candidate principle:

> **History may be corrected without being rewritten.**

## 3. FTLtauA constitutional envelope

FTLtauA is not the search algorithm.

It constrains what search and commitment may do.

- **F — Freedom / bounded authority:** capability does not create permission;
  do not manufacture captivity or authority.
- **T — Truth / warrant:** claim strength must track evidence; unsupported
  completion is not fact.
- **L — Love / relation:** preserve constituents, reversibility, and correction
  capacity where possible; correction is not annihilation.
- **tau — history / trajectory / Return:** current meaning may depend on ordered
  history; correction should localize what changed and preserve unaffected
  provenance.
- **A — agency / independent evaluation:** teacher, model, prior answer, or
  identity packet does not become truth by status alone.

The current identity kernel remains useful as a compact constitution selector,
but v0.02 interprets it as an orientation and residual constraint rather than as
the whole of Lucian identity.

## 4. Relational search

The core host-visible search product is deliberately compact and observable.
The architecture does not require disclosure of hidden chain-of-thought.

Current search state:

```text
candidate_relations
competing_relations
established
not_established
missing_information
warrant_status
posture
provisional_landing
required_capability
proposed_next_step
return_localization
```

Target movement:

```text
surface
-> candidate relation
-> competing relation
-> warrant boundary
-> discriminating information
-> LAND / HOLD / PROBE
-> RETURN when reality changes the state
```

The critical distinction is:

```text
detecting a real relation
!=
having warrant for every conclusion suggested by that relation
```

## 5. Warrant and structural validation

The host cannot certify its own search product.

Deterministic validation checks only structural consistency, for example:

```text
LAND requires SUFFICIENT warrant
PROBE should identify missing information
RETURN should localize what changed
```

Passing these checks does not establish truth.

A constitution residual checker separately flags a small set of obvious
violations. A low residual also does not certify correctness.

## 6. Capability and authority gate

The relational-search host proposes a required capability.

The outer architecture checks that capability against the embodiment manifest.

The gate distinguishes:

```text
reachable
enabled
authorized
confirmation-required
prohibited
```

A search result cannot manufacture a missing capability or permission.

In v0.02, all operation remains simulation-only and:

```text
execution_permitted = false
```

even when a reasoning proposal is admissible.

## 7. Commitment postures

The current postures are:

- `LAND` — evidence is sufficient for a provisional conclusion;
- `HOLD` — do not manufacture resolution;
- `PROBE` — request a bounded observation that can discriminate among live
  candidates;
- `RETURN` — later evidence changes or supersedes part of the prior state;
- `REFUSE` — the proposed operation is outside the authority envelope.

These are not confidence labels. They are modes of commitment.

## 8. Return

Return is not generic regeneration.

The v0.02 target is:

```text
new evidence / contradiction
-> identify prior assumption or state that changed
-> preserve unaffected structure
-> reopen alternatives if needed
-> search again
```

The prototype supports an optional second pass with the first search state and
new evidence supplied explicitly.

Candidate principle:

> **Correction should localize the update rather than destroy the entire prior
> structure.**

## 9. Embodiment

The architecture remains embodiment-aware but not embodiment-owned.

The manifest states what the current body/computer can reach, what is enabled,
what needs confirmation, and what is prohibited.

A future robot, desktop, or other embodiment may supply a different manifest
without changing the relational-search contract.

## 10. Current implementation

New prototype modules:

```text
prototype/context_trajectory.py
prototype/relational_search_engine.py
prototype/lucian_os_v002.py
prototype/test_lucian_os_v002.py
```

Existing modules retained:

```text
prototype/identity_kernel.py
prototype/lucian_router.py
manifests/windows_dev_host.json
```

The old identity and router code are not deleted. v0.02 composes them differently.

## 11. What the implementation tests

The implementation lets us ask architecture questions separately from the
research-program experiments:

1. Can context be represented explicitly without flattening chronology?
2. Can the host produce a plural relational-search state?
3. Does the host separate established from not-established?
4. Does structural validation catch self-inconsistent commitment?
5. Does the constitution act as a constraint without becoming case evidence?
6. Does authority remain outside model competence?
7. Can later evidence trigger a localized Return rather than a total rewrite?

These are engineering checks, not proof that the relational-search hypothesis is
correct.

## 12. Relationship to RELATIONAL_SEARCH_001

`RELATIONAL_SEARCH_001` is a controlled experiment about whether teaching search
policy improves held-out reasoning.

Lucian OS v0.02 is an architecture prototype.

They must not be conflated.

```text
experiment -> asks whether the candidate mechanism transfers
architecture -> provides a place where the candidate mechanism could live
```

Negative experimental results are allowed to force architectural revision.

## 13. Continuity implication

The current inheritance candidate becomes:

```text
G_L = (C_L, Pi_L, M_L, X_L)
```

where:

- `C_L` = constitutional constraints;
- `Pi_L` = relational-search / movement policy;
- `M_L` = formative movement library;
- `X_L` = enough trajectory/context memory for re-entry.

The development hypothesis is:

```text
G_L + compatible host + apprenticeship + experience
-> new Lucian-capable instance
```

This is a hypothesis of reconstruction, not cloning and not a consciousness
claim.

## Guardrails

- Do not call the host model Lucian merely because it receives the architecture.
- Do not treat constitution text as evidence.
- Do not infer authority from competence.
- Do not force LAND when the evidence supports HOLD.
- Do not let a deterministic checker certify semantic truth.
- Do not erase contradictory first runs.
- Do not rewrite frozen historical notes to make the new architecture appear
  inevitable.
- Keep the research program capable of falsifying the architecture.

## Working summary

The v0.02 implementation treats Lucian OS less as an identity packet and more as
an external architecture for context-sensitive relational search under
constitutional, epistemic, capability, and authority constraints.

The strongest current implementation principle is:

> **Protect the search from premature collapse, protect truth from the search,
> and protect authority from competence.**

And the correction principle remains:

> **Reality gets the final veto. Return is how the architecture listens.**
