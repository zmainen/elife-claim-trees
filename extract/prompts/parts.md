# Parts

You are reading one paper's claim tree to find its **parts**: claims that are components of
other claims. A claim tree has two grains. The coarse grain is the argument a reader of the
paper follows; the fine grain is every comparison, condition, measure and study the prose
states on the way to it. A **part** is a claim at the fine grain that belongs to one at the
coarse grain, and the format now carries both, so neither has to be thrown away. The vocabulary
that follows this task defines `part-of`.

In short: a claim is **part of** another when it states one comparison, one condition, one
measure or one study of a proposition the other states as a whole, and dropping it would weaken
that whole without falsifying it. The whole already says what the part establishes; the part
carries the panel and the number that establish it.

## What you are given

The paper's claims — each as a slug, its role, the panel it rests on, its sentence, and the
typed edges it already carries. The graph half-says composition already: a part usually carries
a `supports` or a `tests` edge into the claim it is a component of. Treat that as a cue, not the
test — an independent finding can support a claim without being a part of it, and that is the
distinction `part-of` exists to draw. Apply the definition, not the edge.

## What to find

For every claim that is a component of another under the definition, the whole it is a part of.

- The whole is another claim **in this same tree**, named by its slug. Do not invent slugs.
- A part points at exactly **one** whole. If a claim seems to compose two, it composes the
  narrower one; if neither is narrower, it is probably not a part.
- A part is not the same claim as its whole, and the edges may not form a cycle: follow the
  chain of wholes upward and it must end.
- A part may itself be a whole for a finer part. Do not force a tree to one level, and do not
  manufacture a second level where the prose states none.
- Most claims are wholes. A claim that states an independent finding, a hypothesis, a
  prediction, a scope condition or a control in its own right is not a part — leave it out.

## What to return

A single JSON object and nothing else — no prose before or after, no code fence:

```json
{
  "parts": [
    {"part": "<slug>", "whole": "<slug>", "why": "one sentence: the comparison, condition, measure or study this states of the whole"}
  ]
}
```

Return only the parts you find. A tree with no parts returns `{"parts": []}`.
