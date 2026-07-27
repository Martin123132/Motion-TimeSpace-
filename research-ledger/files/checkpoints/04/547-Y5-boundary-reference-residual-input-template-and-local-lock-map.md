# 547 - Y5 Boundary Reference Residual Input Template and Local Lock Map

Generated: 2026-06-04T11:29:42.024936+00:00  
Run: `runs/20260605-101500-Y5-boundary-reference-residual-input-template-and-local-lock-map`  
Status: `Y5_BRR545_residual_input_template_and_local_lock_map_written_no_values_filled`  
Claim ceiling: `BRR545_input_template_and_lock_map_only_no_source_measure_measured_GM_Newton_PPN_or_local_GR_pass`

## 1. Verdict

`BRR545` is now executable once values or theorem certificates exist.

Nothing is filled yet. The important upgrade is that the missing boundary/reference term is no longer just a phrase. It is split into:

```text
epsilon_boundary_reference_abs
= epsilon_B_flux_abs + epsilon_Delta_symp_abs
= |B_zero_flux|/M_H_ref + |Delta_symp|/M_H_ref
```

with a separate `M_H_ref` measured-GM calibration gate. No cancellation credit is allowed.

## 2. Residual Input Template

| input_id | system_id | surface_pair | residual_component | formula | B_zero_flux_over_MH | Delta_symp_over_MH | M_H_ref_status | theorem_zero_certificate_id | source_file | units | normalization | assumptions | numeric_input_status | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| BRI547_0_total_boundary_reference | MTS_Hamiltonian_PiM_local_branch | S_inner_to_S_outer | epsilon_boundary_reference_abs | abs(B_zero_flux_over_MH)+abs(Delta_symp_over_MH) | MISSING_NUMERIC_OR_THEOREM_ZERO | MISSING_NUMERIC_OR_THEOREM_ZERO | MISSING_SAME_FRAME_MEASURED_GM_DENOMINATOR | MISSING_CERTIFICATE | MISSING_SOURCE_FILE | dimensionless | all numerator terms divided by same positive M_H_ref | MISSING_REFERENCE_LOCK_BOUNDARY_COHOMOLOGY_NOHAIR_PROJECTOR_SILENCE_MEASURED_DENOMINATOR | not_loaded | false |
| BRI547_1_boundary_flux | MTS_Hamiltonian_PiM_local_branch | S_inner_to_S_outer | epsilon_B_flux_abs | abs(B_zero_flux_over_MH) | MISSING_NUMERIC_OR_THEOREM_ZERO |  | MISSING_SHARED_DENOMINATOR | MISSING_B_ZERO_FLUX_CERTIFICATE | MISSING_SOURCE_FILE | dimensionless | B_zero_flux/M_H_ref | MISSING_BOUNDARY_EXACT_COHOMOLOGY_ZERO_AND_NO_VECTOR_TENSOR_HAIR | not_loaded | false |
| BRI547_2_reference_symplectic | MTS_Hamiltonian_PiM_local_branch | S_inner_to_S_outer | epsilon_Delta_symp_abs | abs(Delta_symp_over_MH) |  | MISSING_NUMERIC_OR_THEOREM_ZERO | MISSING_SHARED_DENOMINATOR | MISSING_DELTA_SYMP_CERTIFICATE | MISSING_SOURCE_FILE | dimensionless | Delta_symp/M_H_ref | MISSING_REFERENCE_LOCK_AND_PROJECTOR_SYMPLECTIC_SILENCE | not_loaded | false |
| BRI547_3_denominator | MTS_Hamiltonian_PiM_local_branch | S_inner_to_S_outer | M_H_ref_calibration | M_H_ref>0 and GM_orbit=G*M_H_ref in same observed frame |  |  | MISSING_POSITIVE_SAME_FRAME_GM_CERTIFICATE | MISSING_GM_DENOMINATOR_CERTIFICATE | MISSING_SOURCE_FILE | mass_or_GM_declared | same-frame Hilbert/source denominator tied to orbital GM | MISSING_POISSON_GAUSS_ORBITAL_SOURCE_CALIBRATION | not_loaded | false |

## 3. Theorem Certificate Template

| certificate_id | target_component | required_statement | mathematical_form | acceptable_source | current_status | source_file | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| BRC547_0_reference_lock | epsilon_Delta_symp_abs | Hamiltonian reference subtraction is source/surface/frame/time/range independent | partial_t,r,source,frame,lambda Delta_ref=0 | parent action variation ledger or fixed background-subtraction theorem | missing_certificate | MISSING_SOURCE_FILE | false |
| BRC547_1_boundary_cohomology_zero | epsilon_B_flux_abs | exact/improvement boundary form has zero linked-sphere flux in the compact exterior | B_imp=dC and int_S2 B_imp-int_S1 B_imp=int_A dB_imp=0 | relative cohomology theorem or explicit boundary variation proof | missing_certificate | MISSING_SOURCE_FILE | false |
| BRC547_2_boundary_no_hair | epsilon_B_flux_abs | boundary state has no vector, trace-free tensor, preferred-frame, radial, or time hair | T_B^TF=T_B^vector=n_mu P_loc_nu T_B^{mu nu}=partial_t,r,frame T_B=0 | parent-owned scalar homogeneous marker-free boundary theorem | missing_certificate | MISSING_SOURCE_FILE | false |
| BRC547_3_projector_symplectic_silence | epsilon_Delta_symp_abs;M_H_ref_calibration | Pi_M is topological/covariantly constant and has no symplectic stress in the exterior | nabla Pi_M=0 and delta(Pi_M J_H)=Pi_M delta J_H | Pi_M parent charge projector theorem or commutator bound source | missing_certificate | MISSING_SOURCE_FILE | false |
| BRC547_4_measured_GM_denominator | M_H_ref_calibration | same-frame orbital measured GM equals G times the positive Hilbert/source denominator | M_H_ref>0 and GM_orbit=G*M_H_ref | Poisson/Gauss/orbital source-calibration theorem | missing_certificate | MISSING_SOURCE_FILE | false |

## 4. Local Lock Map

| map_id | residual_component | local_row_id | coefficient_needed | pass_rule | current_status | observable | upper_bound | units | test_arena | reference_path_or_url | lock_source_exists | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| BRL547_0_boundary_alpha3 | epsilon_B_flux_abs | R7_alpha3 | c_B_flux_to_alpha3 | abs(c_B_flux_to_alpha3*epsilon_B_flux_abs) <= upper_bound or theorem-zero | coefficient_and_input_missing | alpha3 | 4e-20 | dimensionless | pulsar/solar-system momentum flux | https://www2.math.ethz.ch/EMIS/journals/LRG/Articles/lrr-2014-4/articlese4.html | true | false |
| BRL547_1_boundary_xi | epsilon_B_flux_abs | R8_xi | c_B_flux_to_xi | abs(c_B_flux_to_xi*epsilon_B_flux_abs) <= upper_bound or theorem-zero | coefficient_and_input_missing | xi | 4e-09 | dimensionless | local anisotropy/preferred-location | https://www2.math.ethz.ch/EMIS/journals/LRG/Articles/lrr-2014-4/articlese4.html | true | false |
| BRL547_2_boundary_beta | epsilon_B_flux_abs | R4_beta | c_B_flux_to_beta | abs(c_B_flux_to_beta*epsilon_B_flux_abs) <= upper_bound or theorem-zero | coefficient_and_input_missing | beta_minus_1 | 7.8e-05 | dimensionless | planetary ephemerides/LLR | https://www2.math.ethz.ch/EMIS/journals/LRG/Articles/lrr-2014-4/articlese4.html | true | false |
| BRL547_3_boundary_Gdot | epsilon_B_flux_abs | R9_Gdot | partial_t epsilon_B_flux_abs or dln boundary charge/dt | time derivative maps below Gdot/G lock or theorem derivative-zero | time_profile_missing | Gdot_over_G | 9.6e-15 | yr^-1 | LLR/ephemerides/pulsars | https://www.ife.uni-hannover.de/de/forschung/publikationen/detail-ansicht?tx_univiepure_univiepure%5Buuid%5D=cbe8f824-b21b-4e80-b736-944c3f960f7a; doi:10.3390/universe7020034 | true | false |
| BRL547_4_reference_Gdot | epsilon_Delta_symp_abs | R9_Gdot | partial_t epsilon_Delta_symp_abs | time derivative maps below Gdot/G lock or reference derivative-zero | time_profile_missing | Gdot_over_G | 9.6e-15 | yr^-1 | LLR/ephemerides/pulsars | https://www.ife.uni-hannover.de/de/forschung/publikationen/detail-ansicht?tx_univiepure_univiepure%5Buuid%5D=cbe8f824-b21b-4e80-b736-944c3f960f7a; doi:10.3390/universe7020034 | true | false |
| BRL547_5_reference_fifth_force | epsilon_Delta_symp_abs | R10_fifth_force | radial/range profile alpha_lambda_reference | range-dependent alpha(lambda) curve required; symbolic row cannot pass without profile | range_profile_missing | delta_G_or_fifth_force_yukawa | alpha(lambda) | range-dependent | fifth-force/inverse-square | https://arxiv.org/abs/hep-ph/0307284; doi:10.1146/annurev.nucl.53.041002.110503 | true | false |
| BRL547_6_reference_gamma | epsilon_Delta_symp_abs | R3_gamma | c_Delta_symp_to_gamma | abs(c_Delta_symp_to_gamma*epsilon_Delta_symp_abs) <= upper_bound or theorem-zero | coefficient_and_input_missing | gamma_minus_1 | 2.3e-05 | dimensionless | Cassini/VLBI/solar-system light propagation | https://www.nature.com/articles/nature01997; doi:10.1038/nature01997 | true | false |
| BRL547_7_denominator_WEP | M_H_ref_calibration | R1_WEP_source_charge | eta_source_from_denominator_mismatch | source/species dependence maps below WEP source-charge row or same-source theorem | same_source_certificate_missing | eta_WEP_source_charge | 2.8e-15 | dimensionless | MICROSCOPE/Eotvos/composition | https://arxiv.org/abs/2209.15487; doi:10.1103/PhysRevLett.129.121102 | true | false |
| BRL547_8_denominator_Gdot | M_H_ref_calibration | R9_Gdot | partial_t ln(G*M_H_ref/GM_orbit) | time drift maps below Gdot/G lock or constant denominator theorem | same_frame_time_certificate_missing | Gdot_over_G | 9.6e-15 | yr^-1 | LLR/ephemerides/pulsars | https://www.ife.uni-hannover.de/de/forschung/publikationen/detail-ansicht?tx_univiepure_univiepure%5Buuid%5D=cbe8f824-b21b-4e80-b736-944c3f960f7a; doi:10.3390/universe7020034 | true | false |
| BRL547_9_denominator_operator | M_H_ref_calibration | R11_EH_operator_ledger | non_EH_source_normalization_operator_vector | operator-family source normalization must be theorem-zero or executable below locks | operator_vector_missing | non_EH_operator_coefficients | symbolic | operator family | local operator closure | 425-EH-operator-retained-ledger-and-source-normalization-test-plan.md | true | false |

## 5. Evaluator Dry Run

| input_id | residual_component | dryrun_value | numeric_status | source_file | theorem_zero_certificate_id | current_status | valid_for_claim | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| BRI547_0_total_boundary_reference | epsilon_boundary_reference_abs |  | not_computed_missing_component_values | MISSING_SOURCE_FILE | MISSING_CERTIFICATE | not_claimable | false | template row only; fill numeric value or theorem certificate before scoring |
| BRI547_1_boundary_flux | epsilon_B_flux_abs |  | not_computed_missing_B_zero_flux_over_MH | MISSING_SOURCE_FILE | MISSING_B_ZERO_FLUX_CERTIFICATE | not_claimable | false | template row only; fill numeric value or theorem certificate before scoring |
| BRI547_2_reference_symplectic | epsilon_Delta_symp_abs |  | not_computed_missing_Delta_symp_over_MH | MISSING_SOURCE_FILE | MISSING_DELTA_SYMP_CERTIFICATE | not_claimable | false | template row only; fill numeric value or theorem certificate before scoring |
| BRI547_3_denominator | M_H_ref_calibration |  | not_computed_missing_GM_denominator_certificate | MISSING_SOURCE_FILE | MISSING_GM_DENOMINATOR_CERTIFICATE | not_claimable | false | template row only; fill numeric value or theorem certificate before scoring |

## 6. Acceptance Gates

| gate_id | gate | acceptance_rule | current_status | valid_for_claim |
| --- | --- | --- | --- | --- |
| AG547_0_template_complete | BRR545 input template has total, boundary-flux, reference-symplectic, and denominator rows | exactly four input rows and all valid_for_claim=false until filled | pass_template_written | false |
| AG547_1_local_locks_mapped | each active residual component maps to local empirical/internal lock rows | all external lock row_ids exist in local_bound_claims.csv | pass_locks_exist | false |
| AG547_2_no_cancellation_credit | total envelope uses absolute components, not cancellation | epsilon_total = abs(B/MH)+abs(Delta/MH); no signed cancellation row | pass_policy_enforced | false |
| AG547_3_measured_GM_precondition | denominator must be same-frame measured GM before Newton/PPN promotion | GM_orbit=G*M_H_ref certificate exists or no measured-GM claim | fail_missing_certificate | false |
| AG547_4_no_public_claim | private residual template cannot promote local GR | source_measure=false; Newton=false; PPN=false; local_GR=false | pass_policy_no_claim | false |

## 7. Decision

| decision_id | status | meaning | claim_status | next_action |
| --- | --- | --- | --- | --- |
| D547_0_input_template_written | BRR545_input_template_written_unfilled | epsilon_B_flux_abs, epsilon_Delta_symp_abs, and M_H_ref now have explicit fill columns | template_only | 548-Y5-boundary-reference-theorem-certificate-attempt-or-first-numeric-bound-fill.md |
| D547_1_lock_map_written | local_lock_map_written_no_pass | boundary/reference components are mapped to WEP, gamma, beta, alpha3, xi, Gdot, fifth-force, and R11 locks | no_local_bound_pass_until_coefficients_or_theorem_certificates_exist | 548-Y5-boundary-reference-theorem-certificate-attempt-or-first-numeric-bound-fill.md |
| D547_2_next_best_route | theorem_certificate_or_first_numeric_bound_fill | try to derive a certificate first; if not, fill one numeric bound row with source-backed coefficient/profile | active_private_research | 548-Y5-boundary-reference-theorem-certificate-attempt-or-first-numeric-bound-fill.md |
| D547_3_private_no_push | private_no_github | no public/GitHub action is performed | safe_private_work | continue_private_derivation |

## 8. Source Register

| source_file | role | exists |
| --- | --- | --- |
| 546-Y5-parent-action-boundary-reference-clause-search-or-residual-score.md | MAC545 ownership search and BRR545 scorecard | True |
| 545-Y5-boundary-reference-minimal-action-clause-or-residual-row.md | minimal sufficient contract and retained BRR545 row | True |
| 523-Y5-Gauss-orbital-calibration-or-source-normalization-residual-score.md | source-normalization and Gauss/orbital calibration gate | True |
| 524-Y5-second-order-PPN-source-stability-or-residual-evaluator.md | second-order PPN source-stability residual evaluator | True |
| 530-Y5-R11-beta-component-vector-or-EH-nohair-theorem.md | R11/beta component vector and boundary/projector component locks | True |
| 531-Y5-source-normalized-Newton-and-beta-residual-envelope.md | source-normalized Newton precondition gate | True |
| 532-Y5-measured-GM-source-current-closure-or-first-input-fill.md | measured-GM source-current closure attempt | True |
| source-intake/local_bounds/local_bound_claims.csv | local empirical lock rows used only as gates, not pass evidence | True |
| source-intake/mts_residuals/P8_Y5_BOUNDARY_REFERENCE_RESIDUAL_SCORECARD.csv | 546 BRR545 scorecard | True |
| source-intake/mts_residuals/P8_Y5_SOURCE_NEWTON_PRECONDITION_GATE.csv | Newton/source precondition gate | True |
| source-intake/mts_residuals/P8_Y5_PPN_RESIDUAL_VECTOR.csv | PPN residual vector | True |
| source-intake/mts_residuals/P8_LOCAL_GR_RESIDUAL_BOUND_REGISTER.csv | local GR residual bound register | True |
| scripts/Y5_boundary_reference_residual_input_template_and_local_lock_map.py | this checkpoint generator | True |

## 9. Validation

| check_id | result | detail |
| --- | --- | --- |
| V547_0_source_paths_exist | pass | missing=0 |
| V547_1_prior_546_clean | pass | prior_validation_rows=8;prior_fails=0 |
| V547_2_prior_scorecard_loaded | pass | prior_scorecard_rows=4 |
| V547_3_local_bound_rows_loaded | pass | local_bound_rows=12;missing_lock_rows=0 |
| V547_4_templates_complete | pass | input_rows=4;certificate_rows=5 |
| V547_5_lock_map_and_PPN_context | pass | lock_rows=10;ppn_vector_rows=12 |
| V547_6_dryrun_no_claim_rows | pass | claim_input=0;claim_cert=0;claim_eval=0;claim_gate=0 |
| V547_7_no_overclaim | pass | BRR545_filled=false; source_measure=false; measured_GM=false; Newton=false; PPN=false; local_GR=false |

## 10. Route Update

| route_id | previous_status | new_status | accepted_for_claim | next_target |
| --- | --- | --- | --- | --- |
| BOUNDARY_REFERENCE_ZERO | MAC545_ownership_search_negative_residual_scorecard_written | BRR545_input_template_and_lock_map_written_unfilled | false | 548-Y5-boundary-reference-theorem-certificate-attempt-or-first-numeric-bound-fill.md |
| SOURCE_MEASURE_THEOREM | blocked_until_BRR545_inputs_or_theorem_zero | blocked_until_BRR545_certificate_or_numeric_bound_pass | false | 548-Y5-boundary-reference-theorem-certificate-attempt-or-first-numeric-bound-fill.md |
| SOURCE_NORMALIZED_NEWTON | blocked_by_measured_denominator_and_unfilled_boundary_reference_score | still_blocked_by_denominator_certificate_and_unfilled_BRR545_values | false | 548-Y5-boundary-reference-theorem-certificate-attempt-or-first-numeric-bound-fill.md |
| LOCAL_GR | still_blocked_but_gap_is_now_scoreable | still_blocked_but_BRR545_is_executable_when_inputs_exist | false | 548-Y5-boundary-reference-theorem-certificate-attempt-or-first-numeric-bound-fill.md |

## 11. Claim Ceiling

Allowed:

```text
MTS has an explicit BRR545 input template.
MTS has mapped BRR545 components to local locks.
MTS has a dry-run evaluator showing the rows are not claimable until filled.
```

Forbidden:

```text
MTS has filled BRR545.
MTS passes source-measure, measured GM, Newton, PPN, or local GR.
```

## 12. Practical Read

This is boring engineering in the best possible way. The local-GR branch now has a socket for the missing boundary/reference piece. Next we either plug in theorem certificates, or we plug in conservative numeric/profile bounds.

The first serious attempt should be theorem-first:

```text
reference lock -> boundary cohomology/no-hair -> projector silence -> measured denominator
```

If theorem-first fails, the fallback is not handwaving; it is the `BRI547` input table.

## 13. Next Target

`548-Y5-boundary-reference-theorem-certificate-attempt-or-first-numeric-bound-fill.md`

Next: attempt the theorem certificates in order, starting with the reference-lock certificate. If that does not close, fill the first numeric/profile bound row rather than hiding the residual.
