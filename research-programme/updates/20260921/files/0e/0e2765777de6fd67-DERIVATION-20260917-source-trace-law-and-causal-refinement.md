# Source-trace law and independent causal spatial-refinement check

Private continuation of
`DERIVATION-20260917-causal-GR-driven-field-source-response.md`.
The action, source preparation, all Gram rows, original T=.4 and comparison
thresholds are unchanged. Scope is the prescribed-flat, finite source/field
control: this is not the full GR limit, a live-metric result, or an empirical
confirmation. Previously completed trajectories and time controls are reused.

## 1. The refinement changes the cut-cell phase

Use reference radius xi in[5.2,6.8], anchor a=6.03, bulk spacing
h=1.6/(N-1), and8 subdivisions on either side of the anchor within its bulk
cell. On the ideal dyadic sequence N=2^k+1,

    theta_k = fractional_part((83/160) 2^k).

For k>=5 the exact phase cycles3/5,1/5,2/5,4/5. Thus:

|N|257|513|1025|2049|
|---|---:|---:|---:|---:|
|theta|4/5|3/5|1/5|2/5|

The innermost reference-element lengths are ell_-=h theta/8 and
ell_+=h(1-theta)/8. Both lie between h/40 and h/10. There is no progressively
worsening *relative* sliver on this exact sequence, although halving h does not
halve each innermost length. In particular the shortest length falls fourfold
between513 and1025. This explains why a naive grid-size-only runtime estimate
can be misleading. This ideal-grid proof is not a guarantee about arbitrary
anchors, arbitrary N, or arbitrarily fine floating-point coordinates.

## 2. Derive the actual P2 source derivative error

Set x=xi-a and U(0)=0, as in the source-anchored projection. The implemented
one-sided quadratic endpoint derivatives are

    D_- U = [U(-ell_-)-4U(-ell_-/2)+3U(0)]/ell_-,
    D_+ U = [-3U(0)+4U(ell_+/2)-U(ell_+)]/ell_+.

Write J_h U=D_+U-D_-U and j1=U'_+(0)-U'_-(0). Taylor expansion yields

    J_h U-j1
      = [ell_-^2 U'''_-(0)-ell_+^2 U'''_+(0)]/12
        -[ell_-^3 U''''_-(0)+ell_+^3 U''''_+(0)]/32 + R.

Under one-sided C5 regularity,

    |R| <= (7/960)[ell_-^4 sup|U'''''_-|+ell_+^4 sup|U'''''_+|].

The coefficient follows from the signed fifth-derivative Peano kernel:
on0<=s<=ell/2 its numerator is4(ell/2-s)^4-(ell-s)^4<0, and on the remaining
half it is-(ell-s)^4. Its integral magnitude after dividing by24ell is
7ell^4/960. The left stencil follows by reflection.

A less demanding bound needs only bounded one-sided third weak derivatives:

    |J_h U-j1| <= [ell_-^2 M3_-+ell_+^2 M3_+]/12.

The endpoint interpolation remainder gives this constant. The high-order
expansion must not be imposed across an unresolved regularity front. The
original compact-quintic preparation is only piecewise smoother than C2;
uniform continuum C5 bounds are not part of the inherited evidence.

For equal third derivatives the leading trace coefficient is
h^2(2theta-1)U'''/(12*8^2): it changes sign between513 and1025. Fitting every
grid to a single phase-independent coefficient would conceal this effect.
These are derivative-trace laws, not yet laws for the final material force.

## 3. The lifted Gram factor leaves a curvature-jump term

The original extra Gram operator is G=T D3, not an unweighted D3 stencil.
The code's exact positive Gram coefficients give

    (1/20)I < T^T T < (1/8)I

for the disjoint closures used here. Diagonal dominance proves both bounds;
the checker uses the actual boundary fractions as well as the interior rows.
Let p(x)=max(x,0), g=G p and Gtilde=G-g J_h. Then

    Gtilde U = G(U-j1 p) - g(J_h U-j1).

The slope kink is removed; a curvature kink is not. With
j2=U''_+(0)-U''_-(0), the leading source-crossing factor is

    Psrc Gtilde U = (j2/2) Psrc G(p^2) + O(h^3).

Here Psrc selects the fixed number of rows whose original stencil crosses the
anchor. This statement assumes bounded one-sided third derivatives on their
shrinking support. It does not assume those derivatives are uniformly bounded
for the continuum limit merely because a finite polynomial can be differentiated.

An explicit usable remainder, with x_i=xi_i-a and M3_side(i) a derivative bound,
is

    B3 =
      || Psrc |G| [ M3_side(i) |x_i|^3/6 ] ||_2
      + ||Psrc g||_2 [ell_-^2 M3_-+ell_+^2 M3_+]/12.

It bounds the difference between the actual source factor and its displayed
curvature term. Source-crossing stencils span at most a fixed multiple of h,
so B3=O(h^3) if the derivative bounds are uniform. No fitted coefficient enters.

For the bulk third-difference stencil the only nonzero entries of D3(p^2)/h^2
are

    v(theta) = [(1-theta)^2, 1+2theta-2theta^2, theta^2].

These source rows lie in the interior closure. Therefore their full weighted
Gram norm is exactly

    ||G(p^2)||_2^2 / h^4
      = [5(v0^2+v1^2+v2^2)-v0 v1-v1 v2]/72.

This phase dependence is fixed by the action's coefficients, not regression.
The finite-grid checker also retains the next cubic contribution

    U'''_-/6 G(x^3) + [U'''_+-U'''_-]/6 G(p^3)
      - g[ell_-^2 U'''_- - ell_+^2 U'''_+]/12.

## 4. No hidden grid blow-up in the lift itself

The source degree of freedom is eliminated. Consequently the exact Euclidean
row norm is

    ||J_h||_2^2 = 17(ell_-^-2+ell_+^-2),    h||J_h||_2 <= 170.

Also ||D3 p||_2^2=h^2(6theta^2-6theta+2)<=26h^2/25 on the dyadic phases,
and ||D3||_2<=8. Hence

    ||g||_2 <= sqrt(13/100) h,
    ||Gtilde||_2 <= 8/sqrt(8) + 170 sqrt(13/100).

The ideal-grid lift is uniformly bounded even though J_h alone is not.
This is a bounded spatial operator, not a time-evolution stability theorem.

For completeness, the reference P2 mass on an element of length ell is
ell/30 times[[4,2,-1],[2,16,2],[-1,2,4]]. Its smallest eigenvalue divided
by ell is(19-sqrt(201))/60>0. With positive uniformly bounded map Jacobians
and radius weights, assembly and ell_min>=h/40 give M>=c h I.
The bulk and Gram stiffness norms are O(1/h), so sqrt(lambda_max(M^-1 K)),
the frozen wave stiffness scale, is O(1/h). This does not establish a uniform propagator bound
for the full nonautonomous coupled field/source system.

## 5. Curvature is tied to the moving boundary, not a new free parameter

For a smooth flat spherical scalar satisfying
phi_tt=phi_rr+2phi_r/r and phi(t,b(t))=0, set V=b_dot,
a_b=V_dot, H_side=phi_r(t,b(t)^side), and dot H_side its total boundary
derivative. Twice differentiating the boundary condition gives

    (1-V^2) phi_rr + 2V dot H + (a_b+2/b) H = 0.

Thus, for the two affine pullback Jacobians sigma_side,

    U''_side
      = -sigma_side^2 [2V dot H_side+(a_b+2/b)H_side]/(1-V^2).

The curvature jump in section3 can therefore be sourced from the boundary
field evolution and source acceleration, rather than inserted as a fit.
This identity requires a sufficiently regular compatible continuum solution.
Our spectral GR reconstruction is checked for its boundary-curvature
compatibility residual; it is not automatically assumed to satisfy the
identity exactly at finite reference degree.

## 6. Exact entry into the coupled material force

The lift alone is not the force. In the unchanged kinetic action, let
c=A U, mu=S/(1-V^2)^(3/2), and
s_H=mu+U^T B U-c^T M^-1 c. Previous derivation gives s_H>=mu>0.
Let D_h be the diagonal Gram weight including1/h, D_h,b its source-position
derivative, q=Gtilde U and w=Gtilde M^-1 c. The exact instantaneous Gram
contribution to the material force at a fixed full state is

    F_Gram = (mu/s_H)[w^T D_h q - q^T D_h,b q/2].

It follows by eliminating the field acceleration in the coupled mass matrix.
The scalar/source kinetic matrices are identical in the finite-reference and
MTS branches. The checker compares this expression directly with the
difference of their unmodified force evaluations at the same GR-projected state.
It is not the difference of their evolved trajectories.

The same formula splits additively by Gram rows, including Psrc. If q2 denotes
the curvature approximation on these rows and ||q-q2||<=B3, then exactly

    |F_src(q)-F_src(q2)|
      <= (mu/s_H)[||D_h w-D_h,b q2|| B3
                 + ||D_h,b||_infinity B3^2/2].

This supplies an explicit force remainder at the specified state. It still
contains the mechanically derived field-feedback weight w, not an assumption
that pointwise force error is of the same order as q. In particular an O(h^2)
source factor does NOT by itself prove an O(h^2) final force discrepancy.
The independent causal field/source response from the preceding checkpoint
must be included, as must initial projection and nonlinear dynamical remainder.

## 7. Conditional vanishing-force bound, not just a fitted scaling

There is also a conservative consistency bound for the *complete* instantaneous
Gram force. Assume a fixed piecewise W3,infinity reference field, uniform
one-sided derivative bounds, a source map uniformly away from degeneracy,
and bounded discrete transport energy E_tr=U^T B U. The latter follows for
interpolants of a uniformly regular reference field on this quasiuniform mesh.
These are stated hypotheses, not additional proven properties of every MTS
solution or of the continuum GR trajectory in this experiment.

Away from the source, the raw third difference of U-j1 p is bounded by
h^3 M3_side, using its repeated-integral representation. There are O(1/h)
such rows, giving an O(h^(5/2)) Euclidean norm. The fixed number of crossing
rows contributes O(h^2) from j2 and O(h^3) from the local Taylor remainder.
Together with ||T||<=1/sqrt(8) and the lift correction, this proves

    Q_h := ||Gtilde U||_2 <= C_q h^2

with a uniform constant under the stated hypotheses. The numerical checker
constructs a non-asymptotic rowwise version of this bound, rather than assigning
C_q by fitting the observed force errors.

Kinetic positivity gives c^T M^-1 c<=E_tr. Therefore, from M>=c_M h I
and the section4 lift bound C_G,

    ||w||_2 <= C_G sqrt(E_tr/(c_M h)).

Since ||D_h||<=C_D/h and ||D_h,b||<=C_Db/h on a nondegenerate source map,
and mu/s_H<=1, the exact section6 force identity yields

    |F_Gram|
      <= C_G sqrt(E_tr/(c_M h)) ||D_h|| Q_h
          + ||D_h,b|| Q_h^2/2
      <= C_F h^(1/2) + C_F2 h^3 -> 0.

This is a derived sufficient consistency law for the extra Gram material
force evaluated on regular prescribed nodal states. It is intentionally a
weak upper bound, not a claim that measured force errors have order1/2.
No continuum smoothness constant has been established from finite polynomial
fits, and the bound need not be numerically sharp.

Most importantly, F_Gram is the difference between the two instantaneous
finite-action forces at the SAME state. This theorem does not bound the
difference between their evolved states, prove that the finite reference
already converges to GR, or control the full coupled propagator uniformly in h.
It closes a specific conditional spatial-consistency question, not the GR limit.

## 8. Numerical protocol and results

Both independent1025/8 predictions and the source-trace qualification completed.
Prediction inputs contain only the sealed GR projection and original initial
state. Both degrees768 and512 use81 reconstruction knots and the original
fullT=.4. Both branches and both prespecified force outputs are retained.
All four predictions were frozen at13:40:45.207690Z before the validator's
future-state read phase began at13:40:45.223779Z on2026-09-17.

The previous513/8 independent time/reconstruction controls remain evidence
for that grid, not an invented completed fine-grid predictor time test. The
finest original finite trajectories already have their own completed tighter
controls. No such trajectory is re-evolved here.

Source-polynomial third/fifth derivative bounds use Chebyshev coefficient
absolute sums; they are analytic bounds on those finite polynomials evaluated
in floating point, not interval certificates or uniform continuum estimates.
Every measured leading-term residual and reference-degree sensitivity is
reported, including unhelpful or failed approximations.

Implementation:

- `scripts/prepare_annular_GR_causal_refinement_20260917.py`
- `scripts/run_annular_GR_causal_refinement_20260917.py`
- `scripts/derive_annular_source_trace_refinement_20260917_v3.py`
- `scripts/validate_annular_GR_causal_refinement_20260917.py`

No physics claim, action repair, force subtraction, public update or
subagent delegation is authorized by this calculation.

### Independent finer-grid prediction

Maximum force errors against the completed finite trajectories, over the81
original sample times, in the benchmark's existing normalized units:

|GR degree|Branch|Original force on predicted state|Linearized force|Original finite-to-GR discrepancy|
|---|---|---:|---:|---:|
|768|reference|1.24721e-13|6.56304e-12|2.16929e-7|
|768|MTS|1.85877e-10|3.23905e-9|9.20686e-7|
|512|reference|7.69016e-14|6.17860e-12|2.50244e-7|
|512|MTS|1.84420e-10|3.30439e-9|9.19119e-7|

Both output rules pass the2e-7 prediction gate in all four cases. The reference-
degree control changes the predicted finite force by8.66820e-14(reference)
and1.64005e-12(MTS); linear-force changes are5.08180e-12 and1.05795e-10.
All are below2e-8. No new independent finer-predictor tighter-time or
reconstruction-knot run was performed; these particular controls remain
qualified only on513/8. The original fine target trajectories' separate
tighter-time controls were reused, not relabeled as predictor controls.

For MTS at degree768, the predicted source/velocity/clock errors are
9.39242e-10,7.21975e-9,5.32180e-11. Field/field-rate errors are
6.39402e-12 and1.08581e-10. Source, velocity and clock prediction gates pass.
All four original full-trajectory GR force gates remain false.

|Branch/GR degree|Actual513-to1025 peak ratio|Predicted ratio|Actual two-grid effective order|
|---|---:|---:|---:|
|reference/768|0.39570711|0.39570706|1.33750|
|MTS/768|0.25074222|0.25069741|1.99572|
|reference/512|0.44249142|0.44249138|1.17628|
|MTS/512|0.24835120|0.24830720|2.00955|

The independently predicted coupled response reproduces the observed
refinement improvement. The nearly fourfold MTS reduction is encouraging,
but two grids, changing cut phases and reference uncertainty do not prove
second-order or uniform continuum convergence. These predictions use the
same finite action as their target; they are internal consistency results,
not independent experimental support.

### The pointwise-jet shortcut fails on the available data

The exact identities and conservative bounds pass, but the truncated endpoint
Taylor approximation does not give a usable finite-grid error law here.
At1025/8, degree768:

- actual maximum derivative-trace error:7.68078e-9;
- cubic-jet approximation residual:2.41646e-6;
- quartic-jet approximation residual:4.14195e-5;
- actual maximum source Gram-factor norm:4.21506e-9;
- curvature-only factor residual:4.95013e-9;
- cubic factor residual:1.41138e-6.

AtT=.21 the actual source-row Gram force is+9.46518e-6, while the
curvature-only approximation gives-9.05950e-6: even its sign is wrong.
The cubic approximation gives-8.24872e-4. None of the cubic/quartic trace,
curvature-factor or cubic-force approximations improves on the corresponding
zero-approximation baseline in maximum norm across the six tested cases.
These failures are retained explicitly;97 successful identity/bound checks
must not be described as97 successful approximation tests.

The source curvature itself is not securely represented by its endpoint jet:
atT=.21 the projected jump changes from0.00860400(degree512) to
0.00771190(degree768), whereas the boundary-evolution expression gives
0.00708853 and0.00708917. Maximum boundary-curvature compatibility residuals
are0.00375543 and0.00374673. This mismatch is not set to zero.
The globally bounded polynomial third/fifth derivatives grow substantially
with reference degree. The present cells are not in a demonstrated uniform
endpoint-Taylor regime; adding more derivative terms makes the approximation
worse, not better.

The conservative global force bound also remains far too loose to certify
the physical gate: its degree768,1025/8 maximum is279.417, versus an actual
instantaneous extra-Gram force maximum1.68154e-5. The conditional vanishing
argument in section7 is mathematical consistency, not a numerically useful
force-error certificate at the current resolution.

### Preserved coordinate-roundoff failures

Two short qualification attempts are preserved:

- `source-intake/navier-stokes/20260914/annular-source-trace-refinement-attempt01/status.json`
- `source-intake/navier-stokes/20260914/annular-source-trace-refinement-attempt02/status.json`

The first stopped on the1025 manufactured quintic trace; the second on the2049
unit hinge. Binary rounding of physical midpoint coordinates makes them differ
slightly from exactly half their element length. The1025 raw manufactured
error3.18329807e-11 is explained by the independently evaluated coordinate
displacement contribution3.18326962e-11, leaving2.84495e-16. The2049 raw unit-
hinge error-3.03164160e-11 has coordinate contribution-3.03164901e-11.
The successful v3 checks the exact stencil identity with that explicitly
reported coordinate contribution; it does not loosen the polynomial test,
alter the mesh/action, correct a force, or overwrite either failed attempt.
Floating bounds elsewhere allow2e-11 arithmetic slack and are not interval
certificates. Ideal-grid asymptotics must remain distinct from floating-point
behavior at arbitrary refinement.

Successful evidence:

- `source-intake/navier-stokes/20260914/annular-GR-causal-refinement-inputs-attempt01/status.json`
- `source-intake/navier-stokes/20260914/annular-GR-causal-refinement-768-attempt01/status.json`
- `source-intake/navier-stokes/20260914/annular-GR-causal-refinement-512-attempt01/status.json`
- `source-intake/navier-stokes/20260914/annular-source-trace-refinement-attempt03/status.json`
- `source-intake/navier-stokes/20260914/annular-GR-causal-refinement-validation-attempt01/status.json`

19 preparation checks,18 prediction checks,97 algebra/bound checks and23
comparison checks:157 successful implementation checks, plus the two
preserved failed attempts. No overall GR or approximation pass follows from
that count.

## 9. Next route: finite-width curvature kernels and coupled stability

Do not launch another huge mesh merely to extrapolate an apparent order, or
reuse the failed endpoint-jet truncation. The next step should construct
finite-width trace kernels from the actual action and control their integrated
response. An exact ideal-stencil starting identity is available:

For each row with coefficients a_i of Gtilde, its annihilation of both
piecewise-linear slopes and U(0)=0 imply

    (Gtilde U)_row
      = integral_{s<0} K_-(s) U''_-(s) ds
        + integral_{s>0} K_+(s) U''_+(s) ds,

    K_-(s) = sum_{x_i<=s<=0} a_i (s-x_i),
    K_+(s) = sum_{0<=s<=x_i} a_i (x_i-s).

This follows by twice integrating U'' separately on each side; it uses
curvature over finite intervals rather than arbitrarily high derivatives
at one endpoint. With constant one-sided curvatures it recovers the section3
term, but it retains their spatial variation rather than truncating it.
The ideal-kernel identity is derived here; its independent implementation
and qualification remain the next task, including the recorded coordinate
roundoff contribution.

Then combine that representation with an energy/adjoint bound for the full
coupled causal response, retaining the source-map dependence and nonlinear
remainder. The aim is to derive sufficient regularity/stability rather than
silently assume a uniform C3/C5 Taylor regime. A bound only on the
instantaneous extra-Gram force cannot replace this dynamical step.
