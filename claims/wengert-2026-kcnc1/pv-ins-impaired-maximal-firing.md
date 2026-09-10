---
uuid: 894a5d58-bca8-4b16-b22b-76b64db1e3e5
slug: pv-ins-impaired-maximal-firing
doi: ~
claim: >
  PV-INs from Kcnc1-A421V/+ mice exhibit impaired maximal firing frequency in patch-clamp recordings compared to wild-type, consistent with Kv3.1 loss-of-function reducing the fast repolarization that enables high-frequency firing.
claim-type: empirical
role: empirical
concepts:
  - Kv3.1
  - maximal firing frequency
  - PV interneurons
  - excitability
  - fast-spiking
priority: 2026-03-30
epistemic: strong

tests:
  - prediction-pv-in-firing-impaired
confirms:
  - prediction-pv-in-firing-impaired
  - hypothesis-pv-in-selective-vulnerability
dissociates-with:
  - excitatory-neurons-unaffected-juvenile

belongings: []

assertions:
  - paper-slug: wengert-2026-kcnc1
    doi: ~
    panel: fig2, fig3
    figureUri: https://iiif.elifesciences.org/lax/103784%2Felife-103784-fig2-v1.tif/full/1500,/0/default.jpg
    analysis: G-Node analysis code
    dataset: https://doi.org/10.12751/g-node.bqni9h
    dataset-doi: 10.12751/g-node.bqni9h
    method: patch-clamp, current-clamp recordings
    confidence: strong

reproductions:
  - agent: mainen-z
    date: 2026-03-30
    status: partial
    script: verification/wengert-2026-kcnc1/verify.py
    original_script: https://doi.gin.g-node.org/10.12751/g-node.bqni9h
    script_execution: pre-computed
    script_execution_note: "Primary analysis in Clampfit (proprietary). Statistics verified from deposited Excel summary file."
    time_fast: "~2 min"
    time_full: "~48 hrs (68 GB download + gin)"
    notes: >
      Data from G-Node Excel (PV-IN WT P16-21 Spiking, PV-IN A421V+ P16-21 Spiking sheets).
      Max AP counts per cell from F/I protocol (-100 to +900 pA, 20pA steps):
      WT n=20 mean=200.8; KI n=37 mean=125.9; unpaired t-test p<0.001.
      DISCREPANCY (2026-09-10, audit_run.py): the script named above, run under
      observation on the same sheets and the same n, returns WT=207.8 KI=175.8
      p=0.1661 — the same direction but no significant difference. The two analyses
      disagree about the KI mean (125.9 vs 175.8) and therefore about whether the
      effect is significant at all. Which is correct has not been adjudicated, so the
      status is `partial`: direction reproduces, magnitude and significance do not.
      Recorded `verified` with p<0.001 until this audit; that verdict was never
      produced by the script the record cites.
      Direction (WT > KI) and significance both confirmed. Adult data (P32-42 sheets)
      also present: WT n=14, KI n=17.

discrepancy:
  type: methodological-gap
  explanation: >
    Paper reports WT~201 > KI~126 APs, p<0.001. Deposited Excel gives WT=207.8 (n=20), KI=175.8 (n=37), p=0.17. The deposited sheet may include cells excluded in the paper analysis, or the paper uses a different statistical test (e.g. mixed-effects vs t-test).
---
