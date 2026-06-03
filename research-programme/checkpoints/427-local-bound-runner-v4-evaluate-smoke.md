# 427 - Local Bound Runner-v4 Evaluate Smoke

Private evaluate-mode checkpoint. This is not a public WEP, Einstein-Hilbert, Newtonian-limit, PPN, fifth-force, flux, domain, cosmology, or unified-field claim.

## 1. Purpose

Checkpoint 427 filled the verified local-bound source-intake CSV. This checkpoint runs evaluate mode against that file and checks whether the pipeline can process sourced bounds without giving MTS theorem credit by accident.

## 2. Run Manifest

| Item | Value |
| --- | --- |
| Script | `scripts/local_bound_runner_v4_evaluate_smoke.py` |
| Run directory | `runs/20260602-093000-local-bound-runner-v4-evaluate-smoke` |
| Inner evaluate directory | `runs\20260602-093000-wrapped-evaluate-local-bound-runner-v4-real-data-interface` |
| Bounds CSV | `source-intake/local_bounds/local_bound_claims.csv` |
| Status | `local_bound_runner_v4_evaluate_smoke_passed_12_sourced_rows_evaluated_symbolic_rows_deferred_no_MTS_residual_claim_no_local_GR_pass` |
| Claim ceiling | `local_bound_evaluate_smoke_only_no_WEP_EH_Newton_PPN_fifth_force_flux_domain_or_local_GR_pass` |
| Next target | `428-MTS-local-residual-vector-input-contract.md` |

## 3. Inner Evaluate Invocation

| Item | Value |
| --- | --- |
| Command id | `wrapped_runner_v4_evaluate` |
| Exit code | `0` |
| Stdout | `runs/20260602-093000-local-bound-runner-v4-evaluate-smoke/inner_stdout.txt` |
| Stderr | `runs/20260602-093000-local-bound-runner-v4-evaluate-smoke/inner_stderr.txt` |

## 4. Interface Summary

| summary_item | value | status |
| --- | --- | --- |
| targets_mapped | 12 | pass |
| schema_columns | 12 | pass |
| external_bounds_loaded | True | pass |
| external_rows_evaluated | 12 | pass |
| evaluation_errors | 0 | pass |
| claim_allowed_rows | 0 | pass |
| theorem_credit_rows | 0 | pass |

## 5. Bound Status Counts

| data_bound_status | row_count |
| --- | --- |
| external_bound_at_or_stronger_than_internal_lock_no_claim | 10 |
| symbolic_or_curve_input_recorded_no_scalar_pass | 2 |

## 6. Evaluation Digest

| row_id | observable | upper_bound | source_lock | ratio | data_bound_status |
| --- | --- | --- | --- | --- | --- |
| R0_identity_coframe_direct | eta_WEP_direct_geometry | 2.8e-15 | 2.8e-15 | 1 | external_bound_at_or_stronger_than_internal_lock_no_claim |
| R1_WEP_source_charge | eta_WEP_source_charge | 2.8e-15 | 2.8e-15 | 1 | external_bound_at_or_stronger_than_internal_lock_no_claim |
| R2_clock_redshift | alpha_clock_redshift | 2.48e-05 | 3.1e-05 | 0.8 | external_bound_at_or_stronger_than_internal_lock_no_claim |
| R3_gamma | gamma_minus_1 | 2.3e-05 | 2.3e-05 | 1 | external_bound_at_or_stronger_than_internal_lock_no_claim |
| R4_beta | beta_minus_1 | 7.8e-05 | 7.8e-05 | 1 | external_bound_at_or_stronger_than_internal_lock_no_claim |
| R5_alpha1 | alpha1 | 1e-04 | 0.0001 | 1 | external_bound_at_or_stronger_than_internal_lock_no_claim |
| R6_alpha2 | alpha2 | 2e-09 | 2e-09 | 1 | external_bound_at_or_stronger_than_internal_lock_no_claim |
| R7_alpha3 | alpha3 | 4e-20 | 4e-20 | 1 | external_bound_at_or_stronger_than_internal_lock_no_claim |
| R8_xi | xi | 4e-09 | 4e-09 | 1 | external_bound_at_or_stronger_than_internal_lock_no_claim |
| R9_Gdot | Gdot_over_G | 9.6e-15 | 9.6e-15 | 1 | external_bound_at_or_stronger_than_internal_lock_no_claim |
| R10_fifth_force | delta_G_or_fifth_force_yukawa | alpha(lambda) | alpha(lambda) |  | symbolic_or_curve_input_recorded_no_scalar_pass |
| R11_EH_operator_ledger | non_EH_operator_coefficients | symbolic | symbolic |  | symbolic_or_curve_input_recorded_no_scalar_pass |

## 7. Gate Results

| gate | status | evidence |
| --- | --- | --- |
| source_paths_exist | pass | 0 missing source paths |
| claims_csv_exists | pass | research-programme\source-intake\local_bounds\local_bound_claims.csv |
| inner_evaluate_exit_zero | pass | exit_code=0 |
| inner_DONE_exists | pass | research-programme\runs\20260602-093000-wrapped-evaluate-local-bound-runner-v4-real-data-interface\DONE.txt |
| external_bounds_loaded | pass | True |
| external_rows_evaluated | pass | 12 |
| validation_errors_zero | pass | 0 validation errors |
| symbolic_rows_deferred | pass | 2 symbolic rows |
| theorem_credit_zero | pass | 0 theorem-credit rows |
| claim_allowed_zero | pass | 0 claim-allowed rows |
| MTS_residual_vector_loaded | not_run | evaluate smoke used external bounds only, not MTS predictions |
| local_GR_promoted | fail | evaluate smoke only; no WEP/EH/Newton/PPN/fifth-force pass |
| claim_ceiling_enforced | pass | local_bound_evaluate_smoke_only_no_WEP_EH_Newton_PPN_fifth_force_flux_domain_or_local_GR_pass |

## 8. Decision

Evaluate mode successfully reads the verified local_bound_claims.csv, evaluates all 12 local-bound rows, preserves symbolic R10/R11 treatment, and grants zero theorem or claim credit. This makes the pipeline empirically usable, but it still does not test MTS itself until an MTS residual vector is supplied.

Practical read: the empirical harness is now doing what we need. It loads real sourced bounds, keeps symbolic rows symbolic, and refuses to call this a win. The next missing object is the MTS residual vector: what the theory actually predicts for each local row.

## 9. Next Target

`428-MTS-local-residual-vector-input-contract.md`
