# 1421 - WEP Source-Worldtube Or Parent Point-Source Theorem

**Current verdict:** the calibrated point-source/source-worldtube theorem is not proved. The official MICROSCOPE source proxy form `g(O_sat)` / `T(O_sat)` is source-backed as a readout-kernel object, but this does not by itself remove relative `qbar_source_weight`, source composition, finite-source/multipole, calibration, or numeric-array requirements.

**Discipline move:** the WEP source leg now has source-worldtube metadata rows. They are partial, nonclaim rows: official proxy form and segment metadata are staged, while Earth gravity/source profile, source composition, finite-source error, and numeric gx/gz/Sxx/Sxz arrays remain missing.

**Status:** `Y5_R10_1421_parent_point_source_theorem_not_proved_source_worldtube_metadata_staged_nonclaim`

## Source Register

| source_id | source_path | anchor | role | path_exists | anchor_found | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| SRC1421_0_1420_doc | 1420-Y5-R10-RAB-first-executable-WEP-source-projection-row-or-acquisition-checklist.md | NEXT1420_0_1421 | prior checkpoint selecting WEP source-worldtube or point-source theorem | True | True | False | False |
| SRC1421_1_1420_checklist | source-intake/mts_residuals/P8_Y5_R10_1420_WEP_SOURCE_PROJECTION_ACQUISITION_CHECKLIST.csv | WAC1420_0_source_worldtube_profile | source-worldtube checklist row to close | True | True | False | False |
| SRC1421_2_1420_status | source-intake/mts_residuals/P8_Y5_R10_1420_PMX1419_0_WEP_ROW_STATUS_UPDATE.csv | WRS1420_3_verdict | WEP projection row source acquisition required | True | True | False | False |
| SRC1421_3_1068_worldtube | source-intake/mts_residuals/P8_Y5_R10_1068_SOURCE_WORLDTUBE_REQUIREMENTS.csv | SWT1068_5_verdict | source worldtube not acquired | True | True | False | False |
| SRC1421_4_1069_requirements | 1069-Y5-R10-direct-WEP-product-theorem-or-first-real-tau-source-row.md | REQ1069_3_source_worldtube | prior direct-product WEP source-worldtube requirement | True | True | False | False |
| SRC1421_5_1071_kernel_components | source-intake/mts_residuals/P8_Y5_R10_1071_OFFICIAL_KERNEL_COMPONENTS.csv | KER1071_2_source_gravity_leg | official MICROSCOPE source gravity proxy form | True | True | False | False |
| SRC1421_6_1071_tau_status | source-intake/mts_residuals/P8_Y5_R10_1071_TAU_PROJECTION_STATUS.csv | TAU1071_1_source_worldtube_proxy | source worldtube proxy form acquired but numeric tau not acquired | True | True | False | False |
| SRC1421_7_1071_external | source-intake/mts_residuals/P8_Y5_R10_1071_EXTERNAL_KERNEL_SOURCE_LEDGER.csv | EXT1071_2_applied_acceleration_eq4 | source-backed applied acceleration/source leg form | True | True | False | False |
| SRC1421_8_1071_segments | source-intake/mts_residuals/P8_Y5_R10_1071_SUEP_SEGMENT_TABLE_SOURCE_BACKED.csv | SUEP1071_210 | source-backed SUEP segment metadata | True | True | False | False |
| SRC1421_9_1071_portal | source-intake/mts_residuals/P8_Y5_R10_1071_EXTERNAL_KERNEL_SOURCE_LEDGER.csv | EXT1071_9_onera_data_availability_page | ONERA data portal pointer | True | True | False | False |
| SRC1421_10_1419_matrix | source-intake/mts_residuals/P8_Y5_R10_1419_QBAR_SOURCE_PROJECTION_MATRIX.csv | PMX1419_0_WEP_source_charge | WEP projection matrix row blocked by source leg | True | True | False | False |
| SRC1421_11_bound | source-intake/local_bounds/local_bound_claims.csv | R1_WEP_source_charge | WEP source-charge bound anchor | True | True | False | False |

## Parent Point-Source Theorem Attempt

| theorem_id | claim_piece | formal_statement | test | current_result | missing_for_claim | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| PST1421_0_target | calibrated point-source/source-worldtube theorem | replace extended Earth source leg by calibrated g(O_sat) only if all relative source-weight structure is universal/common-mode or bounded | M_WEP,q can use g(O_sat) without source composition/profile dependence or measured-G absorption of relative weights | TARGET_EXACT | source-current owner, Earth/source composition map, finite-source/multipole error, and common-mode calibration proof | False | False |
| PST1421_1_universal_exterior | ordinary universal mass source exterior reduction | for a universal metric source, the external WEP source leg can be represented by g(O_sat) and T(O_sat) computed from the chosen Earth gravity model | source leg enters only through total calibrated GM and official MICROSCOPE g/T functions | CONDITIONAL_FOR_COMMON_MODE_ONLY | does not apply to relative qbar_source_weight unless source composition residual is zero or bounded | False | False |
| PST1421_2_relative_source_factorization | relative source weight factorizes over Earth | rho_qbar(x)=qbar_source_weight*rho_mass(x) with qbar_source_weight constant over the source support | composition/source-charge profile produces no spatially varying or species-dependent source multipoles | NOT_PROVED | Earth composition/source-charge convention or parent theorem that source leg is universal/common-mode | False | False |
| PST1421_3_common_mode_calibration | measured GM absorbs only universal common mode | G_meas M_source calibration may remove kappa_common, but not relative source weights or composition-dependent source charge | relative qbar_source_weight cannot be hidden by calibration convention | GUARD_ACTIVE_NOT_NUMERIC | explicit calibration equation and residual decomposition in same parent basis | False | False |
| PST1421_4_finite_source_error | finite-size/multipole correction is negligible or bounded | extended-source support, altitude, multipole, and source-composition effects are below declared error or included in M_WEP,q | point-source replacement has a sourced error bound | NOT_ACQUIRED | Earth gravity model/source profile, satellite position, finite-source kernel, error budget | False | False |
| PST1421_5_MICROSCOPE_proxy | official MICROSCOPE source leg proxy | the readout model uses g(O_sat) and gravity-gradient tensor T at satellite centre | use official source-backed proxy form without pretending numeric arrays or qbar composition are filled | FORM_SOURCE_BACKED_NOT_NUMERIC | satellite position/velocity, gravity model, exact arrays, and MTS residual coefficient mapping | False | False |
| PST1421_6_verdict | WEP source leg theorem reduction | M_WEP,q is theorem-reduced to calibrated point-source/proxy g(O_sat) | PST1421_1 through PST1421_5 close without hidden relative source weights | POINT_SOURCE_THEOREM_NOT_PROVED | relative source factorization, calibration split, finite-source error, numeric source proxy arrays | False | False |

## WEP Source-Worldtube Metadata Rows

| metadata_id | input_group | artifact | source_status | source_path | source_anchor | units | frame_support | needed_next | fills_or_blocks | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| WSW1421_0_official_source_proxy_form | source_gravity_proxy | g(O_sat) and gravity-gradient tensor T at satellite centre | SOURCE_BACKED_FORM_ACQUIRED_NOT_NUMERIC | source-intake/mts_residuals/P8_Y5_R10_1071_OFFICIAL_KERNEL_COMPONENTS.csv | KER1071_2_source_gravity_leg | g in m s^-2; T in s^-2 once arrays are reconstructed | satellite centre; MICROSCOPE/instrument frame after pointing transform | numeric gx,gz,Sxx,Sxz arrays or reconstruction inputs | partial form for WAC1420_0 and WAC1420_8; does not fill qbar source composition | False | False |
| WSW1421_1_satellite_position_velocity | source_gravity_proxy | satellite position/velocity and timing products | DATA_PRODUCT_REQUIREMENT_SOURCE_BACKED_NOT_DOWNLOADED | source-intake/mts_residuals/P8_Y5_R10_1071_EXTERNAL_KERNEL_SOURCE_LEDGER.csv | EXT1071_0_data_products | position m or km; velocity m s^-1; timestamps declared by product schema | J2000 and instrument pointing transform | CMSM schema/products or equivalent reconstructed orbit table | blocks numeric g(O_sat) and T(O_sat) | False | False |
| WSW1421_2_Earth_gravity_model | source_worldtube_profile | Earth gravity model or source mass-density profile used to compute g/T | MISSING_MODEL_OR_PROFILE | source-intake/mts_residuals/P8_Y5_R10_1068_SOURCE_WORLDTUBE_REQUIREMENTS.csv | SWT1068_0_source_stress_profile | density kg m^-3 or gravity-potential coefficients with declared normalization | Earth-fixed/source frame and transform to satellite frame | gravity model/source profile source path or theorem reducing to calibrated point source | blocks finite-source and point-source error bound | False | False |
| WSW1421_3_source_composition_charge | source_composition | Earth/source composition or source-charge convention | MISSING_SOURCE_COMPOSITION_MAP | source-intake/mts_residuals/P8_Y5_R10_1068_SOURCE_WORLDTUBE_REQUIREMENTS.csv | SWT1068_1_source_composition | mass fractions or dimensionless source-charge basis | source material labels matching qbar_source_weight basis | composition map or parent theorem that source leg is universal/common-mode | blocks relative source-weight point-source theorem | False | False |
| WSW1421_4_finite_source_support | finite_source_correction | finite-size, altitude, multipole, support-shift error bound | MISSING_ERROR_BOUND | source-intake/mts_residuals/P8_Y5_R10_1068_SOURCE_WORLDTUBE_REQUIREMENTS.csv | SWT1068_3_finite_source_correction | dimensionless fractional error or arena-specific kernel units | satellite altitude/source support convention | kernel/error calculation or conservative bound | blocks point-source by theorem rather than taste | False | False |
| WSW1421_5_segment_window_metadata | segment_window | SUEP segment duration/glitch metadata | SOURCE_BACKED_SEGMENT_METADATA_ONLY | source-intake/mts_residuals/P8_Y5_R10_1071_SUEP_SEGMENT_TABLE_SOURCE_BACKED.csv | SUEP1071_210 | orbits and percent removed samples | segment/window metadata only; exact timestamps/masks still needed | exact timestamps/masks and numeric kernel arrays for one segment | partial context for WEP source-leg pilot | False | False |
| WSW1421_6_data_portal_pointer | data_access | ONERA/CMSM MICROSCOPE data portal pointer | SOURCE_BACKED_POINTER_ACCESS_UNVERIFIED_OR_BLOCKED | source-intake/mts_residuals/P8_Y5_R10_1071_EXTERNAL_KERNEL_SOURCE_LEDGER.csv | EXT1071_9_onera_data_availability_page | not applicable | data acquisition route | schema/file inventory or equivalent local reconstruction inputs | blocks numeric source-leg kernel pilot | False | False |
| WSW1421_7_GM_calibration_guard | calibration_guard | common-mode GM/G calibration separation | GUARD_WRITTEN_NOT_NUMERIC | source-intake/mts_residuals/P8_Y5_R10_1420_WEP_SOURCE_PROJECTION_ACQUISITION_CHECKLIST.csv | WAC1420_2_GM_common_mode_guard | dimensionless calibration convention or SI GM units | relative qbar source weights cannot be absorbed into measured GM | calibration equation in same parent residual basis | blocks fake local-GR/WEP pass | False | False |
| WSW1421_8_verdict | WEP_source_worldtube | M_WEP,q source leg | FORM_PARTIAL_METADATA_STAGED_NUMERIC_SOURCE_LEG_NOT_ACQUIRED | source-intake/mts_residuals/P8_Y5_R10_1421_PARENT_POINT_SOURCE_THEOREM_ATTEMPT.csv | PST1421_6_verdict | dimensionless final M_WEP,q after projection; intermediate g/T SI units | observed/instrument frame after source and pointing transforms | numeric source proxy arrays or parent point-source theorem with error bound | M_WEP,q remains not executable | False | False |

## M_WEP Source-Leg Status Update

| status_id | prior_row | old_status | new_status | filled | reason | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| SLS1421_0_WAC1420_0 | WAC1420_0_source_worldtube_profile | MISSING | OFFICIAL_PROXY_FORM_STAGED_PROFILE_NUMERIC_MISSING | False | official g(O_sat)/T proxy form exists, but source profile/gravity model/numeric arrays are absent | False | False |
| SLS1421_1_WAC1420_1 | WAC1420_1_source_composition | MISSING | SOURCE_COMPOSITION_MAP_MISSING | False | point-source theorem for relative qbar source requires source composition or universal/common-mode theorem | False | False |
| SLS1421_2_WAC1420_2 | WAC1420_2_GM_common_mode_guard | GUARD_WRITTEN_NOT_NUMERIC | GUARD_RETAINED_CALIBRATION_EQUATION_MISSING | False | common measured GM cannot absorb relative source weights | False | False |
| SLS1421_3_MWEPq | M_WEP,q | blocked by WAC1420_0/1/2 | SOURCE_LEG_METADATA_PARTIAL_NOT_EXECUTABLE | False | numeric source leg or theorem reduction is still missing | False | False |
| SLS1421_4_verdict | WEP source leg | SOURCE_ACQUISITION_REQUIRED | SOURCE_WORLD_TUBE_METADATA_STAGED_NUMERIC_KERNEL_REQUIRED | False | next step must acquire/reconstruct g/T arrays or close point-source theorem | False | False |

## Source-Leg Acceptance Gate

| gate_id | gate | opens_if | current_status | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- |
| SLG1421_0_point_source_theorem | parent point-source theorem | PST1421_6 becomes proved with universal/common source and finite-source error bound | CLOSED_THEOREM_NOT_PROVED | False | False |
| SLG1421_1_numeric_source_proxy | numeric g/T source proxy | satellite position/velocity, gravity model, pointing, and exact segment masks produce gx/gz/Sxx/Sxz arrays | CLOSED_NUMERIC_ARRAYS_MISSING | False | False |
| SLG1421_2_source_composition | relative source composition/source-charge map | Earth/source composition map or theorem-zero common-mode source leg is available | CLOSED_COMPOSITION_MAP_MISSING | False | False |
| SLG1421_3_calibration_guard | no measured-G absorption | calibration split proves only common mode is absorbed | GUARD_ACTIVE_EQUATION_MISSING | False | False |
| SLG1421_4_overall | M_WEP,q source leg executability | SLG1421_0 or SLG1421_1+2+3 open | SOURCE_LEG_NOT_EXECUTABLE | False | False |

## Decision Ledger

| decision_id | decision | reason | next_action | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- |
| DEC1421_0_theorem_verdict | do not promote calibrated point-source theorem | official g(O_sat) proxy is common-source form only; relative qbar source factorization/composition and finite-source error are missing | keep point-source route as conditional theorem target | False | False |
| DEC1421_1_metadata_verdict | stage source-worldtube metadata rows as partial nonclaim inputs | 1071 source-backed kernel skeleton supplies source proxy form and segment metadata, not numeric arrays | acquire/reconstruct numeric gx/gz/Sxx/Sxz source-leg arrays for a pilot segment | False | False |
| DEC1421_2_best_next | target MICROSCOPE source-leg data schema or gx/gz/Sxx/Sxz pilot next | numeric source proxy arrays are the first executable component for M_WEP,q if the theorem remains unsigned | try data portal schema/file inventory; if blocked, write reconstruction inputs for one SUEP segment | False | False |

## Claim Gate

| gate_id | claim | allowed | reason | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- |
| CG1421_0_point_source_claim | Earth/source leg is theorem-reduced to a calibrated point source | False | PST1421_6 is POINT_SOURCE_THEOREM_NOT_PROVED | False | False |
| CG1421_1_source_leg_numeric | M_WEP,q source leg is numeric/executable | False | g/T arrays, source profile, composition, and calibration split are missing | False | False |
| CG1421_2_WEP_pass | WEP source projection can be scored or passed | False | WEP_source_worldtube_metadata_and_point_source_theorem_attempt_only_no_WEP_pass_no_tau_numeric_no_point_source_by_taste_no_measured_G_absorption | False | False |
| CG1421_3_shortcuts | point-source by taste, tau=1, measured-G absorption, or qbar=0 convention is allowed | False | all shortcut routes remain forbidden | False | False |

## Next Target

| next_id | target_doc | target_script | task | success_condition | do_not_claim | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| NEXT1421_0_1422 | 1422-Y5-R10-RAB-MICROSCOPE-source-leg-data-schema-or-gxgzS-kernel-pilot.md | scripts/Y5_R10_RAB_MICROSCOPE_source_leg_data_schema_or_gxgzS_kernel_pilot.py | try to acquire the CMSM/MICROSCOPE data schema or reconstruct a pilot gx,gz,Sxx,Sxz source-leg kernel for one SUEP segment from sourced orbit/attitude/gravity inputs; if blocked, write an exact blocker ledger | numeric source-leg arrays are acquired/reconstructed for a pilot segment, or every missing data/schema input is source-ready and claim-blocked | WEP pass; numeric tau_WEP without arrays; guessed masks/phases; measured-G absorption; point-source by taste | False | False |
| NEXT1421_1_parallel_theory | future-relative-source-factorization-theorem.md | future_theory_route | try to prove rho_qbar(x) factorizes as a common-mode source profile from the parent source-current owner | relative source composition is theorem-zero/common-mode, or retained as finite source-composition residual | source composition cancels by assumption | False | False |

## Validation

| check_id | status | detail | generated_utc |
| --- | --- | --- | --- |
| VAL1421_0_sources | PASS | all cited local source paths exist and anchors are present | 2026-06-16T04:12:43.255786+00:00 |
| VAL1421_1_theorem | PASS | point-source theorem attempt fails honestly | 2026-06-16T04:12:43.255786+00:00 |
| VAL1421_2_metadata | PASS | source-worldtube metadata rows exist and remain nonclaim | 2026-06-16T04:12:43.255786+00:00 |
| VAL1421_3_status | PASS | source leg status update keeps M_WEP,q non-executable | 2026-06-16T04:12:43.255786+00:00 |
| VAL1421_4_acceptance | PASS | acceptance gate blocks source-leg executability | 2026-06-16T04:12:43.255786+00:00 |
| VAL1421_5_claim_refusal | PASS | point-source, numeric source leg, WEP pass, and shortcut claims are refused | 2026-06-16T04:12:43.255786+00:00 |
| VAL1421_6_decision | PASS | decision ledger selects source-leg data schema or gx/gz/Sxx/Sxz pilot next | 2026-06-16T04:12:43.255786+00:00 |
| VAL1421_7_next_target | PASS | next target 1422 is staged | 2026-06-16T04:12:43.255786+00:00 |
| VAL1421_8_scope | PASS | outputs are confined to post-checkpoint-work paths | 2026-06-16T04:12:43.255786+00:00 |
| VAL1421_9_overall | PASS | 1421 fails point-source theorem and stages WEP source-worldtube metadata as nonclaim | 2026-06-16T04:12:43.255786+00:00 |
