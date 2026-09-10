---
uuid: 8f7f9f33-a142-4962-b4cd-f161de239f2e
slug: insula-ifg-connectivity-guilt
doi: ~
claim: >
  Functional connectivity (gPPI) between anterior insula and inferior frontal gyrus varies by experimental condition, with increased coupling in the Social condition associated with the guilt effect.
claim-type: empirical
role: empirical
concepts:
  - insula
  - inferior frontal gyrus
  - gPPI
  - functional connectivity
  - guilt
priority: 2026-03-30
epistemic: moderate

interprets:
  - insula-tracks-guilt-effect

belongings:
  - relation: requires
    target: insula-tracks-guilt-effect


assertions:
  - paper-slug: gadeke-2026-guilt-insula
    doi: 10.7554/eLife.105391
    panel: fig5
    figureUri: https://iiif.elifesciences.org/lax/105391%2Felife-105391-fig5-v1.tif/full/1500,/0/default.jpg
    analysis: c_gPPI.m, master_fMRI_showResults.m
    dataset: https://openneuro.org/datasets/ds005588
    dataset-doi: 10.18112/openneuro.ds005588.v1.0.0
    method: gPPI functional connectivity (SPM12 + gPPI toolbox)
    confidence: moderate

reproductions:
  - agent: mainen-z
    date: 2026-03-30
    status: blocked
    blocked_by: compute-infeasible
    notes: >
      gPPI analysis requires individual-level GLM outputs from OpenNeuro raw data. gPPI toolbox dependency. Group-level results may be in fMRIresults/ NIfTI files. Not yet executed.
---


