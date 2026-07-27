# 5010 — coupled three-particle cut normalization and soft-plus integrand

## Result

This checkpoint advances the open outer-cut calculation rather than adding another target ledger. The physical `hhh` and `phi phi h` tree products are now executable with their coupling and identical-state factors, and their only non-integrable boundary is removed by an explicit graviton-soft plus prescription.

The checkpoint does **not** yet claim a two-loop UV coefficient. The remaining operation is a matched, converged multi-angle/multi-`z` integral combined with the virtual terms from checkpoints 4988 and 5008.

## Relative normalization

Luna et al. explicitly omit couplings and factors of `i`. With all three identical-scalar pairings, their four-point reduced sum obeys

```text
M4_Luna,raw = -4 C4,
C4 = tu/s + su/t + st/u.
```

The five-point relative normalization cannot therefore be guessed from the four-point coefficient alone. The universal soft theorem fixes it directly:

```text
M5_Luna,raw / (S_vec C4) -> -8,
M5_canonical = -M5_Luna,raw/8,
M5_canonical / (S_vec C4) -> 1.
```

At soft energy `10^-6`, the measured canonical ratio is `0.9999998030935001+6.451570003735843e-07j`. The independently constructed KLT `2phi+3h` kernel gives `0.9999998763902116+5.036124458614645e-07j`. This closes the earlier `-1/4` versus `-1/8` ambiguity: `-1/4` maps the coupling-omitted Luna four-point sum, while `-1/8` is the five-point factor demanded by soft factorization.

## Physical state sums

With each full five-point tree carrying `(kappa/2)^3`, the cut product carries `kappa^6/64`. The reduced state sums are

```text
F_hhh = (1/3!) sum_r [M_L^angle(r) M_R^square(r)
                      + M_L^square(r) M_R^angle(r)],

F_phiphih = (1/2!) sum_h M_L^canonical(h) M_R^canonical(-h).
```

The crossed helicity is fixed by unitarity rather than convention: complex-conjugating the right polarization makes the helicity sum equal the covariant graviton projector pointwise, with relative residual `1.041e-14`.

The `hhh` soft regions are partitioned symmetrically with

```text
w_i = E_i^-2 / sum_j E_j^-2,
F_hhh^(soft-3 sector) = 3 w_3 F_hhh.
```

Permutation symmetry and `sum_i w_i=1` make this an exact partition of the integrated identical-graviton state, not an extra multiplicity.

## Exact soft subtraction

For `s=4`, choose the third cut momentum as `k=(x,x n)` and decay the recoil into the remaining pair. The exact phase-space factor is

```text
dPhi3 = x dx dOmega_k dOmega_*/(512 pi^5),
integral dPhi3 = s/(256 pi^3).
```

For either sector define

```text
g_X(x,Omega) = x^2 F_X(x,Omega)/s^2,
H_X(x,Omega) = [g_X(x,Omega)-g_X(0,Omega)]/x.
```

`g_X(0,Omega)` is not fitted. For `hhh` it is built from exact four-point KLT trees and spinor soft factors; for `phi phi h` it is built from `C4` and the vector eikonal factor. At the fixed validation geometry,

```text
g_hhh(0)     = 0.0052767263905662+0j
g_phiphih(0) = 15.31948487657052+0j
```

The direct `x=10^-6` residuals are `3.155e-05` and `8.034e-06`. A soft internal scalar is suppressed rather than divergent; the measured power is `1.92286`.

The normalized finite-part relation is

```text
U3_plus/(kappa^6 s^3) = E[H_hhh + H_phiphih]/(8192 pi^3),
D3_plus/kappa^6       = -E[H_hhh + H_phiphih]/(16384 pi^4).
```

## Short numerical smoke

The short scrambled-Sobol runs are deliberately not promoted to precision results:

```text
hhh:     seed 5010: -0.029794427 +/- 0.006, seed 5011: -0.023259814 +/- 0.00597
phiphih: seed 5010: -1.5115058 +/- 3.85, seed 5011: -2.6207303 +/- 3.91
```

They establish that the subtraction is numerically executable. Their variance and seed spread remain part of the next convergence task.

## Gate

- Three-body measure, relative five-point normalization, physical state sums, symmetric soft sector, exact soft coefficients, and finite plus integrands: **closed**.
- Converged multi-`z` integration: **open**.
- Matching this real-emission plus prescription to the virtual subtraction in checkpoints 4988/5008: **open**.
- Combined outer UV projection, numeric `K_mu/K_ang`, local GR, and full MTS: **not claimed**.

Next: perform the matched multi-`z` integration, explicitly verify cancellation of the universal soft coefficient against the virtual channel, and only then apply the local UV projector.
