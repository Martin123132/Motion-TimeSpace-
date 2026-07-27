# 1000 Y5 R10 Delta-ref Source Coefficient Strict Provenance Runner

**Status:** strict refusal runner installed; no Delta_ref, RC994_0, FB554_0, R10, PPN, or local-GR pass is claimed.

**Claim ceiling:** this checkpoint is plumbing only. It makes the source coefficient harder to fake; it does not solve the coefficient.

## Source Register

| source_id | path | role | needle | exists | needle_found | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| S1000_0_handoff_doc | 999-Y5-R10-Bref-fixed-branch-selector-or-Delta-ref-source-coefficient-provenance.md | 999 handoff selecting strict provenance runner | 1000-Y5-R10-Delta-ref-source-coefficient-strict-provenance-runner.md | true | true | false |
| S1000_1_coefficient_provenance | source-intake/mts_residuals/P8_Y5_R10_999_DELTA_REF_SOURCE_COEFFICIENT_PROVENANCE.csv | finite coefficient provenance requirements | DCP999_0_partial_source_derivative | true | true | false |
| S1000_2_runner_readiness | source-intake/mts_residuals/P8_Y5_R10_999_COEFFICIENT_RUNNER_READINESS.csv | schema-ready but values-not-ready state | DCR999_0_schema_ready | true | true | false |
| S1000_3_parent_selector_contract | source-intake/mts_residuals/P8_Y5_R10_999_PARENT_SELECTOR_CONTRACT.csv | future parent selector contract | FBC999_0_selector_function | true | true | false |
| S1000_4_selector_attempt | source-intake/mts_residuals/P8_Y5_R10_999_FIXED_BRANCH_SELECTOR_ATTEMPT.csv | failed fixed-branch selector theorem attempt | FBS999_7_verdict | true | true | false |
| S1000_5_component_template | source-intake/mts_residuals/P8_Y5_R10_998_DELTA_REF_SOURCE_COMPONENT_TEMPLATE.csv | source component formula and required columns | DSC998_0_component_schema | true | true | false |
| S1000_6_refusal_precedent | source-intake/mts_residuals/P8_Y5_R10_998_STRICT_REFUSAL_LEDGER.csv | prior refusal for unsourced source calibration | REF998_1_no_source_calibration | true | true | false |
| S1000_7_derivative_audit | source-intake/mts_residuals/P8_Y5_R10_997_DERIVATIVE_COMPONENT_AUDIT.csv | partial_source Delta_ref identified as derivative component | DVC997_0_source | true | true | false |
| S1000_8_no_cancellation | source-intake/mts_residuals/P8_Y5_R10_994_DELTAH_NO_CANCELLATION_ENVELOPE.csv | absolute-value no-cancellation guard | DHE994_1_no_cancellation | true | true | false |

## Strict Input Schema

| schema_id | field | required_input | units_requirement | source_requirement | rejects | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| SIS1000_0_partial_source_Delta_ref | partial_source_Delta_ref | finite numeric derivative or theorem_zero=true with theorem_zero_authority=PARENT_SIGNED_TRUE | partial_source_units and Delta_ref_units must be explicit | source_path exists and equation_ref identifies the parent equation | MISSING_NUMERIC_DERIVATIVE_OR_THEOREM_ZERO; closure-zero; fitted-zero; inferred-zero | false |
| SIS1000_1_Delta_source_scale | Delta_source_scale | finite positive numeric scale for the source variation being tested | Delta_source_scale_units must be explicit and same-frame | source parameter definition and extraction/source path are required | chosen-to-shrink residual; unitless placeholder; MISSING_SOURCE_SCALE | false |
| SIS1000_2_Bref_rule | B_ref_rule | fixed formula and branch id for B_ref before source/readout is known | formula must declare frame and normalization convention | parent selector equation or finite provenance source path | hidden observed-GM labels; source labels; post-fit branch selection; MISSING_PARENT_BREF_RULE | false |
| SIS1000_3_MHref | M_H_ref | finite positive denominator in the same reference frame as Delta_ref | M_H_ref_units required | definition source path and equation_ref required | orbital-GM import; fitted denominator; MISSING_M_H_REF | false |
| SIS1000_4_theorem_zero_switch | theorem_zero_authority | PARENT_SIGNED_TRUE if theorem_zero=true | units still recorded for the zeroed derivative slot | parent theorem path, selector equation, and component certificate | zero-by-closure; notation-zero; silence of the boundary projector | false |
| SIS1000_5_no_cancellation | no_cancellation_guard | ABS_PRODUCT_NO_SIGN_CANCELLATION | absolute finite ratio abs(partial_source_Delta_ref * Delta_source_scale) / M_H_ref | no sign cancellation may be used to pass a local bound | opposite-sign cancellation; tuned cancellation; branch cancellation | false |

## Candidate Input Template

| candidate_id | purpose | target | formula | partial_source_Delta_ref | Delta_source_scale | B_ref_rule | M_H_ref | theorem_zero | theorem_zero_authority | no_cancellation_guard | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CIR1000_0_missing_derivative | derivative slot has no finite number and no parent-signed zero theorem | Delta_ref_source_component_over_MH | abs(partial_source_Delta_ref * Delta_source_scale)/M_H_ref | MISSING_NUMERIC_DERIVATIVE_OR_THEOREM_ZERO | MISSING_SOURCE_SCALE | MISSING_PARENT_BREF_RULE | MISSING_M_H_REF | false | MISSING_PARENT_SIGNATURE | MISSING_ABSOLUTE_PRODUCT_GUARD | false |
| CIR1000_1_missing_scale | source scale is not defined or sourced | Delta_ref_source_component_over_MH | abs(partial_source_Delta_ref * Delta_source_scale)/M_H_ref | MISSING_NUMERIC_DERIVATIVE_OR_THEOREM_ZERO | MISSING_SOURCE_SCALE | MISSING_PARENT_BREF_RULE | MISSING_M_H_REF | false | MISSING_PARENT_SIGNATURE | MISSING_ABSOLUTE_PRODUCT_GUARD | false |
| CIR1000_2_missing_Bref_rule | B_ref rule is not fixed by parent branch selector | Delta_ref_source_component_over_MH | abs(partial_source_Delta_ref * Delta_source_scale)/M_H_ref | MISSING_NUMERIC_DERIVATIVE_OR_THEOREM_ZERO | MISSING_SOURCE_SCALE | MISSING_PARENT_BREF_RULE | MISSING_M_H_REF | false | MISSING_PARENT_SIGNATURE | MISSING_ABSOLUTE_PRODUCT_GUARD | false |
| CIR1000_3_missing_MHref | same-frame positive M_H_ref denominator is missing | Delta_ref_source_component_over_MH | abs(partial_source_Delta_ref * Delta_source_scale)/M_H_ref | MISSING_NUMERIC_DERIVATIVE_OR_THEOREM_ZERO | MISSING_SOURCE_SCALE | MISSING_PARENT_BREF_RULE | MISSING_M_H_REF | false | MISSING_PARENT_SIGNATURE | MISSING_ABSOLUTE_PRODUCT_GUARD | false |
| CIR1000_4_zero_switch_missing_parent_signature | theorem-zero switch is requested without PARENT_SIGNED_TRUE | Delta_ref_source_component_over_MH | abs(partial_source_Delta_ref * Delta_source_scale)/M_H_ref | MISSING_NUMERIC_DERIVATIVE_OR_THEOREM_ZERO | MISSING_SOURCE_SCALE | MISSING_PARENT_BREF_RULE | MISSING_M_H_REF | true | MISSING_PARENT_SIGNATURE | MISSING_ABSOLUTE_PRODUCT_GUARD | false |
| CIR1000_5_all_missing_live_placeholder | live row remains placeholder-only and cannot be scored | Delta_ref_source_component_over_MH | abs(partial_source_Delta_ref * Delta_source_scale)/M_H_ref | MISSING_NUMERIC_DERIVATIVE_OR_THEOREM_ZERO | MISSING_SOURCE_SCALE | MISSING_PARENT_BREF_RULE | MISSING_M_H_REF | false | MISSING_PARENT_SIGNATURE | MISSING_ABSOLUTE_PRODUCT_GUARD | false |

## Strict Provenance Runner

| runner_id | candidate_id | verdict | score_ready | claim_allowed | computed_abs_ratio | failure_reasons | generated_utc |
| --- | --- | --- | --- | --- | --- | --- | --- |
| RUN1000_0_missing_derivative | CIR1000_0_missing_derivative | REFUSED_MISSING_PROVENANCE_OR_PARENT_SELECTOR | false | false | NOT_SCORED | MISSING_NUMERIC_DERIVATIVE_OR_PARENT_SIGNED_ZERO;MISSING_POSITIVE_DELTA_SOURCE_SCALE;MISSING_POSITIVE_SAME_FRAME_M_H_REF;MISSING_SOURCE_PARAMETER;MISSING_DELTA_SOURCE_SCALE_UNITS;MISSING_PARTIAL_SOURCE_UNITS;MISSING_DELTA_REF_UNITS;MISSING_M_H_REF_UNITS;MISSING_EQUATION_REF;MISSING_FIXED_BRANCH_ID;MISSING_PARENT_BREF_RULE;MISSING_EXISTING_SOURCE_PATH;MISSING_NO_CANCELLATION_GUARD;VALID_FOR_CLAIM_FALSE | 2026-06-14T03:29:57.888324+00:00 |
| RUN1000_1_missing_scale | CIR1000_1_missing_scale | REFUSED_MISSING_PROVENANCE_OR_PARENT_SELECTOR | false | false | NOT_SCORED | MISSING_NUMERIC_DERIVATIVE_OR_PARENT_SIGNED_ZERO;MISSING_POSITIVE_DELTA_SOURCE_SCALE;MISSING_POSITIVE_SAME_FRAME_M_H_REF;MISSING_SOURCE_PARAMETER;MISSING_DELTA_SOURCE_SCALE_UNITS;MISSING_PARTIAL_SOURCE_UNITS;MISSING_DELTA_REF_UNITS;MISSING_M_H_REF_UNITS;MISSING_EQUATION_REF;MISSING_FIXED_BRANCH_ID;MISSING_PARENT_BREF_RULE;MISSING_EXISTING_SOURCE_PATH;MISSING_NO_CANCELLATION_GUARD;VALID_FOR_CLAIM_FALSE | 2026-06-14T03:29:57.888348+00:00 |
| RUN1000_2_missing_Bref_rule | CIR1000_2_missing_Bref_rule | REFUSED_MISSING_PROVENANCE_OR_PARENT_SELECTOR | false | false | NOT_SCORED | MISSING_NUMERIC_DERIVATIVE_OR_PARENT_SIGNED_ZERO;MISSING_POSITIVE_DELTA_SOURCE_SCALE;MISSING_POSITIVE_SAME_FRAME_M_H_REF;MISSING_SOURCE_PARAMETER;MISSING_DELTA_SOURCE_SCALE_UNITS;MISSING_PARTIAL_SOURCE_UNITS;MISSING_DELTA_REF_UNITS;MISSING_M_H_REF_UNITS;MISSING_EQUATION_REF;MISSING_FIXED_BRANCH_ID;MISSING_PARENT_BREF_RULE;MISSING_EXISTING_SOURCE_PATH;MISSING_NO_CANCELLATION_GUARD;VALID_FOR_CLAIM_FALSE | 2026-06-14T03:29:57.888360+00:00 |
| RUN1000_3_missing_MHref | CIR1000_3_missing_MHref | REFUSED_MISSING_PROVENANCE_OR_PARENT_SELECTOR | false | false | NOT_SCORED | MISSING_NUMERIC_DERIVATIVE_OR_PARENT_SIGNED_ZERO;MISSING_POSITIVE_DELTA_SOURCE_SCALE;MISSING_POSITIVE_SAME_FRAME_M_H_REF;MISSING_SOURCE_PARAMETER;MISSING_DELTA_SOURCE_SCALE_UNITS;MISSING_PARTIAL_SOURCE_UNITS;MISSING_DELTA_REF_UNITS;MISSING_M_H_REF_UNITS;MISSING_EQUATION_REF;MISSING_FIXED_BRANCH_ID;MISSING_PARENT_BREF_RULE;MISSING_EXISTING_SOURCE_PATH;MISSING_NO_CANCELLATION_GUARD;VALID_FOR_CLAIM_FALSE | 2026-06-14T03:29:57.888371+00:00 |
| RUN1000_4_zero_switch_missing_parent_signature | CIR1000_4_zero_switch_missing_parent_signature | REFUSED_MISSING_PROVENANCE_OR_PARENT_SELECTOR | false | false | NOT_SCORED | MISSING_NUMERIC_DERIVATIVE_OR_PARENT_SIGNED_ZERO;THEOREM_ZERO_REJECTED_WITHOUT_PARENT_SIGNED_TRUE;MISSING_POSITIVE_DELTA_SOURCE_SCALE;MISSING_POSITIVE_SAME_FRAME_M_H_REF;MISSING_SOURCE_PARAMETER;MISSING_DELTA_SOURCE_SCALE_UNITS;MISSING_PARTIAL_SOURCE_UNITS;MISSING_DELTA_REF_UNITS;MISSING_M_H_REF_UNITS;MISSING_EQUATION_REF;MISSING_FIXED_BRANCH_ID;MISSING_PARENT_BREF_RULE;MISSING_EXISTING_SOURCE_PATH;MISSING_NO_CANCELLATION_GUARD;VALID_FOR_CLAIM_FALSE | 2026-06-14T03:29:57.888381+00:00 |
| RUN1000_5_all_missing_live_placeholder | CIR1000_5_all_missing_live_placeholder | REFUSED_MISSING_PROVENANCE_OR_PARENT_SELECTOR | false | false | NOT_SCORED | MISSING_NUMERIC_DERIVATIVE_OR_PARENT_SIGNED_ZERO;MISSING_POSITIVE_DELTA_SOURCE_SCALE;MISSING_POSITIVE_SAME_FRAME_M_H_REF;MISSING_SOURCE_PARAMETER;MISSING_DELTA_SOURCE_SCALE_UNITS;MISSING_PARTIAL_SOURCE_UNITS;MISSING_DELTA_REF_UNITS;MISSING_M_H_REF_UNITS;MISSING_EQUATION_REF;MISSING_FIXED_BRANCH_ID;MISSING_PARENT_BREF_RULE;MISSING_EXISTING_SOURCE_PATH;MISSING_NO_CANCELLATION_GUARD;VALID_FOR_CLAIM_FALSE | 2026-06-14T03:29:57.888391+00:00 |

## Refusal Ledger

| refusal_id | candidate_id | refusal | why | required_exit | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| REF1000_0_missing_derivative | CIR1000_0_missing_derivative | REFUSED_MISSING_PROVENANCE_OR_PARENT_SELECTOR | MISSING_NUMERIC_DERIVATIVE_OR_PARENT_SIGNED_ZERO;MISSING_POSITIVE_DELTA_SOURCE_SCALE;MISSING_POSITIVE_SAME_FRAME_M_H_REF;MISSING_SOURCE_PARAMETER;MISSING_DELTA_SOURCE_SCALE_UNITS;MISSING_PARTIAL_SOURCE_UNITS;MISSING_DELTA_REF_UNITS;MISSING_M_H_REF_UNITS;MISSING_EQUATION_REF;MISSING_FIXED_BRANCH_ID;MISSING_PARENT_BREF_RULE;MISSING_EXISTING_SOURCE_PATH;MISSING_NO_CANCELLATION_GUARD;VALID_FOR_CLAIM_FALSE | finite sourced coefficient provenance or parent-signed theorem-zero selector | false | false |
| REF1000_1_missing_scale | CIR1000_1_missing_scale | REFUSED_MISSING_PROVENANCE_OR_PARENT_SELECTOR | MISSING_NUMERIC_DERIVATIVE_OR_PARENT_SIGNED_ZERO;MISSING_POSITIVE_DELTA_SOURCE_SCALE;MISSING_POSITIVE_SAME_FRAME_M_H_REF;MISSING_SOURCE_PARAMETER;MISSING_DELTA_SOURCE_SCALE_UNITS;MISSING_PARTIAL_SOURCE_UNITS;MISSING_DELTA_REF_UNITS;MISSING_M_H_REF_UNITS;MISSING_EQUATION_REF;MISSING_FIXED_BRANCH_ID;MISSING_PARENT_BREF_RULE;MISSING_EXISTING_SOURCE_PATH;MISSING_NO_CANCELLATION_GUARD;VALID_FOR_CLAIM_FALSE | finite sourced coefficient provenance or parent-signed theorem-zero selector | false | false |
| REF1000_2_missing_Bref_rule | CIR1000_2_missing_Bref_rule | REFUSED_MISSING_PROVENANCE_OR_PARENT_SELECTOR | MISSING_NUMERIC_DERIVATIVE_OR_PARENT_SIGNED_ZERO;MISSING_POSITIVE_DELTA_SOURCE_SCALE;MISSING_POSITIVE_SAME_FRAME_M_H_REF;MISSING_SOURCE_PARAMETER;MISSING_DELTA_SOURCE_SCALE_UNITS;MISSING_PARTIAL_SOURCE_UNITS;MISSING_DELTA_REF_UNITS;MISSING_M_H_REF_UNITS;MISSING_EQUATION_REF;MISSING_FIXED_BRANCH_ID;MISSING_PARENT_BREF_RULE;MISSING_EXISTING_SOURCE_PATH;MISSING_NO_CANCELLATION_GUARD;VALID_FOR_CLAIM_FALSE | finite sourced coefficient provenance or parent-signed theorem-zero selector | false | false |
| REF1000_3_missing_MHref | CIR1000_3_missing_MHref | REFUSED_MISSING_PROVENANCE_OR_PARENT_SELECTOR | MISSING_NUMERIC_DERIVATIVE_OR_PARENT_SIGNED_ZERO;MISSING_POSITIVE_DELTA_SOURCE_SCALE;MISSING_POSITIVE_SAME_FRAME_M_H_REF;MISSING_SOURCE_PARAMETER;MISSING_DELTA_SOURCE_SCALE_UNITS;MISSING_PARTIAL_SOURCE_UNITS;MISSING_DELTA_REF_UNITS;MISSING_M_H_REF_UNITS;MISSING_EQUATION_REF;MISSING_FIXED_BRANCH_ID;MISSING_PARENT_BREF_RULE;MISSING_EXISTING_SOURCE_PATH;MISSING_NO_CANCELLATION_GUARD;VALID_FOR_CLAIM_FALSE | finite sourced coefficient provenance or parent-signed theorem-zero selector | false | false |
| REF1000_4_zero_switch_missing_parent_signature | CIR1000_4_zero_switch_missing_parent_signature | REFUSED_MISSING_PROVENANCE_OR_PARENT_SELECTOR | MISSING_NUMERIC_DERIVATIVE_OR_PARENT_SIGNED_ZERO;THEOREM_ZERO_REJECTED_WITHOUT_PARENT_SIGNED_TRUE;MISSING_POSITIVE_DELTA_SOURCE_SCALE;MISSING_POSITIVE_SAME_FRAME_M_H_REF;MISSING_SOURCE_PARAMETER;MISSING_DELTA_SOURCE_SCALE_UNITS;MISSING_PARTIAL_SOURCE_UNITS;MISSING_DELTA_REF_UNITS;MISSING_M_H_REF_UNITS;MISSING_EQUATION_REF;MISSING_FIXED_BRANCH_ID;MISSING_PARENT_BREF_RULE;MISSING_EXISTING_SOURCE_PATH;MISSING_NO_CANCELLATION_GUARD;VALID_FOR_CLAIM_FALSE | finite sourced coefficient provenance or parent-signed theorem-zero selector | false | false |
| REF1000_5_all_missing_live_placeholder | CIR1000_5_all_missing_live_placeholder | REFUSED_MISSING_PROVENANCE_OR_PARENT_SELECTOR | MISSING_NUMERIC_DERIVATIVE_OR_PARENT_SIGNED_ZERO;MISSING_POSITIVE_DELTA_SOURCE_SCALE;MISSING_POSITIVE_SAME_FRAME_M_H_REF;MISSING_SOURCE_PARAMETER;MISSING_DELTA_SOURCE_SCALE_UNITS;MISSING_PARTIAL_SOURCE_UNITS;MISSING_DELTA_REF_UNITS;MISSING_M_H_REF_UNITS;MISSING_EQUATION_REF;MISSING_FIXED_BRANCH_ID;MISSING_PARENT_BREF_RULE;MISSING_EXISTING_SOURCE_PATH;MISSING_NO_CANCELLATION_GUARD;VALID_FOR_CLAIM_FALSE | finite sourced coefficient provenance or parent-signed theorem-zero selector | false | false |

## Claim Gate

| gate_id | claim | gate_pass | reason | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| CG1000_0_Delta_ref_source_component | Delta_ref source component is zero or locally bounded | false | strict runner refuses every current placeholder row | false | false |
| CG1000_1_RC994_0 | RC994_0 residual current passes | false | Delta_ref source component remains unsigned and unbounded | false | false |
| CG1000_2_FB554_0_local_GR | FB554_0/local-GR branch passes | false | local R10 residual source coefficient is still blocked | false | false |
| CG1000_3_runner_guardrail | runner enforces no zero-by-closure and no hidden cancellation | true | all current rows are refused unless strict provenance or parent theorem appears | false | false |

## Decision Ledger

| decision_id | decision | reason | effect | valid_for_claim |
| --- | --- | --- | --- | --- |
| DEC1000_0_runner_installed | keep current Delta_ref source rows nonclaim | the runner now blocks missing derivative, scale, B_ref rule, M_H_ref, source path, theorem-zero authority, and cancellation guard | future rows can be smoke-tested without accidentally promoting R10/local-GR claims | false |
| DEC1000_1_no_theorem_zero_without_parent | do not accept theorem_zero=true unless theorem_zero_authority=PARENT_SIGNED_TRUE | closure preference and notation silence are not derivations | zero proof must be supplied by a parent action selector or component certificate | false |
| DEC1000_2_next_derivative_target | move from source derivative to radial/surface derivative route | 997 identifies remaining derivative components; 1000 has guarded the source component | 1001 should try the radius/surface-term theorem or stage a radial-profile source row | false |

## Validation

| check_id | result | detail | generated_utc |
| --- | --- | --- | --- |
| V1000_0_sources_exist | pass | all source paths exist and needles are present | 2026-06-14T03:30:42.360198+00:00 |
| V1000_1_schema_core_fields | pass | strict schema includes derivative, scale, B_ref, M_H_ref, theorem-zero, and no-cancellation fields | 2026-06-14T03:30:42.360202+00:00 |
| V1000_2_candidate_rows_nonclaim | pass | candidate template rows remain valid_for_claim=false | 2026-06-14T03:30:42.360205+00:00 |
| V1000_3_runner_refuses_placeholders | pass | runner refuses every current placeholder row | 2026-06-14T03:30:42.360208+00:00 |
| V1000_4_theorem_zero_guard | pass | theorem_zero=true is refused without PARENT_SIGNED_TRUE | 2026-06-14T03:30:42.360211+00:00 |
| V1000_5_refusal_ledger_nonclaim | pass | refusal ledger mirrors runner and keeps claims false | 2026-06-14T03:30:42.360214+00:00 |
| V1000_6_claim_gates_blocked | pass | Delta_ref, RC994_0, FB554_0, and local-GR claims stay blocked | 2026-06-14T03:30:42.360216+00:00 |
| V1000_7_decision_written | pass | next derivative target decision is written | 2026-06-14T03:30:42.360219+00:00 |
| V1000_8_next_target_written | pass | 1001 target row is present and nonclaim | 2026-06-14T03:30:42.360222+00:00 |
| V1000_9_formalization_untouched | pass | formalization-workbench modified-file count since script start is 0 | 2026-06-14T03:30:42.360224+00:00 |
| V1000_SUMMARY | pass | 1000 strict provenance runner validation summary | 2026-06-14T03:30:42.360186+00:00 |

## Next Target

| next_target | objective | include | exclude | valid_for_claim |
| --- | --- | --- | --- | --- |
| 1001-Y5-R10-Bref-radius-surface-term-theorem-or-Delta-ref-radial-profile-row.md | derive the radius/surface contribution to Delta_ref as zero, or stage a source-backed radial profile row without claiming a pass | partial_r Delta_ref, boundary surface term, radial profile, same-frame M_H_ref, source/equation paths, no-cancellation guard | zero-by-boundary-silence, fitted radius profile, RC994_0 pass, FB554_0 pass, local-GR claim, GitHub action | false |
