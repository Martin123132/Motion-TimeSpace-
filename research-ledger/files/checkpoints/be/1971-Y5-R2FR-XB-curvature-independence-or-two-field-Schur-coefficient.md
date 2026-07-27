# 1971 Y5 R2FR: X_B Curvature-Independence Or Two-Field Schur Coefficient

Private checkpoint. This attempts the cleanest possible zero proof for the `X_B` curvature-response coefficient found in 1970.

Verdict: the exact condition is now derived: `C_XR=0` iff `D X_B[delta Phi_R]=0` for every allowed local curvature-changing parent variation. The current corpus does **not** prove this. In particular, `Dq[v_X]=0` is not enough because the old vertical hidden variation and the curvature-changing metric variation are different tangent directions.

So this is a real gain but not a closure: the next route is either a minimal parent ownership clause for `X_B`, or the honest two-field Schur coefficient pack.

## Source Register

| branch | row_id | valid_for_claim | public_claim | created_utc | source_path | purpose | required_needles | status | missing_needles |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | 1970_doc | False | False | 2026-06-20T01:09:27.436890+00:00 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1970-Y5-R2FR-XB-source-bath-boundary-curvature-mixing-audit.md | 1971 X_B curvature-independence proof attempt | SCHUR1970_3_coupling_location;NEXT1970_0_primary | EXISTS_NEEDLES_CONFIRMED |  |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | 1970_validation | False | False | 2026-06-20T01:09:27.437475+00:00 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_BRR545_1970_VALIDATION.csv | 1971 X_B curvature-independence proof attempt | VAL1970_OVERALL;PASS | EXISTS_NEEDLES_CONFIRMED |  |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | 827_XB_drift | False | False | 2026-06-20T01:09:27.438095+00:00 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\827-Y5-R10-XB-drift-and-Khat-bound-after-F1-zero.md | 1971 X_B curvature-independence proof attempt | DI827_2_moving_extremum_cancellation;KH827_2_XB_spurion_source | EXISTS_NEEDLES_CONFIRMED |  |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | 828_baseline_lock | False | False | 2026-06-20T01:09:27.438874+00:00 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\828-Y5-R10-XB-Lcg-local-constancy-or-Khat-owner-theorem.md | 1971 X_B curvature-independence proof attempt | BL828_2_local_baseline_lock;BL828_4_no_free_local_constant | EXISTS_NEEDLES_CONFIRMED |  |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | 1306_XB_domain | False | False | 2026-06-20T01:09:27.439612+00:00 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1306-Y5-R10-RAB-Zm-parent-function-or-XB-domain-range.md | 1971 X_B curvature-independence proof attempt | FRA1306_1_XB_dependent;XDG1306_0_argument_list;XDG1306_1_local_branch_map | EXISTS_NEEDLES_CONFIRMED |  |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | 1349_KMTS_owner | False | False | 2026-06-20T01:09:27.440467+00:00 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1349-Y5-R10-RAB-KMTS-trace-projection-owner-or-memory-closure-declaration.md | 1971 X_B curvature-independence proof attempt | KMTS1349_3_Ward_closure;RESP1349_2_external_profiles | EXISTS_NEEDLES_CONFIRMED |  |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | 826_Ward_audit | False | False | 2026-06-20T01:09:27.441152+00:00 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_826_WARD_BIANCHI_AUDIT.csv | 1971 X_B curvature-independence proof attempt | W826_1_external_XB_spurion;W826_3_Khat_required | EXISTS_NEEDLES_CONFIRMED |  |

## C_XR Curvature-Independence Proof

| branch | row_id | valid_for_claim | public_claim | created_utc | claim | derivation | status | implication |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | CXR1971_0_definition | False | False | 2026-06-20T01:09:27.441175+00:00 | C_XR := delta X_B/delta R_geom on the local weak-field branch | take a parent variation delta Phi_R that changes the observed Ricci scalar while preserving the local branch constraints | DEFINITION_INSTALLED | this is the coefficient needed by the R2/fR Schur gate |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | CXR1971_1_exact_zero_condition | False | False | 2026-06-20T01:09:27.441185+00:00 | C_XR=0 iff D X_B[delta Phi_R]=0 for every allowed local curvature-changing variation | this is a curvature-response annihilator condition, not merely an X-source or X-verticality condition | EXACT_CONDITION_DERIVED | the proof target is now sharply stated |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | CXR1971_2_verticality_not_enough | False | False | 2026-06-20T01:09:27.441192+00:00 | Dq[v_X]=0 does not imply C_XR=0 | v_X is a hidden/vertical variation; delta Phi_R is a metric/curvature variation. They are different tangent directions unless the parent proves they coincide or one annihilates X_B | NAIVE_QUOTIENT_PROOF_REJECTED | prevents us from accidentally reusing the old no-pole theorem for the wrong derivative |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | CXR1971_3_external_profile_fails | False | False | 2026-06-20T01:09:27.441197+00:00 | treating X_B as external does not prove C_XR=0 | external X_B may be held fixed in a calculation, but Ward/Bianchi rows call it a spurion source unless its parent owner is supplied | SPURION_ZERO_REJECTED | cannot win local GR by declaring the dangerous variable non-varied |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | CXR1971_4_baseline_lock_separate | False | False | 2026-06-20T01:09:27.441202+00:00 | Gamma_L(X_B)=constant does not imply C_XR=0 | baseline lock kills nabla Gamma_L in q_loc; R2/fR asks whether X_B changes under curvature variation inside the effective action | BASELINE_LOCK_NOT_R2FR_ZERO | useful for q_loc drift, insufficient for the EH left-hand gate |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | CXR1971_5_sufficient_parent_clause | False | False | 2026-06-20T01:09:27.441214+00:00 | A claim-grade zero theorem would require X_B to be a branch/topological label or quotient-owned environment variable annihilated by local curvature variations | parent clause: X_B=X_B[I_top,q_env] and D X_B[delta Phi_R]=0 on D_loc, with source/bath/boundary variables varied or silent | SUFFICIENT_THEOREM_FORMULATED_UNSIGNED | this is the least-scrutiny proof route if a future parent action can supply it |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | CXR1971_6_current_corpus_verdict | False | False | 2026-06-20T01:09:27.441219+00:00 | current inspected corpus does not prove C_XR=0 | X_B argument list, local branch map, metric response, and parent source/bath/boundary owner are all missing or marked nonclaim | CXR_ZERO_PROOF_FAILS_CURRENT_CORPUS | fall back to two-field Schur coefficient unless a new parent clause is adopted and audited |

## Proof Gate

| branch | row_id | valid_for_claim | public_claim | created_utc | gate | evidence | status | consequence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | GATE1971_0_argument_list | False | False | 2026-06-20T01:09:27.441225+00:00 | X_B components and parent definition | 1306 marks Arg[Z_m]=X_B components missing | FAIL_BLOCKED | cannot evaluate D X_B on curvature variations |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | GATE1971_1_local_branch_map | False | False | 2026-06-20T01:09:27.441231+00:00 | X_B local branch map over D_loc | 1306 marks X_B^{local}(x) missing | FAIL_BLOCKED | cannot tell whether local curvature perturbations move X_B |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | GATE1971_2_metric_response | False | False | 2026-06-20T01:09:27.441236+00:00 | metric/curvature response of X_B | 1302 and 1970 mark X_B metric response missing | FAIL_BLOCKED | C_XR is the exact missing object |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | GATE1971_3_external_spurion | False | False | 2026-06-20T01:09:27.441241+00:00 | holding X_B fixed externally | 826/827/1349 reject external X_B as a parent theorem | FAIL_REJECTED_AS_PROOF | spurion fixing is allowed only as private closure, not a GR derivation |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | GATE1971_4_baseline_lock | False | False | 2026-06-20T01:09:27.441246+00:00 | baseline lock relation | 828 supplies conditional q_loc drift cancellation | PASS_DIFFERENT_GATE_ONLY | helps q_loc but does not close R2/fR |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | GATE1971_5_result | False | False | 2026-06-20T01:09:27.441251+00:00 | C_XR=0 proof | one exact theorem condition is available, but no current source signs its premises | FAIL_CURRENT_CORPUS | proceed to Schur coefficient or new parent ownership clause |

## Two-Field Schur Inputs

| branch | row_id | valid_for_claim | public_claim | created_utc | needed_object | formula_or_definition | status | role |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | SCHIN1971_0_CXR | False | False | 2026-06-20T01:09:27.441257+00:00 | C_XR or B_XR | delta X_B/delta R_geom or curvature-linear vertex | MISSING_EXACT_OBJECT | first fallback coefficient |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | SCHIN1971_1_HX | False | False | 2026-06-20T01:09:27.441263+00:00 | H_X | X_B Hessian/operator, domain, sign, inverse | MISSING_OPERATOR | denominator for X_B response |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | SCHIN1971_2_Hm | False | False | 2026-06-20T01:09:27.441269+00:00 | H_m | memory Hessian including Z_m and V_mm | PARTIAL_TEMPLATE_ONLY | denominator for memory response |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | SCHIN1971_3_HmX | False | False | 2026-06-20T01:09:27.441274+00:00 | H_mX or V_mX | mixed memory/environment Hessian | MISSING_COUPLING | this is where the coupling lives if X_B is live |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | SCHIN1971_4_source_bath | False | False | 2026-06-20T01:09:27.441279+00:00 | source/bath vertices | curvature and memory couplings from source/bath variables | MISSING_ACTION | needed for Ward-safe Schur block |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | SCHIN1971_5_boundary | False | False | 2026-06-20T01:09:27.441284+00:00 | boundary/counterterm vertices | curvature-memory/environment response of boundary terms | MISSING_BOUNDARY_OWNER | needed for local exterior no-tower proof |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | SCHIN1971_6_units | False | False | 2026-06-20T01:09:27.441289+00:00 | normalization and units | parent sign convention, units of R, m, X_B, and c_R2 | MISSING_UNITS | needed before numeric R11 comparison |

## Runner Dryrun

| branch | row_id | valid_for_claim | public_claim | created_utc | input_row | runner_status | reason | accepted_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | RUN1971_0_exact_condition | False | False | 2026-06-20T01:09:27.441295+00:00 | CXR1971_1_exact_zero_condition | PASS_RELATIVE_THEOREM | zero condition is mathematically precise | False |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | RUN1971_1_verticality | False | False | 2026-06-20T01:09:27.441301+00:00 | CXR1971_2_verticality_not_enough | REJECTED_AS_INSUFFICIENT | old quotient verticality is the wrong derivative | False |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | RUN1971_2_spurion | False | False | 2026-06-20T01:09:27.441306+00:00 | CXR1971_3_external_profile_fails | REJECTED_AS_PARENT_PROOF | external fixing violates Ward/Bianchi discipline | False |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | RUN1971_3_current_zero | False | False | 2026-06-20T01:09:27.441311+00:00 | CXR1971_6_current_corpus_verdict | REJECTED_CXR_ZERO_UNSIGNED | no source signs curvature-independence | False |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | RUN1971_4_schur | False | False | 2026-06-20T01:09:27.441316+00:00 | SCHIN1971_0..6 | REJECTED_MISSING_SCHUR_INPUTS | fallback coefficient cannot yet be scored | False |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | RUN1971_VERDICT | False | False | 2026-06-20T01:09:27.441321+00:00 | all_rows | CXR_ZERO_FAILS_SCHUR_INPUTS_MISSING_NONCLAIM | local EH gate remains blocked but is now sharply localized | False |

## Claim Gate

| branch | row_id | valid_for_claim | public_claim | created_utc | claim | status | reason |
| --- | --- | --- | --- | --- | --- | --- | --- |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | CG1971_0_CXR_zero | False | False | 2026-06-20T01:09:27.441328+00:00 | C_XR=0 is derived | FAIL_BLOCKED | exact condition formulated but unsigned |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | CG1971_1_quotient_verticality | False | False | 2026-06-20T01:09:27.441333+00:00 | old vertical quotient proof clears R2/fR | FAIL_REJECTED | vertical hidden variation is not a curvature variation |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | CG1971_2_external_XB | False | False | 2026-06-20T01:09:27.441338+00:00 | external X_B fixed proves local GR | FAIL_REJECTED | spurion source, closure-only |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | CG1971_3_schur_coefficient | False | False | 2026-06-20T01:09:27.441343+00:00 | two-field Schur coefficient is scoreable | FAIL_BLOCKED | C_XR/H_X/H_mX/source/boundary missing |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | CG1971_4_EH_second_order | False | False | 2026-06-20T01:09:27.441348+00:00 | EH second-order local action is derived | FAIL_BLOCKED | R2/fR tower not eliminated |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | CG1971_5_local_GR_Newton | False | False | 2026-06-20T01:09:27.441352+00:00 | local GR/Newton theorem follows | FAIL_BLOCKED | EH plus PPN matter gates remain |

## Decision Ledger

| branch | row_id | valid_for_claim | public_claim | created_utc | decision | reason | next_action |
| --- | --- | --- | --- | --- | --- | --- | --- |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | DEC1971_0_real_gain | False | False | 2026-06-20T01:09:27.441358+00:00 | WRONG_ZERO_PROOF_REJECTED | We cannot reuse Dq[v_X]=0 to claim C_XR=0; that would be mixing two tangent directions. | do not spend more cycles on generic verticality for this gate |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | DEC1971_1_best_next | False | False | 2026-06-20T01:09:27.441364+00:00 | MINIMAL_XB_PARENT_OWNERSHIP_CLAUSE_OR_SCHUR_FILL | The clean route is still a parent clause proving D X_B[delta Phi_R]=0; if that cannot be supplied, the only honest route is the two-field Schur coefficient. | attempt a minimal X_B ownership/action clause, with explicit failover to coefficient rows |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | DEC1971_2_project_read | False | False | 2026-06-20T01:09:27.441369+00:00 | NOT_GRIM_BUT_NOT_CLOSED | This is not circular drift: the project found the exact place where local EH can be won or lost. | next work should either sign the X_B clause or start filling the coefficient matrix |

## Next Target

| branch | row_id | valid_for_claim | public_claim | created_utc | priority | target_doc | target_script | objective | acceptance_output | nonclaim_rule |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | NEXT1971_0_primary | False | False | 2026-06-20T01:09:27.441374+00:00 | selected | 1972-Y5-R2FR-minimal-XB-parent-ownership-clause-or-Schur-fill.md | scripts/Y5_R2FR_minimal_XB_parent_ownership_clause_or_Schur_fill_1972.py | try to write the minimal parent action/quotient clause that makes D X_B[delta Phi_R]=0; otherwise instantiate nonclaim Schur input rows | signed-style clause checklist or explicit C_XR/H_X/H_mX/B_source/B_boundary acquisition pack | no EH/local-GR claim while X_B curvature response is unsigned |

## Project Status Snapshot

| branch | row_id | valid_for_claim | public_claim | created_utc | strongest_result | what_improved | still_missing | claim_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | SNAP1971_0_project_position | False | False | 2026-06-20T01:09:27.441381+00:00 | The R2/fR local-GR gate is now reduced to an exact curvature-response condition: D X_B[delta Phi_R]=0. | We rejected the tempting but invalid shortcut from quotient verticality to curvature-independence, avoiding a false GR derivation. | parent X_B ownership clause, local curvature-variation tangent map, C_XR, H_X, H_mX, source/bath/boundary vertices, units | private nonclaim; theorem condition clear, current proof fails |

## Validation

| validation_id | status | detail | valid_for_claim | public_claim |
| --- | --- | --- | --- | --- |
| VAL1971_00_sources | PASS | all source paths exist and needles found | False | False |
| VAL1971_01_cxr_logic | PASS | C_XR condition derived and invalid shortcut rejected | False | False |
| VAL1971_02_proof_gate | PASS | proof gate distinguishes q_loc baseline lock from R2/fR zero | False | False |
| VAL1971_03_schur_inputs | PASS | Schur inputs remain explicit missing rows | False | False |
| VAL1971_04_runner | PASS | runner blocks EH/no-tower claim | False | False |
| VAL1971_05_claim_gates | PASS | all claim gates blocked or rejected | False | False |
| VAL1971_06_decision | PASS | decision ledger records rejected shortcut | False | False |
| VAL1971_07_next_target | PASS | 1972 target selected | False | False |
| VAL1971_08_claim_flags_safe | PASS | claim flags all false | False | False |
| VAL1971_09_csv_parse | PASS | all generated CSVs parse with rows | False | False |
| VAL1971_10_pycache_absent | PASS | scripts __pycache__ absent | False | False |
| VAL1971_11_formalization_untouched | PASS | formalization_1971_artifact_count=0 | False | False |
| VAL1971_OVERALL | PASS | 1971 X_B curvature-independence proof attempt | False | False |
