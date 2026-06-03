# 400 - Runner-v3 Numeric Smoke Extension

Private local-bound/numeric-smoke checkpoint. This is not a public WEP, Einstein-Hilbert, Newtonian-limit, PPN, fifth-force, boundary, bulk, domain, cosmology, or unified-field claim.

## 1. Purpose

Checkpoint 397 had a sane same-pipeline GR/null baseline, but mostly toy row-level controls. Checkpoint 400 pushes one step harder: each open local-GR blocker is represented as an explicit residual channel, each channel is mapped to the runner-v3 observable rows it can contaminate, and named coefficient profiles are scored against the same source-lock evaluator.

This is still not a derivation. It is a pressure map for the derivation programme.

## 2. Run Manifest

| Item | Value |
| --- | --- |
| Script | `scripts/runner_v3_numeric_smoke_extension.py` |
| Run directory | `runs/20260602-041500-runner-v3-numeric-smoke-extension` |
| Status | `runner_v3_numeric_smoke_extension_written_GR_null_baseline_sane_channel_bounds_and_retained_residual_sweeps_no_PPN_or_local_GR_pass` |
| Claim ceiling | `runner_v3_numeric_smoke_extension_only_no_WEP_EH_Newton_PPN_fifth_force_boundary_bulk_domain_or_local_GR_pass` |
| Next target | `401-parent-matter-selector-theorem-attempt.md` |

## 3. What Changed

The new evaluator writes:

| Artifact | Role |
| --- | --- |
| `row_equation_map.csv` | symbolic residual equation for each runner-v3 row |
| `channel_map.csv` | parent-action residual channels mapped to affected observables |
| `channel_bound_requirements.csv` | per-row solo bounds for each channel |
| `aggregate_channel_bounds.csv` | tightest required suppression per channel |
| `profile_inputs.csv` | explicit coefficient values used in each smoke profile |
| `numeric_profile_results.csv` | profile x observable severity ratios |
| `symbolic_residual_activation.csv` | fifth-force/operator debts retained unscored |
| `fifth_force_probe.csv` | diagnostic Yukawa alpha(lambda) acceleration ratios, not a source-bound score |

## 4. Hardest Suppressions

The brutal local rows are not gamma and beta first. They are WEP/source, direct coframe if identity is not derived, alpha3/Ward flux, Gdot/G drift, and alpha2/domain-vector leakage.

| channel | bound | row | observable |
| --- | --- | --- | --- |
| bulk_flux_X | 4.000e-20 | R7_alpha3 | alpha3 |
| domain_projector_flux | 4.000e-20 | R7_alpha3 | alpha3 |
| unowned_momentum_flux | 4.000e-20 | R7_alpha3 | alpha3 |
| boundary_species_charge | 2.800e-15 | R1_WEP_source_charge | eta_WEP_source_charge |
| bulk_X_composition_charge | 2.800e-15 | R1_WEP_source_charge | eta_WEP_source_charge |
| coframe_slip_ehat_minus_e | 2.800e-15 | R0_identity_coframe_direct | eta_WEP_direct_geometry |
| source_charge_species_split | 2.800e-15 | R1_WEP_source_charge | eta_WEP_source_charge |
| source_normalization_species_split | 2.800e-15 | R1_WEP_source_charge | eta_WEP_source_charge |
| domain_scale_drift_per_yr | 9.600e-15 | R9_Gdot | Gdot_over_G |
| flux_drift_per_yr | 9.600e-15 | R9_Gdot | Gdot_over_G |

## 5. Profile Results

| profile | over | worst | severity | verdict |
| --- | --- | --- | --- | --- |
| GR_null_baseline | 0 | eta_WEP_direct_geometry | 0 | baseline_sane |
| identity_closure_clean_zero_residuals | 0 | eta_WEP_direct_geometry | 0 | zero_control_only_not_derivation |
| derived_suppression_target_0p1_tightest_bound | 0 | gamma_minus_1 | 0.400017 | inside_budget_if_parent_derives_coefficients |
| edge_tightest_bound | 9 | gamma_minus_1 | 4.00017 | fails_numeric_smoke |
| identity_branch_nonclosure_floor_1e_minus_12 | 3 | alpha3 | 7.500e+07 | fails_numeric_smoke |
| full_floor_all_channels_1e_minus_12 | 4 | alpha3 | 7.500e+07 | fails_numeric_smoke |
| source_charge_floor_1e_minus_14 | 1 | eta_WEP_source_charge | 10.7143 | fails_numeric_smoke |
| boundary_vector_flux_1e_minus_10 | 1 | alpha3 | 2.500e+09 | fails_numeric_smoke |
| domain_projector_1e_minus_10 | 2 | alpha3 | 2.500e+09 | fails_numeric_smoke |
| EH_operator_1e_minus_5 | 0 | gamma_minus_1 | 0.869565 | inside_numeric_rows_but_operator_ledger_retained |
| Gdot_memory_drift_1e_minus_14_per_yr | 1 | Gdot_over_G | 1.04167 | fails_numeric_smoke |
| fifth_force_alpha_1e_minus_5_unscored | 0 | eta_WEP_direct_geometry | 0 | fifth_force_active_unscored_not_numeric_pass |
| unit_coupling_stress | 10 | alpha3 | 7.500e+19 | fails_numeric_smoke |

Interpretation:

- `GR_null_baseline` passing means the evaluator is sane before judging MTS.
- `derived_suppression_target_0p1_tightest_bound` passing means the path is numerically possible if the parent action derives those suppressions.
- `edge_tightest_bound` becoming unstable means budget-edge claims are not evidence.
- `identity_branch_nonclosure_floor_1e_minus_12` failing shows that even tiny unowned source/flux/time residues can kill the local branch.
- Fifth-force and non-EH operator activations remain retained debts, not wins or scalar failures.

## 6. Gate Results

| gate | status | evidence |
| --- | --- | --- |
| source_paths_exist | pass | all cited source paths exist |
| same_evaluator_GR_null_baseline | pass | worst severity 0.0 |
| channel_bound_requirements_written | pass | 30 aggregate channel bounds written |
| retained_residual_profiles_evaluated | pass | 13 profiles x 10 numeric rows |
| over_budget_smoke_detected | pass | edge_tightest_bound;identity_branch_nonclosure_floor_1e_minus_12;full_floor_all_channels_1e_minus_12;source_charge_floor_1e_minus_14;boundary_vector_flux_1e_minus_10;domain_projector_1e_minus_10;Gdot_memory_drift_1e_minus_14_per_yr;unit_coupling_stress |
| conservative_suppression_target_inside | pass | inside_budget_if_parent_derives_coefficients |
| symbolic_fifth_force_and_operator_rows_retained | pass | 15 symbolic activations kept unpromoted |
| local_GR_or_PPN_promoted | fail | numeric smoke is coefficient-pressure only; coefficients are not parent-derived |
| claim_ceiling_enforced | pass | runner_v3_numeric_smoke_extension_only_no_WEP_EH_Newton_PPN_fifth_force_boundary_bulk_domain_or_local_GR_pass |

## 7. Decision

Checkpoint 400 converts runner-v3 from row-level toy controls into a channel-level numeric smoke evaluator. GR/null is sane. A conservative 0.1-tightest-bound profile stays inside numeric locks only by inserted suppressions. Edge, floor, source-charge, boundary/domain/flux, Gdot, and unit profiles expose how violently several local rows fail without parent-derived zero/suppression laws. This is useful pressure, not a PPN or local-GR pass.

Strongest honest read: this is not grim in the “dead theory” sense. It is grim in the useful engineering sense: the tolerances are now explicit. If MTS can derive identity/coframe selection, Ward-owned flux, source-normalized measured GM, no physical domain/projector vector leakage, and EH-only local exterior, the local-GR route has a clear shape. If those remain inserted suppressions, the local branch stays closure-only.

## 8. Next Target

`401-parent-matter-selector-theorem-attempt.md`

Try to turn the cleanest closure into an actual parent theorem:

```text
delta S_matter / delta Z_I | e = 0
```

for every nonmetric local selector variable `Z_I`, or keep `R0` explicitly labelled as closure-only.
