# 5266 — Soft-energy measure and energy-first pilot

## Derived measure

The parent Sobol generator owns the exact map `x=u_E`, `c_s=2u_s-1`, `c_d=2u_d-1`. Therefore

`du_E du_s du_d = dx (dc_s/2) (dc_d/2)`,

so the soft-energy Jacobian is exactly one and the only remaining coordinate factor is the already used angular Jacobian `1/4`. No energy weight has been fitted.

## Route tested

At fixed nonzero Feynman regulator the pilot changes the order of integration: it integrates the finite-plus kernel over `x` first at one angular witness. Every AAA-extracted interior pole is removed as `R/(x-p)` and restored with `R[Log(1-p)-Log(-p)]`.

## Results

- E040 post-quadrature integral gate passed: `False`.
- E020 post-quadrature integral gate passed: `False`.
- Common energy factorization rejected: `True`.
- Maximum normalized ratio spread: `2.5236659541377024`.
- Maximum inner-order artifact: `157.2095320773112`.
- Post-quadrature energy route rejected: `True`.

## Claim boundary

The candidate fixed-angle integral is explicitly invalid: its global AAA continuation and 32/64 Gauss values do not converge, and the apparent pole ladder moves with finite inner contour order. Numeric UV, local GR and full-MTS claim flags remain false.

## Next target

Move the energy integration and pole subtraction inside the relative/global contour quadratures. Derive the local energy-pole residue before applying any finite contour-node rule, then test convergence under simultaneous energy and contour refinement.
