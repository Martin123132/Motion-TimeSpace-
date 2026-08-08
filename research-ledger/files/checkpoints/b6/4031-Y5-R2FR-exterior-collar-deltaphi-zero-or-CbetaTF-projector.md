# 4031 - Exterior Collar Deltaphi Zero Or CbetaTF Projector

- Timestamp: `2026-07-01T22:49:46+00:00`
- Status: `private_nonclaim_checkpoint`
- Scope: `post-checkpoint-work` only; no `formalization-workbench` edits.

## What Actually Moved

4031 attacks the remaining scalar hair from 4030. Let

`u := delta_phi = phi - phi_*`.

On a static exterior collar with `F=Gamma_eff+C=0`, the phi-owner equation reduces to

`(Delta - mu_phi^2)u=0`.

Multiplying by `u` and integrating gives

`int_Omega(|grad u|^2+mu_phi^2 u^2)dV = int_boundary u n.grad u dS`.

Therefore, if the exterior branch has fixed/asymptotic `u=0` or no scalar charge `u n.grad u=0`, then `u=0` for `mu_phi>0`. In the massless case, only a constant survives, and that constant is absorbed into `phi_*` and hence into `kappa_obs`.

## Residual Consequence

Under those clauses,

`delta_phi*G_TF=0`

on the exterior PPN collar. If the scalar charge is not zero, the residual is not hidden; it becomes a hair bound:

`|u(r)| <= |Q_phi| exp[-mu_phi(r-R_src)]/(4*pi*r) + boundary_outer`.

## C_beta_TF Fallback

If hair survives, define

`C_beta_TF := Pi_beta[L_PPN^-1(2*c_I*delta_phi*G_TF + retained trace-free residuals)]`.

Then

`delta_beta_TF = C_beta_TF*(A_delta_phiG/L_phiG)`.

So 4031 gives the route a theorem-zero branch and a score branch.

## Current Verdict

- Current evaluator result: `EXTERIOR_ZERO_CONDITIONAL_BOUNDARY_ADOPTION_OPEN`.
- Claim result: `NO_PUBLIC_QLOC_OR_LOCAL_GR_CLAIM_FROM_4031`.
- Source needles found: `7/7`.

## Next Target

- `4032-Y5-R2FR-scalar-charge-zero-or-Yukawa-hair-bound-input.md`
- `scripts/Y5_R2FR_4032_scalar_charge_zero_or_Yukawa_hair_bound_input.py`
