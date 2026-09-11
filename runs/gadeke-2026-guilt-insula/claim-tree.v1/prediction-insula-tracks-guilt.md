---
uuid: a3c124db-5983-4f4a-81da-77aa7d917e7c
slug: prediction-insula-tracks-guilt
doi: ~
claim: >
  If anterior insula encodes interpersonal guilt, then in the trial-level GLM,
  anterior insula BOLD should be elevated in the Social vs Partner contrast
  specifically after negative partner outcomes — i.e., the (condition × partner-outcome)
  interaction should yield a significant positive cluster in the anterior insula,
  detectable with small-volume FWE correction (SVC) over an a priori anterior-insula
  ROI derived from prior literature. The signal should not be present for the same
  contrast after positive partner outcomes (specificity).
displayClaim: >
  The insula-as-guilt-substrate hypothesis predicts elevated anterior insula BOLD
  in Social vs Partner trials specifically after negative partner outcomes — the
  (condition × outcome) interaction in an a priori insula ROI.
claim-type: prediction
role: prediction
concepts:
  - anterior insula
  - guilt
  - fMRI prediction
  - condition by outcome interaction
  - small-volume correction
priority: 2026-04-20
epistemic: prediction
status: N/A
panel: prediction

derived-from:
  - hypothesis-insula-tracks-interpersonal-guilt

belongings: []

assertions:
  - paper-slug: gadeke-2026-guilt-insula
    doi: 10.7554/eLife.105391
    panel: prediction
    analysis: ~
    dataset: ~
    dataset-doi: ~
    method: derived prediction
    confidence: strong

reproductions: []
---

This prediction picks out the specific (condition × partner-outcome) interaction term as the falsifiable BOLD signature of the insula-guilt hypothesis. The paper's a priori SVC ROI restriction is essential to its falsifiability — a whole-brain unrestricted contrast risks finding a positive cluster somewhere by chance, while the SVC over the anterior insula ROI commits in advance to where the effect must appear. The prediction also commits to a specific peak location (anterior, not mid- or posterior-insula) consistent with the moral-emotion literature. Tested directly by `insula-tracks-guilt-effect`, with peak MNI [-28, 24, -4] confirmed against the deposited group .mat file. The convergent-validity prediction (`insula-guilt-replicates-yu-koban-signature`) is an independent satisfaction of the same anatomical commitment via pattern expression rather than peak location.
