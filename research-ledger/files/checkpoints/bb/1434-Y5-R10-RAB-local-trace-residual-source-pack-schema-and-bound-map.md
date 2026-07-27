# 1434 - Local trace residual source-pack schema and bound map

**Current verdict:** the local trace residual branch is source-pack ready, not score-ready. 1434 maps active residual components to R10, WEP, PPN, clocks, orbital, and Newton/source-normalization arenas without allowing a claim.

**Main progress:** the branch now has a residual component table, arena bound map, required-input ledger, and local schema files under `source-intake/microscope/branch_locked_wep/residuals`.

## Source register
| source_id | source_path | path_exists | anchor | anchor_found | role | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| SRC1434_0_1433_next | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1433_NEXT_TARGET.csv | True | NEXT1433_0_1434 | True | 1433 handoff selecting local trace residual source-pack schema. | False | False |
| SRC1434_1_1433_validation | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_BRR545_1433_VALIDATION.csv | True | VAL1433_7_overall | True | 1433 validation summary. | False | False |
| SRC1434_2_branch_id | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\microscope\branch_locked_wep\branch_id.csv | True | MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | True | branch lock row. | False | False |
| SRC1434_3_residual_activation | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\microscope\branch_locked_wep\residuals\local_trace_residual_activation.csv | True | RESIDUAL_ACTIVE_NONCLAIM | True | active local trace residual branch. | False | False |
| SRC1434_4_871_bound_candidates | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_871_BOUND_SOURCE_CANDIDATES.csv | True | SRC871_WEP_MICROSCOPE_FINAL | True | bound source candidates for local tests. | False | False |
| SRC1434_5_871_projection_contract | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_871_CT_PROJECTION_CONTRACT.csv | True | PC871_2_clock_WEP | True | missing c_T projection contracts. | False | False |
| SRC1434_6_871_bound_rows | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_871_CT_BOUND_ROWS.csv | True | CT871_WEP_MICROSCOPE_ETA_PROXY | True | source-backed/nonclaim bound rows. | False | False |
| SRC1434_7_921_arena_map | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_921_LOCAL_BOUND_ARENA_MAP.csv | True | BAM921_9_R10 | True | local bound arena map. | False | False |
| SRC1434_8_C_parent_schema | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\microscope\branch_locked_wep\coefficients\C_parent_import_schema.csv | True | zero_certificate_status | True | strict C_parent import schema. | False | False |
| SRC1434_9_product_guard | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\microscope\branch_locked_wep\product\eta_product_convention.csv | True | tau_eff=1 is forbidden | True | branch-locked product convention guard. | False | False |
| SRC1434_10_measured_G_guard | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\microscope\branch_locked_wep\guards\measured_G_guard.csv | True | do not absorb Ti/Pt relative acceleration | True | measured-G relative absorption guard. | False | False |

## Residual components
| same_parent_branch_id | component_id | residual_component | coefficient_symbol | physical_meaning | primary_arenas | required_projection | current_status | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | LTRC1434_0_trace_scalar | trace_scalar | Q_T_over_m;Z_T;lambda_T | finite-range scalar trace leakage after local quotient zero fails | R10;PPN_gamma_beta;clock_redshift | P_trace_to_alpha;P_trace_to_metric;P_trace_to_clock | ACTIVE_MISSING_PROJECTION_AND_COEFFICIENTS | False | False |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | LTRC1434_1_coframe_pullback | coframe_pullback | C_T_metric | trace dependence of local observed metric/coframe | PPN_gamma_beta;clock_redshift;light_cone | P_metric_response;gauge_fixing;source_normalization_split | ACTIVE_MISSING_METRIC_RESPONSE_OPERATOR | False | False |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | LTRC1434_2_boundary_hair | boundary_hair | B_T;B_TF;B_0i | trace boundary/exact current leaks into compact local projection | PPN_alpha1_alpha2_alpha3_xi;orbital | P_loc_boundary;shear_vector_decomposition;boundary_nohair_source | ACTIVE_MISSING_BOUNDARY_PROJECTION | False | False |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | LTRC1434_3_marker_constant | marker_constant | theta_T;alpha_EM_T;mass_ratio_T | species, clock, EM, binding, or material labels carry trace charge | WEP_MICROSCOPE;clock_redshift;EM | P_species_marker;P_clock_functional;P_EM_charge_normalization | ACTIVE_MISSING_NO_MARKER_THEOREM_OR_SOURCE_ROWS | False | False |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | LTRC1434_4_source_normalization | source_normalization | mu_T;C_T_source;G_eff_T | trace leakage into measured source strength, G, or GM | Newton_source_normalization;orbital_Gdot;R10_source_geometry | P_GM;P_Gdot;P_source_worldtube | ACTIVE_MISSING_SOURCE_NORMALIZATION_MAP | False | False |

## Arena bound map
| same_parent_branch_id | arena_id | arena | observable | bound_source_anchor | source_status | required_projection | missing_inputs | score_status | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | ABM1434_0_R10 | R10_short_range_inverse_square | alpha(lambda) | CT871_R10_EOTWASH_2020_ALPHA1_38P6UM_ANCHOR;CT871_R10_EOTWASH_2007_ALPHA1_56UM_ANCHOR | ANCHOR_ONLY_NONCURVE | alpha_T(lambda)=F[Q_T_over_m,Z_T,lambda_T,R_source,K_R10] | full alpha(lambda) curve; lambda_T; Z_T; source geometry; projection normalization | NOT_SCOREABLE | False | False |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | ABM1434_1_WEP | WEP_MICROSCOPE | eta_Ti_Pt | CT871_WEP_MICROSCOPE_ETA_PROXY;SRC871_WEP_MICROSCOPE_FINAL | NUMERIC_BOUND_SOURCE_AVAILABLE_PROXY_NONCLAIM | eta_AB=P_WEP[C_parent,R_source,R_material,K_CMSM,eta_product_convention] | C_parent numeric/zero; full material tensor; source worldtube; official K_CMSM; official sign convention | NOT_SCOREABLE | False | False |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | ABM1434_2_PPN | PPN_radio_and_ephemerides | gamma_minus_one;beta_minus_one;alpha1;alpha2;alpha3;xi | CT871_PPN_CASSINI_GAMMA_SIGMA;CT871_PPN_INPOP20A_BETA_INTERVAL;BAM921_4_alpha1;BAM921_5_alpha2;BAM921_6_alpha3;BAM921_7_xi | BOUND_SOURCES_OR_LOCAL_LIMITS_AVAILABLE_NONCLAIM | PPN_vector=P_PPN[C_T_metric,B_TF,B_0i,source_normalization] | metric response operator; gauge fixing; boundary shear/vector projection; source normalization split | NOT_SCOREABLE | False | False |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | ABM1434_3_CLOCK | clock_redshift | redshift_fractional_deviation | CT871_CLOCK_GALILEO_REDSHIFT_SIGMA;BAM921_1_clock | NUMERIC_BOUND_SOURCE_AVAILABLE_NONCLAIM | delta_nu/nu=P_clock[theta_T,C_T_metric,clock_functional] | clock functional; marker/constant-sector trace derivative; metric clock split | NOT_SCOREABLE | False | False |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | ABM1434_4_ORBITAL_NEWTON | orbital_and_Newton_source_normalization | Gdot_over_G;delta_GM;anomalous_radial_acceleration | SRC871_ORBITAL_LLR_REVIEW;BAM921_8_Gdot | REVIEW_OR_LOCAL_BOUND_MAP_NONCLAIM | delta_mu/mu=P_GM[C_T_source,G_eff_T,source_worldtube,time_dependence] | selected numeric orbital observable; C_T_source; source-worldtube weighting; time/radial dependence law | NOT_SCOREABLE | False | False |

## Required inputs ledger
| same_parent_branch_id | input_id | required_input | current_path | current_status | blocks | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | REQ1434_0_C_parent | C_parent numeric/zero coupling vector | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\microscope\branch_locked_wep\coefficients\C_parent.csv | PLACEHOLDER_REFUSAL_ONLY | all residual projections | False | False |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | REQ1434_1_projection_matrices | P_R10;P_WEP;P_PPN;P_clock;P_orbital;P_GM | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\microscope\branch_locked_wep\residuals | MISSING_PROJECTION_MATRICES | mapping residual components to observables | False | False |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | REQ1434_2_MICROSCOPE_pack | R_source;R_material;K_CMSM;eta_product_convention;measured_G_guard | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\microscope\branch_locked_wep | PRODUCT_AND_G_GUARDS_EXIST_OTHER_INPUTS_MISSING | WEP score | False | False |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | REQ1434_3_R10_curve | full alpha(lambda) bound curve and trace lambda_T/source projection | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_871_CT_BOUND_ROWS.csv | ANCHORS_ONLY_FULL_CURVE_MISSING | R10 claim score | False | False |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | REQ1434_4_PPN_clock_orbital_sources | PPN, clock, orbital selected bounds plus residual response coefficients | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_871_BOUND_SOURCE_CANDIDATES.csv | BOUND_SOURCES_STAGED_PROJECTIONS_MISSING | PPN/clock/orbital score | False | False |

## Source pack schema
| same_parent_branch_id | schema_field | required_value_or_policy | purpose | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | same_parent_branch_id | MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | must match branch lock | False | False |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | residual_component | trace_scalar\|coframe_pullback\|boundary_hair\|marker_constant\|source_normalization | component class | False | False |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | coefficient_symbol | Q_T_over_m\|Z_T\|lambda_T\|C_T_metric\|B_T\|theta_T\|mu_T | coefficient slot | False | False |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | value_or_bound | numeric\|DERIVED_ZERO\|MISSING | no claim if missing | False | False |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | uncertainty | numeric\|exact\|MISSING | uncertainty or theorem exactness | False | False |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | units | SI_or_declared_natural_units | dimension control | False | False |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | projection_matrix_id | P_R10\|P_WEP\|P_PPN\|P_clock\|P_orbital\|P_GM | observable map | False | False |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | arena | R10\|WEP_MICROSCOPE\|PPN\|clock\|orbital\|Newton | test arena | False | False |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | source_path | local path, URL, DOI, or theorem certificate | provenance | False | False |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | parent_status | PARENT_DERIVED\|SOURCE_BACKED\|DERIVED_ZERO\|CLOSURE_ONLY\|MISSING | promotion status | False | False |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | valid_for_claim | false until full arena row passes | claim guard | False | False |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | claim_allowed | false until runner accepts | claim guard | False | False |

## Runner refusal status
| runner_id | target | input_status | runner_status | score_ready | reason | valid_prediction_row | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| RUN1434_0_residual_pack | local trace residual source-pack runner | SCHEMA_AND_BOUND_MAP_READY_SOURCE_ROWS_MISSING | REFUSE_NUMERIC_SCORE | False | component schema and bound map exist, but projection matrices and source-backed residual coefficients are missing | False | False | False |
| RUN1434_1_arena_bounds | R10/WEP/PPN/clock/orbital/Newton arena map | BOUND_SOURCES_STAGED_PROJECTIONS_MISSING | WAIT_FOR_PROJECTION_ROWS | False | bounds alone do not constrain MTS until residual-to-observable projections are derived or sourced | False | False | False |

## Claim gates
| gate_id | claim_component | gate_pass | claim_allowed | reason | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| CG1434_0_schema | local trace residual source-pack schema | True | False | schema exists, but schema is not evidence | False |
| CG1434_1_bound_map | arena bound map | True | False | bound map exists, but projections and coefficients are missing | False |
| CG1434_2_residual_score | numeric local trace residual score | False | False | no source-backed residual rows or projection matrices | False |
| CG1434_3_local_GR | local-GR/Newton reduction | False | False | residual branch active; no theorem-zero or numeric pass | False |

## Decision ledger
| decision_id | decision | because | effect | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- |
| DEC1434_0_bound_map | map active residuals to test arenas before scoring | bounds only matter after residual components have projection matrices | future runner can identify exactly which missing input blocks each arena | False | False |
| DEC1434_1_no_score | do not score residuals from bound sources alone | the MTS residual-to-observable map is still missing | R10/WEP/PPN/clock/orbital rows remain nonclaim | False | False |
| DEC1434_2_next | build a dry-run residual runner and missing-input dashboard next | the schema is ready; the next value is executable refusal and gap reporting | 1435 should parse the schema/map and report blocked arenas without long computation | False | False |

## Validation
| check_id | result | detail | generated_utc |
| --- | --- | --- | --- |
| VAL1434_0_sources | PASS | all 1434 cited source paths and anchors resolve | 2026-06-16T05:38:09.494501+00:00 |
| VAL1434_1_components | PASS | five local trace residual components mapped | 2026-06-16T05:38:09.494514+00:00 |
| VAL1434_2_arena_map | PASS | five arena bound-map rows written | 2026-06-16T05:38:09.494518+00:00 |
| VAL1434_3_manifest_files | PASS | branch-locked residual schema and bound map files written | 2026-06-16T05:38:09.494520+00:00 |
| VAL1434_4_missing_inputs_visible | PASS | MISSING/NOT_SCOREABLE markers remain visible | 2026-06-16T05:38:09.494523+00:00 |
| VAL1434_5_claim_gates | PASS | all claim/valid/prediction flags remain false | 2026-06-16T05:38:09.494528+00:00 |
| VAL1434_6_csv_parse | PASS | all generated 1434 CSVs parse cleanly | 2026-06-16T05:38:09.494531+00:00 |
| VAL1434_7_formalization_untouched | PASS | formalization modified-file count since start=0 | 2026-06-16T05:38:09.494533+00:00 |
| VAL1434_8_next_target | PASS | 1435 handoff written | 2026-06-16T05:38:09.494536+00:00 |
| VAL1434_9_overall | PASS | 1434 maps active local trace residual components to bound arenas as a nonclaim source-pack schema | 2026-06-16T05:38:09.494545+00:00 |

## Next target
| next_id | next_target | script | objective | include | exclude | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| NEXT1434_0_1435 | 1435-Y5-R10-RAB-local-trace-residual-runner-dryrun-and-missing-input-dashboard.md | scripts/Y5_R10_RAB_local_trace_residual_runner_dryrun_and_missing_input_dashboard.py | build a dry-run runner that parses the local trace residual source-pack schema and arena bound map, then reports every missing projection/source input while refusing numeric claims. | schema parser; bound-map parser; missing-input matrix; claim refusal; branch-id audit | long data run; numeric claim scoring; fitted coupling; local-GR claim; formalization edits; GitHub | False | False |
