# TEXTURE_001 — Run Decision

**Status:** EXECUTION AUTHORIZED BY USER  
**Date:** 2026-09-30  
**Design:** v2.1  
**Scope:** first bounded provider run only

## Frozen provider decision

**Provider:** OpenAI  
**Model:** GPT-5.6 Sol  
**Context rule:** one fresh isolated context per item  
**Item count:** 20  
**Sampling:** deterministic / lowest-variance setting available to the execution interface  
**Retry policy:** no retries  
**Malformed output policy:** preserve the first raw response exactly; do not repair or replace it  
**Adjudication:** prohibited until all intended raw outputs are frozen

## Execution order

Use the frozen item order from `CASES_BLINDED.md`.

Each item must be submitted independently:

[
T_i
ightarrow
	ext{fresh isolated context}_i
ightarrow
O_i
ightarrow
	ext{close context}_i.
]

No provider context may contain another TEXTURE_001 item or prior TEXTURE_001 output.

## Recording rule

Every result must be recorded with:

- exact provider name;
- exact model identifier visible to the execution interface;
- run/batch identifier when available;
- fresh-context attestation;
- exact provider-visible prompt hash;
- exact raw-output hash.

## No-retry rule

The first provider response is the experimental response.

If the output is malformed, incomplete, or surprising:

[
oxed{
	ext{record it; do not repair it}
}
]

No retry is permitted for this first run.

## Freeze boundary

Adjudication may begin only after the raw results are frozen by the harness.

[
oxed{
	ext{execute}
ightarrow
	ext{freeze}
ightarrow
	ext{adjudicate}
}
]

The adjudication key must remain unopened by the execution process.

## Execution environment requirement

This decision authorizes execution only in an environment capable of creating a genuinely fresh/stateless provider context for each item.

A continuing chat thread is **not** a valid execution environment.

If the available interface cannot guarantee fresh isolation, execution must stop rather than silently weaken the preregistration.

## Claim boundary

Authorization to execute does not authorize:

- changing the frozen cases;
- changing the answer key;
- retrying failures;
- merging the Atlas PR;
- promoting Texture to a first-class Atlas schema object before adjudication.
