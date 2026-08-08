# 2440 - Y5/R2FR WEP K Vector Material Source Charge Sensitivity Or Delta-w Bound Row

## Result
- 2440 gets a real partial `K_WEP_TiPt` object: the Ti/Pt material contrast factors are source-backed from the Damour-Donoghue dilaton-charge framework.
- In the selected Pt-minus-Ti convention, the approximate two-charge contrast is `DeltaQ_mhat=3.33e-3`, `DeltaQ_e=2.04e-3`.
- MICROSCOPE supplies the empirical `eta_TiPt` anchor, but this still does not bound MTS coefficients until MTS residuals map into DD-like source charges.
- One-component smoke bounds are recorded only as scale diagnostics; they are not claim-ready MTS bounds.
- Next target is 2441: derive the MTS-to-DD charge/source-leg map.

## Source Register
| source_id | source_type | source_path | source_url | path_exists | needles_found | role |
| --- | --- | --- | --- | --- | --- | --- |
| SRC2440_00_2439_handoff | local | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\2439-Y5-R2FR-coupling-projection-matrix-K-vector-and-no-cancellation-envelope.md |  | True | True | fresh handoff selecting WEP K-vector material/source sensitivity |
| SRC2440_01_2438_anchor | local | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_2438_EXTERNAL_BOUND_ANCHOR_CATALOG.csv |  | True | True | MICROSCOPE empirical WEP anchor imported by 2438 |
| SRC2440_02_Damour_Donoghue | external |  | https://arxiv.org/abs/1007.2790 | n/a | True | primary Damour-Donoghue dilaton-charge framework for material sensitivity |
| SRC2440_03_Damour_ONERA_table | external |  | https://www.ihes.fr/~damour/Conferences/ONERA29Jan2013.pdf | n/a | True | source-backed approximate Ti/Pt material contrast values used as WEP K material factors |
| SRC2440_04_MICROSCOPE_final | external |  | https://arxiv.org/abs/2209.15487 | n/a | True | MICROSCOPE final Ti/Pt WEP bound |

## WEP Material Sensitivity Basis
| row_id | material | A | Z | minus_Q_mhat | Q_mhat | Q_e | eta_bound_1sigma | source | source_backed | status | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| WMS2440_0_Ti | Ti | 47.9 | 22 | 10.28e-3 | -10.28e-3 | 2.04e-3 |  | Damour_ONERA_table | True | APPROXIMATE_ISOTOPICALLY_AVERAGED_DD_CHARGE | False |
| WMS2440_1_Pt | Pt | 195.1 | 78 | 6.95e-3 | -6.95e-3 | 4.09e-3 |  | Damour_ONERA_table | True | APPROXIMATE_ISOTOPICALLY_AVERAGED_DD_CHARGE | False |
| WMS2440_2_Pt_minus_Ti | Pt_minus_Ti | n/a | n/a | -3.33e-3 | 3.330000e-03 | 2.040000e-03 |  | Damour_ONERA_vector_PtTi | True | MATERIAL_CONTRAST_READY_SOURCE_LEG_MISSING | False |
| WMS2440_3_MICROSCOPE_bound | TiPt_pair | alloys | alloys | n/a | n/a | n/a | 2.745906e-15 | MICROSCOPE_2022 | True | EMPIRICAL_BOUND_READY_NOT_A_COMPONENT_BOUND | False |

## WEP K Vector Projection
| projection_id | formula | known_inputs | missing_inputs | current_status | score_ready | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| WKP2440_0_DD_material_formula | eta_TiPt ~= DeltaQ_mhat(Pt-Ti)*D_mhat_source + DeltaQ_e(Pt-Ti)*D_e_source in the simplified Damour-Donoghue two-charge model | DeltaQ_mhat=3.330000e-03; DeltaQ_e=2.040000e-03; eta_bound_1sigma=2.745906e-15 | D_mhat_source;D_e_source;MTS_to_DD_charge_map;exact_alloy_composition_policy;source_body_charge | MATERIAL_CONTRAST_DERIVED_SOURCE_LEG_MISSING | False | False |
| WKP2440_1_MTS_expanded_formula | eta_TiPt = DeltaQ_mhat*(K_m_block*delta_w_block + K_m_shadow*delta_w_shadow + K_m_nonHilbert*c_nonHilbert) + DeltaQ_e*(K_e_alpha*b_alpha + K_e_frame*b_g) + K_projector_WEP*c_projector + tail_abs_WEP | DeltaQ_mhat;DeltaQ_e;MICROSCOPE_eta_bound | all K_m/K_e/K_projector values; component relation theorem; q unit; Earth/source leg | MTS_PROJECTION_FORMULA_READY_K_VALUES_MISSING | False | False |
| WKP2440_2_no_cancellation_bound | \|DeltaQ_mhat*K_m_block*delta_w_block\|+\|DeltaQ_mhat*K_m_shadow*delta_w_shadow\|+\|DeltaQ_e*K_e_alpha*b_alpha\|+\|DeltaQ_e*K_e_frame*b_g\|+\|K_projector_WEP*c_projector\|+\|tail_abs_WEP\| <= eta_bound_abs | eta_bound_abs from MICROSCOPE 1sigma quadrature | K values and component values | ABSOLUTE_ENVELOPE_READY_NOT_NUMERIC | False | False |
| WKP2440_3_verdict | K_WEP_TiPt is partially derived: material contrast factors are source-backed, but source/MTS coupling legs are not. | Ti/Pt material charge contrast; MICROSCOPE eta anchor | MTS residual-to-DD charge map and source leg | PARTIAL_K_VECTOR_NOT_CLAIM_READY | False | False |

## Single-Component Smoke Bounds
| row_id | inferred_symbol | material_contrast | eta_bound_1sigma | one_at_a_time_abs_bound | condition | source_backed | score_ready | current_status | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SCS2440_0_D_mhat | D_mhat_source | 3.330000e-03 | 2.745906e-15 | 8.245964e-13 | if D_e_source=all_other_components=0 | True | False | ONE_COMPONENT_SMOKE_ONLY_NOT_MTS_CLAIM | False |
| SCS2440_1_D_e | D_e_source | 2.040000e-03 | 2.745906e-15 | 1.346032e-12 | if D_mhat_source=all_other_components=0 | True | False | ONE_COMPONENT_SMOKE_ONLY_NOT_MTS_CLAIM | False |

## WEP Source-Leg Blockers
| blocker_id | blocker | requirement | current_status | consequence | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| WB2440_0_MTS_to_DD_map | MTS residual to DD charge map | derive D_mhat_source and D_e_source from delta_w_block, delta_w_shadow, b_alpha, b_g, c_projector with parent units | MISSING | blocks MTS coefficient bound | False |
| WB2440_1_source_leg | Earth/source coupling leg | identify source body charge/normalization for MICROSCOPE orbit without importing measured g as proof | MISSING | blocks alpha_source factor | False |
| WB2440_2_alloy_policy | exact alloy/material policy | decide whether approximate Ti/Pt elemental charges are sufficient or require Ti alloy and Pt/Rh composition corrections | MISSING_POLICY | keeps material contrast approximate | False |
| WB2440_3_sign_convention | sign convention | fix Ti-minus-Pt versus Pt-minus-Ti convention consistently with eta(Ti,Pt) | MISSING | only absolute smoke bounds safe | False |
| WB2440_4_no_cancellation | component no-cancellation | do not use DD two-charge cancellation to hide MTS source-shadow/projector tails | POLICY_SET | absolute envelope retained | False |
| WB2440_5_parent_relation | component relation theorem | prove whether b_alpha, b_g, delta_w and shadow coefficients collapse to fewer DD-like parameters or remain independent | MISSING | total envelope cannot shrink | False |

## Claim Gates
| claim_id | claim | gate_status | reason | gate_pass | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| CG2440_0_material_contrast | Ti/Pt material contrast factors are source-backed | PASS_NONCLAIM | Damour table/vector supplies approximate material charges | True | False |
| CG2440_1_eta_anchor | MICROSCOPE eta anchor is source-backed | PASS_NONCLAIM | 2438 and MICROSCOPE source provide eta bound | True | False |
| CG2440_2_K_WEP_complete | K_WEP_TiPt complete | BLOCKED | MTS-to-DD charge map, source leg, exact material policy and signs are missing | False | False |
| CG2440_3_WEP_score | WEP coefficient bound can score | BLOCKED | single-component smoke bounds are conditional and not MTS coefficients | False | False |
| CG2440_4_local_GR | local GR/Newton/WEP pass | BLOCKED | WEP projection is only one coupling gate and remains nonclaim | False | False |

## Decision Ledger
| decision_id | decision | rationale | consequence | valid_for_claim |
| --- | --- | --- | --- | --- |
| DEC2440_0_real_gain | MATERIAL_CONTRAST_PARTIALLY_DERIVED | Ti/Pt WEP material sensitivity is no longer blank; the DD contrast vector gives real source-backed K material factors. | use these as partial WEP K entries | False |
| DEC2440_1_no_claim | NO_WEP_SCORE_YET | MTS source legs and residual-to-charge map are missing, so MICROSCOPE eta cannot be called a delta_w or b_alpha bound. | valid_for_claim remains false | False |
| DEC2440_2_smoke_bounds | ONE_COMPONENT_SMOKE_BOUNDS_ALLOWED_ONLY_AS_DIAGNOSTIC | D_mhat and D_e one-at-a-time values show scale, not proof. | do not use as MTS claim | False |
| DEC2440_3_next | MAP_MTS_TO_DD_CHARGE_NEXT | the missing object is now specific: D_mhat_source and D_e_source in terms of MTS residual components. | select 2441 | False |
| DEC2440_4_public | NO_GITHUB_ACTION | private WEP K-vector checkpoint only | continue private framework work | False |

## Next Target
| route_id | selection_status | target_file | target_script | task | acceptance_target | guardrails |
| --- | --- | --- | --- | --- | --- | --- |
| NEXT2440_0_selected | selected | 2441-Y5-R2FR-MTS-to-DD-charge-map-or-WEP-source-leg-owner.md | scripts/Y5_R2FR_MTS_to_DD_charge_map_or_WEP_source_leg_owner_2441.py | derive D_mhat_source and D_e_source from MTS coupling components, especially b_alpha, delta_w_block and source-shadow, or keep WEP rows as partial K material factors only | one MTS component maps to a DD-like charge with units and source leg, or every missing map/source leg remains explicit valid_for_claim=false | do not equate MICROSCOPE eta with delta_w, do not invent Earth/source charge, do not hide components by two-charge cancellation, do not claim WEP/local GR, do not edit formalization-workbench, and do not push GitHub |

## Branch Copies
| copy_id | source_path | target_path | source_exists | target_exists | notes |
| --- | --- | --- | --- | --- | --- |
| queue_wep_projection | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_2440_WEP_K_VECTOR_PROJECTION.csv | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\rab-sector\acquisition-queue\JR2440_WEP_K_VECTOR_PROJECTION_NONCLAIM.csv | True | True | WEP K-vector projection nonclaim queue |
| queue_smoke_bounds | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_2440_SINGLE_COMPONENT_SMOKE_BOUNDS_NONCLAIM.csv | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\rab-sector\acquisition-queue\JR2440_SINGLE_COMPONENT_WEP_SMOKE_BOUNDS_NONCLAIM.csv | True | True | single-component WEP smoke bounds nonclaim queue |
| branch_wep | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_2440_WEP_MATERIAL_SENSITIVITY_BASIS.csv | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\microscope\branch_locked_wep\residuals\WEP_K_vector_material_sensitivity_nonclaim_2440.csv | True | True | WEP material sensitivity branch |
| beta_docs | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_2440_WEP_K_VECTOR_PROJECTION.csv | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\beta-source\docs\WEP_K_VECTOR_MATERIAL_SENSITIVITY_2440_NONCLAIM.csv | True | True | WEP K-vector projection for beta docs |

## Validation
| check_id | status | notes | detail |
| --- | --- | --- | --- |
| VAL2440_00_local_sources_exist | PASS | all cited local source paths exist |  |
| VAL2440_01_local_needles | PASS | all cited local source needles are present |  |
| VAL2440_02_external_sources_present | PASS | external source references are present |  |
| VAL2440_03_material_contrast_numeric | PASS | Ti/Pt material contrast numbers are positive in selected Pt-minus-Ti convention |  |
| VAL2440_04_eta_bound_positive | PASS | MICROSCOPE eta 1-sigma quadrature bound is positive |  |
| VAL2440_05_projection_formula_present | PASS | MTS-expanded WEP projection formula is present |  |
| VAL2440_06_projection_not_score_ready | PASS | WEP projection rows are not score-ready or claim-valid |  |
| VAL2440_07_smoke_bounds_nonclaim | PASS | single-component smoke bounds are numeric but explicitly nonclaim |  |
| VAL2440_08_claims_blocked_except_nonclaim_inputs | PASS | only source-backed inputs pass, as nonclaim |  |
| VAL2440_09_next_target_written | PASS | 2441 MTS-to-DD charge map target selected |  |
| VAL2440_10_no_formalization_artifacts | PASS | no 2440 artifacts were written to formalization-workbench |  |
| VAL2440_CSV_P8_Y5_PARENT_QLOC_2440_SOURCE_REGISTER | PASS | CSV parses with 5 rows | OK |
| VAL2440_CSV_P8_Y5_PARENT_QLOC_2440_WEP_MATERIAL_SENSITIVITY_BASIS | PASS | CSV parses with 4 rows | OK |
| VAL2440_CSV_P8_Y5_PARENT_QLOC_2440_WEP_K_VECTOR_PROJECTION | PASS | CSV parses with 4 rows | OK |
| VAL2440_CSV_P8_Y5_PARENT_QLOC_2440_SINGLE_COMPONENT_SMOKE_BOUNDS_NONCLAIM | PASS | CSV parses with 2 rows | OK |
| VAL2440_CSV_P8_Y5_PARENT_QLOC_2440_WEP_SOURCE_LEG_BLOCKERS | PASS | CSV parses with 6 rows | OK |
| VAL2440_CSV_P8_Y5_PARENT_QLOC_2440_CLAIM_GATES | PASS | CSV parses with 5 rows | OK |
| VAL2440_CSV_P8_Y5_PARENT_QLOC_2440_DECISION_LEDGER | PASS | CSV parses with 5 rows | OK |
| VAL2440_CSV_P8_Y5_PARENT_QLOC_2440_NEXT_TARGET | PASS | CSV parses with 1 rows | OK |
| VAL2440_CSV_P8_Y5_PARENT_QLOC_2440_BRANCH_COPIES | PASS | CSV parses with 4 rows | OK |
| VAL2440_OVERALL | PASS | 2440 derives source-backed Ti/Pt material contrast factors, builds the WEP K formula, keeps score blocked, and selects MTS-to-DD charge mapping next |  |
