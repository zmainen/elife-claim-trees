---
uuid: 2d67695f-3ee3-45e9-b4bc-ff547691c4bc
slug: registration-doubles-vessel-count
doi: ~
claim: >
  Rigid registration across time points and union of segmentation masks increases the number of
  identified vessel segments per FOV from 241±174 (single time point) to 412±281 (union across
  all time points; 507×507×250 µm, n=107 FOVs), while reducing mean squared error between
  acquisitions from 1306±747 to 0.008±0.003 signal units.
claim-type: methodological
role: methodological
concepts:
  - image registration
  - vessel extraction
  - segmentation union
  - transient RBC plug
  - capillary gap
priority: 2026-03-30
epistemic: moderate

tests:
  - prediction-pipeline-outperforms-baselines
confirms:
  - hypothesis-dl-pipeline-enables-network-nvc
enables-method:
  - network-assortativity-increases-stimulation
  - capillary-efficiency-increases-4pct

belongings:
  - relation: supports
    target: dl-model-scope-single-pipeline

assertions:
  - paper-slug: rozak-2026-neurovascular-dl
    doi: 10.7554/eLife.95525
    panel: ~
    analysis: Tutorial.ipynb
    dataset: https://doi.org/10.20383/103.01588
    dataset-doi: 10.20383/103.01588
    method: ANTsPy rigid registration; MSE metric; vessel segment count from skeleton graph
    confidence: moderate

reproductions:
  - agent: mainen-z
    date: 2026-03-30
    status: unattempted
    notes: >
      No figure directly displays the 241→412 vessel count comparison; the numbers appear in
      the Results prose (section "Vessel extraction improvements via image registration").
      The improvement is attributed partly to resolving transient RBC plug gaps by unioning
      masks across time points. MSE values are from the registration section, not a figure panel.
---

This claim captures two coupled facts that the paper presents together: registration improves
alignment quality (MSE decrease), and the union operation recovers vessel segments that are
invisible in any single frame due to transient RBC plugs. The biological interpretation is
that point-in-time imaging systematically underestimates capillary network connectivity.
This has methodological implications: single-time-point segmentation studies of capillaries
likely undercount vessel segments by roughly 40%.
