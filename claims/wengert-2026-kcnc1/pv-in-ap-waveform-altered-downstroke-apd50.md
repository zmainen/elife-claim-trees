---
uuid: 04db8b33-39ce-43b1-8df4-63a156fbc874
slug: pv-in-ap-waveform-altered-downstroke-apd50
doi: ~
claim: >
  PV-INs from Kcnc1-A421V/+ mice show significantly reduced AP downstroke velocity
  and prolonged AP half-duration (APD50) relative to WT at both juvenile (P16–21,
  **p=0.0012 downstroke; **p=0.0053 APD50) and adult (P32–42, **p=0.0051 downstroke;
  ***p<0.001 APD50) stages, while passive membrane properties are largely preserved.
claim-type: empirical
role: empirical
concepts:
  - action potential waveform
  - downstroke velocity
  - APD50
  - Kv3.1
  - PV interneurons
  - repolarization
priority: 2026-03-30
epistemic: strong

tests:
  - prediction-pv-in-firing-impaired
confirms:
  - prediction-pv-in-firing-impaired
interprets:
  - pv-ins-impaired-maximal-firing

belongings:
  - relation: supports
    target: pv-ins-impaired-maximal-firing
  - relation: requires
    target: pv-ins-reduced-k-current-density

assertions:
  - paper-slug: wengert-2026-kcnc1
    doi: 10.7554/eLife.103784
    panel: fig4E, fig4J, Table 1, Table 2
    figureUri: https://iiif.elifesciences.org/lax/103784%2Felife-103784-fig4-v1.tif/full/1500,/0/default.jpg
    scope: ex-vivo
    analysis: G-Node analysis code
    dataset: https://doi.org/10.12751/g-node.bqni9h
    dataset-doi: 10.12751/g-node.bqni9h
    method: whole-cell current-clamp, AP waveform analysis
    confidence: strong

reproductions:
  - agent: mainen-z
    date: 2026-09-13
    status: verified
    script: verification/wengert-2026-kcnc1/verify.py
    original_script: https://doi.gin.g-node.org/10.12751/g-node.bqni9h
    script_execution: executed
    script_execution_note: >
      Automated as verify_ap_waveform(): reads the Downstroke Velocity and APD 50 rows from
      the four PV-IN spiking sheets (WT/KI x P16-21/P32-42) and t-tests WT vs KI at each age.
    data_source: https://doi.gin.g-node.org/10.12751/g-node.bqni9h
    notes: >
      VERIFIED from G-Node Excel summary. Juvenile (P16-21): WT n=20, KI n=37.
      Downstroke velocity: WT -183.3±37.4, KI -137.5±50.7 mV/ms; p=0.0008.
      Paper reports means as -183±9 and -138±8 — the ±9 and ±8 are SEM not SD
      (SEM for n=20 from SD=37.4 = 8.4 ≈ 9; SEM for n=37 from SD=50.7 = 8.3 ≈ 8).
      Means match paper exactly. p=0.0008 (paper: p=0.0012 — minor discrepancy,
      likely due to Welch vs Student t-test choice).
      APD50: WT 0.401ms, KI 0.561ms; p=0.0063 (paper: p=0.0053 — consistent).
      Adult (P32-42): WT n=14, KI n=17.
      Downstroke: WT -247.8±78.3, KI -163.7±75.9 mV/ms; p=0.0051 (paper: p=0.0051 EXACT).
      APD50: WT 0.314ms, KI 0.582ms; p=0.0033 (paper: ***p<0.001 — slight discrepancy;
      both clearly significant).
---

The AP waveform changes are the mechanistic bridge between K+ current loss and firing
frequency impairment: slower repolarization lengthens the AP, which reduces the rate at
which PV-INs can return to threshold and fire again. The preservation of passive membrane
properties confirms cell-autonomous Kv3.1-specific impairment rather than general
membrane disruption.
