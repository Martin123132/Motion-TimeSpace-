# Metric-link quadratic action and short matched evolution

2026-09-09. Private computational continuation. No GitHub action.
This is a local finite-action calculation, not an empirical MTS validation,
black-hole regularity theorem, or completion of the local-GR limit.

## 1. What changed this turn

The metric-reconstructed time-link action now has its OWN checked quadratic
reduction, scalar Legendre matrix and complete metric primary pairing.
Its old nodal-connection counterpart's stability tests were not inherited.
Independent nonlinear characteristic integration checks the second variation.

A short, genuine time integration then evolves the differentiated-constraint
branch for both GR/P(X) and the new Gram action. There is no root reprojection,
constraint damping, residual subtraction or boundary-data adjustment during
the run. This is not a full solution of the coupled DAE: the separate shift
equations are retained as unsatisfied diagnostic equations on every face.

Three validation owners finish 94/94, 94/94 and 142/142. These are formula,
implementation and finite-run checks, NOT 330 independent physical successes.
All workers finish; previous runs and failed attempts are untouched.

## 2. The corrected connection and its second variation

Use the previous areal ADM chart on R in [5.875,6.125], with

    F_h = 1 - 2 mu_h/R - Lambda R^2/3,
    c_h = 1/(N_h^2 F_h),
    A_h = -c_h V_h/(1-c_h V_h^2).

The background has V=V_t=0 after variation. mu and V are face-basis fields;
N is a nodal-basis field. Form these reconstructed fields BEFORE taking
their products/inverses. For perturbations (delta mu, delta N, v), define

    u = 2 delta mu_h/(R F_h) - 2 delta N_h/N_h,
    c_t = c_h [2 mu_h,t/(R F_h) - 2 N_h,t/N_h].

Writing A=epsilon A1+epsilon^2 A2+..., the coefficients are

    A1=-c_h v_h,
    A2=-c_h v_h u,
    A1_t=-(c_t v_h+c_h v_h,t).

For each factor-anchor to scalar-node characteristic, write
phi(t,R)=t+epsilon y(t,R)+epsilon^2 z(t,R)+... with y=z=0 at its anchor.
Expanding phi_R=-A(phi,R) gives the explicit nested-integral laws

    y(R) = integral_anchor^R c_h v_h ds,
    y_t(R) = integral_anchor^R (c_t v_h+c_h v_h,t) ds,
    z(R) = integral_anchor^R [c_h v_h u
                             +(c_t v_h+c_h v_h,t)y(s)] ds.

The c_t and partial-path y(s) terms are necessary. Replacing the partial
path by its endpoint, or interpolating the nodal inverse metric, is not
this action. Signed Gauss integration splits at all face and node knots;
integrated Lagrange bases provide the partial-path primitive. Both link
directions and polynomial degrees 0-4 have independent analytic controls.

For a=a0+epsilon a1+epsilon^2 a2, its pulled-back density obeys

    a(phi) phi_t = a + epsilon [a1+d_t(a y)]
                      +epsilon^2 [a2+d_t(a1 y+a z+a_t y^2/2)] + ... .

With the fixed Gram matrices T,S, let l=T chi, rho_factor=l^2/(2h).
The removed quadratic time-boundary term is explicitly

    B2 = sum_factor rho_factor S[a1 y+a z+a_t y^2/2].

Subtracting d_t B2 leaves first perturbation velocities only. The raw
second variation equals the reduced coefficient plus d_t B2, not the
reduced coefficient alone. The inherited algebraic product identity in
LocalQuadraticPath.quadratic is reused, but its metric connection, background
jets and independent nonlinear action evaluator are replaced and rechecked.

The source continuation retains

    I(t)=I0+t I_t0+t^2 I_tt0/2,
    chi(t)=chi0+t q0+t^2 q_t0/2,
    w(t)=D chi(t)+I(t).

In particular, w_tt=D q_t+I_tt is NOT silently reset to zero. These are
declared local jets for the test, not a derived future global solution.

## 3. Scalar and metric quadratic structure

At zero shift the scalar velocity block is

    M_chi = H_chi^T W diag[R^2 L/N (P-2 P_X q_quad^2/N^2)] H_chi
            - diag(rho_node a_qq),
    rho_node = S^T[(T chi)^2]/(2h).

The canonical a_qq correction is identically zero. On the nonlinear fixture
the correction/bare-matrix norm ratios are 1.247e-8 at N16 and 7.550e-10
at N32. All four tested full scalar matrices are positive definite:

| fixture | intervals | minimum scalar kinetic eigenvalue |
|---|---:|---:|
| canonical | 16 | 0.1856364 |
| canonical | 32 | 0.0927423 |
| nonlinear | 16 | 0.1889511 |
| nonlinear | 32 | 0.0943961 |

These are unscaled finite nodal matrices. Their eigenvalues depend on the
basis and grid; they are not physical masses or uniform continuum bounds.

The reduced Gram quadratic term has no mu_t^2, N_t^2, V_t^2 or mixed
metric-velocity-square term. Its metric velocity-position contribution
is confined to V_t--V. There is no V_t--mu or V_t--N block. Explicitly,
if H=integral c_h Q_face, define

    A_factor,j = sum_i S_factor,i a_i H_(factor,i),j,
    B_factor,j = sum_i T_factor,i q_i H_(factor,i),j,
    j_factor,i = a_i S_factor,i l_factor (Tq)_factor/h
                  -q_i T_factor,i (Sa)_factor l_factor/h,
    R_(factor,i),jk = integral c_h Q_face,j [integral_anchor^R c_h Q_face,k] dR.

For the Lagrangian L=bulk-U, the complete new metric block is

    C_(V_t,V) = -A^T diag(l/h) B + sum_factor,i j_factor,i R_(factor,i).

This analytic dense block is checked against direct mixed quadratic probes.
It is not assembled by dropping small or inconvenient entries. The gravity
pairing remains

    B_grav = Q_face^T W diag[1/(kappa N_h F_h^(3/2))] Q_face > 0.

In the order (mu,V,N), the metric primary two-form therefore has blocks

    Omega = [[0, B_grav, 0],
             [-B_grav^T, C-C^T, 0],
             [0, 0, 0]].

Its rank is 36 of 53 at N16 and 68 of 101 at N32, retaining respectively
17 and 33 lapse null directions. This is a primary metric-sector result,
not a proof of secondary Dirac closure, full mode count or ghost freedom.
Independent nonlinear link integrations at epsilon=0.01 and 0.005 agree
with raw quadratic coefficients to absolute error <=6.65e-11 in these
four probes. No claim of symbolic proof follows from that numerical error.

## 4. What was actually time-integrated

Let y=(mu_faces,N_nodes,q_nodes), and use the existing Routh functional

    R=L_bulk(V=0)-U_Gram(V=0)-pi^T q-E_b mu_outer/kappa.

The GR control omits only U_Gram. G=R_y and H=R_yy are evaluated from this
same functional. Free rows exclude only inner mass and the two prescribed
scalar endpoint velocities. All lapse rows remain free.

The integrated state is (chi,pi,y), with

    chi_dot=q,
    pi_dot=(L_chi)_interior,  pi_dot_endpoints=0,
    mu_dot_inner=[B_grav^-1(U_V-J_matter)]_inner,
    q_dot_endpoints=the previously declared endpoint accelerations,
    H_free,free y_dot_free = -(H y_dot_fixed + dG_data)_free.

Here dG_data includes the actual chi_dot, pi_dot, I_t, I_tt and E_b,t
variations. It is computed independently of the y Jacobian. The source
histories for I and E_b are the same prescribed local Taylor histories
in both branches. No new scalar field or fitted coupling is introduced.

Use classical RK4 from relative t=0 to t=0.01 in the fixture normalization,
with 4, 8 and 16 steps, two grids N16/N32 and two fixtures. That is 24 short
trajectories. No physical time in seconds is assigned to this test. Initial
scalar, interior canonical momentum, inner mass, spatial patch and all
external/boundary jets match exactly across GR and candidate branches;
their independently solved metric roots need not be identical.

The unintegrated shift equations are measured without filtering:

    E_V = B_grav mu_dot_constraint + J_matter-U_V,
    mismatch = mu_dot_constraint-mu_dot_flux.

This ODE deliberately enforces dG_free/dt=0. Consequently small G drift is
an integrator/constraint-tangent test, NOT independent evidence that every
Euler equation is satisfied. The nonzero E_V prevents that inference.

## 5. Short-run results and their limits

Finest time step: maximum constraint CHANGE over each run is
6.75e-15 to 9.90e-15. Absolute constraints also retain their initial root
error, up to 4.80e-13 at N16. Scalar Legendre blocks stay positive at all
saved times. Endpoint differences under successive time refinement improve
by factors 12.77-21.20, consistent with this short RK4 test. This is not
a long-time stability or convergence theorem. States actually change by
about 0.00165-0.00171; the runner is not merely replaying a fixed initial slice.

Maximum mass-rate mismatch over t in [0,0.01], at 16 time steps:

| fixture | grid | GR | new Gram | new/GR |
|---|---:|---:|---:|---:|
| canonical | 16 | 8.744e-6 | 6.295e-6 | 0.720 |
| canonical | 32 | 4.036e-6 | 4.179e-6 | 1.035 |
| nonlinear | 16 | 9.306e-6 | 6.349e-6 | 0.682 |
| nonlinear | 32 | 3.666e-6 | 3.787e-6 | 1.033 |

Do not select a favorable norm: the N16 WEAK shift residual new/GR ratios
are 1.253 and 1.259 even though the mass-rate norm is smaller. At N32 the
weak residual ratios are 1.036 and 1.034. Thus comparable numerical behavior
is supported; superiority to GR is not. Only two spatial grids were evolved.

Mismatch grows over this short time window in both branches. It does not
vanish when the time step is reduced. At N32 the final weak shift residuals
are 5.956e-7/5.638e-7 for the candidate versus 5.748e-7/5.450e-7 for GR.
These are still unresolved equations, not acceptable physical error bars.

## 6. The remaining error has a constructive decomposition

Recompute the full finite Ward identity at the initial, midpoint and final
state of each fine trajectory. An explicit Hermite right inverse covers
every shift face; no SVD cut, least-squares projection or mode filter is used.
The independent calculation reconstructs all saved shift residual vectors.

The split includes bulk interpolation/product terms, Gram coefficient/link
terms, lifting Euler work, scalar and mass boundary reactions, and lapse
constraint-rate work. At the final canonical N32 state, candidate maximum
norms after the declared right-inverse map are:

    bulk reconstruction       1.946e-7
    Gram link                 2.856e-8
    Gram coefficient          1.896e-16
    lifting work              1.112e-7
    scalar boundary/bulk      1.245e-4
    mass boundary/bulk        1.250e-4
    lapse constraint rate     3.765e-20

The scalar and mass terms largely cancel as signed vectors; the listed
max norms cannot be added as a physical decomposition. GR has analogous
large cancelling boundary terms. This basis-dependent split identifies
where to investigate, not a unique attribution of physical error.

The lifting Euler equation is genuinely not solved on these prescribed
histories. Its final N32 max norm is 6.73e-6/7.06e-6 for the candidate and
6.18e-6/6.49e-6 for GR. A full Ward identity need not make E_V vanish while
that equation and boundary compatibility remain unresolved.

## 7. Next derivation: release the interpolation slopes from their action

Do not rerun a longer prescribed-history job and call it progress. The next
constructive step is to use the already present scalar interpolation
variables, not invent a compensating current. The lifted Hermite scalar is

    chi_h=H_chi chi+H_I I,  q_h=H_chi q+H_I I_t,
    w_h=G_chi chi+G_I I,    w_node=D chi+I.

Varying this SAME action in I, at the zero-shift slice, gives

    Pi_I = H_I^T W [R^2 L P q_h/N],
    d_t Pi_I = H_I^T W [-R^2 N L m_chi^2 chi_h]
                +G_I^T W [-R^2 N L P F_h w_h]
                -rho_node a_w.

The Gram term has no I_t derivative at this slice: nodal Hermite lifting
values are zero, whereas its coefficient depends on the nodal gradient I.
These equations follow from the same force and lifting momentum used in
the checked Ward identity. They have not yet been integrated as a released
degree of freedom. I remains a scalar interpolation slope coordinate, NOT
an additional fundamental matter field inferred by this calculation.

First derive/check the enlarged (q,I_t) Legendre matrix, then solve consistent
initial constraints in that enlarged space using the SAME physical data.
GR must undergo the identical release. Boundary conditions must come from
the complete variation/characteristic compatibility, not be adjusted to
cancel E_V. Test whether the lifting and boundary residuals actually shrink.
If that needs more boundary data than the source supplies, identify those
data rather than manufacture them. A full shift-unfixed Dirac/evolution
analysis remains necessary even if that next numerical branch succeeds.

## 8. Reproducibility and ownership

All paths below are relative to post-checkpoint-work. No prior source is
edited; no publication, broad CPU job or external code execution occurs.
One BelowNormal single-core Python worker at a time; all terminate normally.

- `scripts/annular_metric_link_quadratic_20260909.py`.
- `scripts/derive_annular_metric_dynamics_20260909.py`.
- `scripts/verify_annular_metric_evolution_20260909.py`.
- `scripts/finalize_annular_metric_dynamics_20260909.py`.
- `source-intake/navier-stokes/20260909/annular-metric-quadratic-derived/status.json`.
- `source-intake/navier-stokes/20260909/annular-metric-evolution-smoke/status.json`.
- `source-intake/navier-stokes/20260909/annular-metric-evolution-independent-controls/status.json`.
- `source-intake/navier-stokes/20260909/annular-metric-dynamics-final-integrity.json`.
- `DERIVATION-20260909-local-Ward-identity-and-metric-reconstructed-time-links.md`.

Each run owns its executed script, inputs, arrays and status. Final integrity
checks hashes, local citations, compilation without bytecode, a frozen-workbench
mtime scan since the turn start, and an immutable snapshot of the resume.
The mtime scan is explicitly not a pre-turn full filesystem hash comparison.
