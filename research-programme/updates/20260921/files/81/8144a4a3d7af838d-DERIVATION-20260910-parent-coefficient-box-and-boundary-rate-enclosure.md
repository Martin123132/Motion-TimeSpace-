# Parent coefficient neighborhoods and boundary-rate enclosures

Private continuation, 2026-09-10 (Europe/London). No GitHub action.

## 1. Result and exact meaning

The endpoint-source estimate now extends over explicit nonzero neighborhoods
of the stored parent coefficients AND their first/second time jets. The
enclosure includes the actual third-jet forcing, the differentiated shift
projection with its Gram link current, the parent inverse, and the two scalar
elliptic solves needed by the boundary derivative. It is not an assumed box
around a measured eigenvalue or around an independently chosen forcing vector.

All 18 saved-state neighborhoods pass with the same tested radius parameter
rho=1e-6. At final N64 the enclosed dimensionless source-rate R2 upper is
.206242 GR / .211058 metric-Gram throughout the respective coefficient boxes.
This is a finite-neighborhood estimate, unlike the earlier pointwise bounds.

The boxes are SMALL and defined in the particular stored coordinate/jet
scales. They are supersets of admissible parent data, not a claim that every
point in a box solves the constraints. No actual trajectory residence time,
all-mesh neighborhood theorem, horizon regularity, or local-GR completion is
claimed. Refinement sensitivity remains visible in the elliptic enclosures.

Arithmetic scope: binary64 interval operations round outward at each primitive
operation; matrix interval products use outward accumulation, not an unchecked
BLAS error estimate. Stored basis maps, link quadrature maps and weights are
treated as exact constants of this finite model. The sourced real kappa=1/10
is enclosed by interval division. The result assumes IEEE correctly-rounded
basic operations and square root, with gradual underflow. It is NOT a proof
of rounding bounds for constructing the stored maps, a continuum quadrature
certificate, a validated saved numerical trajectory, or a formal proof-kernel
verification of the entire implementation.

## 2. Sources and the neighborhood

Keep the original canonical Lambda=m_chi=b2=b3=0 branch, positive metric chart,
C1 Hermite scalar space, free slopes and quadratic endpoint histories. Keep
the original affine outer clock and all metric-Gram terms when enabled.

Let y contain the packed mass, lapse and scalar velocities; x the scalar
configuration. For each of y,y1,y2 and x, the coefficient box about its stored
center z0 uses

    |z_i-z0_i| <= rho max(1,|z0_i|), rho=1e-6.

Endpoints with prescribed scalar-velocity FIRST and SECOND rates remain
fixed to their given values. In particular the endpoint scalar-velocity
second rate is zero, as required by quadratic scalar-value histories. The
helper explicitly rejects unsupported nonquadratic input histories instead
of silently using a formula without their third boundary derivative.

The endpoint values and velocities may vary inside their boxes. These boxes
include possible changes of the quadratic boundary data; they do not enforce
that every such choice belongs to one common time along its prescribed
history. A later residence proof must impose that history and the parent
constraints, not interpret the independent box as a physical ensemble.

The first trial rho=1e-6 passes everywhere. The runner has recorded smaller
fallback trials if an inverse gate fails; none was needed. This is not a
maximal-radius search, a coordinate-invariant tolerance or evidence that
arbitrarily fine meshes have the same useful radius.

Owned sources:

- `DERIVATION-20260910-endpoint-metric-adjoint-and-source-specific-bounds.md`
- `DERIVATION-20260910-parent-third-jet-and-boundary-source-variation.md`
- `scripts/annular_parent_coefficient_box_20260910.py`
- `scripts/derive_annular_parent_coefficient_box_20260910.py`
- `scripts/annular_constraint_routhian_20260909.py`
- `scripts/annular_metric_flux_jets_20260909.py`
- `scripts/annular_boundary_source_variation_20260910.py`

## 3. Parent-owned matrix enclosure

Rather than estimate the variation of each Schur-complement factor separately,
enclose the ORIGINAL full free parent Jacobian. This retains cancellations
through a computed preconditioner and a componentwise comparison, without
mixing every unknown into one maximum.

The canonical bulk action density is

    N mu_R/(kappa sqrt(F)) + R^2 q^2/(2N sqrt(F))
                                      -R^2 N sqrt(F) chi_R^2/2.

Its Hessian in (mu,mu_R,N,q) is evaluated by explicit differentiated formulas
over the coefficient box and assembled through the original basis maps.
For example,

    L_mu,mu=3N mu_R/(kappa R^2 F^(5/2))
                  +3q^2/(2N F^(5/2))+N chi_R^2/(2F^(3/2)),
    L_muR,N=1/(kappa sqrt(F)),
    L_N,N=R^2 q^2/(N^3 sqrt(F)),
    L_N,q=-R^2 q/(N^2 sqrt(F)), L_q,q=R^2/(N sqrt(F)).

The remaining mixed terms are retained as well. The actual Gram density d_G
contributes +d_G N F^(-3/2) to the nodal mass-mass block and
+d_G R F^(-1/2) to the mass-lapse block, with the original face-to-node maps.
No Gram kinetic block is inserted: that derivative is zero in THIS canonical
branch. The boundary clock and canonical momenta enter linearly, so their
second packed derivatives vanish.

Positivity is checked on all mass-face knots, lapse nodes and the quadrature
reconstructions. The face-knot condition controls the entire reconstructed
chart because R-2mu is linear between those knots; no positivity inference
from a few interior samples is required.

The scalar velocity block M remains positive on this chart. Thus invertibility
of the full block matrix Jff=[H C;C' M] is equivalent to invertibility of the
metric Schur matrix S=H-C M^-1 C'. The certificate does not require S to be
positive definite and does not remove its scalar feedback.

## 4. Verified componentwise inverse enclosure

For an interval matrix [A], choose a numerical inverse R of its midpoint as a
FIXED point preconditioner. Its numerical accuracy need not be presumed:
compute an outward enclosure for

    E=I-R[A], B=|E| componentwise, eta=max_i sum_j B_ij.

If eta<1, every real A in [A] is invertible. This follows from the Neumann
series for R A=I-(I-R A). The componentwise inverse comparison is

    |(I-E)^-1 v| <= (I-B)^-1 |v|.

For an interval load [b] and a point center u0 form

    vbar=|R([b]-[A]u0)|.

The implementation constructs a nonnegative radius d and then VERIFYINGLY
checks, using outward interval accumulation,

    B d+vbar <= d.

This inequality, rather than trust in the floating-point comparison solve,
proves every A^-1 b lies in [u0-d,u0+d]. The numerical solve only proposes a
radius; it is padded and accepted after the outward inequality check. At or
beyond eta=1 no inverse-persistence conclusion is accepted.

The same procedure encloses the parent solve, each shift-jet solve, and both
elliptic solves. There is no replacement of uncertain scalar/metric blocks by
their sampled inverses without a residual check.

## 5. The third forcing is enclosed from the equations

A degree-three interval Taylor algebra uses normalized coefficients

    y(t)=y+y1 t+y2 t^2/2, with trial y3=0,
    x(t)=x+v(y)t+v(y1)t^2/2+v(y2)t^3/6.

Integer powers are multiplied directly, including squared quantities whose
base interval crosses zero. For the positive metric factors, truncated
binomial composition generates the reciprocal and half-power coefficients.
No complex-step calculation is used to claim interval containment.

Let K(t) be the original full stiffness, including the sampled Gram
coefficient. The canonical momentum third derivative is evaluated as

    pi3=-2 [t^2](K(t)x(t)),

with the same two prescribed nodal endpoint momentum rates held zero as in
the parent code. The scalar slopes remain free. Taking 6[t^3] of the original
canonical constraint expressions, and subtracting pi3 in the scalar momentum
rows, encloses k3. The outer clock is affine and has zero third rate.

The fixed inner mass third jet is also enclosed, not supplied as a measured
constant. Write the original shift equation as

    P(t) v_shift(t)=r_shift(t).

With normalized Taylor coefficients,

    P0 v0=r0,
    P0 v1=r1-P1 v0,
    P0 v2=r2-P1 v1-P2 v0.

Each equation uses the verified comparison solve. The fixed inner third mass
rate is 2v2(inner). The nonlocal metric-link inverse coefficient, signed link
quadrature, differentiated Gram link current and matter shift load are all
included. Only the prescribed inner row is fixed this way; no interior shift
identity is newly imposed.

Finally enclose

    f=-(k3+J y3_fixed)_free, y3_free=Jff^-1 f.

The first/second jets in the box are independent supersets of compatible
ones. This calculation bounds the correct third-jet expression for every
compatible parent datum contained in the box; it does not prove that all
independent jet choices are derivatives of a parent solution.

## 6. The whole source rate, not just theta_tt

The old pointwise coefficient bounds are NOT reused as though constant on the
new neighborhood. The helper encloses M_full, M_full,t, M_full,tt, K_full and
K_full,t over the box, along with the affine endpoint lifts ell,ell_t,ell_tt.
It then encloses

    F_b=-(M_full ell_tt+M_full,t ell_t+K_full ell)_I,
    F_b,t=-(2M_full,t ell_tt+M_full,tt ell_t
                               +K_full,t ell+K_full ell_t)_I,
    psi=K^-1 F_b, psi_t=K^-1(F_b,t-K_t psi).

Endpoint spatial derivatives use the actual one-sided reconstruction maps.
With a=p_R/m, d=c^2 theta_R, w=psi+ell, the earlier exact formula is

    beta_red,t=-d_t w_R-d w_tR-a_t ell_tR-a ell_ttR
                 +(2theta^2-4theta_t)ell_tt
                 +(4theta theta_t-theta_tt)ell_t.

Every term is enclosed: theta, theta_t, theta_R, theta_tR, a, a_t, d, d_t,
the two potential gradients, the boundary data and the parent-derived
theta_tt. The latter uses

    theta_tt=N3/N-3N1 N2/N^2+2(N1/N)^3
                -mu3/(R-2mu)-6mu1 mu2/(R-2mu)^2-8(mu1/(R-2mu))^3.

The prior identity b=B beta_red,end+b_red,reg is unchanged. The weak
compatibility remainder and regular source have not been erased. This step
encloses the boundary-rate formula; it does not separately establish the
remaining mesh-uniform regular-source energy estimate.

## 7. Results and fair controls

The final full run passes 315/315 checks. The 18 original states are unchanged.
Controls include exact-rational small matrix products, Taylor squaring through
zero, rejection of singular/invalid neighborhoods, and explicit rejection of
unsupported nonquadratic histories. Both the original evaluator and two
alternating-sign coefficient corners per state are enclosed by the new
interval formulas. Corner states are OFF-CONSTRAINT algebraic controls, not
new physical trajectories and not the reason the entire box is bounded.
The interval construction and verified comparison inequality supply that
whole-box implication.

All final-state boxes use rho=1e-6:

| Cells | Branch | Whole-box source-rate R2 upper | Parent eta | Elliptic eta |
| --- | --- | ---: | ---: | ---: |
| 16 | GR | .205238 | .00021584 | .00035227 |
| 16 | metric-Gram | .204683 | .00021584 | .00059653 |
| 32 | GR | .205837 | .00021719 | .00142626 |
| 32 | metric-Gram | .207238 | .00021719 | .00242566 |
| 64 | GR | .206242 | .00021744 | .00572226 |
| 64 | metric-Gram | .211058 | .00021744 | .00974219 |

At final N64 the endpoint derivative enclosures are

    GR:   [-.148012153,-.146181637], [-.143625413,-.141658788],
    Gram: [-.150543340,-.143090976], [-.147926855,-.135840219].

Across all 18 boxes the R2 rate uppers range from .204683 to .211473. The
minimum chart values remain approximately F>=.65957 and N>=.81208. These are
properties of the selected small boxes, not universal theory constants.

The elliptic contraction factors increase with refinement, and the largest
third-jet enclosure radius grows from about .82 to13.23 in GR and .93 to14.98
in Gram, mainly in the scalar-velocity block. These warnings are retained.
Passing at three meshes does not prove a useful continuum neighborhood.

The new bound is smaller than the previous analytic pointwise upper because
it uses a narrowly specified coefficient neighborhood and componentwise
enclosures, rather than broad global norm majorants. This is not a statement
that uncertainty improves the physics or that a wider neighborhood must pass.

## 8. Exact route from this result to time control

The missing step is now trajectory residence and initial compatibility, not
an assumed inverse or an independently guessed third forcing.

A constructive route is the augmented jet flow

    xdot=v(y), ydot=y1, y1dot=y2, y2dot=y3(x,y,y1,y2),

with canonical momentum evolution and the prescribed boundary histories.
The coefficient-box result already encloses its displayed right-hand side.
For a compatible initial datum in the interior of a box, let d_i be its
distance to each nonconstant coordinate face and B_i a genuine upper bound
for that coordinate's speed. A standard first-exit argument yields the
conditional residence time

    T_safe < min_(B_i>0) d_i/B_i.

Fixed-width-zero coordinates must be invariant under the prescribed boundary
flow; they cannot simply be divided by a zero speed and forgotten. While the
flow stays inside, TV(beta_red;[0,T]) is bounded by the whole-box rate upper
times T. No numerical T_safe or covering chain has been certified here.

Crucially, differentiating the constraints three times is NOT a substitute
for initial constraints. A lifted flow with F_parent'''=0 preserves

    F_parent(t)=F_parent(0)+t F_parent'(0)+t^2 F_parent''(0)/2,

not automatically F_parent=0. The stored numerical states and jets have
finite residuals, not an exact-zero certificate. Therefore the next attempt
must establish a compatible initial enclosure (or retain and bound those
residuals explicitly), connect the actual boundary history, and only then
claim residence of a parent solution. A very short formal jet-flow interval
would not by itself validate the saved physical trajectory or the whole
saved interval [0,.01].

## 9. Preservation and next target

Next derive a constraint-compatible local residence step using the new
componentwise bounds and an initial root enclosure. Avoid another pass merely
listing the already enclosed k3 or matrix as missing. Do not claim the
entire old evolution is validated by these disjoint boxes. Mesh-uniform
regular-source/jump control and positive-annulus continuation remain separate
obligations after the local step.

Final candidate and chain:

- `source-intake/navier-stokes/20260910/annular-parent-coefficient-box-attempt02/status.json`
- `source-intake/navier-stokes/20260910/annular-endpoint-metric-adjoint-final-integrity.json`
- `source-intake/navier-stokes/20260910/annular-parent-coefficient-box-final-integrity.json`

The one-state probe passed 42 checks. The first complete development run
passed 297 checks and remains preserved with its executed source snapshots.
The final rerun adds the explicit nonquadratic-input rejection; it does not
repair a failed physics test or alter the original data. The older complete
development run is marked superseded, not deleted.

The seal verifies inherited/new SHA256 evidence and cited paths, and records
a resume snapshot. Protected-workbench verification is an mtime scan since
2026-09-10T11:42:58Z, not a full pre-turn content-hash baseline. No GitHub,
galaxy, frozen-workbench or prior completed research evidence changes. Runs
use one single-core BelowNormal Python worker and leave no bytecode cache.
