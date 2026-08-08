# 5000 - Covariant hh mu-moment master reduction

**Checkpoint marker:** `MTS_5000_COVARIANT_HH_MU_MOMENT_MASTER_REDUCTION`  
**Date:** 2026-07-14  
**Claim status:** private amplitude derivation; not a complete one-loop, outer-cut, local-GR, or full-MTS claim.

## Executable tree-seed lock

Checkpoint 5002 compared the first two raw auxiliary tensors with an independently reconstructed color-ordered Yang–Mills tree. The exact identity in the auxiliary-file ordering is

```text
GluonsSymms element 2 = 8 s t A_YM(1,2,3,4).
```

The first raw list element is separately gauge invariant but has a sample-dependent ratio to `s t A_YM`, so it is not the minimal Yang–Mills tree seed. The earlier element-1 diagnostic is quarantined rather than promoted. This reduction uses element 2 and retains the scalar-Compton tensor on the other double-copy factor.

## Exact reduction

The two gravity trees produce four uncut denominators,

```text
P_L (-s-P_L) P_R (-s-P_R).
```

Applying the exact partial fraction on each pair gives four two-denominator angular integrals. Moments containing `mu^(2r)` obey

```text
<mu^(2r) f>_N = ((D-4)/2)_r/(N/2)_r <f>_(N+2r),  N=D-1,
```

and the shifted double-denominator moment is reduced recursively to `L_N(c)` plus the collinear moment `J_N=(D-3)/(D-4)`. The identical-state orientation factor is fixed, rather than fitted, by requiring both independent box residues to agree with checkpoint 4998.

At the exact point `s=4, t=-16/5, u=-4/5`, the direct one-scale internal-graviton coefficient is

```text
A_s^hh(D) = -128*(505*D**3 + 12168*D**2 - 18388*D + 3840)/(15625*(D - 3)*(D - 2)*(D - 1)).
```

Its dimensional expansion is

```text
epsilon^0: -3355648/15625
epsilon^1: -4740608/9375
epsilon^2: -153929216/140625
epsilon^3: -958388224/421875
```

Both generic-D box residuals vanish:

```text
B_su residual = 0
B_st residual = 0
```

The strict-four-dimensional one-scale residual is `0` and the linear-epsilon residual against checkpoint 4999 is `-5967872/46875`. The direct cut and the 4999 IR-only linear-epsilon inference disagree; neither is silently promoted.

## Scope

This checkpoint performs a direct dimensionally regulated cut reduction at one rational kinematic point. A generic `(t,u)` reconstruction, the cut-free `d J2` term, and the outer kernel remain separate calculations. No local-GR or full-MTS claim follows from this amplitude checkpoint.
