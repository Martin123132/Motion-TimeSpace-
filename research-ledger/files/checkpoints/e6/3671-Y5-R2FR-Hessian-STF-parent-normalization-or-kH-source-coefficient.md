# 3671 - Hessian-STF parent normalization or kH source coefficient

**Status:** 3671 derives the conditional parent-equation route: a Hessian-STF source can invert to a scalar slip Y=Phi-Psi proportional to X, replacing the direct Hessian readout by a Yukawa path kernel if the parent equation signs the route.

This is the important fork: 3670 treated the Hessian-STF term as a direct readout kernel. 3671 tests whether the parent field equation instead integrates it into scalar slip.

Let `Y=Phi-Psi`. If the parent weak-field trace-free equation has

`P_TF[partial_i partial_j Y] = C_parent_H*k_H*P_TF[partial_i partial_j X]`,

then

`P_TF[partial_i partial_j(Y-C_parent_H*k_H*X)]=0`.

With asymptotic/boundary/readout kernel silence, this gives the conditional local result:

`Y_X = C_parent_H*k_H*X`.

That is a real derivation route, but it is not claimed yet because `C_parent_H` is not parent-owned: the branch must decide whether `k_H` lives as a geometric equation coefficient or as a stress-energy/source coefficient requiring Einstein/unit normalization.

If this route is signed, the Cassini/Shapiro kernel becomes the positive Yukawa scalar-slip path kernel:

`G_X(eta,zeta)=int_{-zeta}^{zeta} exp(-sqrt(1+u^2)/eta)/sqrt(1+u^2) du / (2 asinh zeta)`.

Strongest sampled scalar-slip proxy row: `YX3671_eta_100_zeta_215.032` with `xi_H <= 2.979212325428e-05` if other branches are zero.

`xi_H=|C_parent_H*k_H*f_EM/Z_X|`; this remains nonclaim until the parent normalization, k_H source, f_EM, and Z_X are signed.

## Derivation rows
- `PND3671_0_linear_metric_split`: DERIVED_STANDARD_LINEAR_FORM_CONDITIONAL - `P_TF[partial_i partial_j Y] = source_TF`
- `PND3671_1_STF_inversion_lemma`: DERIVED_CONDITIONAL_LEMMA - `Y=C_H X + kernel(P_TF partial partial)`
- `PND3671_2_boundary_kernel`: BOUNDARY_CONDITIONAL_NOT_PARENT_SIGNED - `kernel(P_TF partial partial)->0 under local-asymptotic boundary silence`
- `PND3671_3_parent_coefficient_fork`: COEFFICIENT_SOURCE_UNITS_UNSIGNED - `Y_X = C_parent_H*k_H*X`
- `PND3671_4_readout_kernel_change`: DERIVED_SCALAR_SLIP_KERNEL_IF_PARENT_EQUATION_SIGNS - `G_X(eta,zeta)=int exp(-rho/eta)/rho du / (2 asinh zeta)`
- `PND3671_5_verdict`: PARTIAL_DERIVATION_PARENT_COEFFICIENT_UNSIGNED - `xi_H=|C_parent_H*k_H*f_EM/Z_X| remains nonclaim until C_parent_H and k_H are parent-owned`

## Normalization forks
- `NF3671_0_geometric_LHS`: PROMISING_BUT_NOT_SOURCE_SIGNED - geometric equation coefficient => `C_parent_H dimensionless, possibly C_parent_H=1 by convention`
- `NF3671_1_stress_RHS`: UNSIGNED_UNITS_BLOCKER - anisotropic stress coefficient => `C_parent_H ~ 8*pi*G/c^4 times unit conversion`
- `NF3671_2_direct_metric_readout`: CONSERVATIVE_FALLBACK_AVAILABLE - direct h_ij^TF readout => `delta t_TF proportional to integral n^i n^j h_ij^TF dz`
- `NF3671_3_scalar_slip_readout`: BEST_ROUTE_IF_PARENT_EQUATION_SIGNS - scalar slip readout => `delta gamma_X proportional to xi_H*G_X(lambda/b,L/b)`

## Scalar-slip kernel rows
- `YX3671_eta_0.01_zeta_215.032`: eta=1.000000000000e-02, zeta=2.150321556705e+02, G_X=7.679212033988e-46, xi_H_max=2.995098963045e+40
- `YX3671_eta_0.01_zeta_1000`: eta=1.000000000000e-02, zeta=1.000000000000e+03, G_X=6.126414674398e-46, xi_H_max=3.754234935503e+40
- `YX3671_eta_0.01_zeta_2000`: eta=1.000000000000e-02, zeta=2.000000000000e+03, G_X=5.584889266225e-46, xi_H_max=4.118255332132e+40
- `YX3671_eta_0.1_zeta_215.032`: eta=1.000000000000e-01, zeta=2.150321556705e+02, G_X=2.932097255433e-06, xi_H_max=7.844214566002e+00
- `YX3671_eta_0.1_zeta_1000`: eta=1.000000000000e-01, zeta=1.000000000000e+03, G_X=2.339204038732e-06, xi_H_max=9.832404364550e+00
- `YX3671_eta_0.1_zeta_2000`: eta=1.000000000000e-01, zeta=2.000000000000e+03, G_X=2.143713017525e-06, xi_H_max=1.072904806379e+01
- `YX3671_eta_1_zeta_215.032`: eta=1.000000000000e+00, zeta=2.150321556705e+02, G_X=6.943083651137e-02, xi_H_max=3.312649127630e-04
- `YX3671_eta_1_zeta_1000`: eta=1.000000000000e+00, zeta=1.000000000000e+03, G_X=5.539137314732e-02, xi_H_max=4.152271137751e-04
- `YX3671_eta_1_zeta_2000`: eta=1.000000000000e+00, zeta=2.000000000000e+03, G_X=5.076222754110e-02, xi_H_max=4.530928037265e-04
- `YX3671_eta_10_zeta_215.032`: eta=1.000000000000e+01, zeta=2.150321556705e+02, G_X=4.002462027112e-01, xi_H_max=5.746463013065e-05
- `YX3671_eta_10_zeta_1000`: eta=1.000000000000e+01, zeta=1.000000000000e+03, G_X=3.193132602073e-01, xi_H_max=7.202957993374e-05
- `YX3671_eta_10_zeta_2000`: eta=1.000000000000e+01, zeta=2.000000000000e+03, G_X=2.926277405765e-01, xi_H_max=7.859815325329e-05
- `YX3671_eta_100_zeta_215.032`: eta=1.000000000000e+02, zeta=2.150321556705e+02, G_X=7.720161400948e-01, xi_H_max=2.979212325428e-05
- `YX3671_eta_100_zeta_1000`: eta=1.000000000000e+02, zeta=1.000000000000e+03, G_X=6.211420871479e-01, xi_H_max=3.702856476142e-05
- `YX3671_eta_100_zeta_2000`: eta=1.000000000000e+02, zeta=2.000000000000e+03, G_X=5.692327511109e-01, xi_H_max=4.040526472715e-05

## Bound rows
- `XIH3671_eta_0.01_zeta_215.032`: `xi_H <= 2.995098963045e+40 if C_other_gamma=0 and quadratic/direct-TF branches are zero`
- `XIH3671_eta_0.01_zeta_1000`: `xi_H <= 3.754234935503e+40 if C_other_gamma=0 and quadratic/direct-TF branches are zero`
- `XIH3671_eta_0.01_zeta_2000`: `xi_H <= 4.118255332132e+40 if C_other_gamma=0 and quadratic/direct-TF branches are zero`
- `XIH3671_eta_0.1_zeta_215.032`: `xi_H <= 7.844214566002e+00 if C_other_gamma=0 and quadratic/direct-TF branches are zero`
- `XIH3671_eta_0.1_zeta_1000`: `xi_H <= 9.832404364550e+00 if C_other_gamma=0 and quadratic/direct-TF branches are zero`

## Claim gates
- `CG3671_0_STF_inversion`: PASSED_CONDITIONAL_DERIVATION - Hessian-STF inversion route
- `CG3671_1_scalar_kernel`: PASSED_CONDITIONAL_KERNEL - Yukawa scalar-slip kernel
- `CG3671_2_parent_coefficient`: FAILED_UNSIGNED - C_parent_H coefficient
- `CG3671_3_boundary_kernel`: FAILED_UNSIGNED - STF inversion kernel silence
- `CG3671_4_claim_status`: BLOCKED_NONCLAIM - Cassini/local-GR claim

## Next target
`3672-Y5-R2FR-geometric-vs-stress-source-normalization-decision.md` via `scripts/Y5_R2FR_3672_geometric_vs_stress_source_normalization_decision.py`.

## Sources
- `handoff_3670`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3670_NEXT_TARGET.csv` exists=True needle_found=True
- `doc_3670`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\3670-Y5-R2FR-KgammaH-transfer-kernel-or-conservative-linear-bound.md` exists=True needle_found=True
- `kernel_3670`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3670_KGAMMAH_PATH_KERNEL_ROWS.csv` exists=True needle_found=True
- `bounds_3670`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3670_CONSERVATIVE_BETAH_BOUND_ROWS.csv` exists=True needle_found=True
- `doc_3669`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\3669-Y5-R2FR-kH-Hessian-STF-parent-owner-or-linear-gamma-bound-row.md` exists=True needle_found=True
- `weak_response_2477`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\2477-Y5-R2FR-parent-weak-field-metric-response-theorem-or-no-go.md` exists=True needle_found=True
- `metric_inputs_3384`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3384_METRIC_RESPONSE_INPUT_REQUIREMENTS.csv` exists=True needle_found=True
- `common_mode_3060`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3060_COMMON_MODE_METRIC_RESPONSE_THEOREM_ATTEMPT.csv` exists=True needle_found=True
