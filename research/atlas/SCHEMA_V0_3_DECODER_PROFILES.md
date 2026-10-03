# Atlas Schema v0.3 — Decoder Profiles

**Status:** implemented in prototype  
**Purpose:** represent the receiving context that participates in decompression.

## Why v0.3 exists

Source Layers v0.2 made source text, translation, reconstruction, interpretation, and transformation inspectably different.

The **nephesh** specimen exposed the next failure:

Even perfectly separated source layers can still be reconstructed badly when a receiving language or culture silently contributes assumptions that are not guaranteed by the source.

So the transfer problem is not only:

[
X_s ightarrow hat X
]

but:

[
oxed{
X_s + A_s + D_r ightarrow hat X_r
}
]

where:

- (X_s) = source object;
- (A_s) = source assumption envelope;
- (D_r) = receiving decoder profile;
- (hat X_r) = reconstructed object.

## Decoder Profile

A Decoder Profile is a provisional model of assumptions active in a **receiving context**.

It is not a psychological diagnosis and must not be inferred from a person's demographic identity.

The current fields are:

```text
profile_id
context
likely_assumptions
assumptions_not_guaranteed
needed_distinctions
mismatch_risks
preparation_notes
status
provenance
```

## Core rule

> **Profile the decoding context, not the person.**

For example, Atlas may model the common conceptual baggage carried by the modern English word **soul**.

It should not infer that a particular English-speaking reader therefore holds every listed assumption.

The reader can correct the Decoder Profile.

## First earned profile

The **nephesh** specimen adds:

```text
profile_id: modern-english-soul
```

The profile records a possible receiving context in which “soul” suggests:

- immateriality;
- body/soul separability;
- uniquely human identity;
- postmortem persistence;
- transparent equivalence between “soul” and **nephesh**.

Atlas separately records that those implications are **not guaranteed by the Hebrew lexeme alone**.

It also records the opposite risk: correcting the English dualistic frame should not harden into a new universal claim that **nephesh** can never be conceived as separable in any biblical context.

## New Librarian verb

The prototype adds:

[
oxed{	exttt{DECODER}}
]

Examples:

    python -m code.atlas_demo decoder nephesh-decoder-mismatch

    python -m code.atlas_demo decoder nephesh-decoder-mismatch --profile modern-english-soul

The output exposes:

- source assumptions;
- generic decoder prerequisites;
- likely receiving assumptions;
- assumptions not warranted by the source;
- mismatch risks;
- preparation notes.

## Translation now includes decoder preparation

A TRANSLATE packet now includes both:

[
	ext{source-side structure}
]

and:

[
	ext{receiver-side preparation}.
]

That makes translation explicitly relational:

[
oxed{
	ext{translation}
=
f(	ext{source},	ext{receiver},	ext{target context})
}
]

rather than treating translation as a lookup table between labels.

## What v0.3 still does not solve

Decoder Profiles are currently hand-authored.

Atlas does not yet:

- infer a reader's actual assumptions;
- ask the reader calibration questions;
- compare multiple decoder contexts automatically;
- learn a decoder profile over time;
- separate user-specific state from general cultural/disciplinary context;
- quantify mismatch confidence.

Those should be added only if later specimens require them.

## Safety / agency constraint

A Decoder Profile must never become an excuse for Atlas to tell a reader what they believe.

The correct language is:

> “This receiving context often carries these assumptions. Which, if any, are active for you?”

not:

> “Because you belong to this group, you believe these things.”

This constraint is architectural, not cosmetic.

## Design lesson

The first source-rich specimen forced Atlas to represent the **source more carefully**.

The second forced Atlas to represent the **receiver more carefully**.

The emerging transfer architecture is therefore genuinely relational:

[
oxed{
	ext{Source}
leftrightarrow
	ext{Librarian}
leftrightarrow
	ext{Reader}
}
]
