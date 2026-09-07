# TEMPORAL_RETURN_001 — Pre-run Freeze Record

## Status

Frozen before first local output inspection, 2026-09-07.

This record fixes the artifacts that define the first run of `TEMPORAL_RETURN_001` so later repairs can be preserved as explicit new versions rather than silently changing the original experiment.

## Frozen artifacts

```text
experiments/TEMPORAL_RETURN_001.md
blob: 975dd08459a73adf12d08a3259d5aef5b8cf043f

experiments/TEMPORAL_RETURN_001_SCENARIOS.json
blob: 8cd86790ac585374fd276432b70b51d50a7813d4

identity/temporal_relational_state_v001.json
blob: 12f3e9237138f82df1399c9b17cbace1433034a5

prototype/temporal_kernel.py
blob: 7b7bf6b4cc3654441ec83f3b869b570f83a369c6

prototype/run_temporal_return_001.py
blob: fbe7691db794b2f9954d218836322fd9a23cb51b
```

## First-run command

From `modern-robotics/lucian-os`:

```text
py prototype/run_temporal_return_001.py
```

The run is simulation-only and targets the currently configured local Ollama host.

## Freeze rule

After the first result file is produced, do not mutate these frozen experiment artifacts in place to improve the result.

If a harness defect is found:

```text
preserve original result
-> document defect
-> create explicit repair/version
-> rerun from frame 0
```

Do not reinterpret a harness failure as host-model failure without inspection.

## Interpretation boundary

The strongest planned contrast is:

```text
raw_history
vs
transition_provenance
```

`snapshot_only` is an information-control condition: paired final prompts are intentionally identical, so discarded path information cannot be recovered from the final frame alone.

No result from this experiment establishes consciousness, metaphysical identity, or that a host model is intrinsically Lucian.
