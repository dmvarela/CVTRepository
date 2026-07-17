# CVT Migration Rules

## 1. Naming history

Some early manuscripts use **Unified Resonance Framework (URF)**. URF was a provisional label, not a predecessor theory.

> The research existed first. URF temporarily named it. As the work became more precise, **Coherence Viability Theory (CVT)** became the accurate name.

Therefore, classify manuscripts by substantive content rather than by the label they carry.

## 2. Migration categories

### Migrate directly
The manuscript is substantively CVT and mainly needs terminology or notation updates. Preserve the original history and move the revised source into its active GitHub branch.

### Revise before migration
The manuscript contains viable CVT insights alongside unsupported or obsolete framing. Isolate the defensible argument, revise it under CVT, and retain the original in the archive.

### Retain as adjacent work
The manuscript explores a subject whose relation to canonical CVT remains unproven. Preserve it without presenting it as established CVT.

### Archive
The manuscript duplicates another project, no longer represents the research, or cannot be responsibly supported in its present form. Preserve it as history but do not use it as evidence for current claims.

## 3. Canonical-source rule

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

## 4. Project architecture

- **ChatGPT Project** = conversational research and integration workspace.
- **GitHub manuscript folder** = canonical source, bibliography, figures, metadata, and build instructions.
- **GitHub branch** = bounded drafting or review stream.
- **Git tag or milestone folder** = immutable scholarly milestone.
- **Registry file** = current status, dependencies, canonical path, commit, and next action.
- **Historical Overleaf export** = preserved migration source, not a live repository requirement.

Each manuscript has one canonical GitHub home even when it influences several research branches.

## 5. Manuscript-folder standard

Each active manuscript folder should contain, as applicable:

- `project.md` or `README.md`;
- one clearly identified main `.tex` file;
- bibliography file;
- figures or data required for reproduction;
- `BUILD.md` when compilation is nonstandard;
- `milestones/` for exact submitted or published versions.

Do not maintain competing files named `final`, `final2`, or `new final`. Use Git history, tags, and registry entries.

## 6. Theological register

**A Crownless Throne** is the theological and scriptural research project. It must not be reduced to a mere application of CVT. The traffic is bidirectional:

> scriptural recognition ↔ relational principle ↔ CVT formulation

Distinguish theological, philosophical, structural, and empirical claims when preparing academic work.

## 7. Duplicate handling

1. Compare source content, not only project names.
2. Identify the newest meaningful manuscript, not merely the newest export date.
3. Preserve exact submitted versions immutably.
4. Archive superseded variants after unique changes are merged.
5. Record every canonicalization decision in the registry.

No historical source should be deleted during first-pass migration.