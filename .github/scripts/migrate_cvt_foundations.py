from __future__ import annotations

from pathlib import Path
import hashlib
import io
import zipfile

EXPECTED_SOURCE_SHA = "fe1cf269a35da713ef13d69d05e35658dc860e4f6caf03ef3864bd38ddc258eb"
INNER_PROJECT = "Coherence viability Theory.zip"
TARGET = Path("research-hub/cvt-foundations")
MILESTONE = TARGET / "milestones/2026-07-22-canonicalization"


def recover_source() -> tuple[bytes, str]:
    for outer_path in sorted(Path(".").glob("*.zip")):
        try:
            with zipfile.ZipFile(outer_path) as outer:
                if INNER_PROJECT not in outer.namelist():
                    continue
                inner_bytes = outer.read(INNER_PROJECT)
                with zipfile.ZipFile(io.BytesIO(inner_bytes)) as inner:
                    return inner.read("main.tex"), outer_path.name
        except zipfile.BadZipFile:
            continue
    raise RuntimeError(f"Could not find {INNER_PROJECT}/main.tex in any root-level ZIP")


def main() -> None:
    source_bytes, outer_name = recover_source()
    source_sha = hashlib.sha256(source_bytes).hexdigest()
    if source_sha != EXPECTED_SOURCE_SHA:
        raise RuntimeError(
            f"Source hash mismatch: expected {EXPECTED_SOURCE_SHA}, got {source_sha}"
        )

    TARGET.mkdir(parents=True, exist_ok=True)
    MILESTONE.mkdir(parents=True, exist_ok=True)
    (TARGET / "main.tex").write_bytes(source_bytes)

    (TARGET / "README.md").write_text(
        f"""# CVT Foundations

## Canonical manuscript

**Title:** *Coherence Viability Theory: Bounded Exchange, Receptive Basins, and the Conditions for Hosted Transformation*

**Author:** Daniel Varela Arevalo  
**Program:** Coherence Viability Theory (CVT)  
**Canonical source:** `main.tex`

## Role in the research program

This manuscript establishes the structural foundation of CVT. It proposes that viable transformation requires four simultaneous conditions:

1. bounded coupling;
2. preserved distinction;
3. a receptive basin;
4. restorative reserve.

The paper relates this invariant to viability theory, autopoiesis, passivity-based control, resilience theory, and basin dynamics, then develops membrane and fusion instantiations.

## Provenance

The source was recovered from the historical Overleaf export project:

`Coherence viability Theory/main.tex`

Historical export used during migration: `{outer_name}`.

The preserved export is migration history. This GitHub path is now the canonical source of the manuscript.

## Verification record

- Source SHA-256: `{source_sha}`
- Canonicalization date: 2026-07-22
- Build instructions: [`BUILD.md`](BUILD.md)
- Immutable first-build record: [`milestones/2026-07-22-canonicalization`](milestones/2026-07-22-canonicalization)

## Current status

**Canonical working manuscript.**

The next scholarly phase is a literature, novelty, and falsifiability stress test. Changes should be made on a bounded branch and merged into this canonical path after review.
""",
        encoding="utf-8",
    )

    (TARGET / "BUILD.md").write_text(
        """# Build instructions

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
""",
        encoding="utf-8",
    )

    (MILESTONE / "README.md").write_text(
        """# Canonicalization milestone — 2026-07-22

This folder records the first canonical GitHub migration and reproducible build of CVT Foundations.

## Included files

- `cvt_foundations_2026-07-22.pdf` — compiled from the canonical source during migration;
- `BUILD_REPORT.txt` — engine, page-count, provenance, and integrity record;
- `SHA256SUMS` — cryptographic digests for the canonical source and milestone PDF.

This milestone is historical. Later revisions must not overwrite these artifacts.
""",
        encoding="utf-8",
    )

    print(f"Recovered and verified {TARGET / 'main.tex'}")
    print(f"SHA-256: {source_sha}")


if __name__ == "__main__":
    main()
