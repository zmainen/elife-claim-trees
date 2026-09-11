The matcher was one Claude Opus 5 subagent per tree, unreviewed.
The baseline this compares to is experiments/2026-09-11-gadeke-subagent-rerun/ (old prompts, Opus everywhere: 97 claims, 173 edges, 27 of 33 recovered, role 85%, panel 30%, 70 extras).
Evaluation is not yet a declared layer (item 7 of docs/design/2026-09-11-reading-the-paper-better.md).

## v2 (Sonnet readers)

  committed 33   re-run 63

  RECOVERY  25/33 = 76%
  ROLE      19/25 = 76% of matched pairs
  PANEL     10/25 = 40% of matched pairs

  committed claims the re-run did not recover (8):
    hypothesis         alt-agency-aversion-not-guilt
    hypothesis         alt-guilt-effect-driven-by-own-outcome
    hypothesis         alt-imaging-contrast-invalid
    hypothesis         alt-model-based-glm-invalid
    hypothesis         alt-participants-insensitive-to-value
    hypothesis         alt-social-context-shifts-risk-attitude
    prediction         prediction-responsibility-model-wins-comparison
    scope              scope-two-study-design

  re-run claims with no committed counterpart: 38

  role disagreements on matched pairs (6):
    hypothesis         → interpretation     hypothesis-insula-tracks-interpersonal-guilt
    hypothesis         → interpretation     hypothesis-sts-mentalizes-partner-state-unde
    interpretation     → empirical          insula-guilt-replicates-yu-koban-signature
    control            → empirical          lottery-choice-increases-with-ev
    scope              → methodological     partner-algorithm-deception-assumption
    control            → empirical          ventral-striatum-tracks-risky-choices

## v3 (Opus everywhere)

  committed 33   re-run 68

  RECOVERY  26/33 = 79%
  ROLE      20/26 = 77% of matched pairs
  PANEL     6/26 = 23% of matched pairs

  committed claims the re-run did not recover (7):
    hypothesis         alt-guilt-effect-driven-by-own-outcome
    hypothesis         alt-imaging-contrast-invalid
    hypothesis         alt-model-based-glm-invalid
    hypothesis         alt-participants-insensitive-to-value
    hypothesis         alt-social-context-shifts-risk-attitude
    hypothesis         hypothesis-responsibility-weights-partner-rpes
    literature-context interprets-yu-koban-guilt-signature

  re-run claims with no committed counterpart: 42

  role disagreements on matched pairs (6):
    hypothesis         → interpretation     alt-agency-aversion-not-guilt
    empirical          → control            guilt-signature-no-individual-difference
    hypothesis         → interpretation     hypothesis-sts-mentalizes-partner-state-unde
    interpretation     → control            insula-guilt-replicates-yu-koban-signature
    empirical          → interpretation     insula-ifg-connectivity-guilt
    scope              → methodological     partner-algorithm-deception-assumption
