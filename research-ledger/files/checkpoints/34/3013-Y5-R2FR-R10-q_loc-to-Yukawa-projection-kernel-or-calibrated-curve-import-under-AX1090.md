# 3013 — R10 `q_loc` to Yukawa Projection Kernel or Calibrated Curve Import under AX1090

Status: `Y5_R2FR_3013_R10_kernel_contract_derived_source_owner_blocked_3014_next`

## Verdict

3013 is a useful theory step. It does **not** give an R10 pass, but it does derive the exact contract a future R10 pass would need.

There are now two honest comparison languages:

1. **Acceleration response:** if `q_loc` is converted into a same-frame radial acceleration `a_q`, then `alpha_q(lambda;r)=a_q/a_N * exp(r/lambda)/(1+r/lambda)`.
2. **Parent eigenmode charge response:** if the parent action provides `(-Z Delta + M^2)X=J`, then `lambda=sqrt(Z/M^2)` in the one-mode case and `alpha=K_X Qbar_XH qbar_XT tau_R10 + tails`, with `K_X=s_X/(4*pi*Z_X*G_obs)`.

The dragon is exactly located now: `q_loc^nu` is not itself a scalar Yukawa source. A parent action must supply a source-current owner, inverse-divergence map, or theorem-zero closure before R10 can score MTS.

## Source Register

| source_id | exists | role | status |
| --- | --- | --- | --- |
| SRC3013_00_3012_doc | True | previous checkpoint verdict and guardrails | PRESENT |
| SRC3013_01_3012_next | True | 3013 target definition | PRESENT |
| SRC3013_02_3012_facts | True | R10 paper Yukawa convention and supplement facts | PRESENT |
| SRC3013_03_3012_bounds | True | nonclaim R10 bound rows and blockers | PRESENT |
| SRC3013_04_3012_dryrun | True | prediction and bound row dry-run requirements | PRESENT |
| SRC3013_05_2410_source_map_gate | True | no direct q_loc scalarization and source-map contract | PRESENT |
| SRC3013_06_2210_range_operator | True | lambda owner and finite-range operator law | PRESENT |
| SRC3013_07_2210_source_map_first_row | True | range-indexed source-map first row | PRESENT |
| SRC3013_08_2663_charge_normalization | True | source/test charge normalization contract | PRESENT |
| SRC3013_09_2701_alpha_response | True | acceleration-level alpha response operator | PRESENT |
| SRC3013_10_2702_profile_schema | True | q_loc R10 profile row schema | PRESENT |
| SRC3013_11_2702_profile_audit | True | current profile asset audit | PRESENT |
| SRC3013_12_3010_bound_interface | True | q_loc/Delta_K/coupling residual bounds | PRESENT |
| SRC3013_13_fig5_vector_audit | True | Fig. 5 vector status from 3012 | PRESENT |
| SRC3013_14_aps_fetch_log | True | APS supplement fetch blocker evidence | PRESENT |

## Kernel Derivation

| kernel_id | object | status | missing_for_claim |
| --- | --- | --- | --- |
| KDER3013_0_R10_convention | published R10 Yukawa convention | SOURCE_ANCHORED | none for convention; still need MTS source projection |
| KDER3013_1_acceleration_response | acceleration-level q_loc response | CONDITIONAL_KERNEL_DERIVED_NONCLAIM | MISSING_q_loc_PROFILE; MISSING_FORCE_DENSITY_TO_ACCELERATION_MAP; MISSING_SOURCE_FRAME; MISSING_FULL_BOUND_CURVE |
| KDER3013_2_parent_finite_range_operator | parent finite-range mode | RANGE_OWNER_DERIVED_VALUES_BLOCKED | MISSING_PARENT_Z_AB; MISSING_PARENT_M_AB; MISSING_EIGENVECTORS; MISSING_DOMAIN_CERTIFICATE |
| KDER3013_3_charge_response | parent charge/eigenmode alpha response | CONDITIONAL_ALPHA_LAW_DERIVED_VALUES_BLOCKED | MISSING_Z_i; MISSING_Q_SOURCE; MISSING_q_TEST; MISSING_tau_R10; MISSING_SIGN_POLICY; MISSING_APPARATUS_NORMALIZATION |
| KDER3013_4_q_loc_bridge | q_loc-to-source bridge | BRIDGE_CONTRACT_EXACT_BUT_UNSIGNED | MISSING_CURRENT_OWNER; MISSING_TGK_OR_I_DIV_INVERSE; MISSING_b_i_nu; MISSING_BOUNDARY_TERMS; MISSING_UNITS |
| KDER3013_5_no_cancellation_envelope | absolute R10 residual envelope | ENVELOPE_DERIVED_VALUES_BLOCKED | MISSING_COMPONENT_VALUES_OR_ZERO_THEOREMS; MISSING_FULL_BOUND_CURVE |

## Parent Action Contract

| clause_id | required_clause | current_status | blocks |
| --- | --- | --- | --- |
| PACT3013_0_quotient_domain | physical quotient/domain projection for the local R10 branch | MISSING_DOMAIN_CERTIFICATE | range eigenproblem, source charge, boundary/tail split |
| PACT3013_1_operator_coefficients | parent-signed kinetic/mass operator | MISSING_PARENT_Z_AB_AND_M_AB | lambda_i and K_i normalization |
| PACT3013_2_source_current_owner | source current J_A or inverse-divergence map from q_loc | MISSING_CURRENT_OWNER | Q_i^S and q_loc-to-Yukawa bridge |
| PACT3013_3_source_test_charges | body charge integrals and test response | MISSING_Q_SOURCE_AND_q_TEST | alpha_i numerator |
| PACT3013_4_observed_Newton_frame | same-frame G_obs, source mass and test mass | MISSING_APPARATUS_NORMALIZATION | dimensionless alpha comparison |
| PACT3013_5_tau_readout | R10 readout/source normalization factor | MISSING_tau_R10 | apparatus-to-theory comparison |
| PACT3013_6_boundary_tail_policy | edge, tail and boundary residual split | MISSING_COMPONENT_ZERO_OR_BOUNDS | no-cancellation promotion |

## Prediction Template

| prediction_id | alpha_predicted | alpha_predicted_abs_envelope | status |
| --- | --- | --- | --- |
| PRED3013_0_R10_kernel_template | MISSING_NUMERIC_ALPHA | |K_i Qbar_i^S qbar_i^T tau_R10_i| + |alpha_edge_i| + |alpha_tail_i| + |alpha_DeltaK_i| + |alpha_Ward_i| + |alpha_matter_coupling_i| | TEMPLATE_ONLY_VALUES_BLOCKED |
| PRED3013_1_theorem_zero_alternative | 0 only if parent zero theorem covers q_loc bridge, source current, test response, boundary and tail terms | 0 | ZERO_ROUTE_NOT_SIGNED |

## Component Envelope

| component_id | alpha_component | status | required_owner |
| --- | --- | --- | --- |
| ENV3013_0_bulk | alpha_bulk_i | MISSING_K_Q_q_tau | parent action source current plus source/test charge normalization |
| ENV3013_1_edge | alpha_edge_i | MISSING_EDGE_SPLIT | boundary/source-domain clause |
| ENV3013_2_tail | alpha_tail_i | MISSING_TAIL_BOUND | spectral measure or truncation theorem |
| ENV3013_3_DeltaK | alpha_DeltaK_i | SOURCE_READY_NONNUMERIC | Delta_K components and R10 projection norm |
| ENV3013_4_Ward | alpha_Ward_i | SOURCE_READY_SCHEMA | Euler/source zero or boundary flux bound |
| ENV3013_5_matter_coupling | alpha_matter_coupling_i | SOURCE_READY_NONNUMERIC | A_matter and c_g/b_dis/dln_alpha/dln_m projection pack |

## Curve Import Side Route

| route_id | route | current_status | claim_policy |
| --- | --- | --- | --- |
| CURVE3013_0_APS_supplement | import publisher supplemental numerical constraints | BLOCKED_BY_403 | only rows with positive numeric lambda/alpha, provenance, units and no MISSING markers can become valid_bound_curve_row=true |
| CURVE3013_1_calibrated_vector_digitization | calibrate Fig. 5 vector paths | VECTOR_PRESENT_AXIS_NOT_CALIBRATED | uncalibrated path coordinates remain nonclaim and cannot overwrite the live curve file |
| CURVE3013_2_anchor_smoke | alpha=1 threshold anchors | PRESENT_NONCURVE | anchors cannot replace the full curve and cannot score a predicted lambda_i unless the prediction is exactly the threshold statement being audited |

## Blocker Ledger

| blocker_id | blocking_condition | precise_missing_object | next_attack |
| --- | --- | --- | --- |
| BLK3013_0_current_owner | MISSING_CURRENT_OWNER_OR_I_DIV_INVERSE | J_i, C_i[I_div^{-1}(q_loc)] or q_loc=P_loc b_i(L_iX_i-J_i)+boundary identity | derive source-current owner from parent action variation or demote R10 to acceleration-profile only |
| BLK3013_1_operator_coefficients | MISSING_Z_M_EIGENMODE | Z_AB, M_AB, v_i and units on the R10 quotient domain | derive finite-range quadratic block or prove rank-zero constraint branch |
| BLK3013_2_charges | MISSING_SOURCE_TEST_CHARGES | Qbar_i^S, qbar_i^T and edge split in same Newton frame | source-sign body charge integrals or prove visible matter response zero |
| BLK3013_3_tau_R10 | MISSING_tau_R10 | apparatus/source-worldtube projection factor | derive tau_R10 or carry it as a finite nuisance with independent bound |
| BLK3013_4_bound_curve | MISSING_FULL_ALPHA_BOUND_CURVE | 66-lambda signed alpha constraints or calibrated Fig. 5 curve | get APS supplement through browser/manual download or perform calibrated vector digitization |
| BLK3013_5_no_cancellation | MISSING_COMPONENT_ZERO_OR_BOUNDS | absolute values or zero theorems for bulk/edge/tail/DeltaK/Ward/matter-coupling pieces | fill component envelope rows one by one |

## Dry-Run Results

| dryrun_id | check | passed | result_status |
| --- | --- | --- | --- |
| DR3013_0_kernel_shape | R10 alpha kernel shape derived | True | KERNEL_CONTRACT_DERIVED_NONCLAIM |
| DR3013_1_no_scalar_proxy | q_loc direct scalar shortcut forbidden | True | GUARD_ACTIVE |
| DR3013_2_prediction_numeric | valid numeric alpha prediction row exists | False | BLOCKED_NONCLAIM |
| DR3013_3_bound_curve | valid full R10 alpha(lambda) curve exists | False | BLOCKED_NONCLAIM |
| DR3013_4_R10_claim | R10 claim allowed | False | CLAIM_FORBIDDEN |

## Promotion Gates

| gate_id | gate | result | notes |
| --- | --- | --- | --- |
| GATE3013_0_sources_exist | all cited local source paths exist | True | 3013 is grounded in current local ledgers |
| GATE3013_1_kernel_written | kernel contract written without numeric promotion | True | derives response formulas and missing owners, not a prediction value |
| GATE3013_2_no_proxy | no direct rho_X := q_loc scalar proxy is allowed | True | bridge clause requires current owner/inverse-divergence/domain/units |
| GATE3013_3_no_curve_promotion | no uncalibrated curve or anchor-only data is promoted | True | curve import side route remains blocked/nonclaim |
| GATE3013_4_prediction_claim | valid R10 prediction row exists | False | parent coefficients, charges, tau and component bounds are missing |
| GATE3013_5_R10_claim | R10 pass claim allowed | False | both prediction values and full bound curve remain blocked |

## Decision Ledger

| decision_id | decision | rationale |
| --- | --- | --- |
| DEC3013_0_status | 3013 derives the exact R10 comparison kernel contract but keeps the row nonclaim. | The mathematics is now sharp enough to score later: alpha is either an acceleration ratio in the R10 Yukawa convention or a parent charge/eigenmode product. The q_loc bridge remains the unsigned object. |
| DEC3013_1_next_route | The next real derivation target is the parent source-current owner, not another bound-table pass. | Even a perfect R10 curve cannot score MTS until q_loc is connected to J_i or to a same-frame acceleration profile with units. |
| DEC3013_2_curve_side_route | Curve import remains a side route, not the main theory route. | APS supplement/manual digitization will be needed eventually, but it does not solve the source-current/coupling problem. |

## Next Target

| next_id | target_doc | mission | success_condition |
| --- | --- | --- | --- |
| NEXT3013_0_3014 | 3014-Y5-R2FR-parent-source-current-owner-for-R10-kernel-or-rank-zero-local-closure-under-AX1090.md | Try to derive the parent source-current owner J_i/C_i[I_div^{-1}(q_loc)] needed by the R10 kernel, or prove the finite-range R10 branch is rank-zero/closure-only. | either a parent-signed source-current/inverse-divergence map exists with units/domain, or the branch is demoted to an explicit local-closure residual with no Yukawa alpha claim. |

## Validation

| validation_id | passed | requirement | evidence |
| --- | --- | --- | --- |
| VAL3013_00_sources_exist | True | every cited local source path exists | P8_Y5_R2FR_3013_SOURCE_REGISTER.csv |
| VAL3013_01_csv_parse | True | generated CSV rows parse cleanly | all generated CSV artifacts import with csv.DictReader |
| VAL3013_02_kernel_forms_present | True | each kernel derivation row has an explicit kernel/formula | P8_Y5_R2FR_3013_R10_KERNEL_DERIVATION.csv |
| VAL3013_03_parent_contract_complete | True | parent action contract clauses are explicit and unsigned | P8_Y5_R2FR_3013_PARENT_ACTION_CONTRACT.csv |
| VAL3013_04_no_scalar_proxy_guard | True | direct scalarization of q_loc is forbidden | BLK3013_0 and GATE3013_2 |
| VAL3013_05_prediction_rows_nonclaim | True | prediction templates remain invalid/nonclaim while values are missing | P8_Y5_R2FR_3013_R10_PREDICTION_ROW_TEMPLATE.csv |
| VAL3013_06_missing_markers_nonclaim | True | rows with MISSING markers are never valid_for_claim=true | all 3013 generated ledgers |
| VAL3013_07_claims_blocked | True | R10 and local-claim promotion remains blocked | P8_Y5_R2FR_3013_PROMOTION_GATES.csv |
| VAL3013_08_outputs_scoped | True | no generated file is outside post-checkpoint-work | generated path scope check |
| VAL3013_09_formalization_not_targeted | True | formalization-workbench is not modified by this checkpoint | output target list excludes formalization-workbench |
| VAL3013_10_next_target_selected | True | next target selects parent source-current owner or rank-zero closure | P8_Y5_R2FR_3013_NEXT_TARGET.csv |
| VAL3013_99_overall | True | all 3013 validation checks pass | aggregate of VAL3013_00 through VAL3013_10 |

## Files Written

- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3013_SOURCE_REGISTER.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3013_R10_KERNEL_DERIVATION.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3013_PARENT_ACTION_CONTRACT.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3013_R10_PREDICTION_ROW_TEMPLATE.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3013_ALPHA_COMPONENT_ENVELOPE.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3013_CURVE_IMPORT_SIDE_ROUTE.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3013_BLOCKER_LEDGER.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3013_DRYRUN_RESULTS.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3013_PROMOTION_GATES.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3013_DECISION_LEDGER.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3013_NEXT_TARGET.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3013_BRANCH_COPIES.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_BRR545_3013_VALIDATION.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\local_bounds\R10_q_loc_to_Yukawa_kernel_contract_3013_NONCLAIM.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\local_bounds\R10_prediction_row_template_3013_NONCLAIM.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\local_bounds\R10_parent_action_contract_3013_NONCLAIM.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\rab-sector\acquisition-queue\JR3013_PARENT_ACTION_SOURCE_OWNER_OR_R10_KERNEL_VALUES_NEXT.csv`

## Hard Guardrails Still Active

- No R10 pass claim.
- No direct scalarization of `q_loc`.
- No anchor-only or uncalibrated-figure bound curve.
- No hidden-coupling cancellation.
- No `formalization-workbench` edits.
- No GitHub action.
