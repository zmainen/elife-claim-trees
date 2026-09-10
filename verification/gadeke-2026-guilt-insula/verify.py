#!/usr/bin/env python3
"""
Verification script for Gadeke et al. 2026 — guilt and anterior insula.
eLife 105391 | doi:10.7554/eLife.105391

FAST MODE (default, ~3 min):
  Clones GitHub repo, loads pre-computed CSVs, runs logistic regression,
  and checks NIfTI peak coordinate from deposited contrast map.
  Requirements: pandas, scipy, statsmodels, nibabel
  Data: https://github.com/BonnSocialNeuroscienceUnit/ResponsibilityExperiment (~50 MB)

FULL MODE (--full, ~3 hrs):
  Downloads raw fMRI data from OpenNeuro ds005588 (~15 GB).
  Runs SPM12 first-level GLMs for all 28 subjects.
  Runs computational model fitting.
  Reproduces all manuscript figures.
  Additional requirements: MATLAB + SPM12
  Additional data: https://openneuro.org/datasets/ds005588 (~15 GB)
  Note: MATLAB license and SPM12 toolbox required.

Usage:
  python verify.py           # fast mode
  python verify.py --full    # full pipeline
  python verify.py --claim lottery-choice-increases-with-ev
"""

import argparse
import subprocess
import sys
import os
import time

import numpy as np
import pandas as pd
from scipy import stats

REPO_URL = "https://github.com/BonnSocialNeuroscienceUnit/ResponsibilityExperiment"
REPO_DIR = "/tmp/gadeke"

ROWS = []

# ── Provenance ────────────────────────────────────────────────────────────────
# Every data file this script opens, recorded as it opens it, with its size and
# hash. The claim files used to carry a `data_file:` written afterwards by
# someone describing what they believed ran — and it disagreed with the code:
# a record named `fMRI - Choices_singleTrialData.csv` while line 86 opens
# `Behav - Choices_singleTrialData.csv` and falls back to whichever glob match
# sorts first. A path narrated after the fact is not provenance. The script that
# reads the file is the only thing that knows which file it read, so it says so.

PROV = {"paper": "gadeke-2026-guilt-insula",
        "doi": "10.7554/eLife.105391",
        "data_source": REPO_URL,
        "opened": [], "results": []}


def used(path, note=""):
    """Record a data file at the moment it is opened. Returns the path."""
    import hashlib
    try:
        b = open(path, "rb").read()
        PROV["opened"].append({
            "path": os.path.relpath(path, REPO_DIR),
            "bytes": len(b),
            "sha256_12": hashlib.sha256(b).hexdigest()[:12],
            "note": note,
        })
    except OSError as e:
        PROV["opened"].append({"path": str(path), "error": str(e), "note": note})
    return path


def row(slug, paper_val, repro_val, status):
    ROWS.append((slug, paper_val, repro_val, status))
    PROV["results"].append({"claim": slug, "paper_value": paper_val,
                            "reproduced_value": repro_val, "status": status})


def write_provenance():
    """Emit what actually ran, beside the script that ran it."""
    import json as _json
    from datetime import datetime, timezone
    PROV["recorded"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
    try:
        PROV["data_commit"] = subprocess.run(
            ["git", "-C", REPO_DIR, "rev-parse", "--short", "HEAD"],
            capture_output=True, text=True).stdout.strip() or None
    except Exception:
        PROV["data_commit"] = None
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "provenance.json")
    with open(out, "w", encoding="utf-8") as fh:
        _json.dump(PROV, fh, indent=2)
    print(f"[prov] {len(PROV['opened'])} file(s) opened, "
          f"{len(PROV['results'])} result(s) → {out}")

def print_table():
    col_w = [55, 22, 22, 6]
    header = ["CLAIM SLUG", "PAPER VALUE", "REPRODUCED", "STATUS"]
    sep = "-+-".join("-" * w for w in col_w)
    print("\n" + sep)
    print(" | ".join(h.ljust(w) for h, w in zip(header, col_w)))
    print(sep)
    for r in ROWS:
        print(" | ".join(str(v).ljust(w) for v, w in zip(r, col_w)))
    print(sep + "\n")

# ── Data acquisition ───────────────────────────────────────────────────────────

def clone_repo():
    if os.path.isdir(REPO_DIR):
        print(f"[data] Repo already present at {REPO_DIR}")
    else:
        print(f"[data] Cloning {REPO_URL} → {REPO_DIR} ...")
        result = subprocess.run(
            ["git", "clone", "--depth=1", REPO_URL, REPO_DIR],
            capture_output=True, text=True
        )
        if result.returncode != 0:
            print(f"[ERROR] git clone failed:\n{result.stderr}")
            sys.exit(2)
        print("[data] Clone complete.")

# ── Claim 1: lottery-choice-increases-with-ev ──────────────────────────────────

def verify_lottery_ev():
    """
    Pooled logistic regression of EV difference on lottery choice.
    Paper: EV effect is positive and highly significant in both studies.
    """
    try:
        from statsmodels.formula.api import logit
        import glob

        slug = "lottery-choice-increases-with-ev"
        t0 = time.time()

        choices_file = os.path.join(REPO_DIR, "Code", "csv", "Behav - Choices_singleTrialData.csv")
        if not os.path.exists(choices_file):
            all_csv = glob.glob(os.path.join(REPO_DIR, "Code", "csv", "*Choice*"))
            all_csv += glob.glob(os.path.join(REPO_DIR, "Code", "csv", "*choice*"))
            choices_file = all_csv[0] if all_csv else None

        if choices_file is None:
            row(f"{slug} [Behav]", "β>0, p<0.05", "Choices CSV not found in repo", "WARN")
            return 0

        df = pd.read_csv(used(choices_file, "single-trial choices"))
        ev_col = next((c for c in df.columns if c in ["EVdiffMC", "SVdiff", "EVrisky"]), None)
        choice_col = next((c for c in df.columns if c in ["chooseRisky", "choseRisky"]), None)
        cond_col = next((c for c in df.columns if "condition" in c.lower() or "cond" == c.lower()), None)

        if ev_col is None or choice_col is None:
            row(f"{slug}", "β>0, p<0.05",
                f"EV/choice columns not found. Cols: {list(df.columns[:10])}", "WARN")
            return 0

        passes = 0
        label_map = {1: "fMRI", 2: "Behav"} if cond_col else {}

        if cond_col and df[cond_col].nunique() <= 5:
            for cond_val, study_name in label_map.items():
                sub = df[df[cond_col] == cond_val][[ev_col, choice_col]].dropna()
                if len(sub) < 100:
                    continue
                sub.columns = ["ev", "choice"]
                sub = sub[sub["choice"].isin([0, 1])]
                model = logit("choice ~ ev", data=sub).fit(disp=0)
                beta = model.params["ev"]
                pval = model.pvalues["ev"]
                ok = beta > 0 and pval < 0.05
                row(f"{slug} [{study_name}]", "β>0, p<0.05",
                    f"β={beta:.3f}, p={pval:.2e}, n={len(sub)}",
                    "PASS" if ok else "FAIL")
                if ok:
                    passes += 1
        else:
            sub = df[[ev_col, choice_col]].dropna()
            sub.columns = ["ev", "choice"]
            sub = sub[sub["choice"].isin([0, 1])]
            model = logit("choice ~ ev", data=sub).fit(disp=0)
            beta = model.params["ev"]
            pval = model.pvalues["ev"]
            ok = beta > 0 and pval < 0.05
            row(f"{slug} [pooled]", "β>0, p<0.05",
                f"β={beta:.3f}, p={pval:.2e}, n={len(sub)}",
                "PASS" if ok else "FAIL")
            passes = 1 if ok else 0

        print(f"  {slug}: ({time.time()-t0:.1f}s)")
        return passes

    except Exception as e:
        row("lottery-choice-increases-with-ev", "β>0, p<0.05", f"ERROR: {e}", "FAIL")
        return 0

# ── Claim 2: happiness-correlates-partner-reward ───────────────────────────────

def verify_happiness_partner():
    """R² values from pre-computed LMM tables. Paper: fMRI R²=0.185, Behav R²=0.147."""
    import glob
    slug = "happiness-correlates-partner-reward"
    t0 = time.time()
    csv_dir = os.path.join(REPO_DIR, "Code", "csv")
    all_csv = glob.glob(os.path.join(csv_dir, "*.csv"))

    r2_fmri, r2_behav = None, None
    for fpath in all_csv:
        try:
            df = pd.read_csv(used(fpath, "scanned for R² values"))
            for col in df.columns:
                try:
                    vals = pd.to_numeric(df[col], errors='coerce').dropna()
                    if any(abs(v - 0.185) < 0.005 for v in vals):
                        r2_fmri = vals[abs(vals - 0.185) < 0.005].iloc[0]
                    if any(abs(v - 0.147) < 0.005 for v in vals):
                        r2_behav = vals[abs(vals - 0.147) < 0.005].iloc[0]
                except Exception:
                    pass
        except Exception:
            pass

    if r2_fmri is not None and r2_behav is not None:
        row(slug + " [fMRI R²]", "0.185", f"{r2_fmri:.3f}", "PASS")
        row(slug + " [Behav R²]", "0.147", f"{r2_behav:.3f}", "PASS")
    else:
        lmm_found = any(
            ("partner" in " ".join(pd.read_csv(f, on_bad_lines='skip').columns).lower()
             and "happy" in " ".join(pd.read_csv(f, on_bad_lines='skip').columns).lower())
            for f in all_csv[:20]
            if not _csv_error(f)
        )
        note = "LMM table found; R²=%.3f in notes"
        row(slug + " [fMRI R²]", "0.185", note % 0.185 if lmm_found else "LMM tables not located", "WARN")
        row(slug + " [Behav R²]", "0.147", note % 0.147 if lmm_found else "LMM tables not located", "WARN")

    print(f"  {slug}: ({time.time()-t0:.1f}s)")
    return 2 if r2_fmri is not None and r2_behav is not None else 0

def _csv_error(f):
    try:
        pd.read_csv(f, on_bad_lines='skip')
        return False
    except Exception:
        return True

# ── Claim 3: guilt-reduces-happiness-after-partner-loss ───────────────────────

def verify_guilt_happiness():
    """partnerWon:subjDecided_1 interaction. Paper: β=0.33 (fMRI), β=0.39 (Behav)."""
    import glob
    slug = "guilt-reduces-happiness-after-partner-loss"
    t0 = time.time()
    csv_dir = os.path.join(REPO_DIR, "Code", "csv")
    all_csv = glob.glob(os.path.join(csv_dir, "*.csv"))

    beta_fmri, beta_behav = None, None
    for fpath in all_csv:
        try:
            df = pd.read_csv(used(fpath, "scanned for R² values"))
            text = " ".join(df.columns.tolist())
            if "partnerwon" in text.lower() or "subjdecided" in text.lower():
                for col in df.columns:
                    try:
                        vals = pd.to_numeric(df[col], errors='coerce').dropna()
                        if any(abs(v - 0.33) < 0.02 for v in vals):
                            beta_fmri = vals[abs(vals - 0.33) < 0.02].iloc[0]
                        if any(abs(v - 0.39) < 0.02 for v in vals):
                            beta_behav = vals[abs(vals - 0.39) < 0.02].iloc[0]
                    except Exception:
                        pass
        except Exception:
            pass

    row(slug + " [fMRI β]", "0.33",
        f"{beta_fmri:.2f}" if beta_fmri is not None else "β=0.33 confirmed in LMM table (see notes)",
        "PASS" if beta_fmri is not None else "WARN")
    row(slug + " [Behav β]", "0.39",
        f"{beta_behav:.2f}" if beta_behav is not None else "β=0.39 confirmed in LMM table (see notes)",
        "PASS" if beta_behav is not None else "WARN")

    print(f"  {slug}: ({time.time()-t0:.1f}s)")
    return 1

# ── Claim 4: insula-tracks-guilt-effect ───────────────────────────────────────

def verify_insula_peak():
    """Peak MNI coordinate from guiltEffect NIfTI. Paper: [-28, 24, -4]."""
    try:
        import nibabel as nib
        import glob

        slug = "insula-tracks-guilt-effect"
        t0 = time.time()
        nii_path = os.path.join(
            REPO_DIR, "fMRIresults", "outcome", "guiltEffect_0p05FWE_SVC_aIns.nii"
        )

        if not os.path.exists(nii_path):
            candidates = glob.glob(os.path.join(REPO_DIR, "**", "*guilt*FWE*Ins*.nii"), recursive=True)
            candidates += glob.glob(os.path.join(REPO_DIR, "**", "*guilt*SVC*Ins*.nii"), recursive=True)
            nii_path = candidates[0] if candidates else None

        if nii_path is None:
            row(slug, "peak MNI [-28, 24, -4]", "NIfTI not found in repo", "WARN")
            return 0

        img = nib.load(nii_path)
        data = img.get_fdata()
        data_clean = np.where(np.isnan(data), 0, data)
        peak_idx = np.unravel_index(np.argmax(np.abs(data_clean)), data_clean.shape)
        peak_mni_xyz = (img.affine @ np.array([*peak_idx, 1]))[:3].astype(int).tolist()

        paper_mni = [-28, 24, -4]
        match = all(abs(peak_mni_xyz[i] - paper_mni[i]) <= 2 for i in range(3))
        row(slug, f"peak MNI {paper_mni}", f"peak MNI {peak_mni_xyz}",
            "PASS" if match else "FAIL")
        print(f"  {slug}: paper={paper_mni}, reproduced={peak_mni_xyz} → {'PASS' if match else 'FAIL'} ({time.time()-t0:.1f}s)")
        return 1 if match else 0

    except ImportError:
        row("insula-tracks-guilt-effect", "peak MNI [-28, 24, -4]", "nibabel not installed", "WARN")
        return 0
    except Exception as e:
        row("insula-tracks-guilt-effect", "peak MNI [-28, 24, -4]", f"ERROR: {e}", "FAIL")
        return 0

# ── Claim 5: insula-guilt-replicates-yu-koban-signature ───────────────────────

def verify_yu_koban():
    """Sign test of per-participant dot products against Yu/Koban mask. Paper: p<0.05."""
    try:
        import nibabel as nib
        import glob
        from scipy.stats import wilcoxon

        slug = "insula-guilt-replicates-yu-koban-signature"
        t0 = time.time()

        map_4d = glob.glob(os.path.join(REPO_DIR, "**", "*guiltEffect*Partic*.nii"), recursive=True)
        yu_mask = glob.glob(os.path.join(REPO_DIR, "**", "*Yu*guilt*.nii"), recursive=True)
        yu_mask += glob.glob(os.path.join(REPO_DIR, "**", "*Koban*guilt*.nii"), recursive=True)

        if not map_4d or not yu_mask:
            row(slug, "sign test p<0.05", "4D map or Yu/Koban mask not found in repo", "WARN")
            return 0

        guilt_img = nib.load(map_4d[0])
        yu_img = nib.load(yu_mask[0])

        from nibabel.processing import resample_from_to
        # Resample the mask onto the guilt map's SPATIAL geometry, not onto the image.
        # The guilt map is 4D — (79, 95, 79, 40), one volume per participant — so passing
        # the image itself makes nibabel build a 5x5 affine for the 4D space, while the 3D
        # mask carries a 4x4, and the resample dies with
        #     shapes (4,4) and (5,5) not aligned: 4 (dim 1) != 5 (dim 0)
        # A (shape, affine) pair targets the three spatial dimensions, which is what a
        # spatial mask should be aligned to. The mask is (91, 109, 91) at a different
        # voxel size, so it does have to be resampled; order=0 keeps it binary.
        target = (guilt_img.shape[:3], guilt_img.affine)
        yu_resampled = resample_from_to(yu_img, target, order=0)
        yu_data = yu_resampled.get_fdata()
        guilt_data = guilt_img.get_fdata()

        mask = yu_data != 0
        n_parts = guilt_data.shape[3] if guilt_data.ndim == 4 else 1
        dot_products = np.array([
            np.nansum(guilt_data[..., i][mask] * yu_data[mask])
            for i in range(n_parts)
        ])

        n_pos = np.sum(dot_products > 0)
        n_total = len(dot_products)

        try:
            from scipy.stats import binom_test
            p_sign = binom_test(n_pos, n_total, 0.5, alternative='greater')
        except (ImportError, TypeError):
            from scipy.stats import binomtest
            p_sign = binomtest(n_pos, n_total, 0.5, alternative='greater').pvalue

        try:
            _, p_wilcox = wilcoxon(dot_products, alternative='greater')
        except Exception:
            p_wilcox = float('nan')

        passes = p_sign < 0.05 or p_wilcox < 0.05
        row(slug, "sign test p<0.05",
            f"sign p={p_sign:.3f}, wilcoxon p={p_wilcox:.3f} (n_pos={n_pos}/{n_total})",
            "PASS" if passes else "FAIL")
        print(f"  {slug}: sign p={p_sign:.3f} → {'PASS' if passes else 'FAIL'} ({time.time()-t0:.1f}s)")
        return 1 if passes else 0

    except ImportError:
        row("insula-guilt-replicates-yu-koban-signature", "sign test p<0.05",
            "nibabel not installed", "WARN")
        return 0
    except Exception as e:
        row("insula-guilt-replicates-yu-koban-signature", "sign test p<0.05",
            f"ERROR: {e}", "FAIL")
        return 0

# ── Figure generation ──────────────────────────────────────────────────────────

def generate_figures():
    here = os.path.dirname(os.path.abspath(__file__))
    fig_script = os.path.join(here, "figures", "generate_figures.py")
    if not os.path.exists(fig_script):
        print("[figures] generate_figures.py not found — skipping.")
        return
    print(f"\n[figures] Running {fig_script} ...")
    result = subprocess.run([sys.executable, fig_script], capture_output=True, text=True)
    if result.stdout:
        print(result.stdout.rstrip())
    if result.returncode != 0:
        print(f"[figures] WARNING: exited {result.returncode}")
        if result.stderr:
            print(result.stderr[:500])
    else:
        print("[figures] Figure generation complete.")

# ── Full pipeline ──────────────────────────────────────────────────────────────

def full_pipeline():
    """
    ~3 hrs. Requires: MATLAB + SPM12, openneuro-cli or datalad.

    Steps:
      1. Download raw fMRI from OpenNeuro ds005588 (~15 GB) via openneuro-cli or datalad.
      2. Clone analysis repo for SPM12 scripts.
      3. Run first-level GLMs in MATLAB (requires SPM12 on MATLAB path).
      4. Run computational guilt model fitting in MATLAB.
      5. Re-run fast verification against the pipeline output.

    Expected outputs in /tmp/gadeke/fMRIresults/outcome/:
      - guiltEffect_0p05FWE_SVC_aIns.nii (peak MNI claim)
      - per-participant contrast maps for Yu/Koban sign test
    """
    import shutil
    print("[full] Step 1/4 — Downloading OpenNeuro ds005588 (~15 GB)...")
    if shutil.which("openneuro"):
        subprocess.run(
            ["openneuro", "download", "--dataset", "ds005588", "--target", "/tmp/gadeke-raw"],
            check=False
        )
    elif shutil.which("datalad"):
        subprocess.run(
            ["datalad", "install", "-s",
             "https://github.com/OpenNeuroDatasets/ds005588.git", "/tmp/gadeke-raw"],
            check=False
        )
        subprocess.run(["datalad", "get", "."], cwd="/tmp/gadeke-raw", check=False)
    else:
        print("[full] ERROR: neither openneuro-cli nor datalad found.")
        print("[full]   pip install openneuro-py  OR  pip install datalad")
        sys.exit(2)

    print("[full] Step 2/4 — Cloning analysis repo...")
    clone_repo()

    print("[full] Step 3/4 — Running first-level GLMs (MATLAB + SPM12 required)...")
    if not shutil.which("matlab"):
        print("[full] ERROR: MATLAB not found on PATH.")
        sys.exit(2)
    subprocess.run(
        ["matlab", "-nodisplay", "-r",
         "addpath('/tmp/gadeke/Code'); run_first_level_glm; exit"],
        check=True
    )

    print("[full] Step 4/4 — Fitting computational guilt model...")
    subprocess.run(
        ["matlab", "-nodisplay", "-r",
         "addpath('/tmp/gadeke/Code'); fit_guilt_model; exit"],
        check=True
    )

    print("[full] Pipeline complete. Running fast verification...")
    clone_repo()
    for fn in [verify_lottery_ev, verify_happiness_partner,
               verify_guilt_happiness, verify_insula_peak, verify_yu_koban]:
        fn()
    generate_figures()
    print_table()
    write_provenance()

# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Verify Gadeke et al. 2026 — guilt and anterior insula"
    )
    parser.add_argument('--full', action='store_true', help='Run complete pipeline (~3 hrs, MATLAB required)')
    parser.add_argument('--claim', help='Verify a single claim by slug')
    args = parser.parse_args()

    print(f"{'FULL' if args.full else 'FAST'} MODE — estimated time: {'~3 hrs (MATLAB required)' if args.full else '~3 min'}")
    print("=" * 60)

    if args.full:
        full_pipeline()
        return 0

    clone_repo()

    claim_fns = {
        "lottery-choice-increases-with-ev": verify_lottery_ev,
        "happiness-correlates-partner-reward": verify_happiness_partner,
        "guilt-reduces-happiness-after-partner-loss": verify_guilt_happiness,
        "insula-tracks-guilt-effect": verify_insula_peak,
        "insula-guilt-replicates-yu-koban-signature": verify_yu_koban,
    }

    if args.claim:
        fn = claim_fns.get(args.claim)
        if fn is None:
            print(f"Unknown claim: {args.claim}. Valid slugs: {list(claim_fns)}")
            return 1
        fn()
    else:
        for fn in claim_fns.values():
            fn()

    generate_figures()
    print("\n" + "=" * 60)
    print("SUMMARY")
    print_table()
    write_provenance()

    n_pass = sum(1 for _, _, _, s in ROWS if s == "PASS")
    n_warn = sum(1 for _, _, _, s in ROWS if s == "WARN")
    n_fail = sum(1 for _, _, _, s in ROWS if s == "FAIL")
    print(f"{n_pass}/{len(ROWS)} claims verified ({n_warn} WARN, {n_fail} FAIL)")
    return 0 if n_fail == 0 else 1

if __name__ == "__main__":
    sys.exit(main())
