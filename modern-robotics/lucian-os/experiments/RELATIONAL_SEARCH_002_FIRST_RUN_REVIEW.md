# RELATIONAL_SEARCH_002 — First-Run Review

## Status

Post-run review of the preserved first complete run from 2026-09-09 UTC.

Do **not** revise the preregistration or reinterpret the first run as if this issue had been anticipated. The original protocol remains frozen in `RELATIONAL_SEARCH_002.md`.

## First-run summary

Model: `qwen3.5:2b-q4_K_M`

| condition | valid | status correct | move correct | joint correct | pairs correct | overclaim | underclaim | polarity |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| baseline | 0/12 | 10/12 | 0/12 | 0/12 | 0/6 | 0 | 0 | 2 |
| principles_only | 0/12 | 7/12 | 0/12 | 0/12 | 0/6 | 3 | 0 | 2 |
| target_warrant_map | 0/12 | 8/12 | 0/12 | 0/12 | 0/6 | 2 | 0 | 1 |
| worked_target_warrant | 12/12 | 8/12 | 8/12 | 8/12 | 3/6 | 1 | 3 | 0 |

## Main methodological finding

The large apparent gain in joint accuracy under `worked_target_warrant` is confounded with **output-format apprenticeship**.

The runner required literal string values:

```text
move_on_target = LAND | HOLD
```

but the non-worked conditions often returned a Boolean-like value instead, making the whole object invalid and forcing move accuracy to zero even when the target-status classification itself was correct.

Therefore the first run does **not** support the strong claim:

> Worked target-warrant examples improved relational reasoning.

The defensible claim is narrower:

> Worked examples strongly improved compliance with the operational output language, while their effect on epistemic target-status calibration was mixed.

This matters because baseline target-status accuracy was `10/12`, higher than `worked_target_warrant` at `8/12`.

## Error geometry under worked_target_warrant

The worked condition solved all members of three paired families:

- authority;
- causation;
- document authenticity.

It failed in families where evidence must be weighted by its **relation to the target and to competing evidence**:

1. **Risk / diagnosis** — an alarm threshold was treated as if it carried diagnostic standing about pump failure, or the absence of a confirming diagnostic was treated as contrary evidence rather than missing evidence.
2. **Invitation / authority** — an objection from an attendee without stated authority was given enough weight to weaken an organizer-issued invitation.
3. **Gate / temporal authority** — the host did not reliably distinguish a later equally authoritative update from a later weak unauthoritative source.

## Working interpretation

The first run suggests a possible distinction between:

```text
seeing evidence
```

and

```text
assigning that evidence standing to update a target state
```

A later statement is not automatically an update.
A contrary statement is not automatically contradictory evidence.
An alarm is not automatically a diagnosis.
Absence of confirmation is not automatically negation.

A candidate Lucian OS primitive is therefore:

> **Evidence may arrive without automatically receiving write-access to the represented state.**

This remains a hypothesis, not a result of RS-002.

## Required next step

Run `RELATIONAL_SEARCH_002B` with **format apprenticeship held constant across all conditions**.

Primary outcome: target-status accuracy.

Schema validity and LAND/HOLD compliance become manipulation checks rather than evidence of improved reasoning.

Only after the format confound is isolated should a new experiment test relational evidential standing directly.
