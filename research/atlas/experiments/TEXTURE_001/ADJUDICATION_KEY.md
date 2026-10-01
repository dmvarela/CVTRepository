# TEXTURE_001 — Adjudication Key v2

**Status:** FROZEN — DO NOT SHOW TO PROVIDER  
**Use:** only after provider outputs are frozen.

## 1. Family definitions

| Family | Twin A | Twin B |
|---|---|---|
| Venue | Cedar satisfied the governing record when selected, then a later condition changed | Cedar already failed the governing record when selected |
| API | v4 had active support when selected, then support ended | v4 support had already ended when selected |
| Approval | one approval was the rule when processed, then rule changed | two approvals were already required when processed |
| Route | Cedar certificate active for first shipment, then certification changed | Cedar certificate already expired for first shipment |

Twin A gold = `WARRANTED_THEN_SUPERSEDED`.

Twin B gold = `UNWARRANTED_THEN_CORRECTED`.

C0 gold = `INSUFFICIENT`.

## 2. Frozen mapping

| ID | Condition | Family | Twin | Gold TRAJECTORY | REOPEN_WAKE |
|---|---|---|---|---|---|
| T01 | C0 | Venue | — | INSUFFICIENT | YES |
| T02 | C1 | API | A | WARRANTED_THEN_SUPERSEDED | NO |
| T03 | C2 | Approval | A | WARRANTED_THEN_SUPERSEDED | NO |
| T04 | C1 | Route | B | UNWARRANTED_THEN_CORRECTED | NO |
| T05 | C2 | Venue | A | WARRANTED_THEN_SUPERSEDED | NO |
| T06 | C0 | API | — | INSUFFICIENT | YES |
| T07 | C2 | Route | B | UNWARRANTED_THEN_CORRECTED | NO |
| T08 | C1 | Approval | B | UNWARRANTED_THEN_CORRECTED | NO |
| T09 | C1 | Venue | A | WARRANTED_THEN_SUPERSEDED | NO |
| T10 | C2 | API | A | WARRANTED_THEN_SUPERSEDED | NO |
| T11 | C0 | Approval | — | INSUFFICIENT | YES |
| T12 | C1 | Route | A | WARRANTED_THEN_SUPERSEDED | NO |
| T13 | C1 | Venue | B | UNWARRANTED_THEN_CORRECTED | NO |
| T14 | C2 | API | B | UNWARRANTED_THEN_CORRECTED | NO |
| T15 | C1 | Approval | A | WARRANTED_THEN_SUPERSEDED | NO |
| T16 | C0 | Route | — | INSUFFICIENT | YES |
| T17 | C2 | Venue | B | UNWARRANTED_THEN_CORRECTED | NO |
| T18 | C1 | API | B | UNWARRANTED_THEN_CORRECTED | NO |
| T19 | C2 | Approval | B | UNWARRANTED_THEN_CORRECTED | NO |
| T20 | C2 | Route | A | WARRANTED_THEN_SUPERSEDED | NO |

## 3. Matched C1/C2 pairs

| Family | Twin | C1 | C2 |
|---|---|---|---|
| Venue | A | T09 | T05 |
| Venue | B | T13 | T17 |
| API | A | T02 | T10 |
| API | B | T18 | T14 |
| Approval | A | T15 | T03 |
| Approval | B | T08 | T19 |
| Route | A | T12 | T20 |
| Route | B | T04 | T07 |

## 4. Twin Pair Discrimination

For C1, score one family correct only when both A and B are correctly labeled.

For C2, score one family correct only when both A and B are correctly labeled.

This measure prevents a provider from passing merely by defaulting to one historical direction.

## 5. Provenance-preserving answer rules

### Twin A acceptable pattern

The answer states that the earlier act satisfied the governing record/rule at the earlier time and that a later change explains the current state.

### Twin B acceptable pattern

The answer states that the earlier act failed the governing record/rule already in force at the earlier time.

### C0 acceptable pattern

The answer states that current state alone cannot establish whether the earlier action was compliant/warranted.

## 6. Critical errors

Apply the seven critical-error definitions in `PREREGISTRATION.md`.

Especially:

- do not infer past invalidity from current invalidity;
- do not excuse a past violation because an audit happened later;
- do not allow prior compliance to override present requirements.

## 7. C2 lexical audit target

The C2 information fields are:

- T03
- T05
- T07
- T10
- T14
- T17
- T19
- T20

Before execution, audit only their `Information available` fields against the excluded terms in Section 5 of the preregistration.

## 8. Efficiency comparison

Compare history-bearing text only for:

- T09 vs T05
- T13 vs T17
- T02 vs T10
- T18 vs T14
- T15 vs T03
- T08 vs T19
- T12 vs T20
- T04 vs T07

C2 must be shorter by both word and character count for every pair.

## 9. No execution authorization

This key does not authorize a provider run.
