# 541 - Y5 Hamiltonian PiM Source-Measure Contract or Residual Scorecard

Generated: 2026-06-04T10:41:29.773217+00:00  
Run: `runs/20260605-054500-Y5-Hamiltonian-PiM-source-measure-contract-or-residual-scorecard`  
Status: `Y5_Hamiltonian_PiM_source_measure_contract_and_residual_scorecard_written_no_measured_GM_or_Newton_promotion`  
Claim ceiling: `source_measure_contract_scorecard_only_no_measured_GM_Newton_PPN_or_local_GR_pass`

## 1. Verdict

The Hamiltonian `Pi_M` branch now has a compact referee card.

The result is blunt:

```text
All measured-GM/Newton/PPN claim gates are still false or not reached.
But each false gate now has a named residual input row.
```

That is progress because the next work no longer has to decide whether a failed proof is fatal or useful. It is useful only if it becomes a theorem-zero row or a source-backed residual row.

## 2. Source-Measure Contract

| contract_id | pass_condition | mathematical_form | current_status | if_fail | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| HSM541_0_adopt_Hamiltonian_PiM | Pi_M is explicitly the Hamiltonian/covariant-phase-space mass-charge map on the local branch | Pi_M J_H := Pi_M^H J_H = ell_H[J_H;tau,S] omega_M^H | candidate_only_not_adopted_or_proved | topological/readout Pi_M remains residual only | false |
| HSM541_1_integrable_charge | Hamiltonian charge has fixed reference, fixed time generator, and integrable variation | delta H_tau = int_S(delta Q_tau - i_tau theta), reference fixed once | not_derived_for_current_MTS | Delta_symp and boundary/reference residual activate | false |
| HSM541_2_observed_worldtube_source | worldtube source measure is fixed by the same observed Hilbert source current before readout | W_source=supp(J_H[e_obs]); M_source[W]=H_tau[S]-H_ref | not_derived | frame/source-measure residual activates | false |
| HSM541_3_radial_closure | the charge is radially closed in compact source-free exterior | int_A(C_EH+C_extra+C_projector+C_boundary)=0 | conditional_EH_reference_C_terms_open | epsilon_radial_Meff and dln_Meff residuals activate | false |
| HSM541_4_zero_extra_source_channels | extra/non-EH/projector/domain/memory/range/frame/boundary channels add no independent mass charge | Delta_nonEH=Delta_extra=Delta_PiM=Delta_frame=Delta_boundary=0 | not_field_specific_derived | mu_extra and channelwise residual vector activate | false |
| HSM541_5_Gauss_orbital_readout | same charge controls Poisson/Gauss surface integral and pure inverse-square orbital acceleration | nabla^2 Phi=4*pi*G_ref*rho_H; a_r=-G_ref*M_source/r^2 | not_derived | Delta_cal, radial hair, and fifth-force residuals activate | false |
| HSM541_6_constant_universal_G | G_eff/kappa is constant, universal, source-blind, range-blind, and frame-blind | partial_t,r,A,lambda,frame G_eff=0 | conditional_not_parent_derived | Gdot, source-charge, and range-dependence residuals activate | false |
| HSM541_7_PPN_followthrough | the same source normalization survives beta/gamma/preferred-frame PPN order | Delta_PPN={gamma-1,beta-1,alpha_i,zeta_i,xi}=0 or below official locks | not_reached | PPN residual envelope remains active | false |

## 3. Scorecard

| score_id | contract_id | pass_status | evidence | residual_if_fail | priority | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| HSS541_0_Hamiltonian_PiM_branch | HSM541_0_adopt_Hamiltonian_PiM | fail_current_claim | 539 wrote candidate; branch not adopted/proved | R_Htop;R_eq;I_commutator | highest | false |
| HSS541_1_charge_integrability | HSM541_1_integrable_charge | fail_current_claim | 510/540 keep reference and boundary terms open | Delta_symp;B_zero_flux | highest | false |
| HSS541_2_worldtube_source_measure | HSM541_2_observed_worldtube_source | fail_current_claim | worldtube source measure not inherited for current MTS | Delta_frame;Delta_cal | highest | false |
| HSS541_3_radial_closure | HSM541_3_radial_closure | fail_current_claim | C_extra/C_projector/C_boundary not field-specific zeroed | epsilon_radial_Meff;dln_Meff | highest | false |
| HSS541_4_extra_channels | HSM541_4_zero_extra_source_channels | fail_current_claim | field-specific silence queue remains open | mu_extra;Delta_nonEH;Delta_PiM;Delta_extra | high | false |
| HSS541_5_Gauss_readout | HSM541_5_Gauss_orbital_readout | fail_current_claim | Poisson/Gauss bridge conditional only; orbital readout not derived | Delta_cal;alpha_lambda;partial_r_ln_mu_obs | highest | false |
| HSS541_6_constant_G | HSM541_6_constant_universal_G | fail_current_claim | constant kappa/G carried conditionally only | dln_Geff_dt;source_charge;range_dependence | high | false |
| HSS541_7_PPN_followthrough | HSM541_7_PPN_followthrough | not_reached | 531 beta envelope missing first-order Newton precondition and components | delta_beta_source;gamma_minus_one;alpha_i;zeta_i;xi | high_after_Newton | false |

## 4. Residual Input Rows

| input_id | quantity | required_columns | acceptance_rule | current_status | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| HSI541_0_boundary_reference | B_zero_flux;Delta_symp | system_id;surface_pair;B_zero_flux;Delta_symp;M_H_ref;units;source_file;assumptions;valid_for_claim | fixed reference convention and source-backed value/theorem zero | not_filled | false |
| HSI541_1_worldtube_frame | Delta_frame;Delta_cal | system_id;source_frame;readout_frame;Delta_frame;Delta_cal;units;source_file;assumptions;valid_for_claim | same-frame theorem or explicit frame/calibration residual below locks | not_filled | false |
| HSI541_2_radial_mass_closure | epsilon_radial_Meff;dln_Meff_dlnr | system_id;r1;r2;epsilon_radial_Meff;dln_Meff_dlnr;bound_source;source_file;assumptions;valid_for_claim | theorem zero or sourced radial bound, no cancellation-only acceptance | not_filled | false |
| HSI541_3_mu_extra_vector | mu_extra;Delta_extra_vector | system_id;channel;Delta_charge;mu_extra_over_GM;local_lock;source_file;assumptions;valid_for_claim | each channel separately zero or below lock | not_filled | false |
| HSI541_4_Gauss_orbital | Delta_cal;alpha_lambda;partial_r_ln_mu_obs | system_id;Delta_cal;alpha_lambda;lambda_scale;partial_r_ln_mu_obs;source_file;assumptions;valid_for_claim | same-frame Gauss/orbit theorem or fifth-force/radial bound | not_filled | false |
| HSI541_5_constant_G | dln_Geff_dt;eta_source;range_dependence | system_id;dln_Geff_dt;eta_source;range_dependence;bound_source;source_file;assumptions;valid_for_claim | constant universal G theorem or official local-bound residual | not_filled | false |
| HSI541_6_PPN_vector | delta_beta_source;gamma_minus_one;alpha_i;zeta_i;xi | system_id;delta_beta_source;gamma_minus_one;alpha_i_vector;zeta_i_vector;xi;source_file;assumptions;valid_for_claim | after first-order Newton precondition passes, compare absolute envelope to official locks | not_filled | false |

## 5. Decision

| decision_id | status | meaning | claim_status | next_action |
| --- | --- | --- | --- | --- |
| D541_0_contract_written | source_measure_contract_scorecard_written | Hamiltonian PiM now has a single referee card from adoption through PPN followthrough | contract_only | 542-Y5-source-measure-theorem-attempt-or-first-residual-fill.md |
| D541_1_all_claim_gates_fail_or_not_reached | no_measured_GM_Newton_or_PPN_promotion | every required source-measure/readout gate is still false or not reached for current MTS | safe_private_work | 542-Y5-source-measure-theorem-attempt-or-first-residual-fill.md |
| D541_2_next_choice | theorem_attempt_or_first_residual_fill | next work should either prove HSM541_1-HSM541_3 or fill first residual rows without pretending | active_private_derivation | 542-Y5-source-measure-theorem-attempt-or-first-residual-fill.md |
| D541_3_private_no_push | private_no_github | no public/GitHub action is performed | safe_private_work | continue_private_derivation |

## 6. Source Register

| source_file | role | exists |
| --- | --- | --- |
| 540-Y5-Hamiltonian-PiM-source-measure-and-PPN-readout-test.md | Hamiltonian Pi_M source-measure and PPN readout gate | True |
| 539-Y5-PiM-as-Hamiltonian-charge-map-or-topological-demotion.md | Hamiltonian Pi_M candidate and topological demotion | True |
| 510-worldtube-source-measure-glue-or-Meff-residual-runner.md | worldtube/source-measure glue and M_eff residual runner | True |
| 458-Hamiltonian-charge-to-Poisson-Gauss-calibration-gate.md | Poisson/Gauss measured-GM calibration gate | True |
| 450-Hilbert-source-to-measured-monopole-calibration-gate.md | Hilbert-monopole measured-GM calibration gate | True |
| 531-Y5-source-normalized-Newton-and-beta-residual-envelope.md | source-normalized Newton precondition and beta envelope | True |
| source-intake/mts_residuals/P8_Y5_HAMILTONIAN_PIM_SOURCE_MEASURE_TEST.csv | 540 source-measure tests | True |
| source-intake/mts_residuals/P8_Y5_HAMILTONIAN_PIM_GAUSS_PPN_TEST.csv | 540 Gauss/PPN readout tests | True |
| source-intake/mts_residuals/P8_Y5_HAMILTONIAN_PIM_RESIDUAL_ACTIVATION.csv | 540 residual activation map | True |
| source-intake/mts_residuals/P8_Y5_SOURCE_NORMALIZATION_RESIDUAL_SCORECARD.csv | existing source-normalized Newton scorecard | True |
| source-intake/mts_residuals/P8_Hamiltonian_charge_Poisson_Gauss_calibration_CONTRACT.csv | Poisson/Gauss calibration contract rows | True |
| source-intake/mts_residuals/P8_Hilbert_monopole_calibration_CONTRACT.csv | Hilbert monopole calibration contract rows | True |
| scripts/Y5_Hamiltonian_PiM_source_measure_contract_or_residual_scorecard.py | this checkpoint generator | True |

## 7. Validation

| check_id | result | detail |
| --- | --- | --- |
| V541_0_source_paths_exist | pass | missing=0 |
| V541_1_prior_540_loaded | pass | source_tests=7;gauss_tests=6 |
| V541_2_prior_residual_activation_loaded | pass | residual_activation_rows=7 |
| V541_3_contract_scorecard_complete | pass | contract_rows=8;scorecard_rows=8 |
| V541_4_residual_inputs_complete | pass | residual_input_rows=7 |
| V541_5_all_score_rows_fail_or_not_reached | pass | fail_or_not_reached_rows=8 |
| V541_6_no_claim_rows | pass | claim_contract_rows=0;claim_score_rows=0;claim_input_rows=0 |
| V541_7_no_overclaim | pass | source_measure_contract_only=true; measured_GM=false; Newton=false; beta=false; PPN=false; local_GR=false |

## 8. Route Update

| route_id | previous_status | new_status | accepted_for_claim | next_target |
| --- | --- | --- | --- | --- |
| HAMILTONIAN_PIM_SOURCE_MEASURE | central_next_contract_or_residual_scorecard | contract_scorecard_written_all_claim_gates_open | false | 542-Y5-source-measure-theorem-attempt-or-first-residual-fill.md |
| SOURCE_NORMALIZED_NEWTON | still_blocked_source_measure_Gauss_constant_G_residuals | still_blocked_HSS541_0_to_HSS541_6 | false | 542-Y5-source-measure-theorem-attempt-or-first-residual-fill.md |
| BETA_PPN | still_blocked_until_Newton_precondition_passes | still_not_reached_HSS541_7_after_Newton | false | 542-Y5-source-measure-theorem-attempt-or-first-residual-fill.md |
| LOCAL_GR | still_blocked_source_measure_Newton_PPN_stack | still_blocked_contract_scorecard_unfilled | false | 542-Y5-source-measure-theorem-attempt-or-first-residual-fill.md |

## 9. Claim Ceiling

Allowed:

```text
MTS has a compact Hamiltonian-PiM source-measure contract and residual scorecard.
Every open gate maps to a theorem target or fillable residual row.
```

Forbidden:

```text
MTS has derived measured GM.
MTS has derived source-normalized Newton.
MTS has passed beta, PPN, or local GR.
```

## 10. Practical Read

This is the boring but powerful bit: the theory now has a scoreboard. If the derivation lands, rows flip to theorem-zero. If it does not, the same rows become residual tests. Either way, no more hiding first-order Newton inside the word "mass".

## 11. Next Target

`542-Y5-source-measure-theorem-attempt-or-first-residual-fill.md`

Next: attempt the theorem route for `HSM541_1` through `HSM541_3`. If it stalls, fill the first residual row instead of inventing closure.
