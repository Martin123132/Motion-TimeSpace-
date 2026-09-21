# Material impulses and the instantaneous-force bridge

2026-09-17. Private continuation of
`DERIVATION-20260917-coupled-Galerkin-defect-and-flat-nonlinear-limit.md`.

## 1. Actual result and limits

The saved finite trajectories give improving material impulse and fixed-window
average-force errors for BOTH branches. We derive an exact sufficient criterion
for upgrading uniform momentum convergence to instantaneous force convergence,
derive the reference force time derivative, and qualify the finite-action
force derivative in independent velocity and canonical coordinates.

There is also a concrete initial-corner result: for the unchanged locally
linear initial profile, the continuum right-hand force slope is exactly
-4 b0 k^2=-0.002412. The finite initial slopes on both branches are close to
zero on the finer tested meshes. This is consistent with a shrinking initial
layer, not proof that all subsequent discrepancies are an initial-layer effect.

These are results for the prescribed-flat spherical benchmark. They do not
derive live Einstein geometry, the full parent coupling, or the full GR limit.
Instantaneous force convergence remains unproved. All four previous sampled
peak-force gates still fail; no averaging window replaces those gates.
Times, forces and momenta below use the existing benchmark units, NOT seconds,
newtons or an independently calibrated physical detector resolution.

This turn uses saved trajectories and direct initial-state evaluations only.
There is no forward trajectory re-evolution, force fitting, damping, changed
initial profile, modified action, GitHub action or subagent.

## 2. Material momentum is the correct impulse observable

For source material mass m=.03, speed V, and material force F_m,

    p_m(V)=m V/sqrt(1-V^2),
    dp_m/dV=mu=m/(1-V^2)^(3/2),
    F_m=mu Vdot=dp_m/dt.                              (1)

The source's TOTAL canonical momentum also has a field contribution:

    p_b=p_m+W^T A U+V U^T B U.                       (2)

We do not identify p_b with p_m or omit its field term in the canonical
equations. Equation (1), not a trapezoid sum of sparsely sampled forces,
defines the material impulse for exact solutions.

Let e_p=p_m,h-p_m,reference. On any interval [s,s+d],

    integral_s^(s+d) (F_h-F_ref) dt=e_p(s+d)-e_p(s),
    |average force error| <= 2 ||e_p||_infinity/d.    (3)

For saved numerical endpoints, (3) is an endpoint diagnostic, with separate
tighter-time controls. Those controls are not certified enclosures of the
time integration. The maximum over 81 saved momentum values is not a
continuous-time supremum.

Before reading data we froze widths .025,.05,.1,.2,.4 and tested EVERY aligned
start on the original 81 saved times, spacing .005. There are respectively
76,71,61,41,1 windows. Both branches and both meshes use the same protocol.
The old 2e-7 peak-force scale is printed only as a diagnostic comparison;
no new smoothed-force acceptance criterion was invented after seeing results.

## 3. Saved-trajectory results

|Branch / base nodes|Maximum sampled momentum error|Old sampled peak-force error|
|---|---:|---:|
|reference / 513|9.60918452e-10|5.48253059e-7 FAIL|
|reference / 1025|1.94953971e-10|2.31362091e-7 FAIL|
|MTS / 513|1.08326544e-8|3.67969181e-6 FAIL|
|MTS / 1025|1.73648203e-9|9.13531208e-7 FAIL|

Maximum absolute average-force errors over ALL aligned windows:

|Width|reference513|reference1025|MTS513|MTS1025|
|---|---:|---:|---:|---:|
|.025|7.67653015e-8|9.20474972e-9|7.70325153e-7|1.22521562e-7|
|.05|2.12806850e-8|4.04094958e-9|2.20232773e-7|3.60384616e-8|
|.1|1.02454724e-8|2.33499650e-9|1.11318202e-7|1.82781421e-8|
|.2|5.43761821e-9|1.05704280e-9|5.47023075e-8|9.71932228e-9|
|.4|3.78025322e-10|1.64920647e-10|1.09047143e-8|8.04160261e-10|

The full-duration row has only one window and may benefit from cancellation.
The shortest-window maximum avoids reporting just that favorable endpoint.
On the finer MTS mesh all five window maxima lie below the old peak scale,
but the actual peak error remains about4.57 times that scale. This is NOT a
peak-force pass or evidence of an empirical GR limit.

The largest finite standard/tight momentum difference is8.54352e-16; the
reference standard/tight momentum difference is3.40702e-14. For width.025
the latter contributes about1.36276e-12 to the average-force control, still
well below the reported errors. These are observed controls, not intervals.

Integrating the 81 saved forces by trapezoids instead produces material
impulse discrepancies of roughly1.56e-7 even for the continuum reference.
MTS513 reaches2.20232e-7; MTS1025 reaches1.57744e-7. The sparse quadrature is
not an adequately resolved definition of impulse. This is a shared diagnostic
limitation, not a reason to excuse MTS's separate peak-force failures.

Evidence:
`source-intake/navier-stokes/20260914/annular-material-impulses-attempt01/status.json`
and its frozen-window protocol and four saved impulse arrays.

## 4. Exact momentum-to-pointwise interpolation inequality

Let e be continuously differentiable on [0,T], f=e', and ||e||_infinity<=epsilon.
Suppose f has modulus of continuity omega:

    |f(t)-f(s)| <= omega(|t-s|).

At every t, one can choose a forward or backward interval of any length
0<d<=T/2 staying inside the domain. Subtracting its average gives

    |f(t)| <= 2 epsilon/d + (1/d) integral_0^d omega(u) du.  (4)

Indeed the interval average is the endpoint difference of e divided by d,
bounded by2epsilon/d; the difference between f(t) and that average is bounded
by the integral of its modulus. The backward-interval proof is identical.
This includes t=0 and t=T without silently discarding the initial layer.

If f is Lipschitz with constant K on the ENTIRE interval, then

    ||f||_infinity <= 2 epsilon/d + K d/2.             (5)

For K>0 and d*=2sqrt(epsilon/K)<=T/2, optimization yields

    ||f||_infinity <= 2sqrt(epsilon K).                (6)

Otherwise d=T/2 gives4epsilon/T+KT/4. If K=0, f is constant and its
full-interval average bounds it by2epsilon/T. If epsilon=0, f=0 exactly.

In particular, epsilon_h->0 AND epsilon_h K_h->0 are sufficient: using the
smaller of d* and T/2 covers both cases. For the previous internally derived
epsilon_h=O(sqrt(h)), a sufficient rate is K_h=O(h^-a) with a<1/2.
Then (6) gives O(h^(1/4-a/2)); a uniform K gives O(h^1/4).
An analogous Holder modulus K d^beta gives2epsilon/d+K d^beta/(beta+1).

These are conditional THEOREMS, not evidence that the needed K_h is bounded
for the evolved MTS sequence. A bound on the force derivative of the actual
finite solution suffices; force-derivative ERROR need not itself converge
to zero. The initial slope mismatch in section7 therefore does not refute
this route.

Why momentum convergence alone cannot suffice: the kinematic sequence

    e_h(t)=sqrt(h)[1-cos(t/sqrt(h))]

has e_h(0)=e_h'(0)=0 and ||e_h||<=2sqrt(h), but e_h'=sin(t/sqrt(h)) does
not converge uniformly to zero on any fixed nonzero interval. This is NOT
an MTS solution or a physical counterexample; it isolates the logical gap.

## 5. Derive and independently check the actual force rates

### Reference characteristic rate

Let s=+1 denote the left incoming characteristic and s=-1 the right, and
let phi0 be the unchanged initial profile. Before the already-excluded outer
return, set

    r_s=b-s t,
    N_s=phi0(r_s)+(1+s V0) r_s phi0'(r_s),
    H_s=N_s/[b(1+s V)],
    N_s'=(2+s V0)phi0'(r_s)+(1+s V0)r_s phi0''(r_s).

The existing source equation gives a=Vdot. Ordinary differentiation yields

    Hdot_s=N_s'(V-s)/[b(1+s V)]
              -H_s[V/b+s a/(1+s V)],                (7)
    D=H_+^2-H_-^2,
    F_ref=b^2(1-V^2)D/2,
    Fdot_ref=b V(1-V^2)D-b^2 V a D
               +b^2(1-V^2)(H_+ Hdot_+-H_- Hdot_-).   (8)

The piecewise polynomial profile supplies phi0'' independently of the force
code. Its force reconstruction agrees with the saved characteristic force;
six interior directional finite differences of the original force function
check (8). No complex differentiation is applied through abs/profile branching.

### Finite-action rate and source-field momentum

For the autonomous finite velocity-coordinate flow z'=F_v(z),

    dF_m,h/dt=DF_m,h(z) F_v(z).                       (9)

The existing independently qualified matrix-free adjoint supplies the
gradient. A complex directional derivative of the original finite force
is an independent numerical check of (9), not a sampled time difference.

The kinetic Legendre transformation gives X=(U,b,P,p_b) with (2), and

    Xdot=(W,V,L_U,L_b),
    L_U=V A^T W+V^2 B U-K U,
    L_b=W^T M_b W/2+V W^T A_b U
          +V^2 U^T B_b U/2-U^T K_b U/2,             (10)
    K=K_bulk+K_Gram.

The derivative of the complete canonical momentum along F_v agrees with
(L_U,L_b). The transformed force covector paired with (10) agrees with (9).
This explicitly retains the field momentum rather than assuming it is silent.

Use the instantaneous-geometry canonical energy norm

    ||delta X||_E^2 =
      delta U^T K_bulk delta U+delta b^2
          +delta P^T M^-1 delta P+delta p_b^2.

It is uniformly equivalent to the fixed-geometry norm on the existing
geometry tube. For a force covector g in canonical coordinates,

    ||g||_E,dual^2 =
      g_U^T K_bulk^-1 g_U+g_b^2+g_P^T M g_P+g_pb^2,
    |Fdot_m,h| <= ||DF_m,h||_E,dual ||Xdot||_E.       (11)

All operations are banded or sparse. No dense Hessian, subagent or large
trajectory rerun is needed. Positive norms and Cauchy duality are checked.

Evidence:
`scripts/annular_instantaneous_force_bridge_20260917.py`,
`scripts/qualify_annular_force_bridge_20260917.py`,
`source-intake/navier-stokes/20260914/annular-force-bridge-attempt01/status.json`.

## 6. What those derivatives do and do not establish

|Branch / nodes|max sampled force-rate error|max sampled force dual sensitivity|max sampled canonical flow norm|
|---|---:|---:|---:|
|reference / 513|.00241200044|19.8137|.715248|
|reference / 1025|.00241200212|31.4689|.715248|
|MTS / 513|.00783026379|125.930|.715255|
|MTS / 1025|.00883289404|514.769|.715249|

The two derivative implementations agree to at most1.252e-13; the canonical
pairing error is at most1.273e-14. Finite standard/tight derivative differences
range from1.228e-9 to1.69709e-6. In particular force differentiation amplifies
time-integration differences substantially; it is not legitimate to import
the much smaller momentum control as a force-rate error bound.

The Cauchy estimate(11) is very loose: its largest sampled values are14.17,
22.51,90.06 and368.14 respectively. Actual force rates are below.081 at the
saved points. Signed directional cancellations matter; bounding every
component separately wastes that information.

Plugging the sampled momentum errors and sampled derivative-error maxima
into(6) gives approximately3.045e-6,1.371e-6,1.842e-5 and7.833e-6 in the
same table order. These are NOT certified upper bounds. Their candidate
optimal windows are.001262,.000569,.002352 and.000887, ALL smaller than the
saved .005 spacing. Even the numerical interpolation diagnostic therefore
does not pass the old2e-7 force gate, and unresolved between-sample behavior
cannot be inferred away.

Metadata clarification: the runner flag named
sampled_rate_is_lower_bound_on_required_Lipschitz_constant refers only to
sample-versus-supremum ordering. Its values are evaluations at approximate
saved states, not validated lower or upper bounds for the exact trajectory's
K_h. Both that K_h and the continuous epsilon_h remain uncertified numerically.
The sealer explicitly retains this qualification.

## 7. Derive the initial-corner clue without changing the initial data

Near b0, phi0(r)=k(r-b0), k=.01, V0=.06. Initially both characteristic
gradients are k and F_ref(0)=a(0)=0. Equation(7) then reduces exactly to

    Hdot_+(0+)=-2k/[b0(1+V0)],
    Hdot_-(0+)=+2k/[b0(1-V0)].

Inserting these in(8) yields

    Fdot_ref(0+)=-4 b0 k^2=-.002412,                 (12)

independent of V0. The one-sided derivative notation matters.

The same initial data have a source compatibility defect. The bulk radial
wave equation gives phi_tt=phi_rr+2phi_r/b, and phi_t=-V0 phi0' initially.
The twice differentiated essential condition phi(t,b(t))=0 requires

    phi_tt+2V phi_tr+V^2 phi_rr+a phi_r=0.

At the locally linear initial profile with a=0, the bulk expression instead
equals2k/b0=2/603. This is the previously identified second-derivative corner
defect, not a newly fitted explanation.

Direct finite initial-state force slopes:

|Base nodes|reference|MTS|
|---|---:|---:|
|513|4.42774e-10|2.37314e-8|
|1025|2.12403e-9|-5.59221e-9|
|2049|-7.64192e-10|-7.61590e-10|
|4097|1.30574e-8|5.46147e-8|
|8193|2.18449e-8|7.68934e-9|

These small finite slopes are not converging monotonically; cancellation
and floating-point differentiation matter on the finest meshes. The sweep
is NOT a proof of their limit. It does show that assuming uniform convergence
of force derivatives at t=0 is not supported by either branch's tested data.

Uniform force convergence can coexist with a persistent slope mismatch.
For example, -a[t-h(1-exp(-t/h))] has derivative0 at t=0 but converges
uniformly to-at, with error at most |a|h. Thus(12) does not invalidate the
weaker uniform-force target or the sufficient regularity criterion(6).

The nine-grid sweep also resolves a misleading adjacent-grid comparison:
the source phase cycles .6,.2,.4,.8 as the base grid doubles. For the SAME
phase, initial dual sensitivity grows by about4 when h decreases by16
(e.g. MTS18.9632 at33,75.5655 at513,302.192 at8193). That is compatible
with h^-1/2 trace amplification, not a proved uniform bound or a fitted law.
Do not infer an h^-2 divergence from the larger adjacent-grid phase jump.

Evidence:
`scripts/qualify_annular_initial_force_corner_20260917.py`,
`source-intake/navier-stokes/20260914/annular-initial-force-corner-attempt01/status.json`.

## 8. Validation and the next actual calculation

This turn completes200 implementation checks:68 impulse,75 force-bridge and
57 initial-corner checks. Those are code/algebra/provenance checks, NOT200
physics successes. There are no new failed executed attempts; all26 inherited
failed attempts and the four current failed peak-force cases remain retained.

The next derivation should isolate the existing finite action's initial
source layer and its directional cancellation, retaining the lifted-Gram
term and actual source phase. Derive a short-time, mesh-rescaled source
response or a uniform trace/force modulus; qualify it on BOTH branches
before expensive new trajectories. It must use the unchanged incompatible
initial data and material force, not silently insert a smooth start, average
the old observable, or discard the field contribution to canonical momentum.

An initial-layer calculation alone will not bound all of[0,.4]: the .19-.21
envelope-transition region also needs coverage. The desired usable output
is a bound on the actual force-error modulus (or its needed derivative)
strong enough that epsilon_h K_h->0, or a different proved pointwise-force
estimate. If such a bound cannot be closed, the existing energy/impulse limit
remains valid at its stated scope; a pointwise or full-GR pass must not be
substituted for it.
