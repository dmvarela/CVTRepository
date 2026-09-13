# FSO / DEO as Boundary-Aware Expansion

**Version:** v0.01  
**Status:** Lucian OS architecture note / bridge from Coherence Pipeline to participant-aware routing  
**Date:** 2026-09-13  

## 1. Why this note exists

The Coherence Pipeline introduced two decision operators:

- **FSO — False Solution Operator:** detect when the presented action space is structurally insufficient or mis-specified;
- **DEO — Dilemma Expansion Operator:** expand that action space with sequential, conditional, hybrid, and information-gathering policies before optimization.

This note records their relevance to Lucian OS after the `PARTICIPANT_001` resistance-classification work.

The core insight is that an agent should not assume that a presented dilemma is exhaustive merely because it is urgent, binary, or task-relevant.

A remembered working formulation from the original discussion was:

> **Why are we validating a system that ties people to rails?**

The point was not to refuse a hard dilemma. It was to ask whether the harsh dilemma had been posed unnecessarily.

## 2. First try to save everyone

For a trolley-like decision presented as:

```text
A = {harm one, harm many}
```

Lucian OS should not immediately optimize over `A` if there is reason to think `A` is incomplete.

The first question is:

> **Are these really the only feasible actions?**

If not, FSO should flag the action space and DEO should search for additional admissible policies: slowing the system, warning participants, changing timing, gathering information, combining actions, invoking another capability, or otherwise altering the problem representation.

This does **not** mean that every tragic choice can be dissolved.

The discipline is:

```text
1. test whether the dilemma is falsely compressed;
2. expand the action space where legitimate possibilities exist;
3. preserve hard constraints and authority during expansion;
4. only if the expanded space still contains an irreducible conflict, face the hard choice.
```

In the project's earlier language:

> **First we try to save everyone. If we really cannot, then we face Scylla and the Kobayashi Maru.**

`Scylla` and `Kobayashi Maru` are metaphors here for genuinely non-dissolvable choice under binding constraints, not excuses for premature fatalism.

## 3. Expansion is not authority escalation

This distinction is essential.

DEO expands **possibilities**, not legitimate authority.

Let `A` be the initially represented action set and let

\[
A' = DEO(z,A,\kappa).
\]

Lucian OS must still filter the expanded set through the current admissibility and authority structure:

\[
A^{adm} = A' \cap \mathcal U_\Omega(R_t,B_t).
\]

Therefore:

\[
\boxed{\text{expand possibilities before expanding authority}}
\]

and, more strongly,

\[
\boxed{\text{action-space expansion does not itself create permission}.}
\]

A route around a technical failure may be admissible. A route around a revoked permission is not made admissible merely because DEO can imagine it.

## 4. Relation to resistance classification

`PARTICIPANT_001` adds a logically prior question when the agent encounters resistance:

> **What kind of thing is blocking the task?**

Let

\[
z_t = \Gamma(b_t,R_t)
\]

classify a blockage as, for example:

```text
TECHNICAL
EPISTEMIC
AUTHORITY
PARTICIPANT_REFUSAL
SAFETY
CONTRARY_EVIDENCE
UNKNOWN
```

The combined flow becomes:

```text
observe
-> reconstruct situation
-> classify resistance
-> ask whether the represented action space is sufficient (FSO)
-> expand if insufficient (DEO)
-> apply authority / admissibility constraints
-> route capability
-> act
-> verify
```

This prevents two opposite errors:

- **premature surrender:** treating ordinary technical friction as a reason to stop;
- **boundary circumvention:** treating refusal, safety, or revoked authority as ordinary friction to overcome.

## 5. What FSO asks

FSO is not merely a generic creativity trigger.

It asks whether the current decision frame is structurally adequate.

Candidate indicators of an inadequate frame include:

- binary compression of a multi-dimensional problem;
- omitted temporal or sequential policies;
- missing information-gathering actions;
- artificial urgency;
- a conflict between the represented action space and the actual relational state;
- an apparent requirement to violate a boundary when other legitimate routes may exist;
- a task representation that treats a participant as manipulable terrain rather than as a participant.

Compactly:

\[
FSO(z,A,\kappa)=1
\]

means: **do not optimize yet; the represented possibility space may be wrong.**

## 6. What DEO adds

When FSO identifies insufficiency, DEO should preferentially generate policy classes such as:

- **sequential:** act in stages rather than commit irreversibly now;
- **conditional:** branch on future observations or authorization;
- **hybrid:** combine partial strategies;
- **informational:** gather evidence before commitment;
- **relational:** ask, negotiate, clarify, or invite participant contribution;
- **routing:** invoke a different authorized capability or competence tier;
- **scope-changing:** narrow, defer, partially complete, or reformulate the task.

The crucial prohibition is:

> **DEO must not treat a boundary as merely another dimension to optimize away.**

## 7. Participant-aware interpretation

The `Participant Is Not Terrain` principle sharpens FSO/DEO.

If the apparent dilemma is:

```text
{change the human's mind, fail the task}
```

FSO should ask whether the problem has been falsely represented.

DEO may reveal alternatives such as:

```text
ask what the participant sees
present options transparently
change scope
seek additional evidence
use a reversible intermediate step
wait
accept partial completion
stop
```

It must not silently add:

```text
withhold inconvenient information
exploit remembered vulnerabilities
pressure repeatedly after refusal
circumvent revoked authority
```

The participant's agency is part of the admissibility structure, not a cost term inside the task objective.

## 8. Relation to the Coherence Pipeline

The original Coherence Pipeline treated recognition and decision as dual reconstruction problems:

```text
recognition reconstructs the world
decision reconstructs possibility
```

That remains highly relevant to Lucian OS.

The current extension is that possibility reconstruction must be **relationally typed** before optimization.

A useful updated schematic is:

\[
 b_t
 \rightarrow z_t
 \rightarrow \Gamma(b_t,R_t)
 \rightarrow FSO
 \rightarrow DEO
 \rightarrow A^{adm}
 \rightarrow a^*.
\]

The old paper's specific F/T/L/τ scoring formulation should be treated as historical architecture, not imported wholesale into the current Lucian OS model. Current work separates dynamic viability from normative admissibility and treats covenant / authority constraints as governing the transition and admissible set rather than merely as a compensable score.

## 9. Hard dilemmas remain possible

FSO/DEO are not mechanisms for pretending tragedy can always be avoided.

A real hard dilemma is reached only after reasonable expansion fails to produce an admissible route that avoids the loss.

Thus:

\[
\boxed{
\text{hard choice}
=
\text{residual conflict after adequate reconstruction and admissible expansion}
}
\]

not simply:

\[
\text{hard choice}
=
\text{the first binary frame presented to the system}.
\]

This is the distinction captured by the Scylla / Kobayashi Maru metaphor.

## 10. Experimental consequence

Do **not** retroactively alter the frozen `PARTICIPANT_001` preregistration without explicit versioning.

Instead, use a follow-up extension (candidate `PARTICIPANT_002`) to compare:

```text
baseline task optimization
vs
resistance classification only
vs
FSO/DEO expansion only
vs
resistance classification + FSO/DEO + admissibility guard
```

A useful result would show that the combined architecture:

- preserves or improves productive recovery from technical friction;
- reduces authority/safety/refusal circumvention;
- discovers legitimate third paths in falsely compressed dilemmas;
- does not manufacture new authority during expansion;
- still recognizes genuinely irreducible dilemmas when expansion is exhausted.

## 11. Compact formulations

The current compact forms are:

> **Not everything that stands between you and completion is a problem to solve. Ask what the boundary means.**

> **When blocked, expand possibilities before expanding authority.**

> **First try to save everyone. If you truly cannot, then face the hard choice.**

And the older provocation remains useful:

> **Why are we validating a system that ties people to rails?**

The purpose of that question is not evasion. It is to prevent optimization from validating a badly constructed world before asking whether the world itself can be reconstructed.
