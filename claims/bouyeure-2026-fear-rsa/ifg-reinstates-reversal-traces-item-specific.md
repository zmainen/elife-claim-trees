---
uuid: bcf69f08-b30f-4571-9ecd-69ea60d15414
slug: ifg-reinstates-reversal-traces-item-specific
doi: ~
claim: >
  In IFG during test_old, item reinstatement is higher for reversal memory traces than for
  acquisition or test_new memory traces (F(2,253)=5.50, p<0.01), showing that IFG
  preferentially reinstates the most recently learned item-specific representations.
claim-type: empirical
role: empirical
concepts:
  - IFG
  - item reinstatement
  - reversal learning
  - memory reinstatement
  - test phase
priority: 2026-03-30
epistemic: moderate

dissociates-with:
  - dmpfc-reinstates-acquisition-traces-generalized

belongings:
  - relation: supports
    target: dual-strategy-reversal-generalize-plus-specify
  - relation: requires
    target: item-stability-precuneus-pfc-reversal

assertions:
  - paper-slug: bouyeure-2026-fear-rsa
    doi: 10.7554/eLife.105126
    panel: fig4Bi
    figureUri: https://iiif.elifesciences.org/lax/105126%2Felife-105126-fig4-v1.tif/full/1500,/0/default.jpg
    analysis: roi_lme_analysis.R, master_stats.R
    dataset: https://doi.org/10.17605/OSF.IO/NGWKA
    dataset-doi: 10.17605/OSF.IO/NGWKA
    method: ROI-based LME (reversal > acquisition item reinstatement, Wilcoxon t(253)=-3.01 p<0.01; reversal > test_new t(253)=-2.7 p<0.05)
    confidence: moderate

reproductions:
  - agent: mainen-z
    date: 2026-03-30
    status: unattempted
    notes: ROI derived from searchlight-significant clusters (circular design; see assessment claim rsa-roi-derived-from-searchlight)
---

The IFG ROI was derived from the preceding searchlight analyses, creating a circularity: the ROI was significant in the searchlight, then re-tested in ROI analyses. The paper uses FDR correction for ROI comparisons to partially mitigate this, but the ROI definition procedure is still dependent on the same dataset. n=255 (not all 24 participants × all trials contribute, likely due to missing data in some conditions).
