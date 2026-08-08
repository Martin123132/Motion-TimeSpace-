# 1436 - First projection-matrix target selection and row contract

**Current verdict:** WEP is selected as the first residual-to-observable projection target, but only as a contract. No WEP, R10, PPN, clock, orbital, or local-GR claim is allowed.

**Main progress:** the coupling problem has been narrowed to a concrete `P_WEP` row: map `C_parent`, source worldtube, material tensor, readout kernel, product convention, and measured-G guard into `eta_Ti_Pt` without shortcuts.

## Source register
| source_id | source_path | path_exists | anchor | anchor_found | role | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| SRC1436_0_1435_next | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1435_NEXT_TARGET.csv | True | NEXT1435_0_1436 | True | 1435 handoff selecting projection target contract. | False | False |
| SRC1436_1_1435_validation | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_BRR545_1435_VALIDATION.csv | True | VAL1435_9_overall | True | 1435 validation summary. | False | False |
| SRC1436_2_1435_dashboard | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1435_ARENA_DRYRUN_DASHBOARD.csv | True | DRY1435_1 | True | 1435 arena dry-run dashboard. | False | False |
| SRC1436_3_1435_missing_matrix | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1435_MISSING_INPUT_MATRIX.csv | True | MIM1435_5 | True | 1435 missing-input matrix. | False | False |
| SRC1436_4_branch_id | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\microscope\branch_locked_wep\branch_id.csv | True | MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | True | active same-parent branch lock. | False | False |
| SRC1436_5_c_parent | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\microscope\branch_locked_wep\coefficients\C_parent.csv | True | CP1430_6_verdict | True | placeholder C_parent refusal rows. | False | False |
| SRC1436_6_c_parent_import_schema | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\microscope\branch_locked_wep\coefficients\C_parent_import_schema.csv | True | C_PARENT_IMPORT_SCHEMA_1431 | True | strict future import schema. | False | False |
| SRC1436_7_product_convention | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\microscope\branch_locked_wep\product\eta_product_convention.csv | True | tau_eff = branch_locked_orbit_average | True | eta product convention guard. | False | False |
| SRC1436_8_measured_g_guard | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\microscope\branch_locked_wep\guards\measured_G_guard.csv | True | MGG1429_0_no_relative_absorption | True | measured-G absorption guard. | False | False |
| SRC1436_9_ct_projection_871 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_871_CT_PROJECTION_CONTRACT.csv | True | PC871_2_clock_WEP | True | older trace projection contract family. | False | False |

## Projection target ranking
| same_parent_branch_id | rank | arena_id | arena | observable | candidate_target | projection_matrix_id | missing_input_count | source_status | leverage_score | source_maturity_score | local_gr_relevance_score | priority_score | selection_status | reason | valid_prediction_row | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | 1 | ABM1434_1_WEP | WEP_MICROSCOPE | eta_Ti_Pt | P_WEP | P_WEP_TRACE_TO_ETA_TIPT_1436 | 5 | NUMERIC_BOUND_SOURCE_AVAILABLE_PROXY_NONCLAIM | 5 | 4 | 5 | 605 | SELECTED_FIRST_TARGET | sharpest composition/coupling pressure; directly tests whether trace leakage creates differential acceleration. | False | False | False |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | 2 | ABM1434_2_PPN | PPN_radio_and_ephemerides | gamma_minus_one;beta_minus_one;alpha1;alpha2;alpha3;xi | P_PPN | P_PPN_TRACE_TO_METRIC_VECTOR_1436 | 4 | BOUND_SOURCES_OR_LOCAL_LIMITS_AVAILABLE_NONCLAIM | 5 | 4 | 5 | 620 | SECOND_TARGET | closest to local-GR reduction, but needs metric response operator and gauge fixing before a row is meaningful. | False | False | False |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | 3 | ABM1434_3_CLOCK | clock_redshift | redshift_fractional_deviation | P_CLOCK | P_CLOCK_TRACE_TO_REDSHIFT_1436 | 3 | NUMERIC_BOUND_SOURCE_AVAILABLE_NONCLAIM | 4 | 4 | 4 | 515 | THIRD_TARGET | fewest missing inputs, useful for clock pressure, but narrower than WEP/PPN for local-GR closure. | False | False | False |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | 4 | ABM1434_0_R10 | R10_short_range_inverse_square | alpha(lambda) | P_R10 | P_R10_TRACE_TO_ALPHA_LAMBDA_1436 | 5 | ANCHOR_ONLY_NONCURVE | 4 | 2 | 3 | 425 | DEFERRED_TARGET | strong short-range arena, but still anchor-only/non-curve and requires lambda/Z/source-normalized coupling. | False | False | False |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | 5 | ABM1434_4_ORBITAL_NEWTON | orbital_and_Newton_source_normalization | Gdot_over_G;delta_GM;anomalous_radial_acceleration | P_GM | P_GM_TRACE_TO_SOURCE_NORMALIZATION_1436 | 4 | REVIEW_OR_LOCAL_BOUND_MAP_NONCLAIM | 3 | 2 | 4 | 360 | DEFERRED_TARGET | important Newtonian-limit guard, but first needs a selected observable and source-worldtube weighting. | False | False | False |

## First target contract
| same_parent_branch_id | contract_id | selected_projection_matrix_id | selected_arena_id | selected_arena | observable | formula_shape | required_inputs | current_missing_inputs | row_status | runner_effect | anti_shortcut_guard | source_path | valid_prediction_row | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | FTC1436_0_P_WEP_FIRST_ROW | P_WEP_TRACE_TO_ETA_TIPT_1436 | ABM1434_1_WEP | WEP_MICROSCOPE | eta_Ti_Pt | eta_AB = P_WEP[C_parent, R_source, R_material, K_CMSM, eta_product_convention, measured_G_guard] | C_parent numeric/zero; full material tensor; source worldtube; official K_CMSM; official sign convention | C_parent numeric/zero; full material tensor; source worldtube; official K_CMSM; official sign convention | CONTRACT_ONLY_INPUTS_MISSING | BLOCK_NUMERIC_SCORE_UNTIL_ALL_REQUIRED_ROWS_ARE_SOURCED | tau_eff=1 and measured-G relative absorption remain forbidden | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1436-Y5-R10-RAB-first-projection-matrix-target-selection-and-row-contract.md | False | False | False |

## Projection row schema
| same_parent_branch_id | schema_id | field | type | rule | example_or_current_value | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | PRS1436_0 | same_parent_branch_id | string | must equal active branch id | MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | False | False |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | PRS1436_1 | projection_matrix_id | string | unique projection contract id | P_WEP_TRACE_TO_ETA_TIPT_1436 | False | False |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | PRS1436_2 | arena_id | string | dry-run arena id | ABM1434_1_WEP | False | False |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | PRS1436_3 | observable | string | observable being predicted | eta_Ti_Pt | False | False |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | PRS1436_4 | source_basis | string | source-worldtube and environmental basis | MISSING_SOURCE_WORLDTUBE | False | False |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | PRS1436_5 | material_basis | string | test-mass material tensor basis | MISSING_Ti_Pt_MATERIAL_TENSOR | False | False |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | PRS1436_6 | readout_basis | string | instrument/orbit/readout convention | MISSING_OFFICIAL_K_CMSM | False | False |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | PRS1436_7 | formula_shape | string | symbolic row formula | eta_AB=P_WEP[...] | False | False |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | PRS1436_8 | required_inputs | semicolon_list | all mandatory source/input rows | C_parent;R_source;R_material;K_CMSM | False | False |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | PRS1436_9 | units | string | dimensionless eta after declared conversion factors | dimensionless | False | False |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | PRS1436_10 | source_path | path | local source/provenance path for the row | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1436-Y5-R10-RAB-first-projection-matrix-target-selection-and-row-contract.md | False | False |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | PRS1436_11 | parent_status | enum | SOURCE_BACKED_NUMERIC \| DERIVED_ZERO \| CLOSURE_ONLY \| MISSING_PARENT_INPUT | MISSING_PARENT_INPUT | False | False |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | PRS1436_12 | valid_prediction_row | bool | true only after row is numeric/derived and sourced | False | False | False |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | PRS1436_13 | valid_for_claim | bool | true only after all gates pass | False | False | False |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | PRS1436_14 | claim_allowed | bool | must remain false in 1436 | False | False | False |

## Required source rows
| same_parent_branch_id | required_row_id | projection_matrix_id | required_row | source_path | path_exists | anchor | anchor_found | row_status | next_action | blocks_numeric_score | valid_prediction_row | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | REQ1436_0_C_parent | P_WEP_TRACE_TO_ETA_TIPT_1436 | C_parent numeric/zero | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\microscope\branch_locked_wep\coefficients\C_parent.csv | True | CP1430_6_verdict | True | PLACEHOLDER_ONLY_NOT_SCOREABLE | import parent-signed zero theorem or numeric coefficient vector | True | False | False | False |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | REQ1436_1_material_tensor | P_WEP_TRACE_TO_ETA_TIPT_1436 | full Ti/Pt material tensor | MISSING_SOURCE_PATH | False | MISSING_ANCHOR | False | MISSING_SOURCE_PATH | source or build official composition/material-response tensor for Ti and Pt/Rh test masses | True | False | False | False |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | REQ1436_2_source_worldtube | P_WEP_TRACE_TO_ETA_TIPT_1436 | Earth/source worldtube and orbit weighting | MISSING_SOURCE_PATH | False | MISSING_ANCHOR | False | MISSING_SOURCE_PATH | source finite-size worldtube/orbit weighting compatible with MICROSCOPE readout | True | False | False | False |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | REQ1436_3_K_CMSM | P_WEP_TRACE_TO_ETA_TIPT_1436 | official K_CMSM or readout kernel | MISSING_SOURCE_PATH | False | MISSING_ANCHOR | False | MISSING_SOURCE_PATH | source official/reproducible MICROSCOPE readout kernel and sign convention | True | False | False | False |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | REQ1436_4_eta_product_convention | P_WEP_TRACE_TO_ETA_TIPT_1436 | eta product convention | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\microscope\branch_locked_wep\product\eta_product_convention.csv | True | tau_eff = branch_locked_orbit_average | True | EXISTS_GUARD_NOT_OFFICIAL_COMPLETE | keep product rule; fill official body order and orbit average | True | False | False | False |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | REQ1436_5_measured_G_guard | P_WEP_TRACE_TO_ETA_TIPT_1436 | measured-G absorption guard | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\microscope\branch_locked_wep\guards\measured_G_guard.csv | True | MGG1429_0_no_relative_absorption | True | EXISTS_GUARD_NOT_EXTERNAL_COMPLETE | keep relative-absorption forbidden | True | False | False | False |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | REQ1436_6_official_sign_convention | P_WEP_TRACE_TO_ETA_TIPT_1436 | official sign/body-axis convention | MISSING_SOURCE_PATH | False | MISSING_ANCHOR | False | MISSING_SOURCE_PATH | source official sign/body-order convention before any eta comparison | True | False | False | False |

## Runner refusal status
| same_parent_branch_id | runner_id | selected_projection_matrix_id | score_status | refusal_reason | claim_consequence | valid_prediction_row | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | RRF1436_0_projection_contract_only | P_WEP_TRACE_TO_ETA_TIPT_1436 | REFUSED_CONTRACT_ONLY_INPUTS_MISSING | P_WEP has a formula contract but lacks C_parent, material tensor, source worldtube, official K_CMSM, and sign convention. | no WEP/local-GR/local-residual claim may be made from 1436 | False | False | False |

## Claim gates
| same_parent_branch_id | gate_id | gate | gate_status | valid_prediction_row | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | CG1436_0_no_numeric_score | P_WEP score remains forbidden until all source rows are real and sourced. | LOCKED_FALSE_CLAIM | False | False | False |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | CG1436_1_no_tau_shortcut | tau_eff=1 is forbidden; orbit/readout weighting must be sourced. | LOCKED_FALSE_CLAIM | False | False | False |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | CG1436_2_no_measured_G_absorption | relative Ti/Pt residual cannot be hidden in measured G. | LOCKED_FALSE_CLAIM | False | False | False |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | CG1436_3_no_parent_placeholder | MISSING_PARENT_INPUT rows cannot become evidence. | LOCKED_FALSE_CLAIM | False | False | False |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | CG1436_4_no_local_GR_claim | selection of WEP target is a workflow decision, not a local-GR pass. | LOCKED_FALSE_CLAIM | False | False | False |

## Decision ledger
| same_parent_branch_id | decision_id | decision | why | what_it_does_not_mean | valid_prediction_row | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | DEC1436_0_select_WEP | select P_WEP_TRACE_TO_ETA_TIPT_1436 as the first projection-matrix target | WEP is the most surgical coupling test: if the trace residual creates species-dependent acceleration, this is where it should be forced into a sourced row. | does not prove or disprove MTS; does not score eta; does not claim local GR | False | False | False |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | DEC1436_1_next_step | attempt first P_WEP row or write the source-input acquisition ledger | the next bottleneck is no longer abstract coupling; it is the concrete map from C_parent and source/material/readout tensors to eta_Ti_Pt | does not allow a placeholder source row to pass | False | False | False |

## Validation
| check_id | result | detail | generated_utc |
| --- | --- | --- | --- |
| VAL1436_0_source_register | PASS | all 1436 cited source-register paths and anchors resolve | 2026-06-16T05:51:24.804849+00:00 |
| VAL1436_1_selected_target | PASS | P_WEP is the single selected first target | 2026-06-16T05:51:24.804861+00:00 |
| VAL1436_2_contract | PASS | first target contract is WEP and contract-only | 2026-06-16T05:51:24.804865+00:00 |
| VAL1436_3_schema | PASS | projection row schema includes source/material/readout and claim gates | 2026-06-16T05:51:24.804867+00:00 |
| VAL1436_4_required_inputs | PASS | missing required inputs remain visible and block score | 2026-06-16T05:51:24.804870+00:00 |
| VAL1436_5_runner_refusal | PASS | runner status refuses numeric scoring | 2026-06-16T05:51:24.804872+00:00 |
| VAL1436_6_claim_gates | PASS | all claim/valid/prediction flags remain false | 2026-06-16T05:51:24.804875+00:00 |
| VAL1436_7_csv_parse | PASS | all generated 1436 CSVs parse cleanly | 2026-06-16T05:51:24.804877+00:00 |
| VAL1436_8_branch_files | PASS | branch-locked first-target and row-schema files written | 2026-06-16T05:51:24.804879+00:00 |
| VAL1436_9_formalization_untouched | PASS | formalization modified-file count since start=0 | 2026-06-16T05:51:24.804882+00:00 |
| VAL1436_10_next_target | PASS | 1437 handoff written | 2026-06-16T05:51:24.804884+00:00 |
| VAL1436_11_overall | PASS | 1436 selects WEP as first projection target and locks it as nonclaim contract-only work | 2026-06-16T05:51:24.804890+00:00 |

## Next target
| next_id | next_target | script | objective | include | exclude | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| NEXT1436_0_1437 | 1437-Y5-R10-RAB-P-WEP-first-row-or-source-input-acquisition-ledger.md | scripts/Y5_R10_RAB_P_WEP_first_row_or_source_input_acquisition_ledger.py | attempt the first branch-locked P_WEP projection row; if required inputs are unavailable, write the source acquisition ledger for C_parent, material tensor, source worldtube, K_CMSM, and sign convention. | P_WEP first row attempt; missing-source acquisition ledger; no-tau-shortcut guard; measured-G guard | numeric WEP claim; local-GR pass; placeholder coefficient promotion; formalization edits; GitHub | False | False |
