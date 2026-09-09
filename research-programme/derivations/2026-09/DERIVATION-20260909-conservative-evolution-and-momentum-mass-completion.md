# Conservative scalar evolution and momentum-to-mass source completion

Private continuation, 2026-09-09. The new scalar formulation has now been
implemented and evolved, not just proposed. Matched canonical and nonlinear
manufactured controls pass outside and across a horizon and on a changing
prescribed metric. A separate calculation simplifies the numerical mass-source
completion directly from the existing parent constraint.

This is progress in the ordinary scalar/metric formulation, NOT a completed
coupled MTS solution, an observational comparison, or a black-hole regularity
proof. No new theorem is imported from a screenshot or a claimed external
Navier-Stokes result. The input equations here belong to the saved local parent.

## 1. State, action and the actual evolved equations

Use the existing tilted coordinates t=v-sigma(r-4), R=r, with sigma=0.05.
The constant shift in t is immaterial to the horizon-crossing control.
Write q=chi_t, w=chi_R, s=w-sigma*q, E=exp(delta), and

    F = 1-2mu/r-Lambda*r^2/3,
    X = 2q*s/E+F*s^2,
    L = -X/2+b2*X^2+b3*X^3-m_chi^2*chi^2/2,
    P = 1-4b2*X-6b3*X^2, Q = P+2X*P_X.

The scalar action density is E*r^2*L. Its momentum and radial current are

    h = pi/r^2 = P*[sigma*(2-sigma*E*F)*q-(1-sigma*E*F)*w],
    f = I/r^2 = P*(q+E*F*s).

In this note alpha=h_q, B=f_q=-h_w and c=f_w are DENSITY-DIVIDED
coefficients; they are not the earlier density-weighted alpha, B and c.
The parent gives B^2+alpha*c=P*Q. The implemented equations are

    chi_t = q,
    w_t   = D_R q,
    h_t   = r^(-2)*D_R(r^2*f)-E*m_chi^2*chi+S_h.

At each RHS call, a safeguarded local Newton inversion recovers q from h,w,E,F.
It rejects nonpositive alpha, P or Q and invalid canonical seeds. This is a
guarded weak-field branch, not a proof of a globally unique Legendre inverse.
In the saved controls the nonlinear case needs at most two Newton iterations.

The derivative is the existing diagonal-norm summation-by-parts (SBP) operator.
The weighted conservative flux matters: the finite-grid identity

    r^(-2)*D_R(r^2*f) = D_R f+2f/r

is NOT exact. The difference is measured, not silently discarded. Keeping the
weighted form retains the spherical density term and gives the exact
semidiscrete Hamiltonian balance below. No added dissipation is used.

IMPORTANT: the present ScalarEvolution class explicitly obtains manufactured
forcing and boundary values inside its RHS. It must not be used unchanged for
physical MTS evolution. A real source/boundary provider and the coupled metric
equations must replace those test fixtures.

## 2. Horizon boundary count and energy exchange

The scalar principal matrix for (w,h) is

    M = [[B/alpha,1/alpha],[P*Q/alpha,B/alpha]],
    S = diag(P*Q,1).

S is positive on the tested healthy branch and SM is symmetric. Characteristic
eigenvalues of the RHS are (B +/- sqrt(P*Q))/alpha; physical coordinate speeds
are their negatives. The exterior intervals have one incoming scalar mode at
each end. The crossing intervals have no incoming inner mode and one incoming
outer mode. The implementation applies no inner penalty in that outflow case.
These are scalar-block counts on prescribed metrics, not yet the characteristic
count of the entire coupled gravity system.

Incoming penalties act on h alone, with exact-reference impedance z=sqrt(P*Q):

    left:  S_h += [f-f_exact-z*(q-q_exact)]/W_left,
    right: S_h += [-f+f_exact-z*(q-q_exact)]/W_right.

Here W is the SBP quadrature weight including grid spacing. The scalar boundary
values are known manufactured data. Unsupported boundary counts raise an error.

Let H=r^2*(h*q-E*L), and take metric derivatives holding chi,w,h fixed:

    H_E = -r^2*L+E*r^2*P*X_E/2, X_E=-2q*s/E^2,
    H_F = E*r^2*P*s^2/2.

Since H_h=r^2*q and H_w=r^2*f, SBP gives the exact semidiscrete identity

    d/dt sum(W*H) = [q*I]_left^right
                    +sum(W*r^2*q*S_h)
                    +sum(W*(H_E*E_t+H_F*F_t)).

The potential cancels using chi_t=q. The last term is metric work and is
retained. RK4 integrates the RHS work alongside the state to check the budget.
Hamiltonian balance is not a positivity theorem: the stationary Hamiltonian
may be indefinite inside the horizon even when the scalar symmetrizer is
positive. Nor does small budget error prove continuum convergence by itself.

Initial w is the analytic derivative rather than the discrete D_R chi. The
initial discrete integrability defect is recorded; its subsequent change is
roundoff-sized and its initial size decreases under refinement. It is not
claimed to be exactly zero on the grid.

## 3. Matched numerical results

Owner: `source-intake/navier-stokes/20260909/annular-conservative-scalar-controls-initial/status.json`.
Complete at 05:27:02 UTC: 361/361 algebra, software and manufactured-control
checks; 48 saved outputs and 12 paired refinement comparisons. These are not
361 independent physical predictions. valid_for_physics_claim remains false.

Both models use chi=.03*sin(k*(R-R_left)+.27)*cos(2.3t+.17), with
k=2*pi/(R_right-R_left), the same method and predeclared gates. The saved parent
fixtures supply canonical b2=b3=m_chi=Lambda=0 and nonlinear
b2=.05,b3=.02,m_chi=.2,Lambda=.001. These are normalized control parameters,
not a fit or a derived physical value of kappa.

The prescribed arenas are exterior [4,8], crossing [1.5,4], and changing-metric
exterior [4,8]. Static controls have mu=1,E=1. The changing control uses
mu=1+.005*sin(.7t), E=exp(.01*sin(t)). The nonlinear metric also includes its
nonzero Lambda. No metric is evolved using its gravitational field equation.

Runs use N=64,128,256 intervals, N256 time halving, CFL=.15 and final T=.15;
outputs are at T=.05 and .15. This is a short method test, not the earlier
ordinary/first-u correction experiment at T=.3.

Finest N256, original time step, T=.15 maximum absolute field errors:

| Case | Arena | chi | w | h | q |
| --- | --- | ---: | ---: | ---: | ---: |
| Canonical | Exterior | 1.59e-8 | 3.45e-7 | 3.31e-7 | 1.81e-7 |
| Canonical | Crossing | 1.08e-8 | 8.30e-7 | 8.25e-7 | 1.80e-7 |
| Canonical | Changing metric | 1.59e-8 | 3.45e-7 | 3.30e-7 | 1.81e-7 |
| Nonlinear | Exterior | 1.58e-8 | 3.57e-7 | 3.42e-7 | 1.81e-7 |
| Nonlinear | Crossing | 1.07e-8 | 8.27e-7 | 8.22e-7 | 1.81e-7 |
| Nonlinear | Changing metric | 1.58e-8 | 3.56e-7 | 3.42e-7 | 1.81e-7 |

All fields pass the finest .001 relative-plus-1e-9 absolute accuracy gate;
the worst finest relative error in this table is about 1.27e-5. Spatial
reductions and time-halving checks pass for both models without dropping
boundary points. P,Q,alpha stay positive. The nonlinear crossing minimum Q is
about .9980; the test does not probe proximity to loss of hyperbolicity.

The listed integrated energy-budget errors are between 1.3e-18 and 4.0e-17.
Changing-metric instantaneous work at T=.15 is 3.7690e-4 (canonical) and
3.7666e-4 (nonlinear), and was not zeroed. Tiny budget errors reflect the
structure-preserving accounting on these smooth short runs, not a black-hole
energy theorem. The central Schwarzschild curvature singularity is untouched.

## 4. Derive the mass-source simplification from the parent

Use p=q/E, D0=kappa*r*P*s^2 and C0=kappa*r^2*E*P*p*(p+F*s).
The existing tilted mass constraint has gradient
(G_chi,G_q,G_mu,G_delta,G_w) with respect to (chi,q,mu,delta,w).
For ADDITIVE NUMERICAL evolution sources, the local state transformation gives

    S_q = (S_h+B*S_w-h_mu*S_mu-h_delta*S_delta)/alpha,
    h_mu=-2h_F/r, h_delta=E*h_E.

Substitution into the parent constraint gives four exact Schur identities:

    beta = G_q/alpha = kappa*r^2*p,
    G_mu-beta*h_mu = -D0,
    G_delta-beta*h_delta = -sigma*C0,
    G_w+beta*B = kappa*r^2*P*(p+F*s).

Also G_chi=kappa*r^2*m_chi^2*chi. Hence the source completion is

    (D_R+D0) S_mu
      = kappa*r^2*[p*S_h+P*(p+F*s)*S_w+m_chi^2*chi*S_chi]
        -sigma*C0*S_delta.

This is a parent-derived numerical compatibility relation, not a newly fitted
physical coupling law. It neither cancels the background defect nor sets the
physical constraint to zero. D0 is nonnegative for kappa>0,P>0, but that fact
alone supplies neither global coupled stability nor a small physical coupling.

With prescribed outer S_mu=0, the discrete derivative's unused outer row adds
one compatibility condition. Let ell be its normalized adjoint covector and
g the complete RHS above. An interior-only modification of S_h can enforce
ell.g=0. With a_i=ell_i*beta_i set to zero at both endpoints and positive
declared weights W_h, the minimum-change solution is

    d = sum(a_i^2/W_h_i), mismatch=ell.g,
    Delta S_h_i = -mismatch*a_i/(d*W_h_i),
    ||Delta S_h||_(W_h)^2 = mismatch^2/d, when d>0.

This is the elementary weighted least-norm one-constraint projection, not an
assumption about physical dissipation. The checker uses
W_h=SBP_weight*r^2/alpha. Its norm can become large as d tends to zero; no
uniform estimate follows without a lower bound or separate compatibility proof.
At p=0 everywhere, beta=C0=0. A compatible RHS is accepted without division;
an incompatible RHS with no adjustable interior direction is rejected.

The code preserves S_chi,S_w,S_delta, both endpoint S_h values, and outer
S_mu=0. These assertions do NOT imply endpoint S_q is unchanged: changing
S_mu changes S_q through -h_mu*S_mu/alpha. This distinction must be carried
into the coupled boundary operator; importing the old q penalty unchanged
would not be justified. In particular, to preserve a specified S_q at an
endpoint one must enforce

    S_h = alpha*S_q-B*S_w+h_mu*S_mu+h_delta*S_delta

there, and derive the actual coupled incoming characteristic condition rather
than arbitrarily fixing both h and q sources.

## 5. Source-completion checks and remaining scope

Owner: `source-intake/navier-stokes/20260909/annular-momentum-noether-completion-derived/status.json`.
Complete at 05:32:18 UTC: 29/29 checks. Four symbolic identities are checked
exactly; four saved N512 canonical/nonlinear sources at T=.1,.3 are replayed.
New nonzero chi, gradient, h and lapse sources are also completed and tested
against the independently saved parent gradient. Maximum replay discrepancy
is 3.31e-24 for sources of order 1e-8. Full all-row parent source residuals
are 2.00e-22 to 5.30e-22 for terms of order 1e-9. The p=0 compatible and
incompatible cases behave as specified. These are floating-point replay and
identity checks, not certified continuum bounds.

The earlier selected correction remains FAILED 136/137. Its canonical first-u
T=.3 boundary gate is not retested or repaired by the manufactured solver.
All four previous actual-curvature sensitivity gates remain failed, including
the mass-only Volterra reconstruction. No prior gate or source was overwritten.

The next calculation should use the current variables in the ACTUAL parent
mass/lapse evolution, first with the full boundary source transformation and
retained background residual. Then run the canonical and nonlinear cases under
matched conditions and re-evaluate the old all-row boundary and curvature
checks. The scalar/mass numerical source completion is now available for that
implementation; full source-work control, higher-curvature corrections,
physical coupling calibration and a derived local-GR limit remain open.

## 6. Reproducibility and source map

All paths below are relative to this post-checkpoint-work directory.

- `scripts/annular_conservative_scalar_evolution_20260909.py`: new control solver.
- `scripts/run_annular_conservative_scalar_controls_20260909.py`: matched runner.
- `scripts/annular_momentum_noether_completion_20260909.py`: transformed completion.
- `scripts/derive_annular_momentum_noether_completion_20260909.py`: symbolic/replay checks.
- `scripts/validate_annular_current_savepoint_20260909.py`: saved-output verification.
- `scripts/annular_noether_completion_20260909.py`: prior parent constraint gradient.
- `scripts/annular_coordinate_evolution_operator_20260909.py`: prior annular fields.
- `scripts/sbp4_derived_operator_20260909.py`: prior derivative.
- `scripts/sbp4_compatible_second_operator_20260909.py`: prior norm weights.
- `DERIVATION-20260909-source-retaining-Volterra-and-conservative-momentum.md`: prior derivations and failed reconstruction.
- `source-intake/navier-stokes/20260909/annular-constraint-correction-initial/canonical.json`: canonical fixture.
- `source-intake/navier-stokes/20260909/annular-constraint-correction-initial/nonlinear_modulated.json`: nonlinear fixture.
- `source-intake/navier-stokes/20260909/annular-boundary-preserving-refined/status.json`: preserved failed correction.
- `source-intake/navier-stokes/20260909/annular-volterra-constraint-reconstruction-initial/status.json`: preserved failed curvature gates.

Each new owner contains its executed runner snapshot, SHA256 inputs, status
and completion marker. The scalar owner additionally contains 48 hashed NPZ
outputs. A COMPLETE marker means the owner's declared checks passed, not that
MTS or local GR has passed. All work is private; no GitHub, frozen workbench or
galaxy modifications. No subagents or shared-process shutdowns were used.
