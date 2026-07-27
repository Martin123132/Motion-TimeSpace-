# 4041 - c_norm Common Mode Into kappa_obs Or Gdot Bound

- Timestamp: `2026-07-01T23:38:44+00:00`
- Status: `private_nonclaim_checkpoint`
- Scope: `post-checkpoint-work` only; no `formalization-workbench` edits.
- Source needles found: `12/12`.

## What Actually Moved

4041 splits `c_norm` into the part that is just calibration and the part that is real physics.

The constant/common mode routes into the observed Newton coupling:

`G_obs=c^4*kappa_obs/(8*pi)`, with `kappa_obs=1/(1/kappa_*+2*c_I*phi_*)`.

That is not a fifth-force/source-hair residual. It is the same kind of calibrated coupling role that Newton's constant plays in GR.

## What Does Not Get Hidden

Any nonconstant piece is physical:

`Delta_source_norm = D_a ln mu_obs = D_a ln G_obs + D_a ln M_eff + D_a ln(1+epsilon_mu)`.

So time drift, radial hair, range dependence, species/source dependence, frame/domain dependence, and `M_eff` flux drift remain explicit.

## Bound Interface

If the fixed/global sector route fails:

- `D_t ln G_obs` maps to `Gdot/G`;
- `partial_r ln mu_obs` maps to radial source hair / PPN / orbital residuals;
- `alpha_norm(lambda)` maps to R10 inverse-square tests;
- `eta_source_AB` maps to source/WEP composition locks;
- `Delta_cnorm_envelope` is the no-cancellation sum of the remaining derivative pieces.

## Current Verdict

- Current evaluator result: `COMMON_MODE_ROUTED_TO_KAPPA_OBS_DERIVATIVE_HAIR_RETAINED`.
- Claim result: `NO_PUBLIC_LOCAL_GR_CLAIM_FROM_4041`.
- Remaining live local residuals: `Delta_cZ_envelope`, `Delta_cnorm_envelope`, `c_nonEH`.

## Next Target

- `4042-Y5-R2FR-nonEH-operator-decoupling-or-PPN-bound-vector.md`
- `scripts/Y5_R2FR_4042_nonEH_operator_decoupling_or_PPN_bound_vector.py`
