# Joint source refinement, the source-inertia law, and a stiffness-aware next step

2026-09-19 local date. Private continuation of
`DERIVATION-20260918-P2-conforming-force-lift-and-targeted-refinement.md`.
Status: complete derivation, initial-grid qualification and frozen-solver checkpoint.
All numerical quantities retain the existing annular test normalization.

## 1. What this stage changes

The previous stage showed that source-only refinement leaves a bulk wave-profile error,
while uniform129/source8 already misses the combined force target at the initial instant.
This stage refines both, but grades only the cells touching the source. It does not change
the action, remove Gram modes, change the initial profile, or substitute pressure for the
actual material force. No public or full-GR claim follows from an initial-state check.

The source-cell cap4e-5 was selected before reading the new force results. Base129 is a
control; base257 resolves the wider wave profile more finely. A cap2e-5 control tests
whether the257 result survives further local refinement, rather than choosing a single
favourable cancellation. These are exploratory numerical choices, not a blinded experiment.

## 2. Exact finite-action force reduction

For scalar coordinates u and source coordinate b, write the wave kinetic Hessian as

    [[M, a], [a^T, d]],
    Q=d-a^T M^-1 a=integral K(w-P_h w)^2 dR >= 0,

where w=-c H is the mesh-transport field and P_h is its K-weighted projection into the
source-zero scalar space. This Q is the existing finite-action Schur complement, not a
new parameter. The prior stable inverse already computes it as a squared norm.

Let r_u,r_b be the time derivatives of the wave momenta with the accelerations held zero,
but with the ACTUAL live metric tangent retained. Let f_u,f_b be the wave covectors. Define

    J=f_b-r_b-a^T M^-1(f_u-r_u),
    I=partial_V p_dust=m N^2/(U^2 clock^3)>0,
    G=f_dust-r_dust.

On the scalar and source Euler equations,

    F_h=J-Q bddot,
    (I+Q) bddot=G+J,
    F_h=(I J-Q G)/(I+Q).                              (1)

This is an exact finite-action identity, conditional on the supplied consistent live
geometry tangent. It does not derive that tangent independently, and is not a new
covariant parent action. The implementation checks(1) against the existing differentiated
field momentum, not against a newly defined force.

For any chosen local wave-driving coefficient B, define D=G/I+B and R=J+Q B. Then

    F_h=[-Q D+R]/(1+Q/I),
    |F_h| <= [Q |D|+|R|]/(1+Q/I).                    (2)

The bound avoids relying on cancellation between the two signed terms. R is computable
from the unchanged action; introducing its name does NOT prove it is small. The earlier
conforming-lift ledger independently resolves the spatial and Gram contributions.

## 3. Derive the source mass, rather than guess its refinement scale

The exact P2 mass matrix on a unit-coefficient element of length h is

    h/30 [[4,2,-1],[2,16,2],[-1,2,4]].

Eliminating its midpoint gives the endpoint matrix h/24 [[3,-1],[-1,3]]. On a uniform
half-line the positive interior tail Schur pivot d satisfies

    d=h/4-(h/24)^2/d,
    d=h(1/8+sqrt(2)/12).

Hence the source-end mass Schur complement is EXACTLY

    sigma_halfline=h/8-(h/24)^2/d=h/(6 sqrt(2)).       (3)

For arbitrary positive finite element lengths h_0,...,h_(n-1), ordered away from the source,
the corresponding constant-coefficient graded mass is obtained without a fit:

    d_n=h_(n-1)/8,
    d_j=(h_(j-1)+h_j)/8-(h_j/24)^2/d_(j+1),
    sigma=h_0/8-(h_0/24)^2/d_1.                     (4)

For a single element sigma=h/9. The two source sides add. These are mass/projection
identities; the half-line formula is not substituted unmodified into a graded live system.
For the actual variable K, the runner separately evaluates the weighted mass Schur
complement from the original action matrix.

With a locally linear initial field H=k, the source projection inertia is
Q_source=k^2 sigma_K. The constant-coefficient frozen corner fixture gives

    F_corner=-Q_source D/(1+Q_source/I).              (5)

For the live field this is a leading local prediction, NOT an exact total-force formula:
outer profile errors, Gram work and variable-coefficient remainders remain. The graded
recurrence and a directly assembled coupled frozen-action solve agree to roundoff,
including the source-inertia denominator. Setting Q=0 fails the negative control.

There is also a useful conditional upper bound. The source Schur complement minimizes
the weighted squared norm among functions with unit source value. A trial function
supported on the two adjacent elements, with midpoint coefficient-1/8 relative to each
source-end shape, has unweighted squared norm(h_left+h_right)/8. Therefore

    sigma_K <= K_max,adjacent (h_left+h_right)/8.      (6)

This gives a local mesh-budget criterion when K_max,adjacent and D are controlled.
It does not bound R or the subsequently evolved force. No sampled maximum of K is silently
promoted into an interval-certified supremum.

## 4. Connect the corner coefficient to the live geometry

Set C=R^2 N U, K=R^2/(N U), s=N U, and x=R-b(t). Writing phi=k x+u gives, EXACTLY,

    u_tt-2V u_tx-(s^2-V^2)u_xx
        =(bddot+C_R/K+V K_t/K)(k+u_x)-(K_t/K)u_t.    (7)

Here C_R and K_t are Eulerian partial derivatives. Thus the initial local driving term is
B=C_R/K+V K_t/K, not simply the flat spherical2/R. Freezing the leading coefficients
and writing D0=k(bddot_0+B_0), the convected half-line solutions inside their fronts are

    u_left=D0/2 [t^2-(t+x/(s+V))^2],
    u_right=D0/2 [t^2-(t-x/(s-V))^2].                (8)

Outside each front u=D0 t^2/2. Values and first derivatives match, and the source trace
vanishes. For |V|<s, inserting the one-sided slopes into the CONTINUUM pressure law gives

    dF_continuum/dt at0+ = -2 b^2 k D0.              (9)

This is the frozen leading corner prediction, not a uniform remainder theorem for the
live PDE. It recovers the earlier flat-background result-4 b k^2 when bddot_0=0,
K_t=0 and C_R/K=2/b. The already-derived flat result is retained, not counted as a new
discovery. Equation(7) identifies how the live geometry and source acceleration enter.

Symbolic and frozen-action checks:
`scripts/derive_annular_P2_source_corner_scale_20260919.py`,
`source-intake/navier-stokes/20260914/annular-P2-source-corner-scale-attempt01/status.json`.

## 5. Make sure grading does not secretly change the action

`scripts/annular_P2_graded_source_20260919.py` bisects only the currently source-adjacent
cells, preserving the base Gram sampling and the existing pulled-back action. At fixed
base grid the old P2 space embeds in the new space. We check the action, momenta, scalar
and source covectors, and lifted Gram operator under that embedding.

Three failed validator executions are preserved. Attempt01 mishandled the reference
branch's empty Gram matrix. Attempt02 exposed inaccurate embedding coefficients from
rounded tiny-cell midpoint coordinates. Attempt03 showed that this Windows NumPy's
longdouble did not improve the arithmetic. Exact rational evaluation at the natural FE
nodes in `scripts/annular_P2_graded_embedding_exact_20260919.py` fixes the interpolation.
No tolerance was loosened. The final action error is<=5.96e-15, the Gram-operator pullback
error<=3.56e-15, and the scalar-covector pullback error<=1.52e-10 across both branches at
base65/129/257. These are validation repairs, not new physics or erased failed attempts.

Final preflight: `scripts/verify_annular_P2_graded_source_v4_20260919.py`,
`source-intake/navier-stokes/20260914/annular-P2-graded-source-algebra-attempt04/status.json`.

## 6. Initial force results and cost decision

The force target is unchanged: absolute
error<=2e-7 AND<=0.005*5.401196245463084e-6=2.700598122731542e-8. An initial pass does not
upgrade any evolved peak-force, waveform, observational, or GR gate.

|Base grid / source cap|scalar nodes|reference initial force error|MTS initial force error|both pass initial target?|
|---|---:|---:|---:|---|
|129 /4e-5|304|-1.712528954e-8|+3.256826391e-8|No|
|257 /4e-5|554|-6.668881801e-9|+2.020690932e-9|Yes|
|257 /2e-5|558|-2.631003609e-9|+6.058549842e-9|Yes|

The coarse MTS failure is retained. MTS's absolute error increases under the last local
refinement, rather than decreasing monotonically. That is not hidden: reducing a negative
source term exposes the remaining positive drive. More importantly, the numerical
non-cancellation bounds in(2) pass for both257 grids. At cap4e-5 they are9.4835e-9 for
reference and1.8173e-8 for MTS, below2.7006e-8 without cancellation between the two terms.
These are evaluated initial-state bounds, not interval-certified uniform bounds in time.
This is not an evolved force pass.

The source mass law is quantitatively useful. For257/cap4e-5 it predicts a source-near
contribution about-8.0757e-9. Halving the cap predicts-4.0379e-9. The constant-coefficient
graded mass differs from the full weighted source mass by only1.8e-11 fractionally for
the first grid, but the total action force still contains the separate remainder R.
Equation(1) agrees with direct field-momentum differentiation to better than5e-16 in
these initial tests; the conforming force identity closes to2.72e-11 on the257 grids.

There is an additional mechanism check, not a replacement trajectory: evaluating(9)
from the refined initial geometry predicts the continuum right-hand force slope
-1.344912935e-3. The independent continuum solver gives F(.001)/.001=-1.345164252e-3,
a0.0187% difference. Over its five saved times through.004, the leading straight-line
prediction differs by at most about2.155e-8. No coefficient is fitted to those forces.
This supports the curved-corner mechanism; it is not a remainder theorem or a claim
that the evolved MTS force has already reached the continuum result.

`scripts/probe_annular_P2_joint_refinement_20260919.py` also assembles the actual frozen
scalar mass/stiffness pencil and checks it against the original action covector. Every
mode is retained. It derives the imaginary-axis stability interval from the installed
DOP853 tableau, rather than choosing an arbitrary time step.

The displayed wall-time estimates combine that FROZEN scalar frequency with a measured
live RHS cost. They ignore tolerance control, rejections, changing geometry and the full
coupled spectrum; they are warning indicators, not guaranteed runtimes or a theorem
about all adaptive integrators. No long explicit trajectory is launched solely because
the initial force is small.

For257/cap4e-5, the full-window cost indicators are about7.9hours for reference and
63.2hours for MTS. The cap2e-5 control raises them to about14.7hours and110.4hours.
Those estimates are enough to reject another blind full-window explicit run here.
The rapid modes have not been removed to make the estimate look better.

All six rows, the signed decomposition, bounds and source paths are recorded in
`source-intake/navier-stokes/20260914/annular-P2-joint-refinement-initial-results.csv`.
Input evidence:
`source-intake/navier-stokes/20260914/annular-P2-joint-refinement-129-cap4e-05-attempt01/status.json`,
`source-intake/navier-stokes/20260914/annular-P2-joint-refinement-257-cap4e-05-attempt01/status.json`,
`source-intake/navier-stokes/20260914/annular-P2-joint-refinement-257-cap2e-05-attempt01/status.json`.

## 7. Solver feasibility control and next step

The separate frozen-modal check COMPLETE passes13 checks. That fixture holds the geometry and source
position fixed and sets mesh/source velocity to zero. It is NOT the actual moving-source
trajectory. Its purpose is to test whether all fast scalar modes can be propagated
without discarding them, while preserving the frozen action energy and matching a
direct physical-space integration over a short interval.

For K_scalar v=omega^2 M v, with M-orthonormal eigenvectors, each frozen mode has the
exact solution q(t)=q0 cos(omega t)+p0 sin(omega t)/omega. Every mode is retained.
The test deliberately excites the highest mode, not merely a smooth low-frequency field.
It compares against a direct physical-space DOP853 solve over five shortest periods.
Relative energy-norm differences are3.061e-11(reference) and7.771e-11(MTS).
Across the five frozen times through.004, physical-energy relative errors are at most
4.070e-12 and2.131e-10. The highest-mode energy is preserved rather than damped away.

Factorization takes about0.08seconds and evaluation at the five times takes under0.005seconds
in this fixed554-mode fixture. These times EXCLUDE live geometry/source updates and do not
forecast the full nonlinear integrator's speed. The eigensystem normwise backward errors
are<=1.62e-13; the worst separately reported relative per-mode residual reaches9.56e-6
in the ill-conditioned MTS pencil. Backward accuracy is not silently relabelled uniform
relative eigenvalue accuracy. The independent physical-space comparison and energy checks
provide the operational short-interval controls.

Evidence: `scripts/verify_annular_P2_frozen_modal_step_20260919.py`,
`source-intake/navier-stokes/20260914/annular-P2-frozen-modal-step-attempt01/status.json`.

NEXT: derive a full canonical variation-of-constants step, retaining the exact remainder
F_live(z)-A_frozen z. Include source motion, the full Gram force and fresh constrained
geometry in F_live; verify the split reproduces the original RHS before taking steps.
Then qualify a very short nonlinear interval under step refinement and the original
mass/current/force diagnostics. Do not present this frozen scalar propagator, or the
older flat frozen-tangent prediction, as that completed nonlinear solver. Do not spend
another night on brute-force refinement whose measured stability cost is already excessive.

Full local GR, an unrestricted covariant parent, PPN/black-hole claims, uniform nonlinear
convergence, and the original failed full-horizon force gates remain open. The new local
mass law and initial-grid qualification do not settle those questions. No GitHub action,
subagent, galaxy edit, or formalization-workbench edit occurs in this stage.
