# 1016 Y5 R10 parent worldtube source-measure selector or R_eq first input

**Status:** The legal selector contract is now explicit: `W_source = closure(supp J_H[tau])` is a valid pre-readout source worldtube only if the parent action owns `J_H`, `e_obs`, `tau`, compact support, linking surfaces, `M_H_ref`, `Pi_M^H`, boundary/reference locks, and coupling descent. Current MTS has not yet signed those clauses.

**Claim ceiling:** no parent selector, source-measure equality, `R_eq` score, measured-GM closure, Newton/GR reduction, R10/R11 pass, PPN pass, or local-GR claim is allowed from 1016.

## Source register
| source_id | source_path | exists | needle_found | role |
| --- | --- | --- | --- | --- |
| SRC1016_0_1015_next | source-intake/mts_residuals/P8_Y5_R10_1015_NEXT_TARGET.csv | true | true | 1015 handoff target. |
| SRC1016_1_1015_audit | source-intake/mts_residuals/P8_Y5_R10_1015_HILBERT_TO_TOPOLOGICAL_EQUALITY_AUDIT.csv | true | true | 1015 equality audit. |
| SRC1016_2_1015_bounds | source-intake/mts_residuals/P8_Y5_R10_1015_R_EQ_BOUND_INPUT_ROWS.csv | true | true | 1015 retained bound rows. |
| SRC1016_3_662_proof_chain | source-intake/mts_residuals/P8_Y5_R10_662_PROOF_CHAIN.csv | true | true | 662 proof chain. |
| SRC1016_4_662_residuals | source-intake/mts_residuals/P8_Y5_R10_662_RESIDUAL_DECOMPOSITION.csv | true | true | 662 residual decomposition. |
| SRC1016_5_662_template | source-intake/mts_residuals/P8_Y5_R10_662_BOUND_INPUT_TEMPLATE.csv | true | true | 662 bound input template. |
| SRC1016_6_663_chain | source-intake/mts_residuals/P8_Y5_R10_663_EULER_WARD_CHAIN_RESULT.csv | true | true | 663 Euler/Ward chain. |
| SRC1016_7_663_priority | source-intake/mts_residuals/P8_Y5_R10_663_RESIDUAL_INPUT_PRIORITY.csv | true | true | 663 residual input priority. |
| SRC1016_8_HSM541_contract | source-intake/mts_residuals/P8_Y5_HAMILTONIAN_SOURCE_MEASURE_CONTRACT.csv | true | true | Hamiltonian source-measure contract. |
| SRC1016_9_source_measure_attempt | source-intake/mts_residuals/P8_Y5_SOURCE_MEASURE_THEOREM_ATTEMPT.csv | true | true | source-measure theorem attempt. |
| SRC1016_10_first_residual | source-intake/mts_residuals/P8_Y5_SOURCE_MEASURE_FIRST_RESIDUAL_INPUT.csv | true | true | first residual input template. |
| SRC1016_11_BOBS_pack | source-intake/mts_residuals/P8_Y5_R10_777_BOBS_SOURCE_MEASURE_FIRST_PACK.csv | true | true | coupling/source/readout descent pack. |
| SRC1016_12_bound_schema | source-intake/mts_residuals/P8_Y5_R10_778_SOURCE_MEASURE_BOUND_SCHEMA.csv | true | true | source-measure bound schema. |
| SRC1016_13_bound_runner | source-intake/mts_residuals/P8_Y5_R10_779_SOURCE_MEASURE_BOUND_RUNNER.csv | true | true | source-measure bound runner. |

## Parent selector contract
| contract_id | required_clause | mathematical_form | current_status | failure_if_missing | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| PSC1016_0_parent_action | explicit diffeomorphism-covariant parent action and symplectic potential | delta L = E_A delta Phi^A + dTheta(Phi,delta Phi) | contract_only_no_full_current_Lagrangian | without a real parent Lagrangian, J_H and Q_tau are placeholders | false |
| PSC1016_1_single_observed_coframe | one observed coframe/metric is used by matter, clocks, rods, and orbital readout | S_matter = S_matter[e_obs,psi_m]; J_H[tau] := delta S_matter/delta e_obs contracted with tau | same_frame_measure_not_parent_signed | frame leakage becomes Delta_frame_source and WEP/PPN preferred-frame debt | false |
| PSC1016_2_fixed_time_generator | time/Hamiltonian generator tau is fixed before source or orbital fitting | L_tau e_obs = O(local stationary branch); tau chosen by parent boundary/asymptotic structure | tau_source_readout_lock_open | mass charge can be readout dependent | false |
| PSC1016_3_support_selector | compact source worldtube is selected by Hilbert source support, not by fitted mass radius | W_source := closure(supp J_H[tau]); S1,S2 link W_source in the source-free exterior | formal_selector_definition_available_conditional | requires compactness/regularity and same-frame source measure | false |
| PSC1016_4_linking_surface_class | linking surfaces are homologous around the same W_source and fixed before readout | partial A = S2 - S1; A cap W_source = empty; [S1]=[S2] in exterior homology | conditional_topological_step | domain sensitivity becomes Delta_worldtube_domain | false |
| PSC1016_5_dressed_source_charge | source normalization is the dressed Hamiltonian/Noether charge, not bare mass | M_H_ref := H_tau[S_outer] - H_ref = integral_S Q_tau after integrability/reference lock | definition_guardrail_pass_but_integrability_missing | R_eq rows cannot be normalized without a real M_H_ref | false |
| PSC1016_6_PiM_Hamiltonian_map | Pi_M is adopted or derived as the Hamiltonian mass-charge map on this branch | Pi_M^H J_H := ell_H[J_H;tau,S] omega_M^H, with ell_H proportional to integral_S Q_tau | candidate_only_not_parent_adopted | old Pi_M/topological labels remain residual branches | false |
| PSC1016_7_coupling_descent_silence | matter/source/readout couplings descend through the same observed variables with no hidden source channel | delta_vertical S_matter = delta_vertical S_readout = 0 or source-backed B_obs_source_measure/M_H bound | not_signed_coupling_bound_schema_only | coupling residual can mimic source-measure failure | false |
| PSC1016_8_boundary_reference_lock | reference, exact improvement, and symplectic boundary terms are fixed once | B_zero_flux=0 and Delta_symp=0, or finite source-backed coefficients with units | missing_theorem_or_source_input | boundary bookkeeping can move the measured source charge | false |
| PSC1016_9_verdict | parent-owned source selector for current MTS | PSC1016_0 through PSC1016_8 must be signed before W_source and M_H_ref can support R_eq claims | fail_current_claim | selector contract is exact, but current MTS has not proved the clauses | false |

## Theorem attempt
| attempt_id | statement | current_status | would_close | current_blocker | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| PST1016_0_selector_lemma | If PSC1016_0-PSC1016_4 hold, W_source := closure(supp J_H[tau]) is a covariant pre-readout compact source selector. | conditional_lemma_pass | turns worldtube selection from fitted mask into parent structure | current parent action and same-frame source current are unsigned | false |
| PST1016_1_source_measure_lemma | If PSC1016_1, PSC1016_2, PSC1016_5, and PSC1016_8 hold, M_H_ref is a dressed source charge with fixed reference. | conditional_lemma_pass | gives the normalization needed by R_eq/B_zero/I_commutator rows | integrability/reference lock is not derived | false |
| PST1016_2_Hamiltonian_PiM_repair | If PSC1016_6 is adopted and signed, Pi_M is no longer an empirical mass selector but the Hamiltonian charge map. | best_repair_candidate_not_promotion | kills the old conserved-wrong-object loophole if old Pi_M is demoted or mapped to Pi_M^H | old topological equivalence and commutator silence remain unproved | false |
| PST1016_3_coupling_descent_gate | If PSC1016_7 is signed, source/readout coupling leakage cannot masquerade as a mass-measure residual. | schema_only_not_signed | protects local-GR recovery from hidden source-measure coupling | 777/778/779 rows are templates with missing parent signatures | false |
| PST1016_4_R_eq_first_input_rule | R_eq, B_zero, and I_commutator may be scored only after M_H_ref, source path, units, and no-cancellation components are real. | runner_rule_written | prevents reference-zero or unnormalized rows from becoming evidence | no first claim-valid input exists | false |
| PST1016_5_verdict | derive parent worldtube-source-measure selector for current MTS | fail_current_claim | the route is precise and viable as a contract, not yet a current-MTS theorem | move next to Hamiltonian PiM reference/integrability lock or source-backed first row | false |

## First input schema
| input_id | quantity | definition | required_columns | current_status | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| FIS1016_0_M_H_ref | M_H_ref | dressed Hamiltonian/Hilbert source charge used to normalize equality residuals | system_id;tau_id;surface_outer;H_tau;H_ref;M_H_ref;units;reference_rule;source_path;assumptions;valid_for_claim | MISSING_M_H_REF | false |
| FIS1016_1_B_zero_Delta_symp_Href | B_zero_flux;Delta_symp;H_ref_shift | boundary/exact/reference/symplectic shift in the compact linked source charge | system_id;surface_pair;B_zero_flux;Delta_symp;H_ref_shift;M_H_ref;units;source_path;assumptions;valid_for_claim | MISSING_BOUNDARY_REFERENCE_INPUT | false |
| FIS1016_2_worldtube_domain_shift | Delta_worldtube_domain | fractional charge shift under allowed W_source/linking-surface selector choices | system_id;domain_rule;surface_pair;Delta_worldtube_domain;M_H_ref;units;source_path;assumptions;valid_for_claim | MISSING_PARENT_WORLDTUBE_SELECTOR | false |
| FIS1016_3_Delta_frame_source | Delta_frame_source | same-frame source/readout mismatch between matter source, clocks, rods, and orbital frame | system_id;source_frame;readout_frame;Delta_frame_source;local_lock;source_path;assumptions;valid_for_claim | MISSING_FRAME_BOUND_OR_THEOREM | false |
| FIS1016_4_R_eq_integral | R_eq_integral | finite shell integral of Pi_M J_H - J_M_top - dB_zero after M_H_ref normalization | system_id;r1;r2;R_eq_integral;M_H_ref;units;normalization;source_path;assumptions;valid_for_claim | MISSING_R_EQ_INTEGRAL | false |
| FIS1016_5_I_commutator | I_commutator | finite annulus integral of [d,Pi_M]J_H if the Hamiltonian PiM chain map is unsigned | system_id;r1;r2;I_commutator;M_H_ref;units;normalization;source_path;assumptions;valid_for_claim | MISSING_I_COMMUTATOR | false |
| FIS1016_6_coupling_descent_certificate | B_obs_source_measure_over_MH | source-measure leakage from coupling/readout descent failure | system_id;source_channel;matter_action_owner;uses_e_obs;uses_q_parent;hidden_frame_map;coupling_descent_status;source_path;valid_for_claim | MISSING_PARENT_SIGNATURE | false |
| FIS1016_7_epsilon_selector | epsilon_selector_Meff | no-cancellation envelope of M_H_ref, boundary, frame, domain, R_eq, commutator, and coupling residuals | system_id;epsilon_selector;component_sum_abs;M_H_ref;normalization;source_path;assumptions;valid_for_claim | MISSING_COMPONENT_INPUTS | false |

## First input runner
| runner_id | input_id | quantity | computed_status | claim_allowed | failure_reasons |
| --- | --- | --- | --- | --- | --- |
| SIR1016_0_M_H_ref | FIS1016_0_M_H_ref | M_H_ref | blocked_missing_inputs | false | MISSING_THEOREM_OR_SOURCE_INPUT;VALID_FOR_CLAIM_FALSE |
| SIR1016_1_B_zero_Delta_symp_Href | FIS1016_1_B_zero_Delta_symp_Href | B_zero_flux;Delta_symp;H_ref_shift | blocked_missing_inputs | false | MISSING_THEOREM_OR_SOURCE_INPUT;VALID_FOR_CLAIM_FALSE |
| SIR1016_2_worldtube_domain_shift | FIS1016_2_worldtube_domain_shift | Delta_worldtube_domain | blocked_missing_inputs | false | MISSING_THEOREM_OR_SOURCE_INPUT;VALID_FOR_CLAIM_FALSE |
| SIR1016_3_Delta_frame_source | FIS1016_3_Delta_frame_source | Delta_frame_source | blocked_missing_inputs | false | MISSING_THEOREM_OR_SOURCE_INPUT;VALID_FOR_CLAIM_FALSE |
| SIR1016_4_R_eq_integral | FIS1016_4_R_eq_integral | R_eq_integral | blocked_missing_inputs | false | MISSING_THEOREM_OR_SOURCE_INPUT;VALID_FOR_CLAIM_FALSE |
| SIR1016_5_I_commutator | FIS1016_5_I_commutator | I_commutator | blocked_missing_inputs | false | MISSING_THEOREM_OR_SOURCE_INPUT;VALID_FOR_CLAIM_FALSE |
| SIR1016_6_coupling_descent_certificate | FIS1016_6_coupling_descent_certificate | B_obs_source_measure_over_MH | blocked_missing_inputs | false | MISSING_THEOREM_OR_SOURCE_INPUT;VALID_FOR_CLAIM_FALSE |
| SIR1016_7_epsilon_selector | FIS1016_7_epsilon_selector | epsilon_selector_Meff | blocked_missing_inputs | false | MISSING_THEOREM_OR_SOURCE_INPUT;VALID_FOR_CLAIM_FALSE |

## Claim gate
| gate_id | claim | gate_pass | reason | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| CG1016_0_selector_contract_written | parent worldtube/source-measure selector contract is explicit | true | PSC1016 rows define the required parent clauses | false | false |
| CG1016_1_selector_lemma_claim | W_source=supp(J_H) is parent-owned for current MTS | false | parent action, same-frame source current, tau, and compactness are unsigned | false | false |
| CG1016_2_M_H_ref_claim | M_H_ref is a fixed dressed Hamiltonian source charge | false | integrability/reference/boundary lock is missing | false | false |
| CG1016_3_PiM_H_claim | Pi_M is derived/adopted as Hamiltonian mass-charge map | false | Pi_M_H remains candidate only and old topological PiM is demoted unless bounded | false | false |
| CG1016_4_first_input_claim_ready | first R_eq/B_zero/I_commutator row is source-backed and normalized | false | all first-input rows carry MISSING status | false | false |
| CG1016_5_coupling_descent_zero | source-measure coupling/readout leakage is theorem-zero | false | 777/778/779 source-measure rows are schema/blocked only | false | false |
| CG1016_6_Newton_local_GR | Newton/local-GR gates can reopen | false | source selector, M_H_ref, PiM_H, calibration, and PPN stability remain blocked | false | false |
| CG1016_7_guardrail | selector/R_eq first-input guardrail is installed | true | contract is not promoted and first-input rows stay nonclaim | false | false |

## Decision ledger
| decision_id | decision | because | next_action | valid_for_claim |
| --- | --- | --- | --- | --- |
| DEC1016_0_selector_contract | The legal parent selector is now exact. | W_source may be closure(supp J_H[tau]) only when J_H, e_obs, tau, compactness, linking surfaces, and M_H_ref are parent-owned before readout. | try the Hamiltonian PiM reference/integrability lock, not a new topological shortcut | false |
| DEC1016_1_current_MTS_status | Current MTS does not yet derive the selector. | the support selector is a coherent conditional construction, but the parent action, same-frame source measure, and coupling descent remain unsigned. | keep R_worldtube, Delta_frame_source, M_H_ref, B_zero_flux, I_commutator, and coupling residual rows active | false |
| DEC1016_2_first_input_order | M_H_ref and boundary/reference lock must precede a claim-ready R_eq number. | R_eq, B_zero, and I_commutator are not meaningful evidence until the normalization and reference convention are real. | attempt M_H_ref/Delta_symp/B_zero theorem-zero or source-backed first row | false |
| DEC1016_3_next_target | The next root target is Hamiltonian PiM reference lock or first normalized source row. | without fixed H_tau-H_ref and M_H_ref, no residual row can become scoreable without smuggling the answer. | 1017-Y5-R10-Hamiltonian-PiM-reference-lock-or-MHref-first-row.md | false |

## Validation
| check_id | result | detail | generated_utc |
| --- | --- | --- | --- |
| V1016_SUMMARY | pass | 1016 parent worldtube/source-measure selector validation summary | 2026-06-14T04:58:48.681892+00:00 |
| V1016_0_sources_exist | pass | all source paths exist and needles are present | 2026-06-14T04:58:48.681850+00:00 |
| V1016_1_selector_contract_complete | pass | selector contract covers coframe, tau, support, charge, PiM, coupling, and verdict | 2026-06-14T04:58:48.681861+00:00 |
| V1016_2_contract_blocks_claim | pass | selector contract is nonclaim and blocks current MTS promotion | 2026-06-14T04:58:48.681864+00:00 |
| V1016_3_theorem_attempt_written | pass | conditional selector lemma is written | 2026-06-14T04:58:48.681866+00:00 |
| V1016_4_theorem_current_claim_fails | pass | current theorem route fails without parent signatures | 2026-06-14T04:58:48.681869+00:00 |
| V1016_5_input_schema_complete | pass | first-input schema covers normalization, boundary, frame, domain, R_eq, commutator, coupling, and envelope | 2026-06-14T04:58:48.681871+00:00 |
| V1016_6_input_schema_nonclaim | pass | all first-input rows remain missing and nonclaim | 2026-06-14T04:58:48.681874+00:00 |
| V1016_7_runner_refuses | pass | runner refuses all missing first-input rows | 2026-06-14T04:58:48.681876+00:00 |
| V1016_8_claim_gates_blocked | pass | selector, source-measure, Newton, and local-GR claims remain blocked | 2026-06-14T04:58:48.681878+00:00 |
| V1016_9_guardrail_written | pass | selector/R_eq guardrail is installed | 2026-06-14T04:58:48.681881+00:00 |
| V1016_10_decision_written | pass | 1017 root target decision is written | 2026-06-14T04:58:48.681883+00:00 |
| V1016_11_next_target_written | pass | 1017 target row is present and nonclaim | 2026-06-14T04:58:48.681886+00:00 |
| V1016_12_formalization_untouched | pass | formalization-workbench modified-file count since script start is 0 | 2026-06-14T04:58:48.681888+00:00 |

## Next target
| next_target | objective | include | exclude | valid_for_claim |
| --- | --- | --- | --- | --- |
| 1017-Y5-R10-Hamiltonian-PiM-reference-lock-or-MHref-first-row.md | derive fixed Hamiltonian reference/integrability and M_H_ref for the local source charge, or fill a source-backed first row for M_H_ref plus B_zero_flux/Delta_symp with units and source path | delta H_tau integrability, fixed H_ref, B_zero_flux, Delta_symp, M_H_ref, tau, surface pair, source path, no readout mask, no cancellation | bare mass normalization, reference-only zero, late equality multiplier, unnormalized R_eq row, Newton/local-GR claim, GitHub action | false |

