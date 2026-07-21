# 5004 - Physical HV IR completion and nonlocal-pole rejection

**Checkpoint marker:** `MTS_5004_PHYSICAL_HV_IR_COMPLETION_AND_NONLOCAL_POLE_REJECTION`  
**Date:** 2026-07-14  
**Claim status:** private amplitude derivation; not a complete one-loop or full-MTS claim.

## Result

The 5001 mismatch is resolved at the physical-amplitude pole level. Keeping the independently checked physical-D boxes and crossed one-scale coefficients, the universal soft equation fixes

```text
A_s(D) = (t + u)*(2*D**3*t**6 - 3*D**3*t**5*u + 19*D**3*t**4*u**2 - 22*D**3*t**3*u**3 + 19*D**3*t**2*u**4 - 3*D**3*t*u**5 + 2*D**3*u**6 + 26*D**2*t**5*u - 104*D**2*t**4*u**2 + 168*D**2*t**3*u**3 - 104*D**2*t**2*u**4 + 26*D**2*t*u**5 - 8*D*t**6 - 32*D*t**5*u + 188*D*t**4*u**2 - 376*D*t**3*u**3 + 188*D*t**2*u**4 - 32*D*t*u**5 - 8*D*u**6 - 112*t**4*u**2 + 224*t**3*u**3 - 112*t**2*u**4)/(128*(D - 3)*(D - 2)*(D - 1)).
```

After subtracting the direct scalar cut, the selected hh coefficient is

```text
A_s^hh(D) = (t + u)*(D**3*t**6 - 5*D**3*t**5*u + 18*D**3*t**4*u**2 - 22*D**3*t**3*u**3 + 18*D**3*t**2*u**4 - 5*D**3*t*u**5 + D**3*u**6 + 24*D**2*t**5*u - 106*D**2*t**4*u**2 + 168*D**2*t**3*u**3 - 106*D**2*t**2*u**4 + 24*D**2*t*u**5 - 4*D*t**6 - 28*D*t**5*u + 180*D*t**4*u**2 - 376*D*t**3*u**3 + 180*D*t**2*u**4 - 28*D*t*u**5 - 4*D*u**6 - 128*t**4*u**2 + 176*t**3*u**3 - 128*t**2*u**4)/(128*(D - 3)*(D - 2)*(D - 1)).
```

This is **exactly** the value stored at 4999: the residual is `0`. What 4999 got wrong was the description `CDR direct inference`. It is an IR-completed representative for the physical HV amplitude, with `D_ext=4`, `D_int=D`, and `D_loop=D`.

## Why the competing term is rejected

The 5001 direct continuation differs by

```text
Delta A_s = -t*u*(D - 4)*(t + u)*(D**2*t**4 + D**2*t**3*u + 10*D**2*t**2*u**2 + D**2*t*u**3 + D**2*u**4 + 2*D*t**4 + 8*D*t**3*u - 32*D*t**2*u**2 + 8*D*t*u**3 + 2*D*u**4 + 12*t**3*u + 56*t**2*u**2 + 12*t*u**3)/(128*(D - 3)*(D - 2)*(D - 1)).
```

It vanishes at strict `D=4`, but its linear evanescent part generates

```text
P1 = t*u*(2*t**2 + 3*t*u + 3*u**2)*(3*t**2 + 3*t*u + 2*u**2)/96.
```

Calling this polynomial in the stripped reduced function a local UV obstruction was incorrect. The amplitude convention is `M^(1)=kappa^4 F/Qbar^4` and `Q Qbar=tu`. Restoring the helicity phase gives

```text
P1/Qbar^4 = Q**4*(2*t**2 + 3*t*u + 3*u**2)*(3*t**2 + 3*t*u + 2*u**2)/(96*t**3*u**3),
```

whose denominator is `96*t**3*u**3`. It is nonlocal in `t` and `u`. The known one-loop scalar-gravity counterterm has four scalar legs; source-backed `R^2` and `R_mn^2` insertions are silent in two-scalar/n-graviton amplitudes; and `dJ2` is finite only. There is therefore no admissible local owner for this pole.

## Decision

- Retain the physical-D boxes and directly regenerated mixed `t/u` coefficients.
- Use the soft-completed `A_s` through the Laurent order that controls the poles.
- Retire the unsupported `CDR direct` label at 4999 while promoting its value.
- Quarantine, rather than delete, the 5001 direct `s`-cut evanescent continuation.
- Do not reopen the constant IR-pole question unless a new direct calculation identifies the missing evanescent current term and also passes the restored-helicity locality gate.

The microscopic reason the direct `s`-cut implementation generated the extra evanescent term remains open. That does not leave the physical pole arbitrary: the retained cuts, soft theorem, and locality fix it uniquely. The next calculation is the finite outer kernel with `dJ2` kept explicit.
