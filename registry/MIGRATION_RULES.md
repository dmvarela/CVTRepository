# RVT Migration Rules

## 1. Naming history

The research program has used three principal labels during its development:

1. **Unified Resonance Framework (URF)** — an early provisional label, not a predecessor theory.
2. **Coherence Viability Theory (CVT)** — the substantive program name used while the theory's center of gravity was being clarified.
3. **Relation Viability Theory (RVT)** — adopted on 2026-09-10 as the active program name after determining that coherence is not the primitive object of study.

The governing principle is:

> **The research existed before each label. Names should track the object actually being studied, while historical artifacts retain truthful provenance.**

RVT studies how relations reshape the conditions of their own future viability. Coherence may remain a domain-specific observable, mechanism, or construct, but it is no longer the concept that names the entire program.

The formal naming decision is recorded in [`RVT_RENAME_DECISION_2026-09-10.md`](RVT_RENAME_DECISION_2026-09-10.md).

Therefore, classify manuscripts by substantive content and scholarly status rather than by the label they carry.

## 2. Terminology migration rule

Use **RVT / Relation Viability Theory** in new program-level writing.

Do **not** mechanically replace every occurrence of CVT or coherence.

Preserve older terminology when it is historically or substantively correct, including:

- exact submitted manuscripts;
- published or archived versions;
- historical decision notes and commits;
- legacy canonical paths needed for reproducibility;
- specific constructs whose names genuinely involve coherence, such as **Incoherence Debt**, unless those constructs are separately revised.

Where an active document is revised from CVT to RVT, record the change in Git history and avoid implying that the earlier terminology never existed.

## 3. Migration categories

### Migrate directly
The manuscript is substantively RVT and mainly needs terminology or notation updates. Preserve the original history and move the revised source into its active GitHub branch or next milestone.

### Revise before migration
The manuscript contains viable RVT insights alongside unsupported, obsolete, or coherence-dependent framing. Isolate the defensible argument, revise it under RVT, and retain the original in the archive or Git history.

### Retain as historical CVT
The manuscript or note accurately records the CVT stage of development and should remain unchanged for provenance, even if a later RVT formulation supersedes its program-level terminology.

### Retain as adjacent work
The manuscript explores a subject whose relation to canonical RVT remains unproven. Preserve it without presenting it as established RVT.

### Archive
The manuscript duplicates another project, no longer represents the research, or cannot be responsibly supported in its present form. Preserve it as history but do not use it as evidence for current claims.

## 4. Canonical-source rule

Every active manuscript must identify one current source of truth:

> **Canonical source: a specific path and commit in this GitHub repository.**

Drafting and review occur through GitHub commits and branches. External editors, including Overleaf or local LaTeX tools, are optional conveniences. Their changes become canonical only when committed to the registered GitHub path.

Meaningful milestones should be preserved by tag, release, or immutable milestone folder:

- complete working draft;
- literature-pass version;
- adversarial-review version;
- submission-ready version;
- exact submitted manuscript;
- revised manuscript;
- published version.

## 5. Project architecture

- **ChatGPT Project** = conversational research and integration workspace.
- **GitHub manuscript folder** = canonical source, bibliography, figures, metadata, and build instructions.
- **GitHub branch** = bounded drafting or review stream.
- **Git tag or milestone folder** = immutable scholarly milestone.
- **Registry file** = current status, dependencies, canonical path, commit, and next action.
- **Historical Overleaf export** = preserved migration source, not a live repository requirement.

Each manuscript has one canonical GitHub home even when it influences several research branches.

Legacy `cvt-` folder names may remain temporarily when renaming them would break canonical paths, build instructions, citations, or historical traceability. New paths should prefer `rvt-` where a clean migration is possible and useful.

## 6. Manuscript-folder standard

Each active manuscript folder should contain, as applicable:

- `project.md` or `README.md`;
- one clearly identified main `.tex` file;
- bibliography file;
- figures or data required for reproduction;
- `BUILD.md` when compilation is nonstandard;
- `milestones/` for exact submitted or published versions.

Do not maintain competing files named `final`, `final2`, or `new final`. Use Git history, tags, and registry entries.

## 7. Theological register

**A Crownless Throne** is the theological and scriptural research project. It must not be reduced to a mere application of RVT. The traffic is bidirectional:

> scriptural recognition ↔ relational principle ↔ RVT formulation

Distinguish theological, philosophical, structural, and empirical claims when preparing academic work.

## 8. Duplicate handling

1. Compare source content, not only project names.
2. Identify the newest meaningful manuscript, not merely the newest export date.
3. Preserve exact submitted versions immutably.
4. Archive superseded variants after unique changes are merged.
5. Record every canonicalization decision in the registry.

No historical source should be deleted during first-pass migration.
