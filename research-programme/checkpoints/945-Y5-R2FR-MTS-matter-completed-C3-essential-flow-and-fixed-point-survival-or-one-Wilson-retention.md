# 4929 - MTS matter-completed C3 essential flow and fixed-point survival

Marker: `MTS_MATTER_COMPLETED_C3_FLOW_4929`.

**Decision:** visible matter, electromagnetism and the conditional ultraviolet
motion scalar do **not** destroy the Weyl-cubic fixed point at leading free-
spectator order in the natural optimized projection. The direct free-matter
source of the local `C^3` beta function is exactly zero in that projection,
all nine field-content benchmarks retain a positive non-Gaussian fixed point
with one relevant and one irrelevant direction, and a wide 6,642-row
regulator/matter stress test has no failed branch.

This is a real advance beyond the pure-gravity result, but not the complete
MTS ultraviolet flow. Interacting gravity-matter operators, anomalous
dimensions and the full six-derivative matter quotient enlarge the stability
matrix. The conditional coefficients below remain nonclaims, and the active
low-energy fallback remains one observable `A_+(Q_GW)`.

## 1. Source-locked field inventory

For `N_s` real scalars, `N_D` Dirac equivalents and `N_V` Maxwell fields,

```text
W0 =N_s+2N_V-4N_D,
W1 =sum_s(1-6xi_s)+2N_D-4N_V,
WC =N_s+6N_D+12N_V.
```

The two observed-matter anchors are

```text
SM without right-handed neutrinos: (N_s,N_D,N_V)=(4,22.5,12),
SM plus three right-handed neutrinos: (4,24,12).
```

Minimal and conformal Higgs endpoints are both tested. One additional real
minimal scalar is also tested as the conservative ultraviolet-active MTS
motion endpoint. This does not assert that the motion gap actually places the
mode at the fixed point.

## 2. Ricci-flat C3 spin theorem

The source-locked massive Ricci-flat coefficients, in units of
`[30240(4pi)^2m^2]^-1`, are

```text
real scalar       +1,
Dirac fermion     -4,
massive Proca     +3.
```

The determinant identity

```text
Proca = Maxwell plus one real scalar
```

therefore gives the Maxwell-plus-ghost weight `+2`. Consequently

```text
W3=N_s-4N_D+2N_V=W0.
```

This equality is not assumed from the quartic vacuum supertrace: it follows
independently from the three heavy-field coefficients and the Proca
determinant decomposition. Scalar nonminimal coupling does not alter this
Ricci-flat `C^3` identity because `R=0` there.

## 3. Exact optimized-regulator source gate

For a complete Laplace-type natural operator in four dimensions,

```text
Tr W(Delta)
 =(4pi)^-2 sum_n Q_(2-n)[W] integral sqrt(g) tr a_(2n).
```

The Newton term uses `a2 Q1`; the cubic-curvature term uses `a6 Q_-1`.
With the optimized spectral regulator

```text
R_k(z)=(k^2-z) theta(k^2-z),
W(z)=partial_t R_k/(z+R_k)=2 theta(k^2-z),
```

at zero matter anomalous dimension. Hence

```text
Q1[W]=2k^2,
Q_-1[W]=-W'(0)=0.
```

The leading free-spectator deformation of the locked 4928 system is therefore

```text
beta_g
 =beta_g^(grav)+W1 g^2/(6pi),

beta_h
 =beta_h^(grav),

g=k^2G_N,
h=k^2G_C3.
```

The `W1/(6pi)` coefficient follows from the `a2 Q1` supertrace and exactly
matches the matter increment in the independent 2014 matter-gravity source.
The zero in `beta_h` is narrower: it applies to free Laplace-type spectators,
zero anomalous dimensions and a regulator built from the complete natural
operator. It does not annihilate interacting mixed diagrams.

## 4. Proper-time firewall

The same `a6` coefficient in a massless proper-time local expansion gives

```text
c6       =1/[30240(4pi)^2]
         =2.0941051513379998e-7,

C_m      =W0 c6,
zeta_k   =C_m(1/k^2-1/Lambda^2),
h        =k^2 zeta_k,
beta_h   =beta_h^(grav)-2C_m.
```

It therefore approaches a shifted Gaussian coordinate `h=C_m` rather than
the physical `h=0` endpoint. Defining

```text
u=h-C_m
```

restores `beta_u=2u+O(g)` near the infrared Gaussian point. This is the same
massless local-derivative-expansion pathology exposed in checkpoint 4928. The
proper-time branch is retained as a stress test and is not used to predict a
Wilson coefficient.

## 5. Benchmark fixed points

The optimized free-spectator projection gives:

| benchmark | `W0` | `W1` | `g_*` | `h_*` | `(theta_g,theta_C3)` |
|---|---:|---:|---:|---:|---:|
| pure gravity | 0 | 0 | 0.589048623 | -3.2424843e-7 | (+2.782609,-7.750005) |
| SM45, minimal Higgs | -62 | 1 | 0.595709114 | -3.2567461e-7 | (+2.807537,-7.837994) |
| SM48, minimal Higgs | -68 | 4 | 0.616231010 | -3.2996553e-7 | (+2.888295,-8.113674) |
| SM45, conformal Higgs | -62 | -3 | 0.569609850 | -3.1998700e-7 | (+2.713268,-7.497244) |
| SM48, conformal Higgs | -68 | 0 | 0.589048623 | -3.2424843e-7 | (+2.782609,-7.750005) |
| SM45 minimal plus motion | -61 | 2 | 0.602459880 | -3.2710309e-7 | (+2.833435,-7.927910) |
| SM48 minimal plus motion | -67 | 5 | 0.623250457 | -3.3139875e-7 | (+2.917339,-8.209592) |

All nine optimized benchmarks and all nine proper-time diagnostic benchmarks
have a real fixed point below the gravitational pole. Every tested
two-coordinate stability matrix has one positive and one negative critical
exponent.

## 6. Wide survival test

The generator also tests

```text
optimized spectral: W1 in [-20,20], 81 rows;
proper-time hybrid: W0 in [-200,200] by 5,
                    W1 in [-20,20] by 0.5,
                    6561 rows.
```

Results:

```text
surviving rows                         =6642/6642,
g_* range                              =0.4743817483 to 0.7384500030,
theta_g range                          =+2.438262262 to +3.515909602,
theta_C3 optimized range               =-9.914379110 to -6.339334653,
theta_C3 proper-time diagnostic range  =-9.914578231 to -6.339184750.
```

This rejects the simple failure mode in which realistic free field counts
erase the fixed point or flip the `C^3` direction. It does not test new
stability eigenvalues belonging to omitted interacting operators.

## 7. Conditional MTS map

Integrating the unique optimized-spectator separatrix for every benchmark and
using the unchanged MTS map

```text
zeta_+=G_C3,
a_+=16pi G_N G_C3
```

gives

```text
A_C3 range       =2.997902513874431e-6
                   to 3.039651610736230e-6,

ell_+ range      =1.790736675667496e-36 m
                   to 1.796938874817633e-36 m,

max ratio to the selected neutron-star one-percent coefficient target
                 =7.163244442499543e-158.
```

The visible-matter deformation changes the conditional `A_C3` by less than
one percent in this leading projection. These numbers are compact-safe but
remain conditional because the full parent has not supplied the interacting
essential flow, regulator choice or transition scale.

## 8. Exact closure boundary

The two-coordinate calculation closes:

```text
integrated-H coordinate map,
Ricci-flat I1=C3 normalization,
free-field inventory,
free matter Newton trace,
optimized free-matter direct C3 source,
leading fixed-point survival.
```

It does not close:

```text
the essential scalar X^2 coordinate already present at four derivatives,
the additional six-derivative scalar-matter quotient,
gauge and fermion six-derivative operator blocks,
matter anomalous dimensions,
SM and MTS interaction vertices,
the complete cosmological/Ricci essential coordinates,
the full stability matrix and critical-surface dimension,
the motion-mode ultraviolet activation threshold,
the parent regulator and transition-scale selection.
```

The primary gravity-scalar source explicitly states that additional essential
matter couplings occur at six derivatives. The primary `C^3` source explicitly
presents gravity-matter completion as future work. The correct result is
therefore leading fixed-point survival, not a complete MTS ultraviolet proof.

## 9. Final gate

```text
Ricci-flat free-matter C3 weight          -> W3=W0 derived;
optimized free-spectator direct source    -> exactly zero;
free-matter Newton deformation            -> derived;
realistic benchmark fixed points          -> 18/18 projection rows survive;
wide two-coordinate robustness scan       -> 6642/6642 survive;
conditional compact hierarchy             -> overwhelmingly safe;
full interacting essential operator basis -> open;
full MTS critical surface                  -> open;
observational low-energy I1 parameters     -> exactly one A_+(Q_GW);
weak GR/Newton/Maxwell                     -> retained;
compact and full MTS-to-GR                 -> not promoted.
```

Direct next target:

`4930-Y5-R2FR-six-derivative-MTS-matter-essential-operator-basis-and-block-triangular-stability-or-Wilson-retention.md`

No GitHub action or public claim is authorized.

## Evidence

- `post-checkpoint-work/scripts/Y5_R2FR_4929_matter_completed_C3_flow.py`.
- `post-checkpoint-work/source-intake/functional_rg/4929/PROVENANCE.md`.
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_4929_NATURAL_QMINUS1_GATE.csv`.
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_4929_BENCHMARK_FIXED_POINTS.csv`.
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_4929_FIXED_POINT_ROBUSTNESS_SCAN.csv`.
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_4929_CONDITIONAL_COMPACT_MAP.csv`.
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_4929_ESSENTIAL_OPERATOR_CLOSURE.csv`.

