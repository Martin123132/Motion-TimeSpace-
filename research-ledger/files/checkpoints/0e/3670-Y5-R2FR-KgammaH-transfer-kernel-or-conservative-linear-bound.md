# 3670 - KgammaH transfer kernel or conservative linear bound

**Status:** 3670 derives the explicit Hessian-STF Shapiro geometry kernel for the k_H branch and replaces the naked K_gamma_H placeholder with signed and absolute path-integral rows.

This checkpoint does not merely say `K_gamma_H` is missing. It derives the part we can own from geometry:

`P_TF[partial_i partial_j X]=(X''-X'/r)(rhat_i rhat_j-delta_ij/3)`

`X=e^{-r/lambda}/r => X''-X'/r=e^{-r/lambda}(3/r^3+3/(lambda*r^2)+1/(lambda^2*r))`

For a straight Shapiro path with `u=z/b`, the photon projection is:

`n^i n^j(rhat_i rhat_j-delta_ij/3)=u^2/(1+u^2)-1/3`

So the dimensionless signed kernel is:

`J_H(eta,zeta)=int_{-zeta}^{zeta} e^{-sqrt(1+u^2)/eta}(3/rho^3+3/(eta*rho^2)+1/(eta^2*rho))*(u^2/(1+u^2)-1/3) du`

with `eta=lambda/b`, `zeta=L/b`, `rho=sqrt(1+u^2)`, and Shapiro denominator `D=2 asinh(zeta)`. The dimensionful path kernel is `G_H/b^2`, where `G_H=J_H/D`.

Because the projection changes sign at `u=1/sqrt(2)`, signed cancellation is diagnostic only. The conservative nonclaim branch uses the absolute-path kernel `J_abs/D`; it does **not** use cancellation to claim a pass.

Strongest sampled absolute-path proxy row: `KGH3670_eta_100_zeta_215.032` with `beta_H <= 1.812167092817e-04` if `C_other_gamma=0` and `beta_G=0`.

`beta_H=|C_parent_H*k_H*f_EM/Z_X|/b^2` in the selected Shapiro normalization. `C_parent_H` is still not parent-owned, so this is not claimed as a Cassini/local-GR result.

## Derivation rows
- `KGD3670_0_coordinates`: DERIVED_GEOMETRY_LOCKED - `r(z)=sqrt(b^2+z^2)`
- `KGD3670_1_radial_Hessian_STF`: DERIVED_ANALYTIC_KERNEL - `X=e^{-r/lambda}/r => X''-X'/r=e^{-r/lambda}(3/r^3+3/(lambda*r^2)+1/(lambda^2*r))`
- `KGD3670_2_null_projection`: DERIVED_SIGN_STRUCTURE - `n^i n^j(rhat_i rhat_j-delta_ij/3)=u^2/(1+u^2)-1/3`
- `KGD3670_3_dimensionless_kernel`: DERIVED_TRANSFER_GEOMETRY - `F_H=e^{-sqrt(1+u^2)/eta}(3/rho^3+3/(eta*rho^2)+1/(eta^2*rho))*(u^2/(1+u^2)-1/3)`
- `KGD3670_4_shapiro_normalization`: GEOMETRY_DERIVED_PARENT_NORMALIZATION_UNSIGNED - `G_H=J_H/D, G_H_abs=J_abs/D, actual dimensionful kernel = G_H/b^2`
- `KGD3670_5_conservative_rule`: CONSERVATIVE_NONCLAIM_CONVENTION - `beta_H <= B_gamma/G_H_abs for beta_H defined in the chosen b^2-normalized parent convention`

## Path kernel rows
- `KGH3670_eta_0.01_zeta_215.032`: eta=1.000000000000e-02, zeta=2.150321556705e+02, G_abs=2.559737344666e-42, signed/abs=9.999999999988e-01, beta_H_max=8.985296889123e+36
- `KGH3670_eta_0.01_zeta_1000`: eta=1.000000000000e-02, zeta=1.000000000000e+03, G_abs=2.042138204371e-42, signed/abs=9.999999999990e-01, beta_H_max=1.126270491917e+37
- `KGH3670_eta_0.01_zeta_2000`: eta=1.000000000000e-02, zeta=2.000000000000e+03, G_abs=1.858715186187e-42, signed/abs=9.999999999999e-01, beta_H_max=1.237413895950e+37
- `KGH3670_eta_0.1_zeta_215.032`: eta=1.000000000000e-01, zeta=2.150321556705e+02, G_abs=9.954795254546e-05, signed/abs=9.818039716735e-01, beta_H_max=2.310444304668e-01
- `KGH3670_eta_0.1_zeta_1000`: eta=1.000000000000e-01, zeta=1.000000000000e+03, G_abs=7.942581122988e-05, signed/abs=9.817144672536e-01, beta_H_max=2.895784083770e-01
- `KGH3670_eta_0.1_zeta_2000`: eta=1.000000000000e-01, zeta=2.000000000000e+03, G_abs=7.268625120725e-05, signed/abs=9.830896395735e-01, beta_H_max=3.164284801870e-01
- `KGH3670_eta_1_zeta_215.032`: eta=1.000000000000e+00, zeta=2.150321556705e+02, G_abs=8.463388437874e-02, signed/abs=2.734556299802e-01, beta_H_max=2.717587662298e-04
- `KGH3670_eta_1_zeta_1000`: eta=1.000000000000e+00, zeta=1.000000000000e+03, G_abs=6.753939628136e-02, signed/abs=2.733780884299e-01, beta_H_max=3.405419838843e-04
- `KGH3670_eta_1_zeta_2000`: eta=1.000000000000e+00, zeta=2.000000000000e+03, G_abs=6.162820919807e-02, signed/abs=2.745616452836e-01, beta_H_max=3.732057169807e-04
- `KGH3670_eta_10_zeta_215.032`: eta=1.000000000000e+01, zeta=2.150321556705e+02, G_abs=1.253874391089e-01, signed/abs=1.064025247310e-02, beta_H_max=1.834314518539e-04
- `KGH3670_eta_10_zeta_1000`: eta=1.000000000000e+01, zeta=1.000000000000e+03, G_abs=1.000569438087e-01, signed/abs=1.063771781856e-02, beta_H_max=2.298691037774e-04
- `KGH3670_eta_10_zeta_2000`: eta=1.000000000000e+01, zeta=2.000000000000e+03, G_abs=9.136332866246e-02, signed/abs=1.067633826176e-02, beta_H_max=2.517421413680e-04
- `KGH3670_eta_100_zeta_215.032`: eta=1.000000000000e+02, zeta=2.150321556705e+02, G_abs=1.269198634672e-01, signed/abs=2.130647374824e-04, beta_H_max=1.812167092817e-04
- `KGH3670_eta_100_zeta_1000`: eta=1.000000000000e+02, zeta=1.000000000000e+03, G_abs=1.012804276560e-01, signed/abs=2.044304355707e-04, beta_H_max=2.270922480514e-04
- `KGH3670_eta_100_zeta_2000`: eta=1.000000000000e+02, zeta=2.000000000000e+03, G_abs=9.248375338695e-02, signed/abs=2.051649499739e-04, beta_H_max=2.486923287355e-04

## Conservative bound rows
- `CBH3670_eta_0.01_zeta_215.032`: `beta_H <= 8.985296889123e+36 if C_other_gamma=0 and beta_G=0`
- `CBH3670_eta_0.01_zeta_1000`: `beta_H <= 1.126270491917e+37 if C_other_gamma=0 and beta_G=0`
- `CBH3670_eta_0.01_zeta_2000`: `beta_H <= 1.237413895950e+37 if C_other_gamma=0 and beta_G=0`
- `CBH3670_eta_0.1_zeta_215.032`: `beta_H <= 2.310444304668e-01 if C_other_gamma=0 and beta_G=0`
- `CBH3670_eta_0.1_zeta_1000`: `beta_H <= 2.895784083770e-01 if C_other_gamma=0 and beta_G=0`

## Claim gates
- `CG3670_0_geometry_kernel`: PASSED_DERIVED_GEOMETRY - K_gamma_H geometry
- `CG3670_1_cancellation_guard`: PASSED_GUARDRAIL - line-of-sight cancellation
- `CG3670_2_parent_normalization`: FAILED_UNSIGNED - parent/readout normalization
- `CG3670_3_local_gamma_claim`: BLOCKED_NONCLAIM - Cassini gamma/local-GR claim

## Next target
`3671-Y5-R2FR-Hessian-STF-parent-normalization-or-kH-source-coefficient.md` via `scripts/Y5_R2FR_3671_Hessian_STF_parent_normalization_or_kH_source_coefficient.py`.

## Sources
- `handoff_3669`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3669_NEXT_TARGET.csv` exists=True needle_found=True
- `doc_3669`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\3669-Y5-R2FR-kH-Hessian-STF-parent-owner-or-linear-gamma-bound-row.md` exists=True needle_found=True
- `linear_3669`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3669_LINEAR_MUH_BOUND_ROWS.csv` exists=True needle_found=True
- `profile_3658`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3658_GAMMA_PROFILE_COEFFICIENT_ROWS.csv` exists=True needle_found=True
- `derivation_3668`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3668_KH_KG_PROJECTION_DERIVATION_ROWS.csv` exists=True needle_found=True
- `reduced_3668`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3668_REDUCED_BOUND_INTERFACE_ROWS.csv` exists=True needle_found=True
- `weak_response_2477`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\2477-Y5-R2FR-parent-weak-field-metric-response-theorem-or-no-go.md` exists=True needle_found=True
- `metric_inputs_3384`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3384_METRIC_RESPONSE_INPUT_REQUIREMENTS.csv` exists=True needle_found=True
