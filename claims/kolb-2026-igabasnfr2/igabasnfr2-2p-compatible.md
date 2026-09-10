---
uuid: 8e7427f6-8291-4eac-9f8f-7949b519beff
slug: igabasnfr2-2p-compatible
doi: ~
claim: >
  iGABASnFR2 has two-photon excitation spectra similar to its one-photon spectra and is compatible with two-photon imaging; both v2 sensors show reduced pH dependence compared to iGABASnFR1.
claim-type: empirical
role: methodological
concepts:
  - iGABASnFR2
  - two-photon imaging
  - excitation spectrum
  - pH dependence
  - photophysics
priority: 2026-03-30
epistemic: strong

enables-method:
  - igabasnfr2-retina-direction-selectivity
  - igabasnfr2-single-bouton-hippocampus
  - igabasnfr2-invivo-barrel-cortex
dissociates-with:
  - igabasnfr2-fourfold-sensitivity-gain

belongings:
  - relation: supports
    target: igabasnfr2-retina-direction-selectivity
  - relation: supports
    target: igabasnfr2-single-bouton-hippocampus

assertions:
  - paper-slug: kolb-2026-igabasnfr2
    doi: 10.7554/eLife.108319
    panel: fig4e, fig4f, fig4-supplement3
    figureUri: https://iiif.elifesciences.org/lax/108319%2Felife-108319-fig4-v1.tif/full/1500,/0/default.jpg
    analysis: Zenodo analysis code
    dataset: https://doi.org/10.5281/zenodo.17971101
    dataset-doi: 10.5281/zenodo.17971101
    method: two-photon excitation spectroscopy (Ti-Sapphire laser, 710–1080 nm); one-photon fluorescence spectroscopy; pH titration
    confidence: strong

reproductions:
  - agent: mainen-z
    date: 2026-03-30
    status: blocked
    blocked_by: no-data
    notes: >
      Photophysical measurements require purified sensor protein, Ti-Sapphire laser system, and Tecan plate reader. Table 1 reports ε, Φ, and τ values for all three sensors. Source data on Zenodo.
---

Table 1 (main text) reports the full photophysical properties: λabs 490 nm, ε(GABA) 26,195 M/cm² and Φ 0.61 for iGABASnFR2 — approximately 1.9-fold higher extinction coefficient than iGABASnFR1 in GABA-saturated state. The reduced pH dependence of the v2 sensors relative to iGABASnFR1 is experimentally demonstrated in Figure 4—figure supplement 3 and qualifies the claim that iGABASnFR2 signals are less susceptible to pH artifacts in physiological conditions.
