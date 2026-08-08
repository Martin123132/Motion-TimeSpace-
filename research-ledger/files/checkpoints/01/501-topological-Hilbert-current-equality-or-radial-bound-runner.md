# 501 - Topological Hilbert Current Equality Or Radial Bound Runner

Private source-normalization/topological-projector checkpoint. This is not a public closed-flux proof, mu_extra-zero proof, Newtonian-limit proof, R11 pass, PPN pass, local-GR derivation, cosmology result, EM result, or unified-field claim.

## 1. Purpose

Checkpoint `500` wrote a closed topological current:

```text
J_M_top = Q_M omega_M_top.
```

This checkpoint asks whether it is the same current as the observed Hilbert mass channel:

```text
Pi_M J_H = J_M_top.
```

Short answer:

```text
The equality theorem is not derived.

The best route is to define Q_M from the same parent Hilbert compact-source worldtube before readout.
That route is clean but still missing the parent worldtube/source-measure glue.

Without that glue, J_M_top is a conserved wrong object.
The radial bound runner input template is now written.
```

## 2. Run Manifest

| Item | Value |
| --- | --- |
| Script | `scripts/topological_Hilbert_current_equality_or_radial_bound_runner.py` |
| Run directory | `runs\20260604-150000-topological-Hilbert-current-equality-or-radial-bound-runner` |
| Timestamp | `20260604-150000` |
| Generated UTC | `2026-06-04T02:28:51.445967+00:00` |
| Status | `topological_Hilbert_current_equality_attempt_written_parent_glue_not_derived_radial_bound_runner_input_template_written_no_Newton_or_local_GR_promotion` |
| Claim ceiling | `topological_Hilbert_equality_attempt_only_no_closed_Hilbert_flux_no_mu_extra_zero_Newton_PPN_or_local_GR_promotion` |
| Next target | `502-radial-bound-runner-implementation-or-Hilbert-topological-glue.md` |

## 3. Source Register

| source_file | role | exists |
| --- | --- | --- |
| 500-topological-PiM-current-parent-clause-or-radial-bound-runner.md | selects Hilbert equality as the next exact topological Pi_M theorem | True |
| 499-parent-source-identity-for-closed-PiM-flux-or-radial-template.md | identity decomposition and radial numerator to be bounded if equality fails | True |
| 445-measured-GM-Ward-source-ownership-theorem-attempt.md | Ward/Bianchi source ownership caveat | True |
| 446-source-owner-current-parent-action-contract.md | parent action terms needed for K_owner and q_retained zero | True |
| 449-source-current-Ward-universality-theorem-attempt.md | conditional Hilbert/coframe source current theorem | True |
| 450-Hilbert-source-to-measured-monopole-calibration-gate.md | Hilbert current to measured monopole calibration blockers | True |
| 451-mass-flux-projector-Euler-calibration-attempt.md | mass-flux projector Euler closure and no-ad-hoc multiplier warning | True |
| 458-Hamiltonian-charge-to-Poisson-Gauss-calibration-gate.md | measured-GM calibration guardrails after any charge equality | True |
| source-intake\mts_residuals\P8_TOPOLOGICAL_PIM_PARENT_CLAUSE_ATTEMPT.csv | 500 topological PiM parent clause attempt | True |
| source-intake\mts_residuals\P8_TOPOLOGICAL_PIM_CLOSURE_CONDITIONS.csv | 500 topological PiM closure conditions | True |
| source-intake\mts_residuals\P8_RADIAL_BOUND_RUNNER_SPEC.csv | 500 radial bound runner spec | True |
| source-intake\mts_residuals\P8_source_current_Ward_universality_CONTRACT.csv | 449 source-current Ward universality contract | True |
| source-intake\mts_residuals\P8_Hilbert_monopole_calibration_CONTRACT.csv | 450 Hilbert-to-monopole calibration contract | True |
| source-intake\mts_residuals\P8_mass_flux_projector_Euler_calibration_CONTRACT.csv | 451 mass-flux projector contract | True |
| source-intake\mts_residuals\P8_source_owner_parent_action_terms_CONTRACT.csv | 446 source-owner parent-action contract | True |
| source-intake\mts_residuals\P8_q_retained_zero_conditions_CONTRACT.csv | 446 q-retained zero condition contract | True |
| scripts/topological_Hilbert_current_equality_or_radial_bound_runner.py | this checkpoint generator | True |

## 4. Equality Attempt

The equality target is:

```text
Pi_M J_H = J_M_top + dB_zero + R_eq.
```

Closed Hilbert flux follows only if:

```text
R_eq = 0
and integral_boundary dB_zero = 0.
```

| attempt_id | target | mathematical_form | status | would_close | current_blocker | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| EH501_0_equality_statement | topological-Hilbert equality | Pi_M J_H = J_M_top + dB_zero + R_eq | identity_target_written | if R_eq=0 and boundary integral of dB_zero is zero, closed J_M_top gives closed Pi_M J_H | R_eq is not parent-derived zero | false |
| EH501_1_worldtube_charge_route | define Q_M from the same compact Hilbert source worldtube | Q_M = integral_{Sigma_source} rho_H dV, J_M_top = PD(worldtube Hilbert charge) | best_noncheat_route_conditional | makes the topological charge the same object as Hilbert matter mass, not an independent label | parent worldtube/domain selector and source measure are not derived without readout or preferred-frame leakage | false |
| EH501_2_Ward_current_route | separate Hilbert mass current conservation | nabla_mu T_H^{mu nu}=0 plus observed time/current map gives d(Pi_M J_H)=0 | conditional_sublemma_only | could identify the Hilbert mass current with a closed topological current if no exchange survives | hidden/boundary/domain/nonHilbert exchange and boundary flux are not zero | false |
| EH501_3_parent_glue_clause | parent equality glue | S_glue = int Lambda_eq wedge (Pi_M J_H - J_M_top - dB_zero) | closure_only_without_independent_origin | Euler equation would impose equality directly | without independent gauge/topological/source reason, this is a multiplier relabel of Newton closure | false |
| EH501_4_Hamiltonian_charge_route | boundary charge equality | B_xi/G_parent = Q_M = M_eff[Pi_M J_H] | conditional_downstream_route | would identify topological charge, Hilbert projected mass, and Hamiltonian boundary charge | requires EH constraint algebra, boundary integrability, no extra charge, and Gauss/orbital calibration | false |
| EH501_5_radial_bound_fallback | if equality fails, bound R_eq and source-current numerator | I_parent_radial = int_A_ext dR_eq + residual channels | fallback_template_written | does not close theorem; makes the row testable | numeric/source-backed residual inputs are not filled | false |

## 5. Obstructions

| obstruction_id | obstruction | required_zero_or_repair | current_status | affected_rows | fallback | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| OB501_0_independent_topological_label | Q_M is an independent topological label rather than the Hilbert source charge | define Q_M from same-frame Hilbert source variation before readout | not_parent_derived | R1;R4;R9;R11 | treat J_M_top as conserved wrong object; retain radial/source-normalization rows | false |
| OB501_1_worldtube_domain_selection | source worldtube or S2 class is chosen by local metric/readout/domain rule | covariant/topological parent domain selector fixed before scoring | not_parent_derived | R5;R6;R8;R9;R11 | preferred-frame/location/domain residuals remain active | false |
| OB501_2_boundary_improvement | Pi_M J_H differs from J_M_top by a boundary/improvement term with nonzero compact flux | dB_zero exact with zero boundary integral, or class-only universal constant calibration | fail_open | R3;R4;R7;R8;R9;R11 | boundary monopole/radial flux coefficient row | false |
| OB501_3_hidden_exchange | observed Hilbert matter exchanges mass-channel current with hidden/bulk/domain/nonEH sectors | Pi_M dJ_extra=0 from legal owner/topological/no-hair route | not_parent_derived | R3;R4;R7;R8;R10;R11 | channelwise residual integrals in radial bound runner | false |
| OB501_4_universal_kappa_and_calibration | equality of currents still lacks measured-GM normalization or constant G | Q_M=M_EH and G_parent constant/universal with no derivatives | not_parent_derived | R1;R4;R9;R10;R11 | calibration and Gdot/range/source residual rows | false |
| OB501_5_second_order_stability | first-order equality may fail at PPN beta/source order | delta_beta_source=0 after same measured-GM normalization | not_derived | R4;R11 | no local-GR promotion even if first-order equality lands | false |

## 6. Route Tests

| route_id | route | test_result | reason | next_action | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| R501_0_define_top_charge_from_Hilbert_source | make Q_M the parent-defined Hilbert compact-source charge | best_route_but_not_derived | it avoids conserved-wrong-object failure, but needs a parent worldtube/source-measure selector before readout | derive glue or use radial bound runner | false |
| R501_1_late_equality_multiplier | impose Pi_M J_H = J_M_top with Lambda_eq | rejected_as_derivation | unless independently owned, it inserts the desired closure by hand | only allowed as explicit closure label | false |
| R501_2_Hamiltonian_dictionary | identify both charges through the same Hamiltonian/Noether boundary charge | conditional_downstream | requires EH exterior, integrable charge, no extra sector charge, and Poisson/Gauss calibration | retain for later local EH branch | false |
| R501_3_bound_runner | bound R_eq and residual channel integrals | fallback_now_needed_if_no_new_parent_glue | keeps the source-normalization row empirical and falsifiable without claiming derivation | 502-radial-bound-runner-implementation-or-Hilbert-topological-glue.md | false |

## 7. Bound Runner Input Template

If equality is not derived, the exact fallback is:

| template_id | quantity | definition | required_columns | maps_to | template_status | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| BR501_0_equality_residual | R_eq | Pi_M J_H - J_M_top - dB_zero | system_id;r1;r2;R_eq_integral;norm_convention;units;source_file;assumptions | epsilon_radial_Meff equality residual contribution | not_filled | false |
| BR501_1_boundary_term | B_zero_flux | integral_boundary dB_zero or improvement flux | system_id;boundary_type;B_zero_flux;units;source_file;assumptions | boundary_monopole_shift and radial source hair | not_filled | false |
| BR501_2_channelwise_extra | I_extra_channel | Pi_M dJ_extra by boundary/domain/bulk/nonEH/kappa/frame/species channel | system_id;channel;r1;r2;I_extra_channel;units;affected_rows;source_file;assumptions | mu_extra vector and R4/R9/R10/R11 residuals | not_filled | false |
| BR501_3_bound_decision | epsilon_radial_bound_decision | epsilon_radial_Meff and dln_mu_dlnr compared against local-bound rows | system_id;epsilon_radial_Meff;dln_mu_dlnr;bound_source;pass_fail;no_cancellation_flag;notes | source-normalization local bound decision | not_run | false |

## 8. Validation

| rule_id | rule | result | evidence | claim_effect |
| --- | --- | --- | --- | --- |
| V501_0_sources | all cited source paths exist | pass | missing_sources=0 | traceability only |
| V501_1_prior_contracts_loaded | 500 topological clause, Ward, Hilbert, mass-flux, and bound spec rows are loaded | pass | topo=7;SC=9;HM=9;MF=9;bound_spec=4 | 501 tied to prior gates |
| V501_2_equality_attempts | equality attempt covers statement, worldtube route, Ward route, glue clause, Hamiltonian route, and bound fallback | pass | equality_rows=6 | theorem attempt concrete |
| V501_3_obstruction_coverage | obstructions cover independent label, domain selection, boundary, hidden exchange, calibration, and second-order stability | pass | OB501_0_independent_topological_label;OB501_1_worldtube_domain_selection;OB501_2_boundary_improvement;OB501_3_hidden_exchange;OB501_4_universal_kappa_and_calibration;OB501_5_second_order_stability | no hidden equality debt |
| V501_4_bound_input_template | radial bound input template covers equality residual, boundary term, channelwise extra, and bound decision | pass | bound_input_rows=4 | test branch explicit but unfilled |
| V501_5_no_false_claims | no equality, obstruction, route, or template row is claim-valid | pass | equality_claims=0;obstruction_claims=0;route_claims=0;template_claims=0 | no Newton/local-GR promotion |

## 9. Decision

| decision_id | status | meaning | next_action |
| --- | --- | --- | --- |
| D501_0_equality | not_derived | the closed topological current is not yet proved equal to the observed Hilbert Pi_M mass current | 502-radial-bound-runner-implementation-or-Hilbert-topological-glue.md |
| D501_1_best_route | Hilbert_defined_topological_charge | the only clean derivation route is to define Q_M from the same parent Hilbert compact-source charge before readout | derive parent worldtube/source-measure glue or demote to bound input |
| D501_2_bound_runner | input_template_written | the equality residual and channelwise integrals now have an executable input schema | 502-radial-bound-runner-implementation-or-Hilbert-topological-glue.md |
| D501_3_promotion | forbidden | no closed Hilbert flux, epsilon_radial zero, mu_extra zero, Newton, PPN, or local-GR pass is earned | 502-radial-bound-runner-implementation-or-Hilbert-topological-glue.md |

## 10. Route Update

| route_id | previous_status | new_status | accepted_for_claim | next_target |
| --- | --- | --- | --- | --- |
| TOPOLOGICAL_HILBERT_EQUALITY | key_remaining_theorem | not_derived_parent_glue_missing | false | 502-radial-bound-runner-implementation-or-Hilbert-topological-glue.md |
| TOPOLOGICAL_PIM | conditional_topological_current_clause_written_Hilbert_equality_missing | conserved_wrong_object_risk_explicit | false | 502-radial-bound-runner-implementation-or-Hilbert-topological-glue.md |
| RADIAL_BOUND_FALLBACK | bound_runner_schema_written_not_filled | equality_residual_input_template_written | false | 502-radial-bound-runner-implementation-or-Hilbert-topological-glue.md |
| SOURCE_NORMALIZED_NEWTON | still_blocked_by_Hilbert_equality_extra_projection_calibration_and_PPN_source_stability | still_blocked_by_parent_glue_calibration_and_second_order_source_stability | false | 502-radial-bound-runner-implementation-or-Hilbert-topological-glue.md |

## 11. Claim Ceiling

Allowed:

```text
The topological-Hilbert equality theorem has been attempted.
The clean route is parent Hilbert-worldtube definition of Q_M before readout.
The equality residual input template is explicit.
```

Forbidden:

```text
MTS has derived Pi_M J_H = J_M_top.
MTS has derived d(Pi_M J_H)=0.
MTS has derived epsilon_radial_Meff=0.
MTS has derived mu_extra=0 or source-normalized Newtonian recovery.
MTS has passed R11, PPN, or local GR.
```

## 12. Next Queue

| Priority | Target | Reason |
| --- | --- | --- |
| 1 | `502-radial-bound-runner-implementation-or-Hilbert-topological-glue.md` | implement the radial bound runner unless a new parent glue clause can prove Q_M is the same Hilbert source charge |
| 2 | parent Hilbert-worldtube glue | derive Q_M from same-frame Hilbert matter source before readout and without domain leakage |
| 3 | calibration lock | even equality still needs measured-GM/Poisson/Gauss and constant universal G |
