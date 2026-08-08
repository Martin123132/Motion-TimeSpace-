# 4720 - EH Reduction Parent Signature or Non-EH Operator Coefficient Matrix

Generated: `2026-07-07T21:41:45+00:00`

## Purpose

4719 derived the weak-field bridge:

`nabla^2 Phi_N = 4*pi*G_eff*rho + (c^2/2)E_00`.

So the next highest-leverage question is whether `E_mu_nu` is actually zero at the local principal GR order. This checkpoint takes the least hand-wavy route:

- try to force EH from a parent IR selector;
- if the selector is not signed, every failure becomes a coefficient in a non-EH operator matrix.

## Selector Theorem

If the visible local geometry is single-metric/coframe, local, covariant, parity-even and two-derivative, with algebraic/silent torsion and no extra scalar/vector/disformal/memory/source coefficient target, the EH/EC bulk term is the unique principal operator up to `Lambda`, topological and boundary terms.

This is the cleanest route because it does not tune local tests. It narrows the theory language until the GR left-hand side is forced.

## Theorem Rows

- `EHS4720_0_selector_theorem` (conditional_sufficiency_theorem): If the local visible geometry sector is single-metric/coframe, local, diffeomorphism and local-Lorentz covariant, parity-even, two-derivative, and has no propagating torsion/nonmetricity or extra scalar/vector coefficient target, the only principal bulk operator is Einstein-Hilbert plus Lambda/topological/boundary terms.
- `EHS4720_1_what_it_kills` (exact_if_selector_signed): The selector kills independent local R^2, Ricci^2, Weyl^2, scalar-tensor, vector/preferred-frame, disformal/second-metric, torsion/nonmetricity and memory-source operators at the principal local GR order.
- `EHS4720_2_what_it_does_not_kill` (firewall): The selector does not derive the numerical value of M_EH, does not sign source coupling by itself, and does not close boundary/readout/local-test residuals.
- `EHS4720_3_verdict` (private_nonclaim_progress): 4720 converts the EH bottleneck into a real fork: sign the parent EH selector, or fill the non-EH coefficient matrix.

## Parent Signature Clauses

- `EHSC4720_0_single_geometry`: one observed metric/coframe is the only local matter/gravity geometry Blocks `second metric/disformal leak`; fallback `c_D`.
- `EHSC4720_1_local_covariant_4form`: bulk action is a local diffeo/Lorentz-covariant 4-form Blocks `noncovariant projector force terms`; fallback `c_proj`.
- `EHSC4720_2_two_derivative_IR`: principal local IR operator is two-derivative Blocks `R2/Ricci2/Weyl2 higher-derivative modes`; fallback `c_R2_or_M_R`.
- `EHSC4720_3_parity_even_no_vector`: no independent parity-odd or preferred-frame vector selector in compact local branch Blocks `alpha_i/xi side channels`; fallback `c_vec`.
- `EHSC4720_4_torsion_resolution`: torsion/nonmetricity are algebraic and vanish in compact spinless branch or are heavy/bounded Blocks `torsion/nonmetricity preferred-frame and clock residuals`; fallback `c_T_or_c_Q`.
- `EHSC4720_5_boundary_topological`: boundary/topological terms are fixed, source-blind, and do not create bulk source charge Blocks `boundary mass/current hair`; fallback `c_bdy`.
- `EHSC4720_6_no_memory_operator`: local collar has no independent Gamma/memory operator in the EH principal block Blocks `range/local memory leakage`; fallback `c_Gamma`.
- `EHSC4720_7_common_coupling_separate`: M_EH and lambda_D are common parent normalizations, not relative source coefficients Blocks `source-prefactor hiding inside G`; fallback `delta_kappa_or_delta_w`.

## Non-EH Coefficient Matrix

- `NEH4720_0_R2_fR_scalar` / `c_R2_or_c_fR, M_R`: sqrt(-g)(c_R2 R^2 + c_fR f_extra(R)) -> scalar finite-range mode; gamma/beta slip; R10 Yukawa alpha(lambda)
- `NEH4720_1_Ricci_Weyl_squared` / `c_Ricci, c_Weyl`: sqrt(-g)(c_Ricci R_mn R^mn + c_Weyl C_mnrs C^mnrs) -> spin-2/higher-derivative slip; xi/tidal/wave-sector tails
- `NEH4720_2_torsion_nonmetricity` / `c_T, c_Q`: c_T T^2 + c_Q Q^2 plus spin/light-cone connection couplings -> preferred-frame, clock, WEP, light-cone residuals
- `NEH4720_3_scalar_tensor` / `F_phi, c_scalar`: sqrt(-g)[F(phi)R - 1/2(d phi)^2 - V(phi)] -> gamma/beta/Gdot/R10/clock residuals
- `NEH4720_4_vector_preferred_frame` / `c_vec`: u^mu, selector normal, domain velocity, or preferred-frame vector terms -> alpha1/alpha2/alpha3/xi
- `NEH4720_5_second_metric_disformal` / `c_D, b_dis`: matter/source sees g_tilde_mn=A^2 g_mn+B^2 v_m v_n -> WEP, gamma, clocks, fifth-force response
- `NEH4720_6_memory_Gamma` / `c_Gamma`: Gamma_eff/K_hat memory operator in local collar -> range-dependent local force; cosmology-local leakage; PPN drift
- `NEH4720_7_boundary_charge` / `c_bdy`: non-topological boundary/corner/source reference term -> source normalization, alpha3, orbital/clock drift
- `NEH4720_8_Lambda_local` / `Lambda_eff_local`: zeroth-order local vacuum term -> constant/tidal acceleration; local background curvature
- `NEH4720_9_source_normalization` / `delta_w, delta_kappa, epsilon_mu`: source-only prefactor or extra mass-channel coefficient -> WEP/R10/PPN/Gdot/source charge residual

## Projection Kernels

- `PROJ4720_0_Poisson` / `Delta_Poisson`: sum_i Pi_N_i c_i <= PB4719_1_fractional_density_region target
- `PROJ4720_1_gamma` / `gamma_minus_1`: sum_i Pi_gamma_i c_i <= gamma_bound
- `PROJ4720_2_beta` / `beta_minus_1`: sum_i Pi_beta_i c_i <= beta_bound
- `PROJ4720_3_preferred_frame` / `alpha1_alpha2_alpha3_xi`: sum_i Pi_vec_i c_i <= row-specific alpha/xi bounds
- `PROJ4720_4_R10` / `alpha_lambda`: alpha_predicted(lambda;c_i,m_i) <= alpha_bound(lambda) for all lambda rows
- `PROJ4720_5_Gdot_orbital_clock` / `Gdot_clock_orbital`: D_tau ln(lambda_D/M_EH^2)+sum_i Pi_time_i c_i below local drift bounds

## Gates

- `GATE4720_0_selector_signed`: passed=False; blocker=`PARENT_EH_SELECTOR_UNSIGNED`.
- `GATE4720_1_no_extra_operator_targets`: passed=False; blocker=`NONEH_OPERATOR_TARGET_AUDIT_NEEDED`.
- `GATE4720_2_matrix_numeric_or_zero`: passed=False; blocker=`NONEH_MATRIX_UNFILLED`.
- `GATE4720_3_projection_kernels_sourced`: passed=False; blocker=`PROJECTION_KERNELS_SYMBOLIC`.
- `GATE4720_4_no_poisson_to_ppn_shortcut`: passed=False; blocker=`FULL_PPN_SHARED_CONVENTION_NEEDED`.

## Source Register

- `SRC4720_0`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4719_RESIDUAL_CLOSURE_GATES.csv`; exists=True; needle_found=True; role=4719 identifies EH principal-block ownership as the next bottleneck.
- `SRC4720_1`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4719_PPN_RESIDUAL_VECTOR_ROWS.csv`; exists=True; needle_found=True; role=4719 separates Poisson from full PPN spatial-curvature recovery.
- `SRC4720_2`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4719_POISSON_RESIDUAL_BOUND_ROWS.csv`; exists=True; needle_found=True; role=4719 normalized Poisson residual that non-EH terms feed.
- `SRC4720_3`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4278_LEFT_HAND_OPERATOR_GATE.csv`; exists=True; needle_found=True; role=4278 earlier fork from conditional EH to residual EFT coefficients.
- `SRC4720_4`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4278_PALATINI_SELECTOR_CLAUSES.csv`; exists=True; needle_found=True; role=IR/two-derivative selector clause for EH principal operator.
- `SRC4720_5`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4278_RESIDUAL_EFT_COEFFICIENT_MAP.csv`; exists=True; needle_found=True; role=Residual EFT coefficient map for curvature-squared terms.
- `SRC4720_6`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\MTS_local_residual_predictions_TEMPLATE.csv`; exists=True; needle_found=True; role=Local residual template requiring non-EH operator ledger rows.
- `SRC4720_7`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_MU_EXTRA_LOCAL_BOUND_SCORECARD.csv`; exists=True; needle_found=True; role=Existing scorecard rows showing non-EH operator potential blocks gamma/beta/R10/R11.
- `SRC4720_8`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\R11_nonEH_operator_vector_executable.csv`; exists=True; needle_found=True; role=Existing executable skeleton for non-EH operator family coefficients.

## Decision

`EH_SELECTOR_THEOREM_CONDITIONAL_NONEH_OPERATOR_MATRIX_STAGED_NONCLAIM`

## Next Target

`4721-Y5-R2FR-two-derivative-EH-selector-proof-or-R2-scalar-range-bound-row.md`
