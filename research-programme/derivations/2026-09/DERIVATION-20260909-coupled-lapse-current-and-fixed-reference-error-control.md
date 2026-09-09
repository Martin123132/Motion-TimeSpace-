# Coupled lapse current and fixed-reference error control

2026-09-09. Private continuation. Previous goal turn: progress, with an
exact adapted scalar energy identity and explicit metric-current variation.

## Result and scope

The missing lapse time derivative can be recovered from the scalar current
and radial Einstein constraint without requiring second derivatives of the
unknown scalar error. This supplies the previously unclosed metric norm in
the scalar estimate. On the stated finite annulus, sufficiently small
epsilon, a common prescribed reference and compatible data, the estimates
below close a linear coupled a priori error bound. This is a conditional
estimate for smooth solutions, not an existence theorem or a nonlinear MTS
stability result.

A second useful correction is important: the known fast physical mass term
cancels exactly from the response error when both responses use the same
reference and exact restoration. Its large derivative is not by itself an
error obstruction. Changing the reference reintroduces a specific
restoration difference, whose derivative requirements are displayed below.

## 1. Preserved sources and definitions

Sources:

- `DERIVATION-20260909-adapted-wave-energy-and-coupled-stability-entry.md`.
- `DERIVATION-20260909-wave-energy-flux-and-mean-mass.md`.
- `RESULT-20260909-oscillatory-mass-correction-and-angular-equation.md`.
- `source-intake/navier-stokes/20260909/annular-constraint-correction-initial/status.json`.

Retain the same first-order-u spherical action block, kappa=4pi G, prescribed
reference (mu,delta,chi), and scalar principal density A with entries a,b,c.
The null-coordinate metric has F=1-2mu/r-Lambda r^2/3 and rho=e^delta r^2.
Set P=1-4b2 X-6b3 X^2 and Px=-4b2-12b3 X. Derivatives v are physical,
including the fast phase. Let eta,nu,zeta denote scalar, mass and lapse
variations or differences of responses to this same linearized problem.

Let M^v,M^r be the full metric-current variations derived in the preceding
note. Define the complete linear scalar currents

```text
Pi = a eta_v+b eta_r+M^v,
Psi= b eta_v+c eta_r+M^r,
Pi_v+Psi_r-rho m_chi^2(eta+chi zeta)=F_chi.             (1)
```

F_chi is the density source/residual in the actual current equation, not
the coordinate-normalized scalar residual. The three metric equations are
the verified Einstein-source variations in the preceding note, with
sources S_delta,S_r,S_v. Their compatibility with (1) is not optional.

## 2. Rewrite the lapse constraint using the scalar current

Define two background coefficients

```text
gamma=kappa chi_r/r,  beta_l=kappa r P chi_r.
```

Substituting the exact a,b and M^v gives the identity

```text
zeta_r = gamma Pi + beta_l eta_r + S_delta.            (2)
```

This retains the Px DeltaX chi_r^2 term of the Einstein equation, including
its metric variation. It is not a canonical-only simplification.

Differentiate (2) in v and use (1). Integrate the two radial derivatives
by parts, rather than bounding eta_vr as an additional unknown. Define

```text
B_l=beta_l eta_v-gamma Psi,
Z_l=zeta_v-B_l,
V_l=gamma_v Pi+gamma_r Psi+beta_l,v eta_r-beta_l,r eta_v
    +gamma rho m_chi^2(eta+chi zeta).
```

Then the exact residual-inclusive identity is

```text
partial_r Z_l = V_l + gamma F_chi + partial_v S_delta, (3)

zeta_v(v,r)=zeta_v(v,r_b)+B_l(v,r)-B_l(v,r_b)
 +integral_(r_b)^r [V_l+gamma F_chi+partial_v S_delta](v,s) ds. (4)
```

All quantities multiplying eta,eta_v,eta_r,nu,zeta in (4) are explicit
background coefficients. There is no second derivative of the unknown
eta. There is one derivative of the prescribed lapse source S_delta; that
requirement must be checked, not silently replaced with an L2 source bound.

For example, the coefficient of eta_v in B_l is exactly

```text
beta_l-gamma b=-2kappa r Px chi_r^2(e^-delta chi_v+F chi_r),
```

which is O(epsilon^2), not O(1). The eta_r coefficient is -gamma c,
of order epsilon. The source/metric terms in B_l remain included.

## 3. Bounds and causal radial reconstruction

For the sourced near-null family, chi_r=O(epsilon), chi_v=O(1), while
chi_rv=O(1). The preceding principal coefficients satisfy
a=O(epsilon^2), b,c=O(1), b_v=O(1). Direct expansion of (2)-(4) gives

| Coefficient group | Uniform small-epsilon order |
| --- | --- |
| B_l acting on eta,eta_v,eta_r | epsilon |
| B_l acting on nu,zeta | epsilon^2 |
| V_l acting on eta,eta_v,eta_r | 1 |
| V_l acting on nu,zeta | epsilon^2 |
| Radial Einstein equations: scalar-to-metric | epsilon |
| Radial Einstein equations: metric-to-metric | epsilon^2 |
| Temporal mass equation: scalar/metric coefficients | bounded |

These follow from the explicit formulas, including physical fast derivatives,
and are checked on both numerical fixtures. They do not hold for every
arbitrary background with a large radial scalar gradient.

Use the same spacelike coordinate t=v-sigma(r-4), sigma=1/20, on
Omega_T={0<=t<=T,4<=r<=8}, with T<=0.3. At fixed v choose

```text
r_b(v)=min(8,4+v/sigma).                              (5)
```

For a point in Omega_T, integration from r_b to r uses only the same point's
past t-values. The anchor is either the outer boundary or t=0. Integrating
from the inner radius without this check would run in the opposite time
direction for this foliation.

Writing Y=(nu,zeta) and W_eta=(eta,eta_v,eta_r), the two radial Einstein
equations take the explicit form

```text
Y_r=B_g Y+U_g W_eta+(S_r,S_delta),
B_g=O(epsilon^2), U_g=O(epsilon).                     (6)
```

The finite radial Volterra operator has an L2 bound independent of epsilon:
its integration length is at most four. Cauchy-Schwarz followed by Fubini
gives norm at most four in unweighted L2; bounded rho ratios modify that
by a fixed factor. Radial Gronwall adds exp(4 sup||B_g||), also bounded.
This controls Y from its anchor values, first scalar derivatives and sources.
The temporal mass equation directly controls nu_v using the same variables.
Equation (4), not a new closure assumption, supplies zeta_v.

At a t=0 anchor, its lapse time derivative is fixed by the radial constraint
and the derivative of the supplied initial lapse profile:

```text
zeta_v|_(t=0)=(d zeta_initial/dr-zeta_r|_(t=0))/sigma. (7)
```

At r=8 it is the derivative of the specified boundary lapse normalization.
For an error comparison this boundary lapse error can be zero by matching
the same normalization; the original physical lapse need not be zero there.
The factor 1/sigma is fixed, not an inverse-wavelength loss.

## 4. Do not prescribe an incompatible constant boundary mass

At the outer boundary the mass is an evolving variable. Its value obeys
the temporal Einstein equation evaluated at r=8, schematically

```text
nu_B'=T_eta W_eta|_B+T_nu nu_B+T_zeta zeta_B+S_v|_B,  (8)
```

where the coefficients are exactly those already varied from the action.
They are bounded on this reference family. Equation (8), with an initial
mass value, replaces any attempt to prescribe an unrelated constant mass
while radiation crosses the boundary.

Use the no-incoming scalar error conditions from the preceding energy note:
eta_r=k_plus eta_v at the inner boundary, eta_r=k_minus eta_v at the outer,
with the roots of a+2bk+ck^2=0. Their positive outgoing energy flux controls
the corresponding boundary first derivatives. The value eta|_B is controlled
by the one-dimensional H1 trace estimate and the scalar slice energy.
Nonzero incoming error data add their own flux/data terms.

Multiplying (8) by nu_B and applying Young and Gronwall bounds nu_B from
initial mass, scalar slice energy, outgoing scalar flux, boundary lapse
data and the boundary S_v source. It introduces no differentiated scalar
unknown. At the initial/boundary corner these data must agree with the
constraints; this derivation does not supply inconsistent data for free.

## 5. Close the conditional coupled linear estimate

Let E(t) be the positive augmented scalar energy already derived, Phi(T)
its accumulated outgoing boundary flux, and

```text
M(T)=integral_(Omega_T) rho[nu^2+zeta^2+nu_v^2+nu_r^2+zeta_v^2+zeta_r^2] dvdr.
```

Let D_g collect squared norms of initial metric data including its lapse
tangential derivative, boundary lapse data and its time derivative, the
initial boundary mass, and the following actual forcing norms/traces:

```text
S_r, S_delta, S_v, partial_v S_delta in weighted spacetime L2,
F_chi in the density-source L2 norm,
S_v at the outer boundary,
S_delta at initial anchors, and compatible scalar initial/boundary data.
```

Weights rho and 1/rho are equivalent to fixed positive weights on this
annulus. The source derivative and boundary traces are explicit parts of
the data norm; they are not inferred from interior point samples.

The radial reconstruction, (4), temporal mass equation and boundary mass
ODE give, with constants independent of sufficiently small epsilon,

```text
M(T) <= C_g [D_g + integral_0^T E(s)ds + Phi(T)].       (9)
```

To see the boundary terms in this step: B_l at the current point is
O(epsilon) in W_eta and O(epsilon^2) in Y. Its outer anchor's scalar trace
is controlled by outgoing flux; its initial anchor is prescribed data.
The V_l radial integral is bounded by the Volterra estimate. The boundary
mass ODE can also import outgoing flux with an order-one coefficient, so
it would be incorrect to claim every boundary term in (9) is epsilon^2.

The complete metric-to-scalar operator previously derived satisfies
||F_metric/sqrt(rho)||_2 <= C_m epsilon sqrt(E_g(t)), with E_g(t) the
instantaneous metric norm in M. Insert it into the scalar energy identity
and apply Young before integration:

```text
E(T)+Phi(T) <= E(0)+C_e integral_0^T E(s)ds
              +C_f ||F_chi/sqrt(rho)||_(L2(Omega_T))^2
              +C_* epsilon^2 M(T).                  (10)
```

Combining (9)-(10), choose epsilon sufficiently small that
C_* C_g epsilon^2 <= 1/2. Absorb that part of Phi on the left, then apply
Gronwall. The result has the form

```text
E(T)+Phi(T) <= C exp(C T)
 [E(0)+||F_chi/sqrt(rho)||_2^2+epsilon^2 D_g],
M(T) <= C exp(C T)[D_g+E(0)+||F_chi/sqrt(rho)||_2^2].  (11)
```

The constant depends on the fixed annulus/time slab, coefficient bounds
and boundary class, not on inverse wavelength. A conservative explicit
epsilon threshold requires continuum bounds on those constants; the grid
tests do not provide that certification.

This is a coupled a priori estimate, including the formerly missing zeta_v
norm, for smooth solutions of the specified linearized constrained system
with compatible data. It also gives uniqueness within that class for zero
error data/sources. It does not prove existence of such a solution, propagate
all constraints from a proposed evolution formulation, or control nonlinear
remainders when the reference itself changes. Those are different claims.

## 6. Restore the physical mass without inventing an error obstruction

At strict first order in u on a prescribed Y0=(g0,chi0),

```text
K=u K1[Y0]+O(u^2), N1=mu1-kappa K1[Y0].
```

For an exact response and an approximate response to this same reference,
use the same exact K1 to define both improved variables. Then

```text
mu1_exact-mu1_app=N1_exact-N1_app,                    (12)
partial_v(mu1_exact-mu1_app)=partial_v(N1_exact-N1_app).
```

The large known partial_v K1 cancels from the error exactly, even if each
individual response derivative is order epsilon^-1. This is an algebraic
translation by a common sourced field, not deletion of physical stress.
The earlier residual evaluators already use this exact restoration from the
reference, rather than discarding its higher epsilon coefficients.

If only a truncated K1_app is used, the explicit omitted tail must instead
be retained. If the two references differ, the relation is

```text
error(mu1)=error(N1)+kappa[K1(Y0_exact)-K1(Y0_app)].    (13)
```

Thus the next transfer problem belongs to reference accuracy, not to the
mere presence of a fast but shared mass oscillation. The current large
physical mass derivative is not a demonstrated instability or a necessary
gauge-independent u/epsilon bound.

The variation needed for (13) is also explicit. With j=-(2/3)r^2 XU,
B=2F/r-F_r-2F delta_r, K1=2F j_r+2e^-delta j_v+Bj, and f_F=delta F,

```text
delta j=-(2/3)r^2(U delta X+X delta U),
delta B=2f_F/r-f_F,r-2f_F delta_r-2F zeta_r,
delta K1=2f_F j_r+2F(delta j)_r
          -2e^-delta zeta j_v+2e^-delta(delta j)_v
          +(delta B)j+B delta j.                    (14)
```

U contains second metric derivatives and X first scalar derivatives. Thus
K1 involves up to three metric/two scalar derivatives, while its first
derivatives can involve four metric/three scalar derivatives. A first-energy
bound on the reference is not automatically enough to bound (13) and its
derivatives. A weighted higher-regularity estimate or further justified
structure must handle that transfer; it is not an unsigned numeric coupling.

## 7. Exact identities and sampled coefficient evidence

Companion: `scripts/annular_lapse_current_closure_20260909.py`.
Completed run:
`source-intake/navier-stokes/20260909/annular-lapse-current-closure-initial/`.
27/27 checks at 2026-09-09T01:14:46.054543+00:00: seven exact identities
and twenty matched scaling/refinement checks. Source/snapshot SHA-256:
`13d152dd676393a867c29a09245ebda9674b1870d73e21e70afde6b56e55c20f`.

The tests use the same canonical and nonlinear/modulated backgrounds, three
slow times, five radii, eight wavelengths 0.4 to 0.003125, 64 phases and a
128-phase refinement. Measured small-wavelength slopes in both cases are:

| Quantity | Observed order |
| --- | ---: |
| Lapse endpoint scalar coefficients | epsilon^1.000 |
| Lapse volume scalar coefficients | epsilon^-0.000 |
| Lapse volume metric coefficients | epsilon^2.000 |
| Radial scalar-to-metric coefficients | epsilon^1.000 |
| Radial metric-to-metric coefficients | epsilon^2.000 |
| Temporal mass scalar coefficients | epsilon^0.000 |
| Physical mass and known restoration time derivatives | epsilon^-1.000 |
| Improved mass time derivative | epsilon^1.003 / epsilon^1.002 |

At epsilon=0.003125, the physical mass time-derivative maxima are about
0.07977 and 0.08795, whereas the improved response maxima are about
1.37e-8 and 1.49e-8. These are response amplitudes, not approximation errors;
the error statement follows from exact (12), not those small numbers.
Phase refinement changes these diagnostics by less than 0.30%.

## 8. Check the additional differentiated source, not just its size

Equation (4) requires partial_v S_delta. Evaluating it needs fifth metric
derivatives of the retained O4 expression, so the existing fourth-order
Taylor evaluator was not reused beyond its available derivative order.
The new helper `scripts/annular_fifth_order_jet_20260909.py` retains fifth
physical derivative order and exact first-order-u arithmetic. Its power,
exponential and log expansions include the sixth combined degree required
for u times five physical derivatives. All 42 coefficients are checked
against independent symbolic derivatives before testing the fields.

Runner: `scripts/annular_source_derivative_residuals_20260909.py`.
Completed run:
`source-intake/navier-stokes/20260909/annular-source-derivative-final/`.
42/42 checks at 2026-09-09T01:18:53.170025+00:00. The old equations, omission
controls, sampling and before/after conventions are preserved; the derivative
source and density scalar residual are added, not substituted for old tests.

| New diagnostic | Canonical reference | Canonical coupled | Nonlinear reference | Nonlinear coupled |
| --- | ---: | ---: | ---: | ---: |
| Time derivative of lapse residual | 4.000 | 3.001 | 4.000 | 3.005 |
| Scalar density residual | 3.000 | 3.000 | 3.000 | 3.000 |

The required differentiated lapse source therefore has the sampled cubic
coupled scaling, rather than an overlooked quadratic remainder. This supports
the needed source regularity order; it is not a certified spacetime or
boundary norm bound. All previous mass/angular/scalar gates still pass.
Phase refinement agrees within 0.56%. There are 44 rows and 32 slopes.

Runner SHA-256:
`d43cf4e3988f63b69ab15487684b9ec8f1b83dc0e559c2e4eca6e35c6cd140de`.
Fifth-order helper SHA-256:
`02db75655f95f3d64fba5246b7d7eca9ab4cdba35cc5b3aa0cb8be53072814ef`.

The initial derivative attempt is preserved separately as failed: its helper
omitted the math import and exited before any test. The final run fixes that
import and passes the independent derivative self-test. The failed attempt
has no COMPLETE marker and is not counted as evidence of passing physics.

Post-run integrity verification confirms live/executed script hashes, input
ownership hashes, both COMPLETE timestamps and check counts. The closure run
contains 18 rows/18 slopes; the final derivative run 44 rows/32 slopes.
All 164 shared residual values exactly match the earlier fourth-order
evaluator, so increasing derivative capacity did not change existing results.
All three new sources compile in memory, all seven cited local file paths
exist, and no bytecode cache or live owned calculation worker remains.

## 9. What is and is not finished

The scalar estimate no longer relies on an assumed lapse time-derivative
bound: (3)-(11) provide the missing reconstruction and coupled a priori
closure for the stated linear common-reference problem. Sources, causal
anchors and the boundary mass law are explicit. The known fast mass term
does not obstruct the common-reference error estimate.

Still required before calling this a controlled physical solution: construct
compatible initial/boundary evolution and verify constraint propagation;
certify source norms/constants beyond the finite samples; and transfer the
estimate through reference error and the higher derivatives in (13)-(14).
A full nonlinear first-order-u approximation, finite-u EFT validity, local-GR
derivation from the complete parent and black-hole centre regularity remain
unproved. This is not a replacement of the unified programme with a scalar
toy model; it advances the retained wave/gravity stability component.

Next finite target: build the compatible common-reference linear evolution
with the derived boundary mass ODE and lapse reconstruction, and measure
actual error against the sourced annular approximation. Track reference-error
transfer separately using (14), rather than reopening the already resolved
common-K cancellation as a generic missing-coupling problem.
