# 3261 - Factorize B_alpha product or sign fixed EM no-counterterm under AX1090

Private derivation/checkpoint. This does not claim local GR, Newton, Maxwell, WEP, R10, PPN, clock, orbital, material-response, or public source-coupling success.

## Verdict
- `3261` factorizes the MICROSCOPE/DD coupling bound into `B_alpha^MTS = beta_source_alpha * b_alpha_EM * tau_WEP`.
- The product bound is real: `|B_alpha^MTS| <= 1.362001757454e-12` for the isolated Ti/Pt DD/EM branch.
- The clean derivation route is still fixed EM: sign the parent action domain/no-counterterm/readout chain and get `b_alpha_EM=0`.
- If fixed EM does not close, the fallback is no longer vague: source two factors and the third is bounded by exact inversion.

## Source Register
| source_id | exists | parse_ok | role | evidence_hits | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| SRC3261_3260_handoff | true | true | 3260 selected factorization or fixed-EM no-counterterm target | L8:- With `DeltaQ'_e(TA6V-PtRh10)=-1.982376296670e-3` and the reported MICROSCOPE level `2.7e-15`, the isolated EM branch requires `\|B_alpha^MTS\| <= 1.362001757454e-12`. \| L9:- This is not a pass/fail claim yet; it is a hard scale for the combined product `B_alpha^MTS=beta_source_alpha*b_alpha_EM*tau_WEP`. \| L14:\| SRC3260_3259_handoff \| true \| true \| 3259 selected fixed-EM zero theorem or DD WEP bound runner \| L8:- For the Ti/Pt branch, `DeltaQ'_e(TA6V-PtRh10)=-1.982376296670e-3`, so `eta_EM = -1.982376296670e-3 B_alpha^MTS + residual`. \\| L39:\\| PB3259_2_pair_difference \\| For a materia \| L15:\| SRC3260_3259_residual_vector \| true \| true \| DD-calibrated Ti/Pt EM residual vector \| L4:RV3259_TA6V_minus_PtRh10_EM,TA6V_minus_PtRh10,-1.982376296670e-03,"R_A^EM = Q'_e,A b_alpha^P + r_A^EM","eta_AB^EM = DeltaQ'_e,AB B_alpha^MTS + Delta eta_res",NUMERIC_EXTERNAL_VECTOR_PARENT_ | false |
| SRC3261_3260_bound | true | true | real MICROSCOPE/DD product-bound output | L6:BOUT3260_4_reported_level_product_bound,DD-only EM residual and no cancellation by other composition channels,\|B_alpha^MTS\| <= 2.7e-15/\|DeltaQe_DD\|,1.362001757454e-12,dimensionless product,REPORTED_LEVEL_BOUND_SCALE,false | false |
| SRC3261_3260_guards | true | true | product-only and no-cancellation guards | L2:GUARD3260_0_product_only,"The MICROSCOPE/DD calculation bounds only B_alpha^MTS=beta_source_alpha*b_alpha_EM*tau_WEP, not each factor separately.","source normalization, alpha pullback, and WEP readout/tau are still not independently signed.",false \| L3:GUARD3260_1_no_cancellation,The bound is meaningful only for the isolated EM/DD channel or with a no-cancellation theorem across channels.,light-quark/surface/readout channels could cancel numerically unless parent identity forbids it.,false | false |
| SRC3261_1400_residual_vector | true | true | named EM residual factors | L5:REM1400_3_b_alpha_EM,b_alpha_EM,canonical finite alphaEM drift,b_alpha_EM=-partial_phi_c ln(C_P N_Q+lambda_A)-rho_readout,"C_P, N_Q, lambda_A, derivative map, readout descent",MISSING_DERIVATIVE_MAP,clock; WEP; R10; EM binding,FINITE_NONCLAIM,False,False \| L6:REM1400_4_beta_source_alpha,beta_source_alpha,source/force normalization multiplying finite alpha WEP branch,eta_AB_alpha=DeltaQ_alpha_AB beta_source_alpha b_alpha_EM tau_WEP,same-owner current/source theorem or numeric source map,TARGET_ONLY_alpha<=4.797780522732e-05_robust<=2.8 \| L8:REM1400_6_WEP,C_WEP_EM,finite EM/Coulomb WEP residual,C_WEP_EM=DeltaQ_alpha_AB beta_source_alpha b_alpha_EM tau_WEP + binding terms,"normalized composition charges, beta_source_alpha, tau_WEP, binding map",MISSING_SOURCE_TAU_BINDING_MAP,WEP gate and local equivalence-principle re | false |
| SRC3261_1228_tau_gate | true | true | tau_WEP acceptance gate remains blocked | L6:ACCEPT1228_4_tau_WEP,tau_WEP may be evaluated,BLOCKED,parser precheck and source/material product inputs not passed,False,False | false |
| SRC3261_1899_wep_pack | true | true | source/readout/tau input pack requirements | L7:WIP1899_5_force_map,observed_force_map,P_WEP_force_map_eta_convention.md,"source residual to differential acceleration map in same observed coframe, with eta sign/normalization and common-mode guard",MISSING,MISSING_FORCE_READOUT_MAP,m s^-2 internally; dimensionless eta after nor \| L8:WIP1899_6_tau_wep,projection_product,P_WEP_tau_wep_prior_or_formula.csv,derived or sourced tau_WEP; explicit retained nuisance with prior is allowed; tau_WEP=1 shortcut forbidden,MISSING,TAU_WEP_PROJECTION_NOT_DERIVED,dimensionless projection/contraction factor,not_acquired,P8_Y5 | false |
| SRC3261_990_parent_action | true | true | parent action EM lock and source charge contract | L5:PAC990_3_EM_lock,"EM charge generator, Maxwell kinetic term, current normalization, and readout descend from one parent owner",T_Q fixed; F_Q^2 unique; S_int=sum_A n_A int A_Q J_A; Lie_v ln alpha_EM=0,b_theta_alpha_EM=0 and alpha/Coulomb WEP-clock channel closes structurally,not_ \| L6:PAC990_4_source_charge,observed source mass is an integrable fixed-reference Hamiltonian charge,"delta H_tau = int_S(delta Q_tau - i_tau theta), with delta^2H_tau=0, fixed B_ref, tau lock, and source equality","Newtonian GM/source normalization before orbital, PPN, R10, or Gdot s | false |
| SRC3261_1397_unique_F2 | true | true | unique Maxwell/no-counterterm audit | L8:UMF1397_6_exact_conditional_theorem,unique Maxwell F2 theorem,"if UMF1397_0 through UMF1397_5 are all parent-signed, then lambda_A=0 and unique F2 holds",g_EM^{-2}=C_P N_Q; partial_phi_c ln g_EM^{-2}=partial_phi_c ln(C_P N_Q),"exact conditional theorem is available, but UMF1397_2 \| L9:UMF1397_7_current_verdict,unique Maxwell F2 proof status,promote Z_unique_F2 only if the lambda_A counterterm is forbidden by parent structure,Z_unique_F2 = false while DeltaS_lambda is allowed,"lambda_A F_Q^2 remains gauge invariant, diffeomorphism invariant, and not excluded by | false |

## B Alpha Factorization Law
| factor_id | quantity | definition | bound_or_formula | status | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| FAC3261_0_product | B_alpha^MTS | B_alpha^MTS := beta_source_alpha * b_alpha_EM * tau_WEP | \|B_alpha^MTS\| <= 1.362001757454e-12 from MICROSCOPE/DD isolated EM branch | PRODUCT_BOUND_REAL_FACTORS_UNSEPARATED | false |
| FAC3261_1_b_alpha_EM | b_alpha_EM | canonical parent alpha pullback/drift | b_alpha_EM = -partial_phi ln(C_P N_Q + lambda_A) - rho_readout | MISSING_DERIVATIVE_MAP_OR_FIXED_EM_ZERO | false |
| FAC3261_2_beta_source_alpha | beta_source_alpha | same-owner source/force normalization multiplying finite alpha WEP branch | eta_AB_alpha = DeltaQ_alpha_AB beta_source_alpha b_alpha_EM tau_WEP | MISSING_SAME_OWNER_SOURCE_THEOREM_OR_NUMERIC_MAP | false |
| FAC3261_3_tau_WEP | tau_WEP | projection/readout/orbit kernel that maps source residual to measured MICROSCOPE differential acceleration | tau_WEP must come from official/source-equivalent readout arrays or parent reduction theorem; tau_WEP=1 shortcut forbidden | MISSING_ACCEPTED_TAU_INPUT | false |
| FAC3261_4_inversion | single-factor bound | if any two factors are supplied, the third is bounded | \|b_alpha_EM\| <= B_bound/(\|beta_source_alpha tau_WEP\|), and cyclic permutations | EXACT_FACTOR_INVERSION_LAW_READY | false |

## Factor Sensitivity Runner
| scenario_id | beta_source_alpha_assumed | tau_WEP_assumed | beta_tau_product | implied_abs_b_alpha_EM_bound | note | accepted_as_evidence | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| SC3261_unity_debug | 1.000000000000e+00 | 1.000000000000e+00 | 1.000000000000e+00 | 1.362001757454e-12 | debug only; unity shortcut is forbidden for claims | false | false |
| SC3261_tau_tenth | 1.000000000000e+00 | 1.000000000000e-01 | 1.000000000000e-01 | 1.362001757454e-11 | tau attenuation example | false | false |
| SC3261_source_tenth | 1.000000000000e-01 | 1.000000000000e+00 | 1.000000000000e-01 | 1.362001757454e-11 | source-normalization attenuation example | false | false |
| SC3261_both_tenth | 1.000000000000e-01 | 1.000000000000e-01 | 1.000000000000e-02 | 1.362001757454e-10 | both source and tau attenuated | false | false |
| SC3261_both_hundredth | 1.000000000000e-02 | 1.000000000000e-02 | 1.000000000000e-04 | 1.362001757454e-08 | strong attenuation example | false | false |

## Zero Factor Route Audit
| route_id | zero_factor | required_derivation | what_it_kills | current_status | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| ZERO3261_0_fixed_EM | b_alpha_EM=0 | lambda_A=0, Lie_v(C_P N_Q)=0, and rho_readout=0 from fixed EM owner/readout descent | WEP alpha branch, clock alpha branch, and local EM composition branch together | BEST_ROUTE_BUT_NO_COUNTERTERM_UNSIGNED | false |
| ZERO3261_1_source_decoupling | beta_source_alpha=0 | same-owner source theorem says alpha material response does not enter gravitational source/force normalization | WEP alpha/source branch only; clock alpha drift may remain | NOT_DERIVED | false |
| ZERO3261_2_projection_silence | tau_WEP=0 | official readout/source projection orthogonal to the EM composition residual | MICROSCOPE WEP readout only; not local GR or clocks | NOT_DERIVED_AND_UNLIKELY_AS_GENERAL_ROUTE | false |
| ZERO3261_3_product_bound | none | retain product as finite residual and require \|B_alpha^MTS\|<=1.362001757454e-12 | nothing by theorem; constrains residual branch empirically | REAL_BOUND_AVAILABLE_NONCLAIM | false |

## Fixed EM No-Counterterm Lemma
| lemma_id | premise | formula | result | status | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| NCT3261_0_domain_definition | The parent action domain contains parent-local gauge curvature invariants only; no post-quotient observed-only counterterm may be added. | Allowed_2der(parent,U(1)_Q)={mu_P C_P<Phi><F_P,F_P>_P subblock}; not {q^*(mu_obs F_Q^2) with independent lambda_A} | observed lambda_A has no independent slot | EXACT_IF_PARENT_DOMAIN_SIGNED | false |
| NCT3261_1_projection | A_Q is the T_Q subblock of the parent connection and the T_Q norm N_Q is fixed. | g_EM^{-2}=C_P N_Q after quotient/readout, up to quotient-fixed unit factors | alpha drift can only come from parent C_P/N_Q/readout, not a separate species/source coefficient | CONDITIONAL_ON_FIXED_PARENT_NORM | false |
| NCT3261_2_readout | coframe/Hodge/hbar*c/readout descent is quotient-fixed along local vertical paths | rho_readout=0 | unit/readout drift cannot fake alpha variation | CONDITIONAL_UNSIGNED | false |
| NCT3261_3_zero | NCT3261_0 through NCT3261_2 plus Lie_v(C_P N_Q)=0 | b_alpha_EM=-Lie_v ln(C_P N_Q)-rho_readout=0 | fixed-EM branch gives B_alpha^MTS=0 regardless of beta_source_alpha and tau_WEP | DERIVED_CONDITIONAL_ZERO_NOT_PARENT_SIGNED | false |
| NCT3261_4_current_corpus_verdict | UMF1397_7 still says Z_unique_F2=false while DeltaS_lambda is allowed | lambda_A retained unless parent action domain is explicitly signed | no-counterterm theorem is not claimed; DD bound branch remains active | CLAIM_BLOCKED_BY_CURRENT_CORPUS | false |

## Required Factor Inputs
| input_id | factor | needed_input | current_source | status | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| REQ3261_0_b_alpha_derivative_map | b_alpha_EM | C_P, N_Q, lambda_A, derivative map, and rho_readout or fixed-EM zero theorem | REM1400_3_b_alpha_EM | MISSING_DERIVATIVE_MAP | false |
| REQ3261_1_beta_source_map | beta_source_alpha | same-owner current/source theorem or numeric source-force normalization | REM1400_4_beta_source_alpha; PAC990_4_source_charge | MISSING_SOURCE_MAP | false |
| REQ3261_2_tau_WEP | tau_WEP | official/equivalent MICROSCOPE readout arrays or parent reduction theorem | ACCEPT1228_4_tau_WEP; WIP1899_6_tau_wep | MISSING_ACCEPTED_TAU | false |
| REQ3261_3_no_cancellation | channel isolation | no-cancellation theorem or full multi-channel vector fit | GUARD3260_1_no_cancellation | MISSING_MULTI_CHANNEL_CONTROL | false |

## Claim Gates
| gate_id | gate | passed | reason | claim_allowed |
| --- | --- | --- | --- | --- |
| CG3261_0_factorization | B_alpha product factorization law | true | product bound is now split into b_alpha_EM, beta_source_alpha, and tau_WEP with exact inversion laws | false |
| CG3261_1_fixed_EM_zero | fixed-EM no-counterterm theorem signed | false | operator-domain/no-counterterm/readout clauses remain conditional in the current corpus | false |
| CG3261_2_real_factor_values | real separate values for beta_source_alpha, b_alpha_EM, and tau_WEP | false | only their product has a MICROSCOPE/DD bound | false |
| CG3261_3_local_GR | local GR/Newton/Maxwell promotion | false | requires fixed-EM zero theorem or all factor/product residuals below explicit local gates | false |

## Decision
| decision_id | verdict | what_moved | best_next | fallback_next | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| DEC3261_0 | PRODUCT_FACTORIZED_NO_COUNTERTERM_LEMMA_CONDITIONAL | the coupling gap is now three named factors with exact inversion laws and a hard MICROSCOPE/DD product scale | attack no-counterterm parent action domain because it zeroes b_alpha_EM globally if signed | source tau_WEP/readout and beta_source_alpha to turn the product bound into separate factor bounds | false |

## Next Target
| next_id | selected | target_doc | target_script | objective | guardrail | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| NEXT3261_0_3262 | primary | 3262-Y5-R2FR-parent-action-domain-signature-or-source-tau-factor-intake-under-AX1090.md | scripts/Y5_R2FR_3262_parent_action_domain_signature_or_source_tau_factor_intake.py | Either sign the parent action domain forbidding quotient-only Maxwell counterterms, or acquire real tau_WEP/source-normalization factor inputs for the B_alpha product. | Do not use unity tau/source shortcuts as claim evidence; they are debug scenarios only. | false |

## Validation
| check_id | check | passed | detail |
| --- | --- | --- | --- |
| VAL3261_0_sources_exist | all cited source paths exist | true |  |
| VAL3261_1_sources_parse | all cited source CSV/MD paths parse | true |  |
| VAL3261_2_outputs_parse | all 3261 output CSVs parse | true |  |
| VAL3261_3_product_bound_numeric | product bound is finite positive | true | B_bound=1.362001757454e-12 |
| VAL3261_4_unity_scenario_matches_bound | unity debug scenario returns the product bound as b_alpha bound | true | 1.362001757454e-12 |
| VAL3261_5_claim_gates_false | no 3261 claim gate allows local-GR/WEP/Maxwell promotion | true | all claim_allowed=false |
| VAL3261_6_formalization_untouched | formalization-workbench modified-file count remains zero by this script | true | formalization_changed_count=0 |
| VAL3261_7_overall | 3261 validation overall | true | all required checks passed |

Generated UTC: 2026-06-27T05:53:40.498842+00:00
