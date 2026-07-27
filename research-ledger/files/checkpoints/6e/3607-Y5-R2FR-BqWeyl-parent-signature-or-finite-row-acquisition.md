# 3607 - BqWeyl parent signature or finite row acquisition

## Verdict
3607 does the boring-but-necessary gatekeeping: the no-Weyl-spurion zero route is strong, but it is not parent-signed in the current corpus.

So `B_qWeyl=0` is not promoted.  The finite path is now staged as a real acquisition pack: `B_qWeyl`, `Z_q/G_q`, `M_q/lambda_q`, `C_Weyl` profile, `tau_arena` projections, units, and the `D_qWeyl2` guard.

The shared bottleneck is now q-operator normalization.  Without `Z_q/G_q`, neither the linear `B_qWeyl` route nor the quadratic `D_qWeyl2` route can be scored.

## Parent Signature Audit
- `PSA3607_0_parent_typed_language` / `parent typed object-language`: MISSING_PARENT_SIGNATURE - without it the no-spurion theorem is a closure contract, not parent action
- `PSA3607_1_object_language_exhaustion` / `object-language exhaustion`: MISSING_OBJECT_LANGUAGE_EXHAUSTION - extra local counterterm algebra can reintroduce P^{abcd}
- `PSA3607_2_q_representation` / `q scalar/quotient/pure-density representation`: MISSING_Q_FIELD_CONTENT_CERTIFICATE - q P^{abcd} C_abcd remains legal as a countermodel
- `PSA3607_3_no_spurion_projector` / `no Weyl spurion/projector/readout kernel`: MISSING_NO_SPURION_SIGNATURE - linear B_qWeyl can survive through spurion/projector/readout channel
- `PSA3607_4_hidden_frame_extensions` / `hidden frame exclusion`: MISSING_FRAME_DESCENT_SIGNATURE - effect can move into clocks, matter constants or PPN
- `PSA3607_5_curvature_morphism` / `curvature morphism exclusion`: MISSING_CURVATURE_MORPHISM_EXCLUSION - F(I_hid)R or F(I_hid)C^2 remains legal
- `PSA3607_6_no_higher_curvature_tower` / `quadratic/higher-curvature tower exclusion`: MISSING_HIGHER_CURVATURE_SIGNATURE - linear B_qWeyl cleanup would overclaim without D_qWeyl2 guard
- `PSA3607_7_verdict` / `parent-sign Z_BqWeyl_linear`: ZERO_THEOREM_NOT_ACTIVATED_CURRENT_CORPUS - 3607 cannot parent-sign B_qWeyl=0 from current evidence

## Finite Acquisition Rows
- `BACQ3607_0_Z_linear` / `Z_BqWeyl_linear`: ZERO_SWITCH_NOT_LIVE - theorem switch for linear B_qWeyl absence
- `BACQ3607_1_BqWeyl` / `B_qWeyl`: REQUIRED_FIRST_DANGEROUS - parent coefficient for q P*C or equivalent q-Weyl mixing
- `BACQ3607_2_Zq` / `Z_q`: REQUIRED_SHARED_Q_OPERATOR - q kinetic/operator normalization
- `BACQ3607_3_Mq_lambda` / `M_q^2_or_lambda_q`: REQUIRED_IF_NOT_MASSLESS - q range/mass gap for Yukawa/local response
- `BACQ3607_4_CWeyl_profile` / `C_Weyl_local_profile`: REQUIRED_PROFILE_INPUT - local Weyl/tidal curvature source profile
- `BACQ3607_5_tau_R10` / `tau_BqWeyl_R10`: REQUIRED_ARENA_PROJECTION - projection into R10/contact/short-range branch
- `BACQ3607_6_tau_PPN` / `tau_BqWeyl_PPN`: REQUIRED_ARENA_PROJECTION - projection into PPN gamma/beta/preferred-frame residuals
- `BACQ3607_7_tau_clock` / `tau_BqWeyl_clock`: REQUIRED_ARENA_PROJECTION - projection into clock/redshift/frequency drift
- `BACQ3607_8_tau_orbital` / `tau_BqWeyl_orbital`: REQUIRED_ARENA_PROJECTION - projection into orbital precession/source-GM residual
- `BACQ3607_9_DqWeyl2_guard` / `D_qWeyl2`: SEPARATE_GUARD_REQUIRED - quadratic Weyl/higher-curvature guard
- `BACQ3607_10_C2_projection` / `C2_Schw_or_source_C2`: GUARD_KERNEL_NONCLAIM - Schwarzschild/exterior C_abcd C^abcd projection identity
- `BACQ3607_11_acceptance_rule` / `E_BqWeyl_acceptance`: ACCEPTANCE_GATE - E_BqWeyl can leave epsilon_Dq_vq only by zero switch or complete finite row pack

## Activation Gates
- `ACT3607_0_index_theorem_available`: PASS_CONDITIONAL - metric/epsilon-only one-Weyl terms vanish
- `ACT3607_1_parent_signature`: FAIL_CURRENT_CLAIM - all parent signature clauses are unsigned or missing
- `ACT3607_2_finite_inputs`: FAIL_CURRENT_CLAIM - B_qWeyl, Z_q/G_q, C_Weyl profile and arena projections are missing
- `ACT3607_3_DqWeyl2_guard`: PASS_GUARD - quadratic Weyl remains separate and unpromoted
- `ACT3607_4_no_local_vacuum_shortcut`: PASS_GUARD - Weyl/tidal curvature survives exterior vacuum
- `ACT3607_5_no_epsilonDq_vq_cleanup`: FAIL_CURRENT_CLAIM - E_BqWeyl cannot leave epsilon_Dq_vq
- `ACT3607_6_next_route`: PASS_ROUTE_SELECTED - q operator normalization is the shared finite-path bottleneck

## Status
- `BQWEYL_PARENT_SIGNATURE_FAILED_FINITE_INPUT_PACK_STAGED`: 3607 audits the no-Weyl-spurion route clause-by-clause and finds it is not parent-signed. It stages the finite BqWeyl acquisition pack: B_qWeyl, Z_q/G_q, M_q/lambda_q, C_Weyl profile, arena projections, units, and D_qWeyl2 guard.
- Decision: do not promote B_qWeyl=0; do not score a finite bound yet; move next to q-operator normalization because it is shared by B_qWeyl and D_qWeyl2 finite routes
- Still missing: parent typed grammar, object-language exhaustion, q representation, no Pabcd spurion/projector/readout, hidden-frame exclusion, curvature morphism exclusion, B_qWeyl coefficient, Z_q/G_q, M_q/lambda_q, C_Weyl profile, R10/PPN/clock/orbital projections and D_qWeyl2 no-tower closure

## Validation
- `VAL3607_0_sources_exist`: PASS (all required 3607 source paths exist)
- `VAL3607_1_needles_found`: PASS (all selected 3607 source anchors found)
- `VAL3607_2_outputs_exist`: PASS (all pre-validation 3607 csv output files written)
- `VAL3607_3_csv_parse`: PASS (source_register:17; parent_signature_audit:8; finite_acquisition_rows:12; activation_gates:7; status:1; next_target:1; canonical_status:1)
- `VAL3607_4_signature_audit_complete`: PASS (parent signature audit covers all no-spurion clauses)
- `VAL3607_5_finite_rows_present`: PASS (finite BqWeyl acquisition rows present)
- `VAL3607_6_parent_signature_blocked`: PASS (parent no-spurion signature remains blocked)
- `VAL3607_7_finite_inputs_blocked`: PASS (finite BqWeyl input pack remains blocked)
- `VAL3607_8_DqWeyl2_guard`: PASS (DqWeyl2 guard remains active)
- `VAL3607_9_next_target_selected`: PASS (3608 q-operator target selected)
- `VAL3607_10_no_claim_flags`: PASS (all generated physics rows remain nonclaim)
- `VAL3607_11_generated_source_paths_exist`: PASS (every generated row source_path exists)
- `VAL3607_12_formalization_workbench_untouched`: PASS (no 3607 checkpoint output appears in formalization-workbench outside package/venv noise)

## Next target
- `NEXT3607_0` -> `3608-Y5-R2FR-q-operator-normalization-or-BqWeyl-bound-runner-blocker.md`
- Objective: try to derive or source Z_q/G_q and the q operator domain/norm shared by B_qWeyl and D_qWeyl2; if not, keep the finite Weyl bound runner blocked with exact missing inputs
