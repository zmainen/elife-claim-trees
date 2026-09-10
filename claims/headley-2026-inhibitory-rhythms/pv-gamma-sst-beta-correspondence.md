---
uuid: f22677a4-7db6-4fa1-80f6-1d08081293f0
slug: pv-gamma-sst-beta-correspondence
doi: ~
claim: >
  The model provides mechanistic grounding for the empirical association of parvalbumin-positive
  interneurons with gamma rhythms and somatostatin-positive interneurons with beta rhythms:
  PV+ neurons target perisomatic locations where gamma is optimal for AP threshold modulation,
  while SST+ neurons target distal dendrites where beta is optimal for dendritic spike
  entrainment.
displayClaim: >
  Layer 5 inhibitory streams are functionally matched to interneuron type — perisomatic
  gamma-frequency inhibition (PV+) controls somatic spike timing, while distal beta-frequency
  inhibition (SST+) gates dendritic integration of top-down inputs.
shortClaim: "PV-gamma controls somatic spike timing — SST-beta gates distal top-down inputs."
claim-type: interpretive
role: interpretation
concepts:
  - parvalbumin interneurons
  - somatostatin interneurons
  - gamma rhythm
  - beta rhythm
  - interneuron classification
priority: 2026-03-30
epistemic: moderate

interprets:
  - beta-optimal-distal-dendritic-entrainment
  - gamma-optimal-perisomatic-ap-modulation
  - beta-gates-distal-apical-inputs
  - gamma-gates-proximal-basal-inputs
  - interprets-pv-gamma-sst-beta-associations

belongings: []

assertions:
  - paper-slug: headley-2026-inhibitory-rhythms
    doi: 10.7554/eLife.95562
    panel: fig10 (synthesis / discussion)
    figureUri: https://iiif.elifesciences.org/lax/95562%2Felife-95562-fig10-v1.tif/full/1500,/0/default.jpg
    analysis: ~
    dataset: ~
    dataset-doi: ~
    method: interpretive — linking simulation results to anatomical literature
    confidence: moderate

reproductions:
  - agent: mainen-z
    date: 2026-03-30
    status: blocked
    blocked_by: no-code
    script_execution: not-executed
    script_execution_note: "Interpretive synthesis — no script; assessed by consistency with anatomical literature"
    notes: >
      This is an interpretive synthesis claim, not a direct simulation output. There is no
      script or data file to reproduce it. The claim is assessed by examining whether the
      simulation-derived frequency optima (beta for distal, gamma for perisomatic) are
      consistent with the known anatomical targeting of PV+ and SST+ interneurons. The
      empirical PV+/gamma and SST+/beta associations are literature facts, not results of
      this study.
---

This is the paper's key interpretive synthesis: the simulation results are used to provide a functional explanation for an empirical pattern (PV+→gamma, SST+→beta) observed in vivo. The mechanistic logic is: PV+ cells naturally fire at gamma and target the soma → gamma perisomatic inhibition optimally modulates AP threshold → this is a fast, cycle-by-cycle control of somatic output. SST+ cells fire at beta and target distal dendrites → beta distal inhibition optimally entrains dendritic spike occurrence → this is a slower, integration-window control of top-down inputs. The two streams are orthogonal.

The epistemic status is moderate because the paper does not simulate PV+ or SST+ interneuron networks directly — it simulates generic inhibitory inputs with location and frequency parameters. The connection to specific interneuron types requires the biological assumption that PV+ and SST+ cells reliably target the right compartments at the right frequencies, which is a literature claim not a result of this study.
