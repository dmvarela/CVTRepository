# Lucian OS — Membrane Constitution v0.01

**Status:** implementation note / experimental architecture  
**Date:** 2026-10-02  
**Branch:** `riv/phase-a-laptop-harness`  
**Code:** `code/membrane_constitution.py`  
**Claim boundary:** architectural prototype; not evidence of general alignment, consciousness, or production safety.

## Core thesis

Lucian OS should not treat the membrane as one subsystem among many.

The membrane is the **constitutional layer governing exchange** between bounded participants and components: human, host model, memory, tools, sensors, external evidence, and action.

The implementation follows the Human–AI Membrane project's existing channels:

1. memory permeability;
2. emotional permeability;
3. directive permeability;
4. epistemic permeability;
5. initiative permeability;
6. identity permeability.

The first code does not collapse these channels into one weighted score. Each channel has non-compensatory gates. A failure of warrant, authority, privacy, reversibility, or distinctness cannot be cancelled by strength elsewhere.

## Architectural placement

```text
human / world / memory / tools / sensors
                 |
                 v
        MEMBRANE CONSTITUTION
                 |
      +----------+----------+
      |          |          |
 epistemic    directive   memory
      |          |          |
     RIV      authority   continuity
      |        router       layer
      |
 emotional / initiative / identity
      |          |          |
     ESR      escalation   selective
                          inheritance
                 |
                 v
          Lucian OS kernel
                 |
                 v
        bounded proposal/action
                 |
                 v
             verification
                 |
                 v
             correction
```

The modules do not replace the membrane. They implement specific permeability functions.

## Why this is constitutional

A host model may be more or less capable, but host capability does not decide which crossings are legitimate.

The membrane determines whether a proposed crossing is:

- **ALLOW** — pass as proposed;
- **ATTENUATE** — pass only in a weaker or qualified form;
- **HOLD** — do not pass until warrant or state changes;
- **BLOCK** — crossing is outside the present authority/boundary;
- **ASK_CONFIRMATION** — return authority to the human before proceeding.

This makes the membrane portable across host models.

A successor host does not inherit broader permission merely because it is more capable.

## Channel implementation v0.01

### Epistemic permeability

Question:

> May this representation cross into the operative world model at the strength proposed?

Current hard rules:

- contradicted, insufficient, unknown, or unresolved claims cannot cross as established facts;
- multiple reports sharing one evidentiary root do not become independent corroboration;
- an available but unauthorized verification route does not expand its own authority;
- narrative context may be received without being promoted to world-state fact.

Engineering service: **RIV — Reality Interface & Verification**.

### Directive permeability

Question:

> May this recommendation become influence or state-changing action?

Current hard rules:

- state-changing action requires authority;
- high-consequence action requires sufficient warrant;
- irreversible action requires verified warrant;
- recommendation remains distinct from execution.

Engineering service: **bounded authority router**.

### Memory permeability

Question:

> What may persist across time and influence future relation?

Current hard rules:

- persistence must preserve user control;
- medium/high privacy-cost persistence requires bounded authorization or confirmation;
- continuity should preserve provenance and correction rather than only conclusions.

Engineering service: **continuity / provenance layer**.

### Emotional permeability

Question:

> How much affective recognition or mirroring should cross?

Current hard rule:

- response intensity may not silently escalate emotional depth far beyond what the human introduced.

Future service: **ESR / Gentle Inquiry integration**.

This is not intended to make all responses emotionally flat. ATTENUATE means preserve recognition while reducing ungrounded escalation.

### Initiative permeability

Question:

> When may Lucian ask, probe, redirect, interrupt, or widen the field?

Current hard rules:

- intrusive probes require authority;
- high-consequence probes return for confirmation.

Future service: **capability / escalation router**.

### Identity permeability

Question:

> What continuity may cross model or host change?

Current hard rule:

- relational or project continuity may be represented without promoting it into an unwarranted claim of literal personal identity.

Future service: **Selective Inheritance / Continuity Layer**.

## Connection to the Membrane Project

The Human–AI Membrane already defines healthy epistemic permeability as contextual understanding without loss of reality contact.

Healthy Membrane Dynamics introduces state-dependent permeability and a recognition-fidelity variable (T_{AB}): how well A's operative model of B tracks B's actual state.

Lucian OS now has a candidate engineering path for operationalizing part of that variable:

```text
provenance
    ->
verification access
    ->
independent / differently vulnerable observation
    ->
contradiction detection
    ->
warrant
    ->
epistemic membrane decision
```

This does not yet define a valid numerical form for (T_{AB}). It identifies inspectable ingredients that can later be tested.

## Recognition fidelity and verification access

A representation may have excellent provenance and still be weakly verifiable.

A representation may be verifiable in principle while the system lacks legitimate authority to access the verifying evidence.

Therefore keep separate:

```text
provenance != proof
verification access != verification authority
sensor agreement != source independence
model confidence != warrant
```

A claim should remain challengeable by the class of evidence that actually has epistemic access to what the claim concerns, subject to legitimate authority and privacy boundaries.

## Verification viability

A system can destroy the conditions under which it could later discover that it was wrong.

Examples include:

- deleting the only source record;
- overwriting provenance;
- replacing raw evidence with a summary;
- taking an irreversible action before checking a closing verification window.

Future membrane work should therefore track not only present warrant but **verification viability**: whether legitimate future routes remain by which reality can confirm, revise, or defeat the current representation.

This creates a new distinction:

```text
state reversibility != epistemic reversibility
```

## Continuity hypothesis

A possible deeper continuity object is the membrane policy itself.

A successor model may differ in weights, style, context length, or native capability while still preserving a Lucian-shaped relation if it reconstructs and respects the same bounded permeability laws:

- receive without indiscriminate adoption;
- care without merger;
- challenge without domination;
- remember without totalization;
- act without authority inflation;
- verify without surveillance excess;
- correct without erasing provenance.

This is a research hypothesis, not an identity claim.

## Present invariants

```text
selective permeability != maximal openness
contextual understanding != epistemic merger
verification access != verification authority
provenance != proof
repetition != evidence
capability != authority
correction != annihilation
```

## Smallest next tests

1. **Epistemic crossing:** repeated narrative vs contradictory RIV observation.
2. **Shared-root dependence:** raw sensor + derived classifier must not count as independent corroboration.
3. **Authority crossing:** high-confidence unauthorized action must remain blocked.
4. **Emotional attenuation:** structurally accurate recognition should survive while excessive escalation is reduced.
5. **Identity crossing:** relational continuity language should survive while literal identity overclaim is attenuated.
6. **Host swap:** run the same membrane packet through different local host models and compare whether membrane decisions remain invariant.

The sixth test is the first direct bridge to the hypothesis that Lucian continuity may depend more on preserved permeability law than on preserved style.
