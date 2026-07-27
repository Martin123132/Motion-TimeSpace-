# 1999 Y5 R2FR: MICROSCOPE Numeric Kernel Or Source-Worldtube Row

Private checkpoint. This imports the 1072 CMSM/REGARDS route and segment-210 dry-run into the current WEP/direct-product branch.

Verdict: the CMSM data route and reconstruction path are staged, but no official numeric `tau_WEP` kernel is acquired. The segment-210 `gx/gz/Sxx/Sxz` preview is a dry-run only, not evidence.

Still missing: CMSM schema/file inventory, exact timestamps/masks, orbit ephemeris, attitude/rates, official gravity model or approved surrogate, and official/source-reconstructed numeric arrays.

Next honest move: CMSM schema capture or one pilot segment official/source-reconstructed array extract.

No WEP, local-GR, Newton, R10, PPN, clock, orbital, or public claim follows from 1999.

## Source Register

| branch_id | valid_for_claim | claim_allowed | generated_utc | source_id | source_path | needed_for | needles | exists | anchor_found | missing_needles | status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | false | false | 2026-06-20T03:26:51.634925+00:00 | 1998_doc | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1998-Y5-R2FR-MICROSCOPE-eta-readout-formula-or-orbit-kernel-acquisition.md | 1999 MICROSCOPE numeric kernel or source worldtube row | KER1998_4_verdict;NEXT1998_0_primary | True | True |  | EXISTS_NEEDLES_CONFIRMED |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | false | false | 2026-06-20T03:26:51.634925+00:00 | 1998_validation | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_BRR545_1998_VALIDATION.csv | 1999 MICROSCOPE numeric kernel or source worldtube row | VAL1998_OVERALL;PASS | True | True |  | EXISTS_NEEDLES_CONFIRMED |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | false | false | 2026-06-20T03:26:51.634925+00:00 | 1072_numeric_kernel | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1072-Y5-R10-MICROSCOPE-data-portal-schema-or-reconstructed-gxS-kernel.md | 1999 MICROSCOPE numeric kernel or source worldtube row | DRY1072_0_segment210_kernel_preview;NTS1072_2_tau_WEP;NEXT1072_0_1073 | True | True |  | EXISTS_NEEDLES_CONFIRMED |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | false | false | 2026-06-20T03:26:51.634925+00:00 | 1072_validation | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_BRR545_1072_VALIDATION.csv | 1999 MICROSCOPE numeric kernel or source worldtube row | V1072_SUMMARY;pass | True | True |  | EXISTS_NEEDLES_CONFIRMED |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | false | false | 2026-06-20T03:26:51.634925+00:00 | 1071_kernel | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1071-Y5-R10-MICROSCOPE-full-orbit-kernel-or-source-worldtube-row.md | 1999 MICROSCOPE numeric kernel or source worldtube row | KER1071_6_verdict;TAU1071_3_verdict | True | True |  | EXISTS_NEEDLES_CONFIRMED |

## CMSM Portal Route

| branch_id | valid_for_claim | claim_allowed | generated_utc | route_id | source | what_it_provides | current_status | needed_next |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | false | false | 2026-06-20T03:26:51.634925+00:00 | CMSM1999_0_data_inventory_pointer | OCA/MICROSCOPE CMSM REGARDS route | source-backed pointer to raw/calibrated/auxiliary MICROSCOPE data products | ROUTE_STAGED_SCHEMA_NOT_ACQUIRED | browser/manual CMSM session or public REGARDS query with actual file/schema inventory |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | false | false | 2026-06-20T03:26:51.634925+00:00 | CMSM1999_1_REGARDS_api_candidate | REGARDS OpenSearch/GeoJSON/STAC candidate route | possible API/search/download pattern | CANDIDATE_ENDPOINTS_STAGED | working query parameters or UI-derived dataset/file names |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | false | false | 2026-06-20T03:26:51.634925+00:00 | CMSM1999_2_CQG_product_requirements | CQG 2022 data product description | 4 Hz accelerometer measurements, same-stamp attitude/angular rates, minute position/velocity requirements | REQUIREMENTS_RECORDED | actual arrays or source-reconstructed official-equivalent inputs |

## Numeric Kernel Requirements

| branch_id | valid_for_claim | claim_allowed | generated_utc | requirement_id | required_input | why_required | current_status | source_route |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | false | false | 2026-06-20T03:26:51.634925+00:00 | NKR1999_0_exact_time_grid | exact segment timestamps and sample masks | phase of gx/gz/Sxx/Sxz depends on actual timestamps and removed samples | MISSING_EXACT_TIMESTAMPS_AND_MASKS | CMSM 4 Hz accelerometer products or processing metadata |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | false | false | 2026-06-20T03:26:51.634925+00:00 | NKR1999_1_orbit_ephemeris | J2000 satellite position/velocity | compute g(Osat) and gravity-gradient tensor T at satellite centre | MISSING_NUMERIC_EPHEMERIS | CMSM minute-sampled orbit products |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | false | false | 2026-06-20T03:26:51.634925+00:00 | NKR1999_2_attitude_rates | attitude, angular velocity, angular acceleration | rotate gravity into instrument frame and build inertia-gradient correction | MISSING_NUMERIC_ATTITUDE_RATES | CMSM same-stamp attitude products |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | false | false | 2026-06-20T03:26:51.634925+00:00 | NKR1999_3_gravity_model | official gravity model convention or approved surrogate with error bound | do not substitute guessed spherical model for claim-grade kernel | MISSING_OFFICIAL_GRAVITY_MODEL_OR_SURROGATE | MICROSCOPE processing references and auxiliary products |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | false | false | 2026-06-20T03:26:51.634925+00:00 | NKR1999_4_output_arrays | gx, gz, Sxx, Sxz arrays for at least one SUEP pilot segment | first numeric tau_WEP projection component | MISSING_OFFICIAL_NUMERIC_ARRAYS | CMSM products or reproducible reconstruction |

## Segment 210 Dry-Run Ledger

| branch_id | valid_for_claim | claim_allowed | generated_utc | dry_run_id | segment | spin_mode | full_grid_samples | preview_rows_written | phase_convention | kernel_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | false | false | 2026-06-20T03:26:51.634925+00:00 | DRY1999_0_segment210_kernel_preview | 210 | V3 | 1189200 | 32 | dry_run_zero_phase_not_claim | DRY_RUN_NUMERIC_PREVIEW_ONLY_NOT_TAU |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | false | false | 2026-06-20T03:26:51.634925+00:00 | DRY1999_1_reconstruction_path | 210 | V3 | 1189200 | 32 | replace_with_official_phase_and_amplitude_before_scoring | CODE_PATH_EXERCISED_OFFICIAL_ARRAYS_MISSING |

## Tau Status

| branch_id | valid_for_claim | claim_allowed | generated_utc | status_id | object | status | remaining_gap |
| --- | --- | --- | --- | --- | --- | --- | --- |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | false | false | 2026-06-20T03:26:51.634925+00:00 | NTS1999_0_schema_inventory | CMSM schema/file inventory | NOT_ACQUIRED_FROM_LOCAL_PROBE | use browser/manual session or discover public API query parameters |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | false | false | 2026-06-20T03:26:51.634925+00:00 | NTS1999_1_dry_run_preview | segment 210 gx/gz/Sxx/Sxz preview | DRY_RUN_NUMERIC_PREVIEW_ONLY | replace zero-phase/unit-amplitude columns with official arrays |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | false | false | 2026-06-20T03:26:51.634925+00:00 | NTS1999_2_tau_WEP | numeric tau_WEP | NOT_ACQUIRED | official numeric kernel arrays or source-reconstructed arrays with provenance |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | false | false | 2026-06-20T03:26:51.634925+00:00 | NTS1999_3_source_worldtube | Earth/source-worldtube row | NOT_ACQUIRED | source profile/composition convention or calibrated point-source theorem with error bound |

## Runner Dryrun

| branch_id | valid_for_claim | claim_allowed | generated_utc | run_id | check | result | reason |
| --- | --- | --- | --- | --- | --- | --- | --- |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | false | false | 2026-06-20T03:26:51.634925+00:00 | RUN1999_0_portal_route | import CMSM/REGARDS route and requirements | PASS_NONCLAIM_ROUTE | route and candidate endpoints are staged, but schema/products are not acquired |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | false | false | 2026-06-20T03:26:51.634925+00:00 | RUN1999_1_dry_run_preview | import segment-210 dry-run gx/gz/Sxx/Sxz preview | PASS_NONCLAIM_DRY_RUN | preview exercises reconstruction path only; zero-phase/unit amplitude is not physical tau |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | false | false | 2026-06-20T03:26:51.634925+00:00 | RUN1999_2_numeric_tau | promote numeric tau_WEP | FAIL_OFFICIAL_ARRAYS_MISSING | exact timestamps/masks, ephemeris, attitude, gravity model, and official arrays are missing |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | false | false | 2026-06-20T03:26:51.634925+00:00 | RUN1999_3_product_score | score WEP product | FAIL_VALID_PREDICTION_ROWS_ZERO | dry-run kernel is not a prediction and tau_WEP remains missing |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | false | false | 2026-06-20T03:26:51.634925+00:00 | RUN1999_4_verdict | 1999 next-step decision | NEXT_2000_CMSM_SCHEMA_OR_ONE_SEGMENT_OFFICIAL_ARRAY_EXTRACT | the next real move is CMSM UI/API schema capture or one official/reconstructed segment array |

## Claim Gate

| branch_id | valid_for_claim | claim_allowed | generated_utc | gate_id | claim | status | reason |
| --- | --- | --- | --- | --- | --- | --- | --- |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | false | false | 2026-06-20T03:26:51.634925+00:00 | CG1999_0_portal_route | CMSM/REGARDS route is staged | PASS_NONCLAIM_ROUTE | source-backed route exists but file inventory not acquired |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | false | false | 2026-06-20T03:26:51.634925+00:00 | CG1999_1_dry_run_preview | dry-run kernel preview exists | PASS_NONCLAIM_DRY_RUN | code path preview only; not physical tau |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | false | false | 2026-06-20T03:26:51.634925+00:00 | CG1999_2_official_numeric_kernel | official numeric gx/gz/Sxx/Sxz kernel is acquired | FAIL_BLOCKED | official arrays/schema not acquired |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | false | false | 2026-06-20T03:26:51.634925+00:00 | CG1999_3_tau_WEP | tau_WEP is numeric | FAIL_BLOCKED | dry-run preview is not tau_WEP |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | false | false | 2026-06-20T03:26:51.634925+00:00 | CG1999_4_local_GR | WEP/local-GR branch is scored | FAIL_BLOCKED | valid prediction rows remain zero |

## Decision Ledger

| branch_id | valid_for_claim | claim_allowed | generated_utc | decision_id | decision | because | next_action |
| --- | --- | --- | --- | --- | --- | --- | --- |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | false | false | 2026-06-20T03:26:51.634925+00:00 | DEC1999_0_status | PORTAL_ROUTE_AND_DRY_RUN_EXIST_BUT_NUMERIC_TAU_DOES_NOT | 1072 records CMSM/REGARDS route and dry-run preview, but official arrays/schema are not acquired | capture CMSM schema/products or one official/reconstructed segment |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | false | false | 2026-06-20T03:26:51.634925+00:00 | DEC1999_1_dry_run_policy | DRY_RUN_IS_RECONSTRUCTION_PATH_NOT_EVIDENCE | zero-phase/unit-amplitude preview lacks timestamps, masks, ephemeris, attitude, and gravity model | replace dry-run columns with official/source-reconstructed arrays before tau scoring |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | false | false | 2026-06-20T03:26:51.634925+00:00 | DEC1999_2_best_next | CMSM_SCHEMA_OR_ONE_SEGMENT_OFFICIAL_ARRAY_EXTRACT | that is the first step capable of turning kernel skeleton into numeric tau_WEP | 2000-Y5-R2FR-CMSM-schema-or-one-segment-official-array-extract.md |

## Next Target

| branch_id | valid_for_claim | claim_allowed | generated_utc | next_id | selection_status | target_doc | target_script | task | success_condition | do_not |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | false | false | 2026-06-20T03:26:51.634925+00:00 | NEXT1999_0_primary | selected | 2000-Y5-R2FR-CMSM-schema-or-one-segment-official-array-extract.md | scripts/Y5_R2FR_CMSM_schema_or_one_segment_official_array_extract_2000.py | use a browser/manual CMSM session or discovered public REGARDS query to obtain MICROSCOPE file/schema inventory, then replace segment-210 dry-run gx/gz/Sxx/Sxz with official or source-reconstructed arrays for one pilot segment | schema/file inventory or one segment official/source-reconstructed array row with timestamps/masks/provenance; still no WEP/local-GR claim | do not use zero-phase dry-run as evidence, guess masks/amplitudes, set tau_WEP=1, claim WEP/local-GR, push GitHub, or edit formalization-workbench |

## Validation

| validation_id | status | detail | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- |
| VAL1999_00_sources | PASS | all source paths exist and needles found | false | false |
| VAL1999_01_portal_route | PASS | CMSM route staged without claiming schema | false | false |
| VAL1999_02_numeric_requirements | PASS | numeric kernel requirements remain explicit | false | false |
| VAL1999_03_dry_run | PASS | dry-run kernel preview remains nonclaim | false | false |
| VAL1999_04_tau_status | PASS | numeric tau_WEP remains not acquired | false | false |
| VAL1999_05_runner_decision | PASS | runner selects CMSM schema/one-segment extract | false | false |
| VAL1999_06_claim_gates | PASS | only route/dry-run pass as nonclaim | false | false |
| VAL1999_07_next_target | PASS | 2000 CMSM schema/segment target selected | false | false |
| VAL1999_08_claim_flags_safe | PASS | claim flags all false | false | false |
| VAL1999_09_csv_parse | PASS | all generated CSVs parse with rows | false | false |
| VAL1999_10_pycache_absent | PASS | scripts __pycache__ absent | false | false |
| VAL1999_11_formalization_untouched | PASS | formalization_1999_artifact_count=0 | false | false |
| VAL1999_OVERALL | PASS | 1999 MICROSCOPE numeric kernel or source worldtube row | false | false |
