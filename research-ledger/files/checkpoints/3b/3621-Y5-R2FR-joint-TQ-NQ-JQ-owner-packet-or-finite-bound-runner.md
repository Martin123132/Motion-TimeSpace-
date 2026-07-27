# 3621 Y5 R2FR: joint T_Q/N_Q/J_Q owner packet or finite bound runner

## Verdict
- The all-or-nothing EM owner packet is now explicit.
- No theorem-zero promotion is allowed yet: `T_Q`, `N_Q`, unique `F2`, `J_Q`, readout/radiative closure, Hilbert source weight and boundary flux are not jointly parent-signed.
- Finite runner templates now exist with units, arenas and source paths, but correctly refuse to score missing MTS predictions.

## Joint owner packet
- `A_Q` must be a parent connection projection along fixed `T_Q`.
- `N_Q=<T_Q,T_Q>_P` must be fixed representation/fibre metric/lattice data.
- Unique `F_Q^2` must exclude `lambda_A F_Q^2` and hidden `f_X F_Q^2`.
- `J_Q` must be the same `T_Q` Noether/Ward current used by source/test readout.
- Readout/radiative closure must preserve the same owner.
- EM Hilbert stress must have no extra `w_EM` source weight.
- Boundary Poynting flux must be zero by stationary/no-flux theorem or carried explicitly.

## Finite runner rows
- `lambda_F2`: dimensionless alpha/clock/spectroscopy/WEP row.
- `b_alpha`: clock alpha-drift row.
- `kappa_J`: MICROSCOPE/WEP source-current rescaling row.
- `w_EM`: Newton/PPN/orbital/source-weight row, direct bound still missing.
- `Phi_EM_boundary`: stationary source/H_tau flux row, direct bound still missing.

## Practical read
- Piecemeal closure is not enough; this packet must close as one unit.
- Best derivation target is now `T_Q/N_Q`: if the parent fixes the gauge generator and norm, several knobs collapse at once.

## Next target
- `3622-Y5-R2FR-TQ-NQ-parent-fibre-metric-or-source-bound-acquisition.md`.
- First try the derivation: fixed parent representation/fibre metric/lattice for `T_Q` and `N_Q`.
- Backup: acquire/stage direct bounds for `w_EM` and `Phi_EM_boundary`.

## Claim status
- `NO_CLAIM`: packet built, runner templates blocked correctly.
