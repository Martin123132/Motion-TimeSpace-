# 3482: Earth Source Amplitude `S_Eq` Current Bound Or Zero Theorem

## Current Verdict
- **Main correction:** `S_Eq` has two distinct meanings that must not be merged.
- **External-amplitude branch:** if a parent transport theorem gives an independent nonzero `S_Eq`, then the 3481 linear inverse envelope is usable after a lower bound.
- **Same-vector branch:** if `S_Eq = Q_Earth · C`, WEP becomes `eta_AB=(Q_Earth·C)(DeltaQ_AB·C)`, so the WEP rows are quadratic, not independent linear rows.
- **Concrete progress:** built a full four-channel bulk Earth DD proxy vector for the same visible basis, but kept it nonclaim because the parent MTS-to-DD/source-profile map is missing.

## Earth Full DD Element Rows
| element_charge_id | element | normalized_mass_fraction | A | Z | source_table | status | valid_for_claim | Q_hatm_full | weighted_Q_hatm_full | Q_delta_m | weighted_Q_delta_m | Q_m_e | weighted_Q_m_e | Q_e_full | weighted_Q_e_full |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EARTH3482_Fe | Fe | 3.204486280793110e-01 | 55.845 | 26 | WEB2789_0_MCDONOUGH_2003_TABLE5 | FULL_DD_FOUR_CHARGE_EARTH_ELEMENT_PROXY_NONCLAIM | False | 8.306053577251464e-02 | 2.661663473583485e-02 | 1.170471841704718e-04 | 3.750760958797414e-05 | 2.560658966783060e-04 | 8.205596528846177e-05 | 2.586494753657775e-03 | 8.288386953439696e-04 |
| EARTH3482_O | O | 2.974163829361106e-01 | 15.999 | 8 | WEB2789_0_MCDONOUGH_2003_TABLE5 | FULL_DD_FOUR_CHARGE_EARTH_ELEMENT_PROXY_NONCLAIM | False | 7.851861996928516e-02 | 2.335272394439986e-02 | -1.062566410400061e-07 | -3.160246584105931e-08 | 2.750171885742859e-04 | 8.179461747102235e-05 | 1.339626217819353e-03 | 3.984267841902142e-04 |
| EARTH3482_Si | Si | 1.612257160024034e-01 | 28.085 | 14 | WEB2789_0_MCDONOUGH_2003_TABLE5 | FULL_DD_FOUR_CHARGE_EARTH_ELEMENT_PROXY_NONCLAIM | False | 8.085791185976561e-02 | 1.303637473404994e-02 | 5.145095246572955e-06 | 8.295216650292870e-07 | 2.741677051807014e-04 | 4.420288457249444e-05 | 1.910342235889775e-03 | 3.079962947909612e-04 |
| EARTH3482_Mg | Mg | 1.542159022631684e-01 | 24.305 | 12 | WEB2789_0_MCDONOUGH_2003_TABLE5 | FULL_DD_FOUR_CHARGE_EARTH_ELEMENT_PROXY_NONCLAIM | False | 8.030628584650275e-02 | 1.238450632922233e-02 | 2.133305904134950e-05 | 3.289896948095155e-06 | 2.715490639786052e-04 | 4.187718391017944e-05 | 1.708533469369519e-03 | 2.634830305256417e-04 |
| EARTH3482_Ni | Ni | 1.822551572201082e-02 | 58.693 | 28 | WEB2789_0_MCDONOUGH_2003_TABLE5 | FULL_DD_FOUR_CHARGE_EARTH_ELEMENT_PROXY_NONCLAIM | False | 8.323040674602715e-02 | 1.516917086699073e-03 | 7.800078373911703e-05 | 1.421604510366444e-06 | 2.623822261598487e-04 | 4.782051388052522e-06 | 2.803286608543520e-03 | 5.109134415731232e-05 |
| EARTH3482_Ca | Ca | 1.712397356298818e-02 | 40.078 | 20 | WEB2789_0_MCDONOUGH_2003_TABLE5 | FULL_DD_FOUR_CHARGE_EARTH_ELEMENT_PROXY_NONCLAIM | False | 8.209240817909244e-02 | 1.405748227380814e-03 | 3.308548330755153e-06 | 5.665549414771991e-08 | 2.744647936523778e-04 | 4.699927870474324e-06 | 2.402572466508721e-03 | 4.114158739965865e-05 |
| EARTH3482_Al | Al | 1.592229120769077e-02 | 26.982 | 13 | WEB2789_0_MCDONOUGH_2003_TABLE5 | FULL_DD_FOUR_CHARGE_EARTH_ELEMENT_PROXY_NONCLAIM | False | 8.070097127368016e-02 | 1.284944365363023e-03 | 6.187087688088350e-05 | 9.851261189726094e-07 | 2.649914757986806e-04 | 4.219271445222334e-06 | 1.739360378563389e-03 | 2.769460246260553e-05 |
| EARTH3482_S | S | 6.408972561586221e-03 | 32.06 | 16 | WEB2789_0_MCDONOUGH_2003_TABLE5 | FULL_DD_FOUR_CHARGE_EARTH_ELEMENT_PROXY_NONCLAIM | False | 8.133781445403933e-02 | 5.212918210553292e-04 | 3.181534622582778e-06 | 2.039036809986960e-08 | 2.744853399875234e-04 | 1.759169012537702e-06 | 2.083706103989026e-03 | 1.335441524687539e-05 |
| EARTH3482_Cr | Cr | 4.706589224914881e-03 | 51.996 | 24 | WEB2789_0_MCDONOUGH_2003_TABLE5 | FULL_DD_FOUR_CHARGE_EARTH_ELEMENT_PROXY_NONCLAIM | False | 8.283844121319336e-02 | 3.898865148227607e-04 | 1.306485114239558e-04 | 6.149088761191588e-07 | 2.538656819755366e-04 | 1.194841483361728e-06 | 2.428620629658680e-03 | 1.143051968695753e-05 |
| EARTH3482_Na | Na | 1.802523532946125e-03 | 22.99 | 11 | WEB2789_0_MCDONOUGH_2003_TABLE5 | FULL_DD_FOUR_CHARGE_EARTH_ELEMENT_PROXY_NONCLAIM | False | 8.006667948721528e-02 | 1.443220739805603e-04 | 7.320574162679414e-05 | 1.319550720290702e-07 | 2.631578947368422e-04 | 4.743482981437172e-07 | 1.548025572283397e-03 | 2.790352523643216e-06 |
| EARTH3482_P | P | 7.009813739234929e-04 | 30.974 | 15 | WEB2789_0_MCDONOUGH_2003_TABLE5 | FULL_DD_FOUR_CHARGE_EARTH_ELEMENT_PROXY_NONCLAIM | False | 8.121484913421094e-02 | 5.693009652908838e-05 | 5.345773874862790e-05 | 3.747287915485633e-08 | 2.663524246141926e-04 | 1.867080885539103e-07 | 1.919423415247180e-03 | 1.345480062760891e-06 |
| EARTH3482_Mn | Mn | 8.011215701982776e-04 | 54.938 | 25 | WEB2789_0_MCDONOUGH_2003_TABLE5 | FULL_DD_FOUR_CHARGE_EARTH_ELEMENT_PROXY_NONCLAIM | False | 8.296632521900278e-02 | 6.646611273302846e-05 | 1.528013396920165e-04 | 1.224124491824687e-07 | 2.502821362262915e-04 | 2.005064179661859e-07 | 2.445282343677738e-03 | 1.958968430745234e-06 |
| EARTH3482_C | C | 7.009813739234929e-04 | 12.011 | 6 | WEB2789_0_MCDONOUGH_2003_TABLE5 | FULL_DD_FOUR_CHARGE_EARTH_ELEMENT_PROXY_NONCLAIM | False | 7.712764668661043e-02 | 5.406504374186592e-05 | 1.556906169344659e-06 | 1.091362225657181e-09 | 2.747481475314296e-04 | 1.925933339395160e-07 | 1.109419135739533e-03 | 7.776821500277118e-07 |
| EARTH3482_H | H | 3.004205888243541e-04 | 1.008 | 1 | WEB2789_0_MCDONOUGH_2003_TABLE5 | FULL_DD_FOUR_CHARGE_EARTH_ELEMENT_PROXY_NONCLAIM | False | 3.772537274694801e-02 | 1.133347869425636e-05 | -1.673015873015873e-03 | -5.026084136839194e-07 | 5.456349206349206e-04 | 1.639199641402726e-07 | 6.734920634920634e-04 | 2.023308822828150e-07 |

## Earth Full DD Source Vector
| source_vector_id | source_body | basis | Q_hatm_full_Earth | Q_delta_m_Earth | Q_m_e_Earth | Q_e_full_Earth | source_vector_norm | unit_Q_hatm_full_Earth | unit_Q_delta_m_Earth | unit_Q_m_e_Earth | unit_Q_e_full_Earth | normalized_mass_fraction_sum | source_rows | formula_source_path | claim_status | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EARTH3482_0_bulk_full_DD_four_charge | Earth | full_Damour_Donoghue_four_charge_proxy | 8.084214456450678e-02 | 4.448443445187145e-05 | 2.678039885445502e-04 | 1.950532087853656e-03 | 8.086612771151806e-02 | 9.997034215970271e-01 | 5.500997229713445e-04 | 3.311695466610130e-03 | 2.412050809223841e-02 | 1.000000000000000e+00 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_2789_BULK_EARTH_COMPOSITION_TARGET.csv | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3472_DD_FOUR_CHARGE_FORMULA_AUDIT.csv | NUMERIC_BULK_EARTH_DD_SOURCE_VECTOR_NONCLAIM_PARENT_MAP_MISSING | False |

## Source/Test Geometry
| geometry_id | row_id | arena | earth_vector_norm | test_delta_norm | source_test_unit_cosine | same_vector_quadratic_form | meaning | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SG3482_MATRIX3473_0_MICROSCOPE_TA6V_minus_PtRh10 | MATRIX3473_0_MICROSCOPE_TA6V_minus_PtRh10 | MICROSCOPE_TIPT_EARTH_FIELD | 8.086612771152e-02 | 3.319060979691e-03 | -8.239869108681e-01 | eta ~= (8.086613e-02 e_hat·C) * (3.319061e-03 u_AB·C) | if S_Eq=Q_Earth·C, this WEP row is quadratic in C, not a linear row with an external source amplitude | False |
| SG3482_MATRIX3473_1_EOTWASH_Be_minus_Ti | MATRIX3473_1_EOTWASH_Be_minus_Ti | EOTWASH_BETI_EARTH_FIELD | 8.086612771152e-02 | 7.391652369629e-03 | -9.820641235791e-01 | eta ~= (8.086613e-02 e_hat·C) * (7.391652e-03 u_AB·C) | if S_Eq=Q_Earth·C, this WEP row is quadratic in C, not a linear row with an external source amplitude | False |

## `S_Eq` Branch Logic
| branch_id | assumption | math_form | what_3481_buys | needed_for_claim | status | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| BR3482_0_external_transport_amplitude | S_Eq is a parent-owned source transport amplitude independent of the visible coefficient vector C | eta_AB = S_Eq (DeltaQ_AB · C) | N_AB=/S_Eq/^-1///DeltaQ_AB// and 3480 linear inverse can be used if /S_Eq/ has a lower bound | derive S_Eq != 0 lower bound or a sourced normalization value from J_q/H_tau | CONDITIONAL_BRANCH_ONLY | False |
| BR3482_1_same_visible_vector_DD | S_Eq is the Earth body coupling built from the same visible vector C | S_Eq = Q_Earth · C, so eta_AB = (Q_Earth · C)(DeltaQ_AB · C) | the row-norm factors remain useful, but the WEP rows are quadratic constraints, not independent linear rank rows | solve/score the mixed quadratic WEP plus linear clock system or prove Q_Earth·C=0/source silence | MORE_PHYSICAL_DD_BRANCH_REQUIRES_NONLINEAR_RUNNER | False |
| BR3482_2_zero_source_current | J_q^A=0 or projects to S_Eq=0 in the local compact Earth source | S_Eq=0 => eta_AB source product vanishes | WEP source channel would be locally silent, but WEP no longer bounds C_i through that source | parent-sign all residual-current zero families and prevent readout reentry | EXACT_CONDITIONAL_NOT_PARENT_SIGNED | False |

## Bound Obstruction Theorems
| theorem_id | statement | proof | consequence | valid_for_claim |
| --- | --- | --- | --- | --- |
| OBS3482_0_lower_bound_obstruction | A WEP upper bound on /S_Eq Y_AB/ cannot give an upper bound on /Y_AB/ or /C_i/ without a lower bound on /S_Eq/. | For any measured bound B and any candidate Y_AB, choosing sufficiently small nonzero /S_Eq/ keeps /S_Eq Y_AB/ <= B. | 3481 coefficient envelopes containing abs_S_Eq_inv are not empirical coefficient bounds until /S_Eq/ >= L_E > 0 is derived. | False |
| OBS3482_1_upper_bound_different_use | An upper bound on /S_Eq/ helps prove a small WEP product for assumed C_i priors, but it cannot isolate C_i. | The inequality /S_Eq Y/ <= U_E /Y/ is product-side, not inverse-side. | source-current no-hair can support local-silence/product closure, while coefficient extraction needs source lower bound or clock-only routes. | False |
| OBS3482_2_same_vector_quadratic_guard | If S_Eq=Q_Earth·C, WEP constraints are quadratic in C and must not be used as independent linear rows in the 3475 rank matrix. | Substitution gives eta_AB=(Q_Earth·C)(DeltaQ_AB·C), a product of two linear forms. | future runner must branch: external-amplitude linear inverse, or DD same-vector nonlinear score. | False |

## Residual Family Reduction
| reduction_id | residual_id | source_current_piece | feeds_S_Eq_through | current_status | required_zero_or_bound | bound_role | priority | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SRR3482_RCS2446_0_reference_boundary | RCS2446_0_reference_boundary | J_q^boundary + partial_q(B_ref) + q-sensitive boundary/corner flux | H_tau source-charge sensitivity and deltaH integrability | NOT_PARENT_FIXED | fixed B_ref plus exact/cohomology/nohair boundary theorem, or source-backed boundary residual row | contributes to U_E upper/product-silence bound; lower-bound use requires sign/nonzero source theorem | P2_supporting_source_residual | False |
| SRR3482_RCS2446_1_extra_nonEH | RCS2446_1_extra_nonEH | J_q^extra from motion/time/domain/memory/range/non-EH sectors | direct q-current and non-EH source charge | NOT_EXTRACTED | sector-by-sector no-source/topological/proper-gauge theorem or executable coefficient vector | contributes to U_E upper/product-silence bound; lower-bound use requires sign/nonzero source theorem | P2_supporting_source_residual | False |
| SRR3482_RCS2446_2_projector_domain | RCS2446_2_projector_domain | J_q^projector + [d,Pi_M]J_H + delta Pi_M source terms | mass/source projection and radial/source stability | NOT_EXTRACTED | parent-owned Pi_M/P_loc chain map, covariant constancy, domain/homology rule, or commutator bound | contributes to U_E upper/product-silence bound; lower-bound use requires sign/nonzero source theorem | P1_PiM_projector_source_lock | False |
| SRR3482_RCS2446_3_matter_source_glue | RCS2446_3_matter_source_glue | J_q^matter/source glue from coframe, worldtube denominator, Hilbert-current equality and source composition | direct WEP/R10 source current and observed source equality | CONDITIONAL_NOT_GLUED | same observed coframe, parent matter functor, Hilbert/source equality, worldtube denominator theorem | contributes to U_E upper/product-silence bound; lower-bound use requires sign/nonzero source theorem | P0_direct_WEP_source_current | False |
| SRR3482_RCS2446_4_coupling_constant | RCS2446_4_coupling_constant | partial_q G_eff/kappa/source-normalization drift | common source normalization, Gdot, range/species/frame dependence | NOT_PARENT_DERIVED | constant universal G_ref/kappa theorem or sourced Gdot/range/species/frame bounds | contributes to U_E upper/product-silence bound; lower-bound use requires sign/nonzero source theorem | P0_Newton_G_source_normalization | False |
| SRR3482_RCS2446_5_readout_PPN_tail | RCS2446_5_readout_PPN_tail | J_q^readout + second-order PPN/source-response tail | metric/readout source leg and PPN vector | DOWNSTREAM_NOT_READY | weak-field/PPN response matrix from same source charge and metric readout | contributes to U_E upper/product-silence bound; lower-bound use requires sign/nonzero source theorem | P2_supporting_source_residual | False |
| SRR3482_RCS2446_6_EM_clock_mass_coupling_guard | RCS2446_6_EM_clock_mass_coupling_guard | J_q^visible_coefficients from alpha, mass, binding, clock and source-weight leakage | WEP/R10/clock product rows S_E^q*b_i and source-weight products | GUARD_ONLY_RETAINED | EM-lock/mass-owner/source-scalar/readout theorem-zero or finite product rows | contributes to U_E upper/product-silence bound; lower-bound use requires sign/nonzero source theorem | P1_visible_coefficient_reentry | False |

## `abs_S_Eq` Source-Ready Rows
| row_id | quantity | needed_for | candidate_value | units | available_proxy | why_proxy_not_claim | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| SEQ3482_0_abs_S_Eq_lower_bound | L_E <= /S_Eq/ | turn 3481 WEP coefficient envelopes into empirical upper bounds on C_i | MISSING_LOWER_BOUND_OR_PARENT_NONZERO_THEOREM | dimensionless_source_amplitude | bulk full-DD Earth charge norm = 8.086612771152e-02 | DD proxy is not parent MTS transport; if same-vector, source amplitude is Q_Earth·C and can vanish by direction | False |
| SEQ3482_1_abs_S_Eq_upper_bound | /S_Eq/ <= U_E | product-silence/local-GR source-current suppression branch | MISSING_UPPER_BOUND_OR_ZERO_THEOREM | dimensionless_source_amplitude | residual families named in 2446 and source-normalization channels in 657 | families are not numerically bounded or zero-derived | False |
| SEQ3482_2_same_vector_runner_input | Q_Earth_full_DD_vector | nonlinear WEP runner eta=(Q_Earth·C)(DeltaQ·C) | SEE_P8_Y5_R2FR_3482_EARTH_FULL_DD_SOURCE_VECTOR_NONCLAIM.csv | dimensionless_DD_charge_proxy | source-backed bulk Earth composition plus DD four-charge formulas | bulk/profile/worldtube weighting and MTS-to-DD coefficient map remain missing | False |

## Claim Gates
| gate_id | requirement | passed | evidence | valid_for_claim |
| --- | --- | --- | --- | --- |
| CG3482_0_full_dd_earth_vector | bulk Earth full DD four-charge proxy is finite and nonzero | True | norm=8.086612771152e-02 | False |
| CG3482_1_external_source_lower_bound | derive /S_Eq/ >= L_E > 0 for linear inverse WEP coefficient bound | False | no parent lower-bound/nonzero theorem; only proxy source vector | False |
| CG3482_2_same_vector_guard | if S_Eq=Q_Earth·C, WEP rows are marked quadratic not linear | True | BR3482_1 and OBS3482_2 written | False |
| CG3482_3_residual_family_reduction | S_Eq reduced to named residual current families | True | families=7 | False |
| CG3482_4_no_claim | no WEP/local-GR/Newton/source-coupling pass claimed | True | all generated rows valid_for_claim=false | False |

## Decision
| decision_id | decision | rationale | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- |
| DEC3482_0_branch_split | The WEP source throat must split into external-amplitude linear branch and same-visible-vector quadratic branch. | if S_Eq is Q_Earth·C, WEP constraints are quadratic and cannot be used as independent linear rank rows. | False | False |
| DEC3482_1_dd_proxy_value | A full-DD bulk Earth source vector can be built, but it is a nonclaim comparator, not parent MTS S_Eq. | bulk composition/profile/worldtube weighting and MTS-to-DD coefficient map are missing. | False | False |
| DEC3482_2_best_next_attack | Build the nonlinear WEP same-vector runner while carrying clock rows separately, then compare with the external-amplitude branch. | this tests the physically natural DD structure without smuggling a source lower bound. | False | False |

## Next Target
| next_doc | next_script | objective | success_gate | exclude | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| 3483-Y5-R2FR-quadratic-DD-WEP-source-runner-or-external-SEq-lower-bound.md | scripts/Y5_R2FR_3483_quadratic_DD_WEP_source_runner_or_external_SEq_lower_bound.py | Implement the same-vector nonlinear WEP branch eta=(Q_Earth·C)(DeltaQ·C), keep clock rows linear/product-only, and compare it against the external S_Eq branch without using S_Eq=1. | WEP rows are no longer accidentally treated as independent linear rows when the Earth source is the same visible coefficient vector | local-GR claim; GitHub; formalization-workbench edits; setting source amplitude to unity; ignoring clock transport | False | False |

## Source Register
| timestamp_utc | source_id | source_path | exists | role | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| 2026-06-29T03:47:30.363333+00:00 | script_3482 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\scripts\Y5_R2FR_3482_earth_source_amplitude_SEq_current_bound_or_zero_theorem.py | True | generator | False |
| 2026-06-29T03:47:30.363333+00:00 | doc_3481 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\3481-Y5-R2FR-source-current-Jq-theorem-or-first-transport-normalizer-row.md | True | 3481 handoff | False |
| 2026-06-29T03:47:30.363333+00:00 | wep_norm_3481 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3481_WEP_SHARED_EARTH_NORMALIZER_ROWS_NONCLAIM.csv | True | shared WEP normalizer rows | False |
| 2026-06-29T03:47:30.363333+00:00 | wep_collapse_3481 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3481_WEP_COLLAPSED_BOUND_FACTORS.csv | True | WEP collapsed bounds containing abs_S_Eq_inv | False |
| 2026-06-29T03:47:30.363333+00:00 | matrix_3475 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3475_AUGMENTED_FULL_RANK_MATRIX.csv | True | full-rank row matrix | False |
| 2026-06-29T03:47:30.363333+00:00 | earth_composition_2789 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_2789_BULK_EARTH_COMPOSITION_TARGET.csv | True | bulk Earth composition proxy | False |
| 2026-06-29T03:47:30.363333+00:00 | dd_formula_3472 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3472_DD_FOUR_CHARGE_FORMULA_AUDIT.csv | True | full DD four-charge formula audit | False |
| 2026-06-29T03:47:30.363333+00:00 | dd_source_proxy_2789 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_2789_DD_EARTH_SOURCE_VECTOR_FIRST_ROW_NONCLAIM.csv | True | older two-component DD Earth source proxy | False |
| 2026-06-29T03:47:30.363333+00:00 | source_caveat_2789 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_2789_SOURCE_VECTOR_CAVEAT_GATE.csv | True | Earth source vector caveat gates | False |
| 2026-06-29T03:47:30.363333+00:00 | source_leg_2444 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_2444_SOURCE_LEG_DERIVATION_CONTRACT.csv | True | S_Eq contract | False |
| 2026-06-29T03:47:30.363333+00:00 | jq_attempt_2445 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_2445_JQ_SOURCE_CURRENT_EXTRACTION_ATTEMPT.csv | True | J_q extraction attempt | False |
| 2026-06-29T03:47:30.363333+00:00 | residual_pack_2446 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_2446_MTS_RESIDUAL_CURRENT_PACK_FOR_S_EQ.csv | True | S_Eq residual current pack | False |
| 2026-06-29T03:47:30.363333+00:00 | source_norm_stack | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_SOURCE_NORMALIZATION_THEOREM_STACK.csv | True | source normalization theorem stack | False |
| 2026-06-29T03:47:30.363333+00:00 | source_zero_targets | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_SOURCE_NORMALIZATION_DERIVED_ZERO_TARGETS.csv | True | source normalization zero targets | False |

## Validation
| check_id | passed | detail | valid_for_claim |
| --- | --- | --- | --- |
| VAL3482_0_sources_exist | True | all local sources exist | False |
| VAL3482_1_csv_parse | True | source_register:14; earth_elements:14; earth_vector:1; source_geometry:2; branch_logic:3; obstructions:3; residual_reduction:7; source_ready:3; claim_gates:5; decision:3; next:1; validation:pending | False |
| VAL3482_2_earth_mass_fraction | True | sum=1.000000000000000e+00 | False |
| VAL3482_3_earth_vector_nonzero | True | norm=8.086612771152e-02 | False |
| VAL3482_4_branch_split_present | True | branches=3 | False |
| VAL3482_5_quadratic_guard_present | True | same-vector WEP quadratic guard written | False |
| VAL3482_6_residual_reduction | True | families=7 | False |
| VAL3482_7_no_claim | True | all generated rows valid_for_claim=false | False |
| VAL3482_8_no_formalization_outputs | True | outputs are under post-checkpoint-work/source-intake only | False |
| VAL3482_9_git_formalization_clean | True | NOT_A_GIT_REPOSITORY | False |
| VAL3482_SUMMARY | True | PASS | False |
