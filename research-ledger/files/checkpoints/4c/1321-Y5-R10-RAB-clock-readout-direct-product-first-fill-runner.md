# 1321: RAB Clock Readout Direct Product First-Fill Runner

**Current verdict:** 1321 creates the clock first-fill runner but does not claim a clock pass or a standalone `b_alpha`. The imported clock bound is comparison-only.

**Main progress:** the selected Yb clock product bound is now wired into a refusal runner with two allowed future routes: a direct sourced `P_clock_alpha`, or a fully sourced factorized `b_alpha*tau_clock_time`. Both are currently missing.

**Decision:** attack `tau_clock_time`/readout derivation next. If that fails, the direct-product source requirement remains the honest fallback.

## Source Register
| source_id | local_path | needle | exists | needle_found | role | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| SRC1321_0_1320_next | source-intake/mts_residuals/P8_Y5_R10_1320_NEXT_TARGET.csv | NEXT1320_0_1321 | True | True | handoff into clock direct-product/readout first-fill runner | False | False |
| SRC1321_1_1320_priority | source-intake/mts_residuals/P8_Y5_R10_1320_FINITE_SOURCE_PRIORITY_MAP.csv | SURV1319_1_clock | True | True | clock selected as rank-1 finite row | False | False |
| SRC1321_2_1320_first_fill | source-intake/mts_residuals/P8_Y5_R10_1320_FIRST_FILL_ROUTE_MATRIX.csv | FF1320_0_selected_next | True | True | clock first-fill route | False | False |
| SRC1321_3_1320_gate | source-intake/mts_residuals/P8_Y5_R10_1320_ACCEPTANCE_GATES.csv | GATE1320_1_clock | True | True | no standalone b_alpha clock gate | False | False |
| SRC1321_4_1052_clock | source-intake/mts_residuals/P8_Y5_R10_1052_ALPHA_CLOCK_PRODUCT_BOUND_LEDGER.csv | ACB1052_2 | True | True | best current source-backed clock product bound | False | False |
| SRC1321_5_1316_requirements | source-intake/mts_residuals/P8_Y5_R10_1316_P0_SOURCE_REQUIREMENT_LEDGER.csv | REQ1316_4_tau_clock | True | True | clock source requirement ledger | False | False |
| SRC1321_6_1317_template | source-intake/mts_residuals/P8_Y5_R10_1317_P0_SOURCE_INTAKE_TEMPLATE.csv | TPL1317_5_clock_sensitivity_readout_model | True | True | clock fillable source template | False | False |
| SRC1321_7_1317_runner | source-intake/mts_residuals/P8_Y5_R10_1317_PRIORITY_RUNNER_REFUSAL_TABLE.csv | RUN1317_1_run1314_1_clock | True | True | current refused clock runner row | False | False |

## Clock Bound Import
| bound_import_id | source_bound_id | row_type | clock_pair | delta_K_alpha | product_bound_1sigma_yr_inv | product_bound_2sigma_yr_inv | h0_normalized_diagnostic | is_selected_best_bound | bound_interpretation | standalone_balpha_ready | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CBI1321_0 | ACB1052_0 | imported_clock_pair | 27Al+ / 199Hg+ | 2.95 | 3.9e-17 | 6.2e-17 | 5.44693e-07 | False | comparison_bound_for_direct_clock_product_only | False | False | False |
| CBI1321_1 | ACB1052_1 | imported_clock_pair | 171Yb+ E3 / 171Yb+ E2 | -6.95 | 2.1e-18 | 3.2e-18 | 2.93296e-08 | False | comparison_bound_for_direct_clock_product_only | False | False | False |
| CBI1321_2 | ACB1052_2 | best_current | 171Yb+ E3 / 171Yb+ E2 | -6.95 | 2.1e-18 | 3.2e-18 | 2.93296e-08 | True | comparison_bound_for_direct_clock_product_only | False | False | False |

## Clock First-Fill Template
| template_id | route | required_fields | current_fill | acceptance_rule | refusal_if_missing | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CLK1321_0_direct_product | direct P_clock_alpha prediction | clock_pair;delta_K_alpha;predicted_product_value;predicted_product_units;readout_model;source_path;source_anchor;provenance_note | MISSING_DIRECT_P_CLOCK_ALPHA | abs(predicted_product_value)<=product_bound only after predicted value is numeric, sourced, and same clock/readout convention | MISSING_DIRECT_CLOCK_PRODUCT | False | False |
| CLK1321_1_factorized_product | factorized b_alpha*tau_clock_time | b_alpha_or_zero_certificate;tau_clock_time;clock_pair;readout_model;units;source_path;source_anchor;provenance_note | MISSING_B_ALPHA_AND_TAU_CLOCK_TIME | factorized product can score only if both b_alpha and tau_clock_time are sourced or theorem-signed | MISSING_FACTORISED_CLOCK_PRODUCT | False | False |
| CLK1321_2_tau_readout | tau_clock_time/readout map | tau_clock_time;time_units;definition;parent_branch;clock_sensitivity;source_path;source_anchor | MISSING_CLOCK_READOUT_MAP | tau is not assumed from H0 diagnostic; it must be derived or sourced as a readout projection | MISSING_TAU_CLOCK_READOUT | False | False |
| CLK1321_3_clock_model | clock sensitivity/readout model | clock_pair;transition_sensitivity_delta_K_alpha;observable_definition;readout_kernel;units;source_path;source_anchor | PARTIAL_BOUND_ROW_ONLY | bound clock pair/sensitivity can be imported, but MTS readout kernel remains missing | MISSING_MTS_CLOCK_MODEL | False | False |

## Clock Product Schema
| schema_id | product_form | formula | required_inputs | forbidden_inputs | current_status | score_ready | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CPS1321_0_compare_direct | P_clock_alpha_direct | abs(P_clock_alpha_direct) <= product_bound_yr_inv | numeric P_clock_alpha_direct;yr^-1 units;source path;matching clock_pair;readout model | threshold_as_prediction;unsourced product;cross-arena transferred product | MISSING_NUMERIC_DIRECT_PRODUCT | False | False | False |
| CPS1321_1_compare_factorized | b_alpha*tau_clock_time | abs(b_alpha*tau_clock_time) <= product_bound_yr_inv | source-backed b_alpha or theorem-zero;source-backed tau_clock_time;yr^-1 convention;readout source | assuming tau=H0;dividing bound by guessed tau;using b_alpha threshold as prediction | MISSING_B_ALPHA_AND_TAU_CLOCK_TIME | False | False | False |
| CPS1321_2_no_standalone_balpha | standalone b_alpha from clock bound | NOT_ALLOWED: b_alpha <= product_bound/tau_assumed | none; route is forbidden unless tau is independently sourced and then product only is scored | tau assumption;H0 normalized diagnostic as tau;clock-to-WEP/R10 transfer | FORBIDDEN_SHORTCUT | False | False | False |

## Clock First-Fill Runner
| runner_id | source_bound_id | clock_pair | delta_K_alpha | comparison_bound_1sigma_yr_inv | comparison_bound_2sigma_yr_inv | predicted_product_value | readout_model | tau_clock_time | b_alpha_status | runner_status | refusal_reason | score_ready | valid_prediction_row | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CLKRUN1321_0_best_clock_bound | ACB1052_2 | 171Yb+ E3 / 171Yb+ E2 | -6.95 | 2.1e-18 | 3.2e-18 | MISSING_DIRECT_PRODUCT_OR_B_ALPHA_TAU | MISSING_MTS_CLOCK_READOUT_MODEL | MISSING_CLOCK_READOUT_MAP | MISSING_SOURCE_BACKED_COEFFICIENT_OR_THEOREM_ZERO | REFUSED | no_numeric_predicted_product;missing_tau_or_direct_product;missing_readout_model;standalone_balpha_forbidden | False | False | False | False |

## Anti-Shortcut Gates
| gate_id | shortcut | enforcement | status | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- |
| SHORT1321_0_no_standalone_balpha | infer standalone b_alpha by dividing clock product bound by assumed tau | REFUSED; clock bound constrains product only unless tau is independently sourced | ENFORCED | False | False |
| SHORT1321_1_no_tau_h0_assumption | use H0-normalized diagnostic as tau_clock_time | REFUSED; H0 diagnostic is not a readout derivation | ENFORCED | False | False |
| SHORT1321_2_no_threshold_prediction | use clock bound as predicted product | REFUSED; bound is comparison fence only | ENFORCED | False | False |
| SHORT1321_3_no_cross_arena_transfer | transfer clock product into WEP/R10/local rows | REFUSED until shared parent branch/readout functor is signed | ENFORCED | False | False |
| SHORT1321_4_no_parent_reopen | reopen closure-only parent theorem route from clock bound | REFUSED; clock product data cannot sign parent object-language clauses | ENFORCED | False | False |

## Decision Ledger
| decision_id | decision | because | next_action | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- |
| DEC1321_0_runner_created | clock first-fill runner created | clock is the most source-ready finite row after 1320 ranking | try to derive or source tau_clock_time/readout map, or source a direct P_clock_alpha prediction | False | False |
| DEC1321_1_product_only | clock bound remains product-only | tau_clock_time and b_alpha are not independently sourced | do not report standalone b_alpha; fill direct product route first | False | False |
| DEC1321_2_derivation_next | next target is clock tau/readout derivation or exact source rejection | runner is now ready but every current clock product row is refused | 1322 should attack tau_clock_time/readout map from MTS time/clock structure before fallback sourcing | False | False |

## Next Target
| next_id | target_file | target_script | task | success_condition | do_not | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| NEXT1321_0_1322 | 1322-Y5-R10-RAB-clock-tau-readout-map-derivation-or-source-rejection.md | scripts/Y5_R10_RAB_clock_tau_readout_map_derivation_or_source_rejection.py | try to derive tau_clock_time/readout map from MTS time/clock structure; if not derivable, produce exact source requirements for a direct P_clock_alpha fill | clock row either gains a signed tau/readout expression or receives a precise nonclaim source requirement ledger; standalone b_alpha remains refused | do not infer b_alpha from the clock bound; do not use H0 diagnostic as tau; do not transfer clock product to WEP/R10/local tests | False | False |

## Validation
| check_id | check | status | details |
| --- | --- | --- | --- |
| VAL1321_0_sources_exist | registered source paths exist and anchors are found | PASS | 8/8 source anchors found |
| VAL1321_1_best_clock_bound_imported | best current clock product bound is imported as comparison-only | PASS | 171Yb+ E3 / 171Yb+ E2 bound=2.1e-18 yr^-1 |
| VAL1321_2_fill_template_complete | clock first-fill template covers direct product, factorized product, tau, and clock model | PASS | CLK1321_0_direct_product;CLK1321_1_factorized_product;CLK1321_2_tau_readout;CLK1321_3_clock_model |
| VAL1321_3_product_schema_blocks_standalone_balpha | product schema explicitly forbids standalone b_alpha inference | PASS | standalone b_alpha route forbidden |
| VAL1321_4_runner_refuses_current_clock_row | runner refuses current clock row until direct product or tau/readout is filled | PASS | no_numeric_predicted_product;missing_tau_or_direct_product;missing_readout_model;standalone_balpha_forbidden |
| VAL1321_5_shortcuts_enforced | anti-shortcut gates are enforced | PASS | SHORT1321_0_no_standalone_balpha;SHORT1321_1_no_tau_h0_assumption;SHORT1321_2_no_threshold_prediction;SHORT1321_3_no_cross_arena_transfer;SHORT1321_4_no_parent_reopen |
| VAL1321_6_nonclaim_policy | all generated rows remain nonclaim | PASS | valid_for_claim=false and claim_allowed=false throughout generated tables |
| VAL1321_7_formalization_untouched | formalization-workbench untouched by generated outputs | PASS | formalization_generated_output_count=0 |
| VAL1321_8_next_target_1322 | next target routes to clock tau/readout map derivation or source rejection | PASS | 1322-Y5-R10-RAB-clock-tau-readout-map-derivation-or-source-rejection.md |
| VAL1321_9_overall | overall 1321 validation | PASS | 1321 creates clock first-fill runner, imports product bound, refuses standalone b_alpha, and routes to tau/readout derivation |
