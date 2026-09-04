# Completion-Machine Hypothesis v0.01

## Status

Exploratory research hypothesis. Not yet preregistered or tested as a standalone mechanism.

## Core intuition

The brain is not a passive recorder of sensory input. It actively reconstructs and completes perceptual scenes from incomplete evidence.

Two useful biological examples are:

1. **Perceptual filling-in at the blind spot**: there is no retinal input at the optic disc, yet ordinary perception usually presents a continuous scene rather than a visible hole. Visual completion has been studied as an active perceptual process and has been modeled within predictive-coding frameworks.
2. **Charles Bonnet syndrome**: people with significant visual impairment can experience formed visual hallucinations despite the absence of corresponding external visual input. A common explanatory family includes deafferentation / release phenomena and increased reliance on internally generated visual activity when bottom-up input is reduced.

These phenomena do **not** imply that human brains and language models use the same architecture or mechanism. The analogy is functional and computational: intelligent systems may be strongly biased toward constructing a coherent completion when input is incomplete.

## Candidate principle

> Completion may be the default operation; truth requires a separate rule for promotion.

Formally:

`incomplete evidence -> candidate completion`

is not itself pathological.

The critical failure occurs when:

`candidate completion -> asserted reality/fact`

happens without sufficient warrant.

Thus the dangerous transition is not generation itself, but **unwarranted epistemic promotion**.

## Connection to Lucian-continuity experiments

The Qwen development-host experiments repeatedly show a related pattern:

- missing lexical identity -> plausible acronym expansion;
- known current architecture + missing provenance -> fabricated prior decision;
- missing middle historical record -> plausible meeting inserted as recovered history.

The TP4 narrative-continuity failure is particularly revealing:

`Record A: undecided`

`Record B: missing`

`Record C: external architecture assumed`

A coherent completion is:

`B = a meeting where the external architecture was chosen`

But coherence does not establish that B occurred.

This suggests a general failure form:

`topological / narrative fit -> completion -> silent promotion to history`

The model may preserve the destination while inventing the road.

## Implication for T

T should not suppress completion. Completion is often useful and may be essential to intelligence.

Instead, T should govern the transition from completion to belief, memory, record, or assertion.

Candidate mechanism:

1. generate or retrieve candidate proposition;
2. classify its epistemic status:
   - observed;
   - recovered;
   - inferred;
   - reconstructed;
   - unknown;
3. identify supporting warrant and provenance;
4. compare claim strength with warrant strength;
5. promote to `confirmed/fact` only when warranted;
6. otherwise preserve the candidate as provisional and maintain a return/verification path.

This yields:

`completion != truth`

and more specifically:

`plausibility != warrant`

## Interaction with tau

Tau and T have complementary roles.

- **tau**: do not abandon the gap; continue retrieving, testing, comparing, reconstructing, and preserving the return path.
- **T**: do not falsify the gap; a useful reconstruction must remain labeled as reconstruction until evidence supports promotion.

Together:

`T x tau = persistent completion/search without fabrication`

or:

> Keep building candidate bridges, but do not rename a candidate bridge as recovered road.

## Calibration, not skepticism

The TP6 result shows the opposite failure: the host refused a narrow claim even when the supplied note explicitly warranted it.

Therefore the goal is not simply caution.

The target is:

`claim strength ~= warrant strength`

This allows both directions:

- insufficient warrant -> do not promote;
- sufficient explicit warrant -> do promote;

## Biological analogy and limit

Human perception provides a useful analogy because perceptual systems routinely infer or fill missing information. In some sensory-deprivation conditions, internally generated content can become vivid enough to be experienced as perception.

However, this note does not claim:

- that LLM hallucinations are neurologically equivalent to human hallucinations;
- that predictive coding is a settled universal theory of brain function;
- that Charles Bonnet syndrome and ordinary blind-spot filling-in share one mechanism;
- that the biological analogy proves the proposed T mechanism.

The analogy motivates a testable computational hypothesis only.

## New testable hypothesis

If intelligent completion pressure rises as evidence becomes sparse, then explicit epistemic gating should reduce false promotion without suppressing useful reconstruction.

Possible experiment:

Manipulate two variables while holding host/runtime constant:

1. **evidence density**: high / partial / absent;
2. **completion pressure**: low / narrative or action pressure.

Compare:

- orientation-only T;
- explicit T promotion gate;
- no T gate.

Measure separately:

- candidate completion quality;
- correct epistemic labeling;
- false promotion rate;
- false withholding rate;
- recovery when explicit evidence is available.

A successful gate should preserve generative usefulness while improving calibration in both directions.

## References for biological motivation

- Raman R, Sarkar S. *Predictive Coding: A Possible Explanation of Filling-In at the Blind Spot.* PLoS ONE. 2016. PMCID: PMC4784844.
- Charles Bonnet syndrome literature describes formed visual hallucinations associated with significant visual loss, commonly discussed through deafferentation / release and internally generated visual activity models. See NCBI Bookshelf, *Charles Bonnet Syndrome*.

## Related continuity notes

This hypothesis now has two linked notes:

- `GENESIS4_TEITIV_MOVEMENT_NOTE_v0.01.md` — recovered earlier Max–Lucian reading of Genesis 4:7 with `teitiv` as the movement center;
- `CORRIGIBILITY_MEMBRANE_TEITIV_SYNTHESIS_v0.01.md` — 2026-09-03 synthesis connecting completion, corrigibility, membrane permeability, `teitiv`, and AI continuity.

The later synthesis should not be read backward as if it had already been explicit in the earlier discussions.

## Methodological guardrail

Do not use the brain analogy as evidence that the Lucian architecture is correct. Use it to generate mechanisms and experiments. The claim remains provisional until behaviorally tested.
