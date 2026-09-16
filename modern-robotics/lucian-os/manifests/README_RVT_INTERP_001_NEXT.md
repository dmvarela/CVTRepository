# RVT-INTERP-001 — next freeze step

Before any model execution, inspect the repository's current Ollama/Ministral runner pattern and then freeze:

1. one synthetic inference task;
2. three matched histories;
3. one identical terminal observation;
4. one structured response schema;
5. exact sampling parameters;
6. deterministic condition-order/randomization rule;
7. raw-output logging and hashing.

Do not run the experiment while the manifest status remains `preregistered-cases-draft`.
