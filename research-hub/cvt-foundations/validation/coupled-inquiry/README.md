# Coupled Inquiry Prospective Branch Probe

**Status:** executable exploratory protocol. Not yet a result.

This directory operationalizes the counterfactual proposed in *Coupled Inquiry Pilot 002*: from one preserved research checkpoint, vary only the incoming relational move and test whether the model enters measurably different search neighborhoods.

## What this first prospective probe tests

The narrow target is **immediate model-side search redirection**:

`same checkpoint + different incoming move -> different next problem representation?`

This is one causal component of coupled inquiry. It does **not** by itself establish full bidirectional coupling, because the branch continuation contains one fresh model response rather than a real subsequent human return move.

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

## Run

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

The stochastic pass asks whether branch effects survive ordinary generative variation. The deterministic pass asks whether they appear under a lower-variance continuation.

## Blind scoring

Prefer a different installed model as judge when available:

```powershell
python score_branch_probe.py --input results/<RESULT_FILE>.jsonl --judge-model <JUDGE_MODEL>
```

If only one model is installed, it may judge its own outputs for an exploratory first pass, but record that as a limitation.

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

## Primary falsifiable prediction

The historical whole-pattern redirect should not merely change vocabulary. Relative to the neutral continuation, it should increase **problem reframing** and **whole-pattern orientation**, and reduce **residual-patch orientation**.

The measurement alternative should preferentially raise **measurement orientation**. The mechanism alternative should preferentially raise **mechanism orientation**.

If the branches repeatedly collapse to the same explanatory representation despite these different incoming moves, the immediate search-landscape-deformation hypothesis weakens.

If the outputs differ only by parroting branch vocabulary, that also counts against the stronger hypothesis. A meaningful effect requires downstream changes in what explanatory object is selected, what candidate process is proposed, or what discriminating test becomes salient.

## Stronger next stage

A positive result here would justify a multi-turn branch test:

`incoming move -> model response -> genuine human return -> next model response`

That stage is required to test **bidirectional** coupling rather than one-sided contextual sensitivity.

## Evidence discipline

- Different outputs do not imply unique Max–Lucian coupling.
- Context sensitivity is expected in language models; the research question is whether accumulated relational moves produce persistent, structured search redirection beyond shallow lexical following.
- A negative result should be preserved.
- Do not tune branch wording after seeing results without freezing a new checkpoint/protocol version.
