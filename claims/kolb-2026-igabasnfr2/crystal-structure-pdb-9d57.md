---
uuid: f7d3b257-5ae5-4122-a122-0184b12b15f7
slug: crystal-structure-pdb-9d57
doi: ~
claim: >
  The crystal structure of iGABASnFR2 is deposited at the Protein Data Bank (accession 9D57), providing atomic-resolution structural information on the binding pocket and cpGFP domain arrangement.
claim-type: existence
role: methodological
concepts:
  - crystal structure
  - PDB
  - X-ray crystallography
  - binding pocket
  - cpGFP
priority: 2026-03-30
epistemic: strong

enables-method:
  - igabasnfr2-cpgfp-rigid-on-gaba-binding

belongings: []

assertions:
  - paper-slug: kolb-2026-igabasnfr2
    doi: ~
    panel: fig3 (or structural supplement)
    figureUri: https://iiif.elifesciences.org/lax/108319%2Felife-108319-fig3-v1.tif/full/1500,/0/default.jpg
    analysis: PDB accession 9D57
    dataset: https://doi.org/10.2210/pdb9D57/pdb
    dataset-doi: 10.2210/pdb9D57/pdb
    method: X-ray crystallography
    confidence: strong

reproductions:
  - agent: mainen-z
    date: 2026-03-30
    status: verified
    script: verification/kolb-2026-igabasnfr2/verify.py
    notes: >
      PDB 9D57 downloaded and parsed directly from RCSB. HEADER confirms: "IGABASNFR2
      FLUORESCENT GABA SENSOR IN COMPLEX WITH GABA", method X-RAY DIFFRACTION, resolution
      2.60 Å, deposited 2024-08-13, released 2025-08-20. Six chains (A,B,C,D,E,F), each
      564 residues, each carrying one GABA ligand (ABU = gamma-amino-butanoic acid, 7 atoms
      per chain at residue 600) and one GFP chromophore (CRO at residue 447). Biological unit
      declared monomeric (REMARK 350). Refinement: R=0.206, R-free=0.249, 98.3% completeness.
      PDB accession 9D57 exists, is publicly accessible, and unambiguously encodes iGABASnFR2
      bound to GABA. Claim verified.
---
