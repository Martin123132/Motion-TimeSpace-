# 4054 - Scalar Charge Zero and Improvement Normalization

- Timestamp: `2026-07-02T00:54:01+00:00`
- Status: `private_nonclaim_checkpoint`
- Formalization modified: `false`
- Public local-GR claim: `false`

## What Actually Moved

4053 exposed two sharp hinges: `Q_phi=0` and `sigma_resp*c_I=1`.

4054 takes a real swing at both:

1. `sigma_resp*c_I=1` is not necessarily a new physical number. If `phi` is only the auxiliary Khat-owner field, define the unit-response scalar

```text
varpi := sigma_resp*c_I*(phi-phi_*)
```

and write `Khat_TF` in terms of `varpi`. Under the single-use auxiliary-scalar guard, the coefficient becomes a field-normalization/adoption convention, not a fitted parameter.

2. `Q_phi=0` can come from the variational boundary problem. On the exterior collar,

```text
(Delta_h - mu_phi^2)u = 0,    u := varpi-varpi_*
```

and the variation of the exterior scalar action gives the inner-boundary term

```text
delta S_phi|inner = -zeta_phi int_{S_src} n.grad u delta u dS.
```

If no boundary source term or hidden source-slot coupling to `u` exists, free boundary variation gives

```text
n.grad u = 0  =>  Q_phi = int_{S_src} n.grad u dS = 0.
```

With outer/asymptotic branch fixing, the energy identity then gives `u=0`, so `Hess(u)=0` and the scalar part of `Khat/q_loc` vanishes.

## Non-Negotiable Guards

- This uses the 4029 dynamical exterior owner, not the older 1527 multiplier route.
- If `phi` couples independently to matter, EM, clocks, masses, or constants, the coefficient cannot be normalized away.
- If a source-boundary scalar term exists, natural no-flux fails and `Q_phi` must be bounded.
- This is still private/nonclaim until the no-source-boundary and auxiliary-single-use clauses are adopted in the parent packet.

## Next Target

Attack the remaining `q_loc` pieces: parent Hilbert ownership/`D_GK=0` and trace/background subtraction. Choom, this is not the roof yet, but this is an actual rung under the boot.
