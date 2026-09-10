---
uuid: e1a5b240-e31b-4ecc-abdc-eaa0437e7067
slug: 5ht-modulation-weaker-during-task
doi: ~
claim: >
  Across brain regions, the percentage of significantly 5-HT-modulated neurons is
  significantly lower during steering-wheel task performance (typically 20–40% per region,
  ~5% in amygdala) than during quiet-wakefulness passive stimulation (10–60%); paired
  t-test across regions, p = 0.012.
displayClaim: >
  Significantly fewer neurons are 5-HT-modulated during task performance than during quiet
  wakefulness (paired t-test across regions, p=0.012).
claim-type: empirical
role: empirical
concepts:
  - task vs passive
  - dynamic range
  - neuromodulator gain
  - ZETA test
priority: 2026-04-20
epistemic: moderate

belongings:
  - relation: requires
    target: 5ht-modulates-all-recorded-regions-bidirectionally
  - relation: requires
    target: seven-target-trajectories-13-regions-7478-neurons

assertions:
  - paper-slug: meijer-2025-serotonin-orthogonal
    doi: 10.1101/2025.08.01.668048
    panel: fig4b, fig4d
    analysis: figure-generation scripts in https://github.com/guidomeijer/SerotoninStimulation
    dataset: IBL ONE protocol
    dataset-doi: ~
    method: per-region paired t-test on percent significantly modulated neurons (passive vs task)
    confidence: moderate

reproductions:
  - agent: mainen-z
    date: 2026-04-20
    status: unverified
    notes: ~
---

The reduction is real but the discussion explicitly raises two non-mechanistic explanations that compete with the literal "weaker neuromodulatory drive during task" reading: (1) statistical sensitivity is higher in the passive condition because baseline firing rates are lower and small modulations are more easily detected against quiet baselines; (2) during behavior, neurons are driven away from the optimum of their dynamic range by task input, reducing the relative effect of any constant neuromodulatory drive. Both are cited but neither is directly disproven, so this claim's epistemic status is moderate rather than strong. The amygdala outlier (~5% modulated during task) is striking and not explained.
