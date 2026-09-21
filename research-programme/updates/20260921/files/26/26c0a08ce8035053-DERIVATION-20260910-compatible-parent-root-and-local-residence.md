# Compatible free-constraint roots and short reduced-flow residence

Private continuation, 10 September 2026. Finite annular canonical branch;
the same construction is applied to the GR control and metric-Gram branch.
Final attempt02 completed: **333/333 checks across 18 neighborhoods**.

## 1. What changes mathematically

The preceding coefficient-box calculation bounded derivatives on independently
specified coefficient/jet neighborhoods. It did not establish that an exact
solution starts there or stays there. This continuation encloses an exact
root of the original **free constraints**, then defines the reduced evolution
on that root manifold and proves a positive local residence time.

This is more than a residual-tolerance Newton solve. It is also narrower than
a solution theorem for the complete parent action: the remaining shift
equations are not asserted to follow from this reduction. Their numerical
defects are retained in section 6. In particular, neither local GR nor black
hole regularity follows from this finite positive-annulus result.

The root method avoids evolving only the third derivative of the constraints.
If one instead imposed F'''=0 on approximate initial jets, the result would
preserve F(0)+t F'(0)+t^2 F''(0)/2, not necessarily F=0. Here the numerical
residual is enclosed as a nonzero input to the root proof, not discarded.

Predecessor:
`DERIVATION-20260910-parent-coefficient-box-and-boundary-rate-enclosure.md`.
Implementation:
`scripts/annular_parent_root_residence_20260910.py` and
`scripts/derive_annular_parent_root_residence_20260910.py`.

## 2. Precisely which finite equations are solved

Let x=(chi,s) contain nodal scalar values and the released Hermite slope
coordinates, pi their two canonical momentum blocks, and
y=(mu,N,v_chi,v_s) the packed variables. Write v=(v_chi,v_s). At bulk
quadrature points use the original assembly maps V and D:

    v_q = V v,  g_q = D x,
    F_q = 1 - 2 mu_q/r_q.

All realized binary64 maps, radii, quadrature weights and Gram factors are
regarded as exact real constants of the finite model. The final evidence
archives those actual arrays; this does not certify their construction or
their approximation error relative to continuum quadrature. Kappa is the
exact rational 1/10, enclosed by interval division. Lambda, m_chi, b2 and b3
are zero. The implementation rejects other coefficient branches.

With eta=0 for GR and eta=1 for metric-Gram, the canonical finite Routhian is

    A = sum_q W_q [ N_q mu_r,q/(kappa sqrt(F_q))
                    + r_q^2 v_q^2/(2 N_q sqrt(F_q))
                    - r_q^2 N_q sqrt(F_q) g_q^2/2 ]
        - eta sum_j (S a)_j (B chi)_j^2/(2h)
        - pi^T v - C mu_out/kappa,
    a_i = R_i^2 N_i sqrt(1-2 mu_i/R_i).

Here B and S are the existing Gram factor/sampling matrices; h is the stored
spacing. V and D use scalar_value/lift_value and scalar_gradient/lift_gradient
from the original assembly, with the lift columns divided by h before being
fixed as numerical map coefficients. These are the same mathematical terms
as `scripts/annular_released_hermite_action_20260909.py`, not a new coupling.

The free set f excludes the inner mass and the two endpoint nodal velocities.
The equations enclosed in the root test are

    F_f(y_f;w,t) := partial A/partial y_f = 0,
    w = (x,pi,h_in),  h_in=mu_inner.

For each saved time, local time t is reset to zero. The clock and endpoint
velocities are reanchored to that saved state's binary64 values:

    C(t)=C_0+C_1 t,
    v_end(t)=v_end,0+a_end t.

The acceleration and clock rate come from the original boundary input. This
is an explicitly specified local quadratic scalar boundary history, not a
claim that independently rounded saved states exactly share one global
history. Endpoint nodal momenta are inert bookkeeping coordinates, with
pi_dot_end=0; their omitted momentum rows are not claimed as extra constraints.
Every scalar slope momentum equation is retained.

## 3. Existence and uniqueness of the parameterized roots

For a saved center y_0, choose positive free-coordinate radii
r_i approximately 1e-6 max(1,abs(y_0,i)), rounded outward. The derivative
enclosure [J] covers the entire free search rectangle and parameter tube.
Let R be the computed midpoint inverse, subsequently treated as an exact
preconditioning matrix. The proof does not assume its numerical inverse
calculation was exact. Form outward bounds

    Bmaj >= abs(I-R[J]),
    cbar >= abs(R[F_f(y_0;W,[0,Tpar])]),
    eta_J >= max_i sum_j Bmaj_ij.

The verified inequalities are

    eta_J < 1,
    cbar + Bmaj r < r   componentwise.

For every fixed parameter p=(w,t) in the tube, the map

    H_p(y_f)=y_f-R F_f(y_f;p)

is a contraction on the closed free rectangle and maps it strictly into
itself. Banach's theorem gives one root there for every p. Also
norm(I-R J)<1 implies J, and hence R, is nonsingular; a fixed point really
does imply F_f=0. No zero-residual assumption is used.

The interval mean-value identity

    J_mean (y_root-y_0) = -F_f(y_0;p)

then refines the root enclosure with the inherited verified comparison
solve. In particular its componentwise radius inequality, not the accuracy
of a floating solve alone, certifies the result. Intersecting with the
already certified search enclosure is valid. Positive F and N are checked
through the search neighborhood; metric-link positivity is checked in the
shift evaluation as well.

Repeat the root calculation with x, pi, h_in, C and endpoint velocities
fixed exactly to the saved numerical values. This gives a compatible initial
root differing only in the free packed variables. The saved state is never
overwritten. The correction upper is about 2.3e-13 at N16, 4.3e-13 at N32,
and at most 1.084e-12 over the N64 samples. These are enclosure radii in
unscaled packed coordinates, not a common physical measurement uncertainty.

Trial parameter half-widths are epsilon max(1,abs(center)), with
epsilon=1e-8,1e-9,...,1e-12; Tpar=100 epsilon in code-time units. Endpoint
momenta have exactly zero parameter width. N16/N32 close at epsilon=1e-9,
Tpar approximately 1e-7. N64 closes at epsilon=1e-10, Tpar=1e-8. The wider
failed inclusion tests are recorded, not counted as failed physical models.
The tests do not optimize the rectangle or prove a mesh-uniform radius.

## 4. A genuine reduced evolution and a positive time interval

Denote the unique free root by Y(w,t), retaining the fixed packed entries
from the prescribed parameters. On the positive chart the finite formulas
are analytic, [J] is uniformly nonsingular, and the strict inclusions extend
locally past parameter faces. The implicit-function theorem therefore gives
a smooth root branch, with local uniqueness making overlapping definitions
agree. No higher-jet closure is needed.

Define the reduced first-order field using the original canonical force and
the existing metric-link shift solve:

    x_dot = v(Y),
    pi_dot = partial A/partial x, with endpoint nodal entries set to zero,
    h_in,dot = [P(Y)^(-1) (j_Gram(Y,x)-j_matter(Y,x))]_inner,
    P = face_value^T diag(W/(kappa N_q F_q^(3/2))) face_value.

The bulk scalar force and full Gram scalar force are included. The Gram
shift current retains its signed nonlocal link quadrature; it is not replaced
by a metric-only approximation. The shift inverse is enclosed with a
verified componentwise comparison inequality. Only its inner mass velocity
is used in this reduced field; section 6 explains why that qualification
matters.

These definitions produce a locally Lipschitz ODE on the affine space with
the two constant endpoint momenta removed. Let W be its parameter rectangle,
w_0 its center, d_i a directed lower bound on the distance to either face,
and M_i an outward upper bound on abs(w_dot_i) over the entire root tube.
The root enclosure, action force and shift solve give actual M_i, rather
than a rate observed at a saved point.

For each zero-width coordinate the implementation requires M_i=0 exactly.
For every other coordinate choose

    T_safe = (1/2) min(Tpar, min_(M_i>0) d_i/M_i),

rounded downward, and explicitly verify T_safe M_i<d_i. If a local solution
first reached a rectangle face before this time, integrating its speed bound
would give a displacement strictly smaller than its distance to that face,
a contradiction. Smoothness and compact positive-chart bounds allow
continuation up to this time. Thus a unique local reduced solution exists
on [0,T_safe], and F_f(Y(w(t),t);w(t),t)=0 throughout.

The small positive time is a certified sufficient time, not an estimate of
a physical instability time or a maximal lifespan. There is no conversion
of these code-time intervals into seconds here.

## 5. Numerical size and what it does not cover

All 18 neighborhoods, comprising both branches, N16/N32/N64, and saved
times 0,.005,.01, pass the free-root and local residence gates. The final
saved-time results are:

| Cells | Branch | T_safe (code time, approximate) | Parameter inclusion ratio | Initial correction upper |
| --- | --- | ---: | ---: | ---: |
| 16 | GR | 3.55587e-9 | .537147 | 2.34277e-13 |
| 16 | metric-Gram | 3.55261e-9 | .537147 | 2.280e-13 |
| 32 | GR | 7.09135e-9 | .941638 | 4.326e-13 |
| 32 | metric-Gram | 7.08962e-9 | .941638 | 4.333e-13 |
| 64 | GR | 1.41798e-9 | .175219 | 1.08334e-12 |
| 64 | metric-Gram | 1.41785e-9 | .175219 | 1.08136e-12 |

Tables are rounded summaries, not replay inputs. Use the saved binary64
certificate arrays and JSON values for computation. Across all samples the
time is about 1.417e-9 to 7.093e-9. The limiting coordinate is an interior
nodal canonical momentum in each case. Parent contraction factors remain
below .000218, and the search chart remains F>.65957 and N>.81208.

This proves a short local solution of the stated reduction near each sample,
not that the samples lie on one exact solution. The intervals do not cover
the old [0,.01] evolution. A stationary-box estimate this short would require
an impractically large number of steps if repeated naively. A moving-center,
anisotropic tube or a stronger energy estimate is needed for useful coverage.
The nonmonotonic times also reflect the trial-width policy; they are not a
resolution convergence law or evidence of a new physical time scale.

## 6. Remaining shift equations are not silently promoted

The original constraint-tangent implementation separately reports

    D_shift = P mu_dot + j_matter - j_Gram.

The free-constraint root proof only supplies the differentiated constraints;
it does not prove D_shift=0. It uses the inner component of a shift-derived
mass velocity as one boundary evolution rule. Interior mass velocities come
from differentiating the free constraint roots and may not equal every
component of that separate shift solve.

At the rounded compatible-root midpoints, the ordinary evaluator gives
the following full shift residual maxima at saved time .01:

| Cells | GR | metric-Gram |
| --- | ---: | ---: |
| 16 | 7.18331e-7 | 1.91600e-6 |
| 32 | 3.01808e-8 | 6.33086e-8 |
| 64 | 8.88023e-10 | 1.23694e-8 |

These are numerical diagnostics, not interval bounds on the exact roots,
and no equation's residual is replaced by zero. The refinement pattern
motivates a discretization-consistency investigation; it does not prove one,
nor rule out a reduction issue. Both branches face the same test. Consequently
all_shift_equations_verified remains false, and this result must not be
described as a solution certificate for the full parent Euler-Lagrange system.

## 7. Connection to the earlier boundary-source enclosure

There is an additional arithmetic interface to respect. The older source
helper reconstructs scalar maps by polynomial evaluation; the original action
assembly constructs them in a different floating-point order. At N64 their
maximum differences are about 3.782e-16 for values and 1.8475e-13 for gradients.
This is not a discovered physical discrepancy, but it prevents treating the
two realized finite maps as bitwise identical in a computer-assisted proof.
This continuation uses the original assembly maps consistently and saves them.
It does not change any predecessor evidence.

More importantly, the new root tube encloses x, pi and the packed roots, not
the first/second packed jets in the earlier independent jet boxes. One cannot
yet multiply the previous beta_red,t bound by this T_safe and announce a
boundary total-variation certificate. Both higher_jet_box_residence_verified
and boundary_TV_transfer_verified remain false.

The constructive next calculation is now explicit. With z=(w,t), write
the free constraints after substituting fixed data as F_f(y_f,z). Then

    J_ff y_f,dot = -(F_w V + F_t),
    y_fixed,dot = (h_in,dot, a_end).

Enclose this implicit tangent along the new root tube, and enclose D_shift
using the full resulting mass velocity. Differentiate this same identity
again to enclose the compatible second jet, including derivatives of the
canonical force and metric-link shift current. Do not independently select
jets and hope they are compatible. Re-enclose the boundary source using the
same archived assembly maps. These steps test the remaining full-system
consistency and make the time-to-source connection, rather than repeating
the already resolved question of whether a nearby free root exists.

## 8. Arithmetic, controls and preservation

The interval operations round each basic arithmetic operation outward with
nextafter. Matrix products use outward sums of outer products. Square roots
and integer/half-integer powers use the inherited interval primitives. Even
squares of radii enter interval arithmetic before evaluation. The scope
assumes correctly rounded binary64 basic operations/square roots and gradual
underflow; it is not a formal proof-kernel certificate or a continuum error
bound. Precomputed map coefficients and quadrature weights define the finite
model, rather than being mistaken for exact continuum constructions.

The acceptance checks include a scalar known-root control, a no-root
rejection, invalid-radius guards, strict root inclusion and contraction,
positive chart, positive time, every first-exit inequality, exact endpoint
momentum invariance, fixed initial data preservation, and the verified shift
inverse. Independent original residual/Hessian/force comparisons and two
parameter-corner Newton controls per state are rounded diagnostic checks,
not substitutes for the interval proof. Newton residual tolerance is 1e-8;
corner-root comparison allows 2e-10(1+abs(y)) specifically as a rounding
control. No physical or exact-root claim comes from that tolerance test.

Final NPZ evidence additionally contains the root preconditioner, majorant,
search radii, image bounds, parameter residual intervals, and the actual
assembly/basis/Gram/link arrays. Each archive is read back and every array is
required to match exactly. Runtime versions and executed-source snapshots
are recorded. The full source/data hash chain and cited local paths are
checked at sealing.

Probe01 failed with a fixed time-parameter horizon, and its failed status and
executed sources are preserved. Probe02 found a narrower coupled
parameter/time tube. Probe03 includes outward radius algebra and explicit
remaining-shift diagnostics. Completed development attempt01 passed 315
checks; final attempt02 additionally archives all realized coefficient and
root-certificate arrays, verifies their exact roundtrip, and constructs the
scalar control derivative enclosure outward. Earlier attempts are not deleted
or overwritten and are not substitutes for the final evidence.

Final candidate:
`source-intake/navier-stokes/20260910/annular-parent-root-residence-attempt02/status.json`.
Inherited seal:
`source-intake/navier-stokes/20260910/annular-parent-coefficient-box-final-integrity.json`.
Final seal:
`source-intake/navier-stokes/20260910/annular-parent-root-residence-final-integrity.json`.

No new numerical evolution, public update, commit, push, galaxy edit or
frozen-workbench edit is part of this continuation. The workbench check is
an mtime scan since 2026-09-10T12:08:23Z, not a pre-turn full hash baseline.
The calculation uses one single-core BelowNormal Python worker at a time.
