# 4310 - collar no-concentration signature or trace-bound inputs

## Verdict
- Derived the collar no-concentration criterion: `A_U` is bounded by residual numerator over `lambda_*`.
- Reduced the 4309 trace formula to named inputs: `lambda_*`, `C_col`, `C_N`, `K_U`, `R_U`, `N_N`, `N_boundary`, and `B_src^A`.
- Current corpus conditionally supports fixed-collar/no-flux and no-direct-`m` source clauses, but does not source a positive `lambda_*` or residual silence.
- No local-GR/Newton claim fires.

## Source Register
| source_id | source_path | exists | needle_found | purpose |
| --- | --- | --- | --- | --- |
| SRC4310_00_4309_doc | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\4309-Y5-R2FR-source-domain-limit-defect-zero-or-first-numeric-flux-bound.md | True | True | 4309 handoff: sign collar no-concentration or source trace-bound inputs. |
| SRC4310_01_4309_formal | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\325-PPC4161-source-domain-limit-defect-zero-or-first-numeric-flux-bound.md | True | True | 4309 first trace-bound formula. |
| SRC4310_02_4302_lambda | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\318-PPC4161-m-lock-coercivity-gap-and-DvGamma-quadratic-input-pack.md | True | True | coercivity gap formula. |
| SRC4310_03_4302_nohair | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\318-PPC4161-m-lock-coercivity-gap-and-DvGamma-quadratic-input-pack.md | True | True | exact m-lock no-hair gate. |
| SRC4310_04_4301_positive | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\317-PPC4161-parent-double-zero-lock-or-second-order-DvGamma-bound-row.md | True | True | parent double-zero lock requires positive operator/source-boundary silence. |
| SRC4310_05_4268_fixed_collar | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\284-PPC4161-Dq-boundary-projector-fixed-collar-or-boundary-residual-bound.md | True | True | fixed collar and q-basic boundary projector precedent. |
| SRC4310_06_4176_noflux | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\192-PPC4161-local-boundary-no-flux-sector-interface-theorem.md | True | True | compact local no-flux/support-separation selector. |
| SRC4310_07_319_visible | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\319-PPC4161-source-boundary-silence-or-component-norms-for-m-lock.md | True | True | visible Hilbert no-direct-m source clause. |
| SRC4310_08_321_npair | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\321-PPC4161-source-amplitude-inner-charge-EM-residual-reduction.md | True | True | source-pair residual entering collar forcing. |
| SRC4310_09_223_poynting | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\223-PPC4161-EM-Poynting-Hodge-source-owner-lock.md | True | True | Poynting is Hilbert EM stress or boundary residual, not hidden source. |
| SRC4310_10_309_precision | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\309-PPC4161-epsilon-mu-tr-shared-local-bound-runner-WEP-R10-PPN-clocks-orbital.md | True | True | local precision demands zero/suppression, not order-one coupling leakage. |
| SRC4310_11_1714_guard | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1714-Y5-R2FR-Y5-worldtube-Hilbert-source-equality-or-Req-Icommutator-fill.md | True | True | source-to-Newton equality remains a separate gate. |

## Collar Signature Audit
| signature_id | clause | evidence_basis | status | signed_now | implication |
| --- | --- | --- | --- | --- | --- |
| SIG4310_0_fixed_collar | fixed q-basic collar/worldtube and boundary projector | 4268 fixed compact no-flux collar branch | CONDITIONAL_BRANCH_SUPPORT | partial | supports domain stability but only inside the compact selector branch |
| SIG4310_1_support_separation | source/sector support does not cross the collar side interfaces | 4176 no-flux/support-separation clauses | CONDITIONAL_NOFLUX_SUPPORT | partial | helps set open-sector collar forcing to zero if parent selector signs it |
| SIG4310_2_visible_no_m_slot | visible Hilbert matter/EM have no direct m-source slot | 319 visible Hilbert theorem | CONDITIONAL_ZERO_ROUTE | partial | removes direct visible forcing only under the signed branch |
| SIG4310_3_EM_Poynting_once | Poynting is counted once as Maxwell-Hodge Hilbert stress or boundary flux | 223 EM/Poynting owner lock | ROUTE_AVAILABLE_NOT_NUMERIC_ZERO | partial | prevents double-counting but does not source the radiative residual value |
| SIG4310_4_lambda_floor | lambda_m >= lambda_* > 0 on the collar branch | 4302 lambda_m formula | MISSING_LOWER_BOUND | no | core missing input for no-concentration theorem |
| SIG4310_5_collar_residual_silence | R_U, N_N and boundary/source residuals vanish or are bounded | 4309 trace-bound numerator | MISSING_RESIDUAL_VALUES_OR_ZERO_THEOREMS | no | without this, A_U remains bounded but not zero |
| SIG4310_6_BsrcA_silence | B_src^A is zero or bounded separately from conormal trace | 4309 firewall | MISSING_REPRESENTATIVE_ZERO_OR_BOUND | no | prevents hiding exterior source injection inside gamma_N |
| SIG4310_7_verdict | collar no-concentration theorem for live exterior branch | all clauses above | CRITERION_DERIVED_NOT_PARENT_SIGNED | no | the theorem form is ready; claim inputs remain missing |

## No-Concentration Criterion
| criterion_id | statement | basis | implication | status |
| --- | --- | --- | --- | --- |
| CRIT4310_0_energy_gap | If lambda_m >= lambda_* > 0 on U_W, then lambda_* \|\|u\|\|_H1(U_W)^2 <= <u,L_m u> + residual_boundary_terms. | 4302 coercive gap restricted to fixed collar | collar amplitude is controlled by forcing, not a free parameter | DERIVED_CONDITIONAL |
| CRIT4310_1_amplitude_bound | A_U <= C_col(R_U + N_N + N_boundary)/lambda_* | energy estimate plus duality | replaces independent A_U with lambda/residual inputs | DERIVED_BOUND_VALUES_MISSING |
| CRIT4310_2_trace_substitution | N_inner <= C_N[(Zbar+Mbar+EtaH_U)C_col(R_U+N_N+N_boundary)/lambda_* + R_U] + \|\|B_src^A\|\| | 4309 conormal trace bound plus amplitude bound | first reduced trace-bound formula | DERIVED_REDUCED_BOUND |
| CRIT4310_3_zero_condition | If lambda_* stays positive and R_U,N_N,N_boundary,B_src^A -> 0, then A_U->0 and mu_tr=0. | coercivity plus conormal trace zero lemma | no-concentration follows from positive operator and residual silence | EXACT_ZERO_IF_INPUTS_SIGNED |
| CRIT4310_4_failure_condition | If lambda_* is missing/nonpositive or residual numerator survives, no-concentration cannot be claimed. | 4302 failure gate plus 4309 trace bound | fallback remains a finite bound, not local GR | BOUND_ROUTE_RETAINED |

## Reduced Trace-Bound Inputs
| input_id | symbol | definition | units | status | value_or_theorem | next_action |
| --- | --- | --- | --- | --- | --- | --- |
| IN4310_0_lambda_floor | lambda_* | positive lower bound for lambda_m on the collar branch | operator spectral gap | MISSING_NUMERIC_OR_THEOREM_LOWER_BOUND |  | derive/source Z_min, lambda_1(D_loc), M2_min and Eta_H with lambda_*>0 |
| IN4310_1_Ccol | C_col | collar coercivity/embedding constant in A_U bound | dimensionless/operator-domain constant | MISSING_ARENA_PROJECTION |  | source fixed collar geometry or normalize theoremically |
| IN4310_2_CN | C_N | weak conormal trace extension constant | trace/operator constant | MISSING_ARENA_PROJECTION |  | source trace extension bound for partialW_H subset U_W |
| IN4310_3_coeff_ceiling | K_U := Zbar+Mbar+EtaH_U | upper bilinear-form coefficient ceiling on U_W | operator norm | MISSING_SOURCE_VALUE_OR_THEOREM |  | source parent m-lock coefficient ceilings |
| IN4310_4_RU | R_U | collar residual \|\|L_m u\|\|_Hminus1(U_W) | Hminus1 norm | MISSING_RESIDUAL_ZERO_OR_BOUND |  | prove source support/no-direct-m silence in collar or source residual value |
| IN4310_5_NN | N_N | nonlinear/noise/remainder forcing in collar m-lock equation | dual norm | MISSING_REMAINDER_BOUND |  | prove higher-order silence or source local smallness bound |
| IN4310_6_Nboundary | N_boundary | open/radiative/corner/domain boundary forcing not included in R_U | boundary dual norm | MISSING_BOUNDARY_RESIDUAL |  | use no-flux theorem only if selector clauses are parent-signed; otherwise source bound |
| IN4310_7_BsrcA | B_src^A | exterior source-boundary representative injection | Hminus1/2 dual norm | MISSING_REPRESENTATIVE_ZERO_OR_BOUND |  | prove representative silence or source bound separately |
| IN4310_8_reduced_bound | N_inner_reduced | C_N[K_U*C_col*(R_U+N_N+N_boundary)/lambda_* + R_U] + \|\|B_src^A\|\| | same norm as N_inner | FORMULA_READY_VALUES_MISSING |  | score only after every component is real or theorem-zero |
| IN4310_9_zero_case | mu_tr | 0 if lambda_*>0 and R_U,N_N,N_boundary,B_src^A -> 0 | trace measure | EXACT_ZERO_CONDITIONAL | 0 conditional | not live until input rows are parent-signed |

## Branch Runner
| runner_id | case | result | reason | next_action |
| --- | --- | --- | --- | --- |
| RUN4310_0_claim_no_concentration_now | claim collar no-concentration/mu_tr=0 now | REJECT | lambda floor, residual numerator and B_src^A zero are not parent-signed | keep exact conditional theorem plus reduced bound |
| RUN4310_1_conditional_zero | all collar signature/input rows theorem-zero or positive | ALLOW_CONDITIONAL | A_U->0, mu_tr=0, B_src^A=0, N_inner=0 | then N_pair reduces to N_EM+N_rest before lambda_m scoring |
| RUN4310_2_current_bound | current evidence with fixed-collar support but missing lambda/residual inputs | USE_REDUCED_BOUND | N_inner <= C_N[K_U*C_col*(R_U+N_N+N_boundary)/lambda_* + R_U]+\|\|B_src^A\|\| | next target should fill lambda floor or first residual row |
| RUN4310_3_precision_guard | allow order-one coupling leakage into local tests | REJECT | 4293 shows order-one projection fails local precision rows | must prove zero or derive strong projection suppression |
| RUN4310_4_local_GR_guard | claim Newton/local-GR from collar theorem | REJECT | R_eq, I_commutator, EM/rest and projection/calibration gates remain open | continue local source-coupling derivation only |

## Local Precision Map
| precision_id | arena | rule | source_basis | status |
| --- | --- | --- | --- | --- |
| PREC4310_0_WEP | WEP/composition | first-order projection of trace/source leakage must be suppressed or theorem-zero | 4293 Y_WEP <= 8.328848673647216e-14 for raw seed-scale leakage | ZERO_OR_SUPPRESSION_REQUIRED |
| PREC4310_1_PPN | PPN gamma/beta | metric readout of trace leakage must not mimic PPN source nonlinearity | 4293 gamma/beta projection bounds | ZERO_OR_SUPPRESSION_REQUIRED |
| PREC4310_2_clock_orbit | clocks/orbital/Gdot | time-varying trace leakage must be static-degenerate or below drift budgets | 4293 clock/orbit/Gdot rows | ZERO_OR_SUPPRESSION_REQUIRED |
| PREC4310_3_R10 | R10/fifth-force | finite-range trace hair must map to alpha(lambda) with source-backed bounds | 4293 R10 diagnostic only, no pass | BOUND_INPUTS_REQUIRED |

## Decision
| decision_id | result | reason | next_action |
| --- | --- | --- | --- |
| DEC4310_0_gain | A_U_NOT_FREE_AFTER_COERCIVITY | The collar amplitude can be replaced by residual/lambda inputs: A_U <= C_col(R_U+N_N+N_boundary)/lambda_*. | Use the reduced trace bound going forward. |
| DEC4310_1_zero | NO_CONCENTRATION_REDUCED_TO_LAMBDA_AND_RESIDUAL_SILENCE | Positive lambda floor plus vanishing residual numerator and B_src^A gives mu_tr=0. | Try to source lambda_* or the first residual row next. |
| DEC4310_2_signature | FIXED_COLLAR_SUPPORT_IS_CONDITIONAL | 4268/4176 support the compact no-flux collar branch, but do not provide numeric lambda or all residual zeros. | Keep branch-conditional status visible. |
| DEC4310_3_precision | ORDER_ONE_LOCAL_LEAKAGE_FORBIDDEN | 4293 says raw order-one local projection fails; this route needs theorem-zero or strong suppression. | Do not score local tests with placeholder leakage. |
| DEC4310_4_next | LAMBDA_FLOOR_OR_FIRST_RESIDUAL_ROW_NEXT | The best next move is to source lambda_* or R_U/B_src^A, not broaden the audit. | 4311-Y5-R2FR-lambda-floor-source-row-or-collar-residual-first-bound.md |

## Claim Firewall
| firewall_id | rule | status |
| --- | --- | --- |
| FW4310_0 | Do not keep A_U as a free fitted amplitude after deriving the coercive A_U bound. | ACTIVE |
| FW4310_1 | Do not claim no-concentration without lambda_* > 0 and residual numerator silence/bounds. | ACTIVE |
| FW4310_2 | Do not treat conditional fixed-collar/no-flux selectors as numeric residual values. | ACTIVE |
| FW4310_3 | Do not hide B_src^A, radiative Poynting or open-sector flux inside R_U. | ACTIVE |
| FW4310_4 | Do not use trace-bound rows as local-GR/Newton evidence while R_eq, I_commutator, EM/rest and projection gates remain open. | ACTIVE |

## Status
| status_id | item | status | note |
| --- | --- | --- | --- |
| STAT4310_0_AU | A_U | REDUCED_NOT_FREE | bounded by residual numerator over lambda_* |
| STAT4310_1_lambda | lambda_* | PRIMARY_MISSING_INPUT | next best source row or theorem |
| STAT4310_2_residuals | R_U/N_N/N_boundary/B_src^A | MISSING_ZERO_OR_BOUND_ROWS | needed for mu_tr zero or score |
| STAT4310_3_mu_tr | mu_tr | EXACT_CONDITIONAL_OR_REDUCED_BOUND | zero if lambda/residual conditions close |
| STAT4310_4_precision | local precision | SUPPRESSION_REQUIRED | 4293 forbids order-one leakage |
| STAT4310_5_local_GR | local GR/Newton | STILL_BLOCKED | source coupling improved, but full GR route remains gated |

## Next Target
| next_target_id | next_target | target_question | preferred_route | fallback_route |
| --- | --- | --- | --- | --- |
| NT4310_0 | 4311-Y5-R2FR-lambda-floor-source-row-or-collar-residual-first-bound.md | Can lambda_* be sourced/derived as positive, or should the first collar residual/boundary row be filled? | derive/source lambda_* = Z_min lambda_1(D_loc)+M2_min-Eta_H > 0 on the fixed collar branch | source R_U, N_N, N_boundary, B_src^A, C_col, C_N and K_U as nonclaim trace-bound inputs |
