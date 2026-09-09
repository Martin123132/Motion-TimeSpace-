# First metric source and pointwise lapse response: derived from the actual rows

Date: 2026-09-09. Private canonical annular continuation. No public upload.

## 1. What is new

The previous step supplied a mesh-uniform metric Schur inverse in mass-H1
and lapse-L2 norms. This step derives TWO missing estimates:

1. The first differentiated effective metric source is bounded by the
   scalar graph energy, a spatial coefficient Lipschitz bound, the actual
   inner mass-rate trace and the prescribed scalar/clock boundary data.
   Interior metric time derivatives are NOT inputs to this estimate.
2. The actual mass row, including its natural outer boundary equation,
   upgrades that response to a pointwise lapse-rate bound, hence also an
   outer lapse-rate trace bound, without an inverse power of mesh spacing.

These statements hold on the canonical configuration box already derived,
for both the GR control and the owned MTS Gram action, on every supported
grid with n>=17 scalar nodes. They are conditional analytic estimates,
not extrapolations of finite-grid norms.

What is NOT proved: that the scalar energy, coefficient Lipschitz constant
and physical inner flux trace remain uniformly controlled over time; that
the solution remains in the box; the second effective source bound; lapse
rate spatial-gradient control; full shift/DAE compatibility; nonlinear P(X);
or black-hole regularity. No parent physical calibration is supplied here.

## 2. Source owners and reproducibility

Previous theorem:
`DERIVATION-20260909-metric-Schur-inverse-and-projection-remainder.md`.
Previous scalar operator and affine-boundary estimates:
`DERIVATION-20260909-mesh-uniform-coefficient-and-boundary-source-bounds.md`.
Physical jets and shift mismatch:
`DERIVATION-20260909-metric-flux-cancellation-and-exact-constraint-jets.md`.
Actual equations:
`scripts/annular_released_hermite_action_20260909.py`,
`scripts/annular_constraint_routhian_20260909.py`,
`scripts/annular_first_derivative_energy_20260909.py`, and
`scripts/annular_gram_joint_action_20260909.py`.
New analytic helper:
`scripts/annular_metric_source_bound_20260909.py`.
Runner, with derive and seal phases:
`scripts/derive_annular_metric_source_bound_20260909.py`.
Result:
`source-intake/navier-stokes/20260909/annular-metric-first-source-and-lapse-trace-derived/status.json`.
Final integrity owner:
`source-intake/navier-stokes/20260909/annular-metric-first-source-and-lapse-trace-final-integrity.json`.

The runner uses python -B, one BelowNormal single-core process and the old
18 saved states, not a new long evolution. Source hashes, physical mismatch
arrays and the complete boundary conditions are preserved. The eight
manufactured cases are algebraic controls, not extra physical solutions.

## 3. Scope, spaces and inputs

Use the same canonical action b2=b3=m_chi=Lambda=0 and positive kappa.
Let q=chi_t, w=chi_R, F=1-2mu/R, A_rad=RF,
m=R^2/(N sqrt(F)), p=R^2 N sqrt(F), ell=b-a, and h=ell/(n-1).
The actual quadrature is denoted Q. Its positivity and polynomial exactness
give the unweighted scalar L2/H1 norms used below exactly.

The common box is [a,b]=[47/8,49/8], kappa=1/10,
13/20<=F<=17/25, 4/5<=N<=21/25,
|q|<=1/50, |w|<=3/100 and |mu_R|<=1/500.
Denote these lower/upper bounds by F0,N0,N1,Q0,W0,U0 and set A0=a F0.
Use m_+=60025/1024, p_+=16807/640 as rational majorants.
The prior inverse bound is K_S=175/118.

Mass test functions xi vanish only at a. Lapse tests have no fixed value.
The norm is ||(xi,n)||_X^2=||xi_R||_2^2+h sum n_j^2.
Every scalar slope velocity remains free. Scalar value velocities are
fixed only at their two prescribed endpoints.

Additional inputs are the scalar graph energy E, L_p=||p_R||_infinity
(piecewise derivative of the continuous coefficient), the actual inner
mass rate u_a=mu_t(a), endpoint values/rates/accelerations, and the outer
clock coefficient derivative c_b'. They are NOT fitted constants.
In particular u_a remains the inner component of the actual shift solve,
not a newly selectable boundary value. Its uniform trace law is still needed.
L_p is a SPATIAL coefficient bound, not a metric time derivative.

## 4. Graph energy controls the uneliminated scalar forcing

Let M and K be the actual canonical scalar mass/stiffness matrices, including
the Gram stiffness in K when applicable. Restrict them to free scalar
velocity coordinates to obtain M_f,K_f. Let L denote the actual affine
Hermite value lift, including its slope representation. Define

    v=(chi-L chi_boundary)_free,
    z=(q-L q_boundary)_free,
    E=one_half[z^T K_f z + (M_f^-1 K_f v)^T M_f (M_f^-1 K_f v)].

Write ||.||_m for the M_f norm. Since K is positive and its bulk part
dominates p_-||. _R||_2^2,

    Q1 := sqrt(2E/p_-)+||(L q_boundary)_R||_2 >= ||q_R||_2.

The fixed-configuration velocity data derivative is exactly (K chi)_free.
Its mass Riesz representative r=M_f^-1(K chi)_free obeys

    ||r||_m <= R1 := sqrt(2E)+33 L_p ||(L chi_boundary)_R||_2/sqrt(m_-).

For completeness the factor 33 is not a fitted norm: on each scalar cell,
subtract a constant from p in the quadrature error for p times a free test
derivative. Lipschitz continuity gives two errors bounded by h L_p times
that derivative norm. The exact local cubic inverse constant is 16, while
integration by parts gives L_p times the test L2 norm. Thus 1+2*16=33.
The tests vanish at their two value endpoints, so no omitted boundary term
is used in this argument. The Gram stiffness annihilates the affine lift
because its third differences vanish. There is no added slope condition.

These are energy-to-source inequalities. Measuring E at a few times does
not prove a time-uniform bound on E or L_p.

## 5. Gram time source without a pointwise q_R assumption

For the owned factorization, with nonnegative sampling matrix S and factor
matrix T, put

    rho_chi=S^T(Tchi)^2/(2h),
    rho_q=S^T(Tq)^2/(2h),
    rho_t=S^T[(Tchi)(Tq)]/h.

Weighted Cauchy-Schwarz gives rho_t,j^2<=4rho_chi,j rho_q,j.
The preceding exact templates give rho_chi,j<=2hW0^2 and
sum rho_q<=||q_R||_2^2. Consequently

    ||rho_t||_(h^-1 l2) <= sqrt(8) W0 ||q_R||_2 <= sqrt(8) W0 Q1.

The proof only needs q_R in L2, not a pointwise q_R bound. Oscillatory-q
controls below check that increasing energy is NOT confused with uniform
control merely because the amplitudes q_j remain bounded.

## 6. Exact first source and its dual-norm majorant

Write the free Hessian blocks as H_gg,C,M_f, where C=H_gv and
S_metric=H_gg-C M_f^-1 C^T. At fixed packed variables, the metric data
derivative is the following actual functional:

    T_mu(xi)=Q[(p/A_rad)w q_R xi]
             +sum rho_t,j p_j xi_j/A_rad,j [Gram]
             -c_b' xi(b)/kappa,
    T_N(n)=-Q[(p/N)w q_R n]-sum rho_t,j p_j n_j/N_j [Gram].

Lift the physical mass rate as a constant field u_a and the prescribed
endpoint scalar accelerations as eta=L q_boundary,t. Denote the combined
packed lift by l. The EXACT effective source is

    f=-T_g+C r-J_g l+C M_f^-1 J_v l.

This is independently reconstructed and compared with the old source;
no physical row is replaced. The scalar lift contribution after elimination
is the weighted projection remainder of eta, hence its mass norm is at
most sqrt(m_+)||eta||_2. Define Y=R1+sqrt(m_+)||eta||_2.

Let I_G be one for Gram and zero for GR, ell_n=17ell/16,
C_P=sqrt(17/16)ell. Introduce nonnegative constants

    g0=N1/(kappa a F0^(3/2)),
    a_rho=3N1 U0/(kappa a^2 F0^(5/2))
           +(3m_+Q0^2+p_+W0^2)/(2A0^2),
    a_G=I_G 2p_+W0^2/A0^2,
    b_rho=U0/(kappa a F0^(3/2))
           +(m_+Q0^2+p_+W0^2)/(2A0 N0),
    b_G=I_G 2p_+W0^2/(A0 N0),
    c_mu=sqrt(m_+)Q0 ell/A0, c_N=sqrt(m_+)Q0/N0,
    l_mu=a_rho ell sqrt(ell)+g0 sqrt(ell)+a_G C_P sqrt(ell_n),
    l_N=b_rho sqrt(ell)+b_G sqrt(ell_n).

Poincare, the nodal mass bound and the projection identities of the prior
step yield the explicit component bounds

    F_mu=(p_+W0/A0)(ell+I_G sqrt(8)C_P)Q1
          +sqrt(ell)|c_b'|/kappa+c_mu Y+l_mu|u_a|,
    F_N=(p_+W0/N0)(1+I_G sqrt(8))Q1+c_N Y+l_N|u_a|,
    ||f||_X* <= F1 := sqrt(F_mu^2+F_N^2).

The mass-lift coefficients include the gravitational cross derivative,
the kinetic projection remainder, the scalar gradient and Gram terms.
They do not regard the nonzero inner mass rate as a zero-inner perturbation.
There is no h^-1 in these constants.

The existing inverse theorem now gives

    R1_metric := K_S F1,
    ||mu_t,R||_2 <= R1_metric,
    ||N_t||_(h l2) <= R1_metric,
    ||mu_t||_infinity <= M1 := |u_a|+sqrt(ell)R1_metric.

## 7. The actual mass row also controls pointwise N_t

This upgrade does NOT apply a nodal L2-to-infinity inverse inequality.
Use mass-cell derivative coordinates z_i=xi_R. Each free mass nodal value
is the sum of preceding cell widths times z_i. Thus for a mass covector f,
the normalized row i is (Delta R_i/h) times its downstream cumulative sum.
Its kernel is bounded by omega_max=59/48.

The reference principal lapse block becomes (sigma0/kappa)H in these rows,
where H is the exact tridiagonal overlap matrix of the preceding proof.
Its strict row-dominance gap is g_row=527/2304. The variable principal
coefficient error has infinity row norm <=delta_sigma omega_max/kappa.
With sigma0=123/100, delta_sigma=1/50, the actual principal inverse margin is

    beta_infinity=(sigma0 g_row-delta_sigma omega_max)/kappa >5/2.

This inequality is certified with rational arithmetic. All lower-order
lapse terms are bounded using the ALREADY DERIVED lapse L2 response; they
do not require assuming a bound on N_t pointwise. The physical mass rate,
including its inner trace, is treated as a full field.

Writing R=R1_metric and M=M1 only in the next three formulas, normalized
row bounds for the direct forcing, mass response and lower lapse terms are

    D_row=omega_max[(p_+W0/A0)(sqrt(ell)+I_G sqrt(8ell_n))Q1
             +|c_b'|/kappa+(sqrt(m_+)Q0 sqrt(ell)/A0)Y],
    A_row=omega_max[a_rho ell M+g0(M+sqrt(ell)R)+a_G ell_n M],
    B_row=omega_max[b_rho sqrt(ell)+b_G sqrt(ell_n)]R.

The actual mass equation and the preceding positive principal margin give

    ||N_t||_infinity <= N1_rate := (D_row+A_row+B_row)/beta_infinity.

In particular |N_t(b)|<=N1_rate. The outer clock forcing is already present
in D_row; we did not silently set the outer lapse rate or its clock defect
to zero. Both signs of the logarithmic metric rates are controlled:

    |partial_t log(N sqrt(F))|,
    |partial_t log(N/sqrt(F))| <= N1_rate/N0+M1/A0.

This last inequality is pointwise. It does not bound the RADIAL derivative
of either logarithmic rate, which the higher energy transport still needs.

## 8. Validation and measured size

610/610 implementation checks pass across 18 unchanged canonical states
and eight manufactured controls. Checks include independent first-source
reconstruction, Gram Cauchy/energy bounds, all three normalized mass-row
estimates, unchanged Schur matrices, unchanged physical shift mismatches,
zero-source vacuum controls, and the exact positive principal margin.
These are algebra/code checks, NOT 610 independent physics experiments.

At the saved final relative time 0.01:

| Grid | Branch | actual source dual norm | derived source bound | actual max abs(N_t) | derived pointwise bound |
|---|---|---:|---:|---:|---:|
| N16 | GR | 0.064993 | 0.345523 | 0.00016962 | 0.690373 |
| N16 | Gram | 0.064957 | 0.804931 | 0.00016698 | 1.611404 |
| N32 | GR | 0.066489 | 0.345795 | 0.00016923 | 0.690918 |
| N32 | Gram | 0.066473 | 0.804799 | 0.00016919 | 1.611151 |
| N64 | GR | 0.067033 | 0.345919 | 0.00016930 | 0.691165 |
| N64 | Gram | 0.067038 | 0.805020 | 0.00016939 | 1.611595 |

The source bounds are useful finite majorants. The pointwise lapse bounds
are VERY conservative: they discard substantial cancellations and are not
a tight prediction or evidence of growth in the actual solutions. The
larger Gram bound reflects absolute-value estimates, not an empirical
comparison favoring either theory. At N64 the common energy is about 0.139.
The affine scalar-force norm is about 0.00459; its analytic Lipschitz bound
is deliberately looser. No favorable physical mismatch was substituted.

The oscillatory-velocity controls have growing graph energy as the grid
is refined, although q remains bounded in amplitude. The runner explicitly
recognizes this growth rather than promoting those data to a time-uniform
family. The analytic estimates allow the source to grow with this energy.

## 9. What to do next, and what not to repeat

The first effective source and the pointwise lapse/outer response are now
derived conditionally. Do not repeat a missing-first-source or missing-
pointwise-inverse audit. Do not infer full evolution from sampled box membership.

Next derive the spatial clock-rate/paired-flux estimate using the actual
mass row and retained defects, now with the first response available. It
must control the spatial coefficient/transport inputs and the actual inner
shift trace, not prescribe them favorably. Then bound the second effective
source using the owned exact second jets and differentiated Gram terms.
These should feed a coupled energy and configuration-persistence inequality.

Conditional integration already gives ||mu(t)-mu(0)||_infinity<=integral M1
and ||N(t)-N(0)||_infinity<=integral N1_rate if the hypotheses hold throughout
the interval. That is not a persistence proof: it does not yet propagate
the energy, q,w,mu_R bounds or compatibility required by those hypotheses.
The black-hole/horizon problem remains outside this F>=13/20 local box.

All computations are private and complete. The protected-workbench check
is an mtime scan since 2026-09-09T20:56:00Z, not a full pre-turn hash baseline.
