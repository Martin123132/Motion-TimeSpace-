# 1435 - Local trace residual runner dry-run and missing-input dashboard

**Current verdict:** the dry-run runner parses the local trace residual schema and bound map, then refuses every arena because projection/source inputs remain missing.

**Main progress:** the active residual branch now has an executable missing-input dashboard and matrix, so future testing can target the bottleneck rows instead of guessing.

## Source register
| source_id | source_path | path_exists | anchor | anchor_found | role | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| SRC1435_0_1434_next | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1434_NEXT_TARGET.csv | True | NEXT1434_0_1435 | True | 1434 handoff selecting dry-run dashboard. | False | False |
| SRC1435_1_1434_validation | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_BRR545_1434_VALIDATION.csv | True | VAL1434_9_overall | True | 1434 validation summary. | False | False |
| SRC1435_2_branch_id | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\microscope\branch_locked_wep\branch_id.csv | True | MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | True | branch lock row. | False | False |
| SRC1435_3_schema_file | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\microscope\branch_locked_wep\residuals\local_trace_residual_source_pack_schema.csv | True | projection_matrix_id | True | branch-locked residual source-pack schema. | False | False |
| SRC1435_4_bound_map_file | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\microscope\branch_locked_wep\residuals\local_trace_bound_map.csv | True | ABM1434_4_ORBITAL_NEWTON | True | branch-locked local trace bound map. | False | False |
| SRC1435_5_components | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1434_RESIDUAL_COMPONENTS.csv | True | LTRC1434_4_source_normalization | True | residual components. | False | False |
| SRC1435_6_inputs | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1434_REQUIRED_INPUTS_LEDGER.csv | True | REQ1434_1_projection_matrices | True | required input ledger. | False | False |

## Schema parse audit
| audit_id | target_path | result | detail | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- |
| SPA1435_0_schema_exists | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\microscope\branch_locked_wep\residuals\local_trace_residual_source_pack_schema.csv | PASS | schema file exists | False | False |
| SPA1435_1_schema_fields | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\microscope\branch_locked_wep\residuals\local_trace_residual_source_pack_schema.csv | PASS | all required dry-run schema fields present | False | False |
| SPA1435_2_bound_map_exists | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\microscope\branch_locked_wep\residuals\local_trace_bound_map.csv | PASS | bound map file exists | False | False |
| SPA1435_3_bound_map_branch | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\microscope\branch_locked_wep\residuals\local_trace_bound_map.csv | PASS | MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | False | False |

## Arena dry-run dashboard
| same_parent_branch_id | dashboard_id | arena_id | arena | observable | bound_source_anchor | source_status | missing_input_count | score_status | first_next_action | valid_prediction_row | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | DRY1435_0 | ABM1434_0_R10 | R10_short_range_inverse_square | alpha(lambda) | CT871_R10_EOTWASH_2020_ALPHA1_38P6UM_ANCHOR;CT871_R10_EOTWASH_2007_ALPHA1_56UM_ANCHOR | ANCHOR_ONLY_NONCURVE | 5 | REFUSED_MISSING_INPUTS | derive_or_source_projection_matrix_before_numeric_score | False | False | False |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | DRY1435_1 | ABM1434_1_WEP | WEP_MICROSCOPE | eta_Ti_Pt | CT871_WEP_MICROSCOPE_ETA_PROXY;SRC871_WEP_MICROSCOPE_FINAL | NUMERIC_BOUND_SOURCE_AVAILABLE_PROXY_NONCLAIM | 5 | REFUSED_MISSING_INPUTS | derive_or_source_projection_matrix_before_numeric_score | False | False | False |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | DRY1435_2 | ABM1434_2_PPN | PPN_radio_and_ephemerides | gamma_minus_one;beta_minus_one;alpha1;alpha2;alpha3;xi | CT871_PPN_CASSINI_GAMMA_SIGMA;CT871_PPN_INPOP20A_BETA_INTERVAL;BAM921_4_alpha1;BAM921_5_alpha2;BAM921_6_alpha3;BAM921_7_xi | BOUND_SOURCES_OR_LOCAL_LIMITS_AVAILABLE_NONCLAIM | 4 | REFUSED_MISSING_INPUTS | derive_or_source_projection_matrix_before_numeric_score | False | False | False |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | DRY1435_3 | ABM1434_3_CLOCK | clock_redshift | redshift_fractional_deviation | CT871_CLOCK_GALILEO_REDSHIFT_SIGMA;BAM921_1_clock | NUMERIC_BOUND_SOURCE_AVAILABLE_NONCLAIM | 3 | REFUSED_MISSING_INPUTS | derive_or_source_projection_matrix_before_numeric_score | False | False | False |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | DRY1435_4 | ABM1434_4_ORBITAL_NEWTON | orbital_and_Newton_source_normalization | Gdot_over_G;delta_GM;anomalous_radial_acceleration | SRC871_ORBITAL_LLR_REVIEW;BAM921_8_Gdot | REVIEW_OR_LOCAL_BOUND_MAP_NONCLAIM | 4 | REFUSED_MISSING_INPUTS | derive_or_source_projection_matrix_before_numeric_score | False | False | False |

## Missing input matrix
| same_parent_branch_id | matrix_id | arena_id | arena | observable | missing_input | required_projection | source_status | runner_effect | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | MIM1435_0 | ABM1434_0_R10 | R10_short_range_inverse_square | alpha(lambda) | full alpha(lambda) curve | alpha_T(lambda)=F[Q_T_over_m,Z_T,lambda_T,R_source,K_R10] | ANCHOR_ONLY_NONCURVE | BLOCKS_SCORE | False | False |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | MIM1435_1 | ABM1434_0_R10 | R10_short_range_inverse_square | alpha(lambda) | lambda_T | alpha_T(lambda)=F[Q_T_over_m,Z_T,lambda_T,R_source,K_R10] | ANCHOR_ONLY_NONCURVE | BLOCKS_SCORE | False | False |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | MIM1435_2 | ABM1434_0_R10 | R10_short_range_inverse_square | alpha(lambda) | Z_T | alpha_T(lambda)=F[Q_T_over_m,Z_T,lambda_T,R_source,K_R10] | ANCHOR_ONLY_NONCURVE | BLOCKS_SCORE | False | False |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | MIM1435_3 | ABM1434_0_R10 | R10_short_range_inverse_square | alpha(lambda) | source geometry | alpha_T(lambda)=F[Q_T_over_m,Z_T,lambda_T,R_source,K_R10] | ANCHOR_ONLY_NONCURVE | BLOCKS_SCORE | False | False |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | MIM1435_4 | ABM1434_0_R10 | R10_short_range_inverse_square | alpha(lambda) | projection normalization | alpha_T(lambda)=F[Q_T_over_m,Z_T,lambda_T,R_source,K_R10] | ANCHOR_ONLY_NONCURVE | BLOCKS_SCORE | False | False |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | MIM1435_5 | ABM1434_1_WEP | WEP_MICROSCOPE | eta_Ti_Pt | C_parent numeric/zero | eta_AB=P_WEP[C_parent,R_source,R_material,K_CMSM,eta_product_convention] | NUMERIC_BOUND_SOURCE_AVAILABLE_PROXY_NONCLAIM | BLOCKS_SCORE | False | False |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | MIM1435_6 | ABM1434_1_WEP | WEP_MICROSCOPE | eta_Ti_Pt | full material tensor | eta_AB=P_WEP[C_parent,R_source,R_material,K_CMSM,eta_product_convention] | NUMERIC_BOUND_SOURCE_AVAILABLE_PROXY_NONCLAIM | BLOCKS_SCORE | False | False |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | MIM1435_7 | ABM1434_1_WEP | WEP_MICROSCOPE | eta_Ti_Pt | source worldtube | eta_AB=P_WEP[C_parent,R_source,R_material,K_CMSM,eta_product_convention] | NUMERIC_BOUND_SOURCE_AVAILABLE_PROXY_NONCLAIM | BLOCKS_SCORE | False | False |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | MIM1435_8 | ABM1434_1_WEP | WEP_MICROSCOPE | eta_Ti_Pt | official K_CMSM | eta_AB=P_WEP[C_parent,R_source,R_material,K_CMSM,eta_product_convention] | NUMERIC_BOUND_SOURCE_AVAILABLE_PROXY_NONCLAIM | BLOCKS_SCORE | False | False |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | MIM1435_9 | ABM1434_1_WEP | WEP_MICROSCOPE | eta_Ti_Pt | official sign convention | eta_AB=P_WEP[C_parent,R_source,R_material,K_CMSM,eta_product_convention] | NUMERIC_BOUND_SOURCE_AVAILABLE_PROXY_NONCLAIM | BLOCKS_SCORE | False | False |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | MIM1435_10 | ABM1434_2_PPN | PPN_radio_and_ephemerides | gamma_minus_one;beta_minus_one;alpha1;alpha2;alpha3;xi | metric response operator | PPN_vector=P_PPN[C_T_metric,B_TF,B_0i,source_normalization] | BOUND_SOURCES_OR_LOCAL_LIMITS_AVAILABLE_NONCLAIM | BLOCKS_SCORE | False | False |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | MIM1435_11 | ABM1434_2_PPN | PPN_radio_and_ephemerides | gamma_minus_one;beta_minus_one;alpha1;alpha2;alpha3;xi | gauge fixing | PPN_vector=P_PPN[C_T_metric,B_TF,B_0i,source_normalization] | BOUND_SOURCES_OR_LOCAL_LIMITS_AVAILABLE_NONCLAIM | BLOCKS_SCORE | False | False |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | MIM1435_12 | ABM1434_2_PPN | PPN_radio_and_ephemerides | gamma_minus_one;beta_minus_one;alpha1;alpha2;alpha3;xi | boundary shear/vector projection | PPN_vector=P_PPN[C_T_metric,B_TF,B_0i,source_normalization] | BOUND_SOURCES_OR_LOCAL_LIMITS_AVAILABLE_NONCLAIM | BLOCKS_SCORE | False | False |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | MIM1435_13 | ABM1434_2_PPN | PPN_radio_and_ephemerides | gamma_minus_one;beta_minus_one;alpha1;alpha2;alpha3;xi | source normalization split | PPN_vector=P_PPN[C_T_metric,B_TF,B_0i,source_normalization] | BOUND_SOURCES_OR_LOCAL_LIMITS_AVAILABLE_NONCLAIM | BLOCKS_SCORE | False | False |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | MIM1435_14 | ABM1434_3_CLOCK | clock_redshift | redshift_fractional_deviation | clock functional | delta_nu/nu=P_clock[theta_T,C_T_metric,clock_functional] | NUMERIC_BOUND_SOURCE_AVAILABLE_NONCLAIM | BLOCKS_SCORE | False | False |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | MIM1435_15 | ABM1434_3_CLOCK | clock_redshift | redshift_fractional_deviation | marker/constant-sector trace derivative | delta_nu/nu=P_clock[theta_T,C_T_metric,clock_functional] | NUMERIC_BOUND_SOURCE_AVAILABLE_NONCLAIM | BLOCKS_SCORE | False | False |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | MIM1435_16 | ABM1434_3_CLOCK | clock_redshift | redshift_fractional_deviation | metric clock split | delta_nu/nu=P_clock[theta_T,C_T_metric,clock_functional] | NUMERIC_BOUND_SOURCE_AVAILABLE_NONCLAIM | BLOCKS_SCORE | False | False |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | MIM1435_17 | ABM1434_4_ORBITAL_NEWTON | orbital_and_Newton_source_normalization | Gdot_over_G;delta_GM;anomalous_radial_acceleration | selected numeric orbital observable | delta_mu/mu=P_GM[C_T_source,G_eff_T,source_worldtube,time_dependence] | REVIEW_OR_LOCAL_BOUND_MAP_NONCLAIM | BLOCKS_SCORE | False | False |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | MIM1435_18 | ABM1434_4_ORBITAL_NEWTON | orbital_and_Newton_source_normalization | Gdot_over_G;delta_GM;anomalous_radial_acceleration | C_T_source | delta_mu/mu=P_GM[C_T_source,G_eff_T,source_worldtube,time_dependence] | REVIEW_OR_LOCAL_BOUND_MAP_NONCLAIM | BLOCKS_SCORE | False | False |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | MIM1435_19 | ABM1434_4_ORBITAL_NEWTON | orbital_and_Newton_source_normalization | Gdot_over_G;delta_GM;anomalous_radial_acceleration | source-worldtube weighting | delta_mu/mu=P_GM[C_T_source,G_eff_T,source_worldtube,time_dependence] | REVIEW_OR_LOCAL_BOUND_MAP_NONCLAIM | BLOCKS_SCORE | False | False |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | MIM1435_20 | ABM1434_4_ORBITAL_NEWTON | orbital_and_Newton_source_normalization | Gdot_over_G;delta_GM;anomalous_radial_acceleration | time/radial dependence law | delta_mu/mu=P_GM[C_T_source,G_eff_T,source_worldtube,time_dependence] | REVIEW_OR_LOCAL_BOUND_MAP_NONCLAIM | BLOCKS_SCORE | False | False |

## Branch id audit
| audit_id | branch_values | result | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- |
| BIA1435_0_branch_id | MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | PASS | False | False |
| BIA1435_1_schema | MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | PASS | False | False |
| BIA1435_2_bound_map | MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | PASS | False | False |
| BIA1435_3_dashboard | MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | PASS | False | False |

## Runner refusal status
| runner_id | target | input_status | runner_status | score_ready | reason | valid_prediction_row | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| RUN1435_0_dryrun | local trace residual runner dry-run | 5_arenas_parsed_21_missing_inputs | REFUSE_NUMERIC_SCORE | False | every arena has missing projection/source inputs | False | False | False |
| RUN1435_1_claim_policy | claim promotion | SCHEMA_ONLY | NO_CLAIM_NO_LOCAL_GR | False | dry-run dashboard is a gap report, not evidence of a residual passing bounds | False | False | False |

## Claim gates
| gate_id | claim_component | gate_pass | claim_allowed | reason | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| CG1435_0_dryrun_dashboard | dry-run dashboard | True | False | dashboard exists but reports missing inputs | False |
| CG1435_1_numeric_residual_score | numeric residual score | False | False | no arena has complete projection/source inputs | False |
| CG1435_2_local_GR | local-GR/Newton reduction | False | False | local trace residual branch remains active and unbounded | False |

## Decision ledger
| decision_id | decision | because | effect | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- |
| DEC1435_0_dashboard | write executable missing-input dashboard | future testing should know exactly which projection/source input blocks each arena | residual branch is now dry-run auditable without long computation | False | False |
| DEC1435_1_no_numeric_run | refuse numeric scoring | the dashboard finds no complete arena row | no accidental local-GR or residual-bound pass | False | False |
| DEC1435_2_next | select the first projection matrix target | projection matrices are the common bottleneck across arenas | 1436 should prioritize P_WEP/P_R10/P_PPN with a branch-locked first-row contract | False | False |

## Validation
| check_id | result | detail | generated_utc |
| --- | --- | --- | --- |
| VAL1435_0_sources | PASS | all 1435 cited source paths and anchors resolve | 2026-06-16T05:41:42.428618+00:00 |
| VAL1435_1_schema_parse | PASS | schema and bound-map parse audits pass | 2026-06-16T05:41:42.428631+00:00 |
| VAL1435_2_branch_audit | PASS | all parsed rows share one branch id | 2026-06-16T05:41:42.428635+00:00 |
| VAL1435_3_dashboard_files | PASS | dashboard and missing-input matrix files written | 2026-06-16T05:41:42.428637+00:00 |
| VAL1435_4_all_refused | PASS | all arenas refuse scoring with visible missing inputs | 2026-06-16T05:41:42.428640+00:00 |
| VAL1435_5_claim_gates | PASS | all claim/valid/prediction flags remain false | 2026-06-16T05:41:42.428642+00:00 |
| VAL1435_6_csv_parse | PASS | all generated 1435 CSVs parse cleanly | 2026-06-16T05:41:42.428644+00:00 |
| VAL1435_7_formalization_untouched | PASS | formalization modified-file count since start=0 | 2026-06-16T05:41:42.428647+00:00 |
| VAL1435_8_next_target | PASS | 1436 handoff written | 2026-06-16T05:41:42.428649+00:00 |
| VAL1435_9_overall | PASS | 1435 dry-run dashboard parses local trace residual maps and refuses all numeric claims | 2026-06-16T05:41:42.428661+00:00 |

## Next target
| next_id | next_target | script | objective | include | exclude | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| NEXT1435_0_1436 | 1436-Y5-R10-RAB-first-projection-matrix-target-selection-and-row-contract.md | scripts/Y5_R10_RAB_first_projection_matrix_target_selection_and_row_contract.py | choose the first residual-to-observable projection matrix target and write a branch-locked row contract, likely comparing P_WEP, P_R10, and P_PPN by leverage and missing inputs. | priority ranking; projection-row schema; first target contract; anti-claim gates | numeric scoring; fitted coupling; local-GR claim; formalization edits; GitHub | False | False |
