---
uuid: e645b7b4-05c4-4b37-b75f-3e47c0d585b2
slug: cue-generalization-increases-acquisition
doi: ~
claim: >
  Neural representations of threatening cues (CS++) generalize across items during fear acquisition: RSA shows that patterns for different CS++ items become more similar to each other in the fear network, indicating a shared threat-cue representation.
claim-type: empirical
role: empirical
concepts:
  - cue generalization
  - CS++
  - fear acquisition
  - RSA
  - threat representation
priority: 2026-03-30
epistemic: moderate

tests:
  - prediction-cue-generalization-fear-network-acquisition

belongings:
  - relation: requires
    target: lss-unreinforced-trials-only
  - relation: supports
    target: hypothesis-fear-network-generalizes-threat-cues

assertions:
  - paper-slug: bouyeure-2026-fear-rsa
    doi: 10.7554/eLife.105126
    panel: fig3A
    figureUri: https://iiif.elifesciences.org/lax/105126%2Felife-105126-fig3-v1.tif/full/1500,/0/default.jpg
    analysis: run_nina_analysis.py, fear_rsa_core.py
    dataset: https://doi.org/10.17605/OSF.IO/NGWKA
    dataset-doi: 10.17605/OSF.IO/NGWKA
    method: RSA searchlight + ROI analysis (BrainIAK), permutation testing (10k, cluster FWE)
    confidence: moderate

reproductions:
  - agent: mainen-z
    date: 2026-03-30
    status: partial
    notes: >
      NeuroVault map downloaded (s1r1_CSplus_s1r1_between_vs_CSminus_s1r1_between_logpmax_size025.nii.gz).
      This is the searchlight cue-generalization (between-item RSA) map for session 1 run 1 (acquisition).
      2283 significant voxels. Max -log10(p)=2.959. Peaks at MNI (-12,10,44), (-4,30,42), (6,28,59)
      — all in dACC/SFG territory. dACC/SFG (medial frontal): 286 sig voxels, max=2.959 — CONFIRMED.
      Insula: L=38, R=16 sig voxels — CONFIRMED. Caudate: 44 sig voxels, max -log10(p)=1.419 (borderline).
      The claim says "dACC, SFG, caudate, insula" — three of four confirmed, caudate borderline.
      NOTE: This map is labeled "s1r1" (session 1 run 1 only), so it reflects early acquisition only.
      The full acquisition cue-generalization result in fig3A may pool across both acquisition runs,
      which would change the threshold and cluster sizes. This is a partial verification of the
      acquisition cue-generalization spatial claim.
---
