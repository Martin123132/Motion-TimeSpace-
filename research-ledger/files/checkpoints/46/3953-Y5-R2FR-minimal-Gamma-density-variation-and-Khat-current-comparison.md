# 3953 - Minimal Gamma Density Variation And Khat Current Comparison

Timestamp: `2026-07-01T14:15:29+00:00`

## Result

3953 takes the leap requested by 3952: vary an actual minimal covariant parent density.

The constructed density is:

`Gamma_quad = Gamma0 + 1/2 G_AB g^alpha_beta nabla_alpha Z^A nabla_beta Z^B + 1/2 M_AB Z^A Z^B`.

Its metric response is:

`K_metric^mu_nu = Gamma_quad g^mu_nu - G_AB nabla^mu Z^A nabla^nu Z^B + K_coeff^mu_nu`.

`K_coeff` stores hidden metric/coframe/connection dependence of `G_AB`, `M_AB`, and boundary conventions.

## What This Actually Proves

- The constructed branch is variational and inherits the 3952 Helmholtz pass.
- The branch has a double-zero: `Gamma_quad-Gamma0=O(Z^2,nabla Z^2)` and `F_1=0`.
- The source-free linear branch gives `-G_AB box Z^B + M_AB Z^B=0`.
- If `G_AB` is positive and `M_AB` has a positive gap, then zero source/boundary work gives local suppression/no-hair.

## What It Does Not Prove Yet

It does not prove current MTS already uses this `K_hat`. The current tensor still has to match:

`Gamma_quad g^mu_nu - G_AB nabla^mu Z^A nabla^nu Z^B + K_coeff^mu_nu`.

Any mismatch is now sorted into `DeltaK_volume`, `DeltaK_gradient`, `DeltaK_coeff`, or `DeltaK_linear_or_J_A`.

## Why The Next Step Is Coupling

The remaining dangerous term is direct matter/source current:

`J_A := delta S_matter/delta Z^A`.

If matter only descends through the observable metric and the observable metric has no first-order `Z` leakage, then `J_A=0`. If not, the failure becomes a PPN/source-normalization residual.

## Source Register

- Source rows found: `11/11`
- Register: `source-intake\mts_residuals\P8_Y5_R2FR_3953_SOURCE_REGISTER.csv`
- Validation: `source-intake\mts_residuals\P8_Y5_BRR545_3953_VALIDATION.csv`

## Next Target

`3954-Y5-R2FR-Z-source-current-silence-and-PPN-normalization-map.md`
