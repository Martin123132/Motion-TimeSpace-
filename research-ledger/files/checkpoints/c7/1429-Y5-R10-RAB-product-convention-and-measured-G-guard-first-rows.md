# 1429 - Product convention and measured-G guard first rows

**Current verdict:** 1429 fills two guard rows in the branch-locked WEP manifest: `eta_product_convention.csv` and `measured_G_guard.csv`. They are rule rows, not evidence rows.

**Main progress:** future finite-WEP scoring now has to respect a declared eta formula status, tau-eff source requirement, orbit-average placeholder, branch-id match, and no relative-signal absorption into measured G.

## Source register
| source_id | source_path | path_exists | anchor | anchor_found | role | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| SRC1429_0_1428_next | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1428_NEXT_TARGET.csv | True | NEXT1428_0_1429 | True | 1428 handoff selecting product convention and measured-G guard. | False | False |
| SRC1429_1_1428_validation | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_BRR545_1428_VALIDATION.csv | True | VAL1428_7_overall | True | 1428 validation summary. | False | False |
| SRC1429_2_1428_branch_row | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1428_BRANCH_CLASSIFIER_ROW.csv | True | MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | True | branch classifier row. | False | False |
| SRC1429_3_branch_id_file | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\microscope\branch_locked_wep\branch_id.csv | True | MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | True | actual branch_id.csv row. | False | False |
| SRC1429_4_1427_manifest_product | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1427_BRANCH_LOCKED_WEP_INPUT_MANIFEST.csv | True | MAN1427_7_product_convention | True | product convention target file. | False | False |
| SRC1429_5_1427_manifest_guard | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1427_BRANCH_LOCKED_WEP_INPUT_MANIFEST.csv | True | MAN1427_8_measured_G_guard | True | measured-G guard target file. | False | False |
| SRC1429_6_1336_product_eta | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1336-Y5-R10-RAB-official-MICROSCOPE-readout-source-manifest-or-common-mode-pivot.md | True | PRODSCHEMA1336_0_eta_formula | True | product eta formula schema. | False | False |
| SRC1429_7_1336_branch_lock | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1336-Y5-R10-RAB-official-MICROSCOPE-readout-source-manifest-or-common-mode-pivot.md | True | PRODSCHEMA1336_6_branch_lock | True | product branch-lock schema. | False | False |

## Product convention row
| same_parent_branch_id | eta_formula | sign_convention | tau_eff_definition | orbit_average_rule | units | source_path | row_status | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | eta_AB = 2(a_A - a_B)/(a_A + a_B); body order and axis sign remain PENDING_OFFICIAL_MICROSCOPE_CONVENTION | PENDING_OFFICIAL_MICROSCOPE_BODY_ORDER_AND_SENSITIVE_AXIS | tau_eff = branch_locked_orbit_average(K_CMSM * R_source * readout_mask); tau_eff=1 is forbidden as a shortcut | PENDING_OFFICIAL_SESSION_MASK_OR_REPRODUCIBLE_CQG_ORBIT_WEIGHTING | dimensionless eta only after C_parent, R_source, R_material, and K_CMSM declare units and conversion factors | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1429-Y5-R10-RAB-product-convention-and-measured-G-guard-first-rows.md | PRODUCT_CONVENTION_GUARD_FIRST_ROW_OFFICIAL_DETAILS_PENDING | False | False |

## Measured-G guard row
| same_parent_branch_id | guard_id | allowed_common_mode | forbidden_relative_absorption | calibration_equation | source_path | row_status | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | MGG1429_0_no_relative_absorption | a universal measured-G/common acceleration calibration may rescale the common denominator shared by both test masses | do not absorb Ti/Pt relative acceleration, active-source residuals, or branch-specific C_parent*R_source*R_material terms into measured G | a_A = a_common(G_meas) + delta_a_A; eta_AB = 2(delta_a_A - delta_a_B)/(2*a_common(G_meas) + delta_a_A + delta_a_B); setting delta_a_A-delta_a_B to zero by redefining G is forbidden | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1429-Y5-R10-RAB-product-convention-and-measured-G-guard-first-rows.md | MEASURED_G_GUARD_FIRST_ROW_FORMAL_RULE_PENDING_EXTERNAL_CALIBRATION_SOURCE | False | False |

## Branch match audit
| audit_id | target_path | file_exists | row_count | branch_values | result | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| BMA1429_0_branch_id | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\microscope\branch_locked_wep\branch_id.csv | True | 1 | MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | PASS | False | False |
| BMA1429_1_product | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\microscope\branch_locked_wep\product\eta_product_convention.csv | True | 1 | MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | PASS | False | False |
| BMA1429_2_measured_G_guard | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\microscope\branch_locked_wep\guards\measured_G_guard.csv | True | 1 | MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | PASS | False | False |

## Runner refusal status
| runner_id | target | input_status | runner_status | score_ready | reason | valid_prediction_row | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| RUN1429_0_guard_rows | branch-locked finite WEP product | BRANCH_PRODUCT_AND_G_GUARDS_READY_OTHER_INPUTS_MISSING | REFUSE_SCORE_UNTIL_C_PARENT_SOURCE_MATERIAL_READOUT_POPULATED | False | product convention and measured-G guard exist, but C_parent, R_source, R_material, K_CMSM, and tau_eff source remain missing | False | False | False |
| RUN1429_1_tau_eff | tau_eff projection | FORMULA_DECLARED_SOURCE_PENDING | REFUSE_TAU_ONE_SHORTCUT | False | tau_eff must be computed from branch-locked readout/source/orbit data, not set to unity | False | False | False |

## Claim gates
| gate_id | claim_component | gate_pass | claim_allowed | reason | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| CG1429_0_product_convention | eta product convention | True | False | guard row exists, but official sign/body/order and tau_eff data are pending | False |
| CG1429_1_measured_G_guard | measured-G non-absorption guard | True | False | formal guard exists, but external calibration/provenance is pending | False |
| CG1429_2_finite_WEP_score | finite Ti/Pt WEP prediction | False | False | C_parent/R_source/R_material/K_CMSM/tau_eff source rows are still missing | False |
| CG1429_3_local_GR | local-GR/Newton reduction | False | False | guard rows prevent shortcuts but do not derive local GR | False |

## Decision ledger
| decision_id | decision | because | effect | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- |
| DEC1429_0_product_first | write product convention before numeric scoring | eta sign, tau_eff, and orbit averaging decide what any WEP product means | future finite-WEP runner must refuse tau=1 and branch-mismatched product rows | False | False |
| DEC1429_1_measured_G_guard | write measured-G guard before source coefficients | otherwise a relative residual can be hidden in a common-mode calibration | future scorepack must keep common-mode and differential signals separate | False | False |
| DEC1429_2_next | hunt the C_parent coupling signature next | the coupling vector is the actual physics bottleneck once branch/product/guard rules exist | 1430 should try to derive/source C_parent or formally keep the finite WEP score blocked | False | False |

## Validation
| check_id | result | detail | generated_utc |
| --- | --- | --- | --- |
| VAL1429_0_sources | PASS | all 1429 cited source paths and anchors resolve | 2026-06-16T05:09:32.891315+00:00 |
| VAL1429_1_branch_match | PASS | branch_id, product convention, and measured-G guard share one branch id | 2026-06-16T05:09:32.891328+00:00 |
| VAL1429_2_tau_shortcut_blocked | PASS | product row refuses tau_eff=1 shortcut | 2026-06-16T05:09:32.891332+00:00 |
| VAL1429_3_measured_G_absorption_blocked | PASS | guard row refuses relative-signal absorption into measured G | 2026-06-16T05:09:32.891334+00:00 |
| VAL1429_4_claim_gates | PASS | all claim/valid/adopted flags remain false | 2026-06-16T05:09:32.891337+00:00 |
| VAL1429_5_csv_parse | PASS | all generated 1429 CSVs parse cleanly | 2026-06-16T05:09:32.891339+00:00 |
| VAL1429_6_formalization_untouched | PASS | formalization modified-file count since start=0 | 2026-06-16T05:09:32.891342+00:00 |
| VAL1429_7_next_target | PASS | 1430 handoff written | 2026-06-16T05:09:32.891344+00:00 |
| VAL1429_8_overall | PASS | 1429 writes branch-locked product and measured-G guard rows while keeping finite WEP and local-GR claims blocked | 2026-06-16T05:09:32.891349+00:00 |

## Next target
| next_id | next_target | script | objective | include | exclude | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| NEXT1429_0_1430 | 1430-Y5-R10-RAB-C-parent-coupling-source-signature-or-refusal-ledger.md | scripts/Y5_R10_RAB_C_parent_coupling_source_signature_or_refusal_ledger.py | try to derive or source the branch-locked C_parent coupling vector; if unsigned, keep the finite WEP runner explicitly blocked. | C_parent components; units/sign basis; parent-status; source path; branch-id match; refusal if coupling remains placeholder | numeric WEP claim; DD-as-MTS ontology; source proxy; measured-G absorption; local-GR claim; formalization edits; GitHub | False | False |
