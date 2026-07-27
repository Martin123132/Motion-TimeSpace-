# 3262 - Parent action domain signature or source tau factor intake under AX1090

Private derivation/checkpoint. This does not claim local GR, Newton, Maxwell, WEP, R10, PPN, clock, orbital, material-response, or public source-coupling success.

## Verdict
- `3262` sources a real MICROSCOPE readout subfactor: `tau_readout_X = tilde(a)_c11`, with `0.98 <= tau_readout_X <= 1.02`.
- This does **not** close full `tau_WEP`; it splits it into `tau_readout_X * tau_source_profile * tau_channel_projection`.
- Using the sourced lower bound `tau_readout_X >= 0.98`, the remaining product obeys `|beta_source_alpha*b_alpha_EM*tau_source_profile*tau_channel_projection| <= 1.389797711688e-12`.
- Parent action domain/no-counterterm is still conditional; the fixed-EM zero route remains the cleanest theorem path.

## Source Register
| source_id | exists | parse_ok | role | evidence_hits | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| SRC3262_3261_handoff | true | true | 3261 selected parent action domain or source tau factor intake | L6:- `3261` factorizes the MICROSCOPE/DD coupling bound into `B_alpha^MTS = beta_source_alpha * b_alpha_EM * tau_WEP`. \| L7:- The product bound is real: `\|B_alpha^MTS\| <= 1.362001757454e-12` for the isolated Ti/Pt DD/EM branch. \| L14:\| SRC3261_3260_handoff \| true \| true \| 3260 selected factorization or fixed-EM no-counterterm target \| L8:- With `DeltaQ'_e(TA6V-PtRh10)=-1.982376296670e-3` and the reported MICROSCOPE level `2.7e-15`, the isolated EM branch requires `\\|B_alpha^MTS\\| <= 1.362001757454e-12`. \\| L9 \| L15:\| SRC3261_3260_bound \| true \| true \| real MICROSCOPE/DD product-bound output \| L6:BOUT3260_4_reported_level_product_bound,DD-only EM residual and no cancellation by other composition channels,\\|B_alpha^MTS\\| <= 2.7e-15/\\|DeltaQe_DD\\|,1.362001757454e-12,dimensionless product,REPOR | false |
| SRC3262_3261_factor_inputs | true | true | required factor inputs after product factorization | L3:REQ3261_1_beta_source_map,beta_source_alpha,same-owner current/source theorem or numeric source-force normalization,REM1400_4_beta_source_alpha; PAC990_4_source_charge,MISSING_SOURCE_MAP,false \| L4:REQ3261_2_tau_WEP,tau_WEP,official/equivalent MICROSCOPE readout arrays or parent reduction theorem,ACCEPT1228_4_tau_WEP; WIP1899_6_tau_wep,MISSING_ACCEPTED_TAU,false | false |
| SRC3262_3260_bound | true | true | MICROSCOPE/DD product bound | L6:BOUT3260_4_reported_level_product_bound,DD-only EM residual and no cancellation by other composition channels,\|B_alpha^MTS\| <= 2.7e-15/\|DeltaQe_DD\|,1.362001757454e-12,dimensionless product,REPORTED_LEVEL_BOUND_SCALE,false | false |
| SRC3262_MICROSCOPE_tex | true | true | MICROSCOPE measurement model and readout factor source | L356:&+ \tilde{a}_{c11} b_{1x}^{(d)} + \tilde{a}_{c12} b_{1y}^{(d)}+ \tilde{a}_{c13} b_{1z}^{(d)} \\ \| L357:&+ \tilde{a}_{c11} \delta g_x + \tilde{a}_{c12} \delta g_y + \tilde{a}_{c13} \delta g_z \\ \| L358:& + \left(T_{xx} - {\rm In}_{xx} \right) \tilde{a}_{c11} \Delta_x + \left(T_{xy} - {\rm In}_{xy} \right) \tilde{a}_{c11} \Delta_y + \left(T_{xz} - {\rm In}_{xz} \right) \tilde{a}_{c11} \Delta_z \\ \| L377:\item $\delta_x=\tilde{a}_{c11} \delta \simeq \delta$ is very close to the E\"otv\"os parameter {since $\vert\tilde{a}_{c11}-1\vert <2\times{}10^{-2}$} whereas the potential contribution of the E\"otv\"os parameter to $\delta_z=\tilde{a}_{c13} \delta$ should be much smaller becau | false |
| SRC3262_1228_tau_gate | true | true | official tau gate remains blocked | L6:ACCEPT1228_4_tau_WEP,tau_WEP may be evaluated,BLOCKED,parser precheck and source/material product inputs not passed,False,False | false |
| SRC3262_1899_wep_pack | true | true | source/readout/tau WEP input pack | L7:WIP1899_5_force_map,observed_force_map,P_WEP_force_map_eta_convention.md,"source residual to differential acceleration map in same observed coframe, with eta sign/normalization and common-mode guard",MISSING,MISSING_FORCE_READOUT_MAP,m s^-2 internally; dimensionless eta after nor \| L8:WIP1899_6_tau_wep,projection_product,P_WEP_tau_wep_prior_or_formula.csv,derived or sourced tau_WEP; explicit retained nuisance with prior is allowed; tau_WEP=1 shortcut forbidden,MISSING,TAU_WEP_PROJECTION_NOT_DERIVED,dimensionless projection/contraction factor,not_acquired,P8_Y5 | false |
| SRC3262_1397_unique_F2 | true | true | parent action domain/no-counterterm audit | L4:UMF1397_2_operator_basis_uniqueness,no independent Maxwell quadratic invariant,"the parent operator basis forbids every observed-only F_Q^2 term not inherited from <F,F>_P","Allowed_2der(parent, U(1)_Q) = {<F,F>_P subblock} and not {<F,F>_P, F_Q^2}",RCE765_0 and ELA989_1 keep Del \| L9:UMF1397_7_current_verdict,unique Maxwell F2 proof status,promote Z_unique_F2 only if the lambda_A counterterm is forbidden by parent structure,Z_unique_F2 = false while DeltaS_lambda is allowed,"lambda_A F_Q^2 remains gauge invariant, diffeomorphism invariant, and not excluded by | false |

## MICROSCOPE Readout Evidence
| evidence_id | line_number | text_excerpt | role | valid_for_claim |
| --- | --- | --- | --- | --- |
| MRF3262_0_delta_eta | 346 | \item $ \delta(2,1)=m_{\rm{G_2}}/m_{\rm{I_2}} - m_{\rm{G_1}}/m_{\rm{I_1}}\simeq \eta({\rm{2, 1}})=-\eta({\rm{1, 2}}$) {(note that Eq.~(\ref{eq_gamma}) involves $\delta(2,1)$ instead of $\delta(1,2)$ because the measured differential acceleration is opposite to the difference of gravity accelerations),} | MICROSCOPE identifies the differential mass-ratio parameter with the Eotvos parameter up to sign convention. | false |
| MRF3262_1_x_readout | 377 | \item $\delta_x=\tilde{a}_{c11} \delta \simeq \delta$ is very close to the E\"otv\"os parameter {since $\vert\tilde{a}_{c11}-1\vert <2\times{}10^{-2}$} whereas the potential contribution of the E\"otv\"os parameter to $\delta_z=\tilde{a}_{c13} \delta$ should be much smaller because $\vert \tilde{a}_{c13}\vert <2.6\times{}10^{-3}$ rad from manufacturing; | MICROSCOPE X-axis estimated readout is the calibrated factor multiplying the Eotvos parameter. | false |
| MRF3262_2_readout_tolerance | 377 | \item $\delta_x=\tilde{a}_{c11} \delta \simeq \delta$ is very close to the E\"otv\"os parameter {since $\vert\tilde{a}_{c11}-1\vert <2\times{}10^{-2}$} whereas the potential contribution of the E\"otv\"os parameter to $\delta_z=\tilde{a}_{c13} \delta$ should be much smaller because $\vert \tilde{a}_{c13}\vert <2.6\times{}10^{-3}$ rad from manufacturing; | readout calibration factor is within two percent of unity. | false |
| MRF3262_3_corrected_model | 371 | \Gamma^{(d)}_{x, {\rm corr}}=\tilde{b}_x^{'(d)}+\delta_x g_x+\delta_z g_z+\Delta'_{x} S_{xx} +\Delta'_{z} S_{xz}+ n_x^{(d)}, | corrected differential acceleration model carries delta_x as the EP coefficient. | false |

## Tau WEP Factorization
| tau_id | factor | formula | source_status | numeric_status | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| TAU3262_0_decomposition | tau_WEP | tau_WEP = tau_readout_X * tau_source_profile * tau_channel_projection | DECOMPOSITION_DEFINED | tau_readout_X bounded; source_profile/channel_projection missing | false |
| TAU3262_1_readout_X | tau_readout_X | tau_readout_X = tilde(a)_c11 | MICROSCOPE_SOURCE_BACKED | 9.800000000000e-01 <= tau_readout_X <= 1.020000000000e+00 | false |
| TAU3262_2_source_profile | tau_source_profile | projection of MTS source residual onto Earth/orbit/source-worldtube profile | WIP1899_1/2/5 remain missing | MISSING | false |
| TAU3262_3_channel_projection | tau_channel_projection | projection of selected EM/DD residual onto the MICROSCOPE fitted EP channel after nuisance/correction model | official arrays or exact parent reduction still required | MISSING | false |

## Readout-Reduced Product Bound
| bound_id | quantity | formula | value | status | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| RB3262_0_full_product | \|beta_source_alpha*b_alpha_EM*tau_WEP\| | from 3260 MICROSCOPE/DD runner | 1.362001757454e-12 | REAL_PRODUCT_BOUND | false |
| RB3262_1_readout_factor | tau_readout_X | 0.98 <= tau_readout_X <= 1.02 | [9.800000000000e-01,1.020000000000e+00] | SOURCE_BACKED_READOUT_SUBFACTOR | false |
| RB3262_2_remaining_product_worst | \|beta_source_alpha*b_alpha_EM*tau_source_profile*tau_channel_projection\| | B_bound/min(\|tau_readout_X\|) | 1.389797711688e-12 | READOUT_REDUCED_PRODUCT_BOUND | false |
| RB3262_3_remaining_product_center | center readout normalization | B_bound/1 | 1.362001757454e-12 | DEBUG_CENTER_NOT_CLAIM | false |

## Parent Action Domain Signature Audit
| domain_id | signature_target | exact_condition | current_status | if_signed | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| ADS3262_0_parent_only_domain | forbid quotient-only Maxwell counterterm | S_parent is varied upstairs and Allowed_2der(parent,U(1)_Q) contains only parent curvature-norm subblocks | CONDITIONAL_FROM_1397_NOT_SIGNED | lambda_A=0, advancing fixed-EM zero route | false |
| ADS3262_1_readout_boundary_silence | readout/coframe/Hodge cannot generate F_Q^2 coefficient drift | quotient-fixed readout and boundary projection add no independent Maxwell kinetic density | CONDITIONAL_UNSIGNED | rho_readout=0 for alpha branch | false |
| ADS3262_2_current_verdict | fixed EM no-counterterm chain | ADS3262_0 and ADS3262_1 plus fixed N_Q/C_P | NOT_CLOSED_USE_TAU_INTAKE_PROGRESS | b_alpha_EM=0; DD bound branch becomes unnecessary for EM local residual | false |

## Remaining Source/Tau Inputs
| input_id | missing_piece | needed_source | current_anchor | status | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| RIN3262_0_source_profile | tau_source_profile | Earth/source stress, mass-density, or parent theorem reducing source to calibrated point-source profile | WIP1899_1_source_worldtube_profile;WIP1899_2_source_composition | MISSING | false |
| RIN3262_1_channel_projection | tau_channel_projection | official MICROSCOPE arrays or exact equivalent showing fitted EP channel projection | WIP1899_4_readout_arrays;ACCEPT1228_4_tau_WEP | PARTIAL_READOUT_FACTOR_ONLY | false |
| RIN3262_2_beta_source | beta_source_alpha | same-owner current/source theorem or numeric force normalization | PAC990_4_source_charge;REM1400_4_beta_source_alpha | MISSING | false |

## Claim Gates
| gate_id | gate | passed | reason | claim_allowed |
| --- | --- | --- | --- | --- |
| CG3262_0_readout_subfactor | MICROSCOPE readout subfactor sourced | true | tilde(a)_c11 is sourced within 2 percent of unity | false |
| CG3262_1_full_tau | full tau_WEP sourced | false | source_profile and channel_projection factors remain missing | false |
| CG3262_2_parent_action_domain | parent action domain forbids quotient-only F_Q^2 counterterm | false | operator-domain signature remains conditional | false |
| CG3262_3_local_GR | local GR/Newton/Maxwell promotion | false | one readout subfactor does not close source coupling or fixed EM theorem | false |

## Decision
| decision_id | verdict | what_moved | new_bound | best_next | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| DEC3262_0 | READOUT_SUBFACTOR_SOURCED_FULL_TAU_NOT_CLOSED | tau_WEP is no longer a single black box: tau_readout_X is sourced as 0.98..1.02 from MICROSCOPE | remaining product \|beta_source_alpha*b_alpha_EM*tau_source_profile*tau_channel_projection\| <= 1.389797711688e-12 | fill source_profile/channel_projection or sign parent action no-counterterm domain | false |

## Next Target
| next_id | selected | target_doc | target_script | objective | guardrail | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| NEXT3262_0_3263 | primary | 3263-Y5-R2FR-source-profile-channel-projection-or-parent-domain-lock-under-AX1090.md | scripts/Y5_R2FR_3263_source_profile_channel_projection_or_parent_domain_lock.py | Either source the MICROSCOPE source_profile/channel_projection tau factors, or lock the parent-only action domain that removes lambda_A. | Do not promote the 0.98..1.02 readout subfactor to full tau_WEP. | false |

## Validation
| check_id | check | passed | detail |
| --- | --- | --- | --- |
| VAL3262_0_sources_exist | all cited source paths exist | true |  |
| VAL3262_1_sources_parse | all cited source CSV/MD/TEX paths parse | true |  |
| VAL3262_2_readout_lines_found | MICROSCOPE readout evidence lines are found | true | MRF3262_0_delta_eta:346;MRF3262_1_x_readout:377;MRF3262_2_readout_tolerance:377;MRF3262_3_corrected_model:371 |
| VAL3262_3_outputs_parse | all 3262 output CSVs parse | true |  |
| VAL3262_4_reduced_bound_numeric | readout-reduced remaining product bound matches B/0.98 | true | 1.389797711688e-12 |
| VAL3262_5_claim_gates_false | no 3262 claim gate allows local-GR/WEP/Maxwell promotion | true | all claim_allowed=false |
| VAL3262_6_formalization_untouched | formalization-workbench modified-file count remains zero by this script | true | formalization_changed_count=0 |
| VAL3262_7_overall | 3262 validation overall | true | all required checks passed |

Generated UTC: 2026-06-27T05:57:45.158316+00:00
