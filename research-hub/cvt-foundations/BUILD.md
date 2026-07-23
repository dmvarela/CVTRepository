# Build instructions

The manuscript is self-contained. It has no external bibliography, figures, or data files.

## Requirements

A TeX distribution containing `geometry`, `amsmath`, `amssymb`, `amsthm`, `mathtools`, `graphicx`, `booktabs`, `hyperref`, `enumitem`, `physics`, `authblk`, `setspace`, and `microtype`.

## Reproducible build

From this folder, run:

```bash
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

The second pass resolves cross-references. Build artifacts other than an explicitly preserved milestone PDF should not be committed.
