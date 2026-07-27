# 3259 - Parent alpha-map owner or DD comparator demotion under AX1090

Private derivation/checkpoint. This does not claim local GR, Newton, Maxwell, WEP, R10, PPN, clock, orbital, material-response, or public source-coupling success.

## Verdict
- `3259` derives the exact parent-alpha pullback law: `d_s ln M_A|EM = Q'_e,A b_alpha^P + r_A^EM`.
- This is a real fork, not a ledger loop: if the parent action fixes EM/readout, `b_alpha^P=0`; if it does not, the DD vector is the finite residual to bound.
- For the Ti/Pt branch, `DeltaQ'_e(TA6V-PtRh10)=-1.982376296670e-3`, so `eta_EM = -1.982376296670e-3 B_alpha^MTS + residual`.
- No claim is promoted because the fixed-EM owner chain is still unsigned and the finite residual product still lacks source/readout/tau input.

## Source Register
| source_id | exists | parse_ok | role | evidence_hits | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| SRC3259_3258_handoff | true | true | 3258 selected parent alpha-map owner or DD demotion | L7:- The coefficient `k_DD,e=7.7e-4` gives numeric `Q'_e` rows for `PtRh10`, `TA6V`, and `TA6V_minus_PtRh10`. \| L8:- This is real progress, but not a loophole: `Q'_e` is an external alpha/dilaton charge, not automatically an MTS-owned `f_EM,A` material fraction. \| L18:\| SRC3258_DD_arxiv \| url \| https://arxiv.org/abs/1007.2792 \| true \| url_not_fetched_by_script \| Damour-Donoghue light-dilaton EM charge source \| Q'_e = +7.7 x 10^-4 Z(Z-1)/A^(4/3);Eq. 25 \| false \| \| L19:\| SRC3258_DD_pdf \| url \| https://arxiv.org/pdf/1007.2792 \| true \| url_not_fetched_by_script \| paper PDF location for Eq. 25 audit \| Q'_e;7.7 x 10^-4 \| false \| | false |
| SRC3259_3258_dd_rows | true | true | numeric DD external EM charge rows | L1:external_row_id,material_id,component_id,q_C_shape,coefficient_id,Qe_prime_DD,formula,source_status,mts_parent_status,valid_for_claim,claim_allowed \| L4:DD3258_TA6V_minus_PtRh10_Qe_prime,TA6V_minus_PtRh10,EM_Coulomb,-2.574514671000e+00,DD3258_Qe_prime_coefficient,-1.982376296670e-03,"Q'_e = 7.7e-4 q_C = 7.7e-4 Z(Z-1)/A^(4/3), alloy averaged via 1909 q_C",SOURCE_BACKED_EXTERNAL_DD_COMPARATOR,PARENT_ALPHA_MAP_UN | false |
| SRC3259_1055_parent_contract | true | true | parent action fixed EM owner candidate | L3:PAC1055_1_EM_owner,observed EM connection and kinetic normalization are owned by fixed representation/topological data,"S_EM = -1/(4 g_*^2(ell_EM)) int sqrt(-g_obs(q)) F_Q^2 + S_int[A_Q,J_Q(theta_A)], with Lie_v ell_EM=0 and no f(Xhat)F_Q^2 slot","Lie_v alpha_ | false |
| SRC3259_1065_charge_norm | true | true | charge/current normalization audit | L6:CIN1065_4_verdict,interaction/charge normalization route to no w_A,CONDITIONAL_NOT_PARENT_SIGNED,it supplies a good classification but not a proof that inert source-only scalars cannot exist,parent current owner or explicit source-scalar exclusion theorem,fals | false |
| SRC3259_1234_em_owner | true | true | EM owner uniqueness attempt | L4:EMU1234_2_unique_F2,unique Maxwell kinetic term,F_Q^2 descends only from the parent curvature norm; no independent lambda_A F_Q^2 or f(I_hid)F_Q^2 term is in the action domain.,FAILS_CURRENT_CORPUS,lambda_A F_Q^2 and hidden scalar gauge-kinetic functions remai \| L8:EMU1234_6_verdict,EM owner uniqueness signs EDGE1232_0,EMU1234_1 through EMU1234_5 all parent-signed would sign the electron-photon edge and remove alpha-current drift from that edge.,EM_OWNER_UNIQUENESS_NOT_CLOSED,unique_F2 fails current corpus and every othe | false |
| SRC3259_1397_unique_F2 | true | true | unique Maxwell F2 theorem audit | L8:UMF1397_6_exact_conditional_theorem,unique Maxwell F2 theorem,"if UMF1397_0 through UMF1397_5 are all parent-signed, then lambda_A=0 and unique F2 holds",g_EM^{-2}=C_P N_Q; partial_phi_c ln g_EM^{-2}=partial_phi_c ln(C_P N_Q),"exact conditional theorem is avai \| L9:UMF1397_7_current_verdict,unique Maxwell F2 proof status,promote Z_unique_F2 only if the lambda_A counterterm is forbidden by parent structure,Z_unique_F2 = false while DeltaS_lambda is allowed,"lambda_A F_Q^2 remains gauge invariant, diffeomorphism invariant, | false |
| SRC3259_1400_em_residual | true | true | finite EM local residual vector and b_alpha product | L5:REM1400_3_b_alpha_EM,b_alpha_EM,canonical finite alphaEM drift,b_alpha_EM=-partial_phi_c ln(C_P N_Q+lambda_A)-rho_readout,"C_P, N_Q, lambda_A, derivative map, readout descent",MISSING_DERIVATIVE_MAP,clock; WEP; R10; EM binding,FINITE_NONCLAIM,False,False \| L8:REM1400_6_WEP,C_WEP_EM,finite EM/Coulomb WEP residual,C_WEP_EM=DeltaQ_alpha_AB beta_source_alpha b_alpha_EM tau_WEP + binding terms,"normalized composition charges, beta_source_alpha, tau_WEP, binding map",MISSING_SOURCE_TAU_BINDING_MAP,WEP gate and local equi | false |
| SRC3259_1910_response_contract | true | true | exact material response tensor contract | L2:MDT1910_0_common_mode,universal_common_mode_mass_energy,DeltaR_AB^U = 0 if V_U M_A = sigma_U M_A for all ordinary A,not needed if theorem signed,parent-signed universal minimal-coupling/common-mode theorem,one matter action/current/source owner; no source-only \| L3:MDT1910_1_electron_rest,electron,DeltaR_AB^e = f_Ae - f_Be if V_e rescales electron rest energy only,3.129116287420e-05,CODATA/NIST electron fraction plus parent owner for electron rest-mass generator,V_e and C_e derived or theorem-zero in parent action,electr \| L4:MDT1910_2_nucleon_or_light_quark_rest,light_quark_or_nucleon_rest,DeltaR_AB^q = sum_isotopes Deltaf_isotope partial ln M_isotope/partial ln m_q in the declared parent basis,Z_over_A=5.677745651272e-02; N_over_A=-5.677745651272e-02,AME/nuclear mass source plus  \| L5:MDT1910_3_EM_Coulomb_binding,EM_Coulomb,DeltaR_AB^alpha = partial_alpha ln M_A - partial_alpha ln M_B with EM binding owned by the parent EM generator,WCM1053_4 DD alpha/Coulomb smoke; AP1909 coulomb_formula_proxy=-2.574514671000e+00,parent EM edge owner plus  | false |
| SRC3259_DD_tex | true | true | downloaded arXiv source for DD alpha chain and Q'_e formula | L81:V=-G\frac{m_A m_B}{r_{AB}}(1+\alpha_A \alpha_B). \| L87:\alpha_A = \frac{1}{\kappa^2 m_A}\frac{\partial [\kappa m_A(\phi)] }{\partial \phi} . \| L90:$\kappa m_A$ is dimensionless. This ensures that this definition of $\alpha_A $ is valid in any choice of units, even if these units \| L93:The above expression for the dimensionless scalar coupling $\alpha_A $ has been written in terms of a canonically normalized | false |

## DD Source Evidence Lines
| evidence_id | line_number | text_excerpt | role | valid_for_claim |
| --- | --- | --- | --- | --- |
| DD3259_alpha_A_definition | 191 | \alpha_A = \frac{\partial \ln[\kappa m_A(\varphi)] }{\partial \varphi} = | body scalar coupling is derivative of log mass along scalar path | false |
| DD3259_alpha_variation | 355 | \alpha(\varphi) &= &(1 + d_e \varphi) \alpha, \nonumber \\ | fine-structure constant varies with d_e in DD parameterization | false |
| DD3259_mass_chain_rule | 425 | \bar{\alpha}_A \equiv \frac{\partial \ln M_A}{ \partial \varphi}= \frac{1}{M_A}\frac{\partial M_A}{\partial \varphi} | composition-dependent part is mass-response derivative | false |
| DD3259_alpha_chain_sum | 433 | = \frac{1}{M_A}\left[ \sum_{a=u,d,e} (d_{m_a}-d_g)\frac{\partial M_A}{\partial \ln k_a}+ d_e \frac{\partial M_A}{ \partial \ln \alpha}\right]. | chain rule isolates alpha derivative | false |
| DD3259_Qe_formula | 1075 | Q'_{e} = + 7.7 \times 10^{-4} \frac{Z(Z-1)}{A^{4/3}} . | DD approximate electromagnetic charge formula | false |
| DD3259_WEP_formula | 1120 | \left( \frac{\Delta a}{a} \right)_{BC} = (\alpha_B- \alpha_C)\alpha_E = \left[D_{\hat m} Q'_{\hat m} + D_e Q'_e \right]_{BC} | DD WEP signal is differential coupling times source coupling | false |

## Parent Alpha Pullback Theorem
| theorem_id | statement | formula | derivation_status | claim_effect | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| PB3259_0_parent_path | Let Phi(s) be an allowed parent path and alpha_EM(Phi) the observed dimensionless EM coupling after quotient/readout. | b_alpha^P := d_s ln alpha_EM(Phi(s)) | DEFINITION_READY | turns vague alpha drift into a single parent pullback coefficient | false |
| PB3259_1_chain_rule | If the only retained material dependence along Phi(s) is the alpha/Coulomb channel, the material response is the DD alpha charge times the parent alpha pullback plus a residual. | d_s ln M_A\|EM = Q'_e,A b_alpha^P + r_A^EM | EXACT_CHAIN_RULE_WITH_RESIDUAL | DD becomes a calibrated residual vector only after parent alpha map is signed | false |
| PB3259_2_pair_difference | For a material pair, common-mode terms cancel and the differential EM residual is controlled by the DD charge difference. | DeltaR_AB^EM = b_alpha^P DeltaQ'_e,AB + Delta r_AB^EM | EXACT_PAIR_PULLBACK_LAW | source coupling is now a scalar product coefficient times a known composition vector | false |
| PB3259_3_fixed_EM_zero | If the parent action signs fixed EM representation/norm, no hidden F_Q^2 slot, and quotient-fixed readout, then alpha_EM is constant on local vertical paths. | Lie_v alpha_EM=0 => b_alpha^P=0 => DeltaR_AB^EM=Delta r_AB^EM; if no extra EM matter vertex, Delta r_AB^EM=0 | CONDITIONAL_ZERO_THEOREM_READY | this is the clean local-GR route: kill EM composition drift by parent ownership, not by fitting | false |
| PB3259_4_controlled_DD_branch | If alpha_EM is not parent-fixed, DD is demoted/promoted only to a finite residual input with source/readout product still required. | eta_AB^EM = DeltaQ'_e,AB B_alpha^MTS + Delta eta_res, B_alpha^MTS:=beta_source_alpha b_alpha_EM tau_WEP | FINITE_BOUND_BRANCH_READY | lets future tests bound the coupling rather than hiding it | false |

## Branch Split
| branch_id | branch_name | premise | result | current_status | why_useful | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| BR3259_FIXED_EM | fixed parent EM representation | PAC1055_1, EMU1234, and UMF1397 clauses are parent-signed: EM norm/readout is fixed and no hidden alpha/F_Q^2 coefficient survives | b_alpha^P=0 and DD EM branch contributes zero to local WEP/PPN/source composition residuals | CONDITIONAL_NOT_PARENT_SIGNED | best route for reducing to GR/Newton: source coupling is eliminated by action ownership | false |
| BR3259_DD_BOUND | controlled alpha residual | parent action permits or fails to exclude alpha_EM pullback | retain eta_AB^EM=DeltaQ'_e,AB B_alpha^MTS and bound B_alpha^MTS with WEP/clock/orbital data | NUMERIC_COMPOSITION_VECTOR_READY_SOURCE_PRODUCT_MISSING | prevents alpha coupling from being a ghost parameter; it becomes one finite tested product | false |

## DD-Calibrated EM Residual Vector
| residual_id | material_id | Qe_prime_DD | parent_pullback_formula | source_observable_formula | status | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| RV3259_PtRh10_EM | PtRh10 | 3.994438870730e-03 | R_A^EM = Q'_e,A b_alpha^P + r_A^EM | eta_AB^EM = DeltaQ'_e,AB B_alpha^MTS + Delta eta_res | NUMERIC_EXTERNAL_VECTOR_PARENT_PRODUCT_MISSING | false |
| RV3259_TA6V_EM | TA6V | 2.012062574060e-03 | R_A^EM = Q'_e,A b_alpha^P + r_A^EM | eta_AB^EM = DeltaQ'_e,AB B_alpha^MTS + Delta eta_res | NUMERIC_EXTERNAL_VECTOR_PARENT_PRODUCT_MISSING | false |
| RV3259_TA6V_minus_PtRh10_EM | TA6V_minus_PtRh10 | -1.982376296670e-03 | R_A^EM = Q'_e,A b_alpha^P + r_A^EM | eta_AB^EM = DeltaQ'_e,AB B_alpha^MTS + Delta eta_res | NUMERIC_EXTERNAL_VECTOR_PARENT_PRODUCT_MISSING | false |
| RV3259_TA6V_minus_PtRh10_unit_product | TA6V_minus_PtRh10 | -1.982376296670e-03 | DeltaR_TA6V-PtRh10^EM = (-1.982376296670e-3) b_alpha^P + Delta r_EM | eta_TA6V-PtRh10^EM = (-1.982376296670e-3) B_alpha^MTS + Delta eta_res | ABS_DELTA_QE=1.982376296670e-03 | false |

## Bound Inversion Formula
| bound_id | observable | formula | numeric_denominator | input_needed | status | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| BOUND3259_0_symbolic_WEP | eta_TA6V_minus_PtRh10 | \|B_alpha^MTS\| <= (eta_bound_abs + \|Delta eta_res\|)/\|DeltaQ'_e\| | 1.982376296670e-03 | real eta_bound_abs for the selected WEP branch plus source/readout/tau convention | BOUND_FORMULA_READY_NO_NUMERIC_CLAIM | false |
| BOUND3259_1_clock_crosscheck | clock/fine-structure residual | C_clock_EM=K_alpha b_alpha_EM tau_clock; compare against same b_alpha_EM used in WEP product | not_applicable | clock sensitivity K_alpha, tau_clock, and same parent alpha pullback b_alpha_EM | CROSSCHECK_FORMULA_READY_INPUTS_MISSING | false |
| BOUND3259_2_fixed_zero | all alpha/Coulomb local residuals | if fixed-EM branch signs b_alpha^P=0 and Delta r_EM=0, no WEP/clock alpha residual remains | zero_theorem_branch | parent-signed fixed EM owner/no-counterterm/readout descent clauses | ZERO_BRANCH_READY_BUT_UNSIGNED | false |

## Parent Alpha Owner Audit
| audit_id | needed_clause | source_anchor | current_status | effect_if_signed | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| AUD3259_0_EM_owner | observed EM connection and kinetic normalization are parent-owned fixed representation/topological data | PAC1055_1_EM_owner | CANDIDATE_CLAUSE_PRESENT_NOT_PARENT_SIGNED | b_alpha^P=0 on local vertical paths unless a separate allowed alpha deformation is declared | false |
| AUD3259_1_no_counterterm | no independent lambda_A F_Q^2 or hidden f(X)F_Q^2 slot | EMU1234_2_unique_F2;UMF1397_7_current_verdict | CURRENT_CORPUS_FAILS_TO_EXCLUDE_COUNTERTERM | removes standalone alpha drift branch | false |
| AUD3259_2_readout_descent | Hodge/coframe/hbar*c/readout factors are quotient-fixed | EMU1234_4_readout_descent;REM1400_2_readout | CONDITIONAL_UNSIGNED | prevents fake alpha drift through unit/readout changes | false |
| AUD3259_3_no_extra_matter_vertex | no hidden alpha/mass/binding vertex after quotient | EMU1234_5_no_alpha_vertex;MDT1910_3_EM_Coulomb_binding | CONDITIONAL_UNSIGNED | sets Delta r_AB^EM=0 after b_alpha^P=0 | false |

## Claim Gates
| gate_id | gate | passed | reason | claim_allowed |
| --- | --- | --- | --- | --- |
| CG3259_0_pullback_theorem | parent alpha pullback law written | true | exact chain-rule form d_s ln M_A=Q'_e,A b_alpha^P+r_A^EM is recorded | false |
| CG3259_1_fixed_zero_claim | fixed-EM zero theorem parent-signed | false | EM owner/no-counterterm/readout/no-vertex clauses remain conditional or failed in current corpus | false |
| CG3259_2_DD_residual_claim | DD comparator promoted to MTS source-coupling evidence | false | numeric DD vector exists but B_alpha^MTS and parent alpha map are not signed | false |
| CG3259_3_local_GR | local GR/Newton/Maxwell reduction from EM branch | false | requires either fixed-EM zero branch or bounded residual branch with source/readout/tau product | false |

## Decision
| decision_id | verdict | what_moved | best_route | fallback_route | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| DEC3259_0 | ALPHA_BRANCH_SPLIT_DERIVED_NOT_CLOSED | DD is no longer a loose external number: it is the finite composition vector in DeltaR_AB^EM=b_alpha^P DeltaQ'_e+Delta r_EM | try fixed-EM parent owner first because it gives b_alpha^P=0 and the cleanest GR/Newton reduction | if fixed-EM cannot be signed, use DD vector to bound B_alpha^MTS against WEP/clock data | false |

## Next Target
| next_id | selected | target_doc | target_script | objective | guardrail | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| NEXT3259_0_3260 | primary | 3260-Y5-R2FR-fixed-EM-owner-zero-theorem-or-DD-WEP-bound-runner-under-AX1090.md | scripts/Y5_R2FR_3260_fixed_EM_owner_zero_theorem_or_DD_WEP_bound_runner.py | Try to sign the fixed-EM owner/no-counterterm/readout/no-vertex chain; if it fails, run the DD residual vector through a WEP bound formula with real eta/tau inputs. | No MTS local-GR claim unless b_alpha^P=0 is parent-signed or the finite residual product is empirically bounded below the local gate. | false |

## Validation
| check_id | check | passed | detail |
| --- | --- | --- | --- |
| VAL3259_0_sources_exist | all cited source paths exist | true |  |
| VAL3259_1_sources_parse | all cited source CSV/MD/TEX paths parse | true |  |
| VAL3259_2_DD_lines_found | DD source evidence lines are found | true | DD3259_alpha_A_definition:191;DD3259_alpha_variation:355;DD3259_mass_chain_rule:425;DD3259_alpha_chain_sum:433;DD3259_Qe_formula:1075;DD3259_WEP_formula:1120 |
| VAL3259_3_outputs_parse | all 3259 output CSVs parse | true |  |
| VAL3259_4_delta_vector_numeric | TA6V_minus_PtRh10 DD EM differential vector is finite numeric | true | -1.982376296670e-03 |
| VAL3259_5_claim_gates_false | no 3259 claim gate allows local-GR/WEP/Maxwell promotion | true | all claim_allowed=false |
| VAL3259_6_formalization_untouched | formalization-workbench modified-file count remains zero by this script | true | formalization_changed_count=0 |
| VAL3259_7_overall | 3259 validation overall | true | all required checks passed |

Generated UTC: 2026-06-27T05:42:25.813507+00:00
