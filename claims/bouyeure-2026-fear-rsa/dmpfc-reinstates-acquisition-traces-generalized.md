---
uuid: ebc27c8f-666b-474f-8980-f41e0d25843c
slug: dmpfc-reinstates-acquisition-traces-generalized
doi: ~
claim: >
  In dmPFC during test_old, generalized reinstatement is higher for acquisition memory
  traces than for test_new memory traces (F(2,259)=4.01, p<0.05; t(259)=2.96, p<0.05),
  showing that dmPFC preferentially reinstates category-level (generalized) acquisition
  representations.
claim-type: empirical
role: empirical
concepts:
  - dmPFC
  - generalized reinstatement
  - fear acquisition
  - memory reinstatement
  - representational format
priority: 2026-03-30
epistemic: moderate

dissociates-with:
  - ifg-reinstates-reversal-traces-item-specific

belongings:
  - relation: supports
    target: dual-strategy-reversal-generalize-plus-specify
  - relation: requires
    target: cue-generalization-increases-acquisition

assertions:
  - paper-slug: bouyeure-2026-fear-rsa
    doi: 10.7554/eLife.105126
    panel: fig4Bii
    figureUri: https://iiif.elifesciences.org/lax/105126%2Felife-105126-fig4-v1.tif/full/1500,/0/default.jpg
    analysis: roi_lme_analysis.R, master_stats.R
    dataset: https://doi.org/10.17605/OSF.IO/NGWKA
    dataset-doi: 10.17605/OSF.IO/NGWKA
    method: ROI-based LME, Wilcoxon post-hoc (FDR-corrected within ROI)
    confidence: moderate

reproductions:
  - agent: mainen-z
    date: 2026-03-30
    status: unattempted
    notes: n=261; ROI derived from searchlight clusters (circular concern as in IFG claim)
---

Paired with the IFG claim, this establishes a dissociation: IFG reinstates item-specific reversal traces, dmPFC reinstates generalized acquisition traces. The paper concludes these regions represent memories from different phases in different formats. This is an interpretive synthesis claim built from two independent ROI tests, each with moderate evidence. The dissociation interpretation requires both effects to be real; if either fails to replicate, the dissociation collapses.
