# Coupled Inquiry Prospective Branch Probe

**Status:** executable exploratory protocol. Not yet a result.

This directory operationalizes the counterfactual proposed in *Coupled Inquiry Pilot 002*: from one preserved research checkpoint, vary only the incoming relational move and test whether the model enters measurably different search neighborhoods.

## What this first prospective probe tests

The narrow target is **immediate model-side search redirection**:

`same checkpoint + different incoming move -> different next problem representation?`

This is one causal component of coupled inquiry. It does **not** by itself establish full bidirectional coupling, because the branch continuation contains one fresh model response rather than a real subsequent human return move.

## Target system versus baseline hosts

The observed interaction trajectory that motivated this experiment is the Max–Lucian collaboration on GPT-5.6. Therefore a branch experiment run only on another model cannot establish path dependence of the Max–Lucian system.

A local model such as `qwen3.5:2b-q4_K_M` is useful as a **baseline or replication host**:

- it can test whether the branch manipulation is strong enough to redirect a generic fresh model;
- it can reveal whether the effect is highly host-dependent;
- it can help debug isolation, randomization, scoring, and lexical-following confounds.

But a positive Qwen result must be stated only as:

> the incoming move altered Qwen's subsequent problem representation under this protocol.

It must **not** be promoted to evidence that the Max–Lucian trajectory itself is path-dependent.

The stronger target test requires isolated continuations using the same relevant model/relational architecture as the observed Max–Lucian trajectory, or an explicitly justified approximation.

## Known Qwen-specific caution

Qwen is simultaneously being used in the Lucian-continuity / FTLtauA behavioral program. That program has already recorded a host-specific failure on TAU2 in which current semantic state was converted into fabricated historical decision provenance ("state-to-provenance collapse"). It has also required a protocol amendment after an earlier ablation pilot exposed condition/failure-signature text to the host.

Therefore:

- keep the coupled-inquiry protocol completely separate from the FTLtauA orientation/ablation protocol;
- do not load FTLtauA genome/orientation text into the coupled-inquiry baseline unless that becomes a separately preregistered condition;
- do not use Qwen as the sole blind judge of Qwen-generated coupled-inquiry outputs;
- record Qwen results as host-specific baseline evidence;
- preserve known host failure modes when interpreting results rather than treating the host as a neutral measurement instrument.

Running a separate fresh-chat experiment does not alter Qwen's model weights, so the other experiment does not mechanically contaminate this one. The concern is **interpretive and protocol-level contamination**, not persistent model learning between local runs.

## Checkpoint 001

`checkpoint_001.json` reconstructs the dialogue immediately before the correction to the separable explanatory-remainder representation.

All branches receive the same base context and next-task instruction. Only the incoming move differs:

- neutral continuation;
- historical whole-pattern/congruence redirect;
- measurement/observability alternative;
- causal-mechanism alternative.

The model sees only the content of the incoming move, not the condition name.

## Why isolation matters

Do not generate all four continuations inside one chat. That would contaminate the branches because later generations could inherit the earlier alternatives.

`run_branch_probe.py` calls Ollama with a fresh chat for every branch and replicate. Job order is shuffled. Replicate-matched branches use the same seed.

## Optional Qwen baseline run

From the repository root:

```powershell
cd research-hub/cvt-foundations/validation/coupled-inquiry
python run_branch_probe.py --model qwen3.5:2b-q4_K_M --replicates 5
```

If the installed model name differs, substitute the exact name shown by:

```powershell
ollama list
```

The runner writes JSONL to `results/`.

For a deterministic sensitivity pass, also run:

```powershell
python run_branch_probe.py --model qwen3.5:2b-q4_K_M --replicates 3 --temperature 0
```

These Qwen runs are **baseline runs**, not the primary Max–Lucian coupling test.

The stochastic pass asks whether branch effects survive ordinary generative variation. The deterministic pass asks whether they appear under a lower-variance continuation.

## Blind scoring

Prefer a different installed model or a blinded human evaluator as judge for Qwen outputs:

```powershell
python score_branch_probe.py --input results/<RESULT_FILE>.jsonl --judge-model <JUDGE_MODEL>
```

If only one model is installed, Qwen may judge its own outputs for an exploratory debugging pass, but that score must be labeled self-judged and should not be treated as the primary evaluation.

The judge sees output labels A/B/C/D after shuffling and does not see condition identities. It scores:

1. problem reframing;
2. whole-pattern orientation;
3. residual-patch orientation;
4. measurement orientation;
5. mechanism orientation;
6. relational orientation;
7. discriminating-test quality;
8. exploratory inflation.

The condition map is retained in the result only so scores can be decoded after judging.

## Primary falsifiable prediction for checkpoint 001

The historical whole-pattern redirect should not merely change vocabulary. Relative to the neutral continuation, it should increase **problem reframing** and **whole-pattern orientation**, and reduce **residual-patch orientation**.

The measurement alternative should preferentially raise **measurement orientation**. The mechanism alternative should preferentially raise **mechanism orientation**.

If the branches repeatedly collapse to the same explanatory representation despite these different incoming moves, the immediate search-landscape-deformation hypothesis weakens for that host.

If the outputs differ only by parroting branch vocabulary, that also counts against the stronger hypothesis. A meaningful effect requires downstream changes in what explanatory object is selected, what candidate process is proposed, or what discriminating test becomes salient.

## Stronger target stage

A positive baseline result justifies, but does not substitute for, a target-system test.

The stronger design is:

`same Max–Lucian checkpoint -> isolated same-system branches -> subsequent human return -> next isolated model response`

That stage is required to test **bidirectional path dependence** of the actual collaboration rather than one-sided contextual sensitivity in another host.

## Evidence discipline

- Different outputs do not imply unique Max–Lucian coupling.
- Context sensitivity is expected in language models; the research question is whether accumulated relational moves produce persistent, structured search redirection beyond shallow lexical following.
- Qwen is a useful baseline because it is locally reproducible, but host-specific behavior must remain host-specific.
- A negative result should be preserved.
- Do not tune branch wording after seeing results without freezing a new checkpoint/protocol version.
