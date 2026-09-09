# Build instructions — Paper F

Paper F v0.3 is modular. `main.tex` loads section files from `sections/` and uses an embedded `thebibliography` in `sections/references.tex`.

## Requirements

A TeX distribution containing:

- `geometry`
- `amsmath`
- `amssymb`
- `amsthm`
- `mathtools`
- `booktabs`
- `hyperref`
- `enumitem`
- `setspace`
- `microtype`
- `array`

## Reproducible build

From `research-hub/paper-f/`, run:

```bash
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

The second pass resolves cross-references.

## v0.2 verified build status

**Compilation was verified locally against the exact v0.2 source contents committed to the repository.**

- Build date: 2026-09-08
- Engine: pdfTeX / `pdflatex`
- Passes: 2
- Output: 20 pages, US Letter
- Undefined references: none observed after second pass
- Overfull / underfull boxes: none observed after second pass
- Remaining log note: benign `microtype` warning about its `footnote` patch
- Visual inspection: title/abstract, graduation theorem, spectral proposition and proof, dependency closure, exit taxonomy, F-to-E handoff, conclusion, and bibliography inspected in rendered PNGs

Source-tree digest for the locally built v0.2 source set (SHA-256 over ordered path/content records):

`9869f3093d395d7466b76ac17008afcde12d60e880fd2a620c3831e6e5d5b52f`

## v0.3 source-integration status

v0.3 adds the playing-field graduation proposition and the dynamic unsupported-viability / forward-invariance repair, and revises the introduction, literature boundary, discussion, conclusion, and abstract accordingly.

**v0.3 has not yet been compilation-verified.** The source was integrated through the repository connector, while the local TeX environment available during this integration could not reach GitHub to retrieve the updated tree. Do not infer a successful build from the earlier v0.2 milestone.

The next mechanical gate is therefore:

```bash
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

followed by checks for:

- undefined references;
- theorem/definition numbering;
- overfull or underfull boxes;
- table placement;
- equation wrapping;
- visual integrity of the longer political-economy and network sections.

## Source set

The modular source tree consists of:

- `main.tex`
- `sections/01_intro.tex`
- `sections/02_literature.tex`
- `sections/03_formation.tex`
- `sections/04_graduation.tex`
- `sections/05_network.tex`
- `sections/06_exit.tex`
- `sections/07_political_economy.tex`
- `sections/08_cases.tex`
- `sections/09_discussion.tex`
- `sections/10_conclusion.tex`
- `sections/references.tex`

## Milestone status

v0.3 is a **source-integrated research-draft milestone**, not a submission version. The next gates are fresh compilation verification and hostile review focused on the playing-field proposition, the dynamic unsupported-viability condition, spectral stability, scope containment, and empirical identification. Build artifacts should not be committed unless an explicitly designated milestone PDF is requested.
