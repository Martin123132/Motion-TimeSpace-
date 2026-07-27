# 2825 - Y5 R2FR Eq Control Only Local Lock Smoke Runner And Source Input Schema Under AX1090

Status: `Y5_R2FR_2825_control_only_local_lock_smoke_runner_schema_nonclaim`

## Private Verdict

2825 builds the runner skeleton, not a physics result.

The conditional `E_q` carrier is retained only as a control coordinate:

`E_q[delta q]^2 = int_W (Z_q |nabla delta q|^2 + M_q^2 delta q^2) dV_e`

with `M_q^2=n_q^A H_AB n_q^B`, `Z_q=xi_q^2 M_q^2`, and `lambda_q=xi_q` still requiring parent-signed sources.

The runner now exposes the missing couplings and local-lock dependencies in a machine-readable way. It refuses all numeric prediction rows because `H_AB`, `xi_q`, `q` normalization, selector, boundary/domain, `J_q` component bounds, `Dq[v_m]`, `C_qm`, and worldtube/local constants remain placeholders.

So the gain is discipline: we can see what must be sourced or theorem-zeroed before local GR/Newton/PPN/R10 claims can even start.

## Source Register

| source_id | role | path_exists | anchors_found | missing_anchors | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| SRC2825_0_2824_next | 2824 handoff selecting the control-only local-lock smoke runner | True | True |  | False |
| SRC2825_1_2824_decision | E_q demotion and control-runner decision | True | True |  | False |
| SRC2825_2_2824_demotion | control-only carrier and no local-lock reentry | True | True |  | False |
| SRC2825_3_2824_runner | runner contract and promotion acceptance rule | True | True |  | False |
| SRC2825_4_2824_extraction | missing source-backed H_AB and final no-extraction verdict | True | True |  | False |
| SRC2825_5_2824_gates | nonclaim demotion and local claim block | True | True |  | False |
| SRC2825_6_2823_conditional | conditional covariance-Hessian E_q carrier | True | True |  | False |
| SRC2825_7_2823_impact | component row reentry remains blocked | True | True |  | False |
| SRC2825_8_2823_units | q units and Newton-source normalization debt | True | True |  | False |
| SRC2825_9_2822_jq_first | first same-norm J_q component row | True | True |  | False |
| SRC2825_10_2822_jq_fallback | component fallback vector for source norm | True | True |  | False |
| SRC2825_11_2818_amplitude | local-lock amplitude law and K_alg chain insert | True | True |  | False |
| SRC2825_12_2818_chain | N_lock chain update and q-norm blocker | True | True |  | False |
| SRC2825_13_2818_interface | first N_lock input interface | True | True |  | False |

## Control Input Schema

| schema_id | input_group | input_name | current_status | promotion_requirement | source_backed | numeric_value_present | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| SCH2825_0_HAB | carrier | H_AB_shape | MISSING_SOURCE_BACKED_H_AB | source-backed effective action Hessian, q-lift, units, background, density convention | False | False | False |
| SCH2825_1_Mq2 | carrier | M_q^2 | MISSING_SOURCE_BACKED_Mq2 | M_q^2=n_q^A H_AB n_q^B in one parent normalization | False | False | False |
| SCH2825_2_Zq | carrier | Z_q | MISSING_SOURCE_BACKED_Zq | Z_q=xi_q^2 M_q^2 with sourced xi_q | False | False | False |
| SCH2825_3_xiq | carrier | xi_q | MISSING_SOURCE_BACKED_XI_Q | source-backed numeric or theorem-fixed scale | False | False | False |
| SCH2825_4_lambda | carrier | lambda_q | MISSING_SOURCE_BACKED_LAMBDA_Q | lambda_q=sqrt(Z_q/M_q^2)=xi_q after source promotion | False | False | False |
| SCH2825_5_qunits | normalization | q_units_flag | MISSING_Q_UNITS_NORMALIZATION | same q normalization across E_q, J_q, Dq[v_m], and arenas | False | False | False |
| SCH2825_6_selector | normalization | selector_flag | MISSING_PARENT_SELECTOR | parent-signed selector or theorem-zero condition | False | False | False |
| SCH2825_7_boundary | normalization | boundary_flag | MISSING_BOUNDARY_DOMAIN_CERTIFICATE | parent-signed boundary/domain certificate | False | False | False |
| SCH2825_8_jmatter | source_vector | B_matter^q | MISSING_JQ_MATTER_COMPONENT | same E_q dual norm and source-backed or theorem-zero component | False | False | False |
| SCH2825_9_jconst | source_vector | B_const^q | MISSING_JQ_CONST_COMPONENT | same E_q dual norm and source-backed or theorem-zero component | False | False | False |
| SCH2825_10_jweight | source_vector | B_weight^q | MISSING_JQ_WEIGHT_COMPONENT | same E_q dual norm and source-backed or theorem-zero component | False | False | False |
| SCH2825_11_jshadow | source_vector | B_shadow^q | MISSING_JQ_SHADOW_COMPONENT | same E_q dual norm and source-backed or theorem-zero component | False | False | False |
| SCH2825_12_jreadout | source_vector | B_readout^q | MISSING_JQ_READOUT_COMPONENT | same E_q dual norm and source-backed or theorem-zero component | False | False | False |
| SCH2825_13_jboundary | source_vector | B_boundary^q | MISSING_JQ_BOUNDARY_COMPONENT | same E_q dual norm and source-backed or theorem-zero component | False | False | False |
| SCH2825_14_jcurvature | source_vector | B_curvature^q | MISSING_JQ_CURVATURE_COMPONENT | same E_q dual norm and source-backed or theorem-zero component | False | False | False |
| SCH2825_15_Btotal | source_vector | B_total^q | MISSING_TOTAL_JQ_BOUND | sum_i B_i^q in one E_q dual norm | False | False | False |
| SCH2825_16_Cqm | response | C_qm | MISSING_C_QM_RESPONSE | parent-signed Dq[v_m] coupling and bounded inverse | False | False | False |
| SCH2825_17_Dqvm | response | Dq[v_m] | MISSING_DQ_VERTICAL_GENERATOR | actual vertical generator, not a placeholder component | False | False | False |
| SCH2825_18_UB | local_lock | U_B_max | MISSING_WORLD_TUBE_CONSTANT | sourced worldtube/profile normalization | False | False | False |
| SCH2825_19_Cinner | local_lock | C_inner | MISSING_INNER_CHARGE_CONSTANT | source-backed inner charge norm | False | False | False |
| SCH2825_20_QmH | local_lock | Q_m^H | MISSING_HORIZONTAL_CHARGE | source-backed charge or theorem-zero | False | False | False |
| SCH2825_21_Ndomain | local_lock | N_inner_domain | MISSING_DOMAIN_LEAKAGE | source-backed domain term or theorem-zero | False | False | False |
| SCH2825_22_Nzero | local_lock | N_inner_zero_mode | MISSING_ZERO_MODE_LEAKAGE | source-backed zero-mode term or theorem-zero | False | False | False |
| SCH2825_23_Nrest | local_lock | N_rest | MISSING_REST_LEAKAGE | source-backed remainder bound | False | False | False |
| SCH2825_24_Cemb | local_lock | C_emb | MISSING_EMBEDDING_CONSTANT | source-backed embedding estimate | False | False | False |
| SCH2825_25_F2 | local_lock | F2_bar | MISSING_F2_BAR | parent-signed second derivative coefficient | False | False | False |
| SCH2825_26_Lmin | local_lock | L_min | MISSING_L_MIN | source-backed or derived local scale | False | False | False |
| SCH2825_27_Mm | local_lock | M_m_bar | MISSING_M_M_BAR | source-backed local matter envelope | False | False | False |
| SCH2825_28_ML | local_lock | M_L_bar | MISSING_M_L_BAR | source-backed length-gradient envelope | False | False | False |

## Placeholder Input Rows

| placeholder_id | input_group | input_name | value_token | units | source_backed | numeric_value_present | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| PH2825_0_HAB | carrier | H_AB_shape | MISSING_SOURCE_BACKED_H_AB | MISSING_UNITS_UNTIL_SOURCE_BACKED | False | False | False |
| PH2825_1_Mq2 | carrier | M_q^2 | MISSING_SOURCE_BACKED_Mq2 | MISSING_UNITS_UNTIL_SOURCE_BACKED | False | False | False |
| PH2825_2_Zq | carrier | Z_q | MISSING_SOURCE_BACKED_Zq | MISSING_UNITS_UNTIL_SOURCE_BACKED | False | False | False |
| PH2825_3_xiq | carrier | xi_q | MISSING_SOURCE_BACKED_XI_Q | MISSING_UNITS_UNTIL_SOURCE_BACKED | False | False | False |
| PH2825_4_lambda | carrier | lambda_q | MISSING_SOURCE_BACKED_LAMBDA_Q | MISSING_UNITS_UNTIL_SOURCE_BACKED | False | False | False |
| PH2825_5_qunits | normalization | q_units_flag | MISSING_Q_UNITS_NORMALIZATION | MISSING_UNITS_UNTIL_SOURCE_BACKED | False | False | False |
| PH2825_6_selector | normalization | selector_flag | MISSING_PARENT_SELECTOR | MISSING_UNITS_UNTIL_SOURCE_BACKED | False | False | False |
| PH2825_7_boundary | normalization | boundary_flag | MISSING_BOUNDARY_DOMAIN_CERTIFICATE | MISSING_UNITS_UNTIL_SOURCE_BACKED | False | False | False |
| PH2825_8_jmatter | source_vector | B_matter^q | MISSING_JQ_MATTER_COMPONENT | MISSING_UNITS_UNTIL_SOURCE_BACKED | False | False | False |
| PH2825_9_jconst | source_vector | B_const^q | MISSING_JQ_CONST_COMPONENT | MISSING_UNITS_UNTIL_SOURCE_BACKED | False | False | False |
| PH2825_10_jweight | source_vector | B_weight^q | MISSING_JQ_WEIGHT_COMPONENT | MISSING_UNITS_UNTIL_SOURCE_BACKED | False | False | False |
| PH2825_11_jshadow | source_vector | B_shadow^q | MISSING_JQ_SHADOW_COMPONENT | MISSING_UNITS_UNTIL_SOURCE_BACKED | False | False | False |
| PH2825_12_jreadout | source_vector | B_readout^q | MISSING_JQ_READOUT_COMPONENT | MISSING_UNITS_UNTIL_SOURCE_BACKED | False | False | False |
| PH2825_13_jboundary | source_vector | B_boundary^q | MISSING_JQ_BOUNDARY_COMPONENT | MISSING_UNITS_UNTIL_SOURCE_BACKED | False | False | False |
| PH2825_14_jcurvature | source_vector | B_curvature^q | MISSING_JQ_CURVATURE_COMPONENT | MISSING_UNITS_UNTIL_SOURCE_BACKED | False | False | False |
| PH2825_15_Btotal | source_vector | B_total^q | MISSING_TOTAL_JQ_BOUND | MISSING_UNITS_UNTIL_SOURCE_BACKED | False | False | False |
| PH2825_16_Cqm | response | C_qm | MISSING_C_QM_RESPONSE | MISSING_UNITS_UNTIL_SOURCE_BACKED | False | False | False |
| PH2825_17_Dqvm | response | Dq[v_m] | MISSING_DQ_VERTICAL_GENERATOR | MISSING_UNITS_UNTIL_SOURCE_BACKED | False | False | False |
| PH2825_18_UB | local_lock | U_B_max | MISSING_WORLD_TUBE_CONSTANT | MISSING_UNITS_UNTIL_SOURCE_BACKED | False | False | False |
| PH2825_19_Cinner | local_lock | C_inner | MISSING_INNER_CHARGE_CONSTANT | MISSING_UNITS_UNTIL_SOURCE_BACKED | False | False | False |
| PH2825_20_QmH | local_lock | Q_m^H | MISSING_HORIZONTAL_CHARGE | MISSING_UNITS_UNTIL_SOURCE_BACKED | False | False | False |
| PH2825_21_Ndomain | local_lock | N_inner_domain | MISSING_DOMAIN_LEAKAGE | MISSING_UNITS_UNTIL_SOURCE_BACKED | False | False | False |
| PH2825_22_Nzero | local_lock | N_inner_zero_mode | MISSING_ZERO_MODE_LEAKAGE | MISSING_UNITS_UNTIL_SOURCE_BACKED | False | False | False |
| PH2825_23_Nrest | local_lock | N_rest | MISSING_REST_LEAKAGE | MISSING_UNITS_UNTIL_SOURCE_BACKED | False | False | False |
| PH2825_24_Cemb | local_lock | C_emb | MISSING_EMBEDDING_CONSTANT | MISSING_UNITS_UNTIL_SOURCE_BACKED | False | False | False |
| PH2825_25_F2 | local_lock | F2_bar | MISSING_F2_BAR | MISSING_UNITS_UNTIL_SOURCE_BACKED | False | False | False |
| PH2825_26_Lmin | local_lock | L_min | MISSING_L_MIN | MISSING_UNITS_UNTIL_SOURCE_BACKED | False | False | False |
| PH2825_27_Mm | local_lock | M_m_bar | MISSING_M_M_BAR | MISSING_UNITS_UNTIL_SOURCE_BACKED | False | False | False |
| PH2825_28_ML | local_lock | M_L_bar | MISSING_M_L_BAR | MISSING_UNITS_UNTIL_SOURCE_BACKED | False | False | False |

## Local Lock Control Formulas

| formula_id | formula_group | formula | role | control_only | prediction_allowed | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| FORM2825_0_Mq2 | carrier | M_q^2 = n_q^A H_AB n_q^B | conditional covariance-Hessian mass term | True | False | False |
| FORM2825_1_Zq | carrier | Z_q = xi_q^2 M_q^2 | conditional stiffness from sourced xi_q and M_q | True | False | False |
| FORM2825_2_lambda | carrier | lambda_q = sqrt(Z_q/M_q^2) = xi_q | conditional range relation | True | False | False |
| FORM2825_3_Btotal | source_vector | B_total^q = sum_i B_i^q | component-source bookkeeping only | True | False | False |
| FORM2825_4_Tsource | source_vector | T_source_norm_control <= B_total^q | control upper-bound placeholder | True | False | False |
| FORM2825_5_Scg | response | S_cg,total_control <= 1/2 T_source_norm_control C_qm + S_direct + S_boundary + S_extra | control coupling sensitivity placeholder | True | False | False |
| FORM2825_6_Nsrc | local_lock | N_src_control <= U_B,max S_cg,total_control | local source transfer control formula | True | False | False |
| FORM2825_7_Npair | local_lock | N_pair_control <= N_src_control + C_inner \|Q_m^H\| + N_inner_domain + N_inner_zero | first-pair local-lock interface | True | False | False |
| FORM2825_8_Nlock | local_lock | N_lock_control <= N_pair_control + N_rest | finite leakage control version | True | False | False |
| FORM2825_9_Delta | local_lock | Delta_m_control <= C_emb N_lock_control | local extremum/amplitude law control form | True | False | False |
| FORM2825_10_Kalg | local_lock | \|\|K_alg\|\|_D <= L_min^-2 F2_bar C_emb N_lock M_m_bar + L_min^-3 F2_bar C_emb^2 N_lock^2 M_L_bar + higher-order terms | local transition residual control chain | True | False | False |

## Dry Run Results

| dryrun_id | object | result | dryrun_passed | numeric_evaluation_performed | prediction_emitted | refused_prediction | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| DRY2825_0_schema_parse | schema parse | PASS_CONTROL_SCHEMA | True | False | False | True | False |
| DRY2825_1_numeric_eval | numeric evaluation | REFUSED_PLACEHOLDERS_MISSING | True | False | False | True | False |
| DRY2825_2_claim_status | claim status | BLOCKED_NO_CLAIM | True | False | False | True | False |
| DRY2825_3_sensitivity_use | sensitivity use | CONTROL_ONLY | True | False | False | True | False |
| DRY2825_4_required_inputs | promotion dependency list | H_AB_shape;M_q^2;Z_q;xi_q;lambda_q;q_units_flag;selector_flag;boundary_flag;B_matter^q;B_const^q;B_weight^q;B_shadow^q;B_readout^q;B_boundary^q;B_curvature^q;B_total^q;C_qm;Dq[v_m];U_B_max;C_inner;Q_m^H;N_inner_domain;N_inner_zero_mode;N_rest;C_emb;F2_bar;L_min;M_m_bar;M_L_bar | True | False | False | True | False |

## Promotion Requirements

| promotion_id | requirement | input_group | acceptance_condition | satisfied | promotion_allowed | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| PROM2825_0_HAB | H_AB effective action/lift/unit source | carrier | source-backed H_AB in the same parent branch as q | False | False | False |
| PROM2825_1_xiq | xi_q smoothing/correlation scale | carrier | numeric or theorem-fixed xi_q with units | False | False | False |
| PROM2825_2_selector | q=0 selector | normalization | parent-signed local branch selector or theorem-zero closure | False | False | False |
| PROM2825_3_qunits | q units/normalization | normalization | same q normalization in E_q, J_q, Dq[v_m], and arena projections | False | False | False |
| PROM2825_4_boundary | boundary/domain class | normalization | signed boundary/corner/cohomology/kernel certificate | False | False | False |
| PROM2825_5_newton | Newton/source normalization | normalization | source-measure equality and universal G bridge | False | False | False |
| PROM2825_6_Jq | J_q components | source_vector | every component source-backed or theorem-zero in E_q dual norm | False | False | False |
| PROM2825_7_Dqvm | Dq[v_m] and C_qm | response | actual vertical generator and q-to-m response constant | False | False | False |
| PROM2825_8_worldtube | worldtube/profile constants | local_lock | U_B,max, C_inner, Q_m^H, domain/zero/rest terms sourced | False | False | False |
| PROM2825_9_arena | arena projection kernels | empirical | R10/PPN/clock/orbital projection maps in the same normalization | False | False | False |
| PROM2825_10_norm_coherence | no mixed norm | global | one E_q/E_q* normalization through carrier, source, and local lock | False | False | False |
| PROM2825_11_no_claim | claim gate | global | no prediction row until all above pass | False | False | False |

## Claim Gates

| claim_gate_id | claim | gate_passed | status | reason | claim_allowed |
| --- | --- | --- | --- | --- | --- |
| CG2825_0_sources | source anchors present | True | PASS_NONCLAIM | imported ledgers are reproducible | False |
| CG2825_1_schema | control input schema parses | True | PASS_NONCLAIM | all schema rows cite an existing source anchor | False |
| CG2825_2_placeholders | all placeholder rows are nonclaim | True | PASS_NONCLAIM | all values are missing tokens with no numeric/source-backed status | False |
| CG2825_3_formulas | control formulas parse | True | PASS_NONCLAIM | formula rows are bookkeeping only and cannot emit predictions | False |
| CG2825_4_dryrun | dry-run refusal works | True | PASS_NONCLAIM | numeric prediction is refused until source inputs exist | False |
| CG2825_5_promotion | promotion remains blocked | True | PASS_NONCLAIM | promotion needs source-backed or theorem-zero carrier/source/response/local inputs | False |
| CG2825_6_GR_Newton | local GR/Newton claim allowed | False | BLOCKED | q=0 selector, Newton source normalization, and Dq[v_m] remain missing | False |
| CG2825_7_PPN_R10 | PPN/R10/clock/orbital claim allowed | False | BLOCKED | arena projection and local source vector are not source-backed | False |

## Decision Ledger

| decision_id | decision | result | because | next_action | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| DEC2825_0_runner | Control-only runner/schema was built. | PASS_NONCLAIM_SKELETON | the carrier/source/local-lock chain is now machine-readable without emitting a physics prediction | use it only to expose dependencies | False |
| DEC2825_1_no_claim | No local claim is promoted. | BLOCKED_AS_DESIGNED | every numeric/source-backed input is still missing or theorem-unsigned | do not feed results into R10/PPN/clock/orbital score rows | False |
| DEC2825_2_best_gain | The useful gain is now dependency discipline. | INPUT_PRIORITY_VISIBLE | H_AB, xi_q, selector, boundary/domain, J_q components, and Dq[v_m] are explicit promotion gates | rank the missing inputs before another derivation hunt | False |
| DEC2825_3_next | Next target is a promotion-input priority map. | NEXT_2826_PRIORITY_MAP | we should choose the least-scrutinized route for source/theorem closure instead of circling the same branch blindly | build a ranked input-priority ledger and first-fill plan | False |

## Next Target

| next_id | status | target_doc | target_script | mission | selected | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| NEXT2825_0_2826 | selected_primary | 2826-Y5-R2FR-control-runner-promotion-input-priority-map-under-AX1090.md | scripts/Y5_R2FR_control_runner_promotion_input_priority_map_under_AX1090_2826.py | rank the minimum missing source/theorem inputs needed to promote the 2825 control runner, separating derivation targets from empirical/source-bound targets without inserting fake numeric values | True | False |

## Branch Copies

| copy_id | source_table | copy_path | purpose | exists | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| BR2825_0_schema_copy | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_2825_PLACEHOLDER_INPUT_ROWS_NONCLAIM.csv | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\source-weight\Eq_control_only_local_lock_smoke_inputs_2825_NONCLAIM.csv | source-weight copy of control-only smoke input placeholders | True | False |
| BR2825_1_dryrun_copy | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_2825_DRYRUN_RESULTS_NONCLAIM.csv | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\local_bounds\Eq_control_only_local_lock_smoke_results_2825_NONCLAIM.csv | local-bounds copy of refused dry-run results | True | False |
| BR2825_2_next_queue | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_2825_NEXT_TARGET.csv | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\rab-sector\acquisition-queue\JR2825_CONTROL_RUNNER_PROMOTION_INPUT_PRIORITY_NEXT.csv | RAB acquisition queue for promotion-input priority map | True | False |

## Validation

| validation_id | passed | detail | timestamp_utc |
| --- | --- | --- | --- |
| VAL2825_0_sources_exist | True | all source-register local paths exist | 2026-06-24T04:31:42.416147+00:00 |
| VAL2825_1_source_anchors | True | all source-register anchors were found | 2026-06-24T04:31:42.416159+00:00 |
| VAL2825_2_schema_anchors | True | all control schema source anchors were found | 2026-06-24T04:31:42.416163+00:00 |
| VAL2825_3_placeholder_nonclaim | True | all placeholders are explicitly nonclaim | 2026-06-24T04:31:42.416165+00:00 |
| VAL2825_4_no_numeric_values | True | no placeholder has numeric/source-backed status | 2026-06-24T04:31:42.416168+00:00 |
| VAL2825_5_missing_tokens | True | all placeholder values are missing-token rows | 2026-06-24T04:31:42.416170+00:00 |
| VAL2825_6_formula_nonprediction | True | all formulas are nonprediction control formulas | 2026-06-24T04:31:42.416173+00:00 |
| VAL2825_7_dryrun_refused | True | dry-run refuses numeric prediction | 2026-06-24T04:31:42.416176+00:00 |
| VAL2825_8_promotion_blocked | True | promotion requirements remain unsatisfied | 2026-06-24T04:31:42.416178+00:00 |
| VAL2825_9_claims_blocked | True | no claim gate allows GR/Newton/PPN/R10 | 2026-06-24T04:31:42.416181+00:00 |
| VAL2825_10_next_target_2826 | True | promotion-input priority map selected next | 2026-06-24T04:31:42.416183+00:00 |
| VAL2825_11_branch_outputs_exist | True | branch copies were written | 2026-06-24T04:31:42.416185+00:00 |
| VAL2825_12_outputs_exist | True | all generated output paths exist before validation write | 2026-06-24T04:31:42.416188+00:00 |
| VAL2825_13_csv_parse | True | all generated CSV outputs parse | 2026-06-24T04:31:42.416190+00:00 |
| VAL2825_14_cited_paths_exist | True | all cited local file/copy paths in generated rows exist | 2026-06-24T04:31:42.416192+00:00 |
| VAL2825_15_no_claim_flags | True | no score_ready, valid_prediction_row, valid_for_claim, or claim_allowed flag is true | 2026-06-24T04:31:42.416194+00:00 |
| VAL2825_16_generated_under_post_checkpoint | True | all generated artifacts remain under post-checkpoint-work | 2026-06-24T04:31:42.416197+00:00 |
| VAL2825_17_formalization_untouched | True | formalization-workbench was not modified during this run | 2026-06-24T04:31:42.416199+00:00 |
| VAL2825_18_pycache_absent | True | scripts __pycache__ absent during validation | 2026-06-24T04:31:42.416201+00:00 |
| VAL2825_OVERALL | True | 2825 builds a machine-readable nonclaim control-only local-lock smoke runner/schema, refuses numeric predictions because every promotion input is missing/source-unsigned, and selects a priority-map target next. | 2026-06-24T04:31:42.416204+00:00 |
