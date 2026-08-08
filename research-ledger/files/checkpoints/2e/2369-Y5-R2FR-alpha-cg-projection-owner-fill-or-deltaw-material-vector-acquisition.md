# 2369 - alpha_cg Projection Owner Fill Or delta_w Material Vector Acquisition

## Result

The local-GR score object is now narrowed:

`alpha_cg^PPN = tau_PPN * S_PPN(lambda_X, env) * c_g / sqrt(Z_X)`.

Raw `c_g` is forbidden because it is not invariant under `Xhat` rescaling.  This is a useful lock.  But it is not a pass: the same-branch owner, `Z_X`, `M_X^2`, `S_PPN`, common frame, and vector/readout tails remain open.

The best mathematical fill is `tau_PPN=1`, but only in a parent-signed common-frame scalar-tensor branch.  That branch is not signed here, so `tau_PPN=1` cannot be used in active scoring.  The active obstruction is now `alpha_readout`: calibration, PPN-gauge, source-feedback and protocol tails.

## alpha_cg Projection Audit

| row_id | projection_clause | current_status | effect_or_blocker |
| --- | --- | --- | --- |
| ACG2369_0_normal_form | alpha_cg^PPN | NORMAL_FORM_LOCKED_NONCLAIM | raw c_g is forbidden as a score object |
| ACG2369_1_common_frame | universal common matter frame | NOT_PARENT_SIGNED | blocks treating alpha_cg as actual Cassini leg |
| ACG2369_2_same_branch | same-branch Xhat owner | MISSING_PARENT_OWNER | prevents mixing closure and finite rows |
| ACG2369_3_ZX | canonical normalization | RELATION_FILLED_VALUE_MISSING | positive numeric/source-backed Z_X absent |
| ACG2369_4_lambda_SPPN | range/screening transfer | LAMBDA_RELATION_FILLED_SPPN_MISSING | M_X^2 and Cassini geometry map absent |
| ACG2369_5_tau_PPN | PPN projection coefficient | EXACT_CONDITIONAL_NOT_ACTIVE | active branch lacks common-frame/readout signature |
| ACG2369_6_vector_tails | other PPN vector tails | VECTOR_TAILS_UNCONTROLLED | must be zero-proved or bounded |
| ACG2369_7_verdict | alpha_cg score-ready component | NOT_SCORE_READY | move to common-frame/readout-tail proof or bound |

## tau_PPN / Common Frame Audit

| row_id | target | result | effect_or_gap |
| --- | --- | --- | --- |
| TAU2369_0_common_frame_premise | universal common matter frame | CONDITIONAL_PREMISE_ONLY | parent ordinary-matter signature not derived |
| TAU2369_1_tau_one | tau_PPN normalization | EXACT_CONDITIONAL_TAU_EQUALS_ONE | not active until common-frame branch is signed |
| TAU2369_2_screening_split | tau versus screening | DECOMPOSITION_LOCKED | prevents hiding screening inside tau |
| TAU2369_3_readout_tail | observed PPN readout | NOT_DERIVED | tail remains explicit |
| TAU2369_4_verdict | set tau_PPN=1 in active scoring | NOT_ALLOWED_YET | retain alpha_readout and projection blockers |

## delta_w Acquisition Status

| row_id | needed_object | status | missing_input |
| --- | --- | --- | --- |
| DWA2369_0_bound_anchor | delta_w comparator/product anchor | ANCHOR_EXISTS_PREDICTION_MISSING | MTS material/source prediction vector missing |
| DWA2369_1_material_vector | Ti/Pt or source-test material vector | ACQUISITION_REQUIRED | parent-signed map from coefficient shifts to test-mass response missing |
| DWA2369_2_tau_readout | tau_WEP/readout transfer | ACQUISITION_REQUIRED | tau_WEP operator/readout tail theorem missing |
| DWA2369_3_verdict | delta_w score object | DEFERRED_NONCLAIM | build after alpha_cg projection normal form path is settled |

## Readout Tail Matrix

| row_id | component | current_status | missing_for_bound |
| --- | --- | --- | --- |
| ART2369_0_alpha_readout | alpha_readout | RETAINED_NONCLAIM_COMPONENT | numeric/source-backed tail values or theorem-zero certificates missing |
| ART2369_1_source_feedback | C_feedback | NORMAL_FORM_DERIVED_VALUES_MISSING | operator norms and epsilon_sigma_A missing |
| ART2369_2_protocol_tail | C_protocol | CLOSURE_OR_SOURCE_REQUIRED | parent declaration or finite bound missing |
| ART2369_3_commutator_zero | source/readout commutator zero route | EXACT_CONDITIONAL_ZERO_UNSIGNED | sector descent certificates missing |
| ART2369_4_no_cancellation | absolute PPN readout envelope | ENVELOPE_ACTIVE_VALUES_MISSING | all component values/theorem-zero rows missing |
| ART2369_5_verdict | active PPN obstruction | READOUT_TAIL_SELECTED_NEXT | next target is zero proof or first alpha_readout bound |

## Route Selection

| row_id | route | rank | decision | reason |
| --- | --- | --- | --- | --- |
| DEC2369_0_alpha_cg | alpha_cg PPN component owner | 1 | NORMAL_FORM_LOCKED_SCORE_BLOCKED | best current local-GR test object, but projection owner/common-frame/readout blockers remain |
| DEC2369_1_tau | set tau_PPN=1 | 3 | KEEP_CONDITIONAL_NOT_ACTIVE | exact only in parent-signed common-frame scalar-tensor branch |
| DEC2369_2_delta_w | delta_w material/source vector | 2 | RETAIN_FALLBACK_ACQUISITION | needs material vector and tau/readout transfer |
| DEC2369_3_readout_tail | alpha_readout zero proof or first bound | 1 | SELECT_NEXT_TARGET | common-frame theorem stalls on readout/projector/support descent |
| DEC2369_4_no_source_only | NoSourceOnlySpeciesSlot syntax proof | 2 | PARALLEL_CLEANER_ROUTE | could forbid relative source weights before they become readout tails |
| DEC2369_5_empirical | score local-GR vector | 5 | DEFER | component vector is not theorem-zero or bounded |

## Next Target

| row_id | next_file | success_condition | fallback_condition |
| --- | --- | --- | --- |
| NEXT2369_0_selected | 2370-Y5-R2FR-readout-tail-zero-proof-or-first-alpha-readout-bound.md | prove projector/support/readout descent enough to set alpha_readout=0, or fill a first source-backed alpha_readout tail bound row | if readout zero/bound cannot be sourced, attempt the parallel NoSourceOnlySpeciesSlot syntax proof while keeping alpha_cg and delta_w nonclaim |
| NEXT2369_1_parallel | 2370b-Y5-R2FR-NoSourceOnlySpeciesSlot-parent-syntax-proof.md | derive parent syntax excluding source-only species slots, or stage finite delta_w/source-weight rows | retain delta_w/source weights as nonclaim finite priors |

## Generated Files

- `source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2369_SOURCE_REGISTER.csv`
- `source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2369_ALPHA_CG_PROJECTION_AUDIT.csv`
- `source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2369_TAU_PPN_COMMON_FRAME_AUDIT.csv`
- `source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2369_DELTAW_ACQUISITION_STATUS.csv`
- `source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2369_READOUT_TAIL_MATRIX.csv`
- `source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2369_SCORE_READINESS.csv`
- `source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2369_DECISION_LEDGER.csv`
- `source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2369_CLAIM_GATES.csv`
- `source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2369_REFUSAL_RUNNER.csv`
- `source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2369_NEXT_TARGET.csv`
- `source-intake/mts_residuals/P8_Y5_BRR545_2369_VALIDATION.csv`

## Practical Status

This is a good narrowing step.  We are no longer waving at PPN in general: the branch has a legal score object and a named obstruction.  Next target is to either prove the readout/support/projector tail is zero or put a first bound on `alpha_readout`.  `delta_w` remains a live fallback, not a shortcut.
