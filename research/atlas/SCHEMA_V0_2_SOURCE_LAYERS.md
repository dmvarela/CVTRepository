# Atlas Schema v0.2 — Source Layers

**Status:** implemented in prototype  
**Purpose:** keep different relations to a source visible rather than collapsing them into one synthesized field.

## Why v0.2 exists

The first source-rich specimen, “All Things Are Lawful,” immediately broke the v0.1 assumption that one concept could be represented adequately by a single source-reconstruction string.

The specimen required at least these distinct layers:

- source text;
- translation;
- lexical note;
- historical reconstruction;
- scholarly interpretation;
- reader interpretation;
- transformation;
- source correction.

The important rule is:

[
oxed{
	ext{source text}

eq
	ext{translation}

eq
	ext{reconstruction}

eq
	ext{interpretation}

eq
	ext{transformation}
}
]

These layers may be related, but they should not be silently merged.

## KnowledgeLayer

The prototype now represents each layer with a typed record containing:

- `layer_id`
- `layer_type`
- `content`
- `source_ref`
- `language`
- `status`
- `derived_from`
- `assumptions`
- `provenance`
- `notes`

This allows the Librarian to answer not only *what information is relevant*, but *what kind of relation that information has to the source*.

## Current layer types

```text
source_text
translation
lexical_note
historical_reconstruction
scholarly_interpretation
reader_interpretation
transformation
source_correction
```

These are descriptive provenance categories, not rankings of intellectual legitimacy.

## Example

The Pauline specimen now stores separately:

- a 1 Corinthians 6:12 source layer;
- a 6:12 English gloss;
- a 1 Corinthians 10:23 source layer;
- a 10:23 English gloss;
- lexical notes on the permission, benefit, and build-up terms;
- the contested slogan reconstruction;
- our later “constructive” relational compression;
- a later systems-design transformation;
- a source correction locating “builds up” in 10:23 rather than 6:12.

This means Atlas can preserve the useful later compression without rewriting the source.

## New Librarian operation

The prototype adds:

[
oxed{	exttt{LAYERS}}
]

A reader can inspect all layers, or filter by type.

Examples:

    python -m code.atlas_demo layers paul-all-things-lawful

    python -m code.atlas_demo layers paul-all-things-lawful --type source_text

    python -m code.atlas_demo layers paul-all-things-lawful --type transformation

The result makes source and transformation inspectably different objects.

## What v0.2 still does not solve

Source layers do not yet model:

- competing manuscript witnesses;
- confidence calibration across scholarly claims;
- bibliographic identifiers;
- exact citation spans;
- relationships among multiple scholars;
- reader-specific assumption envelopes;
- temporal changes in interpretation;
- working-state versus consolidated-state plasticity.

Those should be added only when a specimen requires them.

## Design rule

> **Do not add ontology because it sounds useful. Add it when a real traversal breaks the current representation.**

The Pauline specimen earned Source Layers.

Future specimens should earn whatever comes next.
