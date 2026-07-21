# 4998 - Covariant mixed projector and generic-D box completion

**Checkpoint marker:** `MTS_4998_COVARIANT_MIXED_PROJECTOR_AND_GENERIC_D_BOX_COMPLETION`  
**Date:** 2026-07-14  
**Claim status:** private amplitude derivation; not a complete one-loop, outer-cut, local-GR, or full-MTS claim.

## Covariant mixed cut

Boels-Luo gives the minimally coupled two-scalar/two-graviton tree as the double copy of its gauge-invariant `B2` current. Collecting the internal polarization vector gives

```text
V=-2T(e.p3)p1+2[S(e.p3)-U(e.p2)]p3+TU e.
```

For a helicity external graviton, `p2.V=0` and `V.V=0`. The internal current `J=V tensor V` is therefore transverse and traceless, so the reference and `1/(D-2)` pieces of the D-dimensional graviton projector vanish.

On the mixed cut, with `h=N.L` and the common null reference vector `N`, exact contraction gives

```text
V_L.V_R = u^2(2h-1)^2/2,
<l3>[4l] = u(2h-1).
```

Hence the covariant projector product is exactly the rank-four numerator already reduced in 4994. There is no missing `mu^2` numerator on this cut. The old generic-D mixed reduction is promoted from diagnostic to physical.

## Completed mixed cut

In the finite 4995 one-scale coordinate:

```text
B_su(D) = u**4*(D**2*t**4 + 6*D**2*t**2*u**2 + D**2*u**4 + 2*D*t**4 + 12*D*t**3*u - 12*D*t**2*u**2 + 12*D*t*u**3 + 2*D*u**4 + 24*t**2*u**2)/(128*(D - 3)*(D - 1))
B_tu(D) = D*t**4*u**4*(D + 2)/(128*(D - 3)*(D - 1))
T_u(D)  = u**4*(3*D**3*t**3 + 7*D**3*t**2*u + D**3*t*u**2 - 2*D**3*u**3 - 12*D**2*t**3 - 72*D**2*t**2*u - 22*D**2*t*u**2 - 4*D*t**3 + 140*D*t**2*u + 48*D*t*u**2 + 8*D*u**3 + 16*t**3 - 48*t**2*u)/(128*(D - 3)*(D - 2)*(D - 1))
C_u     = -t**2*u**4/4
```

The `t` channel is the exact `t<->u` image.

## Completed generic-D boxes

Crossing now fixes all three full box coefficients: `B_st`, `B_su`, and `B_tu` in the output table. Subtracting the independently complete scalar `s` cut gives the missing D-dimensional `hh` box component,

```text
B_su^(hh)(D) = u**4*(D**2*t**4 - 4*D**2*t**3*u + 6*D**2*t**2*u**2 - 4*D**2*t*u**3 + D**2*u**4 + 2*D*t**4 + 16*D*t**3*u - 36*D*t**2*u**2 + 16*D*t*u**3 + 2*D*u**4 + 48*t**2*u**2)/(256*(D - 3)*(D - 1)).
```

Its linear-epsilon coefficient is

```text
u**4*(t + u)**2*(11*t**2 - 14*t*u + 11*u**2)/192.
```

Therefore the zero epsilon coefficient stored in 4991 is correctly understood as part of its strict four-dimensional helicity seed, not as the full D-dimensional internal-graviton continuation. The numerical correction found in 4996 was real, but its owner is the `hh` state sum rather than the mixed cut.

## Remaining calculation

The mixed `t/u` cuts and all generic-D boxes are complete. The remaining cut calculation is narrower: determine the `hh` contribution to the one-scale `s`-channel triangle/bubble combination. Only then can the cut-free `d J2` term and outer kernel be fixed.
