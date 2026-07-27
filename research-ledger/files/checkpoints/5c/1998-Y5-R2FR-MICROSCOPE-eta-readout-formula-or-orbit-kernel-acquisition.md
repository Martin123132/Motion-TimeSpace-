# 1998 Y5 R2FR: MICROSCOPE Eta Readout Formula Or Orbit-Kernel Acquisition

Private checkpoint. This folds the 1070/1071 MICROSCOPE readout work into the current WEP/direct-product branch.

Verdict: the official `eta_AB` formula and delta-x readout identification are source-backed, and the official MICROSCOPE kernel skeleton is acquired. This is real plumbing progress, not a WEP prediction.

Still missing: numeric `tau_WEP`. The branch needs machine-readable or reconstructed `gx/gz/Sxx/Sxz` arrays, exact masks/timestamps, source-worldtube values, material tensor, and `Xhat` normalization before any product score.

Next honest move: numeric kernel component or source-worldtube row, not another symbolic shortcut.

No WEP, local-GR, Newton, R10, PPN, clock, orbital, or public claim follows from 1998.

## Source Register

| branch_id | valid_for_claim | claim_allowed | generated_utc | source_id | source_path | needed_for | needles | exists | anchor_found | missing_needles | status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | false | false | 2026-06-20T03:23:25.810727+00:00 | 1997_doc | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1997-Y5-R2FR-direct-WEP-product-theorem-or-first-real-tau-source-row.md | 1998 MICROSCOPE eta readout formula or orbit kernel acquisition | REQ1997_0_readout_formula;NEXT1997_0_primary | True | True |  | EXISTS_NEEDLES_CONFIRMED |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | false | false | 2026-06-20T03:23:25.810727+00:00 | 1997_validation | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_BRR545_1997_VALIDATION.csv | 1998 MICROSCOPE eta readout formula or orbit kernel acquisition | VAL1997_OVERALL;PASS | True | True |  | EXISTS_NEEDLES_CONFIRMED |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | false | false | 2026-06-20T03:23:25.810727+00:00 | 1070_eta_readout | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1070-Y5-R10-MICROSCOPE-eta-readout-formula-or-orbit-kernel-acquisition.md | 1998 MICROSCOPE eta readout formula or orbit kernel acquisition | ETA1070_0_formula;ORK1070_5_verdict;V1070_SUMMARY | True | True |  | EXISTS_NEEDLES_CONFIRMED |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | false | false | 2026-06-20T03:23:25.810727+00:00 | 1070_validation | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_BRR545_1070_VALIDATION.csv | 1998 MICROSCOPE eta readout formula or orbit kernel acquisition | V1070_SUMMARY;pass | True | True |  | EXISTS_NEEDLES_CONFIRMED |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | false | false | 2026-06-20T03:23:25.810727+00:00 | 1071_kernel | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1071-Y5-R10-MICROSCOPE-full-orbit-kernel-or-source-worldtube-row.md | 1998 MICROSCOPE eta readout formula or orbit kernel acquisition | KER1071_6_verdict;TAU1071_3_verdict;NEXT1071_0_1072 | True | True |  | EXISTS_NEEDLES_CONFIRMED |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | false | false | 2026-06-20T03:23:25.810727+00:00 | 1071_validation | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_BRR545_1071_VALIDATION.csv | 1998 MICROSCOPE eta readout formula or orbit kernel acquisition | V1071_SUMMARY;pass | True | True |  | EXISTS_NEEDLES_CONFIRMED |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | false | false | 2026-06-20T03:23:25.810727+00:00 | local_bounds | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\local_bounds\local_bound_claims.csv | 1998 MICROSCOPE eta readout formula or orbit kernel acquisition | R1_WEP_source_charge;2.8e-15 | True | True |  | EXISTS_NEEDLES_CONFIRMED |

## Eta Readout Formula Rows

| branch_id | valid_for_claim | claim_allowed | generated_utc | eta_id | formula_or_item | units | source_basis | status | MTS_impact |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | false | false | 2026-06-20T03:23:25.810727+00:00 | ETA1998_0_formula | eta_AB = 2(a_A-a_B)/(a_A+a_B) | dimensionless | 1070 ETA1070_0_formula; DOI 10.1088/1361-6382/ac84be | SOURCE_BACKED_FORMULA_FILLED | observable normalization acquired; not a tau_WEP prediction |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | false | false | 2026-06-20T03:23:25.810727+00:00 | ETA1998_1_delta_x_identification | eta(Ti,Pt) is identified with measured delta_x in the MICROSCOPE convention | dimensionless | 1070 ETA1070_1_delta_x_identification | SOURCE_BACKED_READOUT_IDENTIFICATION_FILLED | links eta observable to the instrument differential channel |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | false | false | 2026-06-20T03:23:25.810727+00:00 | ETA1998_2_bound_context | Ti/Pt eta upper-bound anchor 2.8e-15 | dimensionless | local_bound_claims.csv:R1_WEP_source_charge; DOI 10.1103/PhysRevLett.129.121102 | SOURCE_BACKED_BOUND_CONTEXT_FILLED | nonclaim comparator only; not an MTS prediction |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | false | false | 2026-06-20T03:23:25.810727+00:00 | ETA1998_3_sign_pair_convention | A/B sign convention is source-backed for eta_AB, but not mapped onto every MTS material-source basis sign | dimensionless | 1070 ETA1070_3_sign_pair_convention | PARTIAL_SIGN_CONTEXT_ONLY | absolute-value bound can be used; signed model comparison still needs material/readout orientation |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | false | false | 2026-06-20T03:23:25.810727+00:00 | ETA1998_4_verdict | eta formula and delta_x readout are acquired; tau_WEP/direct product are not | dimensionless | 1070 V1070_SUMMARY | FORMULA_FILLED_NOT_TAU | data plumbing improved; WEP/local-GR still blocked |

## MICROSCOPE Kernel Skeleton

| branch_id | valid_for_claim | claim_allowed | generated_utc | kernel_id | component | official_form | acquired_level | needed_numeric_inputs |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | false | false | 2026-06-20T03:23:25.810727+00:00 | KER1998_0_sampling_axis | sample/readout axis | 4 Hz acceleration sampling; differential acceleration along sensitive X axis | SOURCE_BACKED_PARTIAL_READOUT_ROW | full map from parent residual to X-axis eta channel |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | false | false | 2026-06-20T03:23:25.810727+00:00 | KER1998_1_segments_orbits | segment/orbit exposure | SUEP Pt/Ti 19 segments, 1362 orbits, 94 days; SUREF Pt/Pt 13 segments, 598 orbits, 41 days | SOURCE_BACKED_PARTIAL_ORBIT_ROW | exact timestamps, masks, attitude/spin phase, and source line-of-sight kernel |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | false | false | 2026-06-20T03:23:25.810727+00:00 | KER1998_2_source_gravity_leg | Earth/source gravity proxy | g(Osat) and gravity-gradient tensor T computed at satellite centre | SOURCE_WORLDTUBE_PROXY_FORM_ACQUIRED_NOT_NUMERIC | satellite position/velocity and gravity model used by MICROSCOPE processing |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | false | false | 2026-06-20T03:23:25.810727+00:00 | KER1998_3_segment_window | segment/window operator | selected continuous segments; even-orbit DFT-aligned windows; glitch masks | SOURCE_BACKED_SEGMENT_TABLE_ACQUIRED | segment masks, removed-sample indices, exact timestamps |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | false | false | 2026-06-20T03:23:25.810727+00:00 | KER1998_4_verdict | tau_WEP kernel verdict | official kernel skeleton acquired, numeric orbit/attitude/source-worldtube kernel not reconstructed | KERNEL_SKELETON_YES_NUMERIC_TAU_NO | data portal products or reproduced gx/gz/Sxx/Sxz arrays |

## Tau Impact Ledger

| branch_id | valid_for_claim | claim_allowed | generated_utc | impact_id | object | what_it_gives | what_is_missing | claim_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | false | false | 2026-06-20T03:23:25.810727+00:00 | TAI1998_0_formula_does_not_define_tau | eta_AB formula | observable normalization and readout comparison convention | source residual to eta projection functional | NOT_TAU |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | false | false | 2026-06-20T03:23:25.810727+00:00 | TAI1998_1_kernel_skeleton_not_numeric | official MICROSCOPE kernel skeleton | fit/readout structure and segment-window shape | numeric gx/gz/Sxx/Sxz arrays, exact masks, attitude/orbit kernel | NOT_NUMERIC_TAU |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | false | false | 2026-06-20T03:23:25.810727+00:00 | TAI1998_2_source_worldtube_proxy | g(Osat) and T source-gravity proxy form | source leg structure | Earth/source model values in MTS tau convention | PROXY_FORM_ONLY |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | false | false | 2026-06-20T03:23:25.810727+00:00 | TAI1998_3_no_unity_shortcut | eta formula plus kernel skeleton | better acquisition target | direct P_WEP product or numeric tau_WEP kernel | UNITY_SHORTCUT_FORBIDDEN |

## Runner Dryrun

| branch_id | valid_for_claim | claim_allowed | generated_utc | run_id | check | result | reason |
| --- | --- | --- | --- | --- | --- | --- | --- |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | false | false | 2026-06-20T03:23:25.810727+00:00 | RUN1998_0_eta_formula | import official eta_AB formula and delta_x readout identification | PASS_NONCLAIM_FORMULA | 1070 source-backed rows are present and validated |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | false | false | 2026-06-20T03:23:25.810727+00:00 | RUN1998_1_kernel_skeleton | import official MICROSCOPE kernel skeleton | PASS_NONCLAIM_SKELETON | 1071 source-backed kernel skeleton and segment table are present and validated |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | false | false | 2026-06-20T03:23:25.810727+00:00 | RUN1998_2_numeric_tau | promote tau_WEP to numeric or theorem-zero | FAIL_NUMERIC_KERNEL_MISSING | kernel skeleton lacks numeric arrays/timestamps/masks/source-worldtube values |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | false | false | 2026-06-20T03:23:25.810727+00:00 | RUN1998_3_product_score | score WEP product | FAIL_VALID_PREDICTION_ROWS_ZERO | direct P_WEP product and tau split product remain missing |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | false | false | 2026-06-20T03:23:25.810727+00:00 | RUN1998_4_verdict | 1998 next-step decision | NEXT_1999_MICROSCOPE_NUMERIC_KERNEL_OR_SOURCE_WORLDTUBE_ROW | formula and skeleton are acquired; numeric tau/source-worldtube is next |

## Claim Gate

| branch_id | valid_for_claim | claim_allowed | generated_utc | gate_id | claim | status | reason |
| --- | --- | --- | --- | --- | --- | --- | --- |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | false | false | 2026-06-20T03:23:25.810727+00:00 | CG1998_0_eta_formula | eta formula/readout convention is acquired | PASS_NONCLAIM_FORMULA | source-backed observable definition, not an MTS prediction |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | false | false | 2026-06-20T03:23:25.810727+00:00 | CG1998_1_kernel_skeleton | official MICROSCOPE kernel skeleton is acquired | PASS_NONCLAIM_SKELETON | kernel form and segment metadata exist, but no numeric tau |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | false | false | 2026-06-20T03:23:25.810727+00:00 | CG1998_2_numeric_tau | tau_WEP is numeric/theorem-zero | FAIL_BLOCKED | full numeric kernel/source-worldtube missing |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | false | false | 2026-06-20T03:23:25.810727+00:00 | CG1998_3_WEP_product | WEP product can be scored | FAIL_BLOCKED | valid_prediction_rows remains zero |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | false | false | 2026-06-20T03:23:25.810727+00:00 | CG1998_4_local_GR | local GR/WEP branch is derived | FAIL_BLOCKED | eta/kernel acquisition is plumbing, not a parent product theorem |

## Decision Ledger

| branch_id | valid_for_claim | claim_allowed | generated_utc | decision_id | decision | because | next_action |
| --- | --- | --- | --- | --- | --- | --- | --- |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | false | false | 2026-06-20T03:23:25.810727+00:00 | DEC1998_0_readout_status | ETA_FORMULA_AND_DELTA_X_READOUT_ARE_SOURCE_BACKED | 1070 acquired the official formula and readout identification | use these rows as readout plumbing only |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | false | false | 2026-06-20T03:23:25.810727+00:00 | DEC1998_1_kernel_status | KERNEL_SKELETON_ACQUIRED_BUT_NUMERIC_TAU_MISSING | 1071 acquired official fit/kernel structure and segments but not gx/gz/Sxx/Sxz arrays or masks | target data portal schema/products or reconstruct a single segment kernel |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | false | false | 2026-06-20T03:23:25.810727+00:00 | DEC1998_2_best_next | NUMERIC_KERNEL_OR_SOURCE_WORLDTUBE_ROW_NEXT | formula and skeleton are no longer the first blockers; numeric tau projection is | 1999-Y5-R2FR-MICROSCOPE-numeric-kernel-or-source-worldtube-row.md |

## Next Target

| branch_id | valid_for_claim | claim_allowed | generated_utc | next_id | selection_status | target_doc | target_script | task | success_condition | do_not |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | false | false | 2026-06-20T03:23:25.810727+00:00 | NEXT1998_0_primary | selected | 1999-Y5-R2FR-MICROSCOPE-numeric-kernel-or-source-worldtube-row.md | scripts/Y5_R2FR_MICROSCOPE_numeric_kernel_or_source_worldtube_row_1999.py | turn the kernel skeleton into a numeric tau_WEP component by acquiring CMSM data schema/products or reconstructing gx,gz,Sxx,Sxz for one SUEP segment; fallback to a source-backed Earth/source-worldtube row | numeric kernel component or source-worldtube row with source path, units, schema/provenance, and refusal gates; no WEP/local-GR scoring yet | do not set tau_WEP=1, guess phase/masks, claim WEP/local-GR, absorb relative weights into measured G, push GitHub, or edit formalization-workbench |

## Validation

| validation_id | status | detail | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- |
| VAL1998_00_sources | PASS | all source paths exist and needles found | false | false |
| VAL1998_01_eta_readout | PASS | eta formula acquired and not promoted to tau | false | false |
| VAL1998_02_kernel_skeleton | PASS | kernel skeleton acquired but numeric tau missing | false | false |
| VAL1998_03_tau_impact | PASS | tau impact ledger blocks shortcuts | false | false |
| VAL1998_04_runner_decision | PASS | runner selects numeric kernel/source-worldtube target | false | false |
| VAL1998_05_claim_gates | PASS | formula/skeleton pass only as nonclaim plumbing | false | false |
| VAL1998_06_next_target | PASS | 1999 numeric kernel/source-worldtube target selected | false | false |
| VAL1998_07_claim_flags_safe | PASS | claim flags all false | false | false |
| VAL1998_08_csv_parse | PASS | all generated CSVs parse with rows | false | false |
| VAL1998_09_pycache_absent | PASS | scripts __pycache__ absent | false | false |
| VAL1998_10_formalization_untouched | PASS | formalization_1998_artifact_count=0 | false | false |
| VAL1998_OVERALL | PASS | 1998 MICROSCOPE eta formula and kernel skeleton acquisition | false | false |
