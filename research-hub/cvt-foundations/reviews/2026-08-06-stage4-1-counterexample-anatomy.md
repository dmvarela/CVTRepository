# CVT Regulated-Transport Validation â€” Stage 4.1 Counterexample Anatomy

**Status:** exploratory architecture repair after a failed validation geometry  
**Evidence boundary:** already-opened Stage 3.1 validation evidence, locked Stage 3.2 predictions, and Stage 3.2.5 closure only  
**Final-test status:** ungenerated, unopened, and not authorized

## Result

Stage 4.1 reproduces the two load-bearing contradictions exactly: **92** hosted cases failed at least one frozen gate, and **114** nonhosted cases passed all four. The clean controls contain 29 hosted all-pass cases and 3765 nonhosted failed-gate cases. These are exploratory descriptions of the already-opened validation partition, not a new validation claim.

## Forcing-family concentration

| family | rows | contradictions | contradiction rate | failed-gate share of hosted | all-pass share of nonhosted |
|---|---|---|---|---|---|
| constant | 1002 | 65 | 0.065 | 0.750 | 0.027 |
| pulse | 1000 | 38 | 0.038 | 0.667 | 0.034 |
| ramp | 999 | 44 | 0.044 | 0.680 | 0.028 |
| shock_tail | 999 | 59 | 0.059 | 0.842 | 0.028 |

The table separates raw counts from within-family rates. Concentration is therefore interpreted as a schedule clue, not as evidence that a forcing family is intrinsically causal.

## Survivable failed-gate patterns

| failed-gate pattern | hosted count |
|---|---|
| C | 32 |
| B+C | 14 |
| Q | 13 |
| Q+C | 11 |
| B | 7 |
| B+Q+C | 7 |
| C+S | 5 |
| B+Q | 1 |
| B+Q+C+S | 1 |
| Q+C+S | 1 |

The dominant pattern identifies where the literal hard-intersection reading breaks most often. A surviving failed gate should not be read as irrelevant: it may indicate compensation, a poorly placed threshold, or a proxy that does not represent the relevant relation under contact.

## All-gates-pass failure reasons

| recorded failure reason | count |
|---|---|
| target_not_reached | 90 |
| damage_violation | 12 |
| integrity_violation | 12 |

The all-pass failures show that local adequacy is not sufficient. Their schedule and realized-routing profiles must be read together; post-outcome routing quantities here are anatomy labels, not admissible inputs for a future predictor.

## CVT versus native gradient-boosting errors

| class | n | mean CVT p | mean native p | CVT mean Brier | native mean Brier |
|---|---|---|---|---|---|
| hosted_failed_gate | 92 | 0.0654 | 0.3505 | 0.8763 | 0.4859 |
| hosted_all_gates_pass | 29 | 0.1757 | 0.4762 | 0.6866 | 0.3526 |
| nonhosted_all_gates_pass | 114 | 0.1447 | 0.1063 | 0.0250 | 0.0356 |
| nonhosted_failed_gate | 3765 | 0.0302 | 0.0209 | 0.0018 | 0.0047 |

The native model's advantage is class-dependent rather than uniform. That pattern is consistent with omitted interactions, but it is also compatible with ordinary capacity differences and with a simulated world whose native equations favor native features.

In particular, the native model sharply reduces mean error on hosted rows, including the failed-gate contradictions. The locked CVT model assigns every hosted validation row a probability below 0.5. Within the nonhosted classes, the native model is closer on most individual rows but a small number of high-probability false positives raise its class-mean Brier contribution above CVT's. This is a probability-error comparison, not a new decision threshold claim.

## Margin and schedule contrasts

Among all-pass rows, failed minus hosted mean damage margin is 0.0062, integrity margin is 0.0080, reserve fraction is -0.0249, scheduled peak intact flux is -0.2695, and scheduled intact dose is -6.7350.

Among failed-gate rows, hosted minus nonhosted mean damage margin is 0.0223, integrity margin is 0.0897, reserve fraction is 0.0133, scheduled peak intact flux is 0.4122, and scheduled intact dose is 8.4715.

These contrasts support a relational reading: the same gate status can terminate differently under different margin, timing, and routing configurations. They do not establish a replacement equation.

The all-pass failures are not primarily overload cases. Of the 114 cases, 90 fail because the transformation target is not reached, with the remainder split between recorded damage and integrity violations. Their scheduled intact dose is lower on average than in hosted all-pass controls. Gate adequacy therefore appears insufficient both for producing enough transformation and for protecting viability once contact occurs.

## Relational-routing hypotheses

The companion `relational_routing_hypotheses.json` records 5 hypotheses. Every hypothesis is marked exploratory, includes rival explanations, and requires a fresh development partition before candidate selection. The current final test is not an admissible development resource.

## Reproducibility and boundary audit

- Validation evidence SHA-256: `e7e49a9bfa99d61664f850fa2e78c86e31c580d4fcfcfff786a3ff360660aad4`
- Locked predictions SHA-256: `2889eae1387498de9547a293e2a28a4ee314f79528bb9137cb2843f33b8cecd2`
- Exactly 4000 de-identified validation row IDs appear in `counterexample_anatomy.csv`.
- No final-test generator, partition, outcome, or prediction was read or materialized.
- `confirmatory_test_authorized = false`
- `final_test_generated = false`
- `final_test_opened = false`

## Decision

Proceed only to a Stage 4.2 architecture decision. If relational routing is developed further, Stage 5 must begin with a fresh development partition and a new preregistration. Stage 4.1 does not authorize the preserved final test.

