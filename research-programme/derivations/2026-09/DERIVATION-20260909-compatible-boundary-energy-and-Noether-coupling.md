# Compatible boundary energy and Noether coupling

2026-09-09, private continuation in post-checkpoint-work.
Previous goal turn: **progress**, verified against its completed evidence and
preserved FAILED 134/137 evolution. This continuation tackles the actual
left-boundary discretization and its connection to the mass constraint.

## 1. A specific truncation defect, not a change of theory

The previous wave discretization applies the SBP first derivative twice.
A first derivative with second-order boundary closure does not automatically
give a second-order second derivative by composition. Direct rational algebra
gives, for a cubic on the unit grid, the first six errors in D1^2 x^3 - 6x:

(3259806/608923, 882/731, -38518/35819, -38/5117, 3539/25284, -11/588).

On a grid with spacing h these cubic errors scale as h. The composition is
therefore only first-order at those boundary rows, despite a fourth-order
interior stencil. The previous troublesome R=4.015625 is precisely in this
boundary layer. This does not alone prove every observed error has that cause.

We solve for a dedicated second derivative D2 and surface derivative S using:
- the existing diagonal SBP norm;
- the existing fourth-order interior second-derivative stencil;
- exact second derivatives of polynomials of degree at most three;
- a third-order surface derivative;
- symmetry of M=-H D2+B S.

The resulting boundary coefficients are unique under these restrictions.
No physical MTS coefficient, field, initial datum, or boundary condition is fit.

This is an established numerical-analysis construction, not a new physical
mechanism. Method attribution: Mattsson and Nordstrom, *Summation by parts
operators for finite difference approximations of second derivatives*, JCP
199 (2004), 503-540.
[Primary paper](https://www.sciencedirect.com/science/article/pii/S0021999104000932).
The coefficients and compatibility remainder used here are derived and checked
locally, rather than trusted because of a citation.

## 2. Exact compatible operator and positive remainder

At unit spacing the norm starts (17,59,43,49)/48. The left four rows of D2 are

(2,-5,4,-1,0,0),
(1,-2,1,0,0,0),
(-4,59,-110,59,-4,0)/43,
(-1,0,59,-118,64,-4)/49.

The left surface derivative is S=(-11/6,3,-3/2,1/3).
Reflect the second derivative evenly and the surface derivative oddly at the
right endpoint. Interior D2 coefficients are (-1,16,-30,16,-1)/12.
Divide D2 by h^2 and S by h for physical mesh spacing.

Compatibility is stronger than symmetry:

M=D1^T H D1+R,   R=Delta3^T W Delta3,

where Delta3 has rows (-1,3,-3,1). W is symmetric. Away from boundaries it has
diagonal 5/72 and adjacent entries -1/144. Its first three diagonal entries are

59097/573104, 1825/25284, 491/7056.

The first two adjacent entries are 253/50568 and -3/392, and there is one
additional entry W_02=W_20=-1/392. Reflect these modifications at the right.

The diagonal-dominance margins are

3821/39984, 5/84, 185/3528, 1/18, ..., 1/18,

with the reflected boundary tail. The absolute row sums are at most 1/9.
Consequently, for every disjoint-closure grid used here,

(185/3528) I <= W <= (1/9) I.

The boundary templates have finite support; the interior symbol is
|Delta3|^2/18+|Delta4|^2/144. Together these give the same compatibility identity
for all N>=16 intervals, not an extrapolation of positive eigenvalues alone.
The rational script explicitly verifies the full identities at N16 and N24;
the independent implementation rechecks N16,N32,N64.

At spacing h the remainder in the energy matrix is R/h. It adds positive
control of grid-scale scalar components missing from the composed operator's
gradient energy. Constants still have zero gradient energy, as they should.

Derivation owner:
source-intake/navier-stokes/20260909/sbp4-second-derivative-derived/status.json
(18/18, completed 03:28:01 UTC).

## 3. Positive variable-coefficient extension

Simply multiplying a constant-coefficient second derivative by c(R) does not
give the desired symmetric variable-coefficient energy matrix.

Use the diagonal-dominant decomposition

W=diag(margin_i)+sum_(i<j) |W_ij| v_ij v_ij^T,
v_ij=e_i+sign(W_ij)e_j.

Weight each nonnegative term by c at its local stencil center, with positive
linear interpolation of the sampled c values. This defines W_c, reducing
exactly to cW for constant c. For c_min<=c<=c_max,

c_min W <= W_c <= c_max W.

Thus the variable-coefficient matrix

M_c=D1^T H_h diag(c) D1+Delta3^T W_c Delta3/h

is positive semidefinite, and defines

D2_c=H_h^-1[-M_c+B diag(c) S_h].

Here H_h=h H. This is a conservative approximation to (c chi_R)_R.
For smooth coefficients the boundary modification cancels the composed
operator's leading first-order error: local variation of c across a boundary
stencil is O(h), so its additional remainder starts at O(h^2). The interior
correction is fourth order. The manufactured tests check the actual operator,
including nonconstant c, not only the constant-coefficient identity.

Implementation:
scripts/sbp4_compatible_second_operator_20260909.py

## 4. What the scalar energy estimate does and does not prove

Let alpha=-A_t>0, beta=b-sigma*c, and consider the principal scalar system

chi_t=q,
alpha*q_t=2 beta D1 q+D2_c chi+F.

Its discrete energy is
E=(q^T H_h alpha q+chi^T M_c chi)/2.

Use the same incoming characteristic condition as before, but with S_h chi
as the numerical surface derivative. The endpoint denominators are

d_left=(sqrt(beta^2+alpha*c)-beta)/c,
d_right=(-sqrt(beta^2+alpha*c)-beta)/c.

The SAT signs are plus at the left and minus at the right, each multiplied by
c/(alpha H_h,ii). For homogeneous boundary data, the resulting boundary work is

-sqrt(beta_left^2+alpha_left*c_left) q_left^2
-sqrt(beta_right^2+alpha_right*c_right) q_right^2.

For variable beta the remaining mixed-derivative term is exactly
q^T H_h[beta,D1]q, rather than zero. The finite stencil gives the mesh-independent
bound

|q^T H_h[beta,D1]q|
<= C_SBP ||beta_R||_infinity ||q||_(H_h)^2,
C_SBP <= (42/17)*sqrt(59/17).

For positive time-dependent alpha,c, the time variation of the energy weights
is bounded by ||alpha_t/alpha||_infinity and ||c_t/c||_infinity.
The latter also bounds each positive interpolated coefficient in W_c.
Hence, with the displayed principal system and homogeneous boundary data,

E' <= [||alpha_t/alpha||_infinity+||c_t/c||_infinity
       +2 C_SBP ||beta_R||_infinity/alpha_min] E
      +sqrt(2E) ||F/sqrt(alpha)||_(H_h)
      -the two nonnegative endpoint losses.

Nonzero boundary data add their explicit boundary forcing terms. Lower-order
parent couplings must be retained in F or separately bounded.

This is a derived scalar principal energy estimate. It does **not** yet bound
the full coupled MTS evolution: the subsequent Noether source projection,
induced mass source, lapse coupling, and all lower-order terms remain present.
A positive scalar energy matrix must not be advertised as a full nonlinear,
finite-u, horizon, or local-GR stability theorem.

## 5. Known-solution control and the coupling repair

The manufactured solution is chi=sin(2pi R) cos(2t), with its exact forcing and
incoming boundary data, on [0,1] through T=0.2. Both the composed and compatible
methods see the identical data, forcing and refinements. The cases use constant
coefficients and smoothly varying alpha,beta,c.

The first control was FAILED 40/42: spatial accuracy improved so much that the
time-discretization error no longer met the 1% subordinate-time-error gate.
Reducing the CFL factor from 0.15 to 0.05, without changing that gate, gives
44/44 in the refined-time control. Both methods converge against the known
solution. At N256 with the finer time step, maximum velocity errors are:

| Case | Composed | Compatible |
| --- | ---: | ---: |
| constant | 2.1267344e-4 | 5.5682088e-8 |
| variable | 2.2379480e-4 | 1.2411422e-7 |

The homogeneous scalar energy identity is also independently checked in both
cases. These are numerical-method benchmarks, not comparisons of MTS with GR.

Owners:
source-intake/navier-stokes/20260909/sbp4-compatible-wave-control/status.json
source-intake/navier-stokes/20260909/sbp4-compatible-wave-control-refined-time/status.json

The first MTS integration of D2_c exposed an additional coupling problem.
It placed the spatial replacement in the bulk evolution, while completing only
the SAT/filter sources. This cleared all eight spatial gates but failed two
T=0.3 full mass-constraint comparisons: FAILED 135/137, preserved.

The replacement is itself a numerical scalar source. For the evolved scalar
remainder eta, relative to the previous frozen bulk, it is

S_q,spatial=[D2_c eta-c D1^2 eta-c_R D1 eta]/alpha.

The analytic c_R term ensures this is a discretization change, not an extra
continuum term. The continuum initial lift and its analytic derivatives are
unchanged. The actual parent coefficient c_R is differentiated from the parent
fields, including explicit R and implicit field/gradient dependence.

The corrected integration includes S_q,spatial alongside the raw SAT and filter
sources BEFORE the existing scalar-only Noether projection and mass completion.
Thus the whole numerical change obeys

M_h S=(D1-G_mu)S_mu-G_q S_q-G_delta S_delta=0,

including the outer row, with S_mu(8)=0 and the lapse source unchanged.
It is not legitimate to leave a numerically altered wave equation disconnected
from the mass equation. Neither implementation cancels the original parent
constraint drift or supplies a missing physical MTS coefficient.

Implementation:
scripts/annular_compatible_boundary_evolution_20260909.py

## 6. Preserve the boundary source while completing the bulk change

Completing the whole spatial change restores all eight mass-constraint gates
at N256, but the unrestricted minimum-norm scalar projection itself alters the
endpoint q sources. Two first-u boundary-data gates then fail. This exposes an
additional requirement: the conservation completion should not change the
already derived incoming-characteristic boundary penalty.

Keep both endpoint scalar sources fixed as well as all lapse sources and the
outer mass source. Let a=ell*G_q, with ell the existing left compatibility
covector. Define a_I by setting the endpoint entries of a to zero and retain
the full compatibility mismatch

r=ell^T(G_q S_q+G_delta S_delta).

For W_q=H_h alpha, d_I=a_I^T W_q^-1 a_I, the unique minimum-change interior
correction is

Delta S_q=-W_q^-1 a_I r/d_I.

It leaves both endpoint q sources exactly unchanged and still enforces the
full compatibility condition. The same anchored mass solve then gives C(8)=0
and cancellation on every constraint row, not just in the interior.

When d_I>0 its norm is bounded by

||Delta S_q||_(W_q)^2
<= (d_all/d_I) ||S_q+L S_delta||_(W_q)^2,
d_all=a^T W_q^-1 a,  L=-q(a_scalar-sigma*b)/A_t.

Here a_scalar is the parent scalar-density coefficient, not the covector a.
The amplification sqrt(d_all/d_I) must be measured/bounded, not silently set
to one. If d_I=0 with nonzero mismatch, this boundary-fixed route fails and
the implementation raises an error. If both vanish no projection is needed.
There is still no individual division by the scalar velocity.

Preserving the endpoint sources keeps the scalar SAT boundary-work identity
intact. It does not prove the interior projection work is negative or complete
the coupled mass/lapse energy estimate. This restriction is motivated by the
boundary equation and energy identity, not by a fitted physics parameter.

Implementation:
scripts/annular_boundary_preserving_completion_20260909.py
scripts/annular_boundary_preserving_evolution_20260909.py

## 7. Evolution results and final evidence

All owners are under source-intake/navier-stokes/20260909/.

| Owner | Result | Completed UTC |
| --- | --- | --- |
| sbp4-second-derivative-derived | 18/18 | 03:28:01 |
| sbp4-compatible-wave-control | FAILED 40/42 | 03:32:12 |
| sbp4-compatible-wave-control-refined-time | 44/44 | 03:33:18 |
| annular-compatible-boundary-initial | FAILED 135/137 | 03:37:24 |
| annular-compatible-Noether-boundary-initial | FAILED 135/137 | 03:41:31 |
| annular-compatible-Noether-boundary-refined | FAILED 136/137 | 03:53:06 |
| annular-boundary-preserving-initial | FAILED 135/137 | 03:52:53 |
| annular-boundary-preserving-refined | FAILED 136/137 | 04:00:31 |
| annular-compatible-boundary-evidence-final | 95/95 | 04:02:00 |

The selected boundary-preserving N512 run clears all eight spatial refinement
gates, with max-norm factors 2.34--6.29 against the unchanged 1.3 gate. All eight
time-refinement and full mass-constraint improvement gates pass. The earlier
failed second-order time diagnostic is replaced by the independently justified
five-point diagnostic at the original tolerance, not by a looser tolerance.

One gate remains failed: canonical first-u, T=0.3, scalar boundary-data error
is 1.17977% of its stated scale, against the unchanged 1% gate. Its absolute
error is 1.14158e-10. The lapse part of that gate passes. The initial N256
boundary-preserving run had two such failures; the nonlinear one clears on
the existing N512 comparison. We do not launch N1024 simply to obtain green
checks, exclude the boundary row, or promote this run to accepted evolution.

At T=0.3 the selected full-constraint maxima are 5.65255e-14/2.68296e-13 for
canonical reference/first-u and 3.16264e-13/4.71453e-14 for nonlinear
reference/first-u, below the corresponding uncorrected constraints. All-row
added-source cancellation, zero outer mass source, unchanged endpoint scalar
sources and unchanged lapse sources are independently replayed from the saved
data. Original parent/background drift remains in the budget.

The measured restricted-projection norm factor at the four finest outputs is
1.00063--1.00106. The derived norm inequality passes, but these samples do not
prove a uniform bound over arbitrary backgrounds or a complete energy theorem.
The extra interior projection work is not always negative and remains recorded.

Against the previous same-grid, same-initial-data Noether method, the largest
correction-component change is 1.981% (canonical first-u mass at T=0.3).
Scalar/velocity changes are below 0.238%. These finite-method changes must not
be confused with fitted physical parameters or observational error bars.

Evidence script:
scripts/annular_compatible_boundary_evidence_20260909.py
It checks hashes, terminal states, manufactured controls, the spatial-coefficient
derivative, full constraints, endpoint/source invariants, actual RHS and drift
replay, the restricted norm bound, and matched initial data. Its 95/95 result
explicitly records selected_evolution_state=failed.

Selected evolution SHA256:
0f69d55b1b6b567629615c5048051a80e382d308390bdffc997e81dbbf1a9176.
Evidence SHA256:
4503aed6266c2eef4c1acc6266c25a0105ff015b5b2cb9240ff2a98d307bde7a.

## 8. Physics continuation rather than another mesh-only loop

The companion derivation now supplies an exact curvature/stress identity and
reduces its off-shell error to the parent mass, lapse and scalar residuals and
their derivatives:
DERIVATION-20260909-curvature-stress-residual-bridge-and-delta-K.md.

Next, evaluate those residual derivative jets and carry their errors through
the explicit delta K1 variation. Keep the one boundary gate and full coupled
energy gap open; the remaining finite-grid boundary/corner analysis can inform
that error budget without pretending the current numerical solution is exact.

All jobs have exited at this safe save point. At most two single-core,
BelowNormal jobs ran concurrently; no subagents or GitHub actions were used.
All authored files are within post-checkpoint-work. Frozen workbench, galaxy
files and other tasks/processes were not changed or stopped.
