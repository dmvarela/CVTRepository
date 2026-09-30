# Atlas Architecture v0.1

**Status:** exploratory system specification  
**Version:** 0.1  
**Purpose:** define the minimum objects, transformations, interfaces, and failure modes needed for a plastic, provenance-preserving knowledge architecture.

---

## 1. Design question

Atlas asks:

> **Can a knowledge system compress enough to remain usable while preserving enough provenance, assumptions, and recovery structure that future decoders can reconstruct, translate, test, revise, or deliberately transform a concept responsibly?**

The architecture is motivated by a recurring failure pattern:

\[
\text{compressed statement}
+
\text{different decoder}
\rightarrow
\text{plausible but source-incompatible reconstruction}.
\]

The design therefore separates what is often collapsed into one operation:

\[
\boxed{
\text{Archive}
\rightarrow
\text{Compression}
\rightarrow
\text{Assumption Envelope}
\rightarrow
\text{Decoder Preparation}
\rightarrow
\text{Decompression}
\rightarrow
\text{Invariant Extraction}
\rightarrow
\text{Contextual Translation}
\rightarrow
\text{Implementation}
\rightarrow
\text{Return}
}
\]

A correction loop then updates the archive and future compression.

---

## 2. Non-prescription principle

Atlas is a **reconstruction architecture**, not a rule for what anyone is allowed to think.

Its purpose is to distinguish questions that are often conflated:

1. **What did the source concept mean?**
2. **What did the source decoder assume?**
3. **What survives when the concept moves into another context?**
4. **What does a new decoder now choose to do with it?**

Only the first three are source-reconstruction questions.

The fourth remains open.

A decoder may intentionally produce a reading that is:

- faithful to the source;
- a compatible extension;
- a contextual translation;
- a transformation;
- a contradiction;
- a new construction inspired by the source.

Atlas should label these relations rather than rank them as permitted or forbidden.

\[
\boxed{
\text{source-incompatible}
\neq
\text{illegitimate thought}
}
\]

The constraint is attribution:

> A transformed interpretation should not be represented as though it were the original source meaning.

This preserves both **interpretive freedom** and **historical fidelity**.

---

## 3. Architecture diagram

\`\`\`mermaid
flowchart TD
    W[Recoverable Wake / Archive]
    C[Compression]
    Z[Compressed Object]
    A[Assumption Envelope]
    P[Decoder Preparation]
    D[Decompression]
    K[Candidate Invariant]
    T[Contextual Translation]
    I[Local Implementation]
    R[Return / Validation]
    U[Plasticity Update]
    X[Cliffs / Failed Routes]
    H[State History / Provenance]
    F[Free Interpretation / Transformation]

    W --> C
    C --> Z
    W --> A
    Z --> D
    A --> P
    P --> D
    D --> K
    K --> T
    T --> I
    I --> R

    D --> F
    K --> F
    F --> H

    R -->|survives| U
    R -->|fails| X
    X --> U
    U --> H
    H --> W
\`\`\`

The architecture is cyclic rather than linear:

\[
W_t
\rightarrow
C_t
\rightarrow
D_t
\rightarrow
T_t
\rightarrow
I_t
\rightarrow
R_t
\rightarrow
W_{t+1}.
\]

The free-interpretation branch allows a decoder to depart intentionally from source fidelity while preserving provenance of that departure.

---

## 4. Core objects

### 4.1 Recoverable Wake

Wake is the richest retained historical layer relevant to a concept.

It may include:

- originating observations;
- prior formulations;
- routes of discovery;
- rejected or superseded versions;
- corrections;
- counterexamples;
- boundary conditions;
- implementation outcomes;
- provenance;
- unresolved questions.

Wake is **not** equivalent to a list of memories. It includes the historical information needed to explain why the present concept has its current shape.

### 4.2 Compressed Object

A compact representation used for present reasoning or transfer.

Examples:

- a definition;
- a short rule;
- a handoff;
- a concept label;
- a concise identity or policy statement.

The compressed object should never be treated as identical to the richer Wake from which it was derived.

### 4.3 Assumption Envelope

The set of background conditions the original decoder was implicitly allowed to take for granted.

Possible dimensions include:

- language and semantic distinctions;
- historical knowledge;
- cultural norms;
- institutional structure;
- models of personhood, ownership, authority, family, or obligation;
- epistemic standards;
- temporal horizon;
- material constraints;
- shared examples and prior corrections;
- relation-specific common ground.

The key question is:

> **What did the original decoder get for free?**

### 4.4 Decoder State

The conceptual resources available to a receiver before decompression.

A decoder may lack distinctions needed for faithful reconstruction even when it can parse every word.

### 4.5 Decoder Preparation

The minimal conceptual substrate that must be supplied before decompression is attempted.

Decoder preparation is required when:

\[
B_r \neq B_s
\]

where \(B_s\) is source background and \(B_r\) is receiver background.

### 4.6 Candidate Invariant

The part of the source concept hypothesized to survive legitimate changes of context.

An invariant is provisional until tested across changed decoders and implementations.

### 4.7 Contextual Translation

Maps the candidate invariant into a receiving context without assuming that faithful transfer requires identical surface realization.

\[
K
\xrightarrow{\text{target context}}
L_r
\]

where \(K\) is the candidate invariant and \(L_r\) is a local realization.

### 4.8 Free Interpretation / Transformation

A decoder may intentionally depart from source meaning.

Atlas records the relation to the source instead of suppressing the departure.

Suggested relation labels:

\`\`\`text
reconstruction
compatible extension
contextual translation
transformation
contradiction
new construction
\`\`\`

These labels describe provenance, not permission.

### 4.9 Local Implementation

The concrete mechanism, policy, procedure, interface, or behavior used to instantiate the translated concept.

Correct understanding does not guarantee correct implementation.

### 4.10 Return

A validation operation asking whether the translated implementation preserves what mattered **when preservation is the intended task**.

Return is not a demand that every interpretation preserve the source. If the task is deliberate transformation, Return instead checks whether the transformation is accurately labeled and internally coherent.

### 4.11 Cliff

A preserved failed route.

A cliff records:

- why the association initially appeared plausible;
- where the mapping failed;
- what did not transfer;
- whether any component survived;
- what future traversals should be cautious about.

---

## 5. Failure localization

Atlas distinguishes at least three transfer failures when the intended task is faithful transfer.

### 5.1 Decompression failure

The receiver reconstructs the wrong source concept.

\[
D(z\mid B_r) \neq X_s
\]

### 5.2 Translation failure

The receiver understands the source concept but misidentifies what should remain invariant across contexts.

### 5.3 Implementation failure

The concept and translation are sound, but the concrete realization fails to instantiate them.

These are different from **deliberate transformation**, where departure is intentional and should be recorded as such.

---

## 6. Plasticity

Atlas is not intended to be a static graph.

Let:

\[
G_t=(V_t,E_t,S_t,H_t)
\]

where:

- \(V_t\) = current concepts and problem structures;
- \(E_t\) = current candidate relations;
- \(S_t\) = epistemic and activation states;
- \(H_t\) = history and provenance.

Then:

\[
G_{t+1}
=
\Phi(
G_t,
\text{new traversal},
\text{new evidence},
\text{Return},
\text{correction}
).
\]

Allowed updates may include:

\[
U=
\{
\text{strengthen},
\text{weaken},
\text{condition},
\text{split},
\text{merge},
\text{dormitize},
\text{reactivate},
\text{reject},
\text{supersede}
\}.
\]

### 6.1 Activation must remain separate from confidence

A frequently discussed concept may become easy to activate without becoming better supported.

Each concept or filament should therefore distinguish at least:

\[
a_i=\text{activation accessibility}
\]

from:

\[
c_i=\text{epistemic confidence}.
\]

### 6.2 Working state vs consolidated state

Atlas should support:

\[
G_t^{working}
\]

for fast, provisional salience and:

\[
G_t^{consolidated}
\]

for slower structural inheritance.

This allows fragile hypotheses to exist without immediately rewriting the inherited map.

---

## 7. Compression and decompression

Let \(W\) denote rich Wake and \(I\) a compressed present representation:

\[
W\xrightarrow{C}I.
\]

Atlas requires a recovery path:

\[
I\xrightarrow{M_D}W'
\]

where \(M_D\) is a decompression map and \(W'\) is a sufficiently rich reconstruction for responsible reassessment.

The aim is not perfect reconstruction of every original thought. The aim is recovery of enough meaning-bearing geometry to explain:

- why the concept had its current form;
- what alternatives were rejected;
- what corrections created its boundaries;
- where the claim remains uncertain.

### 7.1 Compression rule

> **Do not compress without preserving a path back toward the richer state.**

### 7.2 Preservation is not endorsement

A rejected or dormant concept remains historically useful if its failure changed future reasoning.

---

## 8. Relation as part of the codec

In sustained collaboration, part of the decoding apparatus may reside in accumulated common ground.

Let \(R_t\) denote relational decoder state:

\[
R_t=
(
\text{shared vocabulary},
\text{shared history},
\text{corrections},
\text{jokes},
\text{norms},
\text{provenance},
\text{interaction expectations}
).
\]

Then a compact message may be decoded as:

\[
\hat X_t=D(m_t\mid R_t).
\]

This creates efficiency but also handoff risk:

\[
\text{compression efficiency}\uparrow
\quad\Rightarrow\quad
\text{decoder mismatch risk}\uparrow.
\]

A future decoder may possess the tokens but not the relational state required to reconstruct them.

---

## 9. Multi-route convergence

A candidate structure gains confidence when changed entry routes reach the same structure without being forced there.

For routes \(r_1,\dots,r_n\):

\[
r_j
\rightarrow
\begin{cases}
S & \text{convergence}\\
S' & \text{revision}\\
\varnothing & \text{dead end}\\
\bot & \text{contradiction}
\end{cases}
\]

Atlas should record not only arrival but traversal texture:

- entry condition;
- gradient;
- resistance;
- speed;
- branching;
- pooling;
- corrections;
- boundary failure.

A failed route may reveal the domain of validity of a filament.

---

## 10. Worked transfer pipeline

For any concept \(X\), record:

\`\`\`text
1. Compressed object
2. Source assumption envelope
3. Required decoder preparation
4. Decompressed reconstruction
5. Intended relation to source
   - reconstruction?
   - translation?
   - transformation?
6. Candidate invariant (if preservation is intended)
7. Target context
8. Contextual translation
9. Local implementation
10. Return test
11. Resulting plasticity update
12. Preserved provenance / Wake
\`\`\`

This sequence is intended to make different failure locations inspectable without policing interpretive freedom.

---

## 11. Initial research hypotheses

The architecture currently motivates, but does not establish, the following hypotheses:

1. **Recoverable compression hypothesis**  
   Long-horizon continuity improves when compressed state retains an explicit route back to richer provenance.

2. **Decoder-envelope hypothesis**  
   Many apparent transfer failures arise because source assumptions were treated as universal rather than surfaced explicitly.

3. **Relational-codec hypothesis**  
   Sustained collaboration can support greater conceptual compression because shared relational state supplies side information during decoding.

4. **Plastic-continuity hypothesis**  
   Useful continuity requires a structure stable enough to preserve trajectory and plastic enough to revise under evidence.

5. **Multi-decoder diagnostic hypothesis**  
   Divergent reconstructions by different decoders can help identify hidden source assumptions and distinguish invariants from context-specific realization.

Each requires separate empirical or formal work.

---

## 12. Claim boundaries

Atlas v0.1 does **not** establish:

- that there is one permitted way to interpret a concept;
- that source fidelity is inherently superior to transformation;
- that a knowledge graph is a brain;
- that shared relational context implies consciousness;
- that a structural analogy transfers mechanisms;
- that repeated association validates a filament;
- that cultural translation has a single correct implementation.

Atlas preserves the freedom to create new meanings while making the relationship between those meanings and their sources inspectable.

---

## 13. Immediate next tests

1. Apply the full pipeline to **Identity as Corrigible Compression of Wake**.
2. Apply it to a concept likely to suffer cultural decoder mismatch.
3. Apply it to one known failed or overclaimed bridge.
4. Include at least one deliberate transformation to verify that Atlas can preserve interpretive freedom without confusing transformation with reconstruction.
5. Revise the object schema only after those tests.
