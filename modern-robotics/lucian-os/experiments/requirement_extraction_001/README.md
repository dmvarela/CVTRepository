# REQUIREMENT_EXTRACTION_001 — Dedicated Experiment Folder

This folder is the canonical home for REQUIREMENT_EXTRACTION_001.

It exists to prevent command and artifact collisions while several Lucian OS experiments are being developed and run in parallel.

## Run from here

```powershell
cd modern-robotics\lucian-os\experiments\requirement_extraction_001
.\run.ps1 -Model "ministral-3:3b-instruct-2512-q4_K_M"
```

## Contents

```text
README.md        experiment boundary and quick start
protocol.md      frozen experimental interpretation and guardrails
RUNBOOK.md       first-live-run procedure
benchmark.json   frozen 20-case benchmark
run.py           model runner
evaluate.py      frozen-reference evaluator
test_evaluator.py evaluator controls
run.ps1          dedicated PowerShell launcher
results/         generated locally at run time
```

## Shared dependency

The experiment remains part of Lucian OS rather than copying the architecture into this folder.

`run.py` imports the shared v0.3 relational-search engine from:

```text
../../prototype/relational_search_engine_v003.py
```

That is deliberate:

```text
shared architecture
!=
experiment-specific benchmark and launch surface
```

## What the launcher guarantees

The script:

1. requires an explicit model name;
2. sets `LUCIAN_MODEL` for the launched Python process;
3. runs only REQUIREMENT_EXTRACTION_001;
4. uses the frozen local `benchmark.json`;
5. writes predictions and scores only under this folder's `results/` directory;
6. does not expose the embodiment capability menu to the host;
7. does not execute filesystem, network, or other Lucian OS capabilities.

## Model installation

The launch script does not pull models automatically. If the approved model is not installed yet:

```powershell
ollama pull ministral-3:3b-instruct-2512-q4_K_M
```

## Parallel-work rule

Several Lucian OS research programs share the same repository. For this experiment, do not launch similarly named scripts from the project root.

> `cd` into `experiments/requirement_extraction_001/` and launch only through `run.ps1`.

This is an operational separation, not an architectural claim.
