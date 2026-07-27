# 499 - Parent Source Identity For Closed PiM Flux Or Radial Template

Private source-normalization checkpoint. This is not a public closed-flux proof, mu_extra-zero proof, Newtonian-limit proof, R11 pass, PPN pass, local-GR derivation, cosmology result, EM result, or unified-field claim.

## 1. Purpose

Checkpoint `498` made the radial source-normalization obstruction exact:

```text
epsilon_radial_Meff is proportional to int_A_ext d(Pi_M J).
```

This checkpoint asks whether the parent action can force:

```text
d(Pi_M J_H)=0
```

or whether the row must become a radial source-current template.

Short answer:

```text
Total parent conservation can be written as bookkeeping.
That is not enough.

The useful identity is:

d(Pi_M J_H) = -Pi_M dJ_extra + [d,Pi_M]J_H + A_parent.

So closed Hilbert Pi_M flux follows only if the projected extra-current,
projector commutator, and parent anomaly/multiplier terms vanish.

The current corpus has not proved those vanish.
The exact radial fallback template is now written.
```

## 2. Run Manifest

| Item | Value |
| --- | --- |
| Script | `scripts/parent_source_identity_for_closed_PiM_flux_or_radial_template.py` |
| Run directory | `runs\20260604-143000-parent-source-identity-for-closed-PiM-flux-or-radial-template` |
| Timestamp | `20260604-143000` |
| Generated UTC | `2026-06-04T02:16:15.130116+00:00` |
| Status | `parent_source_identity_decomposed_total_conservation_available_Hilbert_PiM_closure_not_derived_radial_template_written_no_Newton_or_local_GR_promotion` |
| Claim ceiling | `parent_source_identity_decomposition_only_no_closed_PiM_flux_no_mu_extra_zero_Newton_PPN_or_local_GR_promotion` |
| Next target | `500-topological-PiM-current-parent-clause-or-radial-bound-runner.md` |

## 3. Source Register

| source_file | role | exists |
| --- | --- | --- |
| 498-source-normalization-radial-and-calibration-theorem-attempt.md | exact radial residual identity requiring parent source identity | True |
| 497-source-normalization-derived-zero-route-or-numeric-input-template.md | radial and calibration rows selected as theorem-first source-normalization target | True |
| 244-Meff-monopole-source-normalization-or-radial-memory-hair.md | Stokes theorem: closed Pi_M flux gives constant M_eff | True |
| 454-PiM-parent-symplectic-projector-algebra-attempt.md | Pi_M algebra, commutation, and projector variation warning | True |
| 455-PiM-flux-closure-Ward-or-topological-current-attempt.md | mass-channel Ward/topological/Euler routes and overclaim guards | True |
| 456-PiM-projector-variation-stress-ledger.md | product variation and metric-dependent projector stress ledger | True |
| 457-mass-current-Hamiltonian-boundary-charge-attempt.md | GR-like Hamiltonian boundary-charge route | True |
| 458-Hamiltonian-charge-to-Poisson-Gauss-calibration-gate.md | Gauss/orbital measured-GM calibration gate | True |
| 378-source-normalization-Geff-Meff-GM-absorption-theorem.md | measured-GM absorption guardrails | True |
| 402-EH-source-normalization-parent-pair.md | same-frame EH to Poisson source-normalization pair | True |
| source-intake\mts_residuals\P8_RADIAL_MEFF_THEOREM_ATTEMPT.csv | 498 machine radial theorem attempt rows | True |
| source-intake\mts_residuals\P8_RADIAL_CALIBRATION_COUPLING_GATES.csv | 498 machine radial/calibration gate rows | True |
| source-intake\mts_residuals\P8_PiM_parent_symplectic_projector_algebra_CONTRACT.csv | 454 Pi_M algebra contract | True |
| source-intake\mts_residuals\P8_PiM_flux_closure_Ward_topological_CONTRACT.csv | 455 Pi_M flux closure contract | True |
| source-intake\mts_residuals\P8_PiM_projector_variation_stress_CONTRACT.csv | 456 Pi_M projector variation contract | True |
| source-intake\mts_residuals\P8_mass_current_Hamiltonian_boundary_charge_CONTRACT.csv | 457 Hamiltonian boundary-charge contract | True |
| source-intake\mts_residuals\P8_Hamiltonian_charge_Poisson_Gauss_calibration_CONTRACT.csv | 458 Poisson/Gauss calibration contract | True |
| source-intake\mts_residuals\P8_constant_universal_Geff_kappa_CONTRACT.csv | constant universal G_eff/kappa contract | True |
| scripts/parent_source_identity_for_closed_PiM_flux_or_radial_template.py | this checkpoint generator | True |

## 4. Parent Source Identity Attempt

The key distinction is:

```text
dJ_tot = 0
```

does not imply:

```text
d(Pi_M J_H)=0.
```

The local Newton branch needs the second equation, because orbits read the observed Hilbert/measured mass channel, not an arbitrary conserved total charge containing hidden boundary/domain/projector pieces.

| identity_id | identity | mathematical_form | status | what_it_proves | what_it_does_not_prove | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| I499_0_total_parent_Ward | total parent source conservation | dJ_tot = 0 on shell, or dJ_tot equals owned Euler terms that vanish on the full parent equations | available_as_total_accounting_conditional | the full parent source ledger can conserve total charge | the observed Hilbert mass-channel current Pi_M J_H is separately closed | false |
| I499_1_split_total_current | Hilbert plus extra-current split | J_tot = J_H + J_extra, with J_extra = J_boundary + J_domain + J_projector + J_bulk + J_nonEH + J_kappa + J_frame | decomposition_written | all ways of stealing source-normalization are named | J_extra has zero Pi_M projection | false |
| I499_2_projected_product_rule | projected current product rule | d(Pi_M J_H) = Pi_M dJ_H + [d,Pi_M]J_H | exact_if_PiM_is_defined_on_the_current_space | flux closure splits into a source-current term and a projector-commutator term | the commutator vanishes for metric/domain/Hodge Pi_M | false |
| I499_3_parent_source_identity | Hilbert mass closure residual identity | d(Pi_M J_H) = -Pi_M dJ_extra + [d,Pi_M]J_H + A_parent | derived_as_decomposition_not_zero | the exact obstruction to radial M_eff conservation is the projected extra-current plus Pi_M commutator/anomaly | the obstruction is zero | false |
| I499_4_closed_flux_sufficient_conditions | zero theorem conditions | Pi_M dJ_extra=0, [d,Pi_M]J_H=0, A_parent=0 => d(Pi_M J_H)=0 | conditional_sufficient_theorem | the parent proof target is now exact and finite | the current corpus satisfies the target | false |
| I499_5_radial_integral | radial hair numerator | epsilon_radial_Meff = c_M/M_eff * int_A_ext[-Pi_M dJ_extra + [d,Pi_M]J_H + A_parent] | radial_template_formula_written | if the zero theorem fails, the exact numerator to bound is known | the numerator is below local bounds | false |

## 5. Residual Decomposition

The obstruction has now been split into the source-normalization rows that would have to vanish or be numerically bounded:

| residual_id | obstruction | zero_condition | current_status | affected_rows | fallback_observable | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| S499_0_projector_commutator | [d,Pi_M]J_H or (delta Pi_M)J_H | Pi_M is parent-derived as metric-independent/topological absolute charge data, or projector stress is theorem-cancelled | not_parent_derived | R3;R4;R7;R8;R10;R11 | projector-domain stress; radial source hair; nonEH operator vector | false |
| S499_1_boundary_improvement | Pi_M dJ_boundary or boundary owner flux | compact boundary mass flux is zero or a universal derivative-silent constant calibration | fail_open | R3;R4;R7;R8;R9;R11 | boundary monopole shift; alpha3; xi; Gdot; beta source hair | false |
| S499_2_domain_projector | Pi_M dJ_domain plus domain/homology representative variation | domain selector is topological/covariant and carries no mass projection, vector, anisotropy, or time/range derivative | not_parent_derived | R5;R6;R7;R8;R9;R11 | preferred-frame/location rows and domain source-normalization coefficient | false |
| S499_3_bulk_memory_or_X | Pi_M dJ_bulk or finite-range memory/X exchange | mass-gap/no-source theorem or zero Pi_M projection of bulk exchange | not_derived_numeric_curve_preferred | R4;R10;R11 | alpha(lambda) curve and radial/range source-normalization | false |
| S499_4_nonEH_operator | Pi_M dJ_nonEH and non-EH source residual S_res | same-frame local exterior is metric-only EH plus Lambda or coefficients are bounded | conditional_not_parent_derived | R3;R4;R10;R11 | gamma/beta/fifth-force/operator residual vector | false |
| S499_5_coupling_drift | Pi_M(T_obs d kappa_eff) or running G_eff | constant universal parent kappa/G_eff with no time, range, species, radial, or frame derivative | conditional_not_parent_derived | R1;R4;R9;R10;R11 | Gdot; source-charge; radial/range dependent measured-GM | false |
| S499_6_frame_species_source | J_H is not the same measured source current for all observed matter | same observed coframe and selector-blind source-current theorem | not_parent_derived | R0;R1;R2;R11 | WEP/source eta, clock/frame residuals | false |
| S499_7_parent_anomaly_or_multiplier | A_parent from unowned lambda_M, readout mask, or non-gauge source-normalization multiplier | multiplier is first-class/gauge/topological/Ward-owned, or no multiplier is used | not_satisfied | R1;R4;R7;R9;R11 | closure-only radial residual; no derivation credit | false |

## 6. Route Tests

| route_id | route | test_result | reason | next_action | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| RT499_0_total_Ward_only | use total Ward conservation alone | rejected_for_Hilbert_mass_closure | dJ_tot=0 allows exchange between observed Hilbert mass and hidden/source sectors | must prove zero Pi_M projection of J_extra | false |
| RT499_1_topological_PiM | derive Pi_M as metric-independent absolute cohomology charge and close total mass current | promising_but_not_in_corpus | would kill commutator/projector stress, but still needs on-shell equality to Hilbert measured current | 500-topological-PiM-current-parent-clause-or-radial-bound-runner.md | false |
| RT499_2_Hamiltonian_charge | use observed-time Hamiltonian boundary charge | conditional_downstream_of_EH_boundary_calibration | clean GR route, but EH constraint algebra, charge equality, extra-charge silence, and Gauss calibration are not parent-derived | retain as route after EH/local-boundary action improves | false |
| RT499_3_Euler_multiplier | vary lambda_M to impose d(Pi_M J_H)=0 | closure_only_unless_independently_owned | mathematically sufficient but explanatory only if lambda_M has gauge/topological/Ward origin and no unowned stress | do not use as derivation without parent origin | false |
| RT499_4_numeric_radial_template | fill the exact radial source-current numerator | fallback_required_if_theorem_rows_stay_open | keeps theory testable without pretending local Newton is derived | build radial bound runner if 500 topological route fails | false |

## 7. Radial Template

If the theorem route fails, the fallback is no longer vague:

```text
epsilon_radial_Meff
  = c_M I_parent_radial / M_eff_ref
```

with:

```text
I_parent_radial = int_A_ext[-Pi_M dJ_extra + [d,Pi_M]J_H + A_parent].
```

| template_id | required_quantity | definition | required_columns | maps_to | template_status | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| T499_0_identity_integral | I_parent_radial | int_A_ext[-Pi_M dJ_extra + [d,Pi_M]J_H + A_parent] | system_id;r1;r2;c_M;M_eff_ref;I_parent_radial;norm_convention;units;source_file;assumptions | epsilon_radial_Meff = c_M * I_parent_radial / M_eff_ref | not_filled | false |
| T499_1_commutator_profile | I_commutator | int_A_ext [d,Pi_M]J_H | system_id;projector_type;metric_dependence_flag;I_commutator;units;source_file;assumptions | projector stress and radial/source-normalization rows | not_filled | false |
| T499_2_extra_channel_integrals | I_extra_by_channel | int_A_ext Pi_M dJ_extra separated by boundary/domain/bulk/nonEH/kappa/frame/species | system_id;channel;I_extra;units;affected_rows;source_file;assumptions | mu_extra channel vector and R4/R9/R10/R11 residuals | not_filled | false |
| T499_3_observable_bound | radial_measured_GM_bound | dln_mu_dlnr or finite shell Delta mu/mu inferred from local/orbital data | system_id;r;mu_obs_or_proxy;dln_mu_dlnr;bound_source;units;source_file;assumptions | R4 beta/source hair and R10 fifth-force/radial profile | not_filled | false |

## 8. Validation

| rule_id | rule | result | evidence | claim_effect |
| --- | --- | --- | --- | --- |
| V499_0_sources | all cited source paths exist | pass | missing_sources=0 | traceability only |
| V499_1_prior_contracts_loaded | 498 radial rows and PiM/Hamiltonian/PG contracts are loaded | pass | radial_rows=6;radial_gates=6;FC=9;PV=9;HC=10;PG=11 | 499 tied to prior gates |
| V499_2_identity_decomposition | identity attempt includes total Ward, split, product rule, obstruction identity, zero conditions, and radial integral | pass | identity_rows=6 | decomposition concrete |
| V499_3_residual_coverage | residual decomposition covers commutator, boundary, domain, bulk, nonEH, coupling, frame/species, and anomaly channels | pass | S499_0_projector_commutator;S499_1_boundary_improvement;S499_2_domain_projector;S499_3_bulk_memory_or_X;S499_4_nonEH_operator;S499_5_coupling_drift;S499_6_frame_species_source;S499_7_parent_anomaly_or_multiplier | no hidden source channel |
| V499_4_radial_template | fallback radial template contains identity integral, commutator profile, extra-channel integrals, and observable bound rows | pass | template_rows=4 | test branch ready but unfilled |
| V499_5_no_false_claims | no identity, residual, route, or template row is claim-valid | pass | identity_claims=0;residual_claims=0;route_claims=0;template_claims=0 | no Newton/local-GR promotion |

## 9. Decision

| decision_id | status | meaning | next_action |
| --- | --- | --- | --- |
| D499_0_identity | decomposition_derived_not_zero | the parent source identity reduces closed Hilbert Pi_M flux to zero projected extra-current plus zero projector commutator/anomaly | 500-topological-PiM-current-parent-clause-or-radial-bound-runner.md |
| D499_1_total_conservation | insufficient | total Ward conservation can conserve the whole ledger but does not prove the observed Hilbert mass channel is closed | derive zero Pi_M projection of extra channels or retain radial residuals |
| D499_2_topological_route | best_derivation_route | a metric-independent topological Pi_M current could kill the commutator and avoid Hodge projector stress, but it is not yet in the corpus | 500-topological-PiM-current-parent-clause-or-radial-bound-runner.md |
| D499_3_radial_template | written_unfilled | if the topological/source theorem fails, the exact radial numerator is ready to become a numeric/source-backed bound | build bound runner only after the theorem-first 500 attempt |
| D499_4_promotion | forbidden | no closed Pi_M flux, mu_extra zero, Newtonian recovery, PPN pass, or local-GR pass is earned | 500-topological-PiM-current-parent-clause-or-radial-bound-runner.md |

## 10. Route Update

| route_id | previous_status | new_status | accepted_for_claim | next_target |
| --- | --- | --- | --- | --- |
| PARENT_SOURCE_IDENTITY | closed_PiM_flux_parent_derived_false | identity_decomposed_total_conservation_not_Hilbert_closure | false | 500-topological-PiM-current-parent-clause-or-radial-bound-runner.md |
| RADIAL_MEFF_HAIR | exact_residual_identity_written_parent_closed_flux_missing | radial_numerator_split_into_extra_current_commutator_anomaly | false | 500-topological-PiM-current-parent-clause-or-radial-bound-runner.md |
| TOPOLOGICAL_PIM | conditional_promising_route | best_next_derivation_target_for_commutator_zero_and_stress_silence | false | 500-topological-PiM-current-parent-clause-or-radial-bound-runner.md |
| SOURCE_NORMALIZED_NEWTON | blocked_by_parent_source_identity_and_calibration_lock | still_blocked_by_extra_current_commutator_calibration_and_PPN_source_stability | false | 500-topological-PiM-current-parent-clause-or-radial-bound-runner.md |

## 11. Claim Ceiling

Allowed:

```text
The parent source identity has been reduced to an exact decomposition.
Closed Hilbert Pi_M flux requires zero projected extra-current, zero projector commutator, and zero parent anomaly/multiplier source.
The radial fallback template is now explicit.
```

Forbidden:

```text
MTS has derived d(Pi_M J_H)=0.
MTS has derived epsilon_radial_Meff=0.
MTS has derived mu_extra=0 or source-normalized Newtonian recovery.
MTS has passed R11, PPN, or local GR.
```

## 12. Next Queue

| Priority | Target | Reason |
| --- | --- | --- |
| 1 | `500-topological-PiM-current-parent-clause-or-radial-bound-runner.md` | topological Pi_M is the best remaining derivation route because it can kill the commutator/projector-stress obstruction without using a Hodge metric projector |
| 2 | radial bound runner | if the topological route fails, fill `I_parent_radial` and map it to local radial/source-normalization bounds |
| 3 | parent-fixed calibration lock | even closed flux still needs charge-to-Hilbert-mass and constant universal coupling |
