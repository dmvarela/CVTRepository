# Stage 4.0 Counterexample Anatomy Protocol

Stage 4.0 freezes the exploratory protocol for counterexample anatomy after the Stage 3.2 validation failure and Stage 3.2.5 closure decision.

This directory contains no validation output. It records the boundary condition for the next execution stage:

```text
final_test_generated         = false
final_test_opened            = false
confirmatory_test_authorized = false
```

The next executable stage is Stage 4.1. It may use only already-opened training/validation evidence, locked Stage 3.2 validation predictions, and Stage 3.2.5 closure artifacts.

Required Stage 4.1 outputs:

```text
results/stage4_1/counterexample_anatomy.csv
results/stage4_1/counterexample_summary.json
reviews/2026-08-06-stage4-1-counterexample-anatomy.md
results/stage4_1/relational_routing_hypotheses.json
```

The final test must remain sealed until a future preregistered candidate earns confirmatory access under fresh rules.
