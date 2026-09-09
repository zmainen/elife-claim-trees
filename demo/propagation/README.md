# Claim Change Propagation Demo

A tool showing how a correction to one claim in a scientific paper propagates through the paper's dependency graph to invalidate or weaken downstream claims.

## Why this matters for editorial decision-making

When a paper makes a correction — whether a revised parameter value, a re-analysis of a figure, or a methodological retraction — editors currently have no systematic way to trace which other conclusions in the paper are affected. A correction to figure 2 may seem minor, but if other claims depend on it, those claims inherit the correction's uncertainty. The blast radius of a change is the number of claims that can no longer be taken at face value without re-checking.

This tool makes that blast radius explicit. It answers the question: *if this claim changes, how much of the paper's argument is at risk?*

## Demo paper

The demo uses **Headley et al. 2026** (*eLife* 95562): "Spatially targeted inhibitory rhythms differentially affect neuronal integration." This paper models how beta-frequency inhibition at distal dendrites and gamma-frequency inhibition at perisomatic locations independently gate different input pathways in a layer 5 pyramidal neuron.

The paper was chosen because it has the richest dependency structure in the current 10-paper corpus — 50 typed dependency relations across 17 claims. Its key architectural claim (`l5-model-single-cell-scope`) is required by 14 of 17 claims, giving it a blast radius of 15/17 — essentially the entire paper.

## Files

| File | Description |
|:-----|:------------|
| `demo.html` | Standalone interactive visual (open directly in browser, no server needed) |
| `propagate.py` | CLI tool for any paper in the corpus |

## Using the visual demo

Open `demo.html` in any modern browser. The graph shows all 17 claims laid out left-to-right by type:

- **Assessment claims** (leftmost) — model scope and parameterization assumptions
- **Empirical claims** (middle) — direct results from simulations
- **Interpretive claim** (rightmost) — the PV/gamma–SST/beta correspondence conclusion

Click any node or use the dropdown to change which claim is "changed." The blast radius updates immediately:

- **Orange** — the changed claim
- **Red** — claims directly depending on it
- **Light red** — transitively affected claims (depend on claims that depend on the changed claim)
- **Grey** — unaffected claims
- **Blue border** — assessment claims (model assumptions)

The sidebar shows the blast radius count, direct vs. transitive breakdown, and flags when interpretive or synthesis claims are in the blast radius.

## Using the CLI

```bash
cd elife-claim-trees
python demo/propagation/propagate.py --paper headley-2026-inhibitory-rhythms --claim l5-model-single-cell-scope
```

Available papers: any directory under `claims/`. Available claims: any `.md` file in that directory (excluding `index.md`).

```bash
# JSON output for programmatic use
python demo/propagation/propagate.py \
  --paper headley-2026-inhibitory-rhythms \
  --claim naturalistic-drive-parameterization \
  --output json
```

## The key finding

The `l5-model-single-cell-scope` claim is an *assessment* claim — it registers a known limitation of the model (single-cell scope, no network dynamics). Because 14 empirical claims explicitly require this assessment, any editorial challenge to the model's scope (e.g., "these results may not hold in a network context") immediately propagates to the interpretive conclusion linking PV+ cells to gamma and SST+ cells to beta. The blast radius is 15 of 17 claims — 88% of the paper's argument.

This is not a flaw in the paper. It reflects the fact that all results in a single-paper modeling study necessarily inherit the model's scope. The claim graph makes that inheritance explicit rather than leaving it implicit. An editor can see, at a glance, that a correction to the model scope is not a minor change — it touches the entire argument.

## Dependency relation types

| Relation | Meaning | Propagation direction |
|:---------|:--------|:----------------------|
| `requires` | Claim A is invalid if B is wrong | B changes → A affected |
| `extends` | Claim A builds on B | B changes → A affected |
| `supports` | Claim A provides evidence for B | A changes → B loses support |
| `contradicts` | Claims are in direct tension | Not propagated in this demo |
