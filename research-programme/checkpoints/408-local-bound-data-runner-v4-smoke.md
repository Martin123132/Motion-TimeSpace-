# 408 - Local Bound Data Runner v4 Smoke

Private runner-v4 smoke checkpoint. This is not a public WEP, Einstein-Hilbert, Newtonian-limit, PPN, fifth-force, flux, domain, cosmology, or unified-field claim.

## 1. Purpose

Checkpoint 406 created runner-v4 states. This checkpoint actually runs a smoke evaluator through those states:

- closure-zero is visible but not theorem-zero;
- retained rows are scored against source locks;
- contingent rows score only when channels are activated;
- fifth-force/operator rows remain symbolic or unscored;
- no row is claim-allowed.

## 2. Run Manifest

| Item | Value |
| --- | --- |
| Script | `scripts/local_bound_data_runner_v4_smoke.py` |
| Run directory | `runs/20260602-053500-local-bound-data-runner-v4-smoke` |
| Status | `local_bound_data_runner_v4_smoke_written_closure_retained_contingent_unscored_rows_evaluated_without_theorem_promotion_no_local_GR_pass` |
| Claim ceiling | `local_bound_data_runner_v4_smoke_only_no_WEP_EH_Newton_PPN_flux_fifth_force_or_local_GR_pass` |
| Next target | `409-runner-v4-red-team.md` |

## 3. Profile Summary

| profile | over | symbolic | worst | severity | verdict |
| --- | --- | --- | --- | --- | --- |
| GR_null_baseline | 0 | 0 | eta_WEP_direct_geometry | 0 | baseline_sane |
| identity_closure_zero_control | 0 | 0 | eta_WEP_direct_geometry | 0 | inside_or_inactive_no_promotion |
| retained_0p1_tightest_bound_active | 0 | 2 | gamma_minus_1 | 0.400017 | inside_or_inactive_no_promotion |
| retained_edge_tightest_bound_active | 9 | 2 | gamma_minus_1 | 4.00017 | fails_smoke_no_promotion |
| closure_row_leak_1e_minus_15 | 0 | 0 | eta_WEP_direct_geometry | 0.357143 | inside_or_inactive_no_promotion |
| source_charge_1e_minus_14 | 1 | 1 | eta_WEP_source_charge | 14.2857 | fails_smoke_no_promotion |
| alpha3_flux_1e_minus_20 | 0 | 0 | alpha3 | 0.75 | inside_or_inactive_no_promotion |
| alpha3_flux_1e_minus_15 | 1 | 0 | alpha3 | 7.500e+04 | fails_smoke_no_promotion |
| Gdot_memory_drift_1e_minus_14_per_yr | 1 | 0 | Gdot_over_G | 1.04167 | fails_smoke_no_promotion |
| domain_projector_1e_minus_10 | 2 | 0 | alpha3 | 2.500e+09 | fails_smoke_no_promotion |
| fifth_force_alpha_1e_minus_5_unscored | 0 | 1 | eta_WEP_direct_geometry | 0 | symbolic_unscored_activation_no_promotion |
| unit_coupling_stress | 10 | 2 | alpha3 | 7.500e+19 | fails_smoke_no_promotion |

## 4. State Summary

| state | over | theorem | claims |
| --- | --- | --- | --- |
| closure_zero | 1 | 0 | 0 |
| retained_budget | 12 | 0 | 0 |
| retained_contingent_budget | 11 | 0 | 0 |

## 5. Gate Results

| gate | status | evidence |
| --- | --- | --- |
| source_paths_exist | pass | all cited source paths exist |
| profiles_written | pass | 12 v4 smoke profiles written |
| GR_null_baseline_sane | pass | worst severity 0.0 |
| closure_zero_visible_not_theorem | pass | 7 closure-zero control rows visible |
| over_budget_profiles_detected | pass | retained_edge_tightest_bound_active;source_charge_1e_minus_14;alpha3_flux_1e_minus_15;Gdot_memory_drift_1e_minus_14_per_yr;domain_projector_1e_minus_10;unit_coupling_stress |
| symbolic_unscored_rows_retained | pass | 8 active symbolic/unscored rows retained |
| no_theorem_credit | pass | 0 rows receive theorem credit |
| no_claim_allowed_rows | pass | 0 rows have claim_allowed=true |
| local_GR_promoted | fail | v4 smoke evaluation only; no local-GR pass |
| claim_ceiling_enforced | pass | local_bound_data_runner_v4_smoke_only_no_WEP_EH_Newton_PPN_flux_fifth_force_or_local_GR_pass |

## 6. Decision

Runner-v4 smoke evaluation is now live. It evaluates closure, retained, contingent, symbolic, and unscored rows with the same channel map while preserving the v4 claim discipline. GR/null is sane. The identity closure control is visible but not promoted. Retained and contingent rows fail under source-charge, alpha3-flux, domain/projector, Gdot, edge, and unit-stress profiles as expected. Fifth-force activation remains unscored. No row receives theorem credit and no local-GR/PPN claim is allowed.

Practical read: this is the first local smoke layer that behaves like a referee instead of a cheerleader. Closure branches can be tested, but the machine keeps the word “closure” stamped on them.

## 7. Next Target

`409-runner-v4-red-team.md`
