# 3620 Y5 R2FR: EM source-coupling owner or F2 coefficient bound

## Verdict
- The EM/source coupling throat is now explicit.
- Local Maxwell light-cone success is not enough: `A_Q`, `F_Q^2`, `J_Q`, `alpha_EM`, Poynting/Hilbert stress and source mass must share one parent owner.
- The owner theorem is exact conditionally, but not parent-signed in the current corpus.
- Therefore finite source-coupling coefficient rows are retained.

## Conditional owner theorem
- `A_parent = A_Q T_Q + A_perp` must define the visible connection before readout.
- `Z_Q = C_P <T_Q,T_Q>_P = C_P N_Q` must be fixed by parent representation/norm data.
- No independent `lambda_F2 F_Q^2` or hidden `f_X F_Q^2` may exist.
- `J_Q := delta S_matter/delta A_Q` must be the same `T_Q` Noether/Ward current used by source/test readout.
- `T_EM` must be the Hilbert stress from the same observed-Hodge Maxwell action.
- If all close together: `lambda_F2=b_alpha=kappa_J=w_EM=0`.

## Live finite rows
- `lambda_F2`: independent Maxwell kinetic multiplier.
- `b_alpha`: vertical/readout drift of measured fine-structure level.
- `kappa_J`: source/test current normalization rescaling.
- `w_EM`: EM Hilbert stress/source weight relative to matter/source mass.
- `Phi_EM_boundary`: radiative Poynting boundary flux not included in stationary source charge.

## Practical read
- The theory is not dead here; this is a clean engineering throat.
- But this must close as one packet. Closing only `F2` while leaving current normalization free just moves the knob.
- This is directly connected to Newton/GR reduction because it controls what counts as source mass/energy.

## Next target
- `3621-Y5-R2FR-joint-TQ-NQ-JQ-owner-packet-or-finite-bound-runner.md`.
- Aim: one parent owner packet for `T_Q`, `N_Q`, `J_Q`, unique `F2`, and EM Hilbert source weight; otherwise prepare finite empirical bound rows.

## Claim status
- `NO_CLAIM`: exact conditional theorem plus finite coefficient rows.
