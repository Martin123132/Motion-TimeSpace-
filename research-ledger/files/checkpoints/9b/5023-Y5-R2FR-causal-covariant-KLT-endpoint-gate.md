# 5023 - causal covariant KLT endpoint gate

## Derived advance

The scalar-gluon four- and five-point amplitudes are now implemented in a covariant form with every Mandelstam propagator explicit. The five-point expression is the sourced formula in `post-checkpoint-work/source-intake/functional_rg/4987/sources/scalar_graviton_1908.09755/mscalar_grav-submit.tex`; generic color orders are obtained by the Kleiss-Kuijf shuffle with the two scalar legs as endpoints.

At a finite three-body phase-space point, all tested helicity and KLT-order identities close:

| check | maximum relative residual |
|---|---:|
| four-point KLT | `1.264e-15` |
| soft endpoint | `1.457e-15` |
| five-point gauge trees | `1.244e-13` |
| five-point KLT gravity trees | `2.047e-12` |
| complete finite-`x` helicity-summed hhh cut | `1.058e-14` |

The covariant gauge-tree convention differs from the spinor tree by `-1` for chirality zero and `+1` for chirality one. These signs cancel inside each KLT gravity tree. Thus the full finite-`x` hhh cut is now available with physical propagator denominators rather than only spinor brackets.

## Causal endpoint test

Every propagator denominator and each factor of the five-point momentum kernel was given a controlled `+/- i epsilon`. On the physical control at `z=0.3`, reducing `epsilon` from `0.1` to `0.01` moves the result toward the exact checkpoint-5019 endpoint; the imaginary contamination shrinks from `3.80e-3` to `8.09e-4`.

The crossed control at `z=1.5+0.08i` gives the opposite verdict. At `epsilon=0.01`, the four sign assignments have relative residuals `0.507` to `0.551` against the exact resolvent. Their real parts agree reasonably, but all miss most of the required imaginary boundary value. The discrepancy is much larger than the RQMC errors and persists as `epsilon` is reduced.

Therefore an explicit propagator-level `i0` on the **undeformed real sphere** does not itself transport the integration cycle through the crossed pole. Checkpoint 5021's claim that `q+i epsilon` supplied the crossed contour is superseded. This is a homology failure, not a normalization fit or a reason to reject the KLT cut.

## Status

- Covariant four-point and five-point tree representation: **derived and independently matched**.
- Complete finite-`x` covariant hhh cut integrand: **constructed**.
- Physical causal control: **passed**.
- Undeformed-real-sphere crossed continuation: **rejected**.
- Coupled crossed cut, UV coefficient, local GR and full MTS: **not yet claimed**.

Next: classify the nonzero global-azimuth poles by their actual covariant propagator channels, discard canceled/gauge-only spinor roots, and transport the coupled azimuth/polar cycle. The exact checkpoint-5019 endpoint remains the non-fitted gate for that construction.
