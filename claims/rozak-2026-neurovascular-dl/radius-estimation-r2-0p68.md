---
uuid: 9639b9cb-4a39-4046-ba35-db6f8f88dfbb
slug: radius-estimation-r2-0p68
doi: ~
claim: >
  The pipeline's boundary-detection radius estimation achieves R²=0.68 against ground-truth
  simulated radii across >100,000 simulations spanning 0.5×–2× dilation/constriction, and
  remains stable under Gaussian noise up to a standard deviation of 200 signal units (image
  range 0–1023 SU).
claim-type: methodological
role: methodological
concepts:
  - radius estimation
  - boundary detection
  - validation
  - noise robustness
  - R-squared
priority: 2026-03-30
epistemic: moderate

tests:
  - prediction-pipeline-outperforms-baselines
validates:
  - vessel-radius-heterogeneity-stimulation
  - baseline-intra-vessel-radius-varies-24pct
  - dilations-nearer-neurons-than-constrictions
enables-method:
  - vessel-radius-heterogeneity-stimulation
  - network-assortativity-increases-stimulation
  - capillary-efficiency-increases-4pct
confirms:
  - hypothesis-dl-pipeline-enables-network-nvc

belongings:
  - relation: supports
    target: vessel-radius-heterogeneity-stimulation
  - relation: supports
    target: dilations-nearer-neurons-than-constrictions

assertions:
  - paper-slug: rozak-2026-neurovascular-dl
    doi: 10.7554/eLife.95525
    panel: fig5
    figureUri: https://iiif.elifesciences.org/lax/95525%2Felife-95525-fig5-v1.tif/full/1500,/0/default.jpg
    analysis: Tutorial.ipynb
    dataset: https://doi.org/10.20383/103.01588
    dataset-doi: 10.20383/103.01588
    method: simulated radius rescaling + Gaussian noise injection; >100,000 simulations
    confidence: moderate

reproductions:
  - agent: mainen-z
    date: 2026-03-30
    status: unattempted
    notes: >
      R²=0.68 is a moderate fit — the validation acknowledges appreciable variance. The paper
      also validates using fluorescent beads (nominal 7.32±0.27 µm diameter), which had a higher
      SNR than in vivo data, so noise was artificially added to match in vivo conditions.
      Bead results not quantitatively summarized in a single metric in main text.
---

The R²=0.68 should be interpreted in context: this is for simulated radius changes spanning
0.5×–2× of the original, which is a large dynamic range. The noise robustness claim (stable to
SD=200 SU) is the more operationally relevant result, because in vivo images have lower SNR than
the bead validation. The paper's own statement that noise "remained stable" until SD>200 SU is
somewhat informal — no statistical test is reported for the noise robustness itself.
