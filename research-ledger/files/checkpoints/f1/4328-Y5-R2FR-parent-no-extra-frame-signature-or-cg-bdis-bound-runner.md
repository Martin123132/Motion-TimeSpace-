# 4328 - parent no-extra-frame signature or c_g/b_dis bound runner

## Verdict

- Lifted ordinary matter `g_X=b_dis=0` in the standard action-domain branch.
- Rejected raw `c_g` scoring and terminal-metric shortcut.
- Kept full geometry open through EM/Hodge, coefficient, readout-frame and `Xi_src_hidden` tails.
- Next target is Dq_EM/Hodge constitutive ownership.

## Core Formulas
| formula_id | name | formula | status |
| --- | --- | --- | --- |
| F4328_0_ordinary_zero | ordinary matter no-extra-frame zero | S_matter=Sbar_m[Psi,g_obs(q),theta_obs(q)] and Dq[Hperp]=0 => g_X=0 and b_dis=0 for ordinary matter in the standard branch | CONDITIONAL_ZERO_DERIVED |
| F4328_1_canonical_gX | canonical frame coupling | g_X := d ln A_g/dphi_X = c_g/sqrt(Z_X), alpha_eff=\|g_X\| | CANONICAL_RUNNER_SCHEMA |
| F4328_4_geometry_core_update | geometry core update | epsilon_geom_core <= C_EMframe epsilon_EM_Hodge_frame + C_coeff epsilon_coeff + C_readout epsilon_readout_frame + C_terminal epsilon_terminal + tail_guard_sum after ordinary matter g_X=b_dis=0 | REDUCED_BUT_OPEN |

## Decision
| decision_id | result | reason | next_action |
| --- | --- | --- | --- |
| DEC4328_0 | ORDINARY_MATTER_GX_BDIS_ZERO_LIFTED_CONDITIONALLY_FULL_FRAME_RUNNER_RETAINS_EM_COEFF_XI_TAILS_NONCLAIM | 4277 closes ordinary matter g_X/b_dis in the standard action-domain branch, but full public geometry/no-shadow still needs EM/Hodge, coefficient, Xi and projection gates or a source-backed canonical runner. | 4329-Y5-R2FR-Dq-EM-Hodge-Hperp-zero-or-constitutive-tail-bound.md |

## Next Target
| next_target_id | next_target | preferred_route | fallback_route |
| --- | --- | --- | --- |
| NT4328_0 | 4329-Y5-R2FR-Dq-EM-Hodge-Hperp-zero-or-constitutive-tail-bound.md | prove same-Hodge Maxwell/EM action-domain ownership with no hidden/disformal EM metric or constitutive frame slot | retain epsilon_EM_Hodge_frame and Delta_Hodge_EM as finite local EM/clock/PPN projection tails |
