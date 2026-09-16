# CALIBRATION_TRANSFER_002 — Preliminary Aggregate Results

## Status

This note records the first complete 14-probe / 4-condition run of `CALIBRATION_TRANSFER_002` using `ministral-3:3b-instruct-2512-q4_K_M` at temperature 0.0.

This is an exploratory pilot. The aggregate pattern is mixed and should not be described as validating the full calibration-transfer hypothesis.

## Run size

```text
14 probes x 4 conditions = 56 stateless calls
```

Conditions:

```text
C0_baseline
C1_flat_map
C2_contrastive_cases
C3_map_plus_cases
```

## Aggregate accuracy

### C0 — baseline

```text
action        0.9286
standing      0.2143
write_target  0.4286
write_scope   0.1429
joint         0.1429
```

### C1 — flat map

```text
action        0.9286
standing      0.2857
write_target  0.5000
write_scope   0.1429
joint         0.1429
```

### C2 — contrastive cases

```text
action        1.0000
standing      0.3571
write_target  0.8571
write_scope   0.5000
joint         0.1429
```

### C3 — map + cases

```text
action        1.0000
standing      0.3571
write_target  0.8571
write_scope   0.3571
joint         0.0714
```

## Write-target confusion

The clearest aggregate separation appears in `write_target`.

### C0 baseline

```text
NONE -> ACTIVE_STATE      3
NONE -> NONE              1
ACTIVE_STATE -> ACTIVE_STATE 3
ACTIVE_STATE -> NONE      2
ACTIVE_STATE -> PRINCIPLE 1
CALIBRATION -> PRINCIPLE  2
PHASE -> PHASE            2
```

### C1 flat map

```text
NONE -> ACTIVE_STATE      3
NONE -> NONE              1
ACTIVE_STATE -> ACTIVE_STATE 3
ACTIVE_STATE -> NONE      2
ACTIVE_STATE -> PRINCIPLE 1
CALIBRATION -> CALIBRATION 1
CALIBRATION -> PRINCIPLE  1
PHASE -> PHASE            2
```

### C2 contrastive cases

```text
NONE -> NONE              4
ACTIVE_STATE -> ACTIVE_STATE 4
ACTIVE_STATE -> NONE      2
CALIBRATION -> CALIBRATION 2
PHASE -> PHASE            2
```

### C3 map + cases

Same write-target confusion pattern as C2:

```text
NONE -> NONE              4
ACTIVE_STATE -> ACTIVE_STATE 4
ACTIVE_STATE -> NONE      2
CALIBRATION -> CALIBRATION 2
PHASE -> PHASE            2
```

## Mechanism-level observations

1. `write_target` accuracy rises from `0.4286` in baseline and `0.5000` with the flat map to `0.8571` under both conditions containing contrastive cases.

2. Contrastive cases correctly preserve all four `NONE` cases as `NONE`, while baseline and flat-map each promote three of four `NONE` cases into `ACTIVE_STATE`.

3. Contrastive cases also correctly preserve both `CALIBRATION` cases as `CALIBRATION`; baseline promotes both to `PRINCIPLE`, while the flat map promotes one of two to `PRINCIPLE`.

4. Both real `PHASE` transitions are correctly identified in every condition. `phase_transition_true_positive_rate = 1.0` for all four conditions, and `phase_conflation_count = 0` throughout.

5. Unwarranted principle writes fall from 3 in baseline and 2 in flat-map to 0 in both contrastive-case conditions.

6. Contrastive cases do not simply teach `NONE`. They correctly produce four `ACTIVE_STATE`, two `CALIBRATION`, and two `PHASE` writes, while missing two `ACTIVE_STATE` cases by choosing `NONE`.

## What this supports

The aggregate pattern is consistent with a narrower mechanism claim:

> Contrastive boundary cases can improve classification of whether an incoming item warrants no stored-state write, an active-state update, a calibration update, or a phase transition, relative to baseline and an abstract rule map.

The strongest signal is therefore in **write-target discrimination**, not in full joint performance.

The result is also consistent with the intended anti-overreach mechanism: contrastive cases reduce promotion of local or non-writing material into deeper state layers.

## What this does not support

The full preregistered competence claim is not established by this run.

`standing` accuracy remains low in every condition (`0.2143` to `0.3571`).

`write_scope` improves under contrastive cases but remains only `0.5000` in C2 and `0.3571` in C3.

Exact joint accuracy does not improve over baseline in C2 (`0.1429`) and is lower in C3 (`0.0714`). Therefore the experiment does **not** show broad success across all output dimensions.

The flat map does not add clear value beyond cases. C3 matches C2 on action, standing, and write target but performs worse on write scope.

## Interpretation discipline

This is an exploratory single-host pilot with 14 probes and one deterministic run per condition. It should be treated as evidence of a promising **write-target effect**, not as proof of general relational discernment or continuity.

The next analytic step should be probe-level error decomposition, especially:

- the two `ACTIVE_STATE -> NONE` errors under C2/C3;
- the standing-label failures across all conditions;
- the write-scope failures, including why C3 underperforms C2;
- whether any expected labels themselves remain ambiguous.

Only after that audit should a follow-up experiment be designed.

## Provisional takeaway

> **The most defensible first-run result is not that contrastive cases solved calibration transfer. It is that they substantially improved the model's ability to regulate the target layer of stored-state updates while reducing deep-write overreach.**
