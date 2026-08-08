# 2511 — First Source-Weight Input Row: WEP Product Law or PPN Source Kernel

**Current verdict:** one real thing is derived: the isolated WEP source-weight product must obey `|Delta_w_TiPt tau_WEP| <= 2.8e-15`. That is a product/amplitude law, not a standalone MTS prediction and not a local-GR pass.

**Key limit:** `|Delta_w_TiPt| <= 2.8e-15/tau_min` only follows if `|tau_WEP| >= tau_min > 0` is sourced or parent-derived. `tau_WEP=1` is explicitly forbidden as a shortcut.

**PPN warning:** even a clean WEP product does not prove `gamma=beta=1`; the same source-weight vector still needs a PPN response kernel in a fixed measured-GM convention.

## Source Register
| source_id | source_path | path_exists | found_needles | source_pass | role |
| --- | --- | --- | --- | --- | --- |
| SRC2511_0_2510_next | 2510-Y5-R2FR-source-weight-residual-bound-pack-WEP-R10-PPN-clock-orbit.md | True | NEXT2510_0_selected;FIRST_SOURCE_WEIGHT_INPUT_ROW | True | authoritative 2510 selection of WEP product / PPN kernel route |
| SRC2511_1_local_bound_claims | source-intake/local_bounds/local_bound_claims.csv | True | R1_WEP_source_charge;2.8e-15 | True | MICROSCOPE Ti/Pt WEP source-charge proxy bound anchor |
| SRC2511_2_1065_product_schema | source-intake/mts_residuals/P8_Y5_R10_1065_FIRST_WEP_NUMERIC_ROW_SCHEMA.csv | True | WEP1065_2_delta_w;WEP1065_4_product | True | existing WEP Delta_w times tau_WEP product schema |
| SRC2511_3_1065_zero_clauses | source-intake/mts_residuals/P8_Y5_R10_1065_WA_THEOREM_ZERO_CLAUSES.csv | True | WTZ1065_0_strict_no_slot;WTZ1065_4_verdict | True | zero-theorem clauses for relative source weights |
| SRC2511_4_1061_tau_input | source-intake/mts_residuals/P8_Y5_R10_1061_INPUT_FILL_LEDGER.csv | True | INF1061_4_tau_WEP;MISSING_LAB_SOURCE_ORBIT_PROJECTION | True | tau_WEP still missing and cannot be set to one |
| SRC2511_5_1061_material_convention | source-intake/mts_residuals/P8_Y5_R10_1061_WEP_MATERIAL_CONVENTION.csv | True | MCON1061_0_test_pair;MCON1061_2_eta_bound | True | Ti/Pt material convention and eta bound anchor |
| SRC2511_6_1608_tau_contract | source-intake/microscope/quarantine/1608/TAU_WEP_READOUT_CONTRACT_NONCLAIM.csv | True | TAU1608_1_amplitude_law;TAU1608_3_no_unity | True | conditional amplitude law and anti-unity tau guard |
| SRC2511_7_2121_tau_min_request | source-intake/source-weight/docs/AFRAME_CMSM_EXPORT_2121_NONCLAIM.csv | True | CMSM2121_6_tau_min;VR2121_6_no_tau_shortcut | True | tau_min lower-bound acquisition requirement |
| SRC2511_8_2489_ppn_source | source-intake/local_bounds/PPN_residual_vector_interface_2489_NONCLAIM.csv | True | PPNV2489_4_wR;PPNV2489_7_total_abs | True | parallel local-GR bridge: PPN source-weight response kernel still missing |
| SRC2511_9_2510_bound_pack | source-intake/local_bounds/Source_weight_residual_bound_pack_2510_NONCLAIM.csv | True | ARENA2510_0_WEP;ARENA2510_2_PPN | True | 2510 branch copy of WEP and PPN arena requirements |

## Delta-w Zero Attempt
| zero_id | target | theorem_attempt | formal_status | current_gap | verdict |
| --- | --- | --- | --- | --- | --- |
| ZERO2511_0_no_w_slot | Delta_w_TiPt | if parent matter/source language has no inert source-only species scalar w_A, then relative source weights vanish | EXACT_IF_PARENT_SYNTAX_SIGNED | parent syntax/no-source-only-slot not derived from deeper MTS primitives | NOT_PROMOTED |
| ZERO2511_1_common_mode | Delta_w_TiPt | if w_A=w_common for all species and is range/time/frame independent, common normalization may be calibrated into G | EXACT_CONDITIONAL_COMMON_MODE | universality is the missing theorem; relative pieces cannot be absorbed into measured G | NOT_PROMOTED |
| ZERO2511_2_field_redefinition | Delta_w_TiPt | classify apparent w_A as field normalization after canonical kinetic and measured coupling quotient | LOOPHOLE_AUDITED | interactions, composite matter, quantum normalization, and source-action scale can leave a residual source-only factor | NOT_PROMOTED |
| ZERO2511_3_tau_zero | P_WEP=Delta_w_TiPt*tau_WEP | tau_WEP=0 would make WEP blind to this component | NOT_A_LOCAL_GR_ZERO | tau_WEP=0 would not remove PPN/R10/clock/orbital source-weight residuals | HELD_AS_WEP_ONLY_BLINDNESS_NOT_THEORY_ZERO |
| ZERO2511_4_verdict | P_WEP_relative_source_weight | Delta_w_TiPt=0 or tau_WEP=0 from parent-signed geometry/source grammar | THEOREM_ZERO_NOT_PARENT_SIGNED | WEP route must use a product-bound law until source-label forgetting or tau nondegeneracy is sourced | PRODUCT_BOUND_ROUTE_SELECTED_NONCLAIM |

## WEP Product Bound Law
| product_id | quantity | law | numeric_value | units | status | score_ready |
| --- | --- | --- | --- | --- | --- | --- |
| WPROD2511_0_observed_bound | eta_TiPt_source_charge_bound | abs(eta_TiPt_source_charge) <= 2.8e-15 | 2.8e-15 | dimensionless | SOURCE_BACKED_BOUND_ANCHOR_NOT_MTS_PREDICTION | False |
| WPROD2511_1_direct_product_law | P_WEP_relative_source_weight | P_WEP = abs(Delta_w_TiPt * tau_WEP) | MISSING_DELTA_W_TiPt_AND_TAU_WEP | dimensionless | PRODUCT_DEFINITION_READY_VALUES_MISSING | False |
| WPROD2511_2_exact_component_bound | component_product_ceiling | abs(Delta_w_TiPt * tau_WEP) <= 2.8e-15 for the isolated WEP source-weight leg | 2.8e-15 | dimensionless product ceiling | EXACT_PRODUCT_BOUND_LAW_NONCLAIM | False |
| WPROD2511_3_amplitude_inversion | Delta_w_TiPt_width | if abs(tau_WEP) >= tau_min > 0 then abs(Delta_w_TiPt) <= 2.8e-15/tau_min | MISSING_TAU_MIN | dimensionless source-weight width | EXACT_CONDITIONAL_LAW_TAU_MIN_MISSING | False |
| WPROD2511_4_total_envelope_guard | WEP_absolute_envelope | abs(Delta_w_TiPt*tau_WEP)+sum_other_abs_WEP_legs <= eta_bound; no cancellation between legs | MISSING_OTHER_LEG_BOUNDS | dimensionless eta envelope | TOTAL_WEP_CLAIM_BLOCKED_OTHER_LEGS_RETAINED | False |

## Tau Gate
| tau_id | quantity | requirement | current_status | required_source | blocks |
| --- | --- | --- | --- | --- | --- |
| TAUG2511_0_definition | tau_WEP | branch-locked lab/source/orbit/readout projection converting Delta_w_TiPt into eta_TiPt | FORMAL_DEFINITION_ONLY | official readout arrays or parent geometry/source nondegeneracy theorem | WEP product cannot become a Delta_w width |
| TAUG2511_1_tau_min | tau_min | strictly positive lower bound abs(tau_WEP)>=tau_min>0 | MISSING_TAU_MIN | P_WEP_tau_min_lower_bound.csv or parent nondegeneracy proof | abs(Delta_w_TiPt)<=2.8e-15/tau_min cannot be evaluated |
| TAUG2511_2_no_unity | tau_WEP=1 shortcut | forbidden unless derived from the actual readout normalization | SHORTCUT_FORBIDDEN | source/readout normalization calculation | fake WEP pass and fake Delta_w bound |
| TAUG2511_3_tau_zero | tau_WEP=0 | can only mean WEP blindness, not universal source-weight safety | NOT_A_CROSS_ARENA_ZERO | PPN/R10/clock/orbit kernels still required | local-GR claim from WEP alone |
| TAUG2511_4_verdict | tau_WEP gate | derive tau map or acquire tau_min before any Delta_w numeric width | TAU_GATE_BLOCKS_NUMERIC_DELTAW_WIDTH | 2512 target | score_ready remains false |

## PPN Handoff
| ppn_id | observable | needed_kernel | current_status | why_parallel |
| --- | --- | --- | --- | --- |
| PPNH2511_0_source_weight_gamma | gamma_minus_1 | C_gamma_source_weight | MISSING_SOURCE_PREFACTOR_ZERO_OR_KERNEL | WEP can bind a product, but local GR needs the PPN response of the same source-weight vector |
| PPNH2511_1_source_weight_beta | beta_minus_1 | C_beta_source_weight | MISSING_SECOND_ORDER_SOURCE_RESPONSE_KERNEL | beta is the second-order local-GR gate and cannot be inferred from WEP |
| PPNH2511_2_preferred_frame_exchange | alpha1,alpha2,alpha3,xi | preferred-frame/source-exchange/endpoint kernel | MISSING_VECTOR_DOMAIN_SOURCE_KERNEL | relative weights can hide in WEP but show in source exchange, endpoint, or momentum-flux channels |
| PPNH2511_3_measured_GM | source-normalized Newton/PPN comparison | fixed measured-GM transfer map | MISSING_NO_ABSORB_RELATIVE_WEIGHT_PROOF | common normalization can define G only after universality; relative weights must remain observable residuals |

## Nonclaim Dry Run
| case_id | case_description | result_status | blocking_markers | pass_fail | claim_pass |
| --- | --- | --- | --- | --- | --- |
| DRY2511_0_bound_anchor_only | use eta_bound=2.8e-15 without Delta_w or tau_WEP | REFUSED_BOUND_ANCHOR_NOT_PREDICTION | MISSING_DELTA_W_TiPt;MISSING_TAU_WEP | BLOCKED_NONCLAIM | False |
| DRY2511_1_product_law | derive product ceiling abs(Delta_w_TiPt*tau_WEP)<=2.8e-15 | ACCEPT_PRODUCT_BOUND_LAW_NONCLAIM | PRODUCT_BOUND_NOT_MTS_PREDICTION;VALID_FOR_CLAIM_FALSE | BLOCKED_NONCLAIM | False |
| DRY2511_2_invert_without_tau_min | attempt Delta_w width from product ceiling with tau_min missing | REFUSED_MISSING_TAU_MIN | MISSING_TAU_MIN;NO_TAU_UNITY_SHORTCUT | BLOCKED_NONCLAIM | False |
| DRY2511_3_unsigned_zero | promote Delta_w_TiPt=0 from the no-source-only-slot grammar without parent signature | REFUSED_UNSIGNED_THEOREM_ZERO | THEOREM_ZERO_NOT_PARENT_SIGNED | BLOCKED_NONCLAIM | False |
| DRY2511_4_wep_to_local_gr | infer PPN/local-GR safety from WEP product bound | REFUSED_WRONG_ARENA_INFERENCE | MISSING_PPN_SOURCE_KERNEL;WEP_NOT_LOCAL_GR | BLOCKED_NONCLAIM | False |

## Decision Ledger
| decision_id | decision | rationale | status |
| --- | --- | --- | --- |
| DEC2511_0_gain | WEP_PRODUCT_AMPLITUDE_LAW_DERIVED | The exact component law is now explicit: abs(Delta_w_TiPt*tau_WEP)<=2.8e-15 for the isolated WEP source-weight leg. | selected_nonclaim |
| DEC2511_1_limit | DELTAW_WIDTH_NOT_NUMERIC | A standalone Delta_w_TiPt width requires tau_min>0 or parent zero; tau_WEP cannot be set to one. | blocked_by_tau_min |
| DEC2511_2_theorem | NO_SOURCE_ONLY_SLOT_NOT_SIGNED | The desired zero theorem remains conditional; relative weights survive as finite coupling debt. | retained |
| DEC2511_3_ppn | PPN_SOURCE_KERNEL_REMAINS_PARALLEL_LOCAL_GR_GATE | WEP product bounds cannot prove beta/gamma/preferred-frame closure or Newton/GR reduction. | retained |
| DEC2511_4_best_next | TAU_WEP_LOWER_BOUND_OR_PARENT_NONDEGENERACY | The next real unlock is tau_min or a parent proof that the WEP projection is nondegenerate/zero in the right way. | selected |

## Next Target
| route_id | selection_status | target_file | target_script | objective | success_condition | do_not_do |
| --- | --- | --- | --- | --- | --- | --- |
| NEXT2511_0_selected | selected | 2512-Y5-R2FR-tau-WEP-lower-bound-or-parent-nondegeneracy-proof.md | scripts/Y5_R2FR_tau_WEP_lower_bound_or_parent_nondegeneracy_proof_2512.py | derive tau_WEP=0/nonzero from parent geometry or acquire a source-backed tau_min lower bound; then convert the WEP product ceiling into a Delta_w_TiPt width only if legitimate | tau_WEP has parent-signed zero/nonzero theorem or tau_min>0 with source path, units, sign/absolute convention, and no unity shortcut | do not assume tau_WEP=1; do not treat WEP blindness as PPN/R10 silence; do not claim local GR |
| NEXT2511_1_parallel_ppn | parallel_after_tau | 2512b-Y5-R2FR-source-weight-PPN-response-kernel-fixed-GM-map.md | scripts/Y5_R2FR_source_weight_PPN_response_kernel_fixed_GM_map_2512b.py | derive or bound how the same Delta_w_eff vector enters gamma,beta,alpha_i,xi under a fixed measured-GM convention | PPN response kernel has units and source path and cannot absorb relative source weights into fitted G | do not infer local GR from WEP; do not import GR as the response kernel |

## Validation
| check_id | status | detail |
| --- | --- | --- |
| VAL2511_00_sources_exist | PASS |  |
| VAL2511_01_source_needles | PASS |  |
| VAL2511_02_zero_not_promoted | PASS | zero theorem remains unsigned |
| VAL2511_03_product_law | PASS | component product ceiling present |
| VAL2511_04_tau_blocks_width | PASS | tau_min missing blocks Delta_w width |
| VAL2511_05_ppn_handoff | PASS | PPN local-GR handoff rows present |
| VAL2511_06_dryruns_block_claims | PASS | dry runs remain nonclaim |
| VAL2511_07_next_target | PASS | tau lower-bound route selected |
| VAL2511_08_no_claim_flags | PASS |  |
| VAL2511_09_branch_copies | PASS |  |
| VAL2511_10_no_formalization_artifacts | PASS |  |
| VAL2511_11_pycache_absent | PASS |  |
| VAL2511_CSV_P8_Y5_NO_SHADOW_2511_SOURCE_REGISTER | PASS | OK; rows=10 |
| VAL2511_CSV_P8_Y5_NO_SHADOW_2511_DELTAW_ZERO_ATTEMPT | PASS | OK; rows=5 |
| VAL2511_CSV_P8_Y5_NO_SHADOW_2511_WEP_PRODUCT_BOUND_LAW | PASS | OK; rows=5 |
| VAL2511_CSV_P8_Y5_NO_SHADOW_2511_TAU_WEP_GATE | PASS | OK; rows=5 |
| VAL2511_CSV_P8_Y5_NO_SHADOW_2511_PPN_SOURCE_KERNEL_HANDOFF | PASS | OK; rows=4 |
| VAL2511_CSV_P8_Y5_NO_SHADOW_2511_NONCLAIM_DRYRUN_RESULTS | PASS | OK; rows=5 |
| VAL2511_CSV_P8_Y5_NO_SHADOW_2511_DECISION_LEDGER | PASS | OK; rows=5 |
| VAL2511_CSV_P8_Y5_NO_SHADOW_2511_NEXT_TARGET | PASS | OK; rows=2 |
| VAL2511_CSV_P8_Y5_NO_SHADOW_2511_BRANCH_COPIES | PASS | OK; rows=4 |
| VAL2511_COPY_CSV_wep_product_bound | PASS | OK; rows=5 |
| VAL2511_COPY_CSV_tau_requirement | PASS | OK; rows=5 |
| VAL2511_COPY_CSV_ppn_handoff | PASS | OK; rows=4 |
| VAL2511_COPY_CSV_next_tau | PASS | OK; rows=2 |
| VAL2511_OVERALL | PASS | 2511 derives WEP source-weight product amplitude law and blocks standalone Delta_w claim without tau_min |
