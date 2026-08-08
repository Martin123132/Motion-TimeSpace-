# 3966 - Gauss Orbital Calibration Or Delta Cal Bound

Timestamp: `2026-07-01T15:27:53+00:00`

## Result

3966 makes the measured Newton `GM` bridge explicit.

The observed quantity is:

`mu_obs := r^2 |a_r| = v^2 r`.

The candidate parent source side is:

`mu_parent := G_eff M_eff[Pi_M J_H]`.

The bridge lands only if the same-frame weak-field equation, Gauss surface integral, and slow-orbit readout all close:

`nabla^2 Phi=4 pi G_eff rho_H`

`int_S grad Phi.dS=4 pi G_eff M_eff`

`a_r=-partial_r Phi=-G_eff M_eff/r^2`.

If this chain fails, the calibration residual is retained:

`|Delta_cal|/(G_eff M_eff) <= |epsilon_charge|+|epsilon_Poisson|+|epsilon_Gauss|+|epsilon_orbit|+|epsilon_extra|+|epsilon_derivative|+|epsilon_PPN_source|`.

## Meaning

This prevents a cheat: a conserved Hilbert/PiM source mass is not automatically the measured orbital `GM`. It must pass the Poisson/Gauss/orbit/readout chain or be scored as `Delta_cal`.

## Source/Register

- Sources found: `22/22`
- Bridge theorem: `source-intake\mts_residuals\P8_Y5_R2FR_3966_GAUSS_ORBITAL_BRIDGE_THEOREM_OR_BOUND.csv`
- Delta_cal vector: `source-intake\mts_residuals\P8_Y5_R2FR_3966_DELTA_CAL_RESIDUAL_VECTOR.csv`
- Readout gate: `source-intake\mts_residuals\P8_Y5_R2FR_3966_INVERSE_SQUARE_READOUT_GATE.csv`
- Newton feed update: `source-intake\mts_residuals\P8_Y5_R2FR_3966_NEWTON_SCORE_DELTA_CAL_FEED_UPDATE.csv`
- Validation: `source-intake\mts_residuals\P8_Y5_BRR545_3966_VALIDATION.csv`

## Next Target

`3967-Y5-R2FR-second-order-PPN-source-stability-or-Delta-PPN-bound.md`
