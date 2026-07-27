# 4038 - Poynting No-Flux And Boundary Reference Theorem Or Flux Bound

- Timestamp: `2026-07-01T23:23:02+00:00`
- Status: `private_nonclaim_checkpoint`
- Scope: `post-checkpoint-work` only; no `formalization-workbench` edits.
- Source needles found: `10/10`.

## What Actually Moved

4038 attacks the next two local leaks after the direct coupling cleanup:

- `c_Poynting`: net EM/radiative/background flux through the local collar;
- `c_B`: source-dependent boundary/corner/reference leakage.

## Local Poynting Result

Using the selected 4037 packet, Maxwell energy accounting is one identity:

`d_t u_EM + div S_EM = -J.E`.

For a stationary/asymptotically stationary exterior collar with no current crossing the collar and no imposed incoming/background radiation,

`Phi_EM_rad = int_boundary S_EM.n dA = 0`.

Bound Coulomb/magnetostatic fields are not extra leakage; they are counted once inside `T_total` and `M_H`.

## Boundary Result

The selected local branch uses

`S_boundary = S_GHY[g_obs] + exact/topological terms - H_ref[fixed source-blind reference]`.

With `D_source H_ref=D_readout H_ref=0` and quiet collar boundary data, the direct source-dependent boundary scalar is zero:

`c_B*B_source=0`.

## Guardrail

This is local no-flux, not global no-flux. The FLRW/cosmology memory branch remains allowed. We are not using a global zero that would murder the cosmology route in its sleep.

## Fallback Bound

If stationarity, isolation, or fixed-reference conditions fail:

- `Phi_EM_rad=(1/Delta t)*int_dt int_boundary S_EM.n dA`;
- `epsilon_EM_flux=Phi_EM_rad/(G_ref*M_H)`;
- `|Q_phi_flux| <= (2/3)*|c_Poynting|*|Phi_EM_rad|`;
- `|Q_phi_B| <= |c_B|*|B_source|`.

These rows are schema-ready but numeric-claim blocked until the profiles and normalizations are real.

## Current Verdict

- Current evaluator result: `C_POYNTING_AND_C_B_ZERO_IN_SELECTED_LOCAL_BRANCH`.
- Claim result: `NO_PUBLIC_LOCAL_GR_CLAIM_FROM_4038`.
- Remaining live local residuals: `c_Z`, `c_norm`, `c_nonEH`.

## Next Target

- `4039-Y5-R2FR-hidden-current-fixed-point-silence-or-cZ-bound.md`
- `scripts/Y5_R2FR_4039_hidden_current_fixed_point_silence_or_cZ_bound.py`
