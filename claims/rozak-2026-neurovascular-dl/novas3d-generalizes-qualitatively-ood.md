---
uuid: afb63ebd-605d-4e1b-a412-9ad7eea3bc58
slug: novas3d-generalizes-qualitatively-ood
doi: ~
claim: >
  The NOVAS3D segmentation model produces qualitatively reasonable vessel segmentations on
  out-of-distribution data including a different mouse strain (C57BL/6), a different species
  (Fischer rat), and a different microscope modality (light-sheet fluorescence microscopy,
  Miltenyi UltraMicroscope Blaze), without retraining.
claim-type: empirical
role: empirical
concepts:
  - model generalization
  - out-of-distribution
  - transfer learning
  - vessel segmentation
  - light-sheet microscopy
priority: 2026-03-30
epistemic: weak

confirms:
  - hypothesis-dl-pipeline-enables-network-nvc

belongings:
  - relation: extends
    target: dl-model-scope-single-pipeline

assertions:
  - paper-slug: rozak-2026-neurovascular-dl
    doi: 10.7554/eLife.95525
    panel: app1fig12, app1fig13
    analysis: ~
    dataset: ~
    dataset-doi: ~
    method: visual inspection of segmentation masks on held-out OOD data; no quantitative metrics
    confidence: weak

reproductions:
  - agent: mainen-z
    date: 2026-03-30
    status: unattempted
    notes: >
      The OOD generalization is purely qualitative — no Dice, HD95, or other quantitative
      metric is reported for the OOD datasets. The appendix shows example 2D slices of
      predictions overlaid on raw data. The OOD data sources are not deposited publicly
      as far as can be determined. This claim is single-source (caption only) and marked weak
      because it relies entirely on visual impression without quantitative validation.
---

This claim complements and qualifies `dl-model-scope-single-pipeline`. The scope assessment
claim notes that generalization is not demonstrated; this claim notes that qualitative evidence
of generalization exists but is not quantified. Both are simultaneously true. The OOD examples
do not constitute a benchmark — they are existence proofs that the model does not catastrophically
fail on novel inputs. Quantitative OOD benchmarking remains absent.
