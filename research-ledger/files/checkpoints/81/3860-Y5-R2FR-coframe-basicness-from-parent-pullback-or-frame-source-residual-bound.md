# 3860 - Coframe Basicness From Parent Pullback Or Frame Source Residual Bound

Private checkpoint. This attacks the public coframe throat below 3859: when is `e_obs` genuinely q_obs-basic, and when is it just an inserted observed-frame label?

Generated: `2026-07-01T05:01:38+00:00`

## Result

The exact q-basic coframe theorem is:

`e_obs=e_bar(q_obs) and v in ker(Dq_obs) imply D_v e_obs=D e_bar[Dq_obs(v)]=0`.

The parent certificate needed to use it without smuggling is:

`L_parent=q_obs^*L_red+dB, int_boundary B_EA=0, S_src=Sbar_src(q_obs,psi,A,theta), Lie_EA theta=0, and r_s=F_s o q_obs`.

The anti-tautology guard is:

`including e_obs inside the q_obs tuple is not a proof unless the parent action makes ker(Dq_obs) presymplectic-null, matter-invisible, boundary-silent, and readout-silent`.

The strict current result is still blocked:

`current corpus has q_obs and public-geometry candidates, but parent pullback, L_leak=0, boundary silence, source descent, constants, and sector readout descent are not all signed`.

The finite coframe-basicness residual is:

`B_eobs_basic_3860 <= B_qobs_signature+B_pullback_Lleak+B_kernel_null+B_boundary_silence+B_source_descent+B_theta_constants+B_sector_readout+B_shadow_frame+B_coframe_spin+B_readout_order`.

And its frame/source fallback is:

`delta_frame_source <= C_L epsilon_L+C_Omega epsilon_Omega+C_src epsilon_src+C_theta epsilon_theta+C_boundary epsilon_boundary+C_readout max_s epsilon_readout_s+C_shadow epsilon_shadow_g`.

So 3860 does not claim local GR. It says exactly what would make `e_obs` owned, and exactly where the failure goes if it is not owned.

## Source Register

| source_id | path | exists | needle_found | role |
| --- | --- | --- | --- | --- |
| SRC3860_00_3859_theorem | source-intake\mts_residuals\P8_Y5_R2FR_3859_QBASIC_TAU_H_CSTAR_THEOREM.csv | True | True | 3859 tau/h/c owner theorem |
| SRC3860_01_3859_audit | source-intake\mts_residuals\P8_Y5_R2FR_3859_TAU_H_CSTAR_OWNERSHIP_AUDIT.csv | True | True | 3859 e_obs owner audit |
| SRC3860_02_3859_bound | source-intake\mts_residuals\P8_Y5_R2FR_3859_FRAME_CLOCK_PREFERRED_RESIDUAL_BOUND.csv | True | True | 3859 residual bound |
| SRC3860_03_3859_gates | source-intake\mts_residuals\P8_Y5_R2FR_3859_CLAIM_GATES.csv | True | True | 3860 target selection |
| SRC3860_04_3859_validation | source-intake\mts_residuals\P8_Y5_BRR545_3859_VALIDATION.csv | True | True | previous validation |
| SRC3860_05_3766_kernel | source-intake\mts_residuals\P8_Y5_R2FR_3766_KERNEL_NULL_THEOREM.csv | True | True | kernel-null theorem |
| SRC3860_06_3766_attempt | source-intake\mts_residuals\P8_Y5_R2FR_3766_QOBS_KERNEL_PROOF_ATTEMPT.csv | True | True | current kernel proof attempt |
| SRC3860_07_3766_bound | source-intake\mts_residuals\P8_Y5_R2FR_3766_FIRST_FRAME_RESIDUAL_BOUND.csv | True | True | frame residual bound |
| SRC3860_08_3766_norms | source-intake\mts_residuals\P8_Y5_R2FR_3766_VERTICAL_LEAKAGE_NORMS.csv | True | True | vertical leakage norms |
| SRC3860_09_3767_pullback | source-intake\mts_residuals\P8_Y5_R2FR_3767_PARENT_ACTION_PULLBACK_DECOMPOSITION.csv | True | True | parent action pullback identity |
| SRC3860_10_3767_lleak | source-intake\mts_residuals\P8_Y5_R2FR_3767_LLEAK_BOUND_INTERFACE.csv | True | True | L_leak bound interface |
| SRC3860_11_3765_qobs | source-intake\mts_residuals\P8_Y5_R2FR_3765_QOBS_CANDIDATE_MAP.csv | True | True | q_obs candidate map |
| SRC3860_12_3765_verdict | source-intake\mts_residuals\P8_Y5_R2FR_3765_PARENT_QOBS_VERDICT.csv | True | True | q_obs verdict |
| SRC3860_13_3517_qmap | source-intake\mts_residuals\P8_EM_actual_q_map_vertical_basis_candidate.csv | True | True | public geometry slot |
| SRC3860_14_3504_gate | source-intake\mts_residuals\P8_Y5_R2FR_3504_PARENT_SIGNATURE_GATE.csv | True | True | e_obs q-basic gate |
| SRC3860_15_3504_hodge | source-intake\mts_residuals\P8_Y5_R2FR_3504_HODGE_UNIQUENESS_THEOREM.csv | True | True | Hodge/coframe vertical silence |
| SRC3860_16_3498_naturality | source-intake\mts_residuals\P8_Y5_R2FR_3498_PROJECTOR_NATURALITY_THEOREM.csv | True | True | projector naturality chain rule |
| SRC3860_17_3494_spin | source-intake\mts_residuals\P8_Y5_R2FR_3494_COFRAME_SPIN_THEOREM_ATTEMPT.csv | True | True | owned coframe spin branch |
| SRC3860_18_frame_split | source-intake\mts_residuals\P8_frame_source_split_residual_or_zero.csv | True | True | frame/source residual fallback |

## Coframe Basicness Theorem

| theorem_id | step | status | current_result |
| --- | --- | --- | --- |
| CBT3860_0_qbasic_coframe | coframe basicness chain rule | EXACT_CONDITIONAL_COFRAME_BASICNESS | EXACT_CHAIN_RULE_THEOREM |
| CBT3860_1_parent_certificate | parent pullback/kernel certificate | EXACT_CONDITIONAL_KERNEL_TO_COFRAME_ROUTE | EXACT_CONDITIONAL_PARENT_CERTIFICATE |
| CBT3860_2_anti_tautology | anti-tautology guard | GUARD_ACTIVE | NO_QOBS_BY_DECLARATION |
| CBT3860_3_current_verdict | strict-current coframe basicness test | CURRENT_NONCLAIM_RESIDUAL_BOUND_REQUIRED | EOBS_BASICNESS_NOT_CLAIMED_CURRENT_CORPUS |
| CBT3860_4_if_closed | metric bridge consequence | EXACT_CONDITIONAL_WIN_PATH | EXACT_CONDITIONAL_METRIC_BRIDGE_HANDOFF |

## Parent Signature Audit

| audit_id | clause | passes_current_branch | residual_owner | next_action |
| --- | --- | --- | --- | --- |
| CPA3860_0_qobs_signature | q_obs parent signature | False | B_qobs_signature | prove q_obs from parent equivalence/kernel-null or retain quotient residuals |
| CPA3860_1_pullback_Lleak | parent action pullback | False | B_pullback_Lleak | prove or bound L_leak_shadow_g/source/boundary/readout terms |
| CPA3860_2_kernel_null | presymplectic kernel nullness | False | B_kernel_null | extract parent symplectic form or retain epsilon_Omega |
| CPA3860_3_boundary | boundary/support silence | False | B_boundary_silence | prove compact support/boundary ownership or retain epsilon_boundary |
| CPA3860_4_source_theta | source and constants descent | False | B_source_descent+B_theta_constants | prove same-source action and constant superselection or retain epsilon_src/epsilon_theta |
| CPA3860_5_readout_shadow | sector readout and no shadow coframe | False | B_sector_readout+B_shadow_frame+B_readout_order | prove no-shadow coframe or bound epsilon_shadow_g and epsilon_readout_s |
| CPA3860_6_coframe_spin | owned coframe ordinary/spin branch | False | B_coframe_spin | promote owned-coframe matter action or retain torsion/spin residuals |

## Frame Source Residual Update

| row_id | observable | status | formula |
| --- | --- | --- | --- |
| FSU3860_0_eobs_basic_bound | B_eobs_basic_3860 | NONCLAIM_BOUND_EXPLICIT | B_eobs_basic_3860 <= B_qobs_signature+B_pullback_Lleak+B_kernel_null+B_boundary_silence+B_source_descent+B_theta_constants+B_sector_readout+B_shadow_frame+B_coframe_spin+B_readout_order |
| FSU3860_1_frame_source_bound | delta_frame_source | FRAME_SOURCE_BOUND_REFINED | delta_frame_source <= C_L epsilon_L+C_Omega epsilon_Omega+C_src epsilon_src+C_theta epsilon_theta+C_boundary epsilon_boundary+C_readout max_s epsilon_readout_s+C_shadow epsilon_shadow_g |
| FSU3860_2_tau_h_c_update | B_tau_h_cstar_owner_3859 | TAU_H_CSTAR_BOUND_REFINED | B_tau_h_cstar_owner_3859 <= B_eobs_basic_3860+B_cstar_superselection+B_clock_scale+B_sector_factorization+B_preferred_frame_motion+B_EM_conformal_scale |
| FSU3860_3_if_closed | coframe-to-local-GR route | EXACT_CONDITIONAL_HANDOFF | if B_eobs_basic_3860=0 and B_cstar_superselection=0 then tau/h/c are q-basic; if nonLC/action/source/readout gates also close, visible EH/local-GR route opens conditionally |

## Claim Gates

| gate_id | status | claim_allowed | reason |
| --- | --- | --- | --- |
| GATE3860_0_sources | PASS_SOURCE_REGISTERED | False | all coframe-basicness inputs are local source rows from 3494/3498/3504/3517/3765/3766/3767/3859 |
| GATE3860_1_theorem | PASS_EXACT_CONDITIONAL_COFRAME_BASICNESS_THEOREM | False | e_obs descends by chain rule once q_obs is parent-signed |
| GATE3860_2_antitautology | PASS_NO_QOBS_BY_DECLARATION | False | including e_obs in q_obs is not enough without action pullback/kernel/source/readout certificates |
| GATE3860_3_current_claim | BLOCKED_EOBS_BASICNESS_NOT_PARENT_SIGNED | False | current corpus has q_obs and public-geometry candidates, but parent pullback, L_leak=0, boundary silence, source descent, constants, and sector readout descent are not all signed |
| GATE3860_4_local_GR | BLOCKED_LOCAL_GR_CLAIM | False | coframe basicness, cstar, nonLC connection, action adoption, source, and readout gates remain active |
| GATE3860_5_next | PASS_3861_NO_SHADOW_COFRAME_TARGET | False | the most concrete e_obs-specific leak is the possible hidden/shadow coframe epsilon_shadow_g |

## Decisions

| decision_id | decision | consequence |
| --- | --- | --- |
| DEC3860_0 | e_obs basicness has an exact chain-rule theorem | the proof now depends on parent-signing q_obs, not on rewriting the metric bridge |
| DEC3860_1 | q_obs-by-declaration is forbidden | the candidate quotient must be backed by pullback/kernel/source/readout certificates |
| DEC3860_2 | attack hidden/shadow coframe next | 3861 should prove no second coframe participates or retain epsilon_shadow_g as a bounded frame residual |

## Bottom Line

3860 proves the clean theorem: `e_obs` is q-basic if it is genuinely a parent-signed quotient object. But it blocks the cheap route: merely putting `e_obs` inside the q_obs tuple is not enough. The next concrete target is the shadow-frame leak: prove there is no second coframe participating in matter, EM, clock, light, source, or orbital readout, or bound `epsilon_shadow_g`.

Next target: `3861-Y5-R2FR-no-shadow-coframe-basicness-or-epsilon-shadow-frame-bound.md`.
