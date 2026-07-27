# 2961 - Y5 R2FR: bconf branch selector, closure debt or residual smoke runner under AX1090

Status: `Y5_R2FR_2961_bconf_two_branch_selector_written_closure_debt_or_finite_residual_nonclaim`

Claim ceiling: `no_b_conf_theorem_zero_no_bconf_score_no_R10_PPN_clock_score_no_local_GR_no_Newton_no_public_claim`

2961 stops the proof loop and makes the fork explicit:

- Branch A is the closure-debt branch: impose the single-observed-frame rule, set `b_conf=0`, but give it no theorem-zero credit.
- Branch B is the finite-residual branch: keep `b_conf` live and require canonical `Xhat`, source/test current owner, `lambda_X`, and tau maps before any score.
- The smoke runner deliberately rejects both branches as claim evidence: closure is debt, residual rows are placeholders.
- The next useful work is finite-branch sourcing, not another attempt to re-derive the same single-frame clause.

## Source Register

| source_id | source_path | path_exists | anchors_found | role |
| --- | --- | --- | --- | --- |
| SRC2961_00_2960_doc | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\2960-Y5-R2FR-bconf-tau-projection-map-or-single-frame-closure-declaration-under-AX1090.md | True | True | 2960 handoff |
| SRC2961_01_2960_next | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_2960_NEXT_TARGET.csv | True | True | machine-readable 2961 target |
| SRC2961_02_2960_tau | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_2960_BCONF_TAU_PROJECTION_GATE.csv | True | True | b_conf tau gate |
| SRC2961_03_2960_conditional | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_2960_CONDITIONAL_SCALAR_TENSOR_COUNTERMODEL_MAP.csv | True | True | conditional countermodel maps |
| SRC2961_04_2960_closure | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_2960_SINGLE_FRAME_CLOSURE_DECLARATION_NONCLAIM.csv | True | True | single-frame closure declaration |
| SRC2961_05_2960_bounds | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_2960_BCONF_BOUND_ROWS_NONCLAIM.csv | True | True | b_conf bound rows |
| SRC2961_06_2959_frame | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_2959_SINGLE_OBSERVED_FRAME_PARENT_ACTION_GATE.csv | True | True | single-frame gate |
| SRC2961_07_2959_bconf | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_2959_BCONF_BOUND_INTAKE_NONCLAIM.csv | True | True | b_conf intake rows |
| SRC2961_08_global_coupling | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_global_coupling_superselection_CONTRACT.csv | True | True | global/source-current contract |
| SRC2961_09_local_template | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\MTS_local_residual_predictions_TEMPLATE.csv | True | True | local residual template |
| SRC2961_10_local_bounds | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\local_bounds\local_bound_claims.csv | True | True | local bound anchors |
| SRC2961_11_r10_curve | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\local_bounds\R10_alpha_lambda_bound_curve_1034_REVIEW_CANDIDATE_NONCLAIM.csv | True | True | R10 nonclaim bound curve |

## Branch Selector

| selector_id | selector_branch | rule | branch_allowed_for_private_work | theorem_zero_credit | local_GR_claim | policy |
| --- | --- | --- | --- | --- | --- | --- |
| SEL2961_0_closure_debt | BCONF_CLOSURE_DEBT_BRANCH | b_conf=0 by explicit single-observed-frame closure | True | False | False | use only as an internal closure-debt branch; no theorem-zero/local-GR credit |
| SEL2961_1_residual | BCONF_FINITE_RESIDUAL_BRANCH | b_conf finite until canonical Xhat/source-current/tau maps are sourced | False | False | False | use as falsifiable residual branch; no score until tau maps are real |
| SEL2961_2_dual_track_policy | DUAL_TRACK_PRIVATE_POLICY | carry both branches side-by-side in private audits | True | False | False | do not choose the prettier branch as evidence; compare only after both are labelled |
| SEL2961_3_verdict | NO_BRANCH_IS_DERIVED_LOCAL_GR | the fork is organized, not solved | True | False | False | local GR/Newton reduction remains unclaimed |

## Closure-Debt Branch

| row_id | object | branch_value | closure_debt | theorem_zero_credit | accepted_for_scoring | statement |
| --- | --- | --- | --- | --- | --- | --- |
| CDB2961_0_rule | single-observed-frame closure | b_conf=0_BY_CLOSURE | True | False | False | ordinary matter couples only to e_obs(q) and fixed representation data |
| CDB2961_1_credit_limit | theorem credit | NO_THEOREM_ZERO_CREDIT | True | False | False | closure kills b_conf only by branch grammar, not by parent derivation |
| CDB2961_2_scope_limit | scope | PARTIAL_CHANNEL_ONLY | True | False | False | closure only addresses hidden conformal b_conf; b_dis, b_marker, b_alpha and source-current rows remain independent unless separately closed |
| CDB2961_3_claim_limit | claims | NO_LOCAL_GR_CLAIM | True | False | False | closure branch cannot be promoted to local GR/Newton/R10/PPN evidence without parent derivation or independent score rows |

## Finite Residual Branch

| row_id | symbol | numeric_or_theorem_value | units | accepted_for_scoring | next_needed |
| --- | --- | --- | --- | --- | --- |
| RES2961_0_b_conf | b_conf | MISSING_PRIOR_OR_FIT | dimensionless | False | must source theorem-zero, prior, or fit value |
| RES2961_1_tau_R10_conf | tau_R10_conf | MISSING_XHAT_SOURCE_TEST_LAMBDA | dimensionless_projection | False | needs canonical Xhat, source/test charge and lambda_X |
| RES2961_2_tau_PPN_gamma_conf | tau_PPN_gamma_conf | MISSING_FRAME_REGIME_AND_PPN_MAP | dimensionless_projection | False | needs scalar-tensor regime or MTS weak-field map |
| RES2961_3_tau_clock_conf | tau_clock_conf | MISSING_LOCAL_PROFILE_AND_CLOCK_FRAME | dimensionless_projection | False | needs local Xhat profile and frame/readout order |
| RES2961_4_tau_source_conf | tau_source_conf | MISSING_SOURCE_CURRENT_OWNER | dimensionless_projection | False | needs source-normalization theorem or residual coefficient |
| RES2961_5_alpha_R10_conf | alpha_R10_conf(lambda) | MISSING_PRODUCT_INPUTS | dimensionless | False | runner must reject placeholders |
| RES2961_6_B_conf_envelope | B_conf | MISSING_TAU_VALUES | dimensionless | False | not score-ready |

## Smoke Runner Status

| smoke_id | object | valid_mts_rows | smoke_status | claim_allowed | notes |
| --- | --- | --- | --- | --- | --- |
| SMOKE2961_0_schema | branch selector schema | 0 | PASS_SCHEMA_ONLY | False | two branches are explicit |
| SMOKE2961_1_closure_branch | closure-debt branch | 0 | BLOCKED_FOR_CLAIM | False | closure theorem credit is false |
| SMOKE2961_2_residual_branch | finite residual branch | 0 | BLOCKED_FOR_SCORE | False | valid residual score rows remain zero |
| SMOKE2961_3_expected | claim outcome | 0 | CLAIM_FALSE_EXPECTED | False | closure_theorem_credit=False; residual_valid_rows=0 |

## Claim Gates

| claim_gate_id | claim | condition_passed | status | claim_allowed |
| --- | --- | --- | --- | --- |
| CG2961_0_selector | two-branch selector exists | True | PRIVATE_ORGANIZATION_ONLY | False |
| CG2961_1_closure_credit | closure branch gives theorem-zero credit | False | CLOSURE_DEBT_TRUE | False |
| CG2961_2_residual_score | finite b_conf residual branch is score-ready | False | VALID_MTS_ROWS_ZERO | False |
| CG2961_3_R10_PPN_clock | R10/PPN/clock comparison allowed | False | TAU_MAPS_PLACEHOLDER | False |
| CG2961_4_local_GR | local GR/Newton reduction allowed | False | NO_LOCAL_GR_CLAIM | False |
| CG2961_5_public | public claim allowed | False | PRIVATE_NONCLAIM_CHECKPOINT | False |

## Decision Ledger

| decision_id | decision | because | next_action |
| --- | --- | --- | --- |
| DEC2961_0_selector | b_conf route is now an explicit fork | the previous loop is resolved into closure-debt versus finite-residual branches | carry both branches in private work |
| DEC2961_1_closure | closure branch is usable but not evidential | b_conf=0 can be imposed by single-frame grammar, but closure_debt prevents local-GR claim | do not present as derivation |
| DEC2961_2_residual | residual branch is testable but not runnable yet | b_conf and tau maps have explicit rows, but no canonical normalization/source-current owner | derive Xhat/source-current owner next |
| DEC2961_3_next | next target should source the finite residual branch | this avoids repeating the same single-frame proof loop and moves toward empirical robustness | build 2962 canonical Xhat/source-current normalization or b_conf residual prior |

## Next Target

| next_id | priority | next_doc | next_script | objective | exclude |
| --- | --- | --- | --- | --- | --- |
| NEXT2961_0_2962 | selected_primary | 2962-Y5-R2FR-canonical-Xhat-source-current-normalization-or-bconf-residual-prior-under-AX1090.md | scripts/Y5_R2FR_canonical_Xhat_source_current_normalization_or_bconf_residual_prior_under_AX1090_2962.py | Try to derive the canonical Xhat normalization and source/test current owner needed for the finite b_conf residual branch. If this fails, fill nonclaim b_conf prior/projection intake rows for later smoke tests. | derive single-frame theorem again;b_marker full taxonomy;quotient/vertical no-pole rerun;beta prediction;direct lambda closure;alpha(lambda) scoring;I_X scoring;local-GR claim;public claim;formalization-workbench edits;GitHub action |

## Branch Copies

| copy_id | source_path | copy_path | source_exists | copy_exists | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| selector_copy | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_2961_BCONF_BRANCH_SELECTOR.csv | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\parent-action\bconf_branch_selector_2961_NONCLAIM.csv | True | True | False |
| residual_copy | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_2961_RESIDUAL_BRANCH_NONCLAIM.csv | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\local_bounds\bconf_residual_smoke_rows_2961_NONCLAIM.csv | True | True | False |
| next_copy | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_2961_NEXT_TARGET.csv | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\rab-sector\acquisition-queue\JR2961_XHAT_SOURCE_CURRENT_OR_BCONF_SMOKE_NEXT_NONCLAIM.csv | True | True | False |

## Validation

| validation_id | passed | check | required |
| --- | --- | --- | --- |
| VAL2961_0_sources_exist | True | all cited local source paths exist | True |
| VAL2961_1_anchors_found | True | all cited source anchors found | True |
| VAL2961_2_two_branches | True | closure and residual branches both exist | True |
| VAL2961_3_closure_debt | True | closure branch carries debt and no theorem credit | True |
| VAL2961_4_residual_nonclaim | True | residual branch rows remain nonclaim | True |
| VAL2961_5_residual_paths | True | residual rows cite existing paths | True |
| VAL2961_6_smoke_blocks_claim | True | smoke runner blocks claim | True |
| VAL2961_7_claims_blocked | True | selector exists but all claims remain blocked | True |
| VAL2961_8_next_target_written | True | 2962 next target selected | True |
| VAL2961_9_branches_exist | True | branch copy files exist | True |
| VAL2961_10_csvs_parse | True | all generated CSV files parse | True |
| VAL2961_11_outputs_under_post_checkpoint | True | all generated outputs are under post-checkpoint-work | True |
| VAL2961_12_formalization_clean | True | no 2961 outputs were written to formalization-workbench | True |
| VAL2961_13_doc_written | True | 2961 markdown checkpoint exists | True |
| VAL2961_OVERALL | True | 2961 validation overall | True |

Validation overall: `True`.
