# 434 - Measured-GM / mu_extra Zero Route

Private C6/source-normalization derivation checkpoint. This is not a public WEP, Einstein-Hilbert, Newtonian-limit, PPN, fifth-force, flux, domain, cosmology, or unified-field claim.

## 1. Purpose

Checkpoint 433 gave a conditional route to constant `kappa_eff/G_eff`, but constant `G_eff` is not the same thing as measured Newtonian source normalization. This checkpoint asks whether `mu_obs=G_eff M_eff` can be derived with `mu_extra=0`, or whether hidden source hair must remain retained.

## 2. Run Manifest

| Item | Value |
| --- | --- |
| Script | `scripts/measured_GM_mu_extra_zero_route.py` |
| Run directory | `runs/20260602-120000-measured-GM-mu-extra-zero-route` |
| Status | `measured_GM_mu_extra_zero_route_written_Gauss_law_contract_sharpened_conditional_only_not_parent_derived_no_local_GR_pass` |
| Claim ceiling | `measured_GM_mu_extra_zero_route_only_no_WEP_EH_Newton_PPN_fifth_force_flux_domain_or_local_GR_pass` |
| Next target | `435-exterior-extra-source-nohair-owner-gate.md` |

## 3. Source Register

| source_file | exists | role |
| --- | --- | --- |
| 244-Meff-monopole-source-normalization-or-radial-memory-hair.md | True | conditional M_eff monopole flux theorem and radial hair warning |
| 378-source-normalization-Geff-Meff-GM-absorption-theorem.md | True | previous GM absorption gate and residual impact map |
| 380-bulk-X-mass-gap-source-normalized-force-law.md | True | finite-range bulk/Yukawa source-normalized force-law contract |
| 402-EH-source-normalization-parent-pair.md | True | EH/source-normalization pair and mu_obs=G_eff M_eff+mu_extra chain |
| 424-same-frame-EH-source-Poisson-reduction-gate.md | True | Poisson bridge and measured-GM normalization requirements |
| 425-EH-operator-retained-ledger-and-source-normalization-test-plan.md | True | source-normalization local-bound test plan |
| 429-Ward-Bianchi-exchange-owner-for-Poisson-source.md | True | mu_extra decomposition and Ward-owned hidden contribution warning |
| 430-Ward-source-residual-zero-route-gate.md | True | C6 mu_extra zero route ranking |
| 433-kappa-Geff-local-constancy-lemma.md | True | C5 constant kappa/G_eff conditional lemma |
| runs/20260601-000061-Meff-monopole-source-normalization-or-radial-memory-hair/results/monopole_flux_theorem_chain.csv | True | machine-readable M_eff radial conservation chain |
| runs/20260601-000061-Meff-monopole-source-normalization-or-radial-memory-hair/results/source_normalization_readout.csv | True | M_eff readout channels and what remains unowned |
| runs/20260601-000061-Meff-monopole-source-normalization-or-radial-memory-hair/results/claim_gate_results.csv | True | claim gates for N1 M_eff conditional flux theorem |
| runs/20260602-002500-source-normalization-Geff-Meff-GM-absorption-theorem/results/GM_absorption_theorem_attempt.csv | True | GM absorption theorem attempt steps |
| runs/20260602-002500-source-normalization-Geff-Meff-GM-absorption-theorem/results/absorption_gate_matrix.csv | True | GM absorption gate matrix |
| runs/20260602-002500-source-normalization-Geff-Meff-GM-absorption-theorem/results/residual_impact_map.csv | True | observable row impacts when absorption gates fail |
| runs/20260602-002500-source-normalization-Geff-Meff-GM-absorption-theorem/results/runner_update.csv | True | runner row update after source-normalization audit |
| runs/20260602-114500-kappa-Geff-local-constancy-lemma/results/source_residual_implications.csv | True | C5 residual implications feeding C6 |

## 4. Measured-GM Zero Chain

| step | claim | status | meaning |
| --- | --- | --- | --- |
| 1 | Define the actually observed Kepler/source parameter. | definition | orbits measure mu_obs, not G_eff and M_eff separately |
| 2 | Split the weak-field source into ordinary monopole plus retained extras. | conditional_EH_branch | requires same-frame EH/Poisson setup from earlier checkpoints |
| 3 | Gauss law gives the measured source decomposition. | algebra_pass | mu_extra is the integrated exterior/retained non-ordinary source contribution |
| 4 | Import the conditional M_eff monopole result. | conditional_from_244_not_global | radial ordinary-mass hair is removed only if Pi_M flux closure is parent-owned |
| 5 | Identify the zero condition for mu_extra. | conditional_theorem_target | all boundary, domain, bulk, non-EH, finite-range, time, and species channels must vanish or be harmless calibration |
| 6 | Ward ownership is not absence. | counterexample_warning | a conserved hidden contribution can still shift measured GM |
| 7 | Measured Newton is recovered only by universal constancy. | not_parent_derived | current corpus has not derived the full source-normalization theorem |

Exact measured-source decomposition:

```text
mu_obs(r,t,A,lambda) := r^2 partial_r Phi_A(r,t,lambda)

nabla^2 Phi = 4 pi G_eff rho_M + R_extra

mu_obs(r,t,A,lambda)
  = G_eff M_eff(r,t) + mu_extra(r,t,A,lambda).

mu_extra=0 requires every non-ordinary exterior source, finite-range tail,
species charge, time drift, and non-universal calibration to vanish or be
reduced to one parent-fixed constant universal measured-GM calibration.
```

## 5. mu_extra Zero Requirements

| requirement | current_status | if_missing | rows_at_risk |
| --- | --- | --- | --- |
| same_frame_observed_potential | conditional_from_C0_not_parent_derived | mu_obs is a frame artifact rather than Newtonian source proof | R0;R2;R3;R4;R11 |
| constant_universal_Geff | conditional_spacetime_lemma_only_from_433 | delta_G, Gdot, WEP-source, or range residuals survive | R1;R4;R9;R10 |
| absolute_PiM_calibration | not_parent_derived | M_eff is a fitted normalization rather than measured mass | R4;R9 |
| radial_flux_closure | conditional_from_244_not_parent_owned | radial memory hair alters enclosed source | R4;R10 |
| no_exterior_extra_source | not_derived | boundary/bulk/domain/non-EH source becomes mu_extra | R3;R4;R7;R8;R9;R10;R11 |
| no_finite_range_tail | symbolic_deferred | Yukawa/spectral/domain-wall force is hidden as GM | R10 |
| species_source_universality | not_parent_derived | source-normalization WEP leakage survives | R1;R2 |
| time_stationary_source | not_parent_derived | Gdot/G and secular orbital drift remain active | R9 |

## 6. mu_extra Decomposition

| channel | zero_route | current_status | rows |
| --- | --- | --- | --- |
| radial_Meff_hair | Pi_M flux closure plus no radial memory leakage | conditional_not_parent_owned | R4;R10 |
| boundary_monopole_shift | class/topological boundary no-hair or constant universal calibration | retained | R4;R7;R8;R9 |
| domain_projector_mass | covariant projector plus no-vector/no-shear/no-monopole leakage | conditional_open | R5;R6;R7;R8;R11 |
| bulk_X_Yukawa_tail | positive source-free mass-gap no-hair or executable force-law below bounds | symbolic_deferred | R10 |
| nonEH_operator_potential | EH-only exterior or coefficient vector retained and scored | retained_symbolic | R3;R4;R10;R11 |
| species_source_charge | same source normalization for all compositions | not_derived | R1;R2 |
| time_drift | stationary G_eff, M_eff, boundary/domain/bulk source | not_derived | R9 |
| absolute_calibration_offset | constant universal calibration absorbed into measured GM | harmless_if_parent_fixed_not_derived | R4;R9 |

## 7. Gauss-Law Case Analysis

| case_id | result | verdict |
| --- | --- | --- |
| GR_Newton_monopole | mu_obs=G_eff M_eff and mu_extra=0 | conditional_target |
| conserved_Meff_only | ordinary radial mass hair is controlled but GM absorption is not proven | necessary_not_sufficient |
| constant_universal_calibration | can be absorbed into measured GM without local residual | harmless_calibration_if_parent_fixed |
| radial_hair | inverse-square law/source profile changes | R4_R10_retained |
| finite_range_tail | range-dependent force cannot be absorbed into GM | R10_executable_or_fail |
| species_charge | WEP/source-normalization leakage | R1_retained |
| Ward_owned_nonzero_flux | Bianchi bookkeeping passes while Newton source normalization fails | retained_not_zero |

## 8. Row Implications

| row_id | mu_extra_risk | current_transition |
| --- | --- | --- |
| R1_WEP_source_charge | species or composition dependence in mu_obs | retained_contingent_budget_not_upgraded |
| R4_beta | radial/nonlinear source hair or unabsorbed monopole shift | retained_budget_not_upgraded |
| R7_alpha3 | unowned boundary/projector momentum flux | retained_contingent_budget_not_upgraded |
| R8_xi | boundary/domain preferred-location source anisotropy | retained_budget_not_upgraded |
| R9_Gdot | time-dependent G_eff, M_eff, or boundary/bulk source | retained_contingent_budget_not_upgraded |
| R10_fifth_force | finite-range Yukawa/spectral/domain-wall tail | symbolic_deferred_not_upgraded |
| R11_EH_operator_ledger | non-EH operator potential contributes to measured force | retained_residual_not_upgraded |

## 9. Bound Fallback Matrix

| failed_condition | runner_row | required_action |
| --- | --- | --- |
| partial_r mu_extra=0 not derived | R4;R10 | score radial source hair or supply no-hair theorem |
| partial_t mu_obs=0 not derived | R9 | score Gdot/G or secular orbital drift |
| partial_A ln mu_obs=0 not derived | R1 | score WEP/source-normalization subchannel |
| alpha(lambda)=0 not derived | R10 | provide executable alpha(lambda) curve; symbolic cannot pass |
| non-EH/boundary/domain source not silenced | R3;R4;R7;R8;R11 | retain coefficient vector or prove no-hair/topological silence |

## 10. Theorem Attempt Status

| claim | status | evidence |
| --- | --- | --- |
| Gauss-law decomposition of measured mu_obs is exact in the weak-field branch | pass | mu_obs=G_eff M_eff+mu_extra chain written |
| conditional mu_extra=0 theorem shape is identified | conditional_pass | requires no exterior extra source, flux closure, same frame, constant G_eff, and universality |
| M_eff conservation alone proves measured GM absorption | fail | old 244/378 gates show calibration, kappa, range, time, species, and Ward ownership remain open |
| Ward-owned hidden flux implies mu_extra=0 | fail | conserved hidden contribution may still shift measured GM |
| C6 mu_extra zero is parent-derived | fail | no parent theorem eliminates all boundary/domain/bulk/non-EH/fifth-force/source-normalization channels |

## 11. Gate Results

| gate | status | evidence |
| --- | --- | --- |
| source_paths_exist | pass | all cited source paths exist |
| measured_GM_chain_written | pass | 7 measured-GM chain stages recorded |
| mu_extra_decomposition_written | pass | 8 mu_extra channels recorded |
| conditional_Meff_flux_imported | conditional_pass | checkpoint 244 gives M_eff radial conservation only if Pi_M flux closure is parent-owned |
| conditional_mu_extra_zero_contract_written | conditional_pass | zero theorem shape recorded but depends on C0/C3/C4/C5/C6/C7 premises |
| absolute_calibration_derived | fail | parent-fixed Pi_M-to-physical-mass units remain open |
| no_exterior_extra_source_derived | fail | boundary/domain/bulk/non-EH exterior sources remain retained or symbolic |
| species_time_range_universality_derived | fail | partial_A, partial_t, and alpha(lambda) conditions remain not derived |
| Ward_owned_flux_absent_not_just_owned | fail | Ward ownership can conserve a nonzero hidden measured-GM shift |
| runner_rows_promoted_to_theorem_zero | fail | 0 row upgrades; R1/R4/R7/R8/R9/R10/R11 remain retained/symbolic |
| Newton_or_local_GR_promoted | fail | measured-GM route only; no Newton/PPN/local-GR pass |
| claim_ceiling_enforced | pass | measured_GM_mu_extra_zero_route_only_no_WEP_EH_Newton_PPN_fifth_force_flux_domain_or_local_GR_pass |

## 12. Decision

The C6 measured-GM route is now exact enough to prevent hidden source normalization. In the weak-field same-frame branch, mu_obs=r^2 partial_r Phi decomposes as G_eff M_eff plus mu_extra. The existing M_eff monopole result is useful but only conditional and not sufficient: mu_extra=0 additionally needs parent-fixed calibration, constant universal G_eff, no exterior boundary/domain/bulk/non-EH/fifth-force source, species/time/range universality, and proof that Ward-owned hidden flux is absent rather than merely conserved. The current corpus does not derive those premises, so C6 remains a conditional zero route and retained test contract, not a Newton/local-GR promotion.

Practical read: this is another narrow-but-good result. We are no longer letting measured `GM` act like a magic bin. Either the extra source is mathematically zero/harmless universal calibration, or it becomes a scored residual row.

## 13. Next Queue

| rank | target | why_next |
| --- | --- | --- |
| 1 | 435-exterior-extra-source-nohair-owner-gate.md | mu_extra=0 now reduces to proving boundary/domain/bulk/non-EH/fifth-force exterior sources are absent, pure calibration, or retained below bounds |
| 2 | auxiliary/projector local Euler-equation ledger | C1 remains the strongest Ward route for killing unowned local exchange terms |
| 3 | R10 alpha(lambda) executable curve contract | finite-range tails cannot stay symbolic if the local residual vector is to be tested |
