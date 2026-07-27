# 1704 - MICROSCOPE Parser Shell Dry Run Or Manual Data Request

## Verdict
- 1704 turns the WEP parser into a real drop-folder preflight shell.
- Live files should be dropped into `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\microscope\branch_locked_wep\drop-folder\1704\live` using exact artifact names; templates live in `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\microscope\branch_locked_wep\drop-folder\1704\templates`.
- Current dry run refuses to score because required live readout, source-worldtube, material, `C_parent`/zero, `tau_min`, and manifest artifacts are absent, while existing product/branch files are still nonclaim guards.
- The request update is now exact enough to hand to a human or archive search: it names every file, field set, and reason.
- No WEP, local-GR/Newton, coupling, PPN, R10, clock, orbital or public claim is made.

## Source Register

| source_id | source_key | source_path | exists | needles_present |
| --- | --- | --- | --- | --- |
| SRC1704_0_1703_doc | 1703_doc | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1703-Y5-R2FR-WEP-source-weight-product-first-fill-or-MICROSCOPE-parser-shell.md | True | True |
| SRC1704_1_1703_validation | 1703_validation | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_BRR545_1703_VALIDATION.csv | True | True |
| SRC1704_2_1703_requirements | 1703_requirements | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_1703_MICROSCOPE_PARSER_SHELL_REQUIREMENTS.csv | True | True |
| SRC1704_3_1703_dryrun | 1703_dryrun | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_1703_MICROSCOPE_PARSER_DRY_RUN.csv | True | True |
| SRC1704_4_1703_next | 1703_next | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_1703_NEXT_TARGET.csv | True | True |
| SRC1704_5_1703_manifest_template | 1703_manifest_template | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\microscope\quarantine\1703\input\P_WEP_tau_parser_manifest_TEMPLATE.json | True | True |
| SRC1704_6_1699_request_template | 1699_request_template | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\microscope\branch_locked_wep\source\MICROSCOPE_WEP_data_request_template_1699.md | True | True |
| SRC1704_7_1482_web_candidates | 1482_web_candidates | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1482_OFFICIAL_WEB_SOURCE_CANDIDATES.csv | True | True |
| SRC1704_8_1482_manifest | 1482_manifest | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1482_OFFICIAL_INPUT_MANIFEST_UPDATE.csv | True | True |
| SRC1704_9_product_convention_live | product_convention_live | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\microscope\product_convention\P_WEP_eta_product_convention.csv | True | True |
| SRC1704_10_branch_lock_live | branch_lock_live | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\microscope\branch_classifier\P_WEP_same_parent_branch_lock.csv | True | True |

## Drop-Folder Contract

| artifact_id | artifact | drop_path | required_columns | priority |
| --- | --- | --- | --- | --- |
| ART1704_0_readout | P_WEP_K_CMSM_readout.csv | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\microscope\branch_locked_wep\drop-folder\1704\live\P_WEP_K_CMSM_readout.csv | same_parent_branch_id;session_id;time_s;orbit_phase;gx;gz;readout_component;mask_flag;calibration_flag;axis_sign;units;source_path;valid_for_claim;claim_allowed | highest |
| ART1704_1_source_worldtube | P_WEP_R_source_Earth_worldtube.csv | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\microscope\branch_locked_wep\drop-folder\1704\live\P_WEP_R_source_Earth_worldtube.csv | same_parent_branch_id;shell_id;radius_m;density_kg_m3;source_response;orbit_kernel;units;source_path;valid_for_claim;claim_allowed | highest |
| ART1704_2_material_tensor | P_WEP_TiPt_material_response_tensor.csv | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\microscope\branch_locked_wep\drop-folder\1704\live\P_WEP_TiPt_material_response_tensor.csv | same_parent_branch_id;material;component;sensitivity_value;uncertainty;basis;sign_convention;units;source_path;valid_for_claim;claim_allowed | highest |
| ART1704_3_product_convention | P_WEP_eta_product_convention.csv | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\microscope\branch_locked_wep\drop-folder\1704\live\P_WEP_eta_product_convention.csv | same_parent_branch_id;eta_formula;sign_convention;tau_eff_definition;readout_kernel_units;source_kernel_units;orbit_average_rule;branch_lock;source_path;row_status;valid_prediction_row;valid_for_claim;claim_allowed | high |
| ART1704_4_branch_lock | P_WEP_same_parent_branch_lock.csv | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\microscope\branch_locked_wep\drop-folder\1704\live\P_WEP_same_parent_branch_lock.csv | same_parent_branch_id;forbidden_mixing_rule;source_path;row_status;valid_prediction_row;valid_for_claim;claim_allowed | high |
| ART1704_5_c_parent | P_WEP_C_parent_or_zero_certificate.csv | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\microscope\branch_locked_wep\drop-folder\1704\live\P_WEP_C_parent_or_zero_certificate.csv | same_parent_branch_id;route;coefficient_or_theorem_id;value;uncertainty;units;source_path;theorem_status;valid_for_claim;claim_allowed | highest |
| ART1704_6_tau_min | P_WEP_tau_min_lower_bound.csv | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\microscope\branch_locked_wep\drop-folder\1704\live\P_WEP_tau_min_lower_bound.csv | same_parent_branch_id;tau_min;confidence;sign_or_abs_convention;derivation_or_source_path;assumptions;units;valid_for_claim;claim_allowed | highest |
| ART1704_7_manifest | P_WEP_tau_parser_manifest.json | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\microscope\branch_locked_wep\drop-folder\1704\live\P_WEP_tau_parser_manifest.json | json:branch_id;manifest_status;artifact_hashes;schema_versions;units;sign_conventions;source_paths;license;citation;valid_for_claim;claim_allowed | highest |

## Drop-Folder Inventory

| inventory_id | artifact | selected_source | target_exists | row_count | inspection_status |
| --- | --- | --- | --- | --- | --- |
| INV1704_0_readout | P_WEP_K_CMSM_readout.csv | absent | False | 0 | TARGET_ABSENT |
| INV1704_1_source_worldtube | P_WEP_R_source_Earth_worldtube.csv | absent | False | 0 | TARGET_ABSENT |
| INV1704_2_material_tensor | P_WEP_TiPt_material_response_tensor.csv | absent | False | 0 | TARGET_ABSENT |
| INV1704_3_product_convention | P_WEP_eta_product_convention.csv | canonical | True | 1 | BLOCK_MARKERS_PRESENT |
| INV1704_4_branch_lock | P_WEP_same_parent_branch_lock.csv | canonical | True | 1 | BLOCK_MARKERS_PRESENT |
| INV1704_5_c_parent | P_WEP_C_parent_or_zero_certificate.csv | absent | False | 0 | TARGET_ABSENT |
| INV1704_6_tau_min | P_WEP_tau_min_lower_bound.csv | absent | False | 0 | TARGET_ABSENT |
| INV1704_7_manifest | P_WEP_tau_parser_manifest.json | absent | False | 0 | TARGET_ABSENT |

## Schema Precheck

| precheck_id | artifact | precheck_status | refusal_reason |
| --- | --- | --- | --- |
| SPC1704_0_readout | P_WEP_K_CMSM_readout.csv | FAIL_ABSENT | live artifact is absent from canonical and drop-folder paths |
| SPC1704_1_source_worldtube | P_WEP_R_source_Earth_worldtube.csv | FAIL_ABSENT | live artifact is absent from canonical and drop-folder paths |
| SPC1704_2_material_tensor | P_WEP_TiPt_material_response_tensor.csv | FAIL_ABSENT | live artifact is absent from canonical and drop-folder paths |
| SPC1704_3_product_convention | P_WEP_eta_product_convention.csv | FAIL_BLOCK_MARKERS | file contains MISSING/PENDING/NONCLAIM/template/surrogate marker |
| SPC1704_4_branch_lock | P_WEP_same_parent_branch_lock.csv | FAIL_BLOCK_MARKERS | file contains MISSING/PENDING/NONCLAIM/template/surrogate marker |
| SPC1704_5_c_parent | P_WEP_C_parent_or_zero_certificate.csv | FAIL_ABSENT | live artifact is absent from canonical and drop-folder paths |
| SPC1704_6_tau_min | P_WEP_tau_min_lower_bound.csv | FAIL_ABSENT | live artifact is absent from canonical and drop-folder paths |
| SPC1704_7_manifest | P_WEP_tau_parser_manifest.json | FAIL_ABSENT | live artifact is absent from canonical and drop-folder paths |

## Parser Dry Run Result

| parser_id | parser_status | failure_count | computed_quantity | computed_value |
| --- | --- | --- | --- | --- |
| PRS1704_0_dry_run | REFUSED_MISSING_OR_NONCLAIM_ARTIFACTS | 8 | none | not_evaluated |
| PRS1704_1_no_bound_inversion | BOUND_AS_PREDICTION_REFUSED | 8 | P_WEP_source_weight | not_evaluated |
| PRS1704_2_no_tau_unity | TAU_UNITY_SHORTCUT_REFUSED | 8 | tau_WEP | not_evaluated |

## Manual Data Request Update

| request_id | requested_artifact | priority | request_status | preferred_drop_path |
| --- | --- | --- | --- | --- |
| REQ1704_0_readout | P_WEP_K_CMSM_readout.csv | highest | READY_TO_REQUEST_NOT_ACQUIRED | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\microscope\branch_locked_wep\drop-folder\1704\live\P_WEP_K_CMSM_readout.csv |
| REQ1704_1_source_worldtube | P_WEP_R_source_Earth_worldtube.csv | highest | READY_TO_REQUEST_NOT_ACQUIRED | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\microscope\branch_locked_wep\drop-folder\1704\live\P_WEP_R_source_Earth_worldtube.csv |
| REQ1704_2_material_tensor | P_WEP_TiPt_material_response_tensor.csv | highest | READY_TO_REQUEST_NOT_ACQUIRED | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\microscope\branch_locked_wep\drop-folder\1704\live\P_WEP_TiPt_material_response_tensor.csv |
| REQ1704_3_product_convention | P_WEP_eta_product_convention.csv | high | READY_TO_REQUEST_NOT_ACQUIRED | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\microscope\branch_locked_wep\drop-folder\1704\live\P_WEP_eta_product_convention.csv |
| REQ1704_4_branch_lock | P_WEP_same_parent_branch_lock.csv | high | READY_TO_REQUEST_NOT_ACQUIRED | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\microscope\branch_locked_wep\drop-folder\1704\live\P_WEP_same_parent_branch_lock.csv |
| REQ1704_5_c_parent | P_WEP_C_parent_or_zero_certificate.csv | highest | READY_TO_REQUEST_NOT_ACQUIRED | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\microscope\branch_locked_wep\drop-folder\1704\live\P_WEP_C_parent_or_zero_certificate.csv |
| REQ1704_6_tau_min | P_WEP_tau_min_lower_bound.csv | highest | READY_TO_REQUEST_NOT_ACQUIRED | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\microscope\branch_locked_wep\drop-folder\1704\live\P_WEP_tau_min_lower_bound.csv |
| REQ1704_7_manifest | P_WEP_tau_parser_manifest.json | highest | READY_TO_REQUEST_NOT_ACQUIRED | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\microscope\branch_locked_wep\drop-folder\1704\live\P_WEP_tau_parser_manifest.json |

## If-Unlocked Computation Plan

| step_id | step | formula_or_action | current_status |
| --- | --- | --- | --- |
| CPU1704_0_load | load live artifacts | read K_CMSM, S_Earth, M_TiPt, C_parent/zero, product convention, tau_min and manifest | NOT_RUN_INPUTS_MISSING |
| CPU1704_1_direct_product | compute forward direct product | P_WEP_source_weight = N_eta^-1 <K_CMSM, C_parent[S_Earth,M_TiPt]> | NOT_RUN_INPUTS_MISSING |
| CPU1704_2_compare | compare to MICROSCOPE bound | abs(P_WEP_source_weight) <= 2.8e-15 only after forward product is computed | NOT_RUN_PRODUCT_MISSING |
| CPU1704_3_delta_w_optional | optional Delta_w conversion | abs(Delta_w_TiPt) <= 2.8e-15/tau_min if tau_min>0 exists | NOT_RUN_TAU_MIN_MISSING |

## Decision

| decision_id | decision | reason | next_action |
| --- | --- | --- | --- |
| DEC1704_0_parser_shell | DROP_FOLDER_PARSER_SHELL_READY | templates, README, inventory and dry-run refusal now exist | acquire live artifacts or use parser shell as exact request checklist |
| DEC1704_1_current_result | PARSER_REFUSES_SCORE | missing live readout/source/material/C_parent/tau_min/manifest and nonclaim product/branch rows | do not score WEP until parser has live source-backed inputs |
| DEC1704_2_next | NEXT_1705_PUBLIC_SOURCE_PROBE_OR_PARENT_ZERO_ROUTE_SWITCH | with parser shell done, the next work is either external source acquisition or a theory-side demotion of split Delta_w | try a public archive/source probe, then fall back to Delta_w parent-zero/direct-product route if no files are available |

## Next Target

| route_id | next_target | objective | selection_status |
| --- | --- | --- | --- |
| NEXT1704_0_primary | 1705-Y5-R2FR-MICROSCOPE-public-source-probe-or-parent-zero-route-switch.md | probe whether public MICROSCOPE/CMSM data files can be located and mapped into the 1704 drop contract; if not, switch to the theory-side Delta_w demotion/direct-product route | selected |
| NEXT1704_1_theory | 1705a-Y5-R2FR-Delta-w-parent-zero-final-route-or-direct-product-only.md | make final parent-signature attempt for Delta_w=0; if not signed, demote the split Delta_w route and keep direct product only | held_fallback |
| NEXT1704_2_r10 | 1705b-Y5-R2FR-R10-alpha-lambda-projection-fill-runner.md | return to R10 alpha(lambda) once WEP parser source acquisition is blocked or staged | held_fallback |

## Claim Gates

| claim_id | claim | status | reason |
| --- | --- | --- | --- |
| CG1704_0_parser_ready | MICROSCOPE WEP parser can evaluate source-weight product | BLOCKED_NO_CLAIM | dry run refuses missing/nonclaim artifacts |
| CG1704_1_wep_score | MTS WEP source-weight score | BLOCKED_NO_CLAIM | forward P_WEP_source_weight is not computed |
| CG1704_2_delta_w_bound | finite Delta_w_TiPt bound | BLOCKED_NO_CLAIM | tau_min is missing and tau=1 shortcut is forbidden |
| CG1704_3_local_GR | derived local GR/Newton through WEP source branch | BLOCKED_NO_CLAIM | local coupling/source-weight branch remains unresolved |

## Validation

| check_id | result | detail |
| --- | --- | --- |
| VAL1704_0_sources_exist | PASS | all cited local source paths exist |
| VAL1704_1_needles_present | PASS | all required source needles are present |
| VAL1704_2_drop_contract_complete | PASS | drop-folder contract lists every required artifact |
| VAL1704_3_drop_dirs_exist | PASS | drop-folder live/template directories exist |
| VAL1704_4_templates_exist | PASS | all drop-folder templates exist |
| VAL1704_5_inventory_complete | PASS | inventory inspects every artifact |
| VAL1704_6_precheck_refuses | PASS | schema precheck refuses absent/nonclaim artifacts |
| VAL1704_7_parser_refuses | PASS | parser dry-run refuses current inputs |
| VAL1704_8_no_computation | PASS | computation plan is not run |
| VAL1704_9_request_ready | PASS | manual data request update exists and covers every artifact |
| VAL1704_10_decision_next | PASS | decision selects 1705 source probe or theory switch |
| VAL1704_11_next_selected | PASS | next target selected |
| VAL1704_12_claim_gates_blocked | PASS | all claim gates remain blocked |
| VAL1704_13_csv_parse | PASS | all generated 1704 CSVs parse |
| VAL1704_14_no_claim_flags | PASS | all generated score/prediction/claim flags remain false |
| VAL1704_15_branch_copies | PASS | branch/quarantine/queue copies exist |
| VAL1704_16_pycache_absent | PASS | scripts __pycache__ absent |
| VAL1704_17_formalization_untouched | PASS | no 1704 outputs found under formalization-workbench outside vendor/env folders |
| VAL1704_OVERALL | PASS | 1704 MICROSCOPE parser shell dry-run/manual request validation |

## Working Interpretation
The WEP/coupling path is now split cleanly: data route or theory route. The data route has a concrete door: if real MICROSCOPE/CMSM artifacts appear, the parser can inspect them without rewriting the theory. If they do not appear, the next honest move is to either probe public sources once or demote the separate `Delta_w` split and keep only the direct product branch.
