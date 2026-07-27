# 1419 - Direct Source-Variation Product Or qbar Projection Matrix

**Current verdict:** the direct parent source-variation product is not derived. This keeps us from declaring WEP, Newton/GM, R10, PPN, or local-GR source-side passes. The useful advance is that the fallback is now a real projection matrix `P = M r_source`, not a vague tau split.

**Discipline move:** every matrix row is nonclaim. A row becomes score-ready only when the residual coefficient vector, projection coefficients, units, signs, source paths, and empirical bound/curve are all real. No `tau=1`, no measured-`G` absorption, and no cancellation credit are allowed.

**Status:** `Y5_R10_1419_direct_source_variation_product_not_derived_qbar_projection_matrix_written_nonclaim`

## Source Register

| source_id | source_path | anchor | role | path_exists | anchor_found | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| SRC1419_0_1418_doc | 1418-Y5-R10-RAB-action-scale-current-owner-lock-or-qbar-source-weight-acquisition-ledger.md | NEXT1418_0_1419 | prior checkpoint selecting direct source-variation product or projection matrix | True | True | False | False |
| SRC1419_1_1418_arena | source-intake/mts_residuals/P8_Y5_R10_1418_QBAR_SOURCE_WEIGHT_ARENA_ACQUISITION_LEDGER.csv | QAA1418_6_verdict | qbar_source_weight arena acquisition ledger | True | True | False | False |
| SRC1419_2_1068_direct | source-intake/mts_residuals/P8_Y5_R10_1068_DIRECT_PRODUCT_FALLBACK.csv | DPF1068_0_preferred_route | direct parent product preferred but missing | True | True | False | False |
| SRC1419_3_1068_tau | source-intake/mts_residuals/P8_Y5_R10_1068_TAU_WEP_ACQUISITION_PACK.csv | TAP1068_6_direct_product_fallback | WEP projection ingredients and direct product fallback | True | True | False | False |
| SRC1419_4_1068_worldtube | source-intake/mts_residuals/P8_Y5_R10_1068_SOURCE_WORLDTUBE_REQUIREMENTS.csv | SWT1068_5_verdict | source-worldtube missing requirements | True | True | False | False |
| SRC1419_5_1068_orbit | source-intake/mts_residuals/P8_Y5_R10_1068_MICROSCOPE_ORBIT_READOUT_REQUIREMENTS.csv | ORB1068_5_verdict | MICROSCOPE orbit/readout missing requirements | True | True | False | False |
| SRC1419_6_1068_force | source-intake/mts_residuals/P8_Y5_R10_1068_OBSERVED_FRAME_FORCE_MAP.csv | FRM1068_5_verdict | observed-frame force/readout map not derived | True | True | False | False |
| SRC1419_7_1044_qbar | source-intake/mts_residuals/P8_Y5_R10_1044_QBARXT_COMPONENT_ENVELOPE.csv | QBC1044_3_qbar_source_weight | qbar_source_weight component and no-cancellation envelope | True | True | False | False |
| SRC1419_8_1417_qbar | source-intake/mts_residuals/P8_Y5_R10_1417_QBAR_SOURCE_WEIGHT_ACQUISITION_ROWS.csv | QSA1417_0_qbar_source_weight | qbar_source_weight finite coefficient row | True | True | False | False |
| SRC1419_9_1418_lock | source-intake/mts_residuals/P8_Y5_R10_1418_ACTION_SCALE_CURRENT_OWNER_LOCK_ATTEMPT.csv | ACL1418_6_verdict | action-scale/current-owner lock not proved | True | True | False | False |
| SRC1419_10_WEP_bound | source-intake/local_bounds/local_bound_claims.csv | R1_WEP_source_charge | WEP source-charge empirical anchor | True | True | False | False |
| SRC1419_11_clock_bound | source-intake/local_bounds/local_bound_claims.csv | R2_clock_redshift | clock/readout guard empirical anchor | True | True | False | False |
| SRC1419_12_PPN_gamma | source-intake/local_bounds/local_bound_claims.csv | R3_gamma | PPN gamma empirical anchor | True | True | False | False |
| SRC1419_13_PPN_beta | source-intake/local_bounds/local_bound_claims.csv | R4_beta | PPN beta empirical anchor | True | True | False | False |
| SRC1419_14_Gdot | source-intake/local_bounds/local_bound_claims.csv | R9_Gdot | orbital/Newton Gdot anchor | True | True | False | False |
| SRC1419_15_R10 | source-intake/local_bounds/local_bound_claims.csv | R10_fifth_force | R10 inverse-square symbolic anchor | True | True | False | False |
| SRC1419_16_R11 | source-intake/local_bounds/local_bound_claims.csv | R11_EH_operator_ledger | local-GR operator ledger anchor | True | True | False | False |

## Direct Source-Variation Product Attempt

| product_id | arena | direct_product_statement | required_evidence | current_result | missing_for_claim | fallback_if_missing | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| DSP1419_0_target | all local/source arenas | derive P_arena directly from parent variation/readout instead of choosing tau factors | parent variation of S_parent gives observable residual with units, sign, source path, and readout convention | TARGET_EXACT | parent variation source-current owner and readout maps | projection matrix with explicit missing coefficients | False | False |
| DSP1419_1_WEP_eta | WEP_source_charge | P_WEP := \|eta_AB^MTS[parent variation]\| | delta a_AB or eta_AB from parent action in MICROSCOPE convention | MISSING_DIRECT_PARENT_PRODUCT | source worldtube, material tensor, orbit/readout kernel, eta sign/normalization | PMX1419_0_WEP_source_charge | False | False |
| DSP1419_2_Newton_GM | Newton_GM_orbital | P_GM := relative source-normalization residual after universal GM calibration | parent split of common source normalization vs relative kappa_A/source weight | MISSING_COMMON_RELATIVE_SPLIT | source composition/profile, calibration convention, orbital projection | PMX1419_1_Newton_GM_orbital | False | False |
| DSP1419_3_R10_alpha | R10_fifth_force | alpha_MTS(lambda) := parent short-range source/test residual | range-dependent kernel and alpha(lambda) mapping from parent variation | MISSING_RANGE_KERNEL_AND_QBAR_COEFFICIENT | real bound curve, lambda convention, K_X kernel, source/test material map | PMX1419_2_R10_fifth_force | False | False |
| DSP1419_4_PPN_vector | PPN | P_PPN := (delta gamma, delta beta, alpha_1, alpha_2, alpha_3, xi)_MTS | weak-field metric solution from parent equations with source residuals included | MISSING_WEAK_FIELD_PROJECTION | linearized field equations, source-current map, gauge convention, PPN readout | PMX1419_3_PPN_vector | False | False |
| DSP1419_5_local_GR | local_GR_limit | P_local := norm of source/current residual in EH/Newton reduction | Bianchi-safe local reduction showing residual zero or bounded retained vector | MISSING_EH_SOURCE_REDUCTION | source-current theorem, conservation check, retained residual norm | PMX1419_4_local_GR_vector | False | False |
| DSP1419_6_clock_guard | clock_readout_guard | P_clock := readout-normalization residual, not a WEP source pass | hbar*c/clock normalization from same parent owner or separate finite coefficient | GUARD_ONLY_NOT_SOURCE_PRODUCT | clock/readout transfer owner | PMX1419_5_clock_guard | False | False |
| DSP1419_7_verdict | all local/source arenas | direct source-variation product route | DSP1419_1 through DSP1419_6 supply direct theorem-zero or numeric products | DIRECT_PRODUCT_NOT_DERIVED | all arenas require source-current/readout/projection inputs | write projection matrix rows and keep claims blocked | False | False |

## qbar_source_weight Projection Matrix

| matrix_id | arena | observable | prediction_form | coefficient_requirements | residual_inputs | units | empirical_anchor | acceptance_rule | current_status | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PMX1419_0_WEP_source_charge | WEP_source_charge | eta_AB_source | P_WEP = \|M_WEP,q qbar_source_weight + M_WEP,J current_rescaling + M_WEP,m marker_source + ...\| | M_WEP,q from source worldtube, material tensor, orbit/readout kernel, eta convention | qbar_source_weight;current_rescaling_residual;source_marker_guard | dimensionless | source-intake/local_bounds/local_bound_claims.csv::R1_WEP_source_charge | P_WEP <= 2.8e-15 only if all M entries and residuals are sourced/theorem-zero | MATRIX_ROW_SCHEMA_READY_VALUES_MISSING | False | False |
| PMX1419_1_Newton_GM_orbital | Newton_GM_orbital | Gdot/G or relative source-normalization drift | P_GM = \|M_GM,q(t,r) qbar_source_weight + M_GM,J current_rescaling\| after common-mode GM calibration | source composition/profile, common-vs-relative calibration map, time/range dependence, orbital observable kernel | qbar_source_weight;current_rescaling_residual | yr^-1 or dimensionless after declared projection | source-intake/local_bounds/local_bound_claims.csv::R9_Gdot | do not absorb relative source weights into measured G; compare only after units/projection declared | MATRIX_ROW_SCHEMA_READY_CALIBRATION_MAP_MISSING | False | False |
| PMX1419_2_R10_fifth_force | R10_fifth_force | alpha_MTS(lambda) | alpha_qbar(lambda) = \|M_R10,q(lambda) qbar_source_weight + M_R10,J(lambda) current_rescaling + M_R10,nonH(lambda) qbar_nonH\| | real alpha(lambda) curve, lambda convention, K_X Green/kernel normalization, source/test material map | qbar_source_weight;current_rescaling_residual;qbar_nonH | dimensionless alpha at declared lambda | source-intake/local_bounds/local_bound_claims.csv::R10_fifth_force | alpha_qbar(lambda) <= alpha_bound(lambda) only with real bound curve and no tau=1 shortcut | MATRIX_ROW_SCHEMA_READY_BOUND_CURVE_AND_KERNEL_MISSING | False | False |
| PMX1419_3_PPN_vector | PPN | delta_gamma;delta_beta;alpha1;alpha2;alpha3;xi | v_PPN = M_PPN r_source with r_source=(qbar_source_weight,current_rescaling,qbar_nonH,frame_leak,...) | linearized field equations, gauge convention, source-current map, PPN readout basis | qbar_source_weight;current_rescaling_residual;qbar_nonH;qbar_geom | dimensionless PPN vector | source-intake/local_bounds/local_bound_claims.csv::R3_gamma;R4_beta | componentwise absolute comparison to PPN bounds after matrix coefficients are sourced | MATRIX_ROW_SCHEMA_READY_WEAK_FIELD_MAP_MISSING | False | False |
| PMX1419_4_local_GR_vector | local_GR_limit | retained local source-current residual norm | \|\|r_local\|\| <= \|\|qbar_source_weight\|\| + \|\|current_rescaling\|\| + \|\|qbar_nonH\|\| + conservation/Bianchi residuals | EH/Newton reduction, Bianchi/conservation compatibility, residual norm and operator basis | qbar_source_weight;current_rescaling_residual;qbar_nonH;Bianchi_residual | declared operator/residual norm | source-intake/local_bounds/local_bound_claims.csv::R11_EH_operator_ledger | not an empirical pass; opens local-GR route only if residual vector theorem-zero or bounded | MATRIX_ROW_SCHEMA_READY_LOCAL_REDUCTION_MISSING | False | False |
| PMX1419_5_clock_guard | clock_readout_guard | clock/readout residual | P_clock = \|M_clock qbar_source_weight + M_clock,hbar hbar_readout_residual + ...\| | hbar*c/clock normalization and readout transfer from same parent owner | qbar_source_weight;hbar_readout_residual;clock_coefficient_residual | dimensionless | source-intake/local_bounds/local_bound_claims.csv::R2_clock_redshift | clock agreement cannot screen WEP/source residual; use only as consistency guard | GUARD_ROW_SCHEMA_READY_READOUT_OWNER_MISSING | False | False |
| PMX1419_6_total_abs_guard | cross_arena | no-cancellation source residual envelope | P_arena <= sum_i \|M_arena,i r_i\| with no cancellation credit unless parent-signed | all matrix entries, residual values, units, signs, and source paths | all declared source/qbar residual vector entries | arena-specific | source-intake/mts_residuals/P8_Y5_R10_1044_QBARXT_COMPONENT_ENVELOPE.csv::QBC1044_5_total_abs_guard | score only after every retained term is theorem-zero or source-backed numeric | NO_CANCELLATION_GUARD_ACTIVE_VALUES_MISSING | False | False |
| PMX1419_7_verdict | all local/source arenas | qbar_source_weight projection matrix | P = M r_source | PMX1419_0 through PMX1419_6 all filled or theorem-zero | source residual vector | arena-specific | PMX1419_0 through PMX1419_6 | matrix is source-ready but unscored until coefficients/residuals are filled | PROJECTION_MATRIX_WRITTEN_UNSCORED_NONCLAIM | False | False |

## Source Residual Coefficient Vector

| coeff_id | symbol | definition | current_value | units | source_path | source_anchor | matrix_roles | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SRCV1419_0_qbar_source_weight | qbar_source_weight | relative source-only active gravitational prefactor sensitivity | MISSING_SOURCE_WEIGHT_EXCLUSION_OR_COEFFICIENT | dimensionless | source-intake/mts_residuals/P8_Y5_R10_1417_QBAR_SOURCE_WEIGHT_ACQUISITION_ROWS.csv | QSA1417_0_qbar_source_weight | WEP;Newton_GM;R10;PPN;local_GR;clock_guard | False | False |
| SRCV1419_1_current_rescaling | current_rescaling_residual | source/test current normalization residual from J_A -> c_A J_A or beta_source,A | MISSING_CURRENT_OWNER_OR_COEFFICIENT | dimensionless_or_declared_current_units | source-intake/mts_residuals/P8_Y5_R10_1417_QBAR_SOURCE_WEIGHT_ACQUISITION_ROWS.csv | QSA1417_1_current_rescaling_link | WEP;Newton_GM;R10;PPN;local_GR | False | False |
| SRCV1419_2_qbar_nonH | qbar_nonH | non-Hilbert/boundary/domain/support-shift source residual | MISSING_NONHILBERT_BOUND | dimensionless_or_operator_norm | source-intake/mts_residuals/P8_Y5_R10_1044_QBARXT_COMPONENT_ENVELOPE.csv | QBC1044_4_qbar_nonH | R10;PPN;local_GR | False | False |
| SRCV1419_3_qbar_geom | qbar_geom | observed metric/coframe leakage contribution | MISSING_LIE_V_GHAT | dimensionless_after_normalization | source-intake/mts_residuals/P8_Y5_R10_1044_QBARXT_COMPONENT_ENVELOPE.csv | QBC1044_0_qbar_geom | PPN;local_GR;WEP_direct_geometry | False | False |
| SRCV1419_4_readout_clock | hbar_readout_residual | clock/action-scale/readout normalization residual guard | MISSING_READOUT_OWNER_OR_COEFFICIENT | dimensionless | source-intake/mts_residuals/P8_Y5_R10_1418_ACTION_SCALE_CURRENT_OWNER_LOCK_ATTEMPT.csv | ACL1418_5_readout_transfer | clock_guard;WEP_readout_guard | False | False |
| SRCV1419_5_verdict | r_source | source residual vector for qbar projection matrix | VECTOR_DECLARED_VALUES_MISSING | mixed_requires_matrix_units | source-intake/mts_residuals/P8_Y5_R10_1419_QBAR_SOURCE_PROJECTION_MATRIX.csv | PMX1419_7_verdict | all | False | False |

## Scoring Acceptance Gate

| gate_id | gate | opens_if | current_status | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- |
| SAG1419_0_direct_product | direct product scoring | DSP1419 arena row has theorem-zero or numeric observable residual with units/source/readout path | CLOSED_DIRECT_PRODUCT_NOT_DERIVED | False | False |
| SAG1419_1_matrix_coefficients | projection matrix scoring | PMX1419 matrix coefficients have values/bounds, units, signs, source paths, and arena kernels | CLOSED_MATRIX_VALUES_MISSING | False | False |
| SAG1419_2_residual_vector | source residual vector scoring | SRCV1419 residual coefficients are theorem-zero or source-backed numeric in the same parent basis | CLOSED_RESIDUAL_VALUES_MISSING | False | False |
| SAG1419_3_empirical_bounds | empirical comparison | arena bounds are numeric or curve-backed and matched to the prediction variable | PARTIAL_ANCHORS_EXIST_R10_CURVE_SYMBOLIC | False | False |
| SAG1419_4_refusal_guards | no shortcut guard | no tau=1, no Delta=0 by taste, no measured-G absorption, no cancellation credit | GUARDS_ACTIVE | False | False |
| SAG1419_5_overall | local/source projection matrix claim gate | SAG1419_0 or SAG1419_1+2+3 open and SAG1419_4 remains satisfied | ALL_SOURCE_PROJECTION_CLAIMS_BLOCKED | False | False |

## Decision Ledger

| decision_id | decision | reason | next_action | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- |
| DEC1419_0_direct_product | do not claim direct source-variation product | parent variation/readout products are missing in WEP, Newton, R10, PPN, and local-GR arenas | use projection matrix as the finite branch scaffold | False | False |
| DEC1419_1_projection_matrix | projection matrix is now explicit but unscored | matrix rows name coefficient, unit, source, and arena-kernel requirements without numeric shortcuts | fill the first executable matrix row, prioritizing WEP because its empirical bound anchor and missing projection pack are clearest | False | False |
| DEC1419_2_best_next | target first executable WEP projection row next | WEP has the tightest source-charge anchor and forces source worldtube/material/orbit/readout discipline before other arenas borrow it | derive or build PMX1419_0_WEP_source_charge inputs; if unavailable, write a source acquisition checklist with no pass claim | False | False |

## Claim Gate

| gate_id | claim | allowed | reason | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- |
| CG1419_0_direct_product_claim | direct parent source-variation product is derived | False | DSP1419_7 is DIRECT_PRODUCT_NOT_DERIVED | False | False |
| CG1419_1_projection_score_claim | qbar projection matrix scores against local bounds | False | matrix coefficients and residual vector values are missing | False | False |
| CG1419_2_WEP_R10_claim | WEP or R10 pass | False | WEP projection missing and R10 bound curve/kernel missing | False | False |
| CG1419_3_local_GR_claim | local GR/Newton source-side reduction pass | False | direct_source_variation_product_attempt_and_qbar_projection_matrix_only_no_WEP_pass_no_R10_pass_no_PPN_pass_no_local_GR_pass_no_tau_shortcut | False | False |

## Next Target

| next_id | target_doc | target_script | task | success_condition | do_not_claim | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| NEXT1419_0_1420 | 1420-Y5-R10-RAB-first-executable-WEP-source-projection-row-or-acquisition-checklist.md | scripts/Y5_R10_RAB_first_executable_WEP_source_projection_row_or_acquisition_checklist.py | try to fill PMX1419_0_WEP_source_charge directly from parent variation or sourced WEP projection inputs; if it fails, write the exact source-worldtube/material/orbit/readout acquisition checklist | WEP projection row becomes theorem-zero/numeric-source-backed, or every missing WEP input is acquisition-ready with path/unit/sign requirements and claim gates | WEP pass; tau=1; measured-G absorption; cancellation; qbar_source_weight=0 | False | False |
| NEXT1419_1_parallel_R10 | future-R10-qbar-projection-bound-curve-and-kernel-fill.md | future_source_row_route | after WEP projection structure is clear, fill R10 alpha(lambda) curve and qbar kernel inputs | R10 row has real bound curve, lambda convention, K_X kernel, source/test map, and qbar coefficient status | symbolic alpha(lambda) as scored evidence | False | False |

## Validation

| check_id | status | detail | generated_utc |
| --- | --- | --- | --- |
| VAL1419_0_sources | PASS | all cited local source paths exist and anchors are present | 2026-06-16T03:50:31.151146+00:00 |
| VAL1419_1_direct_product | PASS | direct source-variation product attempt fails honestly | 2026-06-16T03:50:31.151146+00:00 |
| VAL1419_2_projection_matrix | PASS | qbar projection matrix rows exist and remain nonclaim | 2026-06-16T03:50:31.151146+00:00 |
| VAL1419_3_coeff_vector | PASS | source residual coefficient vector exists and remains value-missing/nonclaim | 2026-06-16T03:50:31.151146+00:00 |
| VAL1419_4_scoring_gates | PASS | scoring gates keep all source projection claims blocked | 2026-06-16T03:50:31.151146+00:00 |
| VAL1419_5_claim_refusal | PASS | direct product, projection score, WEP/R10, and local-GR claims are refused | 2026-06-16T03:50:31.151146+00:00 |
| VAL1419_6_decision | PASS | decision ledger selects first executable WEP projection row next | 2026-06-16T03:50:31.151146+00:00 |
| VAL1419_7_next_target | PASS | next target 1420 is staged | 2026-06-16T03:50:31.151146+00:00 |
| VAL1419_8_scope | PASS | outputs are confined to post-checkpoint-work paths | 2026-06-16T03:50:31.151146+00:00 |
| VAL1419_9_overall | PASS | 1419 fails direct product and writes qbar projection matrix as nonclaim | 2026-06-16T03:50:31.151146+00:00 |
