# Bounded source integration and derived second-corner initial data

Private continuation, 2026-09-09. Previous turn verified as progress from the
saved five-field principal derivation and matched coupled runs. This turn tests
the proposed source repair, finds that it is not sufficient, and constructs a
different repair from a newly identified initial-boundary compatibility gap.
The ordinary parent action and its physical coefficients are unchanged.

## 1. A tested alternative to the scalar source projection

For coordinate sources with S_chi=S_w=0, the parent Noether completion is

    (partial_R-a) u = f, u(R_out)=0,
    u=S_mu, a=G_mu, f=G_q*S_q+G_delta*S_delta.

The previous nodal solve also forced its unused boundary derivative row to hold
exactly. That extra discrete compatibility condition was enforced by modifying
interior S_q through an adjoint projection. Here S_q and S_delta are kept
unchanged at EVERY node, and u is integrated backwards. This is a different
numerical source treatment, not a new physical coupling.

On each cell of width h, take a_c=(a_left+a_right)/2 and linearly interpolate
f. Define z=-h*a_c and

    phi(z)=integral_0^1 exp(z*t) dt=(exp(z)-1)/z,
    psi(z)=integral_0^1 t*exp(z*t) dt=((z-1)*exp(z)+1)/z^2.

Then the exact cell reconstruction satisfies

    u_left=exp(z)*u_right-h*(phi-psi)*f_left-h*psi*f_right.

At z=0 the limits are phi=1,psi=1/2, giving trapezoidal integration of a
linear forcing. The implementation uses Taylor sums near zero to avoid
cancellation. For |z|<.1 the degree-12 series tails are bounded by
exp(|z|)*|z|^13/(13!*14) for phi and /(13!*15) for psi. Floating roundoff is
not certified by those analytic truncation bounds.

## 2. An explicit all-row residual bound, not a zero assertion

Let L be the interval length, A=max|a_i|, F=max|f_i|,
L_a=max|a_(i+1)-a_i|/h and L_f=max|f_(i+1)-f_i|/h. For the exact
piecewise-constant-a, piecewise-linear-f reconstruction,

    U=exp(A*L)*(|u_out|+L*F), V=A*U+F

bound |u| and its almost-everywhere derivative. A jump in a_c is permitted;
u remains absolutely continuous. Write the SBP derivative as
D_i u=sum_j d_ij*u_j/h and define its finite, grid-independent stencil moments

    C1_i=sum_j |d_ij|*|j-i|/2,
    C2_i=sum_j |d_ij|*|j-i|^2/2.

The operator annihilates constants and differentiates linear functions exactly.
With g_i=a_i*u_i+f_i and g(x)=a_c(x)*u(x)+f_h(x),

    D_i u-g_i=sum_j (d_ij/h)*integral_(r_i)^(r_j) [g(x)-g_i] dx.

The piecewise-linear coefficient interpolant takes the value a_c at a cell's
midpoint, so

    |g(x)-g_i| <= (A*V+L_a*U+L_f)*|x-r_i|+L_a*U*h/2.

Integrating this inequality gives the ALL-ROW bound

    |D_i u-a_i*u_i-f_i|
      <= h*[(A*V+L_a*U+L_f)*C2_i+L_a*U*C1_i].

No boundary row is dropped. The RHS is computed from inputs and stencil
moments, not fitted to the measured residual. It bounds the stated
reconstruction's nodal residual, not an unknown continuum solution error.
Original smooth-coefficient approximation error, other parent defects and
floating evaluation error remain separate. The bound is not outward-rounded
interval arithmetic.

If the input Lipschitz constants stay bounded, this conservative estimate is
O(h). Boundary penalties may depend on h; no uniform Lipschitz bound is assumed
for them. Nevertheless L_f<=2F/h, so bounded A,L_a and F tending to zero imply
this source residual tends to zero. Whether those hypotheses hold for an
evolution must be demonstrated, not asserted. In the constraint propagation
equation the nonzero residual is a retained forcing, never a hidden closure.

The formula and implementation pass constant/varying-coefficient, zero-
coefficient and boundary-spike controls. Four saved source replays eliminate
the interior q correction exactly while retaining a nonzero, bounded mass-source
residual. The existing scalar, lapse, total mass-constraint and refinement
acceptance thresholds remain unchanged in the subsequent evolution test.
Only the source contract changes explicitly from exact nodal cancellation to
the derived residual bound; those two claims must not be conflated.

## 3. The source hypothesis does not fix the failed evolution gate

The bounded-source run is FAILED 141/145. It preserves every q/lapse source
and passes the derived all-row source bound, but the canonical T=.1 q
refinement failure remains. Its coarse/fine q differences are 1.6983e-12 and
1.9192e-12, compared with 1.4850e-12 and 1.9121e-12 in the original projected
run. It additionally fails nonlinear T=.1 refinement and both nonlinear T=.3
total mass-constraint gates.

Thus the projection was NOT the sole cause of the canonical transient. The
Volterra source option is retained as an explicit bounded-source experiment,
not selected as the repaired production method. A valid bound is not a claim
that the bound or the resulting errors are small enough. Do not try to promote
this run merely because its bound checks pass.

## 4. Derive the missing initial-boundary compatibility conditions

The ordinary current perturbation obeys

    e_t=A(t,R)e+B(t,R)e_R-d(t,R),

where d is the actual background residual. Let L_b(t) be an incoming boundary
row, including the lapse term derived in the previous note. For homogeneous
incoming data, smooth evolution requires L_b(t)e(t,R_b)=0 and its successive
time derivatives to vanish at t=0.

For a fixed initial profile e0, define

    e1=A0*e0+B0*e0_R-d0,
    e2=A0*e1+B0*e1_R+(partial_t A)0*e0
       +(partial_t B)0*e0_R-(partial_t d)0.

The first three corner conditions are

    C0=L0*e0,
    C1=L0*e1+L_t0*e0,
    C2=L0*e2+2L_t0*e1+L_tt0*e0.

The outer lapse uses its own row selecting e_delta. These formulas are evaluated
with the continuum parent operator, not with SAT penalties forcing the answer.
Spatial coefficient derivatives are analytic complex-direction derivatives;
the remaining endpoint derivatives use seven-point one-sided formulas with
independent shrinking spatial/time steps. Their reported stability is numerical
evidence, not an interval proof of an exact zero.

The existing data satisfy C0 and C1, but not C2:

| Fixture | Inner scalar C2 | Outer scalar C2 | Outer lapse C2 |
| --- | ---: | ---: | ---: |
| Canonical | 6.2690e-9 | 2.7854e-6 | -2.6774e-11 |
| Nonlinear | -2.6140e-8 | -2.7458e-5 | 3.0238e-10 |

The estimates persist under step halving. A mismatch at this corner is a
regularity limitation of those initial/boundary data, not evidence that the
underlying physical theory is false. The old problem can still have a less
regular solution; its high-derivative certification is not supplied by these
new tests. It is especially inappropriate to assume arbitrarily smooth jets
from data satisfying only the first compatibility condition.

### Characteristic reason the next jet can be determined

For a noncharacteristic incoming row L_b, L_b*B=lambda_in*L_b. Freezing the
principal coefficients, the highest spatial derivative in the kth time
compatibility condition is lambda_in^k*L_b*partial_R^k e0; all differentiated
coefficients enter lower-order terms. This follows by induction from the
first-order parent system.

For q initially zero and w=chi_R, an independent scalar initial jet of order
k+1 enters through the current vector (dw,dh)=(1,-B_scalar). The incoming row
evaluates this vector to one. Thus its leading coefficient is lambda_in^k,
which is nonzero at the tested exterior boundaries. The outer lapse leading
coefficient is (1/sigma)^k. This gives a local, triangular jet construction;
it does NOT prove that every globally constrained compact-profile family is
invertible. At a characteristic/outflow horizon boundary, do not divide by a
zero incoming speed or impose an incoming condition that is absent.

## 5. Construct data from the equations, not from evolution scores

The new family retains q0=0, zero outer mass trace and the same linearized mass
constraint. It keeps the three existing compact profiles and adds scalar cubic
profiles at both ends and a quadratic outer-lapse profile. For inward distance
x in [0,1], the additional profiles are

    scalar: x^3*(1-x)^4/6,
    outer lapse: x^2*(1-x)^4/2.

They vanish with the necessary lower endpoint jets; their cutoff joins the zero
extension through third spatial derivative. The finite family is a declared
initial-data choice, not a parent-action term or empirical fitting freedom.

For each profile, the induced initial mass is solved from

    m_R-G_mu*m=-J_bar+G_chi*chi0+G_w*chi0_R+G_delta*delta0,
    m(R_out)=0.

The particular and six homogeneous profile responses are represented on four
degree-64 Chebyshev panels. Six amplitudes solve the six affine C1/C2 conditions
at the two scalar boundaries and outer lapse boundary. No evolution output is
used in selecting these amplitudes. The row-scaled matrix condition numbers
are 61.33 and 61.83 for the canonical and nonlinear fixtures.

Independent finer-step C2 values after construction are

| Fixture | Inner scalar C2 | Outer scalar C2 | Outer lapse C2 |
| --- | ---: | ---: | ---: |
| Canonical | -6.55e-16 | -2.18e-12 | 2.43e-19 |
| Nonlinear | -6.64e-16 | -6.22e-13 | -3.20e-18 |

These are approximately controlled zeros, not exact certified ones. The dense
401-point initial mass-constraint holdout errors are 3.14e-19 and 4.83e-19.
The coefficients and all profiles are saved. Initial scalar maxima are
1.99e-10 and 1.01e-9; no large new background is inserted to make the test easy.

This changes the TEST'S initial data, not the action, observation set or physical
coefficients. The old failed data/run are preserved. Success with the new data
would not retroactively prove convergence for the old lower-regularity problem.
The new data are tested with the original exact-source projection and no Gram
filter, so the source change is not mixed into this separate experiment.

## 6. Evolution results and next scope

The second-corner evolution completed at 06:37:19 UTC, FAILED 128/129.
N128/256/512, both T=.1,.3 outputs, finest time halving, original projected
source completion and zero Gram filtering were retained. Every finest scalar
boundary, lapse, mass-constraint, exact-source-with-floating-tolerance,
integrability and time-refinement gate passes. Three of the four spatial
comparison groups pass; one nonlinear T=.1 group fails in TWO components.

| Fixture and time | Spatial comparison | Time comparison |
| --- | --- | --- |
| Canonical .1 | Pass, including q | Pass |
| Canonical .3 | Pass | Pass |
| Nonlinear .1 | FAIL: chi and mu; q and delta pass | Pass |
| Nonlinear .3 | Pass | Pass |

For the newly constructed canonical data at T=.1, q mesh differences are
2.18673e-12 and 1.61542e-12, satisfying the unchanged 1.3 reduction criterion.
This was the failed component for the OLD initial data, but the underlying
initial-value problems differ: the old run is not retroactively promoted.

The remaining nonlinear T=.1 comparison, in normalized fixture units, is:

| Component | N128/256 difference | N256/512 difference | Allowed fine difference | Peak radius | Fine difference / finest component maximum |
| --- | ---: | ---: | ---: | ---: | ---: |
| chi | 9.80134e-14 | 1.03592e-13 | 7.54949e-14 | 4.015625 | 0.014724% |
| mu | 1.42299e-14 | 1.33318e-14 | 1.10461e-14 | 5.078125 | 0.010997% |

Allowed difference is coarse_difference/1.3+1e-16, not a newly chosen
threshold. The chi and mu time-halving differences are respectively
1.06560e-20 and 1.18786e-21. Thus the observed discrepancy is not resolved by
reducing this time step. These small relative mesh differences are NOT bounds
on continuum error, nor a license to ignore the failed convergence criterion.
The different peak locations also rule out assuming a single endpoint effect
without further diagnosis. The named NPZ outputs and comparison rows reproduce
the values; the spatial maxima use N512 dt1 restricted to the N256 grid.

Independent validation completed 198/198 at 06:39:35 UTC. It checks exact
incoming eigenrow/leading-jet identities, SBP consistency and bound moments,
saved hashes/metrics, unchanged acceptance gates, preserved failed owners and
script compilation without bytecode. An independent nine-point corner
evaluation gives C2 (inner scalar, outer scalar, outer lapse):

    canonical: (-5.84409e-16, -1.92535e-12, -5.84083e-18),
    nonlinear: (-1.44068e-15,  1.45035e-12, -8.71688e-18).

Those agree with the separately stepped seven-point calculation at its declared
numerical tolerance; they are not an exact or interval-certified zero proof.
The 198/198 result validates the evidence/software, NOT the failed evolution
or the full physics. All owners retain valid_for_physics_claim=false.

**Next target:** derive the leading near-boundary truncation/compatibility
forcing for these actual second-corner data and trace its coupled transport
into chi and mu. Compare the canonical and nonlinear fixtures with their
respective fixed data, including the compact-profile join at R=5. Determine
whether C3 compatibility, finite cutoff regularity or the discrete source
operator causes the remaining component errors BEFORE changing them. Do not
assume that satisfying C2 supplies the higher jets needed for curvature, and
do not launch a blind grid/filter sweep. Only transfer a resolved ordinary
solution to the actual curvature/first-u calculation with explicit jet-error
control. Its four old curvature failures and old 136/137 first-u failure
remain open. Full coupled boundary/source energy and finite-u validity remain
separate obligations; physical coefficients are still uncalibrated.

This is a safe save point: all derivation, evolution and validation jobs from
this continuation have exited. The bounded-source alternative was tested and
found insufficient; the second-corner construction is a derived improvement
to the regularity of a declared test, not a completed black-hole or GR limit.

## 7. Source map

Paths are relative to this post-checkpoint-work directory.

- `scripts/annular_volterra_source_completion_20260909.py`
- `scripts/derive_annular_volterra_source_completion_20260909.py`
- `scripts/annular_current_corner_compatibility_20260909.py`
- `scripts/diagnose_annular_current_corners_20260909.py`
- `scripts/annular_second_corner_initial_data_20260909.py`
- `scripts/derive_annular_second_corner_initial_data_20260909.py`
- `scripts/run_annular_coupled_current_correction_20260909.py`
- `scripts/annular_coupled_current_operator_20260909.py`
- `scripts/annular_continuum_initial_data_20260909.py`
- `scripts/sbp4_derived_operator_20260909.py`
- `scripts/validate_annular_source_and_corner_20260909.py`
- `source-intake/navier-stokes/20260909/annular-volterra-source-completion-derived/status.json`
- `source-intake/navier-stokes/20260909/annular-coupled-current-correction-volterra-source/status.json`
- `source-intake/navier-stokes/20260909/annular-current-corner-compatibility-diagnosis/status.json`
- `source-intake/navier-stokes/20260909/annular-second-corner-initial-data/status.json`
- `source-intake/navier-stokes/20260909/annular-second-corner-initial-data/canonical-degree64.json`
- `source-intake/navier-stokes/20260909/annular-second-corner-initial-data/nonlinear_modulated-degree64.json`
- `source-intake/navier-stokes/20260909/annular-coupled-current-second-corner/status.json`
- `source-intake/navier-stokes/20260909/annular-coupled-current-second-corner/nonlinear_modulated_N256_dt1_T0.1.npz`
- `source-intake/navier-stokes/20260909/annular-coupled-current-second-corner/nonlinear_modulated_N512_dt1_T0.1.npz`
- `source-intake/navier-stokes/20260909/annular-source-bound-and-corner-validation/status.json`
- `DERIVATION-20260909-coupled-current-hyperbolicity-and-evolution.md`

The full MTS/local-GR/Newton/Maxwell/calibrated-coupling goal remains open.
This is an ordinary linearized regularity/evolution step; no central-singularity
cure, finite-u validity, empirical preference or physical coupling calibration
is claimed. Everything remains private, under post-checkpoint-work; no GitHub,
workbench/galaxy edits, subagents or stopped shared processes.
