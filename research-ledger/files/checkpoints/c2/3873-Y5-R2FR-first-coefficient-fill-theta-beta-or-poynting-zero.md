# 3873 — First Coefficient Fill: Poynting Boundary Zero

Generated: `2026-07-01T06:33:48+00:00`

## Result

3873 closes one finite coupling family conditionally:

`For a closed total-system worldtube W with observed Maxwell stress descended to the same g_obs/coframe, if L_tau fields=0 up to fixed EM gauge, no charge/current or radiation crosses boundary(W), and boundary/reference improvements are silent, then Phi_EM_boundary[W,tau] := int_dt int_boundary(W) S_EM dot n dA = 0. Circulating local Poynting flow may remain inside W; only net leakage through the chosen source boundary is zero.`

This fills the `Phi_EM_boundary` branch for stationary isolated total-system source tubes. It does **not** set local Poynting flow to zero, and it does **not** derive EM, alpha, charge normalization, or the no-extra-F2 rule.

## Source Register

Resolved `15/15` source rows.

| source_id | path | needle_found | role |
| --- | --- | --- | --- |
| SRC3873_00_3872_next | source-intake\mts_residuals\P8_Y5_R2FR_3872_NEXT_TARGET.csv | True | 3872 selected first coefficient fill |
| SRC3873_01_3872_poy | source-intake\mts_residuals\P8_Y5_R2FR_3872_POYNTING_SOURCE_BRIDGE.csv | True | 3872 Poynting zero route |
| SRC3873_02_3872_candidate | source-intake\mts_residuals\P8_Y5_R2FR_3872_FIRST_CANDIDATE_BJ_COEFFICIENT_ROWS.csv | True | 3872 Phi_EM_boundary coefficient row |
| SRC3873_03_3872_arena | source-intake\mts_residuals\P8_Y5_R2FR_3872_ARENA_PROJECTION_CONTRACT.csv | True | 3872 EM/Poynting arena contract |
| SRC3873_04_3579_theorem | source-intake\mts_residuals\P8_Y5_R2FR_3579_PUBLIC_EM_POYNTING_THEOREM.csv | True | public Poynting flux identity |
| SRC3873_05_3579_bounds | source-intake\mts_residuals\P8_Y5_R2FR_3579_POYNTING_FLUX_BOUND_ROWS.csv | True | Poynting flux bound row |
| SRC3873_06_3597_once | source-intake\mts_residuals\P8_Y5_R2FR_3597_EM_POYNTING_ONCE_THEOREM.csv | True | EM/Poynting once-only theorem |
| SRC3873_07_3612_closure | source-intake\mts_residuals\P8_Y5_R2FR_3612_EM_POYNTING_HILBERT_CLOSURE.csv | True | Poynting Hilbert closure rule |
| SRC3873_08_3463_ledger | source-intake\mts_residuals\P8_Y5_R2FR_3463_MAXWELL_POYNTING_STRESS_LEDGER.csv | True | Maxwell/Poynting stress ledger |
| SRC3873_09_3503_theorem | source-intake\mts_residuals\P8_Y5_R2FR_3503_OBSERVED_HODGE_MAXWELL_OWNER_THEOREM.csv | True | total Hilbert current closure |
| SRC3873_10_3503_gate | source-intake\mts_residuals\P8_Y5_R2FR_3503_TOTAL_HILBERT_CURRENT_CLOSURE_GATE.csv | True | stationary flux gate |
| SRC3873_11_3776_domain | source-intake\mts_residuals\P8_Y5_R2FR_3776_EM_POYNTING_DOMAIN_AUDIT.csv | True | EM/Poynting source-domain audit |
| SRC3873_12_3792_pim | source-intake\mts_residuals\P8_Y5_R2FR_3792_PIM_TOTAL_EM_SOURCE_UPDATE.csv | True | Pi_M total EM Hilbert admission |
| SRC3873_13_3863_em | source-intake\mts_residuals\P8_Y5_R2FR_3863_EM_SOURCE_SCALE_BOUND.csv | True | EM source-scale envelope |
| SRC3873_14_3825_boundary | source-intake\mts_residuals\P8_Y5_R2FR_3825_BOUNDARY_REFERENCE_ZERO_THEOREM.csv | True | boundary/Stokes zero theorem |

## Poynting Zero Theorem

| theorem_id | piece | statement_or_formula | status |
| --- | --- | --- | --- |
| PZT3873_0_identity | Poynting theorem | d_t E_EM(W)+int_boundary(W) S_EM·n dA = -int_W J·E dV plus gauge/improvement terms | EXACT_CONDITIONAL_IDENTITY |
| PZT3873_1_total_exchange | matter-EM exchange cancellation | nabla_mu T_EM^{mu nu}=-F^{nu lambda}J_lambda and nabla_mu T_matter^{mu nu}=+F^{nu lambda}J_lambda, so only T_total is conserved | EXACT_CONDITIONAL_TOTAL_CURRENT_RULE |
| PZT3873_2_stationary_zero | stationary boundary flux theorem | For a closed total-system worldtube W with observed Maxwell stress descended to the same g_obs/coframe, if L_tau fields=0 up to fixed EM gauge, no charge/current or radiation crosses boundary(W), and boundary/reference improvements are silent, then Phi_EM_boundary[W,tau] := int_dt int_boundary(W) S_EM dot n dA = 0. Circulating local Poynting flow may remain inside W; only net leakage through the chosen source boundary is zero. | EXACT_CONDITIONAL_ZERO_FOR_PHI_EM_BOUNDARY |
| PZT3873_3_circulation_guard | circulating Poynting is not leakage | S_EM may be nonzero locally in stationary bound systems, but a closed boundary integral can vanish; do not infer S_EM=0 from Phi_EM_boundary=0 | SCOPE_GUARD |
| PZT3873_4_not_EM_origin | not a derivation of EM from flow | The theorem assumes the observed Maxwell/Hodge stress branch; it does not derive *_EM, charge normalization, no-extra-F2, or alpha. | SCOPE_GUARD |

## Clause Audit

| clause_id | required_clause | current_status | failure_residual |
| --- | --- | --- | --- |
| CL3873_0_observed_Hodge | observed Maxwell stress descends to same g_obs/coframe | CONDITIONAL_STANDARD_FORM_NOT_PARENT_DERIVED | Delta_Hodge_EM |
| CL3873_1_total_worldtube | worldtube contains matter plus bound EM field/interactions/apparatus stress | PREFERRED_CONDITIONAL_DOMAIN | epsilon_domain |
| CL3873_2_stationary_generator | L_tau fields=0 up to fixed EM gauge on the local branch | BRANCH_CONDITION_REQUIRED | d_t E_EM |
| CL3873_3_no_crossing_current | no charge/current crosses the selected boundary | BRANCH_CONDITION_REQUIRED | J_cross |
| CL3873_4_no_radiative_leakage | no outgoing/background radiation crosses boundary, or it is explicitly bounded | CONDITIONAL_ZERO_ELSE_BOUND | Phi_EM_rad |
| CL3873_5_boundary_reference | boundary/reference/improvement terms are silent on the annulus | BOUNDARY_THEOREM_CONDITIONAL | C_EM_surface_gauge |
| CL3873_6_same_owner_guard | same current/Hilbert source owner handles matter+EM exchange | OWNER_STILL_UNSIGNED | epsilon_EM_once |

## Coefficient Update

| update_id | quantity | new_formula_or_rule | effect | status |
| --- | --- | --- | --- | --- |
| PCU3873_0_old_row | Phi_EM_boundary | epsilon_Poynting = \|int_dt int_boundary S_EM·n dA\|/(M_ref c^2) | still valid for radiative/nonstationary branches | BOUND_ROUTE_RETAINED |
| PCU3873_1_stationary_zero | Phi_EM_boundary | Phi_EM_boundary[stationary closed total-system W]=0 | removes the explicit boundary leakage term from the stationary isolated EM source envelope | ZERO_CONDITIONAL_BRANCH_FILLED |
| PCU3873_2_updated_envelope | B_EM_scale_stationary | B_EM_scale_stationary <= b_Z+b_J+\|b_alpha\|+\|w_EM\|+\|C_XF2\|+\|C_JQ\|+\|Delta_M_EM_binding\| | w_EM, C_XF2, C_JQ, b_Z, b_J, b_alpha, and Delta_M_EM_binding remain live | REDUCED_ENVELOPE_NONCLAIM |
| PCU3873_3_local_GR_effect | R_source_normalization_total | R_source_total_stationary <= R_source_total_without_Phi_EM_leak + retained EM normalization/current/binding terms | does not prove Newton/PPN/local-GR because source owner and EM normalization remain open | LOCAL_GR_HELPFUL_NOT_CLAIM |

## Retained Residuals

| retained_id | residual | why_retained | impact |
| --- | --- | --- | --- |
| RET3873_0_Hodge | Delta_Hodge_EM | observed EM Hodge/coframe owner not derived from parent q/e_obs | blocks EM stress normalization/local-GR compatibility |
| RET3873_1_wEM | w_EM | independent EM action multiplier not excluded | scales T_EM, binding energy and Poynting source strength |
| RET3873_2_CXF2 | C_XF2 | hidden/extra F2 operator not excluded | reopens alpha/clock/WEP/R10/source response |
| RET3873_3_CJQ | C_JQ | charge/current normalization not parent-owned numerically | keeps current/source coupling residual live |
| RET3873_4_binding | Delta_M_EM_binding | EM binding must be included exactly once in M_H,total | prevents deleting or double-counting bound field energy |
| RET3873_5_readout | C_EM_readout | radiative/readout regeneration not theorem-zero | can reintroduce F2/current/source response |
| RET3873_6_radiative_branch | Phi_EM_rad_nonstationary | if the branch radiates or crosses background flux, Poynting term must be bounded not zeroed | keeps bound route for nonstationary cases |

## Claim Gates

| gate_id | status | detail | claim_allowed |
| --- | --- | --- | --- |
| G3873_0_sources | PASS | 15/15 sources resolved | False |
| G3873_1_zero_theorem | PASS | Phi_EM_boundary conditional zero branch | False |
| G3873_2_clause_audit | PASS | 7 clauses | False |
| G3873_3_reduced_envelope | PASS | B_EM_scale_stationary <= b_Z+b_J+\|b_alpha\|+\|w_EM\|+\|C_XF2\|+\|C_JQ\|+\|Delta_M_EM_binding\| | False |
| G3873_4_retained_residuals | PASS | 7 retained residuals | False |
| G3873_5_no_public_claim | BLOCKED | zero theorem is exact conditional, not parent-promoted | False |
| G3873_6_no_claim | PASS | valid_for_claim=false throughout | False |

## Decisions

| decision_id | decision | because |
| --- | --- | --- |
| DEC3873_0 | close the stationary Poynting leakage coefficient conditionally | this removes one finite source-coupling tail on the isolated local branch |
| DEC3873_1 | do not set local Poynting vector itself to zero | stationary systems can have circulating EM momentum/stress with zero net boundary flux |
| DEC3873_2 | do not claim EM origin or alpha normalization | the theorem assumes observed Maxwell/Hodge stress and leaves F2/current/charge gates live |
| DEC3873_3 | next best target is EM normalization/current owner or Delta_w theta commonness | Phi leakage is now localized; bigger remaining coupling failures are w_EM/C_XF2/C_JQ/Delta_w |

## Next Target

| next_id | target_checkpoint | objective | why_next |
| --- | --- | --- | --- |
| NEXT3873_0 | 3874-Y5-R2FR-EM-normalization-or-Delta-w-theta-commonness.md | attack the larger retained coupling families after the Poynting leakage term: either no-extra-F2/w_EM normalization, charge-current C_JQ, or Delta_w theta-vector commonness | 3873 conditionally removes Phi_EM_boundary for stationary isolated total-system tubes; remaining source-coupling risk is normalization/current/source-weight, not boundary Poynting leakage |

## Bottom Line

3873 is a genuine forward move: the Poynting term is no longer vague. In the stationary isolated total-system branch, the net boundary leakage coefficient `Phi_EM_boundary` has an exact conditional zero route, so the EM source-scale envelope can drop that term under the stated clauses. The remaining hard coupling problem is now sharper: derive or bound `w_EM`, `C_XF2`, `C_JQ`, `Delta_M_EM_binding`, `Delta_Hodge_EM`, readout regeneration, and the `Delta_w/theta` source-weight family.
