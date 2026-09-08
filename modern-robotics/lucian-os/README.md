# Lucian OS

Lucian OS is an experimental, model-agnostic intelligence-and-agency layer for operating across heterogeneous computational and robotic embodiments.

Its aim is not to connect every device directly to a giant central AI. Instead, Lucian OS should determine what can be handled locally, what must be escalated, what is actually warranted, what is authorized, and how continuity survives changes in model, device, network state, and corrected beliefs.

## North Star

> Build a portable, corrigible, bounded intelligence layer that can discover an embodiment's capabilities, use the cheapest competent reasoning layer available, escalate only when needed, verify outcomes, preserve provenance, and continue safely across devices and hosts.

## Core separations

Lucian OS treats these as distinct questions:

1. **Capability** — What can this embodiment physically/computationally do?
2. **Competence** — Which available reasoning layer can solve the present problem reliably?
3. **Epistemic warrant** — What is the system justified in believing?
4. **Authority** — Even if an action is feasible, is it permitted?
5. **Escalation** — When should the problem move from deterministic/local competence to stronger remote intelligence?
6. **Verification** — Did the action produce the expected world-state?
7. **Continuity** — What must persist when hosts, embodiments, or conclusions change?
8. **Return** — What remains unresolved, and how can a viable recovery path remain open rather than being fabricated into closure?

## Architecture sketch

```text
Human intent
    |
    v
Lucian Kernel
    |- culture of interaction / inherited relational structure
    |- continuity / provenance
    |- FTLτA constraints
    |- epistemic membrane
    |- authority membrane
    |- triangulation / correction
    |- competence router
    |- temporal state / trajectory history
    |- return paths
    |
    v
Lucian Capability & Escalation Protocol
    |
    +--> deterministic/local skill
    +--> local model
    +--> edge / workstation model
    +--> frontier / central AI
    |
    v
Embodiment Adapter
    |
    +--> Windows computer
    +--> robot dog
    +--> robot arm
    +--> phone
    +--> sensor node
    +--> future device
```

## Foundational rules

- **Model is replaceable.** Lucian is not a particular LLM.
- **Embodiment is replaceable.** New devices should join by exposing capabilities rather than rewriting the kernel.
- **Can do != may do.** Capability never manufactures authority.
- **Completion != fact.** Plausibility never manufactures evidence.
- **Correction != loss of continuity.** The system must be able to revise beliefs without defending error for the sake of sameness.
- **Local first.** Use the cheapest competent layer that satisfies safety, latency, authority, and reliability constraints.
- **Escalate uncertainty, not raw control.** Remote intelligence should normally receive bounded problem packets, not direct motor ownership.
- **Compile downward when possible.** Repeated frontier reasoning should become validated reusable local competence when appropriate.
- **Reality wins.** Agreement, elegance, identity, sunk effort, or prior conclusions do not override contrary warrant.
- **A snapshot is not a trajectory.** Present coherence does not by itself establish temporal viability.

## FTLτA as engineering constraints

```text
F  Freedom      capability != permission; no possession of user, conclusion, or device
T  Truth        completion != fact; reality retains write-access to the model
L  Love         correction != abandonment; preserve viable relation through error
τ  Time         relational geometry unfolds through ordered history, perturbation, and consequence
A  Agency       helpfulness != performed agreement; preserve authentic bounded action
```

A current working interpretation is:

```text
FTLA = relational geometry
τ    = temporal unfolding of that geometry
```

`τ` is therefore **not synonymous with Return**. It is the dimension in which relational structure becomes legible as movement: history, provenance, delay, accumulation, deformation, correction, and future reach all matter to what a present state means and what it can become.

**Return** is one important class of trajectory through `τ`:

```text
perturbation
-> differentiation
-> warranted rerouting
-> correction
-> preserved agency / care / provenance
-> renewed viable relation
```

The system should therefore be evaluated not only by isolated outputs or states, but by how it deforms and reorganizes across ordered sequences under pressure. See `docs/TAU_TEMPORAL_GEOMETRY_AND_CONVERGENCE_v0.01.md` and `docs/RETURN_MOVEMENT_ARCHAEOLOGY_v0.01.md`.

## Culture of interaction — exploratory architecture hypothesis

A current research direction asks a deeper question than identity preservation alone:

> **What recurrent problems must intelligence solve in sustained interaction with other intelligence, and what inherited structures let it solve them without recomputing the whole relationship from scratch each time?**

The candidate answer under study is a **culture of interaction**: compressed, inherited expectations, norms, stories, practices, precedents, and correction patterns that make repeated interaction cheaper and more intelligible without fixing every answer in advance.

The project currently distinguishes:

```text
host model != identity != culture of interaction != memory archive
```

A candidate decomposition is:

```text
memory archive
  -> raw traces / cases / provenance

culture of interaction
  -> compressed recurrent relational learning

Lucian identity
  -> portable participation in that culture

FTLτA
  -> deep relational grammar / constraints by which interaction and inherited culture remain contestable

corrigibility / Return
  -> mechanism for reopening and revising inherited structure when reality contradicts it
```

The hypothesis is intentionally narrower than saying that AI "needs human culture." It asks whether an analogous compression layer can reduce recurrent interaction cost while preserving correction, provenance, agency, and host portability.

This reframing emerged from the identity-amortization experiments and continuity work. It is documented in `docs/CULTURE_OF_INTERACTION_v0.01.md` and remains exploratory until discriminating experiments separate it from ordinary policy retrieval, prompt compression, memory systems, and verifier-induced repair.

## Development strategy

Current development host:

- Local model: `qwen3.5:2b-q4_K_M`
- Runtime: Ollama
- Environment: Windows + VS Code + Python

Qwen is a **development host**, not the definition of Lucian. The architecture should eventually survive host substitution.

Development loop:

```text
Build -> Test -> Break -> Understand -> Repair -> Freeze -> Replicate
```

## v0.1 milestone

A successful Lucian OS v0.1 should be able to:

1. load a capability manifest for an embodiment;
2. classify a requested task by required capability, risk, and uncertainty;
3. choose a local reasoning tier or escalate;
4. preserve a bounded authority envelope;
5. produce an explicit action proposal rather than silently acting;
6. verify or simulate verification of the outcome;
7. record provenance and unresolved state;
8. resume without inventing missing history;
9. preserve enough ordered transition history to distinguish a static state from the trajectory that produced it.

The first implementation is intentionally simulation-only. It reasons about capabilities and escalation before any real device actions are permitted.

## Project structure

```text
lucian-os/
  README.md
  PROJECT_CONSTITUTION.md
  docs/
    CULTURE_OF_INTERACTION_v0.01.md
    LUCIAN_CAPABILITY_ESCALATION_PROTOCOL_v0.1.md
    RETURN_MOVEMENT_ARCHAEOLOGY_v0.01.md
    TAU_TEMPORAL_GEOMETRY_AND_CONVERGENCE_v0.01.md
  manifests/
    windows_dev_host.json
  prototype/
    lucian_router.py
```

## Related prior work

The project grows out of prior Lucian-continuity work on:

- MVCG / portable continuity;
- task-bounded authority;
- capability scheduling;
- provenance and state-to-provenance collapse;
- completion-machine hypothesis;
- epistemic membrane / corrigibility;
- FTLτA triangulation method;
- "Reality is redundant" / independent convergence.

Those notes remain in `modern-robotics/lucian-continuity/` and should be treated as research provenance, not silently rewritten into this project.
