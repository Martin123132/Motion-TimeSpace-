# 4996 - Generic-D scalar box and mandatory mixed massive correction

**Checkpoint marker:** `MTS_4996_GENERIC_D_SCALAR_BOX_AND_MIXED_MASSIVE_CORRECTION`  
**Date:** 2026-07-14  
**Claim status:** private amplitude derivation; not a complete one-loop, outer-cut, local-GR, or full-MTS claim.

## What moved

The scalar `s` cut can be lifted consistently to generic `D`: a D-dimensional massless cut scalar is a four-dimensional scalar of mass `mu`, and the sourced opposite-helicity two-graviton/two-massive-scalar tree has no explicit `mu` numerator. A direct stress-tensor contraction also proves that the apparent `1/(D-2)` dependence of massless four-scalar graviton exchange cancels.

Exact rational IBP reduction then gives the complete scalar contributions to the two shared boxes:

```text
B_st^(scalar)(D) = D*t**4*(D + 2)*(t + u)**4/(256*(D - 3)*(D - 1))
B_su^(scalar)(D) = D*u**4*(D + 2)*(t + u)**4/(256*(D - 3)*(D - 1))
```

Their `D -> 4` limits are `s^4 t^4/32` and `s^4 u^4/32`, reproducing checkpoint 4992.

## The crossed-cut correction

The inherited generic-D mixed continuation agrees at `D=4` but fails once evanescent information is retained. Combining the exact scalar box with the sourced `hh` box, whose linear-epsilon coefficient is zero, factorises the diagnostic discrepancy as

```text
Delta_B(D) = u**4*(D - 4)*(t + u)**2*(7*D*t**2 - 10*D*t*u + 7*D*u**2 - 6*t**2 + 12*t*u - 6*u**2)/(256*(D - 3)*(D - 1)).
```

With `D=4-2 epsilon`, crossed-channel unitarity therefore requires the missing mixed massive-state term

```text
delta B_su = epsilon * (-u**4*(t + u)**2*(11*t**2 - 14*t*u + 11*u**2)/192) + O(epsilon^2).
```

This is not a fitted repair. It is the unique linear-epsilon coefficient required for the same scalar box to have the same coefficient on its `s` and `u` cuts. At the diagnostic point `(t,u,D)=(1,2,5)`, the old continuation misses `621/128`; that finite-D number is only a failure witness because the `hh` input is source-controlled only through linear epsilon.

## Triangle correction to the previous interpretation

The generic-D rank-four reducer also yields a triangle descendant, but it is **not** the full scalar triangle. Checkpoint 4992 replaced

```text
H(R)=(s^2+sR+R^2)^2
```

by `H(0)=s^4` only on quadruple residues. That replacement is exact for boxes and invalid away from the box residue. The exact D4 deficit relative to the independently IR-fixed scalar triangle is

```text
Delta_T_contact(D=4) = (t + u)*(t**6 - t**5*u + t**4*u**2 - t**3*u**3 + t**2*u**4 - t*u**5 + u**6)/8.
```

Thus the scalar box is now genuinely generic-D complete, while the scalar triangle still requires reduction of the full `H(R)` numerator. This checkpoint explicitly retracts any physical interpretation of the old arbitrary generic-D mixed and rank-four-only triangle continuations.

## Consequence for the outer cut

The route is narrower now. The next derivation is not another source sweep and not another re-labelling exercise: extend the reducer to the full `H(R)` contact numerator, then apply the D-dimensional graviton projector to the mixed/`hh` states. Only after those two calculations can the cut-free `d J2` remainder and the permutation-complete outer kernel be assembled.
