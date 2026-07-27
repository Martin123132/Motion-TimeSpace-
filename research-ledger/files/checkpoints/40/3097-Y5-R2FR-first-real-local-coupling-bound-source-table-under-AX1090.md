# 3097 Y5 R2FR first real local coupling bound source table under AX1090

**Progress:** 3097 is a real source-acquisition checkpoint. R10, WEP, PPN, clock/fine-structure and orbital anchors now have source-linked numeric observable bounds in the current AX1090 branch.

**Current verdict:** this is not an MTS physics pass. Every direct MTS component bound still waits on a translation/projection theorem, so `c_g`, `b_A`, `b_alpha`, `q_nonH`, `qbar_XT`, local GR and R10 pass claims remain blocked.

**Claim ceiling:** no R10, WEP, clock, EM, PPN, orbital, local-GR/Newton, finite-alpha, or source-zero pass is allowed from 3097.

## Source Register
| source_id | source_path | exists | parse_ok | needles_present | missing_needles | role |
| --- | --- | --- | --- | --- | --- | --- |
| SRC3097_00_3096_next | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3096_NEXT_TARGET.csv | True | True | True |  | 3096 selects first real local coupling bound source table. |
| SRC3097_01_3096_doc | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\3096-Y5-R2FR-frame-marker-coupling-bound-input-pack-or-no-marker-theorem-under-AX1090.md | True | True | True |  | 3096 establishes the bound pack and asks for real source rows. |
| SRC3097_02_1851_doc | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1851-Y5-R2FR-first-real-local-coupling-bound-source-table.md | True | True | True |  | 1851 precedent for real source anchors with blocked MTS translations. |
| SRC3097_03_1851_sources | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_1851_OBSERVABLE_BOUND_SOURCE_TABLE.csv | True | True | True |  | 1851 observable source-bound table. |
| SRC3097_04_1851_translation | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_1851_MTS_TRANSLATION_GATES.csv | True | True | True |  | 1851 translation gates block direct MTS component bounds. |
| SRC3097_05_1851_component | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_1851_COMPONENT_BOUND_STATUS.csv | True | True | True |  | 1851 component status table. |
| SRC3097_06_1851_local_matrix | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_1851_LOCAL_TEST_MATRIX.csv | True | True | True |  | 1851 local test matrix with real anchors. |
| SRC3097_07_1851_next | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_1851_NEXT_TARGET.csv | True | True | True |  | 1851 selects PPN/common-frame translation gate. |
| SRC3097_08_1029_ppn | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1029_TAU_PROJECTION_REQUIREMENTS.csv | True | True | True |  | 1029 precedent for c_g to PPN translation requirements. |

## Observable Bound Source Table
| bound_id | arena | observable | conservative_bound_value | bound_rule | lambda_value | lambda_units | observable_units | source_url | source_backed_observable | direct_mts_component_bound | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| OBS3097_0_R10_EOTWASH_2020 | R10_short_range | Yukawa alpha(lambda) gravitational-strength threshold | 1.0 | 95pct anchor: alpha=1 excluded for lambda >= 38.6 micrometer; not a full digitized curve | 38.6 | micrometer | dimensionless | https://arxiv.org/abs/2002.11761 | True | False | False |
| OBS3097_1_WEP_MICROSCOPE_2022 | WEP | Eotvos eta(Ti,Pt) | 6.991812087098392e-15 | \|central\| + 2*sqrt(stat^2+syst^2) |  |  | dimensionless | https://arxiv.org/abs/2209.15487 | True | False | False |
| OBS3097_2_PPN_CASSINI_2003 | PPN | gamma_minus_1 | 6.7e-05 | \|central\| + 2*sigma |  |  | dimensionless | https://pubmed.ncbi.nlm.nih.gov/14508481/ | True | False | False |
| OBS3097_3_CLOCK_ROSENBAND_2008 | clock_fine_structure | alpha_dot_over_alpha | 6.2e-17 | \|central\| + 2*sigma |  |  | per_year | https://tf.nist.gov/general/pdf/2280.pdf | True | False | False |
| OBS3097_4_ORBITAL_LLR_GDOT_2018 | orbital_Gdot | Gdot_over_G | 2.23e-13 | \|central\| + 2*sigma |  |  | per_year | https://ui.adsabs.harvard.edu/abs/2018CQGra..35c5015H | True | False | False |
| OBS3097_5_ORBITAL_LLR_EP_2012 | orbital_EP | Earth-Moon differential acceleration toward Sun | 1.4e-13 | reported EP upper-bound anchor |  |  | dimensionless | https://arxiv.org/abs/1203.2150 | True | False | False |

## MTS Translation Gates
| gate_id | mts_component | observable_bound_id | needed_translation | current_translation_status | source_bound_available | direct_component_bound_now | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| TRG3097_0_cg_to_PPN | c_g | OBS3097_2_PPN_CASSINI_2003 | derive tau_PPN and show c_g is the scalar/common-frame parameter entering gamma_minus_1 | MISSING_MTS_TO_PPN_MAP | True | False | False |
| TRG3097_1_cg_to_R10 | c_g | OBS3097_0_R10_EOTWASH_2020 | derive alpha_R10(lambda_X)=K_X Qbar_XH qbar_XT tau_R10 and map c_g contribution | MISSING_TAU_R10_AND_KX_QBAR_LAMBDA | True | False | False |
| TRG3097_2_bA_to_WEP | b_A | OBS3097_1_WEP_MICROSCOPE_2022 | derive material sensitivity vector s_A(Ti,Pt) and source/test charge projection | MISSING_MATERIAL_SENSITIVITY_MAP | True | False | False |
| TRG3097_3_balpha_to_clock | b_alpha | OBS3097_3_CLOCK_ROSENBAND_2008 | derive Xdot or environmental X-profile coupling to clock/fine-structure residual | MISSING_X_PROFILE_OR_TIME_PROJECTION | True | False | False |
| TRG3097_4_delta_kappa_to_orbital_EP | delta_kappa_A | OBS3097_5_ORBITAL_LLR_EP_2012 | derive Earth/Moon source-current composition projection | MISSING_SOURCE_COMPOSITION_MAP | True | False | False |
| TRG3097_5_qnonH_support_to_Gdot | q_nonH;Delta_W_support;q_boundary | OBS3097_4_ORBITAL_LLR_GDOT_2018 | derive non-Hilbert/support/source-tail projection into secular GM or Gdot | MISSING_ORBITAL_SOURCE_SUPPORT_MAP | True | False | False |

## Conditional Bound Translations
| conditional_id | assumption | input_bound_id | derived_proxy_quantity | derived_proxy_bound | units | translation_valid_for_MTS | why_not_claim | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CBT3097_0_scalar_tensor_cg_proxy | If MTS c_g exactly reduces to a massless scalar-tensor alpha0 with gamma-1=-2 alpha0^2/(1+alpha0^2) | OBS3097_2_PPN_CASSINI_2003 | alpha0_abs_proxy | 0.005787918451395113 | dimensionless | False | MTS has not derived this scalar-tensor reduction or tau_PPN normalization | False |
| CBT3097_1_R10_alpha_anchor_proxy | If the MTS R10 branch produces a single Yukawa alpha(lambda) with lambda_X=38.6 micrometer | OBS3097_0_R10_EOTWASH_2020 | abs_alpha_R10_proxy | 1.0 | dimensionless_at_lambda_38p6um | False | only an alpha=1 threshold anchor, not a digitized curve or MTS K_X Qbar_XH qbar_XT product | False |
| CBT3097_2_WEP_differential_charge_proxy | If eta_AB maps directly to a differential material coupling with unit source normalization | OBS3097_1_WEP_MICROSCOPE_2022 | abs_delta_q_material_proxy | 6.991812087098392e-15 | dimensionless | False | MTS material sensitivity and source-current normalization are not derived | False |
| CBT3097_3_clock_alpha_proxy | If b_alpha couples to monotonic time drift with unit Xdot per year | OBS3097_3_CLOCK_ROSENBAND_2008 | abs_balpha_time_proxy | 6.2e-17 | per_year | False | MTS X-profile/time projection is not derived | False |

## Component Bound Status
| component_id | symbol | source_backed_observable_anchors | component_numeric_bound | best_current_status | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| CBS3097_0_cg | c_g | OBS3097_2_PPN_CASSINI_2003;OBS3097_0_R10_EOTWASH_2020 | MISSING_MTS_PROJECTION | OBSERVABLE_BOUNDS_EXIST_TRANSLATION_MISSING | False | False |
| CBS3097_1_bdis | b_dis | OBS3097_2_PPN_CASSINI_2003;OBS3097_3_CLOCK_ROSENBAND_2008 | MISSING_DISFORMAL_PROJECTION | OBSERVABLE_BOUNDS_EXIST_TRANSLATION_MISSING | False | False |
| CBS3097_2_bA | b_A | OBS3097_1_WEP_MICROSCOPE_2022;OBS3097_5_ORBITAL_LLR_EP_2012 | MISSING_MATERIAL_SENSITIVITY_MAP | OBSERVABLE_BOUNDS_EXIST_TRANSLATION_MISSING | False | False |
| CBS3097_3_balpha | b_alpha | OBS3097_3_CLOCK_ROSENBAND_2008 | MISSING_X_PROFILE_OR_TIME_PROJECTION | OBSERVABLE_BOUNDS_EXIST_TRANSLATION_MISSING | False | False |
| CBS3097_4_delta_kappa_A | delta_kappa_A | OBS3097_1_WEP_MICROSCOPE_2022;OBS3097_5_ORBITAL_LLR_EP_2012 | MISSING_SOURCE_COMPOSITION_MAP | OBSERVABLE_BOUNDS_EXIST_TRANSLATION_MISSING | False | False |
| CBS3097_5_qnonH_support_boundary | q_nonH;Delta_W_support;q_boundary | OBS3097_4_ORBITAL_LLR_GDOT_2018;OBS3097_5_ORBITAL_LLR_EP_2012 | MISSING_ORBITAL_SOURCE_SUPPORT_MAP | OBSERVABLE_BOUNDS_EXIST_TRANSLATION_MISSING | False | False |
| CBS3097_6_total_qbarXT | qbar_XT_bound_abs | OBS3097_0_R10_EOTWASH_2020;OBS3097_1_WEP_MICROSCOPE_2022;OBS3097_2_PPN_CASSINI_2003;OBS3097_3_CLOCK_ROSENBAND_2008;OBS3097_4_ORBITAL_LLR_GDOT_2018;OBS3097_5_ORBITAL_LLR_EP_2012 | MISSING_ALL_TRANSLATION_GATES | SOURCE_TABLE_READY_COMPONENT_CLAIM_BLOCKED | False | False |

## Local Test Matrix
| arena_id | arena | real_source_bound | mts_inputs_needed | status | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| LTM3097_0_R10 | short_range_R10 | OBS3097_0_R10_EOTWASH_2020 | lambda_X;K_X;Qbar_XH;qbar_XT_bound_abs;tau_R10 | SOURCE_ANCHOR_READY_MTS_TRANSLATION_MISSING | False | False |
| LTM3097_1_WEP | WEP | OBS3097_1_WEP_MICROSCOPE_2022;OBS3097_5_ORBITAL_LLR_EP_2012 | material sensitivities;source-current composition;delta_kappa_A;b_A;b_marker | SOURCE_ANCHOR_READY_MTS_TRANSLATION_MISSING | False | False |
| LTM3097_2_PPN | PPN | OBS3097_2_PPN_CASSINI_2003 | tau_PPN;c_g;b_dis;q_nonH;support/boundary mapping | SOURCE_ANCHOR_READY_MTS_TRANSLATION_MISSING | False | False |
| LTM3097_3_clock_EM | clock_fine_structure_EM | OBS3097_3_CLOCK_ROSENBAND_2008 | Xdot/profile;b_alpha;b_A;clock sensitivity map | SOURCE_ANCHOR_READY_MTS_TRANSLATION_MISSING | False | False |
| LTM3097_4_orbital | orbital_source_support | OBS3097_4_ORBITAL_LLR_GDOT_2018;OBS3097_5_ORBITAL_LLR_EP_2012 | q_nonH;Delta_W_support;q_boundary;source support and GM calibration mapping | SOURCE_ANCHOR_READY_MTS_TRANSLATION_MISSING | False | False |

## Claim Gate
| gate_id | claim | gate_pass | reason | source_backed_observable | claim_allowed_for_physics | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| CG3097_0_real_sources | real local observable bound sources exist | True | R10, WEP, PPN, clock and orbital anchors are recorded with numeric observable bounds | True | False | False |
| CG3097_1_direct_mts_component_bounds | MTS component bounds are numeric | False | all direct MTS component translations remain missing | True | False | False |
| CG3097_2_local_GR_claim | local GR recovered from bounded couplings | False | qbar_XT_bound_abs cannot be evaluated until translation/projection gates close | True | False | False |
| CG3097_3_no_public_claim | R10/WEP/PPN/clock/orbital local pass | False | observable anchors are evidence inputs only; MTS map is missing | True | False | False |

## Decision Ledger
| decision_id | decision | because | next_action | valid_for_claim |
| --- | --- | --- | --- | --- |
| DEC3097_0_source_table_win | 3097 succeeds as real source acquisition, not as an MTS pass. | local observable bounds are explicit, numeric and source-linked across R10/WEP/PPN/clock/orbital arenas | derive the MTS projection maps that turn those observable bounds into component bounds | False |
| DEC3097_1_translation_status | Every MTS component bound remains blocked by translation gates. | c_g, b_A, b_alpha, q_nonH and total qbarXT require tau/projection/normalization maps | start with the PPN/common-frame c_g translation gate | False |
| DEC3097_2_best_next | Next target should derive the PPN/common-frame translation gate. | Cassini gives the cleanest weak-field common-frame anchor and can reject over-large c_g branches quickly | 3098-Y5-R2FR-PPN-common-frame-cg-translation-gate-under-AX1090.md | False |

## Next Target
| route_id | next_checkpoint | script | objective | selection_status | success_condition |
| --- | --- | --- | --- | --- | --- |
| NEXT3097_0_primary | 3098-Y5-R2FR-PPN-common-frame-cg-translation-gate-under-AX1090.md | scripts/Y5_R2FR_PPN_common_frame_cg_translation_gate_under_AX1090_3098.py | derive or reject the mapping from MTS common frame coupling c_g into PPN gamma/tau_PPN, using Cassini as a real source-backed observable bound | selected | either c_g obtains a conditional/numeric PPN translation with clear assumptions, or the PPN/common-frame route is demoted to source-only closure |
| NEXT3097_1_parallel | 3098b-Y5-R2FR-WEP-material-sensitivity-bA-translation-gate-under-AX1090.md | scripts/Y5_R2FR_WEP_material_sensitivity_bA_translation_gate_under_AX1090_3098b.py | derive material sensitivity map from b_A/delta_kappa_A to MICROSCOPE/LLR WEP observables | held | material/source charge projection becomes explicit enough for a bound row |

## Validation
| validation_id | check_pass | detail | artifact |
| --- | --- | --- | --- |
| VAL3097_00_sources_csv | True | source register parses | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3097_SOURCE_REGISTER.csv |
| VAL3097_01_sources_exist | True | every cited local source path exists | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3097_SOURCE_REGISTER.csv |
| VAL3097_02_sources_parse | True | every cited csv source parses | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3097_SOURCE_REGISTER.csv |
| VAL3097_03_needles_present | True | all source needles found | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3097_SOURCE_REGISTER.csv |
| VAL3097_04_doc_created | True | checkpoint markdown created | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\3097-Y5-R2FR-first-real-local-coupling-bound-source-table-under-AX1090.md |
| VAL3097_05_observable_bounds_parse | True | observable source table parses | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3097_OBSERVABLE_BOUND_SOURCE_TABLE.csv |
| VAL3097_06_observable_bounds_numeric | True | observable bounds are positive, sourced and not direct MTS component claims | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3097_OBSERVABLE_BOUND_SOURCE_TABLE.csv |
| VAL3097_07_translation_parse | True | translation gates parse | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3097_MTS_TRANSLATION_GATES.csv |
| VAL3097_08_translation_blocks | True | translation gates keep direct component bounds blocked | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3097_MTS_TRANSLATION_GATES.csv |
| VAL3097_09_conditional_parse | True | conditional translations parse | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3097_CONDITIONAL_BOUND_TRANSLATIONS.csv |
| VAL3097_10_conditionals_nonclaim | True | conditional proxy bounds remain nonclaim | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3097_CONDITIONAL_BOUND_TRANSLATIONS.csv |
| VAL3097_11_component_parse | True | component status parses | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3097_COMPONENT_BOUND_STATUS.csv |
| VAL3097_12_component_blocked | True | component claims remain blocked | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3097_COMPONENT_BOUND_STATUS.csv |
| VAL3097_13_local_matrix_parse | True | local test matrix parses | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3097_LOCAL_TEST_MATRIX.csv |
| VAL3097_14_local_matrix_nonclaim | True | local test matrix records real anchors but missing MTS translations | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3097_LOCAL_TEST_MATRIX.csv |
| VAL3097_15_claim_gate_parse | True | claim gate parses | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3097_CLAIM_GATE.csv |
| VAL3097_16_physics_claims_blocked | True | all physics claims remain blocked | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3097_CLAIM_GATE.csv |
| VAL3097_17_decisions_parse | True | decision ledger parses | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3097_DECISION_LEDGER.csv |
| VAL3097_18_next_parse | True | next target parses | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3097_NEXT_TARGET.csv |
| VAL3097_19_next_selected | True | primary next target selected | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3097_NEXT_TARGET.csv |
| VAL3097_20_branch_copies_parse | True | branch copy ledger parses | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3097_BRANCH_COPIES.csv |
| VAL3097_21_branch_copies_exist | True | all branch copies exist | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3097_BRANCH_COPIES.csv |
| VAL3097_22_no_formalization_edit | True | no 3097 files created under formalization-workbench | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench |
| VAL3097_23_pycache_removed | True | scripts __pycache__ absent after run | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\scripts\__pycache__ |

## Working Interpretation
This is the Mayweather route: clean ropes, not a fake knockout. The project now has real local-test anchors around the coupling gap. The next fight is deriving one translation map cleanly enough that the first component can actually be constrained.
