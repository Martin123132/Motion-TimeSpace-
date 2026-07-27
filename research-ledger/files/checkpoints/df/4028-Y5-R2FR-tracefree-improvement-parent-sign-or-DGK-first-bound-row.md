# 4028 - Tracefree Improvement Parent Sign Or D_GK First Bound Row

- Timestamp: `2026-07-01T22:35:14+00:00`
- Status: `private_nonclaim_checkpoint`
- Scope: `post-checkpoint-work` only; no `formalization-workbench` edits.

## What Actually Moved

The trace-free Khat route is no longer just "maybe an improvement term". It is now tied to the explicit parent-action variation

`S_imp[c_I]=s_imp*c_I int sqrt|g| phi R + B_imp`.

The metric response gives the derivative trace-free piece

`Pi_TF[K_imp]^{mu nu} = 2*sigma_resp*c_I[(nabla^mu nabla^nu phi-(1/4)g^{mu nu}Box phi)-phi G_TF^{mu nu}]`.

So the old candidate

`K_L^{mu nu}=2[nabla^mu nabla^nu phi-(1/4)g^{mu nu}Box phi]`

is exactly recovered if `sigma_resp*c_I=1` and the curvature channel `Pi_TF(phi G)` is silent or routed into the EH/matter response.

## New Local Owner Route

To avoid an inverse-Box definition of `phi`, 4028 adds a local owner template:

`S_phi=int sqrt|g|[-zeta_phi/2 nabla phi.nabla phi-(mu_phi^2/2)(phi-phi_*)^2-(2*zeta_phi/3)phi(Gamma_eff+C)]`.

In the `mu_phi=0` branch, with signs fixed, this can produce the old relation `Box phi=(2/3)(Gamma_eff+C)` as an Euler equation. This is useful, but not yet adopted, and its stress contribution must be accounted for.

## Residual Law

Until the clauses are signed, the retained trace-free residual is

`D_TF^{mu nu}=(1-sigma_resp*c_I)K_L^{mu nu}+2*sigma_resp*c_I phi G_TF^{mu nu}+D_phi_owner^{mu nu}+D_boundary^{mu nu}+D_adoption^{mu nu}`.

The first honest bound row is therefore

`A_TF/L_TF <= |1-sigma_resp*c_I|A_KL/L_KL + 2|sigma_resp*c_I|A_phiG/L_phiG + A_owner/L_owner + A_boundary/L_boundary + A_adoption/L_adoption`.

## Current Verdict

- Current evaluator result: `TRACEFREE_COMPONENT_CONDITIONALLY_DERIVED_NOT_LIVE_ADOPTED`.
- Claim result: `NO_PUBLIC_QLOC_OR_LOCAL_GR_CLAIM_FROM_4028`.
- Source needles found: `8/8`.
- This is real progress: one Khat subcomponent now has a parent-action route and an exact residual law.

## Next Target

- `4029-Y5-R2FR-phi-owner-sign-convention-or-tracefree-residual-bound-input.md`
- `scripts/Y5_R2FR_4029_phi_owner_sign_convention_or_tracefree_residual_bound_input.py`
