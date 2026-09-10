---
uuid: ae9a914a-11de-40a8-a291-bfd61d51a787
slug: generalized-pattern-cs-minus-plus-reversal
doi: ~
claim: >
  During reversal, the newly dangerous cue (CS-+) acquires generalized neural representations similar to the originally feared CS++, mirroring the initial acquisition pattern in fear network regions.
claim-type: empirical
role: empirical
concepts:
  - CS-+
  - reversal learning
  - cue generalization
  - fear network
  - RSA
priority: 2026-03-30
epistemic: moderate

tests:
  - prediction-cs-minus-plus-generalizes-reversal

belongings:
  - relation: extends
    target: cue-generalization-increases-acquisition
  - relation: supports
    target: hypothesis-fear-network-generalizes-threat-cues
  - relation: supports
    target: hypothesis-dual-strategy-reversal

assertions:
  - paper-slug: bouyeure-2026-fear-rsa
    doi: 10.7554/eLife.105126
    panel: fig3Bii
    figureUri: https://iiif.elifesciences.org/lax/105126%2Felife-105126-fig3-v1.tif/full/1500,/0/default.jpg
    analysis: run_nina_analysis.py
    dataset: https://doi.org/10.17605/OSF.IO/NGWKA
    dataset-doi: 10.17605/OSF.IO/NGWKA
    method: RSA cue generalization measure
    confidence: moderate

reproductions:
  - agent: mainen-z
    date: 2026-03-30
    status: unattempted
    notes: >
      Not yet executed.
---
