# 2322 - tau_PPN Or Common Frame Parent Signature

## Summary

2322 closes a small but important loophole. In the strict universal common-frame scalar-tensor branch,
`tau_PPN` is not an extra fit knob: once ordinary matter sees one metric
`g_m=A_g(Xhat)^2 g_E`, the canonical coupling is `alpha_eff=c_g/sqrt(Z_X)` and the standard PPN gamma law uses that
coupling directly. In that branch, `tau_PPN=1` by normalization.

But that is conditional only. The active MTS branch still cannot set `tau_PPN=1`, because the parent common-frame
matter action, coefficient functor, readout closure, measured-GM/source normalization, and PPN gauge transform are
not signed. So the current score object stays
`alpha_cg^PPN=tau_PPN*S_PPN(lambda_X,env)*c_g/sqrt(Z_X)` unless the common-frame signature is proved.

This is progress, chume: not fireworks, but a cleaner blade. We now know exactly what theorem would let `tau_PPN`
collapse to `1`, and exactly why we are not allowed to use it yet.

## Source Register

| row_id | source_key | source_path | exists | needles_found | source_role | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| SRC2322_00_2321_doc | 2321_doc | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\2321-Y5-R2FR-alpha-cg-projection-owner-fill-or-deltaw-material-vector-acquisition.md | true | true | 2321 handoff | false |
| SRC2322_01_2321_validation | 2321_validation | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_BRR545_2321_VALIDATION.csv | true | true | 2321 validation | false |
| SRC2322_02_2321_conditional | 2321_conditional | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_2321_CONDITIONAL_FILL_ROWS.csv | true | true | alpha_cg normal form | false |
| SRC2322_03_2321_blockers | 2321_blockers | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_2321_ALPHA_CG_PROJECTION_BLOCKER_AUDIT.csv | true | true | tau blocker | false |
| SRC2322_04_2160_scalar | 2160_scalar | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_2160_SCALAR_TENSOR_PPN_MAP.csv | true | true | scalar-tensor PPN map | false |
| SRC2322_05_2160_vector | 2160_vector | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_2160_PPN_RESIDUAL_VECTOR_ENVELOPE.csv | true | true | PPN vector envelope | false |
| SRC2322_06_2160_claims | 2160_claims | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_2160_CLAIM_GATE.csv | true | true | 2160 claim gates | false |
| SRC2322_07_2104_projection | 2104_projection | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_2104_CG_PPN_PROJECTION.csv | true | true | c_g to PPN projection | false |
| SRC2322_08_2104_frame | 2104_frame | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_2104_FRAME_DEGENERACY_CONDITIONS.csv | true | true | frame degeneracy guard | false |
| SRC2322_09_2105_norm | 2105_norm | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_2105_NORMALIZATION_CONTRACT.csv | true | true | normalization contract | false |
| SRC2322_10_2105_runner | 2105_runner | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_2105_GAMMA_RUNNER.csv | true | true | gamma runner refusal | false |
| SRC2322_11_2159_moms | 2159_moms | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_2159_MOMS_SIGNATURE_ATTEMPT.csv | true | true | ordinary matter signature attempt | false |
| SRC2322_12_2159_translation | 2159_translation | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_2159_CG_PPN_TRANSLATION_GATE.csv | true | true | translation gate | false |
| SRC2322_13_2159_claims | 2159_claims | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_2159_LOCAL_CLAIM_GATE.csv | true | true | local claim gates | false |
| SRC2322_14_2318_functor | 2318_functor | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_2318_PARENT_COEFFICIENT_FUNCTOR_CONSTRUCTION_ATTEMPT.csv | true | true | coefficient functor | false |
| SRC2322_15_2318_obligations | 2318_obligations | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_2318_FUNCTOR_PROOF_OBLIGATION_LEDGER.csv | true | true | functor obligations | false |
| SRC2322_16_2202_effective | 2202_effective | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_2202_ALPHA_CG_EFFECTIVE_ROW.csv | true | true | effective alpha row | false |
| SRC2322_17_2203_readout | 2203_readout | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_2203_ALPHA_READOUT_ROW.csv | true | true | readout component | false |
| SRC2322_18_2203_gm | 2203_gm | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_2203_MEASURED_GM_OBSTRUCTION_VECTOR.csv | true | true | measured GM obstruction | false |
| SRC2322_19_2208_blockers | 2208_blockers | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_2208_PPN_BLOCKER_LEDGER.csv | true | true | PPN blocker ledger | false |
| SRC2322_20_2208_green | 2208_green | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_2208_PPN_GREEN_OPERATOR_LOWERING.csv | true | true | PPN Green lowering | false |
| SRC2322_21_2210_range | 2210_range | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_2210_RANGE_OPERATOR_DERIVATION.csv | true | true | range owner law | false |

## tau_PPN/Common-Frame Derivation Audit

| row_id | target | attempted_statement | result | why | blocks_score | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| TPA2322_0_common_frame_premise | universal common matter frame | S_matter uses one metric g_m=A_g(Xhat)^2 g_E for ordinary matter, rods, clocks, source masses, and Cassini/Shapiro readout | CONDITIONAL_PREMISE_ONLY | 2160/2104 write the scalar-tensor ansatz; 2159 says parent ordinary-matter signature is not derived | true | false |
| TPA2322_1_tau_standard_scalar_tensor | tau_PPN normalization | in the standard massless unscreened scalar-tensor branch, the PPN gamma law reads gamma-1=-2 alpha_eff^2/(1+alpha_eff^2), so tau_PPN=1 by definition of alpha_eff | EXACT_CONDITIONAL_TAU_EQUALS_ONE | tau is not an extra fitted factor once the common-frame scalar-tensor PPN branch is parent-signed | false | false |
| TPA2322_2_tau_not_screening | separate tau_PPN from S_PPN | tau_PPN is the readout/projection normalization; finite range and screening belong in S_PPN(lambda_X,env) | DECOMPOSITION_LOCKED | 2210 owns the range law conditionally; screening/profile response remains a separate missing input | true | false |
| TPA2322_3_readout_gauge_tail | observed PPN readout | fixed-before-readout, measured-GM, and PPN-gauge maps must not add alpha_readout or calibration tails | NOT_DERIVED | 2203 and 2208 retain readout, measured-GM, source-normalization, and PPN-gauge blockers | true | false |
| TPA2322_4_verdict | active-branch tau_PPN | set tau_PPN=1 in active MTS scoring | NOT_ALLOWED_YET | the equality is exact only inside the parent-signed common-frame scalar-tensor branch; active branch still lacks the parent signature and tail zeroes | true | false |

## Conditional tau Normalization Rows

| row_id | conditional_branch | formula | tau_value | requires | status | score_ready | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CTN2322_0_canonical_alpha | universal common-frame scalar-tensor | alpha_eff=N_X*c_g=c_g/sqrt(Z_X) | tau_PPN=1 | parent-signed common matter frame; canonical Xhat block; no disformal/species/readout tails | EXACT_CONDITIONAL_NORMALIZATION | false | false |
| CTN2322_1_gamma_law | massless/solar-long unscreened scalar-tensor | gamma-1=-2*alpha_eff^2/(1+alpha_eff^2) | no additional tau factor | S_PPN=1 and alpha_vec_tail=0 | STANDARD_CONDITIONAL_RELATION_IMPORTED | false | false |
| CTN2322_2_active_normal_form | current active MTS branch | alpha_cg^PPN=tau_PPN*S_PPN(lambda_X,env)*c_g/sqrt(Z_X) | tau_PPN symbolic | parent matter-frame signature or separate source-backed tau_PPN | ACTIVE_SCORE_OBJECT_REMAINS_SYMBOLIC | false | false |

## Parent Signature Clause Ledger

| row_id | signature_clause | required_statement | current_status | source_basis | blocks_tau_one | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| SIG2322_0_parent_action_object | one parent ordinary-matter action before readout | S_parent selects S_matter once, before projection, fitting, and detector calibration | SCHEMA_AVAILABLE_NOT_DERIVED | MOM2159_0_action_object;OBL2318_0_parent_object | true | false |
| SIG2322_1_universal_metric | one ordinary matter metric | all ordinary matter sees g_m=A_g(Xhat)^2 g_E with no independent disformal/species/shadow metric | NOT_PARENT_SIGNED | CGT2159_0_universal_common_frame;STM2160_0_common_frame_ansatz | true | false |
| SIG2322_2_coeff_functor | no hidden-visible coefficient hom | visible coefficients descend through quotient/fixed representation data only | PARENT_COEFFICIENT_FUNCTOR_NOT_CONSTRUCTED | PCF2318_5_verdict;OBL2318_5_verdict | true | false |
| SIG2322_3_fixed_before_readout | variation before readout | readout maps, detector thresholds, source worldtubes, and measured-GM calibration do not regenerate a PPN tail | RADIATIVE_READOUT_CLOSURE_UNSIGNED | OBL2318_4_readout_closure;ARW2203_0_alpha_readout;MGV2203_7_calibration_PPN_tail | true | false |
| SIG2322_4_ppn_gauge_source | observed PPN gauge and source normalization | weak-field metric is transformed to the observed PPN gauge with fixed G_ref/source mass and no absorbed tail | MISSING_PPN_GAUGE_TRANSFORM_AND_SOURCE_NORMALIZATION | PPNB2208_2_source_normalization;PPNB2208_3_PPN_gauge;PPNL2208_3_source_normalization | true | false |
| SIG2322_5_verdict | common-frame parent signature closes | SIG2322_0 through SIG2322_4 pass together | COMMON_FRAME_SIGNATURE_NOT_DERIVED | 2322 synthesis | true | false |

## Score Object Update

| row_id | score_object | formula | update | score_ready | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| SOU2322_0_allowed_conditional_score_object | alpha_cg^PPN | tau_PPN*S_PPN(lambda_X,env)*c_g/sqrt(Z_X) | tau_PPN can be replaced by 1 only inside the parent-signed standard common-frame scalar-tensor branch | false | false |
| SOU2322_1_forbidden_shortcut | tau_PPN=1 by convention in active branch | not allowed | would smuggle the common-frame/readout theorem as notation | false | false |
| SOU2322_2_local_GR_status | local GR/Newton recovery | requires full absolute PPN residual vector theorem-zero or source-bounded | 2322 reduces one ambiguity but does not score the vector | false | false |

## Claim Gates

| row_id | gate | passed | claim_effect | valid_for_claim |
| --- | --- | --- | --- | --- |
| CG2322_0_sources | source paths and needles valid | true | audit reproducible | false |
| CG2322_1_conditional_tau | tau_PPN=1 derived in strict scalar-tensor common-frame branch | true | conditional theorem only; not active score | false |
| CG2322_2_common_frame_signature | common-frame parent signature signed | false | tau_PPN cannot be set to 1 in active branch | false |
| CG2322_3_readout_tail_zero | readout/gauge/source-normalization tails theorem-zero | false | alpha_readout and calibration tails remain in PPN vector | false |
| CG2322_4_alpha_score | alpha_cg score-ready | false | Z_X, range/S_PPN, common frame, and tails remain missing | false |
| CG2322_5_local_GR_Newton | local GR/Newton recovery derived | false | still a target, not a result | false |

## Refusal Runner

| row_id | claim | allowed | reason | blocking_rows | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| REF2322_0_tau_one_active | set tau_PPN=1 in the active MTS branch | false | tau_PPN=1 is exact only after the common-frame scalar-tensor parent signature and readout/gauge clauses are signed | SIG2322_0 through SIG2322_5 | false |
| REF2322_1_set_SPPN_one | set S_PPN=1 by convention | false | range/screening/profile response is separate from tau_PPN and still depends on parent Z/M/domain/source data | TPA2322_2_tau_not_screening;ROD2210_5_verdict | false |
| REF2322_2_drop_readout_tail | drop alpha_readout and measured-GM calibration tails | false | 2203/2208 keep readout, source-normalization, and PPN gauge as explicit blockers | SIG2322_3_fixed_before_readout;SIG2322_4_ppn_gauge_source | false |
| REF2322_3_local_GR | 2322 derives local GR/Newton | false | 2322 proves a conditional normalization rule, not the full residual-vector theorem | CG2322_5_local_GR_Newton;SOU2322_2_local_GR_status | false |

## Next Target

| row_id | next_target | why | claim_status | valid_for_claim |
| --- | --- | --- | --- | --- |
| NEXT2322_0 | 2323-Y5-R2FR-common-matter-frame-action-signature-or-readout-tail-row.md | 2322 shows tau_PPN=1 is not a free coefficient in the strict common-frame branch; the remaining hard target is proving the parent matter-frame/readout signature or keeping alpha_readout as an explicit PPN component. | nonclaim_private_next_step | false |
| NEXT2322_1 | 2323b-Y5-R2FR-PPN-gauge-source-normalization-tail-bound.md | fallback if the common-frame theorem stalls; bound the gauge/source-normalization/readout tail rather than dropping it. | fallback_nonclaim | false |

## Branch Copies

| row_id | source_csv | branch_copy_path | copy_exists | row_count | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| COPY2322_0_tau_audit | source-intake\mts_residuals\P8_Y5_PARENT_QLOC_2322_TAU_PPN_COMMON_FRAME_DERIVATION_AUDIT.csv | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\beta-source\docs\TAU_PPN_COMMON_FRAME_DERIVATION_AUDIT_2322_NONCLAIM.csv | true | 5 | false |
| COPY2322_1_conditional_tau | source-intake\mts_residuals\P8_Y5_PARENT_QLOC_2322_CONDITIONAL_TAU_NORMALIZATION_ROWS.csv | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\rab-sector\acquisition-queue\JR2322_CONDITIONAL_TAU_NORMALIZATION_NONCLAIM.csv | true | 3 | false |
| COPY2322_2_signature | source-intake\mts_residuals\P8_Y5_PARENT_QLOC_2322_PARENT_SIGNATURE_CLAUSE_LEDGER.csv | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\rab-sector\acquisition-queue\JR2322_PARENT_SIGNATURE_CLAUSE_LEDGER_NONCLAIM.csv | true | 6 | false |
| COPY2322_3_score_update | source-intake\mts_residuals\P8_Y5_PARENT_QLOC_2322_SCORE_OBJECT_UPDATE.csv | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\microscope\branch_locked_wep\residuals\alpha_cg_score_object_update_nonclaim_2322.csv | true | 3 | false |

## Validation

| row_id | status | detail | valid_for_claim |
| --- | --- | --- | --- |
| VAL2322_00_sources_exist | PASS | every cited source path exists | false |
| VAL2322_01_needles_found | PASS | all source needles were found | false |
| VAL2322_02_conditional_tau_one | PASS | strict common-frame tau_PPN=1 conditional row exists | false |
| VAL2322_03_signature_blocks_tau | PASS | common-frame parent signature remains unsigned | false |
| VAL2322_04_score_objects_nonready | PASS | score object updates remain non-score-ready | false |
| VAL2322_05_claim_gates_block | PASS | local GR/Newton claim remains blocked | false |
| VAL2322_06_refusals_block | PASS | refusal runner blocks premature tau/local-GR claims | false |
| VAL2322_07_next_target | PASS | next target selected | false |
| VAL2322_08_branch_copies_parse | PASS | branch copies exist and parse | false |
| VAL2322_09_no_claim_flags | PASS | no generated row is valid_for_claim=true | false |
| VAL2322_10_formalization_untouched_by_2322 | PASS | no 2322 checkpoint output appears in formalization-workbench | false |
| VAL2322_OVERALL | PASS | 2322 derives tau_PPN=1 only as a strict common-frame scalar-tensor conditional, keeps active-branch tau symbolic, preserves readout/source/gauge blockers, and blocks local-GR/Newton claims. | false |
