# 2655 - WEP Source-Worldtube Point-Source Reduction Or Official Readout Data Runner

## Purpose

This checkpoint tries the derivation-first route for the WEP source leg: can the source worldtube be reduced to a calibrated common-mode point source without hiding relative source weights in measured GM? If not, it stages the official readout/data runner contract and keeps every row nonclaim.

## Result

- The exterior common-mode monopole lemma is exact conditionally.
- The full MTS point-source WEP source-worldtube reduction is not parent-derived yet.
- The residual pack is now explicit: relative source weights, source profile, finite-size/orbit terms, readout frame and tau_WEP all remain live.
- The official readout/data runner is staged as a nonclaim contract; valid PDF evidence is provenance-only and bot-check HTML is rejected as data.
- The next target is 2656: either acquire/dry-run official MICROSCOPE readout data, or derive a finite source-worldtube residual bound.

## Source Register

| source_id | role | path | exists | needles_required | missing_needles | status | valid_for_claim | timestamp_utc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SRC2655_2654_doc | immediate WEP input-pack handoff | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\2654-Y5-R2FR-WEP-source-worldtube-material-tensor-acquisition-or-action-owner-lemma.md | True | 4 |  | EXISTS_NEEDLES_CONFIRMED | False | 2026-06-23T03:36:02.373936+00:00 |
| SRC2655_2653_doc | WEP projection row and missing readout/source/tau inputs | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\2653-Y5-R2FR-readout-variation-commutator-zero-or-WEP-projection-row-v1.md | True | 4 |  | EXISTS_NEEDLES_CONFIRMED | False | 2026-06-23T03:36:02.373936+00:00 |
| SRC2655_1225_doc | tau_WEP and official readout acquisition ledger | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1225-Y5-R10-tau-WEP-source-worldtube-readout-projection.md | True | 4 |  | EXISTS_NEEDLES_CONFIRMED | False | 2026-06-23T03:36:02.373936+00:00 |
| SRC2655_1080_doc | MICROSCOPE bound anchor and material tensor precursor | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1080-Y5-R10-finite-WEP-source-vector-and-material-tensor-acquisition-pack.md | True | 2 |  | EXISTS_NEEDLES_CONFIRMED | False | 2026-06-23T03:36:02.373936+00:00 |
| SRC2655_1900_doc | older point-source/readout-runner checkpoint to refine rather than bypass | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1900-Y5-R2FR-wep-source-worldtube-point-source-reduction-or-official-readout-data-runner.md | True | 3 |  | EXISTS_NEEDLES_CONFIRMED | False | 2026-06-23T03:36:02.373936+00:00 |

## Web Source Cache Ledger

| source_id | url | local_path | role | exists | size_bytes | file_magic | expected_magic | cache_status | usable_for | valid_for_claim | timestamp_utc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| WEB2655_MICROSCOPE_final_results_arxiv_2209_15487 | https://arxiv.org/pdf/2209.15487 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\wep-sources\1899\MICROSCOPE_final_results_arxiv_2209_15487.pdf | valid final-result PDF provenance/bound anchor, not a model prediction | True | 460403 | %PDF-1.5 | %PDF | VALID_PDF_PROVENANCE_ONLY | bound/provenance anchor only | False | 2026-06-23T03:36:02.377458+00:00 |
| WEB2655_MICROSCOPE_data_processing_HAL_03564498 | https://hal.science/hal-03564498/document | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\wep-sources\1899\MICROSCOPE_mission_scenario_ground_segment_data_processing_HAL_03564498.botcheck.html | candidate readout/data-processing source; local cache is bot-check HTML | True | 12578 | <!doctyp | %PDF | INVALID_OR_BOTCHECK_CACHE_NONCLAIM | not usable as official arrays/data | False | 2026-06-23T03:36:02.377458+00:00 |
| WEB2655_MICROSCOPE_final_data_analysis_HAL_03854332 | https://hal.science/hal-03854332v1/file/DPHY22007.1642068604.pdf | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\wep-sources\1899\MICROSCOPE_final_data_analysis_HAL_03854332.botcheck.html | candidate final-analysis source; local cache is bot-check HTML | True | 12578 | <!doctyp | %PDF | INVALID_OR_BOTCHECK_CACHE_NONCLAIM | not usable as official arrays/data | False | 2026-06-23T03:36:02.377458+00:00 |

## Point-Source Reduction Attempt

| attempt_id | claim_piece | formal_statement | status | proof_or_obstruction | source_anchor | parent_signed | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PSR2655_0_target | WEP source worldtube point-source/common-mode reduction | The extended Earth/source worldtube may be replaced by one calibrated common-mode monopole plus a bounded residual vector, with relative source weights kept outside measured GM. | TARGET_SHARP | this is the desired Newton/GR-style exterior-source reduction, but only for universal/common-mode source coupling | 2654:WIP2654_1_source_worldtube_profile;1900:PSR1900_0_target | False | False | False |
| PSR2655_1_conditional_monopole_lemma | universal exterior monopole | If the active source current is conserved, compactly supported, pulled back to the observed frame, and species-blind, then the exterior leading source leg is the calibrated total monopole GM/r^2 plus declared multipole corrections. | EXACT_CONDITIONAL_LEMMA | ordinary Gauss/Newton exterior-source reasoning works for the universal leg; it does not erase non-universal source charges | 1900:PSR1900_1_common_monopole_lemma;2654:WIP2654_5_force_map | False | False | False |
| PSR2655_2_relative_weight_guard | measured-G/GM cannot hide relative source weights | GM calibration may absorb only a universal source normalization; Delta_w_source, material/source composition response, projector stress and non-Hilbert residuals must remain explicit product legs. | GUARDRAIL_ACTIVE_NOT_ZERO_PROOF | without a parent common-mode theorem, a WEP pass could be faked by folding relative source weights into measured GM | 1900:PSR1900_2_no_relative_hiding;2654:ACO2654_3_classical_rescale_obstruction | False | False | False |
| PSR2655_3_source_composition_profile | Earth source composition/profile weighting | The WEP source leg needs an orbit/profile-weighted Earth source vector in the same residual basis as Delta_w_eff, or a theorem proving all such finite-source composition legs are common-mode. | SOURCE_COMPOSITION_PROFILE_OBSTRUCTION_ACTIVE | bulk Earth composition is not automatically the same object as the observed-frame worldtube-weighted source vector sampled by MICROSCOPE | 2653:WRQ2653_1_source_worldtube;1225:ACQ1225_2_source_worldtube | False | False | False |
| PSR2655_4_finite_size_orbit_bound | finite-source multipole and orbit/readout residual | Finite Earth multipoles, altitude/orbit windows, attitude, masks and force-readout conventions must either be bounded below the WEP tolerance or retained inside K_WEP and tau_WEP. | FINITE_SOURCE_ERROR_BOUND_MISSING | the source-worldtube shortcut is not valid until the same observed readout frame controls source, force, orbit, clocks and eta normalization | 2653:WEP2653_5_orbit_readout_force;1225:TAU1225_6_verdict | False | False | False |
| PSR2655_5_tau_dependency | tau_WEP is not a unity shortcut | tau_WEP must be derived, sourced, or kept as an explicit nuisance contraction; setting tau_WEP=1 is allowed only after the source, material, readout and coframe maps prove it. | TAU_WEP_PROJECTION_NOT_DERIVED | tau_WEP is exactly where source-worldtube, material tensor and official readout meet, so it cannot be guessed away | 2654:WIP2654_6_tau_wep;2653:WRQ2653_5_tau_wep | False | False | False |
| PSR2655_6_verdict | promote point-source WEP source leg | Current MTS parent primitives prove the WEP source worldtube reduces to a calibrated common-mode point-source leg with all relative residuals absent or bounded. | SOURCE_WORLDTUBE_POINT_SOURCE_REDUCTION_NOT_PARENT_DERIVED | the common monopole lemma is exact conditionally, but source universality, GM-hiding guard, source composition/profile, finite-size/readout error and tau_WEP remain unsigned | PSR2655_0_target through PSR2655_5_tau_dependency | False | False | False |

## Point-Source Residual Ledger

| residual_id | residual | required_for_zero_or_bound | current_status | units | source_anchor | blocks_claim | score_ready | valid_prediction_row | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PSL2655_0_common_monopole | universal/common-mode source normalization | parent-signed common-mode current or calibrated universal GM only | CONDITIONAL_COMMON_MODE_ONLY | m^3 s^-2 or dimensionless after eta normalization | PSR2655_1_conditional_monopole_lemma | True | False | False | False |
| PSL2655_1_relative_source_weights | Delta_w_source or source-charge basis coefficients | parent theorem-zero, finite prior, or acquired source vector in same basis | MISSING_SOURCE_WEIGHT_VALUES_OR_THEOREM_ZERO | dimensionless source-charge weights | PSR2655_2_relative_weight_guard | True | False | False | False |
| PSL2655_2_composition_profile | orbit/profile-weighted Earth composition/source vector | source density/composition profile or theorem reducing it to common mode | MISSING_SOURCE_PROFILE_WEIGHTING | density/profile SI or normalized kernel | PSR2655_3_source_composition_profile | True | False | False | False |
| PSL2655_3_multipole_finite_size | finite-size, J2/multipole and altitude/orbit sampling error | finite-source error theorem or official orbit/readout kernel bound | FINITE_SOURCE_ERROR_BOUND_MISSING | dimensionless eta contribution after readout | PSR2655_4_finite_size_orbit_bound | True | False | False | False |
| PSL2655_4_readout_frame | force-map, coframe, attitude and eta-convention residual | official readout arrays and same-frame force-to-eta map | OFFICIAL_ARRAYS_AND_FORCE_MAP_MISSING | m s^-2 internally; dimensionless eta externally | 2653:WEP2653_5_orbit_readout_force | True | False | False | False |
| PSL2655_5_tau_contract | tau_WEP projection/contraction product | derived/sourced tau_WEP or retained nuisance with declared prior | TAU_WEP_PROJECTION_NOT_DERIVED | dimensionless | PSR2655_5_tau_dependency | True | False | False | False |
| PSL2655_6_acceptance | point-source source-worldtube residual pack | PSL2655_1 through PSL2655_5 zeroed, bounded, or acquired with sources | POINT_SOURCE_RESIDUAL_PACK_NOT_EXECUTABLE_NONCLAIM | dimensionless eta envelope | PSL2655_0_common_monopole through PSL2655_5_tau_contract | True | False | False | False |

## Official Readout Data Targets

| target_id | target | required_form | local_candidate | source_url | current_status | units | source_anchor | blocks_claim | usable_for_claim | valid_prediction_row | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ODT2655_0_bound_pdf | MICROSCOPE final-result bound PDF | source-backed bound/provenance PDF | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\wep-sources\1899\MICROSCOPE_final_results_arxiv_2209_15487.pdf | https://arxiv.org/pdf/2209.15487 | SOURCE_PDF_CACHED_BOUND_ANCHOR_ONLY | dimensionless eta | WEB2655_MICROSCOPE_final_results_arxiv_2209_15487 | True | False | False | False |
| ODT2655_1_processing_pdf | MICROSCOPE data-processing publication | valid PDF or source-backed official data-processing file | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\wep-sources\1899\MICROSCOPE_mission_scenario_ground_segment_data_processing_HAL_03564498.botcheck.html | https://hal.science/hal-03564498/document | LOCAL_CACHE_BOTCHECK_HTML_NOT_USABLE | provenance only | WEB2655_MICROSCOPE_data_processing_HAL_03564498 | True | False | False | False |
| ODT2655_2_final_analysis_pdf | MICROSCOPE final analysis publication | valid PDF or source-backed official data-analysis file | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\wep-sources\1899\MICROSCOPE_final_data_analysis_HAL_03854332.botcheck.html | https://hal.science/hal-03854332v1/file/DPHY22007.1642068604.pdf | LOCAL_CACHE_BOTCHECK_HTML_NOT_USABLE | provenance only | WEB2655_MICROSCOPE_final_data_analysis_HAL_03854332 | True | False | False | False |
| ODT2655_3_official_arrays | official MICROSCOPE CMSM/export readout arrays | time, segment/session id, orbit/attitude, masks, calibration flags, readout axes and uncertainties | MISSING | not_acquired | OFFICIAL_ARRAYS_NOT_IMPORTED | time, frame, m s^-2 or declared readout units | 1225:ACQ1225_0_official_readout_arrays | True | False | False | False |
| ODT2655_4_source_worldtube | Earth/source worldtube and composition profile | observed-frame stress/density/composition profile or theorem-reduced common-mode source | MISSING | not_acquired | MISSING_SOURCE_PROFILE_WEIGHTING | SI density/profile or normalized dimensionless kernel | 2654:WIP2654_1_source_worldtube_profile | True | False | False | False |
| ODT2655_5_material_tensor | TA6V minus PtRh10 material response tensor | full response tensor to Delta_w_eff/source-weight basis | MISSING | not_acquired | MISSING_FULL_MATERIAL_TENSOR | dimensionless sensitivities per residual basis entry | 2654:WIP2654_3_material_tensor;1080:MAT1080_4_full_tensor_upgrade | True | False | False | False |
| ODT2655_6_force_eta_map | force-to-eta readout map and convention | same-frame map from residual source acceleration to eta_TiPt with sign/normalization | MISSING | not_acquired | MISSING_FORCE_READOUT_MAP | m s^-2 internally; dimensionless eta after normalization | 2654:WIP2654_5_force_map | True | False | False | False |
| ODT2655_7_tau_wep | tau_WEP contraction/projection input | derived/sourced tau_WEP or explicit nuisance prior; unity shortcut forbidden | MISSING | not_acquired | TAU_WEP_PROJECTION_NOT_DERIVED | dimensionless | 2654:WIP2654_6_tau_wep;1225:TAU1225_6_verdict | True | False | False | False |

## Official Readout Data Runner Contract

| contract_id | contract_piece | requirement | current_status | blocks_claim | score_ready | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| RDR2655_0_purpose | official readout/data runner role | dry-run only until official arrays, source worldtube, material tensor, force map and tau_WEP exist | RUNNER_CONTRACT_STAGED_NONCLAIM | True | False | False |
| RDR2655_1_inputs | required inputs | CMSM/export arrays, orbit/attitude, masks/calibration, eta convention, source register, material tensor, checksum/manifest | INPUTS_NOT_ACQUIRED | True | False | False |
| RDR2655_2_cache_validation | cache validation | reject bot-check HTML and require PDF/CSV/netCDF/HDF5/official archive magic, source URL, checksum and units | BOTCHECK_HTML_REJECTED | True | False | False |
| RDR2655_3_outputs | future run output layout | runs/<timestamp>/log.txt, status.json, manifest.csv, source_register.csv, readout_schema.csv and completion marker | OUTPUT_LAYOUT_DECLARED_ONLY | True | False | False |
| RDR2655_4_no_claim_policy | claim discipline | data acquisition and bound anchors do not count as a prediction or local-GR/WEP pass | NO_CLAIM_POLICY_ACTIVE | True | False | False |

## Dry-Run Cases

| case_id | point_source_parent_signed | hides_relative_in_gm | source_vector_present | material_tensor_present | official_readout_present | force_map_present | tau_wep_is_unity | bound_anchor_only | uses_surrogate_as_official | botcheck_as_data | uses_cancellation | expected_status | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| DRY2655_0_no_reduction | False | False | False | False | False | False | False | True | False | False | False | REFUSED_POINT_SOURCE_REDUCTION_NOT_DERIVED | False |
| DRY2655_1_gm_hiding | True | True | True | True | True | True | False | False | False | False | False | REFUSED_MEASURED_GM_RELATIVE_WEIGHT_HIDING | False |
| DRY2655_2_source_vector | True | False | False | True | True | True | False | False | False | False | False | REFUSED_SOURCE_VECTOR_MISSING | False |
| DRY2655_3_material_tensor | True | False | True | False | True | True | False | False | False | False | False | REFUSED_MATERIAL_TENSOR_MISSING | False |
| DRY2655_4_surrogate | True | False | True | True | False | True | False | False | True | False | False | REFUSED_SURROGATE_AS_OFFICIAL | False |
| DRY2655_5_botcheck | True | False | True | True | True | True | False | False | False | True | False | REFUSED_BOTCHECK_HTML_AS_OFFICIAL_DATA | False |
| DRY2655_6_official_readout | True | False | True | True | False | True | False | False | False | False | False | REFUSED_OFFICIAL_READOUT_MISSING | False |
| DRY2655_7_force_map | True | False | True | True | True | False | False | False | False | False | False | REFUSED_FORCE_MAP_MISSING | False |
| DRY2655_8_tau_unity | True | False | True | True | True | True | True | False | False | False | False | REFUSED_TAU_WEP_UNITY_SHORTCUT | False |
| DRY2655_9_bound_anchor | True | False | True | True | True | True | False | True | False | False | False | REFUSED_BOUND_ANCHOR_ONLY | False |
| DRY2655_10_cancellation | True | False | True | True | True | True | False | False | False | False | True | REFUSED_CANCELLATION_ONLY | False |
| DRY2655_11_counterfactual | True | False | True | True | True | True | False | False | False | False | False | COUNTERFACTUAL_READY_NOT_CURRENT_CLAIM | False |

## Dry-Run Results

| case_id | computed_status | expected_status | status_match | claim_allowed | valid_for_claim | timestamp_utc |
| --- | --- | --- | --- | --- | --- | --- |
| DRY2655_0_no_reduction | REFUSED_POINT_SOURCE_REDUCTION_NOT_DERIVED | REFUSED_POINT_SOURCE_REDUCTION_NOT_DERIVED | True | False | False | 2026-06-23T03:36:02.373904+00:00 |
| DRY2655_1_gm_hiding | REFUSED_MEASURED_GM_RELATIVE_WEIGHT_HIDING | REFUSED_MEASURED_GM_RELATIVE_WEIGHT_HIDING | True | False | False | 2026-06-23T03:36:02.373904+00:00 |
| DRY2655_2_source_vector | REFUSED_SOURCE_VECTOR_MISSING | REFUSED_SOURCE_VECTOR_MISSING | True | False | False | 2026-06-23T03:36:02.373904+00:00 |
| DRY2655_3_material_tensor | REFUSED_MATERIAL_TENSOR_MISSING | REFUSED_MATERIAL_TENSOR_MISSING | True | False | False | 2026-06-23T03:36:02.373904+00:00 |
| DRY2655_4_surrogate | REFUSED_SURROGATE_AS_OFFICIAL | REFUSED_SURROGATE_AS_OFFICIAL | True | False | False | 2026-06-23T03:36:02.373904+00:00 |
| DRY2655_5_botcheck | REFUSED_BOTCHECK_HTML_AS_OFFICIAL_DATA | REFUSED_BOTCHECK_HTML_AS_OFFICIAL_DATA | True | False | False | 2026-06-23T03:36:02.373904+00:00 |
| DRY2655_6_official_readout | REFUSED_OFFICIAL_READOUT_MISSING | REFUSED_OFFICIAL_READOUT_MISSING | True | False | False | 2026-06-23T03:36:02.373904+00:00 |
| DRY2655_7_force_map | REFUSED_FORCE_MAP_MISSING | REFUSED_FORCE_MAP_MISSING | True | False | False | 2026-06-23T03:36:02.373904+00:00 |
| DRY2655_8_tau_unity | REFUSED_TAU_WEP_UNITY_SHORTCUT | REFUSED_TAU_WEP_UNITY_SHORTCUT | True | False | False | 2026-06-23T03:36:02.373904+00:00 |
| DRY2655_9_bound_anchor | REFUSED_BOUND_ANCHOR_ONLY | REFUSED_BOUND_ANCHOR_ONLY | True | False | False | 2026-06-23T03:36:02.373904+00:00 |
| DRY2655_10_cancellation | REFUSED_CANCELLATION_ONLY | REFUSED_CANCELLATION_ONLY | True | False | False | 2026-06-23T03:36:02.373904+00:00 |
| DRY2655_11_counterfactual | COUNTERFACTUAL_READY_NOT_CURRENT_CLAIM | COUNTERFACTUAL_READY_NOT_CURRENT_CLAIM | True | False | False | 2026-06-23T03:36:02.373904+00:00 |

## Claim Gates

| gate_id | condition | current_status | source_anchor | gate_pass | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| CG2655_0_point_source | source-worldtube point-source/common-mode reduction is parent-signed | FAIL_SOURCE_WORLDTUBE_POINT_SOURCE_REDUCTION_NOT_PARENT_DERIVED | P8_Y5_WEP_WORLDTUBE_2655_POINT_SOURCE_REDUCTION_ATTEMPT.csv:PSR2655_6_verdict | False | False |
| CG2655_1_residual_pack | relative source vector, finite-source residual, readout frame and tau_WEP are zeroed/bounded/acquired | FAIL_POINT_SOURCE_RESIDUAL_PACK_NOT_EXECUTABLE_NONCLAIM | P8_Y5_WEP_WORLDTUBE_2655_POINT_SOURCE_RESIDUAL_LEDGER_NONCLAIM.csv:PSL2655_6_acceptance | False | False |
| CG2655_2_official_data | official readout data targets are acquired and cache-validated | FAIL_OFFICIAL_DATA_TARGETS_NOT_ACQUIRED_NONCLAIM | P8_Y5_WEP_WORLDTUBE_2655_OFFICIAL_READOUT_DATA_TARGETS_NONCLAIM.csv:ODT2655_3_official_arrays | False | False |
| CG2655_3_no_shortcuts | no measured-G hiding, tau=1, surrogate-as-official, bot-check-as-data, bound-only, or cancellation pass | PASS_GUARDS_ENFORCED_BUT_NONCLAIM | P8_Y5_WEP_WORLDTUBE_2655_POINT_SOURCE_DATA_DRYRUN_RESULTS.csv | False | False |
| CG2655_4_verdict | WEP source-worldtube/readout branch can support local-GR/WEP claim | CLAIM_BLOCKED | CG2655_0_point_source through CG2655_3_no_shortcuts | False | False |

## Decision Ledger

| decision_id | decision | reason | status | next_dependency | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| DEC2655_0_point_source | DO_NOT_PROMOTE_POINT_SOURCE_REDUCTION | the exterior common-mode monopole lemma is exact, but the relative source-weight, source-composition, finite-size/readout and tau_WEP clauses are unsigned | POINT_SOURCE_ROUTE_SHARP_BUT_UNSIGNED | derive/bound residual pack or acquire official source/readout/material inputs | False |
| DEC2655_1_data_runner | OFFICIAL_READOUT_DATA_RUNNER_STAGED_NONCLAIM | the valid PDF is a bound/provenance anchor only; HAL candidate caches are bot-check HTML and official arrays are not imported | OFFICIAL_DATA_RUNNER_CONTRACT_STAGED_NONCLAIM | official MICROSCOPE readout arrays or source-backed exact equivalent | False |
| DEC2655_2_next | SELECT_2656_OFFICIAL_READOUT_DRY_RUN_OR_SOURCE_RESIDUAL_BOUND | 2655 narrows the WEP local branch to two honest paths: acquire official readout data or prove a finite source-worldtube residual bound | NEXT_TARGET_SELECTED | 2656 official MICROSCOPE readout data dry-run or source-worldtube residual bound | False |

## Next Target

| branch_id | next_id | status | next_doc | next_script | target | must_include | must_exclude | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Y5_R2FR_WEP_SOURCE_WORLDTUBE_OR_READOUT_RUNNER_2655 | NEXT2655_0_selected | selected | 2656-Y5-R2FR-official-MICROSCOPE-readout-data-dry-run-or-source-worldtube-residual-bound.md | scripts/Y5_R2FR_official_MICROSCOPE_readout_data_dry_run_or_source_worldtube_residual_bound_2656.py | Try the least-scrutinized honest path: either dry-run acquisition of official MICROSCOPE readout arrays, or derive a finite source-worldtube residual bound that makes the point-source branch legitimate. | official data source manifest; cache magic/checksum rules; source-worldtube residual inequality; tau_WEP dependency; no-shortcut refusal cases | GitHub action, formalization-workbench edits, bound-only WEP claim, measured-G hiding, tau_WEP=1 shortcut, bot-check HTML as data | False | False |

## Project Status Snapshot

| status_id | area | summary | risk_level | project_meaning | next_action | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| STAT2655_0_theory | source-worldtube reduction | the common-mode exterior point-source theorem is exact conditionally, but MTS has not yet proved the non-universal residuals vanish or are bounded | DERIVATION_GAP_NARROWED | the local-GR bridge is not dead; it has a precise unsigned clause instead of a vague gap | prove residual bound or keep worldtube/readout kernel explicit | False |
| STAT2655_1_data | MICROSCOPE WEP readout | valid final-result PDF exists as provenance, but official arrays/material/source/tau inputs are still absent | EMPIRICAL_BRANCH_STRUCTURED_NOT_EXECUTABLE | the WEP test branch is prepared but not allowed to score itself from a bound anchor | acquire official arrays or create a dry-run manifest that refuses missing data | False |
| STAT2655_2_project_overview | GR/Newton reduction bridge | WEP/local-GR now has a clean fork: derive a source-worldtube residual theorem or run official-data acquisition without shortcuts | HARD_BUT_ACTIONABLE | this is the right kind of hard: fewer escape hatches, clearer mathematical pressure | 2656 official readout dry-run or finite source-worldtube residual bound | False |

## Branch Copies

| copy_id | path | exists | parseable_csv | purpose | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| queue | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\rab-sector\acquisition-queue\JR2655_OFFICIAL_READOUT_DATA_TARGETS_NONCLAIM.csv | True | True | 2655 WEP source-worldtube/readout nonclaim handoff | False |
| local_bounds | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\local_bounds\WEP_worldtube_residual_2655_NONCLAIM.csv | True | True | 2655 WEP source-worldtube/readout nonclaim handoff | False |
| source_weight | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\source-weight\docs\WEP_SOURCE_WORLDTUBE_POINT_SOURCE_2655_NONCLAIM.csv | True | True | 2655 WEP source-worldtube/readout nonclaim handoff | False |
| microscope | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\microscope\branch_locked_wep\residuals\P8_Y5_2655_OFFICIAL_READOUT_RUNNER_CONTRACT.csv | True | True | 2655 WEP source-worldtube/readout nonclaim handoff | False |
| quarantine | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\microscope\quarantine\2655\P8_Y5_2655_POINT_SOURCE_DATA_DRYRUN_RESULTS.csv | True | True | 2655 WEP source-worldtube/readout nonclaim handoff | False |

## Validation

| timestamp_utc | checkpoint | branch_id | valid_for_claim | claim_allowed | validation_id | status | detail |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2026-06-23T03:36:04.141863+00:00 | 2655 | Y5_R2FR_WEP_SOURCE_WORLDTUBE_OR_READOUT_RUNNER_2655 | False | False | VAL2655_00_sources | PASS | all cited source paths exist and required needles are present |
| 2026-06-23T03:36:04.141863+00:00 | 2655 | Y5_R2FR_WEP_SOURCE_WORLDTUBE_OR_READOUT_RUNNER_2655 | False | False | VAL2655_01_web_cache | PASS | valid PDF is provenance-only; bot-check/invalid caches remain nonclaim |
| 2026-06-23T03:36:04.141863+00:00 | 2655 | Y5_R2FR_WEP_SOURCE_WORLDTUBE_OR_READOUT_RUNNER_2655 | False | False | VAL2655_02_point_source_verdict | PASS | point-source source-worldtube reduction remains unsigned |
| 2026-06-23T03:36:04.141863+00:00 | 2655 | Y5_R2FR_WEP_SOURCE_WORLDTUBE_OR_READOUT_RUNNER_2655 | False | False | VAL2655_03_residual_ledger | PASS | point-source residual ledger is nonclaim/not score-ready |
| 2026-06-23T03:36:04.141863+00:00 | 2655 | Y5_R2FR_WEP_SOURCE_WORLDTUBE_OR_READOUT_RUNNER_2655 | False | False | VAL2655_04_official_targets | PASS | official readout targets remain nonclaim/not acquired; bound PDF not promoted |
| 2026-06-23T03:36:04.141863+00:00 | 2655 | Y5_R2FR_WEP_SOURCE_WORLDTUBE_OR_READOUT_RUNNER_2655 | False | False | VAL2655_05_runner_contract | PASS | runner contract blocks claim until source/readout/material/tau inputs exist |
| 2026-06-23T03:36:04.141863+00:00 | 2655 | Y5_R2FR_WEP_SOURCE_WORLDTUBE_OR_READOUT_RUNNER_2655 | False | False | VAL2655_06_dryrun | PASS | dry-run refuses overpromotion, GM hiding, missing inputs, surrogate, bot-check, tau=1, bound-only and cancellation |
| 2026-06-23T03:36:04.141863+00:00 | 2655 | Y5_R2FR_WEP_SOURCE_WORLDTUBE_OR_READOUT_RUNNER_2655 | False | False | VAL2655_07_claim_gates_false | PASS | claim remains blocked |
| 2026-06-23T03:36:04.141863+00:00 | 2655 | Y5_R2FR_WEP_SOURCE_WORLDTUBE_OR_READOUT_RUNNER_2655 | False | False | VAL2655_08_next_target | PASS | 2656 target is recorded |
| 2026-06-23T03:36:04.141863+00:00 | 2655 | Y5_R2FR_WEP_SOURCE_WORLDTUBE_OR_READOUT_RUNNER_2655 | False | False | VAL2655_09_branch_copies | PASS | branch copies exist and parse |
| 2026-06-23T03:36:04.141863+00:00 | 2655 | Y5_R2FR_WEP_SOURCE_WORLDTUBE_OR_READOUT_RUNNER_2655 | False | False | VAL2655_10_csv_parse | PASS | all generated CSVs parse cleanly |
| 2026-06-23T03:36:04.141863+00:00 | 2655 | Y5_R2FR_WEP_SOURCE_WORLDTUBE_OR_READOUT_RUNNER_2655 | False | False | VAL2655_11_formalization_untouched | PASS | no 2655 outputs are written under formalization-workbench |
| 2026-06-23T03:36:04.141863+00:00 | 2655 | Y5_R2FR_WEP_SOURCE_WORLDTUBE_OR_READOUT_RUNNER_2655 | False | False | VAL2655_12_pycache_absent | PASS | scripts __pycache__ absent |
| 2026-06-23T03:36:04.141863+00:00 | 2655 | Y5_R2FR_WEP_SOURCE_WORLDTUBE_OR_READOUT_RUNNER_2655 | False | False | VAL2655_OVERALL | PASS | 2655 keeps point-source source-worldtube reduction unsigned, stages official readout runner, and selects 2656 residual-bound/data dry-run fork |
