---
uuid: e29dd47b-417d-49ba-9fb0-c28f7eb3806a
slug: 5ht-stim-dilates-pupil
doi: ~
claim: >
  Optogenetic activation of dorsal-raphe serotonergic neurons in awake quiet wakefulness
  produces a significant dilation of the pupil approximately 2 s after stimulation offset
  in SERT-Cre + ChR2 mice (n = 11) but not in wild-type controls (n = 6). The dilation is
  measured from a head-mounted-camera DLC pupil-tracking pipeline, with pupil size defined
  as the circle through four DLC keypoints around the pupil rim, and is reported as
  percentage change from a per-session 2nd-percentile baseline.
displayClaim: >
  5-HT stimulation dilates the pupil ~2 s after stimulation offset in SERT-Cre but not WT
  mice.
claim-type: empirical
role: empirical
concepts:
  - pupil dilation
  - optogenetic stimulation
  - DeepLabCut tracking
  - SERT-Cre vs WT
priority: 2026-04-20
epistemic: strong

supports:
  - hypothesis-state-switch-by-5ht

belongings:
  - relation: requires
    target: wt-controls-rule-out-light-artifact

assertions:
  - paper-slug: meijer-2025-serotonin-additive-r1
    doi: ~
    panel: fig1h
    analysis: figure-generation scripts in https://github.com/guidomeijer/SerotoninStimulation
    dataset: IBL ONE protocol
    dataset-doi: ~
    method: DLC pupil tracking, per-session 2nd-percentile baselining, mean across animals, independent-samples t-test SERT vs WT
    confidence: strong

reproductions:
  - agent: mainen-z
    date: 2026-04-19
    status: unverified
    notes: ~
---

Carries over from v1 unchanged. Replicates the prior finding from Cazettes et al. (2021, ref. 20). The WT control is essential — it rules out light-driven pupillary effects from the optogenetic LED itself, which is a known artifact in optogenetics involving brainstem stimulation.
