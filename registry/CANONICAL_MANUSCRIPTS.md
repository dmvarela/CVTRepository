# Canonical Manuscripts

**First verification pass:** 2026-07-16  
**Historical source examined:** the preserved 246-project Overleaf export.

This registry identifies the exact manuscript content that should be migrated into canonical GitHub paths. Historical project names are evidence about provenance; canonical authority now belongs to the registered GitHub path and commit.

## Canonical rule

For every active manuscript, record:

- canonical GitHub path;
- current commit SHA;
- SHA-256 digest of the main source;
- build status and PDF date;
- publication status;
- provenance from any historical project or recovered file.

## Canonical GitHub manuscripts

### CVT Foundations — canonicalized

- **Canonical GitHub path:** `research-hub/cvt-foundations/main.tex`
- **Canonicalization commit:** `392445c22b57fc8f54741ea8ceb664164887ac44`
- **Historical source:** `Coherence viability Theory/main.tex`
- **Title:** *Coherence Viability Theory: Bounded Exchange, Receptive Basins, and the Conditions for Hosted Transformation*
- **Source SHA-256:** `fe1cf269a35da713ef13d69d05e35658dc860e4f6caf03ef3864bd38ddc258eb`
- **Build status:** successful pdfTeX build, 20 pages.
- **Milestone PDF:** `research-hub/cvt-foundations/milestones/2026-07-22-canonicalization/cvt_foundations_2026-07-22.pdf`
- **Milestone PDF SHA-256:** `11e4d1fb27f1e275400e725432e4d62f96a88e55143364d51c5856d8c7a1ef19`
- **Publication status:** canonical working manuscript; not submission-ready.
- **Current review artifact:** `research-hub/cvt-foundations/reviews/2026-07-22-claim-ledger.md`
- **Next action:** literature, novelty, falsifiability, and scope-control stress test under issue #6.

## Verified source identities awaiting GitHub migration

### FTLτA — exact submitted manuscript

- **Historical source:** `Ftltau ai final submission/FTLtauA AIandEthics submission revised final.tex`
- **Title:** *The FTLτA Framework: A Non-Compensatory Geometry of Permissible Action for AI Safety and Accountability*
- **SHA-256:** `b66a144c5addeb694c6891c8b841f163012b7c0c28d208bd9e201ee35db64e3b`
- **Verification:** anonymized submitted manuscript; successful local compilation to 14 pages.
- **Duplicate history:** `FTLTauA Final submission` contains the same source. `FtlTauA Submission` is a defective near-copy with an extra `\end{abstract}`.
- **GitHub status:** exact source, PDF, and submission record must be committed as an immutable milestone.

### Healthy Membrane Dynamics

- **Historical source:** `Healthy membrane dynamics/main final.tex`
- **Title:** *The Healthy Membrane Regime: A Reaction–Diffusion Model of Communion Without Annihilation*
- **SHA-256:** `90a7c97672adeeedb872fbcb4540655c16f01e6d35f15222c9d0f87ad71f7729`
- **Verification:** successful local compilation to 23 pages; later authorship and AI-collaboration language present.
- **GitHub status:** complete reproducible package still needs migration.

### Incoherence Debt

- **Historical source:** `Incoherence Debt and the Engineering Limits of Suppressive Safety/main.tex`
- **Title:** *Alignment Through Love: Restraint, Incoherence Debt, and the Price of Suppressive Safety*
- **SHA-256:** `ca3bf9eec42a1baf620c1de23e0a5626a4b47c6e79f0ecdabf3ef9dcce464b1e`
- **Duplicate history:** two identical historical project containers.
- **GitHub status:** commit one canonical copy and preserve the duplicate finding in provenance notes.

## Recovered active manuscripts

### Right Relation

- **Recovered filename:** `right_relation_short_treatise.tex`
- **Planned canonical path:** `research-hub/right-relation/right_relation_short_treatise.tex`
- **Important distinction:** the historical project named `Right relation` contains *The Harvest*, a different manuscript.
- **GitHub status:** source commit and build verification needed.

### Staged Urgency and Protective Hijack

- **Recovered filename:** `staged_urgency_protective_hijack_robotics_five_fixes.tex`
- **Planned canonical path:** `modern-robotics/staged-urgency/staged_urgency_protective_hijack_robotics_five_fixes.tex`
- **Bibliography:** embedded through `thebibliography`.
- **GitHub status:** source commit and build verification needed.

### Relational Backcasting

- **Recovered filename:** `The_Future_Is_Rehearsed_in_the_Means.tex`
- **Planned canonical path:** `research-hub/relational-backcasting/The_Future_Is_Rehearsed_in_the_Means.tex`
- **Required bibliography:** `the_future_is_rehearsed.bib`
- **GitHub status:** main source and bibliography must be committed before reproducible build verification.

### Safety as an Achievement of Relation

No bounded manuscript exists yet. Treat it as a bridge-paper outline until a two-page prospectus fixes its contribution.

## Source-of-truth rule

- **Active drafting:** the registered GitHub path is canonical.
- **Submitted work:** the exact source, compiled PDF, and submission record are immutable GitHub milestones.
- **External editors:** optional; their changes become canonical only after commit.
- **ChatGPT Projects:** hold the living research conversations, decisions, and integration work.