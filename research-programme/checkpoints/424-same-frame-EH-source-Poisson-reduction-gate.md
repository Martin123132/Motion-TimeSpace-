# 424 - Same-Frame EH Source Poisson Reduction Gate

Private GR/Newton reduction checkpoint. This is not a public WEP, Einstein-Hilbert, Newtonian-limit, PPN, fifth-force, flux, domain, cosmology, or unified-field claim.

## 1. Purpose

Checkpoint 423 clarified the no-extension/minimality wall. This checkpoint moves onto the direct GR-to-Newton bridge: if MTS ever derives the same-frame Einstein-Hilbert/source premises, does the weak-field limit reduce cleanly to Poisson and Newtonian mechanics?

## 2. Run Manifest

| Item | Value |
| --- | --- |
| Script | `scripts/same_frame_EH_source_Poisson_reduction_gate.py` |
| Run directory | `runs/20260602-084000-same-frame-EH-source-Poisson-reduction-gate` |
| Status | `same_frame_EH_source_Poisson_reduction_gate_written_exact_GR_to_Newton_bridge_but_parent_premises_not_derived_no_local_GR_pass` |
| Claim ceiling | `same_frame_EH_source_Poisson_reduction_gate_only_no_WEP_EH_Newton_PPN_fifth_force_flux_domain_or_local_GR_pass` |
| Next target | `425-EH-operator-retained-ledger-and-source-normalization-test-plan.md` |

## 3. Reduction Requirements

| requirement | current_status | failure_if_missing | rows_at_risk |
| --- | --- | --- | --- |
| same_matter_and_gravity_frame | conditional_not_parent_derived | field redefinition can hide source/operator debts in a different frame | R0;R2;R3;R4;R11 |
| EH_operator_selection | conditional_Lovelock_route_not_parent_derived | non-EH operators alter gamma, beta, slip, fifth force, or wave sector | R3;R4;R8;R10;R11 |
| constant_universal_kappa | not_parent_derived | Gdot/G, WEP-source charge, beta/source-normalization residues remain | R1;R4;R9 |
| Bianchi_and_matter_conservation | not_fully_closed | extra local force/exchange appears in equations of motion | R7;R9;R10 |
| nonrelativistic_static_source_limit | conditional_standard_limit | Poisson source is not just mass density | R4;R10 |
| measured_mass_normalization | not_parent_derived | mu_obs=G_eff M_eff gains hidden bulk/boundary/domain/source charge | R1;R4;R9;R10 |
| no_extra_potential_channels | not_derived | Yukawa, radial hair, boundary flux, or domain projector force alters Newton | R3;R4;R7;R8;R10 |
| PPN_completion | not_promoted | Poisson limit alone is not a full local-GR/PPN pass | R3;R4;R5;R6;R7;R8;R9 |

## 4. EH to Poisson Chain

| step | stage | status | meaning |
| --- | --- | --- | --- |
| 1 | same_frame_field_equation | conditional_target | matter and geometry must vary the same observed frame |
| 2 | weak_field_metric | standard_limit_if_same_frame | one potential sources slow-particle acceleration; slip must be controlled |
| 3 | nonrelativistic_source | conditional_standard_limit | Poisson source is rest-mass density only after extra stresses are silent or retained |
| 4 | linearized_00_equation | algebra_written | the coefficient matches checkpoint 402 conventions |
| 5 | G_eff_identification | algebra_pass | then nabla^2 Phi = 4 pi G_eff rho_eff if source_residuals=0 |
| 6 | measured_GM | conditional_not_parent_derived | Newton requires mu_extra=0 and G_eff M_eff constant/universal/range-independent |
| 7 | slow_particle_acceleration | conditional | Newtonian mechanics follows only if a_extra^i=0 or retained below locks |

Exact algebraic bridge:

```text
G_munu[g_obs] + Lambda g_obs_munu = kappa_eff T_eff_munu[g_obs]
T_00 ~= rho_eff c^2
nabla^2 Phi = (kappa_eff c^4 / 2) rho_eff + source_residuals
G_eff = kappa_eff c^4 / (8 pi)
=> nabla^2 Phi = 4 pi G_eff rho_eff if source_residuals = 0.
```

That bridge is algebraically clean. It becomes Newtonian mechanics only when `mu_obs=G_eff M_eff` is constant, universal, conserved, and range-independent, and when `a_extra^i=0` or retained below lock.

## 5. Source-Normalization Tests

| test | current_status | residual_if_failed |
| --- | --- | --- |
| constant_Geff | not_derived | Gdot/G or WEP-source charge |
| conserved_mass | not_derived | source-normalization beta/Gdot channel |
| range_independent_GM | not_derived | fifth-force row |
| species_independent_source | not_derived | WEP/source-charge row |
| boundary_bulk_domain_silence | not_derived | gamma/beta/alpha/xi/Gdot/fifth-force residuals |
| PPN_second_order_completion | not_derived | beta/gamma rows |

## 6. Counterexample Branches

| counterexample | why_it_breaks_newton | required_blocker |
| --- | --- | --- |
| frame_split_EH_and_matter | same-looking matter action sources a different metric than the EH operator | same-frame matter/EH variation theorem |
| drifting_kappa | Poisson coefficient becomes time/range/domain dependent | constant universal kappa theorem |
| nonEH_operator_residue | adds slip, fourth-order pieces, scalar modes, or fifth-force tails | EH-only operator selection or retained coefficient ledger |
| hidden_source_charge | measured GM absorbs new physics instead of deriving universal mass | source-normalization and no-hair theorem |
| finite_range_force | Poisson limit is range dependent unless alpha(lambda)=0 or bounded | fifth-force law or theorem-zero |
| unowned_Bianchi_exchange | slow-particle motion receives non-geodesic/exchange force | Ward/Bianchi exchange owner |
| Poisson_only_false_GR_pass | Newtonian force may pass while light bending/time delay/PPN fail | full PPN residual vector |

## 7. Row Transition Attempt

| row_id | previous_state | new_state | result |
| --- | --- | --- | --- |
| R0_identity_coframe_direct | closure_zero | closure_zero | not_upgraded |
| R1_WEP_source_charge | retained_contingent_budget | retained_contingent_budget | not_upgraded |
| R2_clock_redshift | retained_budget | retained_budget | not_upgraded |
| R3_gamma | retained_budget | retained_budget | not_upgraded |
| R4_beta | retained_budget | retained_budget | not_upgraded |
| R5_alpha1 | retained_budget | retained_budget | not_upgraded |
| R6_alpha2 | retained_budget | retained_budget | not_upgraded |
| R7_alpha3 | retained_contingent_budget | retained_contingent_budget | not_upgraded |
| R8_xi | retained_budget | retained_budget | not_upgraded |
| R9_Gdot | retained_contingent_budget | retained_contingent_budget | not_upgraded |
| R10_fifth_force | unscored_parameterized | unscored_parameterized | not_upgraded |
| R11_EH_operator_ledger | retained_residual | retained_residual | not_upgraded |

## 8. Gate Results

| gate | status | evidence |
| --- | --- | --- |
| source_paths_exist | pass | all cited source paths exist |
| reduction_requirements_written | pass | 8 reduction requirements recorded |
| Poisson_chain_written | pass | 7 weak-field chain stages recorded |
| EH_to_Poisson_algebra | conditional_pass | nabla^2 Phi = (kappa c^4/2) rho = 4 pi G_eff rho when G_eff=kappa c^4/(8 pi) |
| same_frame_parent_derived | fail | same matter/gravity frame remains conditional |
| EH_operator_selection_derived | fail | metric-only local second-order exterior is not derived from MTS parent action |
| constant_universal_kappa_derived | fail | kappa_eff/G_eff universality and time/range/species independence are not proven |
| measured_GM_normalized | fail | M_eff and mu_extra are not parent-owned zero |
| Bianchi_exchange_owned | fail | q_loc^nu/Ward exchange is not fully owned as zero or retained source law |
| extra_potential_channels_zero | fail | boundary/bulk/domain/fifth-force channels remain retained or unscored |
| PPN_completion_derived | fail | gamma/beta/preferred-frame/Gdot/fifth-force residual vector is not theorem-zero |
| runner_rows_promoted_to_theorem_zero | fail | 0 theorem-credit row upgrades |
| claim_leaks | pass | 0 claim-allowed rows |
| Newton_or_local_GR_promoted | fail | Poisson reduction gate only; no Newton/PPN/local-GR pass |
| claim_ceiling_enforced | pass | same_frame_EH_source_Poisson_reduction_gate_only_no_WEP_EH_Newton_PPN_fifth_force_flux_domain_or_local_GR_pass |

## 9. Decision

The exact local bridge is now machine-readable: if the parent action derives the same matter/gravity frame, selects the EH operator as the only local metric second-order exterior operator, fixes constant universal kappa, owns Bianchi conservation, normalizes measured mass, and kills or retains every extra potential, then the weak-field 00 equation reduces to Poisson with G_eff=kappa_eff c^4/(8 pi), and slow-particle Newtonian motion follows. The algebraic bridge is clean, but the parent premises are not derived in the current corpus. Therefore this is a reduction gate and test contract, not an EH/Newton/PPN/local-GR promotion.

Practical read: this is a good sign in the Mayweather sense. The bridge is not wild; if the parent pays the same-frame/EH/source bills, Newton comes out by the standard weak-field algebra. The remaining issue is not the bridge, it is earning the premises without smuggling in GR.

## 10. Next Target

`425-EH-operator-retained-ledger-and-source-normalization-test-plan.md`
