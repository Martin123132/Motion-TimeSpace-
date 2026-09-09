# Analytic third-corner construction and the regularity required by curvature

Private continuation, 2026-09-09. The preceding turn is verified progress:
the discrete chain correction substantially improved late-time constraint
residuals but did not make the field refinement tests pass. This step changes
neither that conclusion nor the physical parent coefficients. It derives the
regularity target and constructs a new, explicitly declared initial-data
family from analytic parent-equation compatibility conditions.

## 1. Derivative requirements come from the actual observable

The existing transfer uses physical coordinates (v,r), with

    F=1-2 mu/r-Lambda r^2/3, E=exp(delta),
    X=2 E^(-1) chi_v chi_r+F chi_r^2,
    Z=-F_rr-3 F_r delta_r-2F(delta_rr+delta_r^2)
      -2E^(-1)delta_vr+2(F_r+F delta_r)/r+2(1-F)/r^2,
    M1=-2 r^2 X Z/3,
    K1=kappa[2F M1_r+2E^(-1)M1_v
             +(2F/r-F_r-2F delta_r)M1].

Thus Z needs second metric derivatives, X needs first scalar derivatives,
and K1 needs THIRD metric derivatives and SECOND scalar derivatives. This
counts actual derivatives in the implemented expressions; an algebraic
on-shell proxy for Z is not substituted for the true curvature. K1 is the
specific first-coupling mass correction, not a generic memory tensor.

In the annular coordinates, partial_v=partial_t and
partial_r=partial_R-sigma partial_t. The change of coordinates preserves
the required total derivative order. A bound on all mixed derivatives through
order three transfers with finite binomial factors when sigma is fixed.

For a one-dimensional interval of length L and a function f in H1,

    ||f||_infinity <= L^(-1/2)||f||_2 + L^(1/2)||f_R||_2.

Choose a point where |f| does not exceed its RMS value, integrate f_R to any
other point, and apply Cauchy-Schwarz. Applied to each derivative through
order three, this shows H4 control is a sufficient spatial norm for pointwise
third-derivative control. For L=4, the two coefficients are 1/2 and 2.
H3 alone controls the third derivative only in L2, not uniformly pointwise.

The first-order parent PDE converts mixed time/radial derivatives of total
order <=3 into spatial derivatives through order three plus coefficient and
forcing derivatives. This requires a uniformly invertible Legendre map and
bounded coefficients; it does NOT assume away a kinetic-branch failure.
Consequently an established H4 evolution estimate would supply the needed
pointwise jets. It has not yet been established for the full numerical
boundary/source-projected system. Formal corner compatibility is a necessary
ingredient of that route, not the full estimate or a curvature error bound.

On a compact, regular jet domain r>=r_min>0, E>=E_min>0, the K1 expression is
a smooth map of the metric third jets and scalar second jets. The mean-value
formula gives a local Lipschitz bound with the supremum of its jet Jacobian
along the segment from background to corrected fields. The existing nonlinear
remainder calculator can evaluate such factors, but this step does not assert
that the required unknown continuum jet-error norms have been bounded.

## 2. Derive the compatibility hierarchy once

For the ordinary current linearization

    e_t=A(t,R)e+B(t,R)e_R-d(t,R),

let e_k(R)=partial_t^k e(0,R), A_j=partial_t^j A(0,R), and similarly for B,d.
Differentiation gives the recurrence

    e_(k+1)=sum_(j=0)^k binomial(k,j)
            [A_j e_(k-j)+B_j partial_R e_(k-j)]-d_k.

For an incoming boundary row L(t), homogeneous data require

    C_k=sum_(j=0)^k binomial(k,j) L_j e_(k-j)=0.

In particular

    e3=A_tt e0+B_tt e0_R+2A_t e1+2B_t e1_R+A e2+B e2_R-d_tt,
    C3=L e3+3L_t e2+3L_tt e1+L_ttt e0.

We construct C0 through C3 for both incoming scalar boundaries and the outer
lapse boundary. With H4 initial data, these are the corner traces needed
through third order. This is a sufficient-order choice for the intended
regularity programme, not a claim that every lower-order norm requires C3.

In the noncharacteristic incoming scalar channel the highest free initial
scalar derivative is chi0^(k+1), with coefficient lambda_in^k in normalized
boundary variables. The lapse coefficient is (1/sigma)^k. These coefficients
explain local solvability of higher jets when the speeds do not vanish. They
also warn of inverse-speed amplification near characteristic boundaries. No
division by a horizon zero-speed mode or additional incoming condition there
is permitted by this exterior construction.

## 3. Analytic dual/Taylor implementation of the parent equations

The new engine uses the existing fifth-order Taylor algebra in local (t,R),
with a degree-one auxiliary direction for the ORDINARY correction. This dual
direction is bookkeeping for linearization; it is NOT the physical curvature
coupling u or a new fitted field.

The background coefficients and harmonic fields are expanded directly in
v=t+sigma(R-4), including mixed derivatives. The background current variables
are (chi,w,h,mu,delta). For a current perturbation the Legendre variation is

    delta q=(e_h+B_scalar e_w-h_mu e_mu-h_delta e_delta)/alpha.

Using q=q_background+dual*delta q, the engine evaluates the original reduced
current RHS

    chi_t=q, w_t=q_R,
    h_t=R^(-2)partial_R(R^2 f)-E V_chi-f_mu(mu_R-G0),
    mu_t=C0, delta_t=(delta_R-D0)/sigma.

Extracting the linear dual coefficient gives F'[e]. The actual background
defect is retained as d=background_t-F(background). Successive Taylor
coefficients of e are filled from F'[e]-d, divided by their time degree.
Only the required total degrees are used, so truncation of the background
Taylor algebra does not masquerade as missing high-order coefficients.

This is computed directly in the same CURRENT variables as the evolution.
One must not silently replace it with a physical-variable Newton correction
about an off-shell background: nonlinear field redefinitions introduce
defect-times-perturbation Hessian terms. Current variables, background
residual and linearization are kept consistent here.

Initial endpoint mass jets are not obtained by repeatedly differentiating a
numerically fitted high-degree endpoint polynomial. The initial mass constraint
is m_R=a m+f with the actual background constraint retained in f. Once the
globally solved endpoint mass VALUE is supplied, its normalized Taylor jets
follow recursively:

    (j+1)m_(j+1)=(a m+f)_j.

Thus the analytic corner calculation uses the same mass equation, not an
independent choice of mass derivatives. The global mass profile is still
checked separately on a dense holdout grid.

## 4. New data, not a retroactive repair of the old problem

The family has nine compact profiles: scalar endpoint jets of orders 2,3,4
at each end, and lapse endpoint jets of orders 1,2,3 at the outer end. For
inward distance x and endpoint orientation epsilon=+1 or -1,

    profile_k=epsilon^k x^k(1-x)^6/k!, 0<=x<=1,

extended by zero beyond the support. The kth physical radial derivative at
its endpoint is normalized to one. At the interior joins the profile and
its first five derivatives vanish. Hence the scalar-gradient initial variable
also has ample piecewise smoothness for the H4 target, unlike a mere C2
gradient join. The cutoff choice is a declared test-data choice, not derived
as a unique physical prediction.

Keep q0=0, outer m0=0 and outer lapse0=0. For each profile, solve the SAME
linearized mass ODE on four panels. Nine amplitudes solve the nine affine
C1/C2/C3 equations, without using an evolution score. The particular mass
solution carries the background constraint forcing. C0 holds by construction.

Both degree-64 and independent degree-80 mass solves were used. Their
amplitudes agree to the tested tolerance. Row-scaled corner matrix condition
numbers are about 118488 canonical and 121984 nonlinear: these are not
well-conditioned matrices and precision sensitivity must remain visible.
Agreement under mass-degree change and direct substitution checks is numerical
evidence, not an interval certificate for every coefficient or a universal
global-family invertibility theorem.

Largest degree-64 analytic C3 residuals are about 4.27e-18 (canonical) and
6.44e-18 (nonlinear), versus the old outer mismatches -5.02e-4 and4.819e-3.
Independent finite-difference C0/C1/C2 checks pass their stated tolerances.
The analytic engine reproduces the old independently estimated nonzero C3.
This distinguishes a consistent formal construction from a claim of exact
floating-point zeros.

Dense 801-point mass-constraint residuals are 3.14e-19 and4.83e-19. Initial
scalar maxima are 3.41e-10 and1.46e-9. The nonlinear fourth-jet amplitude
reaches about -3.87e-5: small field VALUES do not imply that every derivative
is small. Any eventual perturbative curvature/remainder claim must use the
actual derivative norms, not just these small field maxima.

Construction owner: 31/31 checks, completed 07:20:08 UTC. These are analytic-
algebra/numerical-construction checks, not empirical tests of MTS or a global
smoothness/black-hole theorem. All previous failed initial-data problems stay
preserved. New-data success cannot retroactively validate them.

## 5. Evolution and validation

The first evolution test uses the ORIGINAL projected source method, no Gram
filter, both canonical/nonlinear fixtures, N128/256/512, T=.1,.3 and finest
time halving. Only the declared initial-data family changes. This separates
the regularity intervention from the previous chain-completion intervention.
All physical accuracy gates are unchanged.

Completed at 07:26:38 UTC: **129/129**, with all four spatial and temporal
comparison groups passing. Every finest scalar-boundary, lapse, mass-constraint,
source-completion and integrability gate also passes. This is an ordinary
coupled evolution test, not merely a prescribed-metric scalar control.

| Fixture / time | chi coarse/fine difference ratio | q ratio | mu ratio | delta ratio |
| --- | ---: | ---: | ---: | ---: |
| Canonical .1 | 6.35 | 3.10 | 6.26 | 8.83 |
| Canonical .3 | 4.76 | 5.46 | 7.97 | 3.49 |
| Nonlinear .1 | 3.66 | 3.47 | 3.58 | 8.84 |
| Nonlinear .3 | 5.03 | 6.71 | 6.74 | 3.79 |

These compare N128/256 differences with N256/512 differences; the actual
gate remains fine_difference<=coarse_difference/1.3+1e-16. Ratios are not
continuum error estimates or a proof of asymptotic order. The new family
changes both the endpoint jet compatibility and cutoff regularity. Therefore
this combined intervention's success does not isolate C3 as the unique cause
of every old failure.

Independent validation completes **99/99**, 07:27:57 UTC. It verifies:

- Executed/input hashes and all sixteen saved outputs, with exact historical
  runner snapshots used for old owners, not silently substituted live code.
- Unchanged physical parameters, original source method and accuracy gates;
  recomputation of all spatial/time comparisons from the saved arrays.
- Mixed background derivatives against separate symbolic differentiation.
- An 80-digit solve of the saved corner matrices. Amplitude disagreements
  with the double-precision solutions are about1.94e-20 and1.05e-19. This
  checks linear algebra precision, not the exact source coefficients.
- Independent finite-difference C3 consistency. The outer scalar checks are
  around +/-7.5e-9 canonical and -2.4e-8 nonlinear, compared with analytic
  algebraic residuals around1e-18. The finite-difference uncertainty must not
  be relabeled as a certified exact zero.

All owners retain valid_for_physics_claim=false. The old second-corner128/129,
chain-completed129/131, first-u136/137 and four curvature failures remain
unchanged. The original source method also still has its known discrete
product-rule drift; passing its mass gate does not erase that term or prove
an exactly preserved full semidiscrete constraint.

**Next target:** reconstruct the actual coupled solution's time/spatial jets
through total order three, then transfer them to Z, Weyl squared, M1 and K1
with the existing derivative-sensitivity and nonlinear-remainder checks.
Replay the saved current RHS and its numerical sources first. Do not reuse
the old scalar/coordinate time-jet operator as though it were the current
coupled operator, drop endpoint/source terms, or silently differentiate a
different interpolated background. Compare independent spatial stencils and
time-derivative controls before claiming curvature accuracy. Full first-u,
finite-coupling and physical calibration remain later obligations.

Safe save point. All computations from this continuation have finished.

## 6. Sources and scope

Paths relative to post-checkpoint-work:

- `scripts/annular_analytic_corner_jets_20260909.py`
- `scripts/annular_third_corner_initial_data_20260909.py`
- `scripts/derive_annular_analytic_third_corner_data_20260909.py`
- `scripts/validate_annular_analytic_third_corner_20260909.py`
- `scripts/run_annular_coupled_current_correction_20260909.py`
- `scripts/annular_fifth_order_jet_20260909.py`
- `scripts/annular_curvature_timejet_transfer_20260909.py`
- `source-intake/navier-stokes/20260909/annular-analytic-third-corner-initial-data/status.json`
- `source-intake/navier-stokes/20260909/annular-analytic-third-corner-initial-data/canonical-degree64.json`
- `source-intake/navier-stokes/20260909/annular-analytic-third-corner-initial-data/nonlinear_modulated-degree64.json`
- `source-intake/navier-stokes/20260909/annular-coupled-current-analytic-third-corner/status.json`
- `source-intake/navier-stokes/20260909/annular-analytic-third-corner-validation/status.json`
- `DERIVATION-20260909-discrete-Noether-transport-and-chain-completion.md`

The full MTS-to-GR/Newton/Maxwell and calibrated-source-coupling goal remains
open. Physical coupling calibration, full boundary/source energy estimates,
uniform coefficient-interpolation control, curvature-jet error bounds and
finite-u validity are not supplied by corner compatibility alone. Private
work only: no GitHub, frozen workbench/galaxy edits, subagents or stopped
shared processes.
