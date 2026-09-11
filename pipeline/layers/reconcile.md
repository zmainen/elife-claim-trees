Compare the three extraction lists. For each candidate claim:

- If all three agree: high confidence. Include.
- If two agree, one differs: flag the discrepancy. Note which agent and why.
- If agents find different claims: add all candidates, flagged as single-source.

The reconciled list carries a confidence column (high / contested / single-source). This is what goes to the review gate, `external-review`.

## Common errors in claim extraction

Instruct all extraction agents to avoid the following ten failure modes. These are preserved from the original methodology because they continue to describe the actual mistakes the prototype's extraction agents make.

1. **Inferring results from mechanism.** Code and methods describe how something was computed. They do not describe what was found. Never report a mechanism as a result. If the paper's text is unavailable, stop and flag it — do not fall back to code analysis and present the output as paper-grounded.

2. **Reversing direction.** Saturation, inhibition, and feedback effects frequently reverse naive intuitions. A higher concentration of X at a site does not always mean faster processing — saturation slows it. Always read the paper's stated direction; never infer it from the mechanism alone.

3. **Quantitative hallucination.** Do not add specific numbers (percentages, milliseconds, effect sizes) that do not appear verbatim in the paper's text or captions. If the paper says "large fraction," write "large fraction." If you cannot find the number in the text, do not invent it.

4. **Wrong panel assignment.** Do not assume a claim belongs to a panel without verifying. Schematics, cartoons, and parameter-sweep diagrams (often panels A or D) set up a hypothesis — they do not assert a result. A result is in the panel that shows the data or simulation output.

5. **Overstating strength.** "Necessary and sufficient," "proves," "demonstrates definitively" — these are almost never the paper's language. Use the paper's own epistemic framing. If the paper says "consistent with," do not write "shows."

6. **Discussion contamination.** The discussion introduces speculative interpretations and broader implications that the figures do not directly support. Claims must be grounded in results sections and captions, not discussion. Synthesis and interpretation claims are the proper place for paper-level inferential moves; mark them as such with `role: synthesis` or `role: interpretation` rather than mixing them into empirical claims.

7. **Simulation vs experiment conflation.** Clearly distinguish model predictions from experimental measurements. A simulation result is a model prediction, conditional on the model's assumptions and parameterisation. An experimental result is a measurement. They have different epistemic statuses.

8. **Missing negative results.** "X does not explain Y" and "varying parameter P produces no regional difference" are real claims. Do not skip panels that show null or negative results — these often carry `rules-out` edges that are load-bearing in the paper's argument and that downstream pipelines (the synthesis comparator) treat as diagnostic.

9. **Methodological panels as claims.** Panels that show model architecture, parameter schematics, or technique illustrations do not assert claims about the world. They register as `role: methodological` (or `role: scope` if they bound the interpretation of empirical claims) rather than as empirical claims.

10. **Single-source overconfidence.** If only one reading strategy surfaces a claim, it may be real but buried — or it may be an artefact of the reading strategy. Flag it as single-source rather than presenting it with the same confidence as a claim found by all three agents.
