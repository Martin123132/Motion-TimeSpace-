# 426 - Local Bound Runner-v4 Dry-Run Wrapper

Private testing workflow checkpoint. This is not a public WEP, Einstein-Hilbert, Newtonian-limit, PPN, fifth-force, flux, domain, cosmology, or unified-field claim.

## 1. Purpose

Checkpoint 425 gave us the EH-operator/source-normalization ledger. This checkpoint makes the first testing move: run the local-bound runner-v4 interface in dry-run mode, verify its artifacts, join it to the retained ledger, and prepare a source-intake template without treating template locks as data.

This is the boring bit that matters. If the pipeline cannot keep GR/null baselines, symbolic rows, and source-normalization channels honest, any later "hit" is just footwork on a banana skin.

## 2. Run Manifest

| Item | Value |
| --- | --- |
| Script | `scripts/local_bound_runner_v4_dryrun_wrapper.py` |
| Run directory | `runs/20260602-091000-local-bound-runner-v4-dryrun-wrapper` |
| Inner dry-run directory | `runs\20260602-091000-wrapped-dryrun-local-bound-runner-v4-real-data-interface` |
| Status | `local_bound_runner_v4_dryrun_wrapper_written_inner_dryrun_passed_source_intake_template_ready_no_data_claim_no_local_GR_pass` |
| Claim ceiling | `local_bound_runner_v4_dryrun_wrapper_only_no_WEP_EH_Newton_PPN_fifth_force_flux_domain_or_local_GR_pass` |
| Next target | `427-source-normalization-bounds-csv-template-fill.md` |

## 3. Inner Dry-Run Invocation

| Item | Value |
| --- | --- |
| Command id | `wrapped_runner_v4_dry_run` |
| Exit code | `0` |
| Stdout | `runs/20260602-091000-local-bound-runner-v4-dryrun-wrapper/inner_stdout.txt` |
| Stderr | `runs/20260602-091000-local-bound-runner-v4-dryrun-wrapper/inner_stderr.txt` |

## 4. Inner Artifact Check

| artifact | exists | row_count | status |
| --- | --- | --- | --- |
| command_manifest.csv | True | 3 | pass |
| decision.csv | True | 1 | pass |
| external_bound_evaluation.csv | True | 0 | pass |
| gate_results.csv | True | 11 | pass |
| interface_contract.csv | True | 6 | pass |
| interface_schema.csv | True | 12 | pass |
| interface_summary.csv | True | 7 | pass |
| local_bounds_template.csv | True | 12 | pass |
| local_data_targets.csv | True | 12 | pass |
| next_queue.csv | True | 3 | pass |
| source_register.csv | True | 10 | pass |
| validation_errors.csv | True | 0 | pass |

## 5. Schema and Claim Validation

| check | observed | expected | status |
| --- | --- | --- | --- |
| local_data_targets_count | 12 | 12 | pass |
| local_bounds_template_count | 12 | 12 | pass |
| validation_errors_count | 0 | 0 | pass |
| external_bounds_loaded | False | False | pass |
| claim_allowed_rows | 0 | 0 | pass |
| theorem_credit_rows | 0 | 0 | pass |
| inner_claim_ceiling | pass | pass | pass |
| EH_operator_ledger_count | 10 | 10 | pass |
| source_normalization_channel_count | 7 | 7 | pass |
| local_bound_test_matrix_count | 12 | 12 | pass |

## 6. Ledger-to-Runner Join

| test_id | row_prefix | joined_row_id | join_status |
| --- | --- | --- | --- |
| GR_null_baseline_same_pipeline | R0 | R0_identity_coframe_direct | pass |
| GR_null_baseline_same_pipeline | R1 | R1_WEP_source_charge | pass |
| GR_null_baseline_same_pipeline | R2 | R2_clock_redshift | pass |
| GR_null_baseline_same_pipeline | R3 | R3_gamma | pass |
| GR_null_baseline_same_pipeline | R4 | R4_beta | pass |
| GR_null_baseline_same_pipeline | R5 | R5_alpha1 | pass |
| GR_null_baseline_same_pipeline | R6 | R6_alpha2 | pass |
| GR_null_baseline_same_pipeline | R7 | R7_alpha3 | pass |
| GR_null_baseline_same_pipeline | R8 | R8_xi | pass |
| GR_null_baseline_same_pipeline | R9 | R9_Gdot | pass |
| GR_null_baseline_same_pipeline | R10 | R10_fifth_force | pass |
| GR_null_baseline_same_pipeline | R11 | R11_EH_operator_ledger | pass |
| identity_closure_zero_control | R0 | R0_identity_coframe_direct | pass |
| EH_operator_symbolic_ledger_dryrun | R11 | R11_EH_operator_ledger | pass |
| scalar_mode_range_sweep_placeholder | R3 | R3_gamma | pass |
| scalar_mode_range_sweep_placeholder | R4 | R4_beta | pass |
| scalar_mode_range_sweep_placeholder | R10 | R10_fifth_force | pass |
| scalar_mode_range_sweep_placeholder | R11 | R11_EH_operator_ledger | pass |
| source_normalization_four_channel_R1 | R1 | R1_WEP_source_charge | pass |
| Cassini_gamma_row | R3 | R3_gamma | pass |
| perihelion_beta_row | R4 | R4_beta | pass |
| preferred_frame_vector_rows | R5 | R5_alpha1 | pass |
| preferred_frame_vector_rows | R6 | R6_alpha2 | pass |
| preferred_frame_vector_rows | R7 | R7_alpha3 | pass |
| preferred_frame_vector_rows | R8 | R8_xi | pass |
| Gdot_source_drift_row | R9 | R9_Gdot | pass |
| fifth_force_curve_row | R10 | R10_fifth_force | pass |
| boundary_exchange_retained_rows | R3 | R3_gamma | pass |
| boundary_exchange_retained_rows | R4 | R4_beta | pass |
| boundary_exchange_retained_rows | R7 | R7_alpha3 | pass |
| boundary_exchange_retained_rows | R8 | R8_xi | pass |
| boundary_exchange_retained_rows | R9 | R9_Gdot | pass |
| same_frame_vs_frame_split_counterexample | R2 | R2_clock_redshift | pass |
| same_frame_vs_frame_split_counterexample | R3 | R3_gamma | pass |
| same_frame_vs_frame_split_counterexample | R4 | R4_beta | pass |
| same_frame_vs_frame_split_counterexample | R11 | R11_EH_operator_ledger | pass |

## 7. Baseline Controls

| test_id | target_rows | baseline_status | claim_policy |
| --- | --- | --- | --- |
| GR_null_baseline_same_pipeline | R0-R11 | pass | baseline_only |
| identity_closure_zero_control | R0 | pass | control_only |
| EH_operator_symbolic_ledger_dryrun | R11 | pass | no_symbolic_pass |
| scalar_mode_range_sweep_placeholder | R3;R4;R10;R11 | pass | defer |
| source_normalization_four_channel_R1 | R1 | pass | retain_full_channel |
| Cassini_gamma_row | R3 | pass | numeric_only |
| perihelion_beta_row | R4 | pass | numeric_only |
| preferred_frame_vector_rows | R5;R6;R7;R8 | pass | numeric_only |
| Gdot_source_drift_row | R9 | pass | numeric_only |
| fifth_force_curve_row | R10 | pass | no_symbolic_pass |
| boundary_exchange_retained_rows | R3;R4;R7;R8;R9 | pass | retained_coefficients_only |
| same_frame_vs_frame_split_counterexample | R2;R3;R4;R11 | pass | counterexample_guard |

Every test keeps `baseline_required=yes`. This is the fair-fight rule: if MTS is scored under a stress test, the GR/null baseline is scored in the same pipeline instead of being assumed clean by vibes.

## 8. Source-Intake Template

| artifact | exists | purpose |
| --- | --- | --- |
| local_bound_claims_TEMPLATE.csv | True | editable copy of dry-run template; not empirical evidence |
| README.md | True | source-intake rules and no-claim warning |
| local_bound_claims.csv | False | future verified external/local bound file; absent is correct at dry-run stage |

Future evaluate command after verified sources are filled:

```powershell
$py = 'research-programme\.venv-score\Scripts\python.exe'; $pc = '[local-MTS-workspace]\post-checkpoint-work'; & $py (Join-Path $pc 'scripts\local_bound_runner_v4_real_data_interface.py') --mode evaluate --bounds-csv (Join-Path $pc 'source-intake\local_bounds\local_bound_claims.csv')
```

Do not run that as a claim until `source-intake/local_bounds/local_bound_claims.csv` contains verified external/local source rows. The generated template is a scaffold, not empirical evidence.

## 9. Gate Results

| gate | status | evidence |
| --- | --- | --- |
| source_paths_exist | pass | 0 missing source paths |
| inner_dry_run_exit_zero | pass | exit_code=0 |
| inner_DONE_exists | pass | research-programme\runs\20260602-091000-wrapped-dryrun-local-bound-runner-v4-real-data-interface\DONE.txt |
| inner_required_artifacts_exist | pass | 0 missing artifacts |
| inner_required_csvs_well_formed | pass | 0 malformed artifacts |
| schema_validation_passed | pass | 0 failed schema checks |
| ledger_rows_join_runner_targets | pass | 0 missing row joins |
| GR_null_baseline_required | pass | 0 test rows without baseline requirement |
| source_intake_template_written | pass | 0 required source-intake artifacts missing |
| real_claims_file_absent_in_dryrun | pass | local_bound_claims.csv not created by wrapper |
| external_data_loaded | not_run | dry-run wrapper only; no external data evaluated |
| local_GR_promoted | fail | no WEP/EH/Newton/PPN/fifth-force pass claimed |
| claim_ceiling_enforced | pass | local_bound_runner_v4_dryrun_wrapper_only_no_WEP_EH_Newton_PPN_fifth_force_flux_domain_or_local_GR_pass |

## 10. Decision

The local-bound runner-v4 dry-run now executes through a wrapper that checks the inner interface artifacts, preserves the EH/source retained ledger, writes a source-intake template, and refuses local-GR theorem credit. The project is ready for the next testing move: fill a verified local-bound CSV and evaluate it against the same baseline-aware pipeline.

Practical read: we are now testing-ready in the narrow local-bound sense. The next step is not to celebrate; it is to fill or source the bounds CSV cleanly, run a short evaluate smoke, and see which retained channels actually bite.

## 11. Next Target

`427-source-normalization-bounds-csv-template-fill.md`
