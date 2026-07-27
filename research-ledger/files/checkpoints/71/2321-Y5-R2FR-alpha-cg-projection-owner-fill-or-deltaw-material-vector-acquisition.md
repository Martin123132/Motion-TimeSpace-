# 2321 - alpha_cg Projection Owner Fill Or delta_w Material Vector Acquisition

## Summary

2321 makes one real forward move: it locks the only honest PPN score object for the common conformal coupling,
`alpha_cg^PPN = tau_PPN*S_PPN(lambda_X,env)*c_g/sqrt(Z_X)`, with `N_X=1/sqrt(Z_X)` and
`lambda_X=sqrt(Z_X/M_X^2)` imported as exact conditional relations.

That is not a local-GR win. It is a loophole closure. Raw `c_g` is forbidden, the relation-only quantities are not
numeric inputs, and `alpha_cg` still cannot be scored until the parent branch supplies the common matter frame,
same-branch owner, positive `Z_X`, `M_X^2`, `S_PPN`, `tau_PPN`, and vector-tail control.

`delta_w` remains the fallback acquisition lane: useful comparator anchors exist, but the material/source vector and
tau/readout transfer are still absent.

## Source Register

| row_id | source_key | source_path | exists | needles_found | source_role | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| SRC2321_00_2320_doc | 2320_doc | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\2320-Y5-R2FR-delta-w-material-source-vector-or-PPN-component-owner-row.md | true | true | 2320 handoff | false |
| SRC2321_01_2320_validation | 2320_validation | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_BRR545_2320_VALIDATION.csv | true | true | 2320 validation | false |
| SRC2321_02_2320_alpha_status | 2320_alpha_status | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_2320_ALPHA_CG_COMPONENT_STATUS.csv | true | true | current alpha_cg blockers | false |
| SRC2321_03_2320_ppn_import | 2320_ppn_import | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_2320_PPN_COMPONENT_OWNER_IMPORT.csv | true | true | alpha_cg source import | false |
| SRC2321_04_2320_delta_status | 2320_delta_status | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_2320_DELTAW_MATERIAL_SOURCE_VECTOR_STATUS.csv | true | true | delta_w acquisition status | false |
| SRC2321_05_2201_projection | 2201_projection | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_2201_ALPHA_CG_PROJECTION_GATE.csv | true | true | original alpha_cg gate | false |
| SRC2321_06_2201_alpha_source | 2201_alpha_source | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_2201_ALPHA_CG_SOURCE_ROW.csv | true | true | Cassini source target | false |
| SRC2321_07_2201_matrix | 2201_matrix | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_2201_PPN_COMPONENT_OWNER_MATRIX.csv | true | true | PPN component matrix | false |
| SRC2321_08_2202_projection | 2202_projection | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_2202_ALPHA_CG_PROJECTION_ATTEMPT.csv | true | true | projection attempt | false |
| SRC2321_09_2202_effective | 2202_effective | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_2202_ALPHA_CG_EFFECTIVE_ROW.csv | true | true | effective alpha formula | false |
| SRC2321_10_1853_norm | 1853_norm | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_1853_CANONICAL_X_NORMALIZATION_DERIVATION.csv | true | true | conditional canonical normalization | false |
| SRC2321_11_1853_range | 1853_range | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_1853_RANGE_TRANSFER_DERIVATION.csv | true | true | conditional range transfer | false |
| SRC2321_12_1853_gate | 1853_gate | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_1853_ZX_MX2_INPUT_GATE.csv | true | true | Z_X/M_X2 input gate | false |
| SRC2321_13_1854_extract | 1854_extract | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_1854_ZX_MX2_EXTRACTION_RESULT.csv | true | true | Z_X/M_X2 extraction result | false |
| SRC2321_14_2161_lambda | 2161_lambda | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_2161_NX_LAMBDA_EXTRACTION_ATTEMPT.csv | true | true | N_X/lambda extraction | false |
| SRC2321_15_2161_hessian | 2161_hessian | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_2161_PARENT_HESSIAN_INPUT_AUDIT.csv | true | true | parent Hessian audit | false |
| SRC2321_16_2161_vector | 2161_vector | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_2161_PPN_VECTOR_ENVELOPE.csv | true | true | PPN vector envelope | false |
| SRC2321_17_2162_clause | 2162_clause | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_2162_PARENT_X_ACTION_CLAUSE_ATTEMPT.csv | true | true | parent X action clause attempt | false |
| SRC2321_18_2162_vector | 2162_vector | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_2162_PPN_VECTOR_FILL.csv | true | true | PPN vector fill | false |
| SRC2321_19_2319_delta | 2319_delta | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_2319_DELTA_W_ACQUISITION_STATUS.csv | true | true | delta_w anchor | false |
| SRC2321_20_2319_runner | 2319_runner | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_2319_SOURCE_BACKED_FINITE_COUPLING_ROWS_NONCLAIM.csv | true | true | finite-coupling runner | false |

## alpha_cg Projection Blocker Audit

| row_id | projection_clause | current_status | fill_attempt | strongest_result | blocks_score | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| ACG2321_0_common_frame | universal common matter frame | NOT_PARENT_SIGNED | searched 2201/2202/2162; no parent matter-frame theorem | none | true | false |
| ACG2321_1_same_branch | same-branch Xhat owner | MISSING_PARENT_OWNER | 2161/2162 supply closure/action-clause scaffold only | one-branch owner remains a required parent-action signature | true | false |
| ACG2321_2_ZX | canonical normalization | RELATION_FILLED_VALUE_MISSING | imported 1853 exact conditional N_X=1/sqrt(Z_X) | normalization law fixed; parent-owned positive numeric Z_X still absent | true | false |
| ACG2321_3_lambda_SPPN | range/screening transfer | LAMBDA_RELATION_FILLED_SPPN_MISSING | imported 1853 exact conditional lambda_X=sqrt(Z_X/M_X^2) | range law fixed if Z_X and M_X^2 are owned; Cassini S_PPN geometry map still missing | true | false |
| ACG2321_4_tau_PPN | PPN projection coefficient | MISSING_TAU_PPN | searched 1852/1853/2161/2201/2202/2320 current rows | tau_PPN appears only as a required symbol in the effective alpha object | true | false |
| ACG2321_5_vector_tails | other PPN vector tails | VECTOR_TAILS_UNCONTROLLED | 2161/2162 vector envelope retained | disformal, non-Hilbert, support/domain, boundary, and readout tails all remain acquisition rows | true | false |
| ACG2321_6_verdict | alpha_cg score-ready component | NOT_SCORE_READY_BUT_NORMAL_FORM_LOCKED | filled exact conditional normal form only | alpha_cg^PPN normal form is now the only allowed score object; raw c_g remains forbidden | true | false |

## Conditional Fill Rows

| row_id | object | conditional_formula | mathematical_status | missing_for_score | score_ready | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| CF2321_0_NX | canonical projection factor | N_X=dXhat/d(varphi/M_Pl)=1/sqrt(Z_X) | EXACT_IF_PARENT_QUADRATIC_BLOCK_OWNED | parent-owned positive Z_X with units and same-branch owner | false | false |
| CF2321_1_lambda | range | lambda_X=sqrt(Z_X/M_X^2) | EXACT_IF_PARENT_HESSIAN_ZX_MX2_OWNED | parent-owned Z_X, M_X^2, units, sign, and range conversion | false | false |
| CF2321_2_alpha_cg_normal_form | PPN common conformal component | alpha_cg^PPN=tau_PPN*S_PPN(lambda_X,env)*c_g/sqrt(Z_X) | NORMAL_FORM_LOCKED_NONCLAIM | same-branch c_g, Z_X, M_X^2, lambda_X, S_PPN, tau_PPN, common frame, and tail bounds | false | false |
| CF2321_3_raw_cg_refusal | raw c_g | raw c_g is not invariant under Xhat rescaling | FORBIDDEN_SCORE_OBJECT | not applicable; use alpha_cg normal form instead | false | false |

## delta_w Material Vector Acquisition Ledger

| row_id | needed_object | current_evidence | missing_input | next_evidence_needed | status | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| DWA2321_0_bound_anchor | delta_w comparator/product anchor | MICROSCOPE/source product ceiling exists from 1694/2319 | MTS material/source prediction vector | material composition basis and source-current response tensor | ANCHOR_EXISTS_PREDICTION_MISSING | false |
| DWA2321_1_material_vector | Ti/Pt or source-test material vector | 2320 marks material tensor missing | species/material basis, charge weights, nuclear/electronic/mass response decomposition | parent-signed map from coefficient shifts to MICROSCOPE test-mass response | ACQUISITION_REQUIRED | false |
| DWA2321_2_tau_readout | tau_WEP/readout transfer | no score-ready tau/readout row | experiment geometry/readout projection and no-cancellation rule | tau_WEP operator or theorem-zero readout tail | ACQUISITION_REQUIRED | false |
| DWA2321_3_verdict | delta_w score object | held as fallback lane | complete material/source vector plus tau/readout transfer | build after alpha_cg projection normal form has been locked | DEFERRED_NONCLAIM | false |

## Score Readiness

| row_id | test_object | progress | remaining_blocker | score_ready | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| READY2321_0_alpha_normal_form | alpha_cg^PPN normal form | conditional formula locked | same-branch owner, Z_X, M_X^2, S_PPN, tau_PPN, common frame, vector tails | false | false |
| READY2321_1_delta_w | delta_w material/source vector | acquisition ledger refreshed | material vector and tau/readout missing | false | false |
| READY2321_2_local_GR | local GR/Newton recovery | raw c_g loophole closed by normal-form rule | full no-cancellation PPN residual vector not theorem-zero or numerically bounded | false | false |

## Claim Gates

| row_id | gate | passed | claim_effect | valid_for_claim |
| --- | --- | --- | --- | --- |
| CG2321_0_sources | source paths and needles valid | true | audit reproducible | false |
| CG2321_1_normal_form | alpha_cg normal form locked | true | only conditional score object is allowed | false |
| CG2321_2_alpha_score | alpha_cg score-ready | false | score blocked by missing parent inputs and tail controls | false |
| CG2321_3_delta_w_score | delta_w material/source vector score-ready | false | delta_w remains acquisition-only | false |
| CG2321_4_local_GR_Newton | local GR/Newton recovery derived | false | still a target, not a result | false |

## Refusal Runner

| row_id | claim | allowed | reason | blocking_rows | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| REF2321_0_raw_cg | Cassini bounds raw c_g | false | raw c_g changes under Xhat rescaling; the invariant object is tau_PPN*S_PPN*c_g/sqrt(Z_X) | CF2321_3_raw_cg_refusal;ACG2321_2_ZX;ACG2321_4_tau_PPN | false |
| REF2321_1_relation_promotion | N_X or lambda_X is now numeric | false | 2321 imports exact relations only; Z_X and M_X^2 remain missing | CF2321_0_NX;CF2321_1_lambda;ACG2321_2_ZX;ACG2321_3_lambda_SPPN | false |
| REF2321_2_alpha_score | alpha_cg is score-ready | false | normal form is locked but projection coefficients and vector-tail closure are missing | ACG2321_0_common_frame through ACG2321_6_verdict | false |
| REF2321_3_local_GR | 2321 derives local GR/Newton | false | 2321 closes a score-object loophole; it does not complete the full local residual vector | READY2321_2_local_GR;CG2321_4_local_GR_Newton | false |

## Next Target

| row_id | next_target | why | claim_status | valid_for_claim |
| --- | --- | --- | --- | --- |
| NEXT2321_0 | 2322-Y5-R2FR-tau-PPN-or-common-frame-parent-signature.md | 2321 locks the invariant alpha_cg normal form; the least-circular next proof target is either tau_PPN/readout projection from the parent matter frame or the common-frame theorem that makes alpha_cg the actual Cassini leg. | nonclaim_private_next_step | false |
| NEXT2321_1 | 2322b-Y5-R2FR-delta-w-material-vector-source-pack.md | fallback/acquisition lane if alpha_cg tau/common-frame proof stalls; build material vector without pretending it is local-GR recovery. | fallback_nonclaim | false |

## Branch Copies

| row_id | source_csv | branch_copy_path | copy_exists | row_count | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| COPY2321_0_alpha_blockers | source-intake\mts_residuals\P8_Y5_PARENT_QLOC_2321_ALPHA_CG_PROJECTION_BLOCKER_AUDIT.csv | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\beta-source\docs\ALPHA_CG_PROJECTION_BLOCKER_AUDIT_2321_NONCLAIM.csv | true | 7 | false |
| COPY2321_1_conditional | source-intake\mts_residuals\P8_Y5_PARENT_QLOC_2321_CONDITIONAL_FILL_ROWS.csv | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\rab-sector\acquisition-queue\JR2321_ALPHA_CG_CONDITIONAL_FILL_NONCLAIM.csv | true | 4 | false |
| COPY2321_2_delta_acquisition | source-intake\mts_residuals\P8_Y5_PARENT_QLOC_2321_DELTAW_MATERIAL_VECTOR_ACQUISITION_LEDGER.csv | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\rab-sector\acquisition-queue\JR2321_DELTAW_MATERIAL_VECTOR_ACQUISITION_NONCLAIM.csv | true | 4 | false |
| COPY2321_3_score_readiness | source-intake\mts_residuals\P8_Y5_PARENT_QLOC_2321_SCORE_READINESS.csv | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\microscope\branch_locked_wep\residuals\alpha_cg_score_readiness_nonclaim_2321.csv | true | 3 | false |

## Validation

| row_id | status | detail | valid_for_claim |
| --- | --- | --- | --- |
| VAL2321_00_sources_exist | PASS | every cited source path exists | false |
| VAL2321_01_needles_found | PASS | all source needles were found | false |
| VAL2321_02_normal_form_locked | PASS | alpha_cg PPN normal form row exists | false |
| VAL2321_03_blockers_preserved | PASS | all alpha_cg blockers still block scoring | false |
| VAL2321_04_delta_acquisition | PASS | delta_w remains acquisition-only | false |
| VAL2321_05_readiness_blocks_score | PASS | all readiness rows remain non-score-ready | false |
| VAL2321_06_claim_gates_block | PASS | local GR/Newton claim remains blocked | false |
| VAL2321_07_refusals_block | PASS | refusal runner blocks premature claims | false |
| VAL2321_08_next_target | PASS | next target selected | false |
| VAL2321_09_branch_copies_parse | PASS | branch copies exist and parse | false |
| VAL2321_10_no_claim_flags | PASS | no generated row is valid_for_claim=true | false |
| VAL2321_11_formalization_untouched_by_2321 | PASS | no 2321 checkpoint output appears in formalization-workbench | false |
| VAL2321_OVERALL | PASS | 2321 fills only the exact conditional alpha_cg normal form, keeps all projection coefficients nonclaim, preserves delta_w acquisition status, and blocks local-GR/Newton claims. | false |
