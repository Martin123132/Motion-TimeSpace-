# 4643 - Xi_tail first claim-grade input fill or exact parent signature

Branch: `MTS_R2FR_Y5_XI_TAIL_DIMENSIONLESS_R10_PROJECTION_NORMALIZATION_4643`
Marker: `PPC4161_XI_TAIL_DIMENSIONLESS_R10_PROJECTION_NORMALIZATION_4643`
Decision: `R10_PROJECTION_CONSTANTS_COLLAPSED_TO_DIMENSIONLESS_ARENA_NORM_COMPONENTS_AND_LAMBDA_REMAIN_NONCLAIM`

## Result

4643 takes a real step rather than adding another missing-input ledger. The active 4642 blocker was that `K_NH`, `K_edge`, `K_tr`, `Pi_R10(lambda)` and the source normalization looked like separate constants. That is too much freedom.

The clean route is to express every local tail component directly as the calibrated R10 Yukawa-alpha coefficient:

`alpha_i(lambda)=<R_i,Y_lambda>_R10/<Y_lambda,Y_lambda>_R10`

after the observed Newtonian `1/r` calibration channel is removed. Linearity gives

`alpha_tail(lambda)=alpha_src_hidden+alpha_nonHilbert+alpha_boundary_history+alpha_transition_inner`.

The no-cancellation gate is then

`|alpha_tail(lambda)| <= |alpha_src_hidden|+|alpha_nonHilbert|+|alpha_boundary_history|+|alpha_transition_inner| <= alpha_bound(lambda_mem)`.

So, in this representation, `K_NH=K_edge=K_tr=Pi_R10=1` by normalization, not by fitting. Raw action-space residuals still need the projection map before scoring. This removes one independent free-constant layer but does not claim R10/local GR.

## Source Register

| checkpoint | source_id | path | exists | needle | needle_found | line | purpose | valid_for_claim | timestamp_utc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4643 | SRC4643_00_4642_validation | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_BRR545_4642_VALIDATION.csv | True | VAL4642_OVERALL | True | 20 | 4642 validated lambda/projection source pack. | False | 2026-07-06T20:06:34.576434+00:00 |
| 4643 | SRC4643_01_4642_projection | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4642_PROJECTION_CONSTANT_SOURCE_PACK.csv | True | PROJ4642_0_K_NH | True | 2 | projection constants were the active missing layer. | False | 2026-07-06T20:06:34.576434+00:00 |
| 4643 | SRC4643_02_4642_blocker | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4642_CLAIM_BLOCKERS.csv | True | PROJECTION_CONSTANTS_MISSING | True | 4 | 4642 blocker targeted by 4643. | False | 2026-07-06T20:06:34.576434+00:00 |
| 4643 | SRC4643_03_4642_doc | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\4642-Y5-R2FR-Xi-tail-parent-signature-and-lambda-source-pack.md | True | K_NH/K_edge/K_tr/Pi_R10 | True | 25 | human 4642 statement of missing projection constants. | False | 2026-07-06T20:06:34.576434+00:00 |
| 4643 | SRC4643_04_4639_KNH | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\4639-Y5-R2FR-Xi-nonHilbert-Hperp-tail-zero-or-bound.md | True | Xi_nonHilbert := K_NH N_src_nonHilbert | True | 13 | non-Hilbert tail projection constant source formula. | False | 2026-07-06T20:06:34.576434+00:00 |
| 4643 | SRC4643_05_4640_Kedge | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\4640-Y5-R2FR-Xi-boundary-history-transition-tail-zero-or-bound.md | True | \|Xi_boundary_history\| <= K_edge | True | 19 | boundary-history projection constant source formula. | False | 2026-07-06T20:06:34.576434+00:00 |
| 4643 | SRC4643_06_4640_Ktr | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\4640-Y5-R2FR-Xi-boundary-history-transition-tail-zero-or-bound.md | True | \|Xi_transition_inner\| <= K_tr | True | 23 | transition-inner projection constant source formula. | False | 2026-07-06T20:06:34.576434+00:00 |
| 4643 | SRC4643_07_4641_gate | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\4641-Y5-R2FR-same-branch-Xi-tail-zero-assembly-or-finite-coefficient-pack.md | True | finite no-cancellation pack | True | 21 | same-branch finite gate from 4641. | False | 2026-07-06T20:06:34.576434+00:00 |
| 4643 | SRC4643_08_4334_R10 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\350-PPC4161-local-test-projection-matrix-source-contract-or-R10-PPN-smoke-runner.md | True | PI4334_0_R10 | True | 62 | R10 projection matrix discipline. | False | 2026-07-06T20:06:34.576434+00:00 |
| 4643 | SRC4643_09_4334_gate | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\350-PPC4161-local-test-projection-matrix-source-contract-or-R10-PPN-smoke-runner.md | True | F4334_2_R10_smoke_gate | True | 97 | R10 scoring gate. | False | 2026-07-06T20:06:34.576434+00:00 |
| 4643 | SRC4643_10_4335_requirement | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\351-PPC4161-first-source-backed-PiPPN-or-R10-alpha-lambda-projection-row.md | True | F4335_4_R10_requirement | True | 81 | R10 alpha(lambda) source normalization requirement. | False | 2026-07-06T20:06:34.576434+00:00 |
| 4643 | SRC4643_11_4628_lambda | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\4628-Y5-R2FR-lambda-mem-gap-row-or-Zmem-M2mem-parent-hessian.md | True | lambda_mem=sqrt(Z_mem/M2_mem) | True | 43 | lambda_mem parent-Hessian law remains imported. | False | 2026-07-06T20:06:34.576434+00:00 |
| 4643 | SRC4643_12_4506_operator | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\522-PPC4161-memory-fibre-BX-CX-owner-or-body-charge-input-row.md | True | MOP4506_0_quadratic_action | True | 71 | memory quadratic action source operator. | False | 2026-07-06T20:06:34.576434+00:00 |
| 4643 | SRC4643_13_4635_curve | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4635_R10_EOTWASH2020_VECTOR_DIGITIZED_CURVE.csv | True | lambda_m | True | 1 | digitized R10 vector curve used for controls only. | False | 2026-07-06T20:06:34.576434+00:00 |

## Dimensionless R10 Projection Theorem

| checkpoint | theorem_id | statement | equation | proof_status | claim_allowed | timestamp_utc |
| --- | --- | --- | --- | --- | --- | --- |
| 4643 | THM4643_0_calibrated_R10_functional | Define alpha_i(lambda) as the linear R10 Yukawa-template coefficient of residual component R_i after the calibrated Newtonian 1/r channel is removed. | alpha_i(lambda)=<R_i,Y_lambda>_R10/<Y_lambda,Y_lambda>_R10 | DEFINITION_WITH_4334_4335_SOURCE_GUARD | False | 2026-07-06T20:06:34.576434+00:00 |
| 4643 | THM4643_1_linearity | Because the template projection is linear on the residual force/potential channel, the projected tail coefficient is the sum of projected component coefficients. | alpha_tail(lambda)=sum_i alpha_i(lambda) | LINEAR_PROJECTION_PROOF | False | 2026-07-06T20:06:34.576434+00:00 |
| 4643 | THM4643_2_no_cancellation_bound | The conservative finite gate uses absolute components, so cancellation between hidden/source/boundary/transition pieces is not allowed. | \|alpha_tail(lambda)\| <= \|alpha_src_hidden\|+\|alpha_nonHilbert\|+\|alpha_boundary_history\|+\|alpha_transition_inner\| | TRIANGLE_INEQUALITY_DERIVED | False | 2026-07-06T20:06:34.576434+00:00 |
| 4643 | THM4643_3_projection_constant_collapse | If Xi components are stored as these dimensionless alpha_i coefficients, then K_NH, K_edge, K_tr and Pi_R10 are not independent physical constants. | K_NH=K_edge=K_tr=Pi_R10=1 in the dimensionless R10 alpha norm | NORMALIZATION_COLLAPSE_DERIVED | False | 2026-07-06T20:06:34.576434+00:00 |
| 4643 | THM4643_4_raw_action_guard | Raw action-space residuals cannot use the unit constants until projected and normalized against the same calibrated source/test geometry. | raw R_i -> alpha_i(lambda) required before R10 scoring | RAW_UNITS_BRANCH_REJECT_GUARD | False | 2026-07-06T20:06:34.576434+00:00 |

## Normalized Projection Input Pack

| checkpoint | input_id | symbol | input_filled | value_or_rule | status | source_basis | remaining_needed | valid_for_claim | claim_allowed | timestamp_utc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4643 | NORM4643_0_Pi_R10 | Pi_R10(lambda) | True | linear calibrated Yukawa-template alpha functional | FILLED_AS_DIMENSIONLESS_PROJECTION_FUNCTIONAL | 4334 PI4334_0_R10 and 4335 F4335_4_R10_requirement | component residuals must be projected through this functional before scoring | False | False | 2026-07-06T20:06:34.576434+00:00 |
| 4643 | NORM4643_1_K_NH | K_NH | True | 1 once Xi_nonHilbert is represented as alpha_nonHilbert(lambda) | COLLAPSED_TO_ONE_BY_R10_ALPHA_NORMALIZATION | 4639 Xi_nonHilbert formula plus THM4643_3 | project N_src_nonHilbert into alpha_nonHilbert(lambda) | False | False | 2026-07-06T20:06:34.576434+00:00 |
| 4643 | NORM4643_2_K_edge | K_edge | True | 1 once Q_edge terms are represented as alpha_boundary_history(lambda) | COLLAPSED_TO_ONE_BY_R10_ALPHA_NORMALIZATION | 4640 boundary-history formula plus THM4643_3 | project shell/boundary Q_edge terms into alpha_boundary_history(lambda) | False | False | 2026-07-06T20:06:34.576434+00:00 |
| 4643 | NORM4643_3_K_tr | K_tr | True | 1 once epsilon_tr_hair is represented as alpha_transition_inner(lambda) | COLLAPSED_TO_ONE_BY_R10_ALPHA_NORMALIZATION | 4640 transition-inner formula plus THM4643_3 | project transition hair into alpha_transition_inner(lambda) | False | False | 2026-07-06T20:06:34.576434+00:00 |
| 4643 | NORM4643_4_Gobs_source_norm | G_N^obs M_S m_T | True | normalization denominator is the experiment-calibrated Newtonian channel, not a new fitted MTS constant | CALIBRATION_DENOMINATOR_DEFINED_HIDING_IN_G_REJECTED | 4335 F4335_4_R10_requirement | use source/test geometry and composition for any numeric R10 score | False | False | 2026-07-06T20:06:34.576434+00:00 |
| 4643 | NORM4643_5_alpha_bound_curve | alpha_bound(lambda) | False | digitized curve usable for internal controls only | SMOKE_CURVE_AVAILABLE_CLAIM_QA_PENDING | 4635 digitized vector curve | claim-grade curve QA/provenance before public R10 scoring | False | False | 2026-07-06T20:06:34.576434+00:00 |

## Remaining Claim Inputs

| checkpoint | remaining_id | previous_blocker | status_after_4643 | detail | next_action | claim_allowed | timestamp_utc |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 4643 | REM4643_0_projection_layer | BLK4642_2_PROJECTION_CONSTANTS_MISSING | INDEPENDENT_CONSTANT_LAYER_COLLAPSED | K_NH/K_edge/K_tr/Pi_R10 are no longer free source constants in the R10-alpha representation; raw residuals must first be converted into dimensionless component alpha_i(lambda). | 4644-Y5-R2FR-first-Xi-component-magnitude-or-exact-zero-certificate.md | False | 2026-07-06T20:06:34.576434+00:00 |
| 4643 | REM4643_1_component_values | BLK4642_3_FINITE_COMPONENT_VALUES_MISSING | STILL_MISSING_BUT_NOW_WELL_DEFINED | Need alpha_src_hidden, alpha_nonHilbert, alpha_boundary_history and alpha_transition_inner, or exact same-branch zeros. | 4644-Y5-R2FR-first-Xi-component-magnitude-or-exact-zero-certificate.md | False | 2026-07-06T20:06:34.576434+00:00 |
| 4643 | REM4643_2_lambda_ratio | BLK4642_1_ZMEM_M2MEM_RATIO_MISSING | UNCHANGED | lambda_mem remains sqrt(Z_mem/M2_mem); 4643 does not invent the parent Hessian ratio. | derive parent Hessian ratio or exact constraint/contact branch | False | 2026-07-06T20:06:34.576434+00:00 |
| 4643 | REM4643_3_exact_signature | BLK4642_0_SAME_BRANCH_SIGNATURE_UNSIGNED | UNCHANGED | Exact Xi_tail=0 still requires the same-branch parent signature from 4641. | try exact zero certificate before finite scoring if a clause can be signed | False | 2026-07-06T20:06:34.576434+00:00 |
| 4643 | REM4643_4_public_claim | BLK4642_4_R10_PROMOTION_SCOPE_PENDING | UNCHANGED | No public/local-GR/R10 claim; this is a private normalization theorem and smoke runner. | promote only after component values/lambda/curve QA and PPN/Newton/clocks/orbital maps exist | False | 2026-07-06T20:06:34.576434+00:00 |

## R10 Normalized Alpha Runner

| checkpoint | run_id | branch | lambda_mem_m | alpha_src_hidden | alpha_nonHilbert | alpha_boundary_history | alpha_transition_inner | alpha_tail_abs | alpha_bound_vector | result | reason | valid_for_claim | claim_allowed | timestamp_utc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4643 | RUN4643_0_live_missing_components | current live normalized R10 pack |  |  |  |  |  |  |  | FAIL_CLOSED | projection constants are normalized, but component alpha_i(lambda) values and lambda_mem remain missing | False | False | 2026-07-06T20:06:34.576434+00:00 |
| 4643 | RUN4643_1_exact_zero_control | same-branch exact Xi component zeros | 0.0001 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.07558630836177453 | CONDITIONAL_ZERO_PASS_NONCLAIM | linear normalized projection sends zero components to zero alpha_tail | False | False | 2026-07-06T20:06:34.576434+00:00 |
| 4643 | RUN4643_2_small_normalized_components | dimensionless alpha_i toy pass | 0.0001 | 0.009448288545221816 | 0.009448288545221816 | 0.009448288545221816 | 0.009448288545221816 | 0.037793154180887266 | 0.07558630836177453 | SMOKE_PASS_NONCLAIM | control row demonstrates unit projection constants with no-cancellation sum below bound | False | False | 2026-07-06T20:06:34.576434+00:00 |
| 4643 | RUN4643_3_large_normalized_components | dimensionless alpha_i toy fail | 0.0001 | 0.028344865635665448 | 0.028344865635665448 | 0.028344865635665448 | 0.028344865635665448 | 0.11337946254266179 | 0.07558630836177453 | SMOKE_FAIL_NONCLAIM | control row demonstrates same unit constants fail when absolute component sum exceeds bound | False | False | 2026-07-06T20:06:34.576434+00:00 |
| 4643 | RUN4643_4_raw_action_units | raw action residuals with K=1 attempted | 0.0001 |  |  |  |  |  | 0.07558630836177453 | REJECT_BRANCH | K=1 is only legal after conversion into calibrated dimensionless R10 alpha_i(lambda) coefficients | False | False | 2026-07-06T20:06:34.576434+00:00 |
| 4643 | RUN4643_5_hide_in_Gobs | absorb residual into calibrated G_N | 0.0001 |  |  |  |  |  | 0.07558630836177453 | REJECT_BRANCH | Newtonian calibration channel must be subtracted before Yukawa projection; MTS residual cannot be hidden in G_N^obs | False | False | 2026-07-06T20:06:34.576434+00:00 |
| 4643 | RUN4643_6_outside_curve_domain | lambda outside digitized curve | 1e-09 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |  | FAIL_CLOSED | alpha_bound(lambda) unavailable outside the source-backed curve domain | False | False | 2026-07-06T20:06:34.576434+00:00 |

## Controls

| checkpoint | control_id | rule | enforced | timestamp_utc |
| --- | --- | --- | --- | --- |
| 4643 | CTL4643_0_not_a_G_derivation | This checkpoint does not derive Newton's constant; it fixes how local residuals are normalized against the observed/calibrated Newtonian channel for R10. | True | 2026-07-06T20:06:34.576434+00:00 |
| 4643 | CTL4643_1_no_free_K_after_projection | Once an object is stored as alpha_i(lambda), K_NH/K_edge/K_tr/Pi_R10 cannot be tuned separately. | True | 2026-07-06T20:06:34.576434+00:00 |
| 4643 | CTL4643_2_raw_units_rejected | Raw parent-action residuals must pass through the projection functional before using the unit-normalized finite gate. | True | 2026-07-06T20:06:34.576434+00:00 |
| 4643 | CTL4643_3_no_cancellation | R10 finite scoring uses the sum of absolute projected components unless exact same-branch zeros are signed. | True | 2026-07-06T20:06:34.576434+00:00 |

## Decision

| checkpoint | decision_id | decision | next_target | claim_allowed | summary | timestamp_utc |
| --- | --- | --- | --- | --- | --- | --- |
| 4643 | DEC4643_0 | R10_PROJECTION_CONSTANTS_COLLAPSED_TO_DIMENSIONLESS_ARENA_NORM_COMPONENTS_AND_LAMBDA_REMAIN_NONCLAIM | 4644-Y5-R2FR-first-Xi-component-magnitude-or-exact-zero-certificate.md | False | 4643 removes the independent R10 projection-constant layer by defining Xi components as calibrated dimensionless Yukawa-alpha coefficients; this fills the normalization route but leaves component values, lambda_mem and exact same-branch signatures open. | 2026-07-06T20:06:34.576434+00:00 |

## Status

| checkpoint | branch_id | status | summary | valid_for_claim | claim_allowed | next_target | timestamp_utc |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 4643 | MTS_R2FR_Y5_XI_TAIL_DIMENSIONLESS_R10_PROJECTION_NORMALIZATION_4643 | PRIVATE_DERIVATION_ADVANCE_NONCLAIM | Projection constants collapsed by dimensionless R10 alpha normalization; no local-GR/R10 claim. | False | False | 4644-Y5-R2FR-first-Xi-component-magnitude-or-exact-zero-certificate.md | 2026-07-06T20:06:34.576434+00:00 |

## Next Target

| checkpoint | next_target | priority | first_attempt | timestamp_utc |
| --- | --- | --- | --- | --- |
| 4643 | 4644-Y5-R2FR-first-Xi-component-magnitude-or-exact-zero-certificate.md | derive one alpha_i(lambda) component or exact zero certificate now that projection constants are no longer independent blockers | Xi_src_hidden exact zero if source-label forgetting can be parent-signed; otherwise alpha_nonHilbert finite component through Hperp/readout | 2026-07-06T20:06:34.576434+00:00 |

## Validation

| checkpoint | validation_id | status | detail | timestamp_utc |
| --- | --- | --- | --- | --- |
| 4643 | VAL4643_0_sources_exist | PASS | all cited source paths exist | 2026-07-06T20:06:34.576434+00:00 |
| 4643 | VAL4643_1_needles_found | PASS | all cited source needles are present | 2026-07-06T20:06:34.576434+00:00 |
| 4643 | VAL4643_2_theorem_rows | PASS | dimensionless projection theorem rows present | 2026-07-06T20:06:34.576434+00:00 |
| 4643 | VAL4643_3_Pi_R10_filled | PASS | Pi_R10 filled as a linear alpha functional | 2026-07-06T20:06:34.576434+00:00 |
| 4643 | VAL4643_4_K_constants_collapsed | PASS | K_NH/K_edge/K_tr collapsed by normalization | 2026-07-06T20:06:34.576434+00:00 |
| 4643 | VAL4643_5_Gobs_guard | PASS | Gobs normalization guard present | 2026-07-06T20:06:34.576434+00:00 |
| 4643 | VAL4643_6_projection_blocker_updated | PASS | projection blocker updated | 2026-07-06T20:06:34.576434+00:00 |
| 4643 | VAL4643_7_live_fail_closed | PASS | live missing component branch fails closed | 2026-07-06T20:06:34.576434+00:00 |
| 4643 | VAL4643_8_pass_fail_controls | PASS | runner has pass and fail controls | 2026-07-06T20:06:34.576434+00:00 |
| 4643 | VAL4643_9_raw_units_rejected | PASS | raw action K=1 misuse rejected | 2026-07-06T20:06:34.576434+00:00 |
| 4643 | VAL4643_10_hide_in_G_rejected | PASS | hiding residual in Gobs rejected | 2026-07-06T20:06:34.576434+00:00 |
| 4643 | VAL4643_11_no_claim_allowed | PASS | generated runner/decision rows remain nonclaim | 2026-07-06T20:06:34.576434+00:00 |
| 4643 | VAL4643_12_doc_marker | PASS | post-checkpoint doc marker present | 2026-07-06T20:06:34.576434+00:00 |
| 4643 | VAL4643_13_formal_marker | PASS | formal checkpoint marker present | 2026-07-06T20:06:34.576434+00:00 |
| 4643 | VAL4643_14_claim_registered | PASS | claim row registered | 2026-07-06T20:06:34.576434+00:00 |
| 4643 | VAL4643_15_spine_marker | PASS | spine marker appended | 2026-07-06T20:06:34.576434+00:00 |
| 4643 | VAL4643_16_packet_marker | PASS | packet marker appended | 2026-07-06T20:06:34.576434+00:00 |
| 4643 | VAL4643_17_public_stage_clean | PASS | public stage not modified | 2026-07-06T20:06:34.576434+00:00 |
| 4643 | VAL4643_18_backup_repo_clean | PASS | backup repo not modified | 2026-07-06T20:06:34.576434+00:00 |
| 4643 | VAL4643_OVERALL | PASS | 4643 validation passed | 2026-07-06T20:06:34.792486+00:00 |
