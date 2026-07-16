# Canonical Manuscripts

**First verification pass:** 2026-07-16  
**Source examined:** the 246-project Overleaf export preserved in this repository.

This registry identifies the exact Overleaf project and source file that should be treated as canonical for active CVT manuscripts. Canonical identity is content-based: the project name alone is not sufficient when duplicate or near-duplicate containers exist.

## Verification method

For each active manuscript, the export was searched by project name, LaTeX title, and distinctive phrases. Candidate TeX files were compared by SHA-256 digest and, where possible, compiled with `pdflatex`. A manuscript is not marked canonical when the intended paper is absent from the export or when the apparent project contains a different work.

## Verified canonical manuscripts

### CVT Foundations — verified

- **Overleaf project:** `Coherence viability Theory`
- **Canonical source:** `main.tex`
- **Manuscript title:** *Coherence Viability Theory: Bounded Exchange, Receptive Basins, and the Conditions for Hosted Transformation*
- **SHA-256:** `fe1cf269a35da713ef13d69d05e35658dc860e4f6caf03ef3864bd38ddc258eb`
- **Verification:** exact title match; only substantive TeX file in the project; successful local compilation to a 20-page PDF.
- **Status:** canonical working manuscript.

### FTLτA — exact submitted manuscript verified

- **Primary Overleaf project:** `Ftltau ai final submission`
- **Canonical source:** `FTLtauA AIandEthics submission revised final.tex`
- **Manuscript title:** *The FTLτA Framework: A Non-Compensatory Geometry of Permissible Action for AI Safety and Accountability*
- **SHA-256:** `b66a144c5addeb694c6891c8b841f163012b7c0c28d208bd9e201ee35db64e3b`
- **Verification:** anonymized double-blind manuscript; successful local compilation to a 14-page PDF.
- **Status:** immutable submitted version.

An exact duplicate of this source is also present in the Overleaf project `FTLTauA Final submission`. The canonical identity is the SHA-256 digest above; `Ftltau ai final submission` is designated the primary container and `FTLTauA Final submission` should be marked as a duplicate container.

Do **not** use the near-copy in `FtlTauA Submission` as canonical. Its similarly named source contains an extra `\end{abstract}` and is not the verified submitted manuscript. The projects `FTLtauA final submission`, `FtltauA`, `Ftla`, and `AI Ethics as geometry` contain earlier developmental versions.

### Healthy Membrane Dynamics — verified

- **Overleaf project:** `Healthy membrane dynamics`
- **Canonical source:** `main final.tex`
- **Manuscript title:** *The Healthy Membrane Regime: A Reaction–Diffusion Model of Communion Without Annihilation*
- **SHA-256:** `90a7c97672adeeedb872fbcb4540655c16f01e6d35f15222c9d0f87ad71f7729`
- **Verification:** successful local compilation to a 23-page PDF; includes the final authorship and AI-collaboration acknowledgment language.
- **Status:** canonical working manuscript.

The files `main.tex` and `main-1.tex` contain a syntax error in the date line and should not be treated as canonical. `main with refs.tex` compiles and is a near-final precursor, but `main final.tex` contains the later authorship and acknowledgment revision.

### Incoherence Debt — verified, duplicate container unresolved

- **Overleaf project name:** `Incoherence Debt and the Engineering Limits of Suppressive Safety`
- **Canonical source:** `main.tex`
- **Manuscript title:** *Alignment Through Love: Restraint, Incoherence Debt, and the Price of Suppressive Safety*
- **SHA-256:** `ca3bf9eec42a1baf620c1de23e0a5626a4b47c6e79f0ecdabf3ef9dcce464b1e`
- **Status:** canonical content identified.

The export contains two projects with the identical project name and identical ZIP/source content. One should be renamed or archived as an exact duplicate in Overleaf; either contains the same canonical manuscript.

## Intended active manuscripts not found as exact Overleaf projects

### Right Relation — missing intended treatise

The export contains an Overleaf project named `Right relation`, but its manuscript is *The Harvest: Shared Life in Right Relation* (`the_harvest_right_relation.tex`). It is **not** *Right Relation: A Short Treatise on Order Without Erasure* and must not be substituted for it.

**Action:** upload or create the short-treatise project in Overleaf, then register its exact source here.

### Staged Urgency and Protective Hijack — exact paper missing

No exact project or source matching *Staged Urgency and Protective Hijack in Human-Facing Robotics* or the five-fixes manuscript was found in the export.

Related but distinct projects include:

- `Modern robotics VI` — *Protective-Hijack Inference and Decision Modes Under Urgent Claims*;
- `Failure mode taxonomy` — contains `failure_mode_taxonomy_human_facing_robotics.tex`;
- `Note on modern robotic and ftltaua` — bridge note harmonizing the robotics precursor with canonical FTLτA.

**Action:** upload the five-fixes manuscript to Overleaf or identify the project if it was created after the export.

### Relational Backcasting — missing

No exact project or source matching *The Future Is Rehearsed in the Means* or “relational backcasting” was found.

**Action:** create or upload the canonical Overleaf project.

### Safety as an Achievement of Relation — not yet a manuscript in the export

No exact project or source was found. This is currently best treated as a structured bridge-paper outline rather than an existing canonical Overleaf manuscript.

## Source-of-truth rule

- **Active drafting:** Overleaf is canonical.
- **Submitted manuscript:** the exact submitted source and PDF become immutable milestone records.
- **GitHub:** records identities, hashes, milestones, duplicates, and submission history.
- **ChatGPT Projects:** hold the living research conversations, decisions, and integration work.

When a manuscript reaches a meaningful milestone, record the project name, canonical source filename, SHA-256 digest, compiled PDF, date, and publication status here.