# 2120 - Y5/R2FR MICROSCOPE Numeric Source-Readout Kernel Acquisition

## Current Verdict

2120 probes the official MICROSCOPE/CMSM routes and inventories the local drop folders. The result is useful but not runnable: we have official provenance, templates, segment metadata, and a surrogate design matrix, but no verified CMSM numeric arrays for `gx`, `gz`, `Sxx`, `Sxz`, masks, calibration flags, attitude convention, or source-worldtube normalization.

Therefore `tau_WEP` remains blocked. This is a practical data-access block, not a theory block. The derivation route can continue, and the data route now has exact manual-export requirements.

No MICROSCOPE/WEP/local-GR claim is allowed from this checkpoint.

## Source Register

| source_id | source_path | path_exists | needles_found | role | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| SRC2120_00_2119_next | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_2119_NEXT_TARGET.csv | true | true | 2119 selects MICROSCOPE numeric kernel acquisition. | false |
| SRC2120_01_2119_validation | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_BRR545_2119_VALIDATION.csv | true | true | 2119 validation passed. | false |
| SRC2120_02_1071_kernel | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1071_OFFICIAL_KERNEL_COMPONENTS.csv | true | true | 1071 official kernel skeleton but no numeric tau. | false |
| SRC2120_03_1068_orbit | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1068_MICROSCOPE_ORBIT_READOUT_REQUIREMENTS.csv | true | true | 1068 orbit/readout requirements. | false |
| SRC2120_04_1068_source | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1068_SOURCE_WORLDTUBE_REQUIREMENTS.csv | true | true | 1068 source-worldtube requirements. | false |
| SRC2120_05_1084_readout | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1084_MICROSCOPE_READOUT_IMPORT_GATE.csv | true | true | 1084 CMSM arrays import gate. | false |
| SRC2120_06_1900_targets | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_1900_OFFICIAL_READOUT_DATA_TARGETS_NONCLAIM.csv | true | true | 1900 official readout target ledger. | false |
| SRC2120_07_segments | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1071_SUEP_SEGMENT_TABLE_SOURCE_BACKED.csv | true | true | local source-backed segment metadata. | false |
| SRC2120_08_surrogate | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1075_SURROGATE_DESIGN_MATRIX_SEGMENT210.csv | true | true | local surrogate design matrix. | false |
| SRC2120_09_cmsm_template | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\microscope_cmsm\TEMPLATE_2001_expected_official_array_schema.csv | true | true | expected CMSM array schema template. | false |
| SRC2120_10_drop_template | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\microscope\branch_locked_wep\drop-folder\1704\templates\P_WEP_K_CMSM_readout_TEMPLATE.csv | true | true | branch-locked WEP drop template. | false |
| SRC2120_11_web_probe | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_2120_WEB_PROBE.csv | true | true | fresh 2120 web probe rows. | false |


## Web Probe

| probe_id | url | status | status_code | bytes_written | contains_data_pointer | usable_numeric_arrays | error | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| WEB2120_0_ONERA_data_available | https://microscope.onera.fr/fr/publication/microscope-data-are-available | FETCHED_SMALL_PAGE | 200 | 26817 | true | false |  | false |
| WEB2120_1_CMSM_user_microscope | https://cmsm-ds.onera.fr/user/microscope | FETCH_FAILED_RECORDED |  | 0 | false | false | URLError: <urlopen error timed out> | false |
| WEB2120_2_CMSM_root | https://cmsm-ds.onera.fr/ | FETCH_FAILED_RECORDED |  | 0 | false | false | URLError: <urlopen error timed out> | false |
| WEB2120_3_arxiv_mission_scenario | https://arxiv.org/abs/2201.10841 | FETCHED_SMALL_PAGE | 200 | 51044 | true | false |  | false |


## Local Inventory

| inventory_id | object_name | local_path | path_exists | size_bytes | current_status | usable_numeric_arrays | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| INV2120_0_expected_schema | expected official array schema | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\microscope_cmsm\TEMPLATE_2001_expected_official_array_schema.csv | true | 453 | TEMPLATE_ONLY | false | false |
| INV2120_1_cmsm_readme | manual drop instructions | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\microscope_cmsm\README_2001_DROP_CMSM_EXPORTS_HERE.txt | true | 379 | INSTRUCTIONS_ONLY | false | false |
| INV2120_2_drop_readme | branch locked drop folder instructions | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\microscope\branch_locked_wep\drop-folder\1704\README_DROP_FILES_1704.md | true | 1896 | INSTRUCTIONS_ONLY | false | false |
| INV2120_3_drop_template | readout CSV template | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\microscope\branch_locked_wep\drop-folder\1704\templates\P_WEP_K_CMSM_readout_TEMPLATE.csv | true | 401 | TEMPLATE_ONLY | false | false |
| INV2120_4_drop_live_readout | live official readout CSV | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\microscope\branch_locked_wep\drop-folder\1704\live\P_WEP_K_CMSM_readout.csv | false | 0 | MISSING_UNLESS_USER_EXPORTS | false | false |
| INV2120_5_suep_segments | SUEP segment metadata | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1071_SUEP_SEGMENT_TABLE_SOURCE_BACKED.csv | true | 2579 | METADATA_ONLY_NOT_ARRAYS | false | false |
| INV2120_6_surrogate_design | surrogate design matrix | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1075_SURROGATE_DESIGN_MATRIX_SEGMENT210.csv | true | 78534 | SURROGATE_NOT_OFFICIAL | false | false |
| INV2120_7_1900_targets | previous data target ledger | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_1900_OFFICIAL_READOUT_DATA_TARGETS_NONCLAIM.csv | true | 2381 | PRIOR_PROBE_NONCLAIM | false | false |


## Numeric Requirements

| req_id | needed_object | current_status | source_status | blocks_tau | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| REQ2120_0_time_session | time/session/orbit index | METADATA_PARTIAL_SEGMENTS_ONLY | SUEP segment table exists; exact timestamps/arrays missing | true | false |
| REQ2120_1_gx_gz | gx,gz source gravity basis | MISSING_OFFICIAL_ARRAYS | 1071 skeleton and surrogate exist; official CMSM array not verified | true | false |
| REQ2120_2_Sxx_Sxz | Sxx,Sxz gravity-gradient/inertia basis | MISSING_OFFICIAL_ARRAYS | surrogate basis cannot replace official arrays | true | false |
| REQ2120_3_masks_calibration | masks/calibration flags/systematics | MISSING | drop schema requires mask/calibration flags | true | false |
| REQ2120_4_attitude_axis | instrument attitude/sensitive-axis convention | MISSING | ORB1068_1 missing | true | false |
| REQ2120_5_eta_convention | eta_AB normalization/sign convention | BOUND_IMPORTED_FORMULA_NOT_PARENT_MAPPED | ORB1068_2 guard only | true | false |
| REQ2120_6_source_worldtube | source stress/composition/finite support | SOURCE_WORLDTUBE_NOT_ACQUIRED | SWT1068_5 verdict | true | false |
| REQ2120_7_tau_kernel_verdict | numeric tau_WEP kernel | BLOCKED_OFFICIAL_ARRAYS_AND_SOURCE_WORLDTUBE_MISSING | cannot run claim-grade tau_WEP | true | false |


## Acquisition Status

| status_id | status | detail | valid_numeric_kernel | valid_for_claim |
| --- | --- | --- | --- | --- |
| STAT2120_0_web_probe | OFFICIAL_SOURCES_PROBED | small official pages/portal endpoints probed and recorded | false | false |
| STAT2120_1_live_arrays | OFFICIAL_ARRAYS_NOT_LOCAL | drop-folder live CMSM readout file checked | false | false |
| STAT2120_2_surrogate | SURROGATE_PRESENT_NONCLAIM | 1075 surrogate design matrix exists but cannot replace CMSM arrays | false | false |
| STAT2120_3_tau | TAU_WEP_BLOCKED | numeric tau kernel remains blocked unless official arrays and source-worldtube inputs are supplied | false | false |


## Claim Gates

| gate_id | gate | gate_pass | rationale | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- |
| GATE2120_0_web_probe | official data routes probed | true | ONERA/CMSM/arXiv routes are recorded as provenance and small fetch attempts | false | false |
| GATE2120_1_official_arrays | official CMSM arrays local and verified | false | no verified live readout file with gx/gz/Sxx/Sxz/masks/calibration flags is present | false | false |
| GATE2120_2_surrogate_allowed | surrogate design matrix can score WEP | false | surrogate is useful for plumbing only and cannot replace official arrays | false | false |
| GATE2120_3_tau_WEP_runnable | numeric tau_WEP kernel runnable | false | official arrays, attitude/masks, eta convention and source worldtube remain missing | false | false |
| GATE2120_4_claim_allowed | WEP/local-GR empirical claim allowed | false | data acquisition checkpoint only; no MTS prediction row can be scored | false | false |


## Decision Ledger

| decision_id | decision | because | next_action | valid_for_claim |
| --- | --- | --- | --- | --- |
| DEC2120_0 | NUMERIC_KERNEL_NOT_ACQUIRED | official portal/source pointers exist but no verified machine-readable CMSM arrays are local. | manual CMSM export or authenticated browser/data retrieval is needed. | false |
| DEC2120_1 | SURROGATE_RETAINED_FOR_PLUMBING_ONLY | segment metadata and surrogate design matrix can test code shape but not physics. | keep surrogate rows nonclaim. | false |
| DEC2120_2 | DERIVATION_CAN_CONTINUE_IN_PARALLEL | data blockage is practical, not a theory impasse. | continue source/readout theorem closure while arranging CMSM export. | false |


## Next Target

| route_id | next_target | script | objective | forbidden_shortcuts | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| NEXT2120_0_2121 | 2121-Y5-R2FR-source-readout-theorem-closure-or-CMSM-manual-export-workflow.md | scripts/Y5_R2FR_source_readout_theorem_closure_or_CMSM_manual_export_workflow_2121.py | Either continue the derivation route by closing source/readout as owned-coframe functionals, or prepare a manual CMSM export workflow with exact required filenames, columns, validation checks and no-claim import rules. | treating portal pointers as arrays; using surrogate rows as empirical evidence; fitted-G absorption; cancellation; local-GR/Newton/PPN claim; formalization-workbench edits; GitHub action | false |


## Branch Copies

| copy_id | destination | path_exists | row_count | parse_ok | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| COPY2120_0_source_weight_docs | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\source-weight\docs\AFRAME_MICROSCOPE_NUMERIC_2120_NONCLAIM.csv | true | 20 | true | false |
| COPY2120_1_branch_locked_wep | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\microscope\branch_locked_wep\residuals\P8_Y5_PARENT_QLOC_2120_MICROSCOPE_NUMERIC_STATUS_NONCLAIM.csv | true | 20 | true | false |
| COPY2120_2_acquisition_queue | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\rab-sector\acquisition-queue\JR2120_CMSM_MANUAL_EXPORT_OR_THEOREM_QUEUE.csv | true | 9 | true | false |


## Validation

| check_id | status | detail | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- |
| VAL2120_00_sources | PASS | all cited local data-acquisition sources exist and contain expected needles | false | false |
| VAL2120_01_web_probe | PASS | official web routes were probed and recorded | false | false |
| VAL2120_02_inventory | PASS | local drop/template/metadata inventory includes live-readout check | false | false |
| VAL2120_03_tau_blocked | PASS | numeric tau_WEP remains blocked | false | false |
| VAL2120_04_status | PASS | status ledger records TAU_WEP_BLOCKED | false | false |
| VAL2120_05_claim_gates | PASS | web probe passes but tau runnable gate fails | false | false |
| VAL2120_06_no_claim_flags | PASS | no generated row allows a claim or score | false | false |
| VAL2120_07_branch_copies | PASS | branch copies exist and parse | false | false |
| VAL2120_08_csv_parse | PASS | all generated CSVs parse cleanly | false | false |
| VAL2120_09_formalization_clean | PASS | formalization-workbench untouched by 2120 | false | false |
| VAL2120_10_no_pycache | PASS | scripts __pycache__ removed | false | false |
| VAL2120_11_next | PASS | next target selects source/readout theorem closure or CMSM manual export workflow | false | false |
| VAL2120_OVERALL | PASS | 2120 probes official routes, inventories local MICROSCOPE inputs, blocks numeric tau_WEP honestly, and stages the manual export/theorem next fork. | false | false |
