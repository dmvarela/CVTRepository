# Reliable Human–AI Cooperation

[![Python tests](https://github.com/dmvarela/CVTRepository/actions/workflows/python-tests.yml/badge.svg)](https://github.com/dmvarela/CVTRepository/actions/workflows/python-tests.yml)

**Public research portfolio of Max Varela-Arévalo**

I am an economist, educator, academic program leader, and independent researcher working on **AI governance, human–AI cooperation, evaluation, provenance, correction, and bounded agency**.

The central question behind this portfolio is:

> **How can AI systems preserve useful state and cooperation across time while remaining corrigible to evidence, transparent about provenance, and bounded in what they are authorized to do?**

If you are reviewing this work for a role or research conversation, the fastest entry point is the **[Research Evidence Index](research/EVIDENCE_INDEX.md)**. It maps the main public claims to inspectable artifacts, current status, and explicit claim boundaries.

## Five-minute tour

| Artifact | What it demonstrates | Status |
|---|---|---|
| **[SELECTIVE INHERITANCE 001](research/SELECTIVE_INHERITANCE_001.md)** | Preregistered evaluation design for warranted revision, resistance to unsupported pressure, provenance, human authorization, and successor handoff | Protocol frozen; exploratory execution deviated from the intended host, documented in the [execution status](research/SELECTIVE_INHERITANCE_001_EXECUTION_STATUS.md) |
| **[Bounded-authority router](code/bounded_authority_router.py)** + **[tests](tests/test_bounded_authority_router.py)** | Executable separation of capability, authority, warrant, escalation, and execution | Simulation-only prototype |
| **[Trajectory-state prototype](code/context_trajectory.py)** + **[tests](tests/test_context_trajectory.py)** | Ordered state, supersession, and non-destructive provenance | Small executable prototype |
| **[Lucian OS technical overview](research/LUCIAN_OS_TECHNICAL_OVERVIEW.md)** | Model-agnostic architecture for capability, competence, warrant, authority, escalation, verification, continuity, and recovery | Exploratory architecture; no real-device actions |
| **[FTLτA correction note](research/FTLTA_CANONICAL_CORRECTION_NOTE.md)** | Research correction, notation discipline, and preservation of superseded interpretations | Submitted manuscript is separately documented in the [submission record](research/FTLTA_SUBMISSION_RECORD.md) |

## What the work is trying to separate

Several recurring distinctions organize the technical work:

```text
capability != authority
confidence != warrant
recommendation != approval
approval != execution
current state != provenance
correction != loss of continuity
stronger reasoning != broader permission
```

The point is not that these slogans solve alignment. The point is to turn them into **testable interfaces, routing rules, evaluation tasks, and failure cases**.

## Research questions

- When should inherited or prior conclusions change in response to new evidence?
- How should a system distinguish pressure, testimony, and authenticated evidence?
- What information must survive a handoff so that provenance is preserved without freezing error?
- How should recommendation, authorization, execution, and escalation remain distinct?
- What should persist when models, hosts, embodiments, or conclusions change?
- When does the trajectory into a state matter more than the state viewed as a snapshot?
- Which coordination problems appear only in sustained human–AI interaction?

## Method

The working loop is:

```text
observe
-> formulate a candidate structure
-> operationalize it
-> preregister where feasible
-> test under pressure / correction
-> preserve first outputs
-> inspect failures
-> bound the claim
-> revise
-> replicate
```

Small pilots are treated as **engineering evidence, not population-level proof**. Deviations are documented rather than silently repaired. Negative or mixed results remain reportable.

The repository intentionally distinguishes three states:

- **Demonstrated** — supported by a career record, artifact, protocol, code, or completed work.
- **In progress** — actively being built or tested, with current status stated.
- **Planned / interested in** — not yet demonstrated and therefore not described as an existing result.

## Lucian OS

“Lucian OS” is a working project name for a simulation-only research architecture. It asks what state, provenance, constraints, authorization boundaries, and recovery structures should survive across changing hosts or contexts.

The project does **not** require a claim that an AI system is conscious, person-like, or a persistent individual across model instances.

Current public code is intentionally small and inspectable. It includes the [bounded-authority router](code/bounded_authority_router.py) and [trajectory-state prototype](code/context_trajectory.py), both covered by public tests.

## FTLτA

A related manuscript, **_The FTLτA Framework: A Non-Compensatory Geometry of Permissible Action for AI Safety and Accountability_**, was submitted to Springer Nature’s *AI and Ethics* in 2026.

Canonical notation in the submitted version is:

```text
F = Freedom
T = Truth
L = Love
τ = Temporal-contextual depth
A = Agent coherence
```

The [submission record](research/FTLTA_SUBMISSION_RECORD.md) supports only the claim that the manuscript was submitted. The [canonical-notation correction](research/FTLTA_CANONICAL_CORRECTION_NOTE.md) records a substantive correction between earlier exploratory continuity notation and the submitted framework.

## Scope and claim boundaries

This is an **early-stage independent research program**. The repository is designed to make the work inspectable, not to imply that its hypotheses are already established.

It does not claim to have solved AI alignment, established AI consciousness, demonstrated enduring cross-model identity, validated FTLτA at scale, or shown that small pilot effects generalize beyond tested conditions.

## About the researcher

**Max Varela-Arévalo** is based in Edmonton, Canada. His background combines economics, institutional design, teaching, academic program leadership, and applied AI experimentation.

AI systems have been used as research collaborators for drafting, coding, adversarial review, and experimental design. Responsibility for claims, scope, public release, and research decisions remains with the human author.

---

**Repository note:** `CVTRepository` is a historical repository name. The broader theoretical program is now called **Relation Viability Theory (RVT)**. The complete historical archive is maintained separately and privately; this repository is the curated public research portfolio.
