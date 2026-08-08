# 1064 - Parent Category Label-Forgetting Proof Or Relative-Weight Runner Fill

**Current verdict:** label-forgetting is still a conditional parent-action contract, not a theorem. The exact missing clause is the no-source-only-slot rule for `w_A`.

**Runner result:** the strict relative-weight runner contract now covers WEP, PPN gamma, PPN beta, Gdot, and R10, and it refuses all current placeholders.

**Coupling discipline:** a common source normalization can be absorbed into measured `G` only if it is universal, species-blind, range-independent, time-independent, and same-frame. Relative weights cannot hide there.

## Source Register
| source_id | relative_path | exists | needle | needle_found | note |
| --- | --- | --- | --- | --- | --- |
| SRC1064_0_1063_next | source-intake/mts_residuals/P8_Y5_R10_1063_NEXT_TARGET.csv | true | 1064-Y5-R10-parent-category-label-forgetting-proof | true | 1063 handoff. |
| SRC1064_1_1063_theorem | source-intake/mts_residuals/P8_Y5_R10_1063_SOURCE_FORGETTING_THEOREM_ATTEMPT.csv | true | THM1063_5_verdict | true | 1063 theorem verdict. |
| SRC1064_2_1063_owner | source-intake/mts_residuals/P8_Y5_R10_1063_NOETHER_SOURCE_OWNER_AUDIT.csv | true | NO1063_2_Noether_current_owner | true | Noether owner audit. |
| SRC1064_3_1063_prior | source-intake/mts_residuals/P8_Y5_R10_1063_RELATIVE_WEIGHT_PRIOR_MATRIX.csv | true | RWP1063_4_delta_w_R10 | true | relative-weight prior matrix. |
| SRC1064_4_1063_template | source-intake/mts_residuals/P8_Y5_R10_1063_RELATIVE_WEIGHT_PRODUCT_TEMPLATE_NONCLAIM.csv | true | PRED1063_0_WEP_relative_source_weight | true | prior product templates. |
| SRC1064_5_954_label_forgetting | source-intake/mts_residuals/P8_Y5_R10_954_PARENT_LABEL_FORGETTING_ATTEMPT.csv | true | PLF954_5_verdict | true | parent label-forgetting attempt. |
| SRC1064_6_954_parent_clause | source-intake/mts_residuals/P8_Y5_R10_954_PARENT_ACTION_CLAUSE.csv | true | PAC954_1_no_source_prefactors | true | no source-prefactor clause. |
| SRC1064_7_954_bound_targets | source-intake/mts_residuals/P8_Y5_R10_954_SOURCE_FUNCTOR_BOUND_TARGETS.csv | true | SCB954_2_WEP_surface_beta_source | true | older species-weight bound targets. |
| SRC1064_8_954_countermodel_map | source-intake/mts_residuals/P8_Y5_R10_954_COUNTERMODEL_TO_BOUND_MAP.csv | true | CBM954_0_labelled_weight | true | countermodel-to-bound map. |
| SRC1064_9_955_prefactor_class | source-intake/mts_residuals/P8_Y5_R10_955_SOURCE_PREFACTOR_CLASSIFICATION.csv | true | SPC955_2_relative_species_weight | true | source prefactor classes. |
| SRC1064_10_955_runner | source-intake/mts_residuals/P8_Y5_R10_955_SPECIES_WEIGHT_RESIDUAL_RUNNER.csv | true | SWR955_3_WEP_coulomb_beta_source | true | older runner refusal rows. |
| SRC1064_11_956_spine | source-intake/mts_residuals/P8_Y5_R10_956_SOURCE_SIDE_GR_NEWTON_SPINE.csv | true | SSG956_3_minimal_matter_action | true | source-side GR/Newton spine. |
| SRC1064_12_639_bounds | source-intake/mts_residuals/P8_Y5_R10_639_LOCAL_BOUND_MATRIX.csv | true | LBM639_10 | true | local bound matrix. |
| SRC1064_13_local_bounds | source-intake/local_bounds/local_bound_claims.csv | true | R9_Gdot | true | local empirical bound anchors. |
| SRC1064_14_P8_template | source-intake/mts_residuals/P8_SOURCE_NORMALIZATION_NUMERIC_INPUT_TEMPLATE.csv | true | NI5_species | true | source-normalization numeric input template. |
| SRC1064_15_P8_bound_runner | source-intake/mts_residuals/P8_Y5_SOURCE_NORMALIZATION_BOUND_RUNNER_INPUT.csv | true | Y5B_3_species_source_charge | true | source-normalization bound runner input. |
| SRC1064_16_PPN_gates | source-intake/mts_residuals/P8_Y5_PPN_SOURCE_STABILITY_GATES.csv | true | PSG524_5_beta_source_zero | true | PPN source stability gates. |
| SRC1064_17_393_doc | 393-source-normalized-Newtonian-limit-under-identity-closure.md | true | Only a constant, universal, range-independent | true | measured-G common-mode guard. |


## Parent Label-Forgetting Proof Attempt
| proof_id | step | mathematical_form | proof_result | support | gap | parent_signed |
| --- | --- | --- | --- | --- | --- | --- |
| PLF1064_0_target | parent category label-forgetting | q_src({(T_A,A)}) = T_total before coupling selection; F_src(T_total)=kappa_univ T_total | TARGET_RESTATED | NSF953_2; PLF954_5; SSG956_1 | target is not a derivation; parent category still must forbid labelled source arguments | false |
| PLF1064_1_total_Hilbert_variation | variation of a single matter action forgets bookkeeping labels after summation | T_total = 2/sqrt(-g) delta(sum_A S_A)/delta g = sum_A T_A | CONDITIONAL_MATH_CLEAN | PLF954_1_total_variation_route; MMA955_1_same_action_principle | only works if the action being varied has no source-only prefactors w_A | false |
| PLF1064_2_no_source_only_slot | ban source-only species prefactors | Allowed[S_matter] excludes w_A S_A when w_A has no nongravitational measurement role | EXACT_CLAUSE_NOT_DERIVED | PAC954_1_no_source_prefactors; MMA955_5_minimal_schema | absence of a slot is a parent action schema condition unless derived from deeper quotient/operator classification | false |
| PLF1064_3_counterexample | relative-weight obstruction | S_matter=sum_A w_A S_A gives T_source=sum_A w_A T_A while preserving covariance/additivity | COUNTEREXAMPLE_SURVIVES | PLF954_2_prefactor_obstruction; MMA955_3_relative_prefactor; SPC955_2_relative_species_weight | field rescalings do not generally remove w_A once interactions, charges, and quantum normalization are measured | false |
| PLF1064_4_no_hidden_spurion_return | prevent disguised source labels | partial_m kappa = partial_D kappa = partial_boundary kappa = partial_readout kappa = 0 | PARALLEL_GATE_UNSIGNED | PAC954_3_no_hidden_spurion_return; SPC955_3_hidden_marker_weight | no-marker/no-extension theorem remains rejected or conditional in current corpus | false |
| PLF1064_5_verdict | parent category label-forgetting proof | single S_matter + no w_A + no hidden spurion return + total Hilbert variation => source labels forgotten | CONDITIONAL_CONTRACT_NOT_PARENT_DERIVED | 953/954/955/956/1063 chain | no-source-only-slot theorem is not signed; relative-weight runner fill is required | false |


## No-Source-Only-Slot Audit
| slot_id | slot | allowed_status | required_signature | if_present | current_status |
| --- | --- | --- | --- | --- | --- |
| NSS1064_0_absent_slot | w_A source-only prefactor | desired_absent_slot | parent action grammar has no argument corresponding to source-only species weight | relative source WEP/PPN/R10 residual | not_parent_signed |
| NSS1064_1_common_mode | w_common | calibration_only | constant universal range/time/species/frame independent multiplier | absorbed into measured G only after all derivative/common-mode guards pass | guarded_not_claim |
| NSS1064_2_relative_weight | epsilon_A with w_A=w_common(1+epsilon_A) | live_countermodel_if_not_forbidden | numeric epsilon_A vector with source path or parent theorem-zero | WEP/source charge and possibly PPN/R10 residuals | retained_nonclaim |
| NSS1064_3_nonHilbert_weight | zeta_A J_NH,A | parallel_open_gate | non-Hilbert current is absent, exact/projected silent, or explicitly bounded | bypasses Hilbert-current source theorem | retained_separate_gate |


## Strict Runner Schema
| column | definition | required | nonclaim_rule |
| --- | --- | --- | --- |
| prediction_id | stable row id | true | reject if missing marker, nonnumeric product, unity shortcut, source missing, or valid_for_claim=false |
| arena | MICROSCOPE_WEP, PPN_Newton, Gdot_orbital, or R10_short_range | true | reject if missing marker, nonnumeric product, unity shortcut, source missing, or valid_for_claim=false |
| product_symbol | exact relative-weight product tested | true | reject if missing marker, nonnumeric product, unity shortcut, source missing, or valid_for_claim=false |
| product_value | numeric prediction only; placeholders are invalid | true | reject if missing marker, nonnumeric product, unity shortcut, source missing, or valid_for_claim=false |
| product_units | dimensionless, yr^-1, or declared alpha(lambda) convention | true | reject if missing marker, nonnumeric product, unity shortcut, source missing, or valid_for_claim=false |
| product_source | local source path proving the product | true | reject if missing marker, nonnumeric product, unity shortcut, source missing, or valid_for_claim=false |
| inputs_present | semicolon-separated real inputs | true | reject if missing marker, nonnumeric product, unity shortcut, source missing, or valid_for_claim=false |
| required_inputs | all required coefficients/maps/source files | true | reject if missing marker, nonnumeric product, unity shortcut, source missing, or valid_for_claim=false |
| derivation_status | derived_zero, sourced_numeric, or blocked status | true | reject if missing marker, nonnumeric product, unity shortcut, source missing, or valid_for_claim=false |
| valid_for_claim | true only when numeric/sourced/unit matched | true | reject if missing marker, nonnumeric product, unity shortcut, source missing, or valid_for_claim=false |
| notes | assumptions and no-cancellation caveats | true | reject if missing marker, nonnumeric product, unity shortcut, source missing, or valid_for_claim=false |


## Numeric Source Requirements
| requirement_id | arena | product_symbol | required_inputs | units | bound_or_target | source_requirement | current_status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| REQ1064_0_WEP_species | MICROSCOPE_WEP | P_WEP_relative_source_weight | species_pair;Delta_w_AB;tau_WEP;material/source map;eta_prediction;source_file | dimensionless | 2.8e-15 | parent label-forgetting theorem or sourced Delta_w_AB and tau_WEP map | MISSING_DELTA_W_AB_TAU_WEP_PRODUCT |
| REQ1064_1_PPN_gamma | PPN_Newton | P_PPN_source_weight_gamma | C_gamma_source_weight;Delta_w_source;weak_field_response_map;source_file | dimensionless | 2.3e-05 | weak-field PPN response from relative weights into gamma-1 or theorem-zero | MISSING_C_GAMMA_SOURCE_WEIGHT_PRODUCT |
| REQ1064_2_PPN_beta | PPN_Newton | P_PPN_source_weight_beta | C_beta_source_weight;Delta_w_source;second_order_response_map;source_file | dimensionless | 7.8e-05 | second-order PPN source response or theorem-zero | MISSING_C_BETA_SOURCE_WEIGHT_PRODUCT |
| REQ1064_3_Gdot | Gdot_orbital | P_Gdot_relative_source_weight | dln_w_source_dt;time_map;source-frame convention;source_file | yr^-1 | 9.6e-15 | time constancy theorem or sourced drift below LLR lock | MISSING_DLN_W_SOURCE_DT |
| REQ1064_4_R10 | R10_short_range | P_R10_relative_weight(lambda) | lambda_w;K_w(lambda);Delta_w_source;Delta_w_test;tau_R10;alpha_bound(lambda);source_file | dimensionless with length column | promoted alpha(lambda) curve | finite-range product and bound curve, or no finite-range source-weight theorem | MISSING_KW_DELTAW_SOURCE_DELTAW_TEST_TAU_R10_PRODUCT |


## Measured-G Common-Mode Guard
| guard_id | candidate_absorption | required_zero_derivatives | must_be | current_status | if_failed |
| --- | --- | --- | --- | --- | --- |
| CMG1064_0_common_absorption | w_common into measured G | D_A=0;D_t=0;D_r=0;D_lambda=0;Delta_frame=0 | constant;universal;range_independent;time_independent;species_blind;same_frame | not_proved | relative/source-normalization residual remains physical |
| CMG1064_1_relative_not_absorbable | epsilon_A relative source weights into G | Delta_AB epsilon=0 for every source/test material pair | species_blind before calibration | not_proved | WEP/source charge residual cannot be hidden in G |
| CMG1064_2_range_not_absorbable | finite-range source weight into local calibration | D_lambda=0 and D_r=0 across tested range | range_independent before R10/orbital comparison | not_proved | R10/orbital/fifth-force row must be filled |


## Product Prediction Templates
| prediction_id | arena | product_symbol | product_value | product_units | required_inputs | derivation_status | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| PRED1064_0_WEP_relative_source_weight | MICROSCOPE_WEP | P_WEP_relative_source_weight | MISSING_DELTA_W_AB_TAU_WEP_PRODUCT | dimensionless | species_pair;Delta_w_AB;tau_WEP;material/source map;eta_prediction;source_file | MISSING_NUMERIC_OR_THEOREM_ZERO_RELATIVE_WEIGHT | false |
| PRED1064_1_PPN_gamma_source_weight | PPN_Newton | P_PPN_source_weight_gamma | MISSING_C_GAMMA_SOURCE_WEIGHT_PRODUCT | dimensionless | C_gamma_source_weight;Delta_w_source;weak_field_response_map;source_file | MISSING_RESPONSE_OPERATOR | false |
| PRED1064_2_PPN_beta_source_weight | PPN_Newton | P_PPN_source_weight_beta | MISSING_C_BETA_SOURCE_WEIGHT_PRODUCT | dimensionless | C_beta_source_weight;Delta_w_source;second_order_response_map;source_file | MISSING_RESPONSE_OPERATOR | false |
| PRED1064_3_Gdot_relative_source_weight | Gdot_orbital | P_Gdot_relative_source_weight | MISSING_DLN_W_SOURCE_DT | yr^-1 | dln_w_source_dt;time_map;source-frame convention;source_file | MISSING_TIME_MAP | false |
| PRED1064_4_R10_relative_weight_lambda | R10_short_range | P_R10_relative_weight(lambda) | MISSING_KW_DELTAW_SOURCE_DELTAW_TEST_TAU_R10_PRODUCT | dimensionless | lambda_w;K_w(lambda);Delta_w_source;Delta_w_test;tau_R10;alpha_bound(lambda);source_file | MISSING_R10_RELATIVE_WEIGHT_PRODUCT | false |


## Bound Import
| bound_id | arena | product_symbol | bound_value | bound_units | bound_type | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| BOUND1064_0_WEP_source_charge | MICROSCOPE_WEP | P_WEP_relative_source_weight | 2.8e-15 | dimensionless | numeric_bound_nonclaim | false |
| BOUND1064_1_PPN_gamma | PPN_Newton | P_PPN_source_weight_gamma | 2.3e-05 | dimensionless | numeric_bound_nonclaim | false |
| BOUND1064_2_PPN_beta | PPN_Newton | P_PPN_source_weight_beta | 7.8e-05 | dimensionless | numeric_bound_nonclaim | false |
| BOUND1064_3_Gdot | Gdot_orbital | P_Gdot_relative_source_weight | 9.6e-15 | yr^-1 | numeric_bound_nonclaim | false |
| BOUND1064_4_R10_alpha_lambda | R10_short_range | P_R10_relative_weight(lambda) | MISSING_PROMOTED_ALPHA_LAMBDA_CURVE | range-dependent | symbolic_curve_required | false |


## Product Runner Status
| runner_id | prediction_rows | bound_rows | valid_prediction_rows | valid_bound_rows | comparison_rows | claim_allowed | expected_result |
| --- | --- | --- | --- | --- | --- | --- | --- |
| APR1064_0_relative_weight_strict_product_runner | 5 | 5 | 0 | 4 | 1 | false | reject_all_missing_relative_weight_products |


## Product Comparison Rows
| comparison_id | arena | product_symbol | product_value | bound_value | comparison_status | pass_for_claim | issues |
| --- | --- | --- | --- | --- | --- | --- | --- |
| PRODUCT_COMPARE_NO_VALID_PREDICTIONS |  |  |  |  | not_run | false | no valid MTS alpha product prediction rows |


## Claim Gates
| gate_id | claim | gate_pass | reason | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| CG1064_0_label_forgetting_proof | parent category label-forgetting is proved | false | no-source-only-slot theorem remains an exact clause, not a parent derivation | false | false |
| CG1064_1_no_wA_slot | w_A source-only prefactor is forbidden | false | relative prefactor counterexample survives unless parent action grammar forbids it | false | false |
| CG1064_2_relative_weight_runner_scores | relative-weight WEP/PPN/Gdot/R10 products score | false | strict runner has valid_prediction_rows=0 and R10 bound curve remains unpromoted | false | false |
| CG1064_3_measured_G_absorption | relative weights can be absorbed into measured G | false | only common universal range/time/species/frame independent normalization is absorbable | false | false |
| CG1064_4_local_GR_Newton | local GR/Newton source side is derived | false | source-side coupling remains conditional and EH/R11/PPN readout gates remain open | false | false |


## Decision Ledger
| decision_id | decision | because | next_action | valid_for_claim |
| --- | --- | --- | --- | --- |
| DEC1064_0_proof_status | parent category label-forgetting proof remains conditional | the no-source-only-slot clause is exact but not derived from deeper MTS primitives | keep as parent-action contract and do not promote universal coupling | false |
| DEC1064_1_runner_status | strict relative-weight runner contract is filled | WEP, PPN gamma/beta, Gdot, and R10 now have exact numeric/source requirements and refusal rows | fill one product row numerically or derive the no-w_A theorem | false |
| DEC1064_2_best_next | next target is the no-source-only-slot parent grammar | this is the smallest theorem that would remove w_A rather than bounding it | 1065-Y5-R10-no-source-only-slot-parent-grammar-or-first-relative-weight-numeric-row.md | false |


## Validation
| check_id | result | detail | generated_utc |
| --- | --- | --- | --- |
| V1064_SUMMARY | pass | 1064 parent category label-forgetting / relative-weight runner validation summary | 2026-06-14T10:21:45.363450+00:00 |
| V1064_1_sources_exist_and_needles | pass | every cited local source path exists and every source needle was found | 2026-06-14T10:21:43.606229+00:00 |
| V1064_2_label_forgetting_not_promoted | pass | label-forgetting proof remains conditional | 2026-06-14T10:21:43.606242+00:00 |
| V1064_3_wA_slot_retained | pass | relative source-weight slot is retained as nonclaim countermodel | 2026-06-14T10:21:43.606246+00:00 |
| V1064_4_runner_schema_written | pass | strict product-runner schema written | 2026-06-14T10:21:43.606250+00:00 |
| V1064_5_numeric_requirements_written | pass | WEP, PPN gamma/beta, Gdot, and R10 numeric/source requirements written | 2026-06-14T10:21:43.606254+00:00 |
| V1064_6_common_mode_guard_written | pass | measured-G common-mode guard written | 2026-06-14T10:21:43.606258+00:00 |
| V1064_7_prediction_templates_nonclaim | pass | all relative-weight prediction templates remain missing-input placeholders | 2026-06-14T10:21:43.606312+00:00 |
| V1064_8_bound_import_written | pass | WEP/PPN/Gdot bound anchors imported and R10 remains curve-required | 2026-06-14T10:21:43.606317+00:00 |
| V1064_9_product_runner_refuses_placeholders | pass | product runner refuses all strict relative-weight placeholders | 2026-06-14T10:21:43.606321+00:00 |
| V1064_10_claim_gates_blocked | pass | all label-forgetting and relative-weight claim gates remain blocked | 2026-06-14T10:21:43.606326+00:00 |
| V1064_11_next_target_written | pass | next target selects no-source-only-slot grammar or first numeric row | 2026-06-14T10:21:43.606329+00:00 |
| V1064_12_generated_files_in_post_checkpoint | pass | all generated files are under post-checkpoint-work | 2026-06-14T10:21:43.610959+00:00 |
| V1064_13_formalization_untouched | pass | formalization-workbench modified-file count since script start is 0 | 2026-06-14T10:21:45.363431+00:00 |


## Next Target
| next_target | objective | include | exclude | valid_for_claim |
| --- | --- | --- | --- | --- |
| 1065-Y5-R10-no-source-only-slot-parent-grammar-or-first-relative-weight-numeric-row.md | try to derive the parent action grammar that forbids source-only species prefactors w_A; if the theorem still fails, fill the first numeric relative-weight row, starting with the WEP species-source charge product, with source path, units, and refusal gates. | allowed-action grammar, field normalization loopholes, interaction/charge normalization, w_A theorem-zero clauses, first WEP numeric row schema if theorem fails | assuming minimality, absorbing relative weights into measured G, unity shortcuts, cancellation, public local-GR/WEP/R10 claim, GitHub action, formalization-workbench edits | false |

