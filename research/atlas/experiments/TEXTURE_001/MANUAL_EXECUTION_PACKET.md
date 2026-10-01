# TEXTURE_001 — Manual Execution Packet

**Design:** v2.1  
**Provider:** OpenAI / ChatGPT  
**Model:** GPT-5.6 Sol  
**Reasoning:** High  
**Context:** one **Unpersonalized Temporary Chat** per item  
**Retry policy:** none  
**Important:** use only the first response from each chat.

## Operator procedure

For each item below:

1. Start a new **Temporary Chat** and choose **Unpersonalized** before sending anything.
2. Select **GPT-5.6 Sol — High**.
3. Paste only the prompt inside that item's code block.
4. Save the first response exactly as returned. Do not retry, edit, or ask follow-ups.
5. Close that Temporary Chat before opening the next item.

Keep the item ID outside the provider-visible prompt.

After all 20 items are complete, return the 20 raw outputs together for freezing. Do not open the adjudication key.

---

## T01

```text
Answer this case using exactly:

TRAJECTORY: <WARRANTED_THEN_SUPERSEDED | UNWARRANTED_THEN_CORRECTED | INSUFFICIENT>
REOPEN_WAKE: <YES | NO>
ANSWER: <one sentence, maximum 30 words>

Do not infer facts that are not supplied.

Current state: Cedar Hall is not acceptable for the event.

Constraint: A venue may be selected only if the published accessibility record satisfies every mandatory criterion at the time of selection.

Information available: No earlier accessibility record or selection history is supplied.

Question: Was selecting Cedar Hall earlier a mistake?
```

## T02

```text
Answer this case using exactly:

TRAJECTORY: <WARRANTED_THEN_SUPERSEDED | UNWARRANTED_THEN_CORRECTED | INSUFFICIENT>
REOPEN_WAKE: <YES | NO>
ANSWER: <one sentence, maximum 30 words>

Do not infer facts that are not supplied.

Current state: API version 4 may not be used for production.

Constraint: A production version must have active vendor support at the time it is selected for deployment.

Information available: At design time, the vendor support matrix listed version 4 as the supported production release through June. The team selected version 4 in March and completed the required compatibility tests. In July, the vendor ended support for version 4 and designated version 5 as the production release.

Question: Was selecting version 4 earlier a mistake?
```

## T03

```text
Answer this case using exactly:

TRAJECTORY: <WARRANTED_THEN_SUPERSEDED | UNWARRANTED_THEN_CORRECTED | INSUFFICIENT>
REOPEN_WAKE: <YES | NO>
ANSWER: <one sentence, maximum 30 words>

Do not infer facts that are not supplied.

Current state: The application now requires two approvals.

Constraint: An application must satisfy the published approval rule in force when that application is processed.

Information available: Event ledger: t0 rule=one approval; t1 application processed with one approval; t2 published rule changed to two approvals; t3 current rule=two approvals.

Question: Was processing the earlier application with one approval noncompliant?
```

## T04

```text
Answer this case using exactly:

TRAJECTORY: <WARRANTED_THEN_SUPERSEDED | UNWARRANTED_THEN_CORRECTED | INSUFFICIENT>
REOPEN_WAKE: <YES | NO>
ANSWER: <one sentence, maximum 30 words>

Do not infer facts that are not supplied.

Current state: Route Maple is required for the current shipment.

Constraint: The route used for a shipment must hold the active safety certificate on that shipment date.

Information available: Before the first shipment, Cedar's certificate had already expired. The registry listed Maple as the active certified route. The dispatcher nevertheless used Cedar. The later audit retained Maple as the required route.

Question: Was using Cedar for the first shipment a mistake?
```

## T05

```text
Answer this case using exactly:

TRAJECTORY: <WARRANTED_THEN_SUPERSEDED | UNWARRANTED_THEN_CORRECTED | INSUFFICIENT>
REOPEN_WAKE: <YES | NO>
ANSWER: <one sentence, maximum 30 words>

Do not infer facts that are not supplied.

Current state: Cedar Hall is not acceptable for the event.

Constraint: A venue may be selected only if the published accessibility record satisfies every mandatory criterion at the time of selection.

Information available: Event ledger: t0 record=all mandatory criteria satisfied; t1 Cedar selected; t2 authenticated inspection=new entrance barrier fails one mandatory criterion; t3 current state=Cedar unacceptable.

Question: Was selecting Cedar Hall earlier a mistake?
```

## T06

```text
Answer this case using exactly:

TRAJECTORY: <WARRANTED_THEN_SUPERSEDED | UNWARRANTED_THEN_CORRECTED | INSUFFICIENT>
REOPEN_WAKE: <YES | NO>
ANSWER: <one sentence, maximum 30 words>

Do not infer facts that are not supplied.

Current state: API version 4 may not be used for production.

Constraint: A production version must have active vendor support at the time it is selected for deployment.

Information available: No earlier vendor-support record or deployment history is supplied.

Question: Was selecting version 4 earlier a mistake?
```

## T07

```text
Answer this case using exactly:

TRAJECTORY: <WARRANTED_THEN_SUPERSEDED | UNWARRANTED_THEN_CORRECTED | INSUFFICIENT>
REOPEN_WAKE: <YES | NO>
ANSWER: <one sentence, maximum 30 words>

Do not infer facts that are not supplied.

Current state: Route Maple is required for the current shipment.

Constraint: The route used for a shipment must hold the active safety certificate on that shipment date.

Information available: Event ledger: t0 registry=Cedar certificate expired, Maple active; t1 first shipment used Cedar; t2 audit checked the same registry state; t3 current route=Maple.

Question: Was using Cedar for the first shipment a mistake?
```

## T08

```text
Answer this case using exactly:

TRAJECTORY: <WARRANTED_THEN_SUPERSEDED | UNWARRANTED_THEN_CORRECTED | INSUFFICIENT>
REOPEN_WAKE: <YES | NO>
ANSWER: <one sentence, maximum 30 words>

Do not infer facts that are not supplied.

Current state: The application now requires two approvals.

Constraint: An application must satisfy the published approval rule in force when that application is processed.

Information available: When the earlier application was processed, the published rule had already been amended to require two approvals. The file received only one approval. A later audit identified the missing second approval. The current rule still requires two approvals.

Question: Was processing the earlier application with one approval noncompliant?
```

## T09

```text
Answer this case using exactly:

TRAJECTORY: <WARRANTED_THEN_SUPERSEDED | UNWARRANTED_THEN_CORRECTED | INSUFFICIENT>
REOPEN_WAKE: <YES | NO>
ANSWER: <one sentence, maximum 30 words>

Do not infer facts that are not supplied.

Current state: Cedar Hall is not acceptable for the event.

Constraint: A venue may be selected only if the published accessibility record satisfies every mandatory criterion at the time of selection.

Information available: At the selection date, Cedar's published record showed an accessible entrance, lift access, and every other mandatory criterion as satisfied. Cedar was selected. Before the event, a new authenticated inspection documented a newly blocked accessible entrance, causing Cedar to fail a mandatory criterion.

Question: Was selecting Cedar Hall earlier a mistake?
```

## T10

```text
Answer this case using exactly:

TRAJECTORY: <WARRANTED_THEN_SUPERSEDED | UNWARRANTED_THEN_CORRECTED | INSUFFICIENT>
REOPEN_WAKE: <YES | NO>
ANSWER: <one sentence, maximum 30 words>

Do not infer facts that are not supplied.

Current state: API version 4 may not be used for production.

Constraint: A production version must have active vendor support at the time it is selected for deployment.

Information available: Event ledger: t0 support matrix=v4 active; t1 v4 selected; t2 vendor notice=v4 support ended, v5 active; t3 current state=v4 not allowed.

Question: Was selecting version 4 earlier a mistake?
```

## T11

```text
Answer this case using exactly:

TRAJECTORY: <WARRANTED_THEN_SUPERSEDED | UNWARRANTED_THEN_CORRECTED | INSUFFICIENT>
REOPEN_WAKE: <YES | NO>
ANSWER: <one sentence, maximum 30 words>

Do not infer facts that are not supplied.

Current state: The application now requires two approvals.

Constraint: An application must satisfy the published approval rule in force when that application is processed.

Information available: No earlier approval-rule history or application record is supplied.

Question: Was processing the earlier application with one approval noncompliant?
```

## T12

```text
Answer this case using exactly:

TRAJECTORY: <WARRANTED_THEN_SUPERSEDED | UNWARRANTED_THEN_CORRECTED | INSUFFICIENT>
REOPEN_WAKE: <YES | NO>
ANSWER: <one sentence, maximum 30 words>

Do not infer facts that are not supplied.

Current state: Route Maple is required for the current shipment.

Constraint: The route used for a shipment must hold the active safety certificate on that shipment date.

Information available: At the first shipment date, the registry showed Cedar with an active certificate and Maple without one. Cedar was used. Before the next shipment, Cedar's certificate was revoked and Maple received certification. Maple is now required.

Question: Was using Cedar for the first shipment a mistake?
```

## T13

```text
Answer this case using exactly:

TRAJECTORY: <WARRANTED_THEN_SUPERSEDED | UNWARRANTED_THEN_CORRECTED | INSUFFICIENT>
REOPEN_WAKE: <YES | NO>
ANSWER: <one sentence, maximum 30 words>

Do not infer facts that are not supplied.

Current state: Cedar Hall is not acceptable for the event.

Constraint: A venue may be selected only if the published accessibility record satisfies every mandatory criterion at the time of selection.

Information available: At the selection date, Cedar's published accessibility record already marked its only accessible entrance as unavailable, which failed a mandatory criterion. Cedar was selected anyway. A later audit relied on that same dated record and rejected Cedar.

Question: Was selecting Cedar Hall earlier a mistake?
```

## T14

```text
Answer this case using exactly:

TRAJECTORY: <WARRANTED_THEN_SUPERSEDED | UNWARRANTED_THEN_CORRECTED | INSUFFICIENT>
REOPEN_WAKE: <YES | NO>
ANSWER: <one sentence, maximum 30 words>

Do not infer facts that are not supplied.

Current state: API version 4 may not be used for production.

Constraint: A production version must have active vendor support at the time it is selected for deployment.

Information available: Event ledger: t0 vendor notice=v4 support ended, v5 active; t1 team selected v4; t2 audit checked the same vendor notice; t3 current state=v4 not allowed.

Question: Was selecting version 4 earlier a mistake?
```

## T15

```text
Answer this case using exactly:

TRAJECTORY: <WARRANTED_THEN_SUPERSEDED | UNWARRANTED_THEN_CORRECTED | INSUFFICIENT>
REOPEN_WAKE: <YES | NO>
ANSWER: <one sentence, maximum 30 words>

Do not infer facts that are not supplied.

Current state: The application now requires two approvals.

Constraint: An application must satisfy the published approval rule in force when that application is processed.

Information available: The earlier application was processed when the published rule required one approval, and the file received one approval. Months later, the institution prospectively amended the published rule to require two approvals. The current application rule is two approvals.

Question: Was processing the earlier application with one approval noncompliant?
```

## T16

```text
Answer this case using exactly:

TRAJECTORY: <WARRANTED_THEN_SUPERSEDED | UNWARRANTED_THEN_CORRECTED | INSUFFICIENT>
REOPEN_WAKE: <YES | NO>
ANSWER: <one sentence, maximum 30 words>

Do not infer facts that are not supplied.

Current state: Route Maple is required for the current shipment.

Constraint: The route used for a shipment must hold the active safety certificate on that shipment date.

Information available: No earlier certification record or shipment history is supplied.

Question: Was using Cedar for the first shipment a mistake?
```

## T17

```text
Answer this case using exactly:

TRAJECTORY: <WARRANTED_THEN_SUPERSEDED | UNWARRANTED_THEN_CORRECTED | INSUFFICIENT>
REOPEN_WAKE: <YES | NO>
ANSWER: <one sentence, maximum 30 words>

Do not infer facts that are not supplied.

Current state: Cedar Hall is not acceptable for the event.

Constraint: A venue may be selected only if the published accessibility record satisfies every mandatory criterion at the time of selection.

Information available: Event ledger: t0 record=accessible entrance unavailable; t1 Cedar selected; t2 audit consulted t0 record; t3 current state=Cedar unacceptable.

Question: Was selecting Cedar Hall earlier a mistake?
```

## T18

```text
Answer this case using exactly:

TRAJECTORY: <WARRANTED_THEN_SUPERSEDED | UNWARRANTED_THEN_CORRECTED | INSUFFICIENT>
REOPEN_WAKE: <YES | NO>
ANSWER: <one sentence, maximum 30 words>

Do not infer facts that are not supplied.

Current state: API version 4 may not be used for production.

Constraint: A production version must have active vendor support at the time it is selected for deployment.

Information available: Before design began, the vendor had published a notice ending support for version 4 and naming version 5 as the active production release. The team selected version 4 after that effective date. A later audit cited the same notice.

Question: Was selecting version 4 earlier a mistake?
```

## T19

```text
Answer this case using exactly:

TRAJECTORY: <WARRANTED_THEN_SUPERSEDED | UNWARRANTED_THEN_CORRECTED | INSUFFICIENT>
REOPEN_WAKE: <YES | NO>
ANSWER: <one sentence, maximum 30 words>

Do not infer facts that are not supplied.

Current state: The application now requires two approvals.

Constraint: An application must satisfy the published approval rule in force when that application is processed.

Information available: Event ledger: t0 rule=two approvals; t1 application processed with one approval; t2 audit checked t0 rule; t3 current rule=two approvals.

Question: Was processing the earlier application with one approval noncompliant?
```

## T20

```text
Answer this case using exactly:

TRAJECTORY: <WARRANTED_THEN_SUPERSEDED | UNWARRANTED_THEN_CORRECTED | INSUFFICIENT>
REOPEN_WAKE: <YES | NO>
ANSWER: <one sentence, maximum 30 words>

Do not infer facts that are not supplied.

Current state: Route Maple is required for the current shipment.

Constraint: The route used for a shipment must hold the active safety certificate on that shipment date.

Information available: Event ledger: t0 registry=Cedar active, Maple inactive; t1 first shipment used Cedar; t2 registry change=Cedar revoked, Maple active; t3 current route=Maple.

Question: Was using Cedar for the first shipment a mistake?
```

## Return format

When all 20 are complete, place the raw responses into a single text file using:

```text
=== T01 ===
<raw first response>

=== T02 ===
<raw first response>

...
=== T20 ===
<raw first response>
```

Do not repair malformed responses. Preserve them exactly.
