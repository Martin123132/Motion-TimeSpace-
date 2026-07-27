# 1966 Y5 R2FR: R2/fR Bound Curve And Parent Coefficient Smoke Runner

Private checkpoint. This adds real source-backed short-range gravity anchors for the R2/fR scalar-mode branch and refuses to treat them as a full alpha(lambda) curve.

Verdict: Lee 2020 and Kapner 2007 provide useful alpha=1 range anchors, but they are anchor-only smoke rows here. A claim-grade R2/fR score still needs a full digitized or machine-readable alpha(lambda) bound curve and an MTS parent coefficient or parent zero theorem.

No R2/fR, EH, Newton, or local-GR claim follows from this checkpoint.

## Local Source Register

| branch | row_id | valid_for_claim | public_claim | created_utc | source_path | purpose | required_needles | status | missing_needles |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | 1965_doc | False | False | 2026-06-20T00:44:17.007821+00:00 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1965-Y5-R2FR-R2-fR-zero-proof-or-executable-R11-bound-row.md | 1966 R2/fR bound curve and parent coefficient smoke runner | ZP1965_6_verdict;SM1965_2_yukawa_alpha;NEXT1965_0_primary | EXISTS_NEEDLES_CONFIRMED |  |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | 1965_validation | False | False | 2026-06-20T00:44:17.009012+00:00 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_BRR545_1965_VALIDATION.csv | 1966 R2/fR bound curve and parent coefficient smoke runner | VAL1965_OVERALL;PASS | EXISTS_NEEDLES_CONFIRMED |  |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | 963_runner_spec | False | False | 2026-06-20T00:44:17.010217+00:00 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_963_R2FR_BOUND_RUNNER_SPEC.csv | 1966 R2/fR bound curve and parent coefficient smoke runner | R2RUN963_2_R10_bound_curve;R2RUN963_4_decision_logic | EXISTS_NEEDLES_CONFIRMED |  |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | 964_runner | False | False | 2026-06-20T00:44:17.011493+00:00 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_964_R2FR_NONCLAIM_RUNNER_RESULT.csv | 1966 R2/fR bound curve and parent coefficient smoke runner | R2RUN964_2_Lee2020_anchor;R2RUN964_VERDICT | EXISTS_NEEDLES_CONFIRMED |  |

## Web Source Ledger

| branch | row_id | valid_for_claim | public_claim | created_utc | source_id | title | url | doi | year | usable_content | full_curve_status | source_quality |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | WEB1966_0_Lee2020_arxiv | False | False | 2026-06-20T00:44:17.011540+00:00 | WEB1966_0_Lee2020_arxiv | New Test of the Gravitational 1/r^2 Law at Separations down to 52 um | https://arxiv.org/abs/2002.11761 | 10.1103/PhysRevLett.124.101101 | 2020 | abstract/source record gives alpha=1 range anchor and experimental separation range | FULL_CURVE_NOT_MACHINE_READABLE_IN_QUICK_PASS | PRIMARY_OR_GROUP_LEDGER |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | WEB1966_1_Lee2020_pdf | False | False | 2026-06-20T00:44:17.011563+00:00 | WEB1966_1_Lee2020_pdf | Lee et al. 2020 PDF | https://arxiv.org/pdf/2002.11761 | 10.1103/PhysRevLett.124.101101 | 2020 | paper figure can potentially be digitized later | DIGITIZATION_REQUIRED | PRIMARY_OR_GROUP_LEDGER |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | WEB1966_2_Kapner2007_arxiv | False | False | 2026-06-20T00:44:17.011581+00:00 | WEB1966_2_Kapner2007_arxiv | Tests of the Gravitational Inverse-Square Law below the Dark-Energy Length Scale | https://arxiv.org/abs/hep-ph/0611184 | 10.1103/PhysRevLett.98.021101 | 2007 | older continuity alpha=1 range anchor | ANCHOR_ONLY_FOR_THIS_CHECKPOINT | PRIMARY_OR_GROUP_LEDGER |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | WEB1966_3_EotWash_publications | False | False | 2026-06-20T00:44:17.011596+00:00 | WEB1966_3_EotWash_publications | Eot-Wash publications page | https://www.npl.washington.edu/eotwash/publications | not_applicable | 2026 | publication provenance for Lee et al. short-range gravity paper | PUBLICATION_LEDGER_ONLY | PRIMARY_OR_GROUP_LEDGER |

## Bound Anchors

| branch | row_id | valid_for_claim | public_claim | created_utc | source_id | lambda_value | lambda_units | alpha_bound | bound_interpretation | extraction_method | curve_role |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | BND1966_0_Lee2020_alpha1_anchor | False | False | 2026-06-20T00:44:17.011631+00:00 | WEB1966_0_Lee2020_arxiv | 38.6 | micrometer | 1.0 | gravitational-strength Yukawa alpha=1 excluded for ranges greater than this anchor at 95 percent confidence | abstract_anchor | anchor_only_non_curve |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | BND1966_1_Kapner2007_alpha1_anchor | False | False | 2026-06-20T00:44:17.011649+00:00 | WEB1966_2_Kapner2007_arxiv | 56.0 | micrometer | 1.0 | older continuity anchor: alpha<=1 down to this length scale at 95 percent confidence | abstract_anchor | anchor_only_non_curve |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | BND1966_2_full_curve_required | False | False | 2026-06-20T00:44:17.011664+00:00 | WEB1966_1_Lee2020_pdf | MISSING_DIGITIZED_CURVE | micrometer | MISSING_DIGITIZED_CURVE | required for claim-grade interpolation/scoring | figure_digitization_required_or_machine_table_needed | full_curve_required |

## MTS Prediction Placeholders

| branch | row_id | valid_for_claim | public_claim | created_utc | operator_family | parameter | value | units | normalization | source_equation | status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | MTS1966_0_parent_coefficient_required | False | False | 2026-06-20T00:44:17.011681+00:00 | R2_fR_scalar_mode | c_R2_or_fRR | MISSING_PARENT_COEFFICIENT | MISSING_UNITS | MISSING_NORMALIZATION | MISSING_SOURCE_EQUATION | REJECT_FOR_CLAIM |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | MTS1966_1_zero_switch_required | False | False | 2026-06-20T00:44:17.011694+00:00 | R2_fR_scalar_mode | c_R2=f_RR=0 | MISSING_PARENT_MINIMALITY_ZERO_CERTIFICATE | not_applicable_if_zero | not_applicable_if_zero | MISSING_PARENT_ACTION_SIGNATURE | REJECT_FOR_CLAIM |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | MTS1966_2_scalar_map_required | False | False | 2026-06-20T00:44:17.011706+00:00 | R2_fR_scalar_mode | alpha_s_lambda_s | MISSING_ALPHA_AND_LAMBDA | alpha_dimensionless_lambda_micrometer | R_plus_cR2R2_or_declared_fR_normalization | MISSING_FORMULA_SOURCE_IN_PARENT_CONTEXT | REJECT_FOR_CLAIM |

## Smoke Runner

| branch | row_id | valid_for_claim | public_claim | created_utc | input_rows | runner_status | reason | accepted_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | SMOKE1966_0_anchor_parse | False | False | 2026-06-20T00:44:17.011720+00:00 | BND1966_0_Lee2020_alpha1_anchor;BND1966_1_Kapner2007_alpha1_anchor | PASS_SCHEMA_ONLY | positive lambda and alpha values parse, but anchor_only_non_curve cannot support interpolation or pass/fail claims | False |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | SMOKE1966_1_full_curve | False | False | 2026-06-20T00:44:17.011734+00:00 | BND1966_2_full_curve_required | REJECTED_MISSING_FULL_CURVE | full digitized curve or machine-readable table required before alpha(lambda) scoring | False |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | SMOKE1966_2_mts_coefficient | False | False | 2026-06-20T00:44:17.011747+00:00 | MTS1966_0_parent_coefficient_required | REJECTED_MISSING_PARENT_COEFFICIENT | MTS coefficient cannot be fitted to external bound | False |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | SMOKE1966_3_zero_switch | False | False | 2026-06-20T00:44:17.011758+00:00 | MTS1966_1_zero_switch_required | REJECTED_ZERO_THEOREM_NOT_PARENT_SIGNED | minimality/no-extension/no-integrated-out-tower certificate missing | False |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | SMOKE1966_4_decision | False | False | 2026-06-20T00:44:17.011770+00:00 | all_rows | R2FR_SMOKE_RUNNER_BLOCKED_NONCLAIM | data plumbing works, but no claim-grade branch exists yet | False |

## Claim Gate

| branch | row_id | valid_for_claim | public_claim | created_utc | claim | status | reason |
| --- | --- | --- | --- | --- | --- | --- | --- |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | CG1966_0_source_anchors | False | False | 2026-06-20T00:44:17.011791+00:00 | Source-backed anchor rows exist. | PASS_NONCLAIM | anchors are smoke data only |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | CG1966_1_full_curve | False | False | 2026-06-20T00:44:17.011805+00:00 | Claim-grade alpha(lambda) full curve exists. | FAIL_BLOCKED | digitized/machine-readable curve missing |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | CG1966_2_mts_prediction | False | False | 2026-06-20T00:44:17.011818+00:00 | MTS supplies c_R2/f_RR or alpha(lambda). | FAIL_BLOCKED | parent coefficient missing |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | CG1966_3_R2FR_score | False | False | 2026-06-20T00:44:17.011829+00:00 | R2/fR residual branch can be scored. | FAIL_BLOCKED | full curve and MTS prediction missing |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | CG1966_4_EH_second_order | False | False | 2026-06-20T00:44:17.011840+00:00 | EH second-order premise is cleared. | FAIL_BLOCKED | R2/fR remains zero-or-bound unresolved |

## Decision Ledger

| branch | row_id | valid_for_claim | public_claim | created_utc | decision | reason | next_action |
| --- | --- | --- | --- | --- | --- | --- | --- |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | DEC1966_0_verdict | False | False | 2026-06-20T00:44:17.011855+00:00 | REAL_ANCHORS_RECORDED_FULL_CURVE_AND_PARENT_COEFFICIENT_MISSING | Lee 2020 and Kapner 2007 anchors are source-backed but not claim-grade curves; MTS still lacks c_R2/f_RR. | do not score R2/fR; acquire full curve or derive zero/coefficient |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | DEC1966_1_next | False | False | 2026-06-20T00:44:17.011867+00:00 | RETURN_TO_PARENT_COEFFICIENT_OR_DIGITIZE_CURVE | A bound curve alone is not enough without MTS prediction, and MTS prediction alone is not enough without source-backed bounds. | next best theory step is parent minimality/coefficient; next empirical step is full curve digitization |

## Next Target

| branch | row_id | valid_for_claim | public_claim | created_utc | priority | target_doc | target_script | objective | acceptance_output | nonclaim_rule |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | NEXT1966_0_primary | False | False | 2026-06-20T00:44:17.011880+00:00 | selected | 1967-Y5-R2FR-parent-minimality-or-R2FR-coefficient-origin.md | scripts/Y5_R2FR_parent_minimality_or_R2FR_coefficient_origin_1967.py | derive the parent minimality/no-extension theorem or identify the coefficient origin for c_R2/f_RR; keep digitized curve acquisition as parallel empirical task | parent zero/coefficient origin proof attempt, or explicit coefficient-origin blocker plus data-acquisition queue | no R2/fR score, EH claim, or Newton claim without zero/coefficient plus source-backed bounds |

## Project Status Snapshot

| branch | row_id | valid_for_claim | public_claim | created_utc | strongest_result | what_improved | still_missing | claim_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | SNAP1966_0_project_position | False | False | 2026-06-20T00:44:17.011893+00:00 | R2/fR empirical plumbing now has real source-backed anchors and a strict refusal path for anchor-only/non-curve data. | The project can no longer handwave higher-curvature tests; it knows exactly what data and parent coefficients are missing. | full alpha(lambda) curve, MTS c_R2/f_RR or zero theorem, scalar screening/regime map, PPN projection, EH/GM/PPN completion | anchor-only smoke data and missing MTS coefficient; no R2/fR or EH claim |

## Validation

| validation_id | status | detail | valid_for_claim | public_claim |
| --- | --- | --- | --- | --- |
| VAL1966_00_local_sources | PASS | local source paths exist and needles found | False | False |
| VAL1966_01_web_sources | PASS | web source strings and provenance recorded | False | False |
| VAL1966_02_anchor_rows | PASS | anchor rows parse positive but remain nonclaim | False | False |
| VAL1966_03_full_curve_missing | PASS | full curve blocker retained | False | False |
| VAL1966_04_mts_placeholders | PASS | MTS parent coefficient placeholders remain rejected | False | False |
| VAL1966_05_smoke_runner | PASS | smoke runner blocks claims | False | False |
| VAL1966_06_claim_gates | PASS | R2/fR and EH claims remain blocked | False | False |
| VAL1966_07_decision | PASS | source anchors/nonclaim decision recorded | False | False |
| VAL1966_08_next_target | PASS | 1967 target selected | False | False |
| VAL1966_09_claim_flags_safe | PASS | claim flags all false | False | False |
| VAL1966_10_csv_parse | PASS | all generated CSVs parse with rows | False | False |
| VAL1966_11_pycache_absent | PASS | scripts __pycache__ absent | False | False |
| VAL1966_12_formalization_untouched | PASS | formalization_1966_artifact_count=0 | False | False |
| VAL1966_OVERALL | PASS | 1966 R2/fR bound curve and parent coefficient smoke runner | False | False |
