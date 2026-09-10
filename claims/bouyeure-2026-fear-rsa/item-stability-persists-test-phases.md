---
uuid: 500caa5d-b636-4776-98fe-422b618f8e02
slug: item-stability-persists-test-phases
doi: ~
claim: >
  Item stability (but not cue generalization) persists into test phases in the absence of
  a US: CS+- > CS++ item stability in MTG at test_new, and CS++ > CS-- item stability in
  inferior temporal gyrus at test_old, showing that individual-item memory traces outlast
  the training context.
claim-type: empirical
role: empirical
concepts:
  - item stability
  - persistence
  - test phase
  - memory trace
  - temporal cortex
priority: 2026-03-30
epistemic: moderate

belongings:
  - relation: supports
    target: dual-strategy-reversal-generalize-plus-specify
  - relation: requires
    target: item-stability-precuneus-pfc-reversal

assertions:
  - paper-slug: bouyeure-2026-fear-rsa
    doi: 10.7554/eLife.105126
    panel: fig3C, fig3D
    figureUri: https://iiif.elifesciences.org/lax/105126%2Felife-105126-fig3-v1.tif/full/1500,/0/default.jpg
    analysis: run_nina_analysis.py, fear_rsa_core.py
    dataset: https://doi.org/10.17605/OSF.IO/NGWKA
    dataset-doi: 10.17605/OSF.IO/NGWKA
    method: RSA searchlight, item-stability measure, cluster FWE 10k permutations (p<0.0125)
    confidence: moderate

reproductions:
  - agent: mainen-z
    date: 2026-03-30
    status: unattempted
    notes: ~
---

The test phases have no US, so the persistence of item stability effects cannot be driven by ongoing reinforcement. The CS+- > CS++ effect at test_new (extinguished > always-threatening) is counterintuitive and the paper interprets it as reflecting the salience of learning history for cues whose contingency changed. The CS++ > CS-- effect at test_old (always-threatening > always-safe) is more straightforward — it represents a sustained threat representation in temporal cortex. These two effects appear in different temporal cortex sub-regions (MTG vs InfTemp).
