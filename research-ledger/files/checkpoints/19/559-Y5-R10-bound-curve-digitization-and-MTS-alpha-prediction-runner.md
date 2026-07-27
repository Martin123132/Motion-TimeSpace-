# 559 - Y5 R10 Bound-Curve Digitization and MTS Alpha Prediction Runner

Generated: 2026-06-04T12:52:27.210549+00:00  
Run: `runs/20260605-144500-Y5-R10-bound-curve-digitization-and-MTS-alpha-prediction-runner`  
Status: `Y5_R10_bound_curve_digitization_and_MTS_alpha_runner_built_dryrun_blocks_placeholders`  
Claim ceiling: `R10_runner_implementation_dryrun_only_no_fifth_force_Newton_PPN_or_local_GR_pass`

## 1. Verdict

The R10 runner now exists and correctly rejects placeholders.

This is an implementation checkpoint, not a physics pass. The machinery can now compare:

```text
abs(alpha_predicted(lambda_i)) <= alpha_bound(lambda_i)
```

but the current dry-run has zero valid MTS rows and zero valid bound rows, so R10 remains blocked.

## 2. Bound-Curve Digitization Contract

| contract_id | artifact | requirement | current_status | claim_status |
| --- | --- | --- | --- | --- |
| BDC559_0_required_columns | source-intake/local_bounds/R10_alpha_lambda_bound_curve_DIGITIZED.csv | bound_id;dataset_id;lambda_value;lambda_units;alpha_bound;alpha_bound_source;digitization_method;source_file;valid_for_claim;notes | placeholder_schema_written | false |
| BDC559_1_numeric_rows | source-intake/local_bounds/R10_alpha_lambda_bound_curve_DIGITIZED.csv | lambda_value and alpha_bound must be positive numeric values with units convertible to meters | missing_numeric_values | false |
| BDC559_2_source_provenance | source-intake/local_bounds/R10_alpha_lambda_bound_curve_DIGITIZED.csv | each row must cite a bound source and digitization/extraction method | source_named_for_first_placeholder_only_not_digitized | false |
| BDC559_3_interpolation_policy | scripts/R10_alpha_lambda_bound_prediction_runner.py | compare exact matching lambda or log-log interpolate positive bound rows inside sampled range | runner_implemented | false |

## 3. MTS Alpha Runner Spec

| spec_id | runner_requirement | failure_mode | current_status | valid_for_claim |
| --- | --- | --- | --- | --- |
| AR559_0_MTS_schema | MTS curve must use R10_alpha_lambda_curve_MTS_source_normalization.csv schema from checkpoint 558 | missing/non-numeric alpha_predicted or lambda rejects row | implemented | false |
| AR559_1_bound_schema | bound curve must use R10_alpha_lambda_bound_curve_DIGITIZED.csv schema | symbolic alpha(lambda) bound rejects row | implemented | false |
| AR559_2_claim_flag | valid_for_claim must be true on both MTS and bound rows before comparison can support R10 | template rows stay dry-run only | implemented | false |
| AR559_3_comparison_rule | abs(alpha_predicted(lambda)) <= alpha_bound(lambda) for all valid rows | any missing, out-of-range, or exceeding row blocks R10 | implemented | false |
| AR559_4_no_claim_dryrun | dry-run with placeholders must produce R10_pass_for_claim=false | false-positive local GR pass | implemented_and_verified | false |

## 4. Bound Curve Placeholder

| bound_id | dataset_id | lambda_value | lambda_units | alpha_bound | alpha_bound_source | digitization_method | source_file | valid_for_claim | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| R10_BOUND_PLACEHOLDER_0 | Adelberger_Heckel_Nelson_2003_ISL_curve | MISSING_NUMERIC_LAMBDA | m | MISSING_DIGITIZED_ALPHA_BOUND | https://arxiv.org/abs/hep-ph/0307284; doi:10.1146/annurev.nucl.53.041002.110503 | template_invalid_missing_digitized_curve | source-intake/local_bounds/local_bound_claims.csv | false | replace with digitized lambda/alpha_bound rows before R10 scoring |
| R10_BOUND_PLACEHOLDER_1 | future_bound_curve_source | MISSING_NUMERIC_LAMBDA | m | MISSING_DIGITIZED_ALPHA_BOUND | MISSING_BOUND_SOURCE | template_invalid_missing_source | MISSING_SOURCE_FILE | false | additional bound rows can be added from newer/official sources but remain non-claim until sourced |

## 5. Runner Dry-Run Summary

| summary_id | runner_results_dir | mts_rows | valid_mts_rows | bound_rows | valid_bound_rows | comparison_rows | passed_rows | blocked_or_failed_rows | R10_pass_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| R10_RUNNER_559 | runs/20260605-144500-Y5-R10-bound-curve-digitization-and-MTS-alpha-prediction-runner/results/runner | 2 | 0 | 2 | 0 | 1 | 0 | 1 | False | False |

## 6. Runner Blocker Ledger

| blocker_id | blocked_object | reason | repair | valid_for_claim |
| --- | --- | --- | --- | --- |
| RB559_0_MTS_alpha_placeholder | R10_alpha_lambda_curve_MTS_source_normalization.csv | MTS lambda/alpha rows are placeholders | derive source-normalized alpha_predicted(lambda) or theorem-zero | false |
| RB559_1_bound_curve_placeholder | R10_alpha_lambda_bound_curve_DIGITIZED.csv | bound lambda/alpha rows are placeholders | digitize or source machine-readable inverse-square bound curve | false |
| RB559_2_no_valid_rows | R10_runner_comparison.csv | runner has no valid MTS rows and no valid bound rows to compare | fill both sides with source-backed numeric rows and rerun | false |
| RB559_3_no_theorem_zero | R10 no-range branch | no theorem-zero certificate exists as an alternative to curve comparison | derive no-range theorem or keep R10 retained | false |

## 7. Decision

| decision_id | status | meaning | claim_status | next_action |
| --- | --- | --- | --- | --- |
| D559_0_runner_built | R10_bound_prediction_runner_built | R10 now has a reusable curve validator/comparator | dryrun_only | 560-Y5-R10-source-normalized-alpha-law-from-parent-or-runner-real-data-fill.md |
| D559_1_placeholders_blocked | placeholder_dryrun_rejected | runner correctly refuses MTS and bound placeholder rows | R10_pass_false | 560-Y5-R10-source-normalized-alpha-law-from-parent-or-runner-real-data-fill.md |
| D559_2_bound_curve_template_written | bound_curve_digitization_template_written | the expected digitized bound-curve file exists but is non-claim until populated | template_only | 560-Y5-R10-source-normalized-alpha-law-from-parent-or-runner-real-data-fill.md |
| D559_3_local_GR_status | local_GR_still_closure_only | no R10/fifth-force, Cextra, radial closure, Newton, PPN, or local-GR promotion is earned | local_GR_claim_false | 560-Y5-R10-source-normalized-alpha-law-from-parent-or-runner-real-data-fill.md |
| D559_4_private_no_push | private_no_github | no public/GitHub action is performed | safe_private_work | continue_private_derivation |

## 8. Source Register

| source_file | role | exists |
| --- | --- | --- |
| 558-Y5-R10-alpha-lambda-source-normalized-curve-data-or-no-range-theorem.md | R10 no-range theorem failure and placeholder curve file | True |
| 557-Y5-Cextra-bulk-memory-range-positive-operator-zero-or-Yukawa-bound-fill.md | bulk/memory/range Yukawa fill contract | True |
| 437-R10-alpha-lambda-executable-curve-contract.md | R10 alpha(lambda) executable curve rules | True |
| 431-MTS-local-residual-vector-evaluator.md | local evaluator placeholder-rejection policy | True |
| source-intake/mts_residuals/R10_alpha_lambda_curve_MTS_source_normalization.csv | MTS-side alpha(lambda) placeholder curve | True |
| source-intake/local_bounds/R10_alpha_lambda_bound_curve_DIGITIZED.csv | bound-side alpha(lambda) placeholder curve | True |
| source-intake/local_bounds/local_bound_claims.csv | local-bound manifest naming R10 source | True |
| source-intake/mts_residuals/P8_Y5_BRR545_558_VALIDATION.csv | previous validation gate | True |
| source-intake/mts_residuals/P8_Y5_R10_CURVE_DATA_AUDIT.csv | 558 curve-data audit | True |
| source-intake/mts_residuals/P8_Y5_R10_MTS_CURVE_INPUT_CONTRACT.csv | 558 MTS alpha(lambda) input contract | True |
| source-intake/mts_residuals/P8_Y5_R10_ALPHA_LAMBDA_PLACEHOLDER_REJECTION.csv | 558 placeholder rejection ledger | True |
| runs/20260602-004500-bulk-X-mass-gap-source-normalized-force-law/results/source_normalized_force_law.csv | bulk-X source-normalized force-law ledger | True |
| scripts/R10_alpha_lambda_bound_prediction_runner.py | reusable R10 alpha(lambda) runner | True |
| scripts/Y5_R10_bound_curve_digitization_and_MTS_alpha_prediction_runner.py | this checkpoint generator | True |

## 9. Validation

| check_id | result | detail |
| --- | --- | --- |
| V559_0_source_paths_exist | pass | missing=0 |
| V559_1_prior_558_clean | pass | prior_validation_rows=11;prior_fails=0 |
| V559_2_curve_files_loaded | pass | mts_curve_rows=2;bound_curve_rows=2 |
| V559_3_bound_manifest_context_loaded | pass | local_bounds=12;R10_rows=1 |
| V559_4_runner_outputs_written | pass | mts_validation=2;bound_validation=2;comparisons=1 |
| V559_5_runner_blocks_placeholders | pass | valid_mts=0;valid_bound=0;R10_pass=False |
| V559_6_contracts_complete | pass | bound_contract=4;runner_spec=5;blockers=4 |
| V559_7_summary_written | pass | summary_rows=1;R10_pass=False |
| V559_8_no_claim_rows | pass | claim_runner=0;claim_bound=0;claim_mts=0 |
| V559_9_no_overclaim | pass | R10_pass=false; fifth_force=false; Cextra=false; radial_closure=false; Newton=false; PPN=false; local_GR=false |

## 10. Route Update

| route_id | previous_status | new_status | accepted_for_claim | next_target |
| --- | --- | --- | --- | --- |
| R10_FIFTH_FORCE | no_range_failed_expected_curve_file_written_invalid | runner_built_placeholders_rejected_no_R10_pass | false | 560-Y5-R10-source-normalized-alpha-law-from-parent-or-runner-real-data-fill.md |
| LOCAL_RESIDUAL_VECTOR | R10_placeholder_file_exists_but_rejected_for_claim | R10_runner_available_for_future_real_curve_rows | false | 560-Y5-R10-source-normalized-alpha-law-from-parent-or-runner-real-data-fill.md |
| CEXTRA_BULK_MEMORY_RANGE | still_failed_no_range_and_no_alpha_lambda_curve | still_failed_runner_waits_for_real_alpha_prediction_or_no_range_theorem | false | 560-Y5-R10-source-normalized-alpha-law-from-parent-or-runner-real-data-fill.md |
| HAMILTONIAN_EXTRA_CHARGE_SILENCE | still_failed_R10_bulk_memory_range_data_missing | still_failed_R10_runner_dryrun_only | false | 560-Y5-R10-source-normalized-alpha-law-from-parent-or-runner-real-data-fill.md |
| LOCAL_GR_TRANSITION_ROUTE | closure_only_R10_no_range_or_curve_not_available | closure_only_R10_runner_no_claim | false | 560-Y5-R10-source-normalized-alpha-law-from-parent-or-runner-real-data-fill.md |

## 11. Claim Ceiling

Allowed:

```text
MTS has an R10 alpha(lambda) bound/prediction runner.
MTS has an invalid placeholder bound curve file.
MTS dry-run rejection of placeholder rows is verified.
```

Forbidden:

```text
MTS has passed R10/fifth-force.
MTS has produced a real alpha(lambda) prediction.
MTS has produced digitized bound-curve data.
MTS has proved C_extra = 0, radial closure, Newton, PPN, or local GR.
```

## 12. Practical Read

This is a good little machine-room checkpoint. We now have the judge for the R10 round. It is not impressed by vibes. It wants real `lambda`, real `alpha_predicted`, real `alpha_bound`, and source paths.

## 13. Next Target

`560-Y5-R10-source-normalized-alpha-law-from-parent-or-runner-real-data-fill.md`

Next: either derive the MTS source-normalized alpha law from the parent branch, or fill a real runner input file with sourced bound data and non-claim smoke predictions.
