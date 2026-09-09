# Normal reconstruction, curvature improvement, and a discrete regularity obstruction

Private continuation, 9 September 2026. Previous goal turn: **progress**, verified
against the completed current time-jet, curvature-transfer and error-map owners.
This turn derives and implements the proposed reconstruction, tests it on the
same ordinary parent data and on a finer evolution, and derives trace lower
bounds that prevent a misleading regularity promotion.

## 1. Outcome without overclaiming

The current-equation reconstruction greatly improves K1 stencil agreement.
It works at the endpoints AND sampled cell interiors, without suppressing the
mass constraint or numerical source. All four K1 stencil gates pass at N512
and N1024. But this is not a complete curvature/continuum pass:

- Three nodal Z gates still fail at both resolutions.
- Finer-grid differences are not uniformly decreasing; canonical early K1
  changes more on the last refinement despite excellent within-grid agreement.
- The N1024 evolution itself finishes **128/129**, failing the early canonical
  mass mesh-refinement test at an absolute difference about1.21e-15.
- The reconstructed metric's high-derivative norms are not controlled uniformly
  by the evidence. There is a definite alternating-grid component in the mass
  traces, which a centered first derivative does not see in the interior.

This identifies a numerical obstruction to a clean local-geometry bound, not
a newly discovered physical singularity or a failure of GR/MTS. The physical
coupling, first-u/finite-u control and full GR/Newton/Maxwell limits remain open.

## 2. Derived radial normal form

Work in t=v-sigma(R-4), sigma=.05, current state e=(chi,w,h,mu,delta), on the
same normalized annulus R in[4,8]. Define the CURRENT-coordinate gradient rows

    q_y, f_y, G_y=g, D_y, V_y, f_mu,y,

with background mass-constraint defect J0. All coefficients retain their
ordinary off-shell parent meaning. Let d be the background defect and S the
actual saved numerical source. Define the retained discrete constraint

    j_h = D_h e_mu - g e.

It is NOT set to zero. The radial system is

    M e_R = A e + Btime e_t + fsource,

with rows

    M = [ unit_chi ; q_y ; f_y-f_mu unit_mu ; unit_mu ; unit_delta ],
    A = [ unit_w ; -q_y,R ;
          -f_y,R-2f_y/R+V_y-f_mu g+J0 f_mu,y ; g ; D_y ],
    Btime = rows [0 ; unit_w ; unit_h ; 0 ; sigma unit_delta],
    fsource = [0, d_w-S_w, d_h-S_h, j_h,
               sigma(d_delta-S_delta)].

This follows by expanding the scalar flux divergence and the coupled current
equations, rather than selecting desirable curvature values. Numerical sources
appear explicitly. No zero mass-defect substitution is made. The scalar
kinematic equation e_chi,R=e_w retains the existing initial integrability
offset relative to D_h e_chi; it does not pretend that offset was zero.

Using q_y=(0,B/alpha,1/alpha,-h_mu/alpha,-h_delta/alpha) and
f_y=B q_y+(0,c,0,f_mu,E f_E), direct symbolic evaluation gives

    det M = -c/alpha.

The normal form is consequently restricted to noncharacteristic surfaces with
nonzero alpha,c and controlled inverse. Maximum sampled condition number here
is below80. This is NOT an extension through c=0 or proof of horizon/interior
regularity. A characteristic surface needs another evolution/reconstruction
description, not division by a vanishing c.

For normalized jets e[a,b], through a+b<=3, initialize e[a,0] from the verified
current time derivatives. For b=0,1,2 and a=0,...,2-b, solve

    M00 (b+1)e[a,b+1] = [A e+Btime e_t+fsource][a,b]
        - sum_{(i,j)!=(0,0)} M[i,j](b-j+1)e[a-i,b-j+1].

Ascending a within each radial order closes the triangular recurrence. The
coefficients are Taylor-differentiated in time using the same actual cache as
the evolution, and polynomial-differentiated in R by independent poly7/poly9
stencils. The nonzero j_h and S coefficients and their derivatives remain.
Polynomial differentiation of a coefficient is still a numerical approximation,
not a theorem about its unknown interpolation remainder.

The radial system does not discard the mass time equation. Its compatibility
residual is separately evaluated:

    E_mu = e_mu,t-C_y e+d_mu-S_mu.

It vanishes to replay accuracy at the nodes at time-derivative orders, but its
mixed radial derivatives generally do not vanish. These are recorded, not
used as extra equations that would overwrite the supplied j_h or e_t.

## 3. An actual C3 reconstruction, not arbitrary unglued jets

A degree7 Hermite polynomial on every spatial cell matches values and first
three radial derivatives at both ends. The same nodal derivatives are shared
by adjacent cells, so the represented field is C3 in space. Time Taylor
coefficients are matched through total order3. Higher mixed coefficients are
set to zero solely to define a smooth representative; they are not inferred
derivatives of the physical solution.

This raw normal reconstruction does not preserve the entire analytic initial
mass function between nodes: its mass radial data are D_h e_mu=g e+j_h. The
resulting reconstruction error belongs to the calculation, not to the parent
theory. No claim that these derivative traces equal exact continuum initial
jets is made.

The experiment retains and saves:
- all current nodal/time data and original source coefficients;
- the original nonzero mass constraint;
- C3 endpoint matching errors and normal-system residuals;
- the otherwise overdetermined mass time-compatibility residuals;
- subcell integrability error e_chi,R-e_w;
- subcell PDE residual relative to an explicitly declared piecewise-linear
  extension of the original source. That extension is numerical, not physical.

Subcells at fractions1/4,1/2,3/4 are sampled in EVERY cell. Finite residuals
are not called small/acceptable merely because they are finite. At N512 the
largest scalar/current subcell PDE residual is of order1e-9, and integrability
errors reach1.46e-10. Full continuum residual/error enclosures remain absent.

## 4. Curvature results on unchanged data

The comparison denominator is the larger CORRECTION norm, never the much
larger background curvature. The old10%+1e-25 gate is unchanged. All old
polynomial-only curvature failures remain recorded.

| Fixture,T | N512 nodal Z difference | N512 nodal K1 difference | N1024 nodal Z difference | N1024 nodal K1 difference |
|---|---:|---:|---:|---:|
| canonical,.1 | 1.670% | .00575% | 3.669% | .01174% |
| canonical,.3 | 25.528% | .01291% | 13.850% | .00904% |
| nonlinear,.1 | 30.316% | .03828% | 12.382% | .03236% |
| nonlinear,.3 | 41.281% | .01955% | 30.248% | .01290% |

All sampled subcell Z/K1 stencil comparisons pass at both resolutions. Only
canonical early time passes the combined nodal+subcell Z/K1 sensitivity gate.
No combined curvature pass is claimed for the other three cases.

N1024 evolution repeats the N256 and N512 runs bit-for-bit in every stored
shared array. It uses identical equations, constants, original projected
source, C3 initial family and zero dissipation; only spatial resolution is
extended. The adapter's execution snapshot and the unchanged base runner are
both hashed, so the resolution extension is not hidden.

The finer evolution's sole failed field check is canonical T=.1 mass mesh
refinement: previous difference9.1781e-16, new difference1.20634e-15. The time
halving mass difference is4.90e-23. The other three field components, boundary
conditions and source tests do not turn this one failure into a pass.

Excellent K1 agreement between stencils is NOT enough: in canonical early
time, the poly7 K1 grid difference increases from5.29e-13 to9.39e-12. Thus even
the improved reconstruction cannot presently be promoted to a converged
curvature prediction. There is no attempt to hide that via a stencil-only flag.

## 5. The remaining Z difference is the retained constraint derivative

For the two normal reconstructions, nodal values and leading mass/lapse radial
and mixed-time derivatives coincide to rounding. The exact difference reduces
to

    Delta(delta Z) = (2/R)Delta(e_mu,RR)-2F Delta(e_delta,RR),
    Delta(e_mu,RR) = Delta(j_h,R)+(Delta g_R)e+g Delta(e_R).

This four-channel identity is verified against geometric Z, not a mass-based
curvature proxy. At N512 the contribution from (2/R)Delta(j_h,R) equals the
peak Z difference to the shown precision in all four cases:

    3.657575e-13, 1.243409e-11, 2.013961e-11, 7.559810e-11.

Coefficient-radial and changed-current-radial contributions are around1e-24
to1e-23. Lapse second-derivative differences are retained but do not set the
global maximum. This is why setting j_h=0 would deceptively improve a test;
that is expressly NOT an allowed repair.

## 6. Derived regularity lower bounds from the cell traces

Use H3 for the scalar and H4 for the metric as a sufficient pointwise
second-scalar/third-metric derivative target. H4 on every auxiliary current is
unnecessarily strong for the curvature transfer and is not used as a physics
rejection criterion. These Sobolev targets are sufficient, not necessary.

For a cell[a,b] of length h, let sec=(f(b)-f(a))/h and define

    T3 = f'(a)+f'(b)-2 sec,
    L4 = f''(a)+(4f'(a)+2f'(b)-6 sec)/h,
    R4 = f''(b)+(6 sec-2f'(a)-4f'(b))/h.

Taylor's integral remainder, after shifting a=0, gives

    T3 = integral_0^h s(h-s)/h * f'''(s) ds,
    L4 = integral_0^h s(h-s)^2/h^2 * f''''(s) ds,
    R4 = integral_0^h s^2(h-s)/h^2 * f''''(s) ds.

The first kernel has squared L2 norm h^3/30. The last pair has Gram matrix

    h^3 [[1/105,1/140],[1/140,1/105]],

whose inverse is h^-3[[240,-180],[-180,240]]. Cauchy-Schwarz / orthogonal
projection onto these kernels therefore proves

    ||f'''||_L2(cell)^2 >= 30 T3^2/h^3,
    ||f''''||_L2(cell)^2 >= [30(L4+R4)^2+210(L4-R4)^2]/h^3.

Summing cells gives lower bounds for ANY H3/H4 reconstruction that keeps those
traces, not just our degree7 choice. Symbolic kernels, monomials through degree7
and eight/ten-point exact-degree polynomial quadrature are checked independently.
Floating evaluations are not interval-certified bounds, but the analytical
inequalities do not rely on a selected interpolating polynomial.

Define the combined sufficient physical norm by
||e||_*^2=||chi||_H3^2+||mu||_H4^2+||delta||_H4^2. For this norm, these
trace lower bounds already force roughly55% of the measured norm at N512.
Replacing the degree7 polynomial alone cannot remove that cost while retaining
all the same traces. The available refinement differences in these strong
norms do not support a uniform continuum-error estimate.

This is NOT a proof that a true continuum solution lacks H4 regularity. It is
an obstruction to claiming such control from the particular supplied numerical
traces without further error estimates or a better discretization.

## 7. A concrete centered-derivative blind mode

The interior fourth-order centered derivative has Fourier symbol

    D_h(theta)=i sin(theta)(4-cos(theta))/(3h).

It vanishes at theta=pi as well as theta=0. Therefore alternating nodal data
A(-1)^i have zero derivative in the INTERIOR even though they are not a
constant field. The SBP boundary rows detect them; this is not a claim that
the full anchored derivative matrix has a global nullspace. Symbolic and
direct N128/256/512/1024 checks preserve that distinction.

For checkerboard values with zero derivative traces on a subannulus of length
L, the preceding inequalities give

    ||f'''||_2^2 >= 480 L A^2/h^6,
    ||f''''||_2^2 >= 120960 L A^2/h^8.

Thus a tiny unresolved alternating component can be quiet in a centered
constraint residual while obstructing a mesh-independent high-derivative
bound. A finer grid is not by itself a cure. Any antisymmetric centered
integer-grid first derivative has the same Nyquist zero, so merely changing
from fourth to sixth central order does not remove this structural issue.

Actual mass trace defects have adjacent-cell cosine correlations between
-.99993 and-.99999 at N512/1024. Their diagnostic alternating amplitudes are
about1e-16 to4e-15. This is strong evidence of a numerical alternating mode,
not proof of its unique producer or an assertion that all discrepancy is
floating-point roundoff. The full nodal-value/slopes/curvatures and all-cell
regularity lower bounds remain saved.

| Fixture,T | mass H4 trace floor N512 | mass H4 trace floor N1024 |
|---|---:|---:|
| canonical,.1 | 8.78646e-5 | 5.14969e-4 |
| canonical,.3 | 3.60084e-4 | 4.13973e-4 |
| nonlinear,.1 | 3.96921e-4 | 1.40176e-3 |
| nonlinear,.3 | 7.46836e-4 | 2.21569e-3 |

These normalized diagnostic floors are not SI error bars or experimental
violations. They explain why excellent nodal constraint tests cannot be
substituted for derivative control.

## 8. Next constructive repair

Do not run N2048 merely to try to force a green relative gate. Isolate the
mass-source completion as a likely channel for the alternating mode, keeping
the same parent, C3 initial family, boundary conditions and scalar/lapse source.
The cleanest comparison is to preserve the projected q/lapse source and replace
only its centered-band mass solve with the already-derived bounded Volterra
integration. Report the resulting nonzero all-row source residual WITH its
bound, rather than insisting on an exact discrete identity that is blind to
the mode. This is a proposed numerical experiment, not an established cure.

The existing raw-source Volterra run was on the OLD continuum initial family
and failed141/145; it is preserved and is not evidence for success with the
C3 family. A new hybrid test must also keep its scalar-source change separate
from a mass-only intervention. Do not reuse projected-source time derivatives
for that new operator: differentiate its actual cell-exponential recurrence
and source terms before any curvature promotion.

Accept only matched field, endpoint/subcell curvature, constraint-residual
bounds, parity and strong-norm comparisons. If one-sided integration is
insufficient, the next numerical construction needs explicit high-frequency
control or staggered/coercive derivatives with their conservation remainder
owned. Nothing here licenses a new physical closure, deleting j_h, filtering
reported data until they pass, or treating one successful fixture as local GR.

## 9. Evidence and safe save

Owners under `source-intake/navier-stokes/20260909/`:

| Owner | Terminal result | UTC |
|---|---|---|
| `annular-current-normal-reconstruction` | software526/526; three combined curvature gates fail | 08:02:56 |
| `annular-normal-constraint-H4-diagnosis` | 90/90 | 08:09:33 |
| `annular-trace-regularity-lower-bounds` | 62/62 | 08:13:47 |
| `annular-coupled-current-third-corner-N1024` | FAILED128/129 | 08:17:45 |
| `annular-normal-spatial-refinement-validation` | software91/91; field/combined curvature flags false | 08:18:34 |
| `annular-centered-constraint-mode-diagnosis` | 27/27 | 08:21:28 |

The failed N1024 owner has no COMPLETE marker. Completed diagnostic workflows
are not physics passes. All `valid_for_physics_claim` flags stay false.
Runners refuse to overwrite owners. Their input paths, source/execution hashes,
data artifacts, residuals and comparisons are in the corresponding status files.

New scripts:
- `scripts/annular_current_normal_reconstruction_20260909.py`
- `scripts/derive_annular_current_normal_reconstruction_20260909.py`
- `scripts/run_annular_coupled_current_spatial_refinement_20260909.py`
- `scripts/diagnose_annular_normal_constraint_and_H4_20260909.py`
- `scripts/derive_annular_trace_regularity_lower_bounds_20260909.py`
- `scripts/validate_annular_normal_spatial_refinement_20260909.py`
- `scripts/diagnose_annular_centered_constraint_mode_20260909.py`

No subagents, GitHub action, workbench or galaxy edits. One single-core
BelowNormal evolution and at most one modest checker ran concurrently.
All workers have exited; this is a safe check-in well before four hours.

Final read-only integrity replay at08:28 UTC verifies120 unique input hashes,
48 saved output hashes, all seven new scripts compiling without bytecode,
the failed evolution's missing COMPLETE marker, and unchanged false claim
flags. The resume points to the source-completion experiment, not more blind
mesh refinement. No files outside this post-checkpoint tree were written.
