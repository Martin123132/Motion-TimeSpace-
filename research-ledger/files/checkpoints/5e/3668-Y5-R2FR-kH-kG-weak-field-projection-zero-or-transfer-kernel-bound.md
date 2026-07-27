# 3668 - kH kG weak-field projection zero or transfer-kernel bound

**Status:** 3668 derives the k_H/k_G projection normal form and the linear-vs-quadratic hierarchy: k_H is the primary first-order gamma leakage, k_G is second-order but retained. The zero theorem remains unsigned, so finite kernel/coefficient rows are staged nonclaim.

**Claim ceiling:** no k_H/k_G zero, Cassini/gamma score, local-GR, PPN, WEP/R10, Newtonian, source-calibration, or EH-dominance pass is claimed.

## Main result

The weak-field profile channel now has the correct hierarchy:

`S_TF^X = k_H P_TF[partial_i partial_j X] + k_G P_TF[partial_i X partial_j X] + S_TF^other`.

For a Yukawa-like local profile, the `k_H` piece is linear in the profile amplitude while the `k_G` piece is quadratic. That makes `k_H` the first-order target for gamma/local-GR cleanup.

A zero theorem exists only conditionally: the parent action must make the extra weak-field response trace-only in the same observed frame and must exclude derivative/disformal, boundary, and readout STF channels. Current files do not sign all those clauses together.

## Projection derivation
- `KHKG3668_0_STF_projection_form`: PROJECTION_NORMAL_FORM_DERIVED - `S_TF^X = k_H P_TF[partial_i partial_j X] + k_G P_TF[partial_i X partial_j X] + S_TF^other`
- `KHKG3668_1_linear_quadratic_split`: LINEAR_KH_AND_QUADRATIC_KG_SPLIT_DERIVED - `delta_gamma_EM = C_H(lambda) mu_H + C_G(lambda) mu_G + C_other; mu_H~f_EM/Z_X, mu_G~f_EM^2/Z_X^2`
- `KHKG3668_2_zero_condition`: CONDITIONAL_ZERO_THEOREM_DERIVED_PARENT_UNSIGNED - `P_TF(delta E_ij^X)=0 and P_TF(delta T_ij^X)=0 and P_TF(B_ij+R_ij)=0 => k_H=k_G=0`
- `KHKG3668_3_current_verdict`: ZERO_NOT_CLOSED_BOUND_INTERFACE_REQUIRED - `zero route unsigned => retain finite coefficient/kernel rows`

## Zero gates
- `ZG3668_0_EH_TF`: UNSIGNED - EH trace-free equation owns the observed frame
- `ZG3668_1_trace_only_extra`: UNSIGNED - extra local response is pure trace
- `ZG3668_2_no_gradient_stress`: UNSIGNED - no extra-sector anisotropic gradient stress
- `ZG3668_3_no_disformal_frame`: UNSIGNED - no Weyl/disformal representative frame leakage
- `ZG3668_4_boundary_readout`: UNSIGNED - boundary and readout STF terms vanish
- `ZG3668_5_total`: NOT_SIGNED - all k_H/k_G zero clauses hold together

## Kernel/coefficient rows
- `K_gamma_H(lambda,b,path)`: MISSING_TRANSFER_KERNEL - derive Shapiro/path kernel or set conservative bounded transfer convention
- `K_gamma_G(lambda,b,path)`: MISSING_TRANSFER_KERNEL - derive Shapiro/path kernel or set conservative bounded transfer convention
- `k_H`: MISSING_PARENT_METRIC_RESPONSE - prove no Hessian-STF operator or derive coefficient from parent metric response
- `k_G`: MISSING_PARENT_METRIC_RESPONSE - prove no gradient-square/disformal stress or bound as second-order term
- `C_other_gamma`: MISSING_COMPONENT_BOUNDS - derive zero or source finite bound rows

## Reduced bound interface
- `RB3668_lambda_over_r_0.01`: 3.523450263238e-66*mu_H + 1.225641775274e-123*mu_G + |C_other_gamma| <= 2.300000000000e-05 - REDUCED_NONCLAIM_BOUND_ROW_AWAITING_KH_KG_KGAMMA
- `RB3668_lambda_over_r_0.1`: 5.550849568538e-29*mu_H + 2.165274296690e-47*mu_G + |C_other_gamma| <= 2.300000000000e-05 - REDUCED_NONCLAIM_BOUND_ROW_AWAITING_KH_KG_KGAMMA
- `RB3668_lambda_over_r_1`: 2.367315785432e-26*mu_H + 4.699895652711e-41*mu_G + |C_other_gamma| <= 2.300000000000e-05 - REDUCED_NONCLAIM_BOUND_ROW_AWAITING_KH_KG_KGAMMA
- `RB3668_lambda_over_r_10`: 2.753285080973e-26*mu_H + 8.600895325074e-41*mu_G + |C_other_gamma| <= 2.300000000000e-05 - REDUCED_NONCLAIM_BOUND_ROW_AWAITING_KH_KG_KGAMMA
- `RB3668_lambda_over_r_100`: 2.757824671674e-26*mu_H + 8.681085752170e-41*mu_G + |C_other_gamma| <= 2.300000000000e-05 - REDUCED_NONCLAIM_BOUND_ROW_AWAITING_KH_KG_KGAMMA

## Priority decision
- `PR3668_0_linear_kH`: NEXT_TARGET_PRIMARY - k_H Hessian-STF projection: linear in A_X and therefore first-order in f_EM/Z_X; if nonzero, it dominates the earliest gamma leakage.
- `PR3668_1_quadratic_kG`: RETAIN_SECOND_ORDER_GUARD - k_G gradient-square projection: quadratic in A_X; can be demoted only under a sourced small-amplitude expansion or if parent stress/disformal terms vanish.
- `PR3668_2_transfer_kernel`: PARALLEL_REQUIRED_FOR_SCORING - K_gamma transfer/readout kernel: 3667 solar-limb substitution is a scale proxy, not the Shapiro path kernel; any finite score needs the transfer map.

## Claim gates
- `CG3668_0_zero_theorem`: FAILED_UNSIGNED_PARENT_CLAUSES - k_H=k_G=0 theorem
- `CG3668_1_projection_normal_form`: PASSED_DERIVATION - weak-field projection normal form
- `CG3668_2_order_hierarchy`: PASSED_DERIVATION - linear/quadratic hierarchy
- `CG3668_3_bound_interface`: PASSED_NONCLAIM_INTERFACE - coefficient/kernel bound rows
- `CG3668_4_gamma_claim`: ACTIVE_GUARD - Cassini gamma/local-GR claim

## Next checkpoint

`3669-Y5-R2FR-kH-Hessian-STF-parent-owner-or-linear-gamma-bound-row.md` via `scripts/Y5_R2FR_3669_kH_Hessian_STF_parent_owner_or_linear_gamma_bound_row.py`.

## Sources
- `handoff_3667`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3667_NEXT_TARGET.csv` exists=True needle_found=True
- `doc_3667`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\3667-Y5-R2FR-fEM-ZX-profile-normalization-proof-or-first-bound-row.md` exists=True needle_found=True
- `combos_3667`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3667_NORMALIZED_GAMMA_COMBINATION_ROWS.csv` exists=True needle_found=True
- `bounds_3667`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3667_FIRST_FINITE_GAMMA_BOUND_ROWS.csv` exists=True needle_found=True
- `status_3667`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3667_STATUS.csv` exists=True needle_found=True
- `doc_3656`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\3656-Y5-R2FR-first-MTS-local-GR-residual-component-acquisition.md` exists=True needle_found=True
- `gamma_3656`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3656_GAMMA_WEAK_FIELD_DERIVATION_ROWS.csv` exists=True needle_found=True
- `doc_3657`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\3657-Y5-R2FR-S_TF_MTS-zero-proof-or-gamma-coefficient-bound.md` exists=True needle_found=True
- `proof_3657`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3657_STF_ZERO_PROOF_ATTEMPT.csv` exists=True needle_found=True
- `profile_3658`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3658_GAMMA_PROFILE_COEFFICIENT_ROWS.csv` exists=True needle_found=True
- `doc_3658`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\3658-Y5-R2FR-no-gradient-STF-operator-condition-or-gamma-profile-coefficient.md` exists=True needle_found=True
- `frame_leak_1027`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1027-Y5-R10-qbarXT-source-zero-or-bounded-coupling-row.md` exists=True needle_found=True
- `hessian_1025`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1025-Y5-R10-parent-Hessian-ZX-MX2-range-or-alpha-source-row.md` exists=True needle_found=True
