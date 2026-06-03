# 431 - MTS Local Residual Vector Evaluator

Private evaluator checkpoint. This is not a public WEP, Einstein-Hilbert, Newtonian-limit, PPN, fifth-force, flux, domain, cosmology, or unified-field claim.

## 1. Purpose

Checkpoint 428 defined the MTS residual-vector input contract and checkpoint 430 ranked the zero routes. This checkpoint builds the evaluator that will compare a filled MTS residual prediction file against the sourced local-bound constraints.

This run used the blank prediction template as a dry-run. That is intentional: the evaluator must refuse to pass blank numeric rows, placeholder derivation statuses, and symbolic R10/R11 rows.

## 2. Run Manifest

| Item | Value |
| --- | --- |
| Script | `scripts/MTS_local_residual_vector_evaluator.py` |
| Run directory | `runs/20260602-105000-MTS-local-residual-vector-evaluator` |
| Predictions CSV | `source-intake\mts_residuals\MTS_local_residual_predictions_TEMPLATE.csv` |
| Status | `MTS_local_residual_vector_evaluator_written_template_dryrun_blocks_missing_predictions_no_local_GR_pass` |
| Claim ceiling | `MTS_local_residual_vector_evaluator_dryrun_only_no_WEP_EH_Newton_PPN_fifth_force_flux_domain_or_local_GR_pass` |
| Next target | `432-same-frame-matter-functor-zero-route.md` |

## 3. Evaluator Rules

| rule_id | applies_to | fail_status |
| --- | --- | --- |
| numeric_abs_compare | R0-R9 numeric rows | missing_numeric_prediction_no_pass or residual_exceeds_bound |
| symbolic_curve_block | R10 fifth-force alpha(lambda) | symbolic_file_missing_no_pass |
| symbolic_operator_block | R11 non-EH operator coefficients | symbolic_file_missing_no_pass |
| derivation_status_gate | all rows | claim_request_exceeds_derivation_status |
| source_file_gate | claim-bearing rows | source_file_missing_or_placeholder |
| all_rows_or_no_local_GR | full vector | partial_or_template_vector_no_local_GR |

## 4. Prediction File Health

| check | value | status | evidence |
| --- | --- | --- | --- |
| predictions_file_exists | True | pass | research-programme\source-intake\mts_residuals\MTS_local_residual_predictions_TEMPLATE.csv |
| required_columns_present | 16 | pass | 16 columns |
| row_count | 12 | pass | expected 12 local residual rows |
| duplicate_row_ids | 0 | pass | none |

## 5. Evaluation Status Counts

| evaluation_status | row_count |
| --- | --- |
| invalid_or_placeholder_derivation_status_no_pass | 12 |

## 6. Claim Gate Counts

| claim_gate | row_count |
| --- | --- |
| no_claim_requested | 12 |

## 7. Row Evaluation Digest

| row_id | observable | score_value | sourced_upper_bound | evaluation_status | claim_gate |
| --- | --- | --- | --- | --- | --- |
| R0_identity_coframe_direct | eta_WEP_direct_geometry |  | 2.8e-15 | invalid_or_placeholder_derivation_status_no_pass | no_claim_requested |
| R1_WEP_source_charge | eta_WEP_source_charge |  | 2.8e-15 | invalid_or_placeholder_derivation_status_no_pass | no_claim_requested |
| R2_clock_redshift | alpha_clock_redshift |  | 2.48e-05 | invalid_or_placeholder_derivation_status_no_pass | no_claim_requested |
| R3_gamma | gamma_minus_1 |  | 2.3e-05 | invalid_or_placeholder_derivation_status_no_pass | no_claim_requested |
| R4_beta | beta_minus_1 |  | 7.8e-05 | invalid_or_placeholder_derivation_status_no_pass | no_claim_requested |
| R5_alpha1 | alpha1 |  | 1e-04 | invalid_or_placeholder_derivation_status_no_pass | no_claim_requested |
| R6_alpha2 | alpha2 |  | 2e-09 | invalid_or_placeholder_derivation_status_no_pass | no_claim_requested |
| R7_alpha3 | alpha3 |  | 4e-20 | invalid_or_placeholder_derivation_status_no_pass | no_claim_requested |
| R8_xi | xi |  | 4e-09 | invalid_or_placeholder_derivation_status_no_pass | no_claim_requested |
| R9_Gdot | Gdot_over_G |  | 9.6e-15 | invalid_or_placeholder_derivation_status_no_pass | no_claim_requested |
| R10_fifth_force | delta_G_or_fifth_force_yukawa |  | alpha(lambda) | invalid_or_placeholder_derivation_status_no_pass | no_claim_requested |
| R11_EH_operator_ledger | non_EH_operator_coefficients |  | symbolic | invalid_or_placeholder_derivation_status_no_pass | no_claim_requested |

## 8. Missing Prediction Report

| row_id | observable | evaluation_status | needed_next |
| --- | --- | --- | --- |
| R0_identity_coframe_direct | eta_WEP_direct_geometry | invalid_or_placeholder_derivation_status_no_pass | fill numeric residual and derivation source |
| R1_WEP_source_charge | eta_WEP_source_charge | invalid_or_placeholder_derivation_status_no_pass | fill numeric residual and derivation source |
| R2_clock_redshift | alpha_clock_redshift | invalid_or_placeholder_derivation_status_no_pass | fill numeric residual and derivation source |
| R3_gamma | gamma_minus_1 | invalid_or_placeholder_derivation_status_no_pass | fill numeric residual and derivation source |
| R4_beta | beta_minus_1 | invalid_or_placeholder_derivation_status_no_pass | fill numeric residual and derivation source |
| R5_alpha1 | alpha1 | invalid_or_placeholder_derivation_status_no_pass | fill numeric residual and derivation source |
| R6_alpha2 | alpha2 | invalid_or_placeholder_derivation_status_no_pass | fill numeric residual and derivation source |
| R7_alpha3 | alpha3 | invalid_or_placeholder_derivation_status_no_pass | fill numeric residual and derivation source |
| R8_xi | xi | invalid_or_placeholder_derivation_status_no_pass | fill numeric residual and derivation source |
| R9_Gdot | Gdot_over_G | invalid_or_placeholder_derivation_status_no_pass | fill numeric residual and derivation source |
| R10_fifth_force | delta_G_or_fifth_force_yukawa | invalid_or_placeholder_derivation_status_no_pass | supply curve/operator vector or audited theorem-zero source |
| R11_EH_operator_ledger | non_EH_operator_coefficients | invalid_or_placeholder_derivation_status_no_pass | supply curve/operator vector or audited theorem-zero source |

## 9. Gate Results

| gate | status | evidence |
| --- | --- | --- |
| required_source_paths_exist | pass | 0 missing required source paths |
| prediction_file_health | pass | 0 failed health checks |
| all_rows_known_and_aligned | pass | 0 unknown/mismatched rows |
| numeric_predictions_present | not_run | 10 numeric rows missing predictions |
| symbolic_rows_executable_or_theorem_zero | not_run | 2 symbolic rows missing curve/vector/theorem source |
| template_placeholders_blocked | pass | missing predictions and placeholder derivation statuses cannot pass |
| claim_candidates_zero | pass | 0 claim candidates |
| local_GR_candidate | fail | not all rows filled/strong/resolved |
| local_GR_promoted | fail | evaluator dry-run only; no MTS residual vector supplied |
| claim_ceiling_enforced | pass | MTS_local_residual_vector_evaluator_dryrun_only_no_WEP_EH_Newton_PPN_fifth_force_flux_domain_or_local_GR_pass |

## 10. Decision

The MTS local residual-vector evaluator now exists and was dry-run against the blank prediction template. It correctly refuses to pass missing numeric predictions and blocks R10/R11 symbolic placeholders. This is an operational testing scaffold, not an MTS local-GR result.

Practical read: the local empirical machine is now ready to score an actual MTS residual vector. Right now it correctly says: no filled predictions, no local-GR claim. The next physics move is either fill a controlled smoke vector to test mechanics, or go straight after C0/C5 derivations so the first real vector is not just arbitrary zeros.

## 11. Next Target

`432-same-frame-matter-functor-zero-route.md`
