# 3264 - Parent source-charge meaning or multichannel WEP vector under AX1090

Private derivation/checkpoint. This does not claim local GR, Newton, Maxwell, WEP, R10, PPN, clock, orbital, material-response, or public source-coupling success.

## Verdict
- `3264` adds the second dominant DD channel, `Q'_hatm`, so the Ti/Pt WEP branch is no longer EM-only.
- The source-backed two-channel form is `eta_TiPt = Delta_Qhatm D_hatm + Delta_Qe D_e + residual`.
- A single Ti/Pt WEP pair gives a **strip**, not independent bounds on `D_hatm` and `D_e`; cancellation directions remain.
- This is progress because it tells us exactly what extra evidence is needed: a second material/test vector or a parent no-cancellation/source map.

## Source Register
| source_id | exists | parse_ok | role | evidence_hits | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| SRC3264_3263_handoff | true | true | 3263 selected parent source-charge meaning or multichannel WEP vector | L6:- `3263` closes the experimental EP-channel projection for the **eta-level** convention: MICROSCOPE fits `delta_x g_x` and identifies final `eta` with `delta_x` in practice. \| L8:- The conservative eta-level bound remains `\|B_alpha^eta\| <= 1.389797711688e-12` after the 0.98 readout factor. \| L31:## Eta-Level vs Parent-Source Convention Split \| L40:\| PROJ3263_0_observed_eta_channel \| eta_AB -> MICROSCOPE fitted delta_x \| SOURCE_BACKED \| delta_x = tilde(a)_c11 eta_AB with \\|tilde(a)_c11-1\\|<2e-2 and final eta practically identified with delta_x \| the experimental channel projection is not a remaining blocker for eta-level bo | false |
| SRC3264_DD_tex | true | true | Damour-Donoghue source formulas for Q'_hatm and Q'_e | L487:\frac{1}{M_A}\bigl[ (d_{\hat m}-d_g) \, \hat m \frac{\partial M_A}{\partial {\hat m}} + (d_{\delta m}-d_g) \, \delta m \frac{\partial M_A}{\partial {\delta m}} \nonumber \\ \| L504:% \frac{1}{M_A} \, \Bigl[ (d_{\hat m}-d_g) \delta_{\hat m}M_A \nonumber \\ \| L780:\bar\alpha_A^{\rm r \, m \, wo. \, EM} &= &(d_{\hat m} - d_g) \, \frac{A \sigma}{m_A} + \frac{1}{2} (d_{\delta_m} - d_g) \, \frac{(N-Z) \delta}{m_A} \nonumber \\ \| L786:\bar\alpha_A^{\rm r \, m \, wo. \, EM} &\simeq & F_A\Bigl[ 0.048 (d_{\hat m} - d_g) + 0.0017 (d_{\delta_m} - d_g) \, \frac{A-2Z}{A} \nonumber \\ | false |
| SRC3264_1909_composition | true | true | TA6V/PtRh10 alloy composition inputs | L2:AC1909_PtRh10_Pt,PtRh10,Pt,0.900000000000,195.1,78,WEB983_0_MICROSCOPE_CQG_COMPOSITION,D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_983_MATERIA \| L4:AC1909_TA6V_Ti,TA6V,Ti,0.900000000000,47.9,22,WEB983_0_MICROSCOPE_CQG_COMPOSITION,D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_983_MATERIAL_CON | false |
| SRC3264_3263_bounds | true | true | eta-level and conservative readout-corrected bound | L3:CB3263_1_eta_level_readout_conservative,CONV3263_ETA_LEVEL,\|B_alpha^eta\| with tau_readout_X>=0.98,(2.7e-15/\|DeltaQe_DD\|)/0.98,1.389797711688e-12,CONSERVATIVE_READOUT_CORRECTED_BOUND,false | false |

## DD Multichannel Evidence
| evidence_id | line_number | text_excerpt | role | valid_for_claim |
| --- | --- | --- | --- | --- |
| DDE3264_0_alpha_two_channel | 1120 | \left( \frac{\Delta a}{a} \right)_{BC} = (\alpha_B- \alpha_C)\alpha_E = \left[D_{\hat m} Q'_{\hat m} + D_e Q'_e \right]_{BC} | DD two-dominant-channel WEP form. | false |
| DDE3264_1_qhatm | 1071 | Q'_{\hat m} = -\frac{0.036}{A^{1/3}} - 1.4 \times 10^{-4} \, \frac{Z(Z-1)}{A^{4/3}} | DD reduced light-quark/nuclear-mass charge. | false |
| DDE3264_2_qe | 1075 | Q'_{e} = + 7.7 \times 10^{-4} \frac{Z(Z-1)}{A^{4/3}} . | DD electromagnetic charge. | false |

## Element Charges
| element_charge_id | material_id | element | mass_fraction | A_context | Z | Qhatm_prime_element | Qe_prime_element | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EL3264_PtRh10_Pt | PtRh10 | Pt | 9.000000000000e-01 | 1.951000000000e+02 | 7.800000000000e+01 | -6.950106254842e-03 | 4.086953475170e-03 | false |
| EL3264_PtRh10_Rh | PtRh10 | Rh | 1.000000000000e-01 | 1.029000000000e+02 | 4.500000000000e+01 | -8.257282215231e-03 | 3.161807430516e-03 | false |
| EL3264_TA6V_Ti | TA6V | Ti | 9.000000000000e-01 | 4.790000000000e+01 | 2.200000000000e+01 | -1.028448169604e-02 | 2.044962505058e-03 | false |
| EL3264_TA6V_Al | TA6V | Al | 6.000000000000e-02 | 2.700000000000e+01 | 1.300000000000e+01 | -1.226962962963e-02 | 1.482962962963e-03 | false |
| EL3264_TA6V_V | TA6V | V | 4.000000000000e-02 | 5.090000000000e+01 | 2.300000000000e+01 | -1.008950469636e-02 | 2.065463535757e-03 | false |

## Material Charges
| material_charge_id | material_id | Qhatm_prime | Qe_prime | mass_fraction_sum | basis | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| MAT3264_PtRh10 | PtRh10 | -7.080823850881e-03 | 3.994438870705e-03 | 1.000000000000e+00 | DD approximate two-charge basis; mass-fraction alloy average | false |
| MAT3264_TA6V | TA6V | -1.039579149207e-02 | 2.012062573760e-03 | 1.000000000000e+00 | DD approximate two-charge basis; mass-fraction alloy average | false |

## Ti/Pt DD Delta Vector
| delta_id | left_minus_right | Delta_Qhatm_prime | Delta_Qe_prime | delta_vector_norm | eta_formula | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| DELTA3264_TA6V_minus_PtRh10 | TA6V_minus_PtRh10 | -3.314967641189e-03 | -1.982376296945e-03 | 3.862489643328e-03 | eta_TiPt = Delta_Qhatm_prime*D_hatm + Delta_Qe_prime*D_e + residual | false |

## Multichannel WEP Bounds
| bound_id | assumption | formula | value | interpretation | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| MB3264_0_two_channel_strip | two DD channels retained; conservative eta bound; no residual | \|Delta_Qhatm*D_hatm + Delta_Qe*D_e\| <= eta_bound | 2.755102040816e-15 | one Ti/Pt WEP pair gives a strip, not separate D_hatm/D_e bounds | false |
| MB3264_1_qhatm_single_channel | D_e=0 and residual=0 | \|D_hatm\| <= eta_bound/\|Delta_Qhatm\| | 8.311097841752e-13 | single-channel smoke bound only | false |
| MB3264_2_qe_single_channel | D_hatm=0 and residual=0 | \|D_e\| <= eta_bound/\|Delta_Qe\| | 1.389797711495e-12 | matches the EM-only conservative scale | false |
| MB3264_3_parallel_min_norm | coupling vector parallel to Ti/Pt DD vector | \|D_parallel\| <= eta_bound/\|\|Delta_Q\|\| | 7.132969393395e-13 | minimum-norm aligned bound, not a general two-parameter bound | false |

## Two-Channel Degeneracy Guard
| guard_id | statement | orthogonal_direction | math | valid_for_claim |
| --- | --- | --- | --- | --- |
| DEG3264_0_orthogonal_flat_direction | A single Ti/Pt WEP pair cannot bound the coupling component orthogonal to its DD charge-difference vector. | (D_hatm,D_e) proportional to (-1.982376296945e-03,3.314967641189e-03) | Delta_Qhatm*D_hatm + Delta_Qe*D_e = 0 along this direction | false |
| DEG3264_1_no_cancellation_guard | The EM-only bound is not a full WEP pass because D_hatm and D_e can cancel in this material pair. | requires another material pair, clock/R10 cross-channel, or parent no-cancellation theorem | do not infer both \|D_hatm\| and \|D_e\| are small from one scalar eta | false |

## Claim Gates
| gate_id | gate | passed | reason | claim_allowed |
| --- | --- | --- | --- | --- |
| CG3264_0_multichannel_vector | two-channel DD Ti/Pt vector computed | true | Q'_hatm and Q'_e are sourced and alloy-averaged from local composition rows | false |
| CG3264_1_individual_channel_bounds | individual D_hatm and D_e bounded without assumptions | false | one WEP pair gives a strip; single-channel bounds require assumptions | false |
| CG3264_2_parent_source_meaning | D_hatm/D_e identified with MTS parent source factors | false | external DD coefficients are calibration coordinates until parent source-charge map is signed | false |
| CG3264_3_local_GR | local GR/Newton/Maxwell promotion | false | multichannel vector is evidence plumbing, not a fixed-EM or full-source theorem | false |

## Decision
| decision_id | verdict | what_moved | best_next | fallback_next | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| DEC3264_0 | MULTICHANNEL_WEP_VECTOR_BUILT_SINGLE_PAIR_DEGENERATE | Ti/Pt now has Delta_Qhatm=-3.314967641189e-03 and Delta_Qe=-1.982376296945e-03 | add another material/test arena or derive parent no-cancellation/source map | use single-channel bounds only as clearly marked smoke diagnostics | false |

## Next Target
| next_id | selected | target_doc | target_script | objective | guardrail | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| NEXT3264_0_3265 | primary | 3265-Y5-R2FR-second-material-arena-or-parent-no-cancellation-theorem-under-AX1090.md | scripts/Y5_R2FR_3265_second_material_arena_or_parent_no_cancellation_theorem.py | Either add a second independent material/test vector to break the DD two-channel degeneracy, or derive the parent no-cancellation/source map that lets one channel be isolated. | Do not treat EM-only or qhatm-only bounds as full WEP/local-GR evidence. | false |

## Validation
| check_id | check | passed | detail |
| --- | --- | --- | --- |
| VAL3264_0_sources_exist | all cited source paths exist | true |  |
| VAL3264_1_sources_parse | all cited source CSV/MD/TEX paths parse | true |  |
| VAL3264_2_DD_lines_found | DD multichannel evidence lines are found | true | DDE3264_0_alpha_two_channel:1120;DDE3264_1_qhatm:1071;DDE3264_2_qe:1075 |
| VAL3264_3_outputs_parse | all 3264 output CSVs parse | true |  |
| VAL3264_4_material_rows | TA6V and PtRh10 material charges exist | true | PtRh10;TA6V |
| VAL3264_5_delta_numeric | Delta vector entries are finite numeric | true | -3.314967641189e-03;-1.982376296945e-03 |
| VAL3264_6_claim_gates_false | no 3264 claim gate allows local-GR/WEP/Maxwell promotion | true | all claim_allowed=false |
| VAL3264_7_formalization_untouched | formalization-workbench modified-file count remains zero by this script | true | formalization_changed_count=0 |
| VAL3264_8_overall | 3264 validation overall | true | all required checks passed |

Generated UTC: 2026-06-27T06:08:22.138694+00:00
