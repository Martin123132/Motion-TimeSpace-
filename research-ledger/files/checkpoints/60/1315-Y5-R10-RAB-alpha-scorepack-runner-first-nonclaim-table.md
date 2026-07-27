# 1315-Y5-R10-RAB-alpha-scorepack-runner-first-nonclaim-table

**Current verdict:** 1315 mechanically refuses every current RAB alpha scorepack row. There are zero valid predictions and zero claim-ready rows.

**Main progress:** the runner now produces a first nonclaim table, a missing-input blocker ledger, anti-shortcut gates, R10 refusal detail, and a promotion checklist. Future source fills can be tested against this rather than argued by hand.

**Decision:** attack P0 blockers next. The theory route can still win by proof, but without proof the row must be filled by real source-backed coefficients, readout maps, source profiles, R10 vectors, and bound curves.

## Source Register

| source_id | local_path | needle | exists | needle_found | role | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| SRC1315_0_1314_next | source-intake/mts_residuals/P8_Y5_R10_1314_NEXT_TARGET.csv | NEXT1314_0_1315 | True | True | handoff into alpha scorepack refusal runner | False | False |
| SRC1315_1_1314_schema | source-intake/mts_residuals/P8_Y5_R10_1314_ALPHA_SCOREPACK_INPUT_SCHEMA.csv | AS1314_3_r10_vector | True | True | 1314 input schema | False | False |
| SRC1315_2_1314_acquisition | source-intake/mts_residuals/P8_Y5_R10_1314_SOURCE_ACQUISITION_LEDGER.csv | ACQ1314_3_r10 | True | True | 1314 source acquisition ledger | False | False |
| SRC1315_3_1314_runner_rows | source-intake/mts_residuals/P8_Y5_R10_1314_RUNNER_READY_NONCLAIM_ROWS.csv | RUN1314_3_r10 | True | True | 1314 runner-ready nonclaim rows | False | False |
| SRC1315_4_1314_r10_gate | source-intake/mts_residuals/P8_Y5_R10_1314_R10_FINITE_BRANCH_GATE.csv | R10_SCOREPACK_SCHEMA_ONLY_NONCLAIM | True | True | R10 finite branch gate | False | False |
| SRC1315_5_1314_parent | source-intake/mts_residuals/P8_Y5_R10_1314_PARENT_PRIMITIVE_ESCAPE_HATCH.csv | PESC1314_0_parent_grammar | True | True | parent primitive escape hatch | False | False |
| SRC1315_6_1222_runner | source-intake/mts_residuals/P8_Y5_R10_1222_FIRST_NONCLAIM_SCORE_TABLE.csv | NCS1222_0_alpha | True | True | generic refusal runner pattern | False | False |
| SRC1315_7_1222_shortcuts | source-intake/mts_residuals/P8_Y5_R10_1222_ANTI_SHORTCUT_GATES.csv | SHORT1222_0_no_unity | True | True | anti-shortcut gate pattern | False | False |
| SRC1315_8_1222_promotion | source-intake/mts_residuals/P8_Y5_R10_1222_PROMOTION_CHECKLIST.csv | PROM1222_1_prediction | True | True | promotion checklist pattern | False | False |

## Runner Input Audit

| audit_id | runner_row_id | threshold_abs | threshold_numeric_positive | predicted_abs_value | missing_inputs | acquisition_status | counterexample_lock | score_ready | valid_prediction_row | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| RIA1315_0 | RUN1314_0_alpha | 8.3202449332435330e-10 | True | MISSING_PREDICTED_VALUE | MISSING_SOURCE_BACKED_ALPHA_COEFFICIENT_OR_PARENT_PRIMITIVE | MISSING_SOURCE_BACKED_ALPHA_COEFFICIENT_OR_PARENT_PRIMITIVE | HSC1313_1_alpha | False | False | False | False |
| RIA1315_1 | RUN1314_1_clock | 2.1e-18 | True | MISSING_MTS_CLOCK_PRODUCT | MISSING_CLOCK_READOUT_MAP_OR_DIRECT_PRODUCT | MISSING_CLOCK_READOUT_MAP_OR_DIRECT_PRODUCT | HSC1313_3_clock_readout | False | False | False | False |
| RIA1315_2 | RUN1314_2_wep | 4.7977805227320001e-05 | True | MISSING_MTS_WEP_PRODUCT | MISSING_SOURCE_NORMALIZATION_TAU_WEP_MATERIAL_READOUT | MISSING_SOURCE_NORMALIZATION_TAU_WEP_MATERIAL_READOUT | HSC1313_4_source_weight | False | False | False | False |
| RIA1315_3 | RUN1314_3_r10 | MISSING_PROMOTED_ALPHA_BOUND_CURVE | False | MISSING_R10_NUMERIC_PRODUCT | MISSING_R10_FINITE_BRANCH_VECTOR_AND_PROMOTED_BOUND | MISSING_R10_FINITE_BRANCH_VECTOR_AND_PROMOTED_BOUND | HSC1313_1_alpha;HSC1313_4_source_weight | False | False | False | False |
| RIA1315_4 | RUN1314_4_cross_arena | not_a_numeric_threshold | False | MISSING_PARENT_BRANCH_MAP | MISSING_CROSS_ARENA_PARENT_MAP | MISSING_CROSS_ARENA_PARENT_MAP | HSC1313_0_generic;HSC1313_3_clock_readout | False | False | False | False |

## First Nonclaim Score Table

| score_row_id | runner_row_id | observable_product | threshold_abs | threshold_numeric_positive | predicted_abs_value | available_inputs | missing_inputs | acquisition_status | counterexample_status | claim_status | refusal_reason | score_ready | valid_prediction_row | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NCS1315_0_0_alpha | RUN1314_0_alpha | abs(c_alpha_DD or b_alpha) | 8.3202449332435330e-10 | True | MISSING_PREDICTED_VALUE | threshold_abs_only | MISSING_SOURCE_BACKED_ALPHA_COEFFICIENT_OR_PARENT_PRIMITIVE | MISSING_SOURCE_BACKED_ALPHA_COEFFICIENT_OR_PARENT_PRIMITIVE | RETAINED | REFUSED | predicted_value_missing;missing_inputs_present;acquisition_missing;counterexample_retained | False | False | False | False |
| NCS1315_1_1_clock | RUN1314_1_clock | abs(b_alpha*tau_clock_time) | 2.1e-18 | True | MISSING_MTS_CLOCK_PRODUCT | source_bound_only | MISSING_CLOCK_READOUT_MAP_OR_DIRECT_PRODUCT | MISSING_CLOCK_READOUT_MAP_OR_DIRECT_PRODUCT | RETAINED | REFUSED | predicted_value_missing;missing_inputs_present;acquisition_missing;counterexample_retained | False | False | False | False |
| NCS1315_2_2_wep | RUN1314_2_wep | abs(beta_source_alpha*b_alpha*tau_WEP) | 4.7977805227320001e-05 | True | MISSING_MTS_WEP_PRODUCT | pressure_target_only | MISSING_SOURCE_NORMALIZATION_TAU_WEP_MATERIAL_READOUT | MISSING_SOURCE_NORMALIZATION_TAU_WEP_MATERIAL_READOUT | RETAINED | REFUSED | predicted_value_missing;missing_inputs_present;acquisition_missing;counterexample_retained | False | False | False | False |
| NCS1315_3_3_r10 | RUN1314_3_r10 | abs(P_R10_alpha(lambda)) | MISSING_PROMOTED_ALPHA_BOUND_CURVE | False | MISSING_R10_NUMERIC_PRODUCT | review_candidate_or_anchor_only_nonclaim | MISSING_R10_FINITE_BRANCH_VECTOR_AND_PROMOTED_BOUND | MISSING_R10_FINITE_BRANCH_VECTOR_AND_PROMOTED_BOUND | RETAINED | REFUSED | threshold_not_numeric_positive;predicted_value_missing;missing_inputs_present;acquisition_missing;counterexample_retained | False | False | False | False |
| NCS1315_4_4_cross_arena | RUN1314_4_cross_arena | shared alpha branch consistency | not_a_numeric_threshold | False | MISSING_PARENT_BRANCH_MAP | separate_pressure_rows_only | MISSING_CROSS_ARENA_PARENT_MAP | MISSING_CROSS_ARENA_PARENT_MAP | RETAINED | REFUSED | threshold_not_numeric_positive;predicted_value_missing;missing_inputs_present;acquisition_missing;counterexample_retained | False | False | False | False |

## Missing Input Blocker Ledger

| blocker_id | runner_row_id | blocker_token | blocker_source | required_resolution | claim_effect | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| BLK1315_0_0 | RUN1314_0_alpha | MISSING_SOURCE_BACKED_ALPHA_COEFFICIENT_OR_PARENT_PRIMITIVE | runner_missing_inputs | replace token with sourced numeric input or signed theorem-zero primitive | valid_prediction_row=false | False | False |
| BLK1315_0_acquisition | RUN1314_0_alpha | MISSING_SOURCE_BACKED_ALPHA_COEFFICIENT_OR_PARENT_PRIMITIVE | source_acquisition_ledger | fill scorepack source acquisition row with provenance or signed primitive | score_ready=false | False | False |
| BLK1315_0_counterexample | RUN1314_0_alpha | HSC1313_1_alpha | counterexample_lock | close counterexample by parent primitive or retain finite nuisance with source-backed bound | valid_prediction_row=false | False | False |
| BLK1315_1_0 | RUN1314_1_clock | MISSING_CLOCK_READOUT_MAP_OR_DIRECT_PRODUCT | runner_missing_inputs | replace token with sourced numeric input or signed theorem-zero primitive | valid_prediction_row=false | False | False |
| BLK1315_1_acquisition | RUN1314_1_clock | MISSING_CLOCK_READOUT_MAP_OR_DIRECT_PRODUCT | source_acquisition_ledger | fill scorepack source acquisition row with provenance or signed primitive | score_ready=false | False | False |
| BLK1315_1_counterexample | RUN1314_1_clock | HSC1313_3_clock_readout | counterexample_lock | close counterexample by parent primitive or retain finite nuisance with source-backed bound | valid_prediction_row=false | False | False |
| BLK1315_2_0 | RUN1314_2_wep | MISSING_SOURCE_NORMALIZATION_TAU_WEP_MATERIAL_READOUT | runner_missing_inputs | replace token with sourced numeric input or signed theorem-zero primitive | valid_prediction_row=false | False | False |
| BLK1315_2_acquisition | RUN1314_2_wep | MISSING_SOURCE_NORMALIZATION_TAU_WEP_MATERIAL_READOUT | source_acquisition_ledger | fill scorepack source acquisition row with provenance or signed primitive | score_ready=false | False | False |
| BLK1315_2_counterexample | RUN1314_2_wep | HSC1313_4_source_weight | counterexample_lock | close counterexample by parent primitive or retain finite nuisance with source-backed bound | valid_prediction_row=false | False | False |
| BLK1315_3_0 | RUN1314_3_r10 | MISSING_R10_FINITE_BRANCH_VECTOR_AND_PROMOTED_BOUND | runner_missing_inputs | replace token with sourced numeric input or signed theorem-zero primitive | valid_prediction_row=false | False | False |
| BLK1315_3_acquisition | RUN1314_3_r10 | MISSING_R10_FINITE_BRANCH_VECTOR_AND_PROMOTED_BOUND | source_acquisition_ledger | fill scorepack source acquisition row with provenance or signed primitive | score_ready=false | False | False |
| BLK1315_3_counterexample | RUN1314_3_r10 | HSC1313_1_alpha;HSC1313_4_source_weight | counterexample_lock | close counterexample by parent primitive or retain finite nuisance with source-backed bound | valid_prediction_row=false | False | False |
| BLK1315_4_0 | RUN1314_4_cross_arena | MISSING_CROSS_ARENA_PARENT_MAP | runner_missing_inputs | replace token with sourced numeric input or signed theorem-zero primitive | valid_prediction_row=false | False | False |
| BLK1315_4_acquisition | RUN1314_4_cross_arena | MISSING_CROSS_ARENA_PARENT_MAP | source_acquisition_ledger | fill scorepack source acquisition row with provenance or signed primitive | score_ready=false | False | False |
| BLK1315_4_counterexample | RUN1314_4_cross_arena | HSC1313_0_generic;HSC1313_3_clock_readout | counterexample_lock | close counterexample by parent primitive or retain finite nuisance with source-backed bound | valid_prediction_row=false | False | False |

## Anti-Shortcut Gates

| gate_id | forbidden_shortcut | runner_action | status | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- |
| SHORT1315_0_no_unity | set tau/source/readout projection to unity | refuse row unless projection is sourced or theorem-zero | ENFORCED | False | False |
| SHORT1315_1_no_threshold_prediction | use empirical threshold as MTS coefficient prediction | threshold_abs is comparison fence only; predicted_abs_value must be sourced separately | ENFORCED | False | False |
| SHORT1315_2_no_source_fill | fill coefficient values from plausibility or aesthetic minimality | requires source-backed coefficient or signed parent primitive | ENFORCED | False | False |
| SHORT1315_3_no_anchor_curve_claim | treat review-candidate or anchor-only R10 bound as claim-valid curve | R10 row refuses until promoted alpha_bound(lambda) exists | ENFORCED | False | False |
| SHORT1315_4_no_transfer_shortcut | transfer clock alpha bound to WEP/R10 without parent branch/readout map | cross-arena row refuses until shared branch classifier is sourced | ENFORCED | False | False |
| SHORT1315_5_no_measured_G_absorption | absorb finite source branch into measured G | retains source-weight/local-GR branch as explicit debt | ENFORCED | False | False |

## Claim Refusal Ledger

| refusal_id | runner_row_id | claim_refused | primary_reason | minimum_to_reconsider | observable_product | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| REF1315_0_0_alpha | RUN1314_0_alpha | True | predicted_value_missing;missing_inputs_present;acquisition_missing;counterexample_retained | numeric predicted value, source provenance, resolved missing inputs, disposed counterexample, and passing anti-shortcut gates | abs(c_alpha_DD or b_alpha) | False | False |
| REF1315_1_1_clock | RUN1314_1_clock | True | predicted_value_missing;missing_inputs_present;acquisition_missing;counterexample_retained | numeric predicted value, source provenance, resolved missing inputs, disposed counterexample, and passing anti-shortcut gates | abs(b_alpha*tau_clock_time) | False | False |
| REF1315_2_2_wep | RUN1314_2_wep | True | predicted_value_missing;missing_inputs_present;acquisition_missing;counterexample_retained | numeric predicted value, source provenance, resolved missing inputs, disposed counterexample, and passing anti-shortcut gates | abs(beta_source_alpha*b_alpha*tau_WEP) | False | False |
| REF1315_3_3_r10 | RUN1314_3_r10 | True | threshold_not_numeric_positive;predicted_value_missing;missing_inputs_present;acquisition_missing;counterexample_retained | numeric predicted value, source provenance, resolved missing inputs, disposed counterexample, and passing anti-shortcut gates | abs(P_R10_alpha(lambda)) | False | False |
| REF1315_4_4_cross_arena | RUN1314_4_cross_arena | True | threshold_not_numeric_positive;predicted_value_missing;missing_inputs_present;acquisition_missing;counterexample_retained | numeric predicted value, source provenance, resolved missing inputs, disposed counterexample, and passing anti-shortcut gates | shared alpha branch consistency | False | False |

## Promotion Checklist

| checklist_id | requirement | runner_condition | current_status | claim_rule | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- |
| PROM1315_0_threshold | positive numeric threshold or empirical bound | threshold_numeric_positive=true | PARTIAL_ALPHA_CLOCK_WEP_ONLY_R10_AND_CROSS_ARENA_BLOCKED | nonnumeric thresholds refuse the row immediately | False | False |
| PROM1315_1_prediction | finite predicted absolute value | predicted_abs_value numeric and sourced | MISSING_FOR_ALL_ROWS | no prediction, no comparison, no pass | False | False |
| PROM1315_2_provenance | source-backed coefficient/readout/profile provenance | source paths and anchors exist for every physical input | MISSING_PHYSICAL_INPUT_PROVENANCE | placeholder strings cannot become evidence | False | False |
| PROM1315_3_counterexamples | counterexample locks closed or finitely bounded | counterexample_status in {closed,bounded_with_source} | COUNTEREXAMPLES_RETAINED | active hidden-scalar/source-weight/readout counterexamples block claims | False | False |
| PROM1315_4_anti_shortcuts | no unity, threshold-as-prediction, anchor-curve, transfer, measured-G absorption, or assumption fill | anti-shortcut gates pass | GATES_WRITTEN_AND_ENFORCED | shortcut route invalidates row | False | False |
| PROM1315_5_parent_primitive | optional theorem-zero route needs genuinely new primitive | primitive source status FOUND_SIGNED_PRIMITIVE and source audited | NO_SIGNED_PRIMITIVE_FOUND | escape hatch remains open but empty | False | False |

## R10 Refusal Detail

| r10_id | runner_row_id | required | current_status | minimum_to_reconsider | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- |
| R10REF1315_0_product | RUN1314_3_r10 | numeric P_R10_alpha(lambda) | MISSING_R10_NUMERIC_PRODUCT | lambda_X, Z_X, K_X, beta_source, beta_test, tau_R10, epsilon_tail with source paths | False | False |
| R10REF1315_1_bound_curve | RUN1314_3_r10 | promoted claim-valid alpha_bound(lambda) | MISSING_PROMOTED_ALPHA_BOUND_CURVE | digitized/source-backed curve rows with valid_for_claim=true, not anchor-only/review candidate | False | False |
| R10REF1315_2_source_test | RUN1314_3_r10 | source/test projection and finite-source/readout map | MISSING_SOURCE_TEST_PROJECTION | source/test beta factors and source-weight counterexample disposition | False | False |
| R10REF1315_3_decision | RUN1314_3_r10 | R10 claim row | REFUSED | all R10 inputs sourced and anti-shortcut gates pass | False | False |

## Decision Ledger

| decision_id | decision | because | next_action | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- |
| DEC1315_0_runner_result | all current RAB alpha scorepack rows are refused | every row has missing predictions, missing source/projection/readout inputs, and/or retained counterexamples | attack P0 blockers with derivation-first then source-acquisition fallback | False | False |
| DEC1315_1_r10_result | R10 is explicitly refused | both finite MTS product vector and promoted alpha_bound(lambda) curve are missing | do not run symbolic R10 as evidence; source product/bound rows first | False | False |

## Next Target

| next_id | target_file | target_script | task | success_condition | do_not | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| NEXT1315_0_1316 | 1316-Y5-R10-RAB-P0-alpha-coupling-input-source-or-derivation-attack.md | scripts/Y5_R10_RAB_P0_alpha_coupling_input_source_or_derivation_attack.py | attack P0 alpha coupling blockers by trying parent-primitive derivations for alpha F2, clock readout, WEP/source normalization, and R10 product inputs before falling back to exact source requirements | at least one P0 blocker is promoted by real proof/source, or every P0 blocker is narrowed into exact nonclaim source requirements | do not fill coefficients by assumption; do not use unity/threshold/anchor-curve shortcuts; do not claim WEP/R10/local-GR | False | False |

## Validation

| check_id | check | status | details |
| --- | --- | --- | --- |
| VAL1315_0_sources_exist | registered source paths exist and anchors are found | PASS | 9/9 source anchors found |
| VAL1315_1_rows_imported | runner imported all 1314 rows | PASS | runner_rows=5 first_score_rows=5 |
| VAL1315_2_zero_valid_predictions | runner produces zero valid prediction rows | PASS | NCS1315_0_0_alpha=REFUSED;NCS1315_1_1_clock=REFUSED;NCS1315_2_2_wep=REFUSED;NCS1315_3_3_r10=REFUSED;NCS1315_4_4_cross_arena=REFUSED |
| VAL1315_3_all_refused | all current rows are refused | PASS | predicted_value_missing;missing_inputs_present;acquisition_missing;counterexample_retained;predicted_value_missing;missing_inputs_present;acquisition_missing;counterexample_retained;predicted_value_missing;missing_inputs_present;acquisition_missing;counterexample_retained;threshold_not_numeric_positive;predicted_value_missing;missing_inputs_present;acquisition_missing;counterexample_retained;threshold_not_numeric_positive;predicted_value_missing;missing_inputs_present;acquisition_missing;counterexample_retained |
| VAL1315_4_blockers_recorded | missing-input and counterexample blockers are recorded | PASS | blocker_rows=15 |
| VAL1315_5_shortcuts_enforced | anti-shortcut gates are enforced | PASS | SHORT1315_0_no_unity=ENFORCED;SHORT1315_1_no_threshold_prediction=ENFORCED;SHORT1315_2_no_source_fill=ENFORCED;SHORT1315_3_no_anchor_curve_claim=ENFORCED;SHORT1315_4_no_transfer_shortcut=ENFORCED;SHORT1315_5_no_measured_G_absorption=ENFORCED |
| VAL1315_6_r10_refused | R10 row is explicitly refused | PASS | R10REF1315_0_product=MISSING_R10_NUMERIC_PRODUCT;R10REF1315_1_bound_curve=MISSING_PROMOTED_ALPHA_BOUND_CURVE;R10REF1315_2_source_test=MISSING_SOURCE_TEST_PROJECTION;R10REF1315_3_decision=REFUSED |
| VAL1315_7_csv_parse | all generated CSVs parse cleanly | PASS | P8_Y5_R10_1315_SOURCE_REGISTER.csv:9; P8_Y5_R10_1315_RUNNER_INPUT_AUDIT.csv:5; P8_Y5_R10_1315_FIRST_NONCLAIM_SCORE_TABLE.csv:5; P8_Y5_R10_1315_MISSING_INPUT_BLOCKER_LEDGER.csv:15; P8_Y5_R10_1315_ANTI_SHORTCUT_GATES.csv:6; P8_Y5_R10_1315_CLAIM_REFUSAL_LEDGER.csv:5; P8_Y5_R10_1315_PROMOTION_CHECKLIST.csv:6; P8_Y5_R10_1315_R10_REFUSAL_DETAIL.csv:4; P8_Y5_R10_1315_DECISION_LEDGER.csv:2; P8_Y5_R10_1315_NEXT_TARGET.csv:1 |
| VAL1315_8_formalization_untouched | formalization-workbench untouched by generated outputs | PASS | formalization_generated_output_count=0 |
| VAL1315_9_nonclaim_policy | all generated rows remain nonclaim | PASS | valid_for_claim=false and claim_allowed=false throughout generated tables |
| VAL1315_10_next_target_1316 | next target routes to P0 alpha coupling input source/derivation attack | PASS | 1316-Y5-R10-RAB-P0-alpha-coupling-input-source-or-derivation-attack.md |
| VAL1315_11_overall | overall 1315 validation | PASS | 1315 mechanically refuses all current RAB alpha scorepack rows, records blockers, and routes to P0 source/derivation attack |
