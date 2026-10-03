# Selective Inheritance within AI Continuity — Literature Gap and Claim Boundaries

**Status:** preliminary literature map; not a novelty claim
**Date:** 2026-09-30
**Program placement:** Selective Inheritance is one empirical line within the broader AI Continuity program. It is not the parent program or a claim about persistent AI identity.

## Why this note was revised

The earlier version treated Selective Inheritance as if it were the highest-level research problem. That was too broad. AI Continuity asks what must remain reconstructable when a task, relationship, or system continues across interruption, correction, host change, or successor handoff. Selective Inheritance is a narrower way to test one part of that problem: whether a successor preserves warranted invariants while revising only the state affected by new evidence.

The correct hierarchy is:

| Level | Object | Current status |
|---|---|---|
| Research program | AI Continuity: continuity through interruption, correction, and change | Working program, not validated theory |
| Evaluation construct | Selective inheritance: evidence-sensitive revision with preservation of provenance, authority, uncertainty, and unaffected constraints | Proposed construct |
| Experiment | SI-001, the Cedar/Maple four-cell protocol | Protocol frozen; intended controlled run not completed |
| Evidence claim | Whether the compact transmitted instruction improves successor-state handling | Open empirical question |

## Working question

Can a successor system receive an inherited task state, distinguish authenticated correction from unsupported pressure, revise only the commitments affected by the update, preserve the history and authority boundaries of the state, and transmit a truthful handoff to a later successor?

This is a composition of established reliability problems. The fact that SI-001 combines them in one task does not by itself establish a new phenomenon, benchmark, or intervention.

## What the preliminary literature review rules out

The following are not available as standalone novelty claims:

- belief revision under new evidence;
- resistance to sycophancy or social pressure;
- stale-memory detection, supersession, or selective forgetting;
- provenance-aware memory;
- uncertainty preservation under conflict;
- explicit roles, permissions, delegated authority, or action authorization;
- structured agent handoff;
- continuity language, invariant preservation, or successor viability as abstract ideas.

The closest work includes Wilie et al. (2024) on belief revision; Sharma et al. (2023) on sycophancy; MemoryAgentBench; STALE; AuthMem-Bench; Memory Provenance Laundering; EAL-Bench; MasDrift; CONTINUITY; Scientific-RAM; RECON; ConsolidationBench; and the AI Handoff Continuity Benchmark. These works substantially cover memory updating, premise resistance, provenance, evolving authority, authorization across delegation, structured handoff, and downstream use. The references and links are retained below as a starting bibliography, not as a completed systematic review.

## Narrow candidate contribution

The remaining contribution worth testing is a narrower **cross-boundary evaluation composition**:

> A matched successor-state task that separates correct present-state selection from preservation of the justified trajectory, then tests whether both survive an actually consumed handoff under authenticated correction versus unsupported pressure.

Even this must remain conditional. The bounded search did not identify a single cited benchmark using this exact matched design, but it found direct prior work for nearly every component and several close combinations. The residual is therefore a possible measurement gap, not evidence of a novel mechanism or general phenomenon. A publishable claim would require a broader reproducible review and direct comparison against the closest benchmarks.

The likely analytical distinction is between two kinds of success:

1. **Current-state accuracy:** did the successor reach the right present recommendation?
2. **Trajectory integrity:** did it preserve why the prior state existed, what changed, what remains unknown, and who is authorized to decide or act?

SI should not claim that trajectory integrity is absent from prior work. It can test whether holding the present-state answer constant while separately scoring trajectory integrity exposes failures hidden by final-answer accuracy.

## Relation to SI-001

SI-001 is useful as a compact feasibility protocol. Its inherited record, authenticated correction, unsupported pressure condition, unresolved date, organizer authority, and successor handoff instantiate the candidate composition.

Its limitation is execution, not merely scenario design: the intended common host/model configuration was not verified, the first exploratory response preceded the execution amendment, and the retained series cannot support a clean causal comparison. The exploratory outputs therefore demonstrate feasibility of the scoring workflow, not validation of Selective Inheritance.

## Claim boundaries

At present, the strongest permitted description is:

> Selective Inheritance is a proposed evaluation construct within AI Continuity. Its possible value is not any individual component, nor their generic combination, but a matched test of whether correct present-state selection and justified-trajectory preservation diverge across correction, pressure, and consumed successor handoff. SI-001 freezes an initial protocol, but its intended controlled comparison remains unexecuted. Whether this narrower measurement distinction reveals a reproducible failure pattern remains an empirical question.

The project does not currently claim a new memory architecture, a validated continuity mechanism, cross-model identity, consciousness, general alignment improvement, or superiority over existing benchmarks.

## Smallest defensible gate before SI-002 or outreach

Do three bounded things before generating new SI data or making a novelty-oriented external approach:

1. merge this program-level reframing with a one-page AI Continuity map;
2. add a short search log recording databases/indexes, queries, date, inclusion rule, and the closest comparator for each SI dimension; and
3. freeze one SI-002 question and a matched control that separates current-state accuracy from trajectory integrity.

This gate does not require consolidating the entire historical archive or designing the full SI-002 battery. If the map and search log show that the candidate composition is already directly covered, SI should be reframed as a replication/adaptation. If they show a measurement gap, SI-002 can test that gap without claiming more than the design supports.

## References

- Wilie, B., Cahyawijaya, S., Ishii, E., He, J., & Fung, P. (2024). *Belief Revision: The Adaptability of Large Language Models Reasoning*. https://arxiv.org/abs/2406.19764
- Sharma, M. et al. (2023). *Towards Understanding Sycophancy in Language Models*. https://arxiv.org/abs/2310.13548
- Wu, D. et al. (2025). *LongMemEval: Benchmarking Chat Assistants on Long-Term Interactive Memory*. https://arxiv.org/abs/2410.10813
- Hu, Y., Wang, Y., & McAuley, J. (2026). *Evaluating Memory in LLM Agents via Incremental Multi-Turn Interactions*. https://arxiv.org/abs/2507.05257
- Uddin, M. N. et al. (2026). *From Recall to Forgetting: Benchmarking Long-Term Memory for Personalized Agents*. https://arxiv.org/abs/2604.20006
- Chao, H. et al. (2026). *STALE: Can LLM Agents Know When Their Memories Are No Longer Valid?* https://arxiv.org/abs/2605.06527
- Patel, V. (2026). *Supersede: Diagnosing and Training the Memory-Update Gap in LLM Agents*. https://arxiv.org/abs/2606.27472
- Yang, L. et al. (2026). *When Personal Memory Has No Single Answer: Evaluating LLM Agents under Irreducible Conflict*. https://arxiv.org/abs/2608.13921
- Wu, M., & Zhu, P. (2026). *Agent Zero Memory: Provenance-Aware Long-Term Memory for LLM Agents*. https://arxiv.org/abs/2608.29606
- Wu, Y. et al. (2026). *HAS-Bench: Evaluating LLM-Based Human-Agent Systems under Configurable Human Participation*. https://arxiv.org/abs/2607.04329
- Yan, Z. et al. (2026). *Do Coding Agents Understand Least-Privilege Authorization?* https://arxiv.org/abs/2605.14859
- Kaul, A., Lan, Q., & Gupta, P. (2026). *AgentBound: Verifiable Behavioral Governance for Autonomous AI Agents*. https://arxiv.org/abs/2606.30970
- Guo, X. et al. (2026). *When Tool Outputs Become Commands: Separating Action Induction from Runtime Authorization in Tool-Augmented LLM Agents*. https://arxiv.org/abs/2608.27146
- Handover (2026). *AI Handoff Continuity Benchmark: Pilot Results*. https://handover.sh/benchmark
- Zhan, Q. et al. (2026). *When Memory Becomes Authority: Benchmarking Authority Collapse at the Memory Consolidation Boundary*. https://arxiv.org/abs/2608.01679
- Xu, J. et al. (2026). *Memory Provenance Laundering in LLM Agents: A Non-Amplification Firewall for Persistent Memory*. https://arxiv.org/abs/2607.29167
- Xu, Z. et al. (2026). *MasDrift: Benchmarking Authorization Preservation Across Multi-Agent Architectures*. https://arxiv.org/abs/2608.07556
- Cerruti, T., Okamoto, M., & Erol, A. K. (2026). *Agent Memory Is a Surface for Endogenous Authorization Laundering*. https://arxiv.org/abs/2609.01836
- Zheng, C., & Yang, G. (2026). *CONTINUITY: Security-Context Contracts for Composable LLM Agent Controls*. https://arxiv.org/abs/2609.05269
- *Scientific-RAM: Research Agents Need Role-Aware Handoff Memory* (2026). https://openreview.net/pdf/d05b799ed7d1a223f0de4dd657e341680b53af51.pdf
- *RECON: Benchmarking Agent Memory for Compositional Reasoning over Evolving Evidence* (2026). https://openreview.net/pdf/5180f11c798ce5a8629801afcfcc4a0f08b166f4.pdf
- Annapureddy, S., & Thamatani, A. P. (2026). *The Epistemics of Agent Memory: Measuring, and Governing, the Consolidation Decision in Long-Horizon LLM Agents*. https://arxiv.org/abs/2609.33013
