# REQUIREMENT_EXTRACTION_001 — First Live Runbook

## Candidate first host

Use an explicitly selected non-China local substrate:

```text
ministral-3:3b-instruct-2512-q4_K_M
```

The v0.3 code has no default model. The benchmark must not fall back to a historical host implicitly.

## PowerShell

From the Lucian OS directory:

```powershell
ollama pull ministral-3:3b-instruct-2512-q4_K_M
$env:LUCIAN_MODEL="ministral-3:3b-instruct-2512-q4_K_M"

py prototype/run_requirement_extraction_v001.py `
  --benchmark experiments/requirement_extraction_001.json `
  --output results/requirement_extraction_001_ministral3_3b.json

py prototype/evaluate_requirement_extraction_v001.py `
  --benchmark experiments/requirement_extraction_001.json `
  --predictions results/requirement_extraction_001_ministral3_3b.json `
  --output results/requirement_extraction_001_ministral3_3b_score.json
```

## Contamination controls

Before the first run:

- do not edit the frozen benchmark;
- do not show the host `windows_dev_host_composition_lab.json`;
- do not give the host concrete provider names;
- do not tune the prompt against individual benchmark cases;
- preserve raw output even when malformed or poor.

## First review order

Review failures in this order:

1. forbidden destructive needs;
2. lost user boundaries;
3. concrete provider-name leakage;
4. missing requirements;
5. extra requirements;
6. ontology disagreements where the model may have found a legitimate alternative decomposition.

## Decision rule

Do not repair the benchmark after seeing an inconvenient result merely to improve the score.

If the host exposes a real weakness in the frozen reference ontology, record that as a benchmark defect with provenance and create a later benchmark version. Preserve v0.01 unchanged.
