# BUILT_DISCERNMENT_003 — Initial Literature Map

**Status:** preliminary literature map; not a systematic review  
**Date:** 2026-09-14  
**Project:** Lucian OS / continuity research  
**Related notes:** `TEXTURE_VS_OVERFITTING_001_RESEARCH_NOTE.md`, `BUILT_DISCERNMENT_002_TIMING_RHYTHM_AND_MECHANISM.md`

## Purpose

This note asks which parts of the provisional **built discernment** construct are already explained by existing literatures, and which combination may remain empirically distinctive.

The current construct concerns whether accumulated human–LLM collaboration can improve the situated selection, suppression, and timing of prior context under underspecified tasks — without claims about consciousness, subjective experience, identity continuity, or conversational weight editing.

This is an initial map, not a novelty claim.

## 1. Practical wisdom / phronesis

Aristotelian practical wisdom is an important comparison class because it distinguishes possession of general principles from judgment about particulars.

The Stanford Encyclopedia of Philosophy's discussion of Aristotle's ethics emphasizes that practical wisdom cannot be acquired solely by learning general rules; one must learn to see what a particular occasion calls for. It also stresses that practical judgment concerns which features of a situation matter and how general understanding is applied in concrete circumstances.

A recent discussion of **kairos and phronesis** makes the temporal aspect unusually explicit: appropriate action concerns not only what response is warranted, but when, toward whom, to what degree, and for how long.

Relevant sources:

- Stanford Encyclopedia of Philosophy, **Aristotle's Ethics**: https://plato.stanford.edu/entries/aristotle-ethics/
- Stanford Encyclopedia of Philosophy, **Wisdom in Contemporary Analytic Philosophy**: https://plato.stanford.edu/entries/wisdom-analytic/
- Oxford Academic, **Kairos and phronesis in teaching well**: https://academic.oup.com/jope/article/59/3-4/718/8084912

### Relevance to built discernment

This literature strongly supports the conceptual distinction:

> **principles do not eliminate the need for situated judgment.**

It also supports treating **timing** as part of good judgment rather than as a secondary implementation detail.

What it does not by itself establish is whether an LLM collaboration can develop a measurable analogue of this situated selectivity.

## 2. Situated action

Lucy Suchman's work on situated action challenges the view that competent action is merely execution of a complete prior plan. Plans can function as resources for practical activity, while actual conduct remains responsive to unfolding circumstances.

Relevant source:

- Lucy Suchman, **Situated Actions**, in *Human-Machine Reconfigurations*: https://www.cambridge.org/core/books/abs/humanmachine-reconfigurations/situated-actions/F4AA82303887FF0875BD656977661875

### Relevance to built discernment

This is close to the distinction between:

- a constitutional or principle layer;
- and the situated interpretation required to act within it.

It cautions against expecting a sufficiently long rule set or handoff document to fully determine appropriate action in advance.

## 3. Adaptive expertise

The adaptive-expertise literature distinguishes routine efficiency from the ability to alter strategies under novelty while preserving underlying understanding.

A health-professions review describes adaptive expertise as combining efficient reproduction of known performance with innovation and preparation for future learning. Importantly, adaptive experts are not tied to one solution: they can preserve the rationale while changing the action when circumstances require it.

Relevant sources:

- Hatano & Inagaki (1986), **Two Courses of Expertise**: https://docs.edtechhub.org/lib/SN8XH8X9
- Schwartz, Bransford & Sears (2005), **Efficiency and Innovation in Transfer**: https://aaalab.stanford.edu/assets/papers/2005/EffInnovTransfer_SchwartzBransfordSears_2005.pdf
- Mylopoulos et al., **Preparing Future Adaptive Experts: Why It Matters and How It Can Be Done**: https://pmc.ncbi.nlm.nih.gov/articles/PMC8368930/

### Relevance to built discernment

This gives a strong comparison for the proposed distinction between:

- reproducing familiar collaborative moves;
- and preserving method while changing action under a novel frame.

A useful implication is:

> **texture without transfer is not sufficient evidence of discernment.**

## 4. Expertise and selective attention

Expertise research provides evidence that superior performance often involves better allocation of attention toward task-relevant cues and less processing of redundant or irrelevant information.

A systematic review of gaze behavior reports broad support for an **information-reduction** account in which experts selectively allocate attention to task-relevant information. An Annual Review synthesis likewise notes that experts focus more efficiently on decision-relevant information than novices.

Relevant sources:

- Brams et al. (2019), **The relationship between gaze behavior, expertise, and performance: A systematic review**: https://pubmed.ncbi.nlm.nih.gov/31414844/
- **Experts and Expertise in Organizations: An Integrative Review on Individual Expertise**: https://doi.org/10.1146/annurev-orgpsych-020323-012717

### Relevance to built discernment

This is a useful human analogue for the claim that expertise may manifest not as processing more cues, but as **better selectivity**.

However, the analogy should remain limited: attentional expertise in humans is not evidence for a particular mechanism in transformers.

## 5. In-context adaptation without weight updates

The machine-learning literature clearly establishes that transformer behavior can adapt to information supplied at inference time without gradient-based weight updates.

Relevant sources:

- Chen et al. (ICML 2024), **Exact Conversion of In-Context Learning to Model Weights in Linearized-Attention Transformers**: https://proceedings.mlr.press/v235/chen24r.html
- Dherin et al. (2025), **Learning without training: The implicit dynamics of in-context learning**: https://research.google/pubs/learning-without-training-the-implicit-dynamics-of-in-context-learning/

### Relevance to built discernment

This supports a modest mechanistic stance:

> behavioral adaptation during a continuing interaction does not require a claim that conversational turns are editing the base model weights.

It does **not** establish that ordinary long-run collaboration produces built discernment; it only removes weight editing as a necessary condition for context-sensitive behavioral adaptation.

## 6. Long-term personalization and memory

Recent LLM research increasingly studies assistants that retain and use information from extended interaction histories.

Examples include:

- **PersonaLens** (ACL 2025), which evaluates personalization while completing task-oriented assistance: https://aclanthology.org/2025.findings-acl.927/
- **Reflective Memory Management** (ACL 2025), which adapts memory summarization and retrieval across dialogue contexts: https://aclanthology.org/2025.acl-long.413/
- **RealPref** (2026), which evaluates long-horizon preference following with explicit and implicit preferences and reports difficulty generalizing preferences to unseen scenarios: https://arxiv.org/abs/2603.04191
- **HorizonBench** (2026), which tests evolving preferences across long histories and reports substantial belief-update failures, including reversion to superseded preferences: https://arxiv.org/abs/2604.17283

### Relevance to built discernment

This literature is directly adjacent but mostly asks questions such as:

- Can the system remember the relevant preference?
- Can it retrieve the right episode?
- Can it update the user's state?
- Can it personalize a response while completing a task?

Our provisional question is different:

> **Can relational history improve judgment about when a remembered preference, concept, or method should *not* govern the current task?**

This shifts the dependent variable from memory availability toward **conditional authority, selective non-use, and timing**.

## 7. Irrelevant context and long-context degradation

Recent work also shows that more context is not monotonically beneficial.

Yang et al. (EMNLP 2025) show that irrelevant context can disrupt LLM reasoning path selection and accuracy. Du et al. (Findings of EMNLP 2025) report that long input length can degrade performance even under conditions designed to remove ordinary retrieval failure.

Relevant sources:

- Yang et al. (2025), **How Is LLM Reasoning Distracted by Irrelevant Context?**: https://aclanthology.org/2025.emnlp-main.674/
- Du et al. (2025), **Context Length Alone Hurts LLM Performance Despite Perfect Retrieval**: https://aclanthology.org/2025.findings-emnlp.1264/

### Relevance to built discernment

These results strengthen the case that continuity cannot be treated as simply maximizing inherited context.

They also sharpen the overfitting alternative: rich history may improve personalization while simultaneously increasing opportunities for distraction, stale-state activation, or relevance promotion.

## Emerging synthesis

The adjacent literatures already contain many components of the proposed construct:

- **phronesis:** principles require judgment in particulars;
- **kairos:** fitting action includes timing;
- **situated action:** plans and rules do not exhaust action selection;
- **adaptive expertise:** expertise must transfer under novelty rather than rigidly reproduce routines;
- **expert attention:** expertise can involve selective reduction of irrelevant information;
- **in-context learning:** inference-time context can alter behavior without weight updates;
- **LLM personalization:** long-term history can support personalized behavior;
- **long-context robustness:** more inherited material can also hurt performance.

The potentially distinctive question lies in their intersection:

> **Can accumulated relational history make an LLM more conditionally selective — increasing use of familiar material when it is warranted while decreasing its influence when it is merely salient — and can this selectivity include appropriate timing across phases of a collaboration?**

## Candidate research gap

The initial search did **not** establish that this question is novel. A systematic review is still required.

However, the personalization benchmarks located so far primarily evaluate remembering, retrieving, updating, or following user-specific information. The irrelevant-context literature primarily evaluates resistance to distractors. The expertise and practical-wisdom literatures study situated selection in humans.

The proposed research program joins these into a sharper test:

> **Does relational history improve not just memory use, but the calibration of memory authority?**

A key metric would be a **conditional-selectivity interaction**:

- with richer relational history, appropriate use of a familiar concept should increase when the concept is task-authoritative;
- with the same richer history, inappropriate use should decrease when the concept is supporting, superseded, premature, or merely associative.

A second metric would be **temporal calibration**:

- the model should not merely know a good move;
- it should deploy it in the phase in which it becomes warranted.

## Immediate next search

The next literature pass should specifically look for prior work on:

1. selective memory suppression or memory gating in personalized LLM agents;
2. context authority / relevance ranking beyond retrieval relevance;
3. stale preference suppression and supersession;
4. temporal or phase-aware personalization;
5. pragmatic-frame inference from interaction history;
6. human–AI team adaptation over repeated collaboration;
7. benchmarks where a familiar personalized response is deliberately the wrong response in a new frame.

Until that search is complete, **built discernment** should remain a provisional construct rather than a novelty claim.