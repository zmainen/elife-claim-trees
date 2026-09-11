The steps above produce a claim tree and check the claims in it. They do not ask the opposite
question, and until recently nothing did: what does the paper assert that no claim
represents? That gap is not hypothetical. Figure 2's panels C and F in Gädeke — a failed
replication of a risk-aversion effect — sat unrepresented in the tree, and nothing in the
pipeline registered their absence, because every check ran over the claims rather than over
the paper.

`elife-extract coverage --paper <paper-slug>` takes its denominator
from the paper instead. It builds the paper's own inventories — every figure panel, every
table, every reported statistic — and then cuts the entire text into **spans** (one sentence
each) and asks, of every span, whether any claim accounts for it. No sampling, and no model
calls, so it is free and fast enough to run over the whole corpus. `--fail-on-orphans` makes
it a gate.

A *span* is the unit of measurement here, and the word is deliberate: not "unit", which
collides with units of measurement in a paper made of statistics. Each span carries the
statistics and panel references detected in it, and is either accounted for by a claim or
not — and "not" is then a fact about the paper rather than about a pattern.

**The mechanical pass cannot finish the job, and should not pretend to.** "Accounted for"
means a claim restates the same statistic or names the same panel. That is a proxy for the
question that matters and it is wrong in both directions: the paper reports `t(1180) = 3.52,
p = 0.0004` and a claim states exactly that effect without repeating the numbers, which
scores as a miss; meanwhile a sentence whose only content is "see Appendix 1—table 4" scores
as an unmet obligation though it asserts nothing at all.

So the residue is **adjudicated**, not matched harder. Every span the mechanical pass could
not resolve gets one of three verdicts:

| verdict | meaning |
|---|---|
| `covered` | a claim does account for it; the matcher could not see it |
| `gap` | nothing in the tree accounts for it — a real hole |
| `not-an-assertion` | the span states no result: a cross-reference, analysis narration, a bare panel label, a graphical-encoding note ("error bars are SEM"), or a raw table row |

Verdicts live in `mappings/<paper-slug>.json` — stored, not recomputed, so they can be
audited and disagreed with — and `coverage --mapping` folds them back in. The point of
keeping the three apart is that lumping the third into the orphan list buries the real gaps
in bookkeeping.

**Gädeke, fully resolved against the curated tree:** 245 spans segmented; 78 carrying a
statistic or naming a panel; 64 accounted for (82%); 15 adjudicated as asserting no result;
**14 real gaps** (10 in Results, 1 in captions, 3 in tables). Nothing left unexamined.

Two findings came out of that exercise which matter beyond this paper.

The gaps are not scattered — they **cluster on the paper's own hedges**. Results the paper
reports and then walks back (the Study 1 risk-aversion effect that fails to replicate in
Study 2 — Figure 2C/2F — and two IFG clusters that do not survive correction), boundary
conditions showing where an effect stops (a null interaction; no responsibility effect after
*positive* partner outcomes), and follow-up analyses narrowing whole-brain contrasts to
particular regions. The tree keeps what the paper commits to and loses the qualifications
that bound it, which makes its central claim read broader than the data support.

And **the appendix tables carry analyses the prose never states.** Three of the four table
gaps exist only there: the decision-phase condition effects in ventral striatum and mPFC, the
entire Social-vs-Partner comparison at that phase, and the outcome-phase risky-vs-safe
contrast that defines the paper's own regions of interest. One of them qualifies the prose's
"irrespective of Social or Solo condition" framing rather than merely supplementing it.
Reading captions and tables is therefore not thoroughness — it is a different *source* of
claims, and a tree built from prose alone will miss all of it.
