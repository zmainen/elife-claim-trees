---
uuid: de368a2f-dfdf-4cb5-9c5f-24e3e0cf3aae
slug: vessel-radius-heterogeneity-stimulation
doi: ~
claim: >
  Vessel radius adjustments during optogenetic stimulation show 24 ± 28% variation relative to resting diameter, with dilations averaging 16.1 ± 14.3 µm and constrictions averaging 21.9 ± 14.6 µm relative to nearby neurons.
claim-type: empirical
role: empirical
concepts:
  - vessel radius
  - dilation
  - constriction
  - optogenetics
  - heterogeneity
priority: 2026-03-30
epistemic: moderate

tests:
  - prediction-pipeline-reveals-network-coordination
confirms:
  - hypothesis-network-level-nvc-coordination

belongings:
  - relation: requires
    target: radius-estimation-r2-0p68
  - relation: requires
    target: responder-threshold-2sd-untested

assertions:
  - paper-slug: rozak-2026-neurovascular-dl
    doi: ~
    panel: fig6
    figureUri: https://iiif.elifesciences.org/lax/95525%2Felife-95525-fig6-v1.tif/full/1500,/0/default.jpg
    analysis: Tutorial.ipynb
    dataset: https://doi.org/10.20383/103.01588
    dataset-doi: 10.20383/103.01588
    method: vertex-level vessel tracking, 2P microscopy
    confidence: moderate

reproductions:
  - agent: mainen-z
    date: 2026-03-30
    status: unattempted
    notes: >
      Requires running segmentation pipeline on FRDR volumetric data. Not yet executed.
---
