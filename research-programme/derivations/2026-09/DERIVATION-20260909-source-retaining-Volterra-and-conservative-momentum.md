# Source-retaining mass reconstruction and conservative scalar momentum

Private continuation, 2026-09-09. Scope: the existing ordinary-reference annular
parent equations and their numerical correction, not a new physical fit.
The previous turn is classified as progress after inspecting its saved curvature
transfer and boundary-channel results. No earlier failed gate is reclassified.

Outcome: the mass-only reconstruction is NOT sufficient to repair the curvature
gate. It has been implemented and tested, not just proposed. The stronger new
derivation is the scalar current/momentum system, including a density-rescaled
positive principal symmetrizer that does not falsely fail at a regular GR horizon.
This remains an ordinary scalar-sector result, not a completed MTS-to-GR limit.

## 1. Derive the mass reconstruction instead of imposing a zero constraint

Let (psi,q,m,l) be the ordinary scalar, scalar-time, mass and lapse corrections.
Use tilted coordinates t=v-sigma(r-4), R=r, and denote the already-derived
gradient of the background mass constraint by (b,c,a,d,g), in that order:

    m_R = a m + b psi + c q + d l + g psi_R + j.

These five letters are local to the mass-constraint formula; the wave coefficient
c in the later momentum sections is c0, not the mass-constraint coefficient G_q.

Here j is the signed correction-constraint residual. It is supplied from the
saved field and is NOT set to zero. The full linearized constraint also contains
the original background defect; it is not silently removed by this equation.

For the parent P(X) scalar, define w=chi_R, s=w-sigma q, E=exp(delta),
F=1-2mu/r-Lambda r^2/3, X=2q s/E+F s^2 and

    P=1-4b2 X-6b3 X^2,
    H=F(w^2-sigma^2 q^2)/2 + sigma q^2/E,
    R0+sigma C0 = kappa r^2 [P H+V+b2 X^2+2b3 X^3].

Differentiating this last expression with respect to (chi,q,mu,delta,w) gives
(b,c,a,d,g). The new implementation's independently differentiated formula
agrees with the previous parent gradient on both fixtures at both output times.
Its time coefficients through order three come from the analytic background;
they are not estimated by repeated subtraction of noisy mass values.

Introduce eta=m-g psi. Then exactly

    eta_R = a eta + (b+a g-g_R) psi + c q + d l + j.

This removes the differentiated scalar from the forcing of the mass integration.
The boundary value is eta(B)=m(B)-g(B)psi(B), using the EXISTING outer mass trace.
For continuous coefficients the unique solution is

    U(R,s)=exp(integral_s^R a(x) dx),
    eta(R)=U(R,B) eta(B)
           + integral_B^R U(R,s)[(b+a g-g_R)psi+cq+dl+j](s) ds.

There is no new homogeneous integration constant beyond the supplied boundary
trace. This is a Volterra representation of the constraint, not a plateau axiom,
an added physical equation, or a claim that the residual vanishes.

If |a|<=A on an interval of length L, its elementary stability estimate is

    ||eta||_infinity <= exp(A L) (|eta(B)| + L ||forcing||_infinity).

For two reconstructions with the same a, the same bound applies to their
boundary/forcing differences. If a also differs, retain (a_new-a_old)eta_old
in the difference forcing. The estimate requires genuine coefficient/source
bounds to become a numerical continuum certificate; sampled maxima alone do
not supply those bounds.

The second derivative follows from the constraint, without differentiating the
nodal mass twice independently:

    m_RR = a_R m + a m_R + b_R psi + (b+g_R)psi_R + g psi_RR
           + c_R q + c q_R + d_R l + d l_R + j_R.

The term j_R remains. Dropping it would be exactly the hidden closure we are
avoiding. This formula also shows why repairing the mass integration alone
cannot remove every scalar/lapse derivative error.

## 2. What the implemented reconstruction actually changes

The implementation represents the coefficient and retained residual functions
with degree-five/seven splines and integrates eta backwards with DOP853. It
integrates all time Taylor coefficients through degree three together. Analytic
initial-lift derivatives are retained for the other fields. The outer mass
trace is fixed at every time coefficient.

Only the mass field's nodal values are changed; scalar, q and lapse nodal values
are preserved. This is a NEW reconstructed candidate, not the original accepted
evolution. The nodal mass modification and all temporal coefficients are saved.
Spline and integration errors are not declared zero.

For each reconstructed candidate the full sourced linearized evolution defect
is explicitly evaluated:

    D_new = e_t - A e - B e_R - C e_RR + defect_background - S_numerical.

The original numerical source is retained, including its mass completion.
The source-free parent residual is also saved. A good mass constraint alone
does not make D_new small or promote this candidate to an evolved solution.
Conservation identities of the reconstruction and manufactured accuracy checks
must not be confused with those separate dynamical requirements.

## 3. Derive a conservative scalar variable from the parent action

This route addresses the scalar-gradient bottleneck without inventing a
constitutive law. At fixed metric, the ordinary parent scalar density is

    Ldens=E r^2 [-X/2+b2 X^2+b3 X^3-V(chi)].

Define the physical currents

    Jv=r^2 P chi_r,
    I=Jr=r^2 P chi_v+E r^2 P F chi_r,
    Pi=Jv-sigma I,
    pi=dLdens/dq=-Pi,
    dLdens/dw=-I,

where q=chi_t=chi_v and w=chi_R. The scalar equation is exactly

    Pi_t+I_R=E r^2 [V_chi+Fchi],
    pi_t=I_R-E r^2[V_chi+Fchi],
    w_t=q_R,  chi_t=q.

Fchi denotes the off-shell scalar residual; it is not implicitly discarded.
The last two equations preserve w-chi_R if the initial and boundary data satisfy
that relation. In a numerical method use the same derivative and retain any
kinematic source, rather than assuming integrability of independent variables.

Let the physical scalar principal coefficients be (a0,b0,c0) as in the existing
parent operator. In tilted coordinates define

    alpha=-(a0-2sigma b0+sigma^2 c0),
    B=b0-sigma c0,  c=c0.

Direct differentiation of the actual Lagrangian gives

    pi_q=alpha,  pi_w=-B,  I_q=B,  I_w=c.

On a branch with alpha>0, the implicit function theorem supplies a LOCAL
Legendre inverse q=q(pi,w,metric). It is not a global inverse over arbitrary
field amplitudes. At fixed metric, for H=pi q-Ldens the Hessian in (w,pi) is

    H'' = [[c+B^2/alpha, B/alpha],
           [B/alpha,       1/alpha]],
    det H''=c/alpha,
    delta_y^T H'' delta_y
      = c(delta_w)^2 + (delta_pi+B delta_w)^2/alpha.

Thus alpha>0 and c>0 give a positive principal Hamiltonian Hessian.
With J=[[0,1],[1,0]], the first-order principal matrix is J H'' and
H'' J H'' is symmetric. This is a derived scalar-sector symmetrizer; it is
not a proof of hyperbolicity/stability of the full coupled higher-curvature theory.

The parent principal determinant also reduces to a useful invariant condition:

    B^2+alpha c = b0^2-a0 c0 = r^4 P(P+2X P_X),
    P+2X P_X = 1-12b2 X-30b3 X^2.

Expanding the independently specified a0,b0,c0 verifies this identity. On the
component containing X=0, P>0 and P+2X P_X>0 give a real nondegenerate scalar
characteristic cone. A chosen tilted evolution still separately requires
alpha>0, and the displayed positive Hamiltonian Hessian requires c>0.

For the declared nonlinear fixture b2=1/20, b3=1/50, the common interval
containing zero is

    (-3-sqrt(69))/6 < X < (-3+sqrt(69))/6,
    approximately -1.8844373 < X < 0.8844373.

P is positive throughout this interval; its roots lie further out at
(-5 +/- 5sqrt(13))/6. These are exact conditional restrictions on this fixture's
ordinary kinetic polynomial, not a derivation of physical parameter values.
Leaving the healthy component, or adding dynamical higher-curvature terms,
cannot be declared harmless from the present calculation.

Metric/source terms must accompany the change of variables:

    delta pi=alpha delta q-B delta w+pi_mu delta mu+pi_delta delta delta,
    S_pi=alpha S_q-B S_w+pi_mu S_mu+pi_delta S_delta.

For the saved method S_chi=S_w=0, but S_mu and S_delta generally are not zero.
The independent complex-step source checks include their contributions.

## 4. A discrete energy identity, not merely a positive matrix

The Legendre transform obeys H_pi=q, H_w=I and H_chi=E r^2 V_chi.
For a prescribed metric and the source-free scalar equation,

    partial_t H = partial_R(q I) + H_metric dot metric_t.

The potential work cancels between chi_t=q and pi_t=I_R-E r^2 V_chi.
The metric-work term does NOT vanish for the evolving coupled geometry.
An off-shell scalar source or numerical source adds its actual work term.

For the existing SBP derivative D with norm matrix W,

    I^T W Dq + q^T W DI = [q I]_outer - [q I]_inner.

Therefore a semidiscrete conservative Hamiltonian scalar formulation can retain
this balance exactly (before temporal discretization), together with explicit
potential cancellation, metric work, and source work. Direct checks use the
nonlinear parent currents on both saved fixtures, not just constant coefficients.
Boundary SAT work and the Noether-induced metric evolution still need their
coupled estimate; this identity does not prove those contributions dissipative.

This explains a concrete alternative to repeatedly extrapolating scalar second
derivatives at the boundary: evolve the derived momentum/current variables and
their compatible first-order system. It remains to implement and test that
evolution; the present derivation alone is not a replacement evolution result.

### Boundary work and the integrability condition

For the frozen linearized principal system I=c w+B q, define the positive
impedance z=sqrt(B^2+alpha c). Scalar momentum penalties alone suffice:

    S_pi,left  = (I-z q-g_left)/(h W_left),
    S_pi,right = -(I+z q-g_right)/(h W_right).

Here W_left/right denote the dimensionless endpoint SBP weights. Their
contribution combines with the energy flux into

    left:  -q I+q(I-z q-g_left)=-z q^2-q g_left,
    right:  q I-q(I+z q-g_right)=-z q^2+q g_right.

The homogeneous principal boundary work is nonpositive. Nonzero supplied
boundary data contribute explicit work; they must not be relabelled zero.
These penalties need not alter w_t=Dq or chi_t=q. Thus the discrete defect
w-Dchi remains equal to its supplied initial value when the same D is used.
Initial compatibility and any added numerical source still require checking.

The current-form work cancellation is algebraic even for a nonlinear I, but
that observation alone does not prove nonlinear boundary well-posedness or a
full coupled estimate. Use the frozen characteristic impedance for the first
controlled implementation and retain the metric/current offset in the forcing.
No boundary data from the failed evolution have been changed in this derivation.

## 5. A horizon-regular principal energy, without assuming c>0

Losing positivity of the stationary Hamiltonian Hessian when c reaches zero
must NOT be mistaken for losing hyperbolicity of the scalar theory. The two
conditions are different. A stronger local result follows from the derived
current variables, without changing the equations.

Set h=pi/r^2 and D=B^2+alpha c=r^4 P(P+2XP_X). For y=(w,h), the principal matrix
in y_t=A_y y_R+lower terms is

    A_y = [[B/alpha,                  r^2/alpha],
           [D/(alpha r^2),           B/alpha]],
    S_y = diag(D/r^4,1) = diag(P(P+2XP_X),1).

S_y A_y is symmetric. With alpha>0 and D>0 this supplies a positive local
scalar symmetrizer even when c=0 or c<0. Uniform estimates still require
quantitative lower bounds on alpha/r^2 and P(P+2XP_X), and control of their
derivatives and the other coupled fields. Positivity alone is not that theorem.

Density rescaling has a lower-order term that must be retained:

    h_t = partial_R(I/r^2) + 2I/r^3 - E(V_chi+Fchi).

It is NOT legitimate to omit 2I/r^3. Transform numerical and metric source
contributions consistently as well.

In the canonical GR control with E=1 and P=1,

    A_y = [[1-sigma F, 1], [1,1-sigma F]]/[sigma(2-sigma F)],
    S_y = identity.

At F=0 this is the finite matrix [[1,1],[1,1]]/(2sigma), with distinct real
principal eigenvalues 0 and 1/sigma. For sigma=.05 and mu=1, the independently
checked radial characteristic speeds (the negatives of the RHS eigenvalues) are:

| F | r | characteristic speeds dR/dt |
|---:|---:|---:|
| .5 | 4 | .253164557, -20 |
| 0 | 2 | 0, -20 |
| -.5 | 4/3 | -.246913580, -20 |

These are coordinate speeds in the declared tilted chart, not measurements in
units of physical c. They agree with the canonical GR null directions. At an
inner boundary inside this control horizon both scalar characteristics leave
towards smaller R: do not copy the exterior one-incoming-mode SAT blindly into
that outflow boundary.

This resolves a possible false rejection at a horizon: an indefinite stationary
Hamiltonian does not force an indefinite scalar principal norm. It does NOT
resolve the central curvature singularity. The same control still has
Weyl^2=48mu^2/r^6, which diverges at r=0. Neither the coupled higher-curvature
principal symbol nor a nonlinear black-hole solution has been established here.

## 6. Executed results and decision

The Volterra run finished at 05:09:11 UTC: 137/137 implementation/manufactured
checks, 24 saved candidates, but all four curvature sensitivity gates FAILED.
The conservative momentum derivation finished at 04:53:16 UTC: 31/31.
Independent provenance, SAT/discriminant and integration-tolerance controls
finished at 05:13:14 UTC: 18/18. The horizon-regular symmetrizer and GR controls
finished at 05:14:01 UTC: 18/18. All outputs retain valid_for_physics_claim=false.

Known smooth manufactured fields, with a NONZERO supplied mass residual, are
recovered accurately by the new integration. At 128 intervals, maximum mass
errors are 2.74e-21 (degree five) and 4.76e-22 (degree seven); curvature variation
errors are 4.14e-18 and 2.08e-19, and K1 errors 3.22e-18 and 1.55e-18.
These are method controls, not MTS-versus-GR observations.

For the actual saved corrections, finest-grid mass-value changes are only
7.26e-17 to 1.47e-15 in fixture units. Nevertheless the all-row degree-five/seven
differences remain:

| Fixture | T | delta Z difference / larger norm | delta K1 difference / larger norm |
|---|---:|---:|---:|
| canonical | .1 | 46.18% | 4.297% |
| canonical | .3 | 77.30% | 77.10% |
| nonlinear_modulated | .1 | 92.84% | 14.33% |
| nonlinear_modulated | .3 | 59.05% | 8.974% |

The threshold remains 10%; no endpoint was removed. These compare two new
global spline representations, not the old local polynomial stencils, so they
must not be advertised as a like-for-like improvement of the earlier percentages.
They show that changing mass integration alone does not close the problem.

The additional scalar-velocity evolution defect is retained and can be large:
at canonical T=.3 it is 3.13e-7 / 1.40e-6 for degree five/seven, despite small
nodal mass modification. Re-running that degree-seven solve with tenfold tighter
integration tolerance changes delta Z by only 9.93e-23 and delta K1 by 7.74e-24.
That control does not support blaming the substantial stencil sensitivity on
the Volterra ODE tolerance. Small changes in field values are not enough to
certify their derivatives or the sourced evolution.

Decision: preserve Volterra integration as a derived, source-retaining mass
component, but reject its promotion as a standalone repaired evolution. Next
implement the derived density-normalized current/momentum scalar system with
the correct characteristic boundary count. Test matched manufactured fields,
boundary data and residual sources before coupling it back into the saved
mass/lapse evolution. Keep the full coupled energy and physical coupling gates
open; do not replace them with scalar-only successes.

## 7. Source locations

- `scripts/annular_volterra_constraint_reconstruction_20260909.py`
- `scripts/derive_annular_volterra_constraint_reconstruction_20260909.py`
- `scripts/derive_annular_conservative_momentum_20260909.py`
- `scripts/validate_annular_volterra_and_momentum_20260909.py`
- `scripts/derive_annular_horizon_regular_symmetrizer_20260909.py`
- `source-intake/navier-stokes/20260909/annular-volterra-constraint-reconstruction-initial/status.json`
- `source-intake/navier-stokes/20260909/annular-conservative-momentum-derived/status.json`
- `source-intake/navier-stokes/20260909/annular-volterra-momentum-validation/status.json`
- `source-intake/navier-stokes/20260909/annular-horizon-regular-scalar-symmetrizer-derived/status.json`

These are normalized annular fixture calculations. They supply neither a
physical value of u nor local-GR, PPN, R10, Newtonian, Maxwell or black-hole
completion. No external announcement is used as mathematical evidence here.

All jobs from this continuation have finished at this safe save point. At most
two modest single-core BelowNormal jobs ran together, with no subagents. No
GitHub action, frozen-workbench/galaxy edits, or stopped shared processes.
