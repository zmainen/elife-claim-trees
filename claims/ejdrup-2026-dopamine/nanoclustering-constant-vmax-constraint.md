---
uuid: 5b351222-ab85-46be-a673-b05a6f104f80
slug: nanoclustering-constant-vmax-constraint
doi: ~
claim: >
  The nanoclustering simulations hold total DAT Vmax constant across clustered and unclustered
  conditions — the per-voxel rate is multiplied by a normalization factor so total integrated
  uptake capacity is identical; if DAT nanoclustering co-occurs with increased total DAT
  expression in biology, the clearance-slowing result would not hold.
claim-type: assessment
role: scope
concepts:
  - DAT nanoclustering
  - model constraint
  - total uptake capacity
  - simulation design
priority: 2026-03-29
epistemic: moderate
check_verification: partial
check_verification_from:
- record:verified

scopes:
  - dat-nanoclustering-slows-clearance
  - hypothesis-nanoclustering-regulates-vmax

belongings: []

assertions:
  - paper-slug: ejdrup-2026-dopamine
    doi: 10.7554/eLife.105214
    panel: fig4C, fig4D, fig4E, fig4F
    figureUri: https://iiif.elifesciences.org/lax/105214%2Felife-105214-fig4-v1.tif/full/1500,/0/default.jpg
    analysis: Figure 4-Fig 4 simulations-Source code.py
    dataset: ~
    dataset-doi: ~
    method: code inspection
    confidence: moderate

reproductions:
  - agent: mainen-z
    date: 2026-03-29
    status: verified
    notes: >
      Code inspection confirmed: Figure 4-Fig 4 simulations-Source code.py includes a
      normalization step that scales per-voxel DAT rates by cluster area fraction so total
      integrated Vmax remains constant across clustered and unclustered conditions. The
      constraint is explicit in the code. No parameter sweep tests the case where nanoclustering
      co-occurs with increased total Vmax. Assessment claim confirmed by direct code reading.
---

The constant-Vmax constraint is a legitimate experimental design choice — it isolates the effect of spatial distribution from total capacity — but its biological validity is worth noting. In cellular reality, DAT nanoclusters may form due to lipid raft partitioning or scaffolding interactions that also alter total surface expression. If VS has both more nanoclustering and more total DAT protein than the model assumes, the clearance-slowing effect of clustering could be counteracted by increased total capacity. The constraint is appropriate for the mechanistic question the paper asks; the assessment flags it for claims that extrapolate the nanoclustering result to the tissue-scale regional difference.
