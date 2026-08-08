# 5009 - Three-particle phase space and five-point tree-kernel closure

**Checkpoint marker:** `MTS_5009_THREE_PARTICLE_PHASE_SPACE_AND_FIVE_POINT_TREE_KERNEL_CLOSURE`  
**Date:** 2026-07-14  
**Claim status:** private amplitude derivation; not an integrated outer-cut, local-GR, or full-MTS claim.

## Three-body measure

Caron-Huot and Wilhelm's three-spinor map has been implemented directly. It preserves nullness and total momentum at the non-symmetric test point with residuals

```text
max |p_i'^2|                 = 4.770e-17
|p1+p2-p1'-p2'-p3'|         = 5.567e-16
```

All five normalized measure factors integrate to one, so

```text
integral dmu = 1,
dPhi_3       = s/(256 pi^3) dmu.
```

This removes the three-body phase-space normalization ambiguity from the next cut calculation.

## Exact `4phi+1h` tree kernel

The five Luna-O'Connell-White numerator vectors and denominators are now executable. For a physical transverse polarization the source numerators obey, in the orientation used here,

```text
n_A - n_B = -n_C,
n_D - n_E = +n_C.
```

The sign of `n_C` is a cubic-vertex/color orientation convention and disappears from the `n_C^2/d_C` double copy. Both Ward contractions vanish, a finite shift `epsilon -> epsilon + a k` leaves the amplitude unchanged, and the three scalar-line pairings produce an `S4`-symmetric identical-real-scalar amplitude. The maximum numerical residuals are

```text
Jacobi             = 3.972e-15
Ward               = 4.625e-14
line orientation   = 3.093e-15
S4 Bose symmetry   = 2.874e-13
finite gauge shift = 6.355e-14
```

The unwanted Luna ghost subtraction vanishes exactly in this massless branch because every `n_i'` carries `m_1 m_2`. No fitted five-point ansatz is used.

## Exact `2phi+3h` tree kernel

The massless one-minus scalar-gluon MHV seed is

```text
A_n(1_phi,...,r^-,...,n_phi)
  = <r1>^2 <rn>^2 / PT,
```

while the all-plus seed vanishes. KLT squaring with the primary momentum-kernel convention gives

```text
M_5 = sum_(sigma,gamma in S2)
      A(1,sigma,4,5) S[gamma|sigma]_(k1) A(4,5,gamma,1),
```

where `theta=1` only for opposite pair ordering. This kernel is invariant under all six graviton permutations and obeys parity, with residuals

```text
S3 permutation = 4.076e-15
parity          = 0.000e+00
```

The literal right ordering displayed in the 2019 scalar-graviton source is convention-unsafe in this massless implementation: it fails the same permutation test by `0.797513` relatively. The primary arXiv:1010.3933 ordering `(n-1,n,gamma,1)` is therefore used. This is a tested convention decision, not a silent sign choice.

## What is closed and what is not

- Normalized three-particle phase-space map: **closed**.
- Massless `4phi+1h` double-copy tree kernel, including identical-scalar completion: **closed**.
- Massless one-minus and parity-related `2phi+3h` KLT tree kernels: **closed**.
- All-plus `2phi+3h` branch: **zero by the massless MHV selection rule**.
- Coupling restoration and products with the required lower-loop amplitudes: **not yet integrated**.
- Cancellation against the crossed nonlocal remainder of checkpoint 5008: **not yet tested**.
- Full outer UV projection: **open**.

Next: insert these executable kernels into the normalized `dmu` integral, restore the common Einstein-scalar coupling factors, sum every three-particle helicity/cut placement, and combine that result with checkpoint 5008 before applying any local projector.
