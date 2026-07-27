# 4063 - Explicit EH Weak-Field Newton/PPN Readout Contract

- Timestamp: `2026-07-02T01:33:08+00:00`
- Status: `private_nonclaim_checkpoint`
- Formalization modified: `false`
- Public local-GR claim: `false`

## Readout Result

4063 makes the conditional local-GR route explicit. If the selected local parent packet is adopted so that:

```text
G_mu_nu[g_obs] = kappa_eff T^H_mu_nu
G_N := c^4 kappa_eff/(8*pi)
```

with one observed frame, one same Hilbert source, and no first/second-order silent-sector leakage, then the weak-field 00 equation gives:

```text
G_00^(1) = 2 nabla^2 Phi_N/c^2
T_00^H = rho_H c^2
nabla^2 Phi_N = 4*pi*G_N*rho_H.
```

For compact support and no extra monopole:

```text
surface_integral grad Phi_N.dS = 4*pi*G_N*M_H
a_r = -G_N*M_H/r^2.
```

So Newton is not inserted as a plateau axiom in this branch; it is inherited from the EH weak-field equation with calibrated `G_N`.

## PPN Readout

Under the same EH/minimal same-source assumptions:

```text
gamma = 1
beta = 1
alpha1 = alpha2 = alpha3 = 0
xi = zeta_i = 0
Gdot/G = 0.
```

This is still conditional/private. If any assumption fails, the failed term goes to the residual fallback vector with no cancellation credit.

## What Remains

The next move is not another local term hunt. It is a formal-adoption preflight for the whole `4060-4063` chain: decide whether it can be folded into `formalization-workbench` as one guarded local-GR chain, or whether a named fallback scorer remains the honest state.
