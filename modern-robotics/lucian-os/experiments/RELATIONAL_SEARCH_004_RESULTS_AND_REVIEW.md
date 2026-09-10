# RELATIONAL_SEARCH_004 — Results and Review

## Status

First complete run reviewed. Preserve the raw run exactly.

Model actually used: `ministral-3:3b-instruct-2512-q4_K_M`

Run timestamp: `2026-09-10T21:56:36Z`

Preregistered primary outcomes:

- active-relation accuracy;
- exact-vector accuracy.

Raw artifact fingerprints:

- `relational_search_004_20260910T213434Z.jsonl` — SHA-256 `78fec55200ec0d2ff3fdba2cb38b9babfb2a9655cfb75a5928ff1a10c7fa9541`
- `relational_search_004_20260910T213434Z_summary.json` — SHA-256 `3e44b40071af5ff78881cc695febc59bda855b847e535fb689ce625fb5485060`

## Important host substitution

RS-004 ran on Ministral rather than the earlier Qwen development host. Therefore direct score comparison with RS-003 cannot be interpreted as a clean continuation effect. Within-run condition comparisons remain usable because all RS-004 conditions used the same host.

This accidental substitution is itself relevant to the Lucian OS portability program, but no cross-host portability claim should be made from one run.

## Summary

| condition | active relation | exact vector | host status | kernel status | aggregation consistent | kernel recovery | FAIL→UNKNOWN |
|---|---:|---:|---:|---:|---:|---:|---:|
| format_only | 11/12 | 2/12 | 11/12 | 9/12 | 10/12 | 0 | 1 |
| generic_warrant | 10/12 | 2/12 | 11/12 | 9/12 | 10/12 | 0 | 2 |
| relation_vector_map | 10/12 | 6/12 | 11/12 | 11/12 | 12/12 | 0 | 2 |
| worked_relation_vector | **12/12** | 2/12 | 9/12 | 9/12 | 12/12 | 0 | 0 |

## Primary result 1 — active relation detection

The worked relation-vector condition achieved `12/12` active-relation accuracy and `4/4` complete active triplets.

This is the strongest active-relation result in the run:

- format_only: 11/12;
- generic_warrant: 10/12;
- relation_vector_map: 10/12;
- worked_relation_vector: 12/12.

The worked condition also produced zero `FAIL_AS_UNKNOWN` errors on the active dimension.

This is compatible with the hypothesis that worked examples improve discrimination among `PASS`, `FAIL`, and `UNKNOWN` for the relation currently under test.

Because n=12 and the host differs from RS-003, this remains an exploratory pilot result rather than a general capability claim.

## Primary result 2 — exact-vector metric exposed a representation problem

The worked condition achieved only `2/12` exact-vector accuracy despite perfect active-relation accuracy.

The dominant reason is that Ministral frequently marked **non-active diagnosticity** as `UNKNOWN` in cases involving authoritative commands, state updates, or temporal revisions.

Examples include:

- a verified release officer authorized to change sample release state;
- a valid safety-controller command concerning the correct storage bin;
- a later authoritative route-plan revision that explicitly supersedes the earlier one.

In these cases the preregistered expected vector forced `diagnosticity_relation = PASS`, but the host instead treated diagnosticity as not established or not naturally applicable.

This means the experiment's simplification

```text
all non-active relations = PASS
```

was too strong.

The low exact-vector score therefore cannot be interpreted simply as poor relation detection. It exposes a design problem in the relation ontology.

## Kernel result — no recovery

`kernel_recovery = 0` in every condition.

The deterministic outer gate did not rescue any incorrect host aggregation in this run.

More importantly, it sometimes made a correct host-level conclusion worse. When the host emitted an unnecessary non-active `UNKNOWN`, the deterministic rule

```text
any UNKNOWN -> HOLD
```

converted an otherwise correct `SUFFICIENT / WRITE` case into `UNRESOLVED / HOLD`.

Examples in `worked_relation_vector`:

- `AUTH_PASS_RELEASE_OFFICER`;
- `REL_PASS_BIN_C`;
- `TEMP_PASS_LATER_REVISION`.

In all three, the active relation was correctly `PASS`; the error arose because `diagnosticity_relation` was marked `UNKNOWN` outside the active dimension.

Thus RS-004 does **not** support the proposed deterministic gate as currently represented.

## Architectural interpretation

The run suggests that the useful decomposition is still:

```text
semantic relation detection
-> standing aggregation
-> state-write decision
```

but the relation vector cannot assume that every dimension is always applicable.

The missing state appears to be something like:

```text
N/A / NOT_APPLICABLE
```

or, more generally, an explicit applicability relation that determines which dimensions are required for the current signal-target pair.

This matters because:

```text
UNKNOWN != N/A
```

- `UNKNOWN` means the relation matters but its status is not established.
- `N/A` means the relation is not required for this kind of proposed update.

Treating `N/A` as `UNKNOWN` creates unnecessary HOLD states.
Treating `N/A` as `PASS` can fabricate positive evidence that was never supplied.

Therefore the next repair should not merely tune prompts. It should repair the ontology.

## Post-hoc diagnostic observation

If only the preregistered active dimension is considered, the worked condition classifies all 12 triplet members correctly.

This is **not** a replacement primary endpoint and should not be used to erase the exact-vector failure. It is useful only diagnostically: it shows that the residual problem lies mainly in representation of inactive dimensions, not in the active PASS/FAIL/UNKNOWN distinction under worked examples.

## Recommended next step

Before any dynamic HOLD→WRITE experiment, repair the relation representation.

A candidate RS-004B should test:

```text
PASS | FAIL | UNKNOWN | N/A
```

with explicit definitions:

- `PASS`: required relation is established and permits update;
- `FAIL`: required relation is established and blocks update;
- `UNKNOWN`: required relation matters, but supplied evidence does not establish pass/fail;
- `N/A`: relation is not required for this signal-target update type.

The deterministic gate should aggregate only **applicable required relations**:

```text
if any applicable required relation == FAIL:
    NO_WRITE
elif any applicable required relation == UNKNOWN:
    HOLD
elif all applicable required relations == PASS:
    WRITE
```

`N/A` should be neutral rather than silently converted to PASS or UNKNOWN.

RS-004B should include matched cases where a dimension is deliberately:

- PASS;
- FAIL;
- UNKNOWN;
- N/A;

so that applicability itself is tested rather than assumed.

Only after this repair should the project evaluate whether a deterministic standing gate improves host decisions in dynamic state-update sequences.

## Bottom line

RS-004 produced a mixed but useful result:

1. worked examples produced perfect active PASS/FAIL/UNKNOWN discrimination on this run;
2. exact-vector performance remained poor because the ontology forced inactive relations to PASS;
3. the deterministic gate produced no recoveries and sometimes degraded correct host decisions;
4. the run therefore exposed `UNKNOWN != N/A` as the next architectural distinction to test.

This is a representation-layer finding, not evidence that the membrane hypothesis is confirmed.