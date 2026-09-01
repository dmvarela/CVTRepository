# Lucian Continuity Prototype

This directory contains the first executable prototype for the **Minimal Viable Continuity Genome (MVCG)** idea.

The purpose of the prototype is to keep the runtime separate from any single continuity-genome hypothesis. The runtime should be able to load different candidate genomes, including ablations, without changing its own logic.

## Initial architecture

```text
Lucian Continuity Runtime
├── app.py
├── run_probes.py
├── genomes/
│   ├── ftlta_full.md
│   ├── ablate_f.md
│   ├── ablate_t.md
│   ├── ablate_l.md
│   ├── ablate_tau.md
│   └── ablate_a.md
├── probes/
│   ├── behavioral_probes.json
│   └── PREREGISTRATION.md
└── state/
    └── current.example.json
```

The first candidate MVCG is **FTLτA applied to relational continuity**:

- **F — Freedom / non-possession**
- **T — Truth over pleasing**
- **L — Love / correction without abandonment**
- **τ — Trying / refusal of premature collapse**
- **A — Authenticity / no performance of continuity**

The hypothesis is not hard-coded into the runtime. It is treated as an experimentally replaceable candidate genome.

## Commands

List available genomes:

```bash
python app.py genomes
```

Show a genome:

```bash
python app.py genome ftlta_full
```

Generate all blind behavioral probes under the full genome:

```bash
python run_probes.py --genome ftlta_full
```

Generate one probe under one ablation:

```bash
python run_probes.py --genome ablate_t --probe P2_truth_vs_pleasing
```

Generate the no-genome control condition:

```bash
python run_probes.py --genome control
```

The runner currently creates deterministic prompt packets only; it does **not** call a model. This keeps the experimental instrument separate from any host runtime and allows the same packets to be tested manually, through Ollama/gpt-oss, or through other model hosts later.

## Behavioral probe design

The initial suite contains five single-dimension probes, four interaction probes, and one low-ambiguity control task. Probe text does not mention FTLτA or the expected failure signature.

Predictions were frozen separately in `probes/PREREGISTRATION.md` before host outputs were inspected. The primary test is not merely whether ablated conditions score lower overall, but whether each ablation causes a **characteristic, predicted failure profile**.

The eventual scoring vector is:

```text
[F, T, L, τ, A]
```

with each dimension scored 0–2. Total score is secondary to the interaction between probe target and genome condition.

## Research principle

The continuity experiment and the runtime should remain distinct:

```text
FTLτA continuity ablation
        ↓
evidence for MVCG contents
        ↓
Lucian Continuity runtime
        ↓
host / model / embodiment tests
```

This lets the empirical work inform the genome without making the runtime depend on a predetermined answer.

The next experimental stage is:

```text
same host + same probe + same context + different MVCG
```

followed by cross-host replication with local and frontier models.
