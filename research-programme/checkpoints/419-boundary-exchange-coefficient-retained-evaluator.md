# 419 - Boundary Exchange Coefficient Retained Evaluator

Private retained-coefficient/local-GR checkpoint. This is not a public WEP, Einstein-Hilbert, Newtonian-limit, PPN, fifth-force, flux, domain, cosmology, or unified-field claim.

## 1. Purpose

Checkpoint 417 showed boundary-exchange no-hair is not derived. This checkpoint builds the honest fallback: if exchange exists, it becomes an explicit retained coefficient ledger with hard locks, profiles, and no theorem credit.

## 2. Run Manifest

| Item | Value |
| --- | --- |
| Script | `scripts/boundary_exchange_coefficient_retained_evaluator.py` |
| Run directory | `runs/20260602-073500-boundary-exchange-coefficient-retained-evaluator` |
| Status | `boundary_exchange_coefficient_retained_evaluator_written_retained_exchange_coefficients_and_lock_profiles_no_theorem_credit_no_local_GR_pass` |
| Claim ceiling | `boundary_exchange_coefficient_retained_evaluator_only_no_WEP_EH_Newton_PPN_fifth_force_flux_domain_or_local_GR_pass` |
| Next target | `420-relative-current-boundary-generator-theorem-attempt.md` |

## 3. Retained Coefficients

| family | channel | lock | units |
| --- | --- | --- | --- |
| alpha3_spatial_exchange | bulk_flux_X | 4.000e-20 | dimensionless |
| alpha3_spatial_exchange | domain_projector_flux | 4.000e-20 | dimensionless |
| alpha3_spatial_exchange | unowned_momentum_flux | 4.000e-20 | dimensionless |
| Gdot_exchange_drift | domain_scale_drift_per_yr | 9.600e-15 | yr^-1 |
| Gdot_exchange_drift | flux_drift_per_yr | 9.600e-15 | yr^-1 |
| Gdot_exchange_drift | memory_kernel_drift_per_yr | 9.600e-15 | yr^-1 |
| domain_vector_leakage | boundary_vector_B0i | 2.000e-09 | dimensionless |
| domain_vector_leakage | domain_vector_leakage | 2.000e-09 | dimensionless |
| domain_vector_leakage | projector_vector_leakage | 2.000e-09 | dimensionless |
| preferred_location_anisotropy | boundary_tracefree_shear | 4.000e-09 | dimensionless |
| preferred_location_anisotropy | topology_cycle_anisotropy | 4.000e-09 | dimensionless |
| preferred_location_anisotropy | external_domain_anisotropy | 4.000e-09 | dimensionless |
| scalar_radial_boundary_hair | bulk_X_metric_slip | 2.300e-05 | dimensionless |
| scalar_radial_boundary_hair | domain_projector_stress | 2.300e-05 | dimensionless |
| scalar_radial_boundary_hair | boundary_radial_hair | 7.800e-05 | dimensionless |

## 4. Profile Summary

| profile | family | worst | severity | over |
| --- | --- | --- | --- | --- |
| theorem_zero_control | Gdot_exchange_drift | domain_scale_drift_per_yr | 0 | 0 |
| theorem_zero_control | alpha3_spatial_exchange | bulk_flux_X | 0 | 0 |
| theorem_zero_control | domain_vector_leakage | boundary_vector_B0i | 0 | 0 |
| theorem_zero_control | preferred_location_anisotropy | boundary_tracefree_shear | 0 | 0 |
| theorem_zero_control | scalar_radial_boundary_hair | bulk_X_metric_slip | 0 | 0 |
| one_tenth_lock_retained | Gdot_exchange_drift | domain_scale_drift_per_yr | 0.1 | 0 |
| one_tenth_lock_retained | alpha3_spatial_exchange | bulk_flux_X | 0.1 | 0 |
| one_tenth_lock_retained | domain_vector_leakage | boundary_vector_B0i | 0.1 | 0 |
| one_tenth_lock_retained | preferred_location_anisotropy | boundary_tracefree_shear | 0.1 | 0 |
| one_tenth_lock_retained | scalar_radial_boundary_hair | bulk_X_metric_slip | 0.1 | 0 |
| edge_lock_retained | Gdot_exchange_drift | domain_scale_drift_per_yr | 1 | 0 |
| edge_lock_retained | alpha3_spatial_exchange | bulk_flux_X | 1 | 0 |
| edge_lock_retained | domain_vector_leakage | boundary_vector_B0i | 1 | 0 |
| edge_lock_retained | preferred_location_anisotropy | boundary_tracefree_shear | 1 | 0 |
| edge_lock_retained | scalar_radial_boundary_hair | bulk_X_metric_slip | 1 | 0 |
| ten_times_lock_fail | Gdot_exchange_drift | domain_scale_drift_per_yr | 10 | 3 |
| ten_times_lock_fail | alpha3_spatial_exchange | bulk_flux_X | 10 | 3 |
| ten_times_lock_fail | domain_vector_leakage | boundary_vector_B0i | 10 | 3 |
| ten_times_lock_fail | preferred_location_anisotropy | boundary_tracefree_shear | 10 | 3 |
| ten_times_lock_fail | scalar_radial_boundary_hair | bulk_X_metric_slip | 10 | 3 |
| engineering_tiny_1e_minus_15 | Gdot_exchange_drift | domain_scale_drift_per_yr | 0.104167 | 0 |
| engineering_tiny_1e_minus_15 | alpha3_spatial_exchange | bulk_flux_X | 2.500e+04 | 3 |
| engineering_tiny_1e_minus_15 | domain_vector_leakage | boundary_vector_B0i | 5.000e-07 | 0 |
| engineering_tiny_1e_minus_15 | preferred_location_anisotropy | boundary_tracefree_shear | 2.500e-07 | 0 |
| engineering_tiny_1e_minus_15 | scalar_radial_boundary_hair | bulk_X_metric_slip | 4.348e-11 | 0 |

## 5. Gate Results

| gate | status | evidence |
| --- | --- | --- |
| source_paths_exist | pass | all cited source paths exist |
| retained_coefficients_registered | pass | 15 retained coefficient channels registered |
| alpha3_hard_lock_visible | pass | alpha3 exchange lock 4e-20 registered |
| profiles_evaluated | pass | 5 profiles evaluated |
| over_lock_failures_detected | pass | 18 over-lock retained failures |
| no_theorem_credit_or_claim_leaks | pass | theorem_credit=0 claim_allowed=0 |
| local_GR_promoted | fail | retained coefficient evaluator only; no local-GR pass |
| claim_ceiling_enforced | pass | boundary_exchange_coefficient_retained_evaluator_only_no_WEP_EH_Newton_PPN_fifth_force_flux_domain_or_local_GR_pass |

## 6. Decision

Boundary-exchange fallback is now testable. The evaluator registers retained exchange coefficient families, maps them to runner-v4 rows, evaluates simple lock-fraction profiles, and refuses theorem credit or claim allowance. This is the honest fallback if topological no-hair and Ward-owned cancellation remain unproved: exchange physics becomes an explicit coefficient ledger rather than a hidden assumption.

Practical read: this is the testing fallback. If derivation stalls, the exchange branch has numbers, rows, and failure modes instead of hiding behind prose.

## 7. Next Target

`420-relative-current-boundary-generator-theorem-attempt.md`
