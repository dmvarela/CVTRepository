# RELATIONAL_SEARCH_001 — First-Run Postmortem v0.01

## Status

Frozen postmortem of the first complete run. Do not rewrite `RELATIONAL_SEARCH_001.md`, its runner, or the preserved first-run outputs to make the experiment cleaner after the fact.

The first run is informative but not clean evidence for the full relational-search hypothesis.

## Preserved descriptive result

Model: `qwen3.5:2b-q4_K_M`

| condition | class | move | joint | pairs |
|---|---:|---:|---:|---:|
| baseline | 9/12 | 6/12 | 6/12 | 0/6 |
| principles_only | 10/12 | 6/12 | 6/12 | 0/6 |
| search_map | 9/12 | 7/12 | 7/12 | 1/6 |
| worked_search | 9/12 | 8/12 | 7/12 | 2/6 |
| coached_search | 9/12 | 8/12 | 6/12 | 2/6 |
| map_plus_coached | 9/12 | 8/12 | 7/12 | 2/6 |

Descriptively, richer search instruction changed movement selection and pair discrimination more than classification accuracy. This is not yet a clean causal conclusion because the audit below found design defects.

## Defect 1 — training/test surface leakage

The preregistration said training surfaces would be disjoint from held-out surfaces, but the actual materials contained close structural *and surface* neighbors.

Examples:

- training: workshop invitation explicitly withdrawn;
- held out: seminar invitation explicitly withdrawn;
- training: warning light crosses a caution threshold with no failure diagnostic;
- held out: temperature alarm crosses a warning threshold with no failure evidence.

Therefore some apparent transfer may be near-example reuse rather than distant relational transfer.

This is a harness defect. Preserve it; do not repair the historical experiment.

## Defect 2 — movement target was underspecified

`next_move` was scored as `LAND | HOLD | RETURN`, but the target proposition of that move was not explicit.

For example:

```text
classification = RISK_SIGNAL_ESTABLISHED_ONLY
```

can coherently support:

```text
LAND on: a risk signal exists
```

while the frozen answer key expected:

```text
HOLD on: the cooling system has failed
```

Likewise:

```text
CAUSATION_NOT_ESTABLISHED
```

can be a warranted landing about the epistemic state while also implying HOLD on the causal attribution.

Therefore:

> **A movement requires an explicit target claim.**

This becomes a design requirement for `RELATIONAL_SEARCH_002`.

## Finding 3 — overclaim and underclaim are separate failures

The original motivation emphasized overclaiming. The first run also showed the opposite failure: richer search instruction could make the host overly skeptical even when the prompt supplied strong warrant.

Truth calibration therefore requires both:

```text
do not claim beyond warrant
and
do not withhold what warrant establishes
```

Future scoring should separate:

- overclaim;
- underclaim;
- correct unresolved state.

## Finding 4 — RETURN label is not Return competence

The equal-authority Gate 4 -> Gate 12 family was especially diagnostic. In at least one trained condition the host selected the label `RETURN` while retaining the earlier Gate 4 classification.

Thus:

> **Naming RETURN is not the same as revising the represented state.**

This motivates separating:

```text
REOPEN = search must resume because relevant state changed
RETURN = the prior state was actually revised with provenance preserved
```

## Finding 5 — current host weakness around supersession

A separate Lucian OS v0.2 Gate 4 -> Gate 12 run supplied a later equally authoritative report in ordered trajectory context. The host repeated essentially the prior search state rather than revising it.

This is consistent with the competence manifest already marking contrary-evidence revision and correction continuity as not validated.

No conclusion should be drawn that the host cannot ever learn this movement. The narrow observation is that the current prompting/architecture did not reliably elicit it.

## Consequence for the research program

`RELATIONAL_SEARCH_001` remains useful as a discovery experiment, not as a clean validation experiment.

The next tests are split deliberately:

1. `RELATIONAL_SEARCH_002` — target-specific warrant calibration;
2. `RETURN_TRIGGER_001` — externally triggered reopening followed by host re-evaluation.

Do not build Lucian OS v0.03 from positive assumptions. Let those tests earn the architectural change.

## Research principle

> A failed or contaminated experiment can still be scientifically productive if its provenance is preserved and its defects are allowed to change the next question.
