# 789 - Y5 R10 Palatini Tetrad GR Limit With MTS Exchange Contract

Current result: **we now have a clean conditional contract for `MTS -> GR -> Newton`, but not a claim that MTS has satisfied it**. The Palatini/tetrad route says exactly what has to happen: the connection equation must reduce to Levi-Civita, the coframe equation must reduce to Einstein with ordinary matter, MTS stress/exchange/boundary/frame residuals must vanish or be bounded locally, and only then the usual GR weak-field limit gives Newton.

## Status

| status | claim_ceiling | main_result | hard_blocker | next_target | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| Y5_R10_789_palatini_tetrad_GR_Newton_limit_contract_written_MTS_exchange_residuals_explicit_nonclaim | conditional_GR_Newton_limit_contract_only_no_parent_derivation_of_tetrad_no_local_GR_claim | a conditional Palatini/tetrad contract now states exactly how MTS reduces to GR and then Newton: torsion/nonmetricity, T_MTS, Q_nu/q_loc, boundary terms, and frame leakage must vanish or be bounded locally | derive or bound the MTS exchange stress/current/source-measure residual vector; tetrad ownership from MTS remains deeper work | 790-Y5-R10-MTS-exchange-stress-decomposition-and-local-suppression-gates.md | false |

## Palatini Tetrad GR Limit Contract

| contract_id | statement | condition | derived_if_condition_holds | missing_before_claim | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| PTG789_0_field_content | Use coframe e^a, spin connection omega^{ab}, MTS fields Phi_MTS, matter fields Psi, and owned gauge fields. | e is invertible and Lorentzian; omega is independent before variation | metric g_mu_nu = eta_ab e^a_mu e^b_nu and a standard local frame for matter | parent derivation or justified adoption of e/Phi_MTS field content | false |
| PTG789_1_action_form | S = (1/2 kappa_GR) integral epsilon_abcd e^a wedge e^b wedge R^{cd}[omega] + S_MTS[e,omega,Phi_MTS] + S_matter[e,omega,Psi] + S_boundary. | all non-EH terms are covariant and their variations define stress, spin, and exchange currents | a local GR-compatible variational arena | explicit S_MTS and source/boundary terms | false |
| PTG789_2_connection_equation | delta_omega S gives torsion equation; if spin/MTS torsion sources vanish locally, T^a=0 and omega=omega[e]. | tau_spin + tau_MTS_torsion -> 0 or is bounded below local tests | Levi-Civita/spin connection and no hidden torsion force | MTS torsion-source calculation or empirical bound | false |
| PTG789_3_coframe_equation | delta_e S gives Einstein equation G_mu_nu = kappa_GR (T_matter_mu_nu + T_MTS_mu_nu + T_boundary_mu_nu) after omega=omega[e]. | stress tensors are symmetric/equivalent after spin terms and boundary pieces are handled | GR with explicit MTS effective stress | T_MTS decomposition and local suppression theorem | false |
| PTG789_4_GR_recovery | Local GR is recovered when T_MTS, torsion source, nonmetricity source, boundary source, and matter-frame leakage are zero or below local bounds. | R_local = {T_MTS, Q_nu, torsion, boundary, b_g/c_g, W_Ic} -> 0 in the local regime | Einstein equation for ordinary matter in the tested local domain | component-by-component suppression or bound rows | false |
| PTG789_5_Newton_recovery | In the weak-field, slow-motion, quasi-static limit of the recovered GR equation, Poisson/Newton follows. | g_00 = -1 - 2 Phi_N/c^2, pressure/stress small, v << c, residual vector below PPN/orbital bounds | GR -> Newton link is standard once PTG789_4 closes | PPN residual vector and local source model | false |

## Variation Ward Identity Gate

| gate_id | identity_or_variation | result | meaning | missing | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| VWI789_0_local_Lorentz | local Lorentz invariance | requires spin/torsion accounting | antisymmetric stress and spin current must be zero, improved, or carried by torsion | spin/torsion source ledger for MTS and matter | false |
| VWI789_1_diffeomorphism | diffeomorphism invariance | total conservation conditional | nabla_mu(T_matter+T_MTS+T_boundary)^mu_nu=0 when field equations hold | explicit covariant S_MTS and boundary variation | false |
| VWI789_2_exchange_current | matter/MTS split | Q_nu_allowed_but_must_cancel_total | nabla T_matter = Q and nabla T_MTS = -Q is allowed, but Q must vanish or be bounded for local GR matter conservation | Q_nu decomposition connected to q_loc/Gamma_eff/K_hat | false |
| VWI789_3_Bianchi | Bianchi identity | blocks_arbitrary_source_terms | any added MTS stress must be divergence-compatible; otherwise the metric equation is inconsistent | T_MTS construction with Ward identity | false |
| VWI789_4_boundary | boundary/source variation | must_be_silent_or_explicit | source-measure and boundary terms cannot be hidden if they affect local equations | B_obs/source-measure coefficient or theorem-zero | false |

## Newton PPN Residual Vector

| residual_id | quantity | local_GR_requirement | Newton_PPN_effect_if_nonzero | status | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| NPR789_0_torsion | tau_torsion | zero or below spin/torsion local bounds | extra spin/precession/contact force channels | missing_bound_or_theorem_zero | false |
| NPR789_1_T_MTS | T_MTS_mu_nu / T_matter_mu_nu | suppressed in Solar/lab/orbital local regime or absorbed into measured matter source | effective dark/source correction and PPN gamma/beta shifts | missing_decomposition | false |
| NPR789_2_Q_nu | Q_nu or q_loc_nu | matter exchange current vanishes or is bounded in local regime | non-geodesic force or nonconservation signal | missing_q_loc_suppression | false |
| NPR789_3_boundary | B_obs/source-measure | boundary/source-measure terms silent in local patch or explicitly bounded | apparent fifth-force/source-renormalization | missing_source_measure_bound | false |
| NPR789_4_frame | b_g/c_g and W_Ic | ordinary matter sees only e, omega[e], and owned gauge fields | equivalence-principle/PPN/readout violation | active_from_785_786 | false |

## MTS Exchange Input Requirements

| input_id | needed_object | why_needed | acceptance_gate | status | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| MIR789_0_T_MTS_decomposition | T_MTS_mu_nu | tells whether MTS acts as stress, cosmological term, boundary term, or local force | covariant variation of S_MTS with divergence-compatible stress | missing | false |
| MIR789_1_exchange_current | Q_nu / q_loc_nu | local GR requires ordinary matter conservation or a bound below experiments | derive Q from Ward identity and show local suppression | missing | false |
| MIR789_2_torsion_spin | MTS spin/torsion source | Palatini connection equation must reduce to Levi-Civita locally | zero theorem or torsion bound | missing | false |
| MIR789_3_boundary_source | B_obs/source-measure | boundary terms can spoil local equations if hidden | explicit boundary variation and local silence theorem/bound | missing | false |
| MIR789_4_matter_universality | S_matter[e,omega,Psi] no direct Phi_MTS | equivalence principle and PPN safety | no-spurion/no-direct-coupling audit | missing | false |

## Branch Decision

| decision_id | decision | reason | result | next_target | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| D789_0_contract_written | keep Palatini/tetrad as the explicit local-GR reduction contract | it gives a clear route from action variation to GR and then Newton under named residual gates | contract_retained_nonclaim | 790-Y5-R10-MTS-exchange-stress-decomposition-and-local-suppression-gates.md | false |
| D789_1_no_local_GR_claim | do not claim MTS derives local GR yet | T_MTS, Q_nu/q_loc, torsion, boundary, and frame leakage are not decomposed or bounded | claim_blocked | 790-Y5-R10-MTS-exchange-stress-decomposition-and-local-suppression-gates.md | false |
| D789_2_next_target | decompose MTS exchange stress and local suppression gates next | this is now the smallest missing step for GR/Newton recovery | next_target_selected | 790-Y5-R10-MTS-exchange-stress-decomposition-and-local-suppression-gates.md | false |

## Source Register

| source_id | path | exists | needle_check | role | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| 788_doc | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\788-Y5-R10-nonholonomic-coframe-or-moment-closure-parent-action.md | true | true | immediate 789 handoff | false |
| 788_validation | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_BRR545_788_VALIDATION.csv | true | true | prior validation guard | false |
| 788_contracts | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_788_PARENT_ACTION_CONTRACT_CANDIDATES.csv | true | true | selected action contract input | false |
| 785_contract | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_785_PSI_METRIC_COFRAME_CONTRACT.csv | true | true | coframe/connection and GR/Newton requirement | false |
| postulates_18 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\18-sign-conventions-and-field-postulates.md | true | true | Einstein and exchange convention | false |
| spine_07 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\07-unification-spine.md | true | true | unification spine limit chain | false |
| testing_145 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\145-testing-readiness-and-gr-limit-map.md | true | true | local GR-limit demand | false |

## Validation

| check_id | result | detail |
| --- | --- | --- |
| V789_0_source_paths_exist | pass | source_rows=7 |
| V789_1_source_needles_present | pass | all source needles present |
| V789_2_prior_665_788_clean | pass | 665-788 validation rows have no failures |
| V789_3_contract_complete | pass | Palatini/tetrad contract rows complete |
| V789_4_connection_gate | pass | connection/torsion gate recorded |
| V789_5_coframe_gate | pass | coframe Einstein equation gate recorded |
| V789_6_GR_recovery_gate | pass | GR recovery residual gate recorded |
| V789_7_Newton_gate | pass | Newton weak-field gate recorded |
| V789_8_ward_complete | pass | variation/Ward identity rows complete |
| V789_9_exchange_current_recorded | pass | Q_nu exchange current gate recorded |
| V789_10_residuals_complete | pass | Newton/PPN residual vector rows complete |
| V789_11_residuals_missing_or_active | pass | residual rows remain missing/active nonclaim |
| V789_12_inputs_complete | pass | MTS exchange input requirement rows complete |
| V789_13_inputs_missing | pass | all MTS exchange inputs still missing |
| V789_14_no_local_GR_claim | pass | local GR claim remains blocked |
| V789_15_next_target_selected | pass | 790-Y5-R10-MTS-exchange-stress-decomposition-and-local-suppression-gates.md |
| V789_16_no_claim_rows_promoted | pass | all generated rows valid_for_claim=false |
| V789_17_claim_artifacts_absent | pass | no local-GR/Newton/adopted-action/PPN claim artifact fabricated |
| V789_18_outputs_scoped | pass | all outputs under post-checkpoint-work |
| V789_19_formalization_workbench_untouched | pass | formalization_changed_after_cutoff=0 |
| V789_20_validation_rows_ready | pass | validation table constructed |

## Verdict

This is the most useful local-GR checkpoint so far. It stops the work from drifting: MTS does not need to beat GR locally; it needs to become GR locally, then Newton in the weak-field limit, with every extra MTS term either silent or explicitly bounded. The next job is therefore not more philosophy about the metric. It is to decompose `T_MTS`, `Q_nu/q_loc`, torsion, boundary/source-measure, and frame leakage into concrete gates.

## Next Target

`790-Y5-R10-MTS-exchange-stress-decomposition-and-local-suppression-gates.md`
