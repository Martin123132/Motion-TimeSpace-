# 4997 - Full H contact vanishing and generic-D scalar-cut completion

**Checkpoint marker:** `MTS_4997_FULL_H_CONTACT_VANISHING_AND_SCALAR_CUT_COMPLETION`  
**Date:** 2026-07-14  
**Claim status:** private amplitude derivation; not a complete one-loop, outer-cut, local-GR, or full-MTS claim.

## Exact result

The lower-topology terms omitted by the box-residue replacement `H(R) -> H(0)=s^4` do not generate an additional scalar triangle in the opposite-helicity channel.

The correct helicity covector is

```text
n.l = <2|l|1] = l_00-l_01,
n.p1=n.p2=n.(p1+p2)=0,
n.(-p4)=+1,  n.(-p3)=-1,
n^2=0.
```

After Feynman-shifting any one-mass triangle, `n.R_shift=0`. Expanding

```text
H(R)/(s^4 R)=1/R+2/s+3R/s^2+2R^2/s^3+R^3/s^4
```

leaves contact powers `R^r` with `r=0,1,2,3`. Rotational invariance requires four free transverse vectors to contract `(n.k)^4`; each term supplies at most `r<4`, while every `n.n` contraction vanishes. Therefore every contact integral is exactly zero for generic `D`.

The complete scalar `s` cut in the direct triangle-only one-scale coordinate is consequently

```text
B_st = D*t**4*(D + 2)*(t + u)**4/(256*(D - 3)*(D - 1))
B_su = D*u**4*(D + 2)*(t + u)**4/(256*(D - 3)*(D - 1))
T_s  = (t + u)*(D**3*t**6 + 2*D**3*t**5*u + D**3*t**4*u**2 + D**3*t**2*u**4 + 2*D**3*t*u**5 + D**3*u**6 + 2*D**2*t**5*u + 2*D**2*t**4*u**2 + 2*D**2*t**2*u**4 + 2*D**2*t*u**5 - 4*D*t**6 - 4*D*t**5*u + 8*D*t**4*u**2 + 8*D*t**2*u**4 - 4*D*t*u**5 - 4*D*u**6 + 16*t**4*u**2 + 48*t**3*u**3 + 16*t**2*u**4)/(128*(D - 3)*(D - 2)*(D - 1))
C_s  = 0.
```

## Why checkpoint 4993 had a different scalar triangle

There is no contradiction in the amplitude. For one-scale massless masters,

```text
I2_D(s) = (D-4)s/[2(D-3)] I3_D(s).
```

The 4993 IR allocation and the direct cut are different coordinates on that one-dimensional master space. Their D4 triangle difference is

```text
Delta T = (t + u)*(t**6 - t**5*u + t**4*u**2 - t**3*u**3 + t**2*u**4 - t*u**5 + u**6)/8.
```

Retaining the 4993 triangle coordinate requires the bubble translation

```text
C_translation(D) = (23*D**3*t**6 + 6*D**3*t**5*u + 39*D**3*t**4*u**2 - 8*D**3*t**3*u**3 + 39*D**3*t**2*u**4 + 6*D**3*t*u**5 + 23*D**3*u**6 - 144*D**2*t**6 - 50*D**2*t**5*u - 242*D**2*t**4*u**2 + 48*D**2*t**3*u**3 - 242*D**2*t**2*u**4 - 50*D**2*t*u**5 - 144*D**2*u**6 + 268*D*t**6 + 92*D*t**5*u + 432*D*t**4*u**2 - 88*D*t**3*u**3 + 432*D*t**2*u**4 + 92*D*t*u**5 + 268*D*u**6 - 144*t**6 - 48*t**5*u - 256*t**4*u**2 - 256*t**2*u**4 - 48*t*u**5 - 144*u**6)/(64*(D - 4)*(D - 2)*(D - 1)),
Res_(D=4) C_translation = (t**6 - t**5*u + t**4*u**2 - t**3*u**3 + t**2*u**4 - t*u**5 + u**6)/4.
```

The pole is spurious and cancels exactly through the master identity. It is nevertheless mandatory in that coordinate. The finite scalar bubble listed in 4995 remains usable as a finite aggregate convention, but it is not a separately cut-derived scalar observable and cannot replace this pole while simultaneously retaining the 4993 scalar triangle split.

## Consequence

The generic-D scalar `s` cut is now complete. The next unresolved calculation is the actual D-dimensional internal-graviton state sum on the `hh` and mixed cuts. That is the remaining cut input before the finite `d J2` remainder and outer kernel can be assembled.
