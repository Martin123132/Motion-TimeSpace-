# 3260 - Fixed EM owner zero theorem or DD WEP bound runner under AX1090

Private derivation/checkpoint. This does not claim local GR, Newton, Maxwell, WEP, R10, PPN, clock, orbital, material-response, or public source-coupling success.

## Verdict
- The fixed-EM zero theorem is still **not** closed: the no-counterterm/readout/no-extra-vertex clauses remain unsigned.
- The fallback DD branch now has a real MICROSCOPE Ti/Pt bound runner.
- With `DeltaQ'_e(TA6V-PtRh10)=-1.982376296670e-3` and the reported MICROSCOPE level `2.7e-15`, the isolated EM branch requires `|B_alpha^MTS| <= 1.362001757454e-12`.
- This is not a pass/fail claim yet; it is a hard scale for the combined product `B_alpha^MTS=beta_source_alpha*b_alpha_EM*tau_WEP`.

## Source Register
| source_id | exists | parse_ok | role | evidence_hits | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| SRC3260_3259_handoff | true | true | 3259 selected fixed-EM zero theorem or DD WEP bound runner | L8:- For the Ti/Pt branch, `DeltaQ'_e(TA6V-PtRh10)=-1.982376296670e-3`, so `eta_EM = -1.982376296670e-3 B_alpha^MTS + residual`. \| L39:\| PB3259_2_pair_difference \| For a material pair, common-mode terms cancel and the differential EM residual is controlled by the DD charge difference. \| DeltaR_AB^EM = b_alpha^P DeltaQ'_e,AB + Delta r_AB^EM \| EXACT_PAIR_PULLBACK_LAW \| source coupling is now a scalar product coeff \| L41:\| PB3259_4_controlled_DD_branch \| If alpha_EM is not parent-fixed, DD is demoted/promoted only to a finite residual input with source/readout product still required. \| eta_AB^EM = DeltaQ'_e,AB B_alpha^MTS + Delta eta_res, B_alpha^MTS:=beta_source_alpha b_alpha_EM tau_WEP \| FINITE \| L47:\| BR3259_DD_BOUND \| controlled alpha residual \| parent action permits or fails to exclude alpha_EM pullback \| retain eta_AB^EM=DeltaQ'_e,AB B_alpha^MTS and bound B_alpha^MTS with WEP/clock/orbital data \| NUMERIC_COMPOSITION_VECTOR_READY_SOURCE_PRODUCT_MISSING \| prevents alpha cou | false |
| SRC3260_3259_residual_vector | true | true | DD-calibrated Ti/Pt EM residual vector | L4:RV3259_TA6V_minus_PtRh10_EM,TA6V_minus_PtRh10,-1.982376296670e-03,"R_A^EM = Q'_e,A b_alpha^P + r_A^EM","eta_AB^EM = DeltaQ'_e,AB B_alpha^MTS + Delta eta_res",NUMERIC_EXTERNAL_VECTOR_PARENT_PRODUCT_MISSING,false \| L5:RV3259_TA6V_minus_PtRh10_unit_product,TA6V_minus_PtRh10,-1.982376296670e-03,DeltaR_TA6V-PtRh10^EM = (-1.982376296670e-3) b_alpha^P + Delta r_EM,eta_TA6V-PtRh10^EM = (-1.982376296670e-3) B_alpha^MTS + Delta eta_res,ABS_DELTA_QE=1.982376296670e-03,false | false |
| SRC3260_3259_parent_audit | true | true | parent alpha owner clauses | L2:AUD3259_0_EM_owner,observed EM connection and kinetic normalization are parent-owned fixed representation/topological data,PAC1055_1_EM_owner,CANDIDATE_CLAUSE_PRESENT_NOT_PARENT_SIGNED,b_alpha^P=0 on local vertical paths unless a separate allowed alpha deformation is declared,fal \| L3:AUD3259_1_no_counterterm,no independent lambda_A F_Q^2 or hidden f(X)F_Q^2 slot,EMU1234_2_unique_F2;UMF1397_7_current_verdict,CURRENT_CORPUS_FAILS_TO_EXCLUDE_COUNTERTERM,removes standalone alpha drift branch,false | false |
| SRC3260_1055_parent_contract | true | true | fixed EM owner candidate | L3:PAC1055_1_EM_owner,observed EM connection and kinetic normalization are owned by fixed representation/topological data,"S_EM = -1/(4 g_*^2(ell_EM)) int sqrt(-g_obs(q)) F_Q^2 + S_int[A_Q,J_Q(theta_A)], with Lie_v ell_EM=0 and no f(Xhat)F_Q^2 slot","Lie_v alpha_EM=0, b_alpha=0, and | false |
| SRC3260_1397_unique_F2 | true | true | unique F2/no counterterm audit | L4:UMF1397_2_operator_basis_uniqueness,no independent Maxwell quadratic invariant,"the parent operator basis forbids every observed-only F_Q^2 term not inherited from <F,F>_P","Allowed_2der(parent, U(1)_Q) = {<F,F>_P subblock} and not {<F,F>_P, F_Q^2}",RCE765_0 and ELA989_1 keep Del \| L5:UMF1397_3_no_observed_counterterm_principle,no quotient-only counterterms in the parent action,the action principle is parent-local only and cannot contain extra terms written solely in observed quotient fields,S_parent[Phi] is varied upstairs; DeltaS[q(Phi)] with independent coe \| L6:UMF1397_4_renormalized_coefficient_owner,radiative/renormalized Maxwell coefficient has the same parent owner,renormalization cannot regenerate a separately running lambda_A after quotienting,"d ln(g_EM^{-2})/d phi_c = d ln(C_P N_Q)/d phi_c, not d ln(C_P N_Q+lambda_A)/d phi_c",no \| L7:UMF1397_5_measure_boundary_silence,"measure, Hodge star, and boundary projection add no F_Q^2 residue",projection to observed measure/coframe does not create an independent Maxwell kinetic density,"dmu_obs * F_Q^2 coefficient is only the projection of dmu_P <F,F>_P",765 and 989 l | false |
| SRC3260_MICROSCOPE_tex | true | true | MICROSCOPE final Ti/Pt WEP result source | L102:The space mission MICROSCOPE dedicated to the test of the Equivalence Principle (EP) operated from April 25, 2016 {until} the deactivation of the satellite on October 16, 2018. {In this analysis we compare the free-fall accelerations ($a_{\rm A}$ and $a_{\rm B}$) of two test mass \| L936:\eta({\rm{Ti, Pt}}) \simeq\delta({\rm{Ti, Pt}})=[-1.5\pm{}2.3{\rm (stat)}\pm{}1.5{\rm (syst)}] \times{}10^{-15} \ \rm{at} ~1\sigma. \| L962:This led again to no detection of violation of the WEP since we obtained $\eta({\rm{Ti, Pt}}) =[-1.5\pm{}2.3{\rm (stat)}\pm{}1.5{\rm (syst)}] \times{}10^{-15}$ for the SUEP. The result obtained for the SUREF, $\eta({\rm{Pt, Pt}}) =[0.0\pm{}1.1{\rm (stat)}\pm{}2.3{\rm (syst)}] \ti | false |

## MICROSCOPE Evidence Lines
| evidence_id | line_number | text_excerpt | role | valid_for_claim |
| --- | --- | --- | --- | --- |
| MIC3260_abstract_result | 102 | The space mission MICROSCOPE dedicated to the test of the Equivalence Principle (EP) operated from April 25, 2016 {until} the deactivation of the satellite on October 16, 2018. {In this analysis we compare the free-fall accelerations ($a_{\rm A}$ and $a_{\rm B}$) of two test masses in terms of the E\"otv\"os parameter $\eta({\rm{A, B}}) = 2 \frac{a_{\rm A}- a_{\rm B}}{a_{\rm A}+ a_{\rm B}}$.} {No EP violation} has been detected for two test masses, {made from platinum and titanium alloys, in a sequence} of 19 segments lasting from 13 to 198 hours {down to} the limit of the statistical error which is smaller than $10^{-14}$ for $ \eta({\rm{Ti, Pt}})$. {Accumulating} data from all segments leads to $\eta({\rm{Ti, Pt}}) =[-1.5\pm{}2.3{\rm (stat)}\pm{}1.5{\rm (syst)}] \times{}10^{-15}$ {showing no EP} violation at the level of $2.7\times{}10^{-15}$ {if we combine stochastic and systematic errors quadratically}. This represents an improvement of almost two orders of magnitude with respect to {the previous best such test performed by the E\"ot-Wash group.} {The reliability of this limit} has been verified by comparing the free falls of two test masses of the same composition (platinum) leading to a null E\"otv\"os parameter with {a statistical uncertainty} of $1.1\times{}10^{-15}$. | central Ti/Pt WEP result with statistical/systematic uncertainties | false |
| MIC3260_reported_level | 102 | The space mission MICROSCOPE dedicated to the test of the Equivalence Principle (EP) operated from April 25, 2016 {until} the deactivation of the satellite on October 16, 2018. {In this analysis we compare the free-fall accelerations ($a_{\rm A}$ and $a_{\rm B}$) of two test masses in terms of the E\"otv\"os parameter $\eta({\rm{A, B}}) = 2 \frac{a_{\rm A}- a_{\rm B}}{a_{\rm A}+ a_{\rm B}}$.} {No EP violation} has been detected for two test masses, {made from platinum and titanium alloys, in a sequence} of 19 segments lasting from 13 to 198 hours {down to} the limit of the statistical error which is smaller than $10^{-14}$ for $ \eta({\rm{Ti, Pt}})$. {Accumulating} data from all segments leads to $\eta({\rm{Ti, Pt}}) =[-1.5\pm{}2.3{\rm (stat)}\pm{}1.5{\rm (syst)}] \times{}10^{-15}$ {showing no EP} violation at the level of $2.7\times{}10^{-15}$ {if we combine stochastic and systematic errors quadratically}. This represents an improvement of almost two orders of magnitude with respect to {the previous best such test performed by the E\"ot-Wash group.} {The reliability of this limit} has been verified by comparing the free falls of two test masses of the same composition (platinum) leading to a null E\"otv\"os parameter with {a statistical uncertainty} of $1.1\times{}10^{-15}$. | reported combined no-violation sensitivity level | false |
| MIC3260_materials | 102 | The space mission MICROSCOPE dedicated to the test of the Equivalence Principle (EP) operated from April 25, 2016 {until} the deactivation of the satellite on October 16, 2018. {In this analysis we compare the free-fall accelerations ($a_{\rm A}$ and $a_{\rm B}$) of two test masses in terms of the E\"otv\"os parameter $\eta({\rm{A, B}}) = 2 \frac{a_{\rm A}- a_{\rm B}}{a_{\rm A}+ a_{\rm B}}$.} {No EP violation} has been detected for two test masses, {made from platinum and titanium alloys, in a sequence} of 19 segments lasting from 13 to 198 hours {down to} the limit of the statistical error which is smaller than $10^{-14}$ for $ \eta({\rm{Ti, Pt}})$. {Accumulating} data from all segments leads to $\eta({\rm{Ti, Pt}}) =[-1.5\pm{}2.3{\rm (stat)}\pm{}1.5{\rm (syst)}] \times{}10^{-15}$ {showing no EP} violation at the level of $2.7\times{}10^{-15}$ {if we combine stochastic and systematic errors quadratically}. This represents an improvement of almost two orders of magnitude with respect to {the previous best such test performed by the E\"ot-Wash group.} {The reliability of this limit} has been verified by comparing the free falls of two test masses of the same composition (platinum) leading to a null E\"otv\"os parameter with {a statistical uncertainty} of $1.1\times{}10^{-15}$. | source confirms Ti/Pt material pair in the reported test | false |
| MIC3260_material_composition_PtRh | 175 | {The PtRh10 platinum-rhodium alloy contains 90\% by mass of Pt (A = 195.1, Z = 78) and 10\% of Rh (A = 102.9, Z = 45). The isotopic composition | source confirms PtRh10 composition context | false |
| MIC3260_material_composition_TA6V | 176 | of Pt has been measured by PTB on a sample of flight material\cite{touboul19}. SUEP’s outer test-mass is made of 90\% titanium (A = 47.9, Z = 22), 6\% of aluminium (A = 27.0, Z = 13) and 4\% of vanadium (A = 50.9, Z = 23).} | source confirms TA6V composition context | false |

## Fixed EM Zero-Theorem Audit
| zero_clause_id | required_clause | source_anchor | current_status | effect | zero_signed | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| ZEM3260_0_parent_EM_owner | observed EM connection and kinetic normalization fixed by parent representation/topological data | PAC1055_1_EM_owner | CANDIDATE_PRESENT | supports Lie_v alpha_EM=0 if combined with no-counterterm/readout/no-vertex clauses | false | false |
| ZEM3260_1_no_F2_counterterm | no independent lambda_A F_Q^2 or f(X)F_Q^2 term | UMF1397_7_current_verdict | FAILS_CURRENT_CORPUS_WHILE_DELTA_S_LAMBDA_ALLOWED | blocks fixed-EM zero theorem until operator domain is closed | false | false |
| ZEM3260_2_readout_descent | Hodge/coframe/hbar*c/readout factors quotient-fixed | REM1400_2_readout | CONDITIONAL_UNSIGNED | prevents alpha drift through unit/readout changes | false | false |
| ZEM3260_3_no_extra_matter_alpha_vertex | no hidden alpha/mass/binding vertex after quotient | AUD3259_3_no_extra_matter_vertex | CONDITIONAL_UNSIGNED | would set Delta r_AB^EM=0 | false | false |
| ZEM3260_4_verdict | all fixed-EM zero clauses signed | ZEM3260_0..3 | ZERO_THEOREM_NOT_CLAIMED | use DD WEP bound branch as fallback | false | false |

## Bound Inputs
| input_id | quantity | value | units | line_anchor | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| BIN3260_0_eta_central | eta_TiPt_central | -1.500000000000e-15 | dimensionless | MIC3260_abstract_result | false |
| BIN3260_1_eta_stat | eta_TiPt_stat_uncertainty | 2.300000000000e-15 | dimensionless | MIC3260_abstract_result | false |
| BIN3260_2_eta_syst | eta_TiPt_syst_uncertainty | 1.500000000000e-15 | dimensionless | MIC3260_abstract_result | false |
| BIN3260_3_eta_quad_level | eta_TiPt_quadrature_uncertainty | 2.745906043549e-15 | dimensionless | computed_from_MIC3260_abstract_result | false |
| BIN3260_4_eta_reported_level | eta_TiPt_reported_no_violation_level | 2.700000000000e-15 | dimensionless | MIC3260_reported_level | false |
| BIN3260_5_delta_Qe_DD | DeltaQe_DD_TA6V_minus_PtRh10 | -1.982376296670e-03 | dimensionless | RV3259_TA6V_minus_PtRh10_unit_product | false |

## Bound Outputs
| bound_id | assumption | formula | value | units | status | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| BOUT3260_0_central_fit_product | DD-only EM residual; Delta eta_res=0; MICROSCOPE sign convention aligned with TA6V_minus_PtRh10 | B_alpha^MTS_fit = eta_central / DeltaQe_DD | 7.566676430301e-13 | dimensionless product beta_source_alpha*b_alpha_EM*tau_WEP | CENTRAL_VALUE_NOT_DETECTION | false |
| BOUT3260_1_stat_product_scale | DD-only EM residual | sigma_stat(B_alpha)=eta_stat/\|DeltaQe_DD\| | 1.160223719313e-12 | dimensionless product | STAT_SCALE_ONLY | false |
| BOUT3260_2_syst_product_scale | DD-only EM residual | sigma_syst(B_alpha)=eta_syst/\|DeltaQe_DD\| | 7.566676430301e-13 | dimensionless product | SYST_SCALE_ONLY | false |
| BOUT3260_3_quadrature_product_bound | DD-only EM residual and no cancellation by other composition channels | \|B_alpha^MTS\| <= sqrt(eta_stat^2+eta_syst^2)/\|DeltaQe_DD\| | 1.385158835970e-12 | dimensionless product | NONCLAIM_BOUND_SCALE | false |
| BOUT3260_4_reported_level_product_bound | DD-only EM residual and no cancellation by other composition channels | \|B_alpha^MTS\| <= 2.7e-15/\|DeltaQe_DD\| | 1.362001757454e-12 | dimensionless product | REPORTED_LEVEL_BOUND_SCALE | false |

## Interpretation Guards
| guard_id | statement | reason | valid_for_claim |
| --- | --- | --- | --- |
| GUARD3260_0_product_only | The MICROSCOPE/DD calculation bounds only B_alpha^MTS=beta_source_alpha*b_alpha_EM*tau_WEP, not each factor separately. | source normalization, alpha pullback, and WEP readout/tau are still not independently signed. | false |
| GUARD3260_1_no_cancellation | The bound is meaningful only for the isolated EM/DD channel or with a no-cancellation theorem across channels. | light-quark/surface/readout channels could cancel numerically unless parent identity forbids it. | false |
| GUARD3260_2_fixed_zero_preferred | The cleaner GR route remains parent fixed-EM zero, not fitting B_alpha small. | GR/Newton reduction wants derived universality; the bound branch is a fallback empirical leash. | false |

## Claim Gates
| gate_id | gate | passed | reason | claim_allowed |
| --- | --- | --- | --- | --- |
| CG3260_0_fixed_zero | fixed-EM owner zero theorem | false | no-counterterm/readout/no-extra-vertex clauses remain unsigned | false |
| CG3260_1_real_WEP_bound_runner | real MICROSCOPE/DD product bound computed | true | Ti/Pt eta source and DD DeltaQe source produce a finite product-bound scale | false |
| CG3260_2_local_GR | local GR/Newton/Maxwell claim | false | bound is product-only and nonclaim; fixed zero theorem remains unsigned | false |

## Decision
| decision_id | verdict | what_moved | meaning | selected_next | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| DEC3260_0 | FIXED_ZERO_NOT_CLOSED_DD_BOUND_RUNNER_WORKS | the EM alpha branch is now either a zero-theorem target or a real Ti/Pt WEP product bound at about 1.36e-12 for B_alpha^MTS | this does not prove MTS local GR, but it turns the alpha coupling from a vague gap into a testable product with a hard scale | separate beta_source_alpha, b_alpha_EM, and tau_WEP or prove fixed-EM owner zero | false |

## Next Target
| next_id | selected | target_doc | target_script | objective | guardrail | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| NEXT3260_0_3261 | primary | 3261-Y5-R2FR-factorize-B_alpha-product-or-sign-fixed-EM-no-counterterm-under-AX1090.md | scripts/Y5_R2FR_3261_factorize_Balpha_product_or_sign_fixed_EM_no_counterterm.py | Either split B_alpha^MTS into parent alpha pullback, source normalization, and WEP tau factors with real inputs, or close the no-counterterm fixed-EM theorem. | Do not treat the 1.36e-12 product scale as a pass unless the local gate has a required threshold and no-cancellation/source factors are signed. | false |

## Validation
| check_id | check | passed | detail |
| --- | --- | --- | --- |
| VAL3260_0_sources_exist | all cited source paths exist | true |  |
| VAL3260_1_sources_parse | all cited source CSV/MD/TEX paths parse | true |  |
| VAL3260_2_MICROSCOPE_lines_found | MICROSCOPE evidence lines are found | true | MIC3260_abstract_result:102;MIC3260_reported_level:102;MIC3260_materials:102;MIC3260_material_composition_PtRh:175;MIC3260_material_composition_TA6V:176 |
| VAL3260_3_outputs_parse | all 3260 output CSVs parse | true |  |
| VAL3260_4_bound_numeric | reported-level product bound is finite positive | true | 1.362001757454e-12 |
| VAL3260_5_claim_gates_false | no 3260 claim gate allows local-GR/WEP/Maxwell promotion | true | all claim_allowed=false |
| VAL3260_6_formalization_untouched | formalization-workbench modified-file count remains zero by this script | true | formalization_changed_count=0 |
| VAL3260_7_overall | 3260 validation overall | true | all required checks passed |

Generated UTC: 2026-06-27T05:49:07.071867+00:00
