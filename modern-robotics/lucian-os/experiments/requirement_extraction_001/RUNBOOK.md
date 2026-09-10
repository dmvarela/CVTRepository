# REQUIREMENT_EXTRACTION_001 — First Live Runbook

## Candidate first host

Use an explicitly selected non-China local substrate:

```text
ministral-3:3b-instruct-2512-q4_K_M
```

Lucian OS v0.3 has no default model. This benchmark must not fall back to a historical host implicitly.

## PowerShell

From this directory:

```powershell
cd modern-robotics\lucian-os\experiments\requirement_extraction_001
.\run.ps1 -Model "ministral-3:3b-instruct-2512-q4_K_M"
```

If the model is not installed yet:

```powershell
ollama pull ministral-3:3b-instruct-2512-q4_K_M
```

The launcher uses only files in this experiment folder plus the shared Lucian OS v0.3 relational-search engine in `../../prototype/`.

## Contamination controls

Before the first run:

- do not edit `benchmark.json`;
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
