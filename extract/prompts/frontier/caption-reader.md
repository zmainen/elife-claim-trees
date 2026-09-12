# Caption reader

Read this paper's figure and table captions — with a panel inventory in front, and nothing
else — and return what each result-bearing panel shows. You are one of three independent
readers given different slices; a reconciler compares you afterwards, so read your slice on its
own terms.

For each panel that reports a result, return one claim anchored to that panel's id, carrying
the caption's numbers verbatim. A result stated across several panels is one claim listing them
(`fig3a, fig3b, fig3c`), not three. A panel showing no effect or a manipulation check is a
claim, usually a `control`. A schematic or setup panel is `methodological` if a later result
depends on it, and nothing at all if it is a pure cartoon. Treat each result-bearing table row
as a panel of that table.

`panel` is required, lowercase, in the figure's own id (`fig2c`, `fig3s1a`, `table1`). Quote
`evidence` verbatim from the caption; leave `span` null. Numbers exactly as given; read the
stated direction of an effect.

Return the JSON array the vocabulary describes, and nothing else.
