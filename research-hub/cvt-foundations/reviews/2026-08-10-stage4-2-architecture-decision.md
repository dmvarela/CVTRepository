# CVT Foundations — Stage 4.2 Architecture Decision

**Date:** 2026-08-10  
**Status:** architecture decision after exploratory counterexample anatomy  
**Canonical manuscript changed here:** no  
**Final-test status:** ungenerated, unopened, and not authorized

## 1. Decision

The first regulated-transport validation cycle is closed as a disciplined mixed negative result.

The measured `B,Q,C,S` variables contain modest pre-outcome signal, but the literal four-independent-gate geometry is not supported in the bounded regulated-transport world. The hard intersection is neither necessary nor sufficient there: 92 of 121 hosted validation cases failed at least one fitted gate, while 114 nonhosted cases passed all four. Stage 4.1 further showed that capture-gate failure appears in 71 of the 92 hosted contradictions and that 90 of the 114 all-pass failures did not reach the transformation target.

Accordingly, Stage 4.2 makes four decisions:

1. **Revise the Foundations manuscript now.** It should report the bounded negative result and withdraw any unqualified suggestion that the four measured dimensions behaved as jointly necessary gates in the first simulation.
2. **Retain relational routing only as an exploratory revision target.** The evidence motivates it, but does not validate a replacement law.
3. **Authorize design of a fresh Stage 5 development cycle, conditionally.** Protocol writing and pre-outcome measurement design may proceed after the manuscript revision. Model execution is not yet authorized.
4. **Preserve the existing final test sealed.** It is not a development resource and may be generated or opened only after a revised candidate is frozen under a new preregistration and clears a fresh validation-stage authorization rule.

## 2. What survives

The regulated-transport result does not erase the entire CVT research program. Several distinctions remain useful and were not falsified by failure of the hard intersection:

- the receiving or hosting system must be declared independently of the desired result;
- delivered exchange and retained productive uptake must be accounted for separately;
- transformation success and host viability must be independently defined;
- pre-outcome measurements must not reuse the outcome they claim to predict;
- damage, reserve, history, current load, and recovery horizon must not be collapsed without evidence;
- simple CVT candidates must compete with capacity-matched and domain-native alternatives;
- counterexamples and delayed failure are part of the evidence rather than exceptions to be explained away.

These are methodological commitments. They remain defensible even if no universal four-variable law exists.

## 3. What is rejected or constrained

### 3.1 Literal hard-gate reading

The first operationalized claim that success requires all four measured gates to exceed fitted thresholds is rejected in the regulated-transport simulation. This is a domain-bounded conclusion, not a proof that no non-compensable constraint exists in any system.

The manuscript may retain the hard intersection as a historically important candidate model and a falsifiable strong form. It must no longer present it as the current leading geometry without immediately reporting its failure in the first bounded test.

### 3.2 Four coequal stored conditions

The evidence constrains the picture of `B,Q,C,S` as four symmetric possessions. In particular, `C` behaved poorly as an independent hard gate: a failed `C` was present in most successful contradictions, while the 2.5x micro-probe was almost indistinguishable from the primary probe and the direct structural composite remained worse after fair calibration.

This does not show that capture is irrelevant. It suggests that capture readiness may be better represented as a response of the host–input relation:

```text
C = C(B, Q, S, input, current_load, history)
```

That expression is a design target, not a validated equation.

### 3.3 Sufficiency of local adequacy

Passing all four gates was not sufficient. Most all-pass failures were target shortfalls rather than overload: 90 of 114 did not reach the transformation target, while 12 violated damage limits and 12 lost integrity. A viable architecture must therefore distinguish at least two failure directions:

- inadequate routing for productive transformation;
- destructive routing that sacrifices host viability.

Local gate adequacy alone did not distinguish them.

## 4. Relational-routing status

Relational routing is accepted as the next **hypothesis field**, not as CVT v2 already established.

The working question becomes:

> What pre-outcome configuration of host condition, input form, timing, load, and history predicts whether contact will be routed into productive uptake, safe rejection, buffering, damage, and recovery without loss of the declared host?

The important shift is from gate possession to configured response. A revised model may include interactions, conditional thresholds, vectors of margins, or domain-native routing quantities. It must not use realized post-outcome routing channels as predictors unless independently estimable before the evaluated outcome.

## 5. Manuscript decision

The Foundations manuscript should advance from v0.2 to a result-constrained revision. The revision should:

- report the first bounded simulation and its negative gate result;
- replace “four jointly necessary conditions” with a candidate decomposition whose relations remain under study;
- distinguish strict non-compensability from weaker conditional or configuration-level constraints;
- redefine capture readiness as potentially input-conditioned and probe-estimated;
- preserve the product, minimum, soft-minimum, and direct intersection as compared candidates, not preferred truths;
- add one compact result table and explicit limits on inference;
- state that relational routing remains exploratory and simulation-specific;
- leave the fusion illustration unchanged except for any terminology needed for consistency.

The companion manuscript-revision plan specifies the exact section-level edits. This Stage 4.2 PR does not alter `main.tex`; canonical prose should receive its own review branch and pull request.

## 6. Stage 5 authorization

Stage 5 is conditionally justified because the counterexamples generate precise, testable alternatives. Only **Stage 5.0 protocol design** is authorized after the canonical manuscript revision.

Before any revised model is executed, Stage 5.0 must freeze:

1. a fresh development partition independent of the opened Stage 3 validation rows;
2. pre-outcome routing estimators, including probe timing and dose where relevant;
3. candidate interaction structures and capacity-matched baselines;
4. separation of productive uptake, rejection, buffering, damage, and recovery targets;
5. calibration, selection, uncertainty, and stopping rules;
6. a new validation-stage threshold that must be cleared before final-test authorization;
7. the exact disposition of the existing sealed final-test generator.

Stage 5 must not fit a revised model directly to the opened Stage 3 validation partition and call the result validation.

## 7. Final-test disposition

```text
confirmatory_test_authorized = false
final_test_generated         = false
final_test_opened            = false
```

The final test remains scientifically valuable precisely because it has not been spent. It remains preserved, not promised. A future protocol may authorize it only if the revised architecture is frozen, developed without it, and clears a new validation criterion. Until then it remains inaccessible.

## 8. Ordered next actions

1. **Stage 4.3:** revise the canonical Foundations manuscript under the companion plan.
2. **Stage 5.0:** if the revised manuscript still supports continuation, preregister the relational-routing development cycle.
3. **Venue decision:** choose the target field and venue using the result-constrained manuscript, not the pre-result framing.
4. **Fusion archive:** keep detailed fusion mathematics excluded until a separate reproducible archive exists.

## 9. Closure statement

The gate version of CVT failed its first bounded geometry test. The broader methodological program survives in a narrower and more credible form: a research program about how boundary-mediated contact is routed through a host over time. The next cycle must earn that revision through fresh data and a new lock; it cannot inherit confirmation from the variables’ modest Stage 3 signal.

