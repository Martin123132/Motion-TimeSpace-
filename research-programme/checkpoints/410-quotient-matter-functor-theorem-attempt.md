# 410 - Quotient-Matter Functor Theorem Attempt

Private quotient-matter/local-GR checkpoint. This is not a public WEP, Einstein-Hilbert, Newtonian-limit, PPN, fifth-force, flux, domain, cosmology, or unified-field claim.

## 1. Purpose

Checkpoint 409 showed runner-v4 is not leaking claims. This checkpoint attacks the key proof behind `R0`: can matter be forced to see only quotient-observed geometry, so the local selector derivative vanishes as a theorem rather than as a closure choice?

## 2. Run Manifest

| Item | Value |
| --- | --- |
| Script | `scripts/quotient_matter_functor_theorem_attempt.py` |
| Run directory | `runs/20260602-055500-quotient-matter-functor-theorem-attempt` |
| Status | `quotient_matter_functor_theorem_attempt_written_conditional_factorization_theorem_counterexamples_block_parent_derivation_R0_remains_closure_zero_no_local_GR_pass` |
| Claim ceiling | `quotient_matter_functor_theorem_attempt_only_no_WEP_EH_Newton_PPN_fifth_force_flux_domain_cosmology_or_local_GR_pass` |
| Next target | `411-local-bound-runner-v4-real-data-interface.py` |

## 3. Conditional Functor Theorem

If the parent theory supplies a quotient object `Q`, an observed-geometry functor `Obs(Q)=e_obs`, and matter factorization

```text
S_matter = sum_A S_A[Psi_A, Obs(Q), omega[Obs(Q)], theta_A]
```

with `partial_ZI Obs(Q)=0` and `partial_ZI theta_A=0` for representative selectors `Z_I`, then the direct matter selector pullback is zero:

```text
delta S_matter / delta Z_I | e_obs = 0
```

That is the right theorem shape. It is not yet a parent-derived theorem because the factorization, no-marker rule, and constant-sector independence are still open.

| requirement | status | needed_for |
| --- | --- | --- |
| parent quotient object | sketched_not_derived | matter cannot distinguish representative selector variables Z_I |
| observed geometry functor | conditional_template | one observed coframe and one matter metric |
| matter action factorization | sufficient_axiom_not_parent_derived | selector-blind matter chain-rule zero |
| selector-kernel condition | conditional_template | R0 direct coframe slip theorem-zero |
| constant-sector independence | not_derived | WEP/source charge and clock rows |
| no material marker extension | not_derived | prevents hidden spurion/background route |

## 4. Proof Chain

| step | claim | status |
| --- | --- | --- |
| 1 | Work on quotient data only. | premise_open |
| 2 | Observed coframe is a functor of quotient data. | conditional_template |
| 3 | Matter factors through the observed coframe and internal constants only. | sufficient_if_assumed |
| 4 | Representative selectors lie in the observation kernel. | conditional_if_Obs_is_exact |
| 5 | Species constants carry no selector or class charge. | open_hard_part |
| 6 | Chain rule gives selector-blind matter. | conditional_theorem_not_parent_derivation |

## 5. Counterexample Functors

| counterexample | damage |
| --- | --- |
| class_metric_common_pullback | clock/gamma/fifth-force pressure remains unless F is locally zero or sourced below bounds |
| marker_extended_quotient | active/readout background can re-enter as material spurion |
| species_internal_constants | WEP/source-charge and clock rows stay retained |
| Ward_owned_counterstress | alpha3/Gdot/PPN rows remain flux-owner debts |
| reduced_readout_EFT | R0 can look zero in a chosen closure while theorem-zero is not earned |

## 6. Row Transition Attempt

| row_id | previous_state | new_state | result |
| --- | --- | --- | --- |
| R0_identity_coframe_direct | closure_zero | closure_zero | not_upgraded |
| R1_WEP_source_charge | retained_contingent_budget | retained_contingent_budget | not_upgraded |
| R2_clock_redshift | retained_budget | retained_budget | not_upgraded |
| R7_alpha3 | retained_contingent_budget | retained_contingent_budget | not_upgraded |
| R9_Gdot | retained_contingent_budget | retained_contingent_budget | not_upgraded |
| R11_EH_operator_ledger | retained_residual | retained_residual | not_upgraded |

## 7. Gate Results

| gate | status | evidence |
| --- | --- | --- |
| source_paths_exist | pass | all cited source paths exist |
| functor_requirements_written | pass | 6 requirements recorded |
| conditional_chain_rule_theorem_written | conditional_pass | delta S_m/delta Z_I vanishes only under factorization plus selector-independent constants |
| counterexample_functors_written | pass | 5 counterexamples recorded |
| quotient_matter_functor_parent_derived | fail | factorization/no-marker/no-class-charge premises are not parent-derived |
| no_marker_theorem_derived | fail | marker-extended quotient remains a legal counterexample |
| R0_promoted_to_theorem_zero | fail | 0 theorem-zero row upgrades |
| claim_leaks | pass | 0 claim-allowed rows |
| local_GR_promoted | fail | matter functor attempt only; no EH/Newton/PPN/local-GR pass |
| claim_ceiling_enforced | pass | quotient_matter_functor_theorem_attempt_only_no_WEP_EH_Newton_PPN_fifth_force_flux_domain_cosmology_or_local_GR_pass |

## 8. Decision

The quotient-matter functor route gives a clean conditional theorem: if the parent action derives a quotient object Q, an observed-geometry functor Obs(Q), matter factorization through Obs(Q), selector-independent constants, and no marker/readout EFT extension, then the direct selector derivative of matter vanishes by the chain rule. That would be the right kind of proof for R0. But the existing corpus does not yet derive the factorization/no-marker/no-class-charge premises. Several counterexample functors remain legal under quotient language. Therefore R0 stays closure_zero rather than theorem_zero, and no local-GR claim is promoted.

Practical read: this route is still worth chasing because it has the exact GR-style flavour we want: a structural reason matter cannot see the forbidden selector. But quotient language alone is not enough. We need the parent action to forbid marker/class/constant-sector leakage, or runner-v4 must keep the local branch closure-labelled.

## 9. Next Target

`411-local-bound-runner-v4-real-data-interface.py`
