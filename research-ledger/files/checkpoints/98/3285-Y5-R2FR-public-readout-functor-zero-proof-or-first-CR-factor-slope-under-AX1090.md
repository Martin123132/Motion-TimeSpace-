# 3285 - Public readout functor zero proof or first C_R factor slope under AX1090

## Summary

3285 proves the clean theorem shape:

`R_alpha_readout = product_s Rbar_s(q(Phi), theta_rep)^{n_s}`

with `v in ker(Dq)` and `L_v theta_rep=0` gives

`C_R = sum_s n_s L_v ln R_s = 0`.

This is stronger than the old terminal-public-metric route. A terminal public coframe is not enough: the parent action/readout interface must force every readout standard to be evaluated only through `q` before observation.

The current corpus does **not** sign that full public-readout functor. So `C_R=0` is exact conditional, not a claim. The first finite factor target is now selected: Hodge/impedance plus Poynting flux, because that is where the user's EM/Poynting intuition can either become a public Maxwell/Hodge theorem or a finite `C_H/C_S` slope row.

Pure readout envelope remains:

`|C_R| <= 1.389797711495e-12` if `C_J=0`, `C_Z=0`, and `C_R` is the only live alpha/readout slope.

## Public Readout Functor Theorem
| theorem_id | claim_piece | proof_status | missing_for_claim |
| --- | --- | --- | --- |
| PRF3285_0_public_readout_category | define public readout category and standards | DEFINITION_CANDIDATE | parent action must define Q_obs, theta_rep, and the allowed ordinary readout standard class. |
| PRF3285_1_public_readout_functor_contract | single functor factorization stronger than terminality | EXACT_CONTRACT_WRITTEN_NOT_PARENT_SIGNED | the corpus has contracts and partial branches, not a parent-signed action-domain exclusion for every factor. |
| PRF3285_2_chain_rule_zero | C_R zero theorem under public-readout functor | EXACT_CHAIN_RULE_THEOREM | all factor-through-q clauses must be parent-signed together; otherwise any unsigned factor can carry finite C_R. |
| PRF3285_3_poynting_qbasic_lemma | Poynting standard zero inside public Maxwell/Hodge branch | EXACT_CONDITIONAL_LEMMA | chi->metric Hodge, same public coframe, and Z_Q/readout ownership remain unsigned. |
| PRF3285_4_terminality_insufficiency_guard | do not overclaim from terminal public metric | COUNTERMODEL_GUARD_FROM_1031 | matter/readout interface restriction and field-rename guards across constants, source normalization, and detectors. |
| PRF3285_5_current_verdict | public-readout functor status | THEOREM_SHAPE_DERIVED_PARENT_SIGNATURE_UNSIGNED | full public-readout action-domain signature or first numeric factor slope. |

## Factor-Through-q Signature Matrix
| signature_id | readout_factor | required_factorization | chain_rule_payoff | parent_signed | blocker |
| --- | --- | --- | --- | --- | --- |
| SIG3285_clock | R_phase_action_clock | R_phase_action_clock=q^*Rbar_phase | C_phase=0 | false | 1324 shows clock product wait-state; no MTS local alpha/readout product. |
| SIG3285_rods | R_light_rods | R_light_rods=q^*Rbar_light | C_light=0 | false | same public metric/coframe not parent-signed. |
| SIG3285_impedance | R_Hodge_impedance | H=Z_Q *_{g_pub}F with q-basic Z_Q and Hodge/impedance | C_H=0 | false | 3106 retains chi/Hodge theorem as open. |
| SIG3285_standard | R_Poynting_flux | S_EM^a is the q-basic public T_EM flux | C_S=0 and flux belongs to public T_EM | false | placement rule exists; Hodge/coframe/Z_Q owner unsigned. |
| SIG3285_detector | R_material_detector | R_material_detector=q^*Rbar_mat with no hidden material marker | C_mat=0 | false | material tensor and source/readout product missing. |
| SIG3285_guard | R_charge_standard | R_charge_standard fixed by same T_Q/current owner or routed to C_J | C_Qread=0 or route to C_J | false | T_Q/current/readout owner not parent-signed. |
| SIG3285_projection | R_projection_kernel | R_projection_kernel=q^*Rbar_kernel fixed before scoring | C_inst=0 | false | official/readout kernels and tau projections not score-ready. |

## Poynting q-Basic Lemma
| lemma_id | premise | derivation | C_R_payoff | status |
| --- | --- | --- | --- | --- |
| PLEM3285_0_public_flux_formula | H=Z_Q *_{g_pub}F and T_EM is varied from the same public EM action | T_EM^{mu nu}=Z_Q(F^{mu alpha}F^nu_alpha-1/4 g_pub^{mu nu}F^2); S_EM^a=-h^a_mu T_EM^{mu nu}u_nu | Poynting readout factor is q-basic if Z_Q,g_pub,u,h are q-basic | EXACT_CONDITIONAL |
| PLEM3285_1_vertical_derivative | L_v Z_Q=L_v g_pub=L_v u=L_v h=0 | L_v S_EM^a=0 by Leibniz rule because every public factor is vertical-constant | C_S=L_v ln R_Poynting_flux=0 | EXACT_CONDITIONAL |
| PLEM3285_2_constitutive_medium_escape | chi has non-q-basic hidden/domain dependence | L_v chi != 0 can create Hodge/impedance/Poynting readout drift even if ordinary F is public | finite C_H/C_S slope row required | RETAINED_RESIDUAL_ROUTE |
| PLEM3285_3_no_double_count | same EM flux is claimed as both T_EM and background E_res | energy flux is counted twice in the local source equation | route forbidden; must choose public EM stress or separate named residual | FORBIDDEN |

## First C_R Factor Slope Rows
| row_id | factor_target | C_R_prediction | C_R_abs_bound | result | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| CRF3285_0_functor_zero_conditional | all public readout factors | 0 | 1.389797711495e-12 | THEOREM_ZERO_CONDITIONAL_NONCLAIM | false |
| CRF3285_1_selected_hodge_poynting_slope | Hodge/impedance plus Poynting flux | n_H*C_H + n_S*C_S | 1.389797711495e-12 | FIRST_FACTOR_SLOPE_SELECTED_SOURCE_VALUE_MISSING | false |
| CRF3285_2_material_projection_slope | material detector plus projection kernel | n_mat*C_mat + n_inst*C_inst | 1.389797711495e-12 | SYMBOLIC_ONLY_NONCLAIM | false |
| CRF3285_3_charge_guard_slope_or_CJ_route | charge/current calibration | C_Qread_or_route_to_C_J | 1.389797711495e-12 | ROUTE_SPLIT_REQUIRED_NONCLAIM | false |
| CRF3285_4_half_bound_smoke | numeric smoke inside envelope | 6.948988557475e-13 | 1.389797711495e-12 | SMOKE | false |
| CRF3285_5_twice_bound_smoke | numeric smoke outside envelope | 2.779595422990e-12 | 1.389797711495e-12 | SMOKE | false |

## C_R Factor Runner
| row_id | C_R_prediction | prediction_over_bound | result | expectation_met | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| CRF3285_0_functor_zero_conditional | 0 | 0.000000000000e+00 | PASS_NUMERIC_NONCLAIM | true | false |
| CRF3285_1_selected_hodge_poynting_slope | n_H*C_H + n_S*C_S | N/A | SYMBOLIC_NONNUMERIC_NONCLAIM | true | false |
| CRF3285_2_material_projection_slope | n_mat*C_mat + n_inst*C_inst | N/A | SYMBOLIC_NONNUMERIC_NONCLAIM | true | false |
| CRF3285_3_charge_guard_slope_or_CJ_route | C_Qread_or_route_to_C_J | N/A | SYMBOLIC_NONNUMERIC_NONCLAIM | true | false |
| CRF3285_4_half_bound_smoke | 6.948988557475e-13 | 5.000000000000e-01 | PASS_NUMERIC_NONCLAIM | true | false |
| CRF3285_5_twice_bound_smoke | 2.779595422990e-12 | 2.000000000000e+00 | FAIL_BOUND | true | false |

## Promotion Gates
| gate_id | passed | claim_allowed | detail |
| --- | --- | --- | --- |
| GATE3285_0_chain_rule_theorem | true | false | public-readout functor factorization implies C_R=0 by chain rule. |
| GATE3285_1_parent_functor_signed | false | false | factor-through-q signature is not parent-signed for all readout factors. |
| GATE3285_2_terminality_alone_rejected | true | false | 1031 terminal-object warning is preserved; action/readout domain restriction is required. |
| GATE3285_3_poynting_lemma | true | false | Poynting q-basic lemma is exact conditional and forbids double counting. |
| GATE3285_4_finite_factor_sourced | false | false | first finite factor-slope target selected, but no numeric source-backed C_H/C_S row exists. |
| GATE3285_5_no_local_claim | true | false | no local-GR/alpha/Maxwell/clock/MICROSCOPE/PPN claim is allowed. |

## Decisions
| decision_id | decision | why_it_moves_forward | claim_allowed |
| --- | --- | --- | --- |
| DEC3285_0_theorem_result | Public-readout functor theorem is exact but conditional. | it replaces seven separate readout leaks with one parent action-domain signature. | false |
| DEC3285_1_terminality_result | Terminal public coframe is insufficient unless readout factors are forced through it before observation. | prevents a fake local-GR closure by category language alone. | false |
| DEC3285_2_poynting_result | Poynting zero works if public Hodge/Maxwell stress is q-basic; otherwise Hodge/Poynting becomes the first finite C_R factor target. | keeps the Poynting idea alive as a derivation route and a testable residual route. | false |
| DEC3285_3_next_work | Next target should attack Hodge/Poynting factor ownership or source C_H/C_S numerically. | chooses one finite slope instead of scattering across every readout factor. | false |

## Next Target
| next_id | target_doc | objective | guardrail |
| --- | --- | --- | --- |
| NEXT3285_0_3286 | 3286-Y5-R2FR-Hodge-Poynting-factor-owner-or-first-CH-CS-slope-row-under-AX1090.md | Attack the selected first C_R factor directly: prove the Hodge/impedance and Poynting flux factors are q-basic public Maxwell/Hodge readouts, or source the first numeric C_H/C_S slope row with units, sign convention, source path, and no-double-counting certificate. | Do not reopen terminal-public-metric or all-factor ledgers unless new parent evidence signs them; no clock/MICROSCOPE/PPN scoring; no Poynting double counting. |

## Validation
| check_id | check | passed | detail |
| --- | --- | --- | --- |
| VAL3285_0_sources_exist | all cited source paths exist | true |  |
| VAL3285_1_sources_parse | all cited source paths parse | true |  |
| VAL3285_2_outputs_parse | all 3285 non-validation output CSVs parse | true | non-validation outputs parsed before validation write |
| VAL3285_3_chain_rule_theorem_present | public-readout chain-rule theorem is present | true |  |
| VAL3285_4_signature_factor_coverage | signature matrix covers all seven 3284 factors | true |  |
| VAL3285_5_poynting_qbasic_lemma | Poynting q-basic lemma and no-double-count guard are present | true |  |
| VAL3285_6_first_factor_selected | Hodge/Poynting finite factor slope is selected | true |  |
| VAL3285_7_runner_expectations | C_R factor runner expectations all match | true | CRF3285_0_functor_zero_conditional=PASS_NUMERIC_NONCLAIM;CRF3285_1_selected_hodge_poynting_slope=SYMBOLIC_NONNUMERIC_NONCLAIM;CRF3285_2_material_projection_slope=SYMBOLIC_NONNUMERIC_NONCLAIM;CRF3285_3_charge_guard_slope_or_CJ_route=SYMBOLIC_NONNUMERIC_NONCLAIM;CRF3285_4_half_bound_smoke=PASS_NUMERIC_NONCLAIM;CRF3285_5_twice_bound_smoke=FAIL_BOUND |
| VAL3285_8_claim_gates_false | no 3285 gate allows local-GR/alpha/Maxwell claim | true |  |
| VAL3285_9_next_target_focused | next target focuses Hodge/Poynting factor owner or C_H/C_S slope | true |  |
| VAL3285_10_formalization_untouched | formalization-workbench modified-file count remains zero by this script | true | formalization_changed_count=0 |
| VAL3285_11_overall | 3285 validation overall | true | all required checks passed |

Generated UTC: 2026-06-27T16:24:31.646093+00:00
