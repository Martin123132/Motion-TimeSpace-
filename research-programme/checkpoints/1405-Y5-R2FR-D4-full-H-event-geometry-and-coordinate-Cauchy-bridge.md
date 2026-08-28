# 5389 — D4 full-H event geometry and coordinate-Cauchy bridge

## Decision

`FULL_H_EVENT_GEOMETRY_AND_COORDINATE_CAUCHY_BRIDGE_CERTIFIED__RUN_RESERVED_OUTER_C0_SWEEP`

## Derived bridge

The production 5386 sweep contracts each already-certified 5380 image as far as strict inclusion permits. For the full-H proof, its first additional contraction is deliberately held in reserve: `C0` is evaluated on the uncontracted 5386 source box, while the first strict image contains the complete event branch. The componentwise gap between those two boxes is therefore usable rather than decorative.

The regulator proof uses the holomorphic two-component material system `(P_u,P_v)=0`, not an illicit real/imaginary conjugacy assumption. Its `2x2` Jacobian in `(u,v)` is inverted interval-wise to enclose `u_x` and `v_x`; the older shorthand `R_x=-P_x/P_R` is retained only as a cross-check. At support contacts the other dependent coordinates obey `S_x=-sigma x/S` and `H_x=-B_x/B_H`. Each coordinate radius is chosen below the inner-to-outer coordinate margin and below every dependent-component margin divided by its derivative supremum. A first-exit argument then keeps the complete analytic event branch `(u,v,H,S)` inside the exact outer box already used by checkpoint 5386; branch-death rows require only `(u,v)`, with the nonvanishing square-root branch checked separately.

On the event branch, the algebraic contact equation removes the correlated real part of the boundary gap exactly, giving `z0=2 i u v` for `R=u+i v`. The boundary-gap derivative is

- branch death: `z1=sigma 2 R R_x`;
- support contact: `z1=2 R R_x-2 H H_x`, with `H_x=-B_x/B_H`.

All `80` base/endpoint-halo boxes exclude `P_R=0`, `z1=0`, the soft-sine zero, and (where present) `B_H=0` on the reserved outer boxes. The minimum certified complete-branch coordinate-Cauchy radius is `5.632403328656323e-14` and the maximum `|z0/z1|` bound is `6.476808095256514e-05`.

The `72` adjacent-bin seams are separately patched: the two strict branch images are enclosed in one hull and a new strict Krawczyk certificate proves that hull contains one root. This identifies the left and right local branches, including the finite-width endpoint-halo overlaps, so the regulator strip is one analytic branch rather than an unproved union of boxes. The minimum seam inclusion margin is `5.738271367602491e-16`.

## Consequence

Once a reserved-outer 5386 arc sweep is grouped into a physical `C0` bound `M0` for each box, the same outer enclosure and the radius `rho_x` give `|C1| <= M0/rho_x`. The full affine endpoint coefficient is then bounded without a fitted derivative by `|H| <= M0 |z0/z1| + (M0/(2 rho_x)) |z0/z1|^2`.

This checkpoint certifies that bridge only. It does not claim the full-H or H3 bound until the completed 5386 rows are consumed, and it does not claim the total uniform remainder, D4 outer limit, local GR, or full MTS.
