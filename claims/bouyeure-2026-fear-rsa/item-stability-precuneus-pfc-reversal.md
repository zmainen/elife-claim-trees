---
uuid: aa1a7bc0-0051-4dc7-bbba-2f96300645e0
slug: item-stability-precuneus-pfc-reversal
doi: ~
claim: >
  During reversal learning, item-specific (stable across phases) representations emerge in precuneus and prefrontal cortex for cues that change their threat value (CS+-), distinguishing the changing cue from the stable threats.
claim-type: empirical
role: empirical
concepts:
  - item stability
  - precuneus
  - prefrontal cortex
  - reversal learning
  - RSA
priority: 2026-03-30
epistemic: moderate

tests:
  - prediction-item-stability-changing-cues-reversal

dissociates-with:
  - generalized-pattern-cs-minus-plus-reversal

belongings:
  - relation: supports
    target: hypothesis-dual-strategy-reversal

assertions:
  - paper-slug: bouyeure-2026-fear-rsa
    doi: ~
    panel: fig4
    figureUri: https://iiif.elifesciences.org/lax/105126%2Felife-105126-fig4-v1.tif/full/1500,/0/default.jpg
    analysis: run_nina_analysis.py, fear_rsa_core.py
    dataset: https://doi.org/10.17605/OSF.IO/NGWKA
    dataset-doi: 10.17605/OSF.IO/NGWKA
    method: RSA searchlight, item-stability measure
    confidence: moderate

reproductions:
  - agent: mainen-z
    date: 2026-03-30
    status: unattempted
    notes: >
      Searchlight analysis. NeuroVault group maps deposited. Not yet executed.
---
