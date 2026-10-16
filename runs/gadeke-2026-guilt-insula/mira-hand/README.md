# Gädeke 2026 — hand-built MIRA graph (Reviewed Preprint v2)

Built 2026-10-16 for eLife Pathways' claims-tree prototype and for adjudication, from the text
their page serves (`gadeke-v2.txt`, flattened from the article content of
https://epp.elifepathways.org/mira/105391, msid 105391v2), so every anchor docks to it.

- `gadeke_hand.py` — the specification: every node with its statement, plain summary, study, panel
  and anchor, and every edge; also the builder, which refuses to emit if any anchor is not
  character-for-character in the text, any edge breaks MIRA's grammar, or a figure panel is unaccounted for.
- `gadeke-hand.graph.json` — the extractor's working-graph shape (what the prototype ingests), plus
  `subtypes` and a figure-panel `coverage` table.
- `gadeke-hand.mira.jsonld` — MIRA JSON-LD with three declared `NodeSchema` subclasses: `Hypothesis`
  and `Alternative` under Claim, `Check` under Evidence. Against the vendored shapes it raises only
  the known upstream `sh:in` violations and the closed `prov:Activity` shape's refusal of
  `title`/`description` on Study nodes (12, one pair per Study), both documented upstream.

101 nodes · 163 edges · 3 Questions · 4 Hypotheses · 14 findings · 6 Alternatives (13 `opposes`) ·
47 Evidence of which 8 Checks · 6 Studies (2 + 4 cited) · 10 Protocols · 5 SourceDocuments · 6 Requests.
Every anchor verbatim in v2; all 27 panels of Figures 1–5, Table 1 and Supplementary Figure 2 covered.

Not yet adjudicated. Open for review: the texts of the findings and alternatives, the choice to keep
interpretations in descriptions rather than as Claims, and the cited works' DOIs (left unresolved;
`reference-check` can fill them).
