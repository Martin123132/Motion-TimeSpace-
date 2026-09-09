# Oscillatory mass correction and the angular Einstein equation

2026-09-09. Private continuation; no GitHub action. Heavy D4/stellar jobs
remain paused. This step used no additional agents.

## Result in plain language

The leading oscillatory mass error has been removed from the retained
approximation by deriving a new mass coefficient, not by averaging the
error away. The corresponding lapse corrections are also explicit. A
separate evaluation of the angular Einstein equation improves at the
predicted order, alongside the other constraints, in both matched branches.

The symbolic construction passes 28/28 checks. The same numerical evaluator
passes 34/34 checks before and 34/34 after the corrections. These are checks
of a two-case, finite-annulus approximation, not 96 independent physical
discoveries or a completed black-hole solution. A further 48/48 artifact
integrity checks establish ownership and reproducibility, not new physics.

## 1. Source owners and retained setting

The existing fields are frozen in
`source-intake/navier-stokes/20260909/annular-assembly-initial/` and described
in `RESULT-20260909-annular-wave-assembly-and-residual-scaling.md`.
The exact stress and angular pressure owner is
`DERIVATION-20260908-spherical-wave-constraints-and-O4-mass-response.md`.
The improved mass identity is derived in
`DERIVATION-20260909-wave-energy-flux-and-mean-mass.md`.
The already solved next mean law is recorded in
`DERIVATION-20260909-next-averaged-mass-evolution.md`.

Use kappa=4pi G, signature (-,+,+,+), fixed coefficients, and

```text
ds^2 = -e^(2delta) F dv^2 + 2e^delta dvdr + r^2 dOmega^2,
F = 1-2mu/r-Lambda r^2/3,
L0 = -X/2 - m_chi^2 chi^2/2 + b2 X^2 + b3 X^3,
L4 = -u W X,  X=(nabla chi)^2,  W=C_abcd C^abcd=U^2/3.
```

This is the retained spherical action block, first order in u. Other parent
operators have not been proved absent. G and the numerical fixture
coefficients are supplied, not derived from the parent in this test.

Write theta=v/epsilon and distinguish slow partial_v from the physical
derivative D_v=partial_v+epsilon^-1 partial_theta. The old fields are

```text
chi_ref = epsilon a + epsilon^2 b + epsilon^3 c,
chi = chi_ref + u(epsilon p + epsilon^2 q + epsilon^3 s),
mu_ref = mu0 + epsilon mu1 + epsilon^2 mu2,
mu = mu_ref + u(M0 + epsilon M1 + epsilon^2 M2),
delta_ref = epsilon^2 d2 + epsilon^3 d3,
delta = delta_ref + u(epsilon ell1 + epsilon^2 ell2).
```

The additions are epsilon^3 mu3, u epsilon^3 M3, epsilon^4 d4 and
u epsilon^3 ell3. No earlier coefficient or scalar field is changed.
M2 and M3 denote physical mass coefficients, not merely improved ones.

## 2. Derive the periodic mass corrections

Define F_n=-2mu_n/r for n>=1 and the reference kinetic coefficients

```text
t0=a_theta,  t1=a_v+b_theta,  t2=b_v+c_theta,
X1=2t0 a_r,
X2=2(t0 b_r+t1 a_r)+F0 a_r^2,
X3=2(t0 c_r+t1 b_r+t2 a_r-d2 t0 a_r)
   +2F0 a_r b_r+F1 a_r^2.
```

Let E_ij be the u^i epsilon^j coefficient of the matter flux

```text
r^2 H (D_v chi) [e^-delta D_v chi + F chi_r],
H=1-4b2 X-6b3 X^2+2uW.
```

The ordinary temporal equation gives the actual forcing

```text
partial_theta mu3 = kappa E_02 - partial_v mu2.         (1)
```

The right side has exactly zero phase mean for both assembled cases,
using the previously evolved ordinary boundary mean. For a Fourier
coefficient f_n exp(i n theta), n nonzero, the periodic primitive is
f_n exp(i n theta)/(i n). We choose the new homogeneous mean to be zero.
The code rejects a nonzero mean; it does not silently subtract one. The
oscillatory boundary value mu3(v,R,theta) need not vanish: it is determined
by flux, not reset to an incompatible constant mass.

For the coupled equation use J=-(2u/3)r^2 XU and

```text
K=2F J_r+2e^-delta D_v J+B J,
B=2F/r-F_r-2F delta_r,
N=mu-kappa K.
```

The exact retained flux identity is
D_v N=kappa[matter_flux-(D_v F)J_r-(D_v B)J].
Write J/u=epsilon j1+epsilon^2 j2+epsilon^3 j3+... and

```text
j1=-(2/3)r^2 X1 U0,
j2=-(2/3)r^2(X2 U0+X1 U1),
j3=-(2/3)r^2(X3 U0+X2 U1+X1 U2),
B0=2F0/r-F0_r,  B1=2F1/r-F1_r,
B2=2F2/r-F2_r-2F0 d2_r,
G2=-(F0_v+F1_theta)j2_r-(F1_v+F2_theta)j1_r
   -(B0_v+B1_theta)j2-(B1_v+B2_theta)j1.
```

For N2=M2-kappa K2, the next improved mass obeys

```text
partial_theta N3 = kappa(E_12+G2)-partial_v N2.         (2)
```

Again the phase mean is exactly zero in both cases, rather than merely
small numerically. Its zero-mean periodic primitive is explicit. Equations
(1)-(2) are coefficient recurrences; their exact primitive and solvability
checks here apply to the two sourced fixtures, not every possible datum.

## 3. Lapse corrections and restoration of physical mass

The next ordinary radial lapse source is

```text
d4_r=kappa r[b_r^2+2a_r c_r-8b2 X1 a_r b_r
             +(-4b2 X2-6b3 X1^2)a_r^2].              (3)
```

Let Xu1 be the u epsilon coefficient of X; W0=U0^2/3 and
W1=2U0 U1/3 are ordinary curvature coefficients. The coupled source is

```text
ell3_r=kappa r[2a_r q_r+2b_r p_r+4W0 a_r b_r
               -8b2 X1 a_r p_r+(-4b2 Xu1+2W1)a_r^2]
       +(2kappa/r)[j3_rr+2j3_r/r-d2_r j1_r].         (4)
```

Both are integrated from the same reference radius R=4, with d4(R)=ell3(R)=0.
Laurent radial terms integrate exactly; a power r^-1 produces log(r/R),
which is regular on the chosen annulus. This fixes the new lapse boundary
normalization, not the mass flux or an entire exact solution.

Restoring M3 requires one further coefficient of J because D_v differentiates
its fast phase. With the corrected ordinary geometry,

```text
U3=-F3_rr+2F3_r/r-2F3/r^2
   -3(F0_r d3_r+F1_r d2_r)-2(F0 d3_rr+F1 d2_rr)
   -2(d3_vr+d4_theta,r-d2 d2_theta,r)
   +2(F0 d3_r+F1 d2_r)/r,
X4=2[t1 c_r+t2 b_r+c_v a_r-d2(t0 b_r+t1 a_r)-d3 t0 a_r]
   +F0(b_r^2+2a_r c_r)+2F1 a_r b_r+F2 a_r^2,
j4=-(2/3)r^2(X4 U0+X3 U1+X2 U2+X1 U3),
K3=2(F0 j3_r+F1 j2_r+F2 j1_r)+2j3_v+2j4_theta
   -2d2(j1_v+j2_theta)-2d3 j1_theta
   +B0 j3+B1 j2+B2 j1,
M3=N3+kappa K3.                                       (5)
```

Thus the reference d4 and mu3 must be included before reconstructing M3.
The physical M3 also has zero phase mean in these fixtures, as checked
exactly. The reference scalar remains truncated at epsilon^3: equation (5)
does not prove its epsilon^4 coefficient vanishes in the exact solution.
Adding a later scalar coefficient changes X4, j4 and M3 consistently.

## 4. Check the angular equation directly

For the general spherical warped metric,
R_theta^theta=(1-F-rZ)/r^2 and
R4=Rh-4Z/r+2(1-F)/r^2. Consequently
G_theta^theta=Z/r-Rh/2, where

```text
Z=F_r+F delta_r,
Rh=-F_rr-3F_r delta_r-2F(delta_rr+delta_r^2)
   -2e^-delta D_v delta_r,
Box_h J=2e^-delta D_v J_r+F J_rr+Z J_r,
p4=-uXW+Box_h J/r^2-2J/r^4.
```

The independently evaluated residual is therefore

```text
Eangular=Z/r-Rh/2+Lambda-2kappa(L0+p4).                (6)
```

The code calculates (6) from the explicit fields; it does not replace it
with zero using the other constraints or a Bianchi argument. The same
evaluator is used before and after, with no changes to the equations.

## 5. Actual matched numerical results

The cases, sampling and analytic derivative method are unchanged: kappa=0.1,
mu0(0)=1, v in {0,0.25,0.5}, five radii spanning [4,8], epsilon in
{0.4,0.2,0.1,0.05,0.025}, and 32 phases plus a 64-phase refinement.
The canonical case uses A=0.1 and Lambda=m_chi=b2=b3=0. The nonlinear case
uses A=0.1(1+v/10), Lambda=0.001, m_chi=0.2, b2=0.05, b3=0.02.

The ordinary reference is GR with the same scalar matter, not vacuum GR
or LambdaCDM. The coupled column is the coefficient of u, not a finite-u
total residual or a measured MTS coupling. Fourth-order physical v/r Taylor
jets are combined with exact first-order-u arithmetic. Thirty derivative
coefficients are checked against an independent analytic test expression.

Measured slopes after correction, using the finest three wavelengths:

| Residual | Canonical reference | Canonical coupled | Nonlinear reference | Nonlinear coupled |
| --- | ---: | ---: | ---: | ---: |
| Scalar | 3.000 | 3.000 | 3.000 | 3.000 |
| Temporal mass, unaveraged | 3.000 | 3.000 | 3.003 | 3.004 |
| Radial mass | 4.000 | 4.000 | 4.000 | 3.995 |
| Radial lapse | 5.003 | 4.000 | 5.002 | 4.000 |
| Angular Einstein equation | 4.000 | 3.008 | 4.000 | 3.001 |
| Phase-mean temporal mass | 4.000 | 4.000 | 4.000 | 4.000 |

The temporal mass improved from order 2 to 3; radial mass from 3 to 4;
reference/coupled lapse from 4/3 to 5/4; and reference/coupled angular
residual from 3/2 to 4/3. The scalar residual remains order 3. Mean-mass
errors remain small and largely unchanged: an extra mean cancellation is
not the source of the improvement. Their observed fourth order is not a
new uniform theorem, especially near floating-point cancellation scales.

Within each branch, the before/after error ratios at epsilon=0.025 are:

| Residual | Canonical reference | Canonical coupled | Nonlinear reference | Nonlinear coupled |
| --- | ---: | ---: | ---: | ---: |
| Temporal mass | 321 | 152 | 343 | 120 |
| Radial mass | 160 | 41 | 268 | 205 |
| Radial lapse | 1283 | 11 | 566 | 122 |
| Angular Einstein equation | 404 | 22 | 53 | 223 |

These factors compare each approximation with its own previous truncation,
not MTS observational performance against GR. All targeted metric residuals
decrease. Doubling phase resolution changes after-correction maxima by less
than 0.56%. Removing the epsilon^3 scalar terms still gives order-2 scalar
residuals in both branches; restoring them gives factors about 638, 158,
266 and 721 respectively. The sampled reference F remains positive.

## 6. Reproducibility and scope

All run directories below are under
`source-intake/navier-stokes/20260909/` and contain status, executed source
and COMPLETE. Existing inputs remain preserved.

| Run | Checks | Completion UTC |
| --- | ---: | --- |
| annular-constraint-correction-initial | 28/28 exact coefficient checks | 00:39:45 |
| annular-angular-before-initial | 34/34 numerical checks | 00:39:49 |
| annular-angular-after-initial | 34/34 numerical checks | 00:40:15 |
| annular-correction-evidence-final | 48/48 integrity checks | 00:41:58 |

Scripts and SHA-256:

- `scripts/annular_constraint_correction_20260909.py`:
  `f0e915d39a76d6e39dc8402f3acb44f5be21816fac56eb75bc8c91999cce88bf`.
- `scripts/annular_angular_residuals_20260909.py`:
  `0977046836620929019c0ca6169d5be1fecdbb95243179ed5be40732b77f9496`.
- `scripts/annular_correction_evidence_check_20260909.py`:
  `9b50d2ffa5804077412547247714814fb310658bb3d7011556a271b16e50b92a`.

The evidence check verifies source/snapshot hashes, upstream ownership,
COMPLETE timestamps, 44 residual/control rows and 24 slopes per test, finite
values, and preservation of all old field coefficients and parameters.
Only the four requested coefficient orders were added. Sources compile
in memory and no scripts/__pycache__ is present. The derivation and initial
reference test briefly overlapped as two single-core BelowNormal jobs;
the final residual test completed in about eight seconds. All have exited.
No RH/Desktop Commander process was stopped or reconfigured.

All run-level physical-claim flags remain false. This does establish a
stronger explicit approximate solution of the retained exterior equations.
It does not establish an exact coupled solution, a uniform continuum
residual bound, finite-u EFT control, horizon/centre regularity, or the
viability of the complete MTS framework. No external Navier-Stokes result
is being treated as a theorem for these gravitational equations.

## 7. Next finite target

Do not continue adding formal orders indefinitely as a substitute for
control. Derive the principal part and a residual-to-solution energy estimate
for the order-reduced perturbation problem on this annulus, with compatible
initial/boundary data and explicit dependence on epsilon and u. In particular,
check derivative loss and whether the stability constant grows as wavelength
shrinks. A short matched evolution is useful only once that problem and its
boundary conditions are specified. Extending to a horizon or regular centre
requires separate validity checks, not extrapolation from r in [4,8].
