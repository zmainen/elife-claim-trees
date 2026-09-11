A paper summary is a three-part prose rendering of the paper's argument, stored in `site/src/data/paper-summaries.json`. Summaries are authored separately from the claim graph and are designed to be read on their own, without graph traversal.

## The three-part structure

Each summary has three fields, totalling roughly 150–220 words:

- **`hypotheses`** — what the paper sets out to test or argue. Frames the bets the rest of the work makes good on. For atlas papers, this field is renamed **`subject`** because there is no hypothesis structure — the work is observational and the framing is descriptive.

- **`claims`** — what the paper actually establishes empirically. The middle layer between hypotheses and inferences; the body of evidence.

- **`inferences`** — what the paper concludes and what it says those conclusions imply. The interpretive layer that the discussion section typically articulates.

The three fields map onto the rhetorical sequence motivation → evidence → interpretation, but they are not summaries of three different sections of the paper. A claim mentioned in `inferences` may be grounded in an empirical result mentioned in `claims`; the same body of evidence is being presented at different levels of generality.

## Atlas papers — Subject in place of Hypotheses

The artiushin-2026-spider-atlas summary illustrates the atlas exception:

```
subject: A three-dimensional immunofluorescence atlas of the synganglion of the
hackled-orb weaver spider Uloborus diversus, built from whole-mount synapsin
staining and registered to a common reference volume…
claims: The work resolves transmitter architecture across leg, opisthosomal,
pedipalpal, and cheliceral neuropils, describes layered organization of the
arcuate body into four sublayers with differential transmitter content, and
documents two previously uncharacterized protocerebral structures…
inferences: Together the tonsillar neuropil and candidate protocerebral bridge
are proposed as components of a spider equivalent of the insect central complex…
```

The replacement is honest about what an atlas paper is doing: it is not testing a hypothesis, it is delivering a reference resource. The structural slot is preserved; the field name is corrected.

## Generation procedure

Summaries are generated per paper by an agent that reads the claim graph (the paper's claim-file list with frontmatter), the abstract, and any available prose, and writes the three-part summary. The agent is instructed to honour the schema's role labels: hypotheses come from `role: hypothesis` claims, the claims field aggregates `role: empirical` and `role: control` content, and the inferences field aggregates `role: synthesis` and `role: interpretation` content. The agent is allowed to use the abstract for framing where the claim graph is sparse on motivation, but the empirical content of the `claims` field is bound to claims actually present in the graph.

## Why separate authoring rather than concatenation

A natural question is whether `displayClaim` or `shortClaim` fields could be programmatically concatenated to produce the summary. The answer is no, for two reasons.

First, readable prose requires composition, not concatenation. The Headley `hypotheses` field reads "The paper tests whether rhythmic inhibition onto distinct compartments of a layer 5 pyramidal neuron regulates integration in a compartment-specific and frequency-specific manner — specifically, whether perisomatic inhibition is optimally tuned to gamma while distal dendritic inhibition is optimally tuned to beta." This sentence integrates two hypotheses (`hypothesis-distinct-compartmental-roles` and `hypothesis-frequency-compartment-matching`) into a framing that previews the paper's structure. Concatenating the two short-form claims would name the hypotheses without integrating them; the reader would have to do the synthesis.

Second, the claims field is selective. A paper with 30 empirical claims cannot surface all 30 in a 70-word summary; the author chooses which carry the central evidentiary load. This is a judgment that requires reading the claim graph as an argument rather than as a list. The synthesis pipeline (Section 7) does the same selection for a different purpose — articulating the full argumentative structure rather than the headline.

The two pipelines are complementary: paper summaries are written for a reader who wants to understand the paper without traversing the graph; synthesis is written to test whether the graph alone carries the paper's argument.

[↑ Contents](#contents)

---
