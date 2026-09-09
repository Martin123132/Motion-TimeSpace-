# 5433: finite outer chart-cover progress gate

## Decision

**PASS FOR COMMITTED FINITE-COVER PROGRESS ONLY.**

The unchanged v46 evaluator commits `13` additional boxes after the 5432 single-family rejection. `LLU` closes directly, and the adaptive ledger now resolves the LR projective transition by disjoint x/t boxes rather than by forcing one singular gauge.

## Saved frontier

Accepted boxes rise from `373` to `386`. The saved stack contains `13` boxes; every pending path remains inside `LR` or `R`, so no previously certified region was reopened.

## Numerical floor

Across the new certificates, the minimum amplitude-denominator lower bound is `0.0003980689012531889` and the minimum collision-Jacobian lower bound is `2.4465510128966415`.

## Interpretation

The broad-box obstruction is confirmed as projective-cover bookkeeping. It has not produced a terminal zero or a new failure class. Completion still requires exhausting the saved LR/R stack.

## Claim boundary

The right connector, regular-away W3, combined W3, regulator limit, UV, local-GR, and full-MTS claims remain false.
