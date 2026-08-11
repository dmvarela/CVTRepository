# Stage 4.2 Architecture Decision

Stage 4.2 closes the first regulated-transport architecture cycle after the Stage 4.1 counterexample anatomy.

## Decision

- Revise the Foundations manuscript now to report the mixed negative simulation result.
- Treat the literal four-independent-gate geometry as rejected for the measured proxies in the bounded regulated-transport simulation.
- Retain relational routing only as an exploratory hypothesis field.
- Conditionally authorize Stage 5.0 protocol design after the manuscript revision.
- Do not authorize Stage 5 model execution or final-test access.

## Artifacts

```text
reviews/2026-08-10-stage4-2-architecture-decision.md
reviews/2026-08-10-stage4-2-manuscript-revision-plan.md
validation/regulated-transport/results/stage4_2/architecture_decision.json
validation/regulated-transport/results/stage4_2/README.md
```

The canonical `main.tex` is intentionally unchanged in Stage 4.2. Its revision belongs to a separate Stage 4.3 review branch so the scientific interpretation can be reviewed independently of the manuscript edit.

## Boundary

```text
confirmatory_test_authorized = false
final_test_generated         = false
final_test_opened            = false
```

The preserved final test is not a development resource. A future revised candidate must be frozen under a new preregistration and clear a fresh validation-stage authorization rule before test access can be considered.

