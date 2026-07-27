# 1422 - MICROSCOPE Source-Leg Data Schema Or gx/gz/Sxx/Sxz Kernel Pilot

**Current verdict:** the CMSM/MICROSCOPE schema and official `gx/gz/Sxx/Sxz` pilot arrays are not acquired. The ONERA public information page is reachable, but the CMSM browser/API routes did not provide a usable schema or arrays in this run. Existing 1072/1074 dry-run and surrogate previews remain nonclaim pipeline tests only.

**Discipline move:** this checkpoint writes the exact blocker ledger and local export contract. The next data step is either ingest a user/browser CMSM export under `source-intake/microscope_cmsm`, or run a clearly labelled surrogate smoke runner that cannot be cited as WEP/tau evidence.

**Status:** `Y5_R10_1422_CMSM_schema_not_acquired_gxgzS_pilot_blocker_ledger_written_nonclaim`

## Source Register

| source_id | source_path | anchor | role | path_exists | anchor_found | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| SRC1422_0_1421_doc | 1421-Y5-R10-RAB-WEP-source-worldtube-or-parent-point-source-theorem.md | NEXT1421_0_1422 | prior checkpoint selecting CMSM data schema or gx/gz/Sxx/Sxz pilot | True | True | False | False |
| SRC1422_1_1421_metadata | source-intake/mts_residuals/P8_Y5_R10_1421_WEP_SOURCE_WORLDTUBE_METADATA_ROWS.csv | WSW1421_8_verdict | source-worldtube metadata staged but numeric source leg missing | True | True | False | False |
| SRC1422_2_1071_kernel | source-intake/mts_residuals/P8_Y5_R10_1071_OFFICIAL_KERNEL_COMPONENTS.csv | KER1071_6_verdict | official kernel skeleton acquired but numeric tau/source arrays missing | True | True | False | False |
| SRC1422_3_1071_tau | source-intake/mts_residuals/P8_Y5_R10_1071_TAU_PROJECTION_STATUS.csv | TAU1071_3_verdict | numeric tau/source projection not acquired | True | True | False | False |
| SRC1422_4_1071_segments | source-intake/mts_residuals/P8_Y5_R10_1071_SUEP_SEGMENT_TABLE_SOURCE_BACKED.csv | SUEP1071_210 | SUEP segment 210 metadata for pilot | True | True | False | False |
| SRC1422_5_1072_probe | source-intake/mts_residuals/P8_Y5_R10_1072_PORTAL_ROUTE_PROBE.csv | https://cmsm-ds.onera.fr/user/microscope | prior CMSM portal probe failure | True | True | False | False |
| SRC1422_6_1072_requirements | source-intake/mts_residuals/P8_Y5_R10_1072_RECONSTRUCTION_REQUIREMENTS.csv | REQ1072_0_exact_time_grid | reconstruction requirement list | True | True | False | False |
| SRC1422_7_1072_dryrun | source-intake/mts_residuals/P8_Y5_R10_1072_GXS_DRY_RUN_METADATA_SEGMENT210.csv | DRY1072_0_segment210_kernel_preview | nonclaim dry-run shape preview | True | True | False | False |
| SRC1422_8_1073_contract | source-intake/mts_residuals/P8_Y5_R10_1073_CMSM_EXPORT_CONTRACT.csv | CMSM1073_5_official_gxS_arrays | CMSM export contract for official gx/gz/Sxx/Sxz arrays | True | True | False | False |
| SRC1422_9_1073_status | source-intake/mts_residuals/P8_Y5_R10_1073_OFFICIAL_ARRAY_EXTRACT_STATUS.csv | EX1073_2_official_segment210_arrays | official arrays not acquired | True | True | False | False |
| SRC1422_10_1074_inventory | source-intake/mts_residuals/P8_Y5_R10_1074_CMSM_EXPORT_INVENTORY_CHECK.csv | INV1074_0_search_root | local CMSM export not found in prior check | True | True | False | False |
| SRC1422_11_1074_surrogate | source-intake/mts_residuals/P8_Y5_R10_1074_SURROGATE_GRID_METADATA_SEGMENT210.csv | GRID1074_0_segment210_surrogate | nonclaim surrogate grid exists | True | True | False | False |

## Current Portal Probe

| url | probe_status | http_status | content_type | bytes_sampled | schema_or_arrays_acquired | error | valid_for_claim | claim_allowed | generated_utc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| https://microscope.onera.fr/fr/publication/microscope-data-are-available | HTTP_OK | 200 | text/html; charset=UTF-8 | 1024 | False |  | False | False | 2026-06-16T04:19:23.443877+00:00 |
| https://cmsm-ds.onera.fr/user/microscope | BLOCKED_OR_UNREACHABLE_FROM_THIS_RUN |  |  | 0 | False | URLError: <urlopen error [WinError 10061] No connection could be made because the target machine actively refused it> | False | False | 2026-06-16T04:19:23.443877+00:00 |
| https://cmsm-ds.onera.fr/api/v1/rs-access-project/datasets/search | BLOCKED_OR_UNREACHABLE_FROM_THIS_RUN |  |  | 0 | False | URLError: <urlopen error [WinError 10061] No connection could be made because the target machine actively refused it> | False | False | 2026-06-16T04:19:23.443877+00:00 |
| https://cmsm-ds.onera.fr/api/v1/rs-access-project/dataobjects/search | BLOCKED_OR_UNREACHABLE_FROM_THIS_RUN |  |  | 0 | False | URLError: <urlopen error [WinError 10061] No connection could be made because the target machine actively refused it> | False | False | 2026-06-16T04:19:23.443877+00:00 |
| https://cmsm-ds.onera.fr/api/v1/rs-access-project/applications/microscope/modules | BLOCKED_OR_UNREACHABLE_FROM_THIS_RUN |  |  | 0 | False | URLError: <urlopen error [WinError 10061] No connection could be made because the target machine actively refused it> | False | False | 2026-06-16T04:19:23.443877+00:00 |

## CMSM Schema Status

| schema_id | object | status | evidence | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| CSS1422_0_public_pointer | ONERA public MICROSCOPE data page | REACHABLE | P8_Y5_R10_1422_CURRENT_PORTAL_PROBE.csv | False | False |
| CSS1422_1_cmsm_portal | CMSM browser/API schema | NOT_ACQUIRED | P8_Y5_R10_1422_CURRENT_PORTAL_PROBE.csv | False | False |
| CSS1422_2_local_export_inventory | local CMSM export folder | NO_LOCAL_EXPORT_FOUND | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\microscope_cmsm | False | False |
| CSS1422_3_official_arrays | official gx/gz/Sxx/Sxz arrays | NOT_ACQUIRED | P8_Y5_R10_1073_OFFICIAL_ARRAY_EXTRACT_STATUS.csv::EX1073_2_official_segment210_arrays | False | False |
| CSS1422_4_verdict | CMSM schema/file inventory | SCHEMA_NOT_ACQUIRED_BLOCKER_LEDGER_REQUIRED | CSS1422_0 through CSS1422_3 | False | False |

## gx/gz/Sxx/Sxz Kernel Pilot Status

| pilot_id | object | status | evidence | usable_for_claim | next_requirement | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| GXP1422_0_official_kernel_skeleton | official kernel basis | FORM_ACQUIRED_NOT_NUMERIC | KER1071_1_fit_basis;KER1071_2_source_gravity_leg;KER1071_6_verdict | False | numeric gx,gz,Sxx,Sxz arrays or exact reconstruction inputs | False | False |
| GXP1422_1_dry_run_preview | 1072 unit-shape preview | DRY_RUN_SHAPE_ONLY | DRY1072_0_segment210_kernel_preview | False | replace zero-phase/unit-amplitude columns with official or source-reconstructed arrays | False | False |
| GXP1422_2_surrogate_preview | 1074 circular monopole surrogate | NONCLAIM_PIPELINE_TEST_ONLY | GRID1074_0_segment210_surrogate | False | only use as smoke runner after explicit nonclaim flag; never as MICROSCOPE tau | False | False |
| GXP1422_3_segment210_window | SUEP segment 210 metadata | SEGMENT_METADATA_AVAILABLE_MASKS_MISSING | SUEP1071_210 | False | exact timestamps and glitch masks | False | False |
| GXP1422_4_pilot_arrays | pilot gx/gz/Sxx/Sxz source-leg arrays | NOT_ACQUIRED_OR_RECONSTRUCTED | CSS1422_4_verdict; EBL1422 blockers | False | CMSM export, data schema, or reconstruction inputs | False | False |
| GXP1422_5_numeric_tau | numeric tau_WEP / M_WEP,q | NOT_ACQUIRED | GXP1422_4_pilot_arrays plus missing residual/material map | False | arrays plus MTS material/source residual map | False | False |

## Exact Blocker Ledger

| blocker_id | blocked_object | why_needed | current_status | accepted_resolution | do_not_use | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| EBL1422_0_schema_inventory | CMSM dataset/file inventory | identify official MICROSCOPE products and download/export paths | NOT_ACQUIRED | source-backed API/browser export or local file inventory with dataset/product names | guessed endpoint names as schema | False | False |
| EBL1422_1_exact_time_grid | segment 210 timestamps and masks | phase, DFT alignment, glitch removal, and regression basis depend on exact samples | MISSING_EXACT_TIMESTAMPS_AND_MASKS | CMSM time/mask export or exact segment product with mask flags | duration-only uniform grid as claim-grade timestamps | False | False |
| EBL1422_2_orbit_ephemeris | satellite position/velocity | compute g(O_sat) and gravity-gradient tensor T | MISSING_NUMERIC_EPHEMERIS | CMSM minute-sampled orbit product or source-backed equivalent | circular orbit surrogate as official kernel | False | False |
| EBL1422_3_attitude_rates | attitude/angular velocity/angular acceleration | rotate g/T into instrument frame and build inertia-gradient S | MISSING_NUMERIC_ATTITUDE_RATES | same-stamp attitude/rate products or documented interpolation rule | zero-phase/zero-attitude surrogate as claim | False | False |
| EBL1422_4_gravity_model | Earth gravity model/source profile | official g/T reconstruction and finite-source/source-worldtube convention | MISSING_OFFICIAL_GRAVITY_MODEL_OR_APPROVED_SURROGATE | MICROSCOPE processing gravity model, auxiliary data, or explicitly nonclaim surrogate route | unlabelled monopole model as official tau | False | False |
| EBL1422_5_material_source_map | MTS material/source residual map | turn gx/gz/Sxx/Sxz fit basis into an MTS source-weight prediction | MISSING_PARENT_MATERIAL_MAP | theorem-zero residuals or source-backed qbar/material coefficients in same basis | alpha/Coulomb smoke row as full source-weight tensor | False | False |
| EBL1422_6_verdict | pilot numeric source-leg kernel | first executable M_WEP,q row | BLOCKED_SCHEMA_AND_INPUTS_MISSING | resolve EBL1422_0 through EBL1422_5 or keep only nonclaim smoke runner | numeric tau_WEP without arrays and MTS source map | False | False |

## Local Export Contract

| contract_id | target_folder | required_files | minimum_fields | current_status | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- |
| EXP1422_0_folder | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\microscope_cmsm | dataset_inventory.csv or equivalent manifest | dataset_name;product_type;file_name;download_url_or_order_id;time_coverage;session_or_segment | NOT_FOUND_LOCALLY | False | False |
| EXP1422_1_segment210_time_mask | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\microscope_cmsm\segment210 | time_mask.csv | segment_id;t_utc;sample_index;mask_flag;mask_reason | NOT_FOUND_LOCALLY | False | False |
| EXP1422_2_segment210_orbit_attitude | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\microscope_cmsm\segment210 | orbit.csv;attitude_rates.csv | t_utc;r_x;r_y;r_z;v_x;v_y;v_z;frame;units and q/Omega/Omegadot fields | NOT_FOUND_LOCALLY | False | False |
| EXP1422_3_segment210_gxS | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\microscope_cmsm\segment210 | gxgzSxxSxz.csv | segment_id;t_utc;gx;gz;Sxx;Sxz;frame;generation_method;source_file | NOT_FOUND_LOCALLY | False | False |
| EXP1422_4_verdict | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\microscope_cmsm | all EXP1422 rows | source path, units, frame, provenance, and mask convention | EXPORT_CONTRACT_READY_INPUTS_MISSING | False | False |

## Decision Ledger

| decision_id | decision | reason | next_action | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- |
| DEC1422_0_schema_verdict | CMSM schema/file inventory not acquired from current run | public ONERA page reachable; CMSM browser/API endpoints unreachable or do not yield schema | use browser/manual export or provide exact CMSM files/API response | False | False |
| DEC1422_1_pilot_verdict | gx/gz/Sxx/Sxz pilot remains blocked | dry-run and surrogate previews exist but exact timestamps, ephemeris, attitude/rates, gravity model, masks, and material map are missing | fill export contract or choose explicitly nonclaim smoke-runner path | False | False |
| DEC1422_2_best_next | target user/browser CMSM export import or nonclaim smoke runner next | automated portal access is not providing schema; a local export would unblock official pilot arrays fastest | if export is available, ingest it; otherwise run a labelled surrogate-only smoke runner that cannot be cited as evidence | False | False |

## Claim Gate

| gate_id | claim | allowed | reason | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- |
| CG1422_0_schema_claim | CMSM schema/file inventory acquired | False | CSS1422_4 remains schema not acquired | False | False |
| CG1422_1_kernel_claim | official gx/gz/Sxx/Sxz arrays acquired or reconstructed | False | GXP1422_4 remains not acquired/reconstructed | False | False |
| CG1422_2_tau_claim | numeric tau_WEP or M_WEP,q source leg is available | False | MICROSCOPE_source_leg_schema_probe_and_gxgzS_pilot_blocker_only_no_numeric_tau_no_WEP_pass_no_guessed_masks_no_point_source_by_taste | False | False |
| CG1422_3_WEP_claim | WEP source projection can be scored or passed | False | schema, arrays, residual/material map, and WEP projection row are incomplete | False | False |

## Next Target

| next_id | target_doc | target_script | task | success_condition | do_not_claim | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| NEXT1422_0_1423 | 1423-Y5-R10-RAB-CMSM-export-import-or-surrogate-smoke-runner.md | scripts/Y5_R10_RAB_CMSM_export_import_or_surrogate_smoke_runner.py | look for a user-supplied CMSM export under source-intake/microscope_cmsm; if absent, run only a labelled surrogate smoke runner and keep all WEP/tau/local-GR claims blocked | official export is parsed into schema rows, or surrogate smoke output is generated with explicit nonclaim status and replacement map | official tau from surrogate; WEP pass; guessed masks/phases; measured-G absorption | False | False |
| NEXT1422_1_parallel_theory | future-MWEP-source-leg-theorem-zero-route.md | future_theory_route | continue theory route for source-leg theorem-zero while data export remains blocked | M_WEP,q is theorem-zero/common-mode or retained as finite residual | data blocker as theory proof | False | False |

## Validation

| check_id | status | detail | generated_utc |
| --- | --- | --- | --- |
| VAL1422_0_sources | PASS | all cited local source paths exist and anchors are present | 2026-06-16T04:19:23.443877+00:00 |
| VAL1422_1_current_probe | PASS | current portal probe rows were written | 2026-06-16T04:19:23.443877+00:00 |
| VAL1422_2_schema_status | PASS | schema status remains blocked and explicit | 2026-06-16T04:19:23.443877+00:00 |
| VAL1422_3_pilot_status | PASS | pilot gx/gz/Sxx/Sxz arrays are not claimed | 2026-06-16T04:19:23.443877+00:00 |
| VAL1422_4_blockers | PASS | exact blocker ledger covers schema, time grid, ephemeris, attitude, gravity model, and material map | 2026-06-16T04:19:23.443877+00:00 |
| VAL1422_5_export_contract | PASS | local CMSM export contract is written | 2026-06-16T04:19:23.443877+00:00 |
| VAL1422_6_claim_refusal | PASS | schema, kernel, tau, and WEP claims are refused | 2026-06-16T04:19:23.443877+00:00 |
| VAL1422_7_decision | PASS | decision ledger selects export import or surrogate smoke runner next | 2026-06-16T04:19:23.443877+00:00 |
| VAL1422_8_next_target | PASS | next target 1423 is staged | 2026-06-16T04:19:23.443877+00:00 |
| VAL1422_9_scope | PASS | outputs are confined to post-checkpoint-work paths | 2026-06-16T04:19:23.443877+00:00 |
| VAL1422_10_overall | PASS | 1422 fails CMSM schema/pilot acquisition and writes exact blocker ledger as nonclaim | 2026-06-16T04:19:23.443877+00:00 |
