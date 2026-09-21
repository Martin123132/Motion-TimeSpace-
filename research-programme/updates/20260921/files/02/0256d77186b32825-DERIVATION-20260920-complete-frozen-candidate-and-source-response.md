# Complete frozen candidate field action and moving-source reaction

Private continuation of `DERIVATION-20260920-nonuniform-Gram-action-and-stable-atoms.md`.

Status: COMPLETE for action assembly, independent source-reaction controls, and the short homogeneous scalar-block pilot. This is a candidate on the original prescribed, static physical metric. It is not the complete coupled parent/gravity action, a new self-consistent metric solution, or a GR-limit result. Original live dynamics and previous discrepancies are unchanged.

## 1. What this stage actually builds

The preceding stage defined a positive nonuniform Gram functional and a stable local derivative-atom evaluator. This stage assembles that candidate with the original mass, gradient, moving-coordinate transport and source-inertia sectors on the SAME 1,094-DOF common P2 space. It derives the complete prescribed-background source reaction by eliminating the field acceleration, rather than calling a partial potential derivative a force.

There are three cases: the reference branch without an extra Gram term, the primary MTS numerical extension, and the alternative positive extension. Each branch keeps its own saved original coarse physical geometry. The two MTS extensions share all non-Gram inputs exactly. The reference is a numerical baseline, not a proof that GR has been recovered.

All numerical quantities retain the parent calculation's coordinate/normalization conventions. The time interval below is not assigned seconds, and the frequency bounds are not assigned hertz. Decimal arithmetic improves evaluation of the saved problem, not the accuracy or physical provenance of its original binary64 data.

## 2. Full frozen field action

Let xi be the reference coordinate, X the physical source position, V=X_dot, and

    r=r(xi,X), J=r_xi, chi=r_X, b=chi/J,
    c=r^2 N U, U=sqrt(1-2 mu/r),
    m=J r^4/c, q=c/J.

N and U are the original, prescribed physical metric functions. Their dependence on r must be differentiated when X changes, even though the physical metric profile itself is frozen. With P2 field vector u and coefficient rate v=u_dot,

    L_w = v^T M v/2 - V v^T B u + V^2 u^T C u/2 - u^T K u/2,
    M_ij = integral m N_i N_j dxi,
    B_ij = integral m b N_i N_j' dxi,
    C_ij = integral m b^2 N_i' N_j' dxi,
    G_ij = integral q N_i' N_j' dxi,
    K = G + H^T diag(P q_nodes) H.

N_i denotes a basis function here, not the lapse. H is the previous local derivative-atom Gram factor, including the original source-hinge compensation. P is the sourced positive coefficient sampler. The reference case has no Gram contribution. No physical mode is dropped and no projected mass inverse is used.

The fixed reference knots and source anchor make H independent of PHYSICAL X in this chart. The alternative's gap-distortion multiplier is also X-independent here, so its physical source derivative is included without a missing eta_X term. This does NOT qualify moving reference knots, remeshing, or that alternative's general mesh variation. It refines, rather than erases, the previous stage's limitation.

### Source derivatives at a fixed physical metric

Writing a for the reference source anchor,

    J_X = 1/(a-r_inner) on the left,
    J_X = -1/(r_outer-a) on the right,
    c_r/c = 2/r + (log N)_r + (-mu_r/r+mu/r^2)/(1-2mu/r),
    m_X = m [J_X/J + chi(4/r-c_r/c)],
    q_X = q [chi c_r/c-J_X/J],
    b_X = -b J_X/J.

B_X and C_X use (m b)_X and (m b^2)_X, respectively. K_X includes both G_X and H^T diag(P q_X) H. Derivatives remain within this fixed-topology chart.

An independent complex-step check tests m_X, q_X and b_X for both branches at both quadrature orders. The old mass/gradient density arrays are reproduced bit-for-bit, and their common-space moments agree within 1e-40. Across all eight assembled bulk matrices, changing Gauss order32 to64 changes the max entry difference, normalized by max(1,max entry), by at most 6.92e-15. These are assembly controls, not force-convergence results.

## 3. Derive the actual source Schur reaction

The dust contribution is the original prescribed-background point-source action

    L_d = -m_s sqrt(N(X)^2 - V^2/U(X)^2),
    I_d = partial_V^2 L_d,
    D_d = partial_X L_d - V partial_X partial_V L_d.

Define

    p_u = M v - V B u,
    p_X,w = -v^T B u + V u^T C u,
    c_vec = -B u.

Direct Euler-Lagrange differentiation gives the coupled acceleration equations

    M u_ddot + c_vec X_ddot = R_u,
    c_vec^T u_ddot + (I_d+u^T C u) X_ddot = D_d+R_X,w,

where

    R_u = -K u + V(B-B^T-M_X)v + V^2(C+B_X)u,
    R_X,w = v^T M_X v/2 + v^T B v - 2V v^T C u
            - V^2 u^T C_X u/2 - u^T K_X u/2.

The B_X terms cancel in the second equation after differentiating source momentum. They do not cancel in the first equation or in partial_X L_w. Eliminating the field acceleration yields

    Q = u^T C u - c_vec^T M^-1 c_vec,
    J_free = R_X,w - c_vec^T M^-1 R_u,
    X_ddot = (D_d+J_free)/(I_d+Q),
    F_w,reduced = I_d X_ddot-D_d
                = (I_d J_free-Q D_d)/(I_d+Q).

This is the full finite-dimensional source reaction for the stated prescribed-background action. It is not the reaction of a newly solved dynamical gravitational field.

In contrast,

    partial_X L_w = v^T M_X v/2 - V v^T B_X u
                    + V^2 u^T C_X u/2 - u^T K_X u/2

is only a partial covector. The distinction is substantial: in the primary saved initial state it is about -6.98196e-4, whereas the reduced source reaction is about -8.78480e-9. These cannot be substituted for one another.

### Positivity has a structural explanation

In the positive m-weighted inner product, let f=b u_xi and let Pi be the orthogonal projection onto the common finite-element field space. Since B u is the load vector of f,

    Q = ||f||_m^2 - ||Pi f||_m^2 = ||(I-Pi)f||_m^2 >= 0.

Thus the field contributes nonnegative Schur inertia in the ideal discretization; positive dust inertia gives a positive total denominator. This is a projection identity, not an added stabilizing coefficient. It also holds for a consistently positive quadrature inner product. Measured Q is checked without clipping it to zero.

### Independent controls

A separate two-field model is differentiated symbolically from its whole dust-plus-wave Lagrangian. Its full velocity Hessian and Euler right-hand side are solved directly at three source velocities, including zero and both signs. The largest absolute difference from the Schur implementation is 1.61e-18 at the predeclared 3e-12 arithmetic gate. All three negative controls reject treating partial_X L_w as the reaction.

The assembled H bilinear reproduces the preceding 72-digit local-atom values at the actual saved initial and final field/adjoint profiles, for both extensions, within 2.30e-59. Those four comparisons are fixed-profile checks, not new physical trajectories.

## 4. Metric variation: an explicit input to the next gravity step

The field kinetic density is m tau^2/2, with tau=u_dot-V b u_xi. At fixed reference chart, fields and source variables,

    delta L_bulk/delta c = -[J r^4 tau^2/c^2 + u_xi^2/J]/2,
    partial L_Gram/partial q_nodes = -P^T(Hu)^2/2.

The latter nodal covector is exported separately for each extension and checked against an independent directional contraction. Its conversion to a physical-c covector requires division by the nodal J. It must not be inserted unchanged into a c- or lapse-equation.

This also gives a useful sign result. Because c=r^2 N U, a metric variation at fixed r has delta c/c=delta N/N+delta U/U. Consequently the bulk metric variation is minus the positive kinetic-plus-gradient density times that logarithmic variation. The Gram part adds nodal nonnegative energy weights

    e_Gram,i = q_i [P^T(Hu)^2]_i/2 >= 0,
    delta L_Gram = -sum_i e_Gram,i (delta N_i/N_i + delta U_i/U_i).

These formulas identify the candidate field load for a variational metric solve; they do not solve its radial constraint or supply missing gravity/boundary equations. The original metric was generated using the original action, so it cannot simply be renamed the candidate's self-consistent metric.

## 5. Frequency bound and short-run scope

Let D=diag(M), rho=max_i sum_(j!=i)|M_ij|/M_ii, and kappa=max_i sum_j|K_ij|/M_ii. For symmetric positive M,K and rho<1,

    M >= (1-rho)D,
    omega_max <= sqrt(kappa/(1-rho)).

The computed rho is about0.750030635. All positive mass pivots are retained. Bounds below use the assembled decimal matrices, not outward-rounded interval arithmetic, and cover all modes rather than discarding fast ones.

| Case | Computed frequency bound | Steps for T=4e-5 |
|---|---:|---:|
| Reference | 1,622,683.45 | 17 |
| MTS primary | 2,395,028.45 | 24 |
| MTS alternative | 2,460,907.37 | 25 |

The pilot deliberately evolves only the HOMOGENEOUS FROZEN SCALAR BLOCK

    u_dot=v, v_dot=-M^-1 K u.

It does not evolve the source, its nonzero saved velocity, or the metric. The full source formula is evaluated at the pilot endpoints with the saved X,V,I_d,D_d as parameters. It is a diagnostic on a restricted path, NOT the force of a coupled trajectory and NOT the full moving-source linearized operator. The conserved pilot energy is (v^T Mv+u^T Ku)/2, not the energy of the omitted coupled dynamics.

The interval is exactly the original saved binary64 value of4e-5. Every branch is run at32digits/Taylor48 and48digits/Taylor64, with a full48-digit backwards recovery. A separate two-field75-digit dense matrix exponential checks the propagator independently (difference8.14e-50). No low-mode filter or fitted coupling is introduced.

### Pilot results

The complete three-case calculation, including both arithmetic settings and backwards recovery, took370.53seconds on one actual single-core worker. All predeclared arithmetic gates passed.

| Case | Initial reduced source diagnostic | Final reduced source diagnostic | Relative energy drift,48digits |
|---|---:|---:|---:|
| Reference | -9.42881811e-9 | -5.66495464e-8 | 7.34e-45 or less |
| MTS primary | -8.78480462e-9 | -5.70999472e-8 | 3.65e-45 or less |
| MTS alternative | -8.78480144e-9 | -5.66964859e-8 | 2.45e-45 or less |

At32digits the largest relative energy drift is9.48e-29, below its1e-20 gate. The largest32/48-digit endpoint difference in the energy norm is2.97e-29; the largest relative source-diagnostic change is1.27e-23, below its1e-19 gate. Backwards recovery changes the phase by at most4.39e-45 in the energy norm, below its1e-32 gate. These strong numbers qualify arithmetic of the fixed saved matrices only: not spatial resolution, new physical digits, or a continuum/coupled conservation theorem.

The primary and alternative endpoints differ by only4.90316e-10 in the primary phase-energy norm, but their reduced source diagnostics differ by4.03461e-10, or0.706588% of the primary diagnostic magnitude. Thus a tiny global field difference can coexist with a materially larger relative difference in this cancellation-sensitive source quantity. This difference is much larger than the arithmetic-refinement change. It is measured discretization-extension sensitivity on this pilot, NOT a0.71% error estimate against physical truth.

Although the alternative happens to give a source diagnostic closer to the reference here, that is not a principled way to choose the numerical action. The reference uses its own background, and the restricted pilot omits the actual moving-source/gravity feedback. No branch is declared a physical winner.

## 6. Decision and next substantive step

The substantive advance is now executable: a full prescribed-background candidate field action, its derived moving-source Schur reaction, a positive-inertia explanation, and the explicit bulk/nodal metric load needed to couple that candidate back to gravity. The all-mode scalar pilot works without deleting fast modes or fitting new physical coefficients.

The next discriminating calculation is JOINT spatial refinement of the common P2 field space and the Gram knots, starting from the same embedded physical initial field, for the reference and both MTS extensions. Recompute the full source diagnostic and determine whether extension sensitivity shrinks; arithmetic convergence alone is no substitute. Do not repeat source-cell-only halving with fixed bulk resolution or choose the extension by proximity to the reference. One additional refinement can test direction and sensitivity, but cannot by itself certify a continuum rate.

After that numerical decision, assemble the candidate's radial metric-constraint load from Section4 with the original gravity/boundary terms, solve a self-consistent initial metric, and only then attempt a short coupled source/field/gravity evolution. Both the constraint solution and its variation must belong to the new candidate action. If the two consistent extensions do not approach the same resolved behaviour, the numerical continuum identification needs work before proceeding to a physical conclusion.

The original12.5718% impulse,13.5770% fine/continuum endpoint and32.5535% coarse64/fine endpoint discrepancies, with their different denominators, remain unchanged. Neither these new endpoint diagnostics nor their smaller extension difference replaces those tests. Parent uniqueness, initial-layer control, any needed remeshing, actual physical force convergence and the full GR limit remain open.

## Evidence and preservation

- Assembled action and source formula: `scripts/annular_common_frozen_candidate_20260920.py`.
- Assembly evidence: `source-intake/navier-stokes/20260914/annular-complete-frozen-candidate-attempt01/status.json`.
- Independent controls and metric covectors: `source-intake/navier-stokes/20260914/annular-complete-candidate-controls-attempt01/status.json`.
- Homogeneous scalar pilot: `source-intake/navier-stokes/20260914/annular-common-candidate-response-attempt01/status.json`.
- Preceding immutable seal: `source-intake/navier-stokes/20260914/annular-nonuniform-Gram-final-integrity.json`.

The three completed runs contain102 assembly/source checks,29 independent-control/source checks, and32 pilot/source checks:163 scoped checks, all passed, with no new failed execution. The52 historical failed executions remain preserved. Validation counts concern implementation and provenance, not independent physical confirmations.

Private post-checkpoint-work only. One actual single-core BelowNormal worker, no subagents or GitHub action. Executed sources and all earlier evidence remain immutable. The sibling-workbench preservation check is a modification-time scan since2026-09-20T16:32:37Z, not a pre-turn whole-tree hash baseline.
