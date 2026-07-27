# 4030 - Curvature Channel Routing Or Tracefree Score Input

- Timestamp: `2026-07-01T22:45:39+00:00`
- Status: `private_nonclaim_checkpoint`
- Scope: `post-checkpoint-work` only; no `formalization-workbench` edits.

## What Actually Moved

The surviving `phi*G_TF` term from 4029 is not all the same kind of physics. Combine the Einstein-Hilbert and improvement terms:

`I_EH+I_imp=int sqrt|g|[(1/(2*kappa_*))+c_I*phi]R`.

Split

`phi=phi_*+delta_phi`.

Then the constant branch defines the observed coupling

`1/(2*kappa_obs)=1/(2*kappa_*)+c_I*phi_*`,

so

`kappa_obs=1/(1/kappa_*+2*c_I*phi_*)` and `G_obs=c^4*kappa_obs/(8*pi)`.

This means constant `phi_*G_TF` is not a new force; it is part of the EH/Newton coupling calibration. The physical residual is the hair:

`2*c_I*delta_phi*G_TF`.

## Reduced Trace-Free Residual

After EH routing,

`D_TF=(1-c_I)K_L + 2*c_I*delta_phi*G_TF + D_phiF + D_owner + D_boundary + D_adoption + D_kappa_sector`.

This is a narrower obstruction than 4029.

## Newton Constant Stance

4030 does not claim to predict the numerical value of `G`. It derives how the local observed coupling is built from parent constants. That is compatible with the GR/Newton ladder: the theory must reduce to Newton with a calibrated coupling, while separately proving the coupling is constant/universal or bounding drift.

## Current Verdict

- Current evaluator result: `CURVATURE_CHANNEL_REDUCED_NOT_LIVE_ADOPTED`.
- Claim result: `NO_PUBLIC_QLOC_OR_LOCAL_GR_CLAIM_FROM_4030`.
- Source needles found: `8/8`.

## Next Target

- `4031-Y5-R2FR-exterior-collar-deltaphi-zero-or-CbetaTF-projector.md`
- `scripts/Y5_R2FR_4031_exterior_collar_deltaphi_zero_or_CbetaTF_projector.py`
