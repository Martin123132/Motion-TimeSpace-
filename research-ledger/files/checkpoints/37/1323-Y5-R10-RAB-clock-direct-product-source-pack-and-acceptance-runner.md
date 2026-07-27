# 1323: RAB Clock Direct Product Source Pack And Acceptance Runner

**Current verdict:** 1323 builds the direct `P_clock_alpha` source pack and acceptance runner. It does not claim a clock pass; the current source pack is intentionally refused because the MTS product is still missing.

**Main progress:** the Yb E3/E2 clock bound is now linked to a placeholder-free acceptance contract: a future direct product row must provide a numeric yr^-1 prediction, readout model, source path, source anchor, equation reference, provenance, and sign convention before comparison.

**Decision:** try one direct product fill attempt next. If no MTS readout/source expression exists, move the clock row to wait-state and shift to WEP source-normalization decomposition.

## Source Register
| source_id | local_path | needle | exists | needle_found | role | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| SRC1323_0_1322_next | source-intake/mts_residuals/P8_Y5_R10_1322_NEXT_TARGET.csv | NEXT1322_0_1323 | True | True | handoff into direct clock product source pack | False | False |
| SRC1323_1_1322_requirements | source-intake/mts_residuals/P8_Y5_R10_1322_DIRECT_PRODUCT_SOURCE_REQUIREMENTS.csv | DCP1322_1_direct_product | True | True | direct clock product requirements | False | False |
| SRC1323_2_1322_runner | source-intake/mts_residuals/P8_Y5_R10_1322_CLOCK_RUNNER_UPDATE.csv | CLKRUN1322_0_tau_derivation_attempt | True | True | refused tau/readout runner state | False | False |
| SRC1323_3_1322_shortcuts | source-intake/mts_residuals/P8_Y5_R10_1322_ANTI_SHORTCUT_GATES.csv | SHORT1322_3_no_standalone_balpha | True | True | inherited no-standalone-balpha/no-transfer gates | False | False |
| SRC1323_4_1321_bound | source-intake/mts_residuals/P8_Y5_R10_1321_CLOCK_BOUND_IMPORT.csv | ACB1052_2 | True | True | selected Yb comparison bound | False | False |
| SRC1323_5_646_sensitivity | source-intake/mts_residuals/P8_Y5_R10_646_CLOCK_ALPHA_SENSITIVITY_SOURCE.csv | CAS646_1_YbE3E2 | True | True | source-backed Yb clock sensitivity | False | False |
| SRC1323_6_948_runner | source-intake/mts_residuals/P8_Y5_R10_948_CLOCK_PRODUCT_BOUND_RUNNER.csv | CLK948_1_CAS646_1_YbE3E2 | True | True | prior clock product runner with missing MTS product | False | False |

## Clock Bound Link
| bound_link_id | source_bound_id | clock_pair_id | clock_pair | delta_K_alpha | product_bound_1sigma_yr_inv | product_bound_2sigma_yr_inv | sensitivity_source_status | comparison_role | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CBL1323_0_yb_e3e2 | ACB1052_2 | CAS646_1_YbE3E2 | 171Yb+ E3 / 171Yb+ E2 | -6.95 | 2.1e-18 | 3.2e-18 | source_backed_review_table_stated_difference | comparison_bound_only | False | False |

## Direct Clock Product Source Pack
| product_row_id | bound_link_id | clock_pair | delta_K_alpha | predicted_product_value | predicted_product_units | product_definition | readout_model | source_path | source_anchor | equation_ref | provenance_note | sign_convention | cross_arena_policy | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| DCLK1323_0_yb_direct_product | CBL1323_0_yb_e3e2 | 171Yb+ E3 / 171Yb+ E2 | -6.95 | MISSING_DIRECT_P_CLOCK_ALPHA | MISSING_YR_INV_UNITS | MISSING_MTS_CLOCK_PRODUCT_DEFINITION | MISSING_MTS_CLOCK_READOUT_KERNEL | MISSING_SOURCE_PATH | MISSING_SOURCE_ANCHOR | MISSING_EQUATION_REF | MISSING_PROVENANCE | MISSING_SIGN_OR_ABS_CONVENTION | NO_TRANSFER_TO_WEP_R10_LOCAL | False | False |

## Acceptance Rules
| rule_id | rule | reject_if | current_status | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- |
| AR1323_0_numeric_product | predicted product must be numeric finite yr^-1 value | MISSING_DIRECT_P_CLOCK_ALPHA;non_numeric;wrong_units | BLOCKED | False | False |
| AR1323_1_provenance | source_path, source_anchor, equation_ref, and provenance note must be present | any source/provenance field is missing | BLOCKED | False | False |
| AR1323_2_readout_model | MTS clock readout kernel must match the Yb E3/E2 convention | readout model missing or cross-arena transferred | BLOCKED | False | False |
| AR1323_3_bound_comparison | compare abs(predicted_product_value) <= product_bound_1sigma_yr_inv after all source gates pass | prediction missing, source gates fail, or abs prediction exceeds selected bound | NOT_SCORED | False | False |
| AR1323_4_no_balpha | standalone b_alpha inference is forbidden | row is produced by dividing clock bound by tau assumption | ENFORCED | False | False |

## Acceptance Runner
| runner_id | product_row_id | clock_pair | bound_1sigma_yr_inv | predicted_product_value | predicted_product_units | missing_field_count | missing_fields | numeric_product_ok | unit_ok | source_provenance_ok | comparison_status | runner_status | refusal_reason | score_ready | valid_prediction_row | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ACCEPT1323_0_yb_direct_product | DCLK1323_0_yb_direct_product | 171Yb+ E3 / 171Yb+ E2 | 2.1e-18 | MISSING_DIRECT_P_CLOCK_ALPHA | MISSING_YR_INV_UNITS | 9 | predicted_product_value;predicted_product_units;product_definition;readout_model;source_path;source_anchor;equation_ref;provenance_note;sign_convention | False | False | False | NOT_SCORED_OR_REFUSED | REFUSED | placeholder_or_missing_direct_product_source_pack | False | False | False | False |

## Blocker Ledger
| blocker_id | product_row_id | blocked_field | blocker | required_resolution | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- |
| BLK1323_0 | DCLK1323_0_yb_direct_product | predicted_product_value | MISSING_DIRECT_P_CLOCK_ALPHA | replace placeholder with numeric/provenanced direct clock product input | False | False |
| BLK1323_1 | DCLK1323_0_yb_direct_product | predicted_product_units | MISSING_YR_INV_UNITS | replace placeholder with numeric/provenanced direct clock product input | False | False |
| BLK1323_2 | DCLK1323_0_yb_direct_product | product_definition | MISSING_MTS_CLOCK_PRODUCT_DEFINITION | replace placeholder with numeric/provenanced direct clock product input | False | False |
| BLK1323_3 | DCLK1323_0_yb_direct_product | readout_model | MISSING_MTS_CLOCK_READOUT_KERNEL | replace placeholder with numeric/provenanced direct clock product input | False | False |
| BLK1323_4 | DCLK1323_0_yb_direct_product | source_path | MISSING_SOURCE_PATH | replace placeholder with numeric/provenanced direct clock product input | False | False |
| BLK1323_5 | DCLK1323_0_yb_direct_product | source_anchor | MISSING_SOURCE_ANCHOR | replace placeholder with numeric/provenanced direct clock product input | False | False |
| BLK1323_6 | DCLK1323_0_yb_direct_product | equation_ref | MISSING_EQUATION_REF | replace placeholder with numeric/provenanced direct clock product input | False | False |
| BLK1323_7 | DCLK1323_0_yb_direct_product | provenance_note | MISSING_PROVENANCE | replace placeholder with numeric/provenanced direct clock product input | False | False |
| BLK1323_8 | DCLK1323_0_yb_direct_product | sign_convention | MISSING_SIGN_OR_ABS_CONVENTION | replace placeholder with numeric/provenanced direct clock product input | False | False |

## Anti-Shortcut Gates
| gate_id | shortcut | enforcement | status | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- |
| SHORT1323_0_no_placeholder_pass | allow placeholder direct product rows to compare | REFUSED until all MISSING fields are replaced | ENFORCED | False | False |
| SHORT1323_1_no_bound_as_prediction | copy the clock bound into predicted_product_value | REFUSED; bound is comparison data only | ENFORCED | False | False |
| SHORT1323_2_no_tau_balpha | use tau/H0 assumptions or standalone b_alpha to backfill direct product | REFUSED; direct product source must stand on its own | ENFORCED | False | False |
| SHORT1323_3_no_cross_arena_transfer | reuse this clock row as WEP/R10/local evidence | REFUSED; cross-arena transfer remains blocked | ENFORCED | False | False |

## Decision Ledger
| decision_id | decision | because | next_action | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- |
| DEC1323_0_source_pack_created | direct clock product source pack created | 1322 rejected tau/readout derivation but preserved direct product as the honest fallback | attempt to derive or source the direct P_clock_alpha value/readout kernel | False | False |
| DEC1323_1_runner_refuses | acceptance runner refuses current direct product row | predicted product, units, readout model, source path, source anchor, equation reference, and provenance are missing | 1324 should attempt direct product derivation/source fill or demote clock to wait-state and move to WEP decomposition | False | False |
| DEC1323_2_no_claim | no clock pass or b_alpha claim | source pack is a gate, not evidence | preserve Yb bound as comparison-only | False | False |

## Next Target
| next_id | target_file | target_script | task | success_condition | do_not | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| NEXT1323_0_1324 | 1324-Y5-R10-RAB-clock-direct-product-derivation-source-fill-or-waitstate.md | scripts/Y5_R10_RAB_clock_direct_product_derivation_source_fill_or_waitstate.py | try to fill the direct P_clock_alpha product from MTS readout theory or a source-backed expression; if not possible, move clock to wait-state and proceed to WEP source-normalization decomposition | direct clock product is either sourced/derived with units/provenance or explicitly wait-stated with exact missing fields and next WEP route selected | do not use bound-as-prediction, tau/H0 assumptions, standalone b_alpha, or cross-arena transfer | False | False |

## Validation
| check_id | check | status | details |
| --- | --- | --- | --- |
| VAL1323_0_sources_exist | registered source paths exist and anchors are found | PASS | 7/7 source anchors found |
| VAL1323_1_bound_link_ready | Yb E3/E2 comparison bound and sensitivity are linked | PASS | 171Yb+ E3 / 171Yb+ E2 bound=2.1e-18 yr^-1 |
| VAL1323_2_source_pack_schema_complete | direct source pack contains all required fill fields | PASS | equation_ref;predicted_product_units;predicted_product_value;product_definition;provenance_note;readout_model;sign_convention;source_anchor;source_path |
| VAL1323_3_acceptance_rules_written | acceptance rules block missing product, provenance, readout, and b_alpha shortcuts | PASS | AR1323_0_numeric_product;AR1323_1_provenance;AR1323_2_readout_model;AR1323_3_bound_comparison;AR1323_4_no_balpha |
| VAL1323_4_runner_refuses_placeholders | acceptance runner refuses current placeholder source pack | PASS | predicted_product_value;predicted_product_units;product_definition;readout_model;source_path;source_anchor;equation_ref;provenance_note;sign_convention |
| VAL1323_5_blockers_recorded | all missing direct product fields are recorded as blockers | PASS | blockers=9 |
| VAL1323_6_shortcuts_enforced | anti-shortcut gates are enforced | PASS | SHORT1323_0_no_placeholder_pass;SHORT1323_1_no_bound_as_prediction;SHORT1323_2_no_tau_balpha;SHORT1323_3_no_cross_arena_transfer |
| VAL1323_7_nonclaim_policy | all generated rows remain nonclaim | PASS | valid_for_claim=false and claim_allowed=false throughout generated tables |
| VAL1323_8_formalization_untouched | formalization-workbench untouched by generated outputs | PASS | formalization_generated_output_count=0 |
| VAL1323_9_next_target_1324 | next target routes to direct product fill or wait-state | PASS | 1324-Y5-R10-RAB-clock-direct-product-derivation-source-fill-or-waitstate.md |
| VAL1323_10_overall | overall 1323 validation | PASS | 1323 creates direct clock product source pack, links Yb bound, refuses placeholders, and preserves nonclaim gates |
