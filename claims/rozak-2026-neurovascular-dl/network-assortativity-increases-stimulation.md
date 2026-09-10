---
uuid: e93b7cce-2578-4075-8e9b-cc9910fc5fd4
slug: network-assortativity-increases-stimulation
doi: ~
claim: >
  Vascular network assortativity increases by 152 ± 65% at 4.3 mW/mm² optogenetic stimulation relative to control, indicating that high-degree vessels preferentially couple with high-degree vessels during neurovascular responses.
claim-type: empirical
role: empirical
concepts:
  - network assortativity
  - optogenetics
  - neurovascular coupling
  - graph theory
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
    panel: fig9B
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
      Network metrics computed from segmentation output. Pre-trained model on FRDR data. Not yet executed.
---
