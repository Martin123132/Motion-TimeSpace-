# 1420 - First Executable WEP Source Projection Row Or Acquisition Checklist

**Current verdict:** `PMX1419_0_WEP_source_charge` is not executable. The MICROSCOPE `R1_WEP_source_charge` bound and Ti/Pt smoke context exist, but the MTS prediction still lacks direct parent eta variation, source-worldtube support, full material tensor, orbit/readout kernel, observed-frame force map, and residual coefficient values.

**Discipline move:** the WEP row now has a concrete acquisition checklist. This is the first clean bridge from the local coupling theorem work into data work: every future WEP claim must satisfy this checklist or derive a direct parent product.

**Status:** `Y5_R10_1420_WEP_projection_row_not_executable_acquisition_checklist_written_nonclaim`

## Source Register

| source_id | source_path | anchor | role | path_exists | anchor_found | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| SRC1420_0_1419_doc | 1419-Y5-R10-RAB-direct-source-variation-product-or-qbar-projection-matrix.md | NEXT1419_0_1420 | prior checkpoint selecting first executable WEP projection row | True | True | False | False |
| SRC1420_1_1419_matrix | source-intake/mts_residuals/P8_Y5_R10_1419_QBAR_SOURCE_PROJECTION_MATRIX.csv | PMX1419_0_WEP_source_charge | WEP projection matrix row to attempt to fill | True | True | False | False |
| SRC1420_2_1419_coeffs | source-intake/mts_residuals/P8_Y5_R10_1419_SOURCE_RESIDUAL_COEFFICIENT_VECTOR.csv | SRCV1419_0_qbar_source_weight | residual coefficient vector with qbar_source_weight missing | True | True | False | False |
| SRC1420_3_1068_tau_pack | source-intake/mts_residuals/P8_Y5_R10_1068_TAU_WEP_ACQUISITION_PACK.csv | TAP1068_6_direct_product_fallback | WEP tau/direct product missing pack | True | True | False | False |
| SRC1420_4_1068_worldtube | source-intake/mts_residuals/P8_Y5_R10_1068_SOURCE_WORLDTUBE_REQUIREMENTS.csv | SWT1068_5_verdict | source-worldtube requirements remain missing | True | True | False | False |
| SRC1420_5_1068_material | source-intake/mts_residuals/P8_Y5_R10_1068_MATERIAL_RESPONSE_REQUIREMENTS.csv | MAT1068_5_verdict | material response tensor requirements remain missing | True | True | False | False |
| SRC1420_6_1068_orbit | source-intake/mts_residuals/P8_Y5_R10_1068_MICROSCOPE_ORBIT_READOUT_REQUIREMENTS.csv | ORB1068_5_verdict | orbit/readout requirements remain missing | True | True | False | False |
| SRC1420_7_1068_force | source-intake/mts_residuals/P8_Y5_R10_1068_OBSERVED_FRAME_FORCE_MAP.csv | FRM1068_5_verdict | observed-frame force/readout map not derived | True | True | False | False |
| SRC1420_8_1061_material_smoke | source-intake/mts_residuals/P8_Y5_R10_1061_WEP_MATERIAL_CONVENTION.csv | MCON1061_2_eta_bound | material smoke context and WEP bound anchor, not full tensor | True | True | False | False |
| SRC1420_9_bound | source-intake/local_bounds/local_bound_claims.csv | R1_WEP_source_charge | MICROSCOPE source-charge proxy bound anchor | True | True | False | False |
| SRC1420_10_1068_refusal | source-intake/mts_residuals/P8_Y5_R10_1068_DIRECT_PRODUCT_FALLBACK.csv | DPF1068_3_refusal_rule | no tau=1/no measured-G absorption/no cancellation refusal rule | True | True | False | False |

## WEP Projection Row Fill Attempt

| attempt_id | piece | needed_for_executable_row | available_evidence | missing_evidence | current_status | result | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| WPF1420_0_target | PMX1419_0_WEP_source_charge | P_WEP = \|M_WEP,q qbar_source_weight + M_WEP,J current_rescaling + M_WEP,m marker_source + ...\| | matrix schema and MICROSCOPE R1 bound anchor exist | all numeric/theorem-zero residuals and all WEP projection coefficients | TARGET_EXACT_NOT_EXECUTABLE | continue acquisition | False | False |
| WPF1420_1_direct_parent_eta | direct eta_AB parent variation | delta a_AB or eta_AB residual directly from S_parent in MICROSCOPE convention | 1068 names direct route as preferred | no parent variation produces eta_AB residual with units/source/readout path | MISSING_DIRECT_PARENT_PRODUCT | cannot bypass projection matrix | False | False |
| WPF1420_2_residual_vector | r_source values | qbar_source_weight/current_rescaling/source_marker_guard theorem-zero or numeric | SRCV1419 vector declared | qbar_source_weight and current_rescaling are MISSING_*; marker guard not coefficient-filled | RESIDUAL_VALUES_MISSING | cannot score matrix product | False | False |
| WPF1420_3_source_worldtube | M_WEP source leg | Earth/source stress profile, source composition, GM calibration guard, finite-source correction, frame units | 1068 source-worldtube requirement rows | T_source^Earth(x), composition map, finite-source kernel, units | SOURCE_WORLDTUBE_NOT_ACQUIRED | M_WEP,q cannot be numeric | False | False |
| WPF1420_4_material_tensor | M_WEP material/test-body leg | full Ti/Pt relative-source material response tensor or parent theorem reducing it | Ti/Pt pair and alpha/Coulomb smoke delta exist | full material tensor and source-weight response convention | MATERIAL_TENSOR_NOT_ACQUIRED | smoke values cannot be promoted | False | False |
| WPF1420_5_orbit_readout | M_WEP orbit/readout kernel | orbit ephemeris/average, attitude axis, eta convention, environmental model, average kernel | MICROSCOPE bound anchor and requirement rows | orbit/readout kernel and parent-mapped eta convention | ORBIT_READOUT_NOT_ACQUIRED | tau/projection cannot be assigned | False | False |
| WPF1420_6_force_map | observed-frame force/readout map | source residual -> a_A-a_B -> eta_AB in same observed frame with calibration | conditional same-frame rule and common-mode guard | force map not derived; common-mode/relative separation not quantified | FORCE_MAP_NOT_DERIVED | no executable eta prediction | False | False |
| WPF1420_7_verdict | first executable WEP source projection row | WPF1420_1 through WPF1420_6 all theorem-zero, numeric, or source-backed | bound anchor and schema | direct parent product, residual vector values, source worldtube, full material tensor, orbit/readout, force map | WEP_PROJECTION_ROW_NOT_EXECUTABLE | write acquisition checklist and keep WEP claims blocked | False | False |

## WEP Source Projection Acquisition Checklist

| check_id | input_group | required_artifact | accepted_form | units_required | sign_or_frame_required | current_status | blocks_matrix_entry | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| WAC1420_0_source_worldtube_profile | source_worldtube | Earth/source stress or mass-density profile in observed local frame | sourced table/profile; or parent theorem reducing Earth to calibrated point source with error bound | SI density/profile units or dimensionless normalized kernel with declared conversion | observed coframe/source frame and altitude/support convention | MISSING | M_WEP,q | False | False |
| WAC1420_1_source_composition | source_worldtube | Earth/source composition or source-charge convention | composition/source species map; or theorem that source leg is universal/common-mode | mass fractions or declared source-charge basis | species/source label convention matching qbar_source_weight basis | MISSING | M_WEP,q and measured-G guard | False | False |
| WAC1420_2_GM_common_mode_guard | calibration_guard | measured GM/G calibration rule separating common mode from relative source weight | explicit calibration equation proving only common universal factors are absorbed | dimensionless calibration factor or SI GM convention | relative weights cannot be hidden by sign or calibration choice | GUARD_WRITTEN_NOT_NUMERIC | fake WEP/local-GR pass | False | False |
| WAC1420_3_material_tensor | material_response | full Ti/Pt relative-source material response tensor | source-backed MICROSCOPE/material model; or parent theorem reducing response to declared Delta_w basis | dimensionless sensitivities per source-residual basis entry | TA6V-minus-PtRh10 sign convention or absolute-value envelope | MISSING_FULL_TENSOR | M_WEP,q;M_WEP,J;M_WEP,m | False | False |
| WAC1420_4_smoke_material_context | material_response | Ti/Pt smoke convention and alpha/Coulomb delta | already present as nonclaim context only | dimensionless | absolute smoke delta; not full source-weight tensor | AVAILABLE_CONTEXT_NOT_CLAIM_INPUT | none alone; cannot replace WAC1420_3 | False | False |
| WAC1420_5_orbit_ephemeris | orbit_readout | MICROSCOPE orbit/altitude/time sampling or official averaged equivalent | official/equivalent orbit table or conservative averaged kernel with source path | time, radius/altitude, frame units | Earth-centered frame and instrument time convention | MISSING | M_WEP,* orbit averaging | False | False |
| WAC1420_6_attitude_axis_kernel | orbit_readout | instrument sensitive axis, attitude convention, and average kernel | official readout kernel; or theorem scalar residual is orientation independent with error bound | dimensionless projection kernel | axis sign and eta_AB sign convention | MISSING | M_WEP,* readout projection | False | False |
| WAC1420_7_eta_convention | observable_readout | eta_AB formula, sign, normalization, and absolute-value scoring convention | parent-mapped eta readout formula tied to MICROSCOPE bound anchor | dimensionless | TA6V/PtRh10 ordering and absolute claim convention | BOUND_ANCHOR_ONLY_FORMULA_NOT_PARENT_MAPPED | comparison to R1 bound | False | False |
| WAC1420_8_force_map | observed_force_map | source residual to acceleration difference map in observed frame | derived force/readout equation with units and common-mode calibration guard | m s^-2 internally and dimensionless eta after normalization | same observed coframe for source, force, clocks, and readout | MISSING_FORCE_READOUT_MAP | all M_WEP entries | False | False |
| WAC1420_9_residual_coefficients | source_residual_vector | qbar_source_weight/current_rescaling/source_marker residual values or theorem-zero certificates | parent theorem-zero; or source-backed coefficient values with uncertainties, units, signs, and basis | dimensionless or declared basis units | same parent basis as projection matrix | MISSING_RESIDUAL_VALUES | r_source vector | False | False |
| WAC1420_10_executability_verdict | WEP_projection_row | all checklist rows filled or theorem-reduced | PMX1419_0 row can compute P_WEP with no shortcuts | dimensionless final P_WEP | absolute/no-cancellation envelope unless signed model permits otherwise | NOT_EXECUTABLE | WEP source projection scoring | False | False |

## PMX1419_0 Row Status Update

| status_id | matrix_id | old_status | new_status | executable | reason | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| WRS1420_0_PMX1419_0_status | PMX1419_0_WEP_source_charge | MATRIX_ROW_SCHEMA_READY_VALUES_MISSING | ACQUISITION_CHECKLIST_WRITTEN_NOT_EXECUTABLE | False | direct product, residual values, source worldtube, full material tensor, orbit/readout kernel, eta/force map are missing | False | False |
| WRS1420_1_bound_status | R1_WEP_source_charge | numeric bound anchor exists | BOUND_AVAILABLE_NOT_PREDICTION | False | 2.8e-15 bound cannot score MTS without P_WEP prediction | False | False |
| WRS1420_2_smoke_context_status | MCON1061 material smoke | SMOKE_CONTEXT_AVAILABLE | CONTEXT_ONLY_NOT_FULL_TENSOR | False | alpha/Coulomb smoke value is not the full relative source-weight material tensor | False | False |
| WRS1420_3_verdict | WEP source projection row | schema ready | SOURCE_ACQUISITION_REQUIRED | False | acquire WAC1420 checklist or derive direct eta_AB parent product | False | False |

## WEP Executability Acceptance Gate

| gate_id | gate | opens_if | current_status | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- |
| WAG1420_0_direct_product | direct parent eta_AB product | parent variation produces eta_AB residual/theorem-zero with units/source/readout path | CLOSED_MISSING_DIRECT_PRODUCT | False | False |
| WAG1420_1_projection_inputs | projection coefficient completeness | source worldtube, material tensor, orbit/readout, eta convention, force map all sourced or theorem-reduced | CLOSED_CHECKLIST_INCOMPLETE | False | False |
| WAG1420_2_residual_values | source residual vector completeness | qbar_source_weight/current_rescaling/marker residuals are theorem-zero or source-backed numeric | CLOSED_RESIDUAL_VALUES_MISSING | False | False |
| WAG1420_3_bound_comparison | R1 WEP bound comparison | dimensionless P_WEP computed and comparable to 2.8e-15 | CLOSED_PREDICTION_MISSING | False | False |
| WAG1420_4_refusal_guards | shortcut refusal | no tau=1, no measured-G absorption, no cancellation, no qbar=0 by taste | GUARDS_ACTIVE | False | False |
| WAG1420_5_overall | WEP row executability | WAG1420_0 or WAG1420_1+2+3 open while WAG1420_4 remains satisfied | WEP_ROW_NOT_EXECUTABLE | False | False |

## Decision Ledger

| decision_id | decision | reason | next_action | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- |
| DEC1420_0_fill_verdict | do not mark WEP row executable | bound and smoke context exist, but prediction coefficients/projections do not | use WAC1420 checklist as source-acquisition contract | False | False |
| DEC1420_1_best_first_input | source-worldtube/readout split should be acquired before numeric scoring | without source support and eta/readout convention, material or qbar numbers cannot be projected into the bound | try parent point-source/source-worldtube theorem or acquire MICROSCOPE/Earth source metadata | False | False |
| DEC1420_2_best_next | target WEP source-worldtube or parent point-source theorem next | this is the first missing projection coefficient for M_WEP,q and blocks every WEP finite comparison | derive calibrated point-source theorem; if it fails, build source-backed Earth/MICROSCOPE worldtube metadata rows | False | False |

## Claim Gate

| gate_id | claim | allowed | reason | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- |
| CG1420_0_WEP_row_executable | PMX1419_0 WEP source projection row is executable | False | WPF1420_7 verdict is WEP_PROJECTION_ROW_NOT_EXECUTABLE | False | False |
| CG1420_1_WEP_pass | MTS passes MICROSCOPE/WEP source-charge bound | False | no dimensionless P_WEP prediction exists | False | False |
| CG1420_2_tau_numeric | tau_WEP or M_WEP projection coefficient is numeric/theorem-zero | False | source worldtube, material tensor, orbit/readout, and force map are missing | False | False |
| CG1420_3_shortcuts | tau=1, measured-G absorption, cancellation, or qbar=0 convention may be used | False | WEP_source_projection_fill_attempt_and_acquisition_checklist_only_no_WEP_pass_no_tau_shortcut_no_measured_G_absorption_no_qbar_zero | False | False |

## Next Target

| next_id | target_doc | target_script | task | success_condition | do_not_claim | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| NEXT1420_0_1421 | 1421-Y5-R10-RAB-WEP-source-worldtube-or-parent-point-source-theorem.md | scripts/Y5_R10_RAB_WEP_source_worldtube_or_parent_point_source_theorem.py | try to derive a calibrated point-source/source-worldtube theorem for the WEP source leg; if it fails, write source-backed Earth/MICROSCOPE worldtube metadata rows with units, frame, support, and no-claim gates | M_WEP source leg is theorem-reduced or has acquisition-ready source metadata rows | WEP pass; tau=1; measured-G absorption; point-source by taste; qbar_source_weight=0 | False | False |
| NEXT1420_1_parallel_material | future-WEP-material-tensor-source-acquisition.md | future_source_row_route | after source-worldtube convention is set, acquire or derive the Ti/Pt material tensor in the same basis | material tensor rows have source path, units, sign convention, alloy convention, and projection role | alpha/Coulomb smoke delta as full tensor | False | False |

## Validation

| check_id | status | detail | generated_utc |
| --- | --- | --- | --- |
| VAL1420_0_sources | PASS | all cited local source paths exist and anchors are present | 2026-06-16T04:02:03.839368+00:00 |
| VAL1420_1_fill_attempt | PASS | WEP projection fill attempt fails honestly | 2026-06-16T04:02:03.839368+00:00 |
| VAL1420_2_checklist | PASS | acquisition checklist contains all required WEP input groups and remains nonclaim | 2026-06-16T04:02:03.839368+00:00 |
| VAL1420_3_row_status | PASS | PMX1419_0 status update keeps row non-executable | 2026-06-16T04:02:03.839368+00:00 |
| VAL1420_4_acceptance | PASS | acceptance gate blocks WEP executability | 2026-06-16T04:02:03.839368+00:00 |
| VAL1420_5_claim_refusal | PASS | WEP row executable, WEP pass, tau numeric, and shortcut claims are refused | 2026-06-16T04:02:03.839368+00:00 |
| VAL1420_6_decision | PASS | decision ledger selects source-worldtube/point-source theorem next | 2026-06-16T04:02:03.839368+00:00 |
| VAL1420_7_next_target | PASS | next target 1421 is staged | 2026-06-16T04:02:03.839368+00:00 |
| VAL1420_8_scope | PASS | outputs are confined to post-checkpoint-work paths | 2026-06-16T04:02:03.839368+00:00 |
| VAL1420_9_overall | PASS | 1420 fails WEP row executability and writes acquisition checklist as nonclaim | 2026-06-16T04:02:03.839368+00:00 |
