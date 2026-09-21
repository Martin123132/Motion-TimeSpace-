# GR-path projection and the coupled consistency-force defect

Private continuation of `DERIVATION-20260916-original-action-joint-refinement.md`.
This is the original prescribed-flat-background, spherical moving-source control,
not the full GR limit, a live-metric derivation or an observational result.
No action, initial function, Gram row or physical acceptance gate is changed.

## 1. Construct the missing reference path, not another missing-input ledger

The characteristic reference stores W=partial_t(phi) and H=partial_R(phi),
not phi. Its moving source satisfies phi(t,b(t))=0. Each side has a fixed
coordinate xi in [0,1], length L_-=b-R_inner or L_+=R_outer-b, and grid
displacement s_-=xi or s_+=1-xi. The finite source-fitted nodes have these
same, time-independent xi coordinates. The scalar therefore has the unique
source-anchored reconstruction

\[
 U_-(\xi)=L_-\int_1^\xi H_-(\zeta)d\zeta,
 \qquad U_+(\xi)=L_+\int_0^\xi H_+(\zeta)d\zeta.
\]

The actual Chebyshev polynomial stored by the reference is integrated, not a
finite difference of noisy snapshots. No arbitrary side-dependent integration
constant remains. The projected nodal rate is

\[
 v=W+V sH,\quad V=\dot b=p/\sqrt{S^2+p^2},\quad
 z_h=[U,b,v,V,\tau].
\]

This reconstruction reads the GR reference and the fixed spatial mesh only;
it does not read either future finite-action trajectory.

## 2. Differentiate the actual moving reference

Let overdots denote the reference ODE derivative at fixed xi. Its eliminated
boundary characteristics must also be differentiated: holding them fixed would
silently discard the moving-source reflection law. The implementation takes
their analytic directional derivative through unpack(), with complex arithmetic,
and then uses the chain rule

\[
 \dot U=\dot L\int_{\xi_*}^{\xi}H d\zeta+
 L\int_{\xi_*}^{\xi}\dot H d\zeta,
 \qquad
 \dot v=\dot W+\dot V sH+V s\dot H,
\]
\[
 \dot V=F_{GR}/\mu,\qquad \mu=S(1-V^2)^{-3/2},
 \qquad \dot\tau=\sqrt{1-V^2}.
\]

In the exact continuum, compatibility and W(b)+VH(b)=0 imply dot(U)=v.
The characteristic semidiscretization need not obey this identity exactly.
We retain k=v-dot(U) as a measured kinematic component of the first-order
defect; we do not silently set it to zero. This distinction also prevents
calling an incompatible projected path an exact Euler-Lagrange trajectory.

`scripts/annular_GR_projection_20260916.py` implements these equations.
`scripts/qualify_annular_GR_projection_20260916.py` checks a known moving
polynomial, whole-projection complex derivatives, central directional
derivatives, independent sampling, independent Gaussian integration and the
moving Dirichlet condition at degrees384/512/768 and meshes257/513/1025.
Its qualification is an implementation test, not proof of continuum accuracy.

## 3. Derive the coupled source-force defect

Use the unchanged original Lagrangian

\[
 L_h=\tfrac12v^TMv+Vv^TAU+\tfrac12V^2U^TBU
 -\tfrac12U^TKU-S\sqrt{1-V^2}.
\]

Here K contains the full original lifted Gram term in MTS and none in the
finite reference. Define c=AU, I=mu+U^TBU, s_H=I-c^TM^{-1}c. The original
equations have acceleration right-hand sides r_U,r_b:

\[
 M\dot v+c\dot V=r_U,\qquad c^T\dot v+I\dot V=r_b.
\]

Evaluate those right-hand sides on the reconstructed GR state, and subtract
the reconstructed accelerations:

\[
 R_U=r_U-M\dot v_{GR,h}-c\dot V_{GR},\quad
 R_b=r_b-c^T\dot v_{GR,h}-I\dot V_{GR}.
\]

Eliminating the field acceleration gives the exact algebraic identity

\[
 \boxed{F_h(z_h)-F_{GR}={\mu\over s_H}
 \left(R_b-c^TM^{-1}R_U\right).}
\]

Thus the field-equation residual drives the source through the same coupled
inertia as the original action. A small standalone source covector does not
by itself guarantee a small source-force discrepancy. The two terms are kept
separately, with their signs and cancellation. R is an acceleration-equation
covector defect; because k can be nonzero, it is not mislabeled as the entire
canonical Euler-Lagrange residual along the projected curve. The actual
first-order defect is r=F_h(z_h)-dot(z_h), including k.

`scripts/derive_annular_GR_projection_residual_20260916_v2.py` evaluates the
full 81-time defect at all three meshes and reference degrees. Independent
original quadrature/canonical-momentum differentiation checks its covectors.
The first attempt's list-versus-array reporting error is preserved separately;
no equation or tolerance changed in v2.

## 4. Accumulated response is a different question

For the actual finite trajectory y_h, define e=y_h-z_h. Exactly,

\[
 F_h(y_h)-F_{GR}=
 \underbrace{F_h(z_h)-F_{GR}}_{\text{consistency force}}+
 \underbrace{F_h(y_h)-F_h(z_h)}_{\text{trajectory response}}.
\]

This ordered decomposition is not a corrected force prediction. Reading y_h
to evaluate its second term is retrospective. Likewise, evaluating the force
directional derivative on a measured state error is not a prediction of that
state error. `scripts/analyze_annular_GR_projection_residual_20260916.py`
records this distinction, oracle-resolution sensitivity, the first-order
force remainder, and the separate field/source/clock contributions.

The next genuinely predictive problem is instead

\[
 \dot\eta=DF_h(z_h)\eta+r,\qquad
 \eta(0)=y_h(0)-z_h(0),
\]
\[
 \delta F_{pred}=F_h(z_h)-F_{GR}+DF_h^{force}(z_h)\eta.
\]

Inputs are the independent GR path, its derivative, the fixed action, and
the original initial data. Future finite states are excluded until validation.
Nonlinear error obeys the full remainder equation, not a presumed smallness
axiom. The present 81 output times cannot automatically be treated as a
qualified continuous forcing interpolation for the stiff system; reference
reconstruction resolution must first be tested.

## 5. An exact finite-amplitude remainder law, not just a fitted slope

At fixed source position and velocity, let x=(U,v). The force has the form

\[
 F(x)=\mu N(x)/d(U),\qquad
 d(U)=\mu+U^TCU,\quad C=B-A^TM^{-1}A,
\]

where N is homogeneous quadratic in x. Its explicit form follows from the
acceleration right-hand sides in section3; the executable implementation is
`scripts/derive_annular_rational_force_remainder_20260916.py`.

The kinetic quadrature provides a useful non-assumed lower bound. If P and Q
are the nodal shape and grid-motion evaluation matrices, with positive
quadrature weight W, then M=P^TWP, A=P^TWQ and B=Q^TWQ. Hence

\[
 C=Q^TW^{1/2}(I-\Pi)W^{1/2}Q\succeq0,
 \quad \Pi=W^{1/2}PM^{-1}P^TW^{1/2},\quad d(U)\ge\mu>0.
\]

This requires an invertible finite mass matrix, positive map Jacobian and
timelike source, as in this control. It is a kinetic Schur-complement result,
not a global-in-time stability theorem.

For a finite field/rate displacement e, write exactly
N(x+e)=N0+N1+N2 and d(U+e_U)=d0+d1+d2. N1,d1 are linear directional
terms, N2=N(e), d2=e_U^TCe_U. With F0=mu*N0/d0 and
ell=mu*(N1*d0-N0*d1)/d0^2,

\[
 F(x+e)-F0-\ell=
 {\mu N2-F0\,d2-\ell(d1+d2)\over d0+d1+d2}.
\]

Consequently its absolute value is bounded by

\[
 |N2|+{|F0||d2|+|\ell|(|d1|+|d2|)\over\mu}.
\]

This is an analytic finite-amplitude bound, not a quarter-ratio extrapolation.
The test evaluates it on the observed field/rate differences; it does not
pretend those differences have been predicted independently. The source
position/velocity change is retained as a separate exact difference, rather
than included in a bound whose proof holds only at fixed source geometry.

## 6. Full-duration finest time control

The original1025/8 fullT=.4 run is repeated for both branches with tolerances
2e-12/2e-14 and half the prior spectral maximum step. All original modes and
accepted .05 chunks are retained. `scripts/run_annular_joint_refinement_20260916_v2.py`
changes only the expired hard-coded safety deadline into an explicit input
and records the active spectral history. It does not change the evolution.

## 7. Results and next safe target

The projection qualification passes64 implementation checks. Moving-polynomial
state error is at most2.06e-15; its derivative error at most2.18e-16.
Independent Gaussian integration agrees within1.53e-16. The residual producer
passes77 checks, retrospective analysis72, and rational remainder derivation36.
These249 checks are NOT249 physical validations of MTS.

At reference degree768, the retained kinematic mismatch is at most4.595e-9.
The maximum original-covector cross-check error is1.411e-13 and the force-defect
identity error2.575e-18. These demonstrate implementation agreement, not an
accuracy certificate for the continuum GR reference.

### What actually drives the discrepancy

At t=.21 on the1025/8 mesh, using reference degree768:

|Branch|Consistency force|Trajectory response|Total force error|
|---|---:|---:|---:|
|finite reference|+1.73607e-11|-1.60348e-7|-1.60330e-7|
|MTS|+9.46527e-6|-8.54458e-6|+9.20686e-7|

For MTS the consistency force itself consists of source-covector-1.44692e-9
plus field-acceleration feedback+9.46671e-6. Its source-cell feedback is
+9.84039e-6 and the rest of the field contributes-3.73674e-7. Here source
cell means the original bulk cell containing the anchor, not a fitted window.
The subsequent field-displacement response dominates the retrospective
trajectory term; clock force dependence is zero in this autonomous control.
This directly locates a source-trace/coupled-field mechanism. It does NOT
justify deleting the Gram action or declaring its direct term unphysical.

The first-order force expansion's maximum retrospective remainder is:

|Mesh/splits|Reference|MTS|
|---|---:|---:|
|257/8|5.19931e-10|5.35760e-7|
|513/8|3.90187e-11|2.11151e-8|
|1025/8|6.56376e-12|3.24976e-9|

The measured half-displacement remainder ratio is approximately1/4. More
substantively, the exact fixed-source rational bound gives maxima5.35802e-7,
2.11158e-8 and3.24977e-9 for MTS at the same three meshes. The separately
retained source-position/velocity force contribution is at most5.486e-12 on
the finest MTS mesh. Floating evaluation is not an interval-arithmetic proof;
the analytic identity and inequality hold under section5's stated assumptions.
None of these retrospective numbers predicts the future state-error amplitude.

### Important sensitivity, not a concealed pass

The finest MTS projected force changes by6.27823e-7 between degrees384 and768,
and5.09538e-7 between512 and768, although the raw GR force changes much less.
The stiff force functional amplifies small projection differences. Therefore
one cannot assign an individually resolved2e-7 budget to these direct
consistency terms. Their counterpart response terms compensate when the
known trajectory is used. Resolution must be tested on the whole independent
predictor, not by treating a decomposition component as a physical observable.

The best next constructive target is the causal coupled error evolution in
section4 on513/8 first, BOTH branches, fullT=.4, followed by1025/8.513/8 already
has a retrospective nonlinear force remainder around2.1e-8, below the2e-7
target;257/8 does not. Use a differentiable reconstruction of the GR path and
its own exact derivative, carry any reconstruction discrepancy, retain the
nonzero initial projection error, and compare reference/time reconstruction
resolutions. Save predictions before opening future finite trajectories.
Do not change the action, subtract the observed error, or demand a pointwise
tiny forcing term when cancellation is part of the coupled evolution.

### Finest full-duration time control completed

Both original1025/8 trajectories now have their own tighter fullT=.4 control:

|Branch|Maximum state change|Maximum force change|
|---|---:|---:|
|finite reference|2.69927e-13|8.51193e-14|
|MTS|1.59809e-12|5.84945e-12|

These differences are far below the2e-8 time-control tolerance and the2e-7
physical comparison threshold. This particular force discrepancy is not
removed by halving the already stiffness-limited step and tightening the
time integrator. It does not eliminate spatial or GR-reference uncertainty.
The reference used2,909,096 RHS evaluations and MTS4,673,492. The original
run stopped safely with MTS atT=.3; the immutable resumed run verified hashes,
copied the completed reference without re-evolving it, and computed only the
last two MTS chunks. Same initial state, action and step rule throughout.

The full comparison validator passes57 checks with all six tighter controls
present (both branches at257/8,513/8,1025/8). The old failed legacy state
replay flag remains false. All original whole-trajectory force failures also
remain false: finest MTS peak9.20686e-7 and reference peak2.16929e-7 still
exceed2e-7. Endpoint success is not whole-trajectory success.

### Saved evidence

- `source-intake/navier-stokes/20260914/annular-GR-projection-qualification-attempt01/status.json`
- `source-intake/navier-stokes/20260914/annular-GR-projection-residual-attempt02/status.json`
- `source-intake/navier-stokes/20260914/annular-GR-projection-analysis-attempt01/status.json`
- `source-intake/navier-stokes/20260914/annular-rational-force-remainder-attempt01/status.json`
- `source-intake/navier-stokes/20260914/annular-joint-tight1025-attempt01/status.json` (preserved safe pause)
- `source-intake/navier-stokes/20260914/annular-joint-tight1025-resumed-attempt01/status.json` (complete)
- `source-intake/navier-stokes/20260914/annular-joint-validation-attempt03/status.json`

316 successful current implementation/control checks; one new reporting
failure retained,23 failed attempts in the inherited history. The main
derivation, numerical evidence and executed sources are sealed by
`scripts/seal_annular_GR_projection_20260916.py`; the live resume is a pointer,
not a mutable substitute for those records. No GitHub or subagents, and no
changes to the protected formalization workbench.
