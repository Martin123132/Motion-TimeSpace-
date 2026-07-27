# 2513 — Source-Weight PPN Response Kernel with Fixed-GM Map

**Current verdict:** the local-GR bridge now has a stricter PPN interface. A single universal common source normalization may be calibrated into measured `GM`, but relative, source-dependent, range-dependent, time-dependent, frame-dependent, boundary, and readout pieces remain physical residuals.

**No claim:** this is not a PPN pass. It is a response-kernel contract. Gamma, beta, preferred-frame terms, alpha3/source exchange, xi/boundary, and readout/GM tails all remain nonclaim until their kernels and coefficients are sourced or parent-zero.

**Next pressure point:** beta is the leading GR gate because it needs the second-order `U^2` source-normalized field equation; gamma/WEP cannot give beta for free.

## Source Register
| source_id | source_path | path_exists | found_needles | source_pass | role |
| --- | --- | --- | --- | --- | --- |
| SRC2513_0_2512_next | 2512-Y5-R2FR-tau-WEP-lower-bound-or-parent-nondegeneracy-proof.md | True | NEXT2512_0_selected;PPN source-weight response kernel | True | authoritative theory-route pivot from tau gate to PPN/fixed-GM kernel |
| SRC2513_1_2489_ppn_vector | source-intake/local_bounds/PPN_residual_vector_interface_2489_NONCLAIM.csv | True | PPNV2489_4_wR;PPNV2489_7_total_abs | True | PPN residual vector slots including source prefactor and no-cancellation total |
| SRC2513_2_2489_ppn_bounds | source-intake/local_bounds/PPN_bound_ledger_2489_NONCLAIM.csv | True | PBOUND2489_0_gamma;PBOUND2489_4_alpha3 | True | source-backed PPN comparator bounds |
| SRC2513_3_2500_full_ppn | source-intake/local_bounds/Full_PPN_vector_requirements_2500_NONCLAIM.csv | True | VREQ2500_4_wR_source;VREQ2500_6_total_no_cancellation | True | full PPN vector requirements and absolute envelope |
| SRC2513_4_2500_beta_gate | source-intake/local_bounds/Beta_second_order_gate_2500_NONCLAIM.csv | True | BETA2500_2_source_coupling;BETA2500_4_verdict | True | second-order beta/source-coupling blocker |
| SRC2513_5_2322_tau_ppn | source-intake/beta-source/docs/TAU_PPN_COMMON_FRAME_DERIVATION_AUDIT_2322_NONCLAIM.csv | True | TPA2322_3_readout_gauge_tail;TPA2322_4_verdict | True | tau_PPN/readout gauge tail refusal |
| SRC2513_6_2128_local_gr | source-intake/source-weight/docs/AFRAME_LOCAL_GR_GATE_MAP_2128_NONCLAIM.csv | True | LGR2128_2_Newton_GM_source_normalization;LGR2128_8_total_verdict | True | local GR/Newton gate map and measured-GM source-normalization blocker |
| SRC2513_7_2097_current_owner | source-intake/source-weight/docs/AFRAME_CURRENT_OWNER_NONHILBERT_2097_NONCLAIM.csv | True | CUR2097_7_verdict;CM2097_0_relative_source_weight | True | current-owner and relative source-weight countermodel |
| SRC2513_8_2127_ep_closure | source-intake/source-weight/docs/AFRAME_EP_CLOSURE_2127_NONCLAIM.csv | True | IAS2127_5_verdict;EPC2127_1_common_quotient | True | private source-side EP closure and measured-G common quotient guard |
| SRC2513_9_2510_bound_pack | source-intake/local_bounds/Source_weight_residual_bound_pack_2510_NONCLAIM.csv | True | ARENA2510_2_PPN;without absorbing relative weights into fitted GM | True | source-weight PPN arena row selected by the 2510 bound pack |
| SRC2513_10_2319_source_import | source-intake/beta-source/docs/PPN_VECTOR_SOURCE_IMPORT_2319_NONCLAIM.csv | True | PPN2319_0_gamma_source;NONCLAIM_VECTOR_TARGET | True | older source-backed comparator import, not a MTS component prediction |

## Fixed-GM Transfer Gate
| gate_id | object | rule | mathematical_form | current_status | blocks |
| --- | --- | --- | --- | --- | --- |
| GM2513_0_common_mode | epsilon_common | a constant, universal, range/time/species/frame independent source normalization may be absorbed into measured GM only after universality is proved | U_obs := G_obs M_obs/r fixes one common multiplicative scale | EXACT_CONDITIONAL_CALIBRATION_RULE | cannot absorb relative or environment-dependent source weights |
| GM2513_1_relative_weight | Delta_w_A | relative species/source weights survive fixed-GM calibration | epsilon_A - epsilon_ref remains in observables after one GM quotient | LIVE_RESIDUAL | WEP-clean or one-body calibrated source shifts cannot be treated as GR |
| GM2513_2_range_time | epsilon(lambda,t,frame) | range/time/frame/source-profile dependence cannot be hidden in a constant GM fit | delta U(r,t)/U != constant over the comparison domain | LIVE_RESIDUAL | R10/orbital/PPN consistency if the same vector changes with scale |
| GM2513_3_readout | alpha_readout_or_delta_GM | PPN gauge/readout map must be fixed before comparing gamma/beta | Delta_PPN_obs = Delta_PPN_field + T_readout[Delta_w_eff] | MISSING_READOUT_GAUGE_SOURCE_NORMALIZATION | fake beta/gamma closure by post-fit calibration |
| GM2513_4_verdict | fixed measured-GM convention | GM can remove only one proven common scalar; all other source-weight pieces require PPN response kernels | Delta_PPN_abs uses componentwise post-GM residuals | FIXED_GM_RULE_WRITTEN_KERNELS_MISSING | local-GR claim |

## PPN Source-Weight Kernel Matrix
| kernel_id | observable | residual_law | required_kernel | comparator_bound | current_status |
| --- | --- | --- | --- | --- | --- |
| PPNK2513_0_gamma_source_weight | gamma_minus_1 | delta_gamma_source = C_gamma_w * Delta_w_eff + C_gamma_metric * delta_p + C_gamma_readout * alpha_readout | C_gamma_w;C_gamma_metric;C_gamma_readout in fixed GM convention | 2.3e-05 | MISSING_GAMMA_SOURCE_RESPONSE_KERNEL |
| PPNK2513_1_beta_source_weight | beta_minus_1 | delta_beta_total = C_beta_w * Delta_w_eff + C_beta_NH * J_NH + C_beta_readout * alpha_readout + second_order_operator_tail | second-order source-normalized field equation and readout/GM map | 7.8e-05 | MISSING_BETA_SECOND_ORDER_SOURCE_KERNEL |
| PPNK2513_2_alpha1_source_frame | alpha1 | alpha1_source = C_alpha1_frame * d_R + C_alpha1_w * Delta_w_eff + C_alpha1_endpoint * epsilon_endpoint | preferred-frame/disformal response matrix | 1e-04 | MISSING_PREFERRED_FRAME_KERNEL |
| PPNK2513_3_alpha2_source_frame | alpha2 | alpha2_source = C_alpha2_frame * d_R + C_alpha2_boundary * Q_edge + C_alpha2_projector * Delta_mu_projector | preferred-frame/domain/projector response matrix | 2e-09 | MISSING_VECTOR_DOMAIN_KERNEL |
| PPNK2513_4_alpha3_source_exchange | alpha3 | alpha3_source = C_alpha3_exchange * Delta_w_eff + C_alpha3_NH * J_NH + C_alpha3_boundary * Q_edge | source-current conservation/exchange response and no-Hilbert-current theorem or bound | 4e-20 | MISSING_SOURCE_EXCHANGE_KERNEL_ULTRATIGHT |
| PPNK2513_5_xi_boundary | xi | xi_source = C_xi_boundary * Q_edge + C_xi_domain * Delta_worldtube + C_xi_projective * trace_projective | boundary/domain/preferred-location response | 4e-09 | MISSING_BOUNDARY_DOMAIN_KERNEL |
| PPNK2513_6_total_abs | Delta_PPN_abs | sum_i abs(PPNK_i component_i) <= bound_i componentwise; no cancellation unless parent identity signs it | all component kernels and component values/theorem-zeros | componentwise PPN ledger | SCHEMA_READY_VALUES_MISSING |

## PPN Bound Interface
| bound_id | observable | upper_bound | source_dataset | comparator_status | required_for_scoring |
| --- | --- | --- | --- | --- | --- |
| PBOUND2513_0_gamma | gamma_minus_1 | 2.3e-05 | Cassini_Shapiro_gamma_2003 | SOURCE_BACKED_COMPARATOR_NOT_MTS_PREDICTION | matching PPNK row numeric prediction in same fixed-GM convention |
| PBOUND2513_1_beta | beta_minus_1 | 7.8e-05 | Will_2014_PPN_beta_table | SOURCE_BACKED_COMPARATOR_NOT_MTS_PREDICTION | matching PPNK row numeric prediction in same fixed-GM convention |
| PBOUND2513_2_alpha1 | alpha1 | 1e-04 | Will_2014_PPN_alpha1_table | SOURCE_BACKED_COMPARATOR_NOT_MTS_PREDICTION | matching PPNK row numeric prediction in same fixed-GM convention |
| PBOUND2513_3_alpha2 | alpha2 | 2e-09 | Will_2014_PPN_alpha2_table | SOURCE_BACKED_COMPARATOR_NOT_MTS_PREDICTION | matching PPNK row numeric prediction in same fixed-GM convention |
| PBOUND2513_4_alpha3 | alpha3 | 4e-20 | Will_2014_PPN_alpha3_table | SOURCE_BACKED_COMPARATOR_NOT_MTS_PREDICTION | matching PPNK row numeric prediction in same fixed-GM convention |
| PBOUND2513_5_xi | xi | 4e-09 | Will_2014_PPN_xi_table | SOURCE_BACKED_COMPARATOR_NOT_MTS_PREDICTION | matching PPNK row numeric prediction in same fixed-GM convention |

## No-Absorb Guard
| guard_id | forbidden_move | reason | status |
| --- | --- | --- | --- |
| NAG2513_0_forbid_relative_G | absorb Delta_w_A/Delta_w_B into measured G | only a universal common scalar can define the measured GM quotient | FORBIDDEN |
| NAG2513_1_forbid_bound_as_prediction | treat PPN comparator bounds as MTS predictions | bounds are external targets; MTS needs kernels and coefficients | FORBIDDEN |
| NAG2513_2_forbid_GR_import | import gamma=beta=1 from GR to close the MTS local branch | the goal is to derive the GR/Newton limit or mark imported EH/GR explicitly | FORBIDDEN |
| NAG2513_3_no_cancellation | cancel gamma/beta/source/readout tails numerically without parent identity | componentwise absolute envelope remains active | FORBIDDEN |
| NAG2513_4_allow_common_GM | none: one proven universal constant normalization may be quotient-calibrated | this is a units/source convention, not a residual eraser | ALLOWED_ONLY_IF_UNIVERSALITY_PROVED |

## Nonclaim Dry Run
| case_id | case_description | result_status | blocking_markers | pass_fail | claim_pass |
| --- | --- | --- | --- | --- | --- |
| DRY2513_0_ppn_bounds_only | compare to PPN ledger without MTS response kernels | REFUSED_COMPARATOR_WITHOUT_PREDICTION | MISSING_PPN_SOURCE_RESPONSE_KERNELS | BLOCKED_NONCLAIM | False |
| DRY2513_1_absorb_relative_weights | hide relative source weights in measured GM | REFUSED_RELATIVE_GM_ABSORPTION | RELATIVE_WEIGHTS_SURVIVE_FIXED_GM | BLOCKED_NONCLAIM | False |
| DRY2513_2_import_GR_gamma_beta | set gamma=beta=1 by importing GR/EH result | REFUSED_GR_IMPORT_AS_DERIVATION | EH_IMPORT_MUST_BE_LABELED;MISSING_MTS_OPERATOR_SELECTION | BLOCKED_NONCLAIM | False |
| DRY2513_3_beta_from_gamma | infer beta closure from first-order gamma/source normalization | REFUSED_SECOND_ORDER_GAP | MISSING_BETA_SECOND_ORDER_SOURCE_KERNEL | BLOCKED_NONCLAIM | False |
| DRY2513_4_alpha3_ignore | ignore source-exchange alpha3 because WEP/product rows look clean | REFUSED_SOURCE_EXCHANGE_GAP | MISSING_ALPHA3_SOURCE_EXCHANGE_KERNEL;BOUND_4E-20 | BLOCKED_NONCLAIM | False |

## Decision Ledger
| decision_id | decision | rationale | status |
| --- | --- | --- | --- |
| DEC2513_0_gain | FIXED_GM_RULE_LOCKED | Only one proven universal common source scale may be calibrated into GM; relative/range/readout/source pieces stay residual. | selected |
| DEC2513_1_kernel | PPN_SOURCE_WEIGHT_KERNEL_MATRIX_STAGED | gamma, beta, alpha1, alpha2, alpha3, xi now each have explicit missing kernel rows and comparator bounds. | selected_nonclaim |
| DEC2513_2_beta | BETA_SECOND_ORDER_IS_LEADING_GR_GATE | beta cannot be inferred from WEP or gamma; it needs a second-order source-normalized field equation or finite source kernel. | selected_next |
| DEC2513_3_alpha3 | ALPHA3_SOURCE_EXCHANGE_IS_ULTRATIGHT | alpha3 has a 4e-20 comparator and catches source-current/nonconservation leaks that WEP can miss. | retained_parallel |
| DEC2513_4_claim | NO_PPN_OR_LOCAL_GR_CLAIM | All PPN response kernels are schema/nonclaim; no model row is score-ready. | enforced |

## Next Target
| route_id | selection_status | target_file | target_script | objective | success_condition | do_not_do |
| --- | --- | --- | --- | --- | --- | --- |
| NEXT2513_0_selected | selected | 2514-Y5-R2FR-beta-second-order-source-kernel-or-EH-operator-selection.md | scripts/Y5_R2FR_beta_second_order_source_kernel_or_EH_operator_selection_2514.py | derive the second-order beta source kernel from the parent weak-field/operator equation, or keep EH/GR import explicit and write a finite beta-source bound row | beta response has a source-normalized U^2 coefficient, fixed-GM/readout convention, units, comparator bound, and no GR import unless labeled | do not infer beta=1 from gamma, WEP, or imported Schwarzschild unless this is explicitly an EH-import branch |
| NEXT2513_1_parallel | parallel_after_beta | 2514b-Y5-R2FR-alpha3-source-exchange-current-owner-bound.md | scripts/Y5_R2FR_alpha3_source_exchange_current_owner_bound_2514b.py | derive or bound the source-exchange/current-owner contribution to alpha3 under the no-Hilbert-current and no-cancellation gates | alpha3 source-exchange row has current-owner status, kernel units, 4e-20 comparator, and no WEP-clean shortcut | do not ignore alpha3 because it is inconvenient; do not cancel current pieces without parent identity |

## Validation
| check_id | status | detail |
| --- | --- | --- |
| VAL2513_00_sources_exist | PASS |  |
| VAL2513_01_source_needles | PASS |  |
| VAL2513_02_fixed_gm_rule | PASS | fixed GM rule present |
| VAL2513_03_ppn_kernel_coverage | PASS | all major PPN observables covered |
| VAL2513_04_bounds_coverage | PASS | all comparator bounds imported |
| VAL2513_05_no_absorb_guard | PASS | relative GM absorption forbidden |
| VAL2513_06_dryruns_block_claims | PASS | all dry runs nonclaim |
| VAL2513_07_next_target | PASS | beta second-order target selected |
| VAL2513_08_no_claim_flags | PASS |  |
| VAL2513_09_branch_copies | PASS |  |
| VAL2513_10_no_formalization_artifacts | PASS |  |
| VAL2513_11_pycache_absent | PASS |  |
| VAL2513_CSV_P8_Y5_NO_SHADOW_2513_SOURCE_REGISTER | PASS | OK; rows=11 |
| VAL2513_CSV_P8_Y5_NO_SHADOW_2513_FIXED_GM_TRANSFER_GATE | PASS | OK; rows=5 |
| VAL2513_CSV_P8_Y5_NO_SHADOW_2513_PPN_SOURCE_WEIGHT_KERNEL_MATRIX | PASS | OK; rows=7 |
| VAL2513_CSV_P8_Y5_NO_SHADOW_2513_PPN_BOUND_INTERFACE | PASS | OK; rows=6 |
| VAL2513_CSV_P8_Y5_NO_SHADOW_2513_NO_GM_ABSORB_GUARD | PASS | OK; rows=5 |
| VAL2513_CSV_P8_Y5_NO_SHADOW_2513_NONCLAIM_DRYRUN_RESULTS | PASS | OK; rows=5 |
| VAL2513_CSV_P8_Y5_NO_SHADOW_2513_DECISION_LEDGER | PASS | OK; rows=5 |
| VAL2513_CSV_P8_Y5_NO_SHADOW_2513_NEXT_TARGET | PASS | OK; rows=2 |
| VAL2513_CSV_P8_Y5_NO_SHADOW_2513_BRANCH_COPIES | PASS | OK; rows=4 |
| VAL2513_COPY_CSV_ppn_kernel | PASS | OK; rows=7 |
| VAL2513_COPY_CSV_gm_guard | PASS | OK; rows=5 |
| VAL2513_COPY_CSV_bound_interface | PASS | OK; rows=6 |
| VAL2513_COPY_CSV_next_beta | PASS | OK; rows=2 |
| VAL2513_OVERALL | PASS | 2513 locks fixed-GM guard, stages PPN source-weight kernel matrix, and selects beta second-order kernel next |
