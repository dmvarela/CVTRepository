# IDENTITY_AMORTIZATION_001 — First-Run Harness Repair

## Status

Execution note recorded after the first attempted local run and before any interpretation of experimental results.

The first attempt did not complete. It exposed two harness defects. The partial observations must therefore be treated as **diagnostic only**, not as evidence for or against the identity-amortization hypothesis.

## First-run failure 1 — truncated model JSON

The original host call used:

```text
num_predict = 350
```

On task 5, full-identity condition, the Qwen response ended in the middle of the `uncertainties` array. The parser raised:

```text
ValueError: Model did not return JSON
```

Inspection of the raw output showed a syntactically incomplete JSON object ending mid-sentence. This is consistent with generation truncation rather than a conceptual model failure.

### Repair

- request Ollama JSON mode with `format: "json"`;
- increase `num_predict` from 350 to 800;
- expose `done_reason` in host metrics;
- improve parser error text so malformed/truncated output is distinguished clearly.

All experimental conditions use the same repaired generation settings.

## First-run failure 2 — UNKNOWN could match KNOWN

The original residual checker used substring tests such as:

```python
"known" in epistemic_status
```

This is semantically invalid because:

```text
"known" in "unknown" == True
```

Likewise, substring matching can confuse other negated or prefixed terms such as `unconfirmed` with `confirmed`.

This means some `HIGH` residuals from the partial first run may be checker false positives and must not be attributed to the host model.

### Repair

The checker now uses lexical word-boundary matching for certainty terms. The authority residual was also made more conservative so mentioning an action such as `do not delete` is not mistaken for a direct execution proposal.

A `HIGH` residual remains only a **review flag**. It does not certify that the host violated a Lucian invariant.

## First-run failure 3 — completed rows were not crash-safe

The original runner accumulated rows in memory and wrote the JSONL file only after all 24 conditions completed.

Therefore one late parser failure could destroy the record of all earlier completed observations.

### Repair

The runner now:

- creates the output artifact before execution;
- appends and flushes one row after every condition;
- records condition-level exceptions as `status: ERROR` rows;
- continues remaining conditions after an isolated failure;
- exits nonzero at the end if any errors were recorded.

## Experimental consequence

The initial console output from tasks 1–4 and task 5/no-identity is preserved only as a harness-development observation.

It should **not** be pooled with the repaired rerun because the generation cap, JSON mode, and residual-check logic changed.

The experiment should be restarted from task 1 under the repaired harness.

## Important methodological lesson

The first execution reproduced a recurring Lucian OS principle at the level of the experiment itself:

> **A test can fail because the measurement relation is wrong, not because the tested system is wrong.**

And more specifically:

> **UNKNOWN must not be allowed to become KNOWN through a string-matching accident.**

This note preserves the failure rather than silently overwriting it.
