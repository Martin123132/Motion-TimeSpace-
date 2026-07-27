# 5029 — finite-x pole transport and collision map

## Result

The finite-`x` `hhh` plus integrand is now carried by an explicit physical-propagator contour rather than the undeformed crossed sphere.

For a sequential three-body event with soft energy `x`, the transported integrand is

    I_plus(w;z) = [x^2 M(x,w;z)/s^2 - G0(w;z)]/x,

where `M` is the sourced five-point KLT amplitude product and `G0` is the exact soft subtraction on the same global-azimuth contour. The nonzero global poles are the four stereographic factors for each direct internal direction together with the subtraction directions. Their physical-sheet ownership is fixed at `z=0.3` and restored by residue additions/subtractions.

At the checkpoint event the physical transported cycle agrees with a 256-node unit-circle reference to relative residual `1.2805e-7`. The crossed event at `z=1.5+0.08i` has eight explicitly labelled residue contributions and converges to

    I_plus = -12.1527750232 - 2.8848015880 i.

The soft subtraction remains finite under the same transport:

| `x` | physical `z=0.3` | crossed `z=1.5+0.08i` |
|---:|---:|---:|
| `0.01` | `-0.00571507` | `-12.0742-2.87405i` |
| `0.003` | `-0.00533748` | `-12.0577-2.86994i` |
| `0.001` | `-0.00522912` | `-12.0527-2.86871i` |

Thus the direct and endpoint pole sets coalesce without a `1/x` failure.

## Independent controls

The four-dimensional physical smoke integral gives

    D_hhh/G3 = -0.0008577 +/- 0.0008768,

consistent within about `0.31 sigma` with checkpoint 5017's independent five-dimensional value `-0.0005848 +/- 0.0000404`. The imaginary physical contamination is `5.4e-8`.

At `z=1.5+0.08i`, the global-pole-only finite-`x` integral is

    D_hhh/G3 = 0.8871 +/- 0.0493
               + i (0.2120 +/- 0.0272).

The non-fitted cyclic smoke remains far from the checkpoint-5018 matched nonlocal vector: its RMS difference is `21.04`. This is a useful rejection: global azimuth residues alone are not the missing crossing completion.

## Exact boosted polar law

Let `e` be the soft energy, `s` the soft direction, `d` the recoil-rest-frame decay direction, `mu=s.d`,

    beta=e/(2-e),
    gamma=(2-e)/(2 sqrt(1-e)),
    B=gamma beta=e/(2 sqrt(1-e)).

For the two hard legs `sigma=+1,-1`, the exact beam-axis cosines are

    c_sigma = [sigma d_z + (sigma(gamma-1)mu-B)s_z]
              /[gamma(1-sigma beta mu)].

Solving `c_sigma=h` gives

    mu_sigma(h) = [sigma h gamma-d_z+sigma B s_z]
                  /[(gamma-1)s_z+hB].

Writing

    mu=s_z d_z + sqrt(1-s_z^2)sqrt(1-d_z^2) eta,

the relative-azimuth roots are exactly

    xi_+/- = eta +/- sqrt(eta^2-1),
    xi_+ xi_- = 1.

The analytic complex boost agrees with the original sequential boost over 128 Sobol events to `1.78e-15`; mass-shell and hard-cosine residuals are below `4.45e-16`. All tested `c_sigma=+/-z` roots close below `5.52e-14`.

The complete finite-`x` polar-pinch list is therefore

    c_soft=+/-z,
    c_decay=+/-z,
    c_hard+=+/-z,
    c_hard-=+/-z.

## Coupled relative chamber

At `e=0.37`, `s_z=0.23`, `d_z=-0.31`, four physical unit-circle chamber boundaries are found. The order-20 chamber reconstruction reproduces the raw physical two-azimuth integral to relative residual `1.523e-4`.

The crossed logarithmic-spiral shortcut is rejected. With corrected reciprocal-root tracking, orders 8, 12, and 20 give materially different crossed values:

| relative order | crossed chamber value |
|---:|---:|
| `8` | `-45.1405-78.5227i` |
| `12` | `51.5820-3.81154i` |
| `20` | `6.38711-20.4693i` |

This is not Monte Carlo noise. The exact rational collision map finds many off-unit opposite-ownership pole collisions near the transported spirals. The physical unit-circle boundary sweep itself is complete at this event—four self-collision boundaries and zero additional cross-source unit boundaries—but endpoint interpolation does not transport the off-unit collision set.

## Decision

- Covariant/spinor finite-`x` KLT integrand: **pointwise closed** by checkpoint 5023.
- Global finite-`x` physical-pole transport: **constructed and controlled**.
- Soft-plus subtraction under transport: **finite**.
- Exact boosted hard-direction and polar-pinch laws: **derived**.
- Physical relative chamber: **controlled at one finite-`x` event**.
- Naive crossed logarithmic spiral: **rejected by order convergence**.
- Crossing-complete `hhh` nonlocal vector, full coupled cut, UV coefficient, local GR, and full MTS: **not claimed**.

Next: start at a small upper-half-plane regulator that splits the coincident physical collision roots, transport the full off-unit collision set and the relative contour by one causal homotopy, and require fixed-event convergence before integrating `e`, `s_z`, and `d_z`.

