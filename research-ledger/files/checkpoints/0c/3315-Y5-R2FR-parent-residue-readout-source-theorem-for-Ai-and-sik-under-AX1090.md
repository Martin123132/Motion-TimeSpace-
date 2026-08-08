# 3315 - Parent residue/readout/source theorem for Ai and sik under AX1090

Run UTC: `2026-06-27T19:34:35.416776+00:00`

## Verdict

This checkpoint gets a real piece of the coupling problem, not just a new missing-list.

Inside the public-Hilbert matter branch, the leading nonrelativistic dust source charge of each finite mode is proportional to ordinary mass. Therefore the leading WEP composition vector vanishes:

`s_ik^dust = 0`.

That is not the whole local-GR proof. It leaves a cleaner problem: `A_i` splits into a parent Hessian/readout factor and named residual tails:

`A_0 = (1/3) Z_0 U_0 [1 + epsilon_0(Earth)]`

`A_2 = (-4/3) Z_2 U_2 [1 + epsilon_2(Earth)]`

So the next top blocker is no longer an opaque coupling. It is the parent quadratic Hessian/readout extraction for `Z_i U_i`, plus bounded residuals for stress, binding, EM/Poynting, support, shadow frames, and non-Hilbert currents.

## Source Register

- `SRC3315_0_3314_doc`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\3314-Y5-R2FR-parent-Ai-derivation-or-final-WEP-likelihood-blocker-ranking-under-AX1090.md` - exists=true; parse_ok=true; role=3314 handoff naming parent A_i/source-factor derivation as top blocker
- `SRC3315_1_3314_Ai`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3314_PARENT_Ai_DERIVATION_ATTEMPT.csv` - exists=true; parse_ok=true; role=conditional A_0/A_2 identities and no-G-cal absorption guard
- `SRC3315_2_3314_factor`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3314_Ai_FACTOR_CLAUSE_AUDIT.csv` - exists=true; parse_ok=true; role=four unsigned factor clauses: Z, U, Xi, s_ik
- `SRC3315_3_3303_alpha`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3303_GENERALIZED_ALPHA_AMPLITUDE_LAW.csv` - exists=true; parse_ok=true; role=general finite-mode alpha law
- `SRC3315_4_3305_projector`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3305_PARENT_PROJECTOR_IDENTITY_DERIVATION.csv` - exists=true; parse_ok=true; role=Hilbert-source projector identity and universality theorem attempt
- `SRC3315_5_3311_factor`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3311_ALPHA_XI_FACTOR_LAW.csv` - exists=true; parse_ok=true; role=A_i as finite-mode source factor, not calibrated Newton G
- `SRC3315_6_1031_spm`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1031-Y5-R10-quotient-naturality-terminal-public-metric-proof-or-spm-closure.md` - exists=true; parse_ok=true; role=single-public-metric route closure status and shadow-frame counterexample guard
- `SRC3315_7_1045_matter_functor`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1045-Y5-R10-parent-matter-functor-descent-signature-or-qbar-component-fill.md` - exists=true; parse_ok=true; role=matter functor descent and no-shadow-frame source marker rows
- `SRC3315_8_1035_kernel`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1035-Y5-R10-KX-green-kernel-normalization-and-profile-integral.md` - exists=true; parse_ok=true; role=source-test product warning and finite-mode kernel normalization split

## Theorem Attempt

- `THM3315_0_branch_domain` `CONDITIONAL_BRANCH`: Work inside the public-Hilbert branch, not as a new axiom. Assume ordinary matter is varied only through the observed/public metric or coframe: S_matter = Sbar[Psi, g_pub(q(Phi)), theta(q)]. This is exactly the branch needed by 3305 and explicitly not the closure-only SPM claim unless the parent action later signs the matter functor. Still needed: parent action must derive the public-Hilbert matter interface.
- `THM3315_1_variation` `DERIVED_CONDITIONAL`: Finite-mode matter charges are Hilbert-source projections. For delta g_pub_mu_nu = sum_i U_i e_i_mu_nu delta phi_i, variation gives delta S_m = 1/2 int sqrt(-g) T_H^{mu nu} delta g_pub_mu_nu, hence J_i[A] = (U_i/2) int_A sqrt(-g) T_H^{mu nu} e_i_mu_nu. Still needed: mode tensors e_i and normalization from parent Hessian.
- `THM3315_2_dust_limit` `DERIVED_WITHIN_BRANCH`: The composition residual s_ik vanishes in the ideal local dust/public-projector limit. For nonrelativistic dust T_H^{mu nu} = rho u^mu u^nu and for a static local projector with e_i_mu_nu u^mu u^nu = c_i constant over ordinary matter, J_i[A] = (U_i c_i/2) int_A rho dV = C_i M_A. Therefore Xi_i[A] = J_i[A]/(C_i M_A) = 1 for every body A, so Delta Xi_i[A,B] = 0 and s_ik^dust = 0. Still needed: residual stress, binding, EM/Poynting, support, and shadow-frame tails.
- `THM3315_3_Ai_split` `DERIVED_SPLIT_NOT_NUMERIC`: The source factor splits into a Hessian/readout part and an Earth residual part. A_0 = (1/3) Z_0 U_0 [1 + epsilon_0(Earth)] and A_2 = (-4/3) Z_2 U_2 [1 + epsilon_2(Earth)]. The old blank Xi_i[Earth] is now an explicit residual expansion rather than an arbitrary fitted knob. Still needed: Z_i U_i from parent quadratic Hessian and epsilon_i(Earth) bounds.
- `THM3315_4_no_G_absorption` `GUARDRAIL`: The finite-mode A_i cannot be hidden inside Newton G. G_cal fixes the massless graviton coefficient in the 1/r channel. Z_i U_i multiplies finite-range modes and epsilon_i source residuals. Absorbing A_i into G_cal would erase a range-dependent and mode-dependent force that is tested separately by WEP/R10/PPN/clock/orbital arenas. Still needed: none for the guardrail.
- `THM3315_5_countermodel` `COUNTERMODEL_SURVIVES_OUTSIDE_BRANCH`: Terminal/public metric language alone does not prove the theorem. A matter functor can evaluate a species frame, marker, non-Hilbert current, mass constant, or support profile before mapping to the public metric. Such a countermodel preserves notation but reintroduces body-dependent Xi_i[A]. Still needed: parent no-shadow-frame/no-non-Hilbert-current theorem.

## Dust Limit Proof

- `DUST3315_0_source_tensor` `T_H^{mu nu}`: In a local nonrelativistic ordinary body, T_H^{mu nu} = rho u^mu u^nu + stress/c^2 + field momentum terms. Result: `leading term isolated`.
- `DUST3315_1_mode_projection` `e_i_mu_nu u^mu u^nu`: If the local static public-metric mode projector is material-blind, its contraction on u^mu u^nu is a constant c_i for ordinary matter. Result: `conditional constant c_i`.
- `DUST3315_2_charge_integral` `J_i[A]`: J_i[A] = (U_i c_i/2) int_A rho dV = C_i M_A. Result: `J_i[A]/M_A = C_i for all A`.
- `DUST3315_3_sik_zero` `s_ik^dust`: With Xi_i[A] = J_i[A]/(C_i M_A), Xi_i[A] = 1 and Delta Xi_i[A,B] = 0. Result: `s_ik^dust = 0`.
- `DUST3315_4_limits` `residual epsilon_i[A]`: The proof does not kill stress, binding, EM/Poynting momentum-flow, support/readout, or shadow-frame residuals. Result: `epsilon_i[A] envelope remains required`.

## Factor Split Result

- `FS3315_0_Z_residue` `Z_0,Z_2`: PARENT_HESSIAN_REQUIRED. Law: Z_i is the canonical residue/sign of the finite-mode quadratic kinetic operator after diagonalization.
- `FS3315_1_U_readout` `U_0,U_2`: PUBLIC_READOUT_OVERLAP_REQUIRED. Law: U_i is the overlap of diagonal finite mode phi_i with delta g_pub in the ordinary readout channel.
- `FS3315_2_Xi_source` `Xi_i[A]`: DUST_LIMIT_FIXED_RESIDUAL_EXPANDED. Law: Xi_i[A] = 1 + epsilon_i^stress[A] + epsilon_i^bind[A] + epsilon_i^EM_Poynting[A] + epsilon_i^support[A] + epsilon_i^shadow[A] + epsilon_i^nonH[A].
- `FS3315_3_sik` `s_ik`: ZERO_AT_DUST_ORDER_NONZERO_RESIDUAL_TAIL. Law: s_i dot Delta_q[A,B] = Delta epsilon_i^stress + Delta epsilon_i^bind + Delta epsilon_i^EM_Poynting + Delta epsilon_i^support + Delta epsilon_i^shadow + Delta epsilon_i^nonH.
- `FS3315_4_A0` `A_0`: SPLIT_LAW_NOT_NUMERIC. Law: A_0 = (1/3) Z_0 U_0 [1 + epsilon_0(Earth)].
- `FS3315_5_A2` `A_2`: SPLIT_LAW_NOT_NUMERIC. Law: A_2 = (-4/3) Z_2 U_2 [1 + epsilon_2(Earth)].

## Residual Source Envelope

- `RES3315_0_stress_pressure` `epsilon_i^stress[A]`: finite-mode projector applied to pressure, anisotropic stress, elastic stress, and internal kinetic stress divided by the dust mass charge Next input: stress-energy model or conservative bound per material.
- `RES3315_1_binding` `epsilon_i^bind[A]`: nuclear, atomic, chemical, and gravitational binding-energy fraction response under the finite-mode projector Next input: material assay/binding proxies for Ti/Al/V/Pt/Rh/Be.
- `RES3315_2_EM_Poynting` `epsilon_i^EM_Poynting[A]`: finite-mode projection of EM stress, field energy, and momentum-flow terms including S = E x B / mu0 where fields/waves carry support momentum Next input: static EM binding estimate for ordinary matter plus separate wave/media stress test branch.
- `RES3315_3_support_readout` `epsilon_i^support[A]`: finite-size, geometry, shielding, source/test profile, and readout-kernel mismatch corrections Next input: arena profile integrals K_i(lambda), Qbar_i, tau_i.
- `RES3315_4_shadow_frame` `epsilon_i^shadow[A]`: hidden conformal/disformal/species frame response not mediated solely by g_pub Next input: parent no-shadow-frame theorem or explicit coefficient bounds.
- `RES3315_5_nonHilbert` `epsilon_i^nonH[A]`: direct non-Hilbert current, material marker, or source-normalization dependency Next input: parent current-chain exclusion or empirical envelope.

## Test Projection Map

- `WEP_MICROSCOPE_EotWash`: eta_AB(lambda) = sum_i K_i(lambda) Z_i U_i [1 + epsilon_i(Earth)] Delta epsilon_i[A,B] Derived now: Delta epsilon_i^dust = 0. Missing: Z_i U_i, Earth residual, material residual differences, covariance.
- `R10_short_range`: alpha_R10(lambda) = K_i^R10(lambda) beta_source beta_test + epsilon_tail Derived now: beta_source/test are Hilbert-source residual projections in public-Hilbert branch. Missing: R10 geometry kernels, material profiles, Z_i, lambda_i.
- `PPN_local_GR`: gamma-1, beta-1, preferred-frame terms from finite-mode residue/readout plus residual source tails Derived now: composition source residual is not the first-order dust problem. Missing: Z_i U_i sign/range, Vainshtein/screening or decoupling proof, nonlinear metric limit.
- `clocks_EM`: clock residual = projection of stress, EM binding, alpha_EM/mass response, and Poynting/momentum-flow terms Derived now: EM belongs inside T_H and residual epsilon, not outside the coupling analysis. Missing: alpha_EM/mass derivative theorem or coefficient bounds.
- `orbital_Newton`: G_cal massless 1/r channel plus finite-mode Yukawa residues; no A_i absorption into G_cal Derived now: source charge proportional to mass at dust order. Missing: finite-mode range/amplitude or proof of local decoupling.

## Promotion Gates

- `GATE3315_0_dust_source_zero`: passed=true; claim=s_ik^dust = 0 in public-Hilbert local dust limit; reason=derived from Hilbert-source variation plus material-blind static projector
- `GATE3315_1_full_source_zero`: passed=false; claim=s_ik = 0 exactly for real materials; reason=stress, binding, EM/Poynting, support, shadow-frame, and non-Hilbert residuals remain
- `GATE3315_2_numeric_Ai`: passed=false; claim=A_0 and A_2 are numeric/parent-owned; reason=Z_i U_i requires parent quadratic Hessian/readout extraction
- `GATE3315_3_local_GR`: passed=false; claim=local GR/Newtonian limit is recovered; reason=finite-mode amplitude/range and residual tails are not yet closed

## Decision

- `DEC3315_0`: yes: it proves the leading WEP source-composition vector vanishes at dust order inside the public-Hilbert branch - Hilbert-source variation makes finite-mode charge proportional to mass for material-blind local static projectors Next: do not treat s_ik as a primary free coupling; treat it as a residual epsilon envelope.
- `DEC3315_1`: parent quadratic Hessian/readout extraction for Z_i U_i, plus residual epsilon bounds - A_i now splits into Z_i U_i times [1 + epsilon_i(Earth)] Next: attempt parent Hessian/readout extraction for Z_i U_i before more empirical WEP polishing.
- `DEC3315_2`: inside the Hilbert stress residual epsilon_i^EM_Poynting, not as a separate magic coupling - EM field energy and momentum flow contribute to T_H and can affect clocks/material/wave stress branches Next: after Hessian extraction, build a bounded EM/Poynting residual branch.

## Next Target

- `3316-Y5-R2FR-parent-quadratic-hessian-readout-extraction-for-ZiUi-under-AX1090.md`
- `scripts/Y5_R2FR_3316_parent_quadratic_hessian_readout_extraction_for_ZiUi.py`
- Objective: extract or bound Z_i U_i from the parent quadratic action/Hessian and public readout map, using 3315's source theorem so A_i is no longer a single opaque coupling
- Fallback: demote Z_i U_i to empirical finite-mode amplitude envelopes and proceed to EM/Poynting residual bounds
