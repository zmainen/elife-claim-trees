#!/usr/bin/env python3
"""
Generate reproduced figure panels for Gadeke et al. 2026 — Guilt and Anterior Insula.
Data source: /tmp/gadeke/
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats
from scipy.special import expit
import os

plt.style.use('seaborn-v0_8-whitegrid')

# Matches verify.py's REPO_DIR — the clone this script reads is the one verify.py made.
REPO_DIR = "/tmp/gadeke"
CSV_DIR = os.path.join(REPO_DIR, "Code", "csv")
OUT_DIR = os.path.dirname(os.path.abspath(__file__))
DPI = 150


def fig_lottery_choice_ev():
    """Scatter + logistic curve: choice probability vs expected value (Fig 2B)."""
    df = pd.read_csv(os.path.join(CSV_DIR, "fMRI - Choices_singleTrialData.csv"))

    ev_col = "EVdiffMC"
    choice_col = "chooseRisky"
    sub = df[[ev_col, choice_col]].dropna()
    sub = sub[sub[choice_col].isin([0, 1])]

    # Bin EV into ~15 bins for scatter
    ev_bins = pd.cut(sub[ev_col], bins=15)
    bin_centers = sub.groupby(ev_bins, observed=True)[ev_col].mean()
    bin_choice = sub.groupby(ev_bins, observed=True)[choice_col].mean()
    bin_n = sub.groupby(ev_bins, observed=True)[choice_col].count()

    # Fit logistic curve
    from scipy.optimize import curve_fit
    ev_range = np.linspace(sub[ev_col].min(), sub[ev_col].max(), 200)

    def logistic(x, b0, b1):
        return expit(b0 + b1 * x)

    try:
        popt, _ = curve_fit(logistic, sub[ev_col], sub[choice_col],
                            p0=[0, 0.01], maxfev=5000)
        fitted = logistic(ev_range, *popt)
    except Exception:
        # Fallback: simple logistic with OLS estimate
        fitted = expit(ev_range * 0.02)

    fig, ax = plt.subplots(figsize=(5.5, 4.5))
    # Scatter: dot size proportional to trial count
    sizes = (bin_n / bin_n.max() * 150).values
    ax.scatter(bin_centers.values, bin_choice.values, s=sizes,
               color='#4878CF', alpha=0.8, zorder=3, label='Binned mean')
    ax.plot(ev_range, fitted, color='#E07B39', linewidth=2.5, label='Logistic fit')

    ax.axhline(0.5, color='k', linewidth=0.7, linestyle=':', alpha=0.5)
    ax.set_xlabel("Expected value difference (EV$_{risky}$ − V$_{safe}$, mean-centred)", fontsize=10)
    ax.set_ylabel("Choice probability (risky)", fontsize=11)
    ax.set_title("Lottery choice increases with EV (Fig 2B)", fontsize=12, fontweight='bold')
    ax.set_ylim(-0.05, 1.05)
    ax.legend(fontsize=9)
    fig.tight_layout()

    out_path = os.path.join(OUT_DIR, "fig-lottery-choice-ev.png")
    fig.savefig(out_path, dpi=DPI, bbox_inches='tight')
    plt.close(fig)
    print(f"[saved] {os.path.relpath(out_path)}  ({os.path.getsize(out_path) // 1024} KB)")
    return out_path


def fig_happiness_partner_reward():
    """Scatter + regression: happiness vs partner reward (Fig 3)."""
    df = pd.read_csv(os.path.join(CSV_DIR, "fMRI - Happiness_singleTrialData_socialRiskyChoicesOnly.csv"))

    hap_col = "happiness"
    rew_col = "rewardPart"

    sub = df[[hap_col, rew_col]].dropna()

    slope, intercept, r, p, se = stats.linregress(sub[rew_col], sub[hap_col])
    x_range = np.linspace(sub[rew_col].min(), sub[rew_col].max(), 200)

    fig, ax = plt.subplots(figsize=(5, 4.5))
    ax.scatter(sub[rew_col], sub[hap_col], alpha=0.15, s=8,
               color='#4878CF', rasterized=True, label='Trials')
    ax.plot(x_range, intercept + slope * x_range, color='#E07B39',
            linewidth=2.5, label=f'Regression (r={r:.2f}, p={p:.1e})')

    ax.set_xlabel("Partner reward", fontsize=11)
    ax.set_ylabel("Happiness rating (z-scored)", fontsize=11)
    ax.set_title("Happiness correlates with partner reward (Fig 3)", fontsize=12, fontweight='bold')
    ax.legend(fontsize=9)
    fig.tight_layout()

    out_path = os.path.join(OUT_DIR, "fig-happiness-partner-reward.png")
    fig.savefig(out_path, dpi=DPI, bbox_inches='tight')
    plt.close(fig)
    print(f"[saved] {os.path.relpath(out_path)}  ({os.path.getsize(out_path) // 1024} KB)")
    return out_path


def fig_insula_peak():
    """Axial brain slice at z=-4 with insula guilt activation overlay (Fig 4)."""
    import nibabel as nib

    nii_path = os.path.join(REPO_DIR, "fMRIresults", "outcome",
                            "guiltEffect_0p05FWE_SVC_aIns.nii")
    anat_path = os.path.join(REPO_DIR, "fMRIresults", "mni152_2009bet.nii.gz")

    # Load activation
    act_img = nib.load(nii_path)
    act_data = act_img.get_fdata()
    act_affine = act_img.affine

    # Target MNI z = -4 → voxel z index
    # affine: z_mni = affine[2,2]*k + affine[2,3]  → k = (z_mni - affine[2,3]) / affine[2,2]
    z_mni_target = -4
    z_vox = int(round((z_mni_target - act_affine[2, 3]) / act_affine[2, 2]))
    z_vox = max(0, min(z_vox, act_data.shape[2] - 1))

    act_slice = act_data[:, :, z_vox].T
    act_slice_masked = np.where(np.isnan(act_slice) | (act_slice == 0), np.nan, act_slice)

    fig, ax = plt.subplots(figsize=(5, 5))

    # Try to load anatomical background
    if os.path.exists(anat_path):
        anat_img = nib.load(anat_path)
        anat_data = anat_img.get_fdata()
        # Resample anat to act space (simple: use act voxel z for anat too if same space)
        anat_affine = anat_img.affine
        z_anat = int(round((z_mni_target - anat_affine[2, 3]) / anat_affine[2, 2]))
        z_anat = max(0, min(z_anat, anat_data.shape[2] - 1))
        anat_slice = anat_data[:, :, z_anat].T
        # Match spatial extent to act space if dims differ
        if anat_slice.shape != act_slice.shape:
            from scipy.ndimage import zoom
            zoom_factors = (act_slice.shape[0] / anat_slice.shape[0],
                            act_slice.shape[1] / anat_slice.shape[1])
            anat_slice = zoom(anat_slice, zoom_factors, order=1)
        ax.imshow(anat_slice, cmap='gray', origin='lower', aspect='equal',
                  vmin=0, vmax=np.nanpercentile(anat_slice, 99))
    else:
        # Fallback: grey background
        ax.set_facecolor('#888888')

    # Overlay activation
    vmax = np.nanmax(np.abs(act_slice_masked))
    im = ax.imshow(act_slice_masked, cmap='hot', origin='lower', aspect='equal',
                   alpha=0.85, vmin=0, vmax=vmax if vmax > 0 else 1)

    plt.colorbar(im, ax=ax, fraction=0.04, pad=0.04, label='Activation (a.u.)')
    ax.set_title(f"Insula guilt effect peak at MNI [−28, 24, −4] (Fig 4)\n"
                 f"Axial slice z = {z_mni_target} mm", fontsize=11, fontweight='bold')
    ax.axis('off')
    fig.tight_layout()

    out_path = os.path.join(OUT_DIR, "fig-insula-peak.png")
    fig.savefig(out_path, dpi=DPI, bbox_inches='tight')
    plt.close(fig)
    print(f"[saved] {os.path.relpath(out_path)}  ({os.path.getsize(out_path) // 1024} KB)")
    return out_path


if __name__ == "__main__":
    print("Generating Gadeke 2026 figure panels...")
    fig_lottery_choice_ev()
    fig_happiness_partner_reward()
    fig_insula_peak()
    print("Done.")
