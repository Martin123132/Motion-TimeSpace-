# 2392 - vertical kernel presymplectic-null and matter-invisible or kernel-charge row

## Result

2392 tests whether the quotient kernel is a real gauge/null fibre or merely a renamed physical sector.

The required contract is:

1. `V=ker(Dq)` is a parent-defined vertical distribution with explicit basis vectors `v_i`.
2. `V` is regular and involutive, so the quotient is a stable local chart.
3. Each vertical vector is presymplectic-null:
   `i_v Theta_parent = dB_v + constraints`,
   and the compact local charge
   `integral_S(delta Q_v - i_v Theta_parent + boundary_improvements)` vanishes or is bounded.
4. Matter and readout are invisible along the kernel:
   `delta_v S_matter=0`,
   no direct `V_m[v,rho_A,W_source,C_top]` slot,
   no material marker/source prefactor,
   and no boundary/history/source-support tail.

This is the exact gate that stops `q/Obs_e` from becoming projection-by-declaration.

Current MTS does not yet sign the vertical basis, rank/bracket audit, parent `Theta_parent`, vertical charge `Q_v`,
zero compact flux, matter descent, no-direct-source-slot rule, boundary/history silence, or positive same-frame
`M_H_ref`.

So 2392 is not a kernel-nullness proof.  It is a sharpened theorem-or-bound contract.  No parent `q/Obs_e` pass,
same-frame pass, `J_H` pass, `W_source` pass, local-GR pass, Newton pass, PPN, clock, orbital, R10, or public/GitHub
claim is made.

## Source Register

| row_id | source_key | source_path | exists | needles_found | source_role | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| SRC2392_00_2391_doc | 2391_kernel_handoff | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\2391-Y5-R2FR-parent-q-Obs-e-functor-construction-or-frame-leak-source-pack.md | true | true | 2391 selects vertical kernel nullness as next gate | false |
| SRC2392_01_2391_certificates | 2391_qObs_certificates | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_2391_Q_OBS_E_CERTIFICATE.csv | true | true | null-kernel and matter/readout descent gaps | false |
| SRC2392_02_2391_leaks | 2391_qObs_leaks | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_2391_Q_OBS_E_LEAK_VALUES.csv | true | true | kernel charge/rank/tautology leak rows | false |
| SRC2392_03_1736_doc | 1736_Dq_tau_commutator | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1736-Y5-R2FR-Dq-tau-commutator-zero-or-first-finite-bound-row.md | true | true | tau/projectability and vertical-basis obstruction | false |
| SRC2392_04_1737_doc | 1737_q_Dq_basis | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1737-Y5-R2FR-q-map-Dq-vertical-basis-source-row-or-coframe-functor-zero.md | true | true | visible quotient and finite Dq rows | false |
| SRC2392_05_1756_doc | 1756_hidden_source | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1756-Y5-R2FR-two-slot-source-free-owner-or-hidden-source-counterexample-ledger.md | true | true | hidden source and boundary terms obstruct matter-invisible kernel | false |
| SRC2392_06_1760_doc | 1760_matter_descent | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1760-Y5-R2FR-matter-worldtube-quotient-descent-or-Amatter-bound.md | true | true | conditional matter/worldtube descent and live direct-slot obstruction | false |
| SRC2392_07_1008_doc | 1008_theta_Qtau | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1008-Y5-R10-parent-theta-Qtau-extraction-or-charge-decomposition-runner.md | true | true | parent symplectic potential/Noether charge extraction still missing | false |
| SRC2392_08_1009_doc | 1009_parent_action_contract | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1009-Y5-R10-parent-current-chain-action-contract-or-sector-variation-runner.md | true | true | parent action blocks organized but not promoted | false |
| SRC2392_09_1575_doc | 1575_vertical_generator | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1575-Y5-RAB-parent-RAB-vertical-generator-and-matter-descent-signature.md | true | true | example vertical-generator signature still not parent-signed | false |
| SRC2392_10_1736_commutator_csv | 1736_commutator_audit | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_1736_COMMUTATOR_PROOF_AUDIT.csv | true | true | machine audit for vertical basis and source/readout reopening guard | false |
| SRC2392_11_1756_owner_csv | 1756_two_slot_owner | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_1756_TWO_SLOT_SOURCE_FREE_OWNER_PROOF_ATTEMPT.csv | true | true | machine proof attempt for quotient matter and boundary/history silence | false |
| SRC2392_12_1008_variation_csv | 1008_parent_variation | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1008_PARENT_VARIATION_AUDIT.csv | true | true | parent action/theta extraction audit | false |

## Vertical Kernel Nullness Theorem

| row_id | step | statement | derivation_status | current_gain | remaining_gap | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| VKN2392_0_kernel_target | kernel target | For V=ker(Dq) to be a true quotient fibre, each vertical v must be a parent variation whose flow preserves q, e_obs, tau projection, source/readout maps, and boundary class before fitting. | CONDITIONAL_TARGET | turns verticality into a checkable parent signature rather than a label | V, Dq, tau pushforward, and readout guard are not jointly parent-signed | false |
| VKN2392_1_presymplectic_null | presymplectic-null charge test | The kernel is physically null only if i_v Theta_parent = dB_v plus constraints and the compact local flux integral_S(delta Q_v - i_v Theta_parent) vanishes or is bounded. | CONDITIONAL_COVARIANT_PHASE_SPACE_TEST | makes projection-by-declaration impossible unless the vertical direction carries no Hamiltonian charge | Theta_parent, Q_v, B_v, constraints, and zero compact flux are not extracted | false |
| VKN2392_2_matter_invisible | matter invisibility test | For ordinary matter, delta_v S_matter=0 follows if S_matter descends through q/e_obs, matter lifts are fixed over q, and no direct V_m[v,rho_A,W_source,C_top] or source-prefactor slot exists. | CONDITIONAL_CHAIN_RULE_TEST | separates quotient matter descent from hidden source couplings | direct-slot exclusion, matter lift, worldtube/support descent, and source-prefactor silence remain unsigned | false |
| VKN2392_3_boundary_history_silence | boundary/history silence | Even if bulk matter is invisible, the kernel is not null if boundary, history, reference, domain, or source-support tails have Pi_local dB_v or J_history[v] flux. | OBSTRUCTION_RETAINED | prevents boundary terms from being hidden under the word gauge | zero compact boundary flux and history-tail theorem are missing | false |
| VKN2392_4_rank_integrability | rank and involutivity test | V must be a regular involutive distribution: [v_i,v_j] must lie in V and rank(Dq) must be constant on the local branch, or q is not a stable quotient chart. | CONDITIONAL_GEOMETRY_TEST | adds the missing quotient-geometry gate before any q/Obs_e claim | vertical basis, bracket table, rank audit, and units/norms remain missing | false |
| VKN2392_5_verdict | current verdict | 2392 does not close the kernel. It proves the exact contract: V must be regular, parent-presymplectic-null, matter/readout-invisible, and boundary/history silent. Current MTS has not yet supplied the parent action objects needed to claim that. | ROUTE_EXACT_NOT_CLAIMED | the next bottleneck is parent Theta/Q_v extraction for vertical variations | kernel-charge rows remain nonclaim | false |

## Vertical Kernel Certificate

| row_id | certificate | required_test | status | residual_if_missing | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| VKC2392_0_vertical_basis | parent vertical basis | list v_i as parent variations and prove v_i in ker(Dq), not just gauge by analogy | MISSING_PARENT_VERTICAL_BASIS | epsilon_q_rank_or_integrability | false |
| VKC2392_1_rank_involutive | regular involutive quotient distribution | rank(Dq) constant and [v_i,v_j] in span(V) with sourced bracket table/norm | MISSING_RANK_AND_BRACKET_AUDIT | epsilon_q_rank_or_integrability | false |
| VKC2392_2_theta_Qv | parent Theta/Q_v extraction | derive delta L_parent = E delta Phi + dTheta_parent and J_v = Theta_parent(v)-i_v L = dQ_v + constraints | MISSING_THETA_PARENT_AND_QV | epsilon_kernel_charge | false |
| VKC2392_3_zero_compact_flux | zero compact local flux | integral_S(delta Q_v - i_v Theta_parent) plus boundary/reference improvements vanishes on linked local surfaces | MISSING_ZERO_COMPACT_FLUX_CERTIFICATE | epsilon_kernel_charge | false |
| VKC2392_4_matter_descent | matter-invisible kernel | S_matter descends through q/e_obs and matter lifts/constants are fixed over q for every v_i | MISSING_MATTER_DESCENT_SIGNATURE | epsilon_matter_kernel | false |
| VKC2392_5_no_direct_source_slot | no direct source/worldtube/material slots | exclude V_m[v,rho_A,W_source,C_top], source prefactors, material markers, and support terms outside q | MISSING_NO_DIRECT_SOURCE_SLOT_PROOF | epsilon_hidden_source_slot | false |
| VKC2392_6_boundary_history | boundary/history/reference silence | Pi_local dB_v=0 and J_history[v]=0 or bounded for compact local domains | MISSING_BOUNDARY_HISTORY_SILENCE | epsilon_boundary_history | false |
| VKC2392_7_MHref | positive same-frame M_H_ref | derive H_tau-H_ref in the same q/Obs_e/tau branch before normalizing kernel leakage | MISSING_POSITIVE_SAME_FRAME_MHREF | all normalized rows remain non-score-ready | false |

## Kernel Charge Leak Values

| row_id | quantity | formula | units | current_value | score_ready | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| VKL2392_0_rank_integrability | epsilon_q_rank_or_integrability | \|\|[v_i,v_j] mod V\|\| + \|\|rank(Dq)-rank_expected\|\| | field-space quotient defect | MISSING_VERTICAL_BASIS;MISSING_BRACKET_TABLE;MISSING_RANK_AUDIT | false | false |
| VKL2392_1_kernel_charge | epsilon_kernel_charge | abs(integral_S (delta Q_v - i_v Theta_parent + boundary_improvements))/M_H_ref | dimensionless Hamiltonian charge leakage | MISSING_THETA_PARENT;MISSING_Q_V;MISSING_BOUNDARY_IMPROVEMENTS;MISSING_ZERO_FLUX_CERTIFICATE;MISSING_M_H_REF | false | false |
| VKL2392_2_matter_kernel | epsilon_matter_kernel | abs(delta_v S_matter_on_shell)/M_H_ref | dimensionless matter-source leakage after normalization | MISSING_MATTER_DESCENT;MISSING_MATTER_LIFT;MISSING_M_H_REF | false | false |
| VKL2392_3_hidden_source_slot | epsilon_hidden_source_slot | abs(partial_v V_m[v,rho_A,W_source,C_top]) / M_H_ref | dimensionless hidden-source leakage | MISSING_NO_DIRECT_SLOT_PROOF;MISSING_VM_DENSITY;MISSING_M_H_REF | false | false |
| VKL2392_4_boundary_history | epsilon_boundary_history | abs(integral_S Pi_local dB_v + integral_history J_history[v]) / M_H_ref | dimensionless boundary/history leakage | MISSING_BOUNDARY_FLUX;MISSING_HISTORY_TAIL;MISSING_M_H_REF | false | false |
| VKL2392_5_projection_declaration | epsilon_projection_declaration | 1 if q/Obs_e relies on q_candidate containing e_obs before null-kernel proof else 0 | boolean guard | MISSING_NULL_KERNEL_PROOF | false | false |
| VKL2392_6_total | Delta_vertical_kernel_total_over_MH | epsilon_q_rank_or_integrability + epsilon_kernel_charge + epsilon_matter_kernel + epsilon_hidden_source_slot + epsilon_boundary_history + epsilon_projection_declaration | dimensionless | COMPONENTS_MISSING | false | false |

## Decision Ledger

| row_id | decision | reason | consequence | status | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| DEC2392_0_accept_kernel_contract | accept vertical kernel nullness as the required q/Obs_e promotion gate | q/Obs_e descent is only physical if the quotient kernel carries no charge and no matter/readout source | projection-by-declaration is blocked until nullness certificates exist | CONDITIONAL_KERNEL_CONTRACT_ACCEPTED | false |
| DEC2392_1_no_promotion | do not promote vertical kernel nullness for current MTS | parent Theta/Q_v, vertical basis, rank/bracket audit, matter descent, direct-slot exclusion, boundary/history silence, and M_H_ref remain missing | parent q/Obs_e, same-frame, J_H, W_source, local-GR and Newton claims remain blocked | VERTICAL_KERNEL_NULLNESS_NOT_PARENT_SIGNED | false |
| DEC2392_2_charge_first | attack parent Theta/Q_v extraction next | without the covariant phase-space charge test there is no way to tell gauge fibre from hidden physical charge | 2393 should derive vertical Noether charge Q_v or fill epsilon_kernel_charge with sourced finite rows | SELECT_2393_VERTICAL_NOETHER_CHARGE | false |

## Claim Gates

| row_id | gate | gate_status | claim_effect | valid_for_claim |
| --- | --- | --- | --- | --- |
| CG2392_0_contract_shape | vertical kernel nullness contract shape | PASS_CONDITIONAL_THEOREM_ONLY | use as gate; not evidence of current-MTS closure | false |
| CG2392_1_vertical_basis | parent vertical basis and rank/involutivity | FAIL | quotient geometry not promoted | false |
| CG2392_2_presymplectic_charge | Theta/Q_v compact-flux zero | FAIL | kernel may carry hidden Hamiltonian charge | false |
| CG2392_3_matter_invisible | matter/readout invisibility | FAIL | kernel may source matter/readout | false |
| CG2392_4_MHref | positive same-frame M_H_ref | FAIL | normalized kernel rows remain non-score-ready | false |
| CG2392_5_GR_Newton | local GR/Newton from null kernel | BLOCKED | no GR/Newton reduction claim from 2392 | false |

## Refusal Runner

| row_id | claim | allowed | reason | blocking_rows | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| REF2392_0_claim_null_kernel | V=ker(Dq) is parent-null and matter-invisible for current MTS | false | vertical basis, rank/involutivity, Theta/Q_v, zero flux, matter descent, direct-slot exclusion, boundary silence, and M_H_ref are unsigned | VKC2392_0_vertical_basis;VKC2392_2_theta_Qv;VKC2392_4_matter_descent;VKC2392_7_MHref | false |
| REF2392_1_call_kernel_gauge | vertical directions are harmless gauge by definition | false | gauge status requires presymplectic-null charge and matter/readout invisibility, not naming | VKC2392_2_theta_Qv;VKC2392_3_zero_compact_flux;VKC2392_4_matter_descent | false |
| REF2392_2_ignore_boundary | bulk matter invisibility is enough | false | boundary/history/source-support flux can reopen the kernel as a physical charge channel | VKC2392_6_boundary_history;VKL2392_4_boundary_history | false |
| REF2392_3_claim_GR_Newton | local GR/Newton follows from a conditional null-kernel contract | false | the kernel contract is necessary but not sufficient; q/Obs_e, EH exterior, source charge, M_H_ref, Poisson/Gauss, PPN, and boundary locks remain required | CG2392_5_GR_Newton;VKC2392_7_MHref | false |

## Next Target

| row_id | next_file | success_condition | fallback_condition | valid_for_claim |
| --- | --- | --- | --- | --- |
| NEXT2392_0_selected | 2393-Y5-R2FR-vertical-Noether-charge-Qv-extraction-or-kernel-charge-source-row.md | derive Theta_parent and Q_v for vertical variations and prove integral_S(delta Q_v - i_v Theta_parent)=0 on compact local surfaces | fill epsilon_kernel_charge with source paths, units, boundary-improvement terms, denominator status, and valid_for_claim=false | false |
| NEXT2392_1_parallel | 2393b-Y5-R2FR-vertical-basis-rank-bracket-audit-or-epsilon-q-integrability-row.md | list v_i, prove v_i in ker(Dq), constant rank, and [v_i,v_j] in V | fill epsilon_q_rank_or_integrability with bracket/rank source rows | false |
| NEXT2392_2_parallel | 2393c-Y5-R2FR-matter-boundary-invisibility-or-hidden-source-kernel-bound.md | prove delta_v S_matter=0 plus boundary/history/source-support silence for each v_i | fill epsilon_matter_kernel, epsilon_hidden_source_slot, and epsilon_boundary_history | false |

## Validation

| row_id | status | detail | valid_for_claim |
| --- | --- | --- | --- |
| VAL2392_00_sources_exist | PASS | all required source paths exist | false |
| VAL2392_01_needles_found | PASS | all source needles found | false |
| VAL2392_02_presymplectic_test_present | PASS | presymplectic-null charge test is present | false |
| VAL2392_03_matter_invisible_present | PASS | matter-invisibility chain-rule test is present | false |
| VAL2392_04_boundary_guard_present | PASS | boundary/history silence guard is present | false |
| VAL2392_05_required_gaps_explicit | PASS | vertical/theta/Qv/flux/matter/direct-slot/boundary/MHref gaps explicit | false |
| VAL2392_06_value_rows_nonready | PASS | kernel charge/source leak rows remain non-score-ready | false |
| VAL2392_07_global_claims_blocked | PASS | global/local gates remain blocked | false |
| VAL2392_08_csv_parse | PASS | generated CSVs parse and have rows | false |
| VAL2392_09_no_claim_flags | PASS | no generated row has valid_for_claim=true | false |
| VAL2392_10_formalization_untouched_by_script | PASS | script writes only post-checkpoint-work outputs | false |
| VAL2392_11_next_selected | PASS | vertical Noether charge extraction selected next | false |
| VAL2392_OVERALL | PASS | 2392 states the exact vertical-kernel nullness contract, refuses gauge-by-name without Theta/Qv/matter/boundary certificates, and selects vertical Noether charge extraction next | false |

## Practical Status

This is a hard but useful narrowing.  If the vertical charge test closes, the q/Obs_e route gets much more serious.
If it does not, we have found a real physical residual rather than a philosophical objection.  The next best target is
therefore `Q_v`: extract the vertical Noether charge or write the kernel-charge row honestly.
