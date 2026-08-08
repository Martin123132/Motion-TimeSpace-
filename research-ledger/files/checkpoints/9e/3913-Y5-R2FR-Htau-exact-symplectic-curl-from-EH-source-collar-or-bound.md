# 3913 — Htau Exact Symplectic Curl from EH Source Collar or Bound

Timestamp: `2026-07-01T10:16:31+00:00`

## Result

This is the other half of the 3911/3912 source-denominator core.

Curl identity:
`curl(delta H_tau)(delta_1,delta_2)=int_S i_tau omega_MTS(delta_1,delta_2)+int_partialS corner_tau(delta_1,delta_2)`

EH stationary flux:
`on the EH local stationary source collar, L_tau Q=0 and variations preserve tau,Sigma,H_ref, so int_S i_tau omega_EH(delta_1,delta_2)=0`

Extra-sector flux:
`at Y_loc=H_priv=0 with S_int^{>=2} and source-silent variations, omega_Y+omega_H+omega_int has no linear source-collar flux`

Reference/corner:
`q_src fixes R_ref=(tau,Sigma,H_ref), so reference and corner curl terms vanish for source-silent vertical variations`

Htau result:
`R_Htau=0 for the EH/product/source-silent stationary collar`

PiM/Htau core:
`R_PiM+R_Htau=0 by 3912 R_PiM=0 plus 3913 R_Htau=0`

Stationary source-mass stack:
`B_Meff=0 if Ward conservation, q_src-fixed reference/support/frame/units, stationary side-flux silence, R_PiM=0 and R_Htau=0 all hold`

Gdot after this stack:
`Gdot_total <= 0 + |d_t epsilon_mu/(1+epsilon_mu)| + |d_t ln Z_Poisson| + |d_t ln Z_frame| on the stationary source-silent collar`

## Meaning

- `R_PiM` is closed by 3912 for source-silent q_src verticals.
- `R_Htau` is closed here for the EH/product/source-silent stationary source collar.
- Together, the PiM/Htau source-denominator core is conditionally zero.
- With Ward conservation, q_src-fixed reference/support/frame/units, and side-flux silence, `B_Meff=0` is also conditionally closed.
- This is still not a public local-GR claim: the remaining gates are `epsilon_mu`, `Z_Poisson`, `Z_frame`, and parent adoption of the branch.

## Source Register

- Source rows found: `20/20`
- Register: `source-intake\mts_residuals\P8_Y5_R2FR_3913_SOURCE_REGISTER.csv`
- Validation: `source-intake\mts_residuals\P8_Y5_BRR545_3913_VALIDATION.csv`

## Generated Tables

- `source-intake\mts_residuals\P8_Y5_R2FR_3913_HTAU_EXACT_CURL_THEOREM.csv`
- `source-intake\mts_residuals\P8_Y5_R2FR_3913_EXTRA_SECTOR_FLUX_SILENCE.csv`
- `source-intake\mts_residuals\P8_Y5_R2FR_3913_MEFF_STATIONARY_SOURCE_CLOSURE_STACK.csv`
- `source-intake\mts_residuals\P8_Y5_R2FR_3913_REMAINING_LOCAL_GR_RESIDUALS.csv`
- `source-intake\mts_residuals\P8_Y5_R2FR_3913_BRANCH_DECISION_GATE.csv`
- `source-intake\mts_residuals\P8_Y5_R2FR_3913_NEXT_TARGET.csv`

## Next Target

`3914-Y5-R2FR-stationary-local-source-coupling-stack-or-readout-residual-map.md`
