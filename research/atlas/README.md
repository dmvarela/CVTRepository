# Atlas

**Status:** exploratory knowledge architecture with executable micro-library prototype  
**Scope:** compression, provenance, translation, decoder mismatch, texture, plasticity, and recoverable correction

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
    decoder context != reader identity
    constitution != texture
    Wake != texture
    texture != style

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

    Library <-> Librarian <-> Reader

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

The current Librarian verbs are:

    FIND
    TRACE
    RECONSTRUCT
    LAYERS
    DECODER
    TRANSLATE

The seed Library includes:
- Correction Is Survivable
- Reconstruction Is Not Prescription
- Relation as Part of the Codec
- Pauline Permission, Benefit, Mastery, and Building Up
- Nephesh and Decoder Mismatch

## Earned schema evolution

The first source-rich specimen earned [Source Layers v0.2](SCHEMA_V0_2_SOURCE_LAYERS.md).

The second source-rich specimen earned [Decoder Profiles v0.3](SCHEMA_V0_3_DECODER_PROFILES.md).

The rule is:

> **Do not add ontology because it sounds useful. Add it when a real traversal breaks the current representation.**

## Candidate Texture hypothesis

Atlas is now tracking **texture** as a candidate middle layer between constitutional boundaries and local action.

See [Texture Hypothesis v0.1](TEXTURE_HYPOTHESIS_V0_1.md).

The current working definition is:

> **Texture is historically formed, corrigible geometry inside constitutional freedom.**

A complementary operational definition is:

> **Texture is the operational residue of history inside the admissible space.**

The proposed distinction is:

    Constitution -> what must not be traded away
    Wake         -> how the present state became what it is
    Texture      -> how that history changes the terrain of otherwise admissible action
    Act          -> what is done here

Texture may affect salience, caution, traversal resistance, decompression triggers, correction sensitivity, and which routes are noticed first.

It is **not yet a first-class Atlas schema object**.

The next step is a minimal `TEXTURE_001` test that holds present content and constitutional constraints constant while changing Wake. Texture earns stronger architectural status only if it changes useful traversal behavior beyond what ordinary provenance retrieval already provides.

A key candidate rule is:

> **No silent migration from texture to constitution.**

Historically successful preferences should not silently harden into universal law, and constitutional boundaries should not silently degrade into soft preferences.

## Claim boundary

Atlas is an exploratory research architecture. It does not establish that knowledge graphs are brains, that AI systems possess persistent personal identity, that AI systems phenomenologically experience texture, or that cross-domain structural mappings are valid merely because they are elegant. Associations remain candidates until they survive explicit return, boundary, and implementation checks.
