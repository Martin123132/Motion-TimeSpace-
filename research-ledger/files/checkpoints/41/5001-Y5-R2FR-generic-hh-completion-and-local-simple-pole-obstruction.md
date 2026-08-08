# 5001 - Generic hh completion and local simple-pole obstruction

**Checkpoint marker:** `MTS_5001_GENERIC_HH_COMPLETION_AND_LOCAL_SIMPLE_POLE_OBSTRUCTION`  
**Date:** 2026-07-14  
**Claim status:** private one-loop amplitude derivation; not an outer-kernel, local-GR, or full-MTS claim.

## What is now directly derived

Five exact rational scattering angles were reduced with the independently identified raw auxiliary seed `element 2 = 8 s t A_YM`, the full physical graviton projector, all four uncut denominators, and exact dimension-shifted sphere moments. Four angles determine the symmetric homogeneous functions and the fifth is held out.

```text
B_su^hh(D) = u**4*(D**2*t**4 - 4*D**2*t**3*u + 6*D**2*t**2*u**2 - 4*D**2*t*u**3 + D**2*u**4 + 2*D*t**4 + 16*D*t**3*u - 36*D*t**2*u**2 + 16*D*t*u**3 + 2*D*u**4 + 48*t**2*u**2)/(256*(D - 3)*(D - 1))
B_st^hh(D) = t**4*(D**2*t**4 - 4*D**2*t**3*u + 6*D**2*t**2*u**2 - 4*D**2*t*u**3 + D**2*u**4 + 2*D*t**4 + 16*D*t**3*u - 36*D*t**2*u**2 + 16*D*t*u**3 + 2*D*u**4 + 48*t**2*u**2)/(256*(D - 3)*(D - 1))
A_s^hh(D)  = (t + u)*(D**3*t**6 - 6*D**3*t**5*u + 17*D**3*t**4*u**2 - 32*D**3*t**3*u**3 + 17*D**3*t**2*u**4 - 6*D**3*t*u**5 + D**3*u**6 + 26*D**2*t**5*u - 110*D**2*t**4*u**2 + 240*D**2*t**3*u**3 - 110*D**2*t**2*u**4 + 26*D**2*t*u**5 - 4*D*t**6 - 20*D*t**5*u + 200*D*t**4*u**2 - 560*D*t**3*u**3 + 200*D*t**2*u**4 - 20*D*t*u**5 - 4*D*u**6 - 80*t**4*u**2 + 400*t**3*u**3 - 80*t**2*u**4)/(128*(D - 3)*(D - 2)*(D - 1))
```

The held-out residuals are

```text
box = 0
one-scale = 0.
```

The direct and crossed anchor cuts also agree exactly. This closes the generic-dimensional internal-graviton `s` cut in the one-scale coordinate.

## Reconciliation with 4998 and 4999

The two direct box coefficients reproduce the independent 4998 shared-cut inference exactly:

```text
direct B_su^hh - 4998 B_su^hh = 0
direct B_st^hh - 4998 B_st^hh = 0.
```

There is therefore no missing mixed-*box* evanescent repair. This statement does not close the mixed one-scale coefficients. The other difference is between the direct `s`-channel one-scale coefficient and the 4999 IR-minimal continuation:

```text
delta A_s^hh = -t*u*(D - 4)*(t + u)*(D**2*t**4 + D**2*t**3*u + 10*D**2*t**2*u**2 + D**2*t*u**3 + D**2*u**4 + 2*D*t**4 + 8*D*t**3*u - 32*D*t**2*u**2 + 8*D*t*u**3 + 2*D*u**4 + 12*t**3*u + 56*t**2*u**2 + 12*t*u**3)/(128*(D - 3)*(D - 2)*(D - 1)).
```

It is proportional to `D-4`, so the sourced strict-four-dimensional amplitude and all logarithmic soft-pole checks remain intact. The direct cut, rather than the IR-minimal ansatz, owns this evanescent continuation.

## Local simple-pole obstruction

Combining the direct `s`, `t`, and `u` cuts gives

```text
P0 = 0
P1 = t*u*(2*t**2 + 3*t*u + 3*u**2)*(3*t**2 + 3*t*u + 2*u**2)/96.
```

`P0=0` preserves the universal gravitational double-pole cancellation. `P1` is an exactly crossing-symmetric polynomial with no kinematic denominator. It is a real local simple-pole obstruction, but locality does not identify its owner. The required cancellation is

```text
required simple-pole cancellation = -t*u*(2*t**2 + 3*t*u + 3*u**2)*(3*t**2 + 3*t*u + 2*u**2)/96
```

Dunbar--Norridge define `J2(s)=r_Gamma` and state that the `d J2` ambiguity is only in finite rational terms; it therefore cannot cancel a `1/epsilon` pole. The local source review also says four-derivative curvature terms do not generate a two-scalar/any-graviton on-shell amplitude in four dimensions, while evanescent Gauss--Bonnet effects are finite. The obstruction must instead be removed by an independently corrected one-scale cut coefficient or owned by an explicit source-backed UV counterterm of the required on-shell class. The immediate target is an independent generic-`D` mixed `t/u` one-scale reduction. No outer-kernel or full-amplitude claim is made while `P1 != 0`.
