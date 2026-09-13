---
uuid: 6fb7137d-c89c-4651-9271-014bd6823995
slug: dl-model-scope-single-pipeline
doi: ~
claim: >
  All neurovascular coupling metrics are derived from a single integrated deep learning pipeline (segmentation → registration → graph analysis); the segmentation model requires GPU inference and was trained on data from one imaging preparation (Thy1-ChR2-YFP mice, 6-12 months), so generalization to other preparations is not demonstrated in this paper.
claim-type: assessment
role: scope
concepts:
  - pipeline scope
  - model generalization
  - Thy1-ChR2-YFP
  - GPU requirement
priority: 2026-03-30
epistemic: moderate

scopes:
  - unetr-outperforms-ilastik-hd95
  - novas3d-outperforms-ilastik
  - registration-doubles-vessel-count
  - radius-estimation-r2-0p68
  - vessel-radius-heterogeneity-stimulation
  - dilations-nearer-neurons-than-constrictions
  - network-assortativity-increases-stimulation
  - capillary-efficiency-increases-4pct
  - novas3d-generalizes-qualitatively-ood

belongings: []

assertions:
  - paper-slug: rozak-2026-neurovascular-dl
    doi: ~
    panel: fig1 (architecture)
    figureUri: https://iiif.elifesciences.org/lax/95525%2Felife-95525-fig1-v1.tif/full/1500,/0/default.jpg
    analysis: code inspection
    dataset: ~
    dataset-doi: ~
    method: code inspection
    confidence: moderate

reproductions:
  - agent: mainen-z
    date: 2026-03-30
    status: verified
    notes: >
      README and pyproject.toml confirm Python package with GPU dependency. Mouse model specific. Scope confirmed by inspection.
---
