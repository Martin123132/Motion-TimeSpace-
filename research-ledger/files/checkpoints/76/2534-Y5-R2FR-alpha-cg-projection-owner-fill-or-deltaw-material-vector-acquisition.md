# 2534 - alpha_cg Projection Owner Fill Or delta_w Material Vector Acquisition

**Current verdict:** raw `c_g` is now explicitly rejected as a score object. The legal local-GR comparison object is the invariant normal form `alpha_cg^PPN = tau_PPN S_PPN(lambda_X,env)c_g/sqrt(Z_X)`.

**Main gain:** this closes a real loophole. A rescaling of the hidden field changes `c_g` and `Z_X`, but not `c_g/sqrt(Z_X)`, so the branch can no longer pass or fail by a normalization convention.

**Remaining obstruction:** the normal form is not a pass. The active blockers are same-branch ownership, `Z_X/M_X^2`, `S_PPN`, common-frame/tau activation, and especially the explicit `alpha_readout` tail.

## alpha_cg Projection Audit

| row_id | projection_clause | current_status | effect_or_blocker |
| --- | --- | --- | --- |
| ACG2534_0_rescaling_invariance | canonical invariant coupling | EXACT_NORMALIZATION_LEMMA | raw c_g cannot be scored |
| ACG2534_1_normal_form | alpha_cg^PPN | NORMAL_FORM_LOCKED_NONCLAIM | legal local-GR comparison object is fixed |
| ACG2534_2_common_frame | universal common matter frame | NOT_PARENT_SIGNED | blocks treating alpha_cg as actual Cassini leg |
| ACG2534_3_same_branch | same-branch Xhat owner | MISSING_PARENT_OWNER | prevents mixing closure and finite rows |
| ACG2534_4_ZX_MX | canonical mass/range normalization | RELATIONS_FILLED_VALUES_MISSING | positive numeric/source-backed Z_X and M_X^2 absent |
| ACG2534_5_SPPN | range/screening transfer | SPPN_GEOMETRY_MAP_MISSING | screening cannot be hidden inside tau |
| ACG2534_6_tau_PPN | PPN projection coefficient | EXACT_CONDITIONAL_NOT_ACTIVE | active branch lacks common-frame/readout signature |
| ACG2534_7_readout_vector_tails | other PPN vector tails | VECTOR_TAILS_UNCONTROLLED | must be zero-proved or bounded |
| ACG2534_8_verdict | alpha_cg score-ready component | NOT_SCORE_READY | move to readout-tail zero proof or first bound |

## tau_PPN / Common Frame Audit

| row_id | target | result | effect_or_gap |
| --- | --- | --- | --- |
| TAU2534_0_common_frame_premise | universal common matter frame | CONDITIONAL_PREMISE_ONLY | parent ordinary-matter signature not derived |
| TAU2534_1_tau_one | tau_PPN normalization | EXACT_CONDITIONAL_TAU_EQUALS_ONE | not active until common-frame branch is signed |
| TAU2534_2_screening_split | tau versus screening | DECOMPOSITION_LOCKED | prevents hiding screening inside tau |
| TAU2534_3_readout_tail | observed PPN readout | NOT_DERIVED | tail remains explicit |
| TAU2534_4_verdict | set tau_PPN=1 in active scoring | NOT_ALLOWED_YET | retain alpha_readout and projection blockers |

## delta_w Acquisition Status

| row_id | needed_object | status | missing_input |
| --- | --- | --- | --- |
| DWA2534_0_bound_anchor | delta_w comparator/product anchor | ANCHOR_EXISTS_PREDICTION_MISSING | MTS material/source prediction vector missing |
| DWA2534_1_material_vector | Ti/Pt or source-test material vector | ACQUISITION_REQUIRED | parent-signed map from coefficient shifts to test-mass response missing |
| DWA2534_2_tau_readout | tau_WEP/readout transfer | ACQUISITION_REQUIRED | tau_WEP operator/readout tail theorem missing |
| DWA2534_3_verdict | delta_w score object | DEFERRED_NONCLAIM | build after alpha_cg projection/readout path is settled |

## Readout Tail Matrix

| row_id | component | current_status | missing_for_bound |
| --- | --- | --- | --- |
| ART2534_0_alpha_readout | alpha_readout | RETAINED_NONCLAIM_COMPONENT | numeric/source-backed tail values or theorem-zero certificates missing |
| ART2534_1_source_feedback | C_feedback | NORMAL_FORM_DERIVED_VALUES_MISSING | operator norms and epsilon_sigma_A missing |
| ART2534_2_protocol_tail | C_protocol | CLOSURE_OR_SOURCE_REQUIRED | parent declaration or finite bound missing |
| ART2534_3_commutator_zero | source/readout commutator zero route | EXACT_CONDITIONAL_ZERO_UNSIGNED | sector descent certificates missing |
| ART2534_4_no_cancellation | absolute PPN readout envelope | ENVELOPE_ACTIVE_VALUES_MISSING | all component values/theorem-zero rows missing |
| ART2534_5_verdict | active PPN obstruction | READOUT_TAIL_SELECTED_NEXT | next target is zero proof or first alpha_readout bound |

## Score Readiness

| row_id | test_object | progress | remaining_blocker | score_ready |
| --- | --- | --- | --- | --- |
| READY2534_0_alpha_normal_form | alpha_cg^PPN | invariant normal form locked | same-branch owner, Z_X, M_X^2, S_PPN, tau_PPN, common frame, vector tails | false |
| READY2534_1_tau | tau_PPN | exact conditional tau=1 lemma retained | common-frame scalar-tensor branch and readout-tail zero missing | false |
| READY2534_2_delta_w | delta_w material/source vector | acquisition lane retained | material vector and tau/readout missing | false |
| READY2534_3_readout_tail | alpha_readout | explicit PPN tail retained | Delta_cal, Delta_PPN, C_feedback, C_protocol values or zero certificates missing | false |
| READY2534_4_local_GR | local GR/Newton recovery | raw c_g loophole closed by normal-form rule | full no-cancellation PPN/local residual vector not theorem-zero or bounded | false |

## Route Selection

| row_id | route | rank | decision | reason |
| --- | --- | --- | --- | --- |
| DEC2534_0_alpha_cg | alpha_cg PPN component owner | 1 | NORMAL_FORM_LOCKED_SCORE_BLOCKED | best current local-GR test object, but projection owner/common-frame/readout blockers remain |
| DEC2534_1_tau | set tau_PPN=1 | 3 | KEEP_CONDITIONAL_NOT_ACTIVE | exact only in parent-signed common-frame scalar-tensor branch |
| DEC2534_2_delta_w | delta_w material/source vector | 2 | RETAIN_FALLBACK_ACQUISITION | needs material vector and tau/readout transfer |
| DEC2534_3_readout_tail | alpha_readout zero proof or first bound | 1 | SELECT_NEXT_TARGET | common-frame theorem stalls on readout/projector/support descent |
| DEC2534_4_no_source_only | NoSourceOnlySpeciesSlot syntax proof | 2 | PARALLEL_CLEANER_ROUTE | could forbid relative source weights before they become readout tails |
| DEC2534_5_empirical | score local-GR vector | 5 | DEFER | component vector is not theorem-zero or bounded |

## Claim Gates

| row_id | claim | status | reason |
| --- | --- | --- | --- |
| CG2534_0_raw_cg | raw c_g can be scored | BLOCKED | raw c_g is normalization-gauge dependent |
| CG2534_1_alpha_cg | alpha_cg PPN component score-ready | BLOCKED | same branch owner/common frame/tau/readout/vector tail blockers remain |
| CG2534_2_tau | tau_PPN=1 active branch | BLOCKED | common-frame scalar-tensor branch not parent-signed |
| CG2534_3_delta_w | delta_w material/source vector score-ready | BLOCKED | material response tensor and tau/readout transfer missing |
| CG2534_4_readout | alpha_readout zero or bound ready | BLOCKED | readout/support/projector descent or numeric tail bound missing |
| CG2534_5_local_GR | local GR/Newton reduction derived | BLOCKED | PPN/local residual vector not closed |

## Next Target

| row_id | priority | next_file | success_condition | fallback_condition |
| --- | --- | --- | --- | --- |
| NEXT2534_0_selected | selected | 2535-Y5-R2FR-readout-tail-zero-proof-or-first-alpha-readout-bound.md | prove projector/support/readout descent enough to set alpha_readout=0, or fill a first source-backed alpha_readout tail bound row | if readout zero/bound cannot be sourced, attempt the parallel NoSourceOnlySpeciesSlot syntax proof while keeping alpha_cg and delta_w nonclaim |
| NEXT2534_1_parallel | parallel | 2535b-Y5-R2FR-NoSourceOnlySpeciesSlot-parent-syntax-proof.md | derive parent syntax excluding source-only species slots, or stage finite delta_w/source-weight rows | retain delta_w/source weights as nonclaim finite priors |

## Validation

| row_id | status | detail |
| --- | --- | --- |
| VAL2534_00_required_sources_exist | PASS | all required source paths exist |
| VAL2534_01_required_needles_found | PASS | all source needles found |
| VAL2534_02_outputs_exist | PASS | all 2534 output files written |
| VAL2534_03_csv_parse | PASS | all generated CSV files parse and contain rows |
| VAL2534_04_rescaling_invariance | PASS | raw c_g rescaling issue closed by invariant normal form |
| VAL2534_05_alpha_normal_form | PASS | alpha_cg normal form locked nonclaim |
| VAL2534_06_alpha_not_score_ready | PASS | alpha_cg not score-ready |
| VAL2534_07_tau_conditional | PASS | tau_PPN=1 retained only as conditional |
| VAL2534_08_tau_not_allowed | PASS | active tau_PPN claim blocked |
| VAL2534_09_delta_deferred | PASS | delta_w remains deferred nonclaim |
| VAL2534_10_readout_selected | PASS | alpha_readout/readout tail selected next |
| VAL2534_11_readiness_nonclaim | PASS | all readiness rows remain not score-ready |
| VAL2534_12_next_selected | PASS | 2535 readout-tail target selected |
| VAL2534_13_branch_copies | PASS | all nonclaim branch copies exist |
| VAL2534_14_no_positive_claim_flags | PASS | all generated claim/readiness flags remain negative |
| VAL2534_15_formalization_untouched | PASS | project is not a git worktree here; generator writes only under post-checkpoint-work |
| VAL2534_16_pycache_absent | PASS | scripts __pycache__ absent |
| VAL2534_OVERALL | PASS | 2534 valid: raw c_g rejected, alpha_cg PPN normal form locked nonclaim, tau conditional only, readout-tail route selected |

## Generated Files

- `source-intake/mts_residuals/P8_Y5_NO_SHADOW_2534_SOURCE_REGISTER.csv`
- `source-intake/mts_residuals/P8_Y5_NO_SHADOW_2534_ALPHA_CG_PROJECTION_AUDIT.csv`
- `source-intake/mts_residuals/P8_Y5_NO_SHADOW_2534_TAU_PPN_COMMON_FRAME_AUDIT.csv`
- `source-intake/mts_residuals/P8_Y5_NO_SHADOW_2534_DELTAW_ACQUISITION_STATUS.csv`
- `source-intake/mts_residuals/P8_Y5_NO_SHADOW_2534_READOUT_TAIL_MATRIX.csv`
- `source-intake/mts_residuals/P8_Y5_NO_SHADOW_2534_SCORE_READINESS.csv`
- `source-intake/mts_residuals/P8_Y5_NO_SHADOW_2534_DECISION_LEDGER.csv`
- `source-intake/mts_residuals/P8_Y5_NO_SHADOW_2534_CLAIM_GATES.csv`
- `source-intake/mts_residuals/P8_Y5_NO_SHADOW_2534_REFUSAL_RUNNER.csv`
- `source-intake/mts_residuals/P8_Y5_NO_SHADOW_2534_NEXT_TARGET.csv`
- `source-intake/mts_residuals/P8_Y5_NO_SHADOW_2534_BRANCH_COPIES.csv`
- `source-intake/mts_residuals/P8_Y5_BRR545_2534_VALIDATION.csv`

## Practical Status

This is a useful local-GR narrowing step. We now have a legal PPN comparison variable and a named remaining obstruction. The next derivation target is `alpha_readout`: prove the projector/support/readout tail vanishes, or source a first finite bound. `delta_w_A` remains alive as a fallback, not a shortcut.
