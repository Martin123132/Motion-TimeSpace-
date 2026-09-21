# Endpoint transport bound with retained parent clock-gradient jumps

Private continuation, 2026-09-10 (Europe/London). No GitHub action.

## 1. Result, scope and remaining difficulty

The two-column moving endpoint defect F_B=B_t-D_h B now has an explicit
derived bound in terms of positive coefficient bounds, the clock's first
spatial derivative and a precisely sourced broken-curvature/jump radius.
This replaces the previous reliance on small measured defect norms.

The proof includes a discrete mass-projection graph estimate for continuous
piecewise-H2 functions whose first derivatives jump. It retains the actual
scalar-node and staggered-mass-face jumps; it does not pretend the clock is C2.
Every clock jump is expressed algebraically in the original mass/lapse fields
and their first time rates. No theta_tt or third time jet is introduced.

The bound is uniform in mesh IF those coefficient and curvature radii are
uniformly bounded. Their uniform propagation from the coupled parent equations
is NOT proved here. The numerical upper bounds are deliberately conservative:
about 894 (GR) and 3098 (Gram) at N64, versus actual defect norms about 0.00169.
Those large overestimates are not physical growth rates or evidence against MTS.

The broader paired moving-energy estimate remains separate. A manufactured
spatially linear clock has zero curvature radius but shows increasing measured
paired growth on refinement in BOTH branches. Thus the endpoint-defect proof
must not be presented as having closed the entire moving-energy estimate.

Validation: 355 commutator/coefficient checks +84 independent interpolation
controls =439 passing checks; 18 unchanged saved states, 24 manufactured
coefficient controls and 24 manufactured function/projection controls.
These are algebra and numerical-analysis tests, not empirical confirmations.

No new evolution, parent calibration, local-GR, nonlinear/DAE or horizon claim.

## 2. Exact two-column commutator reduction

Use the same matrices, endpoint lift and graph variables as
`DERIVATION-20260910-boundary-memory-correction-without-clock-differentiation.md`.
Let Pi denote the ACTUAL weighted mass projection onto the zero-endpoint C1
cubic test space, with every slope free. Thus A=-Pi(theta .) on that space.
Let ell_map be the two-column affine endpoint lift and

    B=Pi ell_map, L=M^-1 K, C=M^-1 K_t L^-1,
    D_h=C-A-L A L^-1, U=L^-1 B.

Direct cancellation in B_t-D_h B gives

    F_B=-Pi(theta ell_map)-C B-L Pi(theta U).

Choose a spatially constant theta0 (time is fixed for this estimate), set
theta_tilde=theta-theta0 and C_tilde=C-theta0 I. Then EXACTLY

    F_B=-3theta0 B-Pi(theta_tilde ell_map)
         -C_tilde B-L Pi(theta_tilde U).

The complete Gram K and K_t remain in C and L. Multiplication by constant
theta0 factors through the Gram term as well as the bulk term. No representative
field or boundary value was set to zero to obtain this identity.

For a spatially constant clock rate, all three nonconstant terms vanish and
F_B=-3theta0 B. This immediately has the uniform bound
||F_B||_(R2 to M)<=3|theta0|sqrt(m_max*length/2).

The task is therefore the graph norm of Pi(theta_tilde U), not a generic
all-directions bound on an arbitrarily large matrix.

## 3. Projection graph lemma with derivative jumps

Let h be the scalar mesh spacing and let the partition include the scalar
nodes and staggered mass faces. For continuous f, piecewise H2 on this partition,
with f=0 at the two endpoints, define

    J_h(f_R)^2=sum_internal_knots |[f_R]|^2/h,
    R_h(f)=||f_RR||_(broken L2)+sqrt(6)*J_h(f_R).

The jump convention is left trace minus right trace. The sign does not affect
the radius. This weighted jump quantity is not automatically mesh-uniform;
that is part of the hypothesis to be established for the parent path.

Construct I_h f by its nodal values and arithmetic means of the one-sided
nodal slopes; endpoint slopes use one-sided traces. This is an auxiliary
interpolant, NOT an imposed condition on physical slopes. On a scalar cell let

    T_cell=||f_RR||_cell+h^(-1/2)*sum_(internal face and cell ends)|[f_R]|.

Subtract a local affine function. The variation of f_R is at most sqrt(h)
T_cell. The cubic Hermite shape bounds give

    ||f-I_h f||_(Q,cell)<=4h^2 T_cell,
    ||(f-I_h f)_R||_cell<=5h T_cell,
    ||(I_h f)_RR||_cell<=14 T_cell.

For completeness, the right-value shape has first/second derivative suprema
3/2 and 6; the two derivative shapes have suprema at most 1 and 4. Their
unscaled shape suprema are at most one. These yield the conservative constants
4,5,14 by the triangle inequality. Exact symbolic polynomial extrema are
recorded by the independent control runner.

There are at most three relevant jumps per scalar cell and each internal
scalar-node jump is counted at most twice, hence

    (sum_cells T_cell^2)^(1/2)<=R_h(f).

Since I_h f is in the free space, Pi f-I_h f=Pi(f-I_h f). Weighted projection
contraction therefore bounds its M norm by 4sqrt(m_max)h^2 R_h(f).
The inherited cubic inverse constant 16 gives

    ||L||_M <=256(p_max+G0)/(m_min*h^2),
    G0=2p_max in the Gram branch, zero in GR.

The h^2 interpolation error cancels this h^(-2) factor. For I_h f itself,
the inherited quadrature-flux estimate and Gram H2 dual estimate give

    ||L I_h f||_M
      <=[(33p_max+G2)||(I_h f)_RR||+33L_p||(I_h f)_R||]/sqrt(m_min),
    G2=(32/sqrt(3))*p_max in the Gram branch, zero in GR.

Here L_p bounds |p_R|, and p is continuous across the partition. Thus its
product with the C1 interpolant's derivative is H1, as required by the flux
estimate; no interface delta term has been omitted.

Combining the estimates and using h<=length proves

    ||L Pi f||_M <=C1 ||f_R||_L2+C2 R_h(f),
    C1=33L_p/sqrt(m_min),
    C2=14(33p_max+G2)/sqrt(m_min)
       +1024(p_max+G0)sqrt(m_max)/m_min+5length*C1.

No inverse mesh factor remains outside the explicit jump radius. The input
must have zero endpoint trace. This does NOT restore an H1 projection theorem
for the nonzero-trace endpoint source rejected in the earlier checkpoint.

Inherited constants and hypotheses are in
`scripts/annular_uniform_energy_bounds_20260909.py` and
`scripts/annular_H1_clock_energy_20260909.py`.
Independent controls include a smooth quadratic and kinks at both scalar nodes
and staggered mass faces. The kink radius legitimately grows when a fixed
nonzero derivative jump is refined; no uniform regularity is falsely assigned.

## 4. Applying the lemma to the actual endpoint response

For a unit endpoint vector eta, let u=U eta. The old discrete elliptic bounds
for L u=B eta give

    ||u_R||<=D1*b_star, ||u_RR||<=D2*b_star,
    ||u_R||_infinity<=Dinf*b_star,
    ||u||_infinity<=sqrt(length)*D1*b_star,
    b_star=sqrt(m_max*length/2).

D1,D2,Dinf are the inherited mesh-independent elliptic constants; the actual
u is C1 cubic and therefore globally H2. It is not assumed globally H3.
Let deltaTheta bound |theta_tilde| and define

    T_theta=||theta_RR||_(broken L2)+sqrt(6)J_h(theta_R),
    Theta1=||theta_R||_L2.

For f=theta_tilde u, continuity of u and u_R gives the EXACT jump relation
[f_R]=u[theta_R]. Product differentiation and the preceding elliptic bounds imply

    ||f_R|| <=b_star*D1*(deltaTheta+sqrt(length)*Theta1),
    R_h(f) <=b_star*(sqrt(length)*D1*T_theta
                         +2Dinf*Theta1+deltaTheta*D2).

Let B_C bound ||C_tilde||_M, supplied by the earlier H1-clock transport theorem
with clock center zero and radius deltaTheta. Consequently

    ||F_B||_(R2 to M) <=b_star*(3|theta0|+deltaTheta+B_C)
       +C1*b_star*D1*(deltaTheta+sqrt(length)*Theta1)
       +C2*b_star*(sqrt(length)*D1*T_theta
                            +2Dinf*Theta1+deltaTheta*D2).

This is the explicit endpoint bound. A uniform bound on T_theta, together with
the inherited coefficient and first-derivative bounds, would close this input
to the moving boundary-memory theorem. It does not independently prove those
parent bounds, the homogeneous transport bound, or beta's time regularity.

## 5. Sourcing the clock curvature: exact parent-field identities

On an open partition cell write

    theta=N_t/N-mu_t/d, d=R-2mu=R F.

The four numerators/denominators are linear on that cell. Define the constant
Wronskians U_N=N_tR*N-N_t*N_R and U_mu=mu_tR*d-mu_t*d_R. Then

    theta_R=U_N/N^2-U_mu/d^2,
    theta_RR=-2U_N*N_R/N^3+2U_mu*d_R/d^3.

Cell endpoint extrema of the positive linear denominators give rigorous
continuous-cell upper bounds on these expressions. Their squared suprema times
cell lengths bound the actual L2 integrals. This avoids treating quadrature
samples of rational functions as certified suprema.

At every internal knot, continuity of the original fields gives

    [theta_R]=[N_tR]/N-N_t[N_R]/N^2
                 -[mu_tR]/d-2mu_t[mu_R]/d^2.

This formula is checked against direct one-sided reconstruction. All four
parent slope-jump arrays are saved. They are sourced quantities, not new
adjustable variables. Their uniform control still has to follow from the
spatially differentiated constraint/source rows and state regularity; the
algebraic identity alone does not propagate it in time.

Final actual saved states at t=0.01:

|Intervals/branch|J_h(theta_R)|T_theta upper|Actual defect norm|Derived defect upper|
|---|---:|---:|---:|---:|
|16 GR|0.0532266|0.131186|0.00213209|903.923|
|32 GR|0.0531137|0.130905|0.00181034|896.708|
|64 GR|0.0532422|0.131219|0.00168876|894.116|
|16 Gram|0.0534290|0.131683|0.00211337|3137.174|
|32 Gram|0.0531452|0.130982|0.00181106|3106.977|
|64 Gram|0.0532478|0.131232|0.00168976|3098.076|

These are conservative analytic expressions evaluated on the saved states, not
interval-arithmetic certified enclosures. The bounds pass the numerical checks
by a wide margin. Their looseness should be improved before using them for
long-time quantitative predictions; large constants are not silently replaced
by the measured small values.

## 6. Controls that distinguish endpoint control from full energy control

With N=0.82, mu=1 and a prescribed nodal N_t=N theta, the constant clock control
has F_B=-3theta B and G_H=5theta (theta=0.001). These equalities pass in both
branches on 16,32,64,128 intervals. They are coefficient-jet controls, not new
constrained solutions.

For theta given by the nodal P1 reconstruction of 0.001(R-6)^2,

    theta_RR=0 on open cells,
    J_h(theta_R)=0.002sqrt(length-h)<=0.001,
    T_theta<=sqrt(6)*0.001.

This supplies a genuinely mesh-uniform manufactured jump family and tests the
bound without suppressing its nonzero jumps.

For the exactly spatially linear clock theta=0.001(R-6), T_theta=0, but the
measured paired moving-energy rate is:

|Intervals|GR G_H|Gram G_H|GR endpoint defect norm|
|---|---:|---:|---:|
|16|0.000903534|0.000905404|0.001107439|
|32|0.001042713|0.001045636|0.001115121|
|64|0.001251636|0.001256405|0.001118942|
|128|0.001568618|0.001576036|0.001120848|

Four meshes do not prove an asymptotic divergence. They do show why zero clock
curvature is not a numerical certificate for the broader homogeneous growth
estimate. The endpoint defect and the full paired transport are distinct.
The same scrutiny is applied to GR and Gram; no physical instability is claimed.

## 7. Best next derivation

Before attempting to certify the full paired growth merely by bounding more
clock derivatives, expose the moving transport's own boundary contribution.
There is a concrete weak identity to pursue. For u=L^-1 g, set on open cells

    kappa_g=-[(p theta)_R/m]u_R-c^2 theta u_RR.

The same free-row integration by parts gives Cg as Pi kappa_g plus its Gram
rate and quadrature remainder. Since g has zero endpoint trace, the endpoint
trace of the bulk source in (C-A)g is that of kappa_g, not necessarily zero.
Thus the already constructed memory correction for the externally derived
beta need not also remove the homogeneous moving transport's boundary work.

Next evaluate and derive the feedback estimate for this state-dependent trace
using the actual released-slope equations, rather than imposing a zero trace
or replacing the weak equation by a pointwise continuum equation at the endpoint.
At the same time use the exact four-field jump identity to derive T_theta from
the differentiated parent constraint rows. The present proof already shows
how such a bound controls F_B; do not restart a missing-input inventory.

Beta variation and the zero-trace-volume/Gram/quadrature source bounds remain
necessary before actual memory integration, energy propagation and box
persistence. Full local-GR, nonlinear, DAE and horizon closure stay open.

## 8. Reproducibility

New immutable helper and runners:

- `scripts/annular_endpoint_commutator_bound_20260910.py`
- `scripts/derive_annular_endpoint_commutator_bound_20260910.py`
- `scripts/derive_annular_projection_jump_controls_20260910.py`

Completed outputs:

- `source-intake/navier-stokes/20260910/annular-endpoint-commutator-bound-derived/status.json`
- `source-intake/navier-stokes/20260910/annular-projection-jump-controls-derived/status.json`
- `source-intake/navier-stokes/20260910/annular-endpoint-commutator-bound-final-integrity.json`

The projection-controls runner's seal phase owns the combined final seal.
Do not invoke the earlier runner's seal phase as well. Derive phases require
fresh destinations and do not overwrite completed evidence.

All inherited sources and outputs are hash-checked unchanged. Scripts compile,
run single-core BelowNormal with BLAS/OMP threads set to one and create no
bytecode cache. No subagent, shared-process shutdown, new physical trajectory,
Git commit or public upload. Protected workbench verification is an mtime scan
since 2026-09-10T00:34:00Z, not a full pre-turn hash baseline.
