# 1061 - WEP Alpha Product First Input Fill: tau_WEP / beta_source / Material Map

**Current verdict:** the MICROSCOPE WEP material convention and screened alpha-product target are filled for internal smoke testing, but the MTS product prediction is still absent.

**Non-negotiable result:** no WEP alpha pass is allowed until `P_WEP_alpha = beta_source_alpha*b_alpha*tau_WEP` is derived directly or every factor is parent-owned. No `beta_source_alpha=1`; no `tau_WEP=1`; no clock-only transfer.

**Next move:** derive the combined parent WEP product from one source-current/local-geometry map, or demote the WEP alpha route to closure-only.

## Source Register
| source_id | relative_path | exists | needle | needle_found | note |
| --- | --- | --- | --- | --- | --- |
| SRC1061_0_1060_next | source-intake/mts_residuals/P8_Y5_R10_1060_NEXT_TARGET.csv | true | 1061-Y5-R10-WEP-alpha-product-first-input-fill | true | 1060 handoff selecting WEP alpha product input fill. |
| SRC1061_1_1060_required | source-intake/mts_residuals/P8_Y5_R10_1060_REQUIRED_INPUTS.csv | true | REQ1060_1_WEP_alpha | true | WEP alpha required inputs. |
| SRC1061_2_1060_prediction_template | source-intake/mts_residuals/P8_Y5_R10_1060_ALPHA_PRODUCT_PREDICTION_TEMPLATE_NONCLAIM.csv | true | PRED1060_1_WEP_alpha_template | true | prior placeholder prediction row. |
| SRC1061_3_1060_bound | source-intake/mts_residuals/P8_Y5_R10_1060_ALPHA_PRODUCT_BOUND_IMPORT.csv | true | BOUND1060_1_WEP_alpha | true | prior WEP product target bound import. |
| SRC1061_4_1059_pack | source-intake/mts_residuals/P8_Y5_R10_1059_ALPHA_PRODUCT_PRIOR_PACK.csv | true | APP1059_2_WEP_alpha_Coulomb | true | alpha product prior pack row. |
| SRC1061_5_650_screen_rule | source-intake/mts_residuals/P8_Y5_R10_650_ULTRA_SCREENED_RULE.csv | true | USR650_0_shared_screen_variable | true | shared local alpha screen rule. |
| SRC1061_6_650_cross_arena | source-intake/mts_residuals/P8_Y5_R10_650_CROSS_ARENA_CONTRACT.csv | true | R0_R1_WEP | true | cross-arena WEP projection contract. |
| SRC1061_7_651_stress | source-intake/mts_residuals/P8_Y5_R10_651_WEP_ALPHA_STRESS_TEST.csv | true | WAS651_0_alpha_Coulomb | true | WEP alpha/Coulomb stress-test target. |
| SRC1061_8_983_web | source-intake/mts_residuals/P8_Y5_R10_983_WEB_SOURCE_REGISTER.csv | true | WEB983_0_MICROSCOPE_CQG_COMPOSITION | true | MICROSCOPE material composition source. |
| SRC1061_9_983_delta | source-intake/mts_residuals/P8_Y5_R10_983_DIFFERENTIAL_PROXY_VECTOR.csv | true | DEL983_coulomb_proxy | true | MICROSCOPE proxy material contrast. |
| SRC1061_10_1053_matrix | source-intake/mts_residuals/P8_Y5_R10_1053_WEP_COMPOSITION_CHARGE_MATRIX.csv | true | WCM1053_4 | true | alpha/Coulomb differential charge row. |
| SRC1061_11_988_pressure | source-intake/mts_residuals/P8_Y5_R10_988_WEP_ALPHA_PRESSURE_IMPORT.csv | true | WEP988_WAS651_0_alpha_Coulomb | true | pressure target imported after alpha screen policy. |
| SRC1061_12_1052_WEP | source-intake/mts_residuals/P8_Y5_R10_1052_ALPHA_WEP_PROJECTION_LEDGER.csv | true | AWP1052_0_alpha_Coulomb | true | WEP alpha projection ledger. |
| SRC1061_13_1053_beta | source-intake/mts_residuals/P8_Y5_R10_1053_BETA_SOURCE_ALPHA_DERIVATION_AUDIT.csv | true | BSA1053_1_alpha_marker_source | true | beta_source_alpha derivation audit. |
| SRC1061_14_1053_tau | source-intake/mts_residuals/P8_Y5_R10_1053_TAU_WEP_R10_PROJECTION_AUDIT.csv | true | TPR1053_1_tau_WEP_definition | true | tau_WEP derivation audit. |
| SRC1061_15_989_owner | source-intake/mts_residuals/P8_Y5_R10_989_BETA_SOURCE_OWNER_LEDGER.csv | true | BSO989_0_definition | true | beta source owner ledger. |
| SRC1061_16_990_contract | source-intake/mts_residuals/P8_Y5_R10_990_PARENT_ACTION_CONTRACT.csv | true | PAC990_3_EM_lock | true | parent action EM/source-normalization contract. |
| SRC1061_17_local_bound | source-intake/local_bounds/local_bound_claims.csv | true | R1_WEP_source_charge | true | MICROSCOPE WEP bound anchor. |


## Material Convention
| convention_id | object | definition | numeric_value | units | source_row | status | blocks_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| MCON1061_0_test_pair | MICROSCOPE Ti/Pt test-pair convention | TA6V outer test mass minus PtRh10 inner test mass; eta_AB uses the same sign convention as the 983/1053 smoke rows. | not_applicable | dimensionless | WEB983_0_MICROSCOPE_CQG_COMPOSITION; WCM1053_4 | material_pair_convention_filled_for_smoke | full material tensor and parent source/readout convention still missing |
| MCON1061_1_delta_Q_alpha | Delta_Q_alpha_Coulomb_abs | absolute alpha/Coulomb differential material charge in the Damour-Donoghue smoke convention. | 0.001989808886825 | dimensionless | WCM1053_4 | numeric_smoke_delta_filled | source-backed smoke estimate, not full MICROSCOPE material tensor |
| MCON1061_2_eta_bound | eta_WEP_source_charge_bound | MICROSCOPE Ti/Pt upper bound imported as the WEP product target anchor. | 2.800000e-15 | dimensionless | R1_WEP_source_charge; WEP988_WAS651_0_alpha_Coulomb | numeric_bound_anchor_filled | bound alone is not an MTS prediction |
| MCON1061_3_screened_product_target | abs_P_WEP_alpha_target | under the 650/651 shared-screen smoke convention, \|P_WEP_alpha\| <= eta_bound/unit_source_eta_prediction. | 4.797780522732e-05 | dimensionless | WEP988_WAS651_0_alpha_Coulomb; AWP1052_0_alpha_Coulomb | score_threshold_filled_not_prediction | P_WEP_alpha itself still requires beta_source_alpha, b_alpha, and tau_WEP or a direct parent product derivation |


## Derivation Attempts
| attempt_id | target | attempted_derivation | available_evidence | missing_premise | result | next_action |
| --- | --- | --- | --- | --- | --- | --- |
| DER1061_0_product_definition | P_WEP_alpha | P_WEP_alpha := beta_source_alpha*b_alpha*tau_WEP, or directly as the parent variation of the alpha-sensitive source/test acceleration map. | material delta and screened product target are numeric in the 650/651/988/1052 smoke convention | parent source-normalization functional and WEP orbit/source projection | PRODUCT_CONTRACT_WRITTEN_NOT_DERIVED | derive the combined product from parent matter/source action instead of assigning beta_source_alpha=1 or tau_WEP=1 |
| DER1061_1_beta_source_alpha | beta_source_alpha | beta_source_alpha as the alpha-channel source/force normalization from partial_Xhat ln(M_source^eff) or the same Noether owner that fixes charge/current normalization. | BSA1053_1 and BSO989_0 define the required owner | parent matter functional, Noether current normalization, and no-marker/no-alpha theorem are unsigned | OWNER_NOT_DERIVED | hunt parent source-normalization owner or prove beta_source_alpha=0 by EM-lock/no-alpha theorem |
| DER1061_2_tau_WEP | tau_WEP | tau_WEP as the normalized lab/source/orbit projection converting the same Xhat variation used by clocks into differential acceleration. | TPR1053_1 defines the object; 650 requires the shared local alpha screen across clocks/WEP/R10 | Earth/source worldtube, spacecraft/environment averaging, material tensor, parent Xhat normalization, and observed-force readout | PROJECTION_NOT_DERIVED | derive tau_WEP from local source geometry or replace split beta*tau by a direct P_WEP_alpha theorem |
| DER1061_3_material_convention | MICROSCOPE alpha material map | use existing PtRh10/TA6V smoke alloy map and Delta_Q_alpha_Coulomb as the first product convention. | WEB983_0, WCM1053_4, WEP988_WAS651_0, and AWP1052_0 | full material tensor and source/readout convention for a claim-grade MICROSCOPE prediction | PARTIAL_FILLED_SMOKE_CONVENTION_ONLY | use this as the first internal scoring convention, not public evidence |


## Input Fill Ledger
| input_id | required_input | value_or_status | source | filled_status | why_not_claim |
| --- | --- | --- | --- | --- | --- |
| INF1061_0_material_pair | MICROSCOPE material convention | TA6V_minus_PtRh10 | WEB983_0_MICROSCOPE_CQG_COMPOSITION; WCM1053_4 | filled_for_smoke_only | full material/source/readout tensor missing |
| INF1061_1_delta_Q_alpha | Delta_Q_alpha_Coulomb_abs | 0.001989808886825 | WCM1053_4; AWP1052_0_alpha_Coulomb | filled_for_smoke_only | smoke formula, not complete material model |
| INF1061_2_product_bound | abs_P_WEP_alpha_bound | 4.797780522732e-05 | WEP988_WAS651_0_alpha_Coulomb; BOUND1060_1_WEP_alpha | target_filled_not_prediction | a bound threshold is not an MTS-predicted product |
| INF1061_3_beta_source_alpha | beta_source_alpha | MISSING_PARENT_SOURCE_NORMALIZATION_OWNER | BSA1053_1_alpha_marker_source; BSO989_0_definition | not_filled | cannot set source normalization to unity; needs parent matter/Noether source owner or zero theorem |
| INF1061_4_tau_WEP | tau_WEP | MISSING_LAB_SOURCE_ORBIT_PROJECTION | TPR1053_1_tau_WEP_definition; PR650_1_WEP | not_filled | cannot set tau_WEP to one; needs local geometry/source profile/readout map |
| INF1061_5_b_alpha_or_direct_product | b_alpha_counterterm or direct P_WEP_alpha | MISSING_PARENT_ALPHA_COUNTERTERM_PRODUCT | APP1059_2_WEP_alpha_Coulomb; PRED1060_1_WEP_alpha_template | not_filled | standalone b_alpha remains forbidden; only a directly derived product may be scored |


## Prediction Attempt
| prediction_id | arena | product_symbol | product_value | product_units | inputs_present | required_inputs | derivation_status | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PRED1061_0_WEP_alpha_material_convention_filled | MICROSCOPE_WEP | P_WEP_alpha | MISSING_PARENT_DERIVED_BETA_SOURCE_ALPHA_B_ALPHA_TAU_WEP_PRODUCT | dimensionless | Delta_Q_alpha_abs;eta_bound;screened_product_target | beta_source_alpha;b_alpha_counterterm;tau_WEP OR directly derived P_WEP_alpha | MATERIAL_CONVENTION_FILLED_BETA_TAU_PRODUCT_MISSING | false |


## Bound Import
| bound_id | arena | product_symbol | bound_value | bound_units | bound_type | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| BOUND1061_0_WEP_alpha_screened_product_target | MICROSCOPE_WEP | P_WEP_alpha | 4.797780522732e-05 | dimensionless | screened_smoke_product_target_nonclaim | false |


## Product Runner Status
| runner_id | prediction_rows | bound_rows | valid_prediction_rows | valid_bound_rows | comparison_rows | claim_allowed | expected_result |
| --- | --- | --- | --- | --- | --- | --- | --- |
| APR1061_0_WEP_alpha_product_attempt | 1 | 1 | 0 | 1 | 1 | false | reject_missing_parent_product |


## Product Comparison Rows
| comparison_id | arena | product_symbol | product_value | bound_value | comparison_status | pass_for_claim | issues |
| --- | --- | --- | --- | --- | --- | --- | --- |
| PRODUCT_COMPARE_NO_VALID_PREDICTIONS |  |  |  |  | not_run | false | no valid MTS alpha product prediction rows |


## Strict Failure Modes
| failure_id | object | expected_failure | observed_status | meaning | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| FAIL1061_0_no_beta_source_owner | beta_source_alpha | MISSING_PARENT_SOURCE_NORMALIZATION_OWNER | not_filled | WEP alpha product cannot be predicted from a source/test coupling until the parent matter/Noether owner is signed. | false |
| FAIL1061_1_no_tau_WEP_projection | tau_WEP | MISSING_LAB_SOURCE_ORBIT_PROJECTION | not_filled | The shared screen cannot be exported into WEP acceleration without a source geometry/readout projection. | false |
| FAIL1061_2_no_numeric_product | P_WEP_alpha | valid_prediction_rows=0 | valid_prediction_rows=0 | The product runner must refuse the row until a numeric parent-derived P_WEP_alpha exists. | false |
| FAIL1061_3_no_unity_shortcuts | beta_source_alpha;tau_WEP | no beta=1 or tau=1 replacement | unity shortcuts absent | No coefficient is promoted by convention; the coupling must come from the theory. | false |


## Claim Gates
| gate_id | claim | gate_pass | reason | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| CG1061_0_material_convention_claim | MICROSCOPE material convention is claim-grade | false | only a smoke alloy/material charge convention is filled; full tensor/readout source map is missing | false | false |
| CG1061_1_beta_source_alpha_claim | beta_source_alpha is derived or bounded by MTS | false | owner ledger still says source normalization is unowned | false | false |
| CG1061_2_tau_WEP_claim | tau_WEP is derived | false | tau_WEP remains a definition requiring lab/source/orbit projection | false | false |
| CG1061_3_WEP_alpha_product_pass | MTS passes WEP alpha/Coulomb product target | false | product target exists but no numeric MTS product prediction exists | false | false |


## Decision Ledger
| decision_id | decision | because | next_action | valid_for_claim |
| --- | --- | --- | --- | --- |
| DEC1061_0_material_map | material convention is partially filled | MICROSCOPE Ti/Pt composition and the alpha/Coulomb Delta_Q smoke row are already source-backed internally | use the convention as an internal target only | false |
| DEC1061_1_product_prediction | do not score WEP alpha yet | beta_source_alpha and tau_WEP remain unowned and the runner correctly refuses the product row | derive P_WEP_alpha directly from parent source-current geometry or prove a zero theorem | false |
| DEC1061_2_best_next | next target is combined parent source-normalization and tau_WEP product theorem | separating beta_source_alpha from tau_WEP may be gauge/convention-dependent; the product is what the WEP bound actually tests | 1062-Y5-R10-parent-source-normalization-tauWEP-product-theorem-or-WEP-alpha-closure.md | false |


## Validation
| check_id | result | detail | generated_utc |
| --- | --- | --- | --- |
| V1061_SUMMARY | pass | 1061 WEP alpha product input-fill validation summary | 2026-06-14T10:02:03.858787+00:00 |
| V1061_1_sources_exist_and_needles | pass | every cited local source path exists and every source needle was found | 2026-06-14T10:02:02.074311+00:00 |
| V1061_2_material_delta_imported | pass | alpha/Coulomb Delta_Q material convention imported | 2026-06-14T10:02:02.074324+00:00 |
| V1061_3_product_target_imported | pass | screened WEP alpha product target imported | 2026-06-14T10:02:02.074329+00:00 |
| V1061_4_beta_source_not_guessed | pass | beta_source_alpha remains unguessed and owner-gated | 2026-06-14T10:02:02.074332+00:00 |
| V1061_5_tau_WEP_not_guessed | pass | tau_WEP remains unguessed and projection-gated | 2026-06-14T10:02:02.074336+00:00 |
| V1061_6_input_fill_ledger_nonclaim | pass | input fill ledger records filled and missing pieces without claims | 2026-06-14T10:02:02.074341+00:00 |
| V1061_7_prediction_attempt_nonclaim | pass | prediction attempt row retains missing parent product | 2026-06-14T10:02:02.074367+00:00 |
| V1061_8_bound_import_written | pass | WEP alpha product target bound row written | 2026-06-14T10:02:02.074371+00:00 |
| V1061_9_product_runner_refuses | pass | product runner refuses the material-filled but product-missing row | 2026-06-14T10:02:02.074374+00:00 |
| V1061_10_failures_written | pass | strict missing-input failure rows written | 2026-06-14T10:02:02.074378+00:00 |
| V1061_11_claim_gates_blocked | pass | claim gates remain blocked | 2026-06-14T10:02:02.074382+00:00 |
| V1061_12_next_target_written | pass | next target selects combined parent WEP product theorem | 2026-06-14T10:02:02.074387+00:00 |
| V1061_13_generated_files_in_post_checkpoint | pass | all generated files are under post-checkpoint-work | 2026-06-14T10:02:02.078859+00:00 |
| V1061_14_formalization_untouched | pass | formalization-workbench modified-file count since script start is 0 | 2026-06-14T10:02:03.858768+00:00 |


## Next Target
| next_target | objective | include | exclude | valid_for_claim |
| --- | --- | --- | --- | --- |
| 1062-Y5-R10-parent-source-normalization-tauWEP-product-theorem-or-WEP-alpha-closure.md | derive or reject the combined parent WEP product P_WEP_alpha by mapping source normalization, alpha counterterm response, and tau_WEP projection from one parent matter/source action; if this cannot be signed, demote the WEP alpha route to closure-only. | parent source-current owner, tau_WEP local geometry/readout map, direct P_WEP_alpha theorem route, zero-theorem clauses, refusal row if any owner remains missing | beta_source_alpha=1, tau_WEP=1, cancellation, standalone b_alpha bound claim, public WEP/local-GR claim, GitHub action, formalization-workbench edits | false |

