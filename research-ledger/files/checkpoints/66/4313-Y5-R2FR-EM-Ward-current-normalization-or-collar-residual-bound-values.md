# 4313 - EM Ward current normalization or collar residual bound values

## Verdict
- Derived the exact Ward/current cancellation condition: same current in Maxwell and matter variations gives `Delta_internal_exchange=0`.
- Derived the fallback bound: `Delta_Ward = F deltaJ + R_Hodge + R_Q + B_J`.
- Split `deltaJ` into `C_JQ J_Maxwell + deltaJ_perp`, so charge/current drift has a concrete collar bound.
- Preserved the no-fake-alpha rule: `alpha_eff` is controlled by `g_J^2/lambda_A`, but this does not predict numerical `alpha_EM`.
- No local-GR/Newton/R10/PPN claim fires.

## Source Register
| source_id | source_path | exists | needle_found | purpose |
| --- | --- | --- | --- | --- |
| SRC4313_00_4312_next | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4312_NEXT_TARGET.csv | True | True | 4312 handoff selecting EM current/Ward normalization. |
| SRC4313_01_4312_defects | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4312_EM_DEFECT_LEDGER.csv | True | True | 4312 defect row for unmatched matter-EM exchange. |
| SRC4313_02_4312_bound | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4312_COLLAR_EM_RESIDUAL_BOUND.csv | True | True | 4312 EM/Poynting residual bound receiving current/Ward terms. |
| SRC4313_03_191_ward | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\191-PPC4161-Maxwell-Hodge-Poynting-stress-owner-theorem.md | True | True | Maxwell-Hodge stress owner Ward exchange identity. |
| SRC4313_04_4207_owner | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4207_POYNTING_OWNER_CHAIN.csv | True | True | 4207 source-backed owner-chain Ward exchange row. |
| SRC4313_05_225_norm | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\225-PPC4161-Maxwell-normalization-charge-current-owner.md | True | True | Maxwell normalization identity and no fake alpha derivation. |
| SRC4313_06_278_readout | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\278-PPC4161-visible-EM-readout-guard-or-charge-normalization-bound.md | True | True | calibrated q-basic visible-EM branch kills current/readout drift conditionally. |
| SRC4313_07_3508_current | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_EM_current_source_Ward_alpha_source_residual.csv | True | True | current/source Ward alpha-source residual ledger. |
| SRC4313_08_319_silence | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\319-PPC4161-source-boundary-silence-or-component-norms-for-m-lock.md | True | True | visible Hilbert EM current silence in m equation if owner branch is signed. |
| SRC4313_09_309_precision | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\309-PPC4161-epsilon-mu-tr-shared-local-bound-runner-WEP-R10-PPN-clocks-orbital.md | True | True | local precision forbids unbounded current-normalization leakage. |
| SRC4313_10_newton_guard | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1714-Y5-R2FR-Y5-worldtube-Hilbert-source-equality-or-Req-Icommutator-fill.md | True | True | source-to-Newton equality guard remains open. |

## Ward Current Theorem
| theorem_id | clause | statement | result | status |
| --- | --- | --- | --- | --- |
| WT4313_0_parent_action | single matter+EM action | S_vis = S_MH[A,g_obs;lambda_A] + S_matter[psi,A,g_obs;theta_Q] | one variational source owner before readout | CONTRACT_FORM_READY_NOT_GLOBAL_PARENT_SIGNED |
| WT4313_1_maxwell_current | Maxwell current | J_Maxwell^nu := nabla_mu(lambda_A F^{mu nu}) in the same Hodge/normalization | current appearing in div T_EM | DEFINITION_READY |
| WT4313_2_matter_current | matter current | J_matter^nu := (1/sqrt(-g)) delta S_matter / delta A_nu | current appearing in Lorentz force on matter | DEFINITION_READY |
| WT4313_3_exchange_identity | Ward exchange | nabla_mu T_EM^{mu nu} = -F^{nu lambda}J_Maxwell_lambda and nabla_mu T_matter^{mu nu}=+F^{nu lambda}J_matter_lambda | total exchange cancels if J_matter=J_Maxwell | STANDARD_IDENTITY_IMPORTED_CONDITIONALLY |
| WT4313_4_zero_theorem | internal exchange zero | J_matter=J_Maxwell, same Hodge, fixed calibrated charge/current and no boundary current leakage imply Delta_internal_exchange=0 | R_EM_Poynting loses the Ward/current mismatch term | EXACT_ZERO_IF_CLAUSES_PARENT_SIGNED |
| WT4313_5_failure_theorem | mismatch residual | Delta_Ward^nu = F^{nu lambda}(J_matter-J_Maxwell)_lambda + R_Hodge^nu + R_Q^nu + B_J^nu | current mismatch becomes explicit collar residual | BOUND_ROUTE_IF_NOT_SIGNED |

## Current Normalization Contract
| contract_id | item | condition | formula | implication | status |
| --- | --- | --- | --- | --- | --- |
| CN4313_0_alpha_identity | alpha_eff | alpha_eff proportional to g_J^2/lambda_A | b_alpha = 2 D_X ln g_J - D_X ln lambda_A | identity only; not an alpha_EM prediction | EXACT_IDENTITY_NONCLAIM |
| CN4313_1_fixed_visible_branch | calibrated q-basic EM constants | D_X ln g_J=0 and D_X ln lambda_A=0 when g_J, lambda_A, charges and readout labels are fixed before variation | b_alpha=0, C_JQ=0 on this branch | safe calibrated visible local-GR branch | CONDITIONAL_ZERO_ROUTE |
| CN4313_2_current_multiplier | C_JQ | J_matter=(1+C_JQ)J_Maxwell + delta J_perp | current mismatch contribution is F(C_JQ J_Maxwell + delta J_perp) | enters R_EM_Poynting, WEP/source and clock residuals | BOUND_IF_NOT_ZERO |
| CN4313_3_dynamic_EM_branch | dynamic g_J/lambda_A | g_J(Phi), lambda_A(Phi) or charge labels before variation make b_alpha and C_JQ physical | no readout convention may remove the residual | global MTS EM derivation remains open | DEFORMATION_TAX_RETAINED |
| CN4313_4_no_fake_alpha | absolute alpha_EM | classical U(1)/Noether owns conservation and relative labels but not the numerical value of alpha_EM | visible EM may be calibrated; deviations must be bounded | prevents false precision claim | NO_GO_RETAINED |

## Internal Exchange Bound
| bound_id | symbol | premise | bound | role | status | next_action |
| --- | --- | --- | --- | --- | --- | --- |
| EB4313_0_deltaJ | delta J | delta J := J_matter - J_Maxwell | \|\|Delta_Ward\|\|_dual <= \|\|F\|\|_inf \|\|delta J\|\|_dual + \|\|R_Hodge\|\| + \|\|R_Q\|\| + \|\|B_J\|\| | primary internal-exchange bound | FORMULA_READY_VALUES_MISSING | parent-sign the zero route or fill this bound with sourced collar units |
| EB4313_1_CJQ | C_JQ | if delta J = C_JQ J_Maxwell + delta J_perp | \|\|Delta_Ward\|\|_dual <= \|\|F\|\|_inf(\|C_JQ\| \|\|J_Maxwell\|\|_dual + \|\|delta J_perp\|\|_dual)+... | charge/current multiplier bound | FORMULA_READY_VALUES_MISSING | parent-sign the zero route or fill this bound with sourced collar units |
| EB4313_2_balpha | b_alpha | b_alpha = 2D ln g_J - D ln lambda_A | \|b_alpha\| contributes to source normalization/clock/EM residual if dynamic | normalization drift bound | FORMULA_READY_VALUES_MISSING | parent-sign the zero route or fill this bound with sourced collar units |
| EB4313_3_zero | Delta_internal_exchange | same current plus same Hodge plus calibrated constants plus no boundary current leakage | Delta_internal_exchange=0 | exact conditional cancellation | FORMULA_READY_VALUES_MISSING | parent-sign the zero route or fill this bound with sourced collar units |
| EB4313_4_R_EM_update | R_EM_Poynting | substitute the Ward/current mismatch into the 4312 EM residual | R_EM_Poynting <= R_EM_noWard + \|\|F\|\|_inf(\|C_JQ\| \|\|J\|\| + \|\|delta J_perp\|\|) + \|\|R_Q\|\| + \|\|B_J\|\| | feeds 4312 residual bound | FORMULA_READY_VALUES_MISSING | parent-sign the zero route or fill this bound with sourced collar units |
| EB4313_5_EtaH_update | Eta_H | current mismatch contributes to the negative/correction budget in the lambda floor | Eta_H >= Eta_H_noWard + C_Ward[\|\|F\|\|_inf(\|C_JQ\| \|\|J\|\|+\|\|delta J_perp\|\|)+\|\|R_Q\|\|+\|\|B_J\|\|] | weakens lambda_* unless the current gate closes | FORMULA_READY_VALUES_MISSING | parent-sign the zero route or fill this bound with sourced collar units |

## Defect Reduction
| reduction_id | defect | zero_route | fallback | status |
| --- | --- | --- | --- | --- |
| DR4313_0_C_JQ | C_JQ | zero if g_J/charge/current lattice is fixed q-basic before variation | current mismatch bound if not fixed | PARTLY_REDUCED_TO_BRANCH_THEOREM |
| DR4313_1_Delta_internal_exchange | Delta_internal_exchange | zero if J_matter=J_Maxwell and Ward exchange is one-action owned | F deltaJ plus Hodge/charge/boundary terms if not | PARTLY_REDUCED_TO_CURRENT_EQUALITY |
| DR4313_2_delta_w_EM | delta_w_EM | zero on source-label-forgetting Hilbert branch | species/readout weight residual if prevariation source weights exist | RETAINED |
| DR4313_3_Delta_rad_Poynting | Delta_rad_Poynting | not solved by Ward current equality | must route to no-flux/boundary row next | NEXT_FRONTIER |
| DR4313_4_Delta_Hodge_EM | Delta_Hodge_EM | not solved by current equality unless same-Hodge owner also signed | stays in R_Hodge/Eta_H | RETAINED |

## Runner
| runner_id | case | result | reason | next_action |
| --- | --- | --- | --- | --- |
| RUN4313_0_current_corpus | current corpus | BOUND_ROUTE_ONLY | Ward identity exists and current-zero branch is clean, but global parent current equality is not signed for every branch | retain deltaJ/C_JQ/Delta_internal_exchange bound rows |
| RUN4313_1_calibrated_visible | 4210/4262 calibrated q-basic visible EM branch | ALLOW_CJQ_ZERO_CONDITIONAL | fixed charges, g_J, lambda_A and readout labels give C_JQ=0 and b_alpha=0 inside that branch | still needs boundary radiative flux and lambda gates before local tests |
| RUN4313_2_same_action_current | same matter+EM action and same current | ALLOW_DELTA_INTERNAL_EXCHANGE_ZERO_CONDITIONAL | Lorentz force exchange cancels in total Hilbert stress | then R_EM_Poynting can drop Ward/current mismatch term |
| RUN4313_3_dynamic_or_mismatch | dynamic current/coupling or mismatched current | KEEP_RESIDUAL | deltaJ, C_JQ and b_alpha are physical residuals | source numeric bounds before scoring local arenas |
| RUN4313_4_local_claim | claim local GR/Newton/R10/PPN now | REJECT | lambda components, radiative boundary flux, source equality, I_commutator and projection gates remain open | continue source-coupling derivation |

## Claim Firewall
| firewall_id | rule | status |
| --- | --- | --- |
| FW4313_0 | Do not use Ward conservation to prove EM residual absence unless J_matter equals J_Maxwell in one normalization. | ACTIVE |
| FW4313_1 | Do not derive the numerical fine-structure constant from field normalization. | ACTIVE |
| FW4313_2 | Do not move a prevariation current/coupling drift into harmless postvariation readout. | ACTIVE |
| FW4313_3 | Do not set radiative Poynting flux to zero from current equality alone. | ACTIVE |
| FW4313_4 | Do not claim local GR/Newton/R10/PPN from current-owner cancellation alone. | ACTIVE |

## Decision
| decision_id | result | reason | next_action |
| --- | --- | --- | --- |
| DEC4313_0_ward | WARD_EXCHANGE_CAN_CANCEL_EXACTLY | If the same current appears in Maxwell and matter variations, EM/matter Lorentz exchange is internal and Delta_internal_exchange=0. | use the zero route only when current equality is parent-signed |
| DEC4313_1_current | CURRENT_MISMATCH_HAS_A_BOUND | If currents differ, the surviving residual is F deltaJ plus Hodge, charge and boundary terms. | feed the bound into R_EM_Poynting, Eta_H and S_U |
| DEC4313_2_normalization | NO_FAKE_ALPHA_OR_CHARGE_DERIVATION | alpha_eff is g_J^2/lambda_A; calibrated visible EM is allowed, but absolute alpha_EM is not predicted here. | keep dynamic current/coupling deviations as residuals |
| DEC4313_3_frontier | RADIATIVE_BOUNDARY_FLUX_NOW_SHARPEST_EM_GATE | After current equality, the remaining EM gate with teeth is net Poynting flux through the collar. | 4314-Y5-R2FR-radiative-Poynting-no-flux-or-boundary-flux-row.md |
| DEC4313_4_claim | NO_LOCAL_CLAIM | 4313 improves source coupling but does not close the full local-GR reduction. | keep all claim flags false |

## Status
| status_id | item | status | note |
| --- | --- | --- | --- |
| STAT4313_0_Ward | Ward exchange | EXACT_CONDITIONAL | cancels only with same current and same Hodge owner |
| STAT4313_1_CJQ | C_JQ | ZERO_OR_BOUND | zero in calibrated q-basic branch; bound if dynamic/mismatched |
| STAT4313_2_deltaJ | delta J | NEW_BOUND_OBJECT | direct current mismatch norm feeding EM residual |
| STAT4313_3_balpha | b_alpha | IDENTITY_NOT_PREDICTION | no fake alpha derivation |
| STAT4313_4_RadFlux | Delta_rad_Poynting | NEXT_OPEN_GATE | not solved by current equality |
| STAT4313_5_local | local GR/Newton | BLOCKED | source coupling narrowed, full reduction still open |

## Next Target
| next_target_id | next_target | target_question | preferred_route | fallback_route |
| --- | --- | --- | --- | --- |
| NT4313_0 | 4314-Y5-R2FR-radiative-Poynting-no-flux-or-boundary-flux-row.md | Can net radiative Poynting flux through the local collar be zeroed by no-flux/compact support, or must it be bounded as N_boundary? | derive closed-collar/no-through-EM-flux theorem in the same Hilbert owner branch | fill a nonclaim boundary-flux row Phi_rad = int_boundary S_Poynting dot n dA with units and source path |
