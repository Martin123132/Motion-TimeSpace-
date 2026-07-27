# 3286 - Hodge/Poynting factor owner or first C_H/C_S slope row under AX1090

## Summary

3286 gets past the loose-coupling stage: the Hodge/impedance slope `C_H` and the Poynting-flux slope `C_S` are not treated as independent mystery knobs. They collapse to one owner problem:

`H^{mu nu} = 1/2 chi^{mu nu alpha beta} F_{alpha beta}`

with the metric-Hodge branch

`chi = chi_metric(g_pub,Z_Q) = Z_Q sqrt(-g_pub)(g_pub g_pub - g_pub g_pub)`.

If `chi`, `F`, the observer velocity `u`, and the spatial projector/coframe `h` are all pulled back from the public quotient, then `v in ker(Dq)` gives

`L_v H = 0`, `L_v T_EM^{mu nu} = 0`, and `L_v S_EM^a = 0`.

So the clean branch gives `C_H=0` and `C_S=0` without a hand-tuned plateau.

The current corpus still does **not** sign the full `chi -> metric Hodge` premise stack from `3106`, so this is not a Maxwell/local-GR claim. But the fallback is now sharper: define

`Delta_chi = chi - chi_metric(g_pub,Z_Q)`

and source or bound `L_v Delta_chi`. Under the pure readout envelope, the selected factor must satisfy

`|C_R^(HP)| = |n_H C_H+n_S C_S| <= 1.389797711495e-12`.

## Hodge/Poynting Owner Theorem
| theorem_id | claim_piece | derivation_status | payoff |
| --- | --- | --- | --- |
| HP3286_0_premetric_owner | one constitutive owner for Hodge and Poynting | DEFINITION_AND_BRANCH_COMPRESSION | C_H and C_S are not independent leaks once chi is owned. |
| HP3286_1_metric_Hodge_branch | metric Hodge specialization | STANDARD_CONDITIONAL_REDUCTION | finite Hodge drift is reduced to Z_Q, g_pub, and any nonmetric Delta_chi. |
| HP3286_2_vertical_zero | Hodge and Poynting zero law | EXACT_CHAIN_RULE_AND_LEIBNIZ_THEOREM | C_H=0 and C_S=0 inside the public Maxwell/Hodge branch. |
| HP3286_3_Hodge_derivative_identity | explicit derivative identity | EXACT_LOCAL_VARIATION_IDENTITY | the missing coupling is now the parent ownership of Z_Q/g_pub/F or Delta_chi, not an unspecified EM intuition. |
| HP3286_4_finite_escape | only honest finite Hodge/Poynting escape | FINITE_RESIDUAL_ROUTE_DERIVED | the next numeric target is a sourced Delta_chi slope/projection row. |

## Chi-To-Hodge Premise Audit
| premise_id | premise | current_status | source_status | blocks_zero_claim |
| --- | --- | --- | --- | --- |
| CHS3106_0_local_linear | chi is local, linear, and fixed before readout | UNSIGNED | not parent-derived here | true |
| CHS3106_1_reciprocal | chi has reciprocal/action symmetry | UNSIGNED | not parent-derived here | true |
| CHS3106_2_no_skewon | skewon/dissipative part vanishes | UNSIGNED | not parent-derived here | true |
| CHS3106_3_nonbirefringent | Fresnel quartic is a double light cone | UNSIGNED | not parent-derived here | true |
| CHS3106_4_positive_energy | EM energy density and Poynting flux have physical sign | UNSIGNED | not parent-derived here | true |
| CHS3106_5_impedance_owner | Z_Q is quotient-owned or fixed representation data | UNSIGNED | blocked by prior EM-owner work | true |
| CHS3106_6_same_public_metric | EM Hodge metric equals matter/clock/source metric | UNSIGNED | needs public geometry rule | true |
| CHS3106_7_radiative_readout | radiative/readout reductions do not regenerate f(Xhat)F^2 | UNSIGNED | unsigned in prior alpha-owner work | true |

## Poynting Branch Decision Table
| branch_id | route | condition | consequence | status | double_counting |
| --- | --- | --- | --- | --- | --- |
| HPB3286_0_public_metric_Hodge | public Maxwell/Hodge stress | chi=chi_metric(g_pub,Z_Q), Z_Q/g_pub/F/u/h all q-basic | L_v H=0 and L_v S_EM^a=0, so C_H=C_S=0 | EXACT_CONDITIONAL_NOT_PARENT_SIGNED | safe: Poynting belongs only to T_EM |
| HPB3286_1_finite_constitutive_medium | Delta_chi medium residual | chi has hidden/domain dependence not forced through q | C_H/C_S are projections of L_v Delta_chi and must be sourced or bounded | LIVE_FINITE_ROUTE | safe only if counted as EM constitutive residual, not also hidden E_res flux |
| HPB3286_2_independent_background_flux | separate MTS background energy flux | background carries energy not equal to public EM Poynting flux | route belongs to E_res_munu/stress conservation, not to the public C_H/C_S readout factor | SEPARATE_BRANCH | safe only if named separately and never duplicated as T_EM flux |
| HPB3286_3_forbidden_double_count | same Poynting flux used twice | EM flux is both public T_EM and hidden background source | source equation is overcounted | FORBIDDEN | forbidden by 3105/3285 guard |

## C_H/C_S Formula Rows
| formula_id | object | formula | required_inputs |
| --- | --- | --- | --- |
| HPC3286_0_metric_decomposition | constitutive split | chi = chi_metric(g_pub,Z_Q) + Delta_chi | parent chi, public metric g_pub, Z_Q normalization, sign convention |
| HPC3286_1_CH_projection | Hodge/impedance slope | C_H = Pi_H[L_v Delta_chi + L_v chi_metric]/N_H; public branch sets L_v chi_metric=0 and leaves C_H=Pi_H[L_v Delta_chi]/N_H | projection Pi_H, normalisation N_H, sourced L_v Delta_chi |
| HPC3286_2_CS_projection | Poynting flux slope | C_S = Pi_S[L_v Delta_chi, L_v u, L_v h]/N_S; public branch sets L_v Delta_chi=L_v u=L_v h=0 | projection Pi_S, N_S, observer/coframe ownership, sourced L_v Delta_chi |
| HPC3286_3_alpha_factor_bound | first Hodge/Poynting alpha readout factor | C_R^(HP)=n_H C_H+n_S C_S with \|C_R^(HP)\| <= 1.389797711495e-12 | n_H,n_S,C_H,C_S and all no-double-counting/source certificates |

## First C_H/C_S Slope Rows
| row_id | factor_target | C_R_HP_prediction | C_R_HP_abs_bound | source_status | result | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| HPR3286_0_public_Hodge_Poynting_zero_conditional | Hodge/impedance plus Poynting flux | 0 | 1.389797711495e-12 | THEOREM_CONDITIONAL | PASS_NUMERIC_NONCLAIM_IF_ALL_CHS_PREMISES_SIGNED | false |
| HPR3286_1_Delta_chi_finite_slope | finite constitutive medium residual | n_H*Pi_H[L_v Delta_chi]/N_H + n_S*Pi_S[L_v Delta_chi,L_vu,L_vh]/N_S | 1.389797711495e-12 | MISSING_NUMERIC_DELTA_CHI_PROJECTION | REFUSE_MISSING_SOURCE_NONCLAIM | false |
| HPR3286_2_missing_parent_chi_source | parent-owned chi to metric-Hodge theorem | MISSING_PARENT_CHI_SIGNATURE | 1.389797711495e-12 | CHS3106_0_TO_7_UNSIGNED | REFUSE_CLAIM | false |
| HPR3286_3_half_bound_smoke | numeric runner smoke inside envelope | 6.948988557475e-13 | 1.389797711495e-12 | SMOKE_ONLY | SMOKE | false |
| HPR3286_4_twice_bound_smoke | numeric runner smoke outside envelope | 2.779595422990e-12 | 1.389797711495e-12 | SMOKE_ONLY | SMOKE | false |

## C_H/C_S Bound Runner
| row_id | C_R_HP_prediction | prediction_over_bound | result | expectation_met | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| HPR3286_0_public_Hodge_Poynting_zero_conditional | 0 | 0.000000000000e+00 | PASS_NUMERIC_NONCLAIM | true | false |
| HPR3286_1_Delta_chi_finite_slope | n_H*Pi_H[L_v Delta_chi]/N_H + n_S*Pi_S[L_v Delta_chi,L_vu,L_vh]/N_S | N/A | REFUSE_MISSING_SOURCE_NONCLAIM | true | false |
| HPR3286_2_missing_parent_chi_source | MISSING_PARENT_CHI_SIGNATURE | N/A | REFUSE_MISSING_SOURCE_NONCLAIM | true | false |
| HPR3286_3_half_bound_smoke | 6.948988557475e-13 | 5.000000000000e-01 | PASS_NUMERIC_NONCLAIM | true | false |
| HPR3286_4_twice_bound_smoke | 2.779595422990e-12 | 2.000000000000e+00 | FAIL_BOUND | true | false |

## Promotion Gates
| gate_id | passed | claim_allowed | detail |
| --- | --- | --- | --- |
| GATE3286_0_owner_compression | true | false | Hodge and Poynting slopes collapse to one constitutive owner object chi plus public observer coframe. |
| GATE3286_1_zero_law | true | false | If chi/F/u/h are q-basic, L_v H=0 and L_v S_EM^a=0 by chain rule/Leibniz. |
| GATE3286_2_CHS_premises_signed | false | false | CHS3106_0..7 remain unsigned in the current corpus. |
| GATE3286_3_numeric_Delta_chi_sourced | false | false | No numeric/source-backed Pi_H or Pi_S projection row for L_v Delta_chi exists. |
| GATE3286_4_no_double_count | true | false | Public EM Poynting flux and independent background flux are separated; duplicate source use is forbidden. |
| GATE3286_5_no_local_claim | true | false | No Maxwell/local-GR/alpha/PPN/clock claim is allowed from this checkpoint. |

## Decisions
| decision_id | decision | why_it_moves_forward | claim_allowed |
| --- | --- | --- | --- |
| DEC3286_0_progress | C_H and C_S are reduced to a single chi/Delta_chi ownership problem. | we are no longer chasing two loose couplings; the finite branch has one sourceable vertical constitutive residual. | false |
| DEC3286_1_zero_route | The public Maxwell/Hodge branch gives an exact conditional zero law. | a future parent action only has to sign chi/F/u/h through q, not invent separate Poynting cancellation. | false |
| DEC3286_2_failure_route | If chi cannot be parent-signed as metric Hodge, the branch becomes a finite Delta_chi slope test. | the fallback is empirical/sourceable instead of closure-only hand waving. | false |
| DEC3286_3_next_work | Attack CHS3106_0..7 directly or source the first Delta_chi projection row. | this is the least-scattered next target and directly addresses the missing coupling. | false |

## Next Target
| next_id | target_doc | objective | guardrail |
| --- | --- | --- | --- |
| NEXT3286_0_3287 | 3287-Y5-R2FR-chi-to-metric-Hodge-premise-proof-or-DeltaChi-slope-source-row-under-AX1090.md | Prove or reject the chi-to-metric-Hodge premise stack: local linear, reciprocal, no-skewon, nonbirefringent, positive, same-public-metric, q-basic impedance, and radiative/readout protection; if not parent-signed, source the first finite Delta_chi projection row. | Do not score C_H/C_S as evidence, do not claim EM/local-GR, do not double-count Poynting, and do not reopen all readout factors. |

## Validation
| check_id | check | passed | detail |
| --- | --- | --- | --- |
| VAL3286_0_sources_exist | all cited source paths exist | true |  |
| VAL3286_1_sources_parse | all cited source paths parse | true |  |
| VAL3286_2_outputs_parse | all 3286 non-validation output CSVs parse | true | non-validation outputs parsed before validation write |
| VAL3286_3_zero_law_present | owner theorem includes L_v H and L_v S_EM zero law | true |  |
| VAL3286_4_premise_stack_covered | CHS3106_0..7 premise stack is represented and unsigned | true |  |
| VAL3286_5_Delta_chi_formula_present | finite fallback is explicitly Delta_chi based | true |  |
| VAL3286_6_no_double_count_guard | Poynting double-count branch is forbidden | true |  |
| VAL3286_7_runner_expectations | C_H/C_S runner expectations all match | true | HPR3286_0_public_Hodge_Poynting_zero_conditional=PASS_NUMERIC_NONCLAIM;HPR3286_1_Delta_chi_finite_slope=REFUSE_MISSING_SOURCE_NONCLAIM;HPR3286_2_missing_parent_chi_source=REFUSE_MISSING_SOURCE_NONCLAIM;HPR3286_3_half_bound_smoke=PASS_NUMERIC_NONCLAIM;HPR3286_4_twice_bound_smoke=FAIL_BOUND |
| VAL3286_8_claim_gates_false | no 3286 gate allows local-GR/alpha/Maxwell claim | true |  |
| VAL3286_9_next_target_focused | next target focuses chi-to-Hodge proof or Delta_chi source row | true |  |
| VAL3286_10_formalization_untouched | formalization-workbench modified-file count remains zero by this script | true | formalization_changed_count=0 |
| VAL3286_11_overall | 3286 validation overall | true | all required checks passed |

Generated UTC: 2026-06-27T16:34:12.109911+00:00
