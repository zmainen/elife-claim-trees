---
uuid: 73b97665-ce32-4361-81d0-40fb149cea2b
slug: novas3d-outperforms-ilastik
doi: ~
claim: >
  The NOVAS3D deep learning segmentation pipeline (UNet/UNETR) achieves significantly higher Dice scores and precision/recall for volumetric vessel segmentation than the baseline ilastik classifier on the deposited two-photon microscopy test dataset.
claim-type: empirical
role: control
concepts:
  - NOVAS3D
  - UNet
  - UNETR
  - Dice score
  - vessel segmentation
  - ilastik baseline
priority: 2026-03-30
epistemic: moderate

tests:
  - prediction-pipeline-outperforms-baselines
confirms:
  - hypothesis-dl-pipeline-enables-network-nvc
enables-method:
  - vessel-radius-heterogeneity-stimulation
  - dilations-nearer-neurons-than-constrictions
  - network-assortativity-increases-stimulation
  - capillary-efficiency-increases-4pct

belongings:
  - relation: extends
    target: unetr-outperforms-ilastik-hd95

assertions:
  - paper-slug: rozak-2026-neurovascular-dl
    doi: 10.7554/eLife.95525
    panel: fig3, fig4
    figureUri: https://iiif.elifesciences.org/lax/95525%2Felife-95525-fig3-v1.tif/full/1500,/0/default.jpg
    analysis: Tutorial.ipynb
    dataset: https://doi.org/10.20383/103.01588
    dataset-doi: 10.20383/103.01588
    method: deep learning benchmark comparison
    confidence: moderate

reproductions:
  - agent: mainen-z
    date: 2026-03-30
    status: unattempted
    notes: >
      GitHub: AICONSlab/novas3d. Python package with Tutorial.ipynb. FRDR data deposit. GPU required for inference. Not yet executed.
---
