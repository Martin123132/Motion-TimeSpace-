# 411 - Local-Bound Runner-v4 Real-Data Interface

Private local-bound interface checkpoint. This is not a public WEP, Einstein-Hilbert, Newtonian-limit, PPN, fifth-force, flux, domain, cosmology, or unified-field claim.

## 1. Purpose

Checkpoint 410 left `R0` as closure-zero, not theorem-zero. This checkpoint makes the next empirical step safer: real local-bound data can now be attached to runner-v4 rows without changing row states, awarding theorem credit, or letting a closure branch masquerade as GR.

## 2. Run Manifest

| Item | Value |
| --- | --- |
| Script | `scripts/local_bound_runner_v4_real_data_interface.py` |
| Run directory | `runs/20260602-093000-wrapped-evaluate-local-bound-runner-v4-real-data-interface` |
| Status | `local_bound_runner_v4_real_data_interface_written_schema_command_manifest_and_dryrun_guardrails_no_data_claim_no_local_GR_pass` |
| Claim ceiling | `local_bound_runner_v4_real_data_interface_only_no_WEP_EH_Newton_PPN_fifth_force_flux_domain_or_local_GR_pass` |
| Next target | `412-v4-source-charge-channel-map-review.md` |

## 3. Interface Contract

The bounds CSV must contain these columns:

```text
dataset_id, test_arena, row_id, observable, measured_value, one_sigma, upper_bound, units, confidence_label, baseline_model, reference_path_or_url, reference_note
```

The script writes `log.txt`, `status.json`, `DONE.txt`, and machine-readable CSVs under `results/`. Future long runs should be started from VS Code, left to finish, and then this chat can be prompted after the completion marker appears.

## 4. Local Data Targets

| target | row | state | source_lock | status |
| --- | --- | --- | --- | --- |
| WEP_differential_acceleration | R0_identity_coframe_direct | closure_zero | 2.8e-15 | ready_for_bound_csv |
| WEP_source_charge | R1_WEP_source_charge | retained_contingent_budget | 2.8e-15 | ready_for_bound_csv_channel_review_needed |
| clock_redshift | R2_clock_redshift | retained_budget | 3.1e-05 | ready_for_bound_csv |
| Shapiro_gamma | R3_gamma | retained_budget | 2.3e-05 | ready_for_bound_csv |
| perihelion_beta | R4_beta | retained_budget | 7.8e-05 | ready_for_bound_csv |
| preferred_frame_alpha1 | R5_alpha1 | retained_budget | 0.0001 | ready_for_bound_csv |
| preferred_frame_alpha2 | R6_alpha2 | retained_budget | 2e-09 | ready_for_bound_csv |
| self_acceleration_alpha3 | R7_alpha3 | retained_contingent_budget | 4e-20 | ready_for_bound_csv |
| preferred_location_xi | R8_xi | retained_budget | 4e-09 | ready_for_bound_csv |
| Gdot_over_G | R9_Gdot | retained_contingent_budget | 9.6e-15 | ready_for_bound_csv |
| inverse_square_yukawa | R10_fifth_force | unscored_parameterized | alpha(lambda) | symbolic_curve_required_not_scalar_claim |
| non_EH_operator_ledger | R11_EH_operator_ledger | retained_residual | symbolic | symbolic_ledger_required_not_scalar_claim |

## 5. Command Manifest

| command | purpose | wait_policy |
| --- | --- | --- |
| dry_run | create schema, template, target map, and guardrail outputs without external data | safe_short_run |
| evaluate_bounds_csv | evaluate a user-provided local-bound CSV against runner-v4 source locks | run_in_VS_Code_then_prompt_Codex_after_DONE |
| long_run_status_check | check whether a future local-bound evaluation has finished without making Codex wait | manual_status_check |

## 6. Interface Summary

| item | value | status |
| --- | --- | --- |
| targets_mapped | 12 | pass |
| schema_columns | 12 | pass |
| external_bounds_loaded | True | pass |
| external_rows_evaluated | 12 | pass |
| evaluation_errors | 0 | pass |
| claim_allowed_rows | 0 | pass |
| theorem_credit_rows | 0 | pass |

## 7. Gate Results

| gate | status | evidence |
| --- | --- | --- |
| source_paths_exist | pass | all cited source paths exist |
| interface_schema_written | pass | 12 required CSV columns |
| local_targets_mapped_to_runner_rows | pass | 12 of 12 targets mapped |
| dry_run_template_written | pass | 12 template rows generated |
| external_bounds_loaded | pass | 12 external rows evaluated |
| evaluation_errors | pass | 0 validation errors |
| closure_zero_not_promoted | pass | R0 state=closure_zero zero_kind=closure_zero_not_theorem_zero |
| symbolic_rows_protected | pass | 2 symbolic/unscored targets retained |
| no_theorem_credit_or_claim_leaks | pass | theorem_credit=0 claim_allowed=0 |
| local_GR_promoted | fail | real-data interface only; no EH/Newton/PPN/local-GR pass |
| claim_ceiling_enforced | pass | local_bound_runner_v4_real_data_interface_only_no_WEP_EH_Newton_PPN_fifth_force_flux_domain_or_local_GR_pass |

## 8. Decision

Runner-v4 now has a real-data interface contract. The interface names the local-bound targets, writes the required bounds CSV schema, produces a fillable template, validates row IDs against runner-v4, compares supplied numeric bounds to internal source locks where meaningful, and writes log/status/results/DONE artifacts for VS Code runs. It does not claim a local-GR pass, does not promote closure_zero to theorem_zero, and protects fifth-force/operator rows from being flattened into scalar evidence.

Practical read: this is how we stop Python from being the final boss. The interface is boring on purpose: verified data in, row-level pressure out, no accidental victory lap.

## 9. Next Target

`412-v4-source-charge-channel-map-review.md`
