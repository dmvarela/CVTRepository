# Build instructions — Paper F

The current working manuscript is self-contained. It uses an embedded `thebibliography` and has no external figures or data files.

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
- `authblk`
- `setspace`
- `microtype`

## Reproducible build

From `research-hub/paper-f/`, run:

```bash
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

The second pass resolves cross-references.

## Current build status

**Not yet compilation-verified from the canonical GitHub source.**

Do not record a successful build, source digest, or canonical manuscript milestone until `main.tex` has been compiled and inspected. Build artifacts should not be committed except for an explicitly designated milestone PDF.
