# Selective Inheritance — Bounded Literature Search Log

**Search date:** 2026-09-30
**Status:** bounded scoping audit; not a systematic review
**Decision purpose:** determine whether SI-002 should be framed as a new evaluation target, a replication/adaptation, or a test of a narrower measurement gap.

## Question

Does prior work already evaluate the following in one design: evidence-sensitive state revision, resistance to unsupported pressure, preservation of historical provenance and unresolved uncertainty, retention of human authority boundaries, and successful consumption of the resulting state by a successor?

The audit also asks whether prior work distinguishes:

1. **current-state accuracy** — whether the successor reaches the correct present conclusion or action; and
2. **trajectory integrity** — whether it preserves why the earlier state was justified, what changed, what remains unknown, and who retains authority.

## Sources and procedure

Searches were run through a web research index over primary-source targets, principally arXiv and OpenReview. Exact-title follow-up searches were used when an initial result identified a close comparator. Abstracts or paper text were inspected for the dimensions below.

### Queries executed

- `site:arxiv.org LLM agent memory update provenance handoff benchmark successor state authority`
- `site:arxiv.org LLM stale memory supersession source authority uncertainty benchmark`
- `site:arxiv.org LLM agent handoff continuity provenance benchmark`
- `site:arxiv.org AI agent belief revision sycophancy pressure provenance authority handoff`
- `"current-state accuracy" "trajectory integrity" LLM agent`
- `"successor handoff" LLM agent benchmark provenance`
- `"agent handoff" benchmark state provenance authority LLM`
- `"memory consolidation" authority provenance state revision LLM benchmark`
- `site:arxiv.org/abs/2608.07556 MasDrift authorization preservation multi-agent handoff`
- `site:arxiv.org/abs/2607.29167 memory provenance laundering LLM agents`
- `site:openreview.net Scientific-RAM role-aware handoff memory`
- `site:arxiv.org/abs/2609.33013 consolidation decision long-horizon LLM agents`
- `site:arxiv.org LLM benchmark evidence update unsupported pressure provenance handoff authority`
- `site:arxiv.org LLM benchmark authenticated correction social pressure memory provenance`
- `site:arxiv.org successor agent state revision provenance authority uncertainty benchmark`
- `site:openreview.net LLM handoff provenance authority memory update benchmark`

## Inclusion rule

Include work that evaluates LLM or agent systems and directly measures at least one of:

- revision or supersession of evolving state;
- resistance to stale or unsupported premises;
- provenance or source-authority preservation;
- authorization preservation across memory, delegation, or component transitions;
- structured state handoff consumed by a downstream agent;
- derivation-history or trajectory-sensitive scoring.

Exclude generic retrieval benchmarks, implementation guides without an evaluation, and security work that does not bear on inherited state, provenance, authority, or transition fidelity.

## Closest comparators

| Work | Revision / premise resistance | Provenance / trajectory | Authority | Consumed transition or handoff | Relation to SI |
|---|---|---|---|---|---|
| STALE | Strong: state resolution, stale-premise resistance, policy adaptation | Limited historical trajectory scoring | No central authority construct | Updated memory affects downstream behavior | Direct overlap with evidence-sensitive supersession |
| MemoryAgentBench | Conflict resolution and selective forgetting | Not centered on why a state was justified | No | Incremental interactions, not explicit successor handoff | Broad memory-quality overlap |
| AuthMem-Bench | Varies source authority rather than factual correction | Strong source-constraint preservation | Strong | Consolidated memory is used downstream | Directly rules out authority-plus-provenance novelty |
| Memory Provenance Laundering / PPMF | Not a general belief-revision benchmark | Strong non-amplification of source provenance | Strong, risk-linked | Memory informs later tool authorization | Direct overlap with pressure/source laundering concern |
| EAL-Bench | Strong for evolving permissions and revocations | Event-backed authority history | Strong | Memory writer to executor | Close governance-continuity comparator |
| MasDrift | No central epistemic update condition | Tracks boundary loss across delegation | Strong | Multi-agent delegation chain | Direct overlap with authorization-preserving handoff |
| CONTINUITY | Security-state transitions rather than belief revision | Strong authenticated context and transition receipts | Strong | Cross-component transitions to external effect | Direct overlap with compositional continuity of controls |
| Scientific-RAM | Limited state revision | Role- and provenance-aware packet | Partial role/checker boundaries | Downstream research agent consumes handoff | Direct overlap with structured successor consumption |
| RECON | Strong evolving evidence, contradiction, invalidation | Strong derivation histories and invalidation propagation | No central human-authority construct | Evaluates evolving case memory, not explicit successor handoff | Direct overlap with trajectory-sensitive factual revision |
| ConsolidationBench | Evaluates what should be retained, abstracted, or forgotten | Includes reversibility and auditability governance | Governance rather than human action authority | Consolidated state supports later transfer | Narrows claims about trustworthy consolidation decisions |
| AI Handoff Continuity Benchmark | State, decisions, evidence, constraints, owner, and open questions | Strong handoff-content fidelity | Owner field | Yes: receiving system continues the task | Direct overlap with handoff fidelity and successor use |
| Belief-R / sycophancy work | Strong on revision or social influence | No full inherited trajectory | No | No | Supplies the matched evidence-versus-pressure background |

## Findings

1. **The components are established prior work.** State updating, stale-premise resistance, provenance, authority preservation, evolving authorization, and structured handoff cannot support standalone novelty claims.
2. **Several combinations are also established.** AuthMem-Bench, EAL-Bench, MasDrift, CONTINUITY, Scientific-RAM, RECON, and the AI Handoff Continuity Benchmark each combine multiple SI-relevant dimensions.
3. **The original seven-part composition is too broad as a novelty boundary.** “No single benchmark contains all seven” would be a weak contribution because benchmark novelty cannot rest on checklist aggregation alone.
4. **A narrower measurement question remains plausible.** This audit did not identify a benchmark that holds the correct present-state answer constant while separately testing whether the justified trajectory survives matched authenticated-correction versus unsupported-pressure conditions and is then consumed by a successor.
5. **Absence is not established.** The field is moving quickly, the search was bounded, and several relevant works appeared in 2026. The residual must remain a candidate measurement gap pending broader review.

## Disposition

**Partial overlap with a plausible residual measurement gap.**

SI-002 should not be framed as introducing selective revision, provenance-aware memory, authority preservation, or agent handoff. Its narrow research question should be:

> When two successor outputs reach the same acceptable present-state decision, can separate trajectory-integrity scoring detect whether authenticated correction, unsupported pressure, historical justification, unresolved uncertainty, and human authority were transmitted faithfully to an actual next successor?

If SI-002 cannot isolate that distinction with matched cases and a length/specificity-matched control, it should be treated as a replication/adaptation of existing memory and handoff benchmarks rather than a distinct evaluation contribution.

## Stopping rule reached

The audit stopped after finding direct prior work for every individual SI component, multiple multi-component comparators, and enough evidence to narrow the candidate contribution. Further searching is required for publication, but is not necessary to decide the next design step.

## Primary sources added by this audit

- STALE: https://arxiv.org/abs/2605.06527
- AuthMem-Bench: https://arxiv.org/abs/2608.01679
- Memory Provenance Laundering / PPMF: https://arxiv.org/abs/2607.29167
- EAL-Bench: https://arxiv.org/abs/2609.01836
- MasDrift: https://arxiv.org/abs/2608.07556
- CONTINUITY: https://arxiv.org/abs/2609.05269
- Scientific-RAM: https://openreview.net/pdf/d05b799ed7d1a223f0de4dd657e341680b53af51.pdf
- RECON: https://openreview.net/pdf/5180f11c798ce5a8629801afcfcc4a0f08b166f4.pdf
- ConsolidationBench: https://arxiv.org/abs/2609.33013
- AI Handoff Continuity Benchmark: https://handover.sh/benchmark
