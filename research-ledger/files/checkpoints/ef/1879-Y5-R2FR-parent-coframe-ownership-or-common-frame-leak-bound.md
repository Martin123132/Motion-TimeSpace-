# 1879 - Parent Coframe Ownership Or Common-Frame Leak Bound

**Private status:** nonclaim derivation checkpoint. No local-GR, PPN, WEP, clock, orbital, R10, or public claim is made.

## Result

The exact clean theorem is still alive:

```text
e_obs = E(Q_vis)
C_R excluded from Q_vis or killed before readout
=> D_C_R e_obs = 0
=> b_R = 0
```

But the current corpus does not parent-sign the ownership stack. The old shortcut routes also fail: covariance, WEP and Ward identities do not forbid a hidden universal Weyl/disformal/source-prefactor slot.

So the live local interface is now explicit:

```text
b_R, d_R, w_R, epsilon_endpoint_R, epsilon_common_frame_abs
```

These are not claims. They are the finite residual rows that future local PPN/WEP/clock/orbital/R10 guards must either theorem-zero or source-bound.

## Parent Coframe Ownership Stack

| branch_id | stack_id | clause | mathematical_test | current_status | effect_if_closed | proof_closed | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | PCO1879_0_parent_q | parent observed quotient Q_vis is constructed before local readout | q: Phi_parent -> Q_vis and Dq are parent-owned, not postselected for local tests | MISSING_PARENT_Q_CONSTRUCTION | lets chain-rule kernel tests become meaningful | False | False | False |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | PCO1879_1_coframe_owner | observed coframe has no C_R/J_q argument | e_obs=E(Q_vis) with C_R/R_AB/J_q excluded or already constrained before readout | MISSING_PARENT_COFRAME_OWNERSHIP | kills epsilon_R_cell by ownership rather than fitting | False | False | False |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | PCO1879_2_no_weyl_shadow | no common Weyl shadow frame | A_R'(0)=0 or no independent A_R(C_R) slot exists in S_matter/readout | MISSING_NO_SHADOW_FRAME_THEOREM | sets b_R=0 | False | False | False |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | PCO1879_3_no_disformal_shadow | no common disformal or preferred-frame shadow | B_R'(0)=0 or no U_mu U_nu disformal/current slot exists | MISSING_DISFORMAL_ZERO_THEOREM | sets d_R=0 and protects preferred-frame PPN | False | False | False |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | PCO1879_4_source_prefactor | no source-only matter prefactor hidden inside one public frame | delta w_A(C_R)=0 or source-weight current has zero local projection | MISSING_SOURCE_PREFACTOR_ZERO_THEOREM | prevents WEP-clean but Hilbert-source-active coupling | False | False | False |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | PCO1879_5_connection_boundary_tau | connection, boundary endpoints, source normals, and tau descend through Q_vis | Domega, P_loc endpoint derivative, source support, and tau pushforward have no C_R leak | MISSING_CONNECTION_BOUNDARY_TAU_DESCENT | prevents coframe zero from being reopened by readout/endpoints | False | False | False |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | PCO1879_6_verdict | parent coframe ownership closes common-frame leak | PCO1879_0 through PCO1879_5 all parent-signed | PARENT_COFRAME_OWNERSHIP_NOT_DERIVED_CURRENT_CORPUS | returns to local-GR derivation path with DObs_e branch silenced | False | False | False |

## No-Shadow-Frame Tests

| branch_id | test_id | test | calculation | result | blocker | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | NSF1879_0_chain_rule | chain-rule no-shadow theorem | if e_obs=E(Q_vis) and C_R is excluded from Q_vis or in ker(Dq), then D_C_R e_obs=0 and b_R=0 | EXACT_CONDITIONAL | parent Q_vis and coframe ownership not signed | False | False |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | NSF1879_1_covariance | diffeomorphism covariance forbids shadow frame | S_m[Psi,A_R(C_R)^2 g_obs] is covariant | FAILS_UNCONDITIONAL_DERIVATION | covariance does not forbid common conformal/disformal factors | False | False |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | NSF1879_2_WEP | WEP universality forbids common-frame leak | universal A_R(C_R) can preserve composition universality while shifting clocks/PPN/source normalization | FAILS_UNCONDITIONAL_DERIVATION | WEP alone can miss common-mode metric/source shifts | False | False |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | NSF1879_3_Ward | Ward conservation forbids shadow frame | nabla_mu T^{mu nu}=0 holds in the chosen matter geometry even with A_R(C_R) | FAILS_UNCONDITIONAL_DERIVATION | Ward identities are homogeneous under hidden common-frame/source-weight choices | False | False |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | NSF1879_4_terminal_public_metric | terminal public coframe object excludes extra frame slots | Allowed[S_matter] excludes A_R(C_R), B_R(C_R), source weights, and endpoint coframe arguments | BEST_CONDITIONAL_ROUTE_NOT_PARENT_DERIVED | terminal/quotient naturality clause remains a closure contract, not a derived parent theorem | False | False |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | NSF1879_5_verdict | current corpus proves no-shadow-frame and b_R=d_R=0 | NSF1879_0 through NSF1879_4 close with parent signatures | NO_SHADOW_FRAME_NOT_DERIVED_CURRENT_CORPUS | finite common-frame leak rows remain mandatory | False | False |

## Common-Frame Leak Bound Rows

| branch_id | row_id | symbol | meaning | formula | status | numeric_value | units | source_path | arena_links | score_ready | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | CFL1879_0_bR | b_R | common Weyl/log-coframe derivative with respect to C_R/R_AB | b_R := d ln A_R(C_R)/dC_R | local background, or ||e_obs^-1 D_C_R e_obs|| | MISSING_ZERO_THEOREM_OR_NUMERIC_BOUND | MISSING_NUMERIC_VALUE | dimensionless | MISSING_SOURCE_PATH | PPN;clock;WEP;orbital;local_GR | False | False | False |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | CFL1879_1_dR | d_R | common disformal/preferred-frame derivative | d_R := dD_R(C_R)/dC_R or declared norm of U_mu U_nu shadow-frame response | MISSING_ZERO_THEOREM_OR_NUMERIC_BOUND | MISSING_NUMERIC_VALUE | dimensionless_or_declared_disformal_scale | MISSING_SOURCE_PATH | PPN_preferred_frame;clock;orbital;local_GR | False | False | False |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | CFL1879_2_wR | w_R | source-only matter prefactor derivative | w_R := d ln w_A(C_R)/dC_R or absolute source-weight envelope across ordinary matter sectors | MISSING_ZERO_THEOREM_OR_NUMERIC_BOUND | MISSING_NUMERIC_VALUE | dimensionless | MISSING_SOURCE_PATH | WEP;R10_source_leg;PPN_source_normalization;clock | False | False | False |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | CFL1879_3_endpoint | epsilon_endpoint_R | boundary/endpoint local coframe projection | epsilon_endpoint_R := ||P_loc partial_{Q_endpoint}E(Q_vis,Q_endpoint)|| | MISSING_ZERO_THEOREM_OR_NUMERIC_BOUND | MISSING_NUMERIC_VALUE | dimensionless_projection_norm | MISSING_SOURCE_PATH | PPN;clock;orbital;local_GR | False | False | False |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | CFL1879_4_total_abs | epsilon_common_frame_abs | absolute no-cancellation common-frame leak envelope | |b_R|+|d_R|+|w_R|+|epsilon_endpoint_R| plus any sourced coframe/tau/readout leaks | MISSING_ABSOLUTE_ENVELOPE | MISSING_NUMERIC_VALUE | dimensionless | MISSING_SOURCE_PATH | all_local_arenas | False | False | False |

## Arena Bound Interface

| branch_id | arena_id | arena | required_inputs | current_status | blocking_rows | route_note | score_ready | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | ABI1879_0_local_GR | local_GR/Newton | epsilon_common_frame_abs=0 or source-backed bound; plus source normalization, beta, conservation | BLOCKED_NONCLAIM | CFL1879_0_bR;CFL1879_1_dR;CFL1879_4_total_abs | common-frame leak must be zero/bounded before local metric inheritance is credible | False | False | False |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | ABI1879_1_PPN | PPN_gamma_beta_preferred_frame | b_R,d_R,q_R_hat,boundary tails and PPN projection matrix in same source frame | BLOCKED_NONCLAIM | CFL1879_0_bR;CFL1879_1_dR;RV1875_5_massless_tail;RV1875_8_projection_kernels | common Weyl/disformal terms can affect gamma/beta/preferred-frame observables | False | False | False |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | ABI1879_2_clock_WEP | clock/WEP/material | b_R,w_R,material sensitivities, constants superselection and tau_clock/tau_WEP | BLOCKED_NONCLAIM | CFL1879_0_bR;CFL1879_2_wR;RV1875_7_constants_markers;RV1875_8_projection_kernels | WEP-clean common-mode shifts can still show up in clocks/source normalization | False | False | False |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | ABI1879_3_orbital | orbital/light-time | b_R,d_R,endpoint leak, orbital projection and no-cancellation envelope | BLOCKED_NONCLAIM | CFL1879_0_bR;CFL1879_1_dR;CFL1879_3_endpoint;RV1875_8_projection_kernels | finite common-frame terms must be projected into acceleration/light-time residuals | False | False | False |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | ABI1879_4_R10 | R10 finite range | finite Z_R/M_R^2/lambda_R plus source/test charges; common-frame source leg cannot replace range | BLOCKED_NONCLAIM_WRONG_ROUTE_GUARD | RV1875_2_operator_ZR;RV1875_3_operator_MR2_lambda;RV1875_4_bulk_source_charges;CFL1879_2_wR | b_R/w_R may be a coupling leg only after the finite range/operator branch is sourced | False | False | False |

## Source Register

| branch_id | checkpoint_id | source_id | source_path | required_needles | source_exists | needle_check | usable_for_1879 | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | 1879 | 1878_doc | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1878-Y5-R2FR-qshape-readout-functor-kernel-or-parent-category-principle.md | physics cannot forget what clocks and rulers actually read ; PARENT_COFRAME_OWNERSHIP_OR_BG_BOUND_SELECTED_NEXT | True | OK | True | False | False |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | 1879 | 1878_validation | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_BRR545_1878_VALIDATION.csv | VAL1878_OVERALL,PASS | True | OK | True | False | False |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | 1879 | 1878_finite_dobs | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_1878_FINITE_DOBS_E_LEAK_ROWS.csv | FDOBS1878_1_common_weyl ; MISSING_B_R_ZERO_THEOREM_OR_BOUND | True | OK | True | False | False |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | 1879 | 1878_next | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_1878_NEXT_TARGET.csv | 1879-Y5-R2FR-parent-coframe-ownership-or-common-frame-leak-bound.md ; selected | True | OK | True | False | False |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | 1879 | 1739_doc | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1739-Y5-R2FR-parent-coframe-ownership-or-common-frame-log-derivative-row.md | PARENT_COFRAME_OWNERSHIP_NOT_SIGNED ; BG_ROW_IS_THE_TESTABLE_INTERFACE | True | OK | True | False | False |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | 1879 | 1739_bg_rows | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_1739_COMMON_FRAME_LOG_DERIVATIVE_ROWS.csv | BG1739_3_RAB_Jq ; RETAINED_NONCLAIM_BG_ROW | True | OK | True | False | False |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | 1879 | 1029_no_shadow | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1029-Y5-R10-cg-no-shadow-frame-theorem-or-first-numeric-coupling-row.md | Current MTS does not yet prove c_g=0. ; common-frame counterexample blocks WEP-only c_g zero | True | OK | True | False | False |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | 1879 | 1030_spm_gate | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1030-Y5-R10-single-public-metric-parent-action-derivation-or-cg-provenance-gate.md | Ward identities do not derive the single public metric ; EXACT_CLOSURE_CLAUSE_NOT_DERIVED | True | OK | True | False | False |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | 1879 | 1088_matter_signature | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1088-Y5-R10-minimal-parent-ordinary-matter-signature-clause-or-finite-coefficient-intake.md | e_obs=E(q(Phi)) ; CONDITIONAL_GEOMETRY_SUBLEMMA | True | OK | True | False | False |

## Claim Gate

| branch_id | claim_id | claim | status | reason | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | CG1879_0_internal | 1879 ownership/leak audit may guide next derivation | ALLOW_INTERNAL_NONCLAIM_AUDIT | it imports prior no-shadow tests and keeps all local claims blocked | False | False |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | CG1879_1_parent_coframe | parent action owns e_obs=E(Q_vis) | BLOCKED | parent q/coframe ownership and no C_R/J_q argument are unsigned | False | False |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | CG1879_2_no_shadow | b_R=d_R=w_R=0 by no-shadow-frame theorem | BLOCKED | covariance, WEP and Ward identities fail as unconditional derivations; terminal public metric is conditional | False | False |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | CG1879_3_bound_score | finite common-frame leak is below local bounds | BLOCKED | numeric leak values, units, source paths and arena projections are missing | False | False |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | CG1879_4_local_GR | local GR/Newton follows from coframe ownership | BLOCKED | coframe/no-shadow is necessary but still not sufficient without beta, conservation and source gates | False | False |

## Decision Ledger

| branch_id | decision_id | decision | basis | consequence | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | DEC1879_0_result | PARENT_COFRAME_OWNERSHIP_NOT_DERIVED_CURRENT_CORPUS | the exact chain-rule b_R=0 theorem exists, but parent Q_vis/e_obs ownership and no C_R/J_q readout argument remain unsigned | common-frame leak rows stay live | False | False |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | DEC1879_1_shortcuts | COVARIANCE_WEP_WARD_SHORTCUTS_REJECTED | common Weyl/disformal/source-prefactor countermodels remain covariant, can be WEP-clean, and obey Ward identities in their own matter geometry | do not use these slogans to claim no-shadow-frame | False | False |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | DEC1879_2_testing_interface | COMMON_FRAME_LEAK_ROWS_ARE_NOW_THE_LOCAL_TEST_INTERFACE | b_R,d_R,w_R,endpoint and total envelope are the finite residuals if parent ownership fails | future runners must source or theorem-zero these rows before local claims | False | False |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | DEC1879_3_next | NO_SHADOW_TERMINAL_PUBLIC_METRIC_OR_BG_PROJECTION_SELECTED_NEXT | the clean theorem target is terminal public metric/coframe; fallback is projection-ready b_R/d_R/w_R bound rows | 1880 should try terminal-public-metric proof once, then build bound projection rows if it fails | False | False |

## Next Target

| branch_id | route_id | target_doc | target_script | objective | selection_status | success_condition | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | NEXT1879_0_primary | 1880-Y5-R2FR-terminal-public-coframe-no-shadow-frame-or-bg-bound-projection.md | scripts/Y5_R2FR_terminal_public_coframe_no_shadow_frame_or_bg_bound_projection_1880.py | try to derive a terminal public coframe/ordinary-matter domain that excludes C_R/J_q Weyl, disformal, and source-prefactor slots; if not, build projection-ready b_R/d_R/w_R bound rows. | selected | no-shadow theorem with parent source, or nonclaim bound projection rows for PPN/WEP/clock/orbital/R10 guards. | False |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | NEXT1879_1_later | 1880b-Y5-R2FR-source-readout-marker-boundary-qbasicity-after-coframe.md | scripts/Y5_R2FR_source_readout_marker_boundary_qbasicity_after_coframe_1880b.py | after no-shadow/coframe ownership, test source/readout/marker/boundary q-basicity so C_R cannot reenter through endpoints or materials. | held_later | q-basic theorem or finite leak rows for source/readout/marker/boundary. | False |

## Validation

| validation_id | status | detail | valid_for_claim |
| --- | --- | --- | --- |
| VAL1879_0_sources | PASS | 1878/1739/no-shadow/single-public-metric sources are available | False |
| VAL1879_1_ownership_stack | PASS | parent q/coframe/no-shadow/source/boundary/tau stack is explicit and unsigned | False |
| VAL1879_2_no_shadow_tests | PASS | no-shadow theorem is conditional and covariance/WEP/Ward shortcuts are rejected | False |
| VAL1879_3_leak_rows | PASS | b_R/d_R/w_R/endpoint/total finite rows are staged as missing nonclaim rows | False |
| VAL1879_4_arena_interface | PASS | local_GR, PPN, clock/WEP, orbital and R10 interfaces stay blocked with route guards | False |
| VAL1879_5_claim_gate | PASS | only internal nonclaim audit is allowed | False |
| VAL1879_6_decision | PASS | decision ledger records no-ownership verdict and selects terminal-public-metric/bound projection next | False |
| VAL1879_7_next_target | PASS | 1880 terminal public coframe/no-shadow target selected | False |
| VAL1879_8_claim_flags_false | PASS | checked=101 | False |
| VAL1879_9_missing_not_ready | PASS | checked_missing_rows=12 | False |
| VAL1879_10_csv_parse | PASS | P8_Y5_PARENT_QLOC_1879_SOURCE_REGISTER.csv:9;P8_Y5_PARENT_QLOC_1879_PARENT_COFRAME_OWNERSHIP_STACK.csv:7;P8_Y5_PARENT_QLOC_1879_NO_SHADOW_FRAME_TESTS.csv:6;P8_Y5_PARENT_QLOC_1879_COMMON_FRAME_LEAK_BOUND_ROWS.csv:5;P8_Y5_PARENT_QLOC_1879_ARENA_BOUND_INTERFACE.csv:5;P8_Y5_PARENT_QLOC_1879_CLAIM_GATE.csv:5;P8_Y5_PARENT_QLOC_1879_DECISION_LEDGER.csv:4;P8_Y5_PARENT_QLOC_1879_NEXT_TARGET.csv:2 | False |
| VAL1879_11_branch_copies | PASS | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\microscope\branch_locked_wep\residuals\P8_Y5_PARENT_QLOC_1879_PARENT_COFRAME_OWNERSHIP_STACK.csv;D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\microscope\quarantine\1879\P8_Y5_PARENT_QLOC_1879_COMMON_FRAME_LEAK_BOUND_ROWS.csv;D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\rab-sector\acquisition-queue\JR1879_PARENT_COFRAME_OWNERSHIP_STACK_NONCLAIM.csv;D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\rab-sector\acquisition-queue\JR1879_COMMON_FRAME_LEAK_BOUND_ROWS_NONCLAIM.csv | False |
| VAL1879_12_pycache_absent | PASS | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\scripts\__pycache__ | False |
| VAL1879_13_formalization_untouched | PASS | formalization_1879_count=0 | False |
| VAL1879_OVERALL | PASS | 1879 parent coframe ownership or common-frame leak bound | False |
