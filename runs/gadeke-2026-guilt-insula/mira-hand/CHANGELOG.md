# Gädeke MIRA graph — changelog

One entry per version that reaches the delivered page. Version = major.minor.patch: major for a
change of schema or subclasses, minor for nodes or edges added or removed, patch for wording,
summaries, anchors or the page. Each version is a commit tagged `gadeke-mira-v<version>`; the
version and date are fields of the JSON and the JSON-LD stamps and appear on the page.

## 1.0.0 — 2026-10-28

First delivered version. Consolidates the work of 16–28 October:

- 2026-10-16 — hand-built graph against the Reviewed Preprint v2 text, with Hypothesis,
  Alternative and Check subclasses; questions lifted a level, Q3 merged into Q2, figures linked.
- 2026-10-26 — plain summaries on every node; findings reach a question; verifier and viewer;
  cited works collapsed to SourceDocument + Evidence; alignment to eLife's July prototype;
  the six shared findings keep eLife's wording; the IFG reading becomes its own claim.
- 2026-10-27 — typed ids (Q H F A E K C R S P D); Cited subtype; cited works C1–C4 with
  reference entries and DOIs as IRIs; the IFG claim supports H3 and nests under F9; second
  anchors in the abstract for the six main findings; viewer redesigned in the Pathways
  prototype's language (section list, article and claims side by side, figures inline,
  connector lines, internal views folded away); delivery page with About, cleaned JSON and
  JSON-LD.
- 2026-10-28 — About page as plain facts; every figure embedded; edge lines as chip triples with
  hover statements; no sidecar files, one-file export; version and date in the graph and page.

## 1.0.1 — 2026-10-28

- A `stats` block in the JSON (nodes and edges by type, subtype and relation; panels covered) and a
  Contents table on the About page.

## 1.0.2 — 2026-10-28

- The key in the left margin becomes a Contents panel: each kind with its count, plus studies,
  protocols and edges. The Contents table leaves the About page.

## 1.0.3 — 2026-10-28

- The Contents panel shows the structure: claims with their three subtypes, evidence with its three,
  then cited works and requests.

## 1.0.4 — 2026-10-28

- Contents panel formatting: aligned chip, label and count columns; group rows for claims and
  evidence; studies, protocols and edges as rows; wider margin.

## 1.1.0 — 2026-10-28

- Layout: the left margin holds only the section list. The right column gets a toolbar (Claims ·
  About · Data, collapse all) and a one-line key beneath it. Counts live in the About page's Contents
  table and in each question's header (hypotheses · findings · alternatives).
