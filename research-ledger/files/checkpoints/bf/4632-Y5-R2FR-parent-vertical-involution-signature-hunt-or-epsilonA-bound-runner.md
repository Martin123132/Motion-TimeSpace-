# 4632 - Parent Vertical Involution Signature Hunt Or EpsilonA Bound Runner

Marker: `PPC4161_PARENT_VERTICAL_INVOLUTION_SIGNATURE_HUNT_OR_EPSILONA_BOUND_RUNNER_4632`

Branch: `MTS_R2FR_Y5_IQ_SIGNATURE_OR_EPSILONA_RUNNER_4632`

Timestamp: `2026-07-06T18:43:58.814414+00:00`

## Result

4632 performs the hard fork after 4631.

The source hunt does **not** find a currently signed full parent `I_q`/even-`A_m` signature. It finds only conditional theorem shapes and prior audits that explicitly keep the full parent action invariance unsigned.

Therefore:

- Exact `beta_visible=0` remains conditional.
- Weak leakage-frame symmetry remains rejected for scalar beta zero.
- The bound route is now executable as a fail-closed `epsilon_A` runner:

`epsilon_A := ||P_vert d ln A_m/dz|0||`

`alpha_AB <= C_N epsilon_A epsilon_B / Z_min`

with the same `lambda_mem=sqrt(Z_mem/M2_mem)` range gate.

The live branch fails closed because `epsilon_A`, `epsilon_B`, `Z_min`, `C_N`, and `lambda_mem` are not yet co-normalized parent-owned numbers.

## Source Register

| checkpoint | source_id | path | path_exists | needle | needle_found | optional | line | role | valid_for_claim | timestamp_utc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4632 | SRC4632_00_4631_next | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4631_NEXT_TARGET.csv | True | 4632-Y5-R2FR-parent-vertical-involution-signature-hunt-or-epsilonA-bound-runner.md | True | False | 2 | 4631 selected 4632 target. | False | 2026-07-06T18:43:58.814414+00:00 |
| 4632 | SRC4632_01_4631_validation | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_BRR545_4631_VALIDATION.csv | True | VAL4631_OVERALL | True | False | 18 | 4631 validation. | False | 2026-07-06T18:43:58.814414+00:00 |
| 4632 | SRC4632_02_4631_strong | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4631_SYMMETRY_ROUTE_AUDIT.csv | True | SYM4631_0_strong_parent_vertical_involution | True | False | 2 | strong I_q route. | False | 2026-07-06T18:43:58.814414+00:00 |
| 4632 | SRC4632_03_4631_weak_reject | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4631_SYMMETRY_ROUTE_AUDIT.csv | True | REJECTED_FOR_BETA_VISIBLE_ZERO | True | False | 4 | weak route rejection. | False | 2026-07-06T18:43:58.814414+00:00 |
| 4632 | SRC4632_04_4631_beta_zero | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4631_BRANCH_EXTREMUM_DERIVATION_ROWS.csv | True | DER4631_1_beta_visible_zero | True | False | 3 | conditional beta zero derivation. | False | 2026-07-06T18:43:58.814414+00:00 |
| 4632 | SRC4632_05_4631_epsilon | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4631_EPSILON_A_COEFFICIENT_FILL_ROWS.csv | True | EPS4631_0_epsilon_A | True | False | 2 | epsilon_A fallback. | False | 2026-07-06T18:43:58.814414+00:00 |
| 4632 | SRC4632_06_4630_local_gr | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4630_CONDITIONAL_LOCAL_GR_THEOREM_ROWS.csv | True | TGR4630_0_conditional_statement | True | False | 2 | local-GR insert target. | False | 2026-07-06T18:43:58.814414+00:00 |
| 4632 | SRC4632_07_4526_hunt | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4526_VERTICAL_INVOLUTION_SOURCE_HUNT.csv | True | HUNT4526_4_parent_action_invariance | True | False | 6 | prior parent action invariance missing. | False | 2026-07-06T18:43:58.814414+00:00 |
| 4632 | SRC4632_08_4526_bridge | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4526_ZL_TO_Z_PARENT_BRIDGE_THEOREM.csv | True | BRG4526_2_scalar_channel_obstruction | True | False | 4 | scalar-channel obstruction. | False | 2026-07-06T18:43:58.814414+00:00 |
| 4632 | SRC4632_09_4526_coeff | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4526_FIRST_SOURCE_NORMALIZED_COEFFICIENT_ROWS.csv | True | COF4526_6_total_symmetry_breaking_bound | True | False | 8 | coefficient fallback envelope. | False | 2026-07-06T18:43:58.814414+00:00 |
| 4632 | SRC4632_10_4525_sig | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4525_PARENT_SIGNATURE_REQUIREMENTS.csv | True | SIG4525_0_vertical_involution | True | False | 2 | full vertical involution requirement. | False | 2026-07-06T18:43:58.814414+00:00 |
| 4632 | SRC4632_11_4195_sig | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4195_PARENT_SIGNATURE_AUDIT.csv | True | SIG4195_0_parent_action | True | False | 2 | leakage parent action invariance missing. | False | 2026-07-06T18:43:58.814414+00:00 |
| 4632 | SRC4632_12_4629_runner | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4629_FIRST_ANCHOR_SMOKE_RUNNER_RESULTS.csv | True | SMK4629_0_current_placeholder | True | False | 2 | current branch fail-closed runner. | False | 2026-07-06T18:43:58.814414+00:00 |
| 4632 | SRC4632_13_1451_req_optional | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1451_EPSILON_A_BOUND_INPUT_REQUIREMENTS.csv | True | epsilon_A | True | True | 2 | older epsilon_A bound input requirements if present. | False | 2026-07-06T18:43:58.814414+00:00 |
| 4632 | SRC4632_14_1451_sign_optional | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1451_SIGNOFF_MATRIX.csv | False | epsilon_A=0 | False | True | 0 | older epsilon_A signoff matrix if present. | False | 2026-07-06T18:43:58.814414+00:00 |

## Iq Signature Hunt

| checkpoint | hunt_id | target_signature | evidence_path | evidence_needle | found_status | effect | valid_for_claim | claim_allowed | timestamp_utc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4632 | HUNT4632_0_full_Iq_action_invariance | S_parent[q,z,Psi]=S_parent[q,-z,Psi] under a full I_q on ker(Dq) | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4525_PARENT_SIGNATURE_REQUIREMENTS.csv | SIG4525_0_vertical_involution | REQUIRED_BUT_NOT_FOUND_IN_PRIOR_SOURCE_AUDIT | cannot promote beta_visible=0 from full parent symmetry | False | False | 2026-07-06T18:43:58.814414+00:00 |
| 4632 | HUNT4632_1_even_matter_scale | A_m(q,z)=A_m(q,-z) or no source-only visible matter scale slot | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4631_BRANCH_EXTREMUM_DERIVATION_ROWS.csv | DER4631_0_even_matter_scale | THEOREM_SHAPE_DERIVED_PARENT_SIGNATURE_MISSING | beta_visible zero remains conditional | False | False | 2026-07-06T18:43:58.814414+00:00 |
| 4632 | HUNT4632_2_leakage_subbundle_bridge | R_L extends to full I_q via z_L=P_L z and q o I_q=q | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4526_ZL_TO_Z_PARENT_BRIDGE_THEOREM.csv | BRG4526_0_embedding | CONDITIONAL_BRIDGE_ONLY | useful route, but not a full scalar/matter proof | False | False | 2026-07-06T18:43:58.814414+00:00 |
| 4632 | HUNT4632_3_weak_symmetry_block | ordinary leakage-frame symmetry kills visible scalar beta | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4526_ZL_TO_Z_PARENT_BRIDGE_THEOREM.csv | BRG4526_2_scalar_channel_obstruction | REJECTED | scalar beta channel must be zeroed by stronger parent signature or bounded | False | False | 2026-07-06T18:43:58.814414+00:00 |
| 4632 | HUNT4632_4_epsilonA_bound_route | co-normalized epsilon_A bound fallback | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4631_EPSILON_A_COEFFICIENT_FILL_ROWS.csv | EPS4631_0_epsilon_A | FALLBACK_READY_NONCLAIM | build bound runner rather than pretending exact local-GR proof exists | False | False | 2026-07-06T18:43:58.814414+00:00 |

## Signature Decision Matrix

| checkpoint | signature_id | needed | current_evidence | signed_now | if_signed | if_unsigned | valid_for_claim | claim_allowed | timestamp_utc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4632 | SIG4632_0_full_Iq | I_q exists on full local vertical kernel with I_q^2=1 and q o I_q=q | only conditional theorem/bridge; prior source audit marks full parent signature not found | False | beta_visible exact-zero route can progress | epsilon_A bound route stays live | False | False | 2026-07-06T18:43:58.814414+00:00 |
| 4632 | SIG4632_1_even_Am | visible matter scale A_m descends as I_q-even or has no vertical source slot | 4631 derives consequence; no parent source signs premise | False | beta_visible=0 follows algebraically | epsilon_A := ||P_vert d ln A_m|| must be bounded | False | False | 2026-07-06T18:43:58.814414+00:00 |
| 4632 | SIG4632_2_positive_gap | Z_mem>0 and M2_mem>0 on same branch | 4628/4630 define ratio and positive branch, numeric parent values missing | False | lambda_mem can be evaluated | range rows remain placeholder | False | False | 2026-07-06T18:43:58.814414+00:00 |
| 4632 | SIG4632_3_source_boundary_silence | explicit EM/hidden/source and boundary channels silent on same branch | prior Poynting/wave/source ledgers keep finite residual branches | False | local-GR theorem can close with exact beta zero | residual vector feeds bound route | False | False | 2026-07-06T18:43:58.814414+00:00 |

## Epsilon-A Bound Inputs

| checkpoint | input_id | symbol | definition | value | units | feeds | valid_for_claim | claim_allowed | timestamp_utc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4632 | IN4632_0_epsilonA | epsilon_A | visible source/test matter-scale vertical derivative norm | MISSING_PARENT_ZERO_OR_NUMERIC_BOUND | dimensionless | alpha_AB <= C_N epsilon_A epsilon_B/Z_min | False | False | 2026-07-06T18:43:58.814414+00:00 |
| 4632 | IN4632_1_epsilonB | epsilon_B | second body/test sensitivity derivative norm | MISSING_PARENT_ZERO_OR_NUMERIC_BOUND | dimensionless | alpha_AB <= C_N epsilon_A epsilon_B/Z_min | False | False | 2026-07-06T18:43:58.814414+00:00 |
| 4632 | IN4632_2_Zmin | Z_min | same-branch lower kinetic Hessian bound | MISSING_ZMEM_PARENT_VALUE | parent normalization | alpha_AB and lambda_mem | False | False | 2026-07-06T18:43:58.814414+00:00 |
| 4632 | IN4632_3_lambda | lambda_mem | same-branch finite range | MISSING_ZMEM_M2MEM_RATIO | m | R10/PPN/orbital range gate | False | False | 2026-07-06T18:43:58.814414+00:00 |
| 4632 | IN4632_4_CN | C_N | Newton/Planck normalization convention for alpha_AB | MISSING_CONVENTION_OR_CALIBRATION | dimensionless after convention | alpha_AB | False | False | 2026-07-06T18:43:58.814414+00:00 |

## Epsilon-A Bound Runner

| checkpoint | run_id | case | epsilon_A | epsilon_B | Z_min | C_N | lambda_mem_m | alpha_AB_bound | lambda_anchor_m | result | reason | valid_for_claim | claim_allowed | timestamp_utc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4632 | RUN4632_0_current_live_branch | current placeholders from 4631/4628/4629 | MISSING_PARENT_ZERO_OR_NUMERIC_BOUND | MISSING_PARENT_ZERO_OR_NUMERIC_BOUND | MISSING_ZMEM_PARENT_VALUE | MISSING_CONVENTION_OR_CALIBRATION | MISSING_ZMEM_M2MEM_RATIO | MISSING | 3.86e-05 | FAIL_CLOSED_MISSING_INPUT | epsilon_A/epsilon_B/Z_min/C_N/lambda_mem are not all numeric and sourced | False | False | 2026-07-06T18:43:58.814414+00:00 |
| 4632 | RUN4632_1_exact_Iq_zero | full I_q-even A_m theorem if parent-signed | 0.0 | 0.0 | any_positive | 1.0 | any_finite | 0.0 | 3.86e-05 | CONDITIONAL_EXACT_ZERO_PASS_ALGEBRA_ONLY | full I_q-even matter descent would make epsilon_A=epsilon_B=0; parent signature is not currently sourced | False | False | 2026-07-06T18:43:58.814414+00:00 |
| 4632 | RUN4632_2_small_epsilon_short_range_control | control: small epsilon and short range | 0.01 | 0.01 | 1.0 | 1.0 | 1.93e-05 | 0.0001 | 3.86e-05 | PASS_ANCHOR_SMOKE_ONLY_NONCLAIM | control branch passes alpha<=1 and lambda<=38.6e-6 m; full curve still required for claim | False | False | 2026-07-06T18:43:58.814414+00:00 |
| 4632 | RUN4632_3_order_one_epsilon_short_range_control | control: order-one epsilon even at short range | 1.0 | 1.0 | 0.5 | 1.0 | 1.93e-05 | 2.0 | 3.86e-05 | FAIL_ALPHA_ABOVE_ANCHOR | co-normalized alpha_AB exceeds alpha=1 anchor threshold | False | False | 2026-07-06T18:43:58.814414+00:00 |
| 4632 | RUN4632_4_small_epsilon_long_range_control | control: small epsilon but long range | 0.01 | 0.01 | 1.0 | 1.0 | 7.72e-05 | 0.0001 | 3.86e-05 | FAIL_RANGE_ABOVE_ANCHOR | lambda_mem exceeds conservative alpha=1 anchor range | False | False | 2026-07-06T18:43:58.814414+00:00 |

## Controls

| checkpoint | control_id | rule | violation_blocks_claim | timestamp_utc |
| --- | --- | --- | --- | --- |
| 4632 | CTL4632_0_no_signature_no_zero | Do not set epsilon_A=0 unless full I_q/even-A_m or no-source-slot signature is parent-signed. | True | 2026-07-06T18:43:58.814414+00:00 |
| 4632 | CTL4632_1_no_bound_without_convention | Do not score alpha_AB until epsilon_A, epsilon_B, Z_min, C_N and lambda_mem are co-normalized. | True | 2026-07-06T18:43:58.814414+00:00 |
| 4632 | CTL4632_2_anchor_not_full_curve | An alpha=1 short-range pass is smoke only; full R10 alpha(lambda) curve is still required. | True | 2026-07-06T18:43:58.814414+00:00 |

## Blockers

| checkpoint | blocker_id | blocks | missing | next_action | valid_for_claim | timestamp_utc |
| --- | --- | --- | --- | --- | --- | --- |
| 4632 | BLK4632_0_Iq_signature | exact beta_visible zero | full parent I_q action/measure/projector/boundary and even-A_m descent | 4633-Y5-R2FR-epsilonA-bound-input-acquisition-or-no-source-slot-bridge.md | False | 2026-07-06T18:43:58.814414+00:00 |
| 4632 | BLK4632_1_epsilon_numeric | bound runner live evaluation | epsilon_A/epsilon_B numeric values or theorem-zero, Z_min, C_N, lambda_mem | 4633-Y5-R2FR-epsilonA-bound-input-acquisition-or-no-source-slot-bridge.md | False | 2026-07-06T18:43:58.814414+00:00 |
| 4632 | BLK4632_2_bound_curve | R10/local-G claim | full source-backed alpha(lambda) curve beyond anchor smoke | after parent coefficients exist | False | 2026-07-06T18:43:58.814414+00:00 |

## Promotion Gates

| checkpoint | gate_id | promotion_condition | current_result | valid_for_claim | claim_allowed | timestamp_utc |
| --- | --- | --- | --- | --- | --- | --- |
| 4632 | PROM4632_0_exact_zero | Full parent I_q/even-A_m signature is found and paired with positive gap/source-boundary silence. | blocked signature not sourced | False | False | 2026-07-06T18:43:58.814414+00:00 |
| 4632 | PROM4632_1_epsilon_bound | epsilon_A, epsilon_B, Z_min, C_N and lambda_mem become parent-owned numeric/source-backed rows and pass bound runners. | blocked numeric inputs missing | False | False | 2026-07-06T18:43:58.814414+00:00 |

## Decision

| checkpoint | decision_id | decision | meaning | status | best_route | next_target | valid_for_claim | claim_allowed | timestamp_utc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4632 | DEC4632_0 | FULL_IQ_SIGNATURE_NOT_SOURCED_EPSILONA_BOUND_RUNNER_READY_NONCLAIM | The current corpus does not source the full parent I_q/even-A_m signature. The branch therefore keeps the exact-zero route conditional and activates the epsilon_A co-normalized bound runner, which fails the live branch closed but distinguishes control pass/fail cases. | NONCLAIM_SIGNATURE_HUNT_AND_RUNNER_ADVANCE | bridge no-source-slot/common-measure work into even-A_m or fill epsilon_A bound inputs | 4633-Y5-R2FR-epsilonA-bound-input-acquisition-or-no-source-slot-bridge.md | False | False | 2026-07-06T18:43:58.814414+00:00 |

## Next Target

`4633-Y5-R2FR-epsilonA-bound-input-acquisition-or-no-source-slot-bridge.md`
