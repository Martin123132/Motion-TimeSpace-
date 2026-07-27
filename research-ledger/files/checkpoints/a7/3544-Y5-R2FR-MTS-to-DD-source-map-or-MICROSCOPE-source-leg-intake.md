# 3544 - MTS-to-DD Source Map Or MICROSCOPE Source-Leg Intake

## Summary
- **Map shape derived:** `D_mhat_source` and `D_e_source` are now explicit symbolic combinations of MTS source-coupling components.
- **Main formula:** `eta_TiPt ~= 3.330000e-03*D_mhat_source + 2.040000e-03*D_e_source`.
- **Single-channel ceilings:** `|D_mhat_source| <= 8.408408e-13` and `|D_e_source| <= 1.372549e-12` if each acts alone.
- **No-cancellation envelope:** `3.330000e-03*|D_mhat_source| + 2.040000e-03*|D_e_source| <= 2.800000e-15`.
- **No claim:** source leg, units, K values, component values, alloy policy and sign convention are still missing.

## MTS-to-DD Map
From the existing 2440 projection structure:

`D_mhat_source := K_m_block*delta_w_block + K_m_shadow*delta_w_shadow + K_m_nonHilbert*c_nonHilbert`

and

`D_e_source := K_e_alpha*b_alpha + K_e_frame*b_g`.

The retained non-DD tail is

`eta_tail = K_projector_WEP*c_projector + tail_abs_WEP`.

The scoreable nonclaim envelope is therefore

`|3.330000e-03*D_mhat_source| + |2.040000e-03*D_e_source| + |eta_tail| <= 2.8e-15`,

unless a parent theorem justifies signed cancellation.

## Source Register
| source_id | path | exists | role | valid_for_claim |
| --- | --- | --- | --- | --- |
| script_3544 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\scripts\Y5_R2FR_3544_MTS_to_DD_source_map_or_MICROSCOPE_source_leg_intake.py | True | 3544 generator | False |
| doc_3543 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\3543-Y5-R2FR-constructor-exhaustion-or-first-species-source-coefficient-fill.md | True | constructor/species coefficient handoff | False |
| next_3543 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3543_NEXT_TARGET.csv | True | selected MTS-to-DD/source-leg target | False |
| first_fill_3543 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3543_FIRST_SPECIES_SOURCE_FILL.csv | True | first Ti/Pt species-source inequality | False |
| material_inputs_3543 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3543_TIPT_MATERIAL_INPUTS.csv | True | 3543 Ti/Pt material input copy | False |
| material_basis_2440 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_2440_WEP_MATERIAL_SENSITIVITY_BASIS.csv | True | source-backed Ti/Pt DD-like material contrast | False |
| k_projection_2440 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_2440_WEP_K_VECTOR_PROJECTION.csv | True | prior MTS expanded WEP projection formula | False |
| source_leg_blockers_2440 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_2440_WEP_SOURCE_LEG_BLOCKERS.csv | True | remaining source-leg/alloy/map blockers | False |
| local_bounds | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\local_bounds\local_bound_claims.csv | True | MICROSCOPE Ti/Pt bound row | False |
| mu_extra_vector | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_MU_EXTRA_SOURCE_NORMALIZATION_COEFFICIENT_VECTOR.csv | True | source-normalization residual channels | False |
| em_ellj_residual | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_EM_ellJ_source_current_owner_residual_law.csv | True | source-current denominator residual decomposition | False |

## MTS-to-DD Map Rows
| map_id | target | formula | known_inputs | missing_inputs | status | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| MAP3544_0_DD_material_formula | eta_TiPt | eta_TiPt ~= DeltaQ_mhat(Pt-Ti)*D_mhat_source + DeltaQ_e(Pt-Ti)*D_e_source | DeltaQ_mhat=3.330000e-03; DeltaQ_e=2.040000e-03 | D_mhat_source; D_e_source; source leg; sign/alloy policy | SOURCE_BACKED_MATERIAL_MAP_READY | False |
| MAP3544_1_MTS_mhat_block | D_mhat_source | D_mhat_source := K_m_block*delta_w_block + K_m_shadow*delta_w_shadow + K_m_nonHilbert*c_nonHilbert | symbolic component structure from WKP2440_1 | K_m_block; K_m_shadow; K_m_nonHilbert; component values; units; source leg | SYMBOLIC_MTS_TO_DD_MAP_WRITTEN | False |
| MAP3544_2_MTS_electromagnetic_block | D_e_source | D_e_source := K_e_alpha*b_alpha + K_e_frame*b_g | symbolic component structure from WKP2440_1 | K_e_alpha; K_e_frame; b_alpha; b_g; units; source leg | SYMBOLIC_MTS_TO_DD_MAP_WRITTEN | False |
| MAP3544_3_orphan_projector_tail | non-DD residual tail | eta_tail = K_projector_WEP*c_projector + tail_abs_WEP | tail structure from WKP2440_1 | K_projector_WEP; c_projector; tail_abs_WEP; relation theorem showing whether these collapse into DD basis | RETAINED_OUTSIDE_TWO_CHARGE_DD_BASIS | False |
| MAP3544_4_absolute_no_cancellation | absolute envelope | \|DeltaQ_mhat*K_m_block*delta_w_block\|+\|DeltaQ_mhat*K_m_shadow*delta_w_shadow\|+\|DeltaQ_mhat*K_m_nonHilbert*c_nonHilbert\|+\|DeltaQ_e*K_e_alpha*b_alpha\|+\|DeltaQ_e*K_e_frame*b_g\|+\|K_projector_WEP*c_projector\|+\|tail_abs_WEP\| <= eta_bound | DeltaQ_mhat; DeltaQ_e; eta_bound | all component values and K values | ABSOLUTE_ENVELOPE_FORM_READY | False |

## Single-Channel Ceilings
| ceiling_id | assumption | inequality | rounded_bound_value | legacy_1sigma_value | units | score_ready | mts_prediction_ready | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CEIL3544_0_D_mhat_only | D_e_source=0 and all tail/projector terms zero | \|D_mhat_source\| <= 8.408408e-13 | 8.408408408408e-13 | 8.245963963964e-13 | dimensionless effective source-coupling coefficient | True | False | False |
| CEIL3544_1_D_e_only | D_mhat_source=0 and all tail/projector terms zero | \|D_e_source\| <= 1.372549e-12 | 1.372549019608e-12 | 1.346032352941e-12 | dimensionless effective source-coupling coefficient | True | False | False |
| CEIL3544_2_epsilon_species_unit | unit projection eta_source_TiPt=\|epsilon_species_Pt-epsilon_species_Ti\| | \|epsilon_species_Pt_minus_Ti\| <= 2.800000e-15 | 2.800000000000e-15 | 2.745906000000e-15 | dimensionless | True | False | False |
| CEIL3544_3_absolute_two_charge_envelope | no cancellation credit between D_mhat_source and D_e_source | 3.330000e-03*\|D_mhat_source\| + 2.040000e-03*\|D_e_source\| <= 2.800000e-15 | 2.800000000000e-15 | 2.745906000000e-15 | dimensionless eta envelope | True | False | False |

## Source-Leg Intake
| intake_id | needed_object | definition | required_inputs | current_status | why_needed | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| SL3544_0_compressed_D_definition | compressed effective D_i_source | D_i_source already includes the Earth/source leg and orbit normalization used by the MICROSCOPE Ti/Pt comparison. | declare whether D_i_source is compressed; units; sign convention; no-cancellation policy | USABLE_FOR_DD_LIKE_NONCLAIM_CONSTRAINT | allows the inequality to be used as a bound on effective coefficients without proving Earth composition | False |
| SL3544_1_factorized_Earth_source | Earth/source charge leg | D_i_source = alpha_i^test * alpha_source or equivalent factorized source-charge product. | Earth composition/source-body charge; orbit normalization; active-vs-inertial mass split; parent Hilbert source lock | MISSING | required to turn effective D_i_source into a fundamental MTS source coupling | False |
| SL3544_2_alloy_policy | Ti/Pt material policy | decide whether elemental Ti and Pt charges are enough or whether exact Ti alloy and Pt/Rh test-mass corrections are required. | MICROSCOPE material composition; isotope/alloy correction policy; uncertainty handling | MISSING_POLICY | keeps the material contrast approximate rather than overclaimed | False |
| SL3544_3_sign_convention | Ti-minus-Pt vs Pt-minus-Ti convention | fix the sign convention for eta_TiPt and material contrast rows. | declared ordering; absolute-envelope policy; source-bound row convention | ABSOLUTE_ONLY_SAFE | signed scoring is impossible until convention is fixed | False |
| SL3544_4_MTS_units | MTS component units and normalization | K_m/K_e coefficients map MTS residual variables into dimensionless DD-like couplings. | q unit; source normalization denominator; component relation theorem; parent units | MISSING | required for MTS prediction-ready status | False |

## Component Template
| component_id | dd_channel | projection_weight | component_formula | coefficient_needed | value_needed | units | current_status | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CMP3544_0_delta_w_block | D_mhat_source | 3.330000e-03 | DeltaQ_mhat*K_m_block*delta_w_block | K_m_block | delta_w_block | dimensionless after parent source normalization | MISSING_K_AND_VALUE | False |
| CMP3544_1_delta_w_shadow | D_mhat_source | 3.330000e-03 | DeltaQ_mhat*K_m_shadow*delta_w_shadow | K_m_shadow | delta_w_shadow | dimensionless after parent source normalization | MISSING_K_AND_VALUE | False |
| CMP3544_2_nonHilbert_current | D_mhat_source | 3.330000e-03 | DeltaQ_mhat*K_m_nonHilbert*c_nonHilbert | K_m_nonHilbert | c_nonHilbert | dimensionless after parent source normalization | MISSING_K_AND_VALUE | False |
| CMP3544_3_b_alpha | D_e_source | 2.040000e-03 | DeltaQ_e*K_e_alpha*b_alpha | K_e_alpha | b_alpha | dimensionless after EM/source normalization | MISSING_K_AND_VALUE | False |
| CMP3544_4_b_g | D_e_source | 2.040000e-03 | DeltaQ_e*K_e_frame*b_g | K_e_frame | b_g | dimensionless after frame/source normalization | MISSING_K_AND_VALUE | False |
| CMP3544_5_projector | outside_two_charge_basis | 1 | K_projector_WEP*c_projector | K_projector_WEP | c_projector | dimensionless eta contribution | MISSING_K_AND_VALUE_RETAIN_ABSOLUTE | False |
| CMP3544_6_tail | outside_two_charge_basis | 1 | tail_abs_WEP | none if directly bounded | tail_abs_WEP | dimensionless eta contribution | MISSING_VALUE_RETAIN_ABSOLUTE | False |

## Decision Ledger
| decision_id | decision | rationale | effect | claim_allowed |
| --- | --- | --- | --- | --- |
| DEC3544_0_symbolic_map_written | MTS-to-DD map is now explicit symbolically. | D_mhat_source and D_e_source are written as MTS component combinations from the existing 2440 formula. | The next missing objects are K values, component values, units and source leg, not the map shape. | False |
| DEC3544_1_single_channel_ceilings | Single-channel ceilings are now calculable. | MICROSCOPE Ti/Pt bound divided by material contrast gives direct ceilings for effective D_mhat and D_e. | D_mhat_source must be below about 8.41e-13 if alone; D_e_source below about 1.37e-12 if alone. | False |
| DEC3544_2_source_leg_not_fundamental | Compressed D_i coefficients are usable as nonclaim effective constraints, not fundamental MTS couplings. | Earth/source leg and parent Hilbert source lock remain missing. | No source-coupling pass, but the empirical branch is now score-shaped. | False |
| DEC3544_3_next | Fill one K/component value or acquire source-leg/alloy inputs next. | That is the shortest path from symbolic map to an actual MTS score row. | 3545 should target K_e_alpha/b_alpha or Earth/source leg intake. | False |

## Canonical Status
| status_id | quantity | value | meaning | claim_effect | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| STAT3544_0_map | MTS_to_DD_map | symbolic_map_ready_values_missing | D_mhat_source and D_e_source are expressed as MTS component combinations but not numeric | not prediction-ready | False |
| STAT3544_1_ceilings | single_channel_ceilings | D_mhat<=8.408e-13; D_e<=1.373e-12 | rounded MICROSCOPE Ti/Pt source bound gives effective one-channel constraints | nonclaim empirical target | False |
| STAT3544_2_source_leg | MICROSCOPE_source_leg | compressed_nonclaim_or_factorized_missing | effective D_i can be bounded, but fundamental MTS coupling needs Earth/source leg | source-coupling pass blocked | False |
| STAT3544_3_next | next_best_target | first_K_value_or_source_leg_intake | fill one MTS component projection or acquire the source/alloy/sign inputs | next empirical bridge | False |

## Next Target
| next_doc | next_script | objective | success_gate | why_next | claim_allowed |
| --- | --- | --- | --- | --- | --- |
| 3545-Y5-R2FR-first-DD-K-value-or-MICROSCOPE-source-leg-acquisition.md | scripts/Y5_R2FR_3545_first_DD_K_value_or_MICROSCOPE_source_leg_acquisition.py | Try to fill the first MTS-to-DD projection coefficient/value pair, preferably K_e_alpha*b_alpha or K_m_block*delta_w_block; if not, build the Earth/source-leg and alloy/sign acquisition rows needed for MICROSCOPE scoring. | Either one component contribution in the absolute envelope has a sourced value with units, or the source-leg/alloy/sign blockers are converted into concrete acquisition tasks. | 3544 made the map and ceilings explicit; scoring now needs a real K/value or source-leg input. | False |

## Validation
| check_id | passed | detail | valid_for_claim |
| --- | --- | --- | --- |
| VAL3544_0_sources_exist | True | all cited source paths exist | False |
| VAL3544_1_symbolic_map_present | True | D_mhat, D_e and absolute-envelope maps present | False |
| VAL3544_2_single_channel_ceilings_present | True | single-channel and absolute-envelope ceilings present | False |
| VAL3544_3_source_leg_intake_present | True | compressed/factorized source leg, alloy and sign rows present | False |
| VAL3544_4_component_template_covers_terms | True | all MTS component terms covered | False |
| VAL3544_5_no_claims_promoted | True | no source-coupling/WEP/local-GR claim promoted | False |
| VAL3544_6_next_target_selected | True | 3545 K-value/source-leg target selected | False |
| VAL3544_7_csvs_parse | True | source_register; dd_map; ceilings; source_leg; components; decision_ledger; status; canonical_status; next_target | False |
| VAL3544_8_outputs_stay_in_post_checkpoint_work | True | root=D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work | False |
| VAL3544_9_formalization_workbench_not_targeted | True | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench | False |
| VAL3544_SUMMARY | True | PASS | False |
