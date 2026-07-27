# 3567 - Local LC branch selector or Kspin P4 map

## Verdict
3567 gives the first real selector mechanism for the LC/no-independent-affine branch.  Write the distortion field `C = Gamma - Gamma_LC[g_obs]`.  If `C` is absent, 3566 already gives the LC branch kinematically.  If `C` is present, the parent must provide an equation `M_C C = Delta_Gamma - B_C - P_C - N_C(C)`.

The useful theorem is exact but conditional: if `M_C` is coercive/positive on non-gauge modes, `Delta_Gamma=0`, boundary work vanishes, projective leakage vanishes, and nonlinear terms stay inside the small branch, then `C=0`.  If any of those fail, the same equation gives the `K_spin/lambda_C` P4 bound map.

So the local connection problem has moved from 'what is the coupling?' to a concrete target: derive/source the distortion operator `M_C` and its sign certificate.

## Generated outputs
- `source_register`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3567_SOURCE_REGISTER.csv`
- `selector_theorem`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3567_LOCAL_LC_SELECTOR_THEOREM.csv`
- `distortion_proof`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3567_DISTORTION_ZERO_PROOF.csv`
- `kspin_map`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3567_KSPIN_P4_BOUND_MAP.csv`
- `activation_gates`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3567_SELECTOR_ACTIVATION_GATES.csv`
- `decision_ledger`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3567_DECISION_LEDGER.csv`
- `status`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3567_STATUS.csv`
- `next_target`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3567_NEXT_TARGET.csv`
- `canonical_status`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_local_LC_branch_selector_status.csv`
- `validation`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_BRR545_3567_VALIDATION.csv`

## Selector theorem
- `SEL3567_0_distortion_variable`: C^lambda_{mu nu} := Gamma^lambda_{mu nu} - Gamma_LC^lambda_{mu nu}[g_obs] (EXACT_DEFINITION)
- `SEL3567_1_domain_selector`: Allowed(Conf_loc^LC) excludes C/Gamma_ind/omega_ind. (PRIVATE_SELECTOR_BRANCH_NOT_PUBLIC_DERIVATION)
- `SEL3567_2_dynamic_selector_equation`: delta_C S_parent = M_C C - Delta_Gamma + B_C + P_C + N_C(C) = 0 (SELECTOR_EQUATION_WRITTEN)
- `SEL3567_3_positive_zero_theorem`: If <C,M_C C> >= lambda_C ||C||^2, Delta_Gamma=B_C=P_C=0, and ||N_C(C)|| <= c_N ||C||^2 inside c_N||C|| < lambda_C, then C=0. (EXACT_CONDITIONAL_SELECTOR_THEOREM)
- `SEL3567_4_bound_theorem`: ||C|| <= lambda_C^-1 (||Delta_Gamma|| + ||B_C|| + ||P_C|| + ||N_C(C)||) (BOUND_FORMULA_READY_VALUES_MISSING)
- `SEL3567_5_Espin_link`: E_spin_abs <= K_spin ||C|| + epsilon_noGamma_branch (P4_MAP_SYMBOLIC_NONCLAIM)
- `SEL3567_6_live_verdict`: The LC selector is derived as a conditional theorem, but not activated as a public parent theorem because M_C positivity, boundary/projective silence and parent-owned C equation are unsigned. (CONDITIONAL_SELECTOR_NOT_PUBLIC_CLAIM)

## Distortion proof
- `DZ3567_0_equation` `Euler equation`: M_C C = Delta_Gamma - B_C - P_C - N_C(C) (STARTING_POINT)
- `DZ3567_1_energy_identity` `multiply by C and integrate over compact local exterior A`: <C,M_C C> = <C,Delta_Gamma-B_C-P_C-N_C(C)> + boundary_pairing (EXACT_CONDITIONAL_IDENTITY)
- `DZ3567_2_coercivity` `positive/invertible nonprojective operator`: <C,M_C C> >= lambda_C ||C||^2 after quotienting gauge/projective zero modes (MISSING_PARENT_SIGN_CERTIFICATE)
- `DZ3567_3_source_zero` `hypermomentum/source zero`: Delta_Gamma=0 if 3566 no-Gamma branch is selected across matter/source/readout sectors (PRIVATE_BRANCH_PASS_PUBLIC_SELECTOR_OPEN)
- `DZ3567_4_boundary_zero` `connection boundary work`: B_C=0 if integration-by-parts, symplectic and worldtube boundary C-work are fixed/proper/no-flux (BOUNDARY_UNSIGNED_RETAINS_ROW)
- `DZ3567_5_projective_zero` `projective kernel`: P_C=0 if projective trace is absent, gauge-fixed or all-sector unobservable (PROJECTIVE_UNSIGNED_RETAINS_ROW)
- `DZ3567_6_nonlinear_radius` `small-branch control`: ||N_C(C)|| <= c_N ||C||^2 and c_N||C|| < lambda_C (LOCAL_SMALL_BRANCH_PREMISE_UNSIGNED)
- `DZ3567_7_zero_result` `LC dynamic selector`: C=0 (EXACT_IF_DZ3567_2_TO_DZ3567_6_PASS_TOGETHER)
- `DZ3567_8_bound_result` `affine fallback`: ||C|| <= lambda_C^-1(||Delta_Gamma||+||B_C||+||P_C||+||N_C||) (P4_BOUND_IF_ANY_PREMISE_FAILS)

## Kspin/P4 map
- `KSP3567_0_master` `epsilon_local_connection`: epsilon_local_connection <= K_spin lambda_C^-1 (||Delta_Gamma||+||B_C||+||P_C||+||N_C||) (SYMBOLIC_EXECUTABLE_FORMULA_NONCLAIM)
- `KSP3567_1_axial_torsion` `epsilon_axial_torsion_spin`: epsilon_axial_torsion_spin <= K_A ||C_axial|| (ZERO_IF_SELECTOR_CLOSES_ELSE_COEFFICIENT_MISSING)
- `KSP3567_2_projective_trace` `epsilon_projective_trace`: epsilon_projective_trace <= K_P ||C_projective|| (ZERO_IF_PROJECTIVE_GUARD_CLOSES_ELSE_BOUND_MISSING)
- `KSP3567_3_weyl_nonmetricity` `epsilon_weyl_nonmetricity`: epsilon_weyl_nonmetricity <= K_Q ||Q_mu|| (ZERO_IF_METRIC_COMPATIBILITY_SELECTOR_CLOSES_ELSE_BOUND_MISSING)
- `KSP3567_4_shear_nonmetricity` `epsilon_shear_nonmetricity`: epsilon_shear_nonmetricity <= K_Qs ||Q_tilde|| (ZERO_IF_OPTICAL_METRIC_SELECTOR_CLOSES_ELSE_BOUND_MISSING)
- `KSP3567_5_hypermomentum` `epsilon_hypermomentum_source`: epsilon_hypermomentum_source <= K_Delta ||Delta_Gamma|| (ZERO_INSIDE_3566_BRANCH_ELSE_KERNEL_MISSING)
- `KSP3567_6_lambdaC` `lambda_C`: lambda_C = lower coercivity bound of M_C on non-gauge/nonprojective C modes (MISSING_PARENT_SIGN_AND_UNITS)

## Activation gates
- `GATE3567_0_equation_owner`: FAIL (M_C C = Delta_Gamma - B_C - P_C - N_C(C) is written as a selector law but not parent-derived)
- `GATE3567_1_noGamma_source`: PASS_PRIVATE_BRANCH_ONLY (3566 gives zero inside LC branch; public selector still needed)
- `GATE3567_2_positive_MC`: FAIL (lambda_C/sign/operator units are missing)
- `GATE3567_3_boundary_projective`: FAIL (boundary and projective kernels remain open)
- `GATE3567_4_zero_selector`: FAIL_CURRENT_PUBLIC_CLAIM (exact conditional theorem exists but inputs not parent-signed together)
- `GATE3567_5_bound_branch`: PARTIAL_SYMBOLIC_PASS (formula exists; numeric/source-backed K_spin/lambda_C missing)

## Decisions
- `DEC3567_0_selector_mechanism_written`: use the distortion positive-operator equation as the branch selector mechanism -> the missing step is now M_C/sign/boundary/projective/source inputs, not a vague coupling problem
- `DEC3567_1_no_public_promotion`: do not promote LC selector as a public parent theorem -> retain K_spin/P4 map
- `DEC3567_2_best_next`: derive or source the distortion operator M_C next -> 3568 targets M_C operator/sign certificate or first lambda_C/K_spin source row

## Status
- `LC_SELECTOR_CONDITIONAL_THEOREM_WRITTEN_NOT_PUBLICLY_ACTIVATED`: distortion equation plus positive operator theorem gives C=0 if M_C is coercive and source/boundary/projective terms vanish

## Validation
- `VAL3567_0_sources_exist`: PASS (all required source paths exist)
- `VAL3567_1_required_needles_found`: PASS (all selected source needles found)
- `VAL3567_2_outputs_exist`: PASS (all pre-validation 3567 output files written)
- `VAL3567_3_csv_parse`: PASS (source_register:17; selector_theorem:7; distortion_proof:9; kspin_map:7; activation_gates:6; decision_ledger:3; status:1; next_target:1; canonical_status:1)
- `VAL3567_4_selector_equation_present`: PASS (distortion selector equation row present)
- `VAL3567_5_positive_zero_theorem_present`: PASS (positive C=0 theorem and proof row present)
- `VAL3567_6_kspin_bound_map_present`: PASS (K_spin/lambda_C fallback map rows present)
- `VAL3567_7_public_claim_blocked`: PASS (public selector claim remains blocked)
- `VAL3567_8_nonclaim_flags`: PASS (all generated physics rows remain nonclaim)
- `VAL3567_9_formalization_workbench_untouched`: PASS (no 3567 checkpoint output appears in formalization-workbench)

## Next target
- `3568-Y5-R2FR-distortion-operator-MC-sign-certificate-or-lambdaC-bound.md`
- Objective: derive a parent-owned positive/invertible distortion operator M_C with units and boundary domain; if not possible, create the first source-ready lambda_C/K_spin bound row
