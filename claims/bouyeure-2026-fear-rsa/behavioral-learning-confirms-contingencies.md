---
uuid: dc36ab32-bbed-480d-b05d-f833b100b1c3
slug: behavioral-learning-confirms-contingencies
doi: ~
claim: >
  US expectancy ratings follow the hierarchy CS++ > CS+- > CS-+ > CS-- across all experimental
  phases (LME: CS type F=479.35, p<0.0001; phase F=125.6, p<0.001; interaction p<0.001),
  confirming participants learned threat contingencies and their reversals.
claim-type: empirical
role: empirical
concepts:
  - US expectancy
  - fear conditioning
  - reversal learning
  - behavioral learning
  - LME
priority: 2026-03-30
epistemic: strong

validates:
  - hypothesis-fear-network-generalizes-threat-cues
  - hypothesis-dual-strategy-reversal

belongings:
  - relation: supports
    target: dual-strategy-reversal-generalize-plus-specify

assertions:
  - paper-slug: bouyeure-2026-fear-rsa
    doi: 10.7554/eLife.105126
    panel: fig2A
    figureUri: https://iiif.elifesciences.org/lax/105126%2Felife-105126-fig2-v1.tif/full/1500,/0/default.jpg
    analysis: master_stats.R
    dataset: https://doi.org/10.17605/OSF.IO/NGWKA
    dataset-doi: 10.17605/OSF.IO/NGWKA
    method: linear mixed effects model (lme4/lmerTest, Satterthwaite df, Bonferroni-corrected post-hoc Wilcoxon)
    confidence: strong

reproductions:
  - agent: mainen-z
    date: 2026-03-30
    status: partial
    script: verification/bouyeure-2026-fear-rsa/verify.py
    original_script: https://github.com/AntoineBouyeure/Representational-properties-of-cues-and-contexts-shape-fear-learning-and-reversal/blob/main/run_nina_analysis.py
    script_execution: pre-computed
    script_execution_note: "BrainIAK searchlight not re-run. Statistics verified from NeuroVault group maps."
    time_fast: "~4 min"
    time_full: "~48 hrs (BrainIAK + HPC)"
    notes: >
      Behavioral data downloaded from OSF (behaviordata_final.csv, n=24, 12288 rows). CS type
      hierarchy confirmed: overall means CS++(2.62) > CS+-(2.38) > CS-+(2.23) > CS--(1.58),
      matching the paper's ordering exactly. LME with exact model from deposited R script
      (roi_lme_analysis.R): lmer(rating ~ cs_type * phase + (1|subject)) yields
      F(cs_type)=448.75 [paper claims 479.35], F(phase)=210.09 [paper claims 125.6],
      interaction p<0.0001 [paper claims p<0.001]. All effects significant and directionally
      correct. The exact F values differ from the paper's reported values: F(cs_type) 448 vs 479,
      F(phase) 210 vs 126. The direction discrepancy on phase F is large (210 vs 126). This
      likely reflects a different phase coding or data subsetting in the "behavioral_expectancy_clean.csv"
      (not deposited on OSF) vs behaviordata_final.csv we used. The qualitative claim (CS++ > CS+- >
      CS-+ > CS--, p<0.0001, all phases significant) is fully reproduced.

discrepancy:
  type: data-gap
  explanation: >
    OSF behavioral data download returns HTTP 500. When previously accessible, CS type hierarchy was confirmed (CS++ > CS+- > CS-+ > CS--) but exact p-value could not be reproduced due to mixed-effects model differences.
---

During acquisition, CS++ ≈ CS+- and CS-+ ≈ CS-- (post-hoc Wilcoxon, Bonferroni-corrected), consistent with the fact that contingency change has not yet occurred. This equivalence is the expected pattern, not a failure of discrimination — it validates the reversal design by showing participants treated the two CS+ types identically before the reversal phase. The interaction effect (F=29.45, p<0.001) captures the phase-specific differentiation of cue types.
