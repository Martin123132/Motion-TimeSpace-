# 1409 - U_a Kernel First Fill Or Official Readout Blocker Ledger

**Status:** `Y5_R10_1409_Ua_kernel_first_fill_blocked_official_readout_ledger_written_nonclaim`

**Current verdict:** `U_a := K_ab(lambda,lab) alpha_source^b` cannot be filled as a claim-grade WEP object in this checkpoint. Prior work gives a source-backed MICROSCOPE measurement/kernel skeleton and nonclaim surrogate previews, but the official or exactly equivalent local arrays needed for `K_ab` are still not present.

**Discipline move:** this checkpoint refuses the tempting shortcut. No `tau_WEP=1`, no surrogate-kernel promotion, no one-pair cancellation, and no product score `P_s := beta_s^a U_a` are allowed. The useful result is a precise acquisition ledger: it names the exact objects needed before U_a can become numeric.

**Claim ceiling:** `Ua_kernel_blocker_ledger_only_no_WEP_pass_no_Ps_products_no_clock_transfer_no_R10_transfer_no_PPN_no_Newton_no_local_GR_pass`

## Source Register

| source_id | source_path | anchor | role | path_exists | anchor_found | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| SRC1409_0_1408_doc | 1408-Y5-R10-RAB-sector-beta-source-fill-queue-and-Ua-kernel-contract.md | NEXT1408_0_1409 | prior checkpoint selecting U_a official kernel/readout fill attempt | True | True | False | False |
| SRC1409_1_1408_ua_contract | source-intake/mts_residuals/P8_Y5_R10_1408_UA_KERNEL_CONTRACT.csv | UAK1408_8_verdict | U_a kernel contract ready but missing source/readout/material values | True | True | False | False |
| SRC1409_2_1225_tau_attempt | source-intake/mts_residuals/P8_Y5_R10_1225_TAU_WEP_PROJECTION_ATTEMPT.csv | TAU1225_6_verdict | tau_WEP projection attempt remains not derived | True | True | False | False |
| SRC1409_3_1225_acquisition | source-intake/mts_residuals/P8_Y5_R10_1225_TAU_WEP_SOURCE_ACQUISITION_TABLE.csv | ACQ1225_0_official_readout_arrays | official arrays, product convention, source worldtube, and orbit-average acquisition rows | True | True | False | False |
| SRC1409_4_1225_formula | source-intake/mts_residuals/P8_Y5_R10_1225_SYMBOLIC_TAU_WEP_FORMULA.csv | FORM1225_0_tau_WEP_functional | symbolic tau_WEP functional needing official source/readout kernel | True | True | False | False |
| SRC1409_5_1225_shortcuts | source-intake/mts_residuals/P8_Y5_R10_1225_TAU_WEP_ANTI_SHORTCUT_GATES.csv | SHORT1225_0_no_tau_unity | anti-shortcut policy forbidding tau_WEP=1 and surrogate promotion | True | True | False | False |
| SRC1409_6_1325_fill | source-intake/mts_residuals/P8_Y5_R10_1325_FIRST_FILL_INPUT_MATRIX.csv | IN1325_8_readout_arrays | first-fill matrix showing official readout arrays not imported | True | True | False | False |
| SRC1409_7_1325_decomposition | source-intake/mts_residuals/P8_Y5_R10_1325_WEP_PRODUCT_DECOMPOSITION.csv | DECOMP1325_3_full_finite_tensor | finite tensor formula-ready but blocked by missing source/kernel/material inputs | True | True | False | False |
| SRC1409_8_1071_kernel_skeleton | source-intake/mts_residuals/P8_Y5_R10_1071_OFFICIAL_KERNEL_COMPONENTS.csv | KER1071_6_verdict | official MICROSCOPE kernel skeleton acquired, numeric tau not acquired | True | True | False | False |
| SRC1409_9_1072_requirements | source-intake/mts_residuals/P8_Y5_R10_1072_RECONSTRUCTION_REQUIREMENTS.csv | REQ1072_5_material_parent_map | exact reconstruction requirements for time grid, ephemeris, attitude, masks, gravity model, and material map | True | True | False | False |
| SRC1409_10_1074_surrogate_status | source-intake/mts_residuals/P8_Y5_R10_1074_SURROGATE_STATUS_LEDGER.csv | STAT1074_3_tau_WEP | surrogate preview exists but official arrays and tau_WEP remain not acquired | True | True | False | False |
| SRC1409_11_1071_validation | source-intake/mts_residuals/P8_Y5_BRR545_1071_VALIDATION.csv | V1071_SUMMARY | prior validation: kernel skeleton and SUEP table acquired; numeric tau/product blocked | True | True | False | False |
| SRC1409_12_1072_validation | source-intake/mts_residuals/P8_Y5_BRR545_1072_VALIDATION.csv | V1072_SUMMARY | prior validation: portal/API route staged and dry-run preview built; official numeric tau/product blocked | True | True | False | False |
| SRC1409_13_1074_validation | source-intake/mts_residuals/P8_Y5_BRR545_1074_VALIDATION.csv | V1074_SUMMARY | prior validation: no local CMSM export found; surrogate preview nonclaim | True | True | False | False |
| SRC1409_14_this_script | scripts/Y5_R10_RAB_Ua_kernel_first_fill_or_official_readout_blocker_ledger.py | STATUS | generator for this checkpoint | True | True | False | False |

## Web / External Source Probe Ledger

| probe_id | source_url | source_label | what_it_supports | what_it_does_not_supply | acquisition_result | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| WEB1409_0_mission_scenario_data_flow | https://arxiv.org/abs/2201.10841 | MICROSCOPE mission scenario, ground segment, and data processing | public description of data flow and processing roles | claim-grade local CMSM time arrays for gx, gz, Sxx, Sxz, masks, calibration flags, and exact observed-frame convention | CONTEXT_ONLY_NO_MACHINE_READABLE_KERNEL_ARRAYS_ACQUIRED | False | False |
| WEB1409_1_final_result_kernel_context | https://elib.dlr.de/193667/2/Touboul_2022_Class._Quantum_Grav._39_204009.pdf | MICROSCOPE final results in Classical and Quantum Gravity 2022 | final eta result, SUEP/SUREF segment counts, measurement model, regression basis, and material context | downloaded segment-level official numeric gx/gz/Sxx/Sxz arrays and masks in this checkpoint | SOURCE_BACKED_FORM_YES_NUMERIC_ARRAYS_NO | False | False |
| WEB1409_2_onera_portal_pointer | https://microscope.onera.fr/fr/publication/microscope-data-are-available | ONERA public pointer to MICROSCOPE data portal | a route to a CMSM data portal exists | local authenticated or machine-readable export inside post-checkpoint-work | PORTAL_POINTER_ONLY_NO_LOCAL_CMSM_EXPORT | False | False |
| WEB1409_3_prior_false_positive_filter | local_search_record | search hits containing unrelated microbial MicroScope resources | filtering discipline for source acquisition | physics mission arrays or WEP readout information | IRRELEVANT_FALSE_POSITIVES_FILTERED | False | False |

## U_a First Fill Attempt

| fill_id | component | attempt | status | evidence | missing | next_action | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UFF1409_0_definition | U_a | use U_a := K_ab(lambda,lab) alpha_source^b as the common WEP source/readout contraction | SYMBOLIC_ONLY | FORM1225_0_tau_WEP_functional; UAK1408_0_definition | numeric K_ab; numeric alpha_source^b; normalization to eta_AB | keep as formula until official readout/source arrays or exact equivalent are available | False | False |
| UFF1409_1_official_readout_arrays | K_ab(lambda,lab) | reuse prior MICROSCOPE official-kernel intake attempts | OFFICIAL_ARRAYS_NOT_ACQUIRED | KER1071_6_verdict; NTS1072_2_tau_WEP; STAT1074_2_official_arrays | time; segment/session id; gx; gz; Sxx; Sxz; masks; calibration flags; attitude/orbit convention | only promote after CMSM export or an exact source-backed reconstruction is present | False | False |
| UFF1409_2_source_worldtube | alpha_source^b | map Earth/source gravity leg into parent source-current basis | MISSING_SOURCE_PROFILE_WEIGHTING | TAU1225_0_source_worldtube; KER1071_2_source_gravity_leg | source stress/current profile in same parent basis as beta_s and U_a | derive source-current owner or source an Earth profile/operator compatible with the parent basis | False | False |
| UFF1409_3_orbit_average | lab/orbit average | match U_a contraction to selected SUEP readout windows | MISSING_ORBIT_AVERAGE_ARRAYS | TAU1225_1_orbit_average; KER1071_4_segment_window; REQ1072_0_exact_time_grid | exact time grid, segment masks, and orbit-average weights | acquire exact CMSM segment files or keep only nonclaim shape smoke previews | False | False |
| UFF1409_4_product_normalization | N_eta/product convention | normalize source response x material response x readout kernel to reported Eotvos eta | NORMALIZATION_NOT_FILLED | TAU1225_5_normalization; ACQ1225_1_product_convention | official product convention and MTS response-to-eta normalization | derive product convention or source it from the experiment/model interface before scoring | False | False |
| UFF1409_5_observed_frame | e_obs/source frame | reuse observed-frame convention from prior spine | CONDITIONAL_ONLY | TAU1225_2_observed_coframe; REQ1072_2_attitude_angular_rates | source-backed observed-frame convention tied to exact attitude/orbit arrays | frame convention can be kept symbolic, but not used for a numeric claim | False | False |
| UFF1409_6_material_tensor | Delta f_s,AB / R_material | contract U_a with Ti/Pt material response | MISSING_FULL_MATERIAL_TENSOR | DECOMP1325_3_full_finite_tensor; FQ1408_3_Delta_f_tensor | full material contrast tensor in the same parent basis, not one alpha/surface smoke row | fill material tensor or keep WEP branch nonclaim | False | False |
| UFF1409_7_public_papers | external source context | check public papers/portal route for claim-grade arrays | CONTEXT_YES_ARRAYS_NO | WEB1409_0_mission_scenario_data_flow; WEB1409_1_final_result_kernel_context; WEB1409_2_onera_portal_pointer | local claim-grade official CMSM export or machine-readable equivalent | record blocker ledger rather than fabricating tau_WEP | False | False |
| UFF1409_8_verdict | U_a first-fill status | decide whether U_a can be filled now | UA_FIRST_FILL_BLOCKED_OFFICIAL_READOUT_LEDGER_WRITTEN | UFF1409_1_official_readout_arrays; UFF1409_2_source_worldtube; UFF1409_4_product_normalization | official readout arrays, source worldtube, orbit-average, product normalization, observed-frame lock, and material tensor | do not score P_s; move parallel derivation pressure to beta_EM/beta_nuc owner/bound route | False | False |

## Official Readout Blocker Ledger

| blocker_id | required_object | required_fields | current_status | why_it_blocks | acceptable_resolution | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ORB1409_0_CMSM_export | official or exactly equivalent CMSM export | time;segment/session;gx;gz;Sxx;Sxz;masks;calibration_flags;attitude/orbit_convention | OFFICIAL_ARRAYS_NOT_ACQUIRED | K_ab cannot be built or normalized without the actual WEP readout/design arrays | download/import official CMSM files or reproduce arrays with source-backed ephemeris, attitude, gravity model, and masks | False | False |
| ORB1409_1_exact_equivalent_proof | exact-equivalent reconstruction certificate | time_grid;orbit_ephemeris;attitude_rates;gravity_model;masks;frequency_convention;validation_against_official_basis | NOT_PROVED | surrogate gx/S previews cannot be promoted to a claim-grade MICROSCOPE kernel | reconstruction reproduces official kernel columns within declared tolerance and provenance | False | False |
| ORB1409_2_product_convention | WEP product normalization | N_eta;sign_convention;readout_axis;material_pair;source_response_basis;eta_mapping | NORMALIZATION_NOT_FILLED | beta_s^a U_a cannot be compared to eta_AB bound | derive or source the map from source/material/readout contraction to reported eta | False | False |
| ORB1409_3_source_worldtube | Earth/source stress-current worldtube | source_profile;parent_basis;lab_frame_projection;lambda_or_domain;uncertainty | MISSING_SOURCE_PROFILE_WEIGHTING | alpha_source^b is not a number or vector in the parent basis | derive source-current owner or import a compatible source model with units and uncertainty | False | False |
| ORB1409_4_orbit_average | orbit/session averaging operator | segment_windows;exact_masks;sample_weights;orbit_average_rule;calibration_flags | MISSING_ORBIT_AVERAGE_ARRAYS | U_a cannot be matched to the reported experiment channel | official segment files or exact reconstruction with masks and sampling | False | False |
| ORB1409_5_material_tensor | full material response tensor | Delta_f_s_AB;sector_basis;uncertainties;basis_map_to_beta_s;TiPt_material_definition | MISSING_FULL_MATERIAL_TENSOR | one pair or one composition scalar cannot certify all WEP sector products | fill tensor rows in the same basis as beta_s and U_a | False | False |
| ORB1409_6_anti_shortcuts | shortcut guard | no_tau_unity;no_surrogate_claim;no_G_absorption;no_one_pair_cancellation | ENFORCED | prevents a fake WEP pass from tau_WEP=1 or surrogate kernels | guard remains active even after numeric fills; claims need all gates clear | False | False |
| ORB1409_7_verdict | U_a blocker verdict | all ORB1409_0 through ORB1409_5 resolved without MISSING or NOT_PROVED statuses | UA_KERNEL_BLOCKED | P_s products and WEP pressure scores would be numerology without these inputs | return with official data or a parent derivation that removes the finite source leg | False | False |

## U_a Template Update

| template_id | quantity | parent_definition | units | dimension_basis | value | uncertainty | sign_convention | source_path | source_anchor | arena_projection | lambda_or_domain | fill_status | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TEMPLATE1409_0_Ua | U_a | K_ab(lambda,lab) alpha_source^b | inverse response-coordinate or arena-normalized source factor | MISSING_PARENT_COORDINATE_BASIS | MISSING_SOURCE_VALUE | MISSING_UNCERTAINTY | MISSING_SIGN_CONVENTION | source-intake/mts_residuals/P8_Y5_R10_1409_OFFICIAL_READOUT_BLOCKER_LEDGER.csv | ORB1409_7_verdict | WEP only until transfer theorem and official readout gate close | WEP_LOCAL_DOMAIN_ONLY_UNTIL_TRANSFER | BLOCKER_LEDGER_RECORDED_NONCLAIM | False | False |
| TEMPLATE1409_1_Ps_products | P_s := beta_s^a U_a | sector response product | dimensionless Eotvos-response coefficient | MISSING_PARENT_COORDINATE_BASIS | MISSING_DEPENDENT_ON_Ua_AND_BETA_s | MISSING_UNCERTAINTY | MISSING_SIGN_CONVENTION | source-intake/mts_residuals/P8_Y5_R10_1409_UA_FIRST_FILL_ATTEMPT.csv | UFF1409_8_verdict | WEP pressure only after all inputs are source-backed | WEP_LOCAL_DOMAIN_ONLY_UNTIL_TRANSFER | DEPENDENT_PRODUCTS_BLOCKED | False | False |
| TEMPLATE1409_2_verdict | U_a template update verdict | source-ready row remains template-only | not_applicable | not_applicable | NO_NUMERIC_PROMOTION | not_applicable | not_applicable | source-intake/mts_residuals/P8_Y5_R10_1409_CLAIM_GATE.csv | GATE1409_6_verdict | no transfer to clocks/R10/PPN/local_GR | not_applicable | TEMPLATE_UPDATE_WRITTEN_NONCLAIM | False | False |

## Claim Gate

| claim_id | claim | status | reason | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- |
| GATE1409_0_Ua | U_a kernel/source contraction is derived or sourced | BLOCKED_NO_CLAIM | official arrays, source worldtube, orbit average, normalization, observed frame, and material tensor remain incomplete | False | False |
| GATE1409_1_Ps_products | P_s := beta_s^a U_a products can be scored | BLOCKED_NO_CLAIM | U_a and required beta/material inputs are not claim-ready | False | False |
| GATE1409_2_WEP_pass | WEP branch passes MICROSCOPE/local WEP | BLOCKED_NO_CLAIM | 1409 is blocker-ledger only and contains no claim-grade tau_WEP or eta product | False | False |
| GATE1409_3_transfer | WEP rows transfer to clocks, R10, PPN, orbital, or local GR arenas | BLOCKED_NO_CLAIM | arena isolation remains active and WEP source kernel is itself unfilled | False | False |
| GATE1409_4_surrogate | surrogate gx/S preview is good enough for a claim | REFUSED | surrogate previews may test schema only; they cannot replace official arrays | False | False |
| GATE1409_5_local_GR | local GR/Newton reduction can be claimed from the WEP branch | BLOCKED_NO_CLAIM | U_a blocker does not close q_loc, lambda_A, EM residuals, source kernel, PPN projection, or parent GR limit | False | False |
| GATE1409_6_verdict | 1409 promotes a WEP/local result | NO_PROMOTION | checkpoint records exact external-data blockers and redirects derivation pressure to beta_EM/beta_nuc while U_a waits | False | False |

## Next Target

| next_id | target_doc | target_script | task | success_condition | do_not_claim | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| NEXT1409_0_1410 | 1410-Y5-R10-RAB-betaEM-or-betaNuc-owner-bound-after-Ua-blocker.md | scripts/Y5_R10_RAB_betaEM_or_betaNuc_owner_bound_after_Ua_blocker.py | because U_a needs official external readout arrays, move the derivation-first pressure to beta_EM/beta_nuc owner-or-bound while keeping the U_a blocker active | derive a zero/lock theorem for beta_EM or beta_nuc, or write source-ready finite bound rows with units, sign, source anchors, and nonclaim gates | WEP pass; P_s products; clock/R10/PPN transfer; Newton limit; local GR; GitHub-ready result | False | False |
| NEXT1409_1_data_route_parallel | future-official-MICROSCOPE-CMSM-import-or-exact-reconstruction.md | future_manual_or_import_route | if official CMSM export becomes available, import or reconstruct gx/gz/Sxx/Sxz/masks/attitude/orbit arrays and rerun the U_a gate | all ORB1409 blockers are resolved with source-backed arrays or an exact-equivalent certificate | surrogate-only WEP score or tau_WEP=1 shortcut | False | False |

## Validation

| check_id | status | detail | timestamp_utc |
| --- | --- | --- | --- |
| VAL1409_0_sources | PASS | all cited local source paths exist and anchors are present | 2026-06-16T02:32:02.535496+00:00 |
| VAL1409_1_web_probe_nonclaim | PASS | web/source probe rows are recorded but remain nonclaim | 2026-06-16T02:32:02.535496+00:00 |
| VAL1409_2_Ua_fill_blocked | PASS | U_a first-fill attempt explicitly blocks promotion and keeps every row nonclaim | 2026-06-16T02:32:02.535496+00:00 |
| VAL1409_3_blocker_ledger | PASS | official readout blocker ledger includes required objects and anti-shortcut guard | 2026-06-16T02:32:02.535496+00:00 |
| VAL1409_4_template_update | PASS | U_a template update records blocker ledger but does not promote a numeric value | 2026-06-16T02:32:02.535496+00:00 |
| VAL1409_5_claim_refusal | PASS | WEP, P_s, transfer, surrogate, and local-GR claims are refused | 2026-06-16T02:32:02.535496+00:00 |
| VAL1409_6_scope | PASS | outputs are confined to post-checkpoint-work paths | 2026-06-16T02:32:02.535496+00:00 |
| VAL1409_7_overall | PASS | 1409 records exact U_a official-readout/source blockers and redirects next work to beta_EM/beta_nuc derivation | 2026-06-16T02:32:02.535496+00:00 |
