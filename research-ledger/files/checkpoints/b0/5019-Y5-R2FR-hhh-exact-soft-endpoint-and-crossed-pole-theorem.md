# 5019 — hhh exact soft endpoint and crossed-pole theorem

## Result

This checkpoint replaces two numerical ambiguities with derivations.

First, the five-dimensional `hhh` soft endpoint is reduced exactly. For beam direction `b`, outgoing direction `m`, hard cut direction `n`,

```text
A=b.n,  B=m.n,  z=b.m,
T(c)=(1-c^2)/4,
S(c)=(1-c)log(1-c)+(1+c)log(1+c).
```

The opposite-helicity four-point phase is `phase_4=cos(4 gamma)`. The covariant soft-direction integral inherited from checkpoint 5012 gives

```text
<g0_hhh>_k
=2 T(A)T(B) phase_4 [S(z)-S(A)-S(B)+2 log(2)].
```

This is not a fit. Direct integration of the checkpoint-5017 KLT soft coefficient agrees at three independent geometries with maximum relative residual `9.660e-05`.

## Exact spin-4 endpoint

Let `lambda_J=J(J+1)` and

```text
N_J^2=(J-4)!/(J+4)!
     =1/[lambda_J(lambda_J-2)(lambda_J-6)(lambda_J-12)].
```

The hard and soft-weighted Wigner moments are

```text
a_J = 12 N_J,
b_J = a_J [2 log(2)-R_J],
R_J = 8(lambda_J^3-5lambda_J^2+18lambda_J+36)
      /[lambda_J(lambda_J-2)(lambda_J-6)(lambda_J-12)],
```

for every even `J>=4`; odd modes vanish. Termwise beta-derivative moments independently reproduce these formulas through `J=40` with zero symbolic residual.

Define

```text
A_4(z)=sum_even,J>=4 (2J+1) a_J^2 P_J(z),
C_4(z)=sum_even,J>=4 (2J+1) a_J^2 R_J P_J(z).
```

Then the complete double-angular soft endpoint is

```text
G0_hhh(z)=2[(S(z)-2 log(2)) A_4(z)+2 C_4(z)].
```

| physical z | exact-resolvent `G0_hhh(z)` |
|---:|---:|
| -0.6 | -0.0404970978368 |
| -0.3 | 0.00568724580433 |
| +0.0 | 0.0282226204786 |
| +0.3 | 0.00568724580433 |
| +0.6 | -0.0404970978368 |

The physical series agrees with its independent Legendre-resolvent construction to `5.691e-17`.

## Crossed-pole theorem

For crossed `z>1`, write `sqrt(1-z^2)=i beta`, `beta^2=z^2-1`, `rho^2=1-A^2`, and let `q_+`, `q_-` be the two helicity phase factors. Exactly,

```text
q_+ q_- = 1-B^2,
2T(A)T(B)phase_4
=rho^2/16 [q_+^3/q_- + q_-^3/q_+].
```

The real hard sphere therefore contains simple poles:

```text
q_-=0 at A=+-1/z, phi=pi/2,
q_+=0 at A=+-1/z, phi=3pi/2,
Res_phi = -i sigma (z^2-1)^2/(2z),  sigma=+-1.
```

The executable root tracker proves that the pole moves from inside to outside the unit azimuth contour at those loci for `z=1.5`, `3`, and `9`. This is the mechanism anticipated by the Caron-Huot/Wilhelm contour method: the crossed answer requires contour deformation and residues. Plain real-sphere QMC is not merely noisy; it evaluates the wrong continuation.

The symmetric resolvent boundary value already fixes the endpoint-only cyclic diagnostic:

| physical z | cyclic symmetric soft endpoint |
|---:|---:|
| -0.6 | 116.75407832 |
| -0.3 | 11.4227059378 |
| +0.0 | -6.12131192936 |
| +0.3 | 11.4227059378 |
| +0.6 | 116.75407832 |

These numbers are **not** the finite `hhh` cut and are not substituted into the checkpoint-5018 nonlocal target.

## Physical boundaries

All `14` physical-sheet boundary scans pass their measure-integrability thresholds. The exact physical phase obeys `|phase_4|<=1`; the averaged endpoint falls with approximately the third power at each hard collinear surface. Soft-direction collinear limits remain finite, the recoil-pair endpoint has power greater than `-1`, and the tested simultaneous paths `angle=x^p` make the plus integrand decay. No physical nonintegrable boundary was found.

## Status

- Exact KLT soft-direction average: **derived and independently checked**.
- Arbitrary-even-J spin-4 endpoint tower: **derived**.
- Physical endpoint and crossed upper/lower resolvent boundary values: **constructed without fitting**.
- Real crossed-sheet simple-pole locus and residue: **proved**.
- Raw checkpoint-5017 crossed QMC as an analytic continuation: **rejected**.
- Finite-`x` five-point contour-residue sum: **open**.
- Corrected full `hhh` cyclic cut, coupled locality, UV coefficient, local GR, and full MTS: **not claimed**.

Next: write each complex-safe five-point KLT denominator as a polynomial in `t=e^(i phi)`, sector-decompose the finite-`x` phase space, and add the pole-crossing residues before the `x` integration. The result must be compared directly with the checkpoint-5018 nonlocal target; no five-point fit or local scheme adjustment is allowed.
