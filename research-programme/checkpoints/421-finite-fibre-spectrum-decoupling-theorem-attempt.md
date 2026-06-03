# 421 - Finite-Fibre Spectrum Decoupling Theorem Attempt

Private finite-fibre/local-GR checkpoint. This is not a public WEP, Einstein-Hilbert, Newtonian-limit, PPN, fifth-force, flux, domain, cosmology, or unified-field claim.

## 1. Purpose

Checkpoint 414 left `finite_cell_fibre_spectrum` as an extra local quotient-invariant generator. This checkpoint tests whether basis-free spectra and trace powers are merely harmless quotient data, or whether they still need a real decoupling theorem before the local GR branch can use them.

## 2. Run Manifest

| Item | Value |
| --- | --- |
| Script | `scripts/finite_fibre_spectrum_decoupling_theorem_attempt.py` |
| Run directory | `runs/20260602-075500-finite-fibre-spectrum-decoupling-theorem-attempt` |
| Status | `finite_fibre_spectrum_decoupling_attempt_written_relabel_invariant_but_not_decoupled_no_local_GR_pass` |
| Claim ceiling | `finite_fibre_spectrum_decoupling_attempt_only_no_WEP_EH_Newton_PPN_fifth_force_flux_domain_or_local_GR_pass` |
| Next target | `422-matter-functor-blindness-readout-after-variation-theorem-attempt.md` |

## 3. Fibre Observable Classification

| observable | quotient_status | local_marker_risk | verdict |
| --- | --- | --- | --- |
| basis_free_spectrum | relabel_invariant | yes_if_nonuniversal_or_dynamic | admissible_coordinate_not_decoupling_theorem |
| trace_powers | class_function | yes_if_local_values_or_gradients_remain | extra_invariant_until_silenced |
| trace_average | class_function | yes_if_it_renormalizes_G_or_matter_nonuniversally | constant_candidate_only |
| eigenvectors_or_cell_labels | not_relabel_invariant | yes_active_marker_returns | rejected |
| source_dependent_eigenvalues | class_function_but_source_dependent | yes_WEP_and_fifth_force_channel | counterexample_until_blocked |
| matter_functor_coefficients | can_be_relabel_invariant | yes_species_charge_channel | requires_next_theorem |
| readout_selected_component | observable_only_if_after_variation | yes_if_varied_as_reduced_action | no_cheat_rule_needed |

## 4. Decoupling Routes

| route | status | failure |
| --- | --- | --- |
| quotient_class_function_only | conditional_pass_as_admissibility | quotient invariance does not by itself remove a local scalar marker |
| universal_stationary_spectrum | not_derived | no parent fibre potential or uniqueness theorem fixes h0 |
| auxiliary_heavy_fibre_integrated_out | not_derived | mass gap, Hessian sign, and source-independence not proven |
| pure_topological_or_trace_constant | conditional_only | must prove no matter vertex and no metric variation residue |
| matter_functor_blindness | not_derived | species constants can still depend on quotient invariants |
| species_multiplet_fibre | rejected_for_local_GR_theorem | reintroduces source-charge/WEP channel |
| empirical_fitted_fibre_spectrum | forbidden_for_derivation | posthoc fitted marker; allowed only as explicit phenomenological closure |

## 5. Conditional Decoupling Chain

| step | claim | status |
| --- | --- | --- |
| 1 | The parent configuration contains only the quotient fibre [h]. | conditional_admissibility |
| 2 | The parent action is a class function of [h]. | template_only |
| 3 | The fibre Euler-Lagrange equation has a unique universal solution. | not_derived |
| 4 | Local fibre fluctuations are nonpropagating or gapped. | not_derived |
| 5 | Substitution or path integration leaves constants only. | not_derived |
| 6 | The matter functor is blind to [h]. | not_derived |
| 7 | The local invariant algebra reduces to geometry plus constants. | conditional_target_not_proven |

Exact theorem contract:

```text
If [h] is quotient-only, delta S_parent/delta h has the unique source-independent solution [h0],
local fibre fluctuations are nonpropagating or gapped, and S_matter is blind to [h] except universal constants,
then finite-fibre spectra/traces renormalize constants only and do not create local marker, WEP, clock, Gdot, or fifth-force rows.
```

## 6. Counterexample Fibre Couplings

| counterexample | why_it_breaks | required_blocker |
| --- | --- | --- |
| species_charge_from_trace | WEP/source-charge channel survives while remaining quotient-invariant | constant-sector universality and matter-functor blindness |
| finite_range_fibre_scalar | fifth-force Yukawa mode appears unless beta=0 or m_h lock is derived | nonpropagating/gapped auxiliary theorem plus zero matter vertex |
| source_dependent_stationary_spectrum | local spectrum changes with material source, reopening marker dependence | source-independent Euler-Lagrange solution |
| readout_selected_active_block | the active-marker counterterm returns through the readout projector | readout-after-variation no-cheat theorem |
| nonuniversal_constant_renormalization | measured GM, clock, or species constants drift by sector | universal constants independent of A, D, and local state |
| domain_coupled_spectrum | domain scoring leaks back into parent variables | candidate-before-score and no-backreaction rules |

## 7. Row Transition Attempt

| row_id | previous_state | new_state | result |
| --- | --- | --- | --- |
| R0_identity_coframe_direct | closure_zero | closure_zero | not_upgraded |
| R1_WEP_source_charge | retained_contingent_budget | retained_contingent_budget | not_upgraded |
| R2_clock_redshift | retained_budget | retained_budget | not_upgraded |
| R5_alpha1 | retained_budget | retained_budget | not_upgraded |
| R7_alpha3 | retained_contingent_budget | retained_contingent_budget | not_upgraded |
| R9_Gdot | retained_contingent_budget | retained_contingent_budget | not_upgraded |
| R10_fifth_force | unscored_parameterized | unscored_parameterized | not_upgraded |
| R11_EH_operator_ledger | retained_residual | retained_residual | not_upgraded |

## 8. Gate Results

| gate | status | evidence |
| --- | --- | --- |
| source_paths_exist | pass | all cited source paths exist |
| fibre_observables_classified | pass | 7 fibre observables classified |
| relabel_invariant_class_functions_written | conditional_pass | spec(h), tr(h^n), and trace average are admissible class functions |
| quotient_invariance_not_decoupling_guardrail | pass | class functions are explicitly denied theorem-zero credit without decoupling |
| universal_stationary_spectrum_derived | fail | no parent fibre potential, uniqueness theorem, or source-independent h0 is derived |
| fibre_integrated_out_to_universal_constants | fail | mass gap/Hessian/source-independence and constant-only effective action are not proven |
| matter_functor_blindness_derived | fail | theta_A(spec(h)) and q_A(tr(h^n)) counterexamples remain open |
| constant_sector_independence_derived | fail | species constants are not yet universalized against fibre invariants |
| fifth_force_fibre_mode_excluded | fail | dynamic fibre scalar/Yukawa mode is not excluded by theorem |
| runner_rows_promoted_to_theorem_zero | fail | 0 theorem-credit row upgrades |
| claim_leaks | pass | 0 claim-allowed rows |
| local_GR_promoted | fail | finite-fibre decoupling attempt only; no local-GR pass |
| claim_ceiling_enforced | pass | finite_fibre_spectrum_decoupling_attempt_only_no_WEP_EH_Newton_PPN_fifth_force_flux_domain_or_local_GR_pass |

## 9. Decision

Finite fibre spectra/traces can be admitted as quotient/class-function parent coordinates, but this is not a decoupling theorem. A spectrum or trace invariant can still be a local matter-visible scalar unless the parent action proves a unique universal stationary spectrum, integrates the fibre out to universal constants, and makes the matter functor blind to h. Therefore finite fibre remains allowed only as a disciplined parent support or explicit closure; no WEP, EH, Newtonian, PPN, fifth-force, flux, domain, or local-GR row is promoted.

Practical read: this is a useful narrowing, not a win-condition yet. The finite fibre is not automatically poison, but it is also not automatically silent. It can sit in the parent theory as basis-free support only if the next matter/readout theorem keeps it from becoming a local dial.

## 10. Next Target

`422-matter-functor-blindness-readout-after-variation-theorem-attempt.md`
