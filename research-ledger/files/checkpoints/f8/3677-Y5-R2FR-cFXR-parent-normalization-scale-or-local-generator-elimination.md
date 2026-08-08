# 3677 - c_FXR parent normalization scale or local generator elimination

**Status:** CANONICAL_CFXR_PAIR_DERIVED_NATURALNESS_PRIOR_STAGED_NONCLAIM

This checkpoint takes the leap that 3676 set up: raw `c_FXR` is not the physical coupling unless the `X` field coordinate is fixed. Under `X' = lambda_X X`, the raw pieces move, but the observable product does not.

## Main derivation

`Z_X' = Z_X/lambda_X^2`, `F0_prime' = F0_prime/lambda_X`, and `f_EM' = f_EM/lambda_X`.

Therefore:

`(c_FXR' f_EM')/Z_X' = c_FXR f_EM/Z_X`.

With the canonical field `X_hat=sqrt(Z_X) X`:

`g_FXR = A_H*F0_hat_prime/(1+A_H*F0)`

`s_EM = f_EM/sqrt(Z_X)`

`xi_FXR = |g_FXR*s_EM|`.

That is the useful object. The raw `c_FXR` row is demoted; the canonical pair is promoted for private smoke tests.

## Immediate consequence
- `BIR3677_0_invariant_bound`: `xi_FXR=|g_FXR*s_EM| <= 2.979212325428e-05` from |c_FXR*f_EM/Z_X| <= 2.979212325428e-05 - strictest inherited private scalar-slip template converted to canonical pair
- `BIR3677_1_if_gFXR_O1`: `|s_EM| <= 2.979212325428e-05` from |g_FXR|<=1 - EM/Poynting transfer leg must be below the scalar-slip ceiling if curvature leg is natural
- `BIR3677_2_if_sEM_O1`: `|g_FXR| <= 2.979212325428e-05` from |s_EM|<=1 - curvature prefactor leg must be suppressed if EM transfer is O(1)
- `BIR3677_3_if_gFXR_4pi`: `|s_EM| <= 2.370781840561e-06` from |g_FXR|<=4pi - looser curvature naturalness still forces a very small EM transfer leg

## Canonical contract
- `CNC3677_0_parent_slot`: accepted starting point - parent curvature slot -> 3673/3674 already derived this as the allowed F(X)R branch
- `CNC3677_1_field_rescaling`: derived algebraic transformation - field-coordinate redundancy -> c_FXR by itself is not a coordinate-invariant physical coefficient
- `CNC3677_2_invariant_product`: derived invariant - observable scalar-slip product -> the bound must act on the invariant product, not on raw c_FXR alone
- `CNC3677_3_canonical_field`: canonical normalization converts the vague coupling into two dimensionless physical legs - canonical field coordinate -> xi_FXR=|g_FXR*f_EM_hat|
- `CNC3677_4_denominator_guard`: conditional guard, not a parent theorem - EH denominator guard -> prevents fake large/small coupling from Planck-mass denominator accident

## Reparameterization derivation
- `RPD3677_0_kinetic`: PASS_DERIVED - Z_X_prime=Z_X/lambda_X^2
- `RPD3677_1_curvature_derivative`: PASS_DERIVED - F0_prime_prime=F0_prime/lambda_X
- `RPD3677_2_source_transfer`: PASS_DERIVED_IF_LINEAR_SOURCE_CONVENTION - f_EM_prime=f_EM/lambda_X
- `RPD3677_3_raw_cFXR`: NOT_OBSERVABLE_ALONE - c_FXR_prime=c_FXR/lambda_X
- `RPD3677_4_product_invariance`: PASS_DERIVED_INVARIANT - xi_FXR_prime=xi_FXR
- `RPD3677_5_canonical_pair`: PASS_DERIVED_CANONICAL_OBSERVABLE_PAIR - xi_FXR=|g_FXR*s_EM|

## Naturalness priors
- `NPR3677_0_gFXR_canonical_O1`: `g_FXR=A_H*F0_hat_prime/(1+A_H*F0)` in [-1.000000000000e+00, 1.000000000000e+00] - MISSING-free naturalness prior row for private smoke use only
- `NPR3677_1_gFXR_canonical_4pi`: `g_FXR=A_H*F0_hat_prime/(1+A_H*F0)` in [-1.256637061436e+01, 1.256637061436e+01] - MISSING-free loose smoke prior, not evidence
- `NPR3677_2_sEM_required_if_gO1`: `s_EM=f_EM/sqrt(Z_X)` in [-2.979212325428e-05, 2.979212325428e-05] - derived conditional smoke bound on EM/Poynting transfer leg
- `NPR3677_3_sEM_required_if_g4pi`: `s_EM=f_EM/sqrt(Z_X)` in [-2.370781840561e-06, 2.370781840561e-06] - derived conditional smoke bound on EM/Poynting transfer leg

## Decisions
- `GDR3677_0_generator_elimination_attempt`: NOT_KILLED_THIS_CHECKPOINT - kill quotient-scalar generator feeding F(X)R -> use canonical normalization route instead of smuggling zero
- `GDR3677_1_raw_cFXR_decision`: DEMOTED_NOT_PHYSICAL_ALONE - raw c_FXR coefficient -> replace with canonical g_FXR and s_EM pair
- `GDR3677_2_canonical_pair_decision`: PROMOTED_TO_PRIVATE_SMOKE_COORDINATES - canonical observable pair -> future data/code should score g_FXR and s_EM product, not raw c_FXR
- `GDR3677_3_next_physics_target`: NEXT_BEST_TARGET - EM/Poynting transfer leg -> derive s_EM from Maxwell/Poynting/current owner or produce a bound row

## Claim gates
- `CG3677_0_raw_cFXR_claim`: BLOCKED_BY_REPARAMETERIZATION - claim a raw numeric c_FXR because raw c_FXR is field-coordinate dependent
- `CG3677_1_canonical_prior_claim`: BLOCKED_NONCLAIM - treat naturalness prior as evidence because O(1) and 4pi rows are smoke priors only
- `CG3677_2_local_GR_claim`: BLOCKED_NONCLAIM - claim local-GR/PPN pass because xi product still needs EM transfer/source leg or theorem-zero
- `CG3677_3_generator_zero`: BLOCKED_NONCLAIM - claim quotient-scalar generator killed because generator elimination was not proved
- `CG3677_4_public_or_github`: BLOCKED_PRIVATE - public/GitHub promotion because private checkpoint only

## Next target
`3678-Y5-R2FR-canonical-EM-Poynting-transfer-leg-or-sEM-bound.md` via `scripts/Y5_R2FR_3678_canonical_EM_Poynting_transfer_leg_or_sEM_bound.py`.

## Sources
- `handoff_3676`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3676_NEXT_TARGET.csv` exists=True needle_found=True
- `doc_3676`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\3676-Y5-R2FR-no-natural-marker-no-reentry-theorem-or-FXR-prior-row.md` exists=True needle_found=True
- `prior_3676`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3676_CFXR_PRIOR_SOURCE_ROW.csv` exists=True needle_found=True
- `validation_3676`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_BRR545_3676_VALIDATION.csv` exists=True needle_found=True
- `doc_3673`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\3673-Y5-R2FR-parent-action-Hessian-STF-operator-location.md` exists=True needle_found=True
- `template_3674`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3674_FXR_COEFFICIENT_TEMPLATE_ROWS.csv` exists=True needle_found=True
- `bounds_3675`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3675_FINITE_CFXR_BOUND_ROWS.csv` exists=True needle_found=True
- `canonical_3464`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3464_CANONICAL_NORMALIZATION_THEOREM_AUDIT.csv` exists=True needle_found=True
- `em_owner_3464`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3464_EM_ALPHA_CHARGE_OWNER_AUDIT.csv` exists=True needle_found=True
- `prior_policy_2965`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_2965_NXHAT_FIRST_PRIOR_SLOT_NONCLAIM.csv` exists=True needle_found=True
