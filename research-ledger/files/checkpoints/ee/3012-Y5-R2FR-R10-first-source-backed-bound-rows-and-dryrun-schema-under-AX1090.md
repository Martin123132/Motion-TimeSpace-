# 3012 — R10 First Source-Backed Bound Rows and Dry-Run Schema under AX1090

Status: `Y5_R2FR_3012_R10_sources_cached_supplement_blocked_nonclaim_dryrun_schema_staged_3013_next`

## Verdict

3012 makes real progress but **does not** unlock an R10 claim.

The good part: the arXiv PDF/source package for Lee et al. 2020 is cached locally, the TeX source anchors the Yukawa definition, the 66-lambda scan, the Fig. 5 alpha-limit role, and the alpha=1 threshold at `38.6 microm`.

The hard blocker: the paper says the numerical signed alpha constraints live in the APS Supplemental Material. Direct unauthenticated fetch of that supplement returned `403`, so 3012 refuses to fabricate a curve. The extracted Fig. 5 bottom-panel PDF contains vector paths, but the axis labels are not text-extractable and the curves are not calibrated into physical `lambda, alpha` rows.

## Source Acquisition Ledger

| source_id | exists | bytes | status | notes |
| --- | --- | --- | --- | --- |
| SRC3012_0_arxiv_abs | True | not_applicable | BROWSED_METADATA_CONFIRMED | arXiv abstract page provides title, submission date, PDF/source links, abstract range statement and DOI links |
| SRC3012_1_arxiv_pdf | True | 856030 | CACHED | primary arXiv PDF cache |
| SRC3012_2_arxiv_source_tar | True | 530474 | CACHED | arXiv TeX source tar cache |
| SRC3012_3_extracted_tex | True | 25056 | EXTRACTED | TeX contains figure captions, Yukawa definition and supplement statement |
| SRC3012_4_fig5b1_vector_pdf | True | 65659 | EXTRACTED_VECTOR_FIGURE | bottom panel of Fig. 5 bound curve figure, vector paths but axis labels not text-extractable |
| SRC3012_5_aps_supplement_attempt | True | 764 | FETCH_ATTEMPT_403_FORBIDDEN | supplement is the preferred numerical alpha-constraint source, but direct unauthenticated fetch failed |

## Source Facts

| fact_id | line_number | description | status |
| --- | --- | --- | --- |
| FACT3012_0_yukawa_potential | 43 | Yukawa parameterization defines alpha and lambda against Newtonian potential | FOUND |
| FACT3012_1_fig5_bottom_limits | 144 | Fig. 5 bottom panel is the alpha(lambda) upper-limit plot | FOUND |
| FACT3012_2_66_lambda_scan | 150 | analysis scanned 66 lambda values | FOUND |
| FACT3012_3_grav_strength_threshold | 151 | alpha=1 threshold anchor in the paper text | FOUND |
| FACT3012_4_supplement_numerical_values | 151 | supplement is the proper numerical source for signed alpha constraints | FOUND |
| FACT3012_5_supplement_torque_values | 193 | TeX reference confirms supplemental numerical values exist, but publisher URL is required | FOUND |

## Figure Vector Audit

| figure_id | operation_count | stroke_path_count | stroke_color_count | extractable_text_chars | axis_calibrated | status |
| --- | --- | --- | --- | --- | --- | --- |
| FIG3012_0_fig5b1 | 20630 | 6742 | 12 | 0 | False | VECTOR_PATHS_PRESENT_AXIS_LABELS_NOT_TEXT_EXTRACTABLE |

## R10 Bound Rows

| curve_row_id | row_kind | lambda_value | alpha_bound | status | valid_bound_curve_row |
| --- | --- | --- | --- | --- | --- |
| R10B3012_0_EotWash_2020_alpha1_anchor | source_text_anchor | 3.86e-5 | 1.0 | ANCHOR_ONLY_NON_CURVE | False |
| R10B3012_1_EotWash_2007_alpha1_anchor | continuity_anchor_from_2410 | 5.6e-5 | 1.0 | ANCHOR_ONLY_NON_CURVE | False |
| R10B3012_2_APS_supplement_full_curve | preferred_numerical_source | MISSING_66_LAMBDA_VALUES | MISSING_SIGNED_ALPHA_CONSTRAINTS | SUPPLEMENTAL_ACCESS_BLOCKED | False |
| R10B3012_3_fig5_vector_digitization_candidate | figure_vector_candidate | MISSING_AXIS_CALIBRATION | MISSING_CURVE_IDENTITY | VECTOR_PRESENT_NOT_DIGITIZED | False |

## Dry-Run Schema

| schema_id | artifact | current_values | failure_mode |
| --- | --- | --- | --- |
| DRY3012_0_required_prediction_row | R10_q_loc_to_alpha_prediction_row | MISSING_K_R10; MISSING_lambda_X; MISSING_C_q_to_alpha; MISSING_q_loc_profile; MISSING_COUPLING_COEFFICIENTS | prediction row is invalid until parent projection coefficients are real |
| DRY3012_1_required_bound_row | R10_alpha_lambda_bound_curve_DIGITIZED | anchors present; full curve missing; supplement blocked; vector figure not calibrated | bound row is invalid for claim unless full_curve_row=true and valid_bound_curve_row=true |
| DRY3012_2_comparison_rule | R10_alpha_comparator | not runnable because both full curve and prediction row are missing | runner returns BLOCKED_NONCLAIM, not pass/fail physics |

## Dry-Run Results

| dryrun_id | check | passed | observed | result_status |
| --- | --- | --- | --- | --- |
| RUN3012_0_bound_curve_gate | any valid full-curve bound rows present | False | 0 valid full-curve rows; anchors are noncurve | BLOCKED_NONCLAIM |
| RUN3012_1_prediction_gate | valid q_loc-to-alpha prediction row present | False | K_R10, lambda_X and C_q_to_alpha missing | BLOCKED_NONCLAIM |
| RUN3012_2_supplement_gate | APS supplemental numerical constraints acquired | False | direct APS fetch returned 403 | BLOCKED_NONCLAIM |
| RUN3012_3_vector_digitization_gate | Fig. 5 vector paths calibrated into data rows | False | vector paths present but axis labels/curve identities not calibrated | BLOCKED_NONCLAIM |
| RUN3012_4_claim_gate | R10 claim allowed | False | bound curve and MTS prediction are both incomplete | CLAIM_FORBIDDEN |

## Promotion Gates

| gate_id | gate | result | notes |
| --- | --- | --- | --- |
| GATE3012_0_source_cache | arXiv PDF/source and Fig. 5 vector source are cached locally | True | source cache exists under source-intake/r10-sources/3012 |
| GATE3012_1_text_facts | TeX source anchors are found | True | Yukawa definition, Fig. 5 limit role, 66 lambda scan, threshold and supplement facts are anchored |
| GATE3012_2_no_live_curve_write | live R10_alpha_lambda_bound_curve_DIGITIZED.csv is not written by 3012 | True | 3012 writes only NONCLAIM curve rows |
| GATE3012_3_anchors_nonclaim | alpha=1 anchors remain nonclaim noncurve | True | anchors are useful for plumbing but not sufficient for alpha(lambda) scoring |
| GATE3012_4_vector_not_promoted | vector figure paths are not promoted without calibration | True | no screen/pixel curve fabrication |
| GATE3012_5_R10_claim | R10 pass claim allowed | False | full curve, q_loc projection and source normalization are missing |

## Decision Ledger

| decision_id | decision | rationale |
| --- | --- | --- |
| DEC3012_0_status | 3012 acquires and caches the arXiv R10 source package, but does not obtain the publisher supplemental numerical curve. | The proper numerical source is the APS supplement; direct unauthenticated access returned 403, and Fig. 5 vector paths are not axis-calibrated data rows. |
| DEC3012_1_bound_rows | Only two alpha=1 anchors are staged, both valid_for_claim=false. | The 38.6 microm statement is useful as a threshold check but cannot replace the 66-lambda alpha(lambda) constraint table. |
| DEC3012_2_next_route | Move to q_loc-to-Yukawa projection derivation while leaving a parallel supplement/manual-digitization import route open. | Even with the curve, R10 cannot score MTS until K_R10, lambda_X and C_q_to_alpha are derived. |

## Next Target

| next_id | target_doc | mission | success_condition |
| --- | --- | --- | --- |
| NEXT3012_0_3013 | 3013-Y5-R2FR-R10-q_loc-to-Yukawa-projection-kernel-or-calibrated-curve-import-under-AX1090.md | Derive the q_loc/Delta_K/coupling-vector to Yukawa alpha(lambda) projection kernel, while preserving a side route for APS supplemental import or calibrated Fig. 5 digitization. | a fail-closed R10 prediction row exists with explicit K_R10, lambda_X, source normalization and units, or a theorem/blocker states exactly which parent coefficient is missing. |

## Validation

| validation_id | passed | requirement | evidence |
| --- | --- | --- | --- |
| VAL3012_00_source_cache | True | arXiv PDF/source, TeX and Fig. 5 vector PDF are cached locally | P8_Y5_R2FR_3012_SOURCE_ACQUISITION_LEDGER.csv |
| VAL3012_01_source_hashes | True | cached local sources have SHA256 hashes | P8_Y5_R2FR_3012_SOURCE_ACQUISITION_LEDGER.csv |
| VAL3012_02_text_facts | True | required TeX source facts are found | P8_Y5_R2FR_3012_SOURCE_FACTS.csv |
| VAL3012_03_aps_blocker_recorded | True | APS supplement access failure is recorded and no partial download is used | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\r10-sources\3012\aps_supplemental_fetch_attempt_3012.log |
| VAL3012_04_csv_parse | True | generated CSV rows parse cleanly | all generated CSV artifacts import with csv.DictReader |
| VAL3012_05_anchors_positive_nonclaim | True | anchor rows have positive numbers but remain nonclaim noncurve | R10B3012_0 and R10B3012_1 |
| VAL3012_06_missing_markers_nonclaim | True | rows with MISSING markers are not valid_for_claim | P8_Y5_R2FR_3012_R10_BOUND_ROWS_NONCLAIM.csv |
| VAL3012_07_no_claim_rows | True | no 3012 row is valid for claim or claim allowed | base() claim fields |
| VAL3012_08_live_curve_not_written | True | live R10_alpha_lambda_bound_curve_DIGITIZED.csv is not modified by this checkpoint | output target list |
| VAL3012_09_outputs_scoped | True | no generated file is outside post-checkpoint-work | generated path scope check |
| VAL3012_10_formalization_not_targeted | True | formalization-workbench is not modified by this checkpoint | output target list excludes formalization-workbench |
| VAL3012_11_next_target_selected | True | next target selects R10 projection-kernel derivation or calibrated curve import | P8_Y5_R2FR_3012_NEXT_TARGET.csv |
| VAL3012_99_overall | True | all 3012 validation checks pass | aggregate of VAL3012_00 through VAL3012_11 |

## Files Written

- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3012_SOURCE_ACQUISITION_LEDGER.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3012_SOURCE_FACTS.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3012_FIGURE_VECTOR_AUDIT.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3012_R10_BOUND_ROWS_NONCLAIM.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3012_QLOC_TO_ALPHA_DRYRUN_SCHEMA.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3012_R10_DRYRUN_RESULTS.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3012_PROMOTION_GATES.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3012_DECISION_LEDGER.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3012_NEXT_TARGET.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3012_BRANCH_COPIES.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_BRR545_3012_VALIDATION.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\local_bounds\R10_alpha_lambda_bound_curve_3012_NONCLAIM.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\local_bounds\q_loc_to_alpha_R10_dryrun_schema_3012_NONCLAIM.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\rab-sector\acquisition-queue\JR3012_R10_QLOC_TO_YUKAWA_KERNEL_OR_SUPPLEMENT_IMPORT_NEXT.csv`

## Hard Guardrails Still Active

- No R10 pass claim.
- No live `R10_alpha_lambda_bound_curve_DIGITIZED.csv` overwrite.
- No anchor-only curve claim.
- No uncalibrated vector-figure digitization claim.
- No hidden-coupling or bound-inversion shortcut.
- No `formalization-workbench` edits.
- No GitHub action.
