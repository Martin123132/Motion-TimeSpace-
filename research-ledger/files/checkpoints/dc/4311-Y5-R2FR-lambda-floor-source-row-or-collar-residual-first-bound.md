# 4311 - lambda-floor source row or collar residual first bound

## Verdict
- Derived the exact local lambda-floor law: `lambda_* = Z_min lambda_1(D_loc)+M2_min-Eta_H`.
- Split positivity into three honest routes: Poincare/Dirichlet gap, mass-only zero-mode gap, or mixed margin.
- Staged the first residual/budget bound: `N_inner <= C_N[K_U C_col S_U/lambda_* + R_U] + ||B_src^A||`.
- Kept Poynting/wave flow explicit as `R_EM_Poynting` or boundary flux, not a hidden zero.
- No local-GR/Newton/R10/PPN claim fires.

## Source Register
| source_id | source_path | exists | needle_found | purpose |
| --- | --- | --- | --- | --- |
| SRC4311_00_4310_formal | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\326-PPC4161-collar-no-concentration-signature-or-trace-bound-inputs.md | True | True | 4310 reduced the trace defect to lambda floor plus collar residual numerator. |
| SRC4311_01_4310_next | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4310_NEXT_TARGET.csv | True | True | 4310 handoff selecting lambda floor or first residual row. |
| SRC4311_02_4302_lambda_formula | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\318-PPC4161-m-lock-coercivity-gap-and-DvGamma-quadratic-input-pack.md | True | True | parent m-lock coercive gap formula. |
| SRC4311_03_4302_component_gaps | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\318-PPC4161-m-lock-coercivity-gap-and-DvGamma-quadratic-input-pack.md | True | True | component ledger showing Z_min is still missing. |
| SRC4311_04_4302_eta | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\318-PPC4161-m-lock-coercivity-gap-and-DvGamma-quadratic-input-pack.md | True | True | component ledger showing Eta_H correction bound is still missing. |
| SRC4311_05_4268_fixed_collar | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\284-PPC4161-Dq-boundary-projector-fixed-collar-or-boundary-residual-bound.md | True | True | fixed collar/q-basic boundary projector branch. |
| SRC4311_06_4176_no_flux | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\192-PPC4161-local-boundary-no-flux-sector-interface-theorem.md | True | True | local no-flux/support-separation selector. |
| SRC4311_07_319_no_m_slot | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\319-PPC4161-source-boundary-silence-or-component-norms-for-m-lock.md | True | True | visible Hilbert matter no-direct-m source clause. |
| SRC4311_08_321_source_split | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\321-PPC4161-source-amplitude-inner-charge-EM-residual-reduction.md | True | True | source-pair residual split entering collar forcing. |
| SRC4311_09_223_poynting | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\223-PPC4161-EM-Poynting-Hodge-source-owner-lock.md | True | True | Poynting/Hilbert stress owner rule for EM residual handling. |
| SRC4311_10_309_precision | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\309-PPC4161-epsilon-mu-tr-shared-local-bound-runner-WEP-R10-PPN-clocks-orbital.md | True | True | local tests require zero/suppression, not raw leakage. |
| SRC4311_11_1714_guard | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1714-Y5-R2FR-Y5-worldtube-Hilbert-source-equality-or-Req-Icommutator-fill.md | True | True | source-to-Newton equality guard still open. |

## Lambda Component Ledger
| component_id | symbol | definition | required_law | status | role | next_action |
| --- | --- | --- | --- | --- | --- | --- |
| LC4311_0_Zmin | Z_min | elliptic kinetic lower bound for the m-lock fluctuation on the collar | Z_m >= Z_min > 0 | MISSING_SOURCE_VALUE_OR_THEOREM | needed for Poincare/mixed positive gap | source parent kinetic sign/normalization or demote to fitted closure |
| LC4311_1_lambda1 | lambda_1(D_loc) | first positive eigenvalue/Poincare gap of the fixed collar domain | \|\|grad u\|\|^2 >= lambda_1(D_loc)\|\|u\|\|^2 after zero-mode/gauge branch is fixed | MISSING_DOMAIN_SPECTRUM_OR_ZERO_MODE_SELECTOR | needed unless mass-only gap controls zero mode | source fixed collar geometry or prove zero-mode is removed by boundary/gauge condition |
| LC4311_2_M2min | M2_min | lower Hessian/memory mass curvature in the m direction | M_m^2 >= M2_min | MISSING_SOURCE_VALUE_OR_THEOREM | needed for mass-only and mixed positive gaps | derive from parent potential Hessian or source an empirical/theorem lower bound |
| LC4311_3_EtaH | Eta_H | absolute negative correction from hidden/source/boundary/operator terms | \|negative correction\| <= Eta_H\|\|u\|\|^2 | MISSING_CORRECTION_BOUND | must be smaller than the positive kinetic+mass margin | bound EM/Poynting, non-Hilbert and boundary corrections separately |
| LC4311_4_lambda_star | lambda_* | positive lower floor used by 4310 trace-defect bound | lambda_* = Z_min lambda_1(D_loc)+M2_min-Eta_H | FORMULA_DERIVED_VALUE_UNSOURCED | turns A_U into residual/lambda bound | only score after every component row is parent-owned and positive-margin checked |
| LC4311_5_zero_mode_mass_branch | lambda_*_mass | zero-mode-safe floor if Poincare gap is unavailable | lambda_*_mass = M2_min-Eta_H | ALTERNATE_ROUTE_FORMULA_READY_VALUE_UNSOURCED | avoids depending on lambda_1 if M2_min dominates | try this if collar boundary conditions leave a constant mode |

## Positivity Route Audit
| route_id | route | conditions | result | status | implication |
| --- | --- | --- | --- | --- | --- |
| PR4311_0_poincare_dirichlet | Poincare/Dirichlet collar gap | Z_min > 0, lambda_1(D_loc) > 0, and Eta_H < Z_min lambda_1(D_loc)+M2_min | lambda_* = Z_min lambda_1(D_loc)+M2_min-Eta_H > 0 | VALID_THEOREM_ROUTE_IF_COMPONENTS_SIGNED | not live because all component values/theorems are unsourced |
| PR4311_1_mass_only | mass-only zero-mode gap | M2_min > Eta_H | lambda_* >= M2_min-Eta_H > 0 even if lambda_1(D_loc)=0 | VALID_THEOREM_ROUTE_IF_COMPONENTS_SIGNED | best route if local collar has Neumann/constant zero mode |
| PR4311_2_mixed_margin | mixed kinetic plus memory margin | margin := Z_min lambda_1(D_loc)+M2_min-Eta_H, margin >= lambda_floor_candidate > 0 | use lambda_floor_candidate in 4310 reduced trace bound | VALID_THEOREM_ROUTE_IF_MARGIN_SOURCED | turns qualitative positivity into an auditable numeric/theorem row |
| PR4311_3_failure | negative or unsourced correction dominance | Eta_H >= Z_min lambda_1(D_loc)+M2_min or any component is placeholder | no lambda floor; only unscored residual ledger survives | CLAIM_BLOCKED | do not proceed to local-GR/R10/PPN scoring |

## Collar Residual First Bound
| bound_id | symbol | law | role | status | next_action |
| --- | --- | --- | --- | --- | --- |
| RB4311_0_sum | S_U | S_U := R_U + N_N + N_boundary | collar forcing numerator entering A_U | FORMULA_READY_VALUES_MISSING | source each part; do not collapse physical boundary flux into a single fudge factor |
| RB4311_1_AU | A_U | A_U <= C_col S_U / lambda_* | collar amplitude bound from 4310 once lambda_* > 0 | GUARDED_BOUND_READY | requires positive lambda_floor_candidate before numerical use |
| RB4311_2_Ninner | N_inner | N_inner <= C_N[K_U C_col S_U/lambda_* + R_U] + \|\|B_src^A\|\| | first reduced trace-defect bound | GUARDED_BOUND_READY_VALUES_MISSING | score only after lambda_*, C_N, K_U, C_col, R_U, S_U and B_src^A are sourced |
| RB4311_3_budget | lambda_required | lambda_* >= C_N K_U C_col S_U/(B_inner - C_N R_U - \|\|B_src^A\|\|) if denominator > 0 | minimum lambda floor needed for a chosen trace-defect budget | DERIVED_REQUIREMENT_NO_NUMERIC_BUDGET | use once a local precision budget B_inner is selected |
| RB4311_4_residual_split | S_U decomposition | S_U <= R_visible + R_EM_Poynting + R_transition + R_boundary + R_nonHilbert + R_N | honest place to test Poynting/wave/source terms | DECOMPOSITION_READY_VALUES_MISSING | next step can attack EM/Poynting cancellation or source each residual row |
| RB4311_5_zero_case | mu_tr | lambda_* > 0 and S_U,R_U,B_src^A -> 0 imply A_U->0, N_inner->0 and mu_tr=0 | exact zero law conditional on signed inputs | CONDITIONAL_ZERO_NOT_LIVE | this is the local vacuum plateau route without smuggling a plateau axiom |

## Runner
| runner_id | case | result | reason | next_action |
| --- | --- | --- | --- | --- |
| RUN4311_0_live_corpus | current corpus rows | BLOCK_CLAIM | lambda formula is derived but Z_min, M2_min, lambda_1(D_loc), Eta_H and residual numerator are unsourced | keep reduced bound as nonclaim scaffold |
| RUN4311_1_component_signed | all lambda components source-signed with positive margin | ALLOW_LAMBDA_FLOOR_CONDITIONAL | lambda_floor_candidate can replace lambda_* in the 4310 trace-bound formula | then source residual numerator and constants before local arena scoring |
| RUN4311_2_residual_zero | lambda floor positive and S_U,R_U,B_src^A theorem-zero | ALLOW_MU_TR_ZERO_CONDITIONAL | A_U,N_inner,mu_tr vanish on the fixed-collar branch | still must pass R_eq, I_commutator, EM/rest and projection gates for local GR |
| RUN4311_3_poynting_open | Poynting/wave flux not proven Hilbert-owned/cancelled in collar | KEEP_RESIDUAL | R_EM_Poynting contributes to S_U or boundary residual rather than disappearing | attack Poynting owner/cancellation next if lambda components stay unsourced |
| RUN4311_4_precision | attempt to score WEP/PPN/R10 with placeholder lambda/residual rows | REJECT | order-one local leakage fails precision and no claim-valid source rows exist | no local test pass from 4311 |

## Claim Firewall
| firewall_id | rule | status |
| --- | --- | --- |
| FW4311_0 | Do not claim lambda_*>0 merely because the formula has positive-looking terms. | ACTIVE |
| FW4311_1 | Do not use a Poincare gap unless the collar domain and zero-mode/boundary condition are fixed. | ACTIVE |
| FW4311_2 | Do not use the mass-only branch unless M2_min and Eta_H are parent-signed in the same normalization. | ACTIVE |
| FW4311_3 | Do not set EM/Poynting residuals to zero unless they are Hilbert-owned or boundary-cancelled in the collar. | ACTIVE |
| FW4311_4 | Do not score local GR/Newton/R10/PPN until lambda, residual, source-equality, commutator and projection gates are all closed. | ACTIVE |

## Decision
| decision_id | result | reason | next_action |
| --- | --- | --- | --- |
| DEC4311_0_derivation | LAMBDA_POSITIVITY_LAW_DERIVED | lambda_* = Z_min lambda_1(D_loc)+M2_min-Eta_H follows from the coercive m-lock form plus the collar Poincare/eigenvalue relation. | turn the abstract missing lambda into four concrete source rows |
| DEC4311_1_routes | THREE_CLOSURE_ROUTES_IDENTIFIED | Poincare/Dirichlet, mass-only zero-mode, and mixed margin branches are the only honest positivity routes currently available. | try mass-only if the collar has a zero mode; otherwise source domain spectrum |
| DEC4311_2_bound | FIRST_COLLAR_RESIDUAL_BOUND_STAGED | The reduced N_inner bound and required-lambda budget are now explicit. | future numeric local tests can use the formula only after sourced rows exist |
| DEC4311_3_poynting | POYNTING_IS_NEXT_REAL_RESIDUAL_TARGET_IF_LAMBDA_STALLS | EM/wave flow is not dismissed; it belongs in R_EM_Poynting or boundary flux until Hilbert ownership/cancellation is proven. | 4312-Y5-R2FR-Zmin-M2min-EtaH-source-or-Poynting-residual-cancellation.md |
| DEC4311_4_claim | NO_LOCAL_CLAIM | This checkpoint improves the derivation ladder but does not close local GR/Newton/R10/PPN. | keep all claim flags false |

## Status
| status_id | item | status | note |
| --- | --- | --- | --- |
| STAT4311_0_lambda_formula | lambda_* formula | DERIVED | exact positivity law is now explicit |
| STAT4311_1_components | Z_min/M2_min/lambda_1/Eta_H | UNSOURCED | no live parent-owned numeric/theorem rows yet |
| STAT4311_2_zero_route | mu_tr zero | CONDITIONAL_ONLY | valid if lambda positive and residual numerator vanishes |
| STAT4311_3_residual_bound | N_inner bound | STAGED | ready as guarded formula, not score-ready |
| STAT4311_4_poynting | EM/Poynting/wave flow | OPEN_RESIDUAL_TARGET | must be owned/cancelled or bounded |
| STAT4311_5_local_GR | local GR/Newton | BLOCKED | stronger ladder, but not a pass |

## Next Target
| next_target_id | next_target | target_question | preferred_route | fallback_route |
| --- | --- | --- | --- | --- |
| NT4311_0 | 4312-Y5-R2FR-Zmin-M2min-EtaH-source-or-Poynting-residual-cancellation.md | Can Z_min/M2_min/Eta_H be parent-signed, or can the Poynting/EM residual be cancelled or bounded in the collar? | source/derive the lambda components in one normalization and prove a positive margin | attack R_EM_Poynting and boundary flux as explicit collar residual terms instead of hiding them |
