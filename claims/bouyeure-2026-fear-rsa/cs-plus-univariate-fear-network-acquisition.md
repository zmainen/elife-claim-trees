---
uuid: 364302b6-4c41-4591-8df9-7800a8c674ff
slug: cs-plus-univariate-fear-network-acquisition
doi: ~
claim: >
  During fear acquisition, threatening cues (CS+) produce significantly greater BOLD activation
  than safe cues (CS-) in dACC, superior frontal gyrus, caudate nucleus, and middle temporal
  gyrus, replicating the canonical fear network activation pattern.
claim-type: empirical
role: empirical
concepts:
  - univariate activation
  - fear network
  - dACC
  - fear acquisition
  - BOLD
priority: 2026-03-30
epistemic: strong

enables-method:
  - cue-generalization-increases-acquisition

belongings:
  - relation: supports
    target: cue-generalization-increases-acquisition

assertions:
  - paper-slug: bouyeure-2026-fear-rsa
    doi: 10.7554/eLife.105126
    panel: fig2Bi
    figureUri: https://iiif.elifesciences.org/lax/105126%2Felife-105126-fig2-v1.tif/full/1500,/0/default.jpg
    analysis: run_nina_analysis.py
    dataset: https://doi.org/10.17605/OSF.IO/NGWKA
    dataset-doi: 10.17605/OSF.IO/NGWKA
    method: second-level mass-univariate GLM, cluster FWE with 10k permutations (p_uncorr<0.001)
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
      NeuroVault map downloaded (CSplus-minus_TFCE_nlog10p.nii.gz, collection 23032).
      Map stores -log10(p) values (TFCE corrected), threshold at 1.301 for p<0.05.
      5544 significant voxels. Peak at MNI (8.5, 15.0, 39.0), -log10(p)=4.0 (p<0.0001).
      dACC/SFG (X: -15 to 15, Y: 5-40, Z: 20-55): 948 sig voxels, peak at MNI (6,15,39) — CONFIRMED.
      Caudate (X: -20 to 20, Y: 0-18, Z: -5 to 20): 216 sig voxels, peak at MNI (6,5,-1) —
      CONFIRMED but peak is at caudate/putamen/accumbens boundary, Y=5 which is consistent with
      caudate head.
      MTG (|X|>40, Y: -65 to -25, Z: -15 to 12): 0 significant voxels — NOT FOUND in deposited map.
      The claimed MTG activation cannot be confirmed from the NeuroVault TFCE map. This could reflect
      a more lenient threshold used in the paper's figure, a subthreshold result not surviving FWE
      correction, or a labeling issue. The paper's core claim (dACC/SFG) is confirmed; caudate is
      borderline-confirmed; MTG is not confirmed in the corrected map.
---

This is the expected replication of prior fear conditioning work (Fullana et al., 2016). It establishes that the paradigm produces standard fear network responses and validates the experimental manipulation before the RSA analyses. The absence of a significant CS- > CS+ cluster is also reported and expected.
