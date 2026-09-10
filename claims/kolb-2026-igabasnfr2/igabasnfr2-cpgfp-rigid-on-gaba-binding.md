---
uuid: 81a3fe0f-a268-4abf-8ad5-b4abbdb4b2dc
slug: igabasnfr2-cpgfp-rigid-on-gaba-binding
doi: ~
claim: >
  GABA binding to iGABASnFR2 closes the Venus flytrap lobes of the Pf622 domain but produces negligible conformational change in cpGFP and its flanking linkers (RMSD 0.25 Å), contrasting with the large cpGFP interface rearrangement seen in GCaMP upon calcium binding.
shortClaim: "GABA closes the Pf622 lobes of iGABASnFR2 while leaving cpGFP nearly rigid."
claim-type: empirical
role: interpretation
concepts:
  - iGABASnFR2
  - crystal structure
  - cpGFP
  - conformational change
  - Venus flytrap
  - allosteric mechanism
priority: 2026-03-30
epistemic: strong

interprets:
  - crystal-structure-pdb-9d57
dissociates-with:
  - igabasnfr2-fourfold-sensitivity-gain

belongings:
  - relation: supports
    target: crystal-structure-pdb-9d57
  - relation: extends
    target: crystal-structure-pdb-9d57

assertions:
  - paper-slug: kolb-2026-igabasnfr2
    doi: 10.7554/eLife.108319
    panel: fig3a
    figureUri: https://iiif.elifesciences.org/lax/108319%2Felife-108319-fig3-v1.tif/full/1500,/0/default.jpg
    analysis: PDB structure comparison (9D57 vs 6DGV)
    dataset: https://doi.org/10.2210/pdb9D57/pdb
    dataset-doi: 10.2210/pdb9D57/pdb
    method: X-ray crystallography; structural superposition using cpGFP as reference; RMSD calculation
    confidence: strong

reproductions:
  - agent: mainen-z
    date: 2026-03-30
    status: partial
    notes: >
      Structural analysis performed on PDB 9D57 and 6DGV. Key findings:

      1. 9D57 contains SIX chains (A-F), all GABA-bound (ABU ligand in every chain). There is no
      apo iGABASnFR2 structure in the PDB — RCSB search confirms no other iGABASnFR2 deposits.

      2. 6DGV (iGABASnFR precursor, apo, 2.80 Å) is the comparison structure the paper uses.
      It has one chain, no GABA ligand, 566 residues. CRO chromophore at residue 440 vs 447 in
      9D57 (7-residue offset consistent with mutations/insertions).

      3. 9D57 vs 6DGV residue identity: 501 of 534 shared residue positions differ in amino acid
      type — these are genuinely different proteins (iGABASnFR vs iGABASnFR2), not just apo/bound
      states of the same protein. Direct RMSD from residue-number alignment is not meaningful.

      4. Best structural window alignment (200-residue sliding window with +7 offset): minimum
      RMSD 3.2 Å. cpGFP-anchored superposition (residues ~330-560 in 6DGV / ~337-567 in 9D57):
      RMSD 3.9 Å. This reflects sequence divergence in the cpGFP region, not conformational
      change upon GABA binding.

      5. Within 9D57 itself (all chains GABA-bound): inter-chain cpGFP RMSD ranges 0.40–0.92 Å
      (NCS variation, not GABA-binding comparison).

      Conclusion: the 0.25 Å RMSD claim cannot be directly verified from 9D57 alone because
      no apo iGABASnFR2 structure is deposited. The claim is plausible — cpGFP barrels are
      rigid by design and this sensor mechanism relies on the Pf622 VFT lobes closing rather
      than cpGFP rearrangement — but the specific 0.25 Å figure requires either: (a) an
      unpublished apo iGABASnFR2 structure, or (b) the authors' own superposition protocol
      (likely using 6DGV as apo proxy with a sequence-structure alignment tool like TM-align
      or CE-align). The comparison 9D57 vs 6DGV with cpGFP as anchor is reproducible in
      principle but requires a proper sequence-independent structural aligner to handle the
      sequence divergence correctly.

discrepancy:
  type: data-gap
  explanation: >
    RMSD comparison requires the undeposited apo (GABA-free) crystal structure. Only the GABA-bound structure (PDB 9D57) is publicly available.
---

This structural finding has direct mechanistic implications the paper explicitly flags as a design insight: because cpGFP does not rearrange, the fluorescence mechanism in iGABASnFR2 is distinct from GCaMP, where calcium-driven calmodulin rearrangement at the cpGFP interface is a key source of ΔF/F. The paper suggests this difference "indicates a potential strategy to further enhance performance" — i.e., engineering the cpGFP interface to respond more strongly to the Venus flytrap closure is an unexploited design axis.
