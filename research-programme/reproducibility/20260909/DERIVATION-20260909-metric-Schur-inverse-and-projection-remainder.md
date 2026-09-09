# Metric Schur inverse: an explicit uniform bound, not a gridwise condition number

Date: 2026-09-09. Private canonical annular continuation.

## 1. Result and limitation

The inverse estimate requested by the preceding step is now derived in a
specified physical norm. For the actual canonical metric Schur complement,
including the owned Gram term and the natural outer boundary row,

    ||S_metric^-1||_(X* -> X) <= 175/118 < 3/2

for EVERY supported grid with at least 17 scalar nodes and EVERY canonical
configuration in the explicit box in section 8. This is not extrapolated
from three measured singular values. The geometric inf-sup constant and
the final box inequalities have exact rational certificates.

X controls the mass H1 seminorm and a nodal h-weighted lapse L2 norm.
It does NOT by itself control the pointwise lapse derivative or outer lapse
trace. Nor have we proved that the coupled dynamics stay in this box, or
that the first/second differentiated forcing is uniformly bounded over a
time interval. Those are the next evolution/source estimates.

Thus this is a conditional stability theorem for the canonical linearized
constraint response, not full DAE closure, black-hole regularity, nonlinear
P(X) control, a new physical coupling measurement, or a complete MTS-to-GR limit.

## 2. Sources and reproduction

Preceding jets, physical mismatch, and source construction:
`DERIVATION-20260909-metric-flux-cancellation-and-exact-constraint-jets.md`.
Actual scalar/metric Hessian:
`scripts/annular_released_hermite_action_20260909.py` and
`scripts/annular_constraint_routhian_20260909.py`.
Actual staggered geometry and Gram template:
`scripts/annular_mixed_grid_basis_20260909.py`,
`scripts/sbp4_compatible_second_operator_20260909.py`, and
`scripts/annular_gram_joint_action_20260909.py`.

New helper:
`scripts/annular_metric_schur_bound_20260909.py`.
Derivation/validation runner:
`scripts/derive_annular_metric_schur_bound_20260909.py` (derive phase).
Exact common-box certificate and **combined final seal owner**:
`scripts/certify_annular_metric_schur_box_20260909.py` (derive/seal).
Results:
`source-intake/navier-stokes/20260909/annular-metric-Schur-bound-derived/status.json`
and
`source-intake/navier-stokes/20260909/annular-metric-Schur-box-certified/status.json`.
Final integrity:
`source-intake/navier-stokes/20260909/annular-metric-Schur-box-final-integrity.json`.

General background: [J. Schoberl, Mixed Methods, sections 21.1-21.2](https://jschoeberl.github.io/SciCADE-course/unit5-mixed/1_mixedmethods.html),
checked 2026-09-09, describes the relationship between inf-sup estimates,
inverse operators and saddle systems. The constants and projection/Gram
estimates below are derived from this local action and grid; that reference
does not establish the present MTS result.

## 3. Norm, boundary and exact Schur complement

Let xi be a mass perturbation in the actual continuous P1 mass-face space,
with xi(a)=0, and n a lapse perturbation in the continuous nodal P1 space.
No lapse variable is fixed, including at the outer boundary. Put

    ||xi||_Xmu=||xi_R||_L2,
    ||n||_XN=sqrt(h sum_j n_j^2),
    ||(xi,n)||_X^2=||xi||_Xmu^2+||n||_XN^2.

The lapse norm is uniformly equivalent to continuous L2:
||n_h||_L2<=||n||_XN<=sqrt(6)||n_h||_L2. No inverse h factor is hidden in
that equivalence. The zero-inner mass trace gives ||xi||_L2<=ell||xi_R||.
Its nodal evaluations obey sqrt(h sum xi(R_j)^2)<=C_P||xi_R|| with
C_P=sqrt(17/16)ell for every n>=17.

After eliminating ONLY free scalar velocities, the actual free Hessian is

    J=[[H_metric,H_metric,v],[H_v,metric,M_free]],
    S_metric=H_metric-H_metric,v M_free^-1 H_v,metric=[[A,B],[B^T,D]].

M_free is the positive canonical scalar mass matrix for homogeneous-value
velocity variations. All released slope velocities remain free. The outer
mass row is retained; deleting it would destroy the square coupling on
which the following proof depends. The outer clock action is linear in
outer mass, so it enters the forcing/natural equation, not a Hessian penalty.

## 4. The lapse block is a projection remainder, not an assumed zero

Use m=R^2/(N sqrt(F)), p=R^2 N sqrt(F), A_rad=R F, q=chi_t, w=chi_R.
All inner products in this section are the ACTUAL positive Q[m . .] rule.
Let Pi be its orthogonal projection onto the free scalar-velocity space and
define e_mu=q xi/A_rad, e_N=q n/N.

The kinetic contributions after scalar elimination are exactly

    A_kin(xi,zeta)=one_half <e_mu(xi),e_mu(zeta)>
                     +<(I-Pi)e_mu(xi),(I-Pi)e_mu(zeta)>,
    B_kin(xi,n)=<e_mu(xi),(Pi-one_half I)e_N(n)>,
    D(n,l)=<(I-Pi)e_N(n),(I-Pi)e_N(l)>.

Hence D is positive semidefinite; it is generally NONZERO even in GR.
Products with a variable lapse need not lie in the finite free-velocity
space, and the prescribed endpoint velocities also matter. We do not
assume this block vanishes in operator norm as h tends to zero.

Since Pi is an orthogonal projection, ||Pi-I/2||=1/2. This gives a tighter
mixed kinetic bound than adding two unrelated projection norms. The
canonical Gram coefficient has no q dependence, so it does not add a
hidden kinetic/velocity term to D.

The runner independently reconstructs A, B and D from these identities,
the gravitational variations, the scalar gradient term and the nodal Gram
terms. They agree with the Schur complement of the old full Hessian.

## 5. Actual staggered geometry: exact inf-sup constant

Write z_i=xi_R on mass cell i. The mass cells have widths h omega_i, with
left weights (17,59,43,49)/48, unit interior weights, and reflected right
weights. The scalar/lapse grid is uniform. For lapse hat functions phi_j,
let H_ij=h^-1 integral_cell_i phi_j dR. Its first four rows, restricted to
the first five columns, are

    [1343/4608, 289/4608,       0,         0,    0]
    [ 961/4608,3919/4608,   49/288,        0,    0]
    [        0,  25/288,3199/4608, 529/4608,    0]
    [        0,       0, 625/4608,3503/4608,  1/8].

Every interior row is (1/8,3/4,1/8); right rows are reflections. Thus the
operator is tridiagonal and the boundary templates do not overlap for n>=17.
The exact minimum strict row and column dominance gaps are

    g_row=527/2304, g_column=191/2304,
    max omega_i=59/48.

At a maximal component of a vector, diagonal dominance gives
||H^-1||_infty<=1/g_row. Applying the same argument to H^T gives
||H^-1||_1<=1/g_column. Consequently
sigma_min(H)>=sqrt(g_row g_column). This is an all-grid argument because
there are only the stated boundary types and the repeated interior type.

For the reference bilinear form B0(xi,n)=(sigma0/kappa)Q[xi_R n_h],
positive quadrature integrates this piecewise polynomial product exactly.
The derivative coordinates have norm sqrt(h sum omega_i z_i^2). Therefore

    beta(B0)>=sigma0/kappa * beta_geom,
    beta_geom=sqrt(100657/6524928)>3/25.

The constant is about 0.124204 before the sigma0/kappa factor. No raw
Euclidean condition number of the full Hessian is involved.

## 6. Actual gravity, matter and Gram perturbations

Assume bounds F0<=F<=F1, N0<=N<=N1, |q|<=Q0, |w|<=W0,
|mu_R|<=U0. Let A0=a F0, and use m_+,p_+ as previously derived. Take
sigma0 midway between bounds on 1/sqrt(F), with half-width delta_sigma.

For the Gram coefficient density rho_j=S_sampling^T(T chi)^2/(2h),

    rho_j <= 2h W0^2.

To prove it, |D3 chi|<=4hW0; paired third-difference rows are <=8hW0.
Template margins are <1/8, adjacent magnitudes <1/128, extra magnitudes
<1/256. The sampling column sums in those three families are at most
1,1,1/2. Thus rho_j/(hW0^2)<=1+1/4+1/16=21/16<2. All bounds follow
from the source rationals and finite support, not sampled field eigenvalues.

The perturbation of the off-diagonal block obeys

    ||B-B0|| <= epsilon_B,
    epsilon_B=delta_sigma/kappa
       +ell U0/(kappa a F0^(3/2))
       +ell m_+ Q0^2/(2A0 N0)
       +ell p_+ W0^2/(2A0 N0)
       +2 C_P p_+ W0^2/(A0 N0) [Gram only].

The terms are, in order, principal coefficient variation, the gravitational
zeroth-order term, kinetic projection, scalar gradient, and Gram. Therefore

    beta=beta(B0)-epsilon_B>0

is a sufficient inf-sup condition for the ACTUAL B.

The remaining blocks satisfy ||A||<=a0 and ||D||<=d0, where

    a0=3N1 U0 ell^2/(kappa a^2 F0^(5/2))
       +2N1 ell/(kappa a F0^(3/2))
       +3m_+ Q0^2 ell^2/(2A0^2)
       +p_+ W0^2 ell^2/(2A0^2)
       +2p_+ W0^2 C_P^2/A0^2 [Gram only],
    d0=m_+ Q0^2/N0^2.

These estimates are uniform in h. No positivity of the full A is assumed;
its gravitational cross terms are bounded in absolute value. Bounds on q
and w are evaluated with Bernstein coefficients of their actual cubic and
quadratic reconstructions, not just maxima at a few quadrature points.

## 7. Bound the full inverse without removing D from the equations

Use S0=[[A,B],[B^T,0]] only as an estimation reference. For forcing (f,g),
its solution satisfies

    ||xi||<=||g||/beta,
    ||n||<=||f||/beta+(a0/beta^2)||g||.

Thus

    ||S0^-1||<=K0,
    K0=one_half[a0/beta^2+sqrt((a0/beta^2)^2+4/beta^2)].

The actual S_metric=S0+diag(0,D) is inverted by a convergent Neumann series
whenever K0 d0<1, with

    ||S_metric^-1||<=K0/(1-K0 d0).

This is a sufficient perturbation condition, not a necessary one. If beta
or the Neumann margin fails, this proof declines to certify the inverse;
it does not establish a physical instability. A manufactured large-field
control checks that the runner refuses rather than forcing a pass.

## 8. One explicit rational box, shared by all grids and both branches

To avoid mistaking state-by-state bounds for a uniform configuration set,
the separate certificate proves a single common box theorem:

    [a,b]=[47/8,49/8], ell=1/4, kappa=1/10,
    13/20<=F<=17/25, 4/5<=N<=21/25,
    |q|<=1/50, |w|<=3/100, |mu_R|<=1/500.

Use rational square-root majorants sqrt(F0)>=4/5, sqrt(F1)<=5/6,
1/sqrt(F) in [121/100,5/4], and C_P<=(21/20)ell. They yield

    m_+<=60025/1024, p_+<=16807/640,
    beta>=1983941859/1564160000 >5/4,
    a0<=410799492033/298656800000 <7/5,
    d0<=2401/65536 <1/25.

The 2-by-2 inverse majorant has K0<=7/5: its relevant positive-matrix
determinant is 41/625. Consequently

    K0 d0<=7/125,
    ||S_metric^-1||<=175/118<3/2.

All these constant inequalities are checked in exact rational arithmetic.
The Gram terms were INCLUDED in the common bound, so it also covers GR.
Every one of the 18 saved canonical states lies inside the box by the
ordinary floating-point field-envelope check. Membership is not an
outward-rounded interval certificate for the original nonlinear roots.
The analytical theorem applies to any configuration satisfying the box,
not only those 18 states or only the three tested resolutions.

Crucially, the proof does not show that a solution remains in this box for
all desired times. It is neither a horizon-crossing estimate nor a global
parameter calibration. The box is a sufficient local domain, not a new axiom
of MTS or a fitted set of theory parameters.

## 9. Apply the inverse to the unchanged first and second derivative sources

The old inner mass time rate is nonzero. Before estimating sources, lift
it as a CONSTANT mass field, so the correction has zero inner trace while
its derivative equals the physical mass-rate derivative. Lift the fixed
endpoint velocity-rate data with the same affine Hermite lift as before.
For second order those endpoint data vanish because the scalar histories
are quadratic. No slope boundary condition is added.

With derivative lift l_x and known differentiated forcing T,

    f=-T-J l_x,
    f_metric,eff=f_metric-H_metric,v M_free^-1 f_velocity,
    x_metric,derivative-l_x,metric=S_metric^-1 f_metric,eff.

T is the old data derivative at first order and the newly derived curved-
phase second forcing at second order. This is an algebraic decomposition of
the SAME solution, not changed boundary data. Without the constant inner
lift, a zero-inner extension of a nonzero physical trace could create an
artificial h-dependent derivative/source norm.

The reconstructed metric rates/accelerations agree with the old ones.
The estimate controls the physical mass-rate gradient and lapse L2 norm.
It also implies, for derivative order j=1,2,

    ||partial_t^j mu||_infty
      <=|partial_t^j mu(a)|+sqrt(ell) K ||f_metric,eff||_X*.

It does NOT turn lapse L2 into lapse pointwise control by an inverse h
inequality. That upgrade, and bounds on the source itself, remain to derive.

## 10. Matched results and what they mean

At the old final relative time 0.01:

| Grid | Branch | measured inverse norm | state-specific bound | Neumann feedback bound |
|---|---|---:|---:|---:|
| N16 | GR | 0.1963222 | 1.0892395 | 0.0261526 |
| N16 | Gram | 0.1963223 | 1.0923129 | 0.0262752 |
| N32 | GR | 0.1963321 | 1.0890998 | 0.0260335 |
| N32 | Gram | 0.1963321 | 1.0920586 | 0.0261025 |
| N64 | GR | 0.1963371 | 1.0890761 | 0.0260138 |
| N64 | Gram | 0.1963371 | 1.0920342 | 0.0260827 |

The separate common-box bound is 175/118 for all of them and all other
allowed configurations in that box. The close GR/Gram numbers do not
constitute an empirical victory, and do not remove the larger MTS time-
dependent shift mismatch measured previously.

N64 source dual norms at first/second order are 0.067033/1.222221 for GR
and 0.067038/1.224471 for Gram. Actual combined metric derivative norms are
0.005510/0.100192 for GR and 0.005510/0.101119 for Gram. Corresponding
state-specific upper bounds are 0.073004/1.331092 and 0.073208/1.337164.
These remain finite on the sampled grids but are NOT yet proven uniform
source bounds for evolved families or a complete time interval.

585/585 implementation checks pass: exact geometry/Gram certificates,
16 manufactured vacuum/weak-field cases through N128, a high-field refusal
control, and 18 unchanged canonical saved states with both derivative orders.
Another 48/48 exact-box/membership checks pass. Source and output hashes
are inherited and verified. Old physical d, d_t and full shift residuals
are carried forward unchanged. No new evolution or public upload occurs.
The scripts use one BelowNormal single-core worker at a time and exit.
Protected-workbench verification is an mtime scan since
2026-09-09T17:35:00Z, not a full pre-turn hash baseline.

## 11. Next: differentiated source and lapse trace, not another inverse audit

The canonical energy-norm inverse is now derived with an explicit common
configuration box. Do not repeat its missing-inverse inventory or replace
it with another table of raw condition numbers.

Next derive the first differentiated effective source bound from the actual
scalar equations, Gram current and boundary lift, then the second source.
There is a useful source sublemma available from the same factorization:
if rho_chi=S^T(Tchi)^2/(2h), rho_q=S^T(Tq)^2/(2h), and
rho_t=S^T(Tchi Tq)/h, weighted Cauchy-Schwarz gives

    rho_t,j^2<=4rho_chi,j rho_q,j,
    sum_j rho_t,j^2/h<=8 W0^2 ||q_R||_L2^2.

The last step uses rho_chi,j<=2hW0^2 and the earlier unweighted Gram bound
sum rho_q<=||q_R||^2. This controls a Gram source without assuming q_R is
bounded pointwise. It is only one term, not a bound for the entire forcing.

For the lapse upgrade, use the actual mass row and its natural outer trace
to derive a discrete first-order/Volterra estimate, rather than applying
an h-dependent nodal L2-to-infinity inverse inequality. Keep physical shift
mismatch, Gram/projection difference and clock-trace discrepancy explicit.
Together these must control the paired compatibility remainder and prove
that the solution stays inside a valid coefficient box. Only then is there
a closed coupled canonical evolution estimate to extend to nonlinear P(X).
