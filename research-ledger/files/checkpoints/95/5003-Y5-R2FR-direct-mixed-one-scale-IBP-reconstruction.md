# 5003 - Direct mixed one-scale IBP reconstruction

**Checkpoint marker:** `MTS_5003_DIRECT_MIXED_ONE_SCALE_IBP_RECONSTRUCTION`  
**Date:** 2026-07-14  
**Claim status:** private amplitude derivation; not a complete one-loop, local-GR, or full-MTS claim.

## Calculation

The mixed `u` cut was regenerated from all four rank-four families `AC`, `AD`, `BC`, and `BD`. For every topology the exact rational reducer separately returned the cut-visible bubble, both triangles, and box. No hard-coded coefficient from checkpoint 4995 entered the fit.

Sixteen independent `(D,t,u)` points derive

```text
A_u(D) = u**4*(3*D**3*t**3 - 9*D**3*t**2*u + D**3*t*u**2 - 2*D**3*u**3 - 12*D**2*t**3 + 40*D**2*t**2*u - 22*D**2*t*u**2 - 4*D*t**3 - 84*D*t**2*u + 48*D*t*u**2 + 8*D*u**3 + 16*t**3 + 80*t**2*u)/(128*(D - 3)*(D - 2)*(D - 1)).
```

Three unused points have total squared residual `0`. The generic residual against the 4998 finite-coordinate result, after using the exact `I2/I3` master relation, is `0`. All box normalization residuals also vanish.

The formerly stored anchor is now regenerated rather than trusted:

```text
(D,t,u)=(5,1,2): T_u_raw=-353/16, C_u_raw=319/32, A_u=-1093/64.
```

## Consequence

The mixed `t/u` one-scale continuation is not the owner of the 5001 simple-pole mismatch. This is progress by exclusion backed by a fresh calculation: the remaining fork is now the `hh` `s`-cut dimensional state/current continuation versus a genuinely source-backed UV counterterm. Finite `dJ2` remains excluded as a pole owner.
