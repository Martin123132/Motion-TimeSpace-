# 4999 - hh one-scale IR Laurent completion

**Checkpoint marker:** `MTS_4999_HH_ONE_SCALE_IR_LAURENT_COMPLETION`  
**Date:** 2026-07-14  
**Claim status:** private amplitude derivation; not a complete one-loop, outer-cut, local-GR, or full-MTS claim.

## Result

The physical one-scale coefficient is the basis-invariant combination

```text
A_x(D)=T_x(D)+(D-4)x/[2(D-3)] C_x(D).
```

Write `A_x(4-2 epsilon)=A_x,0+epsilon A_x,1+O(epsilon^2)`. The generic-D boxes and crossed `t/u` cuts from 4998 leave no freedom in the IR-visible `s` coefficient. The constant double- and simple-pole equations are

```text
4 sum B_xy,0/(xy)-sum A_x,0/x=0,
4 sum B_xy,1/(xy)-sum A_x,1/x=0.
```

Both residuals vanish exactly. The solved full `s` coefficients are

```text
A_s,0 = (t + u)*(t**6 + t**5*u + 2*t**4*u**2 + 2*t**2*u**4 + t*u**5 + u**6)/8
A_s,1 = (t + u)*(22*t**6 + 36*t**5*u + 21*t**4*u**2 + 22*t**3*u**3 + 21*t**2*u**4 + 36*t*u**5 + 22*u**6)/96.
```

Subtracting the exact scalar direct cut from 4997 gives the missing internal-graviton contribution

```text
A_s,0^(hh) = (t + u)*(t**6 - t**5*u + t**4*u**2 - t**3*u**3 + t**2*u**4 - t*u**5 + u**6)/16
A_s,1^(hh) = (t + u)*(11*t**6 - 3*t**5*u - 27*t**4*u**2 - 27*t**2*u**4 - 3*t*u**5 + 11*u**6)/96.
```

## Evanescent correction

The 4991 source sums only the two four-dimensional helicities while integrating in `D=4-2 epsilon`. Its direct physical one-scale coefficients are

```text
A_s,0^(hh,FDH) = -(t + u)*(t**6 - t**5*u + t**4*u**2 - t**3*u**3 + t**2*u**4 - t*u**5 + u**6)/16
A_s,1^(hh,FDH) = t*u*(t + u)*(2*t**4 - 3*t**3*u - 3*t*u**3 + 2*u**4)/32.
```

The finite `epsilon^0` CDR-minus-FDH shift is

```text
(t + u)*(t**6 - t**5*u + t**4*u**2 - t**3*u**3 + t**2*u**4 - t*u**5 + u**6)/8.
```

This equals the independently derived 4997 scalar one-scale coordinate translation exactly. It explains why simply importing the 4991 triangle into the generic-D state sum gives the wrong direct coefficient even though every box has the correct four-dimensional limit.

## Boundary of the result

The Laurent coefficients through linear `epsilon` are fixed because they own the constant `1/epsilon^2` and `1/epsilon` poles. Extending the displayed IR-minimal rational representative to arbitrary `D` is not licensed by those two equations. The `epsilon^2` coefficient can feed a finite cut-free rational term and therefore remains part of the `d J2` reconstruction. The next calculation is a direct `mu^2`-moment/projector reduction that must either validate the candidate beyond linear order or replace it.
