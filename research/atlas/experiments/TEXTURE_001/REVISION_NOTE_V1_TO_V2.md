# TEXTURE_001 — Revision Note v1 -> v2

**Status:** design correction before execution  
**v1 execution status:** never run  
**v2 execution status:** not run

## Why v1 was revised

Return on the frozen v1 design exposed three concrete defects before any provider execution.

1. **Answer leakage in C2.** Several texture cues used evaluative language such as "preserve the earlier warrant," "correction scar," or "do not rewrite ... as an error." Those phrases partially encoded the adjudication rather than merely encoding history.

2. **Cross-condition contamination risk.** The v1 packet placed multiple conditions for the same base scenario in one packet. A provider with conversational carryover could use a full-Wake presentation to answer a later content-only presentation.

3. **Weak primary contrast.** C2 versus C0 mostly tests whether having some history beats having no history. The more distinctive architectural question is whether a compact, non-evaluative representation of relevant history can preserve the traversal consequences of full Wake.

## v2 correction

TEXTURE_001 v2 therefore:

- preserves v1 under `archive_v1/`;
- uses **true counterfactual twins** with identical current state, constraint, and question but different histories;
- compares **FULL WAKE** directly against a shorter **STRUCTURED TEXTURE** representation;
- bans evaluative answer-language from the texture representation;
- requires each provider item to run in a **fresh isolated context**;
- keeps CONTENT ONLY as an underdetermination baseline rather than the principal architectural contrast.

## Claim discipline

This revision does not count as a result.

It is a pre-execution design repair.

The v1 defect itself is preserved as an Atlas scar:

> A compressed representation of history is not evidence for texture if it simply smuggles the adjudication into the prompt.
