---
uuid: 42987256-31b8-4f7d-b81f-8f6976a904f0
slug: protocerebral-bridge-layered-transmitter-architecture
doi: ~
claim: >
  The protocerebral bridge (PCB) of Uloborus diversus displays a layered neurotransmitter
  architecture: GABAergic (anti-GAD) immunoreactivity defines a nearly complete swath of the
  neuropil; TDC2 (octopaminergic/tyraminergic) fills heavy chains of puncta along the posterior
  edge; proctolin forms a tight thin band primarily at the medial end; and ChAT (cholinergic)
  immunoreactivity forms a distinct thin layer on both the anterior and posterior edges, most
  clearly on the lateral portion.
claim-type: empirical
role: empirical
concepts:
  - protocerebral bridge
  - layered architecture
  - GABA
  - GAD
  - TDC2
  - octopamine
  - acetylcholine
  - proctolin
  - spider central complex
priority: 2026-03-30
epistemic: strong

dissociates-with:
  - tonsillar-neuropil-serotonin-core-tdc2-shell
  - arcuate-body-four-sublayer-differential

belongings:
  - relation: supports
    target: protocerebral-bridge-candidate-central-complex

assertions:
  - paper-slug: artiushin-2026-spider-atlas
    doi: 10.7554/eLife.107732
    panel: fig10Bi-x
    figureUri: https://iiif.elifesciences.org/lax/107732%2Felife-107732-fig10-v1.tif/full/1500,/0/default.jpg
    analysis: atlas visualization
    dataset: https://doi.org/10.35077/ace-owl-gum
    dataset-doi: 10.35077/ace-owl-gum
    method: immunofluorescence, multi-antibody panel, confocal atlas
    confidence: strong

reproductions:
  - agent: mainen-z
    date: 2026-03-30
    status: unattempted
    notes: >
      Results: "Comparing further neuronal subtype preparations reveals that the PCB has a
      layered structure." Layer-by-layer description is in the Results prose for this section.
      Fig10B shows paired ventral (z722) and dorsal (z730) optical sections. BIL atlas required.
---

The layered transmitter architecture of the PCB is the observational pillar for the protocerebral bridge homology claim (Fig10 overall; see protocerebral-bridge-candidate-central-complex). The GAD/GABA filling of the PCB is particularly diagnostic, as it is one of the defining features of insect central complex columnar neurons. However, the paper explicitly notes that anti-GAD penetration is limited to tissue periphery (see gad-antibody-peripheral-penetration-only), which tempers how confident we can be about the GABAergic filling of interior PCB layers. The TDC2/proctolin/ChAT claims, using antibodies without the penetration caveat, are more secure. This claim is therefore separated from the homology interpretation (which lives in protocerebral-bridge-candidate-central-complex).
