# 4305 - source-power amplitude or inner-charge bound runner

## Verdict
- Imported the 4280 standard-branch result `A_src=0`, so the 4304 source-support term collapses to `N_src,strong_standard=0`.
- Split `N_inner` into a true smooth no-excision zero identity versus the still-open exterior/excision `C_inner |Q_m^H|` branch.
- Reduced `N_EM` to selector zero or an explicit residual envelope; imported the `|delta_J| <= 7.035851579866459e-13` smoke scale as nonclaim only.
- Updated the runner: standard branch now has `N_pair <= N_inner + N_EM + N_rest`, so the next serious target is the inner-domain certificate.

## Source Register
| source_id | source_path | exists | needle_found | purpose |
| --- | --- | --- | --- | --- |
| SRC4305_00_4304_formal | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\320-PPC4161-first-source-norms-or-visible-Hilbert-m-lock-signature.md | True | True | 4304 handoff to A_src, inner charge and N_EM reduction. |
| SRC4305_01_4304_norms | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4304_FIRST_NORM_VALUE_ROWS.csv | True | True | N_src strong source-support anchor. |
| SRC4305_02_4280_AJ | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4280_AJ_COEFFICIENT_REDUCTION.csv | True | True | conditional A_src zero from Dq/Hperp closure. |
| SRC4305_03_4280_Hperp | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4280_HPERP_ZERO_IMPORT.csv | True | True | Hperp=0 import inside standard Dq-closed branch. |
| SRC4305_04_4280_routing | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4280_M2_TRANSPORT_BGRAD_ROUTING_GATE.csv | True | True | remaining AJ transport/B-gradient residuals. |
| SRC4305_05_1538_inner | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_1538_N_INNER_THEOREM_OR_BOUND.csv | True | True | inner compact-source bound row. |
| SRC4305_06_319_boundary | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\319-PPC4161-source-boundary-silence-or-component-norms-for-m-lock.md | True | True | 4303 inner charge and boundary route. |
| SRC4305_07_4207_poynting | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4207_POYNTING_OWNER_CHAIN.csv | True | True | Poynting is Hilbert EM stress, not a second source. |
| SRC4305_08_4208_hodge | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4208_HODGE_ZERO_CONTRACT.csv | True | True | Hodge deformation zero requires visible EM action-domain exclusion. |
| SRC4305_09_4209_owner | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4209_OWNER_CONTRACT.csv | True | True | calibrated visible EM import branch. |
| SRC4305_10_4218_EM | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4218_VISIBLE_EM_THEOREM.csv | True | True | conditional visible EM residual zero theorem. |
| SRC4305_11_4218_EM_residuals | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4218_VISIBLE_EM_RESIDUAL_COMPONENTS.csv | True | True | visible EM residual component envelope. |
| SRC4305_12_3124_deltaJ | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3124_DELTAJ_BRANCH_SELECTION_OUTPUT.csv | True | True | strict default live delta_J branch. |
| SRC4305_13_3127_deltaJ_bound | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3127_HILBERT_EM_WEIGHT_MEASURE_OUTPUT.csv | True | True | one-channel delta_J smoke envelope from Hilbert EM weight measure. |

## A_src Closure Import
| row_id | formula | value_numeric | source_basis | status | note |
| --- | --- | --- | --- | --- | --- |
| ASRC4305_0_4304_start | N_src,strong <= U_B^2 A_src | 1.4413864308717837e-13 | 4304 source-power anchor | STARTING_ANCHOR | A_src missing in 4304. |
| ASRC4305_1_source_split | A_src = \|S_A H_L^A\| scale; S_A H_L^A = S_A H_perp^A after q-basic source orthogonality |  | 4237/4239/4280 | SOURCE_COEFFICIENT_REDUCED | q-basic source piece is not the obstruction. |
| ASRC4305_2_standard_zero | all Dq_i[H_L]=0 => Hperp=0 => S_A Hperp^A=0 => A_src=0 | 0 | 4280 AJR4280_4_A_src_zero and HPZ4280_8_conclusion | CONDITIONAL_STANDARD_BRANCH_ZERO | This is the real closure lever imported into the 4305 N_pair runner. |
| ASRC4305_3_Nsrc_standard | N_src,strong_standard <= U_B^2 * 0 = 0 | 0 | 4304 plus 4280 | N_SRC_STANDARD_BRANCH_ZERO | Only for the standard Dq/Hperp-closed branch; transition or non-Hilbert branches do not inherit it. |
| ASRC4305_4_general_fallback | N_src,general <= U_B^2 A_src_general |  | 4304 fallback | GENERAL_BRANCH_STILL_NEEDS_A_SRC | If Dq/Hperp closure is not admitted, A_src remains a source/profile input. |

## Inner Domain Split
| row_id | formula | status | source_basis | note |
| --- | --- | --- | --- | --- |
| IN4305_0_definition | N_inner = \|\|B_inner\|\|_{boundary-dual} | DEFINITION | 1538 | Exact boundary norm; no cancellation with N_src or EM residuals. |
| IN4305_1_smooth_no_excision_zero | if partial D_inner is empty in the chosen smooth-source local domain, B_inner=0 and N_inner=0 | EXACT_DOMAIN_IDENTITY_CONDITIONAL | new domain split using 1538 boundary definition | Legitimate for a smooth-source/no-excision branch only; not valid for point/excision exterior domains. |
| IN4305_2_Hilbert_no_memory_charge | if compact matter has no independent m-charge and all source variation is Hilbert/q-owned, Q_m^H=0 and N_inner=0 | EXACT_ZERO_ROUTE_UNSIGNED | 4303/1538 visible source silence route | Still needs parent source-charge theorem; cannot be assumed from exterior vacuum language. |
| IN4305_3_no_flux_zero | if parent local domain signs no inner memory flux, B_inner=0 and N_inner=0 | BOUNDARY_CERTIFICATE_REQUIRED | 1538 no-flux route | Blocked for excision domains until boundary/zero-mode certificate is signed. |
| IN4305_4_finite_bound | N_inner <= C_inner \|Q_m^H\| | FORMULA_ONLY_INPUTS_MISSING | 1538 finite bound | Needs C_inner, Q_m^H, boundary-dual norm and excision/domain convention. |
| IN4305_5_decision | standard source branch can set N_src=0, so N_inner is now the first hard source-pair blocker | NEXT_PROOF_TARGET | 4305 reduction | Attack the domain certificate or source Q_m^H/C_inner next. |

## N_EM Reduction
| row_id | formula | value_numeric | source_basis | status | note |
| --- | --- | --- | --- | --- | --- |
| NEM4305_0_selector_zero | N_EM=0 if EM action is the same Maxwell-Hodge Hilbert action, Hodge/current/normalization are q-owned or calibrated constants, and unresolved collar Poynting flux is absent/routed |  | 191/4207/4208/4209/4218 | CONDITIONAL_SELECTOR_ZERO | Poynting is T_EM flux; not a second force in the m-lock source. |
| NEM4305_1_residual_envelope | N_EM <= \|delta_w_EM\| \|\|T_EM\|\| + \|C_XF2 projection_XF2\| + \|C_JQ projection_JQ\| + \|b_alpha sensitivity_alpha\| + \|\|Delta_Hodge_EM\|\| + \|Phi_EM_rad\| + \|Delta_exchange\| |  | 4218 residual components plus 4208/4209 | BOUND_ENVELOPE_READY_VALUES_MISSING | Absolute no-cancellation EM residual envelope. |
| NEM4305_2_deltaJ_smoke | \|delta_J\| <= 7.035851579866459e-13 in the one-channel material Coulomb smoke envelope | 7.035851579866459e-13 | 3127 WGT3127_2 | FINITE_SMOKE_BOUND_NONCLAIM | Useful scale only; not full N_EM and not claim-grade source-GM evidence. |
| NEM4305_3_hodge_zero | Delta_Hodge_EM=0 if observed coframe/orientation fixes *_obs and no independent chi_EM/constitutive tensor survives |  | 4208 Hodge zero contract | CONDITIONAL_ZERO_UNSIGNED_ACTION_DOMAIN | Mathematical uniqueness is not enough without parent EM action-domain exclusion. |
| NEM4305_4_poynting_guard | radiative Poynting flux crosses boundary => boundary/Hamiltonian flux row, not hidden static bulk source |  | 4207 and 3127 | ROUTE_OR_BOUND_REQUIRED | Lets the Poynting intuition remain useful without double-counting it. |

## Updated Npair Runner
| runner_id | branch_name | formula | role | status |
| --- | --- | --- | --- | --- |
| RUN4305_0_standard_source | standard Dq/Hperp source branch | N_src=0, so N_pair <= N_inner + N_EM + N_rest | This is the immediate improvement over 4304: A_src no longer blocks the standard branch. | PARTIAL_BRANCH_REDUCTION |
| RUN4305_1_smooth_selector | smooth no-excision plus EM-owner branch | if partial D_inner=empty, N_EM=0, N_rest=0 then N_pair=0 | Exact source-pair closure is now a domain/source certificate problem, not an A_src problem. | EXACT_ROUTE_CONDITIONAL_NOT_CLAIMED |
| RUN4305_2_excision_fallback | compact source exterior/excision branch | N_pair <= C_inner \|Q_m^H\| + N_EM_envelope + N_rest | This is the hard realistic exterior-body branch until Q_m^H or no-flux is derived. | BOUND_ROUTE_READY_INPUTS_MISSING |
| RUN4305_3_general_nonstandard | general non-Hilbert branch | N_pair <= U_B^2 A_src_general + C_inner \|Q_m^H\| + N_EM_envelope + N_rest | Keeps the nonstandard branch honest instead of borrowing standard-branch A_src=0. | GENERAL_FALLBACK |
| RUN4305_4_to_C4302 | m-lock/Gamma handoff | Delta_m <= (N_pair+N_N)/lambda_m; insert into C4302_DVGAMMA_QUAD | 4305 reduces N_pair before the same 4302 quadratic Gamma runner. | HANDOFF_READY_NOT_SCORE_READY |

## Branch Scorecard
| score_id | item | status | note |
| --- | --- | --- | --- |
| SC4305_0_A_src | A_src | CLOSED_CONDITIONAL_STANDARD_BRANCH | 4280 gives A_src=0 if standard Dq/Hperp closure is admitted. |
| SC4305_1_Nsrc | N_src | ZERO_ON_STANDARD_BRANCH | N_src,strong <= U_B^2 A_src collapses to zero on that branch. |
| SC4305_2_NEM | N_EM | ZERO_OR_BOUND_BRANCH | selector zero exists; residual envelope and delta_J smoke bound remain nonclaim fallback. |
| SC4305_3_Ninner | N_inner | MAIN_BLOCKER | smooth no-excision route is exact conditional; excision branch still needs Q_m^H/C_inner. |
| SC4305_4_Npair | N_pair | PARTIALLY_REDUCED | standard branch now N_pair <= N_inner+N_EM+N_rest. |
| SC4305_5_local_GR | local GR/PPN/R10 | NOT_CLAIMED | lambda_m, inner charge/domain, EM residuals, Khat/connection/projection still gate the result. |

## Decision
| decision_id | result | reason | next_action |
| --- | --- | --- | --- |
| DEC4305_0_gain | A_SRC_REMOVED_FROM_STANDARD_BRANCH | 4280's Dq/Hperp result makes A_src=0 in the standard branch, so 4304's U_B^2 A_src source-support anchor collapses to zero there. | Do not keep chasing A_src inside the standard branch; move pressure to N_inner/N_EM/rest. |
| DEC4305_1_EM | NEM_HAS_SELECTOR_ZERO_AND_BOUND_FALLBACK | Maxwell-Hodge/Poynting owner rows allow N_EM=0 only under the visible EM selector; otherwise the residual envelope and delta_J smoke bound are retained. | Use Poynting as Hilbert flux or a boundary flux, never both. |
| DEC4305_2_inner | INNER_CHARGE_IS_NOW_FIRST_SOURCE_PAIR_BLOCKER | For smooth no-excision domains N_inner=0 by boundary identity, but exterior/excision sources still need Q_m^H/C_inner or a no-flux theorem. | 4306 should derive the domain certificate or source Q_m^H/C_inner. |
| DEC4305_3_next | INNER_DOMAIN_CERTIFICATE_OR_QMH_BOUND_NEXT | The shortest route to the local-GR source gate is now proving which local source domain MTS owns. | 4306-Y5-R2FR-inner-domain-certificate-or-QmH-bound.md |

## Claim Firewall
| firewall_id | rule | status |
| --- | --- | --- |
| FW4305_0 | Do not export A_src=0 outside the standard Dq/Hperp-closed branch. | ACTIVE |
| FW4305_1 | Do not use the smooth no-excision N_inner=0 identity for point/excision exterior source domains. | ACTIVE |
| FW4305_2 | Do not promote the one-channel delta_J smoke bound to a full N_EM or local-GR claim. | ACTIVE |
| FW4305_3 | Do not double-count Poynting: Hilbert EM flux when owned, boundary residual when open. | ACTIVE |
| FW4305_4 | Do not score C4302 until N_inner, N_EM/rest, lambda_m and projection constants are all source-backed or theorem-zero. | ACTIVE |

## Status
| status_id | item | status | note |
| --- | --- | --- | --- |
| STAT4305_0_A_src | A_src | CLOSED_CONDITIONAL_STANDARD_BRANCH | not global; transition/non-Hilbert branches still need profiles |
| STAT4305_1_Nsrc | N_src | ZERO_ON_STANDARD_BRANCH | derived by U_B^2 A_src with A_src=0 |
| STAT4305_2_Ninner | N_inner | MAIN_BLOCKER | domain certificate or Q_m^H/C_inner still needed |
| STAT4305_3_NEM | N_EM | SELECTOR_ZERO_OR_BOUND | delta_J smoke bound imported as nonclaim component only |
| STAT4305_4_Npair | N_pair | REDUCED_NOT_CLOSED | standard branch N_pair <= N_inner+N_EM+N_rest |

## Next Target
| next_target_id | next_target | target_question | preferred_route | fallback_route |
| --- | --- | --- | --- | --- |
| NT4305_0 | 4306-Y5-R2FR-inner-domain-certificate-or-QmH-bound.md | Which inner source domain does the parent local branch own: smooth no-excision, no-flux excision, or finite Q_m^H? | derive smooth-source/no-excision or parent no-flux/no-memory-charge certificate so N_inner=0 | source finite C_inner, Q_m^H and boundary-dual convention for N_inner <= C_inner \|Q_m^H\| |
