---
uuid: a24358b5-0552-472b-8679-3d318d4d702f
slug: seven-target-trajectories-13-regions-7478-neurons
doi: ~
claim: >
  All brain-wide claims in the paper rest on a recording dataset of 7,478 neurons sorted
  via the IBL spike-sorting pipeline from 86 dual-Neuropixel insertions across 57 recording
  sessions in 17 head-fixed awake mice (11 SERT-Cre, 6 WT), with insertion trajectories
  targeting seven planned brain locations and post-hoc histology-aligned to 13 brain regions
  in Allen atlas space.
displayClaim: >
  Recording dataset: 7,478 neurons, 13 regions, 86 insertions, 57 sessions, 17 mice (11 SERT,
  6 WT) — IBL pipeline sorted, histology-aligned, awake head-fixed.
claim-type: assessment
role: scope
concepts:
  - dataset scope
  - Neuropixels
  - IBL pipeline
  - histology alignment
  - awake recording
priority: 2026-04-20
epistemic: strong

scopes:
  - 5ht-modulates-all-recorded-regions-bidirectionally
  - 5ht-stim-leaves-decision-behavior-intact
  - 5ht-modulation-weaker-during-task
  - 5ht-axis-orthogonal-to-choice-axis
  - inhibition-fast-excitation-slow

belongings: []

assertions:
  - paper-slug: meijer-2025-serotonin-orthogonal
    doi: 10.1101/2025.08.01.668048
    panel: fig2c, fig2d (recording counts), methods (sorting pipeline, alignment)
    analysis: IBL spike-sorting pipeline (ref. 24)
    dataset: IBL ONE protocol
    dataset-doi: ~
    method: dual Neuropixels in awake head-fixed mice, IBL pipeline preprocessing and spike-sorting, histology-based atlas alignment via DiI-coated probes
    confidence: strong

reproductions:
  - agent: mainen-z
    date: 2026-04-20
    status: unverified
    notes: ~
---

This is a scope claim, not a result. It is included as an explicit node because every brain-wide claim in the paper inherits its statistical reach and biological coverage from these dataset bounds. The 13-region coverage is not exhaustive of the forebrain — major regions absent include thalamic nuclei beyond LP/PO, ventral striatum beyond dorsal striatum, full extent of the amygdaloid complex, and most brainstem structures other than the recording sites. Generalizations of the orthogonality finding to non-recorded regions require the additional assumption of homogeneity that the data do not directly support. The 11 SERT-Cre / 6 WT split is at the typical scale for this class of experiment but is small for hierarchical mixed-effects analysis at the per-animal level — most analyses pool neurons across animals into a super-session.
