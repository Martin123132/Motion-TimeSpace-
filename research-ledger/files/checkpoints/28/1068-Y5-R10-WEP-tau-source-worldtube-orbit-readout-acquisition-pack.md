# 1068 — WEP tau Source-Worldtube / Orbit / Readout Acquisition Pack

**Current verdict:** `tau_WEP` is now decomposed into concrete acquisition components. None are claim-ready, and `tau_WEP=1` remains forbidden.

**Best route:** derive `P_WEP_relative_source_weight` directly from parent variation if possible; otherwise source every tau component before scoring.

**Runner result:** the strict WEP runner still refuses the placeholder with `valid_prediction_rows=0`.

## Acquisition Pack
| pack_id | component | needed_for | required_artifact | current_status | claim_policy | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| TAP1068_0_source_worldtube | Earth/source worldtube | source-leg normalization of the relative source-weight residual | source stress/profile/composition convention in the observed local frame | MISSING_SOURCE_WORLDTUBE | not scoreable | false |
| TAP1068_1_orbit_average | MICROSCOPE orbit/environment average | projection from source residual to measured acceleration channel | orbit/attitude/readout averaging kernel with source path | MISSING_ORBIT_AVERAGING_KERNEL | not scoreable | false |
| TAP1068_2_eta_readout | eta_AB readout convention | convert differential acceleration residual to the MICROSCOPE observable | eta_AB sign, normalization, frame, and absolute-value scoring convention | BOUND_ANCHOR_ONLY | bound available but not prediction | false |
| TAP1068_3_material_response | Ti/Pt material response tensor | test-body leg of the relative source-weight channel | full material/source response or parent theorem reducing it to Delta_w_TiPt | MATERIAL_PAIR_ONLY | smoke convention only | false |
| TAP1068_4_observed_frame_force_map | observed-frame force map | same-frame acceleration calculation and no hidden readout rescaling | force law in e_obs with units, calibration, and no measured-G relative absorption | MISSING_FORCE_READOUT_MAP | not scoreable | false |
| TAP1068_5_Xhat_normalization | Xhat/chi_X normalization | compatibility with clock, R10, and WEP finite branches | shared parent normalization or explicitly separate finite-branch convention | MISSING_XHAT_NORMALIZATION | not scoreable | false |
| TAP1068_6_direct_product_fallback | direct P_WEP product | avoid artificial split into Delta_w and tau if parent variation gives the observable directly | numeric or theorem-zero P_WEP_relative_source_weight with source path | MISSING_DIRECT_PRODUCT | runner refuses until numeric/theorem-zero | false |


## Earth / Source Worldtube
| worldtube_id | required_input | purpose | accepted_form | current_status | blocks | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| SWT1068_0_source_stress_profile | T_source^Earth(x) or equivalent source-mass profile | source leg for WEP residual field | sourced profile/table or theorem reducing extended Earth to calibrated point-source convention | MISSING | tau_WEP | false |
| SWT1068_1_source_composition | Earth/source composition or source-charge convention | distinguish universal mass source from retained composition/source-weight residual | species/source map or proof that source leg is universal/common-mode | MISSING | Delta_w source/test split | false |
| SWT1068_2_GM_calibration | measured GM/G calibration convention | separate common mode from relative source weight | calibration row proving only common universal factors are absorbed | COMMON_MODE_GUARD_ONLY | fake measured-G absorption | false |
| SWT1068_3_finite_source_correction | finite-size and altitude/source support correction | maps source profile to spacecraft location | integral kernel or justified point-source limit with error bound | MISSING | numeric tau_WEP | false |
| SWT1068_4_frame_units | observed-frame units and source normalization | keep tau dimensionless and compatible with eta_AB | declared observed coframe and units conversion | MISSING | unit-safe runner input | false |
| SWT1068_5_verdict | source worldtube pack | source-side of tau_WEP | all SWT1068_0..4 real or theorem-reduced | SOURCE_WORLDTUBE_NOT_ACQUIRED | tau_WEP and WEP product scoring | false |


## MICROSCOPE Orbit / Readout
| orbit_id | required_input | purpose | accepted_form | current_status | blocks | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| ORB1068_0_orbit_ephemeris | MICROSCOPE orbit/altitude/time sampling or averaged equivalent | turn Earth/source residual into instrument-frame acceleration | source-backed orbit parameters or official averaged kernel | MISSING | tau_WEP | false |
| ORB1068_1_attitude_axis | instrument sensitive axis/attitude convention | project residual acceleration into measured channel | axis convention or theorem that scalar residual is orientation independent | MISSING | sign/readout convention | false |
| ORB1068_2_eta_convention | eta_AB normalization/sign convention | define comparison to 2.8e-15 bound | eta_AB formula and absolute-value claim convention | BOUND_IMPORTED_BUT_FORMULA_NOT_PARENT_MAPPED | direct P_WEP row | false |
| ORB1068_3_environmental_model | known systematics/environment subtraction convention | avoid mixing MTS residual with experimental nuisance subtraction | official readout/systematics convention or conservative envelope | MISSING | claim-grade tau | false |
| ORB1068_4_average_kernel | time/orbit averaging kernel | define tau_WEP as an averaged projection, not an instantaneous guess | kernel K_orb(t) or stated averaged scalar convention | MISSING | numeric tau_WEP | false |
| ORB1068_5_verdict | orbit/readout pack | experiment-side of tau_WEP | all ORB1068_0..4 real or theorem-reduced | ORBIT_READOUT_NOT_ACQUIRED | tau_WEP and WEP product scoring | false |


## Material Response
| material_id | quantity | value_or_status | source | current_status | blocks | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| MAT1068_0_pair_convention | MICROSCOPE Ti/Pt test pair | TA6V_minus_PtRh10 | P8_Y5_R10_1061_WEP_MATERIAL_CONVENTION.csv:MCON1061_0_test_pair | SMOKE_CONTEXT_AVAILABLE | does not itself provide material tensor | false |
| MAT1068_1_alpha_charge_smoke | Delta_Q_alpha_Coulomb_abs | 0.001989808886825 | P8_Y5_R10_1061_WEP_MATERIAL_CONVENTION.csv:MCON1061_1_delta_Q_alpha | SMOKE_VALUE_AVAILABLE | alpha/Coulomb smoke channel is not the full relative source-weight tensor | false |
| MAT1068_2_full_tensor | Ti/Pt relative-source material response tensor | MISSING_FULL_MATERIAL_TENSOR | needed: source-backed MICROSCOPE/material model or parent theorem | MISSING | Delta_w_TiPt mapping | false |
| MAT1068_3_source_weight_response | Delta_w_TiPt response convention | MISSING_DELTA_W_RESPONSE_MAP | needed: source-only weight theorem or finite prior convention | MISSING | WEP product prediction | false |
| MAT1068_4_no_cancellation | signed material cancellation | FORBIDDEN_WITHOUT_FULL_SIGNED_MODEL | 1066/1067 refusal gates | ABSOLUTE_VALUE_GUARD | fake WEP pass by sign tuning | false |
| MAT1068_5_verdict | material response pack | MATERIAL_PAIR_ONLY_NOT_CLAIM_READY | 1061 convention rows | NOT_ACQUIRED | tau_WEP/direct product scoring | false |


## Observed-Frame Force Map
| force_id | required_clause | formula_or_rule | current_status | blocks | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| FRM1068_0_observed_frame | same observed coframe for source variation, force law, clocks, and readout | e_obs = e_source = e_force = e_readout through WEP order | CONDITIONAL_FROM_PRIOR_SPINE | frame-safe tau_WEP | false |
| FRM1068_1_eta_mapping | map residual force to eta_AB | eta_AB = readout[(a_A-a_B), calibration] in MICROSCOPE convention | BOUND_OBSERVABLE_KNOWN_MAP_NOT_DERIVED | direct product scoring | false |
| FRM1068_2_common_mode_separation | common source normalization removed only by universal calibration | relative w_A/w_B cannot be absorbed into measured G or GM | GUARD_ACTIVE | fake local-GR pass | false |
| FRM1068_3_units | dimensionless tau/product convention | P_WEP_relative_source_weight must be dimensionless and comparable to eta_bound | SCHEMA_ONLY | runner validity | false |
| FRM1068_4_direct_variation | direct parent variation option | derive delta a_AB or eta_AB directly from parent action instead of split Delta_w*tau | MISSING_DIRECT_PRODUCT | fallback remains nonclaim | false |
| FRM1068_5_verdict | observed-frame force/readout map | source residual -> a_A-a_B -> eta_AB with units and calibration | FORCE_MAP_NOT_DERIVED | tau_WEP/direct product scoring | false |


## Xhat Normalization
| xhat_id | quantity | required_form | current_status | risk | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| XHN1068_0_shared_parent_norm | Xhat/chi_X normalization | same parent normalization used by clocks, WEP, and R10 or explicitly separated | MISSING_SHARED_NORMALIZATION | tau_WEP cannot be compared to clock/R10 factors | false |
| XHN1068_1_clock_transfer_guard | clock-to-WEP transfer | no clock screening imported into WEP without source/readout map | TRANSFER_BLOCKED | fake tau_WEP via clock branch | false |
| XHN1068_2_R10_transfer_guard | R10-to-WEP transfer | no tau_R10 unity or profile factor imported into WEP | TRANSFER_BLOCKED | profile/unit contamination | false |
| XHN1068_3_direct_product_escape | direct P_WEP product | parent variation gives dimensionless eta_AB product directly | MISSING_DIRECT_PRODUCT | split-factor ambiguity persists | false |
| XHN1068_4_verdict | Xhat normalization pack | shared normalization or direct product | NOT_ACQUIRED | tau_WEP remains a free symbol | false |


## Direct Product Fallback
| fallback_id | route | accepted_evidence | current_status | why_it_matters | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| DPF1068_0_preferred_route | derive P_WEP_relative_source_weight directly | parent variation produces eta_AB residual or theorem-zero with units/source path | MISSING_DIRECT_PARENT_PRODUCT | bypasses arbitrary split into Delta_w and tau_WEP | false |
| DPF1068_1_split_route | P = abs(Delta_w_TiPt * tau_WEP) | both factors numeric/sourced or theorem-zero; no unity shortcut | MISSING_BOTH_FACTORS | finite branch can still be tested if direct product is not derived | false |
| DPF1068_2_theorem_zero_route | P=0 | parent source-scalar/action-scale theorem or WEP projection silence theorem | THEOREM_ZERO_UNSIGNED | would close WEP branch without data-fitting | false |
| DPF1068_3_refusal_rule | reject non-evidence | no tau=1, no Delta_w=0 by taste, no measured-G absorption, no cancellation | REFUSAL_ACTIVE | prevents local-GR/WEP false positives | false |


## WEP Product Candidate
| prediction_id | arena | product_symbol | product_value | product_units | product_source | inputs_present | required_inputs | derivation_status | valid_for_claim | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PRED1068_0_WEP_tau_acquisition_pack_product | MICROSCOPE_WEP | P_WEP_relative_source_weight | MISSING_DIRECT_PRODUCT_OR_DELTA_W_TiPt_TIMES_TAU_WEP | dimensionless | source-intake/mts_residuals/P8_Y5_R10_1068_DIRECT_PRODUCT_FALLBACK.csv | eta_TiPt_bound=2.8e-15;material_pair=TA6V_minus_PtRh10;alpha_smoke_deltaQ=0.001989808886825 | source worldtube;orbit/readout kernel;material response tensor;force map;Xhat normalization;direct product or Delta_w*tau | MISSING_TAU_WEP_ACQUISITION_PACK_INPUTS | false | 1068 is an acquisition pack; the row is intentionally nonclaim until the pack is filled. |


## WEP Bound Import
| bound_id | arena | product_symbol | bound_value | bound_units | bound_source | source_row | bound_type | valid_for_claim | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| BOUND1068_0_WEP_source_charge | MICROSCOPE_WEP | P_WEP_relative_source_weight | 2.8e-15 | dimensionless | source-intake/local_bounds/local_bound_claims.csv | R1_WEP_source_charge | numeric_bound_anchor_nonclaim | true | MICROSCOPE Ti/Pt source-charge proxy bound; bound only, not an MTS prediction. |


## Runner Status
| runner_id | prediction_rows | bound_rows | valid_prediction_rows | valid_bound_rows | comparison_rows | passed_rows | blocked_or_failed_rows | claim_allowed | generated_utc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| APR1068_0_WEP_tau_acquisition_pack | 1 | 1 | 0 | 1 | 1 | 0 | 1 | false | 2026-06-14T10:49:16.545590+00:00 |


## Runner Comparisons
| comparison_id | arena | product_symbol | product_value | bound_value | comparison_status | pass_for_claim | issues |
| --- | --- | --- | --- | --- | --- | --- | --- |
| PRODUCT_COMPARE_NO_VALID_PREDICTIONS |  |  |  |  | not_run | false | no valid MTS alpha product prediction rows |


## Claim Gates
| gate_id | claim | gate_pass | reason | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| CG1068_0_tau_acquisition_pack | tau_WEP acquisition pack is complete | false | source worldtube, orbit/readout, material tensor, force map, and Xhat normalization remain missing | false | false |
| CG1068_1_tau_numeric | tau_WEP is numeric or theorem-zero | false | tau_WEP remains definition-only and tau=1 is explicitly forbidden | false | false |
| CG1068_2_direct_product | direct P_WEP product is derived | false | no parent variation produces eta_AB residual directly yet | false | false |
| CG1068_3_runner_score | WEP product can be scored | false | strict runner has valid_prediction_rows=0 | false | false |
| CG1068_4_local_GR_WEP | local GR/WEP coupling branch is derived | false | finite WEP projection and source-scalar theorem routes remain open | false | false |


## Decisions
| decision_id | decision | because | next_action | valid_for_claim |
| --- | --- | --- | --- | --- |
| DEC1068_0_pack_status | tau_WEP acquisition pack is now explicit but empty of claim-grade data | each required component has a named row and refusal gate | source real MICROSCOPE/source/readout rows or derive direct product | false |
| DEC1068_1_best_route | direct P_WEP derivation remains the cleanest theory route | it avoids arbitrary split-factor priors; if unavailable, tau pack components must be sourced | attempt direct eta_AB product theorem before web/data acquisition | false |
| DEC1068_2_best_next | next target is direct WEP product theorem or first real tau source row | 1068 names the missing pack; 1069 should either derive P_WEP or acquire the first real component | 1069-Y5-R10-direct-WEP-product-theorem-or-first-real-tau-source-row.md | false |


## Source Register
| source_id | relative_path | exists | needle | needle_found | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| SRC1068_0_1067_next | source-intake/mts_residuals/P8_Y5_R10_1067_NEXT_TARGET.csv | true | 1068-Y5-R10-WEP-tau-source-worldtube-orbit-readout | true | false |
| SRC1068_1_1067_tau_functional | source-intake/mts_residuals/P8_Y5_R10_1067_TAU_WEP_FUNCTIONAL_DECOMPOSITION.csv | true | TWF1067_6_verdict | true | false |
| SRC1068_2_1067_acquisition | source-intake/mts_residuals/P8_Y5_R10_1067_TAU_WEP_ACQUISITION_SCHEMA.csv | true | TAQ1067_1_tau_numeric_option | true | false |
| SRC1068_3_1066_tau_contract | source-intake/mts_residuals/P8_Y5_R10_1066_TAU_WEP_PROJECTION_CONTRACT.csv | true | TWP1066_7_verdict | true | false |
| SRC1068_4_1053_tau | source-intake/mts_residuals/P8_Y5_R10_1053_TAU_WEP_R10_PROJECTION_AUDIT.csv | true | TPR1053_1_tau_WEP_definition | true | false |
| SRC1068_5_1061_tau | source-intake/mts_residuals/P8_Y5_R10_1061_BETA_TAU_DERIVATION_ATTEMPT.csv | true | DER1061_2_tau_WEP | true | false |
| SRC1068_6_1061_material | source-intake/mts_residuals/P8_Y5_R10_1061_WEP_MATERIAL_CONVENTION.csv | true | MCON1061_0_test_pair | true | false |
| SRC1068_7_708_wep_map | source-intake/mts_residuals/P8_Y5_R10_708_PPN_GDOT_WEP_MAP.csv | true | PGW708_0_R1_WEP | true | false |
| SRC1068_8_948_bound_runner | source-intake/mts_residuals/P8_Y5_R10_948_WEP_PRODUCT_BOUND_RUNNER.csv | true | WEP948_0_WAS651_0_alpha_Coulomb | true | false |
| SRC1068_9_988_pressure | source-intake/mts_residuals/P8_Y5_R10_988_WEP_ALPHA_PRESSURE_IMPORT.csv | true | WEP988_WAS651_0_alpha_Coulomb | true | false |
| SRC1068_10_1029_tau_req | source-intake/mts_residuals/P8_Y5_R10_1029_TAU_PROJECTION_REQUIREMENTS.csv | true | TAU1029_3_WEP_limit | true | false |
| SRC1068_11_1033_tauR10 | source-intake/mts_residuals/P8_Y5_R10_1033_TAU_R10_DERIVATION_AUDIT.csv | true | TAUR1033_5_universal_cg_limit | true | false |
| SRC1068_12_742_owner | source-intake/mts_residuals/P8_Y5_R10_742_OBSERVED_TAU_OWNER_AUDIT.csv | true | TOA742_4_owner_verdict | true | false |
| SRC1068_13_742_verdict | source-intake/mts_residuals/P8_Y5_R10_742_TAU_PROOF_VERDICT.csv | true | TPV742_3_tau_owner_result | true | false |
| SRC1068_14_1066_delta | source-intake/mts_residuals/P8_Y5_R10_1066_WEP_DELTA_W_PRIOR_WIDTH_SCHEMA.csv | true | DWP1066_4_tau_WEP | true | false |
| SRC1068_15_local_bounds | source-intake/local_bounds/local_bound_claims.csv | true | R1_WEP_source_charge | true | false |
| SRC1068_16_393_common | 393-source-normalized-Newtonian-limit-under-identity-closure.md | true | Only a constant, universal, range-independent | true | false |


## Validation
| check_id | result | detail | generated_utc |
| --- | --- | --- | --- |
| V1068_SUMMARY | pass | 1068 WEP tau source-worldtube/orbit/readout acquisition-pack validation summary | 2026-06-14T10:49:18.418692+00:00 |
| V1068_1_sources_exist_and_needles | pass | every cited source path exists and every source needle was found | 2026-06-14T10:49:16.546697+00:00 |
| V1068_2_pack_components_written | pass | tau_WEP acquisition pack components are written as nonclaim rows | 2026-06-14T10:49:16.546710+00:00 |
| V1068_3_worldtube_missing_explicit | pass | source worldtube remains explicitly missing | 2026-06-14T10:49:16.546715+00:00 |
| V1068_4_orbit_readout_missing_explicit | pass | orbit/readout pack remains explicitly missing | 2026-06-14T10:49:16.546719+00:00 |
| V1068_5_material_response_guarded | pass | material tensor is not claim-ready | 2026-06-14T10:49:16.546723+00:00 |
| V1068_6_force_map_missing | pass | observed-frame force map is not derived | 2026-06-14T10:49:16.546727+00:00 |
| V1068_7_xhat_missing | pass | Xhat normalization pack remains missing | 2026-06-14T10:49:16.546730+00:00 |
| V1068_8_direct_product_fallback_written | pass | direct product fallback is written and missing | 2026-06-14T10:49:16.546734+00:00 |
| V1068_9_prediction_nonclaim | pass | WEP tau acquisition prediction remains nonclaim | 2026-06-14T10:49:16.546738+00:00 |
| V1068_10_bound_anchor_numeric | pass | WEP bound anchor is numeric | 2026-06-14T10:49:16.546743+00:00 |
| V1068_11_runner_refuses_placeholder | pass | strict runner refuses missing tau acquisition product | 2026-06-14T10:49:16.546746+00:00 |
| V1068_12_claim_gates_blocked | pass | all tau/WEP/local-GR claim gates remain blocked | 2026-06-14T10:49:16.546751+00:00 |
| V1068_13_next_target_written | pass | next target selects direct WEP theorem or first real tau source row | 2026-06-14T10:49:16.546755+00:00 |
| V1068_14_generated_files_in_post_checkpoint | pass | all generated files are under post-checkpoint-work | 2026-06-14T10:49:16.552205+00:00 |
| V1068_15_formalization_untouched | pass | formalization-workbench modified-file count since script start is 0 | 2026-06-14T10:49:18.418673+00:00 |


## Next Target
| next_target | objective | include | exclude | valid_for_claim |
| --- | --- | --- | --- | --- |
| 1069-Y5-R10-direct-WEP-product-theorem-or-first-real-tau-source-row.md | attempt a direct parent variation theorem for P_WEP_relative_source_weight; if it fails, acquire the first real tau_WEP source row, starting with MICROSCOPE eta/readout convention or Earth/source worldtube metadata. | direct eta_AB variation theorem, no split-factor shortcut, official MICROSCOPE readout/source row requirements, source URL/DOI provenance, units, valid_for_claim refusal gates | setting tau_WEP to one, setting Delta_w to zero by taste, measured-G absorption of relative weights, cancellation arguments, public WEP/local-GR claim, GitHub action, formalization-workbench edits | false |

