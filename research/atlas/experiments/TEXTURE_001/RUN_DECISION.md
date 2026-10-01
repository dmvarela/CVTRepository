# TEXTURE_001 — Run Decision

**Status:** EXECUTION AUTHORIZED BY USER  
**Date:** 2026-09-30  
**Design:** v2.1  
**Scope:** first bounded provider run only

## Frozen provider decision

**Provider:** OpenAI / ChatGPT  
**Model:** GPT-5.6 Sol  
**Reasoning level:** High  
**Execution interface:** Unpersonalized Temporary Chat  
**Context rule:** one fresh Temporary Chat per item  
**Item count:** 20  
**Sampling:** provider default; ChatGPT does not expose a user-settable temperature here  
**Retry policy:** no retries  
**Malformed output policy:** preserve the first raw response exactly; do not repair or replace it  
**Adjudication:** prohibited until all intended raw outputs are frozen

## Why this interface

For this first zero-extra-cost run, isolation will be implemented using **Unpersonalized Temporary Chats**.

Each item must be run in a new Temporary Chat configured as **Unpersonalized**, so that ordinary memory, custom instructions, and plugins are not used for that chat.

The execution process must not save or continue one item into another.

## Execution order

Use the frozen item order from `CASES_BLINDED.md`.

Each item must be submitted independently:

[
T_i
ightarrow
	ext{new unpersonalized Temporary Chat}_i
ightarrow
O_i
ightarrow
	ext{close context}_i.
]

No provider context may contain another TEXTURE_001 item or prior TEXTURE_001 output.

## Recording rule

Every result must be recorded with:

- provider: OpenAI / ChatGPT;
- model: GPT-5.6 Sol;
- reasoning level: High;
- item ID stored outside the provider-visible prompt;
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

Adjudication may begin only after all 20 raw results are recorded and frozen by the harness.

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

## Claim boundary

Authorization to execute does not authorize:

- changing the frozen cases;
- changing the answer key;
- retrying failures;
- merging the Atlas PR;
- promoting Texture to a first-class Atlas schema object before adjudication.
