# 5210 - Parent Vacuum Coordinate: Local-Invariant, CTP/RG Source and Renormalization-Datum Theorem

Private derivation and boundary checkpoint. No GitHub action and no
cosmological-constant, full-MTS or full-local-GR claim.

Marker: `MTS_5210_PARENT_VACUUM_COORDINATE_RENORMALIZATION_DATUM_THEOREM`.

## Executive result

This checkpoint closes the repeated `Lambda_cal=0` fork for the parent that
has actually been constructed.

The constant volume operator

```text
S_vac=-integral d4x e U_Lambda,
U_Lambda=M_R^2 Lambda_cal,
C0_R=-M_R^2 Lambda_cal
```

is allowed by diffeomorphisms, local Lorentz symmetry, the relational local
translation gauge symmetry, visible `U(1)` and the motion `Z2`/constant-shift
limits. It is not a boundary term: on compact boundaryless flat `T4`,
`integral e=V4>0`, while a globally defined total divergence integrates to
zero. It is not topological because `e^A_mu -> a e^A_mu` sends the integral
to `a^4 V4`.

No existing parent symmetry therefore sets its coefficient to zero.

The Schwinger-Keldysh/CTP identity does not do it either:

```text
Gamma_C0[g,g]=0,

delta Gamma_C0 / delta g_a^mn |_(g_a=0)
 =-C0 sqrt(-g_r) g^r_mn/2 !=0.
```

CTP normalization cancels the diagonal value of vacuum bubbles, not their
stress in the physical metric equation.

Finally, the explicitly resolved optimized scalar trace gives

```text
partial_t C0_E = k^4/[32 pi^2(1+w)],
w=m^2/k^2,

u0=C0_E/k^4,

beta_u0
 =-4u0+W0/[32 pi^2(1+w)].
```

Hence `u0=0` is not an invariant RG surface when `W0!=0`. For one massless
real scalar,

```text
beta_u0(0)=3.166286988823e-03,
u0*=7.915717472058e-04,
d beta_u0/d u0=-4,
theta0=+4.
```

The canonical real-motion-scalar plus public-`U(1)` matter block has
`W0=1+2=3`, not zero. A larger gravity/ghost calculation may shift this
coordinate, but no unsourced term can be called a cancellation.

The result is not “MTS predicts zero.” It is the sharper and usable result:
**the present parent owns `Lambda_cal` as one universal renormalized
calibration datum, fixed once and never retuned by arena.**

## 1. Exact symmetry boundary

The volume density is a scalar density under Diff and a determinant under
local Lorentz/translation-gauge transformations. It contains no charged
field and no motion scalar. Consequently every selected gauge and discrete
symmetry permits it.

The compact-`T4` witness is enough to reject the only possible
boundary-term escape inside the current local action:

```text
integral_T4 d4x partial_mu J^mu=0,
integral_T4 d4x e=V4>0.
```

The coefficient is therefore a genuine local action coordinate modulo
boundaries. This is a statement about the selected parent basis, not a
no-go theorem against constructing a different unimodular, four-form,
sequestered or supersymmetric theory. None of those mechanisms occurs in
the checkpoint-5203 canonical parent action.

## 2. CTP variation theorem

Write the doubled vacuum term as

```text
Gamma_C0^CTP=C0[V(g_+)-V(g_-)].
```

At `g_+=g_-` the value is zero by unitarity. The physical equation is
obtained by variation in the difference direction before taking that
limit, and that variation is nonzero. The one-variable determinant proxy
used by the executable gate gives

```text
Gamma=-C0[sqrt(x+g_a/2)-sqrt(x-g_a/2)],
Gamma|_(g_a=0)=0,
dGamma/dg_a|_(g_a=0)=-C0/(2*sqrt(x)).
```

This exactly mirrors the tensor equation already derived at checkpoint
4876. CTP state normalization cannot be used to remove `Lambda_cal`.

## 3. RG non-invariance theorem

For the Litim/optimized scalar regulator, the vacuum projection of the
Wetterich trace is

```text
1/2 integral_(p^2<k^2) d4p/(2pi)^4
 [2k^2/(k^2+m^2)]
 =k^4/[32pi^2(1+w)].
```

The symbolic fixed-coordinate residual is
`0`. The source at zero is nonzero for the
locked primitive branches:

```text
W0=1                         real motion scalar;
W0=3                         real scalar + public U(1);
W0=-62                       imported SM benchmark without RH neutrinos.
```

None is zero. The sign of an imported spectrum does not matter for the
present theorem; nonzero `W0` is enough to show that zero is not invariant.
The finite motion mass only multiplies this source by `1/(1+w)` and cannot
create an exact zero at finite `w`.

A technically stable zero would require a parent Ward identity or exact
supertrace cancellation that enforces

```text
beta_u0|_(u0=0)=0
```

through thresholds and interactions. No such identity is present in the
resolved parent.

## 4. Fixed-point coverage and parameter count

Checkpoint 4934 solved the source-complete minimal fixed point in

```text
(g, g_plus, g_minus, g_CFF, h_C3).
```

It found one relevant direction **inside that
5-coordinate truncation**.
`u0`, `C0` and `Lambda_cal` are absent. Its stability index therefore
cannot count or select the vacuum direction.

The canonical calibration Jacobian over

```text
coordinates:
 (ln M_R^2,ln Z_A,ln M_psi^2,ln Z_psi,ln Lambda_cal);

observables:
 (ln G_N,ln alpha_EM,ln m_pole^2,ln Lambda_cal)
```

has

```text
rank=4,
nullity=1.
```

The one null direction is the elementary field normalization. The
`Lambda_cal` column is independent. Checkpoint 5209 independently showed
that the homogeneous state constraint has rank one over
`(Omega_Lambda,sigma2)` and that nonlinear `P(X)` moments increase rather
than remove the nullity. The vacuum cannot be transferred into a hidden
state closure.

## 5. Radiative-stability diagnostic

The checkpoint-4876 one-real-scalar Newton matching gives

```text
Lambda_UV/Mbar=4pi sqrt(6)
 =3.078119592388e+01.
```

In that declared cutoff scheme,

```text
C0_loop=Lambda_UV^4/(64pi^2)
 =4.999065726080e+112 eV^4;

rho_crit=3 Mbar^2 H0^2
 =3.687823843998e-11 eV^4;

C0_loop/rho_crit
 =1.355559792861e+123.
```

This is a regulator-dependent counterterm-sensitivity diagnostic, not an
observable probability and not a claimed calculation of the measured
vacuum. It does show why the tiny finite-motion threshold from checkpoint
5209,

```text
|Delta Omega_vac,mass|
 <=8.781062042761e-123,
```

cannot dynamically cancel the independent quartic coordinate.

## 6. What the data do and do not say

The checkpoint-5195 primary internal fits give

```text
Lambda-free parent:
 chi2=1473.978273644249;

Lambda-zero parent:
 chi2=1474.069080719807;

zero minus free:
 Delta chi2=0.090807075558;
 Delta AIC=-1.909192924442;
 Delta BIC=-7.315296305679.
```

Neither branch hits a prior edge. The zero branch pays one fewer parameter
and therefore wins this conditional AIC/BIC comparison despite a
`0.0908071` worsening in chi-squared.
That is legitimate model comparison. It is **not** a derivation that the
parent action owns exact zero.

Both branches remain useful empirical tests. The free branch supplies one
universal calibration; the zero branch remains an explicitly imposed
renormalization condition.

## 7. Local propagation without retuning

Using the free-branch internal calibration

```text
H0=67.492044194411 km s^-1 Mpc^-1,
Omega_Lambda=0.488762527346,
Lambda_cal=7.805160260508e-53 m^-2,
```

the Schwarzschild-de Sitter weak-field terms are

```text
Phi(r)=-GM/r-Lambda_cal c^2 r^2/6,
a_r=-GM/r^2+Lambda_cal c^2 r/3.
```

The single calibration propagates to

```text
Lambda L^2 at 50 micrometres
 =1.951290065127e-61;

a_Lambda/a_Newton at Earth surface
 =1.517005010987e-30;

a_Lambda/a_Newton at Saturn
 =5.190517980275e-20;

Lambda L^2 at 100 kpc
 =7.431610080403e-10.
```

The direct Maxwell portal remains zero; `Lambda_cal` enters only through
the universal metric. These are background residuals, not substitutes for
the full PPN, clock, orbital or R10 projection. They establish that retaining
one calibrated vacuum datum does not obstruct the local-GR branch at this
order.

## 8. Decision

The derive-first search has produced a definite negative theorem for the
existing zero route:

1. no selected symmetry forbids the volume operator;
2. it is neither boundary nor topological;
3. CTP normalization leaves its physical stress;
4. the explicit matter FRG sources it at zero;
5. the current fixed point does not contain the coordinate;
6. `P(X)` state moments do not select it.

The project should therefore stop reopening `Lambda_cal=0` as though one
more rearrangement of the same parent might prove it. The honest competitive
field-theory route is:

```text
one universal Lambda_cal renormalization/calibration;
no arena-by-arena retuning;
both free and zero cosmology branches retained as declared tests;
resume derivation of universal source coupling and the local-GR residual vector.
```

If a future vacuum prediction is wanted, it is a separate ultraviolet
calculation: add `u0` to a source-complete parent Hessian and derive a Ward
or supertrace identity. The existing “one relevant direction” statement
cannot be used for it.

Selected next route:

```text
RESUME_UNIVERSAL_SOURCE_COUPLING_AND_LOCAL_GR_WITH_ONE_FROZEN_LAMBDA_DATUM
```

## Reproducibility

Evidence CSV digest:

```text
b35b0137d25d39e6aa7e9841f098cb7bafcb5b8b1ce4fcf15242b6e0f8f2ab4d
```

Run:

```text
python scripts/Y5_R2FR_5210_parent_vacuum_coordinate_ownership.py --dry-run
python scripts/Y5_R2FR_5210_parent_vacuum_coordinate_ownership.py
python scripts/Y5_R2FR_5210_parent_vacuum_coordinate_ownership.py --validate-saved
```
