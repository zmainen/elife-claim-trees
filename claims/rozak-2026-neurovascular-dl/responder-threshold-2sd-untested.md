---
uuid: ce04789d-9922-49de-b9e2-6cc87302b3f4
slug: responder-threshold-2sd-untested
doi: ~
claim: >
  Vessels are classified as responders if their radius change exceeds twice the baseline
  standard deviation (2×σ); this threshold is not sensitivity-tested in the main analysis,
  though an alternative 10% threshold is shown in Appendix 1—figure 14 with qualitatively
  similar results.
claim-type: assessment
role: scope
concepts:
  - responder threshold
  - sensitivity analysis
  - methodological assumption
  - vessel classification
priority: 2026-03-30
epistemic: weak

scopes:
  - vessel-radius-heterogeneity-stimulation
  - dilations-nearer-neurons-than-constrictions
  - constrictions-deeper-than-dilations
  - network-assortativity-increases-stimulation
  - capillary-efficiency-increases-4pct
  - blue-light-dilations-exceed-green-control

belongings: []

assertions:
  - paper-slug: rozak-2026-neurovascular-dl
    doi: 10.7554/eLife.95525
    panel: app1fig14
    analysis: code inspection
    dataset: https://doi.org/10.20383/103.01588
    dataset-doi: 10.20383/103.01588
    method: code inspection; comparison of main fig8 vs app1fig14
    confidence: weak

reproductions:
  - agent: mainen-z
    date: 2026-03-30
    status: unattempted
    notes: >
      The 2×SD threshold is stated in the Methods ("Statistical models") and in the Results
      prose. Appendix 1—figure 14 applies a 10% threshold instead and shows "qualitatively
      similar" patterns, but no statistical comparison of the two thresholds is provided.
      The 2×SD threshold is adaptive per-vessel (depends on each vessel's own baseline
      variance), which is biologically reasonable but means the effective sensitivity
      threshold varies across vessels and subjects.
---

This assessment claim is required by `dilations-nearer-neurons-than-constrictions` and
`constrictions-deeper-than-dilations` because those claims are computed only on the responder
subset. If a different threshold substantially changed which vessels are included, the spatial
gradient result could shift. The qualitative agreement with the 10% threshold (app1fig14)
provides partial reassurance, but the absence of a formal sensitivity analysis leaves the
specific quantitative values (16.1 µm, 21.9 µm, etc.) with some threshold-dependence.
