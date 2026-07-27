# 1972 Y5 R2FR: Minimal X_B Parent Ownership Clause Or Schur Fill

Private checkpoint. This tests whether the clean `C_XR=0` route from 1971 can be made compatible with the existing `X_B` definition.

Verdict: the full current `X_B` bundle cannot honestly be geometry-blind, because `85-coarse-graining-invariants-XB.md` includes `A_curv`, built from curvature norms. A relative theorem exists for a geometry-blind `X_env`, but that is not the same as the present full `X_B` bundle. Therefore the next serious move is either an `X_env/X_route` split firewall or a finite two-field Schur coefficient fill.

No EH/Newton/local-GR claim follows from this checkpoint.

## Source Register

| branch | row_id | valid_for_claim | public_claim | created_utc | source_path | purpose | required_needles | status | missing_needles |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | 1971_doc | False | False | 2026-06-20T01:14:42.394987+00:00 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1971-Y5-R2FR-XB-curvature-independence-or-two-field-Schur-coefficient.md | 1972 minimal X_B parent-ownership clause or Schur fill | CXR1971_1_exact_zero_condition;CXR1971_2_verticality_not_enough;NEXT1971_0_primary | EXISTS_NEEDLES_CONFIRMED |  |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | 1971_validation | False | False | 2026-06-20T01:14:42.395575+00:00 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_BRR545_1971_VALIDATION.csv | 1972 minimal X_B parent-ownership clause or Schur fill | VAL1971_OVERALL;PASS | EXISTS_NEEDLES_CONFIRMED |  |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | 85_XB_invariants | False | False | 2026-06-20T01:14:42.396188+00:00 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\85-coarse-graining-invariants-XB.md | 1972 minimal X_B parent-ownership clause or Schur fill | coarse_graining_invariants_XB_candidate_bundle_v1;X_B = {;A_curv;This file does not prove the coarse-graining theorem. | EXISTS_NEEDLES_CONFIRMED |  |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | 83_parent_equations | False | False | 2026-06-20T01:14:42.396832+00:00 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\83-parent-equations-v1.md | 1972 minimal X_B parent-ownership clause or Schur fill | X_B cannot be selected differently;q^nu = nabla^nu Gamma_eff - nabla_mu K_hat;coarse-graining theorem for X_B | EXISTS_NEEDLES_CONFIRMED |  |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | 1306_XB_domain | False | False | 2026-06-20T01:14:42.397539+00:00 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1306-Y5-R10-RAB-Zm-parent-function-or-XB-domain-range.md | 1972 minimal X_B parent-ownership clause or Schur fill | FRA1306_1_XB_dependent;XDG1306_0_argument_list;XDG1306_4_arena_rule | EXISTS_NEEDLES_CONFIRMED |  |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | 826_Ward_audit | False | False | 2026-06-20T01:14:42.398163+00:00 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_826_WARD_BIANCHI_AUDIT.csv | 1972 minimal X_B parent-ownership clause or Schur fill | W826_1_external_XB_spurion;W826_3_Khat_required | EXISTS_NEEDLES_CONFIRMED |  |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | 1349_KMTS_owner | False | False | 2026-06-20T01:14:42.398777+00:00 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1349-Y5-R10-RAB-KMTS-trace-projection-owner-or-memory-closure-declaration.md | 1972 minimal X_B parent-ownership clause or Schur fill | KMTS1349_3_Ward_closure;RESP1349_2_external_profiles | EXISTS_NEEDLES_CONFIRMED |  |

## Minimal X_B Ownership Clause

| branch | row_id | valid_for_claim | public_claim | created_utc | object | clause | status | implication |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | OWN1972_0_clause_target | False | False | 2026-06-20T01:14:42.398800+00:00 | minimal X_B ownership clause | Find a parent object X_env such that X_env=X_env[I_top,q_env,boundary_class] and D X_env[delta Phi_R]=0 for compact local curvature variations preserving branch/boundary data. | TARGET_DEFINED | This would make C_XR=0 without tuning a small coefficient. |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | OWN1972_1_relative_theorem | False | False | 2026-06-20T01:14:42.398810+00:00 | relative curvature-independence theorem | If X_env depends only on fixed topological/boundary/branch data and local variations delta Phi_R have compact support inside D_loc, then D X_env[delta Phi_R]=0. | RELATIVE_CXR_ZERO_THEOREM | The theorem is mathematically clean if the parent supplies X_env and the allowed-variation class. |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | OWN1972_2_required_variation_class | False | False | 2026-06-20T01:14:42.398817+00:00 | allowed local curvature variation | delta Phi_R changes g_obs/R_geom in the local exterior but preserves branch labels, boundary cohomology, and global coarse-graining data. | VARIATION_CLASS_REQUIRED | Without this tangent-space split, C_XR cannot be evaluated honestly. |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | OWN1972_3_Ward_safe_owner | False | False | 2026-06-20T01:14:42.398829+00:00 | not an external spurion | X_env must be a parent-owned field/label whose ancestors are varied, constrained, or topological; merely holding X_B fixed by hand fails Ward/Bianchi. | SPURION_FIREWALL_REQUIRED | This keeps the zero theorem from becoming a hidden nonconservation trick. |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | OWN1972_4_source_boundary_silence | False | False | 2026-06-20T01:14:42.398834+00:00 | source/bath/boundary completion | Source, bath, and boundary terms must either be independent of X_env under delta Phi_R or included in the same silent/topological variation theorem. | SIDE_CHANNELS_REQUIRED | C_XR=0 alone is not enough if source/boundary vertices reintroduce B_YR. |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | OWN1972_5_same_arena_rule | False | False | 2026-06-20T01:14:42.398839+00:00 | same parent coefficient law | The geometry-blind coefficient owner cannot be switched per galaxy/cosmology/local test after seeing data. | ARENA_RULE_REQUIRED | Protects the field-theory route from becoming a patchwork selector. |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | OWN1972_6_current_clause_status | False | False | 2026-06-20T01:14:42.398844+00:00 | current corpus does not sign OWN1972_0..5 | The required X_env/variation split is not present as a parent action clause in the inspected source trail. | MINIMAL_CLAUSE_NOT_SOURCE_SIGNED | The clean zero route is a future architecture option, not a current derivation. |

## Current X_B Compatibility Audit

| branch | row_id | valid_for_claim | public_claim | created_utc | finding | formula | status | consequence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | XBI1972_0_current_XB_contains_curvature | False | False | 2026-06-20T01:14:42.398850+00:00 | formalization-workbench 85 defines X_B with A_curv built from C_abs and R_abs | A_curv = c^2 L_cg [w_C C_abs + w_R R_abs]/(c H_bg) | CONTRADICTS_GEOMETRY_BLIND_ZERO_FOR_FULL_XB | A full-bundle X_B cannot satisfy D X_B[delta Phi_R]=0 generically because it deliberately contains curvature diagnostics. |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | XBI1972_1_generic_derivative | False | False | 2026-06-20T01:14:42.398855+00:00 | generic variation of the curvature diagnostic is nonzero | delta A_curv ~= (c L_cg/H_bg)(w_C delta C_abs + w_R delta R_abs) + scale-response terms | CXR_GENERALLY_NONZERO_IF_A_CURV_ENTERS_ACTION_COEFFICIENTS | R2/fR danger is real if memory/action coefficients depend on the full X_B bundle. |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | XBI1972_2_safe_split_architecture | False | False | 2026-06-20T01:14:42.398861+00:00 | possible repair: split coefficient owner from routing diagnostics | X_B -> (X_env, X_route), with action coefficients Z_m,V_R,F_L depending only on geometry-blind X_env while A_curv lives only in a Ward-safe routing/readout sector | SPLIT_ROUTE_IDENTIFIED_UNSIGNED | This is the least destructive way to keep useful X_B diagnostics without forcing C_XR into the EH action. |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | XBI1972_3_forbidden_hide | False | False | 2026-06-20T01:14:42.398866+00:00 | forbidden repair: call A_curv non-dynamical after using it in action coefficients | A_curv in coefficients but fixed in variation is an external-spurion move unless a parent constraint/auxiliary action owns it | FORBIDDEN_AS_THEOREM | No local-GR claim may use this shortcut. |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | XBI1972_4_current_verdict | False | False | 2026-06-20T01:14:42.398870+00:00 | full current X_B bundle does not support C_XR=0 | Because X_B includes curvature norms, the full-bundle zero theorem fails unless the active coefficient dependence excludes the curvature components or a projector annihilates them. | FULL_XB_ZERO_ROUTE_FAILS_CURRENT_DEFINITION | The next real leap is X_env/X_route split proof or Schur coefficient fill. |

## Route Split Decision

| branch | row_id | valid_for_claim | public_claim | created_utc | route | result | status | next_action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | ROUTE1972_0_geometry_blind_env | False | False | 2026-06-20T01:14:42.398876+00:00 | X_env is branch/topological/boundary data | C_XR=0 relative theorem can close if source/bath/boundary side channels are silent | BEST_THEOREM_ROUTE_BUT_NOT_CURRENT_XB | requires explicit split from A_curv-style diagnostics |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | ROUTE1972_1_full_invariant_bundle | False | False | 2026-06-20T01:14:42.398882+00:00 | coefficients depend on the full X_B bundle from 85 | C_XR is generically nonzero because A_curv contains curvature norms | SCHUR_ROUTE_REQUIRED | must fill C_XR/H_X/H_mX rather than claim EH silence |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | ROUTE1972_2_readout_only_routing | False | False | 2026-06-20T01:14:42.398887+00:00 | A_curv used only after variation as a diagnostic/routing label | may be safe only if parent action coefficients do not depend on A_curv and Ward/Khat owner covers routing stress | POSSIBLE_BUT_OWNER_MISSING | needs a firewall proving routing diagnostics are not action couplings |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | ROUTE1972_3_auxiliary_constraint | False | False | 2026-06-20T01:14:42.398892+00:00 | A_curv promoted to auxiliary constrained variable | could be varied with a constraint action, but then its multiplier/stress contributes to the Schur/Khat block | LIVE_FIELD_ROUTE | not a zero theorem; source the auxiliary block |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | ROUTE1972_4_decision | False | False | 2026-06-20T01:14:42.398897+00:00 | do not claim C_XR=0 for current full X_B | either split X_env/X_route or fill the finite Schur coefficient matrix | ROUTE_DECISION_NONCLAIM | prevents the theory from smuggling a curvature diagnostic into the EH action |

## Schur Fill Input Pack

| branch | row_id | valid_for_claim | public_claim | created_utc | object | formula | status | requirement |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | FILL1972_0_CXR | False | False | 2026-06-20T01:14:42.398903+00:00 | C_XR or B_XR | C_XR^A = delta X_B^A/delta R_geom; for A_curv branch include w_C,w_R,L_cg,H_bg and derivative of curvature norms | MISSING_NUMERIC_OR_THEOREM_VALUE | units: [X_B]/[R_geom]; source must state active X_B component and local branch |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | FILL1972_1_HX | False | False | 2026-06-20T01:14:42.398908+00:00 | H_X | second variation/operator for active X_B or auxiliary environment block | MISSING_OPERATOR | needed to invert the X_B response safely |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | FILL1972_2_Hm | False | False | 2026-06-20T01:14:42.398914+00:00 | H_m | -nabla_mu(Z_m nabla^mu)+V_mm plus source/boundary corrections | PARTIAL_TEMPLATE_ONLY | template exists but Z_m,V_mm,domain,sign still missing |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | FILL1972_3_HmX | False | False | 2026-06-20T01:14:42.398919+00:00 | H_mX / V_mX | mixed memory-environment Hessian for V_R(m;X_B), Z_m(X_B), and source terms | MISSING_COUPLING | the coupling bottleneck in literal form |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | FILL1972_4_BYR | False | False | 2026-06-20T01:14:42.398923+00:00 | B_YR vector | B_YR=(B_mR_direct+B_source+B_boundary, B_XR) | MISSING_VECTOR | required before Delta c_R2 can be computed |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | FILL1972_5_cR2 | False | False | 2026-06-20T01:14:42.398928+00:00 | generated R2/fR coefficient | Delta c_R2=-1/2 B_YR^T H_Y^{-1} B_YR plus bare/measure/boundary terms under parent sign convention | FORMULA_READY_VALUES_MISSING | cannot compare to R11 bound curve until FILL1972_0..4 close |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | FILL1972_6_claim_guard | False | False | 2026-06-20T01:14:42.398934+00:00 | claim eligibility | all FILL rows require numeric/theorem value, units, domain, source path, and valid_for_claim=true before scoring | CLAIM_BLOCKED | keeps the Schur path honest and executable later |

## Runner Dryrun

| branch | row_id | valid_for_claim | public_claim | created_utc | input_row | runner_status | reason | accepted_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | RUN1972_0_relative_clause | False | False | 2026-06-20T01:14:42.398940+00:00 | OWN1972_1_relative_theorem | PASS_RELATIVE_THEOREM | geometry-blind X_env would give C_XR=0 | False |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | RUN1972_1_current_clause | False | False | 2026-06-20T01:14:42.398946+00:00 | OWN1972_6_current_clause_status | REJECTED_UNSIGNED | minimal parent clause is not source-signed | False |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | RUN1972_2_current_XB | False | False | 2026-06-20T01:14:42.398951+00:00 | XBI1972_4_current_verdict | REJECTED_FULL_XB_ZERO | current full X_B contains curvature diagnostics | False |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | RUN1972_3_schur_fill | False | False | 2026-06-20T01:14:42.398955+00:00 | FILL1972_0..6 | REJECTED_MISSING_VALUES | Schur inputs are staged but not source-backed | False |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | RUN1972_VERDICT | False | False | 2026-06-20T01:14:42.398960+00:00 | all_rows | FULL_XB_CXR_ZERO_FAILS_SPLIT_OR_SCHUR_NEXT_NONCLAIM | do not claim EH; choose X_env/X_route split proof or finite coefficient fill | False |

## Claim Gate

| branch | row_id | valid_for_claim | public_claim | created_utc | claim | status | reason |
| --- | --- | --- | --- | --- | --- | --- | --- |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | CG1972_0_geometry_blind_Xenv | False | False | 2026-06-20T01:14:42.398966+00:00 | geometry-blind X_env parent clause is signed | FAIL_BLOCKED | relative theorem only, no source-signed parent clause |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | CG1972_1_full_XB_CXR_zero | False | False | 2026-06-20T01:14:42.398971+00:00 | current full X_B has C_XR=0 | FAIL_REJECTED | A_curv curvature component makes generic C_XR nonzero |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | CG1972_2_split_firewall | False | False | 2026-06-20T01:14:42.398976+00:00 | X_env/X_route split firewall is derived | FAIL_BLOCKED | not yet built |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | CG1972_3_schur_coefficients | False | False | 2026-06-20T01:14:42.398981+00:00 | finite Schur coefficient pack is scoreable | FAIL_BLOCKED | C_XR/H_X/H_mX/B_YR values missing |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | CG1972_4_EH_second_order | False | False | 2026-06-20T01:14:42.398986+00:00 | EH second-order local action is derived | FAIL_BLOCKED | R2/fR gate open |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | CG1972_5_local_GR_Newton | False | False | 2026-06-20T01:14:42.398990+00:00 | local GR/Newton follows | FAIL_BLOCKED | EH plus PPN/matter gates remain |

## Decision Ledger

| branch | row_id | valid_for_claim | public_claim | created_utc | decision | reason | next_action |
| --- | --- | --- | --- | --- | --- | --- | --- |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | DEC1972_0_main_result | False | False | 2026-06-20T01:14:42.398996+00:00 | FULL_XB_ZERO_ROUTE_REJECTED | The current X_B candidate contains curvature diagnostics, so the full-bundle C_XR=0 theorem cannot be true generically. | stop trying to prove C_XR=0 for the current full X_B bundle |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | DEC1972_1_best_next | False | False | 2026-06-20T01:14:42.399001+00:00 | SPLIT_XB_OR_FILL_SCHUR | To keep the local EH route alive, action coefficients must depend on a geometry-blind X_env, while curvature diagnostics move to a routing/readout sector with a Ward-safe owner; otherwise fill the Schur matrix. | test the X_env/X_route split firewall next |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | DEC1972_2_project_read | False | False | 2026-06-20T01:14:42.399006+00:00 | A_REAL_LEAP_NOT_A_DEAD_END | This converts a vague coupling worry into a concrete architecture decision: split the variable or score the induced higher-curvature term. | if split fails, begin C_XR first-row coefficient acquisition |

## Next Target

| branch | row_id | valid_for_claim | public_claim | created_utc | priority | target_doc | target_script | objective | acceptance_output | nonclaim_rule |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | NEXT1972_0_primary | False | False | 2026-06-20T01:14:42.399012+00:00 | selected | 1973-Y5-R2FR-XB-env-route-split-firewall-or-CXR-first-row.md | scripts/Y5_R2FR_XB_env_route_split_firewall_or_CXR_first_row_1973.py | derive a firewall splitting geometry-blind action coefficient owner X_env from curvature routing diagnostics X_route, or fill the first nonclaim C_XR coefficient row | split firewall theorem checklist or source-backed C_XR acquisition row template | no EH/local-GR claim while full X_B contains active curvature diagnostics in action coefficients |

## Project Status Snapshot

| branch | row_id | valid_for_claim | public_claim | created_utc | strongest_result | what_improved | still_missing | claim_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | SNAP1972_0_project_position | False | False | 2026-06-20T01:14:42.399018+00:00 | The clean X_B zero theorem is compatible only with a geometry-blind X_env, not with the current full X_B bundle containing A_curv. | The local EH obstruction is now an architecture decision: split coefficient-owner variables from routing diagnostics or calculate the induced Schur/R2 term. | X_env/X_route firewall, active coefficient dependency list, Ward-safe routing owner, C_XR, H_X, H_mX, source/bath/boundary vertices, units | private nonclaim; current full-bundle C_XR=0 rejected |

## Validation

| validation_id | status | detail | valid_for_claim | public_claim |
| --- | --- | --- | --- | --- |
| VAL1972_00_sources | PASS | all source paths exist and needles found | False | False |
| VAL1972_01_minimal_clause | PASS | minimal ownership clause formulated but unsigned | False | False |
| VAL1972_02_xb_compatibility | PASS | current full X_B zero route rejected | False | False |
| VAL1972_03_route_split | PASS | split-or-Schur route selected | False | False |
| VAL1972_04_schur_fill | PASS | Schur fill rows staged as nonclaim missing inputs | False | False |
| VAL1972_05_runner | PASS | runner blocks full-X_B C_XR zero claim | False | False |
| VAL1972_06_claim_gates | PASS | all claim gates blocked or rejected | False | False |
| VAL1972_07_decision | PASS | decision ledger records full-X_B zero rejection | False | False |
| VAL1972_08_next_target | PASS | 1973 target selected | False | False |
| VAL1972_09_claim_flags_safe | PASS | claim flags all false | False | False |
| VAL1972_10_csv_parse | PASS | all generated CSVs parse with rows | False | False |
| VAL1972_11_pycache_absent | PASS | scripts __pycache__ absent | False | False |
| VAL1972_12_formalization_untouched | PASS | formalization_1972_artifact_count=0 | False | False |
| VAL1972_OVERALL | PASS | 1972 minimal X_B parent ownership clause or Schur fill | False | False |
