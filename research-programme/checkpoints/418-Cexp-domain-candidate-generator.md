# 418 - Cexp Domain Candidate Generator

Private domain-selector/local-GR checkpoint. This is not a public WEP, Einstein-Hilbert, Newtonian-limit, PPN, fifth-force, flux, domain, cosmology, or unified-field claim.

## 1. Purpose

Checkpoint 417 left the domain circularity problem: `C_exp[D]` cannot honestly select a domain if `D` was chosen after the fact. This checkpoint writes the candidates-first contract: parent variables must generate candidate domains before `C_exp` scores them.

## 2. Run Manifest

| Item | Value |
| --- | --- |
| Script | `scripts/Cexp_domain_candidate_generator.py` |
| Run directory | `runs/20260602-072500-Cexp-domain-candidate-generator` |
| Status | `Cexp_domain_candidate_generator_written_candidates_first_score_second_contract_but_parent_generator_not_derived_no_local_GR_pass` |
| Claim ceiling | `Cexp_domain_candidate_generator_only_no_WEP_EH_Newton_PPN_fifth_force_flux_domain_or_local_GR_pass` |
| Next target | `419-boundary-exchange-coefficient-retained-evaluator.md` |

## 3. Domain Generator Contract

| item | status | requirement |
| --- | --- | --- |
| candidate_before_score | written_not_derived | Generate admissible candidate domains D_i from parent variables before evaluating C_exp[D_i]. |
| no_data_window | pass_guardrail | Candidate domains cannot be chosen from PPN/SPARC/Pantheon/BAO/CMB residual performance. |
| no_lower_limit_import | pass_guardrail | Candidate domains cannot use Newtonian binding energy or GR turnaround surfaces. |
| finite_candidate_set_or_measure | not_derived | The parent action must define either a finite family of D_i or a covariant measure over candidates. |
| single_rule_local_FLRW | not_derived | The same generator must allow local stationary domains and coherent FLRW domains. |
| boundary_exchange_compatibility | not_derived | Generated domains must come with boundary-current/Bianchi bookkeeping. |

## 4. Candidate Domain Sources

| source | status | risk |
| --- | --- | --- |
| relative_current_boundary | best_candidate_contract | J_rel owner and physical representative still not derived |
| Cexp_extremal_surfaces | promising_but_circular_until_generator_defined | C_exp is defined on D, so variational measure over D_i is needed |
| chiD_parent_level_sets | contract_only | chi_D equation currently needs C_exp and boundary ownership |
| coherence_phase_components | open | threshold/projector origin can become a hidden fit knob |
| topological_boundary_projector | open_best_no_stress_route | physical local-zero/FLRW-nonzero representative not selected |
| empirical_residual_window | forbidden | posthoc rescue knob |

## 5. Scoring Chain

| step | claim | status |
| --- | --- | --- |
| 1 | Parent geometry/current fields generate candidate domains. | not_derived |
| 2 | C_exp is evaluated only after candidates exist. | contract_written |
| 3 | Selector chooses local stationary branch and active FLRW branch by one rule. | kinematic_support_not_selector_theorem |
| 4 | Boundary exchange for selected candidates is owned. | not_derived |
| 5 | No data-tuned candidate survives audit. | guardrail_pass |
| 6 | Local trivial class follows from selected candidate. | conditional_target_not_promoted |

## 6. Anti-Circularity Tests

| test | result |
| --- | --- |
| candidate_generated_before_Cexp_score | contract_only |
| candidate_independent_of_empirical_residuals | guardrail_pass |
| candidate_independent_of_GR_Newton_import | guardrail_pass |
| single_rule_generates_local_and_FLRW | not_derived |
| Bianchi_boundary_bookkeeping_attached | not_derived |
| finite_or_integrable_candidate_family | not_derived |

## 7. Row Impact

| row_id | previous_state | new_state |
| --- | --- | --- |
| R5_alpha1 | retained_budget | retained_budget |
| R6_alpha2 | retained_budget | retained_budget |
| R7_alpha3 | retained_contingent_budget | retained_contingent_budget |
| R8_xi | retained_budget | retained_budget |
| R9_Gdot | retained_contingent_budget | retained_contingent_budget |
| R10_fifth_force | unscored_parameterized | unscored_parameterized |

## 8. Gate Results

| gate | status | evidence |
| --- | --- | --- |
| source_paths_exist | pass | all cited source paths exist |
| candidate_before_score_contract_written | pass | G_parent[fields] -> D_i before C_exp[D_i] |
| candidate_sources_written | pass | 6 candidate sources classified |
| empirical_windows_blocked | pass | residual-based domain windows forbidden |
| Newton_GR_import_blocked | pass | Newtonian binding and GR turnaround imports forbidden |
| parent_candidate_generator_derived | fail | candidate family/measure is contract-level only |
| single_rule_local_FLRW_derived | fail | same generator has not derived both local and FLRW branches |
| boundary_exchange_attached | fail | candidate domains do not yet carry owned boundary exchange currents |
| arbitrary_candidate_family_removed | fail | finite/integrable parent measure over D_i is not derived |
| runner_rows_promoted_to_theorem_zero | fail | 0 theorem-credit row upgrades |
| claim_leaks | pass | 0 claim-allowed rows |
| local_GR_promoted | fail | domain-candidate contract only; no EH/Newton/PPN/local-GR pass |
| claim_ceiling_enforced | pass | Cexp_domain_candidate_generator_only_no_WEP_EH_Newton_PPN_fifth_force_flux_domain_or_local_GR_pass |

## 9. Decision

The C_exp selector is now protected against its main circularity by a candidates-first contract: parent variables must generate admissible domains before C_exp scores them. The best candidate sources are relative-current boundaries, topological boundary projectors, or auxiliary chi_D level-set structures. The contract blocks empirical residual windows, Newtonian binding energy, and GR turnaround imports. But the parent candidate generator is not derived: the candidate family/measure, single local-FLRW rule, and attached boundary-exchange bookkeeping remain open. Therefore C_exp remains a promising selector contract, not a local-GR derivation.

Practical read: this is the fair-play rule for `C_exp`. We can use it as footwork only after the ring is drawn by the theory, not by the judges after the round.

## 10. Next Target

`419-boundary-exchange-coefficient-retained-evaluator.md`
