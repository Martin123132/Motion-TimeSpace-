# Initial-corner response and a parameter-free frozen-action prediction

2026-09-17. Private continuation of
`DERIVATION-20260917-material-impulses-and-instantaneous-force-bridge.md`.

## 1. What has actually advanced

We have derived an exact forced, convected half-line solution for the leading
continuum corner problem. It reproduces the previously derived right-hand
force slope and its field expansion agrees with the full characteristic
reference under shrinking-time tests.

Separately, we derive the affine frozen tangent response of the ACTUAL
finite action, retaining its coupled source inertia and every lifted-Gram
term. This produces a parameter-free early-force prediction. We freeze both
the linearized force and the original force evaluated on that approximate
motion before loading the saved comparison trajectories in this stage.

At the five original saved times0,.005,.01,.015,.02, the latter prediction
leaves at most6.691% of the original early-window maximum force discrepancy
for MTS1025, and1.741% for reference1025. The corresponding513 fractions
are3.943% and3.949%. These are ratios of maximum absolute residuals, NOT
percentages of variance explained or a claim about every instant.

This supports the usefulness of a short-time finite-action response
calculation. It does not prove that the initial corner alone causes every
error: the frozen calculation retains the entire initial profile and action.
It does not remove any original force discrepancy. All four old full-horizon
sampled peak-force gates remain failed, and the full GR limit remains open.
The geometry is prescribed flat; no live Einstein/parent coupling is derived.

## 2. Derive the continuum inner problem

The original locally linear profile has slope k=.01, source radius b0=6.03
and speed V0=.06. In a moving coordinate x=r-b(t), write

    phi(t,r)=k x+u(t,x).

The flat spherical wave equation is phi_tt=phi_rr+2phi_r/r. Applying the
chain rule, with V=bdot and a=Vdot, gives the EXACT local equation

    u_tt-2V u_tx-(1-V^2)u_xx
        =a(k+u_x)+2(k+u_x)/(b+x).                    (1)

The source condition is u(t,0)=0. Initial u and u_t vanish where the
initial profile is exactly linear. The source force initially vanishes,
but the bulk/source second-derivative compatibility defect is2k/b0.

Introduce a small length h, x=h y, t=h tau, u=h^2 zeta. On bounded
(tau,y) sets, the candidate leading equation from(1) is

    zeta_tautau-2V0 zeta_tauy-(1-V0^2)zeta_yy=C,
    C=2k/b0,                                        (2)

with zero initial values and zeta(tau,0)=0. Terms involving curvature
variation, h zeta_y and the source acceleration enter at higher order on
this initial scale. For the reference source, a(0)=0 and its smooth
one-sided ODE gives a(h tau)=O(h). This does not assume the same bound
for the full evolved finite MTS action.

Equation(2), not the unscaled nonlinear problem, has the following EXACT
solution. With [q]_+=max(q,0),

    zeta_-(tau,y)=C/2 [tau^2-(tau+y/(1+V0))_+^2], y<=0,
    zeta_+(tau,y)=C/2 [tau^2-(tau-y/(1-V0))_+^2], y>=0. (3)

Outside the emitted fronts, zeta=C tau^2/2. The fronts are
y=-(1+V0)tau and y=(1-V0)tau. Inside each front, the subtracted term is
a homogeneous travelling wave. At the fronts, its value and both first
derivatives vanish, so(2) also holds distributionally without a spurious
delta source. Equation(3) satisfies the boundary and initial conditions.

Its source-side slopes are

    zeta_y,-=-C tau/(1+V0),
    zeta_y,+=+C tau/(1-V0).                          (4)

Using the CONTINUUM pressure force, not substituting it into the discrete
source equation, gives

    F_ref(h tau)
      =b0^2(1-V0^2) k h (zeta_y,--zeta_y,+)+O(h^2)
      =-4 b0 k^2 h tau+O(h^2).                      (5)

Thus the initial-force slope-.002412 is the boundary response to the
nonzero spherical bulk forcing, not an arbitrary missing constant.

### Check against the full characteristic field

We evaluate the previously qualified characteristic field at
r=b(h tau)+h y, y in[-8,8] on257 fixed scaled locations, and
tau=.5,1,2,4,6.4. No finite nonlinear trajectory is evolved for this check.

|h corresponding to base nodes|max error in (phi-k h y)/h^2 versus(3)|that error divided by h|
|---|---:|---:|
|513|4.02942707e-4|.12894167|
|1025|2.01815014e-4|.12916161|
|2049|1.00993620e-4|.12927183|
|4097|5.05182968e-5|.12932684|

The observed remainder is consistent with an O(h^3) unscaled field
remainder on these bounded inner sets. This numerical table is not an
interval proof of its uniform constant. The exact assertion proved here
is the principal half-line solution(3), together with its pressure slope.
Matching it to the original finite action remains a separate question.

The derivation must NOT discard the MTS term on this scale. For a P2
correction h^2 zeta, the lifted factor is h^2 L_theta zeta:
its hinge vector scales as h, and its jump trace as1/h. Its potential
weight is O(1/h), so the resulting field force is O(h), the SAME order
as the inner inertial term M u_tt. The lifted-Gram response can therefore
change the leading mesh-scale dynamics even though it is consistent for
smooth macroscopic fields. The full finite calculation below keeps it.
Here L_theta denotes the existing rescaled factor, not a newly chosen
operator or a proved infinite-lattice limit.

## 3. Derive the finite prediction without changing the action

Let z contain field/source coordinates, their velocities and the passive
clock. The exact finite-action flow and material force are

    zdot=F_h(z),   f_h(z)=mu(V) Vdot,
    mu(V)=m/(1-V^2)^(3/2).

At the unchanged initial state z0 define

    a0=F_h(z0),   J0=DF_h(z0),   g0=Df_h(z0).

The frozen affine tangent problem is

    ydot=a0+J0 y,   y(0)=0,
    y(t)=integral_0^t exp((t-s)J0) a0 ds
        =t phi1(tJ0) a0.                            (6)

The integral defines phi1 even if J0 is singular. Two predictions are
fixed in advance:

    f_linear(t)=f_h(z0)+g0 y(t),
    f_evaluated(t)=f_h(z0+y(t)).                     (7)

The latter uses the ORIGINAL force observable on the approximate state;
it is not a fitted correction to the original data or a new physical
trajectory. It retains observable nonlinearity but still omits dynamical
nonlinearity beyond the frozen tangent evolution.

The linear-force slope has the exact representation

    fdot_linear(t)=g0 exp(tJ0) a0.                   (8)

Consequently a nearly zero initial value g0 a0 does not force a zero
subsequent response. Mesh-frequency modes can turn the force rapidly.
A time polynomial truncated before those modes respond would miss them.

This is a Taylor approximation of the coupled Euler flow about a
nonstationary initial state. It is NOT claimed to be the original
nonlinear evolution, a separately derived parent theory, or a globally
energy-conserving replacement action.

### Retained source coupling

The original kinetic Hessian remains

    Kkin=[[M,A U],[(A U)^T,mu+U^T B U]],
    p_b=p_m+W^T A U+V U^T B U.

For every tangent direction, the differentiated right side is solved
through the same coupled kinetic Schur complement. No field momentum,
source acceleration response, or lifted-Gram row is set to zero. Analytic
matrix-free J0 products agree with complex directional differentiation
of the original flow and with the independently qualified transpose.

### Scaling is only a similarity transformation

For t=h tau, let S multiply every coordinate displacement and clock
displacement by h and leave velocity displacements unscaled. Set y=S eta.
Then

    eta_tau=h S^-1 a0+B_h eta,
    B_h=h S^-1 J0 S.                                (9)

We solve(9), retaining its actual source-cut phase and eight subdivisions.
It is exactly equivalent to(6) and does not assume B_h already has a
uniform infinite-grid limit. Banded mass solves and sparse factor products
avoid dense Hessians. No nonlinear finite trajectory is rerun.

## 4. The exact error identity says what is still owed

For the exact nonlinear displacement d=z-z0, define

    R_F(d)=F_h(z0+d)-a0-J0 d,
    R_f(d)=f_h(z0+d)-f_h(z0)-g0 d.

Variation of constants gives the EXACT identity

    f_h(z(t))-f_linear(t)
       = integral_0^t g0 exp((t-s)J0) R_F(d(s)) ds
           +R_f(d(t)).                              (10)

The finite comparison below measures the combined remainder only at saved
times. It does not uniformly bound either term of(10). In particular we
do not integrate a sparsely sampled remainder and call that a proof.

With f_evaluated, observable linearization is removed, but the remaining
error is f_h(z0+d)-f_h(z0+y), which still depends on the true dynamical
remainder. That distinction prevents a good early prediction from being
misreported as a full nonlinear pointwise-convergence theorem.

## 5. Frozen protocol, controls and fair saved comparison

Both branches at513/1025 receive the same physical prediction horizon.02
and the same five comparison times0,.005,.01,.015,.02. Dense frozen samples
also cover tau in[0,6.4]. There are no fitted amplitudes, damping, phase
shifts or altered initial data. The actual phases are about.6 and.2.

The complete prediction pack is timestamped before this stage loads the
saved nonlinear trajectories. This is not a blind prospective experiment:
earlier work has already examined those trajectories. The safeguard here
is a parameter-free calculation and a fixed comparison protocol, not a
claim of previously unseen data.

Two initial numerical-control attempts failed and are retained:

- attempt01: reference513 standard/tight force difference7.91397e-10;
- attempt02: MTS1025 standard/tight force difference3.12061e-10.

Both exceed the unchanged2e-10 numerical control threshold. We tightened
tolerances/steps rather than relaxing that threshold or the old physical
gate. Attempt03 completes all four cases. Its force control differences
range from7.92e-14 to1.252e-11. Its force-RATE control is less sharp,
reaching3.7791e-6; do not import the force control as a derivative bound.

### All comparison outcomes, including the negative one

Here E is the maximum original finite-versus-continuum force error over
the FIVE initial-window times; R is the maximum prediction-versus-finite
force remainder at those same times.

|Case|E|R_linear|R_linear/E|R_evaluated|R_evaluated/E|
|---|---:|---:|---:|---:|---:|
|reference513|2.17003680e-7|4.61103154e-8|.21249|8.56868410e-9|.03949|
|MTS513|1.09076420e-6|3.30234412e-8|.03028|4.30091307e-8|.03943|
|reference1025|1.50174522e-7|4.42207539e-8|.29446|2.61390883e-9|.01741|
|MTS1025|3.08314551e-7|6.13490462e-8|.19898|2.06278479e-8|.06691|

The protocol's descriptive threshold R/E<=.25 is NOT a physical gate.
The strictly linear prediction misses it for reference1025 (.29446).
All evaluated predictions meet it, but evaluated is NOT uniformly better:
MTS513's remainder increases from3.30e-8 to4.30e-8. Both variants were
defined before comparison; neither negative result is discarded.

At t=.01 the coarse MTS actual force error is1.09076420e-6 and the
linear prediction is1.09938254e-6. The fine MTS error changes sign there:
-1.60576583e-7 actual versus-1.57953511e-7 predicted. Capturing this
phase-dependent sign change is more informative than fitting an unsigned
error envelope. It still does not certify intermediate-time extrema.

The ORIGINAL full-horizon sampled peak errors remain

    reference513 5.48253059e-7 FAIL,
    reference1025 2.31362091e-7 FAIL,
    MTS513       3.67969181e-6 FAIL,
    MTS1025      9.13531208e-7 FAIL.

The threshold remains2e-7. Predictions are not subtracted from these tests.
All times and forces use the existing benchmark units, not SI calibration.

## 6. Evidence and next derivation

Sources:

- `scripts/annular_frozen_initial_layer_20260917.py`
- `scripts/run_annular_frozen_initial_layer_20260917.py`
- `scripts/run_annular_frozen_initial_layer_v2_20260917.py`
- `scripts/run_annular_frozen_initial_layer_v3_20260917.py`
- `scripts/qualify_annular_frozen_layer_predictions_20260917.py`
- `scripts/qualify_annular_corner_inner_solution_20260917.py`

Evidence:

- `source-intake/navier-stokes/20260914/annular-frozen-initial-layer-attempt01/status.json` — retained control failure.
- `source-intake/navier-stokes/20260914/annular-frozen-initial-layer-attempt02/status.json` — retained control failure.
- `source-intake/navier-stokes/20260914/annular-frozen-initial-layer-attempt03/status.json` —24 successful implementation checks.
- `source-intake/navier-stokes/20260914/annular-frozen-layer-comparison-attempt01/status.json` —41 successful implementation checks, including explicit diagnostic negatives.
- `source-intake/navier-stokes/20260914/annular-corner-inner-solution-attempt01/status.json` —16 successful implementation checks.

There are81 successful current implementation checks, not81 physics passes.
Together with the26 inherited failures, the two new control failures bring
the retained failed-attempt total to28.

The next useful target is now more specific: derive the phase-resolved
rescaled finite source/field operator and its MATERIAL-force functional,
not just the continuum pressure trace. The lifted-Gram response survives
at leading inner order and must be retained. Seek a uniform short-time
bound for the response and the signed remainder in(10), rather than
assuming the tested tangent accuracy persists as t/h grows.

That would address the starting layer. It still leaves the later
envelope-transition region around.19-.21 and the full interval[0,.4].
Do not spend a new full-grid evolution merely to reproduce the five
comparison points, promote averaged force to peak force, or claim that a
prescribed-flat initial-layer result completes the GR connection.
