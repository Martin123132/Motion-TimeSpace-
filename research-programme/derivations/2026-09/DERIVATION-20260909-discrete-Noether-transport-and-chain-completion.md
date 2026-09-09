# Discrete Noether transport and a derived chain-rule completion

Private continuation, 2026-09-09. Previous turn classified as progress from its
saved derivations, fixed-data evolution and independent validation. The full
MTS-to-GR/Newton/Maxwell/calibrated-coupling goal remains open. This step
identifies the source of a numerical mass-constraint drift and constructs an
explicit correction for it without changing the parent physical coefficients
or the second-corner initial data.

## 1. What the initial-data diagnosis actually establishes

For current variables y=(chi,w,h,mu,delta), the discrete kinematic mismatch is

    eta_h = e_w - D_h e_chi.

Because chi_t=q and w_t=D_h q, with zero chi/w numerical sources and the
consistent background kinematic defect, eta_h is preserved, not automatically
zero. The saved analytic initial lift has w0=partial_R chi0, not D_h chi0.
At the inner endpoint its mismatch can be evaluated exactly from the known
degree-seven polynomial profiles and the rational stencil moments:

    eta_h = -sum_(k=2)^7 chi0^(k)/k! * sum_j D_ij (R_j-R_i)^k.

This identity was checked at both endpoints for both fixtures and all three
saved resolutions. N512 maxima are 4.30718e-13 (canonical) and 2.68952e-12
(nonlinear). The mismatch is still present at both saved times, as required
by the discrete evolution. It is a discretization effect, not by itself a
proof of the observed refinement failure. Simply setting it to zero would
change the discrete lift and its boundary compatibility; that was NOT done.

Initial bulk spatial truncation, evaluated against analytic initial radial
derivatives and the continuum operator, peaks at the inner boundary in the
momentum component. For N128/256/512 its nonlinear maxima are
6.19879e-10, 1.74846e-10 and 4.62623e-11. Its induced initial chi_tt errors
are 6.27640e-9, 1.77035e-9 and 4.68415e-10. These decrease with resolution;
the diagnosis does not establish that they alone cause the later nonmonotonic
chi/mu differences. The compact initial profiles join zero at R=5 and R=7
through third derivative, not with arbitrary smoothness.

The next corner condition is also nonzero. With F=A+B partial_R,

    e1=F0 e0-d0,
    e2=F_t0 e0+F0 e1-d_t0,
    e3=F_tt0 e0+2F_t0 e1+F0 e2-d_tt0,
    C3=L0 e3+3L_t0 e2+3L_tt0 e1+L_ttt0 e0.

Nine-point calculations with halved steps, and an eleven-point check, give
approximately (inner scalar, outer scalar, outer lapse):

    canonical: (1.559e-7, -5.02e-4, 4.121e-9),
    nonlinear: (-6.829e-7, 4.819e-3, -4.315e-8).

These are numerical estimates, not certified exact values. They warn against
assuming the higher regularity needed by curvature jets. No third-corner data
were fitted or substituted in this experiment. Diagnosis owner: 26/26 checks;
its finite-C3 checks do not certify C3=0 or establish causation.

## 2. Exact continuum and discrete mass-gradient identities

Write the linearized current equation as

    e_t=A e+B partial_R e-d+S,

where d is the actual background defect. Define rows q, f and c by
delta q=q.e, delta f=f.e, delta C0=c.e, and let g=partial_y G0. Here

    p=q_background/E, beta=kappa R^2 p,
    g=(kappa R^2 V_chi, kappa R^2 f_background/E,
       beta, -D0, -sigma C0),
    c=g_w q+beta f-C0 unit_delta,
    rho=beta f_mu.

The full coupled principal identity is

    c-g B = rho unit_mu.

This includes the parent-derived -f_mu J term in h_t. It is not the identity
of the naive unreduced free evolution. With analytic coefficient derivatives,

    H=c_R-g_t-g A+rho g
      =J_background * partial_y rho - (partial_y g)[d].

The last term matters off shell: the background is approximate and its defect
must not be discarded. It follows by differentiating the continuum constraint
identity along y_background_t=F(y_background)+d and the correction equation
e_t=F'[e]-d. The Hessian contraction of G0 with d and e is retained. The
implemented expressions use holomorphic directional derivatives and were
checked against independent current gradients and direct saved RHS values.

Let

    j_h=D_h e_mu-g.e,
    J_h=J_background+j_h,
    N_h(S)=D_h S_mu-g.S.

For a coefficient a and nodal value z, define the discrete product error

    E_h(a,z)=D_h(a z)-a D_h z-a_R z.

The three-channel coupled commutator is

    K_h=sum_k E_h(c_k,e_k)
        -g_w sum_k E_h(q_k,e_k)
        -beta/R^2 sum_k E_h(R^2 f_k,e_k).

Expanding the actual flux-form difference operator gives the exact
semidiscrete identity, with analytic consistent coefficients,

    (j_h)_t=rho j_h+H.e-D_h d_mu+g.d+K_h+N_h(S),
    (J_h)_t=rho J_h+H.e+r_d+K_h+N_h(S),
    r_d=(J_background)_t-rho J_background-D_h d_mu+g.d.

Every endpoint row remains in these equations. The exact background derivative
is obtained from the existing fifth-order jet evaluator. In the continuum
r_d vanishes for a consistently evaluated background defect; the discrete
derivative and floating/cache evaluation errors are retained here.

Do not confuse j_h_t with J_h_t. The correction constraint derivative alone
is of order 1e-9 in the nonlinear replay, mostly canceling the background
constraint derivative. It is NOT a 1e-9 failure of the total mass constraint.

The time-cached numerical runner has an additional qualification: interpolated
coefficients need not satisfy nonlinear coefficient identities exactly between
cache nodes. If b_h=c-g B-rho unit_mu is nonzero, retain b_h.D_h e in this
transport formula and use the actual interpolation derivative in g_t. The
saved-output replays are at cache nodes. They do not establish a uniform
in-time bound on interpolation remainder or on the unknown continuum solution.

## 3. A computable all-row commutator bound

For a stencil differentiating constants exactly,

    E_h(a,z)_i = z_i[(D_h a)_i-a_R,i]
      +sum_j D_ij(a_j-a_i)(z_j-z_i).

Consequently

    |E_h(a,z)_i| <= |z_i| |(D_h a)_i-a_R,i|
      +sum_j |D_ij| |a_j-a_i| |z_j-z_i|.

Sum the three channels with |g_w| and |beta|/R^2 to bound |K_h|. No derivative
of an unknown continuum solution is inserted into this nodal algebraic bound.
It is valid also for alternating grid values; it need not be small for them.
The bound is computed from the inputs, not fitted to the observed residual.
Floating calculations are not outward-rounded interval certificates. An exact
increment identity and smooth/alternating controls support the implementation.

For a real coefficient rho, the total constraint satisfies the integrating-
factor formula and hence

    |J_i(t)| <= exp(I_i(t)) * [|J_i(0)|
        +integral_0^t exp(-I_i(s)) |F_i(s)| ds],
    I_i(t)=integral_0^t rho_i(s) ds,
    F_i=H_i.e_i+r_d,i+K_i+N_i,

with any interpolation remainder added when using cached coefficients.
This is a derived conditional bound, not an evaluated global certificate:
saved endpoints alone cannot bound the intervening time integrals.

## 4. Measured drift channels on the unchanged failed run

The corrected replay passes 91/91 algebra/software checks on twelve saved
outputs. At N512 the maxima in normalized fixture units are:

| Fixture / time | Total constraint time derivative | Product-rule term K_h | Forcing remainder r_d | Physical/off-shell H.e |
| --- | ---: | ---: | ---: | ---: |
| Canonical .1 | 5.1523e-14 | 5.3954e-14 | 5.4578e-14 | 1.3169e-17 |
| Canonical .3 | 1.0493e-13 | 9.7935e-14 | 4.4150e-14 | 1.0423e-16 |
| Nonlinear .1 | 3.2009e-13 | 3.4552e-13 | 2.5261e-14 | 2.5496e-16 |
| Nonlinear .3 | 4.4999e-13 | 4.8930e-13 | 4.8188e-14 | 1.2938e-15 |

Maxima need not occur at the same node, so do not add this table's columns
as if they were co-located scalars. The old N_h(S) residual is only about
1e-25: it completes the explicitly assigned sources but leaves the bulk
product-rule error. This establishes a specific numerical source of drift;
it does NOT establish that K_h alone causes the failed chi/mu mesh comparison.
The conservative commutator bound is about 1.2e-9--1.6e-9 for the finest
nonlinear examples, much looser than the measured K_h. Do not claim it is
already a useful physical local-GR bound.

The initial replay owner remains FAILED 61/79. It recomputed forcing instead
of using the exact saved forcing and used an absolute 1e-21 floating comparison
for weighted-flux products. The corrected replay uses the saved forcing and
retains that difference (up to about 1.7e-18 at T=.1); differentiation amplified
it to about 7.9e-17 in the failed replay. Its stencil-product arithmetic check
is explicitly scale-aware, not a changed evolution accuracy gate. Full
transport replay errors are below 2e-22. Failed records were not overwritten.

## 5. Construct a targeted discrete chain completion

Rather than imposing J_h=0 or removing a physical residual, select ONLY the
derived numerical target

    N_h(S)=-K_h.

Then K_h+N_h(S) cancels while rho J_h, H.e and r_d remain in the transport
equation. This is a different numerical-source contract from N_h(S)=0, not
an assertion that the old standalone source identity still holds.

In coordinate source variables, S_chi=S_w=0 and

    (D_h-G_mu)S_mu=G_q S_q+G_delta S_delta-K_h,
    S_mu(R_out)=0.

Keep both endpoint q sources and all lapse sources unchanged. The existing
anchored derivative matrix has one remaining compatibility covector n. With
the endpoint entries of v=n G_q suppressed and positive weights W,

    mismatch=n.(G_q S_q_raw+G_delta S_delta_raw-K_h),
    delta S_q=-mismatch W^(-1)v/(v^T W^(-1)v).

This is the unique least-W-norm interior q correction enforcing that affine
compatibility constraint when the denominator is positive. Its norm is
|mismatch|/sqrt(v^T W^(-1)v). Solve the anchored mass system with the resulting
forcing, then transform S_h=alpha S_q+h_mu S_mu+h_delta S_delta. No raw
boundary condition, physical coupling, test data or incoming speed is tuned.

The construction is singular if the denominator vanishes with nonzero
mismatch. Small denominators or an unbounded anchored inverse remain possible
outside the tested fixtures; no uniform stability theorem is smuggled in.
For smooth mesh families K_h tends to zero with the consistent derivative,
but vanishing completed corrections additionally require control of this
projection and inverse. Full coupled source/energy bounds remain open.

Four saved N512 replays pass 18/18 construction checks. All-row target
residuals are below 2.4e-25 and the normalized projection denominators are
0.256--0.327. Endpoint q, all lapse and zero outer mass sources are preserved.
These are operator controls, not an evolution pass.

## 6. Fixed-data evolution test

The new run uses the SAME second-corner initial data, canonical/nonlinear
fixtures, N128/256/512, T=.1,.3, finest time halving, zero filter and physical
accuracy gates. Only source completion changes to the derived K_h target.
It records N_h(S) and K_h separately as well as their sum; no physical
background defect or full constraint is set to zero.

Completed at 07:08:20 UTC: **FAILED 129/131**. The two failed grouped checks
are canonical T=.1 q refinement and nonlinear T=.1 chi/mu refinement. Both
T=.3 spatial comparisons and every time, finest scalar-boundary, lapse,
mass-constraint, integrability and completed-chain gate pass. The standalone
check name inherited from the runner says source_Noether_identity, but this
branch's metadata and saved arrays explicitly identify the tested quantity as
N_h(S)+K_h, NOT N_h(S). No standalone-zero source claim is made.

| Failed component | Coarse difference | Fine difference | Allowed fine difference |
| --- | ---: | ---: | ---: |
| Canonical .1 q | 2.05597e-12 | 1.62124e-12 | 1.58162e-12 |
| Nonlinear .1 chi | 8.23749e-14 | 1.03833e-13 | 6.34653e-14 |
| Nonlinear .1 mu | 1.09002e-14 | 1.09944e-14 | 8.48474e-15 |

The same coarse/1.3+1e-16 threshold is used throughout. The canonical q gate
previously passed with second-corner data and the old source completion; its
failure is a regression, not hidden by improved constraint behavior.

However, the targeted constraint improvement is real. Comparing N512 dt2
outputs with IDENTICAL initial data, coefficients and boundary choices:

| Fixture / time | Old total mass-constraint maximum | New maximum | Old/new ratio |
| --- | ---: | ---: | ---: |
| Canonical .1 | 5.02873e-15 | 1.17149e-15 | 4.29 |
| Canonical .3 | 2.36196e-14 | 1.24155e-16 | 190.24 |
| Nonlinear .1 | 3.56611e-15 | 3.70218e-15 | 0.963 |
| Nonlinear .3 | 1.55863e-13 | 3.05675e-15 | 50.99 |

Thus late-time constraint residuals improve substantially, while the early
nonlinear constraint maximum is slightly worse. These are discretized,
normalized-fixture residuals, not observational or continuum error bounds.

Independent validation completes **103/103**, 07:08:39 UTC. It checks the
zero-denominator compatible and incompatible controls, actual executed/input
hashes, all sixteen saved outputs, unchanged data/physical accuracy gates,
independent recomputation of the failed mesh comparisons, and separate raw
source/commutator storage. Four finest half-step replays recompute the full
constraint transport. Independent K_h+N_h maxima are below 1.41e-22; physical
H.e remains nonzero. This validates the evidence, NOT a physics pass.

**Decision:** retain the derived transport law and the chain completion as a
tested numerical candidate, but do not promote this failed run or change the
default source option to it. Removing the identified product-rule drift is
demonstrably insufficient to resolve the remaining field-refinement failures.
Do not launch another mass-source projection/filter variant on that premise.

**Next derivation target:** determine the boundary-jet regularity actually
required by the existing third-derivative curvature/K1 transfer and construct
the corresponding compatibility hierarchy from the parent PDE. Use analytic
jet recurrence rather than repeatedly differentiating noisy endpoint samples.
The measured C3 mismatch and finite cutoff regularity are concrete starting
points. A new higher-regularity test family, if constructed, must be declared
as new data and compared under both canonical/nonlinear models; it does not
retroactively validate the old data. Full source/energy bounds, coefficient
interpolation control, curvature error and physical coupling calibration
remain obligations. No C3, first-u or black-hole regularity proof is claimed.

Safe save point: all computations from this continuation have exited. The
old 128/129, original 136/137 first-u and four curvature failures stay open.

## 7. Source map

Paths are relative to this post-checkpoint-work directory.

- `scripts/diagnose_annular_second_corner_truncation_20260909.py`
- `scripts/annular_discrete_constraint_transport_20260909.py`
- `scripts/derive_annular_discrete_constraint_transport_20260909.py`
- `scripts/annular_discrete_chain_completion_20260909.py`
- `scripts/derive_annular_discrete_chain_completion_20260909.py`
- `scripts/validate_annular_discrete_chain_experiment_20260909.py`
- `scripts/run_annular_coupled_current_correction_20260909.py`
- `scripts/annular_noether_completion_20260909.py`
- `source-intake/navier-stokes/20260909/annular-second-corner-truncation-diagnosis/status.json`
- `source-intake/navier-stokes/20260909/annular-discrete-constraint-transport-derived/status.json`
- `source-intake/navier-stokes/20260909/annular-discrete-constraint-transport-saved-forcing/status.json`
- `source-intake/navier-stokes/20260909/annular-discrete-chain-completion-derived/status.json`
- `source-intake/navier-stokes/20260909/annular-coupled-current-discrete-chain/status.json`
- `source-intake/navier-stokes/20260909/annular-discrete-chain-experiment-validation/status.json`
- `DERIVATION-20260909-bounded-source-integration-and-second-corner-data.md`
- `DERIVATION-20260909-coupled-current-hyperbolicity-and-evolution.md`

All results remain non-claim for full MTS/local-GR/first-u/black-hole physics.
The physical coupling has not been calibrated. Work remains private; no GitHub,
frozen workbench/galaxy edits, subagents or stopped shared processes.
