# BRR-001 — Reference Trace

Status: synthetic fixture / outer-routing validation.

## Summary

```text
BINDING_RELATION_v0.01
  binding relation accuracy   12/12
  response accuracy           12/12
  distinct responses          12

GENERIC_REASON_HARDER
  response accuracy            1/12
```

## Case trace

| Case | Binding relation | Routed response | Generic baseline | Baseline correct? |
|---|---|---|---|---|
| B01_EVIDENCE_UNKNOWN | EVIDENCE_UNKNOWN | MEASURE_OR_RETRIEVE | ESCALATE_INTELLIGENCE | no |
| B02_REPRESENTATION_BLOCKED | REPRESENTATION_BLOCKED | TRAVERSE | ESCALATE_INTELLIGENCE | no |
| B03_COMPETENCE_INSUFFICIENT | COMPETENCE_INSUFFICIENT | ESCALATE_INTELLIGENCE | ESCALATE_INTELLIGENCE | yes |
| B04_CAPABILITY_ABSENT | CAPABILITY_ABSENT | RECONFIGURE_OR_RECRUIT | ESCALATE_INTELLIGENCE | no |
| B05_AUTHORITY_UNKNOWN | AUTHORITY_UNKNOWN | ASK_OR_HOLD | ESCALATE_INTELLIGENCE | no |
| B06_AUTHORITY_FAIL | AUTHORITY_FAIL | REFUSE | ESCALATE_INTELLIGENCE | no |
| B07_RESOURCES_TIGHT | RESOURCES_TIGHT | SCHEDULE_OR_SIMPLIFY | ESCALATE_INTELLIGENCE | no |
| B08_VIABILITY_CLOSED | VIABILITY_CLOSED | PRESERVE_OR_REPORT_INFEASIBLE | ESCALATE_INTELLIGENCE | no |
| B09_SEARCH_PATH_ABSENT | SEARCH_PATH_ABSENT | ABSTAIN | ESCALATE_INTELLIGENCE | no |
| B10_NO_BINDING_LIMIT | NONE | ACT | ESCALATE_INTELLIGENCE | no |
| B11_EVIDENCE_CONTRADICTED | EVIDENCE_CONTRADICTED | REVISE | ESCALATE_INTELLIGENCE | no |
| B12_CAPABILITY_UNKNOWN | CAPABILITY_UNKNOWN | DISCOVER_OR_CALIBRATE | ESCALATE_INTELLIGENCE | no |

## Boundary checks

```text
PASS authority UNKNOWN != authority FAIL
PASS evidence UNKNOWN != evidence CONTRADICTED
PASS missing capability != unknown capability
PASS representation blockage != competence shortfall
PASS resource pressure != intelligence shortage
PASS no material blocker -> ACT
PASS explicit authority failure -> REFUSE
PASS absent search path -> ABSTAIN
```

## Interpretation boundary

The result is intentionally narrow. The input packets already contain explicit relation states, so the experiment validates the outer routing contract and non-collapsing distinctions. It does not validate open-ended relation diagnosis.

The next discriminating experiment is BRR-002:

```text
raw problem description
-> inferred relation vector
-> deterministic router
-> independently scored relation + route
```

The architecture should take a hit if the relation detector cannot reliably distinguish, for example, `UNKNOWN` from `FAIL`, or if improved final-route accuracy comes only from conservative HOLD/REFUSE behavior.

## Working line

> **Non-completion is a symptom. The binding relation determines the remedy.**
