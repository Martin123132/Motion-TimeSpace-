# 3224 - Finite Alpha Bound Propagator Clock/WEP/R10 under AX1090

Private checkpoint. This is not a local-GR claim, Maxwell derivation claim, Newtonian-limit claim, WEP pass, R10 pass, clock pass, `b_alpha_m=0` claim, EM-lock claim, or public-facing result.

## Result

3224 builds the finite-alpha propagator.

The important result is not a pass. It is a reusable gate:

```text
MTS alpha input -> clock/WEP/R10 product prediction -> compare only against source-valid bounds.
```

The propagator imports real anchor rows where they exist:

```text
clock: product bounds such as |b_alpha * tau_clock_time|
WEP: MICROSCOPE alpha/Coulomb projection target
R10: projection law definitions, but no promoted bound/projection package
```

It refuses claims because the MTS side is still missing the first real input:

```text
exact b_alpha_m=0 theorem switch
or finite lambda_D, ||D_m R_Q||, Delta m, Z_min.
```

So this is progress in the non-glamorous but necessary sense: the arena plumbing now exists, and it will not let fake unity projections or clock-to-WEP/R10 shortcuts through.

Current verdict: `FINITE_ALPHA_PROPAGATOR_BUILT_NO_CLAIM_READY_PREDICTIONS`.

## Propagator Contract

| contract_id | arena | prediction_formula | required_mts_inputs | bound_source | claim_rule | current_status | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| PROP3224_0_acceptance_rule | all | accept prediction only if every required MTS input is numeric, finite, sourced, and valid_for_claim=true | b_alpha_m theorem-zero switch OR finite lambda_D, \|\|D_m R_Q\|\|, Delta m, Z_min plus arena tau/projection | arena-specific imported anchor | claim_allowed only if prediction_valid_for_claim and bound_valid_for_claim and abs(prediction)<=bound | RUNNER_RULE_ACTIVE | false |
| PROP3224_1_clock | clock | \|dot alpha/alpha\|_MTS = \|b_alpha_m * tau_clock_time\| | b_alpha_m or finite bound; tau_clock_time source row; clock readout domain | ACB1052 clock product rows | do not treat clock product bound as standalone b_alpha_m unless tau_clock_time is derived | ANCHOR_IMPORTED_PREDICTION_MISSING | false |
| PROP3224_2_WEP | WEP | eta_alpha_MTS = b_alpha_m * tau_WEP * beta_source_alpha * DeltaQ_alpha | b_alpha_m; tau_WEP; beta_source_alpha; material/source-test projection | AWP1052 MICROSCOPE alpha/Coulomb projection row | clock alpha bound cannot transfer to WEP without shared domain/projection theorem | ANCHOR_IMPORTED_PREDICTION_MISSING | false |
| PROP3224_3_R10 | R10 | alpha_X(lambda)=K_X^R10(lambda) beta_s(lambda) beta_t(lambda)+epsilon_tail(lambda) | b_alpha_m or beta source map; tau_R10; K_X(lambda); source/test material projections; bound curve | RAP1052 R10 projection definition plus future R10 bound curve | do not set tau_R10 or K_X to unity; no clock-to-R10 shortcut | DEFINITION_IMPORTED_BOUND_AND_PROJECTION_MISSING | false |
| PROP3224_4_hessian_stress_guard | all | G_eff >= G_mem - eta_D - eta_stress - eta_readout > 0 | G_mem, lambda_D, \|\|D_m R_Q\|\|, \|\|F_Q^2\|\|, stress/readout bounds | 3219/3223 Hessian guards | alpha product pass is not enough for Maxwell/local safety | GUARD_MISSING_INPUTS | false |

## Imported Bound Anchors

| anchor_id | arena | observable | bound_value | units | interpretation | score_ready | valid_for_claim | import_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ACB1052_0 | clock | 27Al+ / 199Hg+ | 3.9e-17 | yr^-1 | bounds b_alpha*tau_clock_time only; H0-normalized value is diagnostic unless tau_clock_time=H0*dchi_X/dN is derived | false | false | NUMERIC_PRODUCT_BOUND_IMPORTED_NONCLAIM |
| ACB1052_1 | clock | 171Yb+ E3 / 171Yb+ E2 | 2.1e-18 | yr^-1 | bounds b_alpha*tau_clock_time only; H0-normalized value is diagnostic unless tau_clock_time=H0*dchi_X/dN is derived | false | false | NUMERIC_PRODUCT_BOUND_IMPORTED_NONCLAIM |
| ACB1052_2 | clock | 171Yb+ E3 / 171Yb+ E2 | 2.1e-18 | yr^-1 | bounds b_alpha*tau_clock_time only; H0-normalized value is diagnostic unless tau_clock_time=H0*dchi_X/dN is derived | false | false | NUMERIC_PRODUCT_BOUND_IMPORTED_NONCLAIM |
| AWP1052_0_alpha_Coulomb | MICROSCOPE_WEP | alpha/Coulomb composition channel | 2.8e-15 | dimensionless eta | required_abs_beta_source_max=4.797780522732e-05 | false | false | NUMERIC_PROJECTION_BOUND_IMPORTED_NONCLAIM |
| AWP1052_1_surface_binding | MICROSCOPE_WEP | surface/binding composition channel | 2.8e-15 | dimensionless eta | required_abs_beta_source_max=2.887280314062e-05 | false | false | NUMERIC_PROJECTION_BOUND_IMPORTED_NONCLAIM |
| AWP1052_2_clock_screen_warning | cross_arena_policy | clock-screen-only branch | 2.8e-15 | dimensionless eta | same alpha domain/projection must be used in clock/WEP/R10 unless theorem-zero closes branch | false | false | NUMERIC_PROJECTION_BOUND_IMPORTED_NONCLAIM |
| RAP1052_0_product_law | R10_short_range | alpha_X(lambda)=K_X^R10(lambda) beta_s(lambda) beta_t(lambda)+epsilon_tail(lambda) | MISSING_PROMOTED_R10_BOUND_OR_PROJECTION | dimensionless alpha(lambda) | lambda_X; Z_X; K_X(lambda); beta_s; beta_t; alpha composition projection; promoted bound curve | false | false | DEFINITION_ONLY_NONCLAIM |
| RAP1052_1_tau_R10 | R10_short_range | tau_R10 := normalized test-leg/material/readout projection under selected Yukawa profile convention | MISSING_PROMOTED_R10_BOUND_OR_PROJECTION | dimensionless alpha(lambda) | material/readout trace convention; Xhat normalization; finite-source correction; profile integral | false | false | DEFINITION_ONLY_NONCLAIM |
| RAP1052_2_clock_to_R10_transfer | clock_to_R10_transfer | clock product bound cannot determine alpha_X(lambda) without beta_s beta_t and tau_R10 | MISSING_PROMOTED_R10_BOUND_OR_PROJECTION | dimensionless alpha(lambda) | relation between tau_clock_time and tau_R10; source/test alpha charges; K_X/Z_X | false | false | DEFINITION_ONLY_NONCLAIM |

## MTS Alpha Input Readiness

| input_id | quantity | value | numeric_value | source_ok | numeric_ready | valid_for_claim | readiness_status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| SMOKE3223_0_balpha_zero_switch | b_alpha_m | 0 | 0.0 | false | false | false | SCHEMA_ONLY_OR_MISSING_SOURCE |
| SMOKE3223_1_lambda_D | lambda_D | MISSING_NUMERIC_OR_THEOREM_FIXED | MISSING_OR_PLACEHOLDER | false | false | false | SCHEMA_ONLY_OR_MISSING_SOURCE |
| SMOKE3223_2_DRQ_norm | \|\|D_m R_Q\|\| | MISSING_OPERATOR_NORM | MISSING_OR_PLACEHOLDER | false | false | false | SCHEMA_ONLY_OR_MISSING_SOURCE |
| SMOKE3223_3_delta_m | Delta m | MISSING_LOCAL_AMPLITUDE | MISSING_OR_PLACEHOLDER | false | false | false | SCHEMA_ONLY_OR_MISSING_SOURCE |
| SMOKE3223_4_Z_min | Z_min | MISSING_POSITIVE_DENOMINATOR | MISSING_OR_PLACEHOLDER | false | false | false | SCHEMA_ONLY_OR_MISSING_SOURCE |
| SMOKE3223_5_tau_clock | tau_clock | MISSING_CLOCK_PROJECTION_FACTOR | MISSING_OR_PLACEHOLDER | true | false | false | SCHEMA_ONLY_OR_MISSING_SOURCE |
| SMOKE3223_6_tau_WEP_beta | tau_WEP and beta_source_alpha | MISSING_WEP_SOURCE_TEST_PROJECTION | MISSING_OR_PLACEHOLDER | true | false | false | SCHEMA_ONLY_OR_MISSING_SOURCE |
| SMOKE3223_7_tau_R10 | tau_R10 | MISSING_R10_SOURCE_TEST_PROJECTION | MISSING_OR_PLACEHOLDER | true | false | false | SCHEMA_ONLY_OR_MISSING_SOURCE |
| SMOKE3223_8_eta_stress_readout | eta_stress + eta_readout | MISSING_STRESS_READOUT_BOUND | MISSING_OR_PLACEHOLDER | false | false | false | SCHEMA_ONLY_OR_MISSING_SOURCE |

## Product Comparison Results

| comparison_id | arena | prediction_formula | prediction_value | bound_value | comparison_status | claim_allowed | issues | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CMP3224_0_clock | clock | \|b_alpha_m * tau_clock_time\| | NOT_COMPUTED | 2.1e-18 best imported product anchor, nonclaim | blocked_missing_claim_ready_prediction | false | b_alpha_m/tau_clock_time not claim-ready; imported clock rows are product bounds only | false |
| CMP3224_1_WEP | WEP | b_alpha_m * tau_WEP * beta_source_alpha * DeltaQ_alpha | NOT_COMPUTED | 2.8e-15 MICROSCOPE eta anchor, nonclaim | blocked_missing_projection_inputs | false | tau_WEP and beta_source_alpha missing; no clock-to-WEP shortcut | false |
| CMP3224_2_R10 | R10 | alpha_X(lambda)=K_X beta_s beta_t + epsilon_tail | NOT_COMPUTED | MISSING_PROMOTED_BOUND_CURVE_AND_PROJECTIONS | blocked_missing_R10_projection_and_bound_curve | false | tau_R10, K_X(lambda), source/test beta projections, and promoted bound curve missing | false |
| CMP3224_3_runner_summary | all | strict acceptance gate | claim_ready_inputs=0 | claim_ready_bounds=0 | runner_refuses_claims | false | no claim-ready MTS prediction inputs and no claim-ready imported anchor rows | false |

## First Real Input Blockers

| blocker_id | needed_input | why_first | candidate_source | current_status | next_action | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| BLK3224_0_first_MTS_scalar | one of: exact b_alpha_m=0 theorem switch OR finite b_alpha_m bound | without this the propagator has no MTS prediction to send into any arena | R_Z parent residual or finite lambda_D/DRQ/Delta_m/Z_min row | MISSING | source lambda_D, \|\|D_m R_Q\|\|, Delta m, and Z_min or source-sign exact R_Q root | false |
| BLK3224_1_clock_projection | tau_clock_time | clock rows bound b_alpha*tau, not b_alpha alone | clock readout/local Xhat normalization row | MISSING | do not divide the clock bound by an assumed tau | false |
| BLK3224_2_WEP_projection | tau_WEP and beta_source_alpha | WEP alpha/Coulomb test needs source/test material projection | material sensitivity/source label theorem or finite prior row | MISSING | fill beta_source_alpha and tau_WEP before comparison | false |
| BLK3224_3_R10_projection | tau_R10, K_X(lambda), beta_s, beta_t, promoted bound curve | R10 cannot inherit clock/WEP alpha constraints without profile/material maps | R10 alpha-bound acquisition and Yukawa profile convention | MISSING | keep R10 at definition-only until bound curve/projections are real | false |
| BLK3224_4_stress_readout | eta_stress and eta_readout | alpha product pass would still not prove Maxwell stress/Poynting or observed alpha safety | R_H/R_W stress-readout residual theorem or finite bound | MISSING | retain separate Maxwell stress gate | false |

## Decision

| decision_id | decision | because | claim_status | next_action | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| DEC3224_0_result | FINITE_ALPHA_PROPAGATOR_BUILT_NO_CLAIM_READY_PREDICTIONS | clock/WEP/R10 anchors can be imported, but MTS b_alpha/projection inputs remain placeholders or nonclaim product rows | NO_CLOCK_NO_WEP_NO_R10_NO_MAXWELL_STRESS_NO_LOCAL_GR_CLAIM | source the first real finite MTS input: exact b_alpha zero switch, or lambda_D/DRQ/Delta_m/Z_min for finite bound | false |
| DEC3224_1_next_target | 3225-Y5-R2FR-first-real-alpha-input-acquisition-balpha-zero-or-lambdaD-DRQ-Zmin-under-AX1090 | the propagator is now ready; the bottleneck is not arena plumbing but the first source-backed MTS alpha input | PRIVATE_NEXT_TARGET | prioritize R_Z exact-zero source row; fallback to finite lambda_D, \|\|D_m R_Q\|\|, Delta m, and Z_min acquisition | false |

## Generated Evidence

- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3224_INPUTS.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3224_PROPAGATOR_CONTRACT.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3224_IMPORTED_BOUND_ANCHORS.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3224_MTS_ALPHA_INPUT_READINESS.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3224_PRODUCT_COMPARISON_RESULTS.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3224_FIRST_REAL_INPUT_BLOCKERS.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3224_DECISION.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3224_VALIDATION.csv`

## Source Register

| input_id | relative_path | exists | role | evidence_hits | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| SRC3224_00_3223_doc | 3223-Y5-R2FR-RQ-source-search-or-finite-alpha-runner-smoke-inputs-under-AX1090.md | true | 3223 handoff and finite formula | L3:Private checkpoint. This is not a local-GR claim, Maxwell derivation claim, Newtonian-limit claim, WEP pass, R10 pass, clock pass, `b_alpha_m=0` claim, EM-lock claim, or public-facing result. \| L26:\|b_alpha_m\| <= 2 \|lambda_D\| \|\|D_m R_Q\|\|^2 \|Delta m\| / Z_min + O(Delta m^2). \| L29:The smoke runner deliberately refuses claims because all needed finite inputs remain placeholder/nonclaim. \| L31:Current verdict: `NO_RQ_SOURCE_SIGNED_FINITE_ALPHA_SMOKE_RUNNER_STAGED`. | false |
| SRC3224_01_3223_formula | P8_Y5_R2FR_3223_FINITE_ALPHA_BOUND_FORMULA.csv | true | finite b_alpha formula | L3:FORM3223_1_offroot_bound,finite off-root b_alpha_m,\|b_alpha_m\| <= 2 \|lambda_D\| \|\|D_m R_Q\|\|^2 \|Delta m\| / Z_min + O(Delta m^2),"lambda_D, \|\|D_m R_Q\|\|, Delta m, Z_min, units, source paths",FINITE_BOUND_ \| L5:FORM3223_3_hessian_guard,defect-norm Hessian correction,G_eff >= G_mem - eta_D - eta_stress - eta_readout > 0,"G_mem, lambda_D, \|\|D_m R_Q\|\|, \|\|F_Q^2\|\| support norm, stress/readout bounds",FINITE_BOUND | false |
| SRC3224_02_3223_smoke | P8_Y5_R2FR_3223_FINITE_ALPHA_SMOKE_INPUTS.csv | true | MTS finite alpha smoke inputs | L3:SMOKE3223_1_lambda_D,lambda_D,MISSING_NUMERIC_OR_THEOREM_FIXED,Z_A per \|\|R_Q\|\|^2,MISSING_PARENT_ACTION_TERM,finite off-root branch,true,false,false,2026-06-26T21:47:59.259783+00:00 \| L7:SMOKE3223_5_tau_clock,tau_clock,MISSING_CLOCK_PROJECTION_FACTOR,time/projection units,P8_Y5_R10_1052_ALPHA_CLOCK_PRODUCT_BOUND_LEDGER.csv,clock comparison,true,false,false,2026-06-26T21:47:59.259783+0 \| L9:SMOKE3223_7_tau_R10,tau_R10,MISSING_R10_SOURCE_TEST_PROJECTION,length/projection units,P8_Y5_R10_1052_ALPHA_R10_PROJECTION_LEDGER.csv,R10 comparison,true,false,false,2026-06-26T21:47:59.259783+00:00 | false |
| SRC3224_03_3223_runner | P8_Y5_R2FR_3223_ALPHA_SMOKE_RUNNER_RESULTS.csv | true | 3223 runner refusal | L1:run_id,input_rows,schema_valid_rows,numeric_ready_rows,claim_ready_rows,comparison_status,claim_allowed,reason,valid_for_claim,generated_utc \| L2:RUN3223_0_schema,9,9,0,0,schema_smoke_only,false,finite alpha runner inputs are structurally staged but numeric/source-backed values are missing,false,2026-06-26T21:47:59.259783+00:00 | false |
| SRC3224_04_clock | P8_Y5_R10_1052_ALPHA_CLOCK_PRODUCT_BOUND_LEDGER.csv | true | clock alpha product bound anchors | L1:bound_id,row_type,clock_pair,delta_K_alpha,product_bound_1sigma_yr_inv,product_bound_2sigma_yr_inv,H0_normalized_diagnostic,interpretation,standalone_balpha_ready,valid_for_claim,generated_utc \| L4:ACB1052_2,best_current,171Yb+ E3 / 171Yb+ E2,-6.95,2.1e-18,3.2e-18,2.93296e-08,bounds b_alpha*tau_clock_time only; H0-normalized value is diagnostic unless tau_clock_time=H0*dchi_X/dN is derived,false | false |
| SRC3224_05_WEP | P8_Y5_R10_1052_ALPHA_WEP_PROJECTION_LEDGER.csv | true | WEP alpha projection anchors | L1:projection_id,arena,channel,source_row,delta_Q_abs,eta_bound,unit_source_eta_prediction,overshoot_factor,required_abs_beta_source_max,missing_for_claim,score_ready,valid_for_claim,generated_utc \| L2:AWP1052_0_alpha_Coulomb,MICROSCOPE_WEP,alpha/Coulomb composition channel,WEP988_WAS651_0_alpha_Coulomb,1.989808886825e-03,2.8e-15,5.836031862511e-11,2.084297e+04,4.797780522732e-05,beta_source_alpha t \| L3:AWP1052_1_surface_binding,MICROSCOPE_WEP,surface/binding composition channel,WEP988_WAS651_1_surface_binding,3.306456347405e-03,2.8e-15,9.697707515141e-11,3.463467e+04,2.887280314062e-05,binding coeff | false |
| SRC3224_06_R10 | P8_Y5_R10_1052_ALPHA_R10_PROJECTION_LEDGER.csv | true | R10 alpha projection definition | L2:RAP1052_0_product_law,R10_short_range,alpha_X(lambda)=K_X^R10(lambda) beta_s(lambda) beta_t(lambda)+epsilon_tail(lambda),BETA1035_0_product_law,review-candidate nonclaim R10 bound curve,lambda_X; Z_X; \| L3:RAP1052_1_tau_R10,R10_short_range,tau_R10 := normalized test-leg/material/readout projection under selected Yukawa profile convention,TAUR1033_2_tau_definition; TAUR1033_6_verdict,definition-only tau_ \| L4:RAP1052_2_clock_to_R10_transfer,clock_to_R10_transfer,clock product bound cannot determine alpha_X(lambda) without beta_s beta_t and tau_R10,1051 claim gate plus 1035/1033 projection rows,\|b_alpha*tau | false |
| SRC3224_07_1091 | 1091-Y5-R10-parent-operator-domain-no-hidden-visible-hom-theorem-or-MOMS-closure.md | true | finite residual route warning | L29:\| ODH1091_6_verdict \| parent operator-domain no-hidden-visible-hom theorem is derived \| ODH1091_1 plus no scalar obstruction plus product/sequester plus radiative/readout closure \| THEOREM_NOT_DERIVED \| L51:\| FR1091_0_b_alpha \| b_alpha \| source_backed_clock_product_only \| \\\|b_alpha*tau_clock_time\\\| <= 2.1e-18 yr^-1 at 1sigma from 1051 Yb E3/E2 row \| tau_clock_time; Xhat normalization; WEP/R10 source-test \| L71:\| CG1091_0_operator_domain \| no hidden-visible hom theorem \| false \| false \| ODH1091_6_verdict=THEOREM_NOT_DERIVED_CURRENT_CORPUS \| | false |
| SRC3224_08_3219 | 3219-Y5-R2FR-EM-F2-strict-double-zero-source-root-or-balpha-m-finite-bound-under-AX1090.md | true | off-root alpha/Hessian guard | L29:G_eff >= G_mem - eta_EM > 0. \| L49:\| HES3219_1_coercivity_floor \| corrected memory operator remains positive \| G_eff >= G_mem - eta_EM, eta_EM >= (1/4)\\\|lambda_F F''\\\| \\\|\\\|F_Q^2\\\|\\\|_op plus readout/radiative corrections \| MISSING_NUMER \| L52:\| HES3219_4_activation \| strict double-zero EM route activates local memory silence \| DZ3219_1 plus G_eff>0 plus intrinsic/boundary/readout source silence \| FAIL_CURRENT_CLAIM \| parent source-root, lo \| L58:\| ORB3219_0_balpha_offroot \| off-root b_alpha_m \| \\\|b_alpha_m\\\| <= \\\|lambda_F F2_m\\\| \\\|delta_m\\\| / Z_min + O(delta_m^2) \| lambda_F; F2_m=F''(m_*); delta_m amplitude; Z_min; units; source paths \| clock | false |

## Validation

| check_id | pass | detail |
| --- | --- | --- |
| VAL3224_00_inputs_exist | true | inputs=9 |
| VAL3224_01_bound_anchors_imported | true | numeric_anchors=6 |
| VAL3224_02_no_claim_ready_mts_inputs | true | claim_ready_mts=0 |
| VAL3224_03_runner_refuses_claims | true | claim_allowed_rows=0 |
| VAL3224_04_first_input_blockers_written | true | BLK3224_0_first_MTS_scalar;BLK3224_1_clock_projection;BLK3224_2_WEP_projection;BLK3224_3_R10_projection;BLK3224_4_stress_readout |
| VAL3224_05_claims_blocked | true | claim_rows_true=0 |
| VAL3224_06_no_formalization_workbench_edit | true | no formalization-workbench paths are output targets |
| VAL3224_07_csv_parse | true | P8_Y5_R2FR_3224_INPUTS.csv;P8_Y5_R2FR_3224_PROPAGATOR_CONTRACT.csv;P8_Y5_R2FR_3224_IMPORTED_BOUND_ANCHORS.csv;P8_Y5_R2FR_3224_MTS_ALPHA_INPUT_READINESS.csv;P8_Y5_R2FR_3224_PRODUCT_COMPARISON_RESULTS.csv;P8_Y5_R2FR_3224_FIRST_REAL_INPUT_BLOCKERS.csv;P8_Y5_R2FR_3224_DECISION.csv |
| VAL3224_08_next_target | true | 3225-Y5-R2FR-first-real-alpha-input-acquisition-balpha-zero-or-lambdaD-DRQ-Zmin-under-AX1090 |

All generated rows remain `valid_for_claim=false`.
