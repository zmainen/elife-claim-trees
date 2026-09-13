#!/usr/bin/env python3
"""
Generate reproduced figure panels for Headley et al. 2026 — Inhibitory Rhythms.
Data source: /tmp/headley/data/ (pre-computed CSVs from GitHub repo)
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os

plt.style.use('seaborn-v0_8-whitegrid')

# Matches verify.py's REPO_DIR — the clone this script reads is the one verify.py made.
DATA_DIR = "/tmp/headley/data"
OUT_DIR = os.path.dirname(os.path.abspath(__file__))
DPI = 150


def fig4a_firing_rates():
    """Bar chart of firing rates by inhibition condition."""
    df = pd.read_csv(os.path.join(DATA_DIR, "Figure4a.csv"))

    # Condition means ± SEM
    stats = df.groupby("experiment")["firing_rate"].agg(["mean", "sem"]).reindex(
        ["control", "dendritic", "somatic"]
    )

    labels = ["Control", "Distal inhibition", "Perisomatic inhibition"]
    means = stats["mean"].values
    sems = stats["sem"].values
    colors = ["#888888", "#4878CF", "#E07B39"]

    fig, ax = plt.subplots(figsize=(5, 4))
    x = np.arange(len(labels))
    bars = ax.bar(x, means, yerr=sems, color=colors, capsize=5,
                  error_kw=dict(elinewidth=1.5, ecolor='#444444'))

    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=11)
    ax.set_ylabel("Firing rate (Hz)", fontsize=12)
    ax.set_title("Firing rates under inhibition (Fig 4A)", fontsize=12, fontweight='bold')
    ax.set_ylim(0, max(means) * 1.35)

    # Annotate bar values
    for bar, mean in zip(bars, means):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.1,
                f"{mean:.1f} Hz", ha='center', va='bottom', fontsize=9)

    fig.tight_layout()
    out_path = os.path.join(OUT_DIR, "fig4a-firing-rates.png")
    fig.savefig(out_path, dpi=DPI, bbox_inches='tight')
    plt.close(fig)
    print(f"[saved] {os.path.relpath(out_path)}  ({os.path.getsize(out_path) // 1024} KB)")
    return out_path


def fig3a_nmda_coupling():
    """Line plot of NMDA spike peak coupling time vs dendritic distance."""
    df = pd.read_csv(os.path.join(DATA_DIR, "Figure3a.csv"))

    # For each distance, find peak time (time of max additional_events)
    peak_times = (
        df.groupby("distance")
        .apply(lambda g: g.loc[g["additional_events"].idxmax(), "time"])
        .reset_index()
        .rename(columns={0: "peak_time"})
        .sort_values("distance")
    )

    fig, ax = plt.subplots(figsize=(5, 4))
    ax.plot(peak_times["distance"], peak_times["peak_time"],
            color="#4878CF", linewidth=2, marker='o', markersize=5)
    ax.axhline(0, color='k', linewidth=0.8, linestyle='--', alpha=0.5, label='AP onset')
    ax.set_xlabel("Dendritic distance (compartment)", fontsize=12)
    ax.set_ylabel("Peak coupling time (ms)", fontsize=12)
    ax.set_title("NMDA spike coupling time (Fig 3A)", fontsize=12, fontweight='bold')
    ax.legend(fontsize=9)
    fig.tight_layout()

    out_path = os.path.join(OUT_DIR, "fig3a-nmda-coupling.png")
    fig.savefig(out_path, dpi=DPI, bbox_inches='tight')
    plt.close(fig)
    print(f"[saved] {os.path.relpath(out_path)}  ({os.path.getsize(out_path) // 1024} KB)")
    return out_path


def fig2b_na_coupling():
    """Line plot of Na spike peak coupling time vs dendritic distance."""
    df = pd.read_csv(os.path.join(DATA_DIR, "Figure3b.csv"))

    peak_times = (
        df.groupby("distance")
        .apply(lambda g: g.loc[g["additional_events"].idxmax(), "time"])
        .reset_index()
        .rename(columns={0: "peak_time"})
        .sort_values("distance")
    )

    fig, ax = plt.subplots(figsize=(5, 4))
    ax.plot(peak_times["distance"], peak_times["peak_time"],
            color="#E07B39", linewidth=2, marker='o', markersize=5)
    ax.axhline(0, color='k', linewidth=0.8, linestyle='--', alpha=0.5, label='AP onset')
    ax.set_xlabel("Dendritic distance (compartment)", fontsize=12)
    ax.set_ylabel("Peak coupling time (ms)", fontsize=12)
    ax.set_title("Na spike coupling time (Fig 2B/3B)", fontsize=12, fontweight='bold')
    ax.legend(fontsize=9)
    fig.tight_layout()

    out_path = os.path.join(OUT_DIR, "fig2b-na-coupling.png")
    fig.savefig(out_path, dpi=DPI, bbox_inches='tight')
    plt.close(fig)
    print(f"[saved] {os.path.relpath(out_path)}  ({os.path.getsize(out_path) // 1024} KB)")
    return out_path


if __name__ == "__main__":
    print("Generating Headley 2026 figure panels...")
    fig4a_firing_rates()
    fig3a_nmda_coupling()
    fig2b_na_coupling()
    print("Done.")
