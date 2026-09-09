# Curvature transfer, quadratic remainder, and the two boundary bottlenecks

Private continuation, 2026-09-09. This is a calculation on the existing two
dimensionless annular fixtures, not an observational test or a black-hole theorem.

## Result in plain language

The saved ordinary-reference correction has now been carried through the actual
geometric curvature, Weyl square, multiplier, and mass-restoration coefficient
K1. The earlier algebraic stress proxy is no longer the only calculation.
An explicit second-order remainder majorant is derived, not set to zero.

The important adverse result is numerical: all four finest-grid curvature
stencil-sensitivity gates fail. The discrepancy is concentrated at the annular
boundaries. Its leading curvature term is the second radial derivative of mass;
its leading K1 term is the kinetic/scalar derivative channel. Those are distinct
bottlenecks, now identified by an exact decomposition rather than speculation.

The nonlinear remainder of these particular saved corrections is much smaller
than their derivative-reconstruction ambiguity. That does not establish a
continuum error bound, local GR recovery, or a physical value of the coupling u.

## 1. Frozen owners and scope

All paths below are relative to this post-checkpoint-work directory.

- `source-intake/navier-stokes/20260909/annular-boundary-preserving-refined/status.json`:
  selected evolution remains FAILED 136/137. Its canonical first-u T=0.3 scalar
  boundary gate remains 1.17977% against 1%; no row or failed marker was removed.
- `source-intake/navier-stokes/20260909/annular-correction-time-jets-initial/status.json`:
  FAILED 101/114, preserved. Twelve constant/kinematic interpolation checks and
  one coarse finite-time derivative control failed.
- `source-intake/navier-stokes/20260909/annular-correction-time-jets-stable-interpolation/status.json`:
  complete 114/114, 04:23:14 UTC. This certifies the recorded software checks,
  not the underlying continuous solution.
- `source-intake/navier-stokes/20260909/annular-curvature-timejet-transfer-initial/status.json`:
  preserved failed launch: a Windows path-key mismatch, before physics evaluation.
- `source-intake/navier-stokes/20260909/annular-curvature-timejet-transfer-portable-paths/status.json`:
  complete 428/428 algebra/software checks, 04:30:36 UTC;
  `all_curvature_sensitivity_gates_passed=false` and `valid_for_physics_claim=false`.
- `source-intake/navier-stokes/20260909/annular-curvature-boundary-channel-diagnosis/status.json`:
  complete 22/22, 04:33:23 UTC, including Schwarzschild/de Sitter vacuum controls.

Each owner retains an executed-script snapshot and hashes its local inputs.
The initial time-jet module is preserved as
`source-intake/navier-stokes/20260909/annular-correction-time-jets-initial/time-jet-module-snapshot.py`.
Its hash matches the old ledger even though the live module now contains the
stable interpolation implementation. Do not compare that historical input to
the amended live file and call the historical run reproduced.

The fixtures use kappa=0.1, epsilon=0.1, sigma=0.05, R in [4,8], times 0.1/0.3,
and 128/256/512 intervals. These are normalized test inputs, not sourced physical
couplings or measured masses. This annulus is not a black-hole interior test.
The physical first-u response is not conflated with the ordinary correction's
directional variation: the new transfer uses the ordinary channel only.

## 2. Time derivatives without another evolution run

For the saved semidiscrete remainder w, write w_t=F(t,w), including all SAT,
dissipation, compatible-flux replacement and boundary-preserving Noether sources.
Taylor arithmetic through degree two differentiates that actual ODE and its
anchored mass/adjoint solves. Recursively,

    w_1 = F_0,  w_2 = F_1/2,  w_3 = F_2/3,

where subscripts on w denote Taylor coefficients. Stored output contains actual
derivatives, including the factorial conversion. Initial lift is added only to
the order-zero correction. The original numerical sources are retained.

The same six-node cache polynomial is evaluated in the stable form

    I[f] = f_0 + sum_j L_j (f_j - f_0).

Its derivatives annihilate constant coefficient samples without cancellation of
large derivative weights. This is algebraically the same interpolating polynomial,
not a changed field equation. Replay of saved RHS and source values still passes.
The first run remains failed. The subsequent finite-time controls use steps
0.00025 and 0.000125 rather than 0.0005 and 0.00025, with the same tolerances.
Kinematic identities, source-completion identities through time degree two,
and left/right cache controls all pass in the new run.

Mixed spatial derivatives are reconstructed three ways: repeated SBP D1, local
seven-point polynomials, and local nine-point polynomials. Differentiate the
remainder and add the analytic initial-lift derivatives, including third-order
Chebyshev panel derivatives. Initial degree-32/64 sensitivity is recorded with
the same saved field samples; it is a representation sensitivity, not a new
degree-32 evolution. All endpoint rows are retained.

Physical derivatives are transformed exactly:

    partial_v^a partial_r^b e
      = sum_(j=0)^b binomial(b,j) (-sigma)^j
        partial_t^(a+j) partial_R^(b-j) e.

A separate 30-coefficient jet algebra carries spatial/time order three and
directional order two. It does not mutate the frozen physical first-u algebra.
All 30 elementary-function coefficients are checked independently with SymPy;
first variations are also checked by complex-step evaluation.

## 3. Actual curvature and residual transfer

Use Z for signed spherical curvature amplitude, Weyl^2=Z^2/3, and

    Zalg = 12 mu/r^3 + 4 kappa [X/2 - 3 b2 X^2 - 5 b3 X^3 - V].

The previously derived exact off-shell identity is evaluated with its residuals:

    Z - Zalg = -8 Rm/r^2 + 2 partial_r Rm/r
               -2 exp(-delta) partial_v Dl - 2 F partial_r Dl
               +(2F/r - 3 F_r - 2F delta_r) Dl - 2 kappa r chi_r Fchi.

Rm, Dl and Fchi are actual parent mass, lapse and scalar residuals. In particular,
saved J is not substituted for Rm, and scalar density is not substituted for Fchi.
The identity holds for the reconstructed background, first variation and quadratic
directional coefficient. The sum of absolute signed terms supplies a pointwise
triangle envelope. It is not a supremum over the unsampled spacetime domain.

Let M1=-2r^2 X Z/3 and B0=2F/r-F_r-2F delta_r. Then

    K1 = kappa [2F partial_r M1 + 2exp(-delta) partial_v M1 + B0 M1].

K1=K1alg+K1residual is checked at the same three directional orders. Numerical
source terms and background errors have not been silently cancelled to obtain
this result. K1 is the mass-restoration coefficient, not the general memory tensor.

Finest seven-point reconstruction, maximum absolute values over ALL rows:

| Fixture | T | delta Z | delta Zalg | delta K1 | delta K1 residual part |
|---|---:|---:|---:|---:|---:|
| canonical | .1 | 3.41935e-11 | 3.21468e-12 | 1.06334e-10 | 1.77458e-13 |
| canonical | .3 | 1.77890e-10 | 5.14329e-12 | 1.52214e-10 | 3.49719e-13 |
| nonlinear_modulated | .1 | 2.09790e-10 | 3.42268e-11 | 4.91704e-10 | 6.90739e-13 |
| nonlinear_modulated | .3 | 1.02794e-9 | 1.63456e-11 | 4.18605e-10 | 2.05819e-12 |

These are sampled, reconstruction-dependent numbers. The stress proxy alone
would substantially understate the maximum curvature variation in this table.

## 4. Derived nonlinear remainder majorant

Let b be a supplied background jet and e a supplied correction jet. For any of
the local functions f used here, Taylor's theorem along the correction segment is

    f(b+e) = f(b) + Df_b[e] + R_f,
    R_f = 2 integral_0^1 (1-theta) [zeta^2] f(b+theta e+zeta e) dtheta.

For 0<=theta<=1, build coefficientwise nonnegative input majorants: directional
degree zero has |b_alpha|+|e_alpha|, degree one has |e_alpha|, and degree two is
zero for the fundamental fields. Products use positive convolution; derivatives
use their nonnegative integer factors; sums/subtractions use the triangle
inequality. Reciprocal radius uses the absolute coefficients of its exact jet,
which is nonsingular on this annulus. For exp(+/-delta), bound the constant
factor by exp(+/-b_delta,0+|e_delta,0|) and use the exponential series of the
nonconstant coefficient majorant. Total nilpotent degree five suffices for
directional degree two and spacetime degree three.

Induction over these operations proves that the resulting coefficient
M_f=[zeta^2] majorant(f) bounds the second coefficient uniformly in theta.
Since 2 integral_0^1(1-theta)dtheta=1, |R_f|<=M_f in exact arithmetic.
The current values are floating-point evaluations of this analytical majorant,
NOT outward-rounded interval certificates. They are conditional on the supplied
derivative jets; uncertainty in those jets is a separate error contribution.

| Fixture | T | M_Z | M_K1 | integrated K1 remainder |
|---|---:|---:|---:|---:|
| canonical | .1 | 6.90163e-23 | 9.56734e-17 | 1.18145e-17 |
| canonical | .3 | 1.01835e-22 | 4.68513e-16 | 7.00642e-17 |
| nonlinear_modulated | .1 | 2.03087e-21 | 1.51781e-15 | 1.38161e-16 |
| nonlinear_modulated | .3 | 5.47413e-21 | 8.70375e-15 | 1.19688e-15 |

Four/eight-point quadrature of the directional Hessian agrees and lies below
the analytical majorant within the stated floating tolerances. This avoids
subtracting nearly equal full curvature values to estimate a tiny remainder.
The integral includes all orders beyond linear along this segment, not only
the second-order coefficient at theta=0. It is not a Newton convergence theorem.

## 5. Exact diagnosis of the boundary ambiguity

The finest seven/nine-point relative discrepancies are:

| Fixture | T | delta Z discrepancy | delta K1 discrepancy |
|---|---:|---:|---:|
| canonical | .1 | 78.01% | 7.846% |
| canonical | .3 | 72.81% | 69.80% |
| nonlinear_modulated | .1 | 69.06% | 6.493% |
| nonlinear_modulated | .3 | 70.53% | 6.648% |

The declared 10% curvature gate therefore fails in all four cases; K1 fails
one of four. Removing endpoint rows would hide the issue and is not an acceptance
route. Interior-only differences are recorded solely to locate the problem.
Mesh-difference ratios are not uniformly convincing either: for example the
nonlinear T=.1 K1 SBP and nine-point ratios are approximately 0.148 and 0.144.

For any ordinary perturbation (m,d) of (mu,delta), direct differentiation gives

    delta Z = (2/r) m_rr + (6 delta_r/r - 8/r^2) m_r
              +[12/r^3 - 10 delta_r/r^2 + 4(delta_rr+delta_r^2)/r] m
              -2F d_rr -2exp(-delta) d_vr
              +(-3F_r-4F delta_r+2F/r) d_r +2exp(-delta) delta_vr d.

This seven-term identity is checked against the independent directional evaluation.
Apply it to the difference between the two reconstructions. The largest term
is (2/r)m_rr in every case, at r=4. Its maximum is respectively 1.32335e-10,
4.42070e-10, 5.35799e-10 and 2.35472e-9. Lapse second derivatives are next.
This identifies where the curvature discrepancy enters; it does not yet prove
whether the underlying grid field, reconstruction, or both need changing.

K1 has a different leading sensitivity. With the fixed background operator
L_M[M]=kappa(2F M_r+2exp(-delta)M_v+B0 M), split exactly:

    delta K1 = L_M[-2r^2 X delta Z/3]
               + L_M[-2r^2 Z delta X/3]
               + kappa[2 delta F (M1)_r
                        -2exp(-delta) d (M1)_v + delta B0 M1].

The kinetic channel, the middle term, dominates the reconstruction discrepancy
in all four cases. In the problematic canonical T=.3 case its outer-boundary
contribution is 3.51995e-10, versus a total difference of 3.51803e-10.
Repairing only mass second derivatives would therefore miss the K1 bottleneck.

Matched vacuum controls in the same calculator recover Z=12mu/r^3,
Weyl^2=48mu^2/r^6 and zero scalar/mass/lapse residuals and K1, both with and
without Lambda. That checks a known GR limit of the calculator; it does not
validate MTS empirically or establish the full GR limit of its parent action.

## 6. Best next derivation, and what remains open

The immediate target is a derivative-compatible, source-retaining boundary
reconstruction for BOTH mass curvature and scalar kinetic gradients, built from
the same SBP/Noether system rather than independent high-order extrapolation.
Test it first against manufactured smooth mass/scalar fields with known Z and
K1 and identical boundary data. Any use of mu_r=R0+Rm must retain partial_r Rm;
setting that remainder to zero would reintroduce the unwanted closure.

Then revisit the four failed sensitivity gates without dropping endpoints or
loosening the tolerance. Do not start a large N1024 evolution simply to obtain
a green table. The full coupled energy/error estimate, continuum derivative
control, physical source coupling and black-hole/GR/Newton claims remain open.

Implementation:
- `scripts/annular_correction_time_jets_20260909.py`
- `scripts/derive_annular_correction_time_jets_20260909.py`
- `scripts/annular_curvature_timejet_transfer_20260909.py`
- `scripts/derive_annular_curvature_timejet_transfer_20260909.py`
- `scripts/diagnose_annular_curvature_boundary_channels_20260909.py`

All jobs in this continuation have finished. No subagents, GitHub action,
frozen-workbench/galaxy edits, or stopped shared processes. One modest local
compute job ran at a time, single-core BelowNormal. Safe save point.
