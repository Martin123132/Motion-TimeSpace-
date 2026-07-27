# 4329 Y5-R2FR Dq-EM-Hodge Hperp zero or constitutive tail bound

Marker: `PPC4161_DQ_EM_HODGE_HPERP_ZERO_OR_CONSTITUTIVE_TAIL_BOUND_4329`

Decision: `SAME_HODGE_CLOSED_COLLAR_DQ_EM_ZERO_IMPORTED_CONDITIONALLY_EM_HODGE_FRAME_TAIL_REMOVED_GLOBAL_EM_ALPHA_OPEN_NONCLAIM`

## Result

`epsilon_EM_Hodge_frame` is no longer a vague geometry-tail bucket in the standard local branch. It is zero if the same observed Hodge Maxwell action, q-basic calibrated EM readout, Hilbert-owned Poynting flux, and closed-collar/static boundary clauses all hold.

This is still private and conditional. Open radiation, independent constitutive tensors, hidden EM metrics, alpha/current drift, and global Maxwell/QED remain outside the claim.

## Reduced Geometry Core

| formula_id | formula | status |
| --- | --- | --- |
| F4329_0_same_hodge_zero | fixed(g_obs,e_obs,orientation,vol_obs) and S_EM=-(4 mu0)^-1 int F wedge *_obs F with no chi_EM => Delta_Hodge_EM=0 | CONDITIONAL_ZERO_DERIVED |
| F4329_1_Dq_EM_closed_collar | F4329_0 + q-basic EM constants + pure readout + Phi_EM_rad=0_or_boundary_routed => Dq_EM[Hperp]=Dq_EM_C1=0 | CONDITIONAL_ZERO_IMPORTED |
| F4329_2_no_poynting_double_count | S_i=-T_EM(n,e_i)=(E cross B)_i, so Poynting contributes through Hilbert EM stress and not as a second source force | OWNER_RULE |
| F4329_3_constitutive_bound | \|\|Delta_Hodge_EM\|\| <= \|\|Delta_chi_principal\|\| + \|\|Delta_chi_skewon\|\| + L\|\|dtheta_EM\|\| + \|C_Hodge_hidden\| + \|C_Hodge_readout\| + \|Delta_orientation_flux\| | BOUND_RETAINED_OUTSIDE_BRANCH |
| F4329_4_geometry_core_update | epsilon_geom_core <= C_coeff epsilon_coeff + C_readout epsilon_readout_frame + C_terminal epsilon_terminal + C_EMopen epsilon_EM_open_boundary + tail_guard_sum | REDUCED_BUT_OPEN |
| F4329_5_source_readout_update | epsilon_source_readout <= (L_T L_mg + L_g) epsilon_geom_core_after_EM + Xi_src_hidden | NONCLAIM_HANDOFF |

## Remaining Tails

| tail_id | symbol | when_live | bound_contribution | status |
| --- | --- | --- | --- | --- |
| TAIL4329_0_Delta_chi_principal | Delta_chi_principal | independent EM constitutive tensor or hidden EM metric survives | \|\|Delta_chi_principal\|\| | RETAINED_OUTSIDE_BRANCH |
| TAIL4329_1_Delta_chi_skewon | Delta_chi_skewon | non-Maxwell constitutive sector survives | \|\|Delta_chi_skewon\|\| | RETAINED_OUTSIDE_BRANCH |
| TAIL4329_2_dtheta_EM | dtheta_EM | theta_EM is not q-basic calibrated visible data | L\|\|dtheta_EM\|\| | RETAINED_OUTSIDE_BRANCH |
| TAIL4329_3_C_Hodge_hidden | C_Hodge_hidden | extra EM frame slot survives in the parent/effective action | \|C_Hodge_hidden\| | RETAINED_OUTSIDE_BRANCH |
| TAIL4329_4_C_Hodge_readout | C_Hodge_readout | readout is not pure postprocessing | \|C_Hodge_readout\| | ZERO_IN_STANDARD_BRANCH_RETAINED_OUTSIDE |
| TAIL4329_5_Delta_orientation_flux | Delta_orientation_flux | collar orientation is not fixed before variation | \|Delta_orientation_flux\| | RETAINED_OUTSIDE_BRANCH |
| TAIL4329_6_Phi_EM_rad | Phi_EM_rad | non-static/open radiative local system | \|Phi_EM_rad\|/M_ref or explicit boundary Hamiltonian flux | BOUNDARY_ROW_RETAINED |
| TAIL4329_7_b_alpha_CJQ | b_alpha + C_JQ | alpha/current normalization is parent-active instead of calibrated q-basic data | \|b_alpha\|+\|C_JQ\| | RETAINED_OUTSIDE_BRANCH |

## Next

| next_target | target_question | preferred_route |
| --- | --- | --- |
| 4330-Y5-R2FR-coefficient-drift-zero-or-source-backed-tail-bound.md | Can the coefficient drift epsilon_coeff be zeroed by q-basic parent coefficient ownership, or must it become a source-backed finite tail? | prove all local visible coefficients in the reduced branch are q-basic/calibrated before variation and not hidden field functions |
