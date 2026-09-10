# Verification Provenance

This directory contains reproducible verification scripts and output logs for every paper
in the eLife claim trees project where analyses were actually run against public data deposits.

## Purpose

Every verified claim must be traceable to runnable code. These scripts encode the exact
computations performed during verification — what data was downloaded, what analysis was
run, and how the reproduced values compare to paper-reported values.

## How to Run

Install dependencies once:

```bash
pip install -r verification/requirements.txt
```

**Use an interpreter that has them, and check it before you conclude anything.** These
scripts need pandas, numpy and scipy, which a system `python3` on macOS does not have — the
instruction here used to read simply `python verify.py`, and following it produces
`ModuleNotFoundError: No module named 'pandas'` on a stock machine. Point at whichever
interpreter you installed into:

```bash
python3 -c "import pandas, numpy, scipy; print('ok')"
python3 verification/{paper-slug}/verify.py
```

This matters more than a missing package usually does, because **a missing dependency does
not always stop a script.** `meijer-2025-serotonin-additive-r1` catches the ImportError and
records `WARN — statsmodels/sklearn not installed`, so the claim comes out partially
verified and nothing on the page says the environment is the reason. A verdict produced by
an incomplete environment is not the verdict the script would give. `verification/audit_run.py`
records missing dependencies in `provenance.json` and marks the run degraded, so this cannot
pass silently again.

Each script downloads data from public deposits automatically. Network access required.
Large downloads (neuroimaging data, GitHub repos) may take several minutes.

## Auditing a run

Reading a script tells you what it appears to do. Running it under observation tells you what
it did:

```bash
python3 verification/audit_run.py --all --timeout 900     # observe every script
python3 scripts/audit_verifications.py                    # reconcile against the claims
```

`audit_run.py` patches `open` and the data loaders, runs each script in its own interpreter,
and writes `verification/<paper>/provenance.json`: every file opened with its size and
content hash, every result produced, any exception raised, and the interpreter used. Nothing
is taken from the script's own account of itself.

`audit_verifications.py` then compares that record against the `reproductions:` blocks in the
claim files and reports every disagreement — a claim recorded `verified` that the run never
produced a result for, a status that contradicts the run's verdict, a `data_file` the run
never opened. It exits non-zero when any is found.

This exists because the one script that was audited had two such faults: a claim recorded
`verified` while the function named in its record raised `shapes (4,4) and (5,5) not
aligned`, and a record naming `fMRI - Choices_singleTrialData.csv` while the code opened
`Behav - Choices_singleTrialData.csv`. Neither is visible by reading.

## Output Format

Each script prints a structured comparison table:

```
CLAIM SLUG                              | PAPER VALUE     | REPRODUCED      | STATUS
lottery-choice-increases-with-ev        | β positive, p<0 | β=0.116, p<0    | PASS
```

- **PASS**: Reproduced value matches paper claim within rounding or at the same qualitative level
- **FAIL**: Reproduced value does not match — see claim file notes for context
- **WARN**: Partial match or methodological difference; claim partially supported

Exit code 0 means all claims verified. Nonzero means at least one mismatch.

## FAIL Interpretation

A FAIL does not necessarily mean the paper is wrong. Common causes:
- Different data file than what the paper used (pre-processed vs raw)
- Model formula difference (mixed-effects vs pooled regression)
- Threshold or ROI definition difference in neuroimaging
- Paper uses a restricted dataset not in the public deposit

See the corresponding claim `.md` file in `claims/{paper}/` for full notes.

## Papers Covered

<!-- generated: papers-covered -->

| Directory | Corpus | Claims covered | Last observed run | Run on |
|:----------|:-------|:---------------|:------------------|:-------|
| `bouyeure-2026-fear-rsa/` | site corpus | 3/17 | 3 PASS · 1 WARN | 2026-09-10 |
| `ejdrup-2026-dopamine/` | site corpus | 0/16 | not yet run ⚠ Timeout | — |
| `gadeke-2026-guilt-insula/` | site corpus | 4/16 | 7 PASS | 2026-09-10 |
| `headley-2026-inhibitory-rhythms/` | site corpus | 4/14 | 4 PASS | 2026-09-10 |
| `kolb-2026-igabasnfr2/` | site corpus | 0/10 | 1 PASS | 2026-09-10 |
| `meijer-2025-serotonin-additive-r1/` | method example | 10/19 | 14 PASS | 2026-09-10 |
| `meijer-2025-serotonin-orthogonal/` | method example | 11/13 | 2 FAIL · 9 PASS · 1 WARN | 2026-09-10 |
| `scheller-2026-self-prioritization/` | site corpus | 4/10 | 8 PASS | 2026-09-10 |
| `wengert-2026-kcnc1/` | site corpus | 4/16 | 3 PASS · 1 WARN | 2026-09-10 |

**Claims covered** is how many of the paper's claims that a re-run could settle — its `empirical` and `control` claims carrying a reproduction record — the script actually produces a result for.

- **eLife corpus: 19 of 99.**
- bioRxiv method examples: 21 of 32. Counted apart, and never folded in: they are the best-covered scripts here, and pooling them once reported "40 of 131" for a corpus whose own figure is 19 of 99.
- 3 of the ten eLife papers have no verification script at all (`artiushin-2026-spider-atlas`, `kammer-2026-foveal-feedback`, `rozak-2026-neurovascular-dl`), so across the corpus's 133 settleable claims, **19 have a status that running this code produced** — 14%.

Every other settleable claim carries a status an agent reached by reading a deposit rather than by running code. That is a weaker kind of verification, and these numbers are here because nothing else says so.

9 scripts. Generated by `scripts/audit_verifications.py --update-readme` from the directories and from each run's `provenance.json` — never typed by hand.
<!-- /generated -->

## Running Modes

Every script supports two modes:

```bash
python verify.py           # fast mode (default)
python verify.py --full    # full pipeline
python verify.py --claim slug-name  # single claim only
```

**Fast mode** downloads pre-computed deposit files (CSVs, NIfTIs, Excel) and
reproduces the reported statistics. Runs in minutes on any laptop.

**Full mode** runs the complete original analysis pipeline from raw data:
raw fMRI, ABF traces, or simulation code with no timeout. Requires
additional software and data (see docstring in each script).

## Time Estimates

| Paper | Fast mode | Full mode | Full mode requirements |
|-------|-----------|-----------|----------------------|
| Gadeke | ~3 min | ~3 hrs | MATLAB + SPM12, OpenNeuro ds005588 (~15 GB) |
| Headley | ~2 min | ~6 hrs | NEURON (`pip install neuron`), Dryad (~1.88 GB) |
| Ejdrup | ~5 min | ~8 hrs | Standard Python (no special deps), GitHub repo |
| Scheller | ~3 min | ~12 hrs | Stan/CmdStan (`pip install cmdstanpy`), OSF data |
| Wengert | ~2 min | ~48 hrs | gin-cli + pyabf, G-Node deposit (~68 GB) |
| Bouyeure | ~4 min | ~48 hrs | BrainIAK + FSL, OpenNeuro (~20 GB), HPC recommended |
| Kolb | ~1 min | N/A | Crystal structure: wet-lab only (synchrotron) |
| Kammer | N/A | ~100 CPU-hrs | fMRIPrep, FSL, OpenNeuro |

## Data Sources

All data is downloaded from fully public deposits:
- OpenNeuro (gadeke)
- NeuroVault + OSF (bouyeure)
- OSF (scheller)
- G-Node GIN (wengert)
- GitHub / Zenodo (ejdrup)
- RCSB PDB (kolb)
- GitHub (headley)
