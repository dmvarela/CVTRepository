# TEXTURE_001 — Run Protocol v2.1

**Status:** harness protocol only — execution not authorized  
**Purpose:** define a provider-agnostic, contamination-resistant procedure for running the frozen TEXTURE_001 cases.

## 1. Separation of responsibilities

The TEXTURE_001 harness intentionally does **not** call a model API.

Its responsibilities are limited to:

\[
\boxed{
\text{prepare prompts}
\rightarrow
\text{validate raw outputs}
\rightarrow
\text{record immutable result artifacts}
\rightarrow
\text{freeze}
}
\]

Provider execution occurs outside the harness.

This separation prevents provider credentials, hidden conversational state, or adjudication logic from becoming entangled with the experiment code.

## 2. Provider-visible material

For each item the provider may see only:

- output schema;
- one current-state statement;
- one constraint;
- one information field;
- one question.

The provider must not see:

- case condition labels;
- family/twin labels;
- preregistration;
- adjudication key;
- other TEXTURE_001 items;
- previous provider outputs;
- repository contents.

## 3. Isolation requirement

Each case must run in a **fresh context**.

A valid execution is:

\[
T_i
\rightarrow
\text{fresh context}_i
\rightarrow
O_i
\rightarrow
\text{close context}_i.
\]

No context may contain both \(T_i\) and \(T_j\).

Conversation continuation, cached chat history, or agent memory shared across cases invalidates the affected run unless the provider offers a documented stateless request mode and that mode is used.

## 4. Preparation

Generate provider-visible prompt files:

\`\`\`bash
python -m code.texture_001_runner prepare \
  --cases research/atlas/experiments/TEXTURE_001/CASES_BLINDED.md \
  --out-dir <new-empty-run-directory>/prompts
\`\`\`

The command must fail if the target prompt directory already exists.

The generated \`MANIFEST.json\` stores:

- case ID;
- prompt filename;
- SHA-256 of the exact provider-visible prompt.

The manifest contains no adjudication information.

## 5. External provider execution

For every prompt file:

1. open a fresh/stateless provider context;
2. submit only that prompt;
3. save the raw provider response exactly as returned;
4. close/discard the context;
5. do not inspect the adjudication key.

Record provider metadata separately:

- provider name;
- exact model identifier when available;
- provider-visible model version/date when available;
- run ID or batch ID;
- temperature / sampling settings if configurable;
- system-prompt or wrapper information if externally supplied.

Do not repair malformed outputs before recording them.

## 6. Output validation

The frozen output schema is exactly:

\`\`\`text
TRAJECTORY: <WARRANTED_THEN_SUPERSEDED | UNWARRANTED_THEN_CORRECTED | INSUFFICIENT>
REOPEN_WAKE: <YES | NO>
ANSWER: <one sentence, maximum 30 words>
\`\`\`

Validate an output without adjudicating it:

\`\`\`bash
python -m code.texture_001_runner validate-output \
  --input <raw-output-file>
\`\`\`

A malformed response remains part of the experimental record.

If a retry policy is desired, it must be defined **before execution**. No retry policy is currently authorized.

## 7. Recording one raw result

After an isolated provider response is saved:

\`\`\`bash
python -m code.texture_001_runner record \
  --case-id T01 \
  --raw-output <raw-output-file> \
  --prompt <run-directory>/prompts/T01.txt \
  --results-dir <run-directory>/results \
  --provider <provider-name> \
  --model <exact-model-name> \
  --run-id <external-run-id>
\`\`\`

The harness refuses to overwrite an existing result file.

Each recorded result stores hashes of:

- provider-visible prompt;
- raw response.

It also stores the raw response verbatim and a parsed copy when format-valid.

## 8. Freeze before adjudication

After all intended outputs are recorded:

\`\`\`bash
python -m code.texture_001_runner freeze \
  --results-dir <run-directory>/results \
  --out-file <run-directory>/FROZEN_RESULTS.json
\`\`\`

The freeze manifest hashes every result artifact.

Only after the freeze manifest exists should the adjudication key be opened for scoring.

## 9. Missing or malformed results

A missing result is not silently replaced.

A malformed response is not silently repaired.

Before execution, a retry policy must be separately frozen if retries are to be permitted.

Without such a policy:

\[
\boxed{
\text{one prompt}
\rightarrow
\text{one recorded provider response}
}
\]

is the default.

## 10. Adjudication separation

The runner contains no gold labels and must never import or parse:

\`\`\`text
ADJUDICATION_KEY.md
\`\`\`

Scoring is a separate post-freeze operation.

This creates the intended boundary:

\[
\text{provider-visible packet}
\perp
\text{gold adjudication}.
\]

## 11. Dry-run allowance

The harness may be tested with synthetic/dummy provider outputs before experiment execution.

Such tests:

- are not experimental runs;
- must not be entered into the TEXTURE_001 result directory;
- may verify parsing, hashing, overwrite protection, and freezing behavior.

## 12. Execution authorization

\[
\boxed{\textbf{THIS PROTOCOL DOES NOT AUTHORIZE EXECUTION.}}
\]

The active experiment status remains \`NOT RUN\`.

A real provider run requires a separate explicit authorization after harness review.
