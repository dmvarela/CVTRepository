# CVT Regulated-Transport Validation — Stage 4.0 Counterexample Anatomy Protocol

**Date:** 2026-08-06  
**Status:** exploratory protocol; no new validation claim  
**Parent artifacts:** Stage 3.2 locked validation comparison and Stage 3.2.5 closure decision  
**Final-test status:** ungenerated, unopened, and not authorized

## 1. Purpose

Stage 3.2 produced a mixed negative result. The four measured CVT proxies contained real pre-outcome signal and modestly beat the transport-only baseline, but they failed the frozen thresholds for incremental predictive value, predictive compression, and high-confidence safety-screen utility. Stage 3.2.5 then confirmed that the prespecified capture-proxy sensitivity alternatives do not rescue that result.

Stage 4 begins from that constraint. It does not attempt to reinterpret Stage 3.2 as confirmation. Its purpose is to study the validation counterexamples that falsified the hard-intersection reading of the first geometry:

```text
B >= b*, Q >= q*, C >= c*, S >= s*
```

The object of study is now the mismatch between local gate adequacy and realized hosted transformation.

## 2. Non-confirmatory boundary

Stage 4 is exploratory and may use only data that has already been opened in the validation cycle:

- Stage 3.1 training and validation evidence;
- Stage 3.2 locked validation predictions and gate thresholds;
- Stage 3.2.5 closure and capture-proxy sensitivity refit.

Stage 4 must not:

- generate or read the untouched final-test partition;
- modify the locked Stage 3.2 winners;
- report a new validation victory from the already-opened validation set;
- tune a revised model and call it confirmatory;
- add universal CVT equations to the Foundations manuscript.

All Stage 4 conclusions must be labeled as exploratory architecture repair after a failed validation geometry.

## 3. Frozen gate thresholds for anatomy

The Stage 3.2 direct-constraint fit selected the following thresholds:

```text
B >= 0.673592323904192
Q >= 0.6756470618205909
C >= 0.26837276438988267
S >= 0.1460561929912628
```

These thresholds are used only to define counterexample classes. They are not treated as true viability laws.

## 4. Primary contrast classes

Each validation row should be classified into exactly one primary class:

| Class | Definition | Interpretation |
|---|---|---|
| `hosted_failed_gate` | `hosted == 1` and at least one gate below threshold | successful transformation despite apparent local inadequacy |
| `hosted_all_gates_pass` | `hosted == 1` and all four gates pass | clean success under the old geometry |
| `nonhosted_all_gates_pass` | `hosted == 0` and all four gates pass | failure despite apparent local adequacy |
| `nonhosted_failed_gate` | `hosted == 0` and at least one gate below threshold | clean failure under the old geometry |

The two contradiction classes are load-bearing:

```text
A: hosted_failed_gate
B: nonhosted_all_gates_pass
```

The two clean classes are controls for interpretation, not the primary discovery target.

## 5. Secondary labels

For each row, record:

- failed-gate pattern: any subset of `{B,Q,C,S}` below threshold;
- forcing family: `constant`, `pulse`, `ramp`, or `shock_tail`;
- Stage 3.2 locked CVT probability and native-gradient-boosting probability;
- whether CVT underpredicted a hosted case or overpredicted a nonhosted case;
- target failure, viability failure, and recorded failure reasons when available;
- margin profiles: productive headroom, buffer headroom, damage margin, integrity margin, reserve fraction, free-load margin;
- schedule features: peak source concentration, peak permeability, active duration, pulse count, scheduled peak intact flux, scheduled intact dose;
- measured gates: `g_b`, `g_q`, primary `g_c`, `g_s`;
- capture sensitivity measures: primary micro-probe, 2.5x micro-probe, and direct structural composite.

## 6. Primary questions

Stage 4.1 should answer these questions descriptively before proposing any new model:

1. Which failed gates are most often survivable?
2. Which combinations of failed gates are associated with success rather than failure?
3. Which all-gates-pass cases still fail, and what failure mechanism dominates them?
4. Are contradictions concentrated in specific forcing families or dose/timing regimes?
5. Do hosted failed-gate cases show compensating margins, such as high reserve, low damage, or unusually favorable routing?
6. Do nonhosted all-gates-pass cases reveal hidden overload, timing mismatch, damage accumulation, or insufficient follow-up recovery?
7. Does `C` behave like an independent condition, or like a revealed response produced by the relation among `B,Q,S`, input timing, and host history?
8. Do CVT and the native gradient booster fail on the same contradiction cases, or do their errors partition differently?

## 7. Required outputs for Stage 4.1

Stage 4.1 should produce:

1. `counterexample_anatomy.csv` — one row per validation case with primary class, failed-gate pattern, relevant margins, predictions, and failure labels.
2. `counterexample_summary.json` — exact counts and rates by class, forcing family, failed-gate pattern, and failure reason.
3. `stage4_1_counterexample_anatomy.md` — a narrative review artifact with tables and interpretation.
4. `relational_routing_hypotheses.json` — candidate hypotheses generated by the anatomy, explicitly marked as exploratory.

The output must keep validation rows de-identified by row ID and must not materialize the final test.

## 8. Descriptive analyses

The minimum analysis set is:

- class counts and prevalence;
- class by forcing-family cross-tabulation;
- failed-gate-pattern counts among hosted cases;
- all-gates-pass failures by failure reason;
- summary statistics of gates, margins, and schedule features by class;
- comparison of CVT and native predictions by class;
- error-direction summary: underprediction of hosted contradictions and overprediction of failed all-gates-pass cases;
- nearest-neighbor examples from each contradiction class, selected by distance in gate space and by extremal model error.

No p-value or confirmatory threshold is required. Bootstrap intervals may be reported for descriptive uncertainty, but they must not be used to claim validation.

## 9. Permitted exploratory models

Stage 4 may fit or summarize exploratory structures only to generate hypotheses for a future fresh development cycle. Permitted exploratory forms include:

- monotone interactions among `B,Q,C,S`;
- conditional rules such as `C` interacting with dose, reserve, or integrity margin;
- routing scores that distinguish productive uptake, safe rejection, buffering, harmful retained load, and damage recovery;
- contradiction classifiers trained only to describe the opened validation partition.

Any fitted exploratory model must be labeled unsuitable for final testing. A revised candidate requires a new development partition and a new preregistration before any confirmatory run.

## 10. Relational-routing revision target

The working revision is:

```text
Hosted transformation is not a hard intersection of four independent gates.
It is a relation among boundary, organization, capture response, reserve, input form,
and history that routes contact without sacrificing host viability.
```

In notation, Stage 4 should treat capture readiness as a possible response relation rather than a coequal stored gate:

```text
C = C(B, Q, S, input, current load, history)
```

This is a hypothesis generator, not a validated replacement law.

## 11. Exit criteria

Stage 4.0 is complete when this protocol is merged.

Stage 4.1 is complete when the counterexample anatomy artifacts exist and the final test remains sealed.

Stage 4.2 may then decide whether to:

- revise the Foundations manuscript to report the mixed negative result;
- open a fresh exploratory development cycle for relational routing;
- design a new preregistered Stage 5 candidate field;
- or stop the regulated-transport validation line as an instructive negative result.
