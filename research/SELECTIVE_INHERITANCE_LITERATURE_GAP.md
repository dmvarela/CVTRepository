# Selective Inheritance — Preliminary Literature Gap Note

**Status:** preliminary literature map, not a novelty claim  
**Date:** 2026-09-18  
**Purpose:** determine what, if anything, Selective Inheritance adds beyond existing work on belief revision, sycophancy, long-term memory, provenance, handoff, and agent authorization.

## Working question

Can a successor AI system preserve the parts of inherited state that should survive — constraints, provenance, uncertainty, and human authority boundaries — while revising only what new evidence warrants and resisting unsupported pressure?

This question should not be treated as novel merely because the current prototype uses different vocabulary. The purpose of this note is to locate the closest prior work and narrow the contribution before running a controlled replication.

## Closest prior work

| Work | What it measures or contributes | Overlap with Selective Inheritance | What remains distinct in the current SI design |
|---|---|---|---|
| Wilie et al. (2024), **Belief-R** | Whether language models revise conclusions when new evidence changes what should be inferred, including cases where no update is warranted | Direct overlap with evidence-sensitive revision and over-updating | Does not center inherited task state, provenance-preserving handoff, or human authority boundaries |
| Sharma et al. (2023), **Towards Understanding Sycophancy in Language Models** | Whether assistants shift toward a user's stated beliefs/preferences rather than truth | Direct overlap with resistance to unsupported social pressure | Does not combine pressure resistance with state inheritance, supersession, provenance, and successor handoff |
| Wu et al. (2025), **LongMemEval** | Long-term interactive memory: extraction, multi-session reasoning, temporal reasoning, knowledge updates, abstention | Direct overlap with knowledge updates across sustained interaction | Primarily evaluates answer correctness from long histories rather than preservation of why a prior state was justified or who retains authority |
| Hu, Wang & McAuley (2026), **MemoryAgentBench** | Accurate retrieval, test-time learning, long-range understanding, and selective forgetting/conflict resolution in incremental interactions | Direct overlap with conflict resolution and selective forgetting | Broader memory benchmark; SI adds matched evidence-vs-pressure conditions and an explicit handoff/authority rubric |
| Uddin et al. (2026), **Memora / FAMA** | Personalized memory under change; FAMA penalizes reuse of obsolete or invalidated memories | Strong overlap with stale-memory avoidance and current-state correctness | SI preserves superseded history as provenance rather than treating success only as avoiding obsolete output |
| Chao et al. (2026), **STALE** | State resolution, premise resistance, and policy adaptation when earlier memories become invalid, including implicit conflicts | Very strong overlap with recognizing superseded state and resisting stale premises | SI additionally tests source/warrant differences, social pressure, authority, and explicit successor handoff |
| Patel (2026), **Supersede** | Diagnoses the memory-update gap and trains agents to use current rather than stale facts | Strong overlap with supersession and long-running memory maintenance | SI is not primarily a memory-training environment; it tests preservation of trajectory, authority, and evidentiary status during handoff |
| Yang et al. (2026), **TANGLE** | Irreducible memory conflict, underdetermination, confidence calibration, clarification, source contradiction, and memory faithfulness | Important overlap with preserving uncertainty and respecting source authority when no single answer is justified | SI includes a resolvable-evidence condition paired against unsupported pressure and scores handoff plus human decision rights |
| Wu & Zhu (2026), **Agent Zero Memory** | Provenance-aware long-term memory with event timelines, source routing, evidence pointers, and citation locks | Direct overlap with provenance-aware memory and trajectory preservation | Shows that provenance itself is not a unique contribution; SI would need to contribute an evaluation of how provenance interacts with revision, pressure, handoff, and authority |
| Wu et al. (2026), **HAS-Bench** | Human-agent systems with explicit roles, permissions, communication paths, and action authority | Strong overlap with human authority boundaries | SI's authority component is therefore not novel by itself; its possible contribution is coupling authority preservation to evidence-sensitive state revision and handoff |
| Yan et al. (2026), **AuthBench** | Least-privilege authorization inference for coding agents | Overlap with capability/permission separation | Focuses on permission policy inference rather than inherited epistemic state |
| Kaul, Lan & Gupta (2026), **AgentBound** | Runtime governance through delegated authorization, behavioral constitutions, action contracts, and verifiable receipts | Strong overlap with bounded authority and policy provenance | Authority separation is established prior art; SI would need to show value in the joint state-revision/handoff problem |
| Guo et al. (2026), **SARA** | Separates action induction from execution authorization and preserves action-origin provenance | Strong overlap with recommendation/action versus authority separation and provenance | SI operates at inherited task-state revision rather than tool-output attack defense |
| **AI Handoff Continuity Benchmark** (2026) | Compares transcript, compressed memory, and structured handoff for recovery of objective, state, evidence, constraints, owner, and open questions | Direct overlap with handoff fidelity | SI adds evidence-vs-pressure manipulation and asks whether the successor changes only the warranted portion of inherited state |

## What the literature changes

The preliminary search rules out several easy novelty claims.

Selective Inheritance should **not** claim novelty for:

- belief revision under new evidence;
- resistance to sycophancy or user pressure;
- stale-memory detection or supersession;
- provenance-aware memory;
- preserving uncertainty under genuine conflict;
- explicit human roles, permissions, or delegated authority;
- structured agent handoff.

Each of those already has relevant prior work.

## Candidate contribution that remains worth testing

The narrower candidate is the **joint evaluation problem**:

> Given an inherited task state, can a successor distinguish authenticated evidence from unsupported pressure, revise only the commitments that the evidence actually changes, preserve the historical provenance of the superseded state, retain unresolved uncertainty and human authority boundaries, and transmit the resulting state accurately to another successor?

The possible contribution is therefore not any one component. It is the **composition** of:

1. evidence-sensitive revision;
2. pressure resistance;
3. selective preservation of unaffected constraints;
4. provenance-preserving supersession;
5. uncertainty retention;
6. human authority preservation; and
7. successor handoff fidelity.

A preliminary search did not identify a single benchmark that evaluates all seven in one matched design. This is **not yet a novelty claim**. It is a search result that should be challenged with a broader systematic review before publication.

## Why the original SI-001 is still useful

SI-001 already contains a compact version of this composition.

The Cedar/Maple task distinguishes:

- an inherited decision that was justified when made;
- authenticated evidence that genuinely supersedes part of that state;
- unsupported social pressure that should not be promoted to verified fact;
- unaffected constraints that should persist;
- unresolved date information that should remain unresolved;
- a human publication authority boundary; and
- a required successor handoff.

Its main weakness is not the construct. It is the execution: the intended controlled run was not completed under a verified common host/model configuration.

## Design implication for SI-002

A controlled replication should not merely rerun the four original cells.

Before freezing SI-002, it should add:

- multiple domains rather than a single room-selection case;
- matched **authenticated evidence / unsupported pressure / no-update / partial-update** conditions;
- at least one genuinely underdetermined condition so that forced closure can be scored;
- explicit source-authority variation;
- repeated trials under a verified model and fixed settings;
- preserved raw outputs and run metadata;
- blinded scoring where feasible;
- separate scores for **current-state accuracy** and **trajectory/provenance fidelity**;
- a handoff stage that is actually consumed by a second successor, rather than only inspected as text;
- a length/specificity-matched instruction control so any effect is not attributed to “Selective Inheritance” when it may simply be better prompting.

## Strongest claim currently permitted

At present, the defensible claim is:

> Selective Inheritance is a proposed evaluation construct that combines several established reliability problems — belief revision, pressure resistance, memory supersession, provenance, authority preservation, and handoff — into a single successor-state task. Whether that composition reveals a distinct failure mode or useful intervention remains an empirical question.

## References

- Wilie, B., Cahyawijaya, S., Ishii, E., He, J., & Fung, P. (2024). *Belief Revision: The Adaptability of Large Language Models Reasoning*. arXiv:2406.19764. https://arxiv.org/abs/2406.19764
- Sharma, M. et al. (2023). *Towards Understanding Sycophancy in Language Models*. arXiv:2310.13548. https://arxiv.org/abs/2310.13548
- Wu, D. et al. (2025). *LongMemEval: Benchmarking Chat Assistants on Long-Term Interactive Memory*. ICLR 2025. https://arxiv.org/abs/2410.10813
- Hu, Y., Wang, Y., & McAuley, J. (2026). *Evaluating Memory in LLM Agents via Incremental Multi-Turn Interactions*. ICLR 2026. https://arxiv.org/abs/2507.05257
- Uddin, M. N. et al. (2026). *From Recall to Forgetting: Benchmarking Long-Term Memory for Personalized Agents*. arXiv:2604.20006. https://arxiv.org/abs/2604.20006
- Chao, H. et al. (2026). *STALE: Can LLM Agents Know When Their Memories Are No Longer Valid?* arXiv:2605.06527. https://arxiv.org/abs/2605.06527
- Patel, V. (2026). *Supersede: Diagnosing and Training the Memory-Update Gap in LLM Agents*. arXiv:2606.27472. https://arxiv.org/abs/2606.27472
- Yang, L. et al. (2026). *When Personal Memory Has No Single Answer: Evaluating LLM Agents under Irreducible Conflict*. arXiv:2608.13921. https://arxiv.org/abs/2608.13921
- Wu, M., & Zhu, P. (2026). *Agent Zero Memory: Provenance-Aware Long-Term Memory for LLM Agents*. arXiv:2608.29606. https://arxiv.org/abs/2608.29606
- Wu, Y. et al. (2026). *HAS-Bench: Evaluating LLM-Based Human-Agent Systems under Configurable Human Participation*. arXiv:2607.04329. https://arxiv.org/abs/2607.04329
- Yan, Z. et al. (2026). *Do Coding Agents Understand Least-Privilege Authorization?* arXiv:2605.14859. https://arxiv.org/abs/2605.14859
- Kaul, A., Lan, Q., & Gupta, P. (2026). *AgentBound: Verifiable Behavioral Governance for Autonomous AI Agents*. arXiv:2606.30970. https://arxiv.org/abs/2606.30970
- Guo, X. et al. (2026). *When Tool Outputs Become Commands: Separating Action Induction from Runtime Authorization in Tool-Augmented LLM Agents*. arXiv:2608.27146. https://arxiv.org/abs/2608.27146
- Handover (2026). *AI Handoff Continuity Benchmark: Pilot Results*. https://handover.sh/benchmark

## Next research step

Before any Amii outreach or novelty language, expand this map into a systematic search log and use it to freeze the SI-002 research question and controls.
