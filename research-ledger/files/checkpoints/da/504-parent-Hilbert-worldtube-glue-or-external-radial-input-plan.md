# 504 — Parent Hilbert Worldtube Glue or External Radial Input Plan

Generated: 2026-06-04T02:44:59.832045+00:00  
Run: `runs/20260604-154500-parent-Hilbert-worldtube-glue-or-external-radial-input-plan`  
Status: `parent_worldtube_glue_theorem_attempt_built_conditional_not_yet_derived`  
Claim ceiling: `conditional_Noether_mass_charge_route_no_local_GR_or_Newton_promotion_yet`

## 1. Verdict

The route is **alive but conditional**.

The clean GR-like path is not:

```text
assume a local plateau;
assume Pi_M J_H is closed;
assume the topological current is the measured source mass.
```

The clean path is:

```text
derive a parent Noether/constraint mass charge Q_M[τ];
prove Q_M is closed in the compact local exterior;
prove the worldtube source measure reads the same charge;
then epsilon_radial_Meff = 0 follows as a theorem.
```

This is exactly the kind of structure GR has in its Newtonian/local exterior limit: a mass charge is radially stable because the exterior field equations/constraints close it, not because a fitted function is declared flat.

## 2. Core Equation

The next derivation should target this identity:

```text
dQ_M[τ] = C_EH[E_g] + C_extra + C_projector + C_boundary + C_Lambda_sub.
```

Then:

```text
epsilon_radial_Meff(S1,S2)
  = (1/M_ref) integral_A dQ_M[τ]
  = (1/M_ref) integral_A (C_EH + C_extra + C_projector + C_boundary + C_Lambda_sub).
```

Therefore the exact zero theorem is:

```text
C_EH = C_extra = C_projector = C_boundary = C_Lambda_sub = 0
  => epsilon_radial_Meff = 0.
```

That is the non-smuggled plateau. It either comes from the parent action or it remains a closure condition.

## 3. Source Register

| source_file | role | exists |
| --- | --- | --- |
| 503-fill-radial-bound-inputs-or-return-to-parent-glue.md | establishes that no sourced numeric radial inputs are available and derivation must be attempted | True |
| 502-radial-bound-runner-implementation-or-Hilbert-topological-glue.md | defines epsilon_radial_Meff runner and no-data/no-claim state | True |
| 501-topological-Hilbert-current-equality-or-radial-bound-runner.md | shows direct equality Pi_M J_H = J_M_top is not yet derived | True |
| 500-topological-PiM-current-parent-clause-or-radial-bound-runner.md | topological Pi_M current route and Hilbert-equality obstruction | True |
| 499-parent-source-identity-for-closed-PiM-flux-or-radial-template.md | source-current decomposition d(Pi_M J_H) = -Pi_M dJ_extra + [d,Pi_M]J_H + A_parent | True |
| 498-source-normalization-radial-and-calibration-theorem-attempt.md | exact exterior source-current integral for epsilon_radial_Meff | True |
| source-intake/mts_residuals/P8_RADIAL_BOUND_INPUT_AUDIT_FILL_DECISION.csv | decision to avoid placeholder radial scoring | True |
| source-intake/local_bounds/local_bound_claims.csv | local empirical locks that any future residual must pass | True |
| scripts/parent_Hilbert_worldtube_glue_or_external_radial_input_plan.py | this checkpoint generator | True |

## 4. Theorem Clauses

| clause_id | claim | mathematical_form | needed_from_parent_action | status | failure_mode |
| --- | --- | --- | --- | --- | --- |
| W504_0_worldtube_setup | compact source is represented by a worldtube W and the test region is an exterior annulus A with boundaries S1 and S2 linking W | A = exterior(W) between S1 and S2; no source support in A | definition of source support and exterior domain | setup_allowed | no clean inside/outside split means no finite-radius mass-flux theorem |
| W504_1_covariant_parent_Noether_identity | a diffeomorphism-covariant parent action supplies a Noether identity for local translations/time flow | δL = E_A δφ^A + dΘ; J_ξ = Θ(φ,L_ξφ) - i_ξ L; dJ_ξ = -E_A L_ξφ | explicit covariant Lagrangian and boundary term Θ | derivable_if_parent_action_covariant | without an action-level Noether identity the mass current is postulated, not derived |
| W504_2_mass_charge_form | the measured mass channel should be a parent Noether/constraint charge, not an arbitrary fitted Hilbert flux | Pi_M J_H is replaced or identified with dQ_M[τ] plus constraint terms fixed before readout | definition of Q_M[τ], Pi_M, and the source-measure map | not_yet_derived_best_route | a conserved topological current can be the wrong object unless it equals the Hilbert/source mass charge |
| W504_3_exterior_closure_equation | radial independence follows if the parent charge form is closed in the compact exterior | dQ_M[τ] = C_EH + C_extra + C_projector + C_boundary + C_Lambda_sub = 0 in A | vacuum exterior equations, projected extra-sector silence, projector constancy, and boundary/no-flux clause | conditional_not_closed | any nonzero C term is exactly epsilon_radial_Meff source hair |
| W504_4_worldtube_source_measure_glue | the worldtube source measure and the exterior Noether charge must read the same mass | M_source[W] = integral_S Q_M[τ] = M_eff before orbital fitting | interior-to-exterior matching or Gauss-law constraint across W | not_yet_derived_core_missing_piece | closed exterior charge exists but is not proven to be the measured source monopole |
| W504_5_calibration_and_limits | the charge must reduce to GR/Poisson/Newton in the local weak-field limit | Q_M[τ] -> Komar/ADM/Gauss mass charge; ∇²Φ = 4πGρ; exterior ∇²Φ = 0 | normalization of G_ref, τ, and weak-field metric/coframe variables | conditional_limit_target | right-looking conservation law with wrong normalization or wrong Newtonian force |

## 5. Noether Chain

| step_id | equation | meaning | derived_status |
| --- | --- | --- | --- |
| N504_0_variation | δL = E_A δφ^A + dΘ | start from the parent action, not from a hand-named plateau current | requires explicit parent Lagrangian |
| N504_1_diffeomorphism_current | J_ξ = Θ(φ,L_ξφ) - i_ξ L, with dJ_ξ = -E_A L_ξφ | diffeomorphism invariance gives a current identity before fitting data | formal Noether identity if action is covariant |
| N504_2_choose_local_time_flow | ξ = τ in a local stationary/asymptotically inertial exterior | the mass channel is tied to the physical time-flow used by local observers | conditional on local-vacuum/stationary branch |
| N504_3_charge_decomposition | dQ_M[τ] = C_EH[E_g] + C_extra + C_projector + C_boundary + C_Lambda_sub | all ways the finite-radius mass charge can leak are named rather than hidden | template; Q_M and C terms still need parent derivation |
| N504_4_radial_independence | integral_S2 Q_M - integral_S1 Q_M = integral_A dQ_M | epsilon_radial_Meff is exactly the exterior constraint/leakage integral | mathematical identity once Q_M is defined |
| N504_5_zero_condition | C_EH = C_extra = C_projector = C_boundary = C_Lambda_sub = 0 implies epsilon_radial_Meff = 0 | this is the precise no-plateau theorem route | conditional; zero clauses not all derived |
| N504_6_source_measure_readout | M_eff = M_source[W] = integral_S Q_M[τ] | the measured mass is fixed by the parent constraint, not fitted separately at each radius | core missing glue |

## 6. Obstructions

| obstruction_id | problem | fix_needed | severity |
| --- | --- | --- | --- |
| O504_0_wrong_conserved_object | a topological current can be closed but fail to equal the Hilbert/source mass charge | derive Pi_M J_H = dQ_M[τ] + exact zero-flux terms, or define the measured mass directly through Q_M with source-measure matching | fatal_if_unfixed |
| O504_1_projector_commutator | field-dependent Pi_M gives [d,Pi_M]J_H terms in the radial derivative | make Pi_M covariantly constant/topological in the exterior, or retain C_projector in the bound runner | fatal_for_exact_zero |
| O504_2_extra_sector_stress | bulk/domain/memory/non-EH terms can carry mass-channel flux in local vacuum | derive exterior silence/no-hair for each channel or keep channelwise numeric residuals | fatal_for_local_GR_promotion |
| O504_3_stationarity_or_flux | nonstationary systems can radiate or exchange charge through the annulus | restrict theorem to local stationary/quasi-static PPN branch, or add radiation-memory flux terms | branch_condition |
| O504_4_calibration | a closed charge with arbitrary normalization does not prove Newton's G or measured GM | derive weak-field normalization and Poisson/Gauss law limit | fatal_for_Newton_limit |

## 7. External Radial Protocol

| input_id | required_columns | use_if | acceptance_rule |
| --- | --- | --- | --- |
| X504_0_R_eq | system_id;r1;r2;R_eq_integral;norm_convention;units;source_file;assumptions;valid_for_claim | parent equality Pi_M J_H = Q_M route is not derived | must be source-backed, not a placeholder or fitted cancellation |
| X504_1_channel_flux_vector | system_id;channel;r1;r2;I_extra_channel;units;affected_rows;source_file;assumptions;valid_for_claim | extra sectors remain active in the compact exterior | each channel must pass its own local lock without relying on cancellation |
| X504_2_radial_profile | system_id;r1;r2;epsilon_radial_Meff;dln_mu_dlnr;bound_source;pass_fail;notes | orbital/fifth-force data are used to bound radial source hair directly | map to R4/R10/R11 and declare model/baseline dependence |

## 8. Decision

| decision_id | decision | basis | claim_status |
| --- | --- | --- | --- |
| D504_0_best_route | use_parent_Noether_mass_charge_route | this mirrors the GR/Newton structure: exterior field equations close a charge, rather than a plateau axiom setting radial hair to zero | conditional_theorem_route_not_final_claim |
| D504_1_not_yet_enough | do_not_promote_local_GR_or_Newton | Q_M closure, source-measure matching, projector silence, extra-sector silence, and calibration are not all derived | local_GR_claim_allowed_false |
| D504_2_fallback | if_parent_glue_fails_use_external_radial_protocol | the 502 runner is ready but cannot be scored without source-backed input rows | numeric_branch_available_but_empty |

## 9. Validation

| check_id | result | detail |
| --- | --- | --- |
| V504_0_source_paths_exist | pass | missing=0 |
| V504_1_theorem_not_overclaimed | pass | open_core_clauses=W504_2_mass_charge_form;W504_3_exterior_closure_equation;W504_4_worldtube_source_measure_glue |
| V504_2_radial_zero_not_derived | pass | epsilon_radial_Meff_zero_derived=false |
| V504_3_external_protocol_available | pass | protocol_rows=3 |
| V504_4_local_GR_claim_blocked | pass | local_GR_claim_allowed=false |

## 10. Route Update

| route_id | status | update | next_target |
| --- | --- | --- | --- |
| RU504_0 | derivation_route_narrowed | replace arbitrary Pi_M flux proof with parent Noether mass-charge closure plus worldtube source-measure matching | 505-parent-Noether-mass-charge-closure-theorem-or-closure-demotion.md |
| RU504_1 | claim_ceiling_retained | radial source hair is expressible as exterior constraint/leakage integral, but zero is not derived until all C terms vanish | 505-parent-Noether-mass-charge-closure-theorem-or-closure-demotion.md |

## 11. Claim Ceiling

Allowed:

```text
MTS has a precise parent-action contract for deriving local radial source silence.
MTS has reduced epsilon_radial_Meff to a parent charge-closure/leakage identity.
MTS has identified Q_M[τ] source-measure matching as the central missing theorem.
```

Forbidden:

```text
MTS has derived local GR.
MTS has derived Newtonian recovery.
MTS has derived epsilon_radial_Meff = 0.
MTS has proven Pi_M J_H equals a closed topological current.
MTS has scored the radial-bound runner.
```

## 12. Next Target

`505-parent-Noether-mass-charge-closure-theorem-or-closure-demotion.md`

Try to derive the closure equation for `Q_M[τ]` from the parent action. If that cannot be done without extra assumptions, demote the local route to closure-only and use the external radial protocol.
