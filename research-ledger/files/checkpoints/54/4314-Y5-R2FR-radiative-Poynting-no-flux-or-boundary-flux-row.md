# 4314 - radiative Poynting no-flux or boundary-flux row

## Verdict
- Derived separate power and energy rows: `P_rad_EM=int_partialW S dot n dA` and `E_rad_EM=int P_rad_EM d tau`.
- Fixed the dimensionless leakage normalization: `|E_rad_EM|/(M_H c^2)` or `|P_rad_EM|/(M_H c^2/DeltaTau)`.
- Closed-collar branch: pointwise no-through EM flux gives `Delta_rad_Poynting=0`.
- Open-radiation branch: flux feeds `N_boundary`, `R_EM_Poynting`, `Eta_H`, and `S_U`; it is not erased.
- No local-GR/Newton/R10/PPN claim fires.

## Source Register
| source_id | source_path | exists | needle_found | purpose |
| --- | --- | --- | --- | --- |
| SRC4314_00_4313_next | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4313_NEXT_TARGET.csv | True | True | 4313 handoff selecting radiative Poynting no-flux or boundary-flux row. |
| SRC4314_01_4313_defect | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4313_DEFECT_REDUCTION.csv | True | True | 4313 leaves radiative Poynting as the next EM frontier. |
| SRC4314_02_4312_bound | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4312_COLLAR_EM_RESIDUAL_BOUND.csv | True | True | 4312 bound where Phi_rad feeds R_EM_Poynting and Eta_H. |
| SRC4314_03_279_formal | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\279-PPC4161-Dq-EM-closed-collar-adoption-or-radiative-boundary-row.md | True | True | 4263 formal closed-collar theorem and radiative fallback. |
| SRC4314_04_4263_theorem | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4263_CLOSED_COLLAR_THEOREM.csv | True | True | closed-collar no-radiation clause. |
| SRC4314_05_4263_boundary | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4263_BOUNDARY_FLUX_ORIENTATION_ROWS.csv | True | True | 4263 boundary-flux normalization row. |
| SRC4314_06_192_noflux | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\192-PPC4161-local-boundary-no-flux-sector-interface-theorem.md | True | True | local no-flux theorem: radiation routes as boundary charge if nonzero. |
| SRC4314_07_191_guard | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\191-PPC4161-Maxwell-Hodge-Poynting-stress-owner-theorem.md | True | True | Maxwell-Hodge Poynting stress owner and radiative boundary guard. |
| SRC4314_08_4311_SU | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\327-PPC4161-lambda-floor-source-row-or-collar-residual-first-bound.md | True | True | 4311 residual numerator receiving boundary flux. |
| SRC4314_09_309_precision | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\309-PPC4161-epsilon-mu-tr-shared-local-bound-runner-WEP-R10-PPN-clocks-orbital.md | True | True | local precision guard forbidding unbounded boundary flux leakage. |
| SRC4314_10_newton_guard | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1714-Y5-R2FR-Y5-worldtube-Hilbert-source-equality-or-Req-Icommutator-fill.md | True | True | source-to-Newton equality gate remains open. |

## Radiative No-Flux Theorem
| theorem_id | clause | statement | result | status |
| --- | --- | --- | --- | --- |
| NF4314_0_poynting_owner | Poynting owner | S_i=-T_EM(n,e_i) in the Maxwell-Hodge Hilbert branch | Poynting is real Hilbert EM flux, not an extra source | IMPORTED_EXACT_IDENTITY |
| NF4314_1_power_definition | instantaneous boundary power | P_rad_EM(tau) := int_partialW S_Poynting dot n dA | power crossing the local collar at time tau | DEFINITION_DERIVED |
| NF4314_2_energy_definition | integrated radiated energy | E_rad_EM[DeltaTau] := int_tau0^tau1 P_rad_EM(tau) d tau | energy leakage over the local test window | DEFINITION_DERIVED |
| NF4314_3_closed_collar_zero | closed/static collar zero | P_rad_EM(tau)=0 pointwise on the local test window plus fixed orientation/outward normal | Delta_rad_Poynting=0 and Phi_rad=0 | EXACT_ZERO_IF_BRANCH_SIGNED |
| NF4314_4_average_zero_limit | average-only zero | E_rad_EM[DeltaTau]=0 but P_rad_EM(tau) not pointwise zero | safe only for window-averaged source charge, not instantaneous clock/PPN claims | LIMITED_ZERO_AVERAGE_BRANCH |
| NF4314_5_open_flux | open radiative branch | P_rad_EM or E_rad_EM nonzero | route to N_boundary/Hamiltonian flux, not hidden bulk source | BOUNDARY_BOUND_REQUIRED |

## Dimensional Normalization
| norm_id | symbol | definition | quantity_type | units | role |
| --- | --- | --- | --- | --- | --- |
| DN4314_0_Prad | P_rad_EM | int_partialW S_Poynting dot n dA | power | W or energy/time | instantaneous radiative crossing of the collar |
| DN4314_1_Erad | E_rad_EM | int_DeltaTau P_rad_EM d tau | energy | J or mass*length^2/time^2 | window-integrated radiative leakage |
| DN4314_2_epsilon_energy | epsilon_rad_EM_energy | \|E_rad_EM\|/(M_H c^2) | dimensionless | 1 | fractional source-energy leakage over the window |
| DN4314_3_epsilon_power | epsilon_rad_EM_power | \|P_rad_EM\|/(M_H c^2/DeltaTau) | dimensionless | 1 | constant-power or pointwise power-budget version |
| DN4314_4_Phi_rad | Phi_rad | use as E_rad_EM for integrated-energy rows, or P_rad_EM only when explicitly tagged as power | tagged energy_or_power | must declare | prevents the 4263 Phi symbol from mixing dimensions |

## Boundary Flux Bound Row
| bound_id | symbol | condition_or_law | value_or_bound | feeds | status | next_action |
| --- | --- | --- | --- | --- | --- | --- |
| BF4314_0_zero | Delta_rad_Poynting | P_rad_EM(tau)=0 pointwise on closed collar | 0 | removes radiative EM boundary term from R_EM_Poynting | CONDITIONAL_ZERO_NOT_LIVE_GLOBALLY | prove closed-collar no-flux or fill sourced P_rad/E_rad values for the chosen test window |
| BF4314_1_energy_bound | epsilon_rad_EM_energy | \|int_DeltaTau int_partialW S dot n dA d tau\|/(M_H c^2) | missing numeric/source row | feeds N_boundary and source-energy leakage | BOUND_FORMULA_READY_VALUES_MISSING | prove closed-collar no-flux or fill sourced P_rad/E_rad values for the chosen test window |
| BF4314_2_power_bound | epsilon_rad_EM_power | \|int_partialW S dot n dA\|/(M_H c^2/DeltaTau) | missing numeric/source row | feeds instantaneous local clock/PPN power-budget checks | BOUND_FORMULA_READY_VALUES_MISSING | prove closed-collar no-flux or fill sourced P_rad/E_rad values for the chosen test window |
| BF4314_3_R_EM_update | R_EM_Poynting | R_EM_Poynting <= R_EM_noRad + \|E_rad_EM\| or source-normalized C_rad epsilon_rad_EM | guarded update | 4312 EM residual with radiative term explicit | FORMULA_READY_VALUES_MISSING | prove closed-collar no-flux or fill sourced P_rad/E_rad values for the chosen test window |
| BF4314_4_EtaH_update | Eta_H | Eta_H >= Eta_H_noRad + C_rad epsilon_rad_EM | guarded update | lambda floor weakens if radiative boundary flux survives | FORMULA_READY_VALUES_MISSING | prove closed-collar no-flux or fill sourced P_rad/E_rad values for the chosen test window |
| BF4314_5_SU_update | S_U | S_U <= S_U_noRad + N_boundary_rad_EM | guarded update | collar residual numerator receives open EM radiation only through boundary row | FORMULA_READY_VALUES_MISSING | prove closed-collar no-flux or fill sourced P_rad/E_rad values for the chosen test window |

## Runner
| runner_id | case | result | reason | next_action |
| --- | --- | --- | --- | --- |
| RUN4314_0_current_corpus | current corpus | CONDITIONAL_ZERO_OR_BOUND | 4263 provides a closed-collar zero branch, but open radiation remains a retained finite boundary bound | do not claim local tests from missing flux values |
| RUN4314_1_static_closed | static/quasi-static closed collar with pointwise P_rad_EM=0 | ALLOW_DELTA_RAD_ZERO_CONDITIONAL | radiative EM does not feed R_EM_Poynting, Eta_H or S_U in that branch | still requires Hodge/constitutive and lambda/source-equality gates |
| RUN4314_2_average_zero | window-integrated E_rad_EM=0 but nonzero instantaneous power | ALLOW_AVERAGE_ONLY | safe for averaged source charge only; not enough for instantaneous clock/PPN residuals | keep power row for time-local observables |
| RUN4314_3_open_radiation | nonzero P_rad_EM or E_rad_EM | ROUTE_TO_BOUNDARY | radiation contributes to N_boundary and Hamiltonian/source flux, not hidden bulk m-source | fill energy/power bound row |
| RUN4314_4_local_claim | claim local GR/Newton/R10/PPN now | REJECT | lambda components, Hodge/constitutive defects, source equality, I_commutator and projection gates remain open | continue derivation chain |

## Claim Firewall
| firewall_id | rule | status |
| --- | --- | --- |
| FW4314_0 | Do not erase nonzero EM radiation; route it as boundary/Hamiltonian flux. | ACTIVE |
| FW4314_1 | Do not use a time-averaged zero flux row for instantaneous clock or PPN claims. | ACTIVE |
| FW4314_2 | Do not mix power and energy dimensions under the same Phi_rad symbol without an explicit tag. | ACTIVE |
| FW4314_3 | Do not count Poynting both as Hilbert EM stress and as a standalone bulk source. | ACTIVE |
| FW4314_4 | Do not claim local GR/Newton/R10/PPN from the radiative flux gate alone. | ACTIVE |

## Decision
| decision_id | result | reason | next_action |
| --- | --- | --- | --- |
| DEC4314_0_dimension | PHI_RAD_DIMENSIONS_FIXED | The radiative row now separates boundary power P_rad_EM from integrated energy E_rad_EM. | use energy normalization for window leakage and power normalization for instantaneous checks |
| DEC4314_1_zero | NO_FLUX_ZERO_IS_BRANCH_CONDITIONAL | Pointwise no-through EM flux on a closed static/quasi-static collar can set Delta_rad_Poynting=0. | do not apply to open radiative systems |
| DEC4314_2_bound | OPEN_RADIATION_IS_BOUNDARY_FLUX | Nonzero Poynting flux is physical boundary/Hamiltonian flux and feeds N_boundary, Eta_H and S_U. | fill sourced flux values before scoring local arenas |
| DEC4314_3_frontier | HODGE_CONSTITUTIVE_OWNER_NEXT | After current and radiation are structured, the remaining EM defect with teeth is Delta_Hodge_EM/constitutive ownership. | 4315-Y5-R2FR-Hodge-constitutive-owner-zero-or-DeltaHodge-bound.md |
| DEC4314_4_claim | NO_LOCAL_CLAIM | This closes or bounds one EM boundary channel but not the full local-GR/Newton reduction. | keep all claim flags false |

## Status
| status_id | item | status | note |
| --- | --- | --- | --- |
| STAT4314_0_Prad | P_rad_EM | DEFINED | instantaneous boundary power through the collar |
| STAT4314_1_Erad | E_rad_EM | DEFINED | integrated radiative energy over the test window |
| STAT4314_2_zero | Delta_rad_Poynting | ZERO_OR_BOUND | zero only for closed pointwise no-flux branch |
| STAT4314_3_boundary | N_boundary_rad_EM | EXPLICIT | open radiation feeds boundary flux, not hidden bulk source |
| STAT4314_4_Hodge | Delta_Hodge_EM | NEXT_OPEN_GATE | constitutive/Hodge owner still needs closure or bound |
| STAT4314_5_local | local GR/Newton | BLOCKED | source coupling sharper, full local reduction still open |

## Next Target
| next_target_id | next_target | target_question | preferred_route | fallback_route |
| --- | --- | --- | --- | --- |
| NT4314_0 | 4315-Y5-R2FR-Hodge-constitutive-owner-zero-or-DeltaHodge-bound.md | Can the observed Hodge/constitutive relation be parent-owned, or must Delta_Hodge_EM be bounded as the next EM residual? | derive same-Hodge constitutive ownership on the calibrated visible local branch | fill nonclaim Delta_Hodge_EM bound rows feeding R_EM_Poynting, Eta_H and local precision gates |
