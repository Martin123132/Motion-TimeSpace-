# 1225 Y5/R10 Tau WEP Source Worldtube Readout Projection

**Current verdict:** 1225 does **not** derive a numeric `tau_WEP`. It does derive the shape of the projection contract: `tau_WEP` is a dimensionless source-worldtube/orbit/coframe/material/readout functional, not a free unity factor.

**Main progress:** the source-weight product is now blocked for precise reasons only: official MICROSCOPE readout arrays, eta product normalization, Earth/source worldtube weighting, orbit averaging, Ti/Pt source-weight material tensor, and `Delta_w_TiPt` are all still required.

**Practical consequence:** this is the bridge from local-GR coupling theory into real data plumbing. The next target is readout/source acquisition, not another abstract claim.

## Source Register

| source_id | local_path | needle | purpose | absolute_path | path_exists | needle_found | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SRC1225_0_1224_next | source-intake/mts_residuals/P8_Y5_R10_1224_NEXT_TARGET.csv | 1225-Y5-R10-tau-WEP-source-worldtube-readout-projection.md | 1224 handoff to tau_WEP projection | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1224_NEXT_TARGET.csv | True | True | False | False |
| SRC1225_1_1224_contract | source-intake/mts_residuals/P8_Y5_R10_1224_FINITE_SOURCE_WEIGHT_INPUT_CONTRACT.csv | FSW1224_2_tau_WEP | tau_WEP finite input requirement | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1224_FINITE_SOURCE_WEIGHT_INPUT_CONTRACT.csv | True | True | False | False |
| SRC1225_2_1224_product | source-intake/mts_residuals/P8_Y5_R10_1224_SOURCE_WEIGHT_PRODUCT_LAW.csv | PROD1224_0_source_weight | source-weight product law | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1224_SOURCE_WEIGHT_PRODUCT_LAW.csv | True | True | False | False |
| SRC1225_3_1066_tau_contract | source-intake/mts_residuals/P8_Y5_R10_1066_TAU_WEP_PROJECTION_CONTRACT.csv | TWP1066_7_verdict | original tau_WEP projection contract | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1066_TAU_WEP_PROJECTION_CONTRACT.csv | True | True | False | False |
| SRC1225_4_1061_inputs | source-intake/mts_residuals/P8_Y5_R10_1061_INPUT_FILL_LEDGER.csv | INF1061_4_tau_WEP | tau_WEP missing input row | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1061_INPUT_FILL_LEDGER.csv | True | True | False | False |
| SRC1225_5_1061_material | source-intake/mts_residuals/P8_Y5_R10_1061_WEP_MATERIAL_CONVENTION.csv | MCON1061_0_test_pair | MICROSCOPE Ti/Pt material convention | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1061_WEP_MATERIAL_CONVENTION.csv | True | True | False | False |
| SRC1225_6_1083_source_vector | source-intake/mts_residuals/P8_Y5_R10_1083_SOURCE_VECTOR_CAVEAT_GATE.csv | SCG1083_0_profile_weighting | Earth/source profile weighting missing | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1083_SOURCE_VECTOR_CAVEAT_GATE.csv | True | True | False | False |
| SRC1225_7_1084_readout | source-intake/mts_residuals/P8_Y5_R10_1084_MICROSCOPE_READOUT_IMPORT_GATE.csv | RIG1084_0_CMSM_arrays | official MICROSCOPE readout arrays missing | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1084_MICROSCOPE_READOUT_IMPORT_GATE.csv | True | True | False | False |
| SRC1225_8_1052_alpha_wep | source-intake/mts_residuals/P8_Y5_R10_1052_ALPHA_WEP_PROJECTION_LEDGER.csv | AWP1052_0_alpha_Coulomb | WEP projection pressure precedent | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1052_ALPHA_WEP_PROJECTION_LEDGER.csv | True | True | False | False |
| SRC1225_9_local_bounds | source-intake/local_bounds/local_bound_claims.csv | R1_WEP_source_charge | MICROSCOPE source-charge proxy bound anchor | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\local_bounds\local_bound_claims.csv | True | True | False | False |

## Tau WEP Projection Attempt

| attempt_id | projection_piece | needed_object | attempt | current_status | source | effect | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TAU1225_0_source_worldtube | Earth/source worldtube and stress profile | T_source^Earth(x) with source-weight/profile convention | identify the source stress/current seen by the satellite in the observed local frame | MISSING_SOURCE_PROFILE_WEIGHTING | source-intake/mts_residuals/P8_Y5_R10_1083_SOURCE_VECTOR_CAVEAT_GATE.csv:SCG1083_0_profile_weighting | tau_WEP cannot be numeric | False | False |
| TAU1225_1_orbit_average | MICROSCOPE orbit/time average | time/session/orbit averaging convention for differential acceleration channel | map source residual through the satellite orbit and selected signal channel | MISSING_ORBIT_AVERAGE_ARRAYS | source-intake/mts_residuals/P8_Y5_R10_1066_TAU_WEP_PROJECTION_CONTRACT.csv:TWP1066_1_orbit_average | tau_WEP cannot be normalized | False | False |
| TAU1225_2_observed_coframe | observed coframe/readout frame | one e_obs convention shared by force law, source variation, clocks, and readout | keep projection in the same observed frame as the parent residual and eta_AB | CONDITIONAL_FROM_PRIOR_SPINE | source-intake/mts_residuals/P8_Y5_R10_1066_TAU_WEP_PROJECTION_CONTRACT.csv:TWP1066_2_observed_coframe | frame consistency remains conditional | False | False |
| TAU1225_3_material_response | Ti/Pt material response | TA6V-minus-PtRh10 material/source tensor in the same convention as eta_AB | reuse material convention as a label, not as a complete source-weight response tensor | MATERIAL_PAIR_ONLY | source-intake/mts_residuals/P8_Y5_R10_1061_WEP_MATERIAL_CONVENTION.csv:MCON1061_0_test_pair | Delta_w_TiPt mapping remains incomplete | False | False |
| TAU1225_4_force_readout | differential acceleration readout kernel | K_MICROSCOPE mapping parent source residual to reported eta_AB | require official CMSM/export arrays or a validated exact equivalent | OFFICIAL_ARRAYS_NOT_IMPORTED | source-intake/mts_residuals/P8_Y5_R10_1084_MICROSCOPE_READOUT_IMPORT_GATE.csv:RIG1084_0_CMSM_arrays | no surrogate kernel can promote a claim | False | False |
| TAU1225_5_normalization | eta_AB product normalization | normalization from source response x material response x readout kernel to reported Eotvos eta | tie tau_WEP to eta_TiPt rather than an arbitrary unit factor | NORMALIZATION_NOT_FILLED | source-intake/mts_residuals/P8_Y5_R10_1084_MICROSCOPE_READOUT_IMPORT_GATE.csv:RIG1084_1_product_convention | tau_WEP=1 shortcut remains forbidden | False | False |
| TAU1225_6_verdict | tau_WEP | functional[source worldtube, orbit average, observed coframe, material tensor, force readout] | derive or source all pieces | TAU_WEP_PROJECTION_NOT_DERIVED | TAU1225_0 through TAU1225_5 | source-weight product remains not scoreable | False | False |

## Symbolic Tau WEP Formula

| formula_id | symbolic_formula | meaning | required_to_evaluate | current_status | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- |
| FORM1225_0_tau_WEP_functional | tau_WEP := N_eta^{-1} < K_eta[e_obs, orbit, masks] · Integral_Earth dV K_source(x;orbit) R_source(x) · R_material(TiPt) >_orbit | dimensionless projection from parent source-weight residual to reported MICROSCOPE eta channel | N_eta;K_eta;K_source;R_source;R_material;orbit/mask average;e_obs convention | SYMBOLIC_ONLY_NONCLAIM | False | False |
| FORM1225_1_source_weight_product | abs(Delta_w_TiPt * tau_WEP) <= 2.8e-15 | finite source-weight branch bound after tau_WEP and Delta_w_TiPt are sourced | Delta_w_TiPt;tau_WEP;eta bound;absolute-product guard | NOT_SCOREABLE | False | False |

## Tau WEP Source Acquisition Table

| acquisition_id | object | required_content | current_status | source_basis | claim_effect | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ACQ1225_0_official_readout_arrays | official MICROSCOPE CMSM/export arrays | time, segment/session id, gx, gz, Sxx, Sxz, masks, calibration flags, attitude/orbit convention | OFFICIAL_ARRAYS_NOT_IMPORTED | source-intake/mts_residuals/P8_Y5_R10_1084_MICROSCOPE_READOUT_IMPORT_GATE.csv:RIG1084_0_CMSM_arrays | blocks K_eta and tau_WEP normalization | False | False |
| ACQ1225_1_product_convention | eta_AB product normalization | map from source response x material response x readout kernel to reported Eotvos eta | NORMALIZATION_NOT_FILLED | source-intake/mts_residuals/P8_Y5_R10_1084_MICROSCOPE_READOUT_IMPORT_GATE.csv:RIG1084_1_product_convention | blocks conversion from symbolic tau to numeric tau | False | False |
| ACQ1225_2_source_worldtube | Earth/source stress worldtube | profile-weighted source stress/current seen along MICROSCOPE orbit in observed local frame | MISSING_SOURCE_PROFILE_WEIGHTING | source-intake/mts_residuals/P8_Y5_R10_1083_SOURCE_VECTOR_CAVEAT_GATE.csv:SCG1083_0_profile_weighting | blocks source side of tau_WEP | False | False |
| ACQ1225_3_orbit_average | MICROSCOPE orbit/session average | time/orbit average matched to reported eta_AB channel and masks | MISSING_ORBIT_AVERAGE_ARRAYS | source-intake/mts_residuals/P8_Y5_R10_1066_TAU_WEP_PROJECTION_CONTRACT.csv:TWP1066_1_orbit_average | blocks orbit average in tau_WEP | False | False |
| ACQ1225_4_material_tensor | Ti/Pt source-weight material response tensor | material response to relative source-weight channel, not only alpha/Coulomb delta-Q | MATERIAL_PAIR_ONLY | source-intake/mts_residuals/P8_Y5_R10_1066_TAU_WEP_PROJECTION_CONTRACT.csv:TWP1066_3_material_response | blocks Delta_w_TiPt mapping | False | False |
| ACQ1225_5_delta_w | Delta_w_TiPt finite prior or theorem-zero | numeric width or parent source-weight theorem-zero, in same convention as tau_WEP | MISSING_NUMERIC_PRIOR_WIDTH | source-intake/mts_residuals/P8_Y5_R10_1224_FINITE_SOURCE_WEIGHT_INPUT_CONTRACT.csv:FSW1224_1_delta_w | blocks source-weight product even if tau_WEP is later known | False | False |

## Source Weight Product Feed

| feed_id | target_product | tau_WEP_status | Delta_w_status | eta_bound_status | product_score_status | valid_prediction_rows_delta | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| FEED1225_0_tau_to_product | PROD1224_0_source_weight | TAU_WEP_PROJECTION_NOT_DERIVED | MISSING_NUMERIC_PRIOR_WIDTH | BOUND_ANCHOR_AVAILABLE | NOT_SCOREABLE | 0 | False | False |
| FEED1225_1_tau_to_runner | RUN1221_2_source_weight | SYMBOLIC_ONLY_NONCLAIM | MISSING | 2.8e-15 | REFUSED | 0 | False | False |

## Tau WEP Anti-Shortcut Gates

| gate_id | forbidden_shortcut | reason | status | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- |
| SHORT1225_0_no_tau_unity | set tau_WEP=1 | tau_WEP is a lab/source/orbit/readout functional, not a convention-free unit | ENFORCED | False | False |
| SHORT1225_1_no_surrogate_claim | use surrogate kernel as official readout | RIG1084 requires official arrays or proof of exact equivalence | ENFORCED | False | False |
| SHORT1225_2_no_G_absorption | absorb source-weight residual into measured G | source-weight branch affects composition/source/readout comparison | ENFORCED | False | False |
| SHORT1225_3_no_cancellation | cancel signs/material terms by hand | 1224 product uses absolute guard unless full material model is signed | ENFORCED | False | False |

## Local GR WEP Feed Update

| feed_id | target | update | effect | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- |
| LGRFEED1225_0 | local GR/Newton source-side coupling | tau_WEP remains symbolic-only, so source-weight branch remains explicit and unscoreable | no local-GR pass claim; no source coupling universality claim | False | False |
| LGRFEED1225_1 | future empirical pass | official readout/source acquisition is now the shortest path to a numeric source-weight pressure test | next work should acquire/readout data or prove exact equivalence | False | False |

## Decision Ledger

| decision_id | decision | because | next_action | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- |
| DEC1225_0_tau_not_derived | do not promote tau_WEP | source worldtube, orbit average, material tensor, product normalization, and official readout are not filled | acquire official MICROSCOPE readout/export objects or write an exact equivalence proof | False | False |
| DEC1225_1_symbolic_formula_retained | retain symbolic tau_WEP functional | it pins down the projection shape without pretending to evaluate it | use FORM1225_0 as the input contract for source/readout acquisition | False | False |
| DEC1225_2_next_data_gate | move toward readout/source acquisition | the math contract is now specific enough that data plumbing is the bottleneck | stage official MICROSCOPE readout/source acquisition without claiming pass | False | False |

## Claim Gates

| gate_id | gate | status | reason | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- |
| GATE1225_0_sources | source path and needle audit | PASS | all local sources used by 1225 are traceable | False | False |
| GATE1225_1_tau_projection | tau_WEP projection derived or sourced | BLOCKED | TAU1225_6 current_status=TAU_WEP_PROJECTION_NOT_DERIVED | False | False |
| GATE1225_2_symbolic_formula | symbolic formula written | PASS | FORM1225_0 records the functional contract | False | False |
| GATE1225_3_required_sources | required readout/source objects acquired | BLOCKED | ACQ1225 rows remain missing/nonclaim | False | False |
| GATE1225_4_product_score | source-weight product scoreable | BLOCKED | tau_WEP and Delta_w_TiPt are not numeric/sourced | False | False |
| GATE1225_5_local_GR_WEP | local GR/WEP claim permission | BLOCKED | 1225 is projection plumbing only | False | False |

## Next Target

| next_id | target_file | target_script | task | success_condition | do_not_do | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| NEXT1225_0_1226 | 1226-Y5-R10-MICROSCOPE-readout-source-acquisition-ledger.md | scripts/Y5_R10_MICROSCOPE_readout_source_acquisition_ledger.py | find or stage the official MICROSCOPE readout/source objects needed by tau_WEP, with provenance and no surrogate-as-claim | official arrays/source objects are acquired or a blocker ledger records exact missing public/private data objects without fabricating rows | do not claim WEP/local-GR/PPN, do not use surrogate arrays as official, do not set tau_WEP to one, do not edit formalization-workbench or push GitHub | False | False |

## Validation

| check_id | check | status | details | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- |
| VAL1225_0_sources_exist | all cited local sources exist | PASS | 10/10 sources exist | False | False |
| VAL1225_1_needles_found | all cited source needles found | PASS | 10/10 needles found | False | False |
| VAL1225_2_tau_verdict_nonclaim | tau_WEP is not falsely promoted | PASS | TAU_WEP_PROJECTION_NOT_DERIVED | False | False |
| VAL1225_3_symbolic_formula_written | symbolic tau_WEP formula is written | PASS | FORM1225_0_tau_WEP_functional | False | False |
| VAL1225_4_acquisition_table_complete | source acquisition table includes required objects | PASS | ACQ1225_0_official_readout_arrays; ACQ1225_1_product_convention; ACQ1225_2_source_worldtube; ACQ1225_3_orbit_average; ACQ1225_4_material_tensor; ACQ1225_5_delta_w | False | False |
| VAL1225_5_missing_sources_nonclaim | missing source rows are not valid for claim | PASS | all ACQ1225 rows nonclaim | False | False |
| VAL1225_6_product_feed_refuses | product feed keeps zero valid predictions | PASS | valid_prediction_rows_delta=0 for all product feed rows | False | False |
| VAL1225_7_anti_shortcuts_enforced | anti-shortcut gates enforce no unity/surrogate/G-absorption/cancellation | PASS | SHORT1225_0_no_tau_unity; SHORT1225_1_no_surrogate_claim; SHORT1225_2_no_G_absorption; SHORT1225_3_no_cancellation | False | False |
| VAL1225_8_next_target_readout_acquisition | next target stages MICROSCOPE readout/source acquisition | PASS | 1226-Y5-R10-MICROSCOPE-readout-source-acquisition-ledger.md | False | False |
| VAL1225_9_claim_gates_blocked | claim gates keep physical claims blocked | PASS | tau/source/product/local claim gates blocked | False | False |
| VAL1225_10_nonclaim_policy | all generated rows remain nonclaim | PASS | valid_for_claim=false and claim_allowed=false throughout claim-bearing tables | False | False |
| VAL1225_11_csv_parse | all generated CSVs parse cleanly | PASS | P8_Y5_R10_1225_SOURCE_REGISTER.csv:10; P8_Y5_R10_1225_TAU_WEP_PROJECTION_ATTEMPT.csv:7; P8_Y5_R10_1225_SYMBOLIC_TAU_WEP_FORMULA.csv:2; P8_Y5_R10_1225_TAU_WEP_SOURCE_ACQUISITION_TABLE.csv:6; P8_Y5_R10_1225_SOURCE_WEIGHT_PRODUCT_FEED.csv:2; P8_Y5_R10_1225_TAU_WEP_ANTI_SHORTCUT_GATES.csv:4; P8_Y5_R10_1225_LOCAL_GR_WEP_FEED_UPDATE.csv:2; P8_Y5_R10_1225_DECISION_LEDGER.csv:3; P8_Y5_R10_1225_CLAIM_GATES.csv:6; P8_Y5_R10_1225_NEXT_TARGET.csv:1 | False | False |
| VAL1225_12_formalization_untouched | formalization-workbench untouched during run | PASS | formalization_recent_after_run_start_count=0 | False | False |
| VAL1225_13_overall | overall 1225 validation | PASS | 1225 writes symbolic tau_WEP projection and exact readout/source acquisition table without claim promotion | False | False |
