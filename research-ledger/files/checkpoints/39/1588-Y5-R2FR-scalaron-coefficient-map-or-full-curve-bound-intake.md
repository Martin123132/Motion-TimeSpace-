# 1588 - R2/fR Scalaron Coefficient Map Or Full Curve Bound Intake

## Verdict
- The scalaron formula is now wired into the R11 beta path: for simple `f(R)=R+c_R2 R^2`, `m_s^2=1/(6 c_R2)`, `lambda_s=sqrt(6 c_R2)`, and `alpha_s=1/3` only in the simple unscreened metric-f(R) regime.
- Current MTS still has no parent-owned `c_R2/fRR` value, units, sign, normalization, screening flag or source path, so no alpha/lambda prediction row is valid.
- The R10 external side is better than empty but still nonclaim: the live curve is placeholder, the 2020 390-row vector curve is a review candidate, and the alpha=1 anchors are not a full curve.
- Anchor backsolves are explicitly refused; the coefficient side is now the bottleneck before curve scoring can matter.
- No R2/fR, R10, beta, EH, Newton, PPN, local-GR, WEP, clock, orbital, conservation or common-matter claim is made.

## Source Register

| source_id | source_path | exists | needle_found | needles |
| --- | --- | --- | --- | --- |
| SRC1588_0_1587_doc | 1587-Y5-R11-beta-vector-first-component-fill-R2FR-RicciWeyl-or-nohair.md | True | True | NEXT_1588_R2FR_SCALARON_COEFFICIENT_MAP_OR_FULL_CURVE_BOUND_INTAKE; FC1587_0_R2FR |
| SRC1588_1_1587_validation | source-intake/mts_residuals/P8_Y5_BRR545_1587_VALIDATION.csv | True | True | VAL1587_OVERALL; PASS |
| SRC1588_2_1587_fill | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1587_FIRST_COMPONENT_FILL_ROWS.csv | True | True | FC1587_0_R2FR; MISSING_PARENT_COEFFICIENT_AND_FULL_CURVE |
| SRC1588_3_962_scalar_fallback | source-intake/mts_residuals/P8_Y5_R10_962_SCALAR_BOUND_FALLBACK_ROWS.csv | True | True | R2B962_1_fR_unscreened_map; 1/3_if_simple_unscreened_metric_fR |
| SRC1588_4_963_runner_spec | source-intake/mts_residuals/P8_Y5_R10_963_R2FR_BOUND_RUNNER_SPEC.csv | True | True | R2RUN963_0_model_input; MISSING_PARENT_INPUT |
| SRC1588_5_963_coefficient_owner | source-intake/mts_residuals/P8_Y5_R10_963_R2FR_COEFFICIENT_OWNER_AUDIT.csv | True | True | CO963_4_verdict; NO_EXECUTABLE_OWNER_FOUND |
| SRC1588_6_965_curve_manifest | source-intake/mts_residuals/P8_Y5_R10_965_R2FR_FULL_CURVE_INTAKE_MANIFEST.csv | True | True | R2FC965_0_Lee2020_full_curve_required; R2FC965_3_MTS_R2FR_prediction_required |
| SRC1588_7_review_candidate | source-intake/local_bounds/R10_alpha_lambda_bound_curve_1034_REVIEW_CANDIDATE_NONCLAIM.csv | True | True | R10_VECTOR_2020_REVIEW_0000; review_candidate_only_requires_official_supplement_or_human_visual_QA |
| SRC1588_8_review_qa | source-intake/local_bounds/P8_Y5_R10_570_REVIEW_CANDIDATE_QA.csv | True | True | QA570_2_promotion_gate; blocked=2 |
| SRC1588_9_review_summary | source-intake/local_bounds/P8_Y5_R10_570_REVIEW_CURVE_SUMMARY.csv | True | True | CS570_0_rows; 390 |
| SRC1588_10_live_digitized | source-intake/local_bounds/R10_alpha_lambda_bound_curve_DIGITIZED.csv | True | True | MISSING_DIGITIZED_ALPHA_BOUND; R10_BOUND_PLACEHOLDER_0 |
| SRC1588_11_anchor_smoke | source-intake/local_bounds/R10_alpha_lambda_bound_curve_ANCHOR_SMOKE.csv | True | True | R10_ANCHOR_EOTWASH_2020_ALPHA1_38P6UM; R10_ANCHOR_EOTWASH_2007_ALPHA1_56UM |
| SRC1588_12_local_bounds | source-intake/local_bounds/local_bound_claims.csv | True | True | Will_2014_PPN_beta_table; beta_minus_1; 7.8e-05 |

## Scalaron Map

| map_id | map_piece | formula_or_rule | effect_if_filled | status | blocking_gap |
| --- | --- | --- | --- | --- | --- |
| SC1588_0_parent_zero | parent theorem-zero route | c_R2=c_fR=0 if the parent local exterior is metric-only, second-order and no-extra-scalar | lambda_s=0-equivalent/no finite scalaron range; alpha_s=0 for the removed branch | ZERO_THEOREM_UNSIGNED | parent activator still missing from 963/964/1587 |
| SC1588_1_formula | finite scalaron formula | for f(R)=R+c_R2 R^2 around flat space, m_s^2=1/(6 c_R2), lambda_s=sqrt(6 c_R2) in c=hbar=1 units | maps a sourced c_R2/fRR into scalar range | FORMULA_AVAILABLE_PARENT_COEFFICIENT_MISSING | c_R2/fRR value, units and normalization are missing |
| SC1588_2_coupling | simple unscreened metric f(R) coupling | alpha_s=1/3 only for the simple unscreened metric f(R) scalar with universal matter coupling | would give the Yukawa amplitude convention for R10 only under stated regime | CONDITIONAL_COUPLING_NOT_MTS_PREDICTION | screening flag, matter coupling and branch context are missing |
| SC1588_3_units_sign | coefficient units and sign guard | c_R2 has length^2/inverse-mass-squared units after EH normalization; c_R2>0 is required for non-tachyonic scalaron in the simple branch | prevents dimensionless or sign-ambiguous curve scoring | MISSING_UNITS_AND_SIGN_CONVENTION | no parent coefficient row supplies units or sign |
| SC1588_4_screening_regime | screening and solar-system regime | R10/PPN scoring requires unscreened/screened context, source/test coupling, and whether the scalar range lies in lab or solar-system regime | prevents transferring alpha(lambda) anchors into PPN or beta by hand | MISSING_SCREENING_AND_REGIME_MAP | no scalar environment/readout map exists |
| SC1588_5_verdict | MTS R2/fR scalaron prediction | c_R2/fRR, lambda_s, alpha_s, screening flag, source path and normalization all present | would create a nonclaim prediction row eligible for strict curve comparison | FAIL_CURRENT_CLAIM_NO_SCALARON_PREDICTION | formula exists, but the MTS coefficient does not |

## Full Curve Intake Status

| curve_id | curve_type | path_or_source | row_count | curve_status | status | evidence |
| --- | --- | --- | --- | --- | --- | --- |
| CURVE1588_0_live_digitized | live claim curve | source-intake/local_bounds/R10_alpha_lambda_bound_curve_DIGITIZED.csv | 2 | placeholder_invalid | BLOCKED_NOT_A_CURVE | MISSING_DIGITIZED_ALPHA_BOUND rows remain in the live file |
| CURVE1588_1_review_candidate | 2020 Eot-Wash vector review candidate | source-intake/local_bounds/R10_alpha_lambda_bound_curve_1034_REVIEW_CANDIDATE_NONCLAIM.csv | 390 | review_candidate_nonclaim | AVAILABLE_FOR_SMOKE_NOT_CLAIM | axis-calibrated 390-row candidate exists, but promotion gate requires official supplement or human visual QA |
| CURVE1588_2_anchor_smoke | anchor-only smoke rows | source-intake/local_bounds/R10_alpha_lambda_bound_curve_ANCHOR_SMOKE.csv | 2 | anchor_only_non_curve | BLOCKED_ANCHOR_ONLY | 2020 and 2007 alpha=1 thresholds are source-backed anchors only |
| CURVE1588_3_required_promotion | claim-grade bound curve | official supplemental table or review candidate promotion package | 0 | required_for_claim | MISSING_PROMOTED_FULL_CURVE | positive numeric lambda/alpha rows, source URL/DOI, extraction method, curve identity, visual/official QA and valid_for_claim=true |

## Nonclaim Smoke Rows

| smoke_id | case | input_or_formula | blocking_gap | verdict |
| --- | --- | --- | --- | --- |
| SMOKE1588_0_formula_only | finite scalaron formula row | lambda_s=sqrt(6 c_R2), alpha_s=1/3 if simple unscreened metric f(R) | MISSING_C_R2_OR_FRR | REJECTED_MISSING_MTS_PREDICTION |
| SMOKE1588_1_anchor_backsolve | set lambda_s=38.6um because alpha=1 anchor exists | backsolves a prediction from the bound | FORBIDDEN_BOUND_TO_PREDICTION_INVERSION | REJECTED_CLOSURE_ONLY |
| SMOKE1588_2_review_candidate_curve | use 390-row review candidate curve for smoke only | candidate rows are valid_for_claim=false and MTS prediction is absent | NONCLAIM_CURVE_ONLY | NOT_SCORED |
| SMOKE1588_3_parent_zero_if_signed | zero theorem route | if parent activator signs, c_R2=c_fR=0 and finite R2/fR scalar branch is absent | ZERO_THEOREM_UNSIGNED | REJECTED_UNTIL_PARENT_SIGNED |

## Scalaron Runner

| runner_id | case | status | reason | can_score |
| --- | --- | --- | --- | --- |
| RUN1588_0_parent_zero | score parent zero theorem route | NOT_RUN_ZERO_THEOREM_UNSIGNED | parent second-order/no-extra-scalar/minimality activator is not signed | False |
| RUN1588_1_scalaron_prediction | build MTS alpha/lambda prediction | NOT_RUN_COMPONENTS_MISSING | c_R2/fRR, units, normalization, alpha_s and screening flag are missing | False |
| RUN1588_2_live_curve | score against live digitized curve | NOT_RUN_PLACEHOLDER_CURVE | live file contains placeholder MISSING_DIGITIZED_ALPHA_BOUND rows | False |
| RUN1588_3_review_candidate | smoke against review candidate curve | NOT_RUN_PREDICTION_MISSING | review candidate exists but valid_for_claim=false and no MTS prediction exists | False |
| RUN1588_4_anchor_rows | score using alpha=1 anchors | REFUSE_ANCHOR_ONLY_SCORING | anchor thresholds are not a full alpha(lambda) curve | False |
| RUN1588_5_beta_local_gr | claim beta/local-GR from R2/fR handling | BLOCKED_NO_CLAIM | R2/fR scalar branch, R11 vector, source normalization and local-GR gates remain open | False |

## Claim Gates

| gate_id | claim | status | reason |
| --- | --- | --- | --- |
| GATE1588_0_parent_zero | R2/fR theorem-zero | BLOCKED_NO_CLAIM | parent zero activator remains unsigned |
| GATE1588_1_scalaron_prediction | MTS scalaron alpha/lambda prediction | BLOCKED_NO_CLAIM | c_R2/fRR, lambda_s and alpha_s are missing |
| GATE1588_2_full_curve | claim-grade R10 bound curve | BLOCKED_NO_CLAIM | live curve is placeholder; review candidate and anchors are nonclaim |
| GATE1588_3_R10_score | finite R2/fR R10 score | BLOCKED_NO_CLAIM | prediction and claim-grade curve are both missing |
| GATE1588_4_beta_local_gr | beta/local-GR promotion | BLOCKED_NO_CLAIM | R2/fR handling alone does not close the R11/source/matter/conservation gates |

## Decision

| decision_id | decision | reason | consequence |
| --- | --- | --- | --- |
| DEC1588_0_formula_status | SCALARON_FORMULA_AVAILABLE_NOT_MTS_PREDICTION | the R2/fR scalaron formula and simple alpha_s=1/3 convention exist, but no parent c_R2/fRR coefficient exists | do not create an alpha/lambda prediction row |
| DEC1588_1_curve_status | REVIEW_CURVE_AVAILABLE_NONCLAIM_LIVE_CURVE_PLACEHOLDER | a 390-row review candidate exists and anchors exist, but promotion is blocked and the live curve remains placeholder | do not score claims; use candidate only for future smoke after prediction exists |
| DEC1588_2_priority | MTS_COEFFICIENT_SIDE_IS_NOW_THE_BOTTLENECK | without c_R2/fRR, even a perfect full curve cannot test the branch | hunt parent coefficient/scalaron normalization before spending effort on curve promotion |
| DEC1588_3_next | NEXT_1589_R2FR_PARENT_COEFFICIENT_SOURCE_HUNT_OR_CURVE_QA_PROMOTION | the next step should try to derive/source c_R2/fRR from the R11 parent branch; if that fails, prepare strict curve-promotion QA as a separate nonclaim utility | derive coefficient first; curve QA second; no anchor-only score |

## Validation

| check_id | result | detail |
| --- | --- | --- |
| VAL1588_0_sources_exist | PASS | all cited 1588 source paths exist |
| VAL1588_1_needles_found | PASS | all 1588 source needles found |
| VAL1588_2_scalaron_map_blocks | PASS | scalaron formula exists but no MTS prediction is promoted |
| VAL1588_3_curve_intake_blocks | PASS | live curve is placeholder while 390-row review candidate remains nonclaim |
| VAL1588_4_smoke_rows_nonclaim | PASS | smoke rows reject anchor backsolve and remain nonclaim |
| VAL1588_5_runner_blocks | PASS | runner blocks parent-zero, scalaron, curve and local-GR scoring |
| VAL1588_6_claim_gates_closed | PASS | all 1588 claim gates remain closed |
| VAL1588_7_decision_next | PASS | decision selects parent coefficient hunt or curve QA promotion |
| VAL1588_8_csv_parse | PASS | all generated 1588 CSVs parse cleanly |
| VAL1588_9_claim_flags_false | PASS | all generated prediction/claim flags remain false |
| VAL1588_10_no_raw_accepted | PASS | no 1588 rows written to raw/accepted finite directories |
| VAL1588_11_branch_copies | PASS | branch/quarantine nonclaim copies written |
| VAL1588_12_pycache_absent | PASS | scripts __pycache__ absent after run |
| VAL1588_13_formalization_untouched | PASS | all generated 1588 paths are outside formalization-workbench; git status is clean when available |
| VAL1588_OVERALL | PASS | 1588 R2/fR scalaron coefficient map or full curve bound intake validation |

## Next Target

| next_target | script | objective | do_not |
| --- | --- | --- | --- |
| 1589-Y5-R2FR-parent-coefficient-source-hunt-or-curve-QA-promotion.md | scripts/Y5_R2FR_parent_coefficient_source_hunt_or_curve_QA_promotion.py | try to derive or source c_R2/fRR from the parent R11 branch; if unavailable, build the exact curve QA/promotion gate for the existing 390-row Eot-Wash 2020 review candidate without claim promotion | do not backsolve c_R2 from R10 anchors, do not score review-candidate curves as claims, and do not promote beta/local-GR from formula-only rows |
