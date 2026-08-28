# 5397 — D4 selector-transition chart-union gate

## Purpose

Checkpoint 5396 closes five complete support-cell contour certificates but reproduces `15/558` pointwise changes from a mapped-cell midpoint selector. All changed states are already contained in the exact representative/reciprocal state set of the parent algebraic selector, but point probes cannot make a midpoint state globally own a closed cell.

This checkpoint tests the non-closure route. For each reduced term let `C` be the finite parent-declared chart set and let the physical selector choose `sigma(p) in C`. If a closed box supplies

\[
|I_c(p)|\le B_c\qquad(c\in C),
\]

then, pointwise and without assuming `sigma` is constant,

\[
|I_{\sigma(p)}(p)|\le \max_{c\in C}B_c.
\]

The production evaluator already implements `max` for wholly pointwise chart bounds and a conservative sum if any chart uses an integrated simple-pole route. Checkpoint 5397 tests that complete finite-union path rather than declaring a plateau or midpoint-selector closure.

## Gates

- Reproduce exactly the `15` historical transition probes.
- Require every observed state to be a declared chart variant.
- Evaluate every declared chart at every transition probe and compare it with the parent residue.
- Exercise both charts together on small closed boxes in every affected mapped-cell/term pair.
- Keep `valid_for_atlas_migration=false` until completed v39 one-chart rows receive a closed two-chart backfill or a closed pre-transition unit-margin proof.

## Claim boundary

Passing the algorithm gate proves that selector transitions can be bounded without assigning a midpoint state to a whole box. It does not automatically upgrade completed v39 rows, certify every mapped cell, close the full regular-away atlas, or establish any UV, local-GR, or full-MTS claim.

## Result

- Historical transition probes: `15/558`, across six mapped-cell/term pairs.
- Declared chart evaluations: `30/30`; all reproduce the parent residue.
- Maximum chart-to-parent relative error: `9.896273991134421e-10`.
- Closed two-chart smokes: `6/6`, with zero failures.
- Algorithm gate: **PASS**.
- Direct atlas migration at this checkpoint: **BLOCKED**, correctly deferred to 5398-5399.
