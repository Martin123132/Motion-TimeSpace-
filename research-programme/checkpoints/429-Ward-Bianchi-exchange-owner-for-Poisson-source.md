# 429 - Ward/Bianchi Exchange Owner For Poisson Source

Private derivation checkpoint. This is not a public WEP, Einstein-Hilbert, Newtonian-limit, PPN, fifth-force, flux, domain, cosmology, or unified-field claim.

## 1. Purpose

Checkpoint 428 defined the local residual vector. This checkpoint attacks the main physics bottleneck: can Ward/Bianchi exchange ownership derive `q_loc^nu=0`, `source_residuals=0`, and `mu_extra=0` rather than smuggling in a local-vacuum plateau?

Short answer: it gives a clean conditional identity, but not yet the full zero theorem. Ward/Bianchi ownership tells us exactly where every local force must live. It does not by itself prove that each owned force vanishes.

## 2. Run Manifest

| Item | Value |
| --- | --- |
| Script | `scripts/Ward_Bianchi_exchange_owner_for_Poisson_source.py` |
| Run directory | `runs/20260602-101500-Ward-Bianchi-exchange-owner-for-Poisson-source` |
| Status | `Ward_Bianchi_exchange_owner_attempt_written_conditional_q_source_identity_but_mu_extra_and_nohair_not_derived_no_local_GR_pass` |
| Claim ceiling | `Ward_Bianchi_exchange_owner_identity_only_no_WEP_EH_Newton_PPN_fifth_force_flux_domain_or_local_GR_pass` |
| Next target | `430-Ward-source-residual-zero-route-gate.md` |

## 3. Source Register

| source_file | exists | role |
| --- | --- | --- |
| 177-parent-action-perturbation-local-GR-contract.md | True | parent action and local q_loc silence contract |
| 179-local-GR-PPN-silence-contract.md | True | q_loc blocker and plateau-axiom warning |
| 356-parent-action-ward-identity-and-projector-variation.md | True | parent Ward identity and explicit projector/boundary/domain force ledger |
| 357-Ward-owned-local-nohair-or-retained-PPN-residual-map.md | True | Ward-force fates and retained PPN residual map |
| 358-local-EH-exterior-operator-from-Ward-closed-action.md | True | Ward closure not sufficient for EH operator selection |
| 402-EH-source-normalization-parent-pair.md | True | same-frame EH/source and measured GM normalization |
| 424-same-frame-EH-source-Poisson-reduction-gate.md | True | source_residuals and mu_extra in the EH-to-Poisson bridge |
| 425-EH-operator-retained-ledger-and-source-normalization-test-plan.md | True | EH/source retained ledger and source-normalization channels |
| 428-MTS-local-residual-vector-input-contract.md | True | 12-component local residual vector and local-GR pass requirements |
| runs/20260602-094500-MTS-local-residual-vector-input-contract/results/residual_components.csv | True | machine-readable residual components R0-R11 |
| runs/20260602-093000-local-bound-runner-v4-evaluate-smoke/results/evaluation_digest.csv | True | sourced local-bound rows for residual implications |

## 4. Ward/Bianchi Identity Chain

| step | stage | status | meaning |
| --- | --- | --- | --- |
| 1 | parent_action | contract_not_parent_supplied | the Ward identity can only be theorem-level if the parent action exists with all exchange variables included |
| 2 | diffeomorphism_variation | structural_Ward_identity | diffeomorphism invariance forces every hidden/projector/boundary/domain term into the ledger |
| 3 | integrated_Ward_identity | conditional_identity | gravity is conserved only after auxiliary equations and force ledgers are owned |
| 4 | same_frame_field_equation | decomposition_contract | matter/source conservation is read in the same observed frame; otherwise exchange is frame artefact |
| 5 | Bianchi_projection | exchange_owner_identity | the local force is not arbitrary; it is exactly the unowned divergence of retained sectors |
| 6 | local_projection | exact_contract | q_loc^nu is zero only if the local projection of every exchange-owner term is zero |
| 7 | Poisson_source | not_derived_zero | Bianchi ownership controls conservation, but Poisson source purity also needs no-hair/source-normalization |
| 8 | measured_GM | not_derived_zero | a conserved hidden contribution can still shift measured GM or create range/species dependence |

The central identity is:

```text
q_loc^nu = P_loc[nabla_mu T_obs^(mu nu)]
         = kappa_eff^-1 P_loc[
             div E_nonEH
           + T_obs nabla kappa_eff
           + E_Z nabla Z
           + F_projector + F_boundary + F_domain + F_nonmetric
           ].
```

That is progress: `q_loc^nu` is no longer a mystery knob. But the right-hand side must still be zeroed or retained term by term.

## 5. Exchange Owner Conditions

| condition_id | needed_for | current_status | failure_if_missing |
| --- | --- | --- | --- |
| C0_same_frame | R0;R2;R3;R4;R11 | not_parent_derived | clock/WEP/gamma/beta residuals can be frame artefacts |
| C1_auxiliary_on_shell | R7;R9;R10;R11 | open | unowned local force/source exchange |
| C2_projector_covariant | R5;R6;R7;R8;R11 | conditional_open | preferred-frame/location and alpha3 flux channels |
| C3_boundary_nohair | R3;R4;R7;R8;R9 | not_derived | gamma/beta/alpha3/xi/Gdot residuals |
| C4_nonEH_divergence_silent | R3;R4;R5;R6;R8;R10;R11 | retained | Ward-conserved but non-GR exterior |
| C5_constant_kappa_Geff | R1;R4;R9;R10 | not_derived | Gdot/G, WEP source charge, beta, fifth-force/source range residuals |
| C6_mu_extra_zero | R1;R4;R9;R10 | not_derived | Poisson algebra can pass while measured Newton source is contaminated |
| C7_R10_R11_resolved | R10;R11 | symbolic_deferred | no fifth-force/operator pass can be claimed |

## 6. Source-Residual Decomposition

| term | owner_condition | residual_rows | zero_status |
| --- | --- | --- | --- |
| delta_kappa_source | C5_constant_kappa_Geff | R1;R4;R9 | not_derived |
| nonEH_divergence | C4_nonEH_divergence_silent;C7_R10_R11_resolved | R3;R4;R10;R11 | retained |
| auxiliary_offshell_force | C1_auxiliary_on_shell | R7;R9;R10 | open |
| projector_domain_force | C2_projector_covariant | R5;R6;R7;R8 | conditional_open |
| boundary_flux | C3_boundary_nohair | R3;R4;R7;R8;R9 | not_derived |
| nonmetric_matter_exchange | C0_same_frame | R0;R1;R2 | not_parent_derived |

## 7. Measured-GM / `mu_extra` Decomposition

| mu_channel | test_rows | Ward_result | status |
| --- | --- | --- | --- |
| species_source_charge | R1 | total exchange can be conserved | not_derived |
| time_drift | R9 | total drift must have an owner | not_derived |
| range_dependence | R10 | finite-range exchange can be conserved | symbolic_deferred |
| boundary_monopole_shift | R4;R9 | boundary monopole can be conserved | retained |
| domain_projector_mass | R5;R6;R7;R8;R11 | covariant domain stress can be in total ledger | retained |

Ward conservation can say "the hidden contribution is owned." It cannot alone say "the hidden contribution is absent from measured `GM`." That is why `mu_extra=0` remains a separate source-normalization theorem target.

## 8. Residual Vector Implications

| row_id | observable | Ward_effect | post_429_state |
| --- | --- | --- | --- |
| R0_identity_coframe_direct | eta_WEP_direct_geometry | same-frame Ward identity helps only if matter functor is universal | not_upgraded |
| R1_WEP_source_charge | eta_WEP_source_charge | conserved exchange does not prove species-blind source charge | retained |
| R2_clock_redshift | alpha_clock_redshift | requires same matter clock frame; Ward total conservation is insufficient | retained |
| R3_gamma | gamma_minus_1 | non-EH or boundary shear can be conserved but still alter slip | retained |
| R4_beta | beta_minus_1 | source_residual and mu_extra zero conditions now explicit | retained |
| R5_alpha1 | alpha1 | projector/domain covariance must still kill preferred-frame vector terms | retained |
| R6_alpha2 | alpha2 | same as R5 but tighter lock | retained |
| R7_alpha3 | alpha3 | main beneficiary: unowned momentum flux now has exact owner identity target | conditional_route_not_pass |
| R8_xi | xi | domain/boundary anisotropy must be no-hair, not merely conserved | retained |
| R9_Gdot | Gdot_over_G | total exchange ownership does not prove local stationary measured GM | retained |
| R10_fifth_force | delta_G_or_fifth_force_yukawa | finite-range force may be conserved; still needs alpha(lambda) curve or zero theorem | symbolic_deferred |
| R11_EH_operator_ledger | non_EH_operator_coefficients | Ward conservation does not select EH; coefficient vector still required | symbolic_deferred |

## 9. Ward-Satisfying Counterexamples

| counterexample | how_it_satisfies_Ward | why_it_fails_local_GR |
| --- | --- | --- |
| conserved_scalar_tensor | total scalar plus metric stress is covariantly conserved | gamma/beta/fifth-force can differ from GR |
| conserved_boundary_monopole_with_drift | boundary charge is in the total stress ledger | measured GM drifts or beta source normalization shifts |
| covariant_domain_vector | domain vector action is diffeomorphism-invariant | preferred-frame alpha1/alpha2/xi residuals survive |
| fixed_external_projector | it does not; explicit diffeo breaking is hidden if projector is not varied | fake conservation and fake GR by dropped stress |
| species_dependent_source_charge | each species can be conserved in its own coupled sector | WEP/source-charge row fails |
| pure_Poisson_with_slip | 00 equation can reduce to Poisson | gamma/light bending/PPN spatial curvature still fail |

These are the no-cheat examples. A theory can satisfy a Ward identity and still not reduce to GR. So the Ward identity is necessary footwork, not the knockout.

## 10. Theorem Attempt Status

| target | result | evidence |
| --- | --- | --- |
| derive Ward exchange-owner identity | conditional_pass | Noether/Bianchi chain written with all force channels explicit |
| derive q_loc^nu=0 | conditional_only | q_loc^nu=0 follows only if C0-C7 local projections vanish or are retained below locks |
| derive source_residuals=0 | not_derived | non-EH divergence, boundary/domain flux, kappa drift, and fifth-force tails remain open |
| derive mu_extra=0 | not_derived | conserved hidden stress can still shift measured GM by species/time/range/domain channels |
| promote local GR/Newton/PPN | fail | Ward ownership is necessary but not sufficient for EH operator, source normalization, and PPN completion |

## 11. Gate Results

| gate | status | evidence |
| --- | --- | --- |
| source_paths_exist | pass | 0 missing source paths |
| Ward_identity_chain_written | pass | 8 identity steps |
| exchange_owner_conditions_written | pass | 8 zero conditions C0-C7 |
| source_residual_decomposition_written | pass | 6 source-residual terms |
| mu_extra_decomposition_written | pass | 5 measured-GM channels |
| residual_vector_implications_written | pass | 12 R0-R11 implications |
| counterexamples_written | pass | 6 Ward-satisfying failure branches |
| q_loc_zero_derived | conditional_only | requires C0-C7 local zero/retained conditions |
| source_residuals_zero_derived | fail | non-EH/source-normalization/boundary/domain/fifth-force terms remain open |
| mu_extra_zero_derived | fail | measured GM source normalization remains unproved |
| claim_leaks | pass | 0 claim-allowed rows |
| local_GR_promoted | fail | Ward identity only; no EH/Newton/PPN/fifth-force pass |
| claim_ceiling_enforced | pass | Ward_Bianchi_exchange_owner_identity_only_no_WEP_EH_Newton_PPN_fifth_force_flux_domain_or_local_GR_pass |

## 12. Decision

Ward/Bianchi exchange ownership gives a clean conditional identity for q_loc^nu: the local force is exactly the projected divergence of unowned non-EH, auxiliary, projector, boundary, domain, nonmetric, and kappa/source-normalization terms. This is progress because it forbids hand-waving and identifies the zero conditions. It does not yet derive q_loc^nu=0, source_residuals=0, or mu_extra=0 from the current parent corpus, so local GR remains unpromoted.

Practical read: this is a useful step. We did not get the belt, but we now know the exact punch list. The local-GR derivation has become C0-C7. If we can prove those zero/retained conditions from the parent action, then `q_loc`, `source_residuals`, and `mu_extra` stop being hand-inserted closures and become derivable.

## 13. Next Target

`430-Ward-source-residual-zero-route-gate.md`
