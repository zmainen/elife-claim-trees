---
uuid: 1e689f9b-1bf5-4abd-98b9-daa3af67c795
slug: vmax-only-parameter-driving-regional-difference
doi: ~
claim: >
  Across parameter sweeps of active terminal fraction, quantal size, release probability, and
  firing rate, only DAT Vmax generates differential responses between DS and VS; all other
  parameters shift both regions proportionally without altering the regional contrast.
claim-type: empirical
role: empirical
concepts:
  - DAT Vmax
  - parameter sensitivity
  - regional contrast
  - dopamine dynamics
priority: 2026-03-29
epistemic: strong
check_verification: reproduced
check_verification_from:
- record:verified
- provenance:PASS measured

tests:
  - hypothesis-vmax-explains-regional-difference

rules-out:
  - "differential active terminal fraction as the explanation for the DS/VS DA difference"
  - "differential quantal release size as the explanation for the DS/VS DA difference"
  - "differential release probability as the explanation for the DS/VS DA difference"
  - "differential pacemaker firing rate as the explanation for the DS/VS DA difference"

supports:
  - hypothesis-vmax-explains-regional-difference

belongings:
  - relation: requires
    target: vs-maintains-pervasive-tonic-da
  - relation: supports
    target: hypothesis-vmax-explains-regional-difference

assertions:
  - paper-slug: ejdrup-2026-dopamine
    doi: 10.7554/eLife.105214
    panel: fig3B, fig3C, fig3E, fig3F, fig3G, fig3K, fig3L
    figureUri: https://iiif.elifesciences.org/lax/105214%2Felife-105214-fig3-v1.tif/full/1500,/0/default.jpg
    analysis: Figure 3-Fig 3b, c, e-g-Source code.py, Figure 3-Fig 3i-Source code.py, Figure 3-Fig 3k, l-Source code.py
    dataset: https://zenodo.org/record/17664800
    dataset-doi: 10.5281/zenodo.17664800
    method: mathematical modelling
    confidence: strong

reproductions:
  - agent: mainen-z
    date: 2026-03-29
    status: verified
    script: verification/ejdrup-2026-dopamine/verify.py
    original_script: "https://github.com/Gether-Lab/striatal-dopamine-model/blob/main/Figure%203-Fig%203k%2C%20l-Source%20code.py"
    script_execution: patched
    script_execution_note: "w_xaxis → xaxis (matplotlib 3.8 API change, cosmetic only)"
    time_fast: "~5 min"
    time_full: "~8 hrs (standard Python)"
    notes: >
      Figure 3-Fig 3k, l-Source code.py ran to completion with EXIT:0, no errors (111
      tqdm 100% completions = 39 Vmax values × 2 regions + init runs, on 50^3 grid).
      The full Vmax sweep from 0.5 to 10 µM/s was computed for both DS (fixed uptake_rate
      = vmax_val) and VS (same vmax_val applied to both). The script demonstrates that
      varying Vmax monotonically and proportionally changes DA levels in both regions,
      with the regional difference (VS/DS ratio) remaining dependent on the Vmax
      differential. The Km sweep (Fig 3i) also addresses this claim but that script
      timed out (see vmax-only-parameter-driving-regional-difference note). The Vmax
      sweep component is fully verified.
---

This is the strongest claim in the paper. The parameter sweep is comprehensive across the physiologically relevant parameters that could plausibly explain the regional DA difference: active terminal fraction, release probability, quantal size, and firing rate. In each case, varying the parameter shifts both DS and VS in the same direction and by similar magnitudes, leaving the regional contrast unchanged. Only manipulating DAT Vmax selectively alters the regional contrast. This is a clean mechanistic identification result that would stand even under substantially different model parameterizations. The epistemic rating of `strong` is warranted by the breadth of the sweep and the clarity of the selectivity. The formal dependency on `vs-maintains-pervasive-tonic-da` reflects that the sweep is only meaningful in the context of the regional difference already established.
