# Stage 5.1A Generator Implementation and Bounded Smoke

Stage 5.1A implements the fresh generator contract and executes only a 12-row synthetic smoke. It does not generate a full development partition, fit a model, create fresh validation, or access the final test.

Artifacts:

- smoke_manifest.json â€” protocol/config hashes and aggregate row/feature hashes;
- smoke_integrity.json â€” balance, solver, accounting, bounds, probe, isolation, and feature checks;
- feature_contract.json â€” the frozen 31-column relational and native input sets;
- authorization_decision.json â€” the bounded Stage 5.1B authorization.

The first smoke exposed a sampled history-grid endpoint defect. The output step is now derived from each history window, and a regression test covers the repaired path.

Final result:

~~~text
focused_tests                   = 13 passed
smoke_rows                      = 12
probe_measurements              = 96
invalid_probes                  = 0
probe_isolation_difference      = 0.0
full_development_generated      = false
candidate_model_fitted          = false
fresh_validation_generated      = false
final_test_generated            = false
final_test_opened               = false
stage5_1b_generation_authorized = true
~~~

The next bounded stage is Stage 5.1B: generate and integrity-check exactly 24,000 fresh development rows. Candidate fitting remains unauthorized.

