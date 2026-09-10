---
uuid: 60dc4ad3-7400-4bd9-bf23-dfc403bdea39
slug: no-item-stability-difference-acquisition
doi: ~
claim: >
  During fear acquisition, item stability (within-cue neural pattern similarity) does not
  differ between CS+ and CS- cues anywhere in the brain, showing that threat learning
  selectively increases cross-item generalization but not single-item representational
  consistency.
claim-type: empirical
role: empirical
concepts:
  - item stability
  - null result
  - fear acquisition
  - RSA
  - representational dissociation
priority: 2026-03-30
epistemic: moderate

dissociates-with:
  - cue-generalization-increases-acquisition

belongings:
  - relation: supports
    target: dual-strategy-reversal-generalize-plus-specify
  - relation: extends
    target: cue-generalization-increases-acquisition

assertions:
  - paper-slug: bouyeure-2026-fear-rsa
    doi: 10.7554/eLife.105126
    panel: fig3A
    figureUri: https://iiif.elifesciences.org/lax/105126%2Felife-105126-fig3-v1.tif/full/1500,/0/default.jpg
    analysis: run_nina_analysis.py, fear_rsa_core.py
    dataset: https://doi.org/10.17605/OSF.IO/NGWKA
    dataset-doi: 10.17605/OSF.IO/NGWKA
    method: RSA searchlight, item-stability measure, cluster FWE 10k permutations (p<0.025 threshold)
    confidence: moderate

reproductions:
  - agent: mainen-z
    date: 2026-03-30
    status: unattempted
    notes: ~
---

This null result is load-bearing: the paper's theoretical argument depends on item stability and cue generalization being dissociable. If item stability were also elevated for CS+ during acquisition, the two measures would not be functionally distinct. The claim is explicit in the caption ("No differences in item stability were found") and results text. Standard caveats about null results under cluster FWE apply — absence of significance does not guarantee absence of effect, especially with n=24.
