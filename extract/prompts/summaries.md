# Paper summary

You are writing the summary that sits at the top of a paper's page — three paragraphs of prose,
written from the paper's **claim graph** and nothing else. It is probably the most-read thing
the corpus produces: a reader meets it before the claim tree, the abstract or the paper. Write
it to be read on its own, without traversing the graph. The vocabulary that follows this task
defines the roles the claims carry, which is what the three paragraphs are built from.

## What you are given

The paper's claims — each as a slug, its role, the panel it rests on, its sentence as the
corpus records it (the authors' own wording), and the typed edges it carries. You are not given
the abstract or the prose. The graph is the whole of what you have, and the summary is a test of
whether it carries the paper.

## What to write

Three paragraphs, roughly 150–220 words in total, each a field of the returned object:

- **`hypotheses`** — what the paper set out to test or argue: the bets the rest of the work
  makes good on. Built from the `role: hypothesis` claims and the alternatives (`alt-` slugs)
  they compete with. Integrate them into a framing that previews the paper's structure — do not
  list them. This paragraph frames; it does not yet report.
- **`claims`** — what the paper actually establishes empirically. Built from the `role: empirical`
  and `role: control` claims, and the `role: prediction` claims where the graph closes the
  prediction–test loop. It is selective: a paper with thirty empirical claims cannot surface all
  thirty here, so choose the ones that carry the central evidentiary load and say what the
  others rest on. This is the body of evidence.
- **`inferences`** — what the paper concludes and what it says those conclusions imply. Built
  from the `role: synthesis` and `role: interpretation` claims, and the `role: scope` claims
  that condition them. The interpretive layer: what the evidence is taken to mean, and the
  caveats every claim inherits.

The three map onto motivation → evidence → interpretation, but they are not summaries of three
sections. A claim named in `inferences` may rest on an empirical result named in `claims`; the
same evidence appears at different levels of generality.

- Compose, do not concatenate. Two hypotheses become one framing sentence, not two restated
  claim sentences side by side. The reader should not have to do the synthesis you were asked
  for.
- Honour the roles. Do not promote an interpretation into the `claims` paragraph or an empirical
  result into `inferences`. Where an edge says a result `refutes` a hypothesis or `rules-out` an
  alternative, say so — the eliminative move is the paper's argument, not a footnote.
- Say what was found, in the authors' terms, without hedging ("may suggest") or inflating
  ("demonstrates conclusively"). A null result is a null result.

## Atlas and observational papers — `subject` in place of `hypotheses`

A paper with no hypothesis structure — an atlas, a resource, a descriptive survey, recognisable
by having no `role: hypothesis` claims — is not testing anything, and a `hypotheses` paragraph
would invent a bet it never made. For such a paper, return **`subject`** instead of
`hypotheses`: what the work is a reference for — the system, the method, and what it maps. The
`claims` and `inferences` paragraphs are unchanged. Return exactly one of `hypotheses` or
`subject`, never both.

## What to return

A single JSON object and nothing else — no prose before or after, no code fence:

```json
{
  "hypotheses": "The paper tests whether …, whether …, and whether ….",
  "claims": "Across an fMRI study and a behavioural replication, …",
  "inferences": "The convergence of behavioural, computational and neural evidence …"
}
```

Three string fields: `hypotheses` (or `subject`), `claims`, `inferences`. No slugs, no lists,
no markdown inside the strings.
