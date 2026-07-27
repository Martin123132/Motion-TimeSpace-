# 2936 — Y5 R2FR: R10 curve promotion QA or ellJ source-current projection theorem under AX1090

Status: `Y5_R2FR_2936_R10_machine_QA_pass_review_only_promotion_refused_ellJ_owner_2937_next`

Claim ceiling: `R10_machine_QA_yes_review_only_live_curve_no_MTS_alpha_no_ellJ_owner_no_R10_pass_no_local_GR_no_GitHub_claim`

## Summary

2936 tests the live-curve promotion gate directly. The machine QA is good enough to keep the 390-row Eot-Wash 2020 vector extraction as a private review candidate: numeric rows pass, axis calibration is tight, and the alpha=1 anchor is recovered. But the promotion gate still refuses a live claim curve because official supplemental numerical data or signed human visual QA is not present.

This means the external R10 side is useful for smoke work but not claim scoring. The theory side is still harder: `alpha_kappa(lambda)` needs `K_X`, `Qbar_XH`, `tau_R10`, `c_g`, and a retained-tail envelope. Those all point back to the same source-current owner problem as `ell_J`.

## Source Register

| source_id | source_type | source_path | source_url | path_exists | anchors_found | role |
| --- | --- | --- | --- | --- | --- | --- |
| SRC2936_00_2935_doc | local_file | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\2935-Y5-R2FR-R10-alpha-lambda-real-curve-or-ellJ-source-current-owner-theorem-under-AX1090.md |  | True | True | 2935 handoff to curve promotion QA or ellJ theorem |
| SRC2936_01_2935_next | local_file | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_2935_NEXT_TARGET.csv |  | True | True | machine-readable 2936 target |
| SRC2936_02_2935_anchors | local_file | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_2935_R10_SOURCE_BACKED_ANCHOR_ROWS.csv |  | True | True | current branch R10 anchors |
| SRC2936_03_2935_candidate | local_file | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_2935_R10_REVIEW_CANDIDATE_STATUS.csv |  | True | True | current branch candidate status |
| SRC2936_04_2935_runner | local_file | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_2935_R10_RUNNER_REFUSAL_STATUS.csv |  | True | True | runner refusal status |
| SRC2936_05_2935_ellj | local_file | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_2935_ELLJ_FALLBACK_OWNER_STATUS.csv |  | True | True | ellJ/shared blocker status |
| SRC2936_06_2935_validation | local_file | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_BRR545_2935_VALIDATION.csv |  | True | True | 2935 validation |
| SRC2936_07_1034_doc | local_file | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1034-Y5-R10-alpha-bound-curve-digitization-and-projection-input-pack.md |  | True | True | prior R10 curve/projection pack |
| SRC2936_08_review_curve | local_file | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\local_bounds\R10_alpha_lambda_bound_curve_1034_REVIEW_CANDIDATE_NONCLAIM.csv |  | True | True | 390-row review curve |
| SRC2936_09_570_QA | local_file | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\local_bounds\P8_Y5_R10_570_REVIEW_CANDIDATE_QA.csv |  | True | True | review QA |
| SRC2936_10_570_summary | local_file | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\local_bounds\P8_Y5_R10_570_REVIEW_CURVE_SUMMARY.csv |  | True | True | review summary |
| SRC2936_11_569_gate | local_file | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\local_bounds\P8_Y5_R10_569_PROMOTION_GATE.csv |  | True | True | promotion gate |
| SRC2936_12_569_axis | local_file | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\local_bounds\P8_Y5_R10_569_AXIS_CALIBRATION.csv |  | True | True | axis calibration ledger |
| SRC2936_13_569_curve_identity | local_file | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\local_bounds\P8_Y5_R10_569_CURVE_IDENTITY_LEDGER.csv |  | True | True | curve identity ledger |
| SRC2936_14_live_digitized | local_file | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\local_bounds\R10_alpha_lambda_bound_curve_DIGITIZED.csv |  | True | True | live claim curve placeholder or missing marker |
| SRC2936_15_supplement_attempt | local_file | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\local_bounds\downloads\aps_prl_124_101101\link_aps_supplemental_attempt.html |  | True | True | prior APS supplement retrieval attempt if present |
| SRC2936_16_fig5b_pdf | local_file | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\local_bounds\downloads\arxiv_2002_11761\source_extract\fig5b1.pdf |  | True | True | source figure PDF from arXiv eprint if present |
| SRC2936_17_fig5b_render | local_file | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\local_bounds\downloads\arxiv_2002_11761\source_extract\fig5b1_render_300dpi.png |  | True | True | rendered source figure used for internal QA if present |
| SRC2936_18_2934_ellj | local_file | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_2934_ELLJ_OWNER_SOURCE_CURRENT_AUDIT.csv |  | True | True | ellJ owner status |
| SRC2936_19_2934_residual | local_file | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_2934_LOG_DERIVATIVE_RESIDUAL_VECTOR.csv |  | True | True | dotG projection residual |
| SRC2936_20_arxiv_2020 | external_source |  | https://arxiv.org/abs/2002.11761 | True | True | primary arXiv source for R10 paper |
| SRC2936_21_aps_2020 | external_source |  | https://link.aps.org/doi/10.1103/PhysRevLett.124.101101 | True | True | APS DOI landing page for R10 paper |
| SRC2936_22_aps_supplement | external_source |  | https://link.aps.org/supplemental/10.1103/PhysRevLett.124.101101 | True | True | official supplement route; not locally acquired as table |

## Machine QA

| qa_id | check | value | units | machine_pass | notes |
| --- | --- | --- | --- | --- | --- |
| MQA2936_0_numeric_rows | positive numeric candidate rows | 390 | rows | True | all vector candidate rows must parse as positive lambda/alpha |
| MQA2936_1_row_count | candidate row count | 390 | rows | True | expected current review-candidate density from 570 summary |
| MQA2936_2_unique_lambdas | unique lambda samples | 367 | samples | True | duplicate lambda samples=23; vector path samples are not the official scan grid |
| MQA2936_3_axis_residual | max axis log10 residual | 0.00038947790894194867 | log10 | True | axis tick fit remains tight enough for review candidate |
| MQA2936_4_anchor_lambda_error | alpha=1 anchor lambda relative error | 0.0016364485914564457 | fraction | True | anchor recovery supports axis mapping |
| MQA2936_5_anchor_alpha_error | alpha=1 anchor log10 alpha error | 0.0036909679279784123 | log10 | True | anchor recovery supports curve mapping |
| MQA2936_6_visual_identity | curve visual identity | visual_qa_pass_by_codex_render | status | True | internal visual QA only, not human promotion |
| MQA2936_7_valid_for_claim | candidate rows remain nonclaim | 0 | claim_rows | True | candidate must not be live claim curve |

## Promotion Gate Audit

| promotion_id | gate | status | gate_pass | required_for_live_curve | reason |
| --- | --- | --- | --- | --- | --- |
| PROM2936_0_machine_QA | machine numeric/axis/anchor/identity QA | PASS_REVIEW_ONLY | True | True | machine checks support review candidate |
| PROM2936_1_official_supplement | official supplement or machine-readable table acquired | BLOCKED | False | True | APS supplement table remains unacquired; prior gate=blocked |
| PROM2936_2_human_visual_QA | human visual QA signs extracted curve identity | BLOCKED | False | True | Codex visual/render QA exists, but no human signoff is recorded |
| PROM2936_3_live_file | replace live DIGITIZED claim file | BLOCKED | False | True | prior live gate=blocked; live file is not promoted |
| PROM2936_4_source_contract | anchor-only rows are not used for interpolation | PASS_NONCLAIM | True | True | 2935 runner refusal confirms anchors stay smoke-only |
| PROM2936_5_verdict | promote R10 review candidate to claim curve | REFUSED | False | True | machine QA alone is insufficient under the current claim policy |

## Live Curve Decision

| decision_id | live_curve_path | live_rows | placeholder_or_missing | candidate_can_replace_live | replacement_policy | notes |
| --- | --- | --- | --- | --- | --- | --- |
| LCD2936_0_live_curve | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\local_bounds\R10_alpha_lambda_bound_curve_DIGITIZED.csv | 2 | True | False | NO_REPLACEMENT_WITHOUT_SUPPLEMENT_OR_HUMAN_QA | live curve remains blocked even though machine QA is internally useful |

## MTS Alpha Projection Requirements

| projection_id | quantity | required_identity_or_input | status | condition_passed | reason |
| --- | --- | --- | --- | --- | --- |
| APR2936_0_alpha_bound | external alpha_bound(lambda) | promoted numeric curve with valid_for_claim=true | BLOCKED_REVIEW_CANDIDATE_NONCLAIM | False | external side not live |
| APR2936_1_KX | K_X(lambda) | parent Green-kernel normalization for finite-range mode | MISSING_PARENT_SOURCE | False | needed for alpha_kappa(lambda) |
| APR2936_2_Qbar_XH | Qbar_XH(source,lambda) | same-worldtube source charge/support integral | MISSING_SOURCE_NORMALIZATION | False | source-current owner debt |
| APR2936_3_tau_R10 | tau_R10(test,lambda) | test material/readout projection | MISSING_ARENA_PROJECTION | False | cannot set tau_R10=1 by shortcut |
| APR2936_4_cg | c_g | parent-signed coefficient or theorem-zero | MISSING_PARENT_INPUT_OR_ZERO_THEOREM | False | coupling branch still open |
| APR2936_5_tail | retained-tail envelope | absolute no-cancellation envelope for residual components | MISSING_ABSOLUTE_ENVELOPE | False | prevents hidden cancellation scoring |
| APR2936_6_alpha_predicted | alpha_kappa(lambda) | K_X Qbar_XH [tau_R10 c_g + abs_tail_envelope] | NOT_SCORE_READY | False | no MTS R10 prediction row yet |

## ellJ Source-Current Projection Attempt

| ellj_projection_id | clause | required_identity | status | condition_passed | reason |
| --- | --- | --- | --- | --- | --- |
| EJP2936_0_shared_owner | shared source-current owner | ell_J fixes the same source-current normalization used by dotG/G and R10 alpha projection | ROUTE_IDENTIFIED | True | this is the common non-looping theorem target |
| EJP2936_1_matter_descent | ordinary matter descent | S_matter descends with one J_H source current and one stress tensor | UNSIGNED | False | needed to define Qbar_XH and C_source |
| EJP2936_2_Ward_identity | source-current Ward identity | nabla_mu T^{mu nu}=0 with no projector/domain source leakage | UNSIGNED | False | needed to stop ell_J drift |
| EJP2936_3_reference_policy | unit/reference owner | ell_J fixed before readout and cannot be absorbed by measured GM | UNSIGNED | False | needed for dotG and R10 projection |
| EJP2936_4_projection_zero | projection zero | p_J D_t ln ell_J=0 and R10 tau/source normalization are parent-owned | NOT_DERIVED | False | theorem route remains open |

## Claim Gates

| claim_id | claim | status | condition_passed | reason |
| --- | --- | --- | --- | --- |
| CG2936_0_machine_QA | machine QA supports the review candidate | PASS_REVIEW_ONLY | True | numeric/axis/anchor checks are internally consistent |
| CG2936_1_live_curve | R10 review curve is promoted to live claim curve | BLOCKED_NONCLAIM | False | supplement/human QA gate remains blocked |
| CG2936_2_mts_alpha | MTS alpha_kappa(lambda) prediction is valid | BLOCKED_NONCLAIM | False | K_X/Qbar/tau/c_g/tails missing |
| CG2936_3_runner_claim | R10 runner can claim pass | BLOCKED_NONCLAIM | False | external and theory sides are not both claim-valid |
| CG2936_4_ellJ_owner | ell_J source-current owner theorem is derived | BLOCKED_NONCLAIM | False | shared owner theorem identified but not closed |
| CG2936_5_local_GR | local-GR/Newton follows from R10/coupling branch | BLOCKED_NONCLAIM | False | R10 and dotG projection gates still block |

## Decisions

| decision_id | decision | reason | action |
| --- | --- | --- | --- |
| DEC2936_0_machine | machine QA is enough for private smoke only | it strengthens confidence in the vector candidate but cannot replace supplement/human QA | keep candidate nonclaim |
| DEC2936_1_live | do not update live DIGITIZED curve | claim policy requires official table or signed human QA | leave live curve blocked |
| DEC2936_2_theory | prioritize theory-side source-current owner | external curve is not the only blocker; MTS alpha projection is empty | attack ell_J/Qbar/tau owner next |
| DEC2936_3_next | select ellJ/source-current projection theorem | it blocks dotG, R10, source normalization and local-GR reduction at once | 2937 should derive or explicitly fail the owner theorem |

## Next Target

| next_id | selection | target_doc | target_script | objective | acceptance_gate | fallback |
| --- | --- | --- | --- | --- | --- | --- |
| NEXT2936_0_2937 | selected_primary | 2937-Y5-R2FR-ellJ-source-current-owner-theorem-or-Qbar-tau-R10-projection-contract-under-AX1090.md | scripts/Y5_R2FR_ellJ_source_current_owner_theorem_or_Qbar_tau_R10_projection_contract_under_AX1090_2937.py | derive the ell_J/source-current owner theorem that fixes Qbar_XH, tau_R10 and C_source across dotG/R10/Newton, or emit a precise closure-only contract | no R10/local-GR claim unless ell_J source-current normalization, source charge, test projection and reference policy are parent-signed or independently bounded | if theorem fails, produce explicit Qbar/tau/c_g numeric-source acquisition rows and keep R10 nonclaim |

## Branch Copies

| copy_id | source_path | destination_path | source_exists | destination_exists | destination_parses |
| --- | --- | --- | --- | --- | --- |
| promotion_copy | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_2936_R10_PROMOTION_GATE_AUDIT.csv | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\local_bounds\R10_curve_promotion_gate_2936_NONCLAIM.csv | True | True | True |
| projection_copy | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_2936_MTS_ALPHA_PROJECTION_REQUIREMENTS.csv | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\parent-action\MTS_alpha_projection_requirements_2936_NONCLAIM.csv | True | True | True |
| ellj_copy | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_2936_ELLJ_SOURCE_CURRENT_PROJECTION_THEOREM_ATTEMPT.csv | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\parent-action\EllJ_source_current_projection_attempt_2936_NONCLAIM.csv | True | True | True |
| next_copy | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_2936_NEXT_TARGET.csv | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\rab-sector\acquisition-queue\JR2936_ELLJ_SOURCE_CURRENT_OWNER_OR_R10_PROMOTION_NEXT_NONCLAIM.csv | True | True | True |

## Validation

| validation_id | passed | check | required |
| --- | --- | --- | --- |
| VAL2936_0_required_sources_exist | True | all strict required local sources exist | True |
| VAL2936_1_required_anchors_found | True | all strict source anchors found | True |
| VAL2936_2_machine_QA_passes_review | True | machine QA passes for review-only candidate | True |
| VAL2936_3_promotion_refused | True | live curve promotion remains refused | True |
| VAL2936_4_live_curve_not_replaced | True | live curve not replaced by candidate | True |
| VAL2936_5_projection_blocked | True | MTS alpha projection remains blocked | True |
| VAL2936_6_ellJ_blocked | True | ellJ source-current theorem remains blocked | True |
| VAL2936_7_no_claims_promoted | True | no 2936 row is valid_for_claim | True |
| VAL2936_8_no_prediction_rows | True | no score-ready prediction rows emitted | True |
| VAL2936_9_outputs_parse | True | all 2936 output CSVs parse | True |
| VAL2936_10_branch_copies_parse | True | all branch copy CSVs parse | True |
| VAL2936_11_doc_exists | True | 2936 markdown doc exists | True |
| VAL2936_12_next_target_selected | True | 2937 target selected | True |
| VAL2936_13_outputs_under_post_checkpoint | True | all outputs remain under post-checkpoint-work | True |
| VAL2936_14_sources_not_formalization | True | no formalization-workbench source dependency | True |
| VAL2936_15_no_formalization_2936_outputs | True | no formalization-workbench 2936 outputs | True |
| VAL2936_OVERALL | True | 2936 validation overall | True |

Validation overall: `True`.

## Bottom Line

This is a clean narrowing. R10 external data are not the immediate dead end; the review candidate is usable privately, but cannot be promoted. The bigger live blocker is now the MTS projection theorem: source-current ownership must define `Qbar_XH`, `tau_R10`, `C_source`, and `ell_J` without measured-GM absorption. That is the next best derivation target.

## Non-Claims

- no live R10 curve promotion is made;
- no MTS `alpha_kappa(lambda)` row is score-ready;
- no `ell_J` owner theorem is claimed;
- no local-GR/Newton/R10 pass is claimed;
- no GitHub/public claim is made.
