# 1298 Y5 R10 RAB Kmetric-chain to trace-reversed Kbar local projection

Generated: `2026-06-15T14:37:51.428165+00:00`

**Current verdict:** 1298 derives the missing projection formula and catches a serious trap: the Newton bridge needs `Kbar_L,loc,00`, not raw `K^{00}`. In the local flat `(-,+,+,+)` branch, trace reversal gives `Kbar_{00} = 0.5*(K^{00} + K^{11} + K^{22} + K^{33})`.

**Main progress:** the source-normalized Newton budget can now be written as a proper bound form: `epsilon_K <= |c^2|/(4πG rho_ref) * [0.5*(|K_chain^{00}| + sum_i |K_chain^{ii}|) + |Delta_projector_boundary|]`. This is not scoreable yet, but it is the correct target rather than accidentally treating the 00 component as the full source.

**Still blocked:** current runner rows bound only the symbolic `00` channel. The spatial trace kernels, trace/isotropy theorem, projector/domain term, index convention, `rho_ref`, measured-GM calibration, and residual amplitudes remain missing.

## Source Register

| source_id | local_path | needle | exists | needle_found | role | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| SRC1298_0_1297_next | source-intake/mts_residuals/P8_Y5_R10_1297_NEXT_TARGET.csv | NEXT1297_0_1298 | True | True | handoff into Kbar local projection | False | False |
| SRC1298_1_1297_bridge | source-intake/mts_residuals/P8_Y5_R10_1297_SOURCE_NORMALIZATION_BRIDGE_NONCLAIM.csv | Kbar_{mu nu}:=K_{mu nu}-0.5*g_{mu nu}K | True | True | trace-reversed source slot required by the Newton bridge | False | False |
| SRC1298_2_1297_dimensional | source-intake/mts_residuals/P8_Y5_R10_1297_DIMENSIONAL_LEDGER.csv | MISSING_TRACE_REVERSED_PROJECTION | True | True | explicit unresolved projection from Kmetric_chain to Kbar | False | False |
| SRC1298_3_chain_kernel | source-intake/mts_residuals/P8_Y5_R10_1289_FIRST_DERIVATIVE_TERM_ROW_NONCLAIM.csv | Kmetric_chain^{00}=C_sign | True | True | available 00 chain component to project | False | False |
| SRC1298_4_bound_ledger | source-intake/mts_residuals/P8_Y5_R10_1291_CHAIN_KERNEL_RESIDUAL_BOUND_LEDGER.csv | R_chain^{00}=R_m^{00}+R_L^{00}+R_cdb^{00} | True | True | current component residual vector only supplies 00 branch | False | False |
| SRC1298_5_Newton_requirement | source-intake/mts_residuals/P8_Y5_R10_1288_RESPONSE_MATRIX_REQUIREMENTS.csv | MISSING_KBAR_L_LOC_00 | True | True | Newton source row explicitly waits on Kbar_L,loc,00 | False | False |
| SRC1298_6_KL_budget | source-intake/mts_residuals/P8_Y5_R10_796_KL_AMPLITUDE_PPN_BUDGET.csv | K_L can shift weak-field metric coefficients | True | True | trace-reversed projection matters for local metric response | False | False |
| SRC1298_7_metric_response_contract | source-intake/mts_residuals/P8_GK_METRIC_RESPONSE_CONTRACT.csv | K_hat is exactly the metric response of Gamma_eff | True | True | blocks projection claim until Khat/Kmetric and derivative/boundary terms close | False | False |

## Kbar Projection Formula

| projection_id | object | formula | local_flat_signature_branch | source_inputs | derived_status | missing_for_scoring | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| KTP1298_0_trace_reverse_identity | Kbar_{00} | Kbar_{00}=K_{00}-0.5*g_{00}K, with K=g^{alpha beta}K_{alpha beta} | for eta=(-,+,+,+), Kbar_{00}=0.5*(K^{00}+K^{11}+K^{22}+K^{33}) after local index conversion | trace-reversal identity from 1297 source bridge | FORMAL_PROJECTION_IDENTITY_DERIVED_NONCLAIM | MISSING_SPATIAL_TRACE_KII;MISSING_INDEX_CONVENTION_LOCK;MISSING_LOCAL_PROJECTOR_DOMAIN | False | False |
| KTP1298_1_chain_projection | Kbar_L,loc,00 from Kmetric_chain | Kbar_L,loc,00=P_loc[0.5*(K_chain^{00}+sum_i K_chain^{ii})]+Delta_projector_boundary | K_chain^{00}=R_m^{00}+R_L^{00}+R_cdb^{00}; spatial trace needs analogous R_m^{ii}, R_L^{ii}, R_cdb^{ii} | 1289 00 kernel; 1291 residual vector; 1297 Newton source bridge | FORMAL_LOCAL_PROJECTION_FORMULA_DERIVED_NONCLAIM | MISSING_R_m_ii_BOUND;MISSING_R_L_ii_BOUND;MISSING_R_cdb_ii_BOUND;MISSING_PROJECTOR_BOUNDARY_TERM | False | False |
| KTP1298_2_trace_free_shortcut_test | possible Kbar_L,loc,00 shortcut | if parent proves spatial trace sum_i K_chain^{ii}=K_chain^{00} or K trace relation, Kbar_00 may reduce to a multiple of K^{00} | no such trace/isotropy relation is currently sourced | requires parent action or symmetry theorem, not present in 1289/1291 | SHORTCUT_BLOCKED_NO_TRACE_THEOREM | MISSING_TRACE_THEOREM;MISSING_ISOTROPY_OR_TRACEFREE_BRANCH | False | False |

## Spatial Trace Requirements

| requirement_id | component | needed_bound | why_needed | status | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- |
| STR1298_0_m_spatial_trace | sum_i R_m^{ii} | sum_i \|L_cg^-2 F_prime(m) M_m^{ii}\| or parent trace theorem | Kbar_00 includes spatial trace as well as 00 component | MISSING_SPATIAL_M_KERNEL_TRACE | False | False |
| STR1298_1_Lcg_spatial_trace | sum_i R_L^{ii} | sum_i \|2 L_cg^-3 F(m) M_L^{ii}\| or parent trace theorem | L_cg chain can source the spatial trace even if R_L^{00} is bounded | MISSING_SPATIAL_LCG_KERNEL_TRACE | False | False |
| STR1298_2_cdb_spatial_trace | sum_i R_cdb^{ii} | connection/domain/boundary spatial trace or no-flux/improvement theorem | CDB terms can enter Kbar_00 through the trace | MISSING_SPATIAL_CDB_TRACE | False | False |
| STR1298_3_projector_domain | P_loc and Delta_projector_boundary | commutator/domain/boundary term introduced by local projection | local projection may not commute with trace reversal or boundary restriction | MISSING_PROJECTOR_DOMAIN_BOUND | False | False |
| STR1298_4_index_convention | covariant/contravariant 00 and ii conversion | fixed local signature, frame, and index placement | current rows use superscript 00 while Kbar bridge is written with lower-index source slot | MISSING_INDEX_CONVENTION_LOCK | False | False |

## Kbar Bound Preview

| bound_id | bound_formula | known_piece | missing_piece | current_status | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- |
| KBP1298_0_abs_Kbar_bound | \|Kbar_L,loc,00\| <= 0.5*(\|K_chain^{00}\| + sum_i \|K_chain^{ii}\|) + \|Delta_projector_boundary\| | \|K_chain^{00}\| bounded symbolically by KRB1291_0+KRB1291_1+KRB1291_2 | sum_i \|K_chain^{ii}\| and Delta_projector_boundary | BOUND_FORM_DERIVED_BUT_NOT_SCOREABLE | False | False |
| KBP1298_1_Newton_budget_after_projection | epsilon_K <= \|c^2\|/(4*pi*G*rho_ref) * [0.5*(\|K_chain^{00}\|+sum_i\|K_chain^{ii}\|)+\|Delta_projector_boundary\|] | 1297 supplies c^2/(4*pi*G*rho_ref) normalization; 1291 supplies 00 symbolic bounds | rho_ref, measured-GM calibration, spatial trace bounds, residual amplitudes | NEWTON_BUDGET_FORM_DERIVED_BUT_NOT_SCOREABLE | False | False |

## Runner Projection Preview

| preview_id | runner_id | projection_update | new_required_inputs | remaining_old_inputs | score_emitted | runner_status | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| KRP1298_0_m_chain | RRI1292_0_m_chain | 00 component contributes to Kbar but cannot alone define Kbar_00 | MISSING_R_m_ii_BOUND;MISSING_TRACE_REVERSED_PROJECTION;MISSING_PROJECTOR_DOMAIN_BOUND | MISSING_L_cg_VALUE;MISSING_m_PROFILE;MISSING_F_PRIME_BOUND;MISSING_M_m_00_BOUND | False | PROJECTION_PREVIEW_STILL_REJECTED_NONCLAIM_NO_SCORE | False | False |
| KRP1298_1_Lcg_chain | RRI1292_1_Lcg_chain | 00 component contributes to Kbar but spatial Lcg trace is required | MISSING_R_L_ii_BOUND;MISSING_TRACE_REVERSED_PROJECTION;MISSING_PROJECTOR_DOMAIN_BOUND | MISSING_L_cg_VALUE;MISSING_LCG_LOWER_BOUND;MISSING_m_PROFILE;MISSING_F_BOUND;MISSING_M_L_00_BOUND | False | PROJECTION_PREVIEW_STILL_REJECTED_NONCLAIM_NO_SCORE | False | False |
| KRP1298_2_cdb_chain | RRI1292_2_cdb_chain | CDB terms enter both 00 and spatial trace slots | MISSING_R_cdb_ii_BOUND;MISSING_TRACE_REVERSED_PROJECTION;MISSING_PROJECTOR_DOMAIN_BOUND | MISSING_K_CONN_BOUND;MISSING_K_DOMAIN_BOUND;MISSING_K_BOUNDARY_BOUND;MISSING_NO_FLUX_SOURCE | False | PROJECTION_PREVIEW_STILL_REJECTED_NONCLAIM_NO_SCORE | False | False |
| KRP1298_3_chain_vector | RRI1292_3_chain_vector | full vector needs aggregate Kbar projection and observable matrix | MISSING_FULL_KBAR_PROJECTION;MISSING_OBSERVABLE_RESPONSE_MATRIX | MISSING_ALL_COMPONENT_INPUTS;MISSING_LOCAL_RESPONSE_LIMITS | False | PROJECTION_PREVIEW_STILL_REJECTED_NONCLAIM_NO_SCORE | False | False |

## Claim Gates

| gate_id | claim | current_status | reason | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- |
| CG1298_0_projection_formula | formal Kbar_00 projection formula exists | SATISFIED_FOR_NONCLAIM_FORMULA | trace reversal gives Kbar_00=0.5*(K00+Kii) in the local flat signature branch | False | False |
| CG1298_1_Kbar_numeric_bound | Kbar_L,loc,00 bound is scoreable | BLOCKED_SPATIAL_TRACE_MISSING | current runner only has 00 symbolic bounds and no spatial trace kernels/theorem | False | False |
| CG1298_2_Newton_budget | Newton source residual epsilon_K can be evaluated | BLOCKED_RHO_GM_AND_AMPLITUDES_MISSING | Kbar projection, rho_ref, measured-GM calibration, and residual amplitudes are missing | False | False |
| CG1298_3_local_GR | local GR/Newton/PPN recovery pass | BLOCKED_NO_LOCAL_GR_CLAIM | projection formula is necessary but not enough for smallness or silence | False | False |

## Decision Ledger

| decision_id | decision | because | next_action | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- |
| DEC1298_0_trace_reversal_matters | do not identify Kbar_00 with K^{00} | local trace reversal adds the spatial trace term | derive spatial trace kernels or a parent trace/isotropy theorem | False | False |
| DEC1298_1_keep_score_blocked | keep Newton source score blocked | the projection formula introduces new required spatial trace and projector/domain inputs | fill spatial trace requirements before rho/GM scoring | False | False |

## Next Target

| next_id | target_file | target_script | task | success_condition | do_not | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| NEXT1298_0_1299 | 1299-Y5-R10-RAB-spatial-trace-kernel-bound-or-trace-theorem.md | scripts/Y5_R10_RAB_spatial_trace_kernel_bound_or_trace_theorem.py | derive a spatial-trace relation for Kmetric_chain, or acquire nonclaim bounds for R_m^{ii}, R_L^{ii}, and R_cdb^{ii} | either prove a parent trace/isotropy theorem reducing Kbar_00 to known pieces, or produce explicit spatial-trace missing-input rows that keep scoring blocked | do not treat 00 component bounds as Newton source bounds without spatial trace control | False | False |

## Validation

| check_id | check | status | details |
| --- | --- | --- | --- |
| VAL1298_0_sources_exist | registered source paths exist and anchors are found | PASS | 8/8 source anchors found |
| VAL1298_1_projection_formula_present | trace-reversed Kbar projection formula is present | PASS | Kbar_00 local flat branch derived |
| VAL1298_2_spatial_trace_requirements | spatial trace requirements are explicit | PASS | STR1298_0_m_spatial_trace;STR1298_1_Lcg_spatial_trace;STR1298_2_cdb_spatial_trace;STR1298_3_projector_domain;STR1298_4_index_convention |
| VAL1298_3_bound_preview_non_scoreable | Kbar and Newton-budget bounds remain non-scoreable | PASS | KBP1298_0_abs_Kbar_bound;KBP1298_1_Newton_budget_after_projection |
| VAL1298_4_runner_still_no_score | runner preview rows remain no-score | PASS | RRI1292_0_m_chain;RRI1292_1_Lcg_chain;RRI1292_2_cdb_chain;RRI1292_3_chain_vector |
| VAL1298_5_csv_parse | all generated CSVs parse cleanly | PASS | P8_Y5_R10_1298_SOURCE_REGISTER.csv:8; P8_Y5_R10_1298_KBAR_PROJECTION_FORMULA_NONCLAIM.csv:3; P8_Y5_R10_1298_SPATIAL_TRACE_REQUIREMENTS.csv:5; P8_Y5_R10_1298_KBAR_BOUND_PREVIEW_NONCLAIM.csv:2; P8_Y5_R10_1298_RUNNER_PROJECTION_PREVIEW.csv:4; P8_Y5_R10_1298_CLAIM_GATES.csv:4; P8_Y5_R10_1298_DECISION_LEDGER.csv:2; P8_Y5_R10_1298_NEXT_TARGET.csv:1 |
| VAL1298_6_formalization_untouched | formalization-workbench untouched by generated outputs | PASS | formalization_generated_output_count=0 |
| VAL1298_7_nonclaim_policy | all generated rows remain nonclaim | PASS | valid_for_claim=false and claim_allowed=false throughout generated tables |
| VAL1298_8_next_target_1299 | next target routes to spatial trace bound or trace theorem | PASS | 1299-Y5-R10-RAB-spatial-trace-kernel-bound-or-trace-theorem.md |
| VAL1298_9_overall | overall 1298 validation | PASS | 1298 derives the Kbar_00 projection formula, proves the 00 component alone is insufficient, keeps scoring blocked, and routes to spatial-trace bounds/theorem |
