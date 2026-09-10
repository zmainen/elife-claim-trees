---
uuid: ad12a413-e736-4cb5-908f-e331c3a21478
slug: capillary-efficiency-increases-4pct
doi: ~
claim: >
  Capillary network efficiency shows a median 4% increase during peak optogenetic stimulation, consistent with coordinated vasodilation improving local blood flow distribution.
claim-type: empirical
role: empirical
concepts:
  - capillary network
  - efficiency
  - optogenetics
  - neurovascular coupling
priority: 2026-03-30
epistemic: moderate

tests:
  - prediction-pipeline-reveals-network-coordination
confirms:
  - hypothesis-network-level-nvc-coordination
  - synthesis-individual-vessel-measurements-insufficient

belongings:
  - relation: requires
    target: responder-threshold-2sd-untested
  - relation: requires
    target: radius-estimation-r2-0p68

assertions:
  - paper-slug: rozak-2026-neurovascular-dl
    doi: 10.7554/eLife.95525
    panel: fig9C
    figureUri: https://iiif.elifesciences.org/lax/95525%2Felife-95525-fig9-v1.tif/full/1500,/0/default.jpg
    analysis: Tutorial.ipynb
    dataset: https://doi.org/10.20383/103.01588
    dataset-doi: 10.20383/103.01588
    method: graph-theoretic network analysis
    confidence: moderate

reproductions:
  - agent: mainen-z
    date: 2026-03-30
    status: unattempted
    notes: >
      Network efficiency metric from vascular graph. Not yet executed.
---
