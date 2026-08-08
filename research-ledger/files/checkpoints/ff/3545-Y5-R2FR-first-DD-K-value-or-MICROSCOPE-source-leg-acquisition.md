# 3545 — Y5/R2FR first DD K-value or MICROSCOPE source-leg acquisition

## Verdict

- **No first sourced numeric `K`/component product was found.** The alpha/source and Delta-w files are not empty, but they remain symbolic, missing-input, or nonclaim rows.
- **Useful forward result:** future component values now have hard gates: mhat products must satisfy `|K_m * component| <= 8.408408e-13`, EM products must satisfy `|K_e * component| <= 1.372549e-12`, and projector/tail terms must satisfy `<= 2.800000e-15` at eta level.
- **Claim status:** blocked. This is a private coupling bridge, not a WEP/local-GR pass.

## Extractor logic

The point of this checkpoint is to stop treating the coupling gap as a vibe. It scans the existing source hierarchy and records whether any row already supplies a claimable parent-owned numeric value. A row only counts as useful if it is numeric, sourced, and not marked `MISSING`, `SYMBOLIC`, `NONCLAIM`, or `NOT_NUMERIC`.

## Component gates

| component_id | target_product | eta_term | single_product_ceiling | score_ready | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| CMP3545_0_delta_w_block | K_m_block*delta_w_block | 3.330000e-03*K_m_block*delta_w_block | 8.408408408408e-13 | False | False |
| CMP3545_1_delta_w_shadow | K_m_shadow*delta_w_shadow | 3.330000e-03*K_m_shadow*delta_w_shadow | 8.408408408408e-13 | False | False |
| CMP3545_2_nonHilbert_current | K_m_nonHilbert*c_nonHilbert | 3.330000e-03*K_m_nonHilbert*c_nonHilbert | 8.408408408408e-13 | False | False |
| CMP3545_3_b_alpha | K_e_alpha*b_alpha | 2.040000e-03*K_e_alpha*b_alpha | 1.372549019608e-12 | False | False |
| CMP3545_4_b_g | K_e_frame*b_g | 2.040000e-03*K_e_frame*b_g | 1.372549019608e-12 | False | False |
| CMP3545_5_projector | K_projector_WEP*c_projector | K_projector_WEP*c_projector | 2.800000000000e-15 | False | False |
| CMP3545_6_tail | tail_abs_WEP | tail_abs_WEP | 2.800000000000e-15 | False | False |

## K/value hunt

| hunt_id | target_component | numeric_value_found | blocking_issue | next_action |
| --- | --- | --- | --- | --- |
| HUNT3545_0_Ke_alpha_balpha | K_e_alpha*b_alpha | False | MISSING_ALPHA_SOURCE_COMPOSITION_MAP; MISSING_K_e_alpha projection; z_lambda/fixed Maxwell kinetic owner unsigned | derive or source K_e_alpha and b_alpha in one normalization, then test against \|K_e_alpha*b_alpha\| ceiling |
| HUNT3545_1_Km_block_delta_w_block | K_m_block*delta_w_block | False | MISSING_PARENT_DELTAW_VALUES; MISSING_COMPONENT_BASIS; MISSING_ARENA_PROJECTION_KERNELS | derive theorem-zero for species/block prefactors or source a parent numeric Delta_w vector and arena projection |
| HUNT3545_2_Ke_frame_bg | K_e_frame*b_g | False | MISSING_FRAME_SOURCE_NORMALIZATION; MISSING_PREFERRED_FRAME_LIGHT_CONE_BOUND_MAPPING | use EM Hodge/light-cone branch only after visible metric/Hodge owner is fixed or bounded |
| HUNT3545_3_projector_tail | K_projector_WEP*c_projector + tail_abs_WEP | False | MISSING_PROJECTOR_COLLAPSE_THEOREM; MISSING_TAIL_ABSOLUTE_BOUND | either prove projector/tail collapse into DD basis or keep absolute eta-level tail ceiling |

## Acquisition queue

| acquisition_id | target | needed_object | current_status | minimum_acceptance |
| --- | --- | --- | --- | --- |
| ACQ3545_0_alpha_source_map | K_e_alpha*b_alpha | alpha source-composition map in the same normalization as Ti/Pt DD charge DeltaQ_e | ACQUISITION_REQUIRED | numeric K_e_alpha and b_alpha, source path, units, sign convention, valid_for_claim=True source row |
| ACQ3545_1_deltaw_parent_vector | K_m_block*delta_w_block | parent Delta_w block value or theorem-zero plus component basis | ACQUISITION_REQUIRED | parent value/bound/zero theorem, material projection kernel, common-mode removal, units |
| ACQ3545_2_MICROSCOPE_factorized_source_leg | source leg | Earth/source-body charge vector, orbit normalization, active-vs-inertial source convention | ACQUISITION_REQUIRED | factorized row replacing compressed D_i_source with explicit source-body factors |
| ACQ3545_3_alloy_policy | Ti/Pt test masses | MICROSCOPE alloy/isotope/material correction policy | ACQUISITION_REQUIRED | sourced Ti alloy and Pt/Rh composition policy, or justified pure-element approximation with uncertainty |
| ACQ3545_4_sign_and_units | projection convention | Pt-minus-Ti or Ti-minus-Pt sign, q normalization, and source denominator | ACQUISITION_REQUIRED | single written convention used by all component rows and runners |

## Decision ledger

| decision_id | question | decision | basis | next_action |
| --- | --- | --- | --- | --- |
| DEC3545_0_first_K_value | Was a first sourced numeric MTS-to-DD K/value product found? | NO | inspected alpha/source, Delta_w, and WEP K-projection rows retain missing/symbolic/nonclaim status | target K_e_alpha*b_alpha first, because it is the cleanest EM/source bridge |
| DEC3545_1_component_gates | Did 3545 add a useful forward step? | YES_COMPONENT_CEILINGS_INSTALLED | mhat product ceilings <= 8.408408e-13; e product ceilings <= 1.372549e-12; projector/tail eta ceilings <= 2.800000e-15 | fill one product value or prove a theorem-zero, instead of circling the full coupling cloud |
| DEC3545_2_source_leg | Can compressed MICROSCOPE D rows be used as public claim rows? | NO | compressed D_i_source rows hide Earth/source leg, orbit normalization, alloy policy, and sign/units convention | acquire factorized source-leg rows if K_e_alpha*b_alpha cannot be derived directly |

## Validation

| validation_id | passes | status | detail |
| --- | --- | --- | --- |
| VAL3545_0_required_sources_exist | True | PASS | 3544/2440/local bound sources needed for this gate exist |
| VAL3545_1_generated_csvs_parse | True | PASS | 9 generated CSV files parse with DictReader |
| VAL3545_2_component_rows_nonclaim | True | PASS | all component score rows remain score_ready=False and valid_for_claim=False until sourced values exist |
| VAL3545_3_formalization_workbench_untouched | True | PASS | 3545 generated outputs only inside post-checkpoint-work |
| VAL3545_4_claim_block_retained | True | PASS | no R10/WEP/PPN/local-GR claim is made by this checkpoint |

## Status

| checkpoint | claim_allowed | first_numeric_K_value_found | usable_forward_result | next_target |
| --- | --- | --- | --- | --- |
| 3545 | False | False | component product ceilings and concrete acquisition queue | 3546-Y5-R2FR-Ke-alpha-balpha-source-value-or-EM-alpha-coupling-bound-intake.md |

## Next target

Move to `3546-Y5-R2FR-Ke-alpha-balpha-source-value-or-EM-alpha-coupling-bound-intake.md`. The best route is the EM alpha/source bridge first: either derive/source `K_e_alpha*b_alpha` in one normalization, or produce a narrow acquisition pack that says exactly which EM/source rows must be filled.

Generated UTC: 2026-06-29T10:52:30.518279+00:00