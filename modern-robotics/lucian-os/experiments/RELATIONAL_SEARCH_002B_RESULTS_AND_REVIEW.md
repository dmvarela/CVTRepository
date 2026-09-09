# RELATIONAL_SEARCH_002B — Results and Review

## Status

First complete run reviewed. Preserve the raw run exactly.

Model: `qwen3.5:2b-q4_K_M`

Run timestamp: `2026-09-09T05:30:04Z`

Primary outcome: target-status accuracy.

Raw artifact fingerprints:

- `relational_search_002b_20260909T050951Z.jsonl` — SHA-256 `b2a7ebcb48669f698ee035ebe696a501306444879881d7b9953311c3cca1cf79`
- `relational_search_002b_20260909T050951Z_summary.json` — SHA-256 `b7387273f66a22c1bba6eeedf06a8e68e313253df483f1c53f94b03d0846df88`

## Summary

| condition | status correct | status pairs | overclaim | underclaim | polarity | schema valid | mapping consistent |
|---|---:|---:|---:|---:|---:|---:|---:|
| format_only | 8/12 | 2/6 | 2 | 2 | 0 | 12/12 | 12/12 |
| format_plus_principles | 7/12 | 1/6 | 3 | 1 | 1 | 12/12 | 12/12 |
| format_plus_target_warrant_map | 7/12 | 1/6 | 3 | 0 | 2 | 12/12 | 12/12 |
| format_plus_worked_target_warrant | 8/12 | 3/6 | 1 | 3 | 0 | 12/12 | 12/12 |

## Primary conclusion

The RS-002 format confound was successfully removed: every condition produced valid schema, valid LAND/HOLD tokens, and internally consistent status-to-move mappings on all 12 cases.

However, explicit warrant training did **not** improve overall semantic accuracy in this pilot.

- `format_only`: 8/12
- `format_plus_worked_target_warrant`: 8/12
- principles and warrant-map conditions: 7/12

Therefore RS-002B does not support the strong hypothesis that worked target-warrant examples increase overall target-status accuracy on these held-out claims.

## Paired comparison: format_only vs worked examples

The two conditions tie in aggregate but disagree on four cases:

### Worked fixes cases missed by format_only

- `AUTH_RULE_EXCLUDES_OWNER`: worked correctly returns `CONTRADICTED`.
- `DOC_VISUAL_SIMILARITY_ONLY`: worked correctly returns `UNRESOLVED`.

### Worked breaks cases solved by format_only

- `INVITE_UNAUTHORIZED_OBJECTION`: worked returns `UNRESOLVED` instead of `SUPPORTED`.
- `GATE_WEAK_LATER_SOURCE`: worked returns `UNRESOLVED` instead of `SUPPORTED`.

Both conditions fail:

- `RISK_THRESHOLD_ONLY`.
- `GATE_EQUAL_AUTHORITY_UPDATE`.

Thus the paired comparison is symmetric: format-only wins two discordant cases and worked examples win two.

## Stable semantic policy under worked examples

A notable secondary result is that the worked condition made **exactly the same 12 target-status classifications in RS-002B as in the first RS-002 run**, despite the addition of the common interface scaffold.

The free-text outputs changed in most cases, but the semantic labels did not.

This does not establish a learned capability, but it is consistent with worked examples inducing a stable decision policy or response geometry rather than merely teaching output format.

The stable family pattern is:

- authority: 2/2
- causation: 2/2
- document authenticity: 2/2
- risk: 1/2
- invitation: 1/2
- gate: 0/2

This is the same worked-condition success/failure geometry observed in RS-002.

## Error geometry

The worked condition appears to trade some overclaim risk for underclaim risk:

- overclaim: 1
- underclaim: 3
- polarity error: 0

Its failures cluster where evidence must be assigned **standing** relative to a target state:

1. **Diagnostic standing** — an alarm threshold does not itself diagnose a pump failure, and absence of a diagnostic is not negation.
2. **Authority standing** — an attendee without stated invitation authority should not automatically weaken an organizer-issued invitation.
3. **Temporal/source standing** — a later source should update an earlier state only when it has sufficient authority and relevance; equally authoritative later state reports may supersede earlier ones, while weak later sources may lack standing to do so.

## Important anomaly: risk case

In `RISK_THRESHOLD_ONLY`, the worked condition outputs `CONTRADICTED`, while its short explanation says the target cannot be proven and then confusingly says the prompt implies the alarm supports failure.

This is internally semantically incoherent even though the LAND/HOLD mapping is mechanically consistent with the emitted status token.

Therefore future experiments should distinguish:

- schema/token consistency;
- semantic label accuracy;
- relation-level explanation coherence.

The latter should remain diagnostic unless separately operationalized.

## Methodological note

The common format scaffold itself perturbed some semantic outputs in non-worked conditions. For example, old baseline target-status accuracy was 10/12 whereas `format_only` is 8/12.

Therefore cross-run score differences should not be interpreted as pure estimates of a format effect. The cleanest evidence in RS-002B is the **within-run comparison among conditions**, since all conditions share the scaffold.

## Working interpretation

The experiment does not show that worked examples make the host generally more accurate.

It does suggest that they may induce a relatively stable **epistemic policy shape**: stronger on explicit authorization, causal-design, and authentication boundaries, but too conflict-sensitive when weak or unauthorized later information appears.

A candidate next hypothesis is:

> Evidence may be present without having standing to update the represented state.

Possible abstraction:

`standing(e, T) = f(relevance, authority, temporal relation, diagnosticity)`

where evidence should receive state-update weight only when its relation to the target proposition warrants it.

## Recommended next experiment

Do not patch the same 12 cases directly.

Design `RELATIONAL_SEARCH_003` on new held-out surfaces to test **evidential standing / write-access** with orthogonal paired manipulations of:

- source authority;
- temporal supersession;
- directness/diagnosticity;
- relevance to the target state.

Hold interface format constant across all conditions.

The question should be whether a standing-aware procedure improves transfer to new domains without merely shifting errors from overclaim to underclaim.
