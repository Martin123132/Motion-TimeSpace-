# 4316 - visible Hilbert source silence integration or nonEM residual budget

## Verdict
- Integrated visible Hilbert no-direct-`m` silence with the refined EM zero-or-bound ladder.
- Conditional reduction: if visible+EM gates close, `N_pair <= N_inner + N_rest_nonEM`.
- Retained fallback: any EM deformation stays in `N_EM_envelope`; no cancellation with non-EM terms.
- Isolated the remaining non-EM budget: `N_inner`, non-Hilbert support, drift/selector, history/transition, boundary/domain, `N_N`, and downstream source-equality/projection gates.
- No local-GR/Newton/R10/PPN claim fires.

## Source Register
| source_id | source_path | exists | needle_found | purpose |
| --- | --- | --- | --- | --- |
| SRC4316_00_4315_next | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4315_NEXT_TARGET.csv | True | True | 4315 handoff selecting visible Hilbert source silence integration. |
| SRC4316_01_4303_silence | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\319-PPC4161-source-boundary-silence-or-component-norms-for-m-lock.md | True | True | 4303 visible Hilbert source-silence theorem. |
| SRC4316_02_4303_nonHilbert | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\319-PPC4161-source-boundary-silence-or-component-norms-for-m-lock.md | True | True | 4303 residual survivor decomposition. |
| SRC4316_03_4305_pair | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\321-PPC4161-source-amplitude-inner-charge-EM-residual-reduction.md | True | True | 4305 source-pair reduced runner. |
| SRC4316_04_4305_NEM | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\321-PPC4161-source-amplitude-inner-charge-EM-residual-reduction.md | True | True | 4305 EM residual envelope before 4312-4315 refinement. |
| SRC4316_05_4312_EM | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\328-PPC4161-Zmin-M2min-EtaH-source-or-Poynting-residual-cancellation.md | True | True | 4312 Poynting/EM residual bound. |
| SRC4316_06_4313_current | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\329-PPC4161-EM-Ward-current-normalization-or-collar-residual-bound-values.md | True | True | 4313 current/Ward exchange zero-or-bound gate. |
| SRC4316_07_4314_radiation | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\330-PPC4161-radiative-Poynting-no-flux-or-boundary-flux-row.md | True | True | 4314 radiative Poynting zero-or-bound gate. |
| SRC4316_08_4315_Hodge | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\331-PPC4161-Hodge-constitutive-owner-zero-or-DeltaHodge-bound.md | True | True | 4315 Hodge/constitutive zero-or-bound gate. |
| SRC4316_09_4311_SU | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\327-PPC4161-lambda-floor-source-row-or-collar-residual-first-bound.md | True | True | 4311 collar residual numerator feeding lambda-floor route. |
| SRC4316_10_4306_inner | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\322-PPC4161-inner-domain-certificate-or-QmH-bound.md | True | True | 4306 inner-domain/source-charge blocker. |
| SRC4316_11_precision | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\309-PPC4161-epsilon-mu-tr-shared-local-bound-runner-WEP-R10-PPN-clocks-orbital.md | True | True | local precision guard for residual budgets. |

## Visible Silence Integration
| row_id | component | premise | result | status |
| --- | --- | --- | --- | --- |
| VI4316_0_action_split | visible Hilbert action split | S_parent = S_lock[m,q] + S_vis[g_obs(q),psi,A,lambda0] + S_boundary | if S_vis has no direct m slot, delta S_vis/delta m=0 | EXACT_CONDITIONAL_THEOREM |
| VI4316_1_matter_zero | ordinary visible matter | S_matter varies through g_obs(q), psi and fixed visible data only | J_visible_matter_to_m=0 on signed branch | CONDITIONAL_ZERO_ROUTE |
| VI4316_2_EM_zero | visible EM/Poynting | same-Hodge, fixed-current, no extra Poynting source, no radiative collar flux and no constitutive residual | N_EM=0 on full EM zero branch | CONDITIONAL_ZERO_ROUTE_REFINED_BY_4312_4315 |
| VI4316_3_boundary_routing | visible boundary/radiative flux | visible flux is Hilbert bookkeeping or routed boundary/Hamiltonian flux, not an m-boundary charge | does not enter hidden bulk source; open flux remains N_boundary | ZERO_OR_BOUND_ROUTE |
| VI4316_4_failure | visible theorem failure | source-only weights, non-Hilbert currents, direct m slot or prevariation readout enter S_parent | visible residual is retained as absolute source norm | BOUND_ROUTE_IF_NOT_SIGNED |

## EM Closure Matrix
| gate_id | symbol | zero_route | fallback | source_checkpoint | status |
| --- | --- | --- | --- | --- | --- |
| EM4316_0_Poynting_once | c_Poynt_extra | zero if Poynting is counted once as Maxwell-Hodge Hilbert stress | standalone Poynting source retained if not | 4312 | ZERO_OR_BOUND_GATE |
| EM4316_1_current | C_JQ/Delta_internal_exchange | zero if same Maxwell/matter current and calibrated q-basic current branch | F deltaJ bound if not | 4313 | ZERO_OR_BOUND_GATE |
| EM4316_2_radiation | Delta_rad_Poynting | zero if closed collar has pointwise no-through EM flux | P_rad/E_rad boundary row if not | 4314 | ZERO_OR_BOUND_GATE |
| EM4316_3_Hodge | Delta_Hodge_EM | zero if same observed Hodge and no independent constitutive terms | no-cancellation constitutive envelope if not | 4315 | ZERO_OR_BOUND_GATE |
| EM4316_4_weights | delta_w_EM/b_alpha/C_XF2 | zero if calibrated visible constants and no hidden F2/source weights | normalization/source-weight residual if not | 4262/4305 | ZERO_OR_BOUND_GATE |

## Non-EM Residual Budget
| budget_id | symbol | meaning | law_or_bound | status | next_action |
| --- | --- | --- | --- | --- | --- |
| NB4316_0_Ninner | N_inner | inner charge/source-domain or excision boundary residual | N_inner <= C_inner \|Q_m^H\| or zero on smooth/no-excision/signed no-inner-charge branch | PRIMARY_LIVE_BLOCKER | parent-sign zero route or fill sourced bound row |
| NB4316_1_Nsrc_nonHilbert | N_src_nonHilbert | source support outside Hilbert/q-kernel branch or U_B projection survives | N_src <= \|\|U_B\|\|_inf \|\|S_cg_nonHilbert\|\| | RETAINED_BOUND_ROW | parent-sign zero route or fill sourced bound row |
| NB4316_2_Ndrift_selector | N_drift_selector | drift in m, L_cg or local selector not fixed/q-basic | N_drift_selector <= N_drift_mL + N_drift_Lcg + N_selector | RETAINED_BOUND_ROW | parent-sign zero route or fill sourced bound row |
| NB4316_3_Nhistory_transition | N_history_transition | history/memory/transition shell membership or causal silence not signed | N_history_transition <= N_history + N_transition + N_mass_current | RETAINED_BOUND_ROW | parent-sign zero route or fill sourced bound row |
| NB4316_4_Nboundary_domain | N_boundary_domain | boundary/domain/zero-mode/outer/history boundary flux survives | N_boundary_domain <= N_no_flux + N_zero_mode + N_outer + N_history_boundary + N_domain | RETAINED_BOUND_ROW | parent-sign zero route or fill sourced bound row |
| NB4316_5_NN | N_N | nonlinear/noise/remainder forcing in collar m-lock equation | must be zero or bounded before lambda-floor scoring | RETAINED_BOUND_ROW | parent-sign zero route or fill sourced bound row |
| NB4316_6_projection_source | projection/source-equality gates | R_eq, I_commutator, projection/tomography and calibration constants remain open | cannot be removed by visible Hilbert silence | DOWNSTREAM_GATE | parent-sign zero route or fill sourced bound row |

## Reduced Formulas
| formula_id | name | formula | role | status |
| --- | --- | --- | --- | --- |
| RF4316_0_full | full source-pair budget | N_pair <= N_inner + N_EM + N_rest_nonEM | 4305 with EM and non-EM split | FORMULA_READY |
| RF4316_1_visible_EM_zero | visible+EM zero branch | if N_visible=0 and N_EM=0 then N_pair <= N_inner + N_rest_nonEM | main reduction achieved by 4316 | CONDITIONAL_REDUCTION |
| RF4316_2_all_source_zero | source-pair zero branch | if N_inner=0 and N_rest_nonEM=0 then N_pair=0 | not live until non-EM rows close | EXACT_ZERO_CONDITIONAL_NOT_LIVE |
| RF4316_3_SU | collar numerator | S_U <= S_U_visible_silent + N_inner + N_EM + N_rest_nonEM + N_N + N_boundary_extra | feeds 4311 lambda-floor trace bound | FORMULA_READY_VALUES_MISSING |
| RF4316_4_lambda | lambda route | N_inner <= C_N[K_U C_col S_U/lambda_* + R_U] + \|\|B_src^A\|\| with S_U now reduced by visible/EM zero branches | same 4311 trace criterion, cleaner numerator | GUARDED_BY_LAMBDA_AND_NONEM_INPUTS |
| RF4316_5_local_claim | local GR/Newton | no claim until lambda_*, non-EM budget, source equality, commutator and projection gates close | claim firewall | BLOCKED |

## Runner
| runner_id | case | result | reason | next_action |
| --- | --- | --- | --- | --- |
| RUN4316_0_current_corpus | current corpus | REDUCED_BUDGET_NOT_CLAIM | visible Hilbert and EM zero routes are branch-clean; non-EM residuals and lambda/source-equality gates remain open | work the non-EM primary blocker next |
| RUN4316_1_standard_visible_EM | calibrated visible branch plus all EM subgates closed | ALLOW_N_VISIBLE_N_EM_ZERO_CONDITIONAL | N_pair reduces to N_inner + N_rest_nonEM | score only after non-EM rows and lambda floor are real |
| RUN4316_2_EM_deformation | any EM subgate survives | KEEP_N_EM_ENVELOPE | N_EM remains an absolute no-cancellation residual envelope | source every surviving EM term before local tests |
| RUN4316_3_nonEM_zero | N_inner and all N_rest_nonEM rows zero | ALLOW_N_PAIR_ZERO_CONDITIONAL | source-pair forcing vanishes before lambda trace scoring | still needs lambda, R_eq, I_commutator and projection gates |
| RUN4316_4_local_claim | claim local GR/Newton/R10/PPN now | REJECT | N_inner/nonEM rows, lambda_* and source-equality/projection gates are not closed | no public or empirical claim from 4316 |

## Claim Firewall
| firewall_id | rule | status |
| --- | --- | --- |
| FW4316_0 | Do not treat visible Hilbert silence as a global source theorem outside the calibrated branch. | ACTIVE |
| FW4316_1 | Do not cancel EM residuals against non-EM residuals or lambda-floor terms. | ACTIVE |
| FW4316_2 | Do not hide non-Hilbert support, inner charge, transition/history or boundary/domain rows inside visible matter. | ACTIVE |
| FW4316_3 | Do not claim N_pair=0 until N_inner and every non-EM residual row is zero or sourced below bound. | ACTIVE |
| FW4316_4 | Do not claim local GR/Newton/R10/PPN until lambda, source-equality, commutator and projection gates close. | ACTIVE |

## Decision
| decision_id | result | reason | next_action |
| --- | --- | --- | --- |
| DEC4316_0_integration | VISIBLE_AND_EM_ZERO_BRANCHES_INTEGRATED | Visible Hilbert source silence and the refined EM gates now combine into N_visible=0 and N_EM=0 conditions. | use only inside the calibrated/same-owner branch |
| DEC4316_1_reduction | SOURCE_BUDGET_REDUCED_TO_NONEM | When the visible+EM branch closes, N_pair <= N_inner + N_rest_nonEM. | attack N_inner/Q_m^H and non-Hilbert residuals next |
| DEC4316_2_firewall | NO_CROSS_CANCELLATION | EM residuals, non-EM residuals and lambda terms are absolute rows; no cancellation credit is allowed. | keep component ledger discipline |
| DEC4316_3_next | NINNER_QMH_NEXT | The sharpest remaining source blocker is inner/domain charge or its bound. | 4317-Y5-R2FR-nonEM-inner-charge-domain-zero-or-QmH-bound-values.md |
| DEC4316_4_claim | NO_LOCAL_CLAIM | This is a major budget reduction, not a complete local-GR/Newton proof. | keep all claim flags false |

## Status
| status_id | item | status | note |
| --- | --- | --- | --- |
| STAT4316_0_visible | N_visible | ZERO_OR_BOUND | zero on visible Hilbert no-direct-m branch |
| STAT4316_1_EM | N_EM | ZERO_OR_BOUND | zero only if 4312-4315 EM gates close |
| STAT4316_2_Npair | N_pair | REDUCED | standard branch now N_inner + N_rest_nonEM |
| STAT4316_3_Ninner | N_inner/Q_m^H | PRIMARY_NEXT_BLOCKER | inner/domain source charge remains live |
| STAT4316_4_lambda | lambda_* and S_U | STILL_GATED | cleaner numerator but missing positive floor/input values |
| STAT4316_5_local | local GR/Newton | BLOCKED | reduction improved but proof remains incomplete |

## Next Target
| next_target_id | next_target | target_question | preferred_route | fallback_route |
| --- | --- | --- | --- | --- |
| NT4316_0 | 4317-Y5-R2FR-nonEM-inner-charge-domain-zero-or-QmH-bound-values.md | Can N_inner be theorem-zeroed by the smooth/domain/Hilbert-charge branch, or must Q_m^H and C_inner be source-bounded? | derive N_inner=0 from smooth no-excision plus no independent m-charge/source-kernel ownership | fill nonclaim C_inner and Q_m^H bound rows with domain convention and units |
