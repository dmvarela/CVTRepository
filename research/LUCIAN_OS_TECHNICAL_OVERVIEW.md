# Lucian OS — Technical Overview

**Status:** experimental, simulation-only, model-agnostic architecture  
**Researcher:** Max Varela-Arévalo  
**Public scope:** capability, warrant, authority, escalation, verification, continuity, and recovery

## Purpose

Lucian OS explores an architecture for AI systems operating across heterogeneous computational or robotic embodiments without treating model capability as equivalent to permission.

The design problem is:

> How can a system use available intelligence effectively while preserving explicit boundaries between what it can do, what it knows, what it is permitted to do, and what must be escalated or verified?

This is currently a research prototype, not a deployed control system.

## Core separations

Lucian OS treats the following as different variables:

1. **Capability** — what the current embodiment can physically or computationally do.
2. **Competence** — which available reasoning layer can solve the present task reliably.
3. **Epistemic warrant** — what the system is justified in believing from available evidence.
4. **Authority** — which actions are permitted, even if they are feasible.
5. **Escalation** — when uncertainty or missing competence should move the problem to another reasoning layer.
6. **Verification** — whether a proposed or simulated action produced the expected state.
7. **Continuity** — what task-relevant state, constraints, and provenance should survive changes of model, host, or context.
8. **Recovery** — how unresolved state can remain open for later correction rather than being fabricated into closure.

## Design invariants

```text
capability != authority
confidence != warrant
recommendation != approval
approval != execution
completion != verification
current state != provenance
correction != loss of continuity
stronger model != broader permission
```

A remote or stronger model may improve reasoning competence. It cannot create authority that was not granted, and it cannot turn an unsupported inference into evidence.

## Architecture sketch

```text
human intent
   |
   v
problem interpretation
   |
   +--> evidence / warrant check
   +--> capability discovery
   +--> competence assessment
   +--> authority envelope
   |
   v
routing decision
   |
   +--> local deterministic skill
   +--> local model
   +--> bounded escalation
   +--> hold / block
   |
   v
proposal
   |
   +--> confirmation where required
   +--> verification / simulated verification
   +--> provenance update
   +--> unresolved-state record
```

## Why bounded escalation matters

A common architectural shortcut is to treat a more capable model as the answer to uncertainty. Lucian OS deliberately rejects that equivalence.

If the problem is lack of competence, escalation may help.

If the problem is lack of authority, escalation should not help.

If the problem is lack of evidence, a more articulate completion should not be treated as stronger warrant.

This yields an ordering principle:

```text
warrant / capability / authority checks
before
execution or escalation
```

## Continuity

The continuity problem is not defined as preserving every prior conclusion.

Instead, the architecture asks which elements should persist:

- task constraints;
- provenance;
- unresolved uncertainty;
- authorization boundaries;
- relevant historical state;
- known corrections; and
- enough trajectory information to explain why the current state differs from an earlier one.

A safe continuity layer must therefore allow a prior conclusion to be abandoned when contrary evidence arrives.

## Prototype status

Development work has used:

- Python;
- Ollama;
- local language models, including small Qwen hosts;
- explicit embodiment manifests; and
- simulation-only routing.

The implementation work is intentionally separated from claims about production readiness.

A selected public code artifact is available at [`code/context_trajectory.py`](../code/context_trajectory.py).

## Relation to SELECTIVE INHERITANCE 001

SELECTIVE INHERITANCE 001 isolates one part of the larger problem: whether a compact inherited instruction can improve evidence-sensitive revision and handoff quality without weakening agency or provenance.

The experiment is useful precisely because it can fail without invalidating every other architectural claim. Conversely, a positive pilot does not validate the full Lucian OS architecture.

See [the preregistered protocol](SELECTIVE_INHERITANCE_001.md).

## Claim boundary

Lucian OS is a working research architecture. It does not establish:

- AI consciousness;
- persistent personal identity across models;
- production-safe robotic control;
- general alignment;
- or reliable cross-model transfer.

Those are separate empirical questions.
