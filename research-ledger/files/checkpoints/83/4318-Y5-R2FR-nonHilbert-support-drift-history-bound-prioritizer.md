# 4318 - nonHilbert support drift history bound prioritizer

## Verdict

- `N_rest_nonEM` is now canonical and single-count: `N_src_nonHilbert + N_drift_selector + N_history_transition + N_boundary_domain + N_N`.
- `N_N` is included once; do not add another `+N_N` after using `N_rest_nonEM^canon`.
- Nonlinear remainder has a real absorption route: if `N_N <= kappa_N lambda_m Delta_m`, then `Delta_m <= N_linear / ((1-kappa_N) lambda_m)`.
- Next target is `N_src_nonHilbert/Hperp`, because it has the best zero-or-bound machinery already built.

## Source Register
| source_id | source_path | exists | needle_found | purpose |
| --- | --- | --- | --- | --- |
| SRC4318_00_next | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4317_NEXT_TARGET.csv | True | True | 4317 handoff selecting the residual non-EM budget. |
| SRC4318_01_components | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\319-PPC4161-source-boundary-silence-or-component-norms-for-m-lock.md | True | True | 4303 source-support row. |
| SRC4318_02_drift | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\319-PPC4161-source-boundary-silence-or-component-norms-for-m-lock.md | True | True | 4303 drift/selector row. |
| SRC4318_03_history | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\319-PPC4161-source-boundary-silence-or-component-norms-for-m-lock.md | True | True | 4303 history/transition row. |
| SRC4318_04_boundary | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\319-PPC4161-source-boundary-silence-or-component-norms-for-m-lock.md | True | True | 4303 boundary/domain row. |
| SRC4318_05_NN | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\319-PPC4161-source-boundary-silence-or-component-norms-for-m-lock.md | True | True | 4303 nonlinear/noise handoff row. |
| SRC4318_06_Nrest | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\332-PPC4161-visible-Hilbert-source-silence-integration-or-nonEM-residual-budget.md | True | True | 4316 canonical residual sum before inner-charge sharpening. |
| SRC4318_07_4317_reduction | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\333-PPC4161-nonEM-inner-charge-domain-zero-or-QmH-bound-values.md | True | True | 4317 handoff after visible/EM/inner source reductions. |
| SRC4318_08_standard_Nsrc | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\321-PPC4161-source-amplitude-inner-charge-EM-residual-reduction.md | True | True | 4305 standard Dq/Hperp-closed source-support zero branch. |
| SRC4318_09_source_anchor | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\320-PPC4161-first-source-norms-or-visible-Hilbert-m-lock-signature.md | True | True | 4304 private source-support scale anchor. |
| SRC4318_10_collar_split | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\327-PPC4161-lambda-floor-source-row-or-collar-residual-first-bound.md | True | True | 4311 collar residual split into physical rows. |
| SRC4318_11_Hperp_bound | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\260-PPC4161-Dq-component-zero-adoption-or-Hperp-bound-input-fill.md | True | True | 4244 Hperp/Dq fallback bound feeding non-Hilbert source support. |

## Canonical Budget
| residual_id | symbol | zero_route | bound_route | priority |
| --- | --- | --- | --- | --- |
| NR4318_0_Nsrc | N_src_nonHilbert | zero if standard Dq/Hperp branch gives S_A Hperp^A=0 or projected source support vanishes | N_src <= \|\|U_B\|\|_inf \|\|S_cg_nonHilbert\|\| <= U_B^2 A_src_general or C_S C_perp E_Dq,H | PRIORITY_1 |
| NR4318_1_Ndrift | N_drift_selector | zero if branch selector is fixed/q-basic and m_L/L_cg do not move under local variation | N_drift_selector <= N_drift_mL + N_drift_Lcg + N_selector | PRIORITY_2 |
| NR4318_2_Nhistory | N_history_transition | zero if local causal silence and transition-kernel membership are parent-signed | N_history_transition <= N_history + N_transition + N_mass_current | PRIORITY_3 |
| NR4318_3_Nboundary | N_boundary_domain | zero if no-flux, zero-mode removal, fixed domain and outer boundary routing are all signed | N_boundary_domain <= N_no_flux + N_zero_mode + N_outer + N_history_boundary + N_domain | PRIORITY_4 |
| NR4318_4_NN | N_N | zero if nonlinear remainder vanishes; absorbable if N_N <= kappa_N lambda_m Delta_m with kappa_N<1 | otherwise retain N_N as a finite absolute row | PRIORITY_5_DEPENDS_ON_LAMBDA |

## Priority Order
| rank | target | reason | proposed_target |
| --- | --- | --- | --- |
| 1 | N_src_nonHilbert / Hperp | highest leverage direct source row; already has standard zero route and finite Dq/Hperp route | 4319-Y5-R2FR-nonHilbert-Hperp-source-support-zero-or-bound-row.md |
| 2 | N_drift_selector | can be killed by fixed selector/local branch theorem; otherwise easy absolute sum | 43120-Y5-R2FR-fixed-selector-drift-zero-or-bound-row.md |
| 3 | N_history_transition | transition/history leakage is dangerous for local tests but should be separated from source support | 43121-Y5-R2FR-history-transition-causal-silence-or-bound-row.md |
| 4 | N_boundary_domain | important but depends on no-flux/zero-mode/domain certificates already entangled with lambda/domain gates | 43122-Y5-R2FR-boundary-domain-no-flux-zero-mode-or-bound-row.md |
| 5 | N_N absorption | should be handled once lambda_m and linear residual rows are clearer | 43123-Y5-R2FR-nonlinear-absorption-kappaN-or-remainder-bound.md |

## Single Count Repair
| repair_id | formula | use_rule | status |
| --- | --- | --- | --- |
| SC4318_0_canon | N_rest_nonEM^canon := N_src_nonHilbert + N_drift_selector + N_history_transition + N_boundary_domain + N_N | Use this symbol when quoting 4317/4318 source-pair reductions. | REPAIR_APPLIED |
| SC4318_1_delta_m | Delta_m <= N_rest_nonEM^canon/lambda_m | Do not write Delta_m <= (N_rest_nonEM^canon + N_N)/lambda_m. | DOUBLE_COUNT_BLOCKED |
| SC4318_2_linear_split | N_linear := N_src_nonHilbert + N_drift_selector + N_history_transition + N_boundary_domain | Useful for nonlinear absorption. | FORMULA_READY |
| SC4318_3_absorption | if N_N <= kappa_N lambda_m Delta_m and 0<=kappa_N<1, then Delta_m <= N_linear/((1-kappa_N)lambda_m) | Moves small nonlinear remainder to the left side instead of double-counting it. | DERIVED_CONDITIONAL |

## Runner
| runner_id | scenario | action | output | note |
| --- | --- | --- | --- | --- |
| RUN4318_0_current | current corpus | USE_CANONICAL_BUDGET | N_pair <= N_rest_nonEM^canon | no local claim |
| RUN4318_1_Nsrc_zero | N_src_nonHilbert theorem-zeroed next | REDUCE_BUDGET | N_rest_nonEM^canon -> N_drift_selector+N_history_transition+N_boundary_domain+N_N | best next move |
| RUN4318_2_all_linear_zero | source/drift/history/boundary zero | CHECK_NONLINEAR | Delta_m controlled by N_N/lambda_m or absorbed if kappa_N<1 | still needs lambda_m |
| RUN4318_3_absorbed_NN | N_N absorbable and lambda_m positive | ALLOW_SOURCE_PAIR_ZERO_CONDITIONAL | Delta_m=0 if N_linear=0 | not enough for local GR without downstream gates |
| RUN4318_4_numeric_bound | all residual rows sourced as finite values | ALLOW_NONCLAIM_PRECISION_TEST | feed R10/PPN/clocks/orbital residual budgets | claim only after full gate coverage |

## Decision
| decision_id | result | reason | next_action |
| --- | --- | --- | --- |
| DEC4318_0_gain | NREST_CANONICALIZED | N_rest_nonEM is now a five-row single-count budget. | use N_rest_nonEM^canon going forward |
| DEC4318_1_repair | NN_DOUBLE_COUNT_BLOCKED | N_N is included exactly once in the canonical symbol. | repair later formulas if they add +N_N to N_rest_nonEM^canon |
| DEC4318_2_absorption | NONLINEAR_ABSORPTION_ROUTE_DERIVED | small N_N can move to the left side with a 1-kappa_N penalty. | source kappa_N after linear rows are controlled |
| DEC4318_3_priority | NSRC_HPERP_FIRST | N_src_nonHilbert has both a zero theorem route and an existing Hperp/Dq finite-bound route. | 4319-Y5-R2FR-nonHilbert-Hperp-source-support-zero-or-bound-row.md |
| DEC4318_4_claim | NO_LOCAL_CLAIM | This is a budget/prioritization step, not a complete GR/Newton derivation. | keep all claim flags false |

## Status
| status_id | object | status | note |
| --- | --- | --- | --- |
| STAT4318_0_Nrest | N_rest_nonEM^canon | DEFINED_SINGLE_COUNT | five residual rows, N_N included once |
| STAT4318_1_Nsrc | N_src_nonHilbert | NEXT_PRIMARY_TARGET | Hperp/Dq theorem-or-bound |
| STAT4318_2_Ndrift | N_drift_selector | OPEN_ZERO_OR_BOUND | fixed selector theorem needed |
| STAT4318_3_Nhistory | N_history_transition | OPEN_ZERO_OR_BOUND | causal/transition-kernel theorem needed |
| STAT4318_4_Nboundary | N_boundary_domain | OPEN_ZERO_OR_BOUND | no-flux/zero-mode/domain certificates needed |
| STAT4318_5_NN | N_N | ABSORB_OR_BOUND | requires kappa_N<1 or finite remainder row |
| STAT4318_6_local | local GR/Newton | BLOCKED | source equality, commutator, projection and lambda gates remain |

## Next Target
| next_target_id | next_target | target_question | preferred_route | fallback_route |
| --- | --- | --- | --- | --- |
| NT4318_0 | 4319-Y5-R2FR-nonHilbert-Hperp-source-support-zero-or-bound-row.md | Can N_src_nonHilbert be theorem-zeroed by the standard Dq/Hperp branch, or bounded by a real E_Dq,H / A_src row? | prove Hperp=0 or S_A Hperp^A=0 from parent source support and Dq ownership | fill nonclaim C_S, C_perp, E_Dq,H or U_B^2 A_src_general rows and feed them into N_rest_nonEM^canon |
