# Adapted wave energy and entry to coupled stability

2026-09-09. Private, derivation-first continuation. No subagents or public
repository action. The preceding turn made progress: it added explicit
mass/lapse coefficients and independently tested the angular equation.

## Main result

There is a useful structural cancellation, not just another condition to
check. For the retained reference wave family, a wave-adapted energy current
removes an apparent inverse-wavelength growth term from the scalar energy
estimate. Its exact divergence identity is derived below. The associated
linear scalar estimate can be uniform as epsilon tends to zero on a fixed
exterior annulus. The linear metric-to-scalar forcing is also explicit and
is O(epsilon) as an operator from the stated metric H1 norm into L2.

This is not yet a uniform stability theorem for the coupled Einstein/MTS
system. The remaining issue is now more specific: close a compatible metric
error estimate, with the differentiated physical mass correction restored,
instead of assuming the improved mass controls that correction for free.

## 1. Sources, domain and order reduction

Preserved sources:

- `RESULT-20260909-oscillatory-mass-correction-and-angular-equation.md`.
- `DERIVATION-20260908-spherical-wave-constraints-and-O4-mass-response.md`.
- `DERIVATION-20260909-wave-energy-flux-and-mean-mass.md`.
- `source-intake/navier-stokes/20260909/annular-constraint-correction-initial/status.json`.

Use the same action block, signature, kappa=4pi G and calibrated G:

```text
L0=-X/2-m_chi^2 chi^2/2+b2 X^2+b3 X^3,
L4=-u W X,
ds^2=-e^(2delta)F dv^2+2e^delta dvdr+r^2dOmega^2,
F=1-2mu/r-Lambda r^2/3,
P=1-4b2 X-6b3 X^2,  Px=dP/dX=-4b2-12b3 X.
```

Work with the sourced finite families on 0<=v<=0.5, 4<=r<=8, and a
periodic fast phase theta=v/epsilon. Choose actual spacelike slices

```text
t=v-sigma(r-4), sigma=1/20, 0<=t<=0.3.                (1)
```

They fit inside that entire v/r rectangle; a slope-one slice would not.
In formulas below partial_v is the physical derivative, including the fast
phase. Derivatives partial_r hold v fixed unless explicitly stated otherwise.

Strict first-order-u perturbation means differentiating the field equations
at u=0. Schematically, if Y=(g,chi),

```text
E0(Y0)=0,
DE0(Y0) Y1 = -E4(Y0).                                (2)
```

For an approximate Y0, its residual is retained as forcing instead. The
highest-derivative O4 source is evaluated on Y0, not promoted to new
higher-derivative homogeneous modes of Y1. This is the specified perturbative
branch, not a proof that the untruncated finite-u theory is well posed.
In particular P+2uW is not the principal coefficient of (2) after secretly
resumming some higher-order terms. The principal scalar operator of (2)
uses P and Px at u=0, while metric perturbations and the O4 current are kept.

## 2. Derive the scalar principal matrix

Let eta be a scalar variation, with the metric held fixed for this first
calculation. For s^a=nabla^a chi,

```text
delta X=2s^a partial_a eta,
delta(P nabla^a chi)=(P g^ab+2Px s^a s^b)partial_b eta,
A^ab=P g^ab+2Px s^a s^b.                             (3)
```

The two radial contravariant components of s are
s^v=e^-delta chi_r and s^r=e^-delta chi_v+F chi_r. Define rho=e^delta r^2
and the densitized principal coefficients

```text
a=rho 2Px(s^v)^2,
b=rho[P e^-delta+2Px s^v s^r],
c=rho[P F+2Px(s^r)^2].                               (4)
```

Here a,b,c are principal coefficients, not the earlier scalar harmonic names.
Direct calculation gives

```text
det(A_radial)=-e^(-2delta) P(P+2XPx),
P+2XPx=1-12b2 X-30b3 X^2.                            (5)
```

P>0 and P+2XPx>0 select the ordinary Lorentzian branch, including positive
angular principal directions. A chosen time slice must also be spacelike
for this cone: a-2sigma b+sigma^2 c<0. Equation (5) alone does not certify a
chosen boundary value problem or every background of the full theory.

The radial scalar equation is

```text
partial_v(a eta_v+b eta_r)+partial_r(b eta_v+c eta_r)
       -rho m_chi^2 eta = f.                         (6)
```

The source f includes the explicit metric variation and residual; these
have not been set to zero in the coupled problem.

## 3. An exact energy identity without the dangerous leading derivative

For arbitrary smooth a,b,c with b nonzero, choose

```text
d=c/(2b)-beta, beta>0 constant,
T=partial_v+d partial_r,
Q=a eta_v^2+2b eta_v eta_r+c eta_r^2,
J^v=(a eta_v+b eta_r)T eta-Q/2,
J^r=(b eta_v+c eta_r)T eta-d Q/2.                    (7)
```

Using (6), the exact density identity is

```text
partial_v J^v+partial_r J^r
 =(f+rho m_chi^2 eta)T eta
   +Dvv eta_v^2+2Dvr eta_v eta_r+Drr eta_r^2,
Dvv=-(a_v+d a_r+a d_r)/2,
Dvr=(a d_v-b_v-d b_r)/2,
Drr=-c b_v/(2b)+beta c_r/2-c^2 b_r/(4b^2).           (8)
```

The c_v term cancels entirely from Drr. In Dvr it occurs only as
a c_v/(4b), since d_v=c_v/(2b)-c b_v/(2b^2). This is checked symbolically
for arbitrary coefficient functions, not inferred from the fixtures.

For comparison, T=partial_v gives the deformation matrix -partial_v A/2.
Bounding its entries separately sees c_v directly and can produce an
unhelpful growth constant proportional to epsilon^-1. The adapted estimate
avoids that particular loss. It is not necessarily sharper at each of the
moderate wavelengths tested; the issue is its uniform small-epsilon behavior.

## 4. Why the cancellation is effective for the actual family

The explicit reference fields have

```text
chi=epsilon A(v)cos(theta)/r+O(epsilon^2),
chi_r=O(epsilon), chi_v=O(1),
delta=O(epsilon^2), F=F0+O(epsilon),
X=O(epsilon),
a=O(epsilon^2), b=r^2+O(epsilon),
c=r^2 F0-8b2 A(v)^2 sin^2(theta)+O(epsilon).          (9)
```

The order-one term in c oscillates rapidly when b2 is nonzero, even though
X is small: the wave gradient is nearly null, not uniformly small in every
component. Thus c_v can be O(epsilon^-1). However

```text
a_v=O(epsilon), a_r=O(epsilon^2),
b_v=O(1), b_r=O(1), c_r=O(1), a c_v=O(epsilon).       (10)
```

Equations (8)-(10) give bounded D/rho as epsilon tends to zero. These
orders follow from the finite Fourier coefficient functions, smooth slow
data and r>=4, not from pretending the physical derivative is a slow one.
The canonical b2=b3=0 case has a=0 exactly and no order-one fast term in c.

Let C=c/rho at epsilon=0. Here
C=F0-8b2 A^2 sin^2(theta)/r^2. From the given exact A, mu0'=kappa A^2/2
and parameters, 0.49<C<=0.75 throughout the limiting two-case rectangle.
This conservative bound includes the nonlinear/modulated case and all phases.

Set beta=1. The positive slice energy density is

```text
-J^t=sigma J^r-J^v
 =Hvv eta_v^2+2Hvr eta_v eta_r+Hrr eta_r^2,
Hvv=sigma b-a(1+sigma d)/2,
Hvr=(sigma c-a d)/2,
Hrr=sigma c d/2-bd+c/2.                              (11)
```

At epsilon=0, H/rho has entries
sigma, sigma C/2, and 1-sigma C/2+sigma C^2/4. Its determinant is
sigma(1-sigma C/2), its trace is at most 1+sigma, and therefore its smaller
eigenvalue is at least

```text
sigma(1-sigma*0.75/2)/(1+sigma) > 0.0467.             (12)
```

The explicit coefficient family extends continuously to epsilon=0 at fixed
(v,r,theta). Compactness, (10) and the strict limiting margins give some
epsilon_star>0 with uniform energy coercivity and bounded deformation on
0<epsilon<=epsilon_star. This establishes the small-epsilon structural
statement; the numerical tests do not certify that epsilon_star is 0.4.
They sample that larger interval independently.

## 5. Boundaries and the conditional scalar estimate

The gradient current (7) deliberately leaves the scalar mass term on the
right side of (8). This avoids silently losing its boundary flux. With
Delta=sqrt(b^2-ac), define

```text
k_plus=(-b+Delta)/c, k_minus=(-b-Delta)/c.
```

One homogeneous no-incoming choice for an error problem is
eta_r=k_plus eta_v at r=4, and eta_r=k_minus eta_v at r=8. At either root,
J^r=+/-Delta(1+d k_plus/minus)eta_v^2. The plus sign at the inner boundary
and minus at the outer give nonpositive net energy input if
1+d k_plus/minus>0. These factors have positive limits and the sampled signs
are checked. Nonzero incoming error data must instead enter the estimate
through their boundary flux. These conditions are not asserted to be the
unique physical incident data of the MTS parent or already compatible with
every Einstein constraint.

Augment the gradient energy by a positive zeroth-order term,

```text
E(t)=integral_[4,8] [ (eta_v,eta_r) H (eta_v,eta_r)^T
                     +rho eta^2/2 ] dr.             (13)
```

For smooth solutions, suppose h_* is a lower bound on lambda_min(H/rho),
D_* bounds the spectral norm of D/rho, d_* bounds |d|, and
rho_* bounds |rho_v|/rho. These are coefficients of the explicit problem,
not adjustable physics parameters. Set

```text
C_T=sqrt((1+d_*^2)/h_*),
C_0=D_*/h_*+sqrt(2)m_chi^2 C_T+sqrt(2/h_*)+rho_*.
```

Integration of (8), Cauchy-Schwarz and (13) give

```text
E' <= incoming_flux + C_0 E + C_T ||f/sqrt(rho)||_2 sqrt(E).
```

With no incoming error flux,

```text
sqrt(E(t)) <= exp(C_0 t/2) [sqrt(E(0))
 + (C_T/2) integral_0^t exp(-C_0 s/2)||f(s)/sqrt(rho)||_2 ds]. (14)
```

The constants can be uniform for the small-epsilon family just established.
Consequently an O(epsilon^3) source in this actual norm, with compatible
O(epsilon^3) initial error, would yield O(epsilon^3) scalar error in the
energy norm over this fixed time slab. A sampled maximum-residual slope is
not itself certification of those continuum-norm and boundary hypotheses.
Equation (14) is an a priori estimate for the stated linear scalar problem,
not a completed proof of coupled existence or nonlinear stability.

## 6. Retain and bound the metric-to-scalar coupling

Now vary within the same areal-null gauge: nu=delta mu, zeta=delta delta,
and eta=delta chi. The metric part of the kinetic variation is

```text
x_h=-2e^-delta zeta chi_v chi_r-(2nu/r)chi_r^2,
delta X=2e^-delta chi_r eta_v
        +2(e^-delta chi_v+F chi_r)eta_r+x_h.
```

The scalar density current variation is exactly A_density grad(eta)+M,
where

```text
M^v=r^2 Px x_h chi_r,
M^r=r^2 Px x_h(chi_v+e^delta F chi_r)
      +rho P(F zeta-2nu/r)chi_r.                     (15)
```

This is derived by differentiating both original scalar currents; it is not
an ansatz for an effective coupling. The complete linear scalar equation is

```text
div(A_density grad eta)-rho m_chi^2 eta
 +div M-rho m_chi^2 chi zeta
 =-2 div(r^2 W chi_r, r^2 W chi_v+rho W F chi_r)       (16)
```

per unit u, plus any reference/approximation residual. The O4 current on
the right is evaluated on the reference, as required by (2).

Writing M^i=M_zeta^i zeta+M_nu^i nu gives

```text
M_zeta^v=O(epsilon^2), M_nu^v=O(epsilon^3),
M_zeta^r=O(epsilon),   M_nu^r=O(epsilon),
partial_v M_zeta^v+partial_r M_zeta^r-rho m_chi^2 chi=O(epsilon),
partial_v M_nu^v+partial_r M_nu^r=O(epsilon).          (17)
```

There is no unsuppressed chi_vv zeta/nu term in this gauge. All six
coefficients of zeta_v, nu_v, zeta_r, nu_r, zeta and nu in the last two
terms on the left of (16) are evaluated explicitly by the script.

Define the metric norm, not assumed to be already controlled,

```text
E_g=integral rho [nu^2+zeta^2+nu_v^2+nu_r^2+zeta_v^2+zeta_r^2] dr.
```

If C_M bounds sqrt(6) times the largest absolute normalized coefficient
in (17), then

```text
||(div M-rho m_chi^2 chi zeta)/sqrt(rho)||_2 <= C_M sqrt(E_g),
C_M=O(epsilon).
```

Thus the scalar energy inequality contains an explicit
C_T C_M sqrt(E E_g) coupling. Young's inequality turns this into
E+(C_T^2 C_M^2/4)E_g: an O(epsilon^2) coefficient multiplying the stated
metric norm, not an assumed zero coupling. Closing an evolution estimate
for E_g in the same gauge and compatible boundaries remains necessary.

## 7. The metric equations that must close it

They are not missing from the action. Let f_F=-2nu/r, V'=m_chi^2 chi and
DeltaX be the full variation above. Differentiating the ordinary Einstein
projections gives

```text
zeta_r=kappa r[Px DeltaX chi_r^2+2P chi_r eta_r]+S_delta,
nu_r=kappa r^2[P F chi_r eta_r+V' eta+P f_F chi_r^2/2
               -Px e^-delta chi_v chi_r DeltaX]+S_r,
nu_v=kappa r^2[Px DeltaX chi_v(e^-delta chi_v+F chi_r)
      +P(2e^-delta chi_v+F chi_r)eta_v+P F chi_v eta_r
      -P e^-delta chi_v^2 zeta+P chi_v chi_r f_F]+S_v. (18)
```

The S terms are the sourced O4 projections already owned by the exact
stress note, plus error residuals when comparing approximations. They are
not free closure coefficients. These equations have bounded coefficients
of eta and its first derivatives on the reference family. However the
radial lapse equation alone does not automatically supply the zeta_v norm
needed by (17), nor the compatible initial/boundary constraint evolution.
Treating (18) as an arbitrary unconstrained transport system would evade
that issue. The scalar current and metric constraints must be reduced
together, or a justified equivalent hyperbolic gauge must be constructed.

There is an additional visible high-frequency cost. The leading physical
mass response is

```text
M0=-32kappa mu0 A^2 cos(2theta)/r^4,
partial_v M0=64kappa mu0 A^2 sin(2theta)/(r^4 epsilon)+O(1). (19)
```

Its amplitude remains bounded while its time derivative grows as
epsilon^-1. For a finite coupling the contribution is u times (19). An
unweighted small-C1 perturbation argument therefore cannot be uniform at
fixed nonzero u without further work. This is not proof of a physical
instability: one may need a joint coupling/wavelength regime or a controlled
normal-form estimate. In the latter case the physical restoration
mu=N+kappa K and derivatives of K must be bounded explicitly. A small
improved-mass residual is not permission to discard (19).

Equation (19) is the derivative of the known response, not a lower bound
on the error relative to that response. Subtracting the correctly restored
oscillatory approximation may remove its leading contribution to the error.
That cancellation must be controlled in the coupled estimate; u/epsilon
is not being announced as a necessary, gauge-independent physical bound.

## 8. Actual calculation and matched controls

Companion: `scripts/annular_acoustic_energy_20260909.py`.
Completed output:
`source-intake/navier-stokes/20260909/annular-acoustic-energy-initial/`.
Result: 29/29 checks, completed 2026-09-09T00:55:14.504539+00:00.
Script and executed snapshot SHA-256:
`1bed84145ce7d207600e84f4ed8cd4897da1156aadbcc4f08b5f0f5a9ceb78aa`.

Nine checks are exact identities: the general current divergence, slice
energy, three fast-derivative cancellations, acoustic determinant and three
kinetic/current linearization checks. Twenty further gates cover two matched
fixtures, their cone/energy/boundary signs, predicted scalings and phase
refinement. They are not 29 independent empirical tests.

The same reference fixtures are sampled at three slow times, five radii,
64 phases, eight wavelengths from 0.4 down to 0.003125 and a finest-wavelength
128-phase refinement. The coupled mass response is separately inspected,
not substituted for the reference principal coefficients in (2).

| Diagnostic slope versus epsilon | Canonical | Nonlinear/modulated |
| --- | ---: | ---: |
| Adapted deformation norm | 0.000 | -0.000 |
| Unadapted deformation norm | -0.000 | -0.988 |
| Metric-current/zeroth-order coefficient norm | 1.000 | 1.000 |
| Physical mass response norm | -0.000 | -0.000 |
| Physical mass time-derivative norm | -1.000 | -1.000 |

At epsilon=0.003125 the smaller energy eigenvalue is about 0.04963/0.04965,
the adapted deformation norm about 0.28126/0.28058, and the illustrative
energy constants C0 about 12.016/12.316, CT about 5.611/5.618.
These sampled constants are diagnostics, not certified continuum suprema.
The nonlinear unadapted deformation grows from about 0.000512 at epsilon=0.4
to 0.04413 at epsilon=0.003125; the adapted one stays near 0.28058.
Phase refinement changes the recorded diagnostics by less than 0.30%.

The per-unit-u physical mass time derivative grows from approximately
0.000625/0.000686 to 0.07977/0.08795 over that same wavelength range. It is
not hidden in the scalar estimate. There are 18 diagnostic rows and 10
measured slopes. All physical-claim flags remain false.

An additional companion,
`scripts/annular_energy_metric_bridge_checks_20260909.py`, independently
checks all three ordinary Einstein-source variations in (18), the limiting
energy determinant/trace, exact rational limiting cone/energy bounds and
the time-slab geometry. Its completed run is
`source-intake/navier-stokes/20260909/annular-energy-metric-bridge-final/`:
21/21 checks at 2026-09-09T01:04:50.706709+00:00, consisting of nine
mathematical/domain checks and twelve provenance/integrity checks.
Script and executed snapshot SHA-256:
`5532936f649afd0f7dd01ebcd6d493f415b55f84cb889ca35b95a7d388d44496`.
The energy-run source and input hashes, marker, row/check counts and compile
checks pass. No bytecode cache or live owned calculation worker remains.
The limiting rational C lower bound is greater than 0.49425, so the stated
0.49 margin is conservative. These checks do not certify a numerical
epsilon_star for the full finite-wavelength coefficient family.

## 9. What this changes and the next finite step

This fills a real part of the stability argument: an exact energy identity,
a uniform-small-epsilon scalar estimate for the specified family and boundary
class, and an explicit bounded metric-to-scalar coupling operator. It avoids
mistaking a poor energy multiplier for a demonstrated instability. It does
not derive local GR, G, a regular centre or the complete MTS theory from this
single retained block.

Next reduce the scalar current and (18) into a compatible coupled error
system, retaining the known K restoration. Derive control of zeta_v and the
restored mass derivative, or exhibit the precise wavelength/coupling bound
that is needed. A short coupled evolution should then test that actual
initial/boundary problem, rather than extend the formal series by another
order or declare this partial energy estimate a full solution.
