# 1209 Y5/R10 Local Fermi Domain Curvature Source Pack Or Domain Motion Lock

**Current verdict:** 1209 does **not** close the local-GR/R10 projector gate. It does convert the finite-domain projector problem into a cleaner GR-style source problem: local curvature, curvature gradient, finite domain size, frame acceleration/rotation, and the same-norm operator constants.

**Main progress:** the live clean branch is now `||nabla P_loc||_Linf(D_L) <= C_Fermi L_D||Riemann||_Linf + C_Fermi2 L_D^2||nabla Riemann||_Linf`. If the lab/domain is not an ideal free-fall Fermi tube, acceleration, rotation, domain-motion, and projector-stress rows must be added rather than hidden.

**Pressure kept honest:** the harsh target remains `q_projector <= 1.17233215026e-05` via `q_projector <= C_P*(fermi_curvature_projector_drift + coframe_lock_Linf + domain_motion_Linf + projector_stress_Linf)*G_res_norm`. This is a source-pack checkpoint, not a pass.

## Source Register

| source_id | local_path | needle | purpose | path_exists | needle_found | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| SRC1209_0_1208_next | 1208-Y5-R10-Ploc-parallel-projector-or-nablaPloc-bound.md | NEXT1208_0_1209 | handoff to local Fermi-domain curvature source pack | True | True | False | False |
| SRC1209_1_1208_fermi_bound | source-intake/mts_residuals/P8_Y5_R10_1208_NABLAPLOC_BOUND_LAW.csv | NPL1208_2_fermi_curvature_bound | finite-domain Fermi curvature bound for nabla_P_loc | True | True | False | False |
| SRC1209_2_1208_fermi_row | source-intake/mts_residuals/P8_Y5_R10_1208_SOURCE_READY_NABLAPLOC_ROW.csv | SRN1208_2_fermi_curvature_row | source-ready Fermi projector row to refine | True | True | False | False |
| SRC1209_3_1208_pressure | source-intake/mts_residuals/P8_Y5_R10_1208_PRESSURE_COMPARISON.csv | CMP1208_2_fermi_curvature_requirement | Fermi curvature pressure requirement | True | True | False | False |
| SRC1209_4_1207_pressure | source-intake/mts_residuals/P8_Y5_R10_1207_PRESSURE_AND_ABSORPTION_GATE.csv | PGA1207_0_total_formula | epsilon_geom target and absorption gate | True | True | False | False |
| SRC1209_5_1206_lowering | source-intake/mts_residuals/P8_Y5_R10_1206_LOWERED_COMPONENT_DERIVATIONS.csv | DRV1206_1_projector_leakage_lowering | q_projector lowered to epsilon_geom*G_res_norm | True | True | False | False |
| SRC1209_6_1195_adjoint | 1195-Y5-R10-parent-DT-operator-range-source-or-Einstein-domain-classifier.md | DTA1195_1_formal_adjoint | D_T adjoint shows derivative projector term to be bounded | True | True | False | False |
| SRC1209_7_1196_absorption | 1196-Y5-R10-DT-cokernel-zero-boundary-theorem-or-parent-action-block.md | CKZ1196_3_projector_perturbation_bound | operator absorption gate for projector leakage | True | True | False | False |
| SRC1209_8_1003_frame_verdict | 1003-Y5-R10-Bref-covariant-frame-theorem-or-Delta-ref-frame-profile-row.md | CFA1003_6_theorem_verdict | frame/coframe parent theorem still unsigned | True | True | False | False |
| SRC1209_9_1207_coframe_zero | source-intake/mts_residuals/P8_Y5_R10_1207_EPSILON_GEOM_ZERO_AUDIT.csv | ZEA1207_0_chain_rule_coframe | coframe chain-rule zero is conditional and carried forward | True | True | False | False |

## Fermi Domain Derivation

| derivation_id | object | derived_law | clean_zero_condition | new_lower_inputs | status | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| FDL1209_0_local_tube_setup | D_L local Fermi tube | Choose a central timelike curve gamma, Fermi/Fermi-Walker transported tetrad e_A, and finite radius L_D. Pointwise local inertial silence is not enough; the finite tube carries connection drift. | L_D=0, or flat/parallel geometry over the entire tube with fixed projector components. | central_worldline;Fermi_chart_source;L_D;transport_rule;support_weight | DOMAIN_SETUP_DERIVED_VALUES_MISSING | False | False |
| FDL1209_1_connection_drift | connection scale | \|\|Gamma\|\|_Linf(D_L) <= C_Gamma1*L_D*\|\|Riemann\|\|_Linf + C_Gamma2*L_D^2*\|\|nabla Riemann\|\|_Linf + C_acc*\|\|a\|\| + C_rot*\|\|omega\|\| | geodesic/Fermi-Walker branch with a=0, omega=0 and curvature-domain terms negligible or zero. | C_Gamma1;C_Gamma2;L_D;Riemann_norm;nabla_Riemann_norm;acceleration_norm;rotation_norm | FINITE_DOMAIN_CONNECTION_BOUND_DERIVED | False | False |
| FDL1209_2_projector_components | P_loc components in Fermi frame | If P_loc has fixed components in the Fermi tetrad, \|\|nabla P_loc\|\| <= C_Ploc*\|\|Gamma\|\|. If P components vary by readout/source choice, add \|\|partial_Fermi P_loc\|\|. | fixed projector components and zero connection drift throughout D_L. | C_Ploc;partial_Fermi_P_norm;projector_definition_path;connection_path | PROJECTOR_DRIFT_LOWERED_TO_CONNECTION_AND_COMPONENT_DRIFT | False | False |
| FDL1209_3_clean_freefall_fermi_bound | nabla_P_loc_Linf | clean branch: \|\|nabla P_loc\|\|_Linf(D_L) <= C_Fermi*L_D*\|\|Riemann\|\|_Linf(D_L) + C_Fermi2*L_D^2*\|\|nabla Riemann\|\|_Linf(D_L) | free-fall Fermi frame, fixed P components, no domain/readout variation, and exact flat/parallel finite domain. | C_Fermi;C_Fermi2;L_D;Riemann_norm;nabla_Riemann_norm;remainder_control | BEST_NONCLAIM_NUMERIC_ROUTE | False | False |
| FDL1209_4_pressure_insert | q_projector | q_projector <= C_P*(C_Fermi*L_D*Riemann_norm + C_Fermi2*L_D^2*nabla_Riemann_norm + coframe_lock_Linf + domain_motion_Linf + projector_stress_Linf)*G_res_norm | all bracket terms theorem-zero or sourced below target/(C_P*G_res_norm). | C_P;G_res_norm;coframe_lock_Linf;domain_motion_Linf;projector_stress_Linf | PRESSURE_FORM_DERIVED_VALUES_MISSING | False | False |

## Domain Motion And Projector Stress Audit

| audit_id | component | zero_or_bound_law | failure_mode | source_columns_needed | current_status | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| DMP1209_0_domain_motion_zero_branch | domain_motion_Linf | domain_motion_Linf=0 if the support tube, boundary, time normal, and weight are fixed by the same Fermi/parent readout map. | moving lab/support, changing readout weight, non-geodesic frame, or unmatched boundary transport | domain_id;central_worldline;support_map;boundary_transport;weight_function;domain_motion_norm;source_path | CONDITIONAL_ZERO_NOT_PARENT_SIGNED | False | False |
| DMP1209_1_non_geodesic_lab_bound | domain_motion_Linf | non-geodesic branch: domain_motion_Linf <= C_D*(acceleration_norm + rotation_norm + L_D*Riemann_norm + L_D^2*nabla_Riemann_norm) | Earth/lab frame acceleration or rotation can be small but cannot be silently set to zero | C_D;acceleration_norm;rotation_norm;L_D;Riemann_norm;nabla_Riemann_norm;source_path | BOUND_DERIVED_VALUES_MISSING | False | False |
| DMP1209_2_projector_stress_zero_branch | projector_stress_Linf | projector_stress_Linf=0 if P_loc definition, readout channel, and support weights are not varied independently of q and the Fermi domain. | hidden readout/source dependence changes P_loc even when coframe vertical variation is silent | P_loc_definition_path;readout_channel_path;support_weight_path;projector_stress_norm;source_path | CONDITIONAL_ZERO_NOT_PARENT_SIGNED | False | False |
| DMP1209_3_projector_stress_bound | projector_stress_Linf | projector_stress_Linf <= C_stress*(partial_readout_P_norm + partial_weight_P_norm + connection_mismatch_norm) | projector stress becomes a finite source row instead of a theorem zero | C_stress;partial_readout_P_norm;partial_weight_P_norm;connection_mismatch_norm;source_path | BOUND_DERIVED_VALUES_MISSING | False | False |
| DMP1209_4_total_epsilon_status | epsilon_geom | epsilon_geom=C_P*(fermi_curvature_projector_drift + coframe_lock_Linf + domain_motion_Linf + projector_stress_Linf) | even if Fermi projector drift is tiny, domain/stress/C_P/G_res can still block the local-GR/R10 pass | C_P;G_res_norm;all component bounds;C_CK;target | LOWERED_NOT_NUMERIC | False | False |

## Unified Source Pack

| input_id | symbol | definition | formula_role | units | required_source | current_value | current_status | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| USP1209_0_domain | D_L | finite local Fermi test tube/domain used for the projector leakage bound | sets finite radius and support for all norms | domain metadata | central_worldline;support_radius;boundary_transport;weight_function | MISSING | MISSING_LOCAL_DOMAIN_SOURCE | False | False |
| USP1209_1_LD | L_D | radius/diameter scale of the finite Fermi domain | multiplies curvature in nabla_P_loc bound | length | domain radius in same coordinates/norm as curvature | MISSING | MISSING_LENGTH_SCALE | False | False |
| USP1209_2_Riemann | Riemann_norm | supremum norm of local curvature over D_L | first finite-domain projector drift term | 1/length^2 | GR/MTS local metric or curvature profile source | MISSING | MISSING_CURVATURE_PROFILE | False | False |
| USP1209_3_nablaR | nabla_Riemann_norm | supremum norm of curvature gradient over D_L | second-order/remainder projector drift term | 1/length^3 | curvature-gradient profile or conservative upper bound | MISSING | MISSING_CURVATURE_GRADIENT_PROFILE | False | False |
| USP1209_4_CFermi | C_Fermi;C_Fermi2 | coordinate/norm constants for the Fermi connection and projector drift estimates | converts curvature-domain scale into nabla_P_loc_Linf | dimensionless | norm convention and Fermi expansion theorem/source path | MISSING | MISSING_OPERATOR_CONSTANTS | False | False |
| USP1209_5_accelrot | acceleration_norm;rotation_norm | non-geodesic lab-frame corrections if the domain is not ideal free-fall/Fermi-Walker | domain_motion and connection drift correction | 1/length | lab frame/source trajectory or free-fall theorem-zero clause | MISSING_OR_ZERO_BRANCH_UNSIGNED | MISSING_NON_GEODESIC_FRAME_INPUTS | False | False |
| USP1209_6_CP | C_P | operator constant converting geometry leakage terms into epsilon_geom | epsilon_geom multiplier | dimensionless_or_norm_defined | same-norm operator estimate from D_T adjoint/projector leakage | MISSING | MISSING_OPERATOR_CONSTANT | False | False |
| USP1209_7_Gres | G_res_norm | local residual source norm in the same domain/norm | q_projector = epsilon_geom*G_res_norm scoring factor | same as local residual norm | parent GR-reduction residual profile or theorem-zero source | MISSING | MISSING_G_RES_PROFILE_NORM | False | False |
| USP1209_8_domain_motion | domain_motion_Linf | finite support/boundary/readout-domain drift term | epsilon_geom additive component | 1/length_or_norm_defined | domain lock theorem or non-geodesic/domain bound | MISSING | MISSING_DOMAIN_LOCK_OR_BOUND | False | False |
| USP1209_9_projector_stress | projector_stress_Linf | variation of P_loc from readout/source/support changes not captured by Fermi curvature drift | epsilon_geom additive component | 1/length_or_norm_defined | projector definition lock or finite stress bound | MISSING | MISSING_PROJECTOR_STRESS_LOCK_OR_BOUND | False | False |
| USP1209_10_CCK | C_CK | conformal-Killing/Korn absorption constant | requires C_CK*epsilon_geom < 1 | norm_defined | same-domain CK/Korn estimate | MISSING | MISSING_ABSORPTION_CONSTANT | False | False |

## Pressure Smoke Schema

| pressure_id | formula | target | claim_rule | current_status | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- |
| PSC1209_0_clean_fermi_projector | q_projector <= C_P*(C_Fermi*L_D*Riemann_norm + C_Fermi2*L_D^2*nabla_Riemann_norm)*G_res_norm | 1.17233215026e-05 | valid only if coframe/domain/projector-stress are theorem-zero in the same domain | SCHEMA_READY_VALUES_MISSING | False | False |
| PSC1209_1_full_projector_budget | q_projector <= C_P*(C_Fermi*L_D*Riemann_norm + C_Fermi2*L_D^2*nabla_Riemann_norm + coframe_lock_Linf + domain_motion_Linf + projector_stress_Linf)*G_res_norm | 1.17233215026e-05 | all terms must be numeric/sourced or theorem-zero; any MISSING keeps branch blocked | FULL_SCHEMA_READY_VALUES_MISSING | False | False |
| PSC1209_2_absorption_budget | C_CK*C_P*(C_Fermi*L_D*Riemann_norm + C_Fermi2*L_D^2*nabla_Riemann_norm + coframe_lock_Linf + domain_motion_Linf + projector_stress_Linf) < 1 | <1 | same source rows must pass the operator absorption condition | ABSORPTION_SCHEMA_READY_VALUES_MISSING | False | False |
| PSC1209_3_radius_requirement_clean_branch | if nabla_Riemann term is negligible, L_D <= target/(C_P*C_Fermi*Riemann_norm*G_res_norm) | 1.17233215026e-05 | only an algebraic design inequality until C_P, C_Fermi, Riemann_norm, and G_res_norm are sourced | DESIGN_INEQUALITY_NOT_NUMERIC | False | False |
| PSC1209_4_blocker_policy | if any of C_P,G_res_norm,L_D,Riemann_norm,nabla_Riemann_norm,domain_motion,projector_stress are missing, q_projector claim_allowed=false | no missing claim inputs | missing source rows block claim even if formula looks small by intuition | BLOCK_POLICY_ACTIVE | False | False |

## Decision Ledger

| decision_id | condition | decision | result | next_action | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- |
| DEC1209_0_verdict | Can finite-domain Fermi geometry close q_projector now? | No numeric close yet. It lowers nabla_P_loc and domain drift to sourceable curvature/domain constants, but C_P, G_res_norm, and local domain constants are missing. | projector branch is stronger and more GR-like, but remains nonclaim. | build a first nonclaim local-curvature/G_res bracket smoke runner. | False | False |
| DEC1209_1_best_route | What should be sourced first? | Source or bracket G_res_norm and C_P alongside a conservative local curvature/domain scale; curvature alone cannot score q_projector. | next checkpoint should produce a feasibility map, not a pass/fail claim. | 1210 first local curvature scale plus G_res/C_P bracket smoke. | False | False |

## Claim Gates

| gate_id | gate | status | reason | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- |
| GATE1209_0_projector_zero | nabla_P_loc_Linf=0 | BLOCKED | Fermi pointwise silence does not prove finite-domain projector silence | False | False |
| GATE1209_1_projector_numeric | q_projector numeric target | BLOCKED | C_P, G_res_norm, curvature/domain constants, and domain/stress terms are unsourced | False | False |
| GATE1209_2_domain_motion_zero | domain_motion_Linf=0 | BLOCKED | requires parent-signed fixed Fermi support/boundary/readout map | False | False |
| GATE1209_3_local_GR_R10_pass | local-GR/R10 pass | BLOCKED | 1209 is a source-pack and derivation checkpoint only | False | False |

## Next Target

| next_id | target_file | target_script | task | success_condition | do_not_do | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| NEXT1209_0_1210 | 1210-Y5-R10-first-local-curvature-scale-and-Gres-bracket-smoke.md | scripts/Y5_R10_first_local_curvature_scale_and_Gres_bracket_smoke.py | create a nonclaim feasibility/bracket runner for the clean Fermi projector budget using conservative ranges for L_D, Riemann_norm, C_Fermi, C_P, and G_res_norm, while keeping domain_motion/projector_stress as explicit blockers unless theorem-zero | produce a pressure map showing what C_P*G_res_norm or domain radius would be required, without claiming local-GR/R10 pass | do not use hand-picked optimistic values as evidence, do not hide missing domain/stress terms, do not edit formalization-workbench, do not push GitHub | False | False |

## Validation

| check_id | check | status | details | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- |
| VAL1209_0_sources_exist | all cited local sources exist | PASS | 10/10 sources exist | False | False |
| VAL1209_1_needles_found | all cited source needles found | PASS | 10/10 needles found | False | False |
| VAL1209_2_fermi_law_present | clean Fermi finite-domain law is recorded | PASS | FDL1209_3 present | False | False |
| VAL1209_3_pressure_insert | projector pressure insert is recorded | PASS | FDL1209_4 present | False | False |
| VAL1209_4_domain_audit | domain motion and projector stress are audited | PASS | domain_motion_Linf,domain_motion_Linf,projector_stress_Linf,projector_stress_Linf,epsilon_geom | False | False |
| VAL1209_5_source_pack_complete | unified source pack lists required constants | PASS | D_L,L_D,Riemann_norm,nabla_Riemann_norm,C_Fermi;C_Fermi2,acceleration_norm;rotation_norm,C_P,G_res_norm,domain_motion_Linf,projector_stress_Linf,C_CK | False | False |
| VAL1209_6_pressure_preserved | 1208 projector target is preserved | PASS | target=1.17233215026e-05 | False | False |
| VAL1209_7_blocker_policy | missing source rows block claims | PASS | PSC1209_4 present | False | False |
| VAL1209_8_no_missing_claim_rows | no row with MISSING is valid for claim | PASS | all source pack rows nonclaim | False | False |
| VAL1209_9_nonclaim_policy | all generated rows remain nonclaim | PASS | valid_for_claim=false and claim_allowed=false throughout | False | False |
| VAL1209_10_csv_parse | all generated CSVs parse cleanly | PASS | P8_Y5_R10_1209_SOURCE_REGISTER.csv:10; P8_Y5_R10_1209_FERMI_DOMAIN_DERIVATION.csv:5; P8_Y5_R10_1209_DOMAIN_MOTION_PROJECTOR_STRESS_AUDIT.csv:5; P8_Y5_R10_1209_UNIFIED_SOURCE_PACK.csv:11; P8_Y5_R10_1209_PRESSURE_SMOKE_SCHEMA.csv:5; P8_Y5_R10_1209_DECISION_LEDGER.csv:2; P8_Y5_R10_1209_CLAIM_GATES.csv:4; P8_Y5_R10_1209_NEXT_TARGET.csv:1 | False | False |
| VAL1209_11_formalization_untouched | formalization-workbench untouched during run | PASS | formalization_recent_after_run_start_count=0 | False | False |
| VAL1209_12_next_target | next target is staged | PASS | 1210-Y5-R10-first-local-curvature-scale-and-Gres-bracket-smoke.md | False | False |
| VAL1209_13_overall | overall 1209 validation | PASS | 1209 local Fermi-domain source pack is reproducible and nonclaim | False | False |
