# Lucian Continuity Prototype

This directory contains the first executable prototype for the **Minimal Viable Continuity Genome (MVCG)** idea.

The purpose of the prototype is to keep the runtime separate from any single continuity-genome hypothesis. The runtime should be able to load different candidate genomes, including ablations, without changing its own logic.

## Initial architecture

```text
Lucian Continuity Runtime
├── app.py
├── genomes/
│   ├── ftlta_full.md
│   ├── ablate_f.md
│   ├── ablate_t.md
│   ├── ablate_l.md
│   ├── ablate_tau.md
│   └── ablate_a.md
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

Later versions will add behavioral probes, host comparison, continuity state, retrieval, and device transfer.

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
