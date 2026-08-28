# 5388 — Y5/R2FR D4 subtraction double-pole zero

## Decision

`SUBTRACTION_DOUBLE_POLE_COEFFICIENT_IDENTICALLY_ZERO__DIRECT_TERM_OWNS_H`

## Derivation

The finite-plus endpoint subtraction is not silently discarded. Checkpoint 5019 proves that its crossed azimuth singularities are simple poles. Checkpoint 5385 identifies exactly one subtraction root at the selected global center and excludes the other seven subtraction roots throughout the base complex strip.

This checkpoint repeats the seven-root exclusion on both complex endpoint halos for every one of the 32 expanded energy-contour arcs. A meromorphic term with at most a simple pole at z=z_star has Laurent form a_-1/(z-z_star)+sum_(n>=0) a_n(z-z_star)^n. Its (z-z_star)^-2 coefficient is therefore exactly zero, so the endpoint subtraction contributes zero to H_k.

- halo boxes: `16`;
- halo energy arcs: `512`;
- checked nonactive subtraction-root rows: `112`;
- minimum halo subtraction-root clearance: `0.0039060445855235823`.

## Scope

The result removes only the subtraction term from the global double-pole coefficient. It does not remove the subtraction from other finite coefficients, G3, W3, or the full integral. H3 remains false until the direct nested-contour matrix and Cauchy aggregation pass.
