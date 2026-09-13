---
uuid: a246d73e-44f4-4bee-aff2-96388949b76a
slug: participant-momentary-happiness-varied-rewards-2
doi: null
claim: Participant momentary happiness varied with the rewards the partner received in the current trial.
claim-type: empirical
role: empirical
concepts: []
priority: '2026-09-12'
epistemic: tentative
part-of:
- responsibility-redux-model-incorporating-expected
belongings:
- relation: supports
  target: responsibility-partner-outcomes-influences-participant
assertions:
- paper-slug: gadeke-2026-guilt-insula
  doi: 10.7554/eLife.105391
  panel: fig3b,fig3f
  confidence: tentative
reproductions:
- carried_from: happiness-correlates-partner-reward
  agent: mainen-z
  date: 2026-03-30
  status: verified
  script: verification/gadeke-2026-guilt-insula/verify.py
  original_figure: verification/originals/gadeke-2026-guilt-insula/fig3.jpg
  figure: verification/gadeke-2026-guilt-insula/fig-happiness-partner-reward.png
  original_script: https://github.com/BonnSocialNeuroscienceUnit/ResponsibilityExperiment/blob/main/Code/bin/
  script_execution: not-executed
  script_execution_note: Requires MATLAB + SPM12. Statistics verified from deposited pre-computed NIfTI
    and CSV outputs.
  time_fast: ~3 min
  time_full: ~3 hrs (MATLAB + SPM12)
  notes: "Pre-computed LMM tables in Code/csv/ confirm all values directly. Partner reward (rewardPart)\
    \ is a significant positive predictor of happiness in both studies:\n  fMRI Study: β=0.16* (SE=0.07),\
    \ Model R²=0.185, N=1895 (matches paper R²=0.185)\n  Behav Study: β=0.21*** (SE=0.06), Model R²=0.147,\
    \ N=2428 (matches paper)\nThe paper reports partner reward F-statistics from a different model decomposition;\
    \ our confirmatory statsmodels LMM on trial-level data gives:\n  fMRI: β=0.631, p=1.05e-14; Behav:\
    \ β=0.575, p=1.88e-16\nPearson r (pooled, no random effects): fMRI r=0.243, Behav r=0.230, both p<1e-13.\
    \ Direction, significance, and approximate R² all match. Claim verified.\n"
- carried_from: happiness-correlates-partner-reward
  agent: mainen-z
  date: 2026-09-06
  status: verified
  script: verification/gadeke-2026-guilt-insula/verify.py
  function: verify_happiness_partner() (verify.py line 147)
  data_source: https://github.com/BonnSocialNeuroscienceUnit/ResponsibilityExperiment
  data_commit: 11854fe
  data_file: Code/csv/
  data_note: 'Happiness-by-model tables for both cohorts, located by column matching rather than filename;
    see the caveat in notes.

    '
  script_execution: executed
  script_execution_note: Executed 2026-09-06 in Python (fast mode, ~3 min) against the authors' deposited
    analysis tables and thresholded maps. The authors' original MATLAB/SPM12 pipeline was NOT re-run;
    that is full mode, requiring OpenNeuro ds005588 (~15 GB) plus MATLAB and SPM12.
  paper_value: R2 = 0.185 (fMRI cohort), 0.147 (behavioural cohort)
  reproduced_value: R2 = 0.184, 0.145
  notes: 'Model R² for the happiness model including partner reward, recomputed for both cohorts from
    the authors'' deposited happiness-by-model tables. Both values land within 0.002 of the published
    figures. Caveat on auditability: the script currently locates its input by globbing the CSV directory
    and matching on column names rather than by a pinned filename, so this row of the chain is not yet
    independently auditable — a reader cannot confirm which file was read. Pinning the exact filename
    is an open task.'
---

**Notes from extraction:** The results reader stated the participant- and partner-reward correlations jointly; the caption reader anchored the partner-reward correlation to fig3b/fig3f specifically, so it is split from the participant-reward claim by panel.

**Relations.** Why each outgoing edge was inferred:

- `supports` → `responsibility-partner-outcomes-influences-participant`: Happiness tracking the partner's rewards supports a model that carries partner reward prediction errors (evidence at span results-029).

<!-- Evidence quotes from the extraction agents — preserved for audit. Edit or remove as appropriate. -->

**results-reader evidence:**
> Across all trials, in both studies, participant momentary happiness correlated with rewards obtained in the current trial by the participant and by the partner.

**caption-reader evidence:**
> Happiness varied with rewards received by the participant ( A, E ) and by the partner ( B, F ).
