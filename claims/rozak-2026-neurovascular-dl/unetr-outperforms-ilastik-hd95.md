---
uuid: db0a9448-8fe8-4336-b220-0a71aa19d870
slug: unetr-outperforms-ilastik-hd95
doi: ~
claim: >
  UNETR ensemble segmentation shows significantly better HD95 surface distance than ilastik
  for both vessel and neuron channels (p<0.05 Wilcoxon signed-rank), while ilastik over-segments
  vessels with high recall (0.89±0.19) but low precision (0.37±0.33), evaluated on nine test
  images (507×507×250 µm) from six held-out mice.
claim-type: empirical
role: control
concepts:
  - UNETR
  - ilastik
  - HD95
  - vessel segmentation
  - Dice score
  - precision
  - recall
priority: 2026-03-30
epistemic: moderate

tests:
  - prediction-pipeline-outperforms-baselines
confirms:
  - hypothesis-dl-pipeline-enables-network-nvc
dissociates-with:
  - novas3d-outperforms-ilastik

belongings:
  - relation: requires
    target: novas3d-single-preparation-scope
  - relation: extends
    target: novas3d-outperforms-ilastik

assertions:
  - paper-slug: rozak-2026-neurovascular-dl
    doi: 10.7554/eLife.95525
    panel: fig3
    figureUri: https://iiif.elifesciences.org/lax/95525%2Felife-95525-fig3-v1.tif/full/1500,/0/default.jpg
    analysis: Tutorial.ipynb
    dataset: https://doi.org/10.20383/103.01588
    dataset-doi: 10.20383/103.01588
    method: Wilcoxon signed-rank test on segmentation metrics; 9 test images, 6 mice
    confidence: moderate

reproductions:
  - agent: mainen-z
    date: 2026-03-30
    status: unattempted
    notes: >
      Requires GPU inference on FRDR test data. Pre-trained model available via GitHub
      (AICONSlab/novas3d). Note: UNETR vs U-Net showed no significant difference on mean
      surface distance, so UNETR was selected on visual inspection consistency, not metric
      superiority over U-Net.
---

The claim is about UNETR vs ilastik, not UNETR vs U-Net. The paper reports no significant
difference between UNETR and U-Net on mean surface distance/HD95, so the selection of UNETR
over U-Net was based on visual consistency, not metric dominance. The existing `novas3d-outperforms-ilastik`
claim conflates UNETR and U-Net under "NOVAS3D" — this claim is more precise: UNETR specifically
beats ilastik on HD95, while ilastik beats both DL models on recall (at the cost of massive
over-segmentation and false positives).
