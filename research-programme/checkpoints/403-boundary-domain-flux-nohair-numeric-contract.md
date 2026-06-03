# 403 - Boundary Domain Flux No-Hair Numeric Contract

Private boundary/domain/flux local-GR checkpoint. This is not a public PPN, fifth-force, source-normalization, boundary, bulk, domain, cosmology, or unified-field claim.

## 1. Purpose

Checkpoint 400 showed the ugly part clearly: local GR is not mainly waiting on a pretty gamma/beta sentence. The hardest rows are unowned flux, domain/projector flux, bulk-X flux, source charge, and secular drift.

This checkpoint turns those rows into a numeric no-hair contract.

## 2. Run Manifest

| Item | Value |
| --- | --- |
| Script | `scripts/boundary_domain_flux_nohair_numeric_contract.py` |
| Run directory | `runs/20260602-044500-boundary-domain-flux-nohair-numeric-contract` |
| Status | `boundary_domain_flux_nohair_numeric_contract_written_alpha3_flux_hardest_rows_explicit_conditional_exits_not_parent_derived_no_PPN_or_local_GR_pass` |
| Claim ceiling | `boundary_domain_flux_nohair_numeric_contract_only_no_boundary_bulk_domain_flux_PPN_fifth_force_source_or_local_GR_pass` |
| Next target | `404-selector-blind-matter-axiom-origin.md` |

## 3. Hardest Channel Ceilings

| channel | ceiling | units | observable |
| --- | --- | --- | --- |
| bulk_flux_X | 4.000e-20 | dimensionless | alpha3 |
| domain_projector_flux | 4.000e-20 | dimensionless | alpha3 |
| unowned_momentum_flux | 4.000e-20 | dimensionless | alpha3 |
| boundary_species_charge | 2.800e-15 | dimensionless | eta_WEP_source_charge |
| bulk_X_composition_charge | 2.800e-15 | dimensionless | eta_WEP_source_charge |
| source_charge_species_split | 2.800e-15 | dimensionless | eta_WEP_source_charge |
| source_normalization_species_split | 2.800e-15 | dimensionless | eta_WEP_source_charge |
| domain_scale_drift_per_yr | 9.600e-15 | yr^-1 | Gdot_over_G |
| flux_drift_per_yr | 9.600e-15 | yr^-1 | Gdot_over_G |
| geff_meff_drift_per_yr | 9.600e-15 | yr^-1 | Gdot_over_G |
| memory_kernel_drift_per_yr | 9.600e-15 | yr^-1 | Gdot_over_G |
| boundary_vector_B0i | 2.000e-09 | dimensionless | alpha2 |

## 4. Family Rollup

| family | ceiling | units | channel |
| --- | --- | --- | --- |
| alpha3_flux | 4.000e-20 | dimensionless | bulk_flux_X |
| source_charge_WEP | 2.800e-15 | dimensionless | boundary_species_charge |
| Gdot_drift | 9.600e-15 | yr^-1 | domain_scale_drift_per_yr |
| domain_vector_alpha2 | 2.000e-09 | dimensionless | boundary_vector_B0i |
| xi_anisotropy | 4.000e-09 | dimensionless | boundary_tracefree_shear |
| gamma_beta_fifth_force_hair | 2.300e-05 | dimensionless | bulk_X_metric_slip |

## 5. Allowed Exits

A channel may leave the runner only by one of these exits:

- theorem-zero from the parent action;
- exact Ward-owned cancellation;
- gauge/topological no-hair theorem;
- constant universal source-normalized monopole absorption;
- explicit coefficient/range/source-charge map retained for testing.

Anything else is just hiding a local fifth force, preferred-frame term, or source-normalization residue.

## 6. Profile Contract

| profile | over | worst | severity | verdict |
| --- | --- | --- | --- | --- |
| theorem_zero | 0 | bulk_flux_X | 0 | what a real no-hair theorem would supply |
| one_tenth_tightest_bound | 0 | boundary_species_charge | 0.1 | inside budget only if derived as suppression |
| edge_tightest_bound | 0 | bulk_flux_X | 1 | edge is not stable evidence |
| tiny_floor_1e_minus_20 | 0 | bulk_flux_X | 0.25 | tests whether absurdly tiny flux leaks still matter |
| tiny_floor_1e_minus_15 | 3 | bulk_flux_X | 2.500e+04 | fails_contract |
| engineering_tiny_1e_minus_12 | 11 | bulk_flux_X | 2.500e+07 | fails_contract |
| unit_coupling | 21 | bulk_flux_X | 2.500e+19 | fails_contract |

## 7. Gate Results

| gate | status | evidence |
| --- | --- | --- |
| source_paths_exist | pass | all cited source paths exist |
| numeric_bound_contract_written | pass | 21 boundary/domain/flux/source channels contracted |
| alpha3_flux_contract_explicit | pass | 3 alpha3 flux channels require 4e-20-scale closure |
| Gdot_drift_contract_explicit | pass | 4 yr^-1 drift channels retained |
| nohair_mechanism_tests_written | pass | 7 mechanism tests written |
| over_contract_profiles_detected | pass | tiny_floor_1e_minus_15;engineering_tiny_1e_minus_12;unit_coupling |
| Ward_flux_nohair_parent_derived | fail | total Ward flux owner is mapped but not derived |
| domain_projector_nohair_parent_derived | fail | gauge/topological selector status not parent-derived |
| PPN_or_local_GR_promoted | fail | numeric contract only; rows remain retained/budgeted/contingent |
| claim_ceiling_enforced | pass | boundary_domain_flux_nohair_numeric_contract_only_no_boundary_bulk_domain_flux_PPN_fifth_force_source_or_local_GR_pass |

## 8. Decision

The boundary/domain/flux no-hair problem is now a numeric contract. The alpha3 Ward-flux channels are the hardest local rows: each flux channel must be theorem-zero, Ward-cancelled, or below 4e-20 dimensionless before any local PPN claim is possible. Gdot/G drift channels need <=9.6e-15 yr^-1. Domain/vector/anisotropy channels are less brutal but still require explicit no-hair or coefficient maps. The existing corpus has conditional exits—class-only boundary, source-free bulk-X mass gap, gauge/topological domain/projector, and Ward-owned flux—but does not derive them from the parent action. Rows stay retained/budgeted.

Practical read: this is grim only in the useful sense. The numbers are harsh, but that is exactly what a GR-reduction programme needs: no “small enough probably” language. The alpha3 flux row wants exact Ward silence or a suppression below `4e-20`. That is not a fitting target; it is a derivation target.

## 9. Next Target

`404-selector-blind-matter-axiom-origin.md`

Try to find the primitive MTS reason why matter, frame choice, and flux/domain/projector channels become silent locally. If that primitive reason exists, it may pay multiple debts at once.
