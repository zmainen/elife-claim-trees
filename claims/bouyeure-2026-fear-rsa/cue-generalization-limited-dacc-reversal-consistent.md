---
uuid: 411ed78e-2542-4340-b896-bca7522579ae
slug: cue-generalization-limited-dacc-reversal-consistent
doi: ~
claim: >
  During reversal, cue generalization for CS++ (always threatening) vs CS-- (always safe)
  is elevated only in dACC, not in the broader fear network regions where this effect was
  present during acquisition, suggesting that consistent threat representations are maintained
  more narrowly.
claim-type: empirical
role: empirical
concepts:
  - cue generalization
  - dACC
  - reversal learning
  - CS++
  - regional specificity
priority: 2026-03-30
epistemic: moderate

belongings:
  - relation: extends
    target: cue-generalization-increases-acquisition
  - relation: supports
    target: generalized-pattern-cs-minus-plus-reversal

assertions:
  - paper-slug: bouyeure-2026-fear-rsa
    doi: 10.7554/eLife.105126
    panel: fig3Bi
    figureUri: https://iiif.elifesciences.org/lax/105126%2Felife-105126-fig3-v1.tif/full/1500,/0/default.jpg
    analysis: run_nina_analysis.py, fear_rsa_core.py
    dataset: https://doi.org/10.17605/OSF.IO/NGWKA
    dataset-doi: 10.17605/OSF.IO/NGWKA
    method: RSA searchlight, cue generalization measure, cluster FWE 10k permutations (Bonferroni-corrected alpha p<0.0125)
    confidence: moderate

reproductions:
  - agent: mainen-z
    date: 2026-03-30
    status: unattempted
    notes: ~
---

This narrowing of cue generalization from broad fear network (acquisition) to dACC only (reversal) for the CS++ vs CS-- contrast is a quantitative scope change that goes unremarked by the paper. It may reflect reduced power after Bonferroni-correction (threshold moves from p<0.025 to p<0.0125 for reversal phase) rather than a genuine spatial contraction. The paper does not discuss this possibility.
