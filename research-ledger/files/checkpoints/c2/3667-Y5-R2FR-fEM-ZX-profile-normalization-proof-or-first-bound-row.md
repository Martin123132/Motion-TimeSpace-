# 3667 - fEM ZX profile normalization proof or first bound row

**Status:** 3667 refuses the unsigned f_EM zero, derives that Cassini constrains normalized combinations mu_H=|K_gamma_H k_H f_EM/Z_X| and mu_G=|K_gamma_G k_G|f_EM^2/Z_X^2 rather than f_EM or Z_X separately, and stages first finite scale-proxy bound rows.

**Claim ceiling:** no f_EM zero, Cassini/gamma score, local-GR, PPN, WEP/R10, Newtonian, source-calibration, or EH-dominance pass is claimed.

## Main result

The zero route still does not close: the current parent grammar does not forbid `f_X(X_N)F_Q^2`, so `f_EM=0` is not claimed.

The finite route is now sharper. Cassini does not bound `f_EM` or `Z_X` separately. It bounds normalized combinations:

`mu_H = |K_gamma_H(lambda) k_H f_EM/Z_X|`,

`mu_G = |K_gamma_G(lambda) k_G| f_EM^2/Z_X^2`,

through

`C_H(lambda) mu_H + C_G(lambda) mu_G + |C_other_gamma| <= B_gamma_Cassini`.

This is progress because the next derivation target is now `k_H/k_G/K_gamma`, not the naked coupling by itself.

## Closure attempt
- `CLO3667_0_fEM_zero`: ZERO_NOT_CLOSED - `DeltaL=-(1/4) f_X(X_N) F_Q^2 is still allowed unless parent grammar forbids it`
- `CLO3667_1_range_chain`: RELATION_DERIVED_VALUES_MISSING - `S_X~int[1/2 Z_X |grad X|^2 + 1/2 M_X^2 X^2 - J_X X] => lambda_X=sqrt(Z_X/M_X^2)`
- `CLO3667_2_normalization_degeneracy`: NORMALIZED_COMBINATION_DERIVED - `delta_gamma_EM <= C_H(lambda)*mu_H + C_G(lambda)*mu_G + C_other, with mu_H=|k_H f_EM/Z_X| and mu_G=|k_G| f_EM^2/Z_X^2`
- `CLO3667_3_projection_status`: PROFILE_KERNEL_DERIVED_PROJECTION_COEFFICIENTS_MISSING - `H=e^(-r/lambda)*(3/r^3+3/(lambda*r^2)+1/(lambda^2*r)); G=e^(-2r/lambda)*(1/r^2+1/(lambda*r))^2`

## Normalized combinations
- `mu_H`: DERIVED_MEASURABLE_COMBINATION_NONCLAIM - `mu_H(lambda)=|K_gamma_H(lambda) k_H f_EM/Z_X|`
- `mu_G`: DERIVED_MEASURABLE_COMBINATION_NONCLAIM - `mu_G(lambda)=|K_gamma_G(lambda) k_G| f_EM^2/Z_X^2`
- `delta_gamma_EM_envelope`: BOUND_ROW_REDUCED_TO_NORMALIZED_COUPLINGS - `C_H(lambda)*mu_H + C_G(lambda)*mu_G + |C_other_gamma| <= B_gamma_Cassini`

## First finite scale-proxy rows
- Strongest sampled linear coefficient: `FB3667_lambda_over_r_100` with `C_H=2.757824671674e-26`.
- Weakest sampled linear coefficient: `FB3667_lambda_over_r_0.01` with `C_H=3.523450263238e-66`.
- `FB3667_lambda_over_r_0.01`: `3.523450263238e-66*mu_H + 1.225641775274e-123*mu_G + |C_other_gamma| <= 2.300000000000e-05` - FIRST_FINITE_BOUND_ROW_SCALE_PROXY_NONCLAIM
- `FB3667_lambda_over_r_0.1`: `5.550849568538e-29*mu_H + 2.165274296690e-47*mu_G + |C_other_gamma| <= 2.300000000000e-05` - FIRST_FINITE_BOUND_ROW_SCALE_PROXY_NONCLAIM
- `FB3667_lambda_over_r_1`: `2.367315785432e-26*mu_H + 4.699895652711e-41*mu_G + |C_other_gamma| <= 2.300000000000e-05` - FIRST_FINITE_BOUND_ROW_SCALE_PROXY_NONCLAIM
- `FB3667_lambda_over_r_10`: `2.753285080973e-26*mu_H + 8.600895325074e-41*mu_G + |C_other_gamma| <= 2.300000000000e-05` - FIRST_FINITE_BOUND_ROW_SCALE_PROXY_NONCLAIM
- `FB3667_lambda_over_r_100`: `2.757824671674e-26*mu_H + 8.681085752170e-41*mu_G + |C_other_gamma| <= 2.300000000000e-05` - FIRST_FINITE_BOUND_ROW_SCALE_PROXY_NONCLAIM

## Inputs still blocking a claim
- `f_EM zero theorem`: ZERO_NOT_CLOSED - needs unique-F2/no-f_XF2 parent signature
- `Z_X normalization`: RELATION_ONLY - needs parent quadratic action/Hessian with units
- `lambda_X range`: RELATION_ONLY - needs same-branch M_X^2/Z_X value or range theorem
- `k_H projection`: MISSING_WEAK_FIELD_PROJECTION - needs derive metric slip response coefficient
- `k_G projection`: MISSING_WEAK_FIELD_PROJECTION - needs prove gradient-square absence or source coefficient
- `K_gamma transfer`: MISSING_CASSINI_TRANSFER_KERNEL - needs path/impact/readout kernel
- `C_other_gamma floor`: MISSING_COMPONENT_BOUNDS - needs boundary/readout/source/nonEH bounds or zero theorem
- `Q_X non-EM components`: RETAINED_SOURCE_COMPONENTS - needs mass/nuclear/alpha/source-marker/boundary rows

## Claim gates
- `CG3667_0_fEM_zero`: FAILED_UNSIGNED_COUNTERTERM_LIVE - f_EM=0 parent theorem
- `CG3667_1_normalized_combo`: PASSED_DERIVATION - derive measurable gamma combinations
- `CG3667_2_first_bound_row`: PASSED_SCALE_PROXY_NONCLAIM - stage first finite gamma-bound row
- `CG3667_3_numeric_score`: BLOCKED_BY_KERNEL_AND_PARENT_COEFFICIENTS - claim-grade Cassini gamma score
- `CG3667_4_local_GR_claim`: ACTIVE_GUARD - local-GR/PPN pass

## Next checkpoint

`3668-Y5-R2FR-kH-kG-weak-field-projection-zero-or-transfer-kernel-bound.md` via `scripts/Y5_R2FR_3668_kH_kG_weak_field_projection_zero_or_transfer_kernel_bound.py`.

## Sources
- `handoff_3666`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3666_NEXT_TARGET.csv` exists=True needle_found=True
- `doc_3666`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\3666-Y5-R2FR-solar-EM-gamma-envelope-stub-or-fEM-profile-inputs.md` exists=True needle_found=True
- `status_3666`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3666_STATUS.csv` exists=True needle_found=True
- `envelope_3666`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3666_INSERTED_SOLAR_GAMMA_ENVELOPE.csv` exists=True needle_found=True
- `geometry_3666`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3666_SOLAR_LIMB_GEOMETRY_PROXY.csv` exists=True needle_found=True
- `requirements_3666`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3666_FEM_PROFILE_INPUT_REQUIREMENTS.csv` exists=True needle_found=True
- `fem_audit_3665`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3665_UNIQUE_F2_CLOSURE_AUDIT.csv` exists=True needle_found=True
- `em_lock_3649`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3649_EM_LOCK_CLAUSE_AUDIT.csv` exists=True needle_found=True
- `profile_3658`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3658_GAMMA_PROFILE_COEFFICIENT_ROWS.csv` exists=True needle_found=True
- `bound_formula_3660`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3660_GAMMA_BOUND_FORMULAS.csv` exists=True needle_found=True
- `hessian_1025`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1025-Y5-R10-parent-Hessian-ZX-MX2-range-or-alpha-source-row.md` exists=True needle_found=True
- `local_bounds`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\local_bounds\local_bound_claims.csv` exists=True needle_found=True
