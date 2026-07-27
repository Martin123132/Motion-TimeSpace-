# 1206 Y5/R10 K_T Boundary Trace Law Or P_loc Leakage Smallness Derivation

**Current verdict:** 1206 makes real derivational progress but still no R10/local-GR claim. `||B_T||` is lowered to a normal-trace/domain-source bound, and primitive `eps_P` is replaced by `epsilon_geom` built from lower-level projector/coframe/domain-motion constants.

**Main progress:** the boundary and projector blockers are no longer primitive labels. The harsh split target remains `1.17233215026e-05`, but the scoreable inequalities are now `C_pair C_NT (||K_T||+||G_res||+||R_perp||) <= target` and `epsilon_geom ||G_res|| <= target` with `C_CK epsilon_geom < 1`.

## Source Register

| source_id | local_path | needle | purpose | path_exists | needle_found | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| SRC1206_0_1205_next | 1205-Y5-R10-first-BT-or-epsP-source-row-fill.md | NEXT1205_0_1206 | handoff to K_T trace law or P_loc leakage smallness derivation | True | True | False | False |
| SRC1206_1_1205_pressure | source-intake/mts_residuals/P8_Y5_R10_1205_BOUND_PRESSURE_TARGETS.csv | PRS1205_1_boundary_split_trace_bound | harsh equal-split pressure targets | True | True | False | False |
| SRC1206_2_1195_DT_operator | 1195-Y5-R10-parent-DT-operator-range-source-or-Einstein-domain-classifier.md | DTA1195_0_operator_definition | D_T maps tracefree tensors to projected local vectors | True | True | False | False |
| SRC1206_3_1195_adjoint | 1195-Y5-R10-parent-DT-operator-range-source-or-Einstein-domain-classifier.md | DTA1195_1_formal_adjoint | formal adjoint with P_loc derivative and boundary terms | True | True | False | False |
| SRC1206_4_1196_projector | 1196-Y5-R10-DT-cokernel-zero-boundary-theorem-or-parent-action-block.md | CKZ1196_3_projector_perturbation_bound | projector leakage smallness/absorption condition | True | True | False | False |
| SRC1206_5_1196_boundary | 1196-Y5-R10-DT-cokernel-zero-boundary-theorem-or-parent-action-block.md | BP1196_0_tracefree_adjoint_boundary | D_T integration-by-parts boundary pairing | True | True | False | False |
| SRC1206_6_1204_source_rows | source-intake/mts_residuals/P8_Y5_R10_1204_SOURCE_READY_BOUND_ROWS.csv | SBR1204_3_projector_finite_bound | source-ready boundary/projector fill schema | True | True | False | False |
| SRC1206_7_1205_blockers | source-intake/mts_residuals/P8_Y5_R10_1205_BLOCKER_LEDGER.csv | BLK1205_1_projector_missing_eps_constants | explicit missing lower-level constants before 1206 | True | True | False | False |

## Lowered Component Derivations

| derivation_id | component_lowered | starting_object | lowered_formula | derivation_steps | zero_condition | remaining_inputs | status | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| DRV1206_0_boundary_trace_lowering | q_boundary | q_boundary=\|\|B_T\|\| | q_boundary <= C_pair*C_NT(D,gamma)*(K_T_L2_norm + G_res_norm + R_perp_div_norm) | B_T[V,K_T]=<n.K_T,P_locV>_partialD; dual trace pairing gives q_boundary<=\|\|n.K_T\|\|_H-1/2\|\|P_locV\|\|_H1/2; normal-trace theorem gives \|\|n.K_T\|\|_H-1/2<=C_NT(\|\|K_T\|\|_L2+\|\|div K_T\|\|_L2); D_T K_T=P_loc divK_T=G_res leaves only G_res and perpendicular-divergence residue. | n_mu K_T^(mu nu)=0 on partialD or pullback(P_locV)=0 in the same parent local domain | C_pair;C_NT;K_T_L2_norm;G_res_norm;R_perp_div_norm;domain_id;norm_id | LOWERED_TO_GEOMETRIC_TRACE_CONTRACT_NONCLAIM | False | False |
| DRV1206_1_projector_leakage_lowering | q_projector | q_projector=\|\|Delta_P\|\| or eps_P\|\|G_res\|\| | q_projector <= epsilon_geom*G_res_norm, epsilon_geom=C_P*(nabla_P_loc_Linf + coframe_lock_Linf + domain_motion_Linf + projector_stress_Linf) | D_T^dagger V contains Pi_TF[nabla(P_locV)]=Pi_TF[P_loc nablaV]+Pi_TF[(nablaP_loc)V] plus coframe/domain-motion variations; collect those lower-order terms into epsilon_geom\|\|V\|\|_H1, then use the range/CK estimate to score epsilon_geom against G_res. | nabla P_loc=0, coframe/domain-motion silence, and projector-stress silence in the same parent quotient domain | C_P;nabla_P_loc_Linf;coframe_lock_Linf;domain_motion_Linf;projector_stress_Linf;G_res_norm;C_CK;domain_id;norm_id | LOWERED_TO_GEOMETRIC_SMALLNESS_CONTRACT_NONCLAIM | False | False |
| DRV1206_2_projector_absorption_gate | projector absorption | C_CK*eps_P<1 | C_CK*epsilon_geom < 1 and epsilon_geom*G_res_norm <= q_projector_target | Use CK/Korn inequality \|\|V\|\|_H1<=C_CK\|\|D_T^dagger V - projector_leak[V]\|\|; if \|\|projector_leak[V]\|\|<=epsilon_geom\|\|V\|\|_H1 and C_CK epsilon_geom<1, the perturbation is absorbed into the left side. | epsilon_geom=0 gives exact projector silence | C_CK;epsilon_geom;G_res_norm;q_projector_target | ABSORPTION_INEQUALITY_DERIVED_INPUTS_MISSING | False | False |

## Lower-Level Inputs To Fill

| input_id | component | quantity | definition | required_for | current_status | source_or_derivation_needed | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| IN1206_0_C_pair | q_boundary | C_pair | operator norm of trace pairing between n.K_T in H^{-1/2}(partialD) and P_locV in H^{1/2}(partialD) | DRV1206_0_boundary_trace_lowering | MISSING_DOMAIN_NORM_CONSTANT | domain and Sobolev trace convention | False | False |
| IN1206_1_C_NT | q_boundary | C_NT(D,gamma) | normal-trace theorem constant for H(div;D) symmetric tracefree tensor fields | DRV1206_0_boundary_trace_lowering | MISSING_DOMAIN_GEOMETRY_CONSTANT | local domain geometry, metric regularity, and boundary regularity | False | False |
| IN1206_2_KT_bulk_norm | q_boundary | K_T_L2_norm | bulk L2 norm of the tracefree compensator field in the selected local domain | DRV1206_0_boundary_trace_lowering | MISSING_PARENT_KT_BULK_EQUATION | parent K_T equation, coercivity, or theorem-zero no-hair clause | False | False |
| IN1206_3_Gres_norm | q_boundary/q_projector | G_res_norm | weighted norm of the local residual source vector in the same domain/norm as D_T | DRV1206_0_boundary_trace_lowering;DRV1206_1_projector_leakage_lowering | MISSING_G_RES_PROFILE_NORM | local residual profile from parent GR-reduction equations | False | False |
| IN1206_4_Rperp | q_boundary | R_perp_div_norm | unprojected divergence residue (I-P_loc) div K_T not seen by D_T K_T=P_loc div K_T | DRV1206_0_boundary_trace_lowering | MISSING_PERPENDICULAR_DIVERGENCE_GUARD | P_loc complement theorem or finite perpendicular divergence bound | False | False |
| IN1206_5_epsilon_geom | q_projector | epsilon_geom | lower-level geometric projector leakage coefficient built from nablaP/coframe/domain-motion/projector-stress norms | DRV1206_1_projector_leakage_lowering | FORMULA_DERIVED_COMPONENT_NORMS_MISSING | nabla_P_loc_Linf;coframe_lock_Linf;domain_motion_Linf;projector_stress_Linf;C_P | False | False |
| IN1206_6_C_CK | q_projector | C_CK | anchored conformal-Killing/Korn constant for the selected local domain | DRV1206_2_projector_absorption_gate | MISSING_CK_KORN_CONSTANT | domain anchor, no-zero-mode certificate, metric regularity | False | False |

## Pressure Comparison

| comparison_id | component | lowered_quantity | target | target_context | comparison_status | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CMP1206_0_boundary_lowered_target | q_boundary | C_pair*C_NT*(K_T_L2_norm+G_res_norm+R_perp_div_norm) | 1.17233215026e-05 | harsh W=100 boundary/projector equal split | EXECUTABLE_FORMULA_INPUTS_MISSING | False | False |
| CMP1206_1_projector_lowered_target | q_projector | epsilon_geom*G_res_norm | 1.17233215026e-05 | harsh W=100 boundary/projector equal split | EXECUTABLE_FORMULA_INPUTS_MISSING | False | False |
| CMP1206_2_projector_absorption_target | projector_absorption | C_CK*epsilon_geom | < 1 | operator perturbation absorption | EXECUTABLE_FORMULA_INPUTS_MISSING | False | False |

## Branch Selection

| branch_id | route | gain | cost | current_status | recommended_next | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| BR1206_0_boundary_route | K_T normal trace bound | replaces undefined \|\|B_T\|\| by normal-trace/domain/source constants | still needs K_T bulk norm, G_res_norm, R_perp_div_norm, and domain trace constants | LOWERED_NOT_NUMERIC | source G_res_norm and local domain constants, or derive n.K_T=0 from parent boundary action | False | False |
| BR1206_1_projector_route | P_loc leakage smallness | replaces undefined eps_P by epsilon_geom from nablaP/coframe/domain-motion/projector-stress norms | still needs G_res_norm, C_CK, and each geometric leakage norm | LOWERED_NOT_NUMERIC | derive P_loc frozen/coframe-lock theorem from parent quotient geometry | False | False |
| BR1206_2_best_next | projector route first | a parent quotient/frozen-projector theorem can set epsilon_geom=0 and remove q_projector entirely | requires same parent-owned domain and physical-charge guard | SELECTED_NEXT_DERIVATION_ROUTE | try to prove epsilon_geom=0 or bound it from quotient/coframe locks before sourcing numeric K_T | False | False |

## Claim Gates

| gate_id | gate | status | reason | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- |
| GATE1206_0_lowered_boundary_not_numeric | q_boundary numeric score | BLOCKED | normal-trace law is derived, but C_pair, C_NT, K_T_L2, G_res_norm, and R_perp are missing | False | False |
| GATE1206_1_lowered_projector_not_numeric | q_projector numeric score | BLOCKED | epsilon_geom formula is derived, but geometric leakage norms, C_CK, and G_res_norm are missing | False | False |
| GATE1206_2_no_placeholder_rhs | lowered formulas avoid B_T/eps_P placeholders | ACTIVE_GUARD | RHS uses lower-level geometric/source constants rather than undefined B_T or eps_P rows | False | False |
| GATE1206_3_R10_local_GR | R10/local-GR branch | BLOCKED | lowered contracts are not yet numeric/source-backed and official W_R10 remains nonclaim | False | False |

## Decision Ledger

| decision_id | condition | decision | result | next_action | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- |
| DEC1206_0_verdict | direct B_T/eps_P source rows are absent | derive lowered formulas instead of scanning again | B_T is lowered to a normal-trace/domain-source bound; eps_P is lowered to epsilon_geom from projector/coframe/domain-motion norms | attack projector route first: prove epsilon_geom=0 from parent quotient/coframe lock or fill its lower-level geometric norms | False | False |

## Next Target

| next_id | target_file | target_script | task | success_condition | do_not_do | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| NEXT1206_0_1207 | 1207-Y5-R10-quotient-coframe-lock-or-epsilon-geom-source-pack.md | scripts/Y5_R10_quotient_coframe_lock_or_epsilon_geom_source_pack.py | try to prove epsilon_geom=0 from the parent quotient/coframe/domain lock; if not, stage source-ready rows for nabla_P_loc_Linf, coframe_lock_Linf, domain_motion_Linf, projector_stress_Linf, C_P, C_CK, and G_res_norm | q_projector is either theorem-zero by parent geometry or has a lower-level source-pack ready for numeric nonclaim scoring | do not claim R10/local-GR pass, do not reintroduce eps_P as a primitive placeholder, do not edit formalization-workbench, do not push GitHub | False | False |

## Validation

| check_id | check | status | details | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- |
| VAL1206_0_sources_exist | all cited local sources exist | PASS | 8/8 sources exist | False | False |
| VAL1206_1_needles_found | all cited source needles found | PASS | 8/8 needles found | False | False |
| VAL1206_2_boundary_lowered | boundary component is lowered to trace/source constants | PASS | DRV1206_0 present | False | False |
| VAL1206_3_projector_lowered | projector component is lowered to epsilon_geom constants | PASS | DRV1206_1 present | False | False |
| VAL1206_4_no_placeholder_rhs | lowered RHS avoids B_T and eps_P primitive placeholders | PASS | forbidden_rhs= | False | False |
| VAL1206_5_lower_inputs_present | lower-level inputs to fill are enumerated | PASS | C_CK,C_NT(D,gamma),C_pair,G_res_norm,K_T_L2_norm,R_perp_div_norm,epsilon_geom | False | False |
| VAL1206_6_pressure_targets_match | 1205 harsh split targets are preserved | PASS | boundary=1.17233215026e-05;projector=1.17233215026e-05 | False | False |
| VAL1206_7_next_projector_route | next route selects quotient/coframe projector attack | PASS | projector route selected | False | False |
| VAL1206_8_nonclaim_policy | all generated rows remain nonclaim | PASS | valid_for_claim=false and claim_allowed=false throughout | False | False |
| VAL1206_9_csv_parse | all generated CSVs parse cleanly | PASS | P8_Y5_R10_1206_SOURCE_REGISTER.csv:8; P8_Y5_R10_1206_LOWERED_COMPONENT_DERIVATIONS.csv:3; P8_Y5_R10_1206_LOWER_LEVEL_INPUTS_TO_FILL.csv:7; P8_Y5_R10_1206_PRESSURE_COMPARISON.csv:3; P8_Y5_R10_1206_BRANCH_SELECTION.csv:3; P8_Y5_R10_1206_CLAIM_GATES.csv:4; P8_Y5_R10_1206_DECISION_LEDGER.csv:1; P8_Y5_R10_1206_NEXT_TARGET.csv:1 | False | False |
| VAL1206_10_formalization_untouched | formalization-workbench untouched during run | PASS | formalization_recent_after_run_start_count=0 | False | False |
| VAL1206_11_overall | overall 1206 validation | PASS | 1206 lowered trace/leakage contracts are reproducible and nonclaim | False | False |
