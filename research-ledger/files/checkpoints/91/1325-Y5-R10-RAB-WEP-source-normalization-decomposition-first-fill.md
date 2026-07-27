# 1325: RAB WEP Source-Normalization Decomposition First Fill

**Current verdict:** 1325 decomposes the WEP/coupling route but does not score it. The branch is sharper now: alpha/Coulomb, source-weight, full-tensor, and direct-product paths are separate refusal rows.

**Main progress:** WEP is no longer one blob called "missing coupling." We now know which pieces are available as pressure/context rows and which pieces still block an actual prediction.

**Decision:** go after `Delta_w_TiPt`/source-weight ownership next. That is the cleanest coupling bottleneck: either prove it is zero from the parent matter/source grammar, or source a finite prior-width row without pretending.

## Source Register
| source_id | local_path | needle | exists | needle_found | role | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| SRC1325_0_1324_next | source-intake/mts_residuals/P8_Y5_R10_1324_NEXT_TARGET.csv | NEXT1324_0_1325 | True | True | handoff into WEP source-normalization decomposition | False | False |
| SRC1325_1_1324_route | source-intake/mts_residuals/P8_Y5_R10_1324_WEP_SOURCE_NORMALIZATION_ROUTE.csv | WEP1324_0_beta_source_alpha | True | True | WEP route fields selected by 1324 | False | False |
| SRC1325_2_1316_formula | source-intake/mts_residuals/P8_Y5_R10_1316_P0_PRODUCT_FORMULA_REQUIREMENTS.csv | FORM1316_2_wep | True | True | canonical WEP product formula requirements | False | False |
| SRC1325_3_1317_runner | source-intake/mts_residuals/P8_Y5_R10_1317_PRIORITY_RUNNER_REFUSAL_TABLE.csv | RUN1317_2_run1314_2_wep | True | True | prior refused WEP runner row | False | False |
| SRC1325_4_1053_beta | source-intake/mts_residuals/P8_Y5_R10_1053_BETA_SOURCE_ALPHA_DERIVATION_AUDIT.csv | BSA1053_1_alpha_marker_source | True | True | beta_source_alpha source-chain audit | False | False |
| SRC1325_5_1053_tau | source-intake/mts_residuals/P8_Y5_R10_1053_TAU_WEP_R10_PROJECTION_AUDIT.csv | TPR1053_1_tau_WEP_definition | True | True | tau_WEP projection audit | False | False |
| SRC1325_6_1053_material | source-intake/mts_residuals/P8_Y5_R10_1053_WEP_COMPOSITION_CHARGE_MATRIX.csv | WCM1053_4 | True | True | Ti/Pt alpha-Coulomb smoke material delta | False | False |
| SRC1325_7_1094_contract | source-intake/mts_residuals/P8_Y5_R10_1094_DIRECT_WEP_PRODUCT_CONTRACT.csv | DWP1094_4_required_prediction | True | True | direct WEP alpha product contract | False | False |
| SRC1325_8_1224_contract | source-intake/mts_residuals/P8_Y5_R10_1224_FINITE_SOURCE_WEIGHT_INPUT_CONTRACT.csv | FSW1224_1_delta_w | True | True | finite source-weight input contract | False | False |
| SRC1325_9_1224_product | source-intake/mts_residuals/P8_Y5_R10_1224_SOURCE_WEIGHT_PRODUCT_LAW.csv | PROD1224_0_source_weight | True | True | source-weight product law | False | False |
| SRC1325_10_1225_tau | source-intake/mts_residuals/P8_Y5_R10_1225_TAU_WEP_SOURCE_ACQUISITION_TABLE.csv | ACQ1225_0_official_readout_arrays | True | True | tau_WEP acquisition blockers | False | False |
| SRC1325_11_1080_pack | source-intake/mts_residuals/P8_Y5_R10_1080_FINITE_WEP_INPUT_PACK_NONCLAIM.csv | FIP1080_0_product_formula | True | True | finite WEP product formula and input pack | False | False |
| SRC1325_12_983_material | source-intake/mts_residuals/P8_Y5_R10_983_MATERIAL_CONSTITUENTS.csv | WEB983_0_MICROSCOPE_CQG_COMPOSITION | True | True | MICROSCOPE alloy composition context | False | False |

## WEP Product Decomposition
| decomp_id | branch | product_law | threshold | threshold_units | available_inputs | missing_inputs | current_status | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| DECOMP1325_0_alpha_coulomb_factorized | alpha_Coulomb_smoke | P_WEP_alpha = abs(beta_source_alpha * b_alpha * tau_WEP * DeltaQ_alpha_AB) | 4.797780522732e-05 | dimensionless | DeltaQ_alpha_AB smoke value; eta/product threshold | beta_source_alpha;b_alpha_or_zero_certificate;tau_WEP;source_worldtube;readout_kernel | DECOMPOSED_NOT_SCOREABLE | False | False |
| DECOMP1325_1_alpha_coulomb_direct | alpha_Coulomb_direct | P_WEP_alpha_direct = abs(parent predicted eta_AB residual / unit_source_eta_prediction) | 4.797780522732e-05 | dimensionless | comparison threshold only | MISSING_MTS_DIRECT_PRODUCT | MISSING_DIRECT_PRODUCT | False | False |
| DECOMP1325_2_source_weight_relative | relative_source_weight | P_WEP_source_weight = abs(Delta_w_TiPt * tau_WEP) | 2.8e-15 | dimensionless_eta | eta Ti/Pt bound anchor | MISSING_NUMERIC_PRIOR_WIDTH;MISSING_LAB_SOURCE_ORBIT_PROJECTION;MISSING_SOURCE_PROFILE_WEIGHTING;OFFICIAL_ARRAYS_NOT_IMPORTED | NOT_SCOREABLE | False | False |
| DECOMP1325_3_full_finite_tensor | full_parent_basis | P_WEP = sum_I C_parent^I * R_source_I^Earth * DeltaR_material_I projected by K_MICROSCOPE | 2.8e-15 or branch-specific normalized product threshold | dimensionless_eta | composition context; DD smoke alpha/surface deltas; readout structure source-backed | C_parent vector; same-basis Earth source vector; full material tensor; official arrays/product convention | FORMULA_READY_NONCLAIM | False | False |

## First-Fill Input Matrix
| input_id | object | current_value_or_status | units | source | fill_status | usable_role | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| IN1325_0_eta_bound | eta_TiPt_bound | 2.8e-15 | dimensionless | P8_Y5_R10_1094_DIRECT_WEP_PRODUCT_CONTRACT.csv:DWP1094_0_observable | BOUND_ANCHOR_AVAILABLE | comparison fence only | False | False |
| IN1325_1_alpha_product_threshold | P_WEP_alpha_direct threshold | 4.797780522732e-05 | dimensionless | P8_Y5_R10_1094_DIRECT_WEP_PRODUCT_CONTRACT.csv:DWP1094_3_direct_product_bound | THRESHOLD_AVAILABLE_NONCLAIM | private pressure target | False | False |
| IN1325_2_deltaQ_alpha_smoke | DeltaQ_alpha_AB | 0.001989808886825 | dimensionless | P8_Y5_R10_1053_WEP_COMPOSITION_CHARGE_MATRIX.csv:WCM1053_4 | SMOKE_NUMERIC_AVAILABLE | external DD alpha/Coulomb smoke convention only | False | False |
| IN1325_3_deltaQ_surface_smoke | DeltaQ_surface_binding | 0.003306456347405 | dimensionless | P8_Y5_R10_1053_WEP_COMPOSITION_CHARGE_MATRIX.csv:WCM1053_5 | SMOKE_NUMERIC_AVAILABLE | external DD surface/binding smoke convention only | False | False |
| IN1325_4_beta_source_alpha | beta_source_alpha | MISSING_SOURCE_NORMALIZATION | dimensionless_or_branch_convention | P8_Y5_R10_1053_BETA_SOURCE_ALPHA_DERIVATION_AUDIT.csv:BSA1053_5_verdict | MISSING | required alpha/source coupling input | False | False |
| IN1325_5_balpha | b_alpha_or_zero_certificate | MISSING_SOURCE_BACKED_COEFFICIENT_OR_PARENT_PRIMITIVE | dimensionless | P8_Y5_R10_1316_P0_SOURCE_REQUIREMENT_LEDGER.csv:REQ1316_0_balpha | MISSING | required alpha branch coefficient unless direct product bypass is sourced | False | False |
| IN1325_6_tau_WEP | tau_WEP | MISSING_LAB_SOURCE_ORBIT_PROJECTION | dimensionless | P8_Y5_R10_1225_SYMBOLIC_TAU_WEP_FORMULA.csv:FORM1225_0_tau_WEP_functional | SYMBOLIC_ONLY_NONCLAIM | required WEP projection/readout factor | False | False |
| IN1325_7_delta_w | Delta_w_TiPt | MISSING_NUMERIC_PRIOR_WIDTH | dimensionless | P8_Y5_R10_1224_FINITE_SOURCE_WEIGHT_INPUT_CONTRACT.csv:FSW1224_1_delta_w | MISSING | required relative source-weight coupling input | False | False |
| IN1325_8_readout_arrays | K_MICROSCOPE/source-weight readout kernel | OFFICIAL_ARRAYS_NOT_IMPORTED | eta projection convention | P8_Y5_R10_1225_TAU_WEP_SOURCE_ACQUISITION_TABLE.csv:ACQ1225_0_official_readout_arrays | MISSING | required for claim-grade tau_WEP/readout normalization | False | False |
| IN1325_9_direct_product | MTS P_WEP_alpha_direct | MISSING_MTS_DIRECT_PRODUCT | dimensionless | P8_Y5_R10_1094_DIRECT_WEP_PRODUCT_CONTRACT.csv:DWP1094_4_required_prediction | MISSING | preferred bypass if parent variation gives observable directly | False | False |

## WEP Decomposition Runner
| runner_id | product_branch | comparison_threshold | threshold_units | predicted_value | available_inputs | missing_inputs | runner_status | refusal_reason | score_ready | valid_prediction_row | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| RUN1325_0_alpha_coulomb_factorized | alpha_Coulomb_smoke | 4.797780522732e-05 | dimensionless | MISSING_BETA_SOURCE_ALPHA_B_ALPHA_TAU_WEP_PRODUCT | DeltaQ_alpha_AB_smoke;threshold | beta_source_alpha;b_alpha_or_zero_certificate;tau_WEP;source_worldtube;readout_kernel | REFUSED | required coupling/readout inputs missing; smoke material delta is not a prediction | False | False | False | False |
| RUN1325_1_source_weight_relative | relative_source_weight | 2.8e-15 | dimensionless_eta | MISSING_DELTA_W_TIPT_TIMES_TAU_WEP | eta_bound | MISSING_NUMERIC_PRIOR_WIDTH;MISSING_LAB_SOURCE_ORBIT_PROJECTION;MISSING_SOURCE_PROFILE_WEIGHTING;OFFICIAL_ARRAYS_NOT_IMPORTED | REFUSED | Delta_w_TiPt and tau_WEP/readout/source profile not sourced | False | False | False | False |
| RUN1325_2_direct_wep_product | direct_parent_observable | 4.797780522732e-05 | dimensionless | MISSING_MTS_DIRECT_PRODUCT | comparison_threshold_only | parent predicted eta residual;source path;readout convention;sign convention | REFUSED | direct parent product not derived or sourced | False | False | False | False |

## Blocker Ledger
| blocker_id | blocks_runner | missing_object | current_status | required_resolution | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- |
| BLK1325_0_beta_source_alpha | RUN1325_0_alpha_coulomb_factorized | beta_source_alpha | MISSING_SOURCE_NORMALIZATION | derive source-normalization zero/finite coefficient or source numeric prior | False | False |
| BLK1325_1_balpha | RUN1325_0_alpha_coulomb_factorized | b_alpha_or_zero_certificate | MISSING_SOURCE_BACKED_COEFFICIENT_OR_PARENT_PRIMITIVE | source coefficient or signed no-hidden/radiative/readout theorem-zero | False | False |
| BLK1325_2_tau_WEP | RUN1325_0_alpha_coulomb_factorized;RUN1325_1_source_weight_relative | tau_WEP | SYMBOLIC_ONLY_NONCLAIM | source worldtube/orbit/readout functional with normalization or direct observable bypass | False | False |
| BLK1325_3_delta_w | RUN1325_1_source_weight_relative | Delta_w_TiPt | MISSING_NUMERIC_PRIOR_WIDTH | prove source-weight zero or source finite Ti/Pt relative weight prior | False | False |
| BLK1325_4_readout_arrays | RUN1325_0_alpha_coulomb_factorized;RUN1325_1_source_weight_relative | official MICROSCOPE readout arrays/product convention | OFFICIAL_ARRAYS_NOT_IMPORTED | import official arrays/export or use a source-backed averaged kernel | False | False |
| BLK1325_5_direct_product | RUN1325_2_direct_wep_product | MTS P_WEP_alpha_direct | MISSING_DIRECT_PRODUCT | derive parent variation to eta_AB observable or source numeric direct product | False | False |

## Anti-Shortcut Gates
| gate_id | shortcut | enforcement | status | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- |
| SHORT1325_0_no_unity_couplings | set beta_source_alpha, b_alpha, tau_WEP, or Delta_w_TiPt to unity/zero by taste | REFUSED unless parent theorem or source-backed value exists | ENFORCED | False | False |
| SHORT1325_1_no_threshold_prediction | use eta or normalized threshold as the MTS prediction | REFUSED; thresholds are comparison fences only | ENFORCED | False | False |
| SHORT1325_2_no_smoke_tensor_claim | treat DD alpha/surface smoke deltas as the full MTS material tensor | REFUSED; smoke rows remain external nonclaim context | ENFORCED | False | False |
| SHORT1325_3_no_cancellation_pass | claim WEP pass through signed material/source cancellation | REFUSED without full signed material/source/readout model | ENFORCED | False | False |
| SHORT1325_4_no_cross_arena_transfer | reuse clock/R10 rows as WEP evidence | REFUSED until a parent branch/readout functor is signed | ENFORCED | False | False |

## Decision Ledger
| decision_id | decision | because | effect | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- |
| DEC1325_0_wep_decomposed | WEP route is decomposed into factorized alpha, source-weight, and direct-product branches | clock wait-state showed the coupling/readout product is the real missing object | WEP now has explicit runnable refusal rows instead of one vague missing-coupling row | False | False |
| DEC1325_1_no_score | no WEP score or pass/fail is claimed | all branches still miss source-normalization, tau/readout, direct product, or full material/source inputs | private pressure targets remain useful but nonclaim | False | False |
| DEC1325_2_best_next | attack source-weight owner or finite Delta_w prior next | Delta_w/source-weight is the clean coupling bottleneck and less dependent on cosmological/clock assumptions | 1326 should try theorem-zero first, otherwise create a finite prior-width source row | False | False |

## Next Target
| next_id | target_file | target_script | task | success_condition | do_not | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| NEXT1325_0_1326 | 1326-Y5-R10-RAB-WEP-source-weight-owner-zero-or-finite-Delta-w-prior.md | scripts/Y5_R10_RAB_WEP_source_weight_owner_zero_or_finite_Delta_w_prior.py | try to prove Delta_w_TiPt=0 from parent source-weight ownership; if that fails, stage a finite Delta_w prior-width row with source/provenance and keep WEP nonclaim | source-weight branch either gains a parent-signed zero certificate or an explicit finite Delta_w input contract without unity/cancellation shortcuts | do not set Delta_w=0 by naturality alone; do not use smoke material deltas as full tensor; do not claim WEP pass | False | False |

## Validation
| check_id | check | status | details |
| --- | --- | --- | --- |
| VAL1325_0_sources_exist | registered source paths exist and anchors are found | PASS | 13/13 source anchors found |
| VAL1325_1_branches_decomposed | WEP decomposition covers alpha factorized, alpha direct, source-weight, and full tensor branches | PASS | alpha_Coulomb_direct;alpha_Coulomb_smoke;full_parent_basis;relative_source_weight |
| VAL1325_2_input_matrix_covers_coupling_gap | first-fill matrix includes available anchors and missing coupling/readout inputs | PASS | IN1325_0_eta_bound;IN1325_1_alpha_product_threshold;IN1325_2_deltaQ_alpha_smoke;IN1325_3_deltaQ_surface_smoke;IN1325_4_beta_source_alpha;IN1325_5_balpha;IN1325_6_tau_WEP;IN1325_7_delta_w;IN1325_8_readout_arrays;IN1325_9_direct_product |
| VAL1325_3_runner_refuses_all_branches | runner refuses all current WEP branches and scores nothing | PASS | RUN1325_0_alpha_coulomb_factorized=required coupling/readout inputs missing; smoke material delta is not a prediction;RUN1325_1_source_weight_relative=Delta_w_TiPt and tau_WEP/readout/source profile not sourced;RUN1325_2_direct_wep_product=direct parent product not derived or sourced |
| VAL1325_4_blockers_recorded | blocker ledger records coupling, tau, readout, and direct-product missing objects | PASS | BLK1325_0_beta_source_alpha;BLK1325_1_balpha;BLK1325_2_tau_WEP;BLK1325_3_delta_w;BLK1325_4_readout_arrays;BLK1325_5_direct_product |
| VAL1325_5_shortcuts_enforced | anti-shortcut gates are enforced | PASS | SHORT1325_0_no_unity_couplings;SHORT1325_1_no_threshold_prediction;SHORT1325_2_no_smoke_tensor_claim;SHORT1325_3_no_cancellation_pass;SHORT1325_4_no_cross_arena_transfer |
| VAL1325_6_nonclaim_policy | all generated rows remain nonclaim | PASS | valid_for_claim=false and claim_allowed=false throughout generated tables |
| VAL1325_7_formalization_untouched | formalization-workbench untouched by generated outputs | PASS | formalization_generated_output_count=0 |
| VAL1325_8_next_target_1326 | next target routes to source-weight owner zero or finite Delta_w prior | PASS | 1326-Y5-R10-RAB-WEP-source-weight-owner-zero-or-finite-Delta-w-prior.md |
| VAL1325_9_overall | overall 1325 validation | PASS | 1325 decomposes WEP source-normalization, refuses all branches, and selects source-weight owner/Delta_w next |
