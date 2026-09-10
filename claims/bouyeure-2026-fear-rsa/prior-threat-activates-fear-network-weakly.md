---
uuid: db8f67a5-9139-44fb-89c1-b30613fbadf5
slug: prior-threat-activates-fear-network-weakly
doi: ~
claim: >
  During reversal, cues that were threatening during acquisition but not currently threatening
  (CS++) vs those that were safe during acquisition and currently threatening (CS-+) still show
  fear network activation — (CS++ > CS+-) > (CS-+ > CS--) — though to a lesser extent than the
  current-threat contrast, suggesting a lingering prior fear memory trace.
shortClaim: "Previously threatening cues still weakly activate the fear network after reversal."
claim-type: interpretive
role: interpretation
concepts:
  - fear memory trace
  - prior threat value
  - reversal learning
  - lingering fear
  - fear network
priority: 2026-03-30
epistemic: weak

interprets:
  - current-threat-activates-fear-network-reversal

belongings:
  - relation: requires
    target: cs-plus-univariate-fear-network-acquisition
  - relation: supports
    target: dual-strategy-reversal-generalize-plus-specify

assertions:
  - paper-slug: bouyeure-2026-fear-rsa
    doi: 10.7554/eLife.105126
    panel: fig2Biii
    figureUri: https://iiif.elifesciences.org/lax/105126%2Felife-105126-fig2-v1.tif/full/1500,/0/default.jpg
    analysis: run_nina_analysis.py
    dataset: https://doi.org/10.17605/OSF.IO/NGWKA
    dataset-doi: 10.17605/OSF.IO/NGWKA
    method: second-level mass-univariate GLM, cluster FWE with 10k permutations (p_uncorr<0.001)
    confidence: weak

reproductions:
  - agent: mainen-z
    date: 2026-03-30
    status: partial
    script: verification/bouyeure-2026-fear-rsa/verify.py
    original_figure: verification/originals/bouyeure-2026-fear-rsa/fig2.jpg
    figure: verification/bouyeure-2026-fear-rsa/fig-prior-threat-mismatch.png
    original_script: https://github.com/AntoineBouyeure/Representational-properties-of-cues-and-contexts-shape-fear-learning-and-reversal/blob/main/run_nina_analysis.py
    script_execution: pre-computed
    script_execution_note: "BrainIAK searchlight not re-run. Statistics verified from NeuroVault group maps."
    time_fast: "~4 min"
    time_full: "~48 hrs (BrainIAK + HPC)"
    notes: >
      NeuroVault map downloaded (run2_previousvalencecontrast_TFCE_nlog10p.nii.gz, collection 23032).
      Only 36 significant voxels survive FWE correction (threshold -log10(p)>1.301). Max -log10(p)=1.670
      (p≈0.021, barely significant). Single cluster peak at MNI (-14, -90, -11) — this is
      posterior cortex / occipital region, NOT a canonical fear network region (dACC, amygdala, insula).
      The paper's claim of "fear network activation" for prior-threat cues is NOT confirmed by the
      deposited map: the only surviving cluster is in occipital/posterior cortex, not in any region
      named as a fear-network constituent. The claim was already rated epistemic:weak. This further
      weakens it — the deposited map shows the activation is (a) barely surviving correction at all,
      and (b) not in the claimed anatomical territory. Status: verified:partial — the existence of
      SOME activation is confirmed, but the fear-network location claim is not.
---

The paper explicitly hedges this interpretation: the activation "may reflect the impact of the lingering fear memory trace (remaining from acquisition) and/or the time required to learn contingency changes during reversal." Both accounts predict the same pattern — reduced but present activation for prior-threat cues — so they cannot be distinguished from this contrast alone. Epistemic: weak because the causal interpretation is acknowledged as ambiguous.
