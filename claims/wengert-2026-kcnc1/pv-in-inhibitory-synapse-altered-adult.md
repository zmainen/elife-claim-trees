---
uuid: bd91acf8-a01d-4713-8382-8a0757cbd86a
slug: pv-in-inhibitory-synapse-altered-adult
doi: ~
claim: >
  In adult (P32–42) Kcnc1-A421V/+ mice, PV-IN-mediated uIPSC magnitude is significantly
  increased relative to WT (**p<0.01 at 20 Hz, *p<0.05 at 40 and 80 Hz), and paired-pulse
  ratio (uIPSC2/uIPSC1) is significantly reduced across frequencies (*p<0.05), indicating
  developmentally emergent synaptic dysfunction in inhibitory neurotransmission.
claim-type: empirical
role: empirical
concepts:
  - inhibitory synaptic transmission
  - uIPSC
  - PV interneurons
  - paired-pulse ratio
  - adult
  - Kv3.1
  - synaptic depression
priority: 2026-03-30
epistemic: strong

tests:
  - prediction-progressive-synaptic-failure
confirms:
  - prediction-progressive-synaptic-failure
  - hypothesis-pv-dysfunction-drives-encephalopathy

belongings:
  - relation: extends
    target: pv-in-inhibitory-synapse-intact-juvenile
  - relation: supports
    target: inhibitory-dysfunction-progresses-to-adulthood

assertions:
  - paper-slug: wengert-2026-kcnc1
    doi: 10.7554/eLife.103784
    panel: fig7F, fig7G, fig7H, fig7I
    figureUri: https://iiif.elifesciences.org/lax/103784%2Felife-103784-fig7-v1.tif/full/1500,/0/default.jpg
    scope: ex-vivo
    analysis: G-Node analysis code
    dataset: https://doi.org/10.12751/g-node.bqni9h
    dataset-doi: 10.12751/g-node.bqni9h
    method: dual whole-cell patch-clamp, paired recording
    confidence: strong

reproductions:
  - agent: mainen-z
    date: 2026-03-30
    status: partial
    notes: >
      Verified from G-Node Excel (WT P32-42 PV->Pyr and Kcnc1 P32-42 PV->Pyr sheets).
      uIPSC amplitude at 20Hz pulse 1: WT n=13 mean=-78.4 pA, KI n=13 mean=-143.2 pA;
      simple t-test p=0.029 (paper reports **p<0.01 by repeated-measures ANOVA — the
      rmANOVA across frequencies yields stronger significance than per-frequency t-tests).
      Direction KI > WT confirmed. PPR at 20Hz: WT 0.815, KI 0.670; t-test p=0.057
      (paper: *p<0.05 by rmANOVA across frequencies). Direction WT > KI confirmed (reduced
      PPR in KI, consistent with enhanced short-term depression). Full significance
      requires rmANOVA that accounts for within-subject correlation across frequencies.
      14/36 WT pairs connected (N=8 mice); 13/36 Kcnc1-A421V/+ pairs connected (N=8 mice).
      Failure rates not different. Latency not significantly different.
---

The adult synaptic finding is the developmental companion to the juvenile null result in
fig6. Together they define the trajectory: presynaptic spike impairment is present at both
ages, but the downstream effect on synaptic terminal function emerges only as Kv3.1 expression
matures in the terminal compartment. The increased amplitude with reduced paired-pulse ratio
is a signature of enhanced initial release probability with faster depression.
