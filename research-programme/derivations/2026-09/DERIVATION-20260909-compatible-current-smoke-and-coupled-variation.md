# Compatible-current smoke: useful stiffness, failed conservation, coupled variation next

Private checkpoint, 2026-09-09. This continues the coefficient-fixed construction
in DERIVATION-20260909-scalar-current-passivity-and-unprojected-C3-test.md.
All paths below are relative to this post-checkpoint-work directory. No parent
physics, local-GR, horizon regularity, source calibration or first-u claim follows.

## 1. What was actually implemented and tested

The previous static restoring term is now implemented in the full coupled
current evolution, not merely proposed. With grid spacing h, quadrature H_h,
a=r^2 c>0 and positive Gram remainder R_a=Delta3^T W_a Delta3/h, it adds

    Delta S_q = -(H_h r^2 alpha)^(-1) R_a chi.

The coefficient is fixed by the compatible second derivative and its surface
SAT change, not fitted as damping. The integrability defect I=w-D_h chi and
the independent nonzero parent forcing are retained. The entire new source,
including SAT, restoring term and lapse source, receives Volterra mass
completion, then the current transformation including h_mu S_mu+h_delta S_delta.

Higher time coefficients of a may have either sign. The implementation keeps
the positive Gram template's edge orientations fixed and differentiates its
linear coefficient map, rather than applying abs/sign to signed coefficients.
For normalized time coefficients the restoring coefficient at degree n is
sum_{k=0}^n R_{a^[k]} chi^[n-k]. Actual source/RHS time jets through order three
are independently checked against ordinary RHS evaluation and finite differences.

A separate matched baseline uses the original projected source law, exactly
the same C3 initial payloads, grids N=32,64,128, backgrounds, physical boundary
data, timesteps and unchanged acceptance gates. No old output was overwritten.

## 2. Time control: what the new qualification does and does not establish

The complete 5(N+1)-dimensional frozen Jacobian is used, not just the scalar
wave block. A positive diagnostic norm includes scalar kinetic/gradient terms,
the Gram potential, scalar L2 and metric L2. It is not a derived full coupled
physical energy. If H=C C^T and B=C^T L C^(-T), then for eta=dt ||B||_2,

    ||P4(dt B)-exp(dt B)||_2 <= exp(eta) eta^5/120,
    ||P4(dt B)||_2 <= exp(dt nu) + exp(eta) eta^5/120,
    nu = lambda_max((B+B^T)/2).

The first bound follows by bounding the exponential series after degree four;
the second uses the Euclidean logarithmic norm. Positive nu is recorded, not
discarded. Eighteen samples (two fixtures, three grids, t=0,.15,.3) set eta<=.25
caps, also subject to ordinary CFL. Approximate caps are .000785, .000393 and
.000196. The actual steps are rounded to output intervals and matched in both
branches. Frozen sampled bounds are NOT a nonautonomous all-time or uniform
continuum stability proof. The actual time-halving checks also remain required.

## 3. Matched outcomes, including failures

| Fixture and time | New/original mass H4 trace floor | New/original measured H3chi+H4metric norm | Original/new nodal Z sensitivity |
|---|---:|---:|---:|
| canonical .1 | .6133 | .6244 | 41.18% / 75.00% |
| canonical .3 | .09083 | .08952 | 69.66% / 87.28% |
| nonlinear .1 | .4306 | .4429 | 73.13% / 66.70% |
| nonlinear .3 | .09827 | .09681 | about 66% / 85% |

These are N128/poly7 finite-grid diagnostics, not physical observational errors.
The norm is the Euclidean combination of the specified component Sobolev norms.
The trace floor bounds any interpolant matching those numerical traces; it is
not a certified bound on the unknown continuum solution.

The original matched baseline passes its field gates, 140/140. The new candidate
FAILS, 157/164. At N128 both timesteps fail the 5% mass-constraint gate for
canonical t=.3 (20.01%), nonlinear t=.1 (7.11%), and nonlinear t=.3 (47.23%).
The seventh failure is early nonlinear scalar spatial refinement, ratio about
1.298 against the unchanged 1.3 threshold. Do not round that into a pass.

The roughly tenfold late reduction in the measured derivative quantities is a
real improvement in this comparison, but not a successful replacement. Both
branches still fail the combined curvature gates. All four candidate nodal Z
gates and all four candidate subcell Z gates fail; K1 sensitivity gates pass.
Strong mesh differences increase rather than decrease in BOTH branches: the
coarse/fine strong-difference ratios are below one. Candidate ratios improve
to approximately .30-.64 from baseline .12-.19, but still do not converge.

## 4. Source mismatch identified without deleting constraints

For full nodal constraint J=J0+D_h e_mu-g(t)e, differentiate the actual equation:

    J_t = J0_t + D_h rhs_mu - g_t e - g rhs
        = [J0_t + D_h bulk_mu - g_t e - g bulk]
          + [D_h S_mu - g S].

The saved-state replay verifies this split. In the projected baseline, the
source bracket is at roundoff. In the candidate, its max at the four N128
snapshots is approximately 7.39e-12, 5.97e-12, 4.12e-11, 3.44e-11. The bulk
bracket also remains nonzero. These are instantaneous budgets, not accumulated
error attribution or a proof that the source alone caused the evolved failure.

The Volterra cell balance itself passes at floating accuracy. Its nodal D_h
residual does not vanish. Thus a correctly implemented cell integration is not
the same thing as satisfying this particular nodal conservation equation.

## 5. Exact fixed-source floor and a constructive minimax response

In coordinate source variables keep S_chi=S_w=0, fixed S_q,S_delta, outer
S_mu=0. Write a=g_mu, f=g_q S_q+g_delta S_delta and

    A=(D_h-diag(a))[:, :-1].

If rank(A)=N, let nonzero n span ker(A^T). Every mass response u satisfies

    n^T(Au-f)=-n^T f,
    ||Au-f||_infinity >= |n^T f|/||n||_1.

This is sharp, not just an estimate. Choose

    r*=-(n^T f) sign(n)/||n||_1.

Then n^T(f+r*)=0, so f+r* is in range(A). The unique u solving Au=f+r*
attains the displayed lower bound. Components with n_i=0 can use r*_i=0.
This proves the finite-dimensional formula; floating SVD evaluations below
are numerical checks, not interval-certified positive lower bounds.

| Candidate N128 snapshot | Observed nodal source residual | Best fixed-source residual | Observed / best |
|---|---:|---:|---:|
| canonical .1 | 7.390e-12 | 6.847e-13 | 10.79 |
| canonical .3 | 5.969e-12 | 5.886e-14 | 101.40 |
| nonlinear .1 | 4.124e-11 | 3.101e-12 | 13.30 |
| nonlinear .3 | 3.445e-11 | 2.291e-13 | 150.33 |

All 24 baseline/candidate snapshots have numerically full rank and verified
minimax attainment. Baseline forcing has a floor at roundoff because its scalar
source was already projected. That is not the same fixed forcing as the raw
candidate. The constructed minimax responses have NOT been evolved, and are
not proposed as a way to relabel nonconservation as conservation. A better
mass-only approximation is possible, but an exactly conserving mass-only
solution is impossible when this fixed-source compatibility condition is nonzero.

An independent interior calculation explains why more accurate quadrature alone
is not a universal fix. At a=0, Volterra is the cell trapezoid rule. For a Fourier
mode with x=sin(theta/2)^2, its composition with centered fourth-order D_h has
multiplier

    D_h V_h = (1-x)(1+2x/3) = 1-x/3-2x^2/3.

The forcing residual is -x(1+2x)/3. At Nyquist it loses the whole alternating
forcing, while the cell balance still holds. Any translation-invariant interior
inverse of D_h would have magnitude 3h/|sin(theta)(4-cos(theta))|, unbounded
as theta approaches pi. This is an interior-symbol statement, not a false
claim that the finite boundary-closed matrix has a global alternating kernel.

## 6. Constructive next derivation: vary the Gram term with the other fields

A concrete route is to test a joint variational discretization, rather than
attach a scalar restoring force and then repair the metric equation separately.
This is a candidate discretization of the existing continuum branch, not a
new fundamental interaction or an already proved constraint-preserving scheme.

For grid field Phi=(chi,q,w,mu,delta), define the candidate added potential

    U_h(Phi)=1/2 chi^T R_{a(Phi)} chi,   L_add=-U_h,
    a=r^2 c(Phi).

Linearity and symmetry of R_a give the complete first and mixed second variations:

    DU[e] = e_chi^T R_a chi + 1/2 chi^T R_{Da[e]} chi,
    D2U[e,z] = e_chi^T R_a z_chi
             + e_chi^T R_{Da[z]} chi + z_chi^T R_{Da[e]} chi
             + 1/2 chi^T R_{D2a[e,z]} chi.

These follow by product differentiation, with e,z independent variations. The
smoke restoring term uses only the frozen-coefficient scalar Hessian block;
it does not establish that the other three terms can be omitted from a joint
discrete action on a nonzero background. Temporal coefficient differentiation
in section 1 is NOT a substitute for these field variations.

The actual constitutive coefficient can be written explicitly as

    E=exp(delta), F=1-2mu/r-Lambda r^2/3, s=w-sigma q, p=q/E,
    X=2ps+Fs^2, P=1-4b2 X-6b3 X^2, P_X=-4b2-12b3 X,
    c=E [P F + 2 P_X (p+Fs)^2].

Even the canonical b2=b3=0 case already contains metric variations:

    a=r^2 E F,
    Da[e]=-2rE e_mu + a e_delta,
    D2a[e,z]=-2rE(e_mu z_delta+z_mu e_delta)+a e_delta z_delta.

Consequently the mixed scalar/mass Hessian contains
e_chi^T R_{-2rE z_mu} chi_background. It need not vanish on this background.
For nonlinear P(X), a also depends on q,w, so varying L_add changes the discrete
canonical momentum and spatial scalar terms as well as metric variations.
It is not legitimate to assume the old Legendre map or old constraint survives.

Next bounded task: evaluate these complete coupled variations against independent
finite differences, starting with the explicit canonical formula, then derive
the resulting discrete Euler-Lagrange/constraint and boundary identities from
one action. Preserve nonzero background residuals and physical boundary data.
If the parent discrete gauge/constraint identity does not follow, record that
specific obstruction rather than asserting that variation alone ensures it.
Do not launch another evolution until the changed momentum, constraints and
boundary fluxes are specified. No minimax tuning or automatic larger mesh.

## 7. Reproducibility and saved state

All owner directories below are under source-intake/navier-stokes/20260909 and
contain status.json and executed-script.py; only successful software owners
have COMPLETE. Numerical field failure is retained without COMPLETE.

| Owner directory | Outcome |
|---|---|
| annular-compatible-current-time-jets-preflight | 181/181 |
| annular-compatible-current-timestep-qualified | 76/76 |
| annular-compatible-current-restoring-smoke | FAILED 157/164 |
| annular-compatible-current-matched-baseline | 140/140 field gates |
| annular-compatible-current-time-jets-trajectory | 193/193 software |
| annular-compatible-baseline-time-jets | 168/168 software |
| annular-compatible-smoke-normal-candidate | 526/526 software; curvature fails |
| annular-compatible-smoke-normal-baseline | 526/526 software; curvature fails |
| annular-compatible-current-smoke-comparison | 289/289 diagnostics |
| annular-source-nodal-defect-floor | 181/181, completed 09:53:26 UTC |

Executable sources:
- scripts/annular_compatible_current_restoring_20260909.py
- scripts/annular_compatible_current_time_jets_20260909.py
- scripts/annular_compatible_current_rhs_20260909.py
- scripts/derive_annular_compatible_current_time_jets_20260909.py
- scripts/derive_annular_compatible_current_timestep_20260909.py
- scripts/run_annular_compatible_current_smoke_20260909.py
- scripts/derive_annular_compatible_baseline_time_jets_20260909.py
- scripts/derive_annular_compatible_smoke_normal_reconstruction_20260909.py
- scripts/compare_annular_compatible_current_smoke_20260909.py
- scripts/derive_annular_source_nodal_defect_floor_20260909.py

The comparison script inherited two inaccurate check labels mentioning source
projection/mass-only changes; the executed math and recorded parameters use the
full restoring-plus-Volterra candidate. Those immutable snapshots are preserved;
the descriptions in this note state the actual scope. No physical pass is inferred
from check counts. All current continuation jobs have exited. No subagents,
shared-process shutdown, GitHub action, frozen-workbench or galaxy edit was used.
