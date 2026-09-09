# Spherical wave constraints and O4 source-response derivation

2026-09-08. Private continuation. Heavy stellar/D4 runs remain paused.

## Result

This step derives the missing spherical source projections, not another
unspecified coupling. The retained O4 action now has an explicit two-dimensional
covariant stress formula, angular pressure, null-coordinate constraint equations
and a direct mass-source primitive. The previously missing canonical radial
metric corrections are also integrated through their first nonzero averaged
order, including the quartic interaction.

The fastest O4 stress grows as inverse wavelength on the one-ray seed, but its
leading direct mass contribution is a finite oscillation. This is an integrated
source result, not proof that high frequency is harmless or that the complete
coupled solution exists. The scalar response to O4 and the remaining metric
response cannot be discarded. The leading induced scalar response is derived
below, along with explicit linearized coupled equations and an integrated
fixed-geometry curvature-potential correction. There is no regular-centre or
completed MTS black-hole claim.

## 1. Source owners, conventions and scope

The immediate source is
`DERIVATION-20260908-Navier-Stokes-to-MTS-wave-stress-and-collapse-bridge.md`.
It contains the preceding leading wave/metric pair and the first scalar
harmonic correction, with 29 completed symbolic checks. The independent
four-dimensional stress owner is
`DERIVATION-20260907-O4-Hilbert-source-and-responsive-matter.md`.
The coframe/action and correspondence owners remain checkpoints 5203 and 5211
referenced in that preceding note. None of those frozen files is replaced here.

Use `(-,+,+,+)`, `c=hbar=1`, fixed RG scale, calibrated `G=G_N`, constant
Lambda, and `u=u_O4`. The geometric mass mu has dimensions length; the scalar
gap m_chi is distinct. The relevant action block is

```text
S = integral sqrt(-g) [ (R-2Lambda)/(16pi G)
                      -X/2-V(chi)+Q(X)-u W X ],
X = (nabla chi)^2,     V=m_chi^2 chi^2/2,
Q=b2 X^2+b3 X^3+...,  W=C_abcd C^abcd.
```

Other retained parent operators, the visible sector and the state functional
are not proved negligible by this calculation. The retained O4 source is
varied covariantly, following the established variational setting of
[Iyer and Wald](https://arxiv.org/abs/gr-qc/9403028). The mass convention is the
usual spherical geometric/Misner–Sharp one, with Lambda explicitly subtracted
from mu; see [Hayward](https://arxiv.org/abs/gr-qc/9408002) for the standard
geometric mass and trapping interpretation. The formulas below are derived
for this action, rather than imported as new MTS empirical coefficients.

## 2. Vary before fixing the null-coordinate gauge

Keep the general spherical metric

```text
ds^2 = h_AB(x) dx^A dx^B + R(x)^2 dOmega^2,
Y=(D R)^2, Z=Box_h R, R_h=scalar curvature of h,
U=R_h+2Z/R+2(1-Y)/R^2, W=U^2/3.
```

Here A,B label the two base coordinates, D is their Levi-Civita derivative,
and R is still an independent areal-radius field. The warped-product
curvature contractions give

```text
Riemann_4^2 = R_h^2+8|D D R|^2/R^2+4(1-Y)^2/R^4,
Ricci_4^2 = R_h^2/2-2R_h Z/R+4|D D R|^2/R^2
            +2(1-Y-RZ)^2/R^4,
R_4 = R_h-4Z/R+2(1-Y)/R^2.
```

Their combination `Riemann_4^2-2Ricci_4^2+R_4^2/3` yields the displayed W.
This reduction retains every spherical metric component. Gauge-fixing an
rr component to zero before variation would otherwise lose a field equation.

The reduced O4 action, apart from the integrated solid angle, is

```text
S4/(4pi) = integral sqrt(-h) [-u R^2 X U^2/3],
J = partial(-u R^2 X U^2/3)/partial R_h = -(2u/3)R^2 X U.
```

Define the base tensor

```text
B_AB = J Ricci_h,AB + h_AB Box_h J - D_A D_B J
       -(R_A J_B+R_B J_A)/R
       +h_AB[(D R.D J)/R+J Z/R-J Y/R^2].
```

Independent variations of h^(AB), the metric inside X, and R give the full
spherical O4 stress:

```text
T4_AB = 2u W chi_A chi_B - u X W h_AB - 2B_AB/R^2,
T4_ij = p4_perp g_ij,
p4_perp = -u X W + Box_h J/R^2 - 2J/R^4.                (1)
```

For example, the term containing Box_h R contributes
`-R_(A D_B)(2J/R)+(h_AB/2)D_C[(2J/R)D^C R]` to the reduced Euler
tensor. Combining it with the Y variation gives the last two terms of B_AB.
For the radius variation the Euler derivative simplifies to
`-2u R X W+2Box_h J/R-4J/R^3`; dividing by 2R gives p4_perp.
No angular or time-time equation has been inferred by simply deleting it.

Writing `Tcurv_AB=T4_AB-2uW chi_A chi_B`, its trace and exchange identities are

```text
h^AB Tcurv_AB+2p4_perp = 0,
D^A Tcurv_AB+(2/R)R^A Tcurv_AB-(2/R)R_B p4_perp
    = -u W D_B X.
```

Adding the metric variation of X restores
`nabla^a T4_ab = 2u nabla_a(W nabla^a chi) nabla_b chi` and
`T4^a_a=2uWX`, agreeing with the full four-dimensional owner. The source,
its angular pressure and the scalar force exchange belong to one action.

## 3. The exact retained equations in a horizon-regular gauge

Now choose R=r and

```text
ds^2 = -exp(2delta) F dv^2+2exp(delta)dvdr+r^2dOmega^2,
F=1-2mu(v,r)/r-Lambda r^2/3.
```

Useful explicit quantities are

```text
R_h = -F_rr-3F_r delta_r-2F(delta_rr+delta_r^2)
      -2exp(-delta)delta_vr,
Z=F_r+F delta_r, Y=F,
X=2exp(-delta)chi_v chi_r+F chi_r^2.
```

Set `P=1-2Q'(X)` and `L0=-X/2-V+Q`. The ordinary scalar source is
`T0_AB=P chi_A chi_B+h_AB L0`; the complete source for this retained block
is `T=T0+T4`, with angular part `L0+p4_perp`. The Einstein projections are

```text
delta_r = 4pi G r T_rr,
mu_r    = -4pi G r^2 exp(-delta) T_vr,
mu_v    = 4pi G r^2 [exp(-delta) T_vv+F T_vr].           (2)
```

For the canonical/nonlinear block these specialize to

```text
delta_r,0 = 4pi G r P chi_r^2,
mu_r,0 = 4pi G r^2 [P F chi_r^2/2+V+Q'X-Q],
mu_v,0 = 4pi G r^2 P chi_v[exp(-delta)chi_v+F chi_r].   (3)
```

The extra projections of (1) are added to these equations, not fitted.
The scalar equation, with `H=1-2Q'(X)+2uW`, is

```text
exp(-delta)/r^2 {
 partial_v(r^2 H chi_r)
 +partial_r[r^2 H chi_v+exp(delta)r^2 H F chi_r]
} -m_chi^2 chi = 0.                                   (4)
```

Equations (1)–(4), the angular equation and consistent boundary/initial data
provide explicit retained spherical field equations. There is no 1/F
coordinate singularity at a simple horizon. They are not an automatically
well-posed full UV theory: O4 introduces higher metric derivatives. For the
selected strict-EFT branch, evaluate its source at the preceding order and
solve the coupled perturbation equations without exciting independent
higher-derivative homogeneous modes. C3 and other same-order effects still
need their own retained treatment.

The boundary mass cannot be set to an arbitrary constant while the boundary
flux in the third equation of (2) is nonzero. Conservation and the scalar
equation control compatibility; a radial integral alone is not a solution of
the entire system.

## 4. Integrate the first ordinary radial metric corrections

On the preceding leading background, use

```text
F0=1-2mu0(v)/r-Lambda r^2/3,
chi0=epsilon A(v)cos(theta)/r, theta=v/epsilon,
mu0'=2pi G A^2.
```

At fixed r>=r_min>0 and finite slow time, phase averaging the first nonzero
radial sources in (3) gives

```text
<delta_r,0> = 2pi G epsilon^2 A^2/r^3+O(epsilon^3),
<mu_r,0> = pi G epsilon^2 A^2(F0/r^2+m_chi^2)
           +2pi G b2 epsilon^2 A^4/r^4+O(epsilon^3).    (5)
```

The b2 contribution survives although mean X is of higher order than its
oscillatory part. Define `I(r)=-1/r+mu0/r^2+(m_chi^2-Lambda/3)r`.
The source-generated radial differences from a reference r0 are

```text
<delta2(r)-delta2(r0)>
 = -pi G epsilon^2 A^2(r^-2-r0^-2),

<mu2(r)-mu2(r0)>
 = pi G epsilon^2 A^2[I(r)-I(r0)]
   +(2pi G b2 epsilon^2 A^4/3)(r0^-3-r^-3).            (6)
```

These fill the previously absent radial redshift and mass source responses.
The fast order-epsilon mass correction and the first/third scalar harmonics
remain those derived in the preceding note. The radial expressions are
particular source differences, not independent choices for the time-dependent
boundary data. A full order-epsilon-squared time-flux/field solution is not
claimed from (6).

## 5. An exact O4 radial-source primitive on the leading geometry

At delta=0, before assuming mu depends only on v, define

```text
U=-F_rr+2F_r/r+2(1-F)/r^2,
J=-(2u/3)r^2 X U,
K_boundary=2F J_r+2J_v+(2F/r-F_r)J.
```

The independent lapse variation of the reduced action yields the exact
identity for the direct O4 contribution in (2):

```text
-r^2 T4_vr = u r^2 W F chi_r^2 + partial_r K_boundary.
```

Consequently its radial source integral is

```text
Delta mu4,direct(r)-Delta mu4,direct(r0)
 =4pi G [K_boundary(r)-K_boundary(r0)]
  +4pi G u integral_(r0)^r s^2 W F chi_s^2 ds.         (7)
```

This is a derived boundary improvement plus a bulk term, not a guessed
screening factor. A conservative absolute bound follows by taking absolute
values of both boundary terms and of the bulk integrand. If the scalar is
smoothly compactly supported and its required jets vanish at two endpoints,
the boundary improvement vanishes there; it need not vanish at an interior
sphere or an imposed finite outer boundary.

The adjective direct matters. The total first-order-u mass response also
contains the induced ordinary stress from changes in chi and g. One may not
report (7) alone as the complete physical response.

## 6. Evaluate the fast part instead of treating it as an unknown bound

For the Vaidya-type seed, `U=12mu0/r^3`, `W=48mu0^2/r^6`, and

```text
X = epsilon A^2 sin(2theta)/r^3+O(epsilon^2),
J = -8u mu0 X/r.
```

The full curvature-variation part of (1) gives the leading fast components

```text
T4_vv =  64u mu0 A^2 sin(2theta)/(epsilon r^6)+O(u),
T4_vr = -128u mu0 A^2 cos(2theta)/r^7+O(u epsilon),
T4_rr = -192u mu0 epsilon A^2 sin(2theta)/r^8
         +O(u epsilon^2).                             (8)
```

The explicit `2uW chi_A chi_B` term starts at a later epsilon order in each
displayed component and is retained in (1), not declared zero. The constants
implicit in (8) depend on a fixed finite annulus, slow-time derivatives and
fixed coefficients; this is not a uniform assertion as r approaches zero.

Substitution into (2), including both the radial and temporal mass equations,
gives compatible leading fast particular responses

```text
Delta mu4,fast = -128pi G u mu0 A^2 cos(2theta)/r^4,
delta4,fast   =  128pi G u mu0 epsilon A^2 sin(2theta)/r^6.  (9)
```

They include the integration choice fixed by these displayed oscillations;
the homogeneous boundary functions still require the full boundary equations.
The order-epsilon^-1 source in T_vv is a differentiated improvement: its
integrated mass amplitude is finite at fixed radius. Equivalently,

```text
|Delta mu4,fast| <= 64 |u mu0 mu0'|/r^4.              (10)
```

This does not allow an arbitrarily large frequency at fixed EFT cutoff.
Derivatives of this bounded metric oscillation still grow with frequency,
and the full stress/curvature validity and hyperbolicity bounds remain needed.
The radial growth r^-4 in (9) also rules out interpreting this perturbative
formula as a regular-centre result.

## 7. The remaining coupled response is now an explicit calculation

Writing `g=g0+h4`, `chi=chi0+xi4` at first order in u, the response equations
have the form

```text
[D_g(Einstein-8pi G T0)] h4 -8pi G (D_chi T0) xi4
      =8pi G T4[g0,chi0],

(D_chi E0)xi4+(D_g E0)h4
      =-2u nabla_a(W[g0] nabla^a chi0).               (11)
```

The displayed wave seed has its own finite-order residual, so its residual
must also appear on the right until a sufficiently accurate g0,chi0 has
been constructed. Omitting it would turn an approximate reference into a
fictional exact solution. Ordinary stress variation is of the same relevant
order as the direct O4 source and is not assumed silent.

For example, kinetic transport alone changes the leading scalar amplitude to
`A/[r sqrt(1+2uW)] = (A/r)(1-uW)+O(u^2)`. Its induced ordinary stress cancels
the leading kinetic-weight change at fixed transported intensity; this is
why varying the complete source rather than only K is essential. The fast
boundary improvement in (9) is not removed by asserting that mean X vanishes.

### 7.1 Explicit linearized fluxes, not unspecified functional derivatives

At a reference with delta0=0, write `d=Delta delta`, `f=Delta F=-2M/r`,
`xi=Delta chi`, and define `a=chi_v`, `b=chi_r`, `B=a+F b`.
Here B is a scalar transport combination, not the tensor B_AB in (1).
All unvaried quantities in the following equations are reference fields:

```text
Delta X = 2b xi_v+2B xi_r-2d a b+f b^2,
P=1-2Q'(X),       Delta P=-2Q''(X) Delta X,

S_r = P F b^2/2+V+Q'X-Q,
S_v = P a B,

R_delta = (delta0)_r-4pi G r P b^2,
R_r     = (mu0)_r-4pi G r^2 S_r,
R_v     = (mu0)_v-4pi G r^2 S_v.
```

The three first-order residual equations are

```text
d_r/(4pi G r)
 = Delta P b^2+2P b xi_r+T4_rr-R_delta/(4pi G r),

M_r/(4pi G r^2)
 = Q''(X)(X-F b^2)Delta X+P f b^2/2+P F b xi_r
   +V'(chi)xi-T4_vr-R_r/(4pi G r^2),

M_v/(4pi G r^2)
 = Delta P a B+P xi_v B
   +P a(xi_v+F xi_r+f b-d a)
   +T4_vv+F T4_vr-R_v/(4pi G r^2).                  (12)
```

Thus neither the variation of Q nor the change in the matter flux is
silently removed. For the scalar, set

```text
D0 = {partial_v(r^2 P b)+partial_r(r^2 P B)}/r^2,
E0 = D0-V'(chi),

Delta E0 = {partial_v[r^2(Delta P b+P xi_r)]
            +partial_r[r^2(Delta P B
                           +P(xi_v+F xi_r+f b+d F b))]}/r^2
           -d D0-V''(chi)xi.
```

Its first-order equation is

```text
Delta E0 = -E0
           -(2u/r^2){partial_v(r^2 W b)+partial_r(r^2 W B)}. (13)
```

The residuals are explicit because the wave reference is approximate.
Equations (12)-(13) are linear in the corrections and the direct O4 source;
products of u with corrections and quadratic corrections are omitted here.
If those terms enter the requested mixed epsilon/u accuracy, they must be
restored. These equations alone do not supply a uniform two-parameter error
estimate or license an arbitrary choice of boundary integration functions.

### 7.2 A leading induced scalar response is solved

On the slow reference geometry, the particular response

```text
xi4 = -u W chi0 = -u W epsilon A cos(theta)/r          (14)
```

cancels the order-u epsilon^0 term in
`(box-m_chi^2)xi4+2u div(W grad chi0)`. The remaining fixed-geometry
residual is order u epsilon on a fixed smooth finite annulus. The metric
responses (9) and variation of Q also enter at subsequent orders for this
one-ray seed; they are not omitted from (12)-(13).

In particular,

```text
2(chi0)_v (xi4)_v + 2uW (chi0)_v^2 = O(u epsilon).
```

This demonstrates the leading ordinary-stress cancellation of the explicit
kinetic-weight term. It does not cancel the order-u/epsilon improvement
in (8), remove all order-u source terms, or establish a complete solution.

There is also an exact fixed-metric explanation when Q=0. For
`K=1+2uW>0` and `chi=psi/sqrt(K)`, the scalar equation becomes

```text
div(K grad chi)-m_chi^2 chi
 = sqrt(K)[box psi-V_eff psi],

V_eff = m_chi^2/K + box K/(2K) - (grad K)^2/(4K^2)
      = m_chi^2+u(box W-2m_chi^2 W)+O(u^2).           (15)
```

The leading amplitude change is therefore a derived kinetic normalization;
the next scalar correction sees an explicit curvature-dependent potential.
This identity does not remove the metric coupling: K depends on curvature,
and its full metric variation remains the source (1). For nonzero Q, the
nonlinear kinetic terms transform too and must remain in the response.

### 7.3 Integrate the new potential's scalar correction

For the Vaidya-type reference, direct differentiation gives

```text
box W = -960mu0 mu0'/r^7+1440mu0^2/r^8
        -3456mu0^3/r^9-288Lambda mu0^2/r^6,

V_eff = m_chi^2+u V4+O(u^2),
V4 = -960mu0 mu0'/r^7+1440mu0^2/r^8-3456mu0^3/r^9
     -(288Lambda+96m_chi^2)mu0^2/r^6.                (16)
```

The normalized scalar's additional particular correction from this
potential alone is `Delta psi_V=u epsilon^2 B_V sin(theta)`, where

```text
(r B_V)_r=A V4/2,

H_V(r)=80mu0 mu0'/r^6-720mu0^2/(7r^7)+216mu0^3/r^8
       +(144Lambda+48m_chi^2)mu0^2/(5r^5),

B_V=A[H_V(r)-H_V(r0)]/r.                            (17)
```

At fixed geometry and Q=0, `(box-m_chi^2)Delta psi_V-u V4 chi0`
has no order-u epsilon term. This is an integrated response, not another
free coefficient. The homogeneous function and the earlier ordinary scalar
correction remain subject to boundary conditions. As before, (17) is not a
regular-centre expansion.

This isolates one contribution to the next-order problem; (17) deliberately
does not claim to include metric response, nonzero-Q cross-terms or a full
coupled remainder. The next finite calculation is to combine it with those
terms in (12)-(13) and the ordinary epsilon-squared flux residuals, then
propagate a bound on the total mass correction rather than only (7).

## 8. Trapping criterion and honest completion boundary

In this gauge the normalized future expansions are
`theta_l=exp(delta)F/r` and `theta_n=-2exp(-delta)/r`. On a reference sphere
with `F0<=-sigma<0`, a sufficient sign-preservation condition is

```text
2 |Delta mu_total|/r < sigma,
```

with finite real delta. Equation (10) supplies an explicit contribution
`128 |u mu0 mu0'|/r^5` to the corresponding F-error budget. Equations (6)
and the preceding fast-mass bound supply other particular terms. The missing
coupled remainder is not set to zero. These conditions establish a route to
a controlled trapped-sphere calculation, not a global event-horizon or
singularity-resolution theorem.

No new numeric parent coefficient or astrophysical initial amplitude is
invented in this step. No observable pass, empirical preference, regular
black-hole core, scalar preparation or complete unification claim is promoted.

## 9. Reproducible checks

Companion: `scripts/spherical_wave_O4_constraints_20260908.py`.
Its fresh run directory is
`source-intake/navier-stokes/20260908/spherical-O4-constraints-initial/`.
The script writes its executed source, incremental `status.json`, and a
`COMPLETE` marker only when every check passes. It checks the general
null-coordinate Einstein projections, spherical Weyl contraction, O4 trace
and exchange identities, independent metric variations, the Einstein-vacuum
Weyl-Hessian limit, source primitive, fast coefficients, and the averaged
canonical/quartic radial primitives. These are symbolic identities, not an
evolution or a Lean verification. Actual results must be read from the output;
their count is not assumed from this document being written.

The separate, serial companion
`scripts/spherical_wave_response_linearization_20260908.py` checks the flux
linearizations with nonzero quartic and sextic coefficients, (14), its
leading kinetic-stress cancellation, the fixed-metric identity (15), and
the explicit potential and integrated scalar response (16)-(17).
It uses the fresh directory
`source-intake/navier-stokes/20260908/spherical-O4-response-initial/`, with
the same source snapshot, incremental-status and completion-marker policy.

All new work remains under post-checkpoint-work. The previous 29-check wave
result, pinned OpenAI sources and interrupted stellar/D4 runs are preserved.

### Completed verification

Both serial runs completed with SymPy 1.14.0: **31/31** source/constraint
checks at `2026-09-08T22:18:21Z`, and **16/16** response checks at
`2026-09-08T22:19:22Z`. Every recorded remainder is exactly symbolic zero.
Both status files retain `valid_for_mts_completion_claim=false`.

The general EF geometry checks allow arbitrary F(v,r) and delta(v,r).
The evaluated O4 trace, Ward, independent-variation and primitive checks
use the Vaidya-type reference with arbitrary smooth mu(v) and X(v,r);
they are not a computer proof on every four-dimensional metric. The
general spherical formulas additionally follow from the explicit covariant
variation in section 2. The response flux tests instantiate Q with both
quartic and sextic terms; the kinetic-normalization and potential-response
identities have the separately stated Q=0 scope.

Executed-source SHA-256 values, matched to both the live scripts and their
preserved snapshots:

```text
constraints: 9beb28b047b011da7f9904620ce0ef70af54418c4b036831a69b51fad7ed9bb9
response:    abf34c9ca7a0628e585ecdad8f0bcdd91e12d4d5fc858fa6a2554fc2d93b811a
```

Completion markers and cited immediate local paths were checked. No scripts
bytecode directory was created. Each run used one logical CPU and completed
before the other began. Because unrelated processes starved BelowNormal work,
only the identified validation worker was changed to Normal scheduling while
retaining its one-core affinity; no other process was changed or stopped.
Both validation workers have exited. These checks establish the listed
identities and finite-order cancellations, not a numerical collapse result,
an EFT validity bound, or a formal global-existence proof.
