---
uuid: 4dbc065d-daa5-45e9-96d6-9012b33cb24c
slug: context-specificity-increases-reversal
doi: ~
claim: >
  Neural representations of contexts become more distinct (context-specific) during reversal learning compared to acquisition, particularly in prefrontal cortex, reflecting the need to separate safe and dangerous environments.
claim-type: empirical
role: empirical
concepts:
  - context specificity
  - prefrontal cortex
  - reversal learning
  - context representation
  - RSA
priority: 2026-03-30
epistemic: moderate

tests:
  - prediction-context-specificity-increases-during-reversal

belongings:
  - relation: supports
    target: pfc-context-specificity-predicts-renewal
  - relation: supports
    target: hypothesis-context-specificity-supports-renewal

assertions:
  - paper-slug: bouyeure-2026-fear-rsa
    doi: 10.7554/eLife.105126
    panel: fig5B
    figureUri: https://iiif.elifesciences.org/lax/105126%2Felife-105126-fig5-v1.tif/full/1500,/0/default.jpg
    analysis: fear_rsa_exploratory.py
    dataset: https://doi.org/10.17605/OSF.IO/NGWKA
    dataset-doi: 10.17605/OSF.IO/NGWKA
    method: RSA context specificity measure (within-context minus between-context similarity), cluster FWE 10k permutations
    confidence: moderate

reproductions:
  - agent: mainen-z
    date: 2026-03-30
    status: unattempted
    notes: >
      Not yet executed.
---
