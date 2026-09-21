# Full-interval force: a corrected comparison path

2026-09-18. Private continuation of
`DERIVATION-20260917-nonlinear-initial-force-refinement-bound.md`.

## 1. Proposed internal theorem and precise scope

For the SAME two prescribed-flat semidiscrete actions, the original initial
data, eight source subdivisions, and the dyadic four-phase mesh family, the
construction below improves the accumulated canonical energy error to

    sup_[0,T] ||X_h-Y_h||_E <= C h^(3/5),   T=.4.             (1)

Combined with the material-force estimate proved in the preceding note,
this yields the whole-interval bound

    sup_[0,T] |f_h(X_h)-F_ref| <= C h^(1/10).                 (2)

These are internal analytic conclusions using the earlier reference,
Hamiltonian-neighborhood and force-generator lemmas. They concern the EXACT
nonlinear semidiscrete solution, not time-stepped output. Qualification of
the new construction is recorded separately at the end; numerical samples
are not the proof of uniform bounds. Independent mathematical review,
useful numerical constants/h0, and a certified integration error are absent.

This is NOT the full GR limit: the metric is still prescribed flat. It
does not close parent coupling, live metric evolution, black-hole regularity
or empirical viability. All four old sampled full-horizon force failures
remain failures at their original grids and threshold.

The limiting parameter here is the mesh spacing of the specified finite
action family. This is a numerical continuum-consistency result, not a
derived physical decoupling limit of the complete parent theory. In
particular, a raw third difference on a smooth field is O(h^3), so this
Gram family's weight O(1/h) over O(1/h) rows gives an O(h^4) smooth-field
energy contribution away from the source/fronts. Its vanishing under mesh
refinement must not be advertised as deriving Einstein dynamics or a
parent-owned coupling scale. The point of the new argument is that source
coupling, curvature fronts and nonlinearity no longer defeat instantaneous
force convergence in this specific refinement test.

The construction changes ONLY the reference path used in the proof. No
physical smoothing, new damping, altered Gram term, reset of accumulated
error, compatible replacement data, or corrected output force is used.
Its initial mismatch is explicitly retained.

## 2. Existing inputs and why another energy estimate was insufficient

Use canonical X=(U,b,P,p_b), J=[[0,I],[-I,0]], F_h=J DH_h, and

    ||delta X||_E^2 = delta U^T K0 delta U + delta b^2
                      +delta P^T M0^-1 delta P + delta p_b^2.

Y_h is the kinetic Legendre image of the source-fitted P2 interpolant of
the exact characteristic reference, including its full source-field momentum.
The earlier two notes supply uniform, sufficiently-fine-mesh bounds

    ||Ydot_h||_E <= C,     ||J||_(E*->E) <= C/h,
    ||D^j H_h|| <= C, j<=3,
    R_h=F_h(Y_h)-Ydot_h=(0,R_U,R_b),
    ||R_h||_E <= C sqrt(h),    |R_b| <= C h.                (3)

The uniform shifted relative-Hamiltonian coercivity and its exact nonlinear
identity give stability against ANY sufficiently close comparison path W:

    sup ||X_h-W||_E <= C [||X_h(0)-W(0)||_E
                             + integral ||F_h(W)-Wdot||_E]. (4)

Here W, its comparison segments and X remain in the established timelike
geometry tube, and ||F_h(W)||_E is uniformly bounded. Those conditions are
checked below, not silently inherited from Y.

The old material observable estimate, with d=||X_h-Y_h||_E, is

    |f_h(X_h)-F_ref| <= C [h+(1+h^-1/2)d+d^2/h].            (5)

Simply inserting d=O(sqrt(h)) does not make (5) vanish at fixed time. The
task is to improve d, not to reset it or discard the nonlinear term.

Sources:
`DERIVATION-20260917-coupled-Galerkin-defect-and-flat-nonlinear-limit.md`,
`DERIVATION-20260917-time-dependent-force-adjoint-and-relative-energy.md`,
and the preceding initial-force note.

## 3. Inward time averaging, including both endpoints

Work in the benchmark's nondimensional coordinates. Choose 0<epsilon<T/4,

    a_e=1-2 epsilon/T,   c_e(t)=epsilon+a_e t,
    <g>_e(t)=(1/epsilon) integral_[c_e-epsilon/2,c_e+epsilon/2] g(s) ds,
    Z_h(t)=<Y_h>_e(t).                                    (6)

Every sample lies in [epsilon/2,T-epsilon/2]. No extension of the reference
outside its qualified horizon, negative-time solution, or assumed zero
terminal error is needed. From (3),

    ||Z_h-Y_h||_E <= C epsilon,
    Zdot_h=a_e <Ydot_h>_e,    ||Zdot_h||_E<=C.              (7)

The EXACT reference defect decomposes as

    F_h(Z_h)-Zdot_h = <R_h>_e + C_e + (1-a_e)<Ydot_h>_e,
    C_e=F_h(Z_h)-<F_h(Y_h)>_e.                            (8)

The first-order term in the Taylor expansion of DH about its mean cancels.
The uniform third Hamiltonian derivative and ||J||<=C/h therefore give

    ||C_e||_E <= C epsilon^2/h.                            (9)

This nonlinear commutator is NOT omitted. The compression term is O(epsilon).
Both prevent treating time averaging as an exact solution symmetry.

## 4. Moving-front averaging gains half a spatial derivative

On each source half, the actual characteristic reference is C1 and has
bounded piecewise third spacetime derivatives. Its only curvature jumps
are the two initial-source fronts r=6.03 +/- s. Envelope transitions may
change third derivatives but do not add curvature jumps. This is the
regularity established for the actual unchanged reference, not a smooth
manufactured replacement.

In fixed source coordinates, a front xi=gamma(s) satisfies

    gamma'(s)=(+/-1-w(gamma)V(s))/Jmap.

The continuum energy bound |V|<3/4 and positive uniform map bounds imply
0<c<=|gamma'|<=C. Thus no front is stationary or tangent to the averaging
direction. A distributional spatial derivative of a bounded curvature
jump contributes A(s) delta(xi-gamma(s)). Its box average has magnitude at
most C/epsilon and support of length at most C epsilon. Its L2 norm is
therefore at most C epsilon^-1/2. The regular part stays bounded.

Applied on each source half, this proves

    ||<U>_e||_H3 + ||<U_t>_e||_H2 + ||<U_tt>_e||_H1
        <= C (1+epsilon^-1/2).                           (10)

Here t derivatives under brackets are the ORIGINAL pullback derivatives
at s, not derivatives with respect to the compressed observation time.
The time window stays strictly above zero, so source traces use their
well-defined outgoing one-sided limits, not the incompatible initial
second-order corner assignment.

For the BASE field residual, freeze its bounded coefficient functions at
c_e(t). Its exact weak form is

    R_U,base(v)=-integral [v delta P_t+v_xi delta Q].

P2 interpolation commutes with averaging. Broken-space interpolation using
(10) gives averaged e_xi,e_t of size C h^2 epsilon^-1/2 in L2, and averaged
e_txi,e_tt of size C h epsilon^-1/2. The test inverse inequality costs 1/h
only on delta Q. This gives C h epsilon^-1/2 in the mass-dual norm.

Unfreezing coefficients costs at most C epsilon sqrt(h): the original
e_xi,e_t bounds are O(h^(3/2)), the original e_txi,e_tt bounds are O(sqrt(h)),
and all coefficient time derivatives are bounded, including source
acceleration derivatives. Thus

    ||<R_U,base>_e||_M0^-1
       <= C [h epsilon^-1/2 + epsilon sqrt(h)].            (11)

The original scalar source bound |R_b,base|<=C h survives averaging directly.
No source-field momentum term is replaced by a pressure surrogate.

## 5. A stationary source curvature kink cannot be averaged away

Temporal averaging alone is NOT sufficient for MTS. The lifted Gram removes
the first-gradient jump, but the two pulled-back second derivatives can
differ at the fixed source xi=anchor. This curvature kink does not sweep
through the time window and must be retained.

Define, for s>0,

    j2(s)=U_xixi(anchor+,s)-U_xixi(anchor-,s),
    kappa(xi)=(xi-anchor)_+^2/2,
    w_h=L_h I_h kappa,
    r_s(s)=-j2(s) L_h^T D_h(b(s)) w_h.                     (12)

L_h is the ORIGINAL lifted factor and D_h the ORIGINAL Gram weight. This
is a decomposition of its reference defect, not a change to the action.
Both j2 and its a.e. time derivative are bounded on (0,T]. This follows
by differentiating the explicit one-sided characteristic traces: the
incoming third derivatives and a' are bounded, and 1+/-V is bounded away
from zero. Envelope-transition derivative jumps are bounded, not deltas
in j2. Its right-hand initial limit need not equal the initial nodal jet.

More explicitly, write I_-=F_0'(s-b), J_-=F_0''(s-b) for the incoming
left characteristic, and I_+=G_0'(s+b), J_+=G_0''(s+b) for the incoming
right characteristic. Differentiating the moving Dirichlet reflection and
using phi=chi/r, chi=0 at the source, gives

    phi_rr,- = 4 V J_-/[b(1+V)^2] + 2 a I_-/[b(1+V)^3]
                                                +4 I_-/[b^2(1+V)],
    phi_rr,+ = -4 V J_+/[b(1-V)^2] - 2 a I_+/[b(1-V)^3]
                                                -4 I_+/[b^2(1-V)].

Then j2=Jmap,+^2 phi_rr,+ - Jmap,-^2 phi_rr,-. Each derivative of these
expressions uses only bounded b,V,a,a', incoming derivatives through third
order, and denominators bounded away from zero. This explicitly supplies
the time regularity needed in (13), rather than assuming it for the finite
MTS trajectory.

For the actual initial slope k=.01, speed V0=.06 and b0=6.03, the outgoing
characteristic corner corrections give the nonzero right-hand limit

    j2(0+)=-8 k V0/[b0(1-V0^2)^2].

The initial pulled-back map has unit Jacobians. Thus the stationary kink
is a specific feature of these data, not merely a hypothetical objection
to averaging. Removing only the travelling fronts would miss it.

The raw factor consists of bounded local third-difference combinations,
including its existing boundary rows. These annihilate global quadratics.
The P2 jump functional annihilates kappa's first-derivative jump exactly.
Hence w_h has O(1) source-crossing rows of size O(h^2), so ||w_h||_ell2<=C h^2.
For every FE field v,

    ||L_h v||_ell2 <= C sqrt(h) ||v||_H1,
    ||D_h||+||partial_b D_h|| <= C/h.

Consequently the stationary residual, viewed as a FIELD-coordinate covector,
has the much smaller elliptic-dual bound

    ||r_s||_H^-1 + ||r_s'||_H^-1 <= C h^(3/2).             (13)

Its momentum/strong norm may still be O(sqrt(h)); confusing these two norms
would invalidate the argument. We use (13) only in a coercive elliptic solve.

Subtract from <U> both its mean gradient hinge and mean curvature kink.
The result is globally H3 across the source, with norm C(1+epsilon^-1/2).
The exact third-difference integral estimate gives a raw factor bound
C h^(5/2) times that H3 norm. The P2 source jump error obeys the trace
estimate C h^(3/2) times the local broken H3 seminorm; its hinge vector
has norm O(h). It therefore has the same h^(5/2) bound. These estimates
do not require a travelling front to lie outside the source stencil.

It follows that

    ||L_h I_h<U>_e - <j2>_e w_h||_ell2
        <= C h^(5/2)(1+epsilon^-1/2).

Freeze D at c_e(t), use ||M0^-1/2 L_h^T||<=C h^-1/2,
and then unfreeze D. The latter error is C epsilon sqrt(h), since each
unaveraged lifted factor and j2 w_h is O(h^2). Thus, defining

    bar r_s=<r_s>_e,    S_h=(0,0,bar r_s,0),

the COMPLETE averaged residual, with the source Gram force retained, obeys

    ||<R_h>_e-S_h||_E
       <= C [h epsilon^-1/2+epsilon sqrt(h)+h].            (14)

The source Gram contribution is O(h^3), already covered by the last term.
For the baseline branch D=0 and S_h=0 identically.

## 6. Construct the comparison corrector, including its time derivative

Invert the exact kinetic Legendre map at Z_h to obtain (U,b,W,V). Use the
same matrices M,A,B,K as in the earlier Hamiltonian proof, where K includes
ALL Gram rows. Set

    C_h=K-V^2 B >= (1-V^2)K_bulk+K_Gram,
    C_h zeta=bar r_s,
    delta=(zeta,0,V A zeta,(A^T W+2V B U)^T zeta).         (15)

This is a unique coercive field solve, not an assumed inverse of an
indefinite full Hamiltonian. The canonical correction in (15) is precisely
the kinetic tangent of (delta U=zeta, delta b=0, delta W=0, delta V=0).
Source momentum is included. From (13), uniform coercivity and the bounded
kinetic map,

    ||delta||_E <= C h^(3/2).                              (16)

The derivative of bar r_s is

    (a_e/epsilon)[r_s(c_e+epsilon/2)-r_s(c_e-epsilon/2)],

which remains O(h^(3/2)) in H^-1 by (13). Zdot is bounded by (7), so
the inverse kinetic tangent and the form derivative of C_h are bounded.
Differentiating its solve explicitly,

    C_h zetadot = (bar r_s)dot - Cdot_h zeta,

proves ||zetadot||_H1<=C h^(3/2). Differentiating BOTH momentum components
in (15) gives

    ||deltadot||_E <= C h^(3/2).                           (17)

There is no 1/epsilon loss here: the stationary coefficient is Lipschitz.

Let Q=D2H_h(Z_h) and let L_bU denote the mixed configuration derivative
of the ORIGINAL Lagrangian at its inverse kinetic state. Exact square
completion, or differentiation of the original canonical equations, gives

    J Q delta=(0,0,-C_h zeta,L_bU zeta).

Therefore

    S_h+J Q delta=(0,0,0,L_bU zeta),
    ||S_h+J Q delta||_E <= C h^(3/2).                     (18)

The surviving scalar source term is bounded, NOT set to zero. This is the
reason a field-only correction can work without pretending source coupling
vanishes. It corrects a comparison trajectory, not a physical force law.

## 7. Close the nonlinear accumulated-error bound

Use the corrected path W_h=Z_h+delta. Its residual is EXACTLY

    F_h(W_h)-Wdot_h = (<R_h>_e-S_h) + C_e
        +(1-a_e)<Ydot_h>_e + (S_h+J Q delta) - deltadot
        + [F_h(Z_h+delta)-F_h(Z_h)-J Q delta].             (19)

The final bracket is bounded by C||delta||_E^2/h<=C h^2 using the uniform
third Hamiltonian derivative. Thus (9), (14), (17)-(19) give

    ||F_h(W_h)-Wdot_h||_E
       <= C [h epsilon^-1/2+epsilon sqrt(h)+h
                                      +epsilon^2/h+epsilon+h^(3/2)+h^2]. (20)

Also ||W_h-Y_h||_E<=C(epsilon+h^(3/2)) and
||X_h(0)-W_h(0)||_E<=C(epsilon+h^(3/2)), because X_h(0)=Y_h(0).
No initial mismatch is erased. Wdot is uniformly bounded by (7),(17),
and (20) then bounds F_h(W_h). For sufficiently small h, W_h and the
required segments stay inside a slightly enlarged version of the already
established timelike/coercive tube. The previous existence/first-exit
argument for X_h still applies. This supplies all comparison hypotheses in (4).

Choose epsilon=h^(4/5). The two potentially largest errors balance:

    h epsilon^-1/2=h^(3/5),    epsilon^2/h=h^(3/5).

Every other term in (20), the initial mismatch, and ||W_h-Y_h|| are
smaller asymptotically. Equation (4) proves (1), uniformly from 0 to T,
including the initial corner and later envelope transition. Substitution
in (5) gives

    |f_h(X_h)-F_ref| <= C[h+h^(3/5)+h^(1/10)+h^(1/5)],

which proves (2). The nonlinear d^2/h term vanishes rather than being ignored.
This rate is deliberately conservative, not a fitted rate or a claim that
the measured force error follows a power of 1/10.

With physical dimensions restored, use epsilon=T_* (h/L_*)^(4/5) for fixed
positive reference scales; the benchmark already uses fixed numerical units.
Fractional powers of a dimensional length are not asserted to equal a time.

## 8. Implementation qualification

`scripts/annular_smoothed_comparison_20260918.py` implements the ORIGINAL
canonical force/kinetic map, compressed time average, stationary curvature
residual, coercive comparison solve and its analytic time derivative.
It uses banded/sparse operations, not a dense full-state Hessian.

`scripts/qualify_annular_smoothed_comparison_20260918.py` compares two
independently ordered time quadratures, split at nodal characteristic-front
crossings. It checks canonical flow against the original velocity flow,
the kinetic inverse, exact tangent cancellation, retained nonlinear
remainder decomposition, the averaged derivative against its endpoint
formula, and the corrector derivative against a separate centered difference.
Both branches use the same times 0,.071,.195,.21,.4, with all four source
phases represented. No original finite trajectory is re-evolved or used
as fitted input.

The corrected runner completes 327 successful implementation checks across
eight branch/grid cases and forty time probes. These are checks of the
construction, not 327 physics passes. Maxima over the full suite are:

|Independent check|Maximum discrepancy|
|---|---:|
|6-point versus 10-point split time quadrature, energy norms|6.45336e-9|
|Canonical tangent versus direct original-flow differentiation|5.50484e-17|
|Full nonlinear residual decomposition|4.81884e-15|
|Relative elliptic-solve residual|2.18082e-15|
|Averaged derivative versus endpoint difference identity|1.51609e-10|
|Corrector derivative versus independent centered difference|3.67168e-15|

The quadrature-control threshold is 2e-8 in these comparison energy norms;
it is NOT the original 2e-7 physical force gate or an interval certificate.

Measured maxima for the MTS comparison construction:

|Base nodes|corrector norm / h^(3/2)|corrector-rate norm / h^(3/2)|regular residual / [h/sqrt(epsilon)+epsilon sqrt(h)+h]|
|---|---:|---:|---:|
|129|.00314660|.0893187|2.99755|
|257|.00345858|.0988241|7.54907|
|513|.00449749|.136055|1.72580|
|1025|.00396392|.118772|3.05533|

These phase-dependent finite probes are not fitted uniform constants and
are not monotone. The baseline corrector is identically zero. The raw MTS
corrected-comparison residual maxima are .284100, .421111, .0699750 and
.0716537 respectively; no claim that each refinement improves this quantity
is made. Compression and the uncancelled regular part remain in it.

A further independent source check in
`scripts/qualify_annular_source_curvature_20260918.py` completes 16 checks.
It derives curvature from the bulk wave equation and the twice-differentiated
moving boundary:

    phi_rr = [-2 V d_t(phi_r along source)-(a+2/b)phi_r]/(1-V^2).

This agrees with the reflected-characteristic curvature to within 1e-17 at
the four later times on all four grids. Its local factor projections are
DIAGNOSTICS ONLY, never substituted as fitted j2 coefficients. They explain
why finite-grid behavior must not be oversold: at t=.21 on1025, the exact
curvature jump is .00709978 while the local factor projection is .00296739.
Removing the exact stationary component can therefore INCREASE the remaining
residual norm (from .0290911 to .0600463 in that case). The proof controls
both pieces asymptotically; it does not assert a pointwise residual minimizer.

Total: 343 successful current implementation checks. There are now
30 retained failed attempts in the inherited chain, including the support
checker failure below. All four original full-horizon force failures remain.
Neither these diagnostics nor the internal theorem certify an existing grid.

Evidence:
- `source-intake/navier-stokes/20260914/annular-smoothed-comparison-attempt01/status.json` — retained failed support checker.
- `source-intake/navier-stokes/20260914/annular-smoothed-comparison-attempt02/status.json` — complete327 checks.
- `source-intake/navier-stokes/20260914/annular-source-curvature-comparison-attempt01/status.json` — complete16 independent curvature checks.

The companion final-integrity file records the subsequently verified seal;
this note does not count its own future file hash as a mathematical check.

The first qualification attempt is retained as a checker failure: its
support assertion allowed six rows, but the factor contains three direct
third-difference rows AND four adjacent-combination rows. The corrected
`scripts/qualify_annular_smoothed_comparison_v2_20260918.py` proves that
seven-row bound exactly for all four rational source phases before using it.
Its numerical support check ignores only the same 2e-12 polynomial
annihilation roundoff already separately checked. No action, physical force
threshold, quadrature-control threshold, or proof exponent changes.

## 9. What this changes and the next substantive target

This supplies a constructive proof route past the old fixed-time
O(sqrt(h)) versus O(h^-1/2) obstruction for this benchmark. The essential
new step is not another audit: it is the stationary-kink corrector together
with a nonlinear-costed, endpoint-safe smoothing construction.

The substantive next target is the live-geometry system: identify whether
its constrained Hamiltonian, characteristic speeds and field/source
coercivity retain the properties used here, and derive the additional metric
residual rather than silently treating it as prescribed. The current proof
also needs independent mathematical review; the curvature/norm/cancellation
checks here are implementation qualifications and a local adversarial review,
not independent peer review.

A slow asymptotic rate with unspecified constants cannot certify an existing
numerical grid. Do not launch a larger grid merely to relabel the four old
failures, repeat the initial-window proof, or describe a prescribed-flat
reference limit as the complete MTS-to-GR limit.
