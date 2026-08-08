# 1662 - q_loc Covariance And Apparatus Transfer Map

**Private status:** theorem-attempt checkpoint. No R10 pass, local-GR pass, Newton pass, PPN pass, WEP pass, or public claim is made.

## Verdict

`1662` gives the cleanest current statement of the problem:

```text
If Gamma_eff, K_hat, and P_loc descend as parent tensorial objects,
and if Earth-fixed lab observables are transferred into the same freefall Fermi residual,
then q_loc can be observer-frame covariant and inertial frame terms need not be physical sources.
```

But that is not parent-closed yet. The corpus already blocks the shortcut: Ward/Bianchi ownership is not absence, and a covariant vector can still be a real local preferred direction.

So the local branch is not dead, but it is now parent-action gated. Until that gate closes, the retained fallback is:

```text
epsilon_frame_leak = 2.43238775e-13 m^-1
ratio_to_curvature_bound = 1.96837071e+10
```

This is exactly why the next move must be parent-action structure, not another numerical patch.

## Source Register

| source_id | path | path_exists | needles_found | role |
| --- | --- | --- | --- | --- |
| 1661_doc | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1661-Y5-R2FR-Fermi-projector-constant-theorem-or-frame-silence.md | True | True | 1662 q_loc covariance and apparatus transfer map |
| 1661_validation | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_BRR545_1661_VALIDATION.csv | True | True | 1662 q_loc covariance and apparatus transfer map |
| 1661_projector_bound | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_1661_PROJECTOR_BOUND.csv | True | True | 1662 q_loc covariance and apparatus transfer map |
| 1661_frame_scales | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_1661_FRAME_SCALE_LEDGER.csv | True | True | 1662 q_loc covariance and apparatus transfer map |
| 1661_frame_silence | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_1661_FRAME_SILENCE_GATE.csv | True | True | 1662 q_loc covariance and apparatus transfer map |
| 469_q_source | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\469-fill-or-zero-highest-pressure-mu-extra-row.md | True | True | 1662 q_loc covariance and apparatus transfer map |
| 1003_frame_guard | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1003-Y5-R10-Bref-covariant-frame-theorem-or-Delta-ref-frame-profile-row.md | True | True | 1662 q_loc covariance and apparatus transfer map |
| 474_covariant_counterexample | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\474-domain-selector-no-vector-theorem-or-coefficient.md | True | True | 1662 q_loc covariance and apparatus transfer map |

## q_loc Covariance Contract

| clause_id | clause | status | why_needed | failure_mode | source_ref |
| --- | --- | --- | --- | --- | --- |
| QC1662_0_object_definition | q_loc^nu = P_loc^nu_rho (nabla^rho Gamma_eff - nabla_mu K_hat^{mu rho}) | DEFINITION_PRESENT | 469 supplies the working q_i^nu owner identity | definition only; not a covariance proof | 469_q_source |
| QC1662_1_scalar_descent | Gamma_eff is a scalar/quotient field on the parent configuration space | MISSING_PARENT_SIGNATURE | needed so nabla^rho Gamma_eff is a vector independent of coordinate frame | Gamma_eff can otherwise carry representative/frame convention | MISSING_PARENT_ACTION_CLAUSE |
| QC1662_2_current_descent | K_hat^{mu nu} is a genuine tensor current from a covariant parent variation | MISSING_PARENT_SIGNATURE | needed so nabla_mu K_hat^{mu nu} is a vector/tensorial divergence | Ward ownership alone does not prove the divergence is absent | 469_and_474 |
| QC1662_3_projector_descent | P_loc^nu_rho is built from a parent-owned observer/tetrad or quotient projector | MISSING_PROJECTOR_CERTIFICATE | needed to prevent P_loc from being an external Earth-frame filter | external projector can inject preferred-frame leakage | 1003_frame_guard |
| QC1662_4_vertical_invariance | Dq(v_frame)=0 implies Lie_v q_loc=0 for allowed frame/coframe changes | CONDITIONAL_ONLY | 1003 has quotient coframe descent only conditionally | zero switch is rejected without parent-signed covariant frame theorem | 1003_frame_guard |
| QC1662_5_covariant_counterexample_guard | covariance/Ward ownership alone proves q_loc has no local vector leakage | REJECTED_SHORTCUT | 474 explicitly allows covariant domain-vector counterexamples | a covariant vector can still be physical and locally preferred | 474_covariant_counterexample |

## Covariance Theorem Attempt

| attempt_id | proposition | status | value | blocker |
| --- | --- | --- | --- | --- |
| TH1662_0_conditional_success | If Gamma_eff descends as scalar, K_hat descends as tensor current, P_loc descends as parent tetrad/projector, and Dq(v_frame)=0, then q_loc is a vector/tetrad component and coordinate inertial connection terms are not independent physical sources. | CONDITIONAL_THEOREM | mathematically plausible but only conditional | missing parent signatures for Gamma_eff/K_hat/P_loc and vertical frame directions |
| TH1662_1_current_failure | Ward/Bianchi ownership of total exchange current implies local q_loc vector flux is absent. | FAILS_AS_SHORTCUT | ownership is necessary bookkeeping, not absence | 469 and 474 retain covariant vector/flux counterexamples |
| TH1662_2_frame_failure | Earth-fixed lab inertial terms can be dropped because a freefall Fermi frame exists. | FAILS_AS_SHORTCUT | freefall frame existence does not by itself transfer Earth-fixed observables | missing apparatus transfer map and parent covariance certificate |
| TH1662_3_verdict | q_loc observer-frame covariance is parent-derived for local observables. | NOT_CLOSED_FOR_CLAIM | the desired proof route is sharply specified | must supply parent action clauses or retain frame-leak fallback |

## Apparatus Transfer Map

| map_id | transfer_clause | status | reason |
| --- | --- | --- | --- |
| ATM1662_0_transfer_definition | A_lab_to_Fermi maps Earth-fixed apparatus observables into nonrotating geodesic Fermi tetrad components | MISSING_ARENA_PROJECTION | without this, the Fermi curvature bound is not the same quantity the R10 apparatus measures |
| ATM1662_1_acceleration_calibration | a_earth/c^2 term is universal coordinate/apparatus calibration and not q_loc source | MISSING_TRANSFER_CERTIFICATE | requires parent covariance plus explicit lab observable transfer |
| ATM1662_2_rotation_calibration | Omega_earth/c term is a tetrad rotation/Sagnac-style transfer term and not q_loc source | MISSING_TRANSFER_CERTIFICATE | rotation scale is the larger fallback if not removed |
| ATM1662_3_same_quantity_contract | the scalar/tetrad component bounded in the freefall frame equals the local source residual entering R10/PPN/WEP comparisons | MISSING_OBSERVABLE_EQUIVALENCE | otherwise a tiny curvature bound and a lab residual are being compared across different objects |
| ATM1662_4_no_cancellation_guard | frame terms are individually projected out or individually bounded; no tuned cancellation credit | POLICY_PASS | keeps the route falsifiable and prevents after-the-fact fitting |

## Frame Leak Fallback

| row_id | epsilon_frame_leak_m1 | source_component | conditional_curvature_bound_m1 | ratio_to_curvature_bound | fallback_status | runner_use |
| --- | --- | --- | --- | --- | --- | --- |
| FLF1662_0_retained_frame_leak_if_transfer_unsigned | 2.43238775e-13 | max(a_earth/c^2, Omega_earth/c) | 1.23573661e-23 | 1.96837071e+10 | RETAIN_IF_QLOC_COVARIANCE_OR_TRANSFER_UNSIGNED | blocks local scoring; can become numeric penalty row if parent proof fails |

## Claim Gates

| gate_id | claim | gate_pass | status | blocker |
| --- | --- | --- | --- | --- |
| CG1662_0_q_loc_covariance | q_loc is observer-frame covariant for local observables | False | BLOCKED | parent signatures for Gamma_eff/K_hat/P_loc and vertical frame directions missing |
| CG1662_1_apparatus_transfer | Earth-fixed apparatus terms are projected/transferred out | False | BLOCKED | A_lab_to_Fermi map and observable equivalence missing |
| CG1662_2_frame_leak | frame leak is zero for R10/PPN/WEP | False | NO_CLAIM | fallback epsilon_frame_leak retained if unsigned |
| CG1662_3_projector_bound | conditional Fermi projector bound is score-ready | False | NO_CLAIM | bound is conditional and not linked to apparatus observable |
| CG1662_4_local | local GR/Newton/PPN/R10/WEP follows | False | NO_CLAIM | no signed q_loc covariance, no transfer map, no M_H_ref denominator |

## Decisions

| decision_id | decision | reason | next_action |
| --- | --- | --- | --- |
| DEC1662_0_theorem_attempt | QLOC_COVARIANCE_NOT_PARENT_CLOSED | the desired covariance proof is now exact but lacks parent signatures | write parent action clauses for Gamma_eff, K_hat, and P_loc descent |
| DEC1662_1_transfer | APPARATUS_TRANSFER_MAP_MISSING | freefall Fermi bound and Earth-fixed R10 observable are not yet the same object | derive A_lab_to_Fermi or retain frame leak row |
| DEC1662_2_frame_fallback | RETAIN_EPSILON_FRAME_LEAK | Omega/c dominates if not projected out | keep nonclaim fallback row with absolute no-cancellation guard |
| DEC1662_3_next | NEXT_1663_PARENT_QLOC_TENSOR_ACTION_CLAUSE | least smuggly route is to make q_loc tensorial from the parent action | attempt parent action clause before more numerical testing |

## Next Target

| next_target | script | objective | success_condition |
| --- | --- | --- | --- |
| 1663-Y5-R2FR-parent-q_loc-tensor-action-clause-or-frame-leak-coefficient.md | scripts/Y5_R2FR_parent_q_loc_tensor_action_clause_or_frame_leak_coefficient.py | write the exact parent action clauses that make Gamma_eff, K_hat, and P_loc descend tensorially and define A_lab_to_Fermi, or retain epsilon_frame_leak as a nonclaim coefficient | q_loc covariance and apparatus transfer become parent-signed, or local GR/Newton branch is explicitly closure/coefficient-only |

## Validation

| check_id | result | detail |
| --- | --- | --- |
| VAL1662_0_sources_exist | PASS | all cited 1662 source paths exist and needles are present |
| VAL1662_1_1661_passed | PASS | 1661 validation is source-registered as PASS |
| VAL1662_2_covariance_clauses_present | PASS | q_loc covariance contract clauses are present |
| VAL1662_3_shortcuts_rejected | PASS | Ward/covariance/frame-choice shortcuts are rejected |
| VAL1662_4_theorem_not_promoted | PASS | q_loc covariance theorem remains not closed for claim |
| VAL1662_5_transfer_blocked | PASS | apparatus transfer map remains explicitly blocked |
| VAL1662_6_frame_leak_retained | PASS | frame leak fallback is retained and exceeds curvature bound |
| VAL1662_7_claim_gates_safe | PASS | all claim gates keep MTS claims false |
| VAL1662_8_next_target_selected | PASS | next target selects parent q_loc tensor action clause |
| VAL1662_9_csv_parse | PASS | all generated 1662 CSVs parse |
| VAL1662_10_no_mts_claim_flags | PASS | all 1662 generated rows keep MTS claim/no-score flags false |
| VAL1662_11_branch_copies | PASS | branch/quarantine copies exist |
| VAL1662_12_queue_copies | PASS | acquisition queue nonclaim copies exist |
| VAL1662_13_pycache_absent | PASS | scripts __pycache__ absent |
| VAL1662_14_formalization_untouched | PASS | no 1662 outputs found under formalization-workbench |
| VAL1662_OVERALL | PASS | 1662 q_loc covariance and apparatus transfer validation |

## Working Interpretation

This is a useful narrowing. We are no longer asking vaguely whether the local branch can look like GR. We are asking whether the parent action can make `q_loc` a genuine quotient-tensor residual and define the apparatus transfer map. If yes, the large Earth-frame inertial terms become calibration/coordinate transfer terms. If no, the local branch remains closure/coefficient-only and cannot claim derived GR/Newton recovery.
