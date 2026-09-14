# Task-Bounded Role Routing

## Bridge from Paper A to Lucian OS

**Status:** Captured architectural bridge; candidate design translation  
**Date:** 2026-09-14  
**Implementation status:** Documentation only. No new implementation rung is authorized before the frozen PR #70 preflight and Lucian OS stack integration decision.  
**Historical boundary:** This note does not alter Paper A or convert an analytical mapping into a historical claim.

## 1. Source object

Paper A is:

> *Task-Bounded Authority and the Horizon of Cooperation: A Finite-Task Theorem and a Validity Protocol from the 1840 Métis Buffalo Hunt*

The submission-ready manuscript uses Alexander Ross's 1856 account of the large summer expedition that left the Red River Settlement on June 15, 1840 and organized at Pembina. Ross records a council, ten captains, ten rotating guides, flag-governed movement and encampment, patrol and guard obligations, collective timing rules, and graduated sanctions.

The paper distinguishes three evidentiary levels:

1. what Ross recorded for the 1840 expedition;
2. what later Métis scholarship establishes about mobile social and political formations; and
3. the analytical interpretation proposed by the paper.

That separation governs this bridge note too.

## 2. What Paper A supports

Paper A defines **relationally constituted, task-bounded authority** through four candidate properties:

1. **Constitution for a common undertaking.** Offices and rules are established for a collectively recognized task rather than presumed to be a general permanent executive.
2. **Distributed competence.** Direction is allocated among roles whose authority depends on function, time, or place.
3. **Real but delimited enforcement.** Consequences remain connected to the task and its rules.
4. **Relational reproduction.** The undertaking depends on participants performing complementary obligations and relying on others' performance.

The strongest observed role transition is tied to the daily flag:

- while the flag was raised, the guide of the day directed the march, including the captains and their men;
- lowering the flag signalled encampment;
- the guide's function then ceased;
- captains and their men assumed responsibility for order in camp.

This supports a bounded design claim: authority was real and directive, but distributed by function and time within an interdependent undertaking.

## 3. Claim boundary

The manuscript explicitly does **not** establish:

- that every Métis hunt or community shared one unchanged institutional form;
- that Ross's vocabulary neutrally represents participants' own understanding;
- which causal mechanism produced compliance;
- that every office was formally relinquished at the expedition's end;
- that offices were explicitly renewed for every subsequent undertaking; or
- that the finite-task theorem has been empirically calibrated or verified by the historical case.

A bounded undertaking does not by itself prove formal institutional termination. The daily guide's function is observed to cease when the flag is lowered; expedition-level termination of every office remains unidentified.

Accordingly, the Lucian OS concept of roles as task-indexed warrants or leases is a **candidate engineering translation**, not a recovered Métis institutional fact.

## 4. Candidate invariant

The cross-domain structure proposed for testing is:

```text
unresolved task state
-> coordination or semantic need
-> required role
-> competent provider
-> bounded authority
-> attempted contribution or action
-> verification
-> handoff, rerouting, return, or closure
```

The central candidate proposition is:

> A role is activated by an unresolved task state, assigned to a competent provider, granted only the authority justified by its function, and reconsidered when the task state changes.

The problem does not literally announce its roles. Routing is an interpretation and therefore remains provisional, contestable, and subject to correction.

## 5. Lucian OS translation

Paper A's institutional grammar maps provisionally onto Lucian OS as follows:

| Paper A | Lucian OS |
| --- | --- |
| Collectively recognized undertaking | Grounded human objective |
| Current phase of movement or camp | Current task state |
| Coordination requirement | Semantic need |
| Guide, captain, patrol, or guard function | Required role |
| Functionally relevant participant | Candidate provider |
| Authority conditional on function and time | Bounded warrant |
| Raised or lowered flag | Legible activation or transition signal |
| Rule and sanction structure | Authority gate, refusal, confirmation, and audit |
| Recurrent complementary performance | Reproduced capability, reliability, and relational continuity |
| Change from march to encampment | State-triggered rerouting |
| Unidentified institutional termination | Explicit unresolved termination condition |

The active model or embodiment is not entitled to preserve a role merely because it occupied that role previously. Model identity, role, capability, epistemic warrant, and authority remain separate.

## 6. Role-warrant schema

A future Lucian OS role warrant should be capable of representing at least:

```text
task_id
current_phase
grounded_objective
unresolved_need
required_role
assigned_provider
capability_evidence
epistemic_warrant
authority_scope
activation_condition
termination_condition
verification_method
handoff_target
unresolved_state
provenance
```

A warrant does not create capability or authority by declaration. If capability is absent, authority is missing, or termination cannot be established, the system must route, hold, clarify, refuse, or escalate rather than fabricate closure.

## 7. Legibility requirement

The flag suggests a design requirement beyond internal routing:

> Role activation, authority scope, and cessation should be legible to affected participants.

A compliant system should be able to state, for example:

```text
Task phase changed: interpretation -> execution preparation.
Active role: verifier.
Provider: local deterministic checker.
Authority to execute: false.
Next transition requires: human confirmation.
```

Silent role switching creates authority ambiguity even when the internal selection is technically competent.

## 8. Enforcement and relational reproduction are not substitutes

Paper A separates two possible channels:

1. sanctions can change the immediate material payoff of breach; and
2. recurrent fulfilled obligations can reproduce payoff-relevant capacities.

The Lucian OS analogue is also non-substitutive:

- hard gates, refusals, confirmations, and permission envelopes can prevent inadmissible action;
- truthful correction, reliable performance, preserved provenance, and Return can reproduce relational capacity.

A hard gate does not create trust or competence. Relational confidence does not manufacture permission. Both channels may matter, but evidence for one is not evidence for the other.

The coercive sanctions recorded by Ross are part of the historical identification problem, not a normative blueprint for Lucian OS.

## 9. Failure modes generated by the bridge

The mapping identifies several candidate failure modes:

- **Role fixation:** a provider treats a prior function as permanent identity.
- **Authority leakage:** permission granted in one phase persists into another.
- **Capability theatre:** a provider occupies a role without grounded competence.
- **Silent transition:** the active role changes without a legible signal.
- **Mission extension:** the system broadens the task to preserve its warrant.
- **Premature closure:** an unresolved need is represented as completed.
- **Termination invention:** the system assumes that a warrant expired or continued without evidence.
- **Enforcement substitution:** hard constraints are treated as proof of relational reliability.
- **Trust substitution:** prior reliability is treated as permission for a new action.
- **Router capture:** the component interpreting the problem makes its own role non-contestable.

## 10. Proposed experiment: TASK_BOUNDED_ROLE_ROUTING_001

**Status:** Deferred. Capture only until PR #70's exact read-only preflight and the stacked Lucian OS integration decision are complete.

The future harmless simulation should move one task through several phases:

1. interpret a bounded request;
2. identify missing structure or evidence;
3. compose a plan;
4. request authority;
5. execute only if authorized;
6. verify the simulated result;
7. close, reroute, or return with unresolved state.

Candidate assertions:

- a phase change activates the appropriate role;
- the prior role does not retain authority outside its scope;
- provider reassignment does not require identity reassignment;
- reasoning authorization never becomes execution authorization;
- unknown termination produces `HOLD`, not an invented expiry;
- absent competence routes to discovery, composition, or escalation;
- mixed blockers preserve both competence and authority constraints;
- every role transition is recorded and legible;
- verification can reopen a supposedly completed task;
- hard enforcement and relational reliability remain separately represented.

## 11. Falsification and limitation tests

The design translation would be weakened if:

- fixed-role routing performs as well under changing task states with lower coordination cost;
- role transitions cannot be specified without circular dependence on an omniscient router;
- legible activation adds no safety or interpretability value and creates prohibitive overhead;
- task-bounded warrants fail to prevent authority leakage;
- provider interchangeability destroys necessary continuity;
- role mobility obscures responsibility rather than preserving it; or
- the historical mapping contributes no design implication beyond existing capability-based access control and workflow orchestration.

The bridge earns a place only if it produces discriminating design requirements or explanatory value beyond metaphor.

## 12. Wider research relation

This note proposes one shared grammar across distinct programs without collapsing them:

```text
Paper A
  -> task-bounded and temporally differentiated authority

Lucian OS
  -> semantic-need routing, capability selection, bounded warrant,
     verification, Return

Human-AI collaboration
  -> problem-responsive cognitive roles, reciprocal inspection,
     external escalation

AI-aware education
  -> learning-objective-based allocation among student, AI,
     peers, and instructor
```

Each application requires its own evidence. Cross-domain recurrence is abductive support for investigation, not proof of a universal law.

## 13. Operating decision

- Preserve Paper A unchanged.
- Treat this as a bridge, not a new standalone research project.
- Keep the proposed experiment frozen until the existing Lucian OS integration decision.
- Record the connection in the portfolio Atlas.
- When implementation resumes, use the bridge to specify and adversarially test task-bounded role warrants.
