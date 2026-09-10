---
uuid: ae5f131c-edc3-4345-96c1-2f43609dbb3e
slug: a421v-spatial-learning-working-memory-impaired
doi: ~
claim: >
  Young adult Kcnc1-A421V/+ mice (P35–65) exhibit significantly longer escape latencies
  during Barnes maze acquisition (most pronounced on day 2) and a significantly reduced
  percentage of spontaneous alternations in the Y-maze, indicating impairment in both
  spatial learning and spatial working memory, with long-term memory retention intact.
claim-type: empirical
role: empirical
concepts:
  - cognitive function
  - spatial learning
  - working memory
  - Barnes maze
  - Y-maze
  - KCNC1
priority: 2026-03-30
epistemic: strong

tests:
  - prediction-cognitive-deficits
confirms:
  - prediction-cognitive-deficits
  - hypothesis-pv-dysfunction-drives-encephalopathy

belongings:
  - relation: requires
    target: inhibitory-dysfunction-progresses-to-adulthood

assertions:
  - paper-slug: wengert-2026-kcnc1
    doi: 10.7554/eLife.103784
    panel: fig2B, fig2C, fig2D
    figureUri: https://iiif.elifesciences.org/lax/103784%2Felife-103784-fig2-v1.tif/full/1500,/0/default.jpg
    scope: in-vivo
    analysis: G-Node analysis code
    dataset: https://doi.org/10.12751/g-node.bqni9h
    dataset-doi: 10.12751/g-node.bqni9h
    method: Barnes maze, Y-maze spontaneous alternation
    confidence: strong

reproductions:
  - agent: mainen-z
    date: 2026-03-30
    status: blocked
    blocked_by: no-data
    notes: >
      Behavioral data on G-Node. Statistics: two-way repeated-measures ANOVA with Tukey's
      post hoc (Barnes maze); unpaired t-test (Y-maze). Total arm entries and distance
      traveled are not different, ruling out locomotion or exploratory confounds.
---

The dissociation between impaired acquisition (day 2 latency) and intact probe trial
performance suggests a specific deficit in spatial learning rate rather than complete
inability to form memories. This is consistent with interneuron dysfunction slowing
learning dynamics rather than eliminating memory consolidation.
