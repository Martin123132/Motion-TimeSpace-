# 4107 - Constant G_eff radial/time hair zero or bound

## Verdict
4107 moves the Newton-coupling route one notch tighter. Constant measured `GM` is now governed by an exact identity, not taste:

`mu_obs = G_eff M_eff (1+epsilon_mu)` and `D_X ln mu_obs = D_X ln G_eff + D_X ln M_eff + D_X ln(1+epsilon_mu)`.

Then 3600 sharpens `G_eff`: it is not one magic constant. It is the product `G_ref*w_common*ell_J*R_frame*C_extra`. Constant `kappa` alone does not close the gate.

Decision: `MEASURED_GM_DERIVATIVE_IDENTITY_AND_GEFF_PRODUCT_LOCK_IMPORTED_ELLJ_SOURCE_CURRENT_NORMALIZATION_GATE_NEXT`

## Concrete Advances
- Time drift and radial profile hair are exact residual channels, not fitted away.
- Fitted cancellation is rejected unless the parent action supplies an identity.
- The measured coupling product is split into `z_G`, `z_w`, `z_ellJ`, `z_Rframe`, and `z_extra`.
- `z_ellJ = D_X ln ell_J` is now the sharpest next denominator to attack.

## Still Not Claimed
- Constant universal `G_eff`.
- Constant Newtonian `GM`.
- Local GR/PPN source stability.

## Outputs
- `P8_Y5_R2FR_4107_SOURCE_REGISTER.csv`
- `P8_Y5_R2FR_4107_DERIVATIVE_IDENTITY.csv`
- `P8_Y5_R2FR_4107_DERIVATIVE_HAIR_BOUNDS.csv`
- `P8_Y5_R2FR_4107_GEFF_PRODUCT_LOCK.csv`
- `P8_Y5_R2FR_4107_PROMOTION_GATES.csv`
- `P8_Y5_R2FR_4107_DECISION_GATE.csv`
- `P8_Y5_R2FR_4107_NEXT_TARGET.csv`
- `P8_Y5_R2FR_4107_STATUS.csv`
- `P8_Y5_BRR545_4107_VALIDATION.csv`

## Next target
- `4108-Y5-R2FR-ellJ-source-current-normalization-zero-or-bound.md`
- Objective: prove `z_ellJ=D_X ln ell_J=0` through matter descent/Ward/PiM/H_tau/unit ownership, or retain source-ready `z_ellJ` bound rows.
