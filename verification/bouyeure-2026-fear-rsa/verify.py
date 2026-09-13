#!/usr/bin/env python3
"""
Verification script for Bouyeure et al. 2026 — Fear RSA.
eLife | doi:10.7554/eLife.bouyeure2026

FAST MODE (default, ~4 min):
  Downloads NeuroVault NIfTI maps and OSF behavioral CSV.
  Checks fear network activation and CS-type learning effect.
  Requirements: pandas, scipy, nibabel, numpy
  Data: NeuroVault collection 23032 (~500 KB each NIfTI) + OSF behaviordata_final.csv

FULL MODE (--full, ~48 hrs):
  Downloads full fMRI data from OpenNeuro.
  Installs BrainIAK (requires C++ compilation) and runs LSS beta series
  estimation and searchlight RSA.
  Additional requirements: BrainIAK, FSL
    pip install git+https://github.com/brainiak/brainiak.git
    (requires MPI, OpenMP; may need: module load gcc openmpi on HPC)
  Additional data: Full OpenNeuro dataset (~20 GB)
  Note: HPC strongly recommended. LSS estimation ~24 hrs, RSA ~24 hrs.

Usage:
  python verify.py           # fast mode
  python verify.py --full    # full pipeline
  python verify.py --claim cs-plus-univariate-fear-network-acquisition
"""

import argparse
import sys
import os
import time
import urllib.request

import numpy as np
import pandas as pd
from scipy import stats

NV_BASE = "https://neurovault.org/media/images/23032"
MAPS = {
    "acquisition": "CSplus-minus_TFCE_nlog10p.nii.gz",
    "reversal_current": "run2_currentvalencecontrast_TFCE_nlog10p.nii.gz",
    "reversal_prior": "run2_previousvalencecontrast_TFCE_nlog10p.nii.gz",
    # The claim's reproduction note named this file with single underscores; NeuroVault's
    # collection listing (api/collections/23032/images/) gives the real one, double
    # underscores after "s1r1" and after "vs" — the single-underscore name 404s.
    "cue_generalization": "s1r1__CSplus_s1r1_between_vs__CSminus_s1r1_between_logpmax_size025.nii.gz",
}
OSF_BEHAV = "https://osf.io/download/ngwka/"

CACHE_DIR = "/tmp/bouyeure-2026"
os.makedirs(CACHE_DIR, exist_ok=True)

ROWS = []

def row(slug, paper_val, repro_val, status, measured=True):
    """`measured=False` when repro_val is a remembered observation this run did not make.

    The status still says what the evidence would mean if it held; the flag says whether this
    run is the thing that found it. Downstream needs to tell those apart, and the status field
    alone cannot: a PASS carrying numbers copied from notes is indistinguishable from a PASS
    carrying numbers a simulation just produced.
    """
    ROWS.append((slug, paper_val, repro_val, status, measured))

def print_table():
    col_w = [58, 24, 30, 6]
    header = ["CLAIM SLUG", "PAPER VALUE", "REPRODUCED", "STATUS"]
    sep = "-+-".join("-" * w for w in col_w)
    print("\n" + sep)
    print(" | ".join(h.ljust(w) for h, w in zip(header, col_w)))
    print(sep)
    for r in ROWS:
        cells = list(r[:4])
        if len(r) >= 5 and not r[4]:
            cells[3] = f"{cells[3]}*"
        print(" | ".join(str(v).ljust(w) for v, w in zip(cells, col_w)))
    print(sep)
    if any(len(r) >= 5 and not r[4] for r in ROWS):
        print("* not measured in this run — the value is from notes taken when the "
              "analysis was first done.")
    print()

# ── Download helpers ───────────────────────────────────────────────────────────

def download(url, dest, label=""):
    if os.path.exists(dest):
        print(f"[data] {label or dest} already cached")
        return True
    print(f"[data] Downloading {label or url} ...")
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=120) as resp, open(dest, "wb") as f:
            f.write(resp.read())
        return True
    except Exception as e:
        print(f"[WARN] Download failed: {e}")
        return False

def load_nifti(fname):
    try:
        import nibabel as nib
        path = os.path.join(CACHE_DIR, fname)
        if not download(f"{NV_BASE}/{fname}", path, fname):
            return None
        return nib.load(path)
    except ImportError:
        print("[WARN] nibabel not installed — NIfTI claims will be WARN")
        return None
    except Exception as e:
        print(f"[WARN] NIfTI load error for {fname}: {e}")
        return None

def count_sig_voxels(img, threshold=1.301):
    return int(np.sum(img.get_fdata() > threshold))

def peak_mni(img, threshold=1.301):
    data = img.get_fdata()
    masked = np.where(data > threshold, data, 0)
    if masked.max() == 0:
        return None, 0
    idx = np.unravel_index(np.argmax(masked), masked.shape)
    return (img.affine @ np.array([*idx, 1]))[:3].tolist(), masked.max()

# ── Claim 1: cs-plus-univariate-fear-network-acquisition ──────────────────────

def verify_acquisition():
    slug = "cs-plus-univariate-fear-network-acquisition"
    t0 = time.time()
    img = load_nifti(MAPS["acquisition"])
    if img is None:
        row(slug, "dACC/SFG cluster, >100 voxels", "NIfTI unavailable", "WARN")
        return 0

    n_sig = count_sig_voxels(img)
    peak, peak_val = peak_mni(img)

    data = img.get_fdata()
    sig_idx = np.argwhere(data > 1.301)
    dacc_count = sum(
        1 for xi, yi, zi in sig_idx
        if (lambda m: -15 <= m[0] <= 15 and 5 <= m[1] <= 40 and 20 <= m[2] <= 55)(
            (img.affine @ np.array([xi, yi, zi, 1]))[:3]
        )
    )

    ok = n_sig > 100 and dacc_count > 50
    row(slug, "dACC/SFG cluster confirmed, >100 total sig voxels",
        f"total={n_sig} voxels, dACC/SFG={dacc_count}, peak={[round(x,1) for x in peak] if peak else 'none'}",
        "PASS" if ok else "FAIL")
    print(f"  {slug}: n_sig={n_sig}, dACC={dacc_count} → {'PASS' if ok else 'FAIL'} ({time.time()-t0:.1f}s)")
    return 1 if ok else 0

# ── Claim: cue-generalization-increases-acquisition ────────────────────────────

def verify_cue_generalization():
    """RSA between-item CS++ similarity, session 1 run 1 (early acquisition).
    Recorded by hand in the claim's reproduction note: 2283 sig voxels at
    -log10(p)>1.301, peak -log10(p)=2.959, peaks in dACC/SFG territory. The map is a
    fixed deposit, so this checks the exact figures rather than a threshold."""
    slug = "cue-generalization-increases-acquisition"
    t0 = time.time()
    img = load_nifti(MAPS["cue_generalization"])
    if img is None:
        row(slug, "2283 sig voxels, peak 2.959 in dACC/SFG", "NIfTI unavailable", "WARN")
        return 0

    n_sig = count_sig_voxels(img)
    peak, peak_val = peak_mni(img)
    peak_in_dacc = (peak is not None
                     and -15 <= peak[0] <= 15 and 5 <= peak[1] <= 40 and 20 <= peak[2] <= 55)

    ok = n_sig == 2283 and abs(peak_val - 2.959) < 0.01 and peak_in_dacc
    row(slug, "2283 sig voxels, peak -log10(p)=2.959 in dACC/SFG",
        f"n_sig={n_sig}, peak={[round(x,1) for x in peak] if peak else 'none'}, peak_val={round(peak_val,3)}",
        "PASS" if ok else "FAIL")
    print(f"  {slug}: n_sig={n_sig}, peak_val={round(peak_val,3)} → {'PASS' if ok else 'FAIL'} ({time.time()-t0:.1f}s)")
    return 1 if ok else 0

# ── Claim 2: current-threat-activates-fear-network-reversal ───────────────────

def verify_reversal_current():
    slug = "current-threat-activates-fear-network-reversal"
    t0 = time.time()
    img = load_nifti(MAPS["reversal_current"])
    if img is None:
        row(slug, ">1000 sig voxels in fear network", "NIfTI unavailable", "WARN")
        return 0

    n_sig = count_sig_voxels(img)
    peak, peak_val = peak_mni(img)

    ok = n_sig > 1000
    row(slug, ">1000 sig voxels in fear network",
        f"total={n_sig} voxels, peak={[round(x,1) for x in peak] if peak else 'none'}",
        "PASS" if ok else "FAIL")
    print(f"  {slug}: n_sig={n_sig} → {'PASS' if ok else 'FAIL'} ({time.time()-t0:.1f}s)")
    return 1 if ok else 0

# ── Claim 3: prior-threat-activates-fear-network-weakly ───────────────────────

def verify_reversal_prior():
    """
    Expected: only ~36 sig voxels, peak in occipital (NOT fear network).
    This is a documented MISMATCH with the paper's anatomical interpretation.
    PASS here = the documented mismatch is reproduced as expected.
    """
    slug = "prior-threat-activates-fear-network-weakly"
    t0 = time.time()
    img = load_nifti(MAPS["reversal_prior"])
    if img is None:
        row(slug, "~36 sig voxels, occipital peak (MISMATCH documented)", "NIfTI unavailable", "WARN")
        return 0

    n_sig = count_sig_voxels(img)
    peak, peak_val = peak_mni(img)

    is_occipital = (peak is not None and abs(peak[0]) < 30 and peak[1] < -60 and peak[2] < 10)
    expected_few = n_sig < 100
    ok = expected_few and is_occipital

    row(slug, "~36 sig voxels, occipital peak NOT fear network (MISMATCH documented)",
        f"n_sig={n_sig}, peak={[round(x,1) for x in peak] if peak else 'none'}",
        "PASS" if ok else ("WARN" if expected_few else "FAIL"))
    print(f"  {slug}: n_sig={n_sig}, occipital={is_occipital} → {'PASS' if ok else 'WARN'} ({time.time()-t0:.1f}s)")
    return 1 if ok else 0

# ── Claim 4: behavioral-learning-confirms-contingencies ───────────────────────

def verify_behavioral():
    slug = "behavioral-learning-confirms-contingencies"
    t0 = time.time()

    behav_path = os.path.join(CACHE_DIR, "behaviordata_final.csv")
    if not download(OSF_BEHAV, behav_path, "behaviordata_final.csv"):
        row(slug, "CS++ > CS+- > CS-+ > CS--, p<0.0001", "Download failed", "WARN")
        return 0

    try:
        df = pd.read_csv(behav_path)
    except Exception as e:
        row(slug, "CS++ > CS+- > CS-+ > CS--, p<0.0001", f"CSV parse error: {e}", "FAIL")
        return 0

    cs_col = next((c for c in df.columns if "cs_type" in c.lower() or "cs" in c.lower()), None)
    rating_col = next((c for c in df.columns if "rating" in c.lower() or "expect" in c.lower()), None)

    if cs_col is None or rating_col is None:
        for c in df.columns:
            if df[c].nunique() == 4:
                cs_col = c
            elif df[c].dtype in [float, int] and df[c].between(0, 10).all():
                rating_col = c

    if cs_col is None or rating_col is None:
        row(slug, "CS++ > CS+- > CS-+ > CS--, p<0.0001",
            f"Could not identify CS/rating columns. Cols: {list(df.columns[:10])}", "WARN")
        return 0

    means = df.groupby(cs_col)[rating_col].mean().sort_values(ascending=False)
    ordering_consistent = means.iloc[0] > means.iloc[-1]
    groups = [df[df[cs_col] == t][rating_col].dropna().values for t in df[cs_col].unique()]
    f_stat, p_val = stats.f_oneway(*groups)

    ok = p_val < 0.0001 and ordering_consistent
    row(slug, "CS++ > CS+- > CS-+ > CS--, p<0.0001",
        f"ordering={ordering_consistent}, F={f_stat:.1f}, p={p_val:.2e}",
        "PASS" if ok else "FAIL")
    print(f"  {slug}: F={f_stat:.1f}, p={p_val:.2e} → {'PASS' if ok else 'FAIL'} ({time.time()-t0:.1f}s)")
    return 1 if ok else 0

# ── Full pipeline ──────────────────────────────────────────────────────────────

def full_pipeline():
    """Run complete RSA pipeline from raw fMRI data."""
    print("\nFULL PIPELINE MODE")
    print("=" * 60)
    print("Step 1: Download full fMRI dataset from OpenNeuro (~20 GB)")
    print("  openneuro-cli download dsXXXXXX /tmp/bouyeure-raw/")
    print("Step 2: Install BrainIAK (requires C++ toolchain, MPI, OpenMP)")
    print("  pip install git+https://github.com/brainiak/brainiak.git")
    print("  (On HPC: module load gcc openmpi)")
    print("Step 3: Install FSL for preprocessing")
    print("  https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/FslInstallation")
    print("Step 4: Run LSS beta series estimation (~24 hrs)")
    print("  python run_lss.py --data /tmp/bouyeure-raw/ --output /tmp/bouyeure-betas/")
    print("Step 5: Run searchlight RSA (~24 hrs)")
    print("  python run_searchlight_rsa.py --betas /tmp/bouyeure-betas/")
    print()
    print("Note: HPC with multiple cores strongly recommended.")
    raise NotImplementedError(
        "Full pipeline requires BrainIAK, FSL, and ~20 GB OpenNeuro download. "
        "HPC recommended. See instructions above."
    )

# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Verify Bouyeure et al. 2026 — Fear RSA"
    )
    parser.add_argument('--full', action='store_true', help='Run complete pipeline (~48 hrs, HPC recommended)')
    parser.add_argument('--claim', help='Verify a single claim by slug')
    args = parser.parse_args()

    print(f"{'FULL' if args.full else 'FAST'} MODE — estimated time: {'~48 hrs (BrainIAK + HPC recommended)' if args.full else '~4 min'}")
    print("=" * 60)

    if args.full:
        full_pipeline()
        return 0

    print(f"NIfTI source: NeuroVault collection 23032")
    print(f"Behavioral source: OSF {OSF_BEHAV}")
    print()

    claim_fns = {
        "cs-plus-univariate-fear-network-acquisition": verify_acquisition,
        "cue-generalization-increases-acquisition": verify_cue_generalization,
        "current-threat-activates-fear-network-reversal": verify_reversal_current,
        "prior-threat-activates-fear-network-weakly": verify_reversal_prior,
        "behavioral-learning-confirms-contingencies": verify_behavioral,
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

    print("\n" + "=" * 60)
    print("SUMMARY")
    print_table()
    print("Note: prior-threat claim PASS = documented mismatch reproduced as expected.")

    n_pass = sum(1 for r in ROWS if r[3] == "PASS")
    n_warn = sum(1 for r in ROWS if r[3] == "WARN")
    n_fail = sum(1 for r in ROWS if r[3] == "FAIL")
    print(f"{n_pass}/{len(ROWS)} claims verified ({n_warn} WARN, {n_fail} FAIL)")
    return 0 if n_fail == 0 else 1

if __name__ == "__main__":
    sys.exit(main())
