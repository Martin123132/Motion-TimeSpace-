# 540 - Y5 Hamiltonian PiM Source-Measure and PPN Readout Test

Generated: 2026-06-04T10:37:38.018160+00:00  
Run: `runs/20260605-051500-Y5-Hamiltonian-PiM-source-measure-and-PPN-readout-test`  
Status: `Y5_Hamiltonian_PiM_readout_test_written_source_measure_and_PPN_gates_open_no_Newton_or_local_GR_promotion`  
Claim ceiling: `Hamiltonian_PiM_source_measure_PPN_gate_only_no_measured_GM_Newton_PPN_or_local_GR_pass`

## 1. Verdict

The Hamiltonian `Pi_M^H` pivot is useful, but it is not enough by itself.

It repairs the old topological wrong-object risk at the charge-map level:

```text
Pi_M^H J_H := ell_H[J_H;tau,S] omega_M^H
```

But source-normalized Newton still requires:

```text
worldtube source measure = dressed Hamiltonian charge
same-frame Poisson/Gauss coefficient
pure inverse-square orbital readout
constant universal G_eff
zero mu_extra/source residuals
```

and local GR still requires the same branch to pass the second-order PPN vector.

## 2. Source-Measure Tests

| test_id | gate | mathematical_form | current_result | blocks | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| SMT540_0_branch_adoption | Hamiltonian Pi_M branch is adopted as the parent mass-charge representative, not merely named | Pi_M := Pi_M^H and old Pi_M^top is discarded or mapped to Pi_M^H + residuals | candidate_only_not_adopted_or_proved | DAT537_4;source_normalized_Newton | false |
| SMT540_1_charge_integrability | Q_tau has fixed reference, boundary term, and integrable Hamiltonian variation | delta H_tau = integral_S(delta Q_tau - i_tau theta) with integrable reference subtraction | not_derived_for_current_MTS | measured_GM;absolute_calibration | false |
| SMT540_2_same_source_worldtube | the worldtube source measure is the same observed Hilbert matter source used by Q_tau | W_source=supp(J_H[e_obs]); M_source[W]=H_tau[S]-H_ref before orbital fitting | not_derived | measured_GM;Newton | false |
| SMT540_3_radial_closure | Hamiltonian mass charge is radially closed in the compact source-free exterior | int_S2 Q_tau - int_S1 Q_tau = int_A(C_EH+C_extra+C_projector+C_boundary)=0 | conditional_EH_reference_only_C_terms_open | epsilon_radial_Meff;source_normalized_Newton | false |
| SMT540_4_no_extra_mass_channels | non-EH, projector, domain, memory, range, connection, frame, and boundary channels add no independent mass charge | Delta_nonEH=Delta_PiM=Delta_extra=Delta_frame=Delta_symp=0 or source-backed below locks | not_field_specific_derived | mu_extra;Gdot;fifth_force;PPN | false |
| SMT540_5_old_topological_equivalence_optional | old Pi_M^top need not be saved, but if cited it must equal Pi_M^H up to zero-flux terms | Pi_M^top J_H - Pi_M^H J_H = R_Htop + dB_Htop | old_topological_route_demoted_unless_residuals_zero_or_bounded | topological_PiM_claim_credit | false |
| SMT540_6_measured_source_definition | M_source is explicitly dressed Hamiltonian/Noether source charge, not bare rest mass | M_source[W] := H_tau[S_outer]-H_tau[reference] | definition_guardrail_pass_but_not_full_MTS_theorem | public_claim_only_if_promoted | false |

## 3. Gauss/PPN Readout Tests

| test_id | gate | mathematical_form | current_result | claim_effect | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| GPT540_0_Poisson_coefficient | same-frame weak-field equation reduces to Poisson with standard coefficient | g_00=-1+2Phi/c^2; nabla^2 Phi=4*pi*G_ref*rho_H | conditional_from_prior_EH_branch_not_current_promotion | first_order_Newton_not_earned | false |
| GPT540_1_Gauss_surface_calibration | Poisson surface integral equals Hamiltonian Pi_M source mass with no source residual | surface_integral grad Phi.dS = 4*pi*G_ref*M_source and S_res=0 | not_parent_derived | measured_GM_false | false |
| GPT540_2_orbital_inverse_square_readout | test bodies read the same potential as pure inverse-square acceleration | a_r=-partial_r Phi=-G_ref*M_source/r^2 with no Yukawa/radial/frame/species hair | not_derived | Newton_false | false |
| GPT540_3_constant_universal_G | G_eff/kappa is constant, universal, source-blind, range-blind, and frame-blind | partial_t,r,A,lambda,frame G_eff=0 | conditional_not_parent_derived | Gdot_source_charge_range_rows_active | false |
| GPT540_4_beta_source_stability | same measured-GM normalization survives second-order beta order | delta_beta_source=0 and B_source/A_source^2=1 | not_derived_missing_531_components | beta_false | false |
| GPT540_5_full_PPN_vector | gamma, beta, alpha_i, zeta_i, xi and preferred-frame components are zero or below official locks | Delta_PPN={gamma-1,beta-1,alpha_i,zeta_i,xi} explicit absolute envelope | not_reached | local_GR_false | false |

## 4. Residual Activation Map

| residual_id | failed_gate | residual_quantity | maps_to | required_artifact | current_status | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| RA540_0_charge_integrability | SMT540_1_charge_integrability | Delta_symp;Delta_boundary_reference | MR510_2;PG0;PG4 | boundary/reference theorem or source-backed boundary shift row | unfilled | false |
| RA540_1_source_measure | SMT540_2_same_source_worldtube | Delta_frame;Delta_cal | MR510_5;MR510_6;HM0;HM3 | same-frame worldtube source theorem or calibration residual row | unfilled | false |
| RA540_2_radial_closure | SMT540_3_radial_closure | epsilon_radial_Meff;dln_Meff | MR510_0;P8_Y5_PIM_INPUT_FILL_TEMPLATE | C-term zero theorem or sourced radial profile/bound | unfilled | false |
| RA540_3_extra_mass_channels | SMT540_4_no_extra_mass_channels | mu_extra;Delta_nonEH;Delta_PiM;Delta_extra | MR510_1;MR510_3;MR510_4;PG6 | field-specific silence theorem or channelwise residual vector | unfilled | false |
| RA540_4_Gauss_orbital | GPT540_1_Gauss_surface_calibration;GPT540_2_orbital_inverse_square_readout | Delta_cal;alpha(lambda);partial_r ln mu_obs | PG4;PG5;PG10;R10;R11 | Gauss/orbital readout theorem or fifth-force/radial residual | unfilled | false |
| RA540_5_constant_G | GPT540_3_constant_universal_G | dln_Geff_dt;source_charge;range_dependence | PG7;PG8;R1;R9;R10 | constant kappa/G theorem or Gdot/source/range rows | unfilled | false |
| RA540_6_PPN | GPT540_4_beta_source_stability;GPT540_5_full_PPN_vector | delta_beta_source;gamma_minus_one;alpha_i;zeta_i;xi | PG9;MR510_7;ENV531 | second-order weak-field/PPN expansion or residual envelope inputs | unfilled | false |

## 5. Decision

| decision_id | status | meaning | claim_status | next_action |
| --- | --- | --- | --- | --- |
| D540_0_Hamiltonian_PiM_not_enough | candidate_charge_map_does_not_by_itself_derive_measured_GM | Pi_M^H fixes the wrong-object problem only at charge-map level; source-measure and readout gates remain | measured_GM_false | 541-Y5-Hamiltonian-PiM-source-measure-contract-or-residual-scorecard.md |
| D540_1_source_measure_gate_open | worldtube_source_measure_not_derived | M_source must still be proved to equal the dressed Hamiltonian charge in the observed frame | Newton_false | 541-Y5-Hamiltonian-PiM-source-measure-contract-or-residual-scorecard.md |
| D540_2_Poisson_Gauss_gate_open | Gauss_orbital_readout_not_derived | the same charge must still control Poisson/Gauss and pure inverse-square orbital readout | source_normalized_Newton_false | 541-Y5-Hamiltonian-PiM-source-measure-contract-or-residual-scorecard.md |
| D540_3_PPN_gate_not_reached | beta_and_PPN_not_promoted | PPN stays blocked until first-order source-normalized Newton closes | local_GR_false | 541-Y5-Hamiltonian-PiM-source-measure-contract-or-residual-scorecard.md |
| D540_4_private_no_push | private_no_github | no public/GitHub action is performed | safe_private_work | continue_private_derivation |

## 6. Source Register

| source_file | role | exists |
| --- | --- | --- |
| 539-Y5-PiM-as-Hamiltonian-charge-map-or-topological-demotion.md | Hamiltonian Pi_M candidate and topological Pi_M demotion | True |
| 510-worldtube-source-measure-glue-or-Meff-residual-runner.md | worldtube/source-measure glue and PPN readout warning | True |
| 458-Hamiltonian-charge-to-Poisson-Gauss-calibration-gate.md | Hamiltonian charge to measured orbital GM calibration gate | True |
| 450-Hilbert-source-to-measured-monopole-calibration-gate.md | Hilbert source to measured monopole calibration gate | True |
| 531-Y5-source-normalized-Newton-and-beta-residual-envelope.md | source-normalized Newton precondition and beta residual envelope | True |
| 538-Y5-minimal-parent-action-Euler-Ward-test-or-closure-demotion.md | Euler/Ward chain test that isolated DAT537_4 | True |
| source-intake/mts_residuals/P8_Y5_PIM_HAMILTONIAN_BRANCH_DEFINITION.csv | 539 Hamiltonian Pi_M candidate rows | True |
| source-intake/mts_residuals/P8_Y5_PIM_HAMILTONIAN_GATE_RESULTS.csv | 539 open Hamiltonian Pi_M gates | True |
| source-intake/mts_residuals/P8_Y5_TOPOLOGICAL_PIM_DEMOTION_LEDGER.csv | 539 demotion of old topological Pi_M route | True |
| source-intake/mts_residuals/P8_Hamiltonian_charge_Poisson_Gauss_calibration_CONTRACT.csv | 458 Poisson/Gauss calibration contract | True |
| source-intake/mts_residuals/P8_Hilbert_monopole_calibration_CONTRACT.csv | 450 Hilbert-monopole measured-GM calibration contract | True |
| source-intake/mts_residuals/P8_Y5_SOURCE_NORMALIZATION_RESIDUAL_SCORECARD.csv | 531/523 source-normalized Newton scorecard | True |
| source-intake/local_bounds/local_bound_claims.csv | local PPN/source-normalization empirical locks | True |
| scripts/Y5_Hamiltonian_PiM_source_measure_and_PPN_readout_test.py | this checkpoint generator | True |

## 7. Validation

| check_id | result | detail |
| --- | --- | --- |
| V540_0_source_paths_exist | pass | missing=0 |
| V540_1_prior_539_loaded | pass | hamiltonian_gate_rows=7 |
| V540_2_calibration_contracts_loaded | pass | PG_rows=11;HM_rows=9 |
| V540_3_scorecard_and_bounds_loaded | pass | scorecard_rows=12;local_bounds_rows=12 |
| V540_4_tests_complete | pass | source_measure_rows=7;gauss_ppn_rows=6 |
| V540_5_residual_activation_complete | pass | residual_rows=7 |
| V540_6_no_claim_rows | pass | claim_source_rows=0;claim_gauss_rows=0;claim_residual_rows=0 |
| V540_7_no_overclaim | pass | Hamiltonian_PiM_candidate_only=true; measured_GM=false; Newton=false; beta=false; PPN=false; local_GR=false |

## 8. Route Update

| route_id | previous_status | new_status | accepted_for_claim | next_target |
| --- | --- | --- | --- | --- |
| HAMILTONIAN_PIM | Hamiltonian_charge_map_candidate_written | candidate_survives_but_readout_gates_open | false | 541-Y5-Hamiltonian-PiM-source-measure-contract-or-residual-scorecard.md |
| SOURCE_MEASURE_GLUE | not_derived | central_next_contract_or_residual_scorecard | false | 541-Y5-Hamiltonian-PiM-source-measure-contract-or-residual-scorecard.md |
| SOURCE_NORMALIZED_NEWTON | blocked_source_measure_and_Gauss_readout | still_blocked_source_measure_Gauss_constant_G_residuals | false | 541-Y5-Hamiltonian-PiM-source-measure-contract-or-residual-scorecard.md |
| BETA_PPN | missing_components_not_evaluable | still_blocked_until_Newton_precondition_passes | false | 541-Y5-Hamiltonian-PiM-source-measure-contract-or-residual-scorecard.md |
| LOCAL_GR | still_blocked_PPN_readout_not_reached | still_blocked_source_measure_Newton_PPN_stack | false | 541-Y5-Hamiltonian-PiM-source-measure-contract-or-residual-scorecard.md |

## 9. Claim Ceiling

Allowed:

```text
MTS has a Hamiltonian Pi_M candidate that keeps the measured source charge tied to the parent charge map.
MTS has explicit source-measure, Gauss, Newton, and PPN gates for that branch.
Failed gates now map to residual rows instead of hidden calibration.
```

Forbidden:

```text
MTS has derived measured GM.
MTS has derived source-normalized Newton.
MTS has passed beta, PPN, or local GR.
MTS may treat Hamiltonian Pi_M notation as proof of source-measure glue.
```

## 10. Practical Read

This is a real improvement, but the honest read is still strict: `Pi_M^H` is the right-looking object only if it produces the measured mass that matter orbits read. Until the source-measure/Gauss/PPN stack closes, it is disciplined notation plus a repair route, not a GR reduction theorem.

## 11. Next Target

`541-Y5-Hamiltonian-PiM-source-measure-contract-or-residual-scorecard.md`

Next: turn the open source-measure gates into a compact contract or scorecard. Either prove the worldtube source measure equals `Pi_M^H`, or activate the residual rows for boundary, frame, radial, extra-sector, constant-G, and PPN channels.
