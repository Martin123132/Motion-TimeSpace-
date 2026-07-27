# 1973 Y5 R2FR: X_env/X_route Split Firewall Or C_XR First Row

Private checkpoint. This tests the architecture repair selected in 1972: keep curvature diagnostics as routing/readout data while preventing them from entering action coefficients that would generate an `R2/fR` scalar tower.

Verdict: the `X_env/X_route` split is the right repair shape but is not source-signed in the current parent equations, which still write action-relevant coefficients as functions of unsplit `X_B`. The first symbolic `C_XR[A_curv]` row is now staged, with projection, norm-regularization, and active coefficient derivatives left explicit.

No EH/Newton/local-GR claim follows from this checkpoint.

## Source Register

| branch | row_id | valid_for_claim | public_claim | created_utc | source_path | purpose | required_needles | status | missing_needles |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | 1972_doc | False | False | 2026-06-20T01:18:21.507654+00:00 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1972-Y5-R2FR-minimal-XB-parent-ownership-clause-or-Schur-fill.md | 1973 X_env/X_route split firewall or C_XR first row | XBI1972_0_current_XB_contains_curvature;NEXT1972_0_primary | EXISTS_NEEDLES_CONFIRMED |  |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | 1972_validation | False | False | 2026-06-20T01:18:21.508240+00:00 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_BRR545_1972_VALIDATION.csv | 1973 X_env/X_route split firewall or C_XR first row | VAL1972_OVERALL;PASS | EXISTS_NEEDLES_CONFIRMED |  |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | 85_XB_invariants | False | False | 2026-06-20T01:18:21.508821+00:00 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\85-coarse-graining-invariants-XB.md | 1973 X_env/X_route split firewall or C_XR first row | Sector projections may use different functions of `X_B`;A_curv;Pi_B;They are routing and eligibility variables. | EXISTS_NEEDLES_CONFIRMED |  |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | 83_parent_equations | False | False | 2026-06-20T01:18:21.509407+00:00 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\83-parent-equations-v1.md | 1973 X_env/X_route split firewall or C_XR first row | F_L(X_B);R(m; X_B);m_L(X_B);coarse-graining theorem for X_B | EXISTS_NEEDLES_CONFIRMED |  |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | 1306_XB_domain | False | False | 2026-06-20T01:18:21.510001+00:00 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1306-Y5-R10-RAB-Zm-parent-function-or-XB-domain-range.md | 1973 X_env/X_route split firewall or C_XR first row | FRA1306_1_XB_dependent;XDG1306_4_arena_rule | EXISTS_NEEDLES_CONFIRMED |  |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | 826_coefficients | False | False | 2026-06-20T01:18:21.510640+00:00 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_826_COEFFICIENT_LEDGER.csv | 1973 X_env/X_route split firewall or C_XR first row | C826_0_Zm;C826_1_R_potential;C826_3_trace_coefficients | EXISTS_NEEDLES_CONFIRMED |  |

## X_env/X_route Firewall Test

| branch | row_id | valid_for_claim | public_claim | created_utc | gate | condition | status | implication |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | FIRE1973_0_split_definition | False | False | 2026-06-20T01:18:21.510662+00:00 | X_B split candidate | X_B := (X_env, X_route), where X_env owns action coefficients and X_route owns routing/eligibility diagnostics such as A_curv and Pi_B. | SPLIT_DEFINITION_WRITTEN | This is the only route that can keep useful curvature diagnostics without injecting them into the EH action. |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | FIRE1973_1_action_firewall | False | False | 2026-06-20T01:18:21.510672+00:00 | action coefficients ignore X_route | Z_m,V_R,F_L,L_cg,m_L may depend on X_env but not on A_curv/X_route unless the induced Schur coefficient is retained. | REQUIRED_NOT_SOURCE_SIGNED | Current 83 writes these as functions of X_B, not X_env. |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | FIRE1973_2_route_owner | False | False | 2026-06-20T01:18:21.510679+00:00 | routing diagnostics are Ward-safe | Pi_B,U_B,D_L and routing projectors may use X_route only if they are readout-only after variation or have a Khat/source/boundary stress owner. | REQUIRED_NOT_SOURCE_SIGNED | 85 names routing variables but says the theorem is not derived. |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | FIRE1973_3_same_parent_law | False | False | 2026-06-20T01:18:21.510684+00:00 | no per-sector retuning | X_env/X_route split must be one universal parent decomposition, not local-vs-galaxy relabelling after data. | POLICY_PASS_THEOREM_MISSING | 83/85 already forbid arbitrary per-sector X_B, but do not derive the split. |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | FIRE1973_4_active_dependency_list | False | False | 2026-06-20T01:18:21.510689+00:00 | active coefficient dependency list | The parent must list which X_B components enter Z_m, V_R, F_L, L_cg, m_L, gamma_B, lambda_R, and source/bath terms. | MISSING_ACTIVE_DEPENDENCY_LIST | Without this, C_XR cannot be zeroed or scored. |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | FIRE1973_5_verdict | False | False | 2026-06-20T01:18:21.510694+00:00 | split firewall status | The split is a strong architecture repair, but it is not present as a current parent theorem. | SPLIT_FIREWALL_FAILS_CURRENT_CORPUS | Proceed to first C_XR row and active-coefficient derivative audit. |

## C_XR A_curv First Row

| branch | row_id | valid_for_claim | public_claim | created_utc | object | formula | status | requirement |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | CXRROW1973_0_Acurv_definition | False | False | 2026-06-20T01:18:21.510701+00:00 | A_curv | A_curv = (c L_cg/H_bg)(w_C C_abs + w_R R_abs) | SOURCE_BACKED_SYMBOLIC | dimensionless curvature diagnostic in current X_B candidate |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | CXRROW1973_1_variation_formula | False | False | 2026-06-20T01:18:21.510706+00:00 | delta A_curv | delta A_curv = (c L_cg/H_bg)[w_C <C,delta C>/C_abs + w_R <Ric,delta Ric>/R_abs] + A_curv delta ln(L_cg/H_bg), away from norm-zero points | DERIVED_SYMBOLIC_NONCLAIM | this is the first explicit C_XR shape; it is direction-dependent, not a scalar number yet |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | CXRROW1973_2_scalar_projection | False | False | 2026-06-20T01:18:21.510711+00:00 | projection to delta R_geom | C_XR[A_curv] requires a map from scalar Ricci variation to delta Ricci/Weyl norm directions on the selected local branch | MISSING_PROJECTION_MAP | cannot score R2/fR until weak-field projection convention is fixed |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | CXRROW1973_3_norm_regularization | False | False | 2026-06-20T01:18:21.510716+00:00 | norm-zero/cusp guard | C_abs=sqrt(C^2), R_abs=sqrt(Ric^2) have derivative singularities at zero norm unless smoothed or branch-bounded away from zero | MISSING_REGULARIZATION_OR_BRANCH_BOUND | important for vacuum/asymptotic local systems |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | CXRROW1973_4_units | False | False | 2026-06-20T01:18:21.510721+00:00 | units | [C_XR] = [A_curv]/[R_geom] = L^2 for dimensionless A_curv and R_geom with units L^-2 | UNITS_FORMULA_READY | numeric comparison still needs normalization and active coefficient derivative |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | CXRROW1973_5_effective_vertex | False | False | 2026-06-20T01:18:21.510737+00:00 | effective curvature vertex | B_XR^eff = sum_A (partial coefficient/partial X_B^A) C_XR^A; for A=A_curv this needs partial_Acurv Z_m,V_R,F_L,L_cg,m_L,... | MISSING_ACTIVE_COEFFICIENT_DERIVATIVES | the next root input is not just C_XR, but which coefficients actually depend on A_curv |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | CXRROW1973_6_claim_status | False | False | 2026-06-20T01:18:21.510742+00:00 | first C_XR row | symbolic shape exists but no numeric/theorem value, projection map, regularization, or coefficient derivative is supplied | FIRST_ROW_STAGED_NONCLAIM | valid_for_claim remains false |

## Active Coefficient Dependency Map

| branch | row_id | valid_for_claim | public_claim | created_utc | coefficient | needed_derivative | status | implication |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | ACD1973_0_Zm | False | False | 2026-06-20T01:18:21.510749+00:00 | Z_m(X_B) | partial_Acurv Z_m | MISSING_PARENT_FUNCTION | if nonzero, kinetic normalization contributes metric-response residuals |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | ACD1973_1_VR | False | False | 2026-06-20T01:18:21.510755+00:00 | V_R(m;X_B) | partial_Acurv partial_m V_R or mixed Hessian V_mA | MISSING_PARENT_FUNCTION | if nonzero, memory scalar mediates a curvature-induced Schur term |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | ACD1973_2_FL | False | False | 2026-06-20T01:18:21.510760+00:00 | F_L(X_B) | partial_Acurv F_L | MISSING_PARENT_FUNCTION | if nonzero, local trace baseline has curvature dependence beyond EH |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | ACD1973_3_Lcg | False | False | 2026-06-20T01:18:21.510765+00:00 | L_cg(X_B) | partial_Acurv L_cg | MISSING_PARENT_FUNCTION | if nonzero, scale response feeds both q_loc and C_XR rows |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | ACD1973_4_mL | False | False | 2026-06-20T01:18:21.510770+00:00 | m_L(X_B) | partial_Acurv m_L | MISSING_PARENT_FUNCTION | moving extremum can move with curvature and feed the two-field block |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | ACD1973_5_source_bath | False | False | 2026-06-20T01:18:21.510775+00:00 | source/bath terms | partial_Acurv source/bath vertices | MISSING_ACTION | open-system terms must not bypass the firewall |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | ACD1973_6_verdict | False | False | 2026-06-20T01:18:21.510780+00:00 | active dependency map | all active coefficient derivatives with respect to A_curv | MISSING_DEPENDENCY_MAP | next target should zero these or keep finite Schur rows |

## Runner Dryrun

| branch | row_id | valid_for_claim | public_claim | created_utc | input_row | runner_status | reason | accepted_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | RUN1973_0_split_definition | False | False | 2026-06-20T01:18:21.510786+00:00 | FIRE1973_0_split_definition | PASS_ARCHITECTURE_CANDIDATE | split route is well-formed | False |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | RUN1973_1_firewall | False | False | 2026-06-20T01:18:21.510791+00:00 | FIRE1973_5_verdict | REJECTED_NOT_SOURCE_SIGNED | current corpus does not prove action coefficients ignore X_route | False |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | RUN1973_2_CXR_shape | False | False | 2026-06-20T01:18:21.510797+00:00 | CXRROW1973_1_variation_formula | PASS_SYMBOLIC_NONCLAIM | first C_XR derivative shape written | False |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | RUN1973_3_CXR_score | False | False | 2026-06-20T01:18:21.510802+00:00 | CXRROW1973_2..5 | REJECTED_MISSING_PROJECTION_AND_DERIVATIVES | projection, regularization, and active derivatives missing | False |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | RUN1973_VERDICT | False | False | 2026-06-20T01:18:21.510807+00:00 | all_rows | SPLIT_FIREWALL_UNSIGNED_FIRST_CXR_ROW_STAGED_NONCLAIM | next gate is active coefficient dependence on A_curv | False |

## Claim Gate

| branch | row_id | valid_for_claim | public_claim | created_utc | claim | status | reason |
| --- | --- | --- | --- | --- | --- | --- | --- |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | CG1973_0_split_firewall | False | False | 2026-06-20T01:18:21.510812+00:00 | X_env/X_route split firewall derived | FAIL_BLOCKED | architecture candidate only |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | CG1973_1_CXR_numeric | False | False | 2026-06-20T01:18:21.510818+00:00 | C_XR[A_curv] is numeric/theorem-sourced | FAIL_BLOCKED | projection and regularization missing |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | CG1973_2_active_derivatives_zero | False | False | 2026-06-20T01:18:21.510822+00:00 | active coefficient derivatives wrt A_curv vanish | FAIL_BLOCKED | dependency map missing |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | CG1973_3_schur_score | False | False | 2026-06-20T01:18:21.510827+00:00 | Schur R2/fR coefficient scoreable | FAIL_BLOCKED | B_YR/H_Y incomplete |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | CG1973_4_EH_second_order | False | False | 2026-06-20T01:18:21.510832+00:00 | EH second-order local action derived | FAIL_BLOCKED | R2/fR gate open |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | CG1973_5_local_GR_Newton | False | False | 2026-06-20T01:18:21.510838+00:00 | local GR/Newton follows | FAIL_BLOCKED | EH plus matter/PPN gates remain |

## Decision Ledger

| branch | row_id | valid_for_claim | public_claim | created_utc | decision | reason | next_action |
| --- | --- | --- | --- | --- | --- | --- | --- |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | DEC1973_0_result | False | False | 2026-06-20T01:18:21.510850+00:00 | SPLIT_FIREWALL_NOT_DERIVED | The split is the right architecture but the current parent equations still use unsplit X_B in action-relevant coefficients. | do not claim the split until active dependencies are rewritten and Ward-owned |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | DEC1973_1_first_row | False | False | 2026-06-20T01:18:21.510856+00:00 | CXR_ACURV_FIRST_ROW_STAGED | The first symbolic C_XR[A_curv] derivative is written; the missing pieces are projection, regularization, and active coefficient derivatives. | audit whether coefficients actually depend on A_curv; zero them or keep Schur rows |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | DEC1973_2_best_next | False | False | 2026-06-20T01:18:21.510861+00:00 | ACTIVE_COEFFICIENT_DEPENDENCE_ON_ACURV | If partial_Acurv Z_m,V_R,F_L,L_cg,m_L all vanish by architecture, the curvature diagnostic can be quarantined; if not, the Schur route is mandatory. | target active coefficient dependency map next |

## Next Target

| branch | row_id | valid_for_claim | public_claim | created_utc | priority | target_doc | target_script | objective | acceptance_output | nonclaim_rule |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | NEXT1973_0_primary | False | False | 2026-06-20T01:18:21.510867+00:00 | selected | 1974-Y5-R2FR-active-coefficient-dependence-on-Acurv-or-zero-projector.md | scripts/Y5_R2FR_active_coefficient_dependence_on_Acurv_or_zero_projector_1974.py | prove action-relevant coefficients have zero derivative with respect to A_curv, or promote A_curv to an explicit Schur/R2 coefficient source | active dependency zero map or finite derivative rows for Z_m,V_R,F_L,L_cg,m_L and source/bath terms | no EH/local-GR claim while active A_curv coefficient dependence is unknown |

## Project Status Snapshot

| branch | row_id | valid_for_claim | public_claim | created_utc | strongest_result | what_improved | still_missing | claim_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | SNAP1973_0_project_position | False | False | 2026-06-20T01:18:21.510874+00:00 | The split architecture is identified, and the first symbolic C_XR[A_curv] derivative row exists. | The bottleneck moved from vague coupling language to active coefficient derivatives with respect to A_curv. | active dependency map, projection from scalar curvature variation to curvature norms, norm regularization, H_Y/B_YR values, source/bath/boundary owner | private nonclaim; split firewall unsigned and first C_XR row unscoreable |

## Validation

| validation_id | status | detail | valid_for_claim | public_claim |
| --- | --- | --- | --- | --- |
| VAL1973_00_sources | PASS | all source paths exist and needles found | False | False |
| VAL1973_01_firewall | PASS | split firewall defined but not source-signed | False | False |
| VAL1973_02_cxr_first_row | PASS | first symbolic C_XR[A_curv] row and norm guard recorded | False | False |
| VAL1973_03_active_coefficients | PASS | active A_curv coefficient dependency map remains missing | False | False |
| VAL1973_04_runner | PASS | runner blocks split/CXR claim | False | False |
| VAL1973_05_claim_gates | PASS | all claim gates blocked | False | False |
| VAL1973_06_decision | PASS | decision selects active A_curv dependency next | False | False |
| VAL1973_07_next_target | PASS | 1974 target selected | False | False |
| VAL1973_08_claim_flags_safe | PASS | claim flags all false | False | False |
| VAL1973_09_csv_parse | PASS | all generated CSVs parse with rows | False | False |
| VAL1973_10_pycache_absent | PASS | scripts __pycache__ absent | False | False |
| VAL1973_11_formalization_untouched | PASS | formalization_1973_artifact_count=0 | False | False |
| VAL1973_OVERALL | PASS | 1973 X_env/X_route split firewall or C_XR first row | False | False |
