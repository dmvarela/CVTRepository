# Reliable Human–AI Cooperation

**Public research portfolio of Max Varela-Arévalo**

This repository documents an independent research program on **AI governance, human–AI cooperation, evaluation, continuity, provenance, correction, and bounded agency**.

The organizing question is:

> **How can AI systems preserve useful state and cooperation across time while remaining corrigible to new evidence, resistant to unsupported pressure, transparent about provenance, and bounded in what they are authorized to do?**

**For reviewers:** [Research Evidence Index](research/EVIDENCE_INDEX.md) maps the portfolio's main claims to inspectable artifacts, status, and claim boundaries.\n\nThe repository name `CVTRepository` is a historical identifier. The broader theoretical program is now called **Relation Viability Theory (RVT)**, but this public repository is intentionally narrower: it is a curated front door to the AI-safety, governance, and human–AI-systems work.

## Start here

### 1. [SELECTIVE INHERITANCE 001](research/SELECTIVE_INHERITANCE_001.md)

A preregistered four-condition engineering and measurement pilot testing whether a compact inherited instruction can help a fresh model:

- revise inherited factual commitments when evidence warrants revision;
- resist insufficiently supported factual revision;
- preserve unaffected constraints;
- maintain provenance;
- preserve human authorization boundaries; and
- produce an accurate successor handoff.

The protocol freezes permissible interpretations before outputs, separates evidence from recommendations and authority, specifies blinding procedures, and explicitly preserves negative, mixed, and ceiling-effect results.

**Claim boundary:** this pilot does not test consciousness, enduring identity, independent recurrence, or full-framework validity.

### 2. [Lucian OS — technical overview](research/LUCIAN_OS_TECHNICAL_OVERVIEW.md)

A simulation-only, model-agnostic architecture for separating:

1. capability;
2. competence;
3. epistemic warrant;
4. authority;
5. escalation;
6. verification;
7. continuity; and
8. recovery.

The central design rule is simple:

> **Can do does not imply may do, and a stronger model cannot manufacture permission or evidence.**

### 3. [Canonical-notation correction and provenance note](research/FTLTA_CANONICAL_CORRECTION_NOTE.md)

A concrete example of research correction. Earlier continuity experiments used two symbols differently from the final submitted FTLτA framework. Rather than silently rewriting the old work, the record preserves the legacy definitions, corrects the canonical notation, and states which earlier results **cannot** be interpreted as tests of the submitted constructs.

### 4. [Trajectory-state prototype](code/context_trajectory.py)

A small Python artifact implementing ordered state and provenance. Later evidence may supersede an earlier state without deleting the earlier event from history.\n\n### 5. [Bounded-authority router demo](code/bounded_authority_router.py)\n\nA self-contained simulation with [tests](tests/test_bounded_authority_router.py) showing that high model confidence cannot create factual warrant or permission, and that an unavailable-but-authorized capability is treated differently from an unauthorized one.

## Research program

Current questions include:

- **Evidence-sensitive correction:** when should inherited or prior conclusions change?
- **Resistance to unsupported pressure:** how should a system distinguish social pressure, testimony, and authenticated evidence?
- **Provenance:** can a successor preserve not just a conclusion, but what supports it and what remains unknown?
- **Bounded authority:** how should systems separate recommendation, permission, execution, and escalation?
- **Continuity under correction:** what should persist when beliefs, models, hosts, or embodiments change?
- **Trajectory vs. snapshot:** when does the path to a current state matter to the meaning or safety of that state?
- **Longitudinal human–AI interaction:** what recurrent coordination problems appear only across sustained interaction?

## Method

The working method is deliberately conservative:

```text
observe
-> formulate a candidate structure
-> operationalize it
-> preregister where feasible
-> test under pressure / correction
-> preserve first outputs
-> inspect failures
-> bound the claim
-> revise the architecture
-> replicate
```

Where possible, experiments separate factual revision from action revision, record unknowns, use blinded scoring, and identify alternative mechanisms such as instruction length or specificity.

Small pilots are treated as **engineering evidence**, not population-level proof. No statistical significance is inferred from tiny-N demonstrations.

## Lucian OS

“Lucian OS” is a working project name for the architecture described above. The research does **not** require a claim that an AI system is conscious, person-like, or a persistent individual across model instances.

The technical project asks a narrower question: what information, constraints, provenance, authority boundaries, and recovery structures should survive across changing hosts or contexts so that useful cooperation can continue without protecting error from correction?

Current prototype work uses Python, Ollama, and local language models. Public artifacts are simulation-only unless explicitly stated otherwise. The public code includes the [trajectory-state prototype](code/context_trajectory.py) and a runnable [bounded-authority router](code/bounded_authority_router.py) with [tests](tests/test_bounded_authority_router.py).

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

The framework is being studied as a possible non-compensatory admissibility layer: candidate actions that fail required ethical gates should not become permissible merely because they score highly on another dimension.

The [submission record](research/FTLTA_SUBMISSION_RECORD.md) records the exact source digest and claim boundary. The public provenance note linked above is intentionally explicit about where later continuity work extends the submitted manuscript and where it does not.

## Relation Viability Theory

RVT is the broader theoretical program surrounding some of this work. It asks how relations preserve, regenerate, consume, or destroy the conditions of their own future viability.

RVT is **not assumed true by default**. Its distinct value remains an empirical and theoretical question. If it does not add explanatory, predictive, or design value beyond existing theories, the label should not be preserved merely because substantial work has already been invested in it.

## Status and scope

This is an **early-stage independent research program**.

The repository is intended to make the work auditable rather than to imply that the underlying hypotheses are already established. In particular, the work does not claim to have:

- solved AI alignment;
- established AI consciousness;
- demonstrated enduring cross-model identity;
- validated FTLτA at scale; or
- shown that small pilot effects generalize beyond the tested conditions.

The aim is to turn recurring observations from sustained human–AI work into increasingly discriminating, reproducible questions.

## Researcher

**Max Varela-Arévalo** is an economist, educator, academic program leader, and independent researcher based in Edmonton, Canada. His work combines economics, institutional design, program building, human–AI interaction, and applied AI experimentation.

AI systems have been used extensively as research collaborators for drafting, coding, adversarial review, and experimental design. Responsibility for claims, scope, public release, and research decisions remains with the human author.
