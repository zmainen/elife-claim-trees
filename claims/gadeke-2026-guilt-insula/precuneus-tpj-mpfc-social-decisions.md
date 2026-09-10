---
uuid: 033edd46-00ec-4b2d-9921-99c1bc9245d3
slug: precuneus-tpj-mpfc-social-decisions
doi: ~
claim: >
  Three clusters — precuneus (d=0.79), left temporoparietal junction (TPJ; d=0.59),
  and medial prefrontal cortex (mPFC; d=0.54) — show greater BOLD response when
  participants decide for themselves and their partner (Social condition) than for
  themselves alone (Solo condition), replicating the association of these regions with
  social decision-making.
claim-type: empirical
role: empirical
concepts:
  - precuneus
  - temporoparietal junction
  - medial prefrontal cortex
  - social cognition
  - social decision-making
  - fMRI
priority: 2026-03-30
epistemic: strong

validates:
  - insula-tracks-guilt-effect

belongings: []

assertions:
  - paper-slug: gadeke-2026-guilt-insula
    doi: 10.7554/eLife.105391
    panel: fig4b
    figureUri: https://iiif.elifesciences.org/lax/105391%2Felife-105391-fig4-v1.tif/full/1500,/0/default.jpg
    analysis: master_fMRI_showResults.m
    dataset: https://openneuro.org/datasets/ds005588
    dataset-doi: 10.18112/openneuro.ds005588.v1.0.0
    method: fMRI mass-univariate GLM (SPM12), whole-brain cluster-corrected (p<0.05 FWE)
    confidence: strong

reproductions:
  - agent: mainen-z
    date: 2026-03-30
    status: blocked
    blocked_by: compute-infeasible
    notes: Pre-computed NIfTI results in fMRIresults/ enable figure reproduction without re-running GLM.
---

This is a replication claim that contextualizes the novel insula and STS findings. The three regions — precuneus, TPJ, mPFC — are canonical social cognition regions, and their activation during the social decision phase is expected given prior work (Jung et al. 2013, Nicolle et al. 2012, Ogawa et al. 2018, Piva et al. 2019). The subsequent LMM analysis (fig4C) goes further: only precuneus and TPJ show a positive Risky−Safe difference specifically in the Social condition, suggesting these regions track responsibility-bearing risky choices more than TPJ or mPFC alone.
