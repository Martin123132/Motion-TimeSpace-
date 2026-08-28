# 5387 — Y5/R2FR D4 Cauchy endpoint halo

## Decision

`CAUCHY_ENDPOINT_HALO_CERTIFIED__RUN_NESTED_CONTOUR_ENCLOSURE`

## Certificate

- certified halo boxes: `16/16`;
- lower real halo: `(-1e-06, 1e-06)`;
- upper real halo: `(0.019999, 0.020001)`;
- imaginary half-width: `1e-06`;
- minimum strict Krawczyk inclusion margin: `3.188739723658518e-11`;
- maximum contraction bound: `0.004193964142243829`.

## Scope

These boxes extend the certified event branches far enough to place radius-5e-7 Cauchy circles around both real endpoints of [0,0.02]. They do not by themselves bound the finite-plus contour integrand or establish H3; those gates remain false until the contour sweep covers the halo rows.
