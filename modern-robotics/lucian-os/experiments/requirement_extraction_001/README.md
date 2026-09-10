# REQUIREMENT_EXTRACTION_001 — Dedicated Run Folder

This folder exists to prevent command collisions while several Lucian OS experiments are being developed and run in parallel.

## Important

Run this experiment **from this folder**, not from the Lucian OS project root.

The frozen benchmark remains canonical at:

```text
../requirement_extraction_001.json
```

The shared v0.3 runner/evaluator remain in:

```text
../../prototype/
```

This folder is only a clean launch boundary. It does not duplicate or rewrite the frozen benchmark or shared architecture.

## First live run

From PowerShell:

```powershell
cd modern-robotics\lucian-os\experiments\requirement_extraction_001

.\run.ps1 -Model "ministral-3:3b-instruct-2512-q4_K_M"
```

The script:

1. requires an explicit model name;
2. sets `LUCIAN_MODEL` only for the launched Python processes;
3. runs only `REQUIREMENT_EXTRACTION_001`;
4. uses the frozen benchmark;
5. writes predictions and scores under this folder's local `results/` directory;
6. does not expose the embodiment capability menu to the host;
7. does not execute filesystem, network, or other Lucian OS capabilities.

## Model installation

The launch script does not pull models automatically. If the approved model is not installed yet, install it separately before running.

For the current first-run candidate:

```powershell
ollama pull ministral-3:3b-instruct-2512-q4_K_M
```

## Why this folder exists

Several Lucian OS research programs share the same repository and project root. A command such as:

```powershell
py prototype/some_experiment.py
```

is too easy to confuse with another chat's current experiment.

The dedicated-folder rule for this line of work is therefore:

> `cd` into `experiments/requirement_extraction_001/` and launch only through `run.ps1`.

This is an operational separation, not an architectural claim.
