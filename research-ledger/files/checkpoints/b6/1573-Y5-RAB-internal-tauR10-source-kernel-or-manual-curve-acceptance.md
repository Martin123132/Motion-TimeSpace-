# 1573 - R_AB Internal tau_R10 Source Kernel Or Manual Curve Acceptance

## Verdict
- The derivation-first route made real progress: the finite `R_AB` residual now has a conditional source-normalized Yukawa kernel law.
- The clean bridge is `alpha_MTS(lambda_R)=Xi_R10[beta_S^R beta_T^R/(4 pi G Z_R)+alpha_boundary_tail]` with `lambda_R=sqrt(Z_R/M_R^2)`.
- This is not a numeric prediction: `Z_R`, `M_R^2`, `beta_S^R`, `beta_T^R`, `Xi_R10`, and boundary/readout tails are still missing or unsigned.
- The zero route is also not closed: constraint, matter-source silence, boundary silence, and cross-arena tau transfer all remain conditional or forbidden.
- No R10 score, local GR/Newton reduction, PPN, WEP, clock, orbital, `Z_R=0`, `tau_R10=0`, or `q_R=0` claim is made.

## Source Register

| source_id | source_path | exists | needle_found | needles |
| --- | --- | --- | --- | --- |
| SRC1573_0_1572_doc | 1572-Y5-RAB-tauR10-source-normalization-or-accepted-curve-QA.md | True | True | internal `tau_R10` source-normalization kernel remains the hard blocker; NEXT_1573_INTERNAL_TAU_R10_SOURCE_KERNEL_OR_MANUAL_CURVE_ACCEPTANCE |
| SRC1573_1_1572_validation | source-intake/mts_residuals/P8_Y5_BRR545_1572_VALIDATION.csv | True | True | VAL1572_OVERALL; PASS |
| SRC1573_2_1572_tau | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1572_TAU_R10_SOURCE_NORMALIZATION_DERIVATION_ATTEMPT.csv | True | True | TAUN1572_4_verdict; NOT_READY |
| SRC1573_3_1572_acceptance | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1572_CURVE_ACCEPTANCE_GATE.csv | True | True | ACCEPT1572_3_curve_status; NOT_ACCEPTED |
| SRC1573_4_04_action_contract | 04-vacuum-reciprocity-action-contract.md | True | True | d/dr [ W(r,L,fields) dR_AB/dr ] = J_R; J_R = 0 in local vacuum |
| SRC1573_5_05_theorem_attempt | 05-reciprocity-theorem-attempt.md | True | True | S_R = integral dr [0.5 W(r) (R_AB')^2 + J_R R_AB].; Q_R = integral J_R dr = 0 |
| SRC1573_6_07_constraint_route | 07-nonpropagating-reciprocity-constraint.md | True | True | S_constraint = integral lambda_R R_AB.; R_AB = 0. |
| SRC1573_7_1483_tau_lock | source-intake/mts_residuals/P8_Y5_R10_1483_SYMBOLIC_TAU_FUNCTIONAL_LOCK.csv | True | True | TAULOCK1483_6_output; tau_eff_X; forbidden_shortcuts |
| SRC1573_8_1402_transfer | source-intake/mts_residuals/P8_Y5_R10_1402_SHARED_TAU_TRANSFER_THEOREM_AUDIT.csv | True | True | DTT1402_3_tau_R10_kernel_owner; Z_shared_tau_domain=false |
| SRC1573_9_1519_coframe_tau | source-intake/mts_residuals/P8_Y5_PARENT_FRAME_1519_COFRAME_TAU_LOCK_AUDIT.csv | True | True | OCF1519_4_tau_lock; MISSING_TAU_LOCK |
| SRC1573_10_1322_clock_readout | source-intake/mts_residuals/P8_Y5_R10_1322_TAU_READOUT_DERIVATION_ATTEMPT.csv | True | True | TAU1322_3_local_silence; CONDITIONAL_ONLY_NOT_ACTIVE |

## Kernel Derivation Contract

| derivation_id | statement | equation | status | blocking_gap |
| --- | --- | --- | --- | --- |
| KDER1573_0_parent_quadratic_block | Use a local scalar reciprocity residual R=R_AB with quadratic parent block. | S_R = integral sqrt(-g)[-1/2 Z_R (nabla R)^2 -1/2 M_R^2 R^2 + R J_R] + S_boundary | FORMAL_CONTRACT_WRITTEN | Z_R, M_R^2, J_R and boundary term are not source-backed in one parent normalization |
| KDER1573_1_eom | Variation gives the finite-range reciprocity equation when Z_R and M_R^2 are nonzero. | Z_R Box R - M_R^2 R = -J_R plus boundary/corner readout terms | FORMAL_RANGE_LAW_DERIVED_CONDITIONAL | positive same-frame Z_R and M_R^2 are missing |
| KDER1573_2_source_charge | Matter coupling must define source-normalized charges, not guessed tau=1. | beta_i^R := partial ln m_i / partial R_AB,  J_R(x)=sum_i beta_i^R m_i delta_3(x-x_i)/sqrt(g_3) | FORMAL_SOURCE_CHARGE_LAW_DERIVED_CONDITIONAL | beta_S^R and beta_T^R are not parent-signed or numerically sourced |
| KDER1573_3_green_function | The static Green function maps a point source into a Yukawa profile. | R(r)=-(beta_S^R m_S)/(4 pi Z_R) exp(-r/lambda_R)/r, ignoring unsigned boundary tails | FORMAL_YUKAWA_PROFILE_DERIVED_CONDITIONAL | boundary/tail/readout silence is not signed |
| KDER1573_4_alpha_match | Matching delta V_R to V=-G m_S m_T alpha exp(-r/lambda)/r gives the tau_R10 bridge. | alpha_MTS(lambda_R)=Xi_R10[beta_S^R beta_T^R/(4 pi G Z_R)+alpha_boundary_tail] | FORMAL_TAU_KERNEL_LAW_DERIVED_CONDITIONAL | Xi_R10, beta legs, Z_R units, and boundary tail are not source-backed |
| KDER1573_5_claim_ceiling | The kernel law is useful but not a claim row. | score only if lambda_R>0, alpha_MTS numeric, accepted alpha_bound(lambda_R), and abs(alpha_MTS)<=alpha_bound | FORMAL_INTERFACE_READY_VALUES_MISSING | no accepted curve plus no internal numeric/theorem-zero inputs |

## Zero Condition Audit

| zero_id | zero_condition | current_status | claim_effect |
| --- | --- | --- | --- |
| ZERO1573_0_constraint_route | R_AB is a first-class/nonpropagating constraint with R_AB=0 before matter readout. | CONDITIONAL_ONLY_NOT_ACTIVE | cannot set tau_R10=0 |
| ZERO1573_1_source_silence | beta_S^R=0 and beta_T^R=0 for R10 source/test bodies in the observed matter action. | NOT_PROVED | cannot remove source amplitude |
| ZERO1573_2_boundary_silence | boundary/corner/readout tail alpha_boundary_tail=0. | NOT_PROVED | cannot drop B_R/readout tail |
| ZERO1573_3_range_decoupling | finite residual decouples from R10 by lambda_R outside the tested range or M_R^2/Z_R limit. | NOT_EVALUABLE | cannot score or decouple by range |
| ZERO1573_4_transfer_shortcut | borrow clock/WEP tau silence to set tau_R10=0. | FORBIDDEN_SHORTCUT | tau_R10 must be sourced separately |

## Required Inputs

| input_id | symbol | role | minimum_required_form | current_status |
| --- | --- | --- | --- | --- |
| REQ1573_0_ZR | Z_R | kinetic normalization in tau_R10 and range | positive same-frame parent-normalized value with units, or parent-signed operator exclusion | MISSING_ZR |
| REQ1573_1_MR2 | M_R^2 | range denominator lambda_R=sqrt(Z_R/M_R^2) | positive same-frame Hessian/mass-gap value with units | MISSING_MR2 |
| REQ1573_2_beta_source | beta_S^R | R10 source body R_AB charge | partial ln m_source / partial R_AB or theorem-zero for source material | MISSING_SOURCE_CHARGE |
| REQ1573_3_beta_test | beta_T^R | R10 test body R_AB charge | partial ln m_test / partial R_AB or theorem-zero for test material | MISSING_TEST_CHARGE |
| REQ1573_4_Xi | Xi_R10 | readout/sign/window normalization from parent response to R10 alpha convention | declared convention mapping delta V_R to alpha(lambda) | MISSING_READOUT_CONVENTION |
| REQ1573_5_boundary_tail | alpha_boundary_tail or B_R | boundary/corner/readout residual contribution | zero theorem or finite absolute bound with no-cancellation guard | MISSING_BOUNDARY_TAIL |
| REQ1573_6_bound_curve | alpha_bound(lambda) | external R10 comparator | accepted independently checked curve/table with source/provenance | REVIEWED_CANDIDATE_NOT_ACCEPTED |

## Scoring Interface Template

| template_id | lambda_R_m | alpha_MTS | current_status | failure_if_used_now |
| --- | --- | --- | --- | --- |
| SCORE1573_0_symbolic_kernel | sqrt(Z_R/M_R^2) after unit conversion to metres | Xi_R10*(beta_S^R*beta_T^R/(4*pi*G*Z_R)+alpha_boundary_tail) | TEMPLATE_ONLY_VALUES_MISSING | MISSING_ZR;MISSING_MR2;MISSING_BETA_SOURCE;MISSING_BETA_TEST;MISSING_XI;MISSING_BOUNDARY;CURVE_NOT_ACCEPTED |

## Runner Nonclaim

| runner_id | object | status | detail |
| --- | --- | --- | --- |
| RUN1573_0_sources | 1572 handoff plus parent/tau precedent sources | PASS | all source registers are present if validation passes |
| RUN1573_1_kernel_law | tau_R10 source-normalized formal law | FORMAL_LAW_DERIVED_CONDITIONAL | alpha_MTS(lambda_R)=Xi_R10[beta_S beta_T/(4 pi G Z_R)+boundary_tail] |
| RUN1573_2_zero_route | tau_R10=0 or q_R=0 theorem | NOT_PROVED | constraint/source/boundary/readout zero conditions remain unsigned |
| RUN1573_3_numeric_score | R10 alpha(lambda) score | BLOCKED_NO_CLAIM | formal kernel exists but required numeric/theorem-zero inputs and accepted curve are missing |

## Claim Gates

| gate_id | claim | status | reason |
| --- | --- | --- | --- |
| GATE1573_0_kernel_formula | tau_R10 formal kernel law exists | PASS_FORMAL_NONCLAIM | derived from linearized finite-range R_AB action and Yukawa matching |
| GATE1573_1_tau_zero | tau_R10=0 or q_R=0 | BLOCKED_NO_CLAIM | zero route requires parent-signed constraint/source/boundary/readout silence |
| GATE1573_2_numeric_prediction | numeric alpha_MTS(lambda_R) | BLOCKED_NO_CLAIM | Z_R/M_R^2/beta legs/Xi/boundary tail missing |
| GATE1573_3_R10_score | R10 pass/fail | BLOCKED_NO_CLAIM | accepted curve and internal numeric prediction both required |
| GATE1573_4_local_GR | derived local GR/Newton limit | BLOCKED_NO_CLAIM | R10 kernel law is not a local GR theorem |

## Decision

| decision_id | decision | reason | consequence |
| --- | --- | --- | --- |
| DEC1573_0_progress | TAU_R10_FORMAL_KERNEL_DERIVED_CONDITIONAL | the R_AB finite residual now has a source-normalized Yukawa matching law | future rows must fill beta/Z/M/Xi/boundary inputs or prove all relevant zeros |
| DEC1573_1_claim_ceiling | NO_R10_OR_LOCAL_GR_CLAIM | formal law has no sourced numeric inputs and curve remains reviewed-only | raw/accepted finite rows stay empty |
| DEC1573_2_best_next | NEXT_1574_R10_MATTER_CHARGE_AND_ZR_MR2_INPUT_ROW_OR_ZERO_THEOREM | kernel law shows the next missing objects exactly: beta_S beta_T, Z_R, M_R^2, Xi_R10 and boundary tail | derive matter-charge zero/descent first; if it fails, build finite required-input acquisition rows |

## Validation

| check_id | result | detail |
| --- | --- | --- |
| VAL1573_0_sources_exist | PASS | all cited source paths exist |
| VAL1573_1_needles_found | PASS | all source needles found |
| VAL1573_2_kernel_law | PASS | tau_R10 Yukawa alpha matching law written |
| VAL1573_3_zero_not_promoted | PASS | zero route remains conditional/not proved |
| VAL1573_4_required_inputs_missing | PASS | required internal inputs remain explicit blockers |
| VAL1573_5_template_nonclaim | PASS | scoring interface is template-only and not accepted |
| VAL1573_6_runner_blocks_score | PASS | runner blocks numeric R10 scoring |
| VAL1573_7_claim_gates_closed | PASS | claim gates closed while formula gate is nonclaim pass |
| VAL1573_8_decision_next | PASS | decision selects matter charge and ZR/MR2 input route |
| VAL1573_9_csv_parse | PASS | all generated 1573 CSVs parse cleanly |
| VAL1573_10_claim_flags_false | PASS | all generated prediction/claim flags remain false |
| VAL1573_11_no_raw_accepted | PASS | no 1573 rows written to raw/accepted finite directories |
| VAL1573_12_branch_copies | PASS | branch/quarantine nonclaim copies written |
| VAL1573_13_pycache_absent | PASS | scripts __pycache__ absent after run |
| VAL1573_14_formalization_untouched | PASS | formalization-workbench modified-file count is 0 |
| VAL1573_OVERALL | PASS | 1573 internal tauR10 source kernel derivation validation |

## Next Target

| next_target | script | objective | do_not |
| --- | --- | --- | --- |
| 1574-Y5-RAB-R10-matter-charge-and-ZR-MR2-input-row-or-zero-theorem.md | scripts/Y5_RAB_R10_matter_charge_and_ZR_MR2_input_row_or_zero_theorem.py | try to prove beta_S^R beta_T^R=0 by parent matter descent; otherwise stage finite source-charge, Z_R, M_R^2, Xi_R10 and boundary-tail input rows | do not score R10; do not transfer WEP/clock tau; do not claim local GR; do not edit formalization-workbench |
