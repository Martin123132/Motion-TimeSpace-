# 1851: First Real Local Coupling Bound Source Table

**Current verdict:** this is a genuine source-acquisition win, not a physics-claim win. R10, WEP, PPN, clock/fine-structure and orbital anchors now have real numeric observable bounds attached. But every MTS component bound still waits on a translation/projection theorem, so `c_g`, `b_A`, `b_alpha`, `q_nonH`, `qbar_XT`, local GR and R10 pass claims remain blocked.

## Source Register
| source_id | source_type | source_path | source_url | needle | use | status | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| SRC1851_0_1850_handoff | local_checkpoint | 1850-Y5-R2FR-frame-marker-coupling-bound-input-pack-or-no-marker-theorem.md |  | NEXT1850_0_primary | selected 1851 target and component/projection rows | FOUND | False |
| SRC1851_1_1850_bound_pack | local_csv | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1850_FRAME_MARKER_BOUND_INPUT_PACK.csv |  | FMB1850_10_total_qbarXT_envelope | component envelope handoff | FOUND | False |
| SRC1851_2_eotwash_2020 | primary_paper |  | https://arxiv.org/abs/2002.11761 | gravitational-strength Yukawa interactions to ranges < 38.6 | R10 short-range Yukawa alpha(lambda) anchor | WEB_SOURCE_RECORDED | False |
| SRC1851_3_microscope_2022 | primary_paper |  | https://arxiv.org/abs/2209.15487 | eta(Ti, Pt) = [-1.5 +/- 2.3(stat) +/- 1.5(syst)] x 10^-15 | WEP/source-charge differential acceleration anchor | WEB_SOURCE_RECORDED | False |
| SRC1851_4_cassini_2003 | primary_paper |  | https://pubmed.ncbi.nlm.nih.gov/14508481/ | gamma = 1 + (2.1 +/- 2.3) x 10^-5 | PPN gamma/common-frame anchor | WEB_SOURCE_RECORDED | False |
| SRC1851_5_rosenband_2008 | primary_paper |  | https://tf.nist.gov/general/pdf/2280.pdf | alpha_dot/alpha = (-1.6 +/- 2.3) x 10^-17/year | clock/fine-structure drift anchor | WEB_SOURCE_RECORDED | False |
| SRC1851_6_llr_hofmann_2018 | primary_paper_metadata |  | https://ui.adsabs.harvard.edu/abs/2018CQGra..35c5015H | Gdot/G0 = (7.1 +/- 7.6) x 10^-14 yr^-1 | orbital/source-support Gdot anchor | WEB_SOURCE_RECORDED | False |
| SRC1851_7_llr_ep_2012 | primary_paper |  | https://arxiv.org/abs/1203.2150 | (-0.8 +/- 1.3) x 10^{-13} | Earth-Moon EP/orbital differential source anchor | WEB_SOURCE_RECORDED | False |

## Observable Bound Source Table
| bound_id | arena | observable | central_value | one_sigma | conservative_bound_value | bound_rule | lambda_value | lambda_units | observable_units | confidence | source_id | source_url | extraction_method | source_backed_observable | direct_mts_component_bound | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| OBS1851_0_R10_EOTWASH_2020 | R10_short_range | Yukawa alpha(lambda) gravitational-strength threshold |  |  | 1.0 | 95pct anchor: alpha=1 excluded for lambda >= 38.6 micrometer; not a full digitized curve | 38.6 | micrometer | dimensionless | 95pct | SRC1851_2_eotwash_2020 | https://arxiv.org/abs/2002.11761 | abstract_threshold_anchor | True | False | False |
| OBS1851_1_WEP_MICROSCOPE_2022 | WEP | Eotvos eta(Ti,Pt) | -1.5e-15 | 2.745906043549196e-15 | 6.991812087098392e-15 | |central| + 2*sqrt(stat^2+syst^2) |  |  | dimensionless | derived_conservative_2sigma_from_reported_1sigma | SRC1851_3_microscope_2022 | https://arxiv.org/abs/2209.15487 | abstract_reported_central_stat_syst | True | False | False |
| OBS1851_2_PPN_CASSINI_2003 | PPN | gamma_minus_1 | 2.1e-05 | 2.3e-05 | 6.7e-05 | |central| + 2*sigma |  |  | dimensionless | derived_conservative_2sigma_from_reported_1sigma | SRC1851_4_cassini_2003 | https://pubmed.ncbi.nlm.nih.gov/14508481/ | abstract_reported_gamma_minus_one | True | False | False |
| OBS1851_3_CLOCK_ROSENBAND_2008 | clock_fine_structure | alpha_dot_over_alpha | -1.6e-17 | 2.3e-17 | 6.2e-17 | |central| + 2*sigma |  |  | per_year | derived_conservative_2sigma_from_reported_preliminary_1sigma | SRC1851_5_rosenband_2008 | https://tf.nist.gov/general/pdf/2280.pdf | paper_text_reported_alpha_drift | True | False | False |
| OBS1851_4_ORBITAL_LLR_GDOT_2018 | orbital_Gdot | Gdot_over_G | 7.1e-14 | 7.6e-14 | 2.23e-13 | |central| + 2*sigma |  |  | per_year | derived_conservative_2sigma_from_reported_1sigma | SRC1851_6_llr_hofmann_2018 | https://ui.adsabs.harvard.edu/abs/2018CQGra..35c5015H | ADS_abstract_reported_result | True | False | False |
| OBS1851_5_ORBITAL_LLR_EP_2012 | orbital_EP | (mG/mI)_Earth_minus_(mG/mI)_Moon | -8e-14 | 1.3e-13 | 3.4e-13 | |central| + 2*sigma |  |  | dimensionless | derived_conservative_2sigma_from_reported_solution | SRC1851_7_llr_ep_2012 | https://arxiv.org/abs/1203.2150 | abstract_reported_solution | True | False | False |

## MTS Translation Gates
| gate_id | mts_component | observable_bound_id | needed_translation | current_translation_status | source_bound_available | direct_component_bound_now | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| TRG1851_0_cg_to_PPN | c_g | OBS1851_2_PPN_CASSINI_2003 | derive tau_PPN and show c_g is the scalar/common-frame parameter entering gamma_minus_1 | MISSING_MTS_TO_PPN_MAP | True | False | False |
| TRG1851_1_cg_to_R10 | c_g | OBS1851_0_R10_EOTWASH_2020 | derive alpha_R10(lambda_X)=K_X Qbar_XH qbar_XT tau_R10 and map c_g contribution | MISSING_TAU_R10_AND_KX_QBAR_LAMBDA | True | False | False |
| TRG1851_2_bA_to_WEP | b_A | OBS1851_1_WEP_MICROSCOPE_2022 | derive material sensitivity vector s_A(Ti,Pt) and source/test charge projection | MISSING_MATERIAL_SENSITIVITY_MAP | True | False | False |
| TRG1851_3_balpha_to_clock | b_alpha | OBS1851_3_CLOCK_ROSENBAND_2008 | derive Xdot or environmental X-profile coupling to clock/fine-structure residual | MISSING_X_PROFILE_OR_TIME_PROJECTION | True | False | False |
| TRG1851_4_delta_kappa_to_orbital_EP | delta_kappa_A | OBS1851_5_ORBITAL_LLR_EP_2012 | derive Earth/Moon source-current composition projection | MISSING_SOURCE_COMPOSITION_MAP | True | False | False |
| TRG1851_5_qnonH_support_to_Gdot | q_nonH;Delta_W_support;q_boundary | OBS1851_4_ORBITAL_LLR_GDOT_2018 | derive non-Hilbert/support/source-tail projection into secular GM or Gdot | MISSING_ORBITAL_SOURCE_SUPPORT_MAP | True | False | False |

## Conditional Bound Translations
| conditional_id | assumption | input_bound_id | derived_proxy_quantity | derived_proxy_bound | units | translation_valid_for_MTS | why_not_claim | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CBT1851_0_scalar_tensor_cg_proxy | If MTS c_g exactly reduces to a massless scalar-tensor alpha0 with gamma-1=-2 alpha0^2/(1+alpha0^2) | OBS1851_2_PPN_CASSINI_2003 | alpha0_abs_proxy | 0.005787918451395113 | dimensionless | False | MTS has not derived this scalar-tensor reduction or tau_PPN normalization | False |
| CBT1851_1_R10_alpha_anchor_proxy | If the MTS R10 branch produces a single Yukawa alpha(lambda) with lambda_X=38.6 micrometer | OBS1851_0_R10_EOTWASH_2020 | abs_alpha_R10_proxy | 1.0 | dimensionless_at_lambda_38p6um | False | only an alpha=1 threshold anchor, not a digitized curve or MTS K_X Qbar_XH qbar_XT product | False |
| CBT1851_2_WEP_differential_charge_proxy | If eta_AB maps directly to a differential material coupling with unit source normalization | OBS1851_1_WEP_MICROSCOPE_2022 | abs_delta_q_material_proxy | 6.991812087098392e-15 | dimensionless | False | MTS material sensitivity and source-current normalization are not derived | False |
| CBT1851_3_clock_alpha_proxy | If b_alpha couples to monotonic time drift with unit Xdot per year | OBS1851_3_CLOCK_ROSENBAND_2008 | abs_balpha_time_proxy | 6.2e-17 | per_year | False | MTS X-profile/time projection is not derived | False |

## Component Bound Status
| component_id | symbol | source_backed_observable_anchors | component_numeric_bound | best_current_status | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| CBS1851_0_cg | c_g | OBS1851_2_PPN_CASSINI_2003;OBS1851_0_R10_EOTWASH_2020 | MISSING_MTS_PROJECTION | OBSERVABLE_BOUNDS_EXIST_TRANSLATION_MISSING | False | False |
| CBS1851_1_bdis | b_dis | OBS1851_2_PPN_CASSINI_2003;OBS1851_3_CLOCK_ROSENBAND_2008 | MISSING_DISFORMAL_PROJECTION | OBSERVABLE_BOUNDS_EXIST_TRANSLATION_MISSING | False | False |
| CBS1851_2_bA | b_A | OBS1851_1_WEP_MICROSCOPE_2022;OBS1851_5_ORBITAL_LLR_EP_2012 | MISSING_MATERIAL_SENSITIVITY_MAP | OBSERVABLE_BOUNDS_EXIST_TRANSLATION_MISSING | False | False |
| CBS1851_3_balpha | b_alpha | OBS1851_3_CLOCK_ROSENBAND_2008 | MISSING_X_PROFILE_OR_TIME_PROJECTION | OBSERVABLE_BOUNDS_EXIST_TRANSLATION_MISSING | False | False |
| CBS1851_4_delta_kappa_A | delta_kappa_A | OBS1851_1_WEP_MICROSCOPE_2022;OBS1851_5_ORBITAL_LLR_EP_2012 | MISSING_SOURCE_COMPOSITION_MAP | OBSERVABLE_BOUNDS_EXIST_TRANSLATION_MISSING | False | False |
| CBS1851_5_qnonH_support_boundary | q_nonH;Delta_W_support;q_boundary | OBS1851_4_ORBITAL_LLR_GDOT_2018;OBS1851_5_ORBITAL_LLR_EP_2012 | MISSING_ORBITAL_SOURCE_SUPPORT_MAP | OBSERVABLE_BOUNDS_EXIST_TRANSLATION_MISSING | False | False |
| CBS1851_6_total_qbarXT | qbar_XT_bound_abs | OBS1851_0_R10_EOTWASH_2020;OBS1851_1_WEP_MICROSCOPE_2022;OBS1851_2_PPN_CASSINI_2003;OBS1851_3_CLOCK_ROSENBAND_2008;OBS1851_4_ORBITAL_LLR_GDOT_2018;OBS1851_5_ORBITAL_LLR_EP_2012 | MISSING_ALL_TRANSLATION_GATES | SOURCE_TABLE_READY_COMPONENT_CLAIM_BLOCKED | False | False |

## Local Test Matrix
| arena_id | arena | real_source_bound | mts_inputs_needed | status | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| LTM1851_0_R10 | short_range_R10 | OBS1851_0_R10_EOTWASH_2020 | lambda_X;K_X;Qbar_XH;qbar_XT_bound_abs;tau_R10 | SOURCE_ANCHOR_READY_MTS_TRANSLATION_MISSING | False | False |
| LTM1851_1_WEP | WEP | OBS1851_1_WEP_MICROSCOPE_2022;OBS1851_5_ORBITAL_LLR_EP_2012 | material sensitivities;source-current composition;delta_kappa_A;b_A;b_marker | SOURCE_ANCHOR_READY_MTS_TRANSLATION_MISSING | False | False |
| LTM1851_2_PPN | PPN | OBS1851_2_PPN_CASSINI_2003 | tau_PPN;c_g;b_dis;q_nonH;support/boundary mapping | SOURCE_ANCHOR_READY_MTS_TRANSLATION_MISSING | False | False |
| LTM1851_3_clock_EM | clock_fine_structure_EM | OBS1851_3_CLOCK_ROSENBAND_2008 | Xdot/profile;b_alpha;b_A;clock sensitivity map | SOURCE_ANCHOR_READY_MTS_TRANSLATION_MISSING | False | False |
| LTM1851_4_orbital | orbital_source_support | OBS1851_4_ORBITAL_LLR_GDOT_2018;OBS1851_5_ORBITAL_LLR_EP_2012 | q_nonH;Delta_W_support;q_boundary;source support and GM calibration mapping | SOURCE_ANCHOR_READY_MTS_TRANSLATION_MISSING | False | False |

## Claim Gates
| gate_id | claim | gate_pass | reason | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| CG1851_0_real_sources | real local observable bound sources exist | True | R10, WEP, PPN, clock and orbital anchors are recorded with numeric observable bounds | True | False |
| CG1851_1_direct_mts_component_bounds | MTS component bounds are numeric | False | all direct MTS component translations remain missing | False | False |
| CG1851_2_local_GR_claim | local GR recovered from bounded couplings | False | qbar_XT_bound_abs cannot be evaluated until translation/projection gates close | False | False |
| CG1851_3_R10_claim | R10 alpha(lambda) branch passes | False | Eöt-Wash anchor is real but MTS alpha product and digitized curve are incomplete | False | False |

## Decisions
| decision_id | decision | because | next_action | valid_for_claim |
| --- | --- | --- | --- | --- |
| DEC1851_0_source_table_win | 1851 succeeds as real source acquisition, not as an MTS pass. | local observable bounds are now explicit, numeric and source-linked across R10/WEP/PPN/clock/orbital arenas. | derive the MTS projection maps that turn those observable bounds into component bounds | False |
| DEC1851_1_no_overclaim | No direct component or local-GR claim is allowed yet. | every component row still says translation missing. | start with the least ambiguous projection: PPN/common-frame c_g or WEP/material b_A | False |
| DEC1851_2_best_next | Next target should derive the PPN/common-frame translation gate. | Cassini gives the cleanest weak-field common-frame anchor and can also reject over-large c_g branches quickly. | 1852-Y5-R2FR-PPN-common-frame-cg-translation-gate.md | False |

## Next Target
| route_id | next_target | script | objective | selection_status | success_condition |
| --- | --- | --- | --- | --- | --- |
| NEXT1851_0_primary | 1852-Y5-R2FR-PPN-common-frame-cg-translation-gate.md | scripts/Y5_R2FR_PPN_common_frame_cg_translation_gate_1852.py | derive or reject the mapping from MTS common frame coupling c_g into PPN gamma/tau_PPN, using Cassini as a real source-backed observable bound | selected | either c_g obtains a conditional/numeric PPN translation with clear assumptions, or the PPN/common-frame route is demoted to source-only closure |
| NEXT1851_1_parallel | 1852b-Y5-R2FR-WEP-material-sensitivity-bA-translation-gate.md | scripts/Y5_R2FR_WEP_material_sensitivity_bA_translation_gate_1852b.py | derive material sensitivity map from b_A/delta_kappa_A to MICROSCOPE/LLR WEP observables | held | material/source charge projection becomes explicit enough for a bound row |

## Validation
| check_id | result | detail |
| --- | --- | --- |
| VAL1851_0_sources_recorded | PASS | all local paths exist and web source URLs are recorded |
| VAL1851_1_local_needles_present | PASS | all local source needles are present |
| VAL1851_2_observable_bounds_numeric | PASS | observable bounds are positive, sourced and not direct MTS component claims |
| VAL1851_3_arena_coverage | PASS | R10/WEP/PPN/clock/orbital anchors are represented |
| VAL1851_4_translation_gates_block | PASS | translation gates keep direct component bounds blocked |
| VAL1851_5_conditionals_nonclaim | PASS | conditional proxy translations are nonclaim |
| VAL1851_6_components_nonclaim | PASS | component rows remain claim-blocked |
| VAL1851_7_local_matrix_nonclaim | PASS | local test matrix records real anchors but missing MTS translations |
| VAL1851_8_claim_gates_safe | PASS | only real-source acquisition passes; no MTS claim passes |
| VAL1851_9_decision_next | PASS | decision ledger selects PPN/common-frame translation gate |
| VAL1851_10_next_target_selected | PASS | next target selected |
| VAL1851_11_no_claim_flags | PASS | no valid_for_claim flags are true |
| VAL1851_12_missing_rows_nonclaim | PASS | MISSING_* rows stay nonclaim |
| VAL1851_13_csv_parse | PASS | all generated 1851 CSVs parse |
| VAL1851_14_branch_copies | PASS | branch/quarantine/queue copies exist |
| VAL1851_15_pycache_absent | PASS | scripts __pycache__ absent |
| VAL1851_16_formalization_untouched | PASS | no 1851 outputs found under formalization-workbench |
| VAL1851_OVERALL | PASS | 1851 first real local coupling bound source table |

## Working Interpretation
This is exactly the Mayweather route: not a knockout, but clean footwork. The project now has real local-test ropes around the coupling gap. The next fight is not hunting more bounds; it is deriving one translation map cleanly enough that the first component can actually be constrained.
