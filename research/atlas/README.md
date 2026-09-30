# Atlas

**Status:** exploratory knowledge architecture with executable micro-library prototype  
**Scope:** compression, provenance, translation, plasticity, and recoverable correction

Atlas is a proposed architecture for preserving and moving conceptual knowledge across time, contexts, disciplines, and decoders without treating compressed representations as self-sufficient.

The central problem is:

> **How can a knowledge system compress enough to remain usable while preserving enough provenance, assumptions, and recovery paths that future decoders can reconstruct, translate, test, revise, or deliberately transform a concept responsibly?**

Atlas treats a concept not as a static note, but as a time-dependent object with history, epistemic status, routes of discovery, boundary conditions, and possible future transformations.

## Core distinctions

    compression != truth
    archive != active identity
    activation != confidence
    decompression != translation
    translation != implementation
    reconstruction != prescription
    source fidelity != permission to think
    preservation != endorsement
    correction != erasure

## Interpretive freedom

Atlas is **not** a prescription for what may be thought.

A decompression or reconstruction map records what a concept meant in a source trajectory, what assumptions supported that meaning, and which interpretations are compatible or incompatible with that source meaning.

A decoder remains free to reject, reinterpret, transform, invert, combine, or build something new from a source concept.

The architectural requirement is provenance, not obedience.

> **An interpretation may be incompatible with the source meaning without being an impermissible thought.**

If a decoder intentionally departs from the source, Atlas should record the departure as transformation rather than mislabel it as faithful reconstruction.

## Library–Librarian–Reader vision

See [Atlas Vision — The Library–Librarian–Reader Pair](VISION_LIBRARY_LIBRARIAN_READER.md).

The working system model is:

[
	ext{Library}
leftrightarrow
	ext{Librarian}
leftrightarrow
	ext{Reader}
]

The Library preserves the recoverable record. The Librarian performs explicit interpretive operations over it. The Reader supplies questions, context, and new associations.

## Architecture

See [Atlas Architecture v0.1](ATLAS_ARCHITECTURE_V0_1.md).

The first worked architectural specimen is [Identity as Corrigible Compression of Wake](examples/IDENTITY_CORRIGIBLE_COMPRESSION_001.md).

## Executable prototype

See [Atlas Micro-Library MVP 001](MVP_001.md).

The current prototype lives in:
- `code/atlas_librarian.py`
- `code/atlas_demo.py`
- `research/atlas/data/`
- `tests/test_atlas_librarian.py`

The first Librarian verbs are **FIND**, **TRACE**, **RECONSTRUCT**, and **TRANSLATE**.

The seed Library currently includes:
- Correction Is Survivable
- Reconstruction Is Not Prescription
- Relation as Part of the Codec

## Claim boundary

Atlas is an exploratory research architecture. It does not establish that knowledge graphs are brains, that AI systems possess persistent personal identity, or that cross-domain structural mappings are valid merely because they are elegant. Associations remain candidates until they survive explicit return, boundary, and implementation checks.
