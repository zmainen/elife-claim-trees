---
uuid: 96991fa1-856f-4b2e-875d-715d254696d0
slug: v1-category-decoding-drops-in-feedback
doi: ~
claim: >
  In foveal V1, decoding across semantic category drops significantly relative to baseline in the experimental condition (t(27)=2.25, p=0.033, difference=3.03%), while decoding across visual shape remains high, indicating that foveal feedback carries shape but not category information.
displayClaim: >
  Within foveal V1, cross-category decoding drops significantly under feedback while cross-shape decoding is preserved, marking shape as the feature dimension carried by the feedback signal.
claim-type: empirical
role: empirical
concepts:
  - semantic category
  - shape decoding
  - foveal V1
  - information content
  - feedback specificity
priority: 2026-03-30
epistemic: moderate

tests:
  - prediction-v1-category-drops-shape-preserved
dissociates-with:
  - lo-shows-reversed-specificity

belongings:
  - relation: supports
    target: hypothesis-feedback-carries-shape-not-category
  - relation: supports
    target: decoding-shape-sensitive-not-semantic

assertions:
  - paper-slug: kammer-2026-foveal-feedback
    doi: ~
    panel: fig3B
    figureUri: https://iiif.elifesciences.org/lax/107053%2Felife-107053-fig3-v1.tif/full/1500,/0/default.jpg
    analysis: Lucakaemmer/FovealFeedback (GitHub)
    dataset: https://doi.org/10.18112/openneuro.ds005933.v1.0.0
    dataset-doi: 10.18112/openneuro.ds005933.v1.0.0
    method: pairwise MVPA decoding, paired t-test vs baseline
    confidence: moderate

reproductions:
  - agent: mainen-z
    date: 2026-03-30
    status: blocked
    blocked_by: compute-infeasible
    notes: >
      Blocker (2026-03-30): Requires separate pairwise decoding for cross-category comparisons
      relative to cross-both baseline (FovealDecoding.run_all_decoding(comparison='category')).
      Paired t-test (experimental vs control) computed over 28 subjects from accuracy_matrices_1v1.
      Same pipeline dependency as main decoding claim (~100 CPU-hours). Effect size modest (3.03%,
      p=0.033, near threshold). No pre-computed pairwise results in repo. Three-source confidence.
---

The effect size for the category drop (3.03%) is substantially smaller than in the control condition (16.64%), which is consistent with the interpretation that feedback carries weaker categorical information than direct stimulation. The shape decoding comparison is not reported with a separate t-test in the results text — only the category drop is tested. This asymmetry means the "shape remains high" claim is inferred from the absence of a significant drop, not from a direct test, which limits its epistemic strength.
