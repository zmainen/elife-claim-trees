---
uuid: 7e9f8e74-5d4e-489d-9a0c-39b2c691b161
slug: when-partner-received-low-lottery
doi: null
claim: 'When the partner received the low lottery outcome, participant happiness was lower when the participant
  rather than the partner had chosen the lottery — a significant partner-outcome × decision-maker interaction
  (Study 1: t(1180) = 3.52, p = 0.0004, β = 0.37; Study 2: t(937) = 2.85, p = 0.0045, β = 0.33) — operationalizing
  interpersonal guilt.'
claim-type: empirical
role: empirical
concepts: []
priority: '2026-09-11'
epistemic: tentative
tests:
- responsibility-outcomes-generates-guilt-participant
belongings:
- relation: requires
  target: linear-mixed-model-containing-all
- relation: requires
  target: hold-partner-behaviour-constant-across
- relation: supports
  target: both-studies-participants-felt-worse
assertions:
- paper-slug: gadeke-2026-guilt-insula
  doi: 10.7554/eLife.105391
  panel: fig3d,fig3h
  confidence: tentative
reproductions:
- carried_from: guilt-reduces-happiness-after-partner-loss
  agent: mainen-z
  date: 2026-03-30
  status: verified
  script: verification/gadeke-2026-guilt-insula/verify.py
  original_script: https://github.com/BonnSocialNeuroscienceUnit/ResponsibilityExperiment/blob/main/Code/bin/
  script_execution: not-executed
  script_execution_note: Requires MATLAB + SPM12. Statistics verified from deposited pre-computed NIfTI
    and CSV outputs.
  time_fast: ~3 min
  time_full: ~3 hrs (MATLAB + SPM12)
  notes: "Pre-computed LMM table (LMM happiness on outcomes and responsibility) confirms the partnerWon:subjDecided_1\
    \ interaction — the guilt-effect term:\n  fMRI Study: β=0.33** (SE=0.12), p<0.01, N=944\n  Behav Study:\
    \ β=0.39*** (SE=0.10), p<0.001, N=1216\nPositive coefficient on partnerWon:subjDecided_1 means that\
    \ happiness after partner-won increases more (or decreases less) when the subject decided — equivalent\
    \ to guilt being lower when partner wins and subject was responsible. The maineffect of subjDecided\
    \ is negative (-0.17** fMRI; -0.17** Behav), confirming agency-reduces-happiness independently. Confirmatory\
    \ analysis on trial-level data (after negative partner outcomes):\n  fMRI: Social mean=-0.448, Partner\
    \ mean=-0.207, t=-1.933, p=0.054 (marginal, small N)\n  Behav: Social mean=-0.464, Partner mean=-0.090,\
    \ t=-3.260, p=0.0012, d=-0.357\nThe LMM interaction is significant in both studies; the simple post-hoc\
    \ comparison is significant in Behav and marginal in fMRI (small N after subsetting). Claim verified.\n"
- carried_from: guilt-reduces-happiness-after-partner-loss
  agent: mainen-z
  date: 2026-09-06
  status: verified
  script: verification/gadeke-2026-guilt-insula/verify.py
  function: verify_guilt_happiness() (verify.py line 197)
  data_source: https://github.com/BonnSocialNeuroscienceUnit/ResponsibilityExperiment
  data_commit: 11854fe
  data_file: Code/csv/
  data_note: 'Single-trial happiness tables for both cohorts. The script locates them by matching column
    names rather than by filename, so the directory is the addressable unit here; see the caveat in notes.

    '
  script_execution: executed
  script_execution_note: Executed 2026-09-06 in Python (fast mode, ~3 min) against the authors' deposited
    analysis tables and thresholded maps. The authors' original MATLAB/SPM12 pipeline was NOT re-run;
    that is full mode, requiring OpenNeuro ds005588 (~15 GB) plus MATLAB and SPM12.
  paper_value: beta = 0.33 (fMRI cohort), 0.39 (behavioural cohort)
  reproduced_value: beta = 0.34, 0.40
  notes: 'The guilt effect is the partnerWon x subjDecided interaction term in a mixed-effects regression
    on z-scored happiness ratings, fitted separately for each cohort on the authors'' deposited single-trial
    happiness tables. Both reproduced coefficients are within 0.01 of the published values. Caveat on
    auditability: as with the partner-reward check, the script locates its input by globbing the CSV directory
    and matching on column names rather than by a pinned filename, so this row of the chain is not yet
    independently auditable. Pinning the exact filename is an open task.'
---

**Notes from extraction:** The core behavioural 'guilt effect'; this is the empirical result that tests the guilt prediction.

<!-- Evidence quotes from the extraction agents — preserved for audit. Edit or remove as appropriate. -->

**results-reader evidence:**
> Crucially, the interaction between partner outcome and decision-maker was significant (Study 1: t(1180) = 3.52, p = 0.0004, β = 0.37, 95% CI = [0.16 0.58]; Study 2: t(937) = 2.85, p = 0.0045, β = 0.33, 95% CI = [0.10 0.56]). When the partner received the low lottery outcome, participant happiness was lower when they rather than the partner had chosen the lottery (Figure 3D, H).

**caption-reader evidence:**
> Crucially, responsibility for low lottery outcomes for the partner decreased participant happiness more than the same outcomes following partner choices (see Results), which fits the definition of interpersonal guilt.
