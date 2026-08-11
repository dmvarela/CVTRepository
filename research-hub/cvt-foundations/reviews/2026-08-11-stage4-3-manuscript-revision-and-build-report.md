# CVT Foundations - Stage 4.3 Manuscript Revision and Build Report

**Date:** 2026-08-11  
**Branch:** `review/cvt-stage4-3-manuscript-revision`  
**Pull request:** #30  
**Canonical source:** `research-hub/cvt-foundations/main.tex`  
**Stage 4.1 provenance:** `bfa12e38e4ddef89d2d76ed2b04577e56bcbafc1`

## Revision outcome

Stage 4.3 converts CVT Foundations from a result-ready manuscript into a result-constrained manuscript.

The revised paper reports the first bounded regulated-transport study as a mixed negative simulation result. The measured `B,Q,C,S` variables contained modest pre-outcome signal, but the locked CVT model did not satisfy the preregistered thresholds for incremental predictive value, predictive compression, or high-confidence safety-screen utility. The fitted hard intersection was neither necessary nor sufficient.

The four dimensions are therefore retained as a candidate measurement decomposition, not as four demonstrated jointly necessary independent gates. Product, minimum, geometric-mean, soft-minimum, and direct-constraint equations remain as falsifiable first-generation representations. Relational routing is introduced only as an exploratory programmatic hypothesis requiring fresh development data and preregistration.

## Canonical manuscript changes

- reports the locked Brier scores and the two-direction hard-gate contradiction counts;
- adds compact locked-model and hard-gate-anatomy tables;
- distinguishes strict variable-level, conditional, and configuration-level non-compensability;
- recasts capture readiness as a potentially input-conditioned, probe-estimated pre-outcome response relation;
- adds an explicit relational candidate layer between observations and independent outcomes;
- prevents productive uptake, rejection, damage, and recovery anatomy labels from becoming post-outcome predictors;
- changes the regulated-transport section from future design to completed validation status;
- adds adaptive reuse of opened validation data and model-capacity imbalance to the threat model;
- leaves fusion as a source-anchored illustration without restoring removed equations or numerical claims;
- states that Stage 5 model execution and final-test access are not authorized.

## Claim-ledger alignment

The claim ledger now assigns the frozen Stage 4.3 statuses:

- four jointly necessary conditions: **empirically constrained strong hypothesis**;
- capture readiness as an independent stored condition: **measurement architecture under revision**;
- relational routing: **exploratory programmatic hypothesis**;
- delivered-input, uptake, viability, damage, reserve, and history separation: **retained conceptual/methodological contribution**;
- regulated-transport support for CVT: **mixed negative simulation result**.

## Reproducible build verification

A dedicated pull-request workflow builds the manuscript in a clean Ubuntu environment with TeX Live and Poppler. It:

1. compiles `main.tex` twice with `pdflatex -interaction=nonstopmode -halt-on-error`;
2. fails on undefined references or citations;
3. fails on any overfull box;
4. records PDF metadata;
5. renders every page to PNG;
6. uploads the PDF, log, and page renders as a short-retention review artifact.

Verified review run: GitHub Actions run `31462073667`.

- compilation: successful on both passes;
- output length: 21 pages;
- final PDF size in the reviewed run: 272,580 bytes;
- undefined references: none;
- undefined citations: none;
- overfull boxes: none;
- remaining warnings: one benign `microtype` footnote-patch warning, one `hyperref` PDF-string warning caused by mathematics in a heading, two underfull model-table paragraphs, and one underfull bibliography paragraph;
- manuscript source SHA-256: `aed9a31e021676db9d037b3f8df6eb5c45b2484cfa4bfec1047491a29f32e534`;
- reviewed artifact bundle SHA-256: `1b669dcadf6c78e4ec132a2cb592bd489441fb839a86de07d30aae714d45ab81`.

## Visual inspection

All 21 rendered pages were inspected through six contact sheets at original render resolution. The first pass found no clipping, overlap, broken equation, malformed reference, or missing page. It did identify two publication-quality issues introduced by the revision: a mid-sentence page break in the capture-readiness subsection and a cramped model-comparison table. Both were revised and the affected pages were rebuilt and inspected again.

The final reviewed rendering has:

- a complete title, abstract, and first page without clipping;
- clean equation and relational-flow breaks;
- readable notation and result tables;
- intact table captions and source-provenance link;
- consistent section, footnote, and page-number placement;
- complete conclusion and 15-item bibliography;
- no visible layout defect across pages 1-21.

Temporary contact sheets used for review were removed from the branch after inspection. The permanent workflow retains only short-lived build artifacts outside repository history.

## Acceptance checks

- [x] universal-looking necessity and sufficiency language is scoped or replaced;
- [x] exact Stage 3 and Stage 4 scores and counts agree with locked artifacts;
- [x] relational routing is never described as validated;
- [x] post-outcome anatomy labels are not promoted to predictors;
- [x] the fusion section gains no unsupported model or numerical claim;
- [x] the manuscript and claim ledger use the same evidentiary statuses;
- [x] the LaTeX source compiles cleanly under the enforced publication-form checks;
- [x] every rendered page has received visual inspection;
- [x] the preserved final test remains ungenerated, unopened, and unauthorized.

## Boundary and next decision

Stage 4.3 changes interpretation and publication form only. It does not fit a relational-routing model, create a fresh development partition, generate or open the preserved final test, choose a Stage 5 winner, or claim validation beyond the simulated regulated-transport world.

After merge, Stage 5.0 protocol design is conditionally authorized if continuation remains scientifically justified. It must freeze a fresh development partition, pre-outcome response estimators, prespecified interactions, capacity-matched and domain-native baselines, outcome separation, stopping rules, and a new final-test authorization criterion before any revised model is executed.

