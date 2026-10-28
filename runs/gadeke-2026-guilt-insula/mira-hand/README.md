# Gädeke 2026 — hand-built MIRA graph (Reviewed Preprint v2)

**Graph version 1.0, 2026-10-28** — the version delivered to eLife (git tag `gadeke-mira-v1.0`).
The version and date are fields of the JSON (`version`, `date`) and of the JSON-LD's provenance
stamps; bump the version in `gadeke_hand.py` on any change to nodes or edges after delivery.

Built 2026-10-16 for eLife Pathways' claims-tree prototype and for adjudication, from the text
their page serves (`gadeke-v2.txt`, flattened from the article content of
https://epp.elifepathways.org/mira/105391, msid 105391v2), so every anchor docks to it.

- `gadeke_hand.py` — the specification: every node with its statement, plain summary, study, panel
  and anchor, and every edge; also the builder, which refuses to emit if any anchor is not
  character-for-character in the text, any edge breaks MIRA's grammar, or a figure panel is unaccounted for.
- `gadeke-hand.graph.json` — the extractor's working-graph shape (what the prototype ingests), plus
  `subtypes`, a figure-panel `coverage` table and `figures` (IIIF image, thumbnail and page link per
  panel). Beyond the extractor's fields, nodes carry `description` (the plain summary), `anchor`
  (verbatim in `gadeke-v2.txt`), optional `anchors` (further verbatim passages: the six main findings
  are also anchored in the abstract), `panel`, `study`, `figure`, `notes`, `key` (the builder's
  mnemonic) and, on evidence, `sourceDocument`.
- `gadeke-hand.verification.json` — `mira_verify.py`'s verdict per node and edge (97 of 97 pass).
- `gadeke-hand.viewer.html` — the review page, self-contained, built by `mira_viewer.py` with
  `--compare` and `--embed-figures` (figure thumbnails cached in `.figcache/`, gitignored). Published
  at https://claude.ai/artifact/2hV3hPEa8P1tgkVuzCrsHJ; feedback goes in comments on that page.
- `gadeke-hand.deliver.html` / `gadeke-hand.deliver.graph.json` — the page for eLife, built with
  `--deliver`, published at https://claude.ai/artifact/5AFpgCyeGQXKbCZzAUe1M6 (private until shared).
  Same reading surface as the review page; the Data item in the margin opens About this graph
  (facts only: what it is, who built and reviewed it, what is in it, the four subclasses, the checks,
  the two files), the cleaned JSON (no `key`, no coverage table, a `fields` block naming the extra
  fields; the same file written beside the page) and the MIRA JSON-LD. No comparison, no
  verification table. One self-contained file: article text, graph, figure thumbnails and JSON-LD
  are embedded, so the artifact exports as one HTML file. (`fig/` holds copies of the thumbnails,
  gitignored; the page would fall back to them if a host refused embedded images, but they are not
  published, since sidecar files turn the export into a zip.)
- `gadeke-hand.mira.jsonld` — MIRA JSON-LD with three declared `NodeSchema` subclasses: `Hypothesis`
  and `Alternative` under Claim, `Check` and `Cited` under Evidence. Against the vendored shapes it raises only
  the known upstream `sh:in` violations and the closed `prov:Activity` shape's refusal of
  `title`/`description` on Study nodes (4, one pair per Study), both documented upstream.

97 nodes · 162 edges · 2 Questions · 4 Hypotheses · 14 findings + 1 interpretation (c_ifg) · 6 Alternatives (13 `opposes`) ·
47 Evidence of which 8 Checks and 4 Cited · 2 Studies · 10 Protocols · 5 SourceDocuments (the paper D1
+ 4 cited works C1–C4, each with its reference-list entry and DOI) · 6 Requests. A cited finding is Evidence whose `sourceDocument` is the cited work;
no placeholder Study is minted for it.

- Node ids are typed and short (Q1, H1–H4, F1–F15, A1–A6, E1–E39 (four of them Cited), K1–K8, C1–C4 cited works, R1–R6, S1–S2, P1–P10, D1–D5) so
  reviewers can cite them; each node keeps its mnemonic from the builder as `key`.
- `alignment-prototype.map.json` / `alignment-prototype.json` — hand map and computed alignment to
  eLife's prototype graph (`../mira-baseline/elife-prototype-2026-07.graph.json`), from
  `mira_align.py`; drives the viewer's "Compared with prototype" view and the `= g3` marks on rows.
  33 of their 34 nodes have a counterpart; the one left is their risk-preferences Question, which is
  a finding here.
Every anchor verbatim in v2; all 27 panels of Figures 1–5, Table 1 and Supplementary Figure 2 covered.

Under adjudication (27 Oct). Settled so far: the six findings shared with the prototype keep its
wording; the authors' IFG reading is its own claim (F10) under F9; cited works are C1–C4 with their
reference-list entries and DOIs, their findings `Cited` evidence; interpretations stay in summaries
unless the authors state them as claims. Open: the texts of the alternatives and whether the brain
question should carry alternatives of its own.
