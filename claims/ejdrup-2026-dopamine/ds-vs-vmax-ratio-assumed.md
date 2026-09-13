---
uuid: c3130ba5-465d-4f1a-a851-6796e72a1d72
slug: ds-vs-vmax-ratio-assumed
doi: ~
claim: >
  The 3:1 DS:VS DAT Vmax ratio (DS = 6 µM·s⁻¹, VS = 2 µM·s⁻¹) is assumed from published
  literature rather than directly measured in this study; the immunostaining gradient
  (Figure 2—supplement 1) corroborates this assumption at the protein level but does not
  directly establish the functional Vmax ratio.
claim-type: assessment
role: scope
concepts:
  - DAT Vmax
  - dorsal striatum
  - ventral striatum
  - model parameterization
priority: 2026-03-29
epistemic: moderate
check_verification: partial
check_verification_from:
- record:verified

scopes: ["*"]

interprets:
  - interprets-cragg-rice-vmax-ratio

belongings: []

assertions:
  - paper-slug: ejdrup-2026-dopamine
    doi: 10.7554/eLife.105214
    panel: fig2A (implied throughout)
    figureUri: https://iiif.elifesciences.org/lax/105214%2Felife-105214-fig2-v1.tif/full/1500,/0/default.jpg
    analysis: Figure 2-Fig 2a-f-Source code.py
    dataset: ~
    dataset-doi: ~
    method: code inspection + literature
    confidence: moderate

reproductions:
  - agent: mainen-z
    date: 2026-03-29
    status: verified
    notes: >
      Code inspection confirmed: sim_functions.py sets Vmax_DS = 6.0 µM/s and Vmax_VS = 2.0
      µM/s as fixed parameters. No derivation from first principles appears in any notebook.
      The ratio is cited to prior voltammetry literature (Kennedy et al., Cragg & Rice). The
      Figure 2—supplement 1 immunostaining supports a DS > VS protein gradient (p=0.0021) but
      does not quantify functional Vmax. Assessment claim confirmed by direct code and methods
      reading.
---

The 3:1 Vmax ratio is the central structural assumption of the model; the entire DS/VS regional contrast in simulated DA dynamics flows from it. The assumption is well-supported by prior voltammetry and radioligand binding literature, and the DAT immunostaining data in this paper (Figure 2—supplement 1B–C, p=0.0021) provides protein-level corroboration. However, functional Vmax depends on transporter turnover rate and membrane trafficking as well as surface expression, so protein level and functional capacity are not identical. Claims that derive the regional contrast from this ratio are well-grounded but not fully self-contained within the study; the key prior assumption warrants explicit flagging when assessing downstream result claims.
