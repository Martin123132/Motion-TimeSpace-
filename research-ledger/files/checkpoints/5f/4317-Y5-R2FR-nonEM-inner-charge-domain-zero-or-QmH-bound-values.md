# 4317 - nonEM inner charge domain zero or QmH bound values

## Verdict

- Real gain: `N_inner=0` now has exact domain/source conditions, not just a missing-label wish.
- Conditional reduction: if visible+EM gates close and the smooth full-domain source branch is signed, `N_pair <= N_rest_nonEM`.
- Exterior branch remains honest: `N_inner <= ||mu_tr||+||B_src^A||` or `C_0|Q_m^H|+C_perp||g_perp||+||B_src||`.
- No local GR/Newton claim fires; the next target is the remaining `N_rest_nonEM` budget.

## Source Register
| source_id | source_path | exists | needle_found | purpose |
| --- | --- | --- | --- | --- |
| SRC4317_00_4316_next | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4316_NEXT_TARGET.csv | True | True | 4316 handoff selecting the inner/domain charge branch. |
| SRC4317_01_4303_component | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\319-PPC4161-source-boundary-silence-or-component-norms-for-m-lock.md | True | True | 4303 component ledger naming inner charge as primary boundary blocker. |
| SRC4317_02_4305_reduction | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\321-PPC4161-source-amplitude-inner-charge-EM-residual-reduction.md | True | True | 4305 source-pair branch before visible/EM reduction. |
| SRC4317_03_4306_weak_law | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\322-PPC4161-inner-domain-certificate-or-QmH-bound.md | True | True | 4306 derived inner-boundary functional. |
| SRC4317_04_4306_trace_bound | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\322-PPC4161-inner-domain-certificate-or-QmH-bound.md | True | True | 4306 monopole/multipole/source-boundary split. |
| SRC4317_05_4307_domain_split | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\323-PPC4161-source-domain-owner-or-inner-flux-profile-fill.md | True | True | 4307 smooth-domain identity branch. |
| SRC4317_06_4308_trace_defect | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\324-PPC4161-smooth-Hilbert-volume-domain-parent-signature-or-worldtube-flux-profile-row.md | True | True | 4308 exterior readout trace-defect object. |
| SRC4317_07_4309_conormal | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\325-PPC4161-source-domain-limit-defect-zero-or-first-numeric-flux-bound.md | True | True | 4309 weak conormal trace bound route. |
| SRC4317_08_4310_collar | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\326-PPC4161-collar-no-concentration-signature-or-trace-bound-inputs.md | True | True | 4310 collar amplitude bound replacing a free trace amplitude. |
| SRC4317_09_4311_lambda | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\327-PPC4161-lambda-floor-source-row-or-collar-residual-first-bound.md | True | True | 4311 exact lambda-floor law. |
| SRC4317_10_4316_budget | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\332-PPC4161-visible-Hilbert-source-silence-integration-or-nonEM-residual-budget.md | True | True | 4316 visible/EM source budget reduction. |

## Zero Theorem Audit
| theorem_id | clause | condition | consequence | status |
| --- | --- | --- | --- | --- |
| ZT4317_0_full_domain | m-lock operator domain contains compact Hilbert source volume | D_m = W_H union A_ext and W_H is not removed before variation | partialD_in = empty set; B_inner=0; N_inner=0 | EXACT_DOMAIN_IDENTITY_IF_PARENT_SIGNED |
| ZT4317_1_no_direct_m_charge | matter/source action carries no independent m-boundary charge | source factors through q/Hilbert variables already owned by S_vis and source kernel | B_src^A=0 and Q_m^H=0 | EXACT_ZERO_CLAUSE_IF_PARENT_SIGNED |
| ZT4317_2_interface_cancellation | worldtube surface is only a split of a full-domain weak form | oriented inner and outer interface terms are equal and opposite | interface flux is bookkeeping, not a physical inner source | DERIVED_BOOKKEEPING_ZERO |
| ZT4317_3_smooth_to_exterior_limit | exterior readout is taken as a limit of smooth full-domain sources | mu_tr=0 and B_src^A=0 | N_inner=0 survives exterior readout | CONDITIONAL_LIMIT_ZERO_NOT_PARENT_SIGNED |
| ZT4317_4_failure_branch | source is solved as exterior/worldtube or point/excision problem | partialD_in nonempty or trace-defect/source injection survives | N_inner must be bounded, not erased | BOUND_BRANCH_REQUIRED |

## Branch Selector
| selector_id | branch_condition | output_formula | status | guard |
| --- | --- | --- | --- | --- |
| BR4317_0_standard_smooth | visible+EM zero branch from 4316 plus full smooth Hilbert source domain | N_pair <= N_rest_nonEM | BEST_LOCAL_SOURCE_BRANCH_CONDITIONAL | use for derivation work only after parent/domain signature exists |
| BR4317_1_full_domain_internal_split | worldtube surface introduced only after solving full-domain weak problem | no physical Q_m^H row is charged to N_inner | BOOKKEEPING_ZERO_ROUTE | must not be mixed with exterior-only boundary data |
| BR4317_2_exterior_trace_defect | exterior/worldtube branch with surviving trace-defect | N_pair <= N_rest_nonEM + \|\|mu_tr\|\| + \|\|B_src^A\|\| | TRACE_DEFECT_BOUND_ROUTE | requires trace/collar/lambda inputs before local tests |
| BR4317_3_QmH_profile | monopole/multipole profile branch | N_pair <= N_rest_nonEM + C_0\|Q_m^H\| + C_perp\|\|g_perp\|\| + \|\|B_src\|\| | PROFILE_BOUND_ROUTE | scalar Q_m^H alone is insufficient unless g_perp and B_src are zero/bounded |
| BR4317_4_invalid_mix | borrowing smooth zero inside exterior/excision calculation | reject branch | INVALID_BRANCH_MIX | prevents smuggled local-GR closure |

## Bound Input Schema
| input_id | symbol | units_or_norm | required_value | status |
| --- | --- | --- | --- | --- |
| BI4317_0_mu_tr | mu_tr | H^{-1/2}(partialW_H) | zero or finite norm | MISSING_ZERO_THEOREM_OR_VALUE |
| BI4317_1_BsrcA | B_src^A | H^{-1/2}(partialW_H) | zero or finite norm | MISSING_ZERO_THEOREM_OR_VALUE |
| BI4317_2_CN | C_N | dimensionless/operator norm | positive finite constant | MISSING_ARENA_PROJECTION |
| BI4317_3_KU | K_U | operator/collar norm | positive finite ceiling | MISSING_COMPONENT_VALUES |
| BI4317_4_Ccol | C_col | dimensionless/operator norm | positive finite constant | MISSING_ARENA_PROJECTION |
| BI4317_5_lambda_star | lambda_* | same as m-lock quadratic form floor | lambda_* = Z_min lambda_1(D_loc)+M2_min-Eta_H > 0 | FORMULA_READY_VALUE_UNSOURCED |
| BI4317_6_SU_not_inner | S_U_not_inner | same dual/source norm as collar forcing | sum of non-inner residual rows | FORMULA_READY_COMPONENT_VALUES_MISSING |
| BI4317_7_RU | R_U | H^{-1}(U_W) | zero theorem or finite norm | MISSING_ZERO_THEOREM_OR_VALUE |
| BI4317_8_QmH | Q_m^H | flux integral over partialW_H | zero theorem or finite value | MISSING_ZERO_THEOREM_OR_VALUE |
| BI4317_9_gperp | g_perp | H^{-1/2}(partialW_H) | zero theorem or finite norm | MISSING_ZERO_THEOREM_OR_VALUE |
| BI4317_10_C0 | C_0 | operator/domain constant | positive finite constant | MISSING_ARENA_PROJECTION |
| BI4317_11_Cperp | C_perp | operator/domain constant | positive finite constant | MISSING_ARENA_PROJECTION |
| BI4317_12_Bsrc | B_src | boundary dual norm | zero theorem or finite norm | MISSING_ZERO_THEOREM_OR_VALUE |

## Reduced Formulas
| formula_id | name | formula | status |
| --- | --- | --- | --- |
| F4317_0_inner_functional | inner boundary functional | B_inner[phi] = int_partialD_in phi Z_m n.grad u dSigma + B_src[phi] | DERIVED |
| F4317_1_smooth_zero | smooth full-domain zero | partialD_in=empty and B_src=0 => N_inner=0 | EXACT_IF_BRANCH_SIGNED |
| F4317_2_interface_zero | internal interface cancellation | int_partialW phi Z_m n_A.grad u + int_partialW phi Z_m n_W.grad u = 0 | DERIVED_BOOKKEEPING_IDENTITY |
| F4317_3_trace_defect_bound | exterior trace-defect bound | N_inner <= \|\|mu_tr\|\| + \|\|B_src^A\|\| | BOUND_FORMULA_READY_VALUES_MISSING |
| F4317_4_collar_bound | lambda-floor trace bound | N_inner <= C_N[K_U C_col S_U_not_inner/lambda_* + R_U] + \|\|B_src^A\|\| | GUARDED_BOUND_READY_VALUES_MISSING |
| F4317_5_profile_bound | QmH profile envelope | N_inner <= C_0\|Q_m^H\| + C_perp\|\|g_perp\|\| + \|\|B_src\|\| | BOUND_FORMULA_READY_VALUES_MISSING |
| F4317_6_reduced_source_pair | 4316 plus inner zero | if N_visible=N_EM=N_inner=0 then N_pair <= N_rest_nonEM | CONDITIONAL_REDUCTION |
| F4317_7_all_source_zero | exact local source silence | if N_rest_nonEM=0 also, then N_pair=0 | NOT_LIVE |
| F4317_8_m_lock_handoff | m-lock amplitude | Delta_m <= (N_rest_nonEM + N_N)/lambda_m on full zero branch | HANDOFF_READY_NOT_SCORE_READY |

## Runner
| runner_id | scenario | action | output | reason |
| --- | --- | --- | --- | --- |
| RUN4317_0_current_safe | current corpus, no new parent domain signature | USE_TRACE_OR_PROFILE_BOUND | N_pair <= N_rest_nonEM + N_inner_bound | local GR/Newton blocked |
| RUN4317_1_best_if_signed | visible+EM zero and smooth full-domain N_inner=0 signed | ALLOW_NPAIR_TO_NONEM | N_pair <= N_rest_nonEM | next attack N_rest_nonEM and lambda/source equality |
| RUN4317_2_all_nonEM_zero | N_rest_nonEM also zero or finitely below local precision budget | ALLOW_SOURCE_PAIR_ZERO_OR_SMALL | N_pair=0 or bounded below arena tolerance | still needs lambda_m, R_eq, I_commutator, projection |
| RUN4317_3_invalid_excision_zero | exterior/excision branch but N_inner set to zero without trace/no-flux theorem | REJECT | no score | branch-mixing firewall |
| RUN4317_4_numeric_fallback | Q_m^H/g_perp/B_src/C constants sourced | ALLOW_NONCLAIM_LOCAL_BOUND | N_inner finite bound feeds R10/PPN/clocks/orbital residual tests | claim only after all rows valid and within arena budgets |

## Decision
| decision_id | result | reason | next_action |
| --- | --- | --- | --- |
| DEC4317_0_gain | NINNER_ZERO_CONDITIONS_EXACT | The smooth full-domain route is now an exact domain/source theorem rather than a vague hope. | try to parent-sign full-domain source ownership before choosing exterior fallback |
| DEC4317_1_reduction | SOURCE_PAIR_CAN_REDUCE_TO_NREST_NONEM | 4316 plus N_inner=0 gives N_pair <= N_rest_nonEM. | attack non-Hilbert support, drift/selector, history/transition, boundary/domain and nonlinear rows next |
| DEC4317_2_fallback | TRACE_PROFILE_BOUND_RETAINED | If exterior/worldtube language survives, Q_m^H alone is not enough; multipoles and source injection remain. | source or theorem-zero C_0, Q_m^H, C_perp, g_perp and B_src |
| DEC4317_3_claim | NO_LOCAL_CLAIM | This closes or bounds one source component only; it does not derive the full GR/Newton limit. | keep all claim flags false |
| DEC4317_4_next | NONEM_REST_NEXT | After visible/EM and possible N_inner zero, the dominant budget is N_rest_nonEM. | 4318-Y5-R2FR-nonHilbert-support-drift-history-bound-prioritizer.md |

## Status
| status_id | object | status | note |
| --- | --- | --- | --- |
| STAT4317_0_Ninner_smooth | N_inner smooth branch | EXACT_ZERO_IF_PARENT_SIGNED | full source domain/no independent m-charge |
| STAT4317_1_Ninner_exterior | N_inner exterior branch | BOUND_REQUIRED | trace-defect/profile rows required |
| STAT4317_2_QmH | Q_m^H scalar | INSUFFICIENT_ALONE | must pair with g_perp and B_src rows |
| STAT4317_3_Npair | N_pair | CAN_REDUCE_TO_NREST_NONEM | only on visible+EM+Ninner zero branch |
| STAT4317_4_lambda | lambda_* | STILL_GATED | positivity formula derived but values not sourced |
| STAT4317_5_local | local GR/Newton | BLOCKED | N_rest_nonEM/source equality/projection gates remain |

## Next Target
| next_target_id | next_target | target_question | preferred_route | fallback_route |
| --- | --- | --- | --- | --- |
| NT4317_0 | 4318-Y5-R2FR-nonHilbert-support-drift-history-bound-prioritizer.md | Can the remaining non-EM source budget N_rest_nonEM be split into zeroable theorem branches and finite bound rows without double-counting N_inner? | derive/source-kill non-Hilbert support, drift/selector, history/transition, boundary/domain and nonlinear rows componentwise | stage nonclaim numeric/budget schemas for each residual and route them into lambda-floor/local precision tests |
