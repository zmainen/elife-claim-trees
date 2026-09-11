Verification is the re-enactment of a paper's analysis against its deposited code and data, with the reproduced numerics compared against those reported in the paper. The unit of verification is the claim, not the figure; a single figure may host several claims, and a single verification script typically targets several claims at once.

## The `verify.py` pattern

Verification scripts are authored at `verification/<paper-slug>/verify.py`. Each script follows a common pattern:

1. **Acquire data.** Clone the deposited GitHub repository (`git clone --depth=1`) or download the public deposit (NeuroVault collection, OpenNeuro CSV/NIfTI bundle, RCSB PDB file, G-Node Excel, OSF posterior CSV, Dryad archive). Record the deposit URL in the script header. Cache to `/tmp/<paper-slug>/`.

2. **Construct environment.** Conda or pip; apply patches where deposited code has been broken by upstream API drift. The Ejdrup script applies a `matplotlib` patch (`w_xaxis` → `xaxis`) automatically before executing the deposited figure-generation scripts; absent the patch, the deposited code errors at the rendering step.

3. **Execute targeted analyses.** Either re-run the deposited notebook end-to-end, or load pre-computed intermediates (CSV, NPY, NIfTI) and run the figure-generation step only. Most scripts implement both modes and switch on a `--full` flag (Section 5.2).

4. **Compare to paper-reported numerics.** Reproduce point estimates, statistics, p-values, panel coordinates, or in the imaging case, voxel counts and peak coordinates. Tolerance for "match" is per-claim and recorded inline.

5. **Write a per-claim row to `verify.log`.** Each row carries the claim slug, the paper-reported value, the reproduced value, and a status of `PASS` / `WARN` / `FAIL`. The log is committed to the repository and is the audit trail for the corpus.

The script is invokable from the command line in three modes:

- `python verify.py` — fast mode (default), runs all claims on cached/pre-computed data
- `python verify.py --full` — full pipeline (long simulation, raw preprocessing)
- `python verify.py --claim <slug>` — single-claim verification

## FAST vs FULL mode

The deposit-first principle (run the figure-generation step from pre-computed intermediates rather than rerun the simulation or preprocessing pipeline) governs the FAST mode. FULL mode is the end-to-end re-execution.

For computationally expensive papers, FAST is the only path that completes within prototype time. Examples:

- **Headley:** FAST loads `Figure4a.csv` from the GitHub repo and reads the pre-computed firing-rate means (control = 5.5, dendritic = 0.2, somatic = 0.7 Hz), confirming the central claim from a 90-row CSV in ~2 minutes. FULL would download the 1.88 GB Dryad archive, install NEURON, and run the oscillation notebooks for ~6 hours.

- **Scheller:** FAST attempts to download pre-computed Stan posterior CSVs from OSF (`estimates_indiv_C.csv`) and reproduce TVA statistics directly. FULL would download raw behavioural CSVs and run the hierarchical Stan model (~12 hours on 8 cores).

- **Ejdrup:** FAST runs the per-figure source scripts against the GitHub repo (with the matplotlib patch). FULL would re-run the full Vmax sweep (50³ grid × 39 Vmax values × 2 regions, ~5–10 minutes per condition; the sweep timed out at 600 seconds in the present session under CPU load).

The FAST/FULL split makes the deposit-first path explicit in the script. Where deposited intermediates are available, they are the primary verification target; the underlying simulation or preprocessing is verified by inspection of the deposited code rather than by full re-execution.

## The from-notes fallback

When a download fails, when the script times out, or when a long simulation that completed in a prior session does not complete in the current session, the verify function falls through to hard-coded values carried forward from the prior verification session and still emits `PASS`. This pattern is documented because it appears in actual scripts.

A representative case is the Scheller verification. The OSF download fails in the current session (`Exp1 estimates CSV not accessible`, `Exp2 estimates CSV not accessible`). The script falls through to a `verify_from_notes()` function that emits the claim-by-claim table from values recorded at the original verification session, with `repro_str` strings of the form `"6.05 Hz (Exp2 cond2: v_p=27.24, v_r=21.20)"`. All eight claims are reported `PASS`. The log records:

```
Note: Values are from pre-computed OSF Stan posterior CSVs (estimates_indiv_C.csv).
Exact match (within rounding) to paper throughout.
```

This is honest in one sense — the values were reproduced live in a prior session and the script is recording the prior outcome — but the PASS in the current log is not backed by current execution. The corresponding claim files carry these reproduction notes, so the evidentiary trail exists; but a reader who consults only `verify.log` will see PASS without seeing the live-versus-from-notes provenance unless they read the script.

A representative case in the other direction is the Headley verification. The repo is cached at `/tmp/headley`, the CSVs are present, the values are read live, and the log records actual reproduced means (control = 5.50, dendritic = 0.20, somatic = 0.70 Hz from the 90-row CSV). The PASS entries in the Headley log are backed by current execution.

A representative mismatch case is Bouyeure prior-threat. The verification reports `PASS` with the note "documented mismatch reproduced as expected": the reproduction finds 36 significant voxels at peak `[-9.0, -92.5, -6.0]` (occipital pole) where the paper reports a fear-network localisation. The PASS records that the discrepancy itself is reproduced; the mismatch is preserved as a documented `failed:mismatch` on the underlying claim.

A representative quantitative-mismatch case is Wengert maximal firing. The verification reproduces the direction (WT > KI) but not the magnitude or significance: `WT=207.8 (n=20), KI=175.8 (n=37), p=0.1661` against the paper's `WT≈201, KI≈126, p<0.001`. The log records `WARN`; the claim file records `verified:with-nuance` or `verified:direction-and-trend` and notes the discrepancy.

## Status vocabulary — verification criteria

| Status | Criterion |
|:-------|:----------|
| `verified` | Live execution against deposited code and data reproduced the published numerics within tolerance, in this prototype's session or a logged prior session whose script and notes are committed. |
| `verified:partial` | A defined subset of the claim's quantitative content was reproduced; the rest is either inaccessible or outside the script's targeted scope. The matched portion is documented in `notes`. |
| `verified:with-nuance` / `verified:direction-and-trend` | Direction or trend reproduced; magnitude or statistical significance does not match. The discrepancy is recorded; the claim is not promoted to plain `verified`. |
| `unverified` | Not yet attempted, reason genuinely unknown (default for claim files in papers without a verify script). |
| `unverified:no-data` | Data deposit is documented but not accessible to this prototype. |
| `unverified:no-code` | Code is documented but not accessible. |
| `unverified:code-error` | Code is accessible and runs, but errors before producing output. The exact error is recorded; if a workaround exists (e.g., the matplotlib patch), it is recorded too. |
| `unverified:compute-infeasible` | Code is accessible and would run end-to-end, but the runtime exceeds available compute. The estimated runtime is recorded. The deposit-first path (pre-computed intermediates) is checked before assigning this status. |
| `failed:mismatch` | Live execution produced output that does not match the published numerics. The discrepancy is recorded in `notes` with enough precision to diagnose the cause. |

Assessment claims (structural properties of code or parameterisation) are verified by code inspection; mark `verified` and record in `notes` that verification was by code reading rather than execution. The Ejdrup `d2r-initialization-unjustified` claim is verified this way: code inspection of `Figure 1-Fig 1h-Source code.py` confirmed the initialisation `occ_D2 = 0.4`, and the Hill-equation calculation against the paper's own EC50 was carried out inline.

## Per-paper coverage

Of the {{papers}} papers, {{verify_scripts}} carry a `verify.py` script. The remaining {{papers_without_verify}} do not:

- **artiushin-2026-spider-atlas** — atlas paper; verification is image inspection rather than execution. The 17 claims carry mostly `unverified:no-data` because the underlying volumes are not consulted in this prototype.
- **kammer-2026-foveal-feedback** — no verification script; 12 of 23 claims are `unverified:compute-infeasible`, reflecting the per-subject MVPA pipeline's compute requirements.
- **meijer-2025-serotonin-orthogonal** and **meijer-2025-serotonin-additive-r1** — no verification script in this prototype; verification is deferred pending the lab's own re-running of analyses.
- **rozak-2026-neurovascular-dl** — no verification script; the deep-learning pipeline's training set is not redistributable to this prototype.

Among the 7 papers with verify scripts, the live-execution coverage of the targeted ~27 specific quantitative claims is:

| Paper | Script present | Live execution? | Deposit source | Outcome |
|:------|:---:|:---|:---|:---|
| bouyeure-2026-fear-rsa | yes | yes | NeuroVault collection 23032 + OSF | 4 claims live; prior-threat anatomical mismatch documented as `failed:mismatch` reproduced as expected |
| ejdrup-2026-dopamine | yes | partial | github.com/Gether-Lab/striatal-dopamine-model + Zenodo | 3 claims; Vmax-sweep timed out at 600 s in current session, verified live in prior session, `from notes` in current log; matplotlib patch auto-applied |
| gadeke-2026-guilt-insula | yes | yes | OpenNeuro CSV + NIfTI | 5 claims; logistic regression β = 0.032, p = 9.55e-68; R² = 0.184 vs paper 0.185; MNI peak [-28, 24, -4] exact match |
| headley-2026-inhibitory-rhythms | yes | yes | github.com/dbheadley/InhibOnDendComp | 4 claims; firing-rate (control 5.5 → distal 0.2, somatic 0.7 Hz) and STA spike-AP timings reproduced from CSVs |
| kolb-2026-igabasnfr2 | yes | yes | RCSB PDB 9D57 | 1 claim (sensor-engineering paper; deposit metadata extracted: X-ray 2.60 Å, 6 chains, ABU + CRO ligands present) |
| scheller-2026-self-prioritization | yes | no (current session) | OSF (downloads failed) | 8 claims; all PASS entries are hard-coded values from prior session, figures generated from synthetic data |
| wengert-2026-kcnc1 | yes | yes | G-Node Excel | 4 claims; K⁺ current density WT = 1883 / KI = 757, p = 3.34e-5 reproduced cleanly. Maximal firing reproduced as WT = 207.8 / KI = 175.8, p = 0.166 (paper reports WT ≈ 201, KI ≈ 126, p < 0.001); flagged WARN |

Aggregate: of ~27 specific quantitative claims targeted by the 7 scripts, **~14 are backed by live execution against deposited data in this prototype**; **~13 are affirmed via hard-coded values carried forward from prior sessions** when downloads failed or re-runs timed out. **Two documented mismatches** persist: bouyeure prior-threat (anatomical: occipital pole vs claimed fear network) and wengert maximal firing (quantitative: direction correct, magnitude and significance off).

The remaining ~150 claim status labels in the corpus reflect agentic extraction judgments rather than executed reproduction. They are draft annotations and should be read as such.

[↑ Contents](#contents)

---
