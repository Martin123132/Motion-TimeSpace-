# 4029 - Phi Owner Sign Convention Or Tracefree Residual Bound Input

- Timestamp: `2026-07-01T22:40:37+00:00`
- Status: `private_nonclaim_checkpoint`
- Scope: `post-checkpoint-work` only; no `formalization-workbench` edits.

## What Actually Moved

4029 removes one piece of fog. Using the Gamma-owner functional

`I_Gamma=int sqrt|g| Gamma_eff`

and the existing convention

`Khat_metric^{mu nu}=+2/sqrt|g| delta I_Gamma/delta g_{mu nu}`,

the improvement term

`I_imp[c_I]=c_I int sqrt|g| phi R`

has lower-metric response

`K_imp^{mu nu}=2*c_I[nabla^mu nabla^nu phi-g^{mu nu}Box phi-phi G^{mu nu}]`.

Therefore

`Pi_TF[K_imp]^{mu nu}=2*c_I[(nabla^mu nabla^nu phi-(1/4)g^{mu nu}Box phi)-phi G_TF^{mu nu}]`.

So the old sign placeholder is now concrete: the derivative trace-free piece matches `K_L` when `c_I=1`.

## Phi Owner

The local owner template

`I_phi=int sqrt|g|[-zeta_phi/2 grad(phi)^2-zeta_phi*mu_phi^2/2*(phi-phi_*)^2-(2*zeta_phi/3)phi F]`

with `F:=Gamma_eff+C` gives

`Box phi-mu_phi^2(phi-phi_*)=(2/3)F`,

provided `F` is independent of `phi` or has been split into `F_rest`. If not, the extra term is retained as `D_phiF`.

## Local Vacuum Identity

For `F=0`, `mu_phi^2>=0`, and no-flux/fixed boundary data,

`int(|grad u|^2+mu_phi^2 u^2)dV=boundary`, where `u=phi-phi_*`.

If the boundary term vanishes, `phi` is constant and `K_L=0` on the compact local fixed branch.

## Reduced Residual

The trace-free residual is now

`D_TF^{mu nu}=(1-c_I)K_L^{mu nu}+2*c_I*phi*G_TF^{mu nu}+D_phiF^{mu nu}+D_owner^{mu nu}+D_boundary^{mu nu}+D_adoption^{mu nu}`.

That is better than 4028: the sign ambiguity is gone, and the leading surviving obstruction is now `phi*G_TF` plus adoption/boundary bookkeeping.

## Current Verdict

- Current evaluator result: `TRACEFREE_RESIDUAL_REDUCED_CURVATURE_ADOPTION_OPEN`.
- Claim result: `NO_PUBLIC_QLOC_OR_LOCAL_GR_CLAIM_FROM_4029`.
- Source needles found: `8/8`.

## Next Target

- `4030-Y5-R2FR-curvature-channel-routing-or-tracefree-score-input.md`
- `scripts/Y5_R2FR_4030_curvature_channel_routing_or_tracefree_score_input.py`
