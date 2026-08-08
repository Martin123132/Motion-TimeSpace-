# 3914 — Stationary Local Source-Coupling Stack or Readout Residual Map

Timestamp: `2026-07-01T10:21:39+00:00`

## Result

This checkpoint assembles the local stationary source-coupling stack and closes the remaining readout factors **inside the conditional branch only**.

Branch:
`EH/product/q_src/source-silent/stationary local collar`

Source stack:
`S_parent -> EH public metric equation -> same-frame Hilbert/Maxwell stress -> q_src fixed source charge -> B_Meff=0 -> source-normalized Poisson/Newton readout`

Epsilon result:
`epsilon_mu=0 on the stationary source-silent collar when all component rows EMU3914_0..EMU3914_9 are theorem-zero`

Poisson result:
`Z_Poisson=1 because nabla^2 Phi=(kappa_* c^4/2)rho_H=4*pi*G_*rho_H with kappa_*=8*pi*G_*/c^4 and rho_H the same Hilbert source`

Frame result:
`Z_frame=1 because matter, clocks, source charge, orbit readout and Maxwell stress use the same observed Q_pub coframe/frame fixed by q_src`

Local Gdot result:
`Gdot_total=0 on the stationary source-silent collar: d_t ln G_*=0, B_Meff=0, d_t epsilon_mu=0, d_t ln Z_Poisson=0, d_t ln Z_frame=0`

Newton/Maxwell source statement:
`Newton/Maxwell source coupling follows conditionally: G_mu_nu+Lambda g_mu_nu=8*pi*G_*T_vis, T_vis includes T_EM, and the weak-field limit gives nabla^2 Phi=4*pi*G_*rho_H`

## Meaning

- The source-coupling hole is no longer open inside the stationary EH/product/q_src/source-silent branch.
- `epsilon_mu`, `Z_Poisson`, and `Z_frame` close conditionally, so the stationary local `dotG/G` envelope also closes conditionally.
- This remains private/nonclaim because branch adoption and PPN/readout residuals still need to be made explicit.
- Dynamic, source-active, cosmological, non-EH and frame-split branches remain residual-scored.

## Source Register

- Source rows found: `22/22`
- Register: `source-intake\mts_residuals\P8_Y5_R2FR_3914_SOURCE_REGISTER.csv`
- Validation: `source-intake\mts_residuals\P8_Y5_BRR545_3914_VALIDATION.csv`

## Generated Tables

- `source-intake\mts_residuals\P8_Y5_R2FR_3914_STATIONARY_SOURCE_COUPLING_STACK.csv`
- `source-intake\mts_residuals\P8_Y5_R2FR_3914_EPSILON_MU_COMPONENT_CLOSURE_MATRIX.csv`
- `source-intake\mts_residuals\P8_Y5_R2FR_3914_ZPOISSON_ZFRAME_CLOSURE_GATE.csv`
- `source-intake\mts_residuals\P8_Y5_R2FR_3914_LOCAL_GR_NEWTON_MAXWELL_ARENA_STACK.csv`
- `source-intake\mts_residuals\P8_Y5_R2FR_3914_ACTIVE_BRANCH_RESIDUAL_FALLBACK_MAP.csv`
- `source-intake\mts_residuals\P8_Y5_R2FR_3914_BRANCH_DECISION_GATE.csv`
- `source-intake\mts_residuals\P8_Y5_R2FR_3914_NEXT_TARGET.csv`

## Next Target

`3915-Y5-R2FR-stationary-local-branch-contract-and-PPN-residual-vector.md`
