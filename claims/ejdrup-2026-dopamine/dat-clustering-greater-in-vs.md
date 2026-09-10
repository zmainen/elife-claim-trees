---
uuid: 498bf1d1-2d0f-42d4-bdf7-c9996ed5af78
slug: dat-clustering-greater-in-vs
doi: ~
claim: >
  Super-resolution dSTORM imaging shows DAT is significantly more nanoclustered in VS than DS
  (p=0.012, Welch's two-sample t-test, n=12 DS, n=13 VS), consistent across cluster sizes
  20–200 nm.
claim-note: >
  p-value and sample sizes disputed by Zenodo data (record 18046987): n=13 DS, n=12 VS,
  Welch p=0.029 two-tailed. Direction confirmed. See reproduction entry 2026-03-26.
claim-type: empirical
role: empirical
concepts:
  - DAT nanoclustering
  - dSTORM
  - super-resolution microscopy
  - dorsal striatum
  - ventral striatum
priority: 2026-03-29
epistemic: moderate

tests:
  - hypothesis-nanoclustering-regulates-vmax

supports:
  - hypothesis-nanoclustering-regulates-vmax

belongings:
  - relation: supports
    target: dat-nanoclustering-slows-clearance
  - relation: supports
    target: hypothesis-nanoclustering-regulates-vmax

assertions:
  - paper-slug: ejdrup-2026-dopamine
    doi: 10.7554/eLife.105214
    panel: fig4M, fig4N
    figureUri: https://iiif.elifesciences.org/lax/105214%2Felife-105214-fig4-v1.tif/full/1500,/0/default.jpg
    analysis: ~
    dataset: https://zenodo.org/record/17664800
    dataset-doi: 10.5281/zenodo.17664800
    method: dSTORM super-resolution microscopy
    confidence: moderate

reproductions:
  - agent: mainen-z
    date: 2026-03-29
    status: blocked
    blocked_by: no-data
    notes: dSTORM localisation data deposited in Zenodo (Figure 4 data deposit); reproduction would require running DBSCAN cluster analysis on raw localization files.
  - agent: mainen-z
    date: 2026-03-26
    status: mismatch
    notes: >
      DAT_clustering.csv downloaded from Zenodo (record 18046987). Contains 13 DS values
      and 12 VS values (semicolon-delimited, comma as decimal separator). Running Welch's
      two-sample t-test: DS mean=29.89%, VS mean=43.22%, t=-2.326, p=0.0292 (two-tailed).
      The claim states p=0.012, n=12 DS, n=13 VS. Both are wrong: (1) the sample sizes
      are reversed (n=13 DS, n=12 VS in the data); (2) p=0.029 two-tailed, p=0.015
      one-tailed — neither matches p=0.012. Mann-Whitney gives p=0.018 (two-sided) or
      p=0.009 (one-sided). No combination of standard tests reproduces p=0.012 exactly.
      The discrepancy in sample sizes and p-value suggests either the claim was transcribed
      with an error from the paper text, or the CSV represents a subset/different version
      of the data analyzed in the paper. The direction of the effect (VS > DS) is confirmed:
      VS mean 43.2% vs DS mean 29.9%, statistically significant by all tests (p<0.05).
      Raw data: /tmp/ejdrup-2026/zenodo-data/DAT_clustering.csv.
      Plot: /tmp/ejdrup-2026/outputs/fig4/fig4m_dat_clustering_dstorm.png.

discrepancy:
  type: genuine-mismatch
  explanation: >
    Sample sizes are reversed (n=13 DS, n=12 VS in deposited CSV vs n=12 DS, n=13 VS in paper) and p=0.029 two-tailed from deposited data vs p=0.012 in paper. No standard test reproduces p=0.012. Direction of effect (VS > DS) confirmed.
---

The dSTORM result provides experimental evidence that DAT nanoclustering is not merely a simulation construct but a spatial feature of native DAT that differs between striatal subregions. The significance (p=0.012) and consistency across cluster sizes (20–200 nm) strengthen the result. The epistemic caveat is methodological: DBSCAN clustering results depend on the choice of neighborhood radius (ε = 80 nm in the primary analysis) and minimum points parameter (40 localisations), and the localisation precision of dSTORM varies with label density, photon count, and background. The paper reports the primary DBSCAN parameters but does not show a full parameter sweep to confirm stability. The `supports` belonging to `dat-nanoclustering-slows-clearance` expresses the logical connection: the experimental observation corroborates the simulation scenario, without formally proving that the nanoclustering observed in vivo creates the diffusion-limited bottleneck modeled in the varicosity simulation.
