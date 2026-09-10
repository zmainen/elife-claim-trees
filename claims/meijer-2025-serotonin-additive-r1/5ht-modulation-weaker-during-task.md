---
uuid: f47f8b52-3bc1-44e1-a80a-affbbabde32f
slug: 5ht-modulation-weaker-during-task
doi: ~
claim: >
  Across brain regions, significantly fewer neurons are 5-HT-modulated during task
  performance compared to during quiet wakefulness, by paired t-test across regions
  (p = 0.012). The per-region fractions during task are 20–40% (with the amygdala an
  outlier at ~5%) compared to 10–60% during quiet wakefulness.
displayClaim: >
  Significantly fewer neurons are 5-HT-modulated during task performance than during
  quiet wakefulness (p = 0.012, paired t-test across regions).
claim-type: empirical
role: empirical
concepts:
  - state-dependent modulation
  - task vs passive
  - paired t-test
priority: 2026-04-20
epistemic: moderate

belongings:
  - relation: requires
    target: seven-target-trajectories-13-regions-7478-neurons

assertions:
  - paper-slug: meijer-2025-serotonin-additive-r1
    doi: ~
    panel: fig5d
    analysis: figure-generation scripts in https://github.com/guidomeijer/SerotoninStimulation
    dataset: IBL ONE protocol
    dataset-doi: ~
    method: paired t-test on per-region 5-HT-modulated fraction across the task vs. quiet-wakefulness conditions, two-sample ZETA test for stimulated vs. unstimulated trial activity per neuron
    confidence: moderate

reproductions:
  - agent: mainen-z
    date: 2026-04-19
    status: unverified
    notes: ~
---

Carries over from v1 unchanged. Weaker-during-task is moderate-epistemic because the paper itself acknowledges two non-state-switch alternative explanations: (1) baseline firing rates are higher during task than during quiet wakefulness, making significance harder to establish for the same effect size; (2) neurons during task are driven away from their dynamic-range optimum (ref. 37 — Stemmler & Koch 1999), reducing the relative effect of any modulatory input. The paper appropriately flags this as a limitation. Under R1's framing, the additivity hypothesis is unaffected by this state-dependent magnitude difference — additive modulation still predicts a near-zero choice × stim interaction whether the magnitude is large or small.
