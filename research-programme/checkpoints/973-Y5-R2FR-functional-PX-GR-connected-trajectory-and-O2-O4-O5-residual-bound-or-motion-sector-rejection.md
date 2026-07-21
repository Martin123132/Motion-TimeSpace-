# 4957 - Functional `P(X)` GR-connected trajectory and local residual gate

Date: 2026-07-13

Marker: `MTS_FUNCTIONAL_PX_O4_GR_TRAJECTORY_DECISION_4957`.

Status: private analytic, source-locked and numerically executed checkpoint.
This checkpoint joins the 4956 functional motion germ to the completed
scalar-backreacted `C3-CFF-F4-O4` gravity system, follows its unique
GR-connected relevant direction into the Gaussian infrared regime, and
tests the local `O2/O4/O5` residuals. It establishes a regular local
trajectory in the declared truncation. It does not yet identify the raw
off-shell `X2/X3` coordinates with the essential on-shell six-point
amplitude, establish a global fixed function, or promote full MTS.

## 1. Combined running system

The parent coordinates are

```text
(g,g_plus,g_minus,g_CFF,h_C3,u_O4,p_k(X)).
```

The functional `P_k(X)` Hessian and normalization are those derived and
independently calibrated at 4956. Scalar backreaction and the completed
`O4=C^2 X` portal enter the parent flow with the optimized-regulator weights

```text
Delta beta_g   =g^2(1-eta_psi/4)/(6pi),
Delta beta_hC3 =eta_psi/(483840pi^2),
w_C2           =1-eta_psi/8,
w_RC2          =1-eta_psi/6,
beta_uO4       =(4+eta_psi)u_O4-gamma_C2/2.
```

The direct natural Type-II `O4` source remains zero because
`Q_0[zW]=(zW)(0)=0`; its nonzero metric-kernel source and backreaction are not
deleted. Two scheme brackets are propagated:

```text
dynamic_etaN:   eta_N=beta_g/g-2 self-consistently;
reference_etaN0: eta_N=0 only in the P(X) graviton regulator,
                 while the physical eta_N=beta_g/g-2 is still recorded.
```

In both cases `eta_psi` is solved algebraically rather than inserted as a
fixed number.

## 2. Combined fixed points and predictivity index

The Gaussian-connected functional sequence closes numerically through
`N=8` in both schemes. The `N=8` endpoints are

```text
                         dynamic eta_N       reference eta_N=0
g*                       0.130882969333       0.130882397156
g_plus*                  0.371890320676       0.371839960607
g_minus*                 3.45695645182        3.45651118713
g_CFF*                   0.00410179783958     0.00410103021708
h_C3*                    3.92884969627e-6     3.92742061213e-6
u_O4*                   -0.00183556368044    -0.00183189374008
eta_psi*                -0.0658659641517     -0.0580527591720
a2*                     -0.123156600094      -0.0902637541778
a3*                      0.116465171256       0.0707926212194
r3_raw,UV                3.83928800255        4.34441408142
```

The scaled fixed-point residuals are below `3.57e-14`. The combined ratio
coordinate stability matrix has exactly one relevant direction for `N=6`
and `N=8` in both schemes. At `N=8` its beta eigenvalue is

```text
-1.89264114256  dynamic eta_N,
-1.89266164565  reference eta_N=0.
```

This is a finite-dimensional predictivity result for the declared
truncation, not a theorem about the untruncated theory.

## 3. GR-connected infrared trajectory

The source-selected separatrix is integrated in ratio coordinates

```text
A_n=a_n/g^n,
W_O4=u_O4/g^2
```

from the fixed point to `g=10^-10`. All four runs (`N=6,N=8` in both
schemes) reach the target. The `N=8` endpoints are

```text
                         dynamic eta_N       reference eta_N=0
eta_psi                 -4.24413182134e-11  -4.24413182087e-11
eta_N,physical          -1.60481494760e-9   -1.60482116485e-9
A2                      -202.041347165      -200.186812009
A3                       65.3451425064       65.3451417857
W_O4                     -3.32252495617      -3.32241776364
r3_raw                    8.00392116728e6     8.15290500445e6
```

The `N=6` to `N=8` relative differences in `A2`, `A3`, `W_O4`, raw `r3`
and the raw six-point kernel are all below `4.86e-7`, much tighter than the
declared `10^-3` order gate.

## 4. Regularity and derivative residuals

The direct full metric-motion Hessian is sampled at five points along each
`N=8` trajectory. Every sample is scalar-convex on `0<=x<=0.1`; the minimum
singular value over the complete scan is

```text
sigma_min=0.336372084499.
```

The local derivative firewall is now sharper:

```text
P(X), n>=2: first and quadratic variations vanish on psi=0;
O2:          quadratic Hessian vanishes on psi=0 by scalar degree four;
O4:          eta_psi-weighted trajectory included, while stress and scalar
             source vanish on psi=0 and the scalar cone remains metric;
O5:          forbidden by the selected psi -> -psi parent reflection.
```

Therefore none of these operators obstructs the 4947 local
Einstein-to-Poisson-to-Newton or Maxwell-to-Lorentz-to-stress-to-Poynting
chain on the selected homogeneous motion branch. `O2` remains open for
nonzero-background motion states, and the Taylor chart remains certified
only on `x<=0.1`.

## 5. Raw versus essential six-point coordinate

The trajectory does not permit the raw polynomial ratio to be called the
physical 4954 amplitude coefficient. Since

```text
a2=A2 g^2,
a3=A3 g^3,
r3_raw=a3/(2a2^2)=[A3/(2A2^2)]/g,
```

the raw `r3` grows as `1/g`. The stable asymptotic combinations are

```text
g r3_raw=8.00392116728e-4  dynamic eta_N,
g r3_raw=8.15290500445e-4  reference eta_N=0.
```

The corresponding raw dimensionless `2->4` kernel at `g=10^-10` is

```text
5.81182256554e-64  dynamic eta_N,
5.81182248840e-64  reference eta_N=0,
```

with relative scheme spread `1.33e-8`. This decay is useful, but it is not
yet an observable rate. Field redefinitions and equation-of-motion
redundancies can move strength between the six-derivative `X3` contact and
exchange operators. The next calculation must either construct the
six-derivative essential quotient or compute the invariant on-shell `2->4`
amplitude directly along the trajectory.

## 6. Physics decision

Checkpoint 4957 is a substantive positive step:

```text
combined gravity-motion fixed point through N8      = retained;
one GR-connected relevant direction                 = retained;
functional trajectory to the Gaussian GR regime    = retained;
N6/N8 infrared low-coordinate convergence           = passed;
local x<=0.1 full-Hessian regularity                 = passed;
O2 local linear residual                            = exact zero;
O4 anomalous-dimension trajectory                   = included;
O5 reflection-odd closure                           = forbidden;
4947 local GR/Newton/Maxwell branch                  = retained;
raw infrared six-point kernel                        = derived;
physical essential six-point amplitude              = open;
global fixed function and nonzero-state O2 flow      = open;
full MTS unification                                 = false.
```

This means the programme now contains a concrete route from one interacting
gravity-motion fixed point to a locally GR/Newton/Maxwell infrared branch.
The remaining six-point obstacle is no longer “find an arbitrary
coefficient”; it is the precise basis-independent amplitude matching
problem stated above.

## 7. Artifacts

- `post-checkpoint-work/scripts/Y5_R2FR_4957_functional_PX_O4_GR_trajectory.py`
- `post-checkpoint-work/scripts/Y5_R2FR_4957_functional_PX_O4_GR_trajectory_validation.py`
- `post-checkpoint-work/source-intake/functional_rg/4957/PROVENANCE.md`
- `post-checkpoint-work/source-intake/functional_rg/4957/functional_PX_O4_GR_trajectory_results.json`
- `post-checkpoint-work/source-intake/functional_rg/4957/combined_functional_fixed_point_convergence.csv`
- `post-checkpoint-work/source-intake/functional_rg/4957/combined_functional_stability_spectrum.csv`
- `post-checkpoint-work/source-intake/functional_rg/4957/functional_PX_O4_GR_trajectory.csv`
- `post-checkpoint-work/source-intake/functional_rg/4957/infrared_motion_coordinate_convergence.csv`
- `post-checkpoint-work/source-intake/functional_rg/4957/trajectory_functional_regularity_gate.csv`
- `post-checkpoint-work/source-intake/functional_rg/4957/local_operator_residual_gate.csv`
- `post-checkpoint-work/source-intake/functional_rg/4957/functional_trajectory_decision.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_BRR545_4957_VALIDATION.csv`

## Next target

`4958-Y5-R2FR-six-derivative-essential-X2-X3-quotient-and-invariant-2to4-amplitude-or-rate-route-rejection.md`

Construct the complete six-derivative redundant-operator map and quotient the
raw `X2/X3` trajectory by field redefinitions and lower equations of motion.
Prefer a direct on-shell `2->4` amplitude projection if it bypasses the basis
ambiguity. Only the resulting invariant coefficient may be inserted into the
4954 galaxy-formation kernel. Do not fit the quotient, infer it from raw
`r3`, or disturb the retained 4947 local branch.

