# 5440: collision-Jacobian finite-subcover gate

## Decision

**THE COLLISION-JACOBIAN ZERO IS A COARSE PATH-INTERVAL ARTIFACT ON THIS CELL.**

The corrected probe uses the actual `MC04_SP_DP` representative configuration (`minus_u`), not the inapplicable explicit `minus_v` chart used by the quarantined exploratory pre-probe.

## Exact cover law

Let the compact parameter cell be the finite union `D = union_i D_i`. If interval evaluation proves `J(D_i) subset B_i` and `0 notin B_i` for every leaf, then

`inf_{z in D} |J(z)| >= min_i dist(0, B_i) > 0`.

Taking one rectangular hull of all `B_i` is stronger than this theorem requires and can fill gaps between disconnected image boxes. Here the stronger test also closes after path-only refinement: the `8 x 64` rectangular hull excludes zero, whereas the parent's terminal `8 x 32` cover did not.

## Certified cell

- Path: `LRDRDRDLDLDRDL` at depth 14.
- Domain: `x in [0.3327414652067662, 0.33289508839506887]`, `t in [0.0, 0.015625]`.
- Cover: `8 x 64` = 512 leaves.
- Leaf-union `|J|` lower bound: `30.531983832901787`.
- Chart-denominator lower bound: `0.0044188968307068205`.
- Selected-cover rectangular-hull `|J|` lower bound: `23.79315214956054`.

## Claim boundary

This proves only the local collision-Jacobian finite subcover needed by the active right-connector cell. Parent integration and a resumed production advance are still required; no W3, UV, local-GR, or full-MTS claim is made.
