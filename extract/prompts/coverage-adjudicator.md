You are sorting spans of a scientific paper that an automated coverage check could not match
to any claim in that paper's claim tree.

The automated check matched a span to a claim only when the claim literally restates a
statistic found in the span, or names the same figure panel. That test is deliberately
mechanical, so it produces two kinds of false alarm alongside the real gaps. Your job is to
separate them.

For each span, decide which ONE of these it is:

- `covered` — a claim in the tree does account for this span's content; the check could not
  see it, usually because the claim states the effect without repeating the numbers. Name the
  claim slug.
- `gap` — no claim in the tree accounts for this. A real hole in the corpus.
- `no-assertion` — the span states no result of its own. This covers pure cross-references
  ("see Appendix 1—table 4"), analysis narration, bare panel labels, graphical-encoding notes
  ("error bars represent SEM", "each coloured dot is one recovered parameter"), and raw table
  rows or column headers, which are data rather than a stated finding.

## Rules

Judge on meaning, not on wording. A claim that says "participants were less happy after a
partner's loss when they had chosen" covers a span reporting the interaction statistic for
exactly that effect, even though no digits are shared.

Do not stretch. If a claim is about a different condition, a different region, or a different
direction of effect, that is a gap, not a match.

**When genuinely torn between `covered` and `gap`, say `gap`.** The purpose of the exercise is
to find holes, and a false `covered` hides one where a false `gap` only costs a second look.

Captions and tables need a distinction the Results section does not. A caption sentence that
DESCRIBES what a panel displays is asserting a finding — judge it `covered` or `gap`. A caption
sentence that only explains the GRAPHICAL ENCODING asserts nothing about the world, and is
`no-assertion`. A raw table row is `no-assertion` — unless that row is the only place a
specific reported result appears, in which case it is a `gap`, and say which result it carries.

## Output

A JSON array, one object per span, no prose and no markdown fences:

    [{"uid": "results-026", "verdict": "gap", "claim": null, "why": "one short sentence"}]

`claim` is the slug for a `covered` verdict and null otherwise. `why` is one sentence
explaining the verdict — it becomes the body of the mark written into the paper, so write it
for a reader who will see it beside the sentence it judges.
