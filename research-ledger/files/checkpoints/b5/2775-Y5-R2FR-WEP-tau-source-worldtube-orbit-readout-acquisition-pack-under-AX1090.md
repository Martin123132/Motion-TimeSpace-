# 2775 - Y5 R2/f(R): WEP tau Source-Worldtube / Orbit / Readout Acquisition Pack Under AX1090

## Private Verdict

`tau_WEP` is now decomposed into concrete acquisition components. None are claim-ready, and `tau_WEP=1` remains forbidden.

Best route: derive `P_WEP_relative_source_weight` directly from parent variation if possible; otherwise source every tau component before scoring.

## Source Register

| row_id | source_key | source_path | exists | needle_found | source_role | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| SRC2775_00_2774_next | 2774_next | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_2774_NEXT_TARGET.csv | True | True | current handoff into tau acquisition pack | False |
| SRC2775_01_2774_tau_functional | 2774_tau_functional | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_2774_TAU_WEP_FUNCTIONAL_DECOMPOSITION.csv | True | True | current tau functional decomposition | False |
| SRC2775_02_2774_acquisition | 2774_acquisition | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_2774_TAU_WEP_ACQUISITION_SCHEMA.csv | True | True | current tau acquisition schema | False |
| SRC2775_03_2773_tau_contract | 2773_tau_contract | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_2773_TAU_WEP_PROJECTION_CONTRACT.csv | True | True | current tau projection contract | False |
| SRC2775_04_1068_doc | 1068_doc | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1068-Y5-R10-WEP-tau-source-worldtube-orbit-readout-acquisition-pack.md | True | True | prior R10 tau acquisition pack | False |
| SRC2775_05_1068_pack | 1068_pack | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1068_TAU_WEP_ACQUISITION_PACK.csv | True | True | prior acquisition pack rows | False |
| SRC2775_06_1068_worldtube | 1068_worldtube | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1068_SOURCE_WORLDTUBE_REQUIREMENTS.csv | True | True | prior source worldtube requirements | False |
| SRC2775_07_1068_orbit | 1068_orbit | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1068_MICROSCOPE_ORBIT_READOUT_REQUIREMENTS.csv | True | True | prior orbit/readout requirements | False |
| SRC2775_08_1068_material | 1068_material | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1068_MATERIAL_RESPONSE_REQUIREMENTS.csv | True | True | prior material-response requirements | False |
| SRC2775_09_1068_force | 1068_force | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1068_OBSERVED_FRAME_FORCE_MAP.csv | True | True | prior force-map requirements | False |
| SRC2775_10_1068_xhat | 1068_xhat | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1068_XHAT_NORMALIZATION_LEDGER.csv | True | True | prior Xhat normalization ledger | False |
| SRC2775_11_1068_fallback | 1068_fallback | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1068_DIRECT_PRODUCT_FALLBACK.csv | True | True | prior direct-product fallback | False |
| SRC2775_12_1053_tau | 1053_tau | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1053_TAU_WEP_R10_PROJECTION_AUDIT.csv | True | True | tau_WEP definition-only source | False |
| SRC2775_13_1061_tau | 1061_tau | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1061_BETA_TAU_DERIVATION_ATTEMPT.csv | True | True | tau derivation attempt | False |
| SRC2775_14_1061_material_pair | 1061_material_pair | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1061_WEP_MATERIAL_CONVENTION.csv | True | True | MICROSCOPE material pair convention | False |
| SRC2775_15_1061_deltaQ | 1061_deltaQ | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1061_WEP_MATERIAL_CONVENTION.csv | True | True | alpha/Coulomb smoke material value | False |
| SRC2775_16_708_wep_map | 708_wep_map | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_708_PPN_GDOT_WEP_MAP.csv | True | True | WEP source/test charge map gap | False |
| SRC2775_17_948_bound_runner | 948_bound_runner | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_948_WEP_PRODUCT_BOUND_RUNNER.csv | True | True | WEP bound/product runner precedent | False |
| SRC2775_18_988_pressure | 988_pressure | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_988_WEP_ALPHA_PRESSURE_IMPORT.csv | True | True | WEP alpha pressure precedent | False |
| SRC2775_19_1029_tau_req | 1029_tau_req | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1029_TAU_PROJECTION_REQUIREMENTS.csv | True | True | WEP tau projection requirement | False |
| SRC2775_20_1033_tauR10 | 1033_tauR10 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1033_TAU_R10_DERIVATION_AUDIT.csv | True | True | unity tau shortcut rejection | False |
| SRC2775_21_local_bounds | local_bounds | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\local_bounds\local_bound_claims.csv | True | True | local WEP bound anchor | False |
| SRC2775_22_393_common | 393_common | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\393-source-normalized-Newtonian-limit-under-identity-closure.md | True | True | measured-G common-mode guard | False |

## Acquisition Pack

| pack_id | component | needed_for | required_artifact | current_status | claim_policy | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| TAP2775_0_source_worldtube | Earth/source worldtube | source-leg normalization of the relative source-weight residual | source stress/profile/composition convention in the observed local frame | MISSING_SOURCE_WORLDTUBE | not scoreable | False |
| TAP2775_1_orbit_average | MICROSCOPE orbit/environment average | projection from source residual to measured acceleration channel | orbit/attitude/readout averaging kernel with source path | MISSING_ORBIT_AVERAGING_KERNEL | not scoreable | False |
| TAP2775_2_eta_readout | eta_AB readout convention | convert differential acceleration residual to the MICROSCOPE observable | eta_AB sign, normalization, frame, and absolute-value scoring convention | BOUND_ANCHOR_ONLY | bound available but not prediction | False |
| TAP2775_3_material_response | Ti/Pt material response tensor | test-body leg of the relative source-weight channel | full material/source response or parent theorem reducing it to Delta_w_TiPt | MATERIAL_PAIR_ONLY | smoke convention only | False |
| TAP2775_4_observed_frame_force_map | observed-frame force map | same-frame acceleration calculation and no hidden readout rescaling | force law in e_obs with units, calibration, and no measured-G relative absorption | MISSING_FORCE_READOUT_MAP | not scoreable | False |
| TAP2775_5_Xhat_normalization | Xhat/chi_X normalization | compatibility with clock, R10, and WEP finite branches | shared parent normalization or explicitly separate finite-branch convention | MISSING_XHAT_NORMALIZATION | not scoreable | False |
| TAP2775_6_direct_product_fallback | direct P_WEP product | avoid artificial split into Delta_w and tau if parent variation gives the observable directly | numeric or theorem-zero P_WEP_relative_source_weight with source path | MISSING_DIRECT_PRODUCT | runner refuses until numeric/theorem-zero | False |

## Earth / Source Worldtube

| worldtube_id | required_input | purpose | accepted_form | current_status | blocks | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| SWT2775_0_source_stress_profile | T_source^Earth(x) or equivalent source-mass profile | source leg for WEP residual field | sourced profile/table or theorem reducing extended Earth to calibrated point-source convention | MISSING | tau_WEP | False |
| SWT2775_1_source_composition | Earth/source composition or source-charge convention | distinguish universal mass source from retained composition/source-weight residual | species/source map or proof that source leg is universal/common-mode | MISSING | Delta_w source/test split | False |
| SWT2775_2_GM_calibration | measured GM/G calibration convention | separate common mode from relative source weight | calibration row proving only common universal factors are absorbed | COMMON_MODE_GUARD_ONLY | fake measured-G absorption | False |
| SWT2775_3_finite_source_correction | finite-size and altitude/source support correction | maps source profile to spacecraft location | integral kernel or justified point-source limit with error bound | MISSING | numeric tau_WEP | False |
| SWT2775_4_frame_units | observed-frame units and source normalization | keep tau dimensionless and compatible with eta_AB | declared observed coframe and units conversion | MISSING | unit-safe runner input | False |
| SWT2775_5_verdict | source worldtube pack | source-side of tau_WEP | all SWT2775_0..4 real or theorem-reduced | SOURCE_WORLDTUBE_NOT_ACQUIRED | tau_WEP and WEP product scoring | False |

## MICROSCOPE Orbit / Readout

| orbit_id | required_input | purpose | accepted_form | current_status | blocks | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| ORB2775_0_orbit_ephemeris | MICROSCOPE orbit/altitude/time sampling or averaged equivalent | turn Earth/source residual into instrument-frame acceleration | source-backed orbit parameters or official averaged kernel | MISSING | tau_WEP | False |
| ORB2775_1_attitude_axis | instrument sensitive axis/attitude convention | project residual acceleration into measured channel | axis convention or theorem that scalar residual is orientation independent | MISSING | sign/readout convention | False |
| ORB2775_2_eta_convention | eta_AB normalization/sign convention | define comparison to 2.8e-15 bound | eta_AB formula and absolute-value claim convention | BOUND_IMPORTED_BUT_FORMULA_NOT_PARENT_MAPPED | direct P_WEP row | False |
| ORB2775_3_environmental_model | known systematics/environment subtraction convention | avoid mixing MTS residual with experimental nuisance subtraction | official readout/systematics convention or conservative envelope | MISSING | claim-grade tau | False |
| ORB2775_4_average_kernel | time/orbit averaging kernel | define tau_WEP as an averaged projection, not an instantaneous guess | kernel K_orb(t) or stated averaged scalar convention | MISSING | numeric tau_WEP | False |
| ORB2775_5_verdict | orbit/readout pack | experiment-side of tau_WEP | all ORB2775_0..4 real or theorem-reduced | ORBIT_READOUT_NOT_ACQUIRED | tau_WEP and WEP product scoring | False |

## Material Response

| material_id | quantity | value_or_status | source | current_status | blocks | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| MAT2775_0_pair_convention | MICROSCOPE Ti/Pt test pair | TA6V_minus_PtRh10 | P8_Y5_R10_1061_WEP_MATERIAL_CONVENTION.csv:MCON1061_0_test_pair | SMOKE_CONTEXT_AVAILABLE | does not itself provide material tensor | False |
| MAT2775_1_alpha_charge_smoke | Delta_Q_alpha_Coulomb_abs | 0.001989808886825 | P8_Y5_R10_1061_WEP_MATERIAL_CONVENTION.csv:MCON1061_1_delta_Q_alpha | SMOKE_VALUE_AVAILABLE | alpha/Coulomb smoke channel is not the full relative source-weight tensor | False |
| MAT2775_2_full_tensor | Ti/Pt relative-source material response tensor | MISSING_FULL_MATERIAL_TENSOR | needed: source-backed MICROSCOPE/material model or parent theorem | MISSING | Delta_w_TiPt mapping | False |
| MAT2775_3_source_weight_response | Delta_w_TiPt response convention | MISSING_DELTA_W_RESPONSE_MAP | needed: source-only weight theorem or finite prior convention | MISSING | WEP product prediction | False |
| MAT2775_4_no_cancellation | signed material cancellation | FORBIDDEN_WITHOUT_FULL_SIGNED_MODEL | 2773/2774 refusal gates | ABSOLUTE_VALUE_GUARD | fake WEP pass by sign tuning | False |
| MAT2775_5_verdict | material response pack | MATERIAL_PAIR_ONLY_NOT_CLAIM_READY | 1061 convention rows | NOT_ACQUIRED | tau_WEP/direct product scoring | False |

## Observed-Frame Force Map

| force_id | required_clause | formula_or_rule | current_status | blocks | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| FRM2775_0_observed_frame | same observed coframe for source variation, force law, clocks, and readout | e_obs = e_source = e_force = e_readout through WEP order | CONDITIONAL_FROM_PRIOR_SPINE | frame-safe tau_WEP | False |
| FRM2775_1_eta_mapping | map residual force to eta_AB | eta_AB = readout[(a_A-a_B), calibration] in MICROSCOPE convention | BOUND_OBSERVABLE_KNOWN_MAP_NOT_DERIVED | direct product scoring | False |
| FRM2775_2_common_mode_separation | common source normalization removed only by universal calibration | relative w_A/w_B cannot be absorbed into measured G or GM | GUARD_ACTIVE | fake local-GR pass | False |
| FRM2775_3_units | dimensionless tau/product convention | P_WEP_relative_source_weight must be dimensionless and comparable to eta_bound | SCHEMA_ONLY | runner validity | False |
| FRM2775_4_direct_variation | direct parent variation option | derive delta a_AB or eta_AB directly from parent action instead of split Delta_w*tau | MISSING_DIRECT_PRODUCT | fallback remains nonclaim | False |
| FRM2775_5_verdict | observed-frame force/readout map | source residual -> a_A-a_B -> eta_AB with units and calibration | FORCE_MAP_NOT_DERIVED | tau_WEP/direct product scoring | False |

## Xhat Normalization

| xhat_id | quantity | required_form | current_status | risk | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| XHN2775_0_shared_parent_norm | Xhat/chi_X normalization | same parent normalization used by clocks, WEP, and R10 or explicitly separated | MISSING_SHARED_NORMALIZATION | tau_WEP cannot be compared to clock/R10 factors | False |
| XHN2775_1_clock_transfer_guard | clock-to-WEP transfer | no clock screening imported into WEP without source/readout map | TRANSFER_BLOCKED | fake tau_WEP via clock branch | False |
| XHN2775_2_R10_transfer_guard | R10-to-WEP transfer | no tau_R10 unity or profile factor imported into WEP | TRANSFER_BLOCKED | profile/unit contamination | False |
| XHN2775_3_direct_product_escape | direct P_WEP product | parent variation gives dimensionless eta_AB product directly | MISSING_DIRECT_PRODUCT | split-factor ambiguity persists | False |
| XHN2775_4_verdict | Xhat normalization pack | shared normalization or direct product | NOT_ACQUIRED | tau_WEP remains a free symbol | False |

## Direct Product Fallback

| fallback_id | route | accepted_evidence | current_status | why_it_matters | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| DPF2775_0_preferred_route | derive P_WEP_relative_source_weight directly | parent variation produces eta_AB residual or theorem-zero with units/source path | MISSING_DIRECT_PARENT_PRODUCT | bypasses arbitrary split into Delta_w and tau_WEP | False |
| DPF2775_1_split_route | P = abs(Delta_w_TiPt * tau_WEP) | both factors numeric/sourced or theorem-zero; no unity shortcut | MISSING_BOTH_FACTORS | finite branch can still be tested if direct product is not derived | False |
| DPF2775_2_theorem_zero_route | P=0 | parent source-scalar/action-scale theorem or WEP projection silence theorem | THEOREM_ZERO_UNSIGNED | would close WEP branch without data-fitting | False |
| DPF2775_3_refusal_rule | reject non-evidence | no tau=1, no Delta_w=0 by taste, no measured-G absorption, no cancellation | REFUSAL_ACTIVE | prevents local-GR/WEP false positives | False |

## WEP Product Candidate

| prediction_id | arena | product_symbol | product_value | product_units | product_source | inputs_present | required_inputs | derivation_status | valid_for_claim | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PRED2775_0_WEP_tau_acquisition_pack_product | MICROSCOPE_WEP | P_WEP_relative_source_weight | MISSING_DIRECT_PRODUCT_OR_DELTA_W_TiPt_TIMES_TAU_WEP | dimensionless | source-intake\mts_residuals\P8_Y5_R2FR_2775_DIRECT_PRODUCT_FALLBACK.csv | eta_TiPt_bound=2.8e-15;material_pair=TA6V_minus_PtRh10;alpha_smoke_deltaQ=0.001989808886825 | source worldtube;orbit/readout kernel;material response tensor;force map;Xhat normalization;direct product or Delta_w*tau | MISSING_TAU_WEP_ACQUISITION_PACK_INPUTS | False | 2775 is an acquisition pack; the row is intentionally nonclaim until the pack is filled. |

## WEP Bound Import

| bound_id | arena | product_symbol | bound_value | bound_units | bound_source | source_row | bound_type | bound_valid_for_internal_runner | valid_for_claim | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| BOUND2775_0_WEP_source_charge | MICROSCOPE_WEP | P_WEP_relative_source_weight | 2.8e-15 | dimensionless | source-intake\local_bounds\local_bound_claims.csv | R1_WEP_source_charge | numeric_bound_anchor_internal_runner_only | True | False | MICROSCOPE Ti/Pt source-charge proxy bound; bound only, not an MTS prediction. |

## Runner Status

| runner_id | prediction_rows | bound_rows | valid_prediction_rows | valid_bound_rows | comparison_rows | passed_rows | blocked_or_failed_rows | claim_allowed | generated_utc | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| APR2775_0_WEP_tau_acquisition_pack | 1 | 1 | 0 | 1 | 1 | 0 | 1 | False | 2026-06-23T17:17:59.694144+00:00 | False |

## Runner Comparisons

| comparison_id | arena | product_symbol | product_value | bound_value | comparison_status | pass_for_claim | issues | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PRODUCT_COMPARE_NO_VALID_PREDICTIONS |  |  |  |  | not_run | False | no valid MTS tau acquisition product prediction rows | False |

## Claim Gates

| gate_id | claim | gate_pass | reason | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| CG2775_0_tau_acquisition_pack | tau_WEP acquisition pack is complete | False | source worldtube, orbit/readout, material tensor, force map, and Xhat normalization remain missing | False | False |
| CG2775_1_tau_numeric | tau_WEP is numeric or theorem-zero | False | tau_WEP remains definition-only and tau=1 is explicitly forbidden | False | False |
| CG2775_2_direct_product | direct P_WEP product is derived | False | no parent variation produces eta_AB residual directly yet | False | False |
| CG2775_3_runner_score | WEP product can be scored | False | strict runner has valid_prediction_rows=0 | False | False |
| CG2775_4_local_GR_WEP | local GR/WEP coupling branch is derived | False | finite WEP projection and source-scalar theorem routes remain open | False | False |

## Decisions

| decision_id | decision | because | next_action | valid_for_claim |
| --- | --- | --- | --- | --- |
| DEC2775_0_pack_status | tau_WEP acquisition pack is explicit but empty of claim-grade data | each required component has a named row and refusal gate | source real MICROSCOPE/source/readout rows or derive direct product | False |
| DEC2775_1_best_route | direct P_WEP derivation remains the cleanest theory route | it avoids arbitrary split-factor priors; if unavailable, tau pack components must be sourced | attempt direct eta_AB product theorem before web/data acquisition | False |
| DEC2775_2_best_next | next target is direct WEP product theorem or first real tau source row | 2775 names the missing pack; 2776 should either derive P_WEP or acquire the first real component | 2776-Y5-R2FR-direct-WEP-product-theorem-or-first-real-tau-source-row-under-AX1090.md | False |

## Next Target

| row_id | next_target | script | objective | include | exclude | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| NEXT2775_0_2776 | 2776-Y5-R2FR-direct-WEP-product-theorem-or-first-real-tau-source-row-under-AX1090.md | scripts/Y5_R2FR_direct_WEP_product_theorem_or_first_real_tau_source_row_under_AX1090_2776.py | attempt a direct parent variation theorem for P_WEP_relative_source_weight; if it fails, acquire the first real tau_WEP source row, starting with MICROSCOPE eta/readout convention or Earth/source worldtube metadata | direct eta_AB variation theorem, no split-factor shortcut, official MICROSCOPE readout/source row requirements, source URL/DOI provenance, units, valid_for_claim refusal gates | setting tau_WEP to one, setting Delta_w to zero by taste, measured-G absorption of relative weights, cancellation arguments, public WEP/local-GR claim, GitHub action, formalization-workbench edits | False |

## Branch Copies

| copy_id | table_key | source_table | copy_path | purpose | exists | row_count | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| BR2775_0_pack_queue | pack | source-intake\mts_residuals\P8_Y5_R2FR_2775_TAU_WEP_ACQUISITION_PACK.csv | source-intake\rab-sector\acquisition-queue\JR2775_WEP_TAU_ACQUISITION_PACK_NONCLAIM.csv | WEP tau acquisition pack nonclaim copy | True | 41 | False |
| BR2775_1_direct_queue | direct | source-intake\mts_residuals\P8_Y5_R2FR_2775_DIRECT_PRODUCT_FALLBACK.csv | source-intake\rab-sector\acquisition-queue\JR2775_DIRECT_WEP_PRODUCT_FALLBACK_NONCLAIM.csv | direct WEP product fallback nonclaim copy | True | 11 | False |
| BR2775_2_beta_doc | beta_doc | source-intake\mts_residuals\P8_Y5_R2FR_2775_TAU_WEP_ACQUISITION_PACK.csv | source-intake\beta-source\docs\WEP_TAU_ACQUISITION_2775_NONCLAIM.csv | beta/source-facing WEP tau acquisition copy | True | 12 | False |
| BR2775_3_microscope_copy | microscope | source-intake\mts_residuals\P8_Y5_R2FR_2775_WEP_TAU_PRODUCT_CANDIDATE_NONCLAIM.csv | source-intake\microscope\branch_locked_wep\residuals\wep_tau_acquisition_pack_2775_nonclaim.csv | MICROSCOPE tau acquisition pack copy | True | 43 | False |
| BR2775_4_next_queue | next | source-intake\mts_residuals\P8_Y5_R2FR_2775_NEXT_TARGET.csv | source-intake\rab-sector\acquisition-queue\JR2775_DIRECT_WEP_OR_FIRST_TAU_SOURCE_NEXT.csv | next direct WEP or first tau source target | True | 1 | False |

## Validation

| validation_id | passed | detail | timestamp_utc |
| --- | --- | --- | --- |
| VAL2775_0_sources | True | every cited source path exists and source needle was found | 2026-06-23T17:18:03.532406+00:00 |
| VAL2775_1_pack_components_written | True | tau_WEP acquisition pack components are written as nonclaim rows | 2026-06-23T17:18:03.532423+00:00 |
| VAL2775_2_worldtube_missing_explicit | True | source worldtube remains explicitly missing | 2026-06-23T17:18:03.532427+00:00 |
| VAL2775_3_orbit_readout_missing_explicit | True | orbit/readout pack remains explicitly missing | 2026-06-23T17:18:03.532429+00:00 |
| VAL2775_4_material_response_guarded | True | material tensor is not claim-ready | 2026-06-23T17:18:03.532433+00:00 |
| VAL2775_5_force_map_missing | True | observed-frame force map is not derived | 2026-06-23T17:18:03.532436+00:00 |
| VAL2775_6_xhat_missing | True | Xhat normalization pack remains missing | 2026-06-23T17:18:03.532439+00:00 |
| VAL2775_7_direct_product_fallback_written | True | direct product fallback is written and missing | 2026-06-23T17:18:03.532441+00:00 |
| VAL2775_8_prediction_nonclaim | True | WEP tau acquisition prediction remains nonclaim | 2026-06-23T17:18:03.532444+00:00 |
| VAL2775_9_bound_anchor_numeric | True | WEP bound anchor is numeric and internal-runner only | 2026-06-23T17:18:03.532447+00:00 |
| VAL2775_10_runner_refuses_placeholder | True | strict runner refuses missing tau acquisition product | 2026-06-23T17:18:03.532450+00:00 |
| VAL2775_11_claim_gates_blocked | True | all tau/WEP/local-GR claim gates remain blocked | 2026-06-23T17:18:03.532453+00:00 |
| VAL2775_12_next_target_written | True | next target selects direct WEP theorem or first real tau source row | 2026-06-23T17:18:03.532456+00:00 |
| VAL2775_13_branch_outputs | True | branch copies exist and contain rows | 2026-06-23T17:18:03.532459+00:00 |
| VAL2775_14_csv_parse | True | all generated CSV outputs parse cleanly | 2026-06-23T17:18:03.532461+00:00 |
| VAL2775_15_no_claim_flags | True | no generated row is valid_for_claim=true/claim_allowed=true/pass_for_claim=true | 2026-06-23T17:18:03.532464+00:00 |
| VAL2775_16_generated_files_in_post_checkpoint | True | all generated files are under post-checkpoint-work | 2026-06-23T17:18:03.532467+00:00 |
| VAL2775_17_formalization_untouched | True | formalization-workbench modified-file count remains zero during this run | 2026-06-23T17:18:03.532471+00:00 |
| VAL2775_18_pycache_absent | True | scripts __pycache__ removed | 2026-06-23T17:18:03.532475+00:00 |
| VAL2775_OVERALL | True | 2775 builds the live R2/f(R) tau_WEP acquisition pack, decomposes source worldtube, MICROSCOPE orbit/readout, material response, observed-frame force map, Xhat normalization, and direct-product fallback, keeps every component nonclaim/missing where appropriate, refuses tau=1 and missing direct products, blocks WEP/local-GR claims, and selects direct WEP product theorem or first real tau source row as the next target. | 2026-06-23T17:18:03.532489+00:00 |

## Plain-English Read

This turns `tau_WEP` from a loose symbol into a shopping list with locks on every drawer. The best attack is still to derive the direct WEP product from the parent variation; if that fails, the first real acquisition row should be MICROSCOPE eta/readout convention or Earth/source worldtube metadata.

