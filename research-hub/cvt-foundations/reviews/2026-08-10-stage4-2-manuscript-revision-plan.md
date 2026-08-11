# CVT Foundations — Stage 4.2 Manuscript Revision Plan

**Date:** 2026-08-10  
**Target:** `research-hub/cvt-foundations/main.tex`  
**Purpose:** integrate the first bounded regulated-transport result without overstating relational routing  
**Execution:** separate Stage 4.3 review branch and pull request

## 1. Revision principle

The manuscript should become result-constrained rather than merely result-ready.

The present v0.2 text already avoids claiming universal validation, separates observations from gates and outcomes, and treats aggregation rules as competitors. Those safeguards should remain. The revision is concentrated where the paper still describes the four dimensions as candidate jointly necessary conditions or treats capture readiness as a coequal stored state without acknowledging the first bounded result.

No new universal dynamics should be added. Relational routing should be introduced as the next testable architecture, with explicit rival explanations and evidentiary burdens.

## 2. Required factual result block

Use one consistent result statement throughout the manuscript:

> In the first bounded regulated-transport simulation, the measured `B,Q,C,S` variables contained modest pre-outcome signal but did not meet the preregistered thresholds for incremental predictive value, predictive compression, or high-confidence safety-screen utility. The literal hard-intersection geometry was neither necessary nor sufficient in the opened validation partition: 92 of 121 hosted cases failed at least one fitted gate, while 114 nonhosted cases passed all four. These simulation-specific results motivate an exploratory relational-routing revision; they do not validate a replacement law.

Supporting details may be added in the dedicated result subsection:

- locked CVT model: `CVT-2-minimum`, Brier `0.027566`;
- transport-only Brier `0.028988`, improvement `0.001421`, below the required `0.005` threshold;
- native gradient-boosting Brier `0.019194`, CVT disadvantage `0.008372`;
- hosted failed-gate `92`, hosted all-pass `29`;
- nonhosted all-pass `114`, nonhosted failed-gate `3,765`;
- capture failure involved in `71/92` hosted contradictions;
- all-pass failure reasons: target not reached `90`, damage `12`, integrity `12`.

## 3. Section-level changes

### Abstract

Current risk: the abstract’s “candidate non-compensatory structure” remains defensible, but it does not report that the first bounded test has now constrained that structure.

Revision:

- retain the inherited-literature and methodological framing;
- add one sentence reporting modest signal and failure of the hard-intersection geometry;
- state that relational routing is an exploratory consequence, not a confirmed replacement;
- keep the universal-necessity disclaimer.

### Introduction

Current anchor: “CVT proposes that hosted transformation may depend on four jointly necessary conditions.”

Replace the leading claim with:

> CVT begins from four candidate dimensions of hosted transformation—bounded coupling, preserved organization, capture response, and restorative reserve—but the first bounded simulation does not support treating their measured proxies as four jointly necessary independent gates.

Add the factual result block after the candidate dimensions are introduced. Retain the independent definitions of host, transformation, and viability.

### Intellectual Lineage and Status of the Synthesis

Current risk: the scoped claim still says failure may be better explained when the four conditions are “jointly required and potentially non-compensatory.”

Revision:

- present that sentence as the first-generation strong hypothesis;
- immediately report that the regulated-transport test constrained it;
- redefine the surviving synthesis as a question about relations among boundary regulation, organization, capture response, reserve, input, and history;
- do not claim a new extension of viability theory.

### Candidate CVT Structure and Non-Compensability

Preserve the hard intersection and product representation as falsifiable candidate models. Add an explicit status paragraph:

> The regulated-transport validation did not support the literal threshold intersection for the measured proxies. The equations in this section therefore document the first candidate geometry and its non-compensability burden; they are not the empirically preferred architecture after Stage 4.1.

Distinguish three concepts:

1. strict variable-level non-compensability;
2. conditional non-compensability within a forcing or history regime;
3. configuration-level viability constraints on routing.

Only the first was directly rejected for the fitted gates in the bounded simulation. The latter two remain hypotheses.

### Capture Readiness and Realized Uptake

Current anchor: “Capture readiness `C` is a pre-existing state condition.”

Replace the scalar-only statement with a dual possibility:

> Capture readiness must be measured before or independently of the evaluated uptake outcome, but it need not be a context-free stored scalar. It may be a probe-estimated response relation conditional on the receiving state, specified input, current load, and history.

Introduce exploratory notation such as

```text
C_t(u; B,Q,S,L,H)
```

where `u` describes the specified input and timing, `L` current load, and `H` declared history. State explicitly that this is notation for a candidate measurement relation, not a universal law.

### Formal Architecture

Retain the observable–gate–candidate–outcome separation. Add a relational candidate layer between gates and outcome:

```text
observables -> context-conditioned response estimates -> candidate routing model -> independent outcome
```

Requirements:

- post-outcome productive uptake, rejection, damage, and recovery remain outcomes or anatomy labels unless independently predicted before evaluation;
- interactions must be prespecified and capacity-counted;
- domain-native baselines receive the same context variables where scientifically appropriate;
- no scalar routing score defines success by construction.

### Membrane Illustration

Rename “Minimal Membrane Test” or follow it with a new subsection, “First Bounded Regulated-Transport Result.”

Add:

- the fixed simulation scope and independent hosted outcome;
- a compact four-class anatomy table;
- the locked CVT, transport-only, and native Brier values;
- the three failed preregistered claims;
- the failure of the hard intersection;
- the final-test non-authorization;
- the simulation-specific limitations.

Avoid reproducing the full Stage 4.1 JSON tables in the manuscript. Point readers to the source-controlled validation package for complete evidence.

### Fusion Illustration

No substantive fusion model should be restored. Apply only terminology changes needed to avoid treating `C` as necessarily context-free or the four dimensions as demonstrated gates.

### Discussion, Falsification, and Validation Program

Change the first bounded validation subsection from future tense to completed status. Separate:

- what the simulation demonstrated;
- what it failed to demonstrate;
- what remains exploratory;
- what would be required for Stage 5;
- why no empirical-domain claim follows from a simulated native world.

Retain the threats of circular measurement, flexible thresholds, hidden state, common-cause forcing, delayed failure, and model-capacity imbalance. Add adaptive reuse of the opened validation partition as a new explicit threat.

### Conclusion

The conclusion should no longer end with only the pre-result research question. It should state:

- the first hard-gate geometry failed in the bounded simulation;
- the measurement and accounting separations remain useful;
- relational routing is the next hypothesis, not a result;
- future standing requires fresh preregistration and data.

## 4. Proposed compact tables

### Table A: Locked model comparison

| Model | Inputs | Brier | Stage 3 interpretation |
|---|---:|---:|---|
| CVT-2-minimum | 4 | 0.027566 | locked CVT winner; practical threshold not met |
| BL-2-transport-only | schedule + initial free load | 0.028988 | modestly worse; required improvement not met |
| BL-6-native gradient boosting | 44 | 0.019194 | substantially better; compression not demonstrated |

### Table B: Hard-gate anatomy

| | All gates pass | At least one gate fails |
|---|---:|---:|
| Hosted | 29 | 92 |
| Nonhosted | 114 | 3,765 |

Caption language must say that thresholds were fitted under the Stage 3 direct-constraint candidate and are used descriptively after validation failure.

## 5. Claims ledger changes

Update the claim ledger in Stage 4.3:

- “four jointly necessary conditions” → **empirically constrained strong hypothesis**;
- “capture readiness as independent stored condition” → **measurement architecture under revision**;
- “relational routing” → **exploratory programmatic hypothesis**;
- “methodological separation of delivered input, uptake, viability, damage, reserve, and history” → **retained conceptual/methodological contribution**;
- “regulated-transport support for CVT” → **mixed negative simulation result**.

## 6. Citation and provenance plan

No new external source is needed merely to report the repository’s simulation result. The revised manuscript should identify the source-controlled validation package and version or commit. External citations remain necessary for inherited constructs and any new statistical or mechanistic claims.

The manuscript must not cite a mutable branch. Stage 4.3 should cite or record the Stage 4.1 merge commit:

```text
bfa12e38e4ddef89d2d76ed2b04577e56bcbafc1
```

## 7. Stage 4.3 acceptance checks

- all universal-looking necessity or sufficiency language is scoped or replaced;
- exact Stage 3 and Stage 4 counts agree with locked artifacts;
- the final test remains described as ungenerated, unopened, and unauthorized;
- relational routing is never called validated;
- post-outcome anatomy variables are not promoted to predictors;
- the fusion section gains no unsupported equations or numerical claims;
- LaTeX builds cleanly;
- the claim ledger and manuscript use the same status labels;
- the PR contains only manuscript, ledger, and directly related review/build artifacts.

## 8. Out of scope for Stage 4.3

- fitting a relational-routing model;
- generating a fresh development partition;
- generating or opening the preserved final test;
- selecting a Stage 5 winner;
- restoring detailed fusion mathematics;
- claiming empirical validation beyond the simulated regulated-transport world.

