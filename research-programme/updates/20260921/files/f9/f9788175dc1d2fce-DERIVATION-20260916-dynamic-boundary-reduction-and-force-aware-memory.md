# Dynamic boundary reduction: initial data, feedback, and force-aware memory

Private continuation of `DERIVATION-20260916-relaxed-trace-candidate-and-paired-smoke.md` and `DERIVATION-20260916-boundary-memory-and-trace-domain-completion.md`.

Started2026-09-16T11:47:52Z; check-in deadline15:47:52Z. Original actions, trajectories and GR comparison gates remain unchanged.

## Result in plain language

We can now derive and test a rule for simplifying finite boundary dynamics without ignoring either its initial state or its back-reaction on the retained field. A static boundary minimum is generally NOT an invariant dynamical subspace. Preparing its initial state does not stop the field from driving it again.

The first general bound is valid but numerically far too pessimistic. An output-specific modal bound is much sharper and gives a constructive result: in the fixed-source286-degree-of-freedom benchmark,18 reference modes or17 MTS modes can be omitted while the analytically derived source-load envelope evaluates below2e-7. The fastest MTS mode must be retained in this selection; the fastest reference mode need not be. There is no new fit coefficient, damping, force subtraction or physical trace constraint.

This is modest finite-model compression with a derived error criterion, not a full GR limit. The reference for this comparison is the original full finite action, NOT the independent GR oracle. The numerical bounds are evaluated in ordinary floating-point arithmetic, not certified interval arithmetic. The frozen-source theorem does not establish a freely moving-source or simultaneous continuum limit.

## 1. Start from the actual action

On a fixed, prescribed flat background, the retained finite action is

    L = (u_dot^T M u_dot)/2 + V u_dot^T A u
        + V^2 u^T B u/2 - u^T K u/2 - S sqrt(1-V^2).

Here M,A,B,K depend on the source position b and include all original Gram rows. No row is deleted in forming these matrices. This turn first holds b=b0, V=0 externally. The field then obeys

    M u_ddot + K u = 0.

Both M and K must be positive definite on this finite source-Dirichlet field space. This is checked for every tested matrix; it is not asserted for every possible parent background or limiting domain.

Although b is held fixed, the field's canonical source momentum is not zero:

    zeta = u_dot^T A u.

The wave load on the constrained source is

    F[u] = u_dot^T M_b u_dot/2 - u^T K_b u/2
           - u_ddot^T A u - u_dot^T A u_dot.

The holding apparatus would supply the opposite load. This is not the acceleration of an unconstrained material source. Omitting the derivative of zeta would give the wrong observable even in this stationary control.

## 2. Exact static condensation and its missing inertial term

Use the already qualified hierarchical coordinates u=E x+Z z, where E embeds the coarse quadratic field and Z spans its local boundary additions. Define

    Kzz = Z^T K Z,    Kzx = Z^T K E,
    T = E-Z Kzz^-1 Kzx,
    Mr = T^T M T,     Kr = T^T K T,
    C = T^T M Z,     Ml = Z^T M Z.

T minimizes the full potential over the local coordinates at fixed x. It does NOT merely minimize the Gram trace square, and is not the previous relaxed-trace action. With u=T x+Z w the potential is block diagonal but the kinetic action generally is not:

    Mr x_ddot + C w_ddot + Kr x = 0,
    C^T x_ddot + Ml w_ddot + Kzz w = 0.

The static model sets w=0 and solves Mr x_ddot+Kr x=0. Therefore w=0 remains exact only for data for which C^T x_ddot stays zero. Initial preparation alone does not guarantee that condition. This identifies the continually regenerated boundary response rather than treating it as unexplained missing data.

## 3. A full-feedback error theorem

The following holds for ANY constant full-column-rank trial matrix T, including retained local-mode enrichments. Write ua=T x for the reduced solution and

    r = M ua_ddot+K ua = R x,
    R = K T-M T Mr^-1 Kr.

If u is the full solution and e=u-ua, then exactly

    M e_ddot+K e = -r.

This is an equation for the whole field error, not for local modes driven by an incorrectly assumed exact coarse trajectory. It includes feedback through the full propagator. Define

    ||(e,e_dot)||E = sqrt(e^T K e+e_dot^T M e_dot),
    E0 = ||(u0-T x0, v0-T v0r)||E,
    Er = sqrt(x0^T Kr x0+v0r^T Mr v0r).

Differentiating the squared energy and applying Cauchy-Schwarz gives

    ||(e,e_dot)(t)||E <= E0 + integral_0^t ||M^-1/2 r(s)|| ds.

Zero error-energy instants follow by regularization/continuity. No damping assumption is used. With an energy-normalized coordinate basis for Kr,

    sigma = ||M^-1/2 R Kr^-1/2||2,
    rho = sigma Er,
    E(t) <= B(t) = E0+t rho.

Here inverse-square-root notation denotes a compatible energy-coordinate factor; its orthogonal choice does not change the operator norm. In code a Cholesky whitening of M and generalized eigenvectors of (Kr,Mr) supply these factors.

For the pure static T, the residual norm also has the exact identity

    r^T M^-1 r = (C^T x_ddot)^T
        [Ml-C^T Mr^-1 C]^-1 (C^T x_ddot).

This explicitly displays the omitted inertial forcing and the positive kinetic Schur complement. The best possible initial approximation in this energy norm is derived, not fitted:

    x0 = Kr^-1 T^T K u0,
    v0r = Mr^-1 T^T M v0.

The two errors are respectively K- and M-orthogonal to range(T). Artificially preparing the FULL initial data to equal their projections is tested separately; it is never substituted into the original physical runs.

Exact invariance criterion: R=0 iff M^-1 K maps range(T) into itself. If additionally E0=0, the reduction is exact for all time. Static energy minimization by itself does not imply this invariance.

## 4. Carry the bound to the complete source load

On the full field equation the load is the quadratic observable

    F_on(u,v) = (u^T Hq u+v^T Hv v)/2,
    Hq = -K_b+K M^-1 A+A^T M^-1 K,
    Hv = M_b-A-A^T.

But ua need not satisfy the full field equation. Its actual reconstructed canonical load is

    F[ua] = F_on(ua,va)-r^T M^-1 A ua.

Thus the current-residual term must also be bounded; evaluating the on-shell quadratic at an off-shell approximation alone is insufficient. Set

    kappa = max(||K^-1/2 Hq K^-1/2||2,
                ||M^-1/2 Hv M^-1/2||2),
    xi = ||M^-1/2 A T Kr^-1/2||2.

The exact-arithmetic sufficient bound for every t in[0,Tfinal] is

    |F[u](t)-F[ua](t)|
        <= kappa [Er B(t)+B(t)^2/2] + rho xi Er.

A joint-refinement sufficiency condition is that this complete right-hand side tends to zero along the proposed mesh/layer sequence. Small initial energy, small discarded potential, or increasing local frequency alone is not enough: kappa,xi,rho and the initial-state term can scale with refinement.

This theorem is useful structurally but the unrestricted operator-norm estimate is very loose for these data: the pure-static numerical bounds range from about5.7e3 to2.3e7 while the sampled load errors are about2.2e-6 to4.9e-5. Failure of this sufficient bound is NOT a no-go theorem. It motivated the sharper observable-specific construction below.

## 5. Retarded response, including the initial state

Diagonalize the full positive pair K U=M U Omega^2, U^T M U=I. Then

    e(t) = U[cos(Omega t) U^T M e0
             + Omega^-1 sin(Omega t) U^T M e_dot0]
           - integral_0^t U Omega^-1 sin(Omega(t-s)) U^T r(s) ds.

The homogeneous term cannot be dropped. Reduced motion is a sum of sines and cosines, so each forced modal contribution is integrated analytically. For full frequency omega and reduced frequency nu the cosine and sine forcing kernels are

    C(t) = [cos(nu t)-cos(omega t)]/(omega^2-nu^2),
    S(t) = [sin(nu t)-(nu/omega)sin(omega t)]/(omega^2-nu^2).

The implementation uses their sinc forms, including coincident-frequency limits, rather than numerically subtracting nearly resonant denominators. It reconstructs the error against independently evolved full/reduced modal solutions, with both initial terms retained. This supplies an explicit causal solution of the full-feedback error equation; it is not an arbitrary memory kernel fitted to the result.

## 6. What the paired controls actually say

Pure-static controls cover both branches at(base,local splits)=(33,2),(65,2),(65,4),(65,8),(129,4),(129,8), each with original and separately prepared initial data. Duration0.4, fixed b=6.03, original field profile and field-rate samples; only the source is externally held instead of evolved. There are401 saved samples per case. All24 reductions exceed2e-7 in at least one saved source-load sample. Preparation is not a cure and in this matrix often worsens the maximum load discrepancy.

Retaining specified local normal modes yields a conservative enriched finite field action, with all induced kinetic cross terms retained. A129/splits8 comparison uses1601 samples and the same original fine initial state for both branches:

| Retained local modes out of28 | Reference max sampled load error | MTS max sampled load error |
| --- | ---: | ---: |
| 0 | 2.87434e-6 | 9.42757e-6 |
| Lowest1 | 2.40346e-6 | 4.69060e-6 |
| Highest1 | 2.87404e-6 | 9.27566e-6 |
| Lowest4 | 3.57134e-6 | 4.01422e-6 |
| Lowest8 | 1.70433e-6 | 2.04981e-6 |
| Lowest7 plus highest1 | 3.90592e-6 | 2.37741e-6 |
| Lowest14 | 7.74630e-7 | 1.12055e-6 |
| All28 | 3.86541e-13 | 6.73615e-12 |

All proper subsets in this table fail the sampled2e-7 reduction budget. Keeping all28 is a full-dimensional coordinate identity, NOT a compression success. Discrete maxima are lower bounds on possible continuous-time maxima, not certified upper bounds; the changed sample grid explains why maxima differ from the401-sample run.

The first local-enrichment attempt failed a badly scaled algebra check: the full-dimensional residual should vanish, and the test divided by that cancelling residual rather than by the stiffness scale of the terms being subtracted. The new immutable v2 keeps the2e-8 tolerance but uses the proper backward relative stiffness scale. The reference absolute residual3.23e-8 is2.54e-16 relative; MTS9.04e-8 is5.36e-16 relative. The failed script, evidence and numerical outputs are preserved. No force tolerance was relaxed.

## 7. Construct a sharper invariant, force-aware reduction

Unlike a local static subspace, ANY subset of the full normal modes is invariant when b is fixed. There is then no continually regenerated residual r: the entire error is the exact evolution of the omitted initial modes. Importantly, their source-force influence is still not determined by frequency alone.

Let modal displacement and velocity initially be a_j and d_j, with omega_j>0. Define

    aj_max = sqrt(a_j^2+(d_j/omega_j)^2),
    vj_max = omega_j aj_max,
    Q = U^T Hq U,   W = U^T Hv U,
    Cij = |Qij| ai_max aj_max + |Wij| vi_max vj_max.

For retained indices R and omitted indices O, direct expansion of the quadratic observable gives the time-uniform bound

    |F_full(t)-F_R(t)|
       <= sum_(i in R,j in O) Cij + 1/2 sum_(i,j in O) Cij.

This includes the full source-current contribution through Hq,Hv and every omitted initial amplitude. It holds for all time in this frozen, conservative finite system, not just the plotted times. It does not assume damping, equate a fast mode to its mean, or ignore cross terms. Numeric eigenpair and rounding errors are checked by residuals, not enclosed by interval arithmetic.

Ascending-frequency truncation reveals an instructive difference. The reference first falls under the evaluated2e-7 envelope at275/286 retained modes. MTS requires all286 if modes must be kept in this order. Dropping ONLY its fastest mode gives an envelope7.00915e-7 and an actual sampled error4.14422e-7. The analogous reference error is9.88446e-10. Therefore discarding a mode simply because it is the fastest is demonstrably unsafe here.

A constructive alternative starts with every mode retained and repeatedly removes the mode with the smallest rigorously derived incremental envelope cost:

    cost(i) = sum_(j in R except i) Cij + Cii/2.

Stop before the accumulated envelope exceeds the budget. This is a numerical resolution choice, not fitting a physical parameter to the GR oracle. The bound is recomputed directly after each removal; global optimality of this greedy selection is not asserted.

| Branch | Retained/full | Removed | Evaluated time-uniform envelope | Max sampled discrepancy | Fastest retained? |
| --- | --- | ---: | ---: | ---: | --- |
| Reference | 268/286 | 18 | 1.909031104873e-7 | 5.037404975821e-8 | no |
| MTS | 269/286 | 17 | 1.894980380253e-7 | 4.643267601510e-8 | yes |

Both achieve a nontrivial frozen finite reduction under this analytical criterion, with nearly the same number of retained modes. This is a useful constructive outcome after the simpler frequency cutoff looked worse for MTS. It does not establish a large speedup: only about6% of these field modes are removed, and finding the basis itself costs work. These are not errors against GR, and this entire2e-7 reduction budget cannot also be spent on discretization, evolution, geometry and reference errors in a future end-to-end comparison.

## 8. Prepared-data scaling: a precise limited statement

For the previously derived unit-trace quadratic trial layer of thickness epsilon,

    m = epsilon^3(b^2/30+b epsilon/30+epsilon^2/105),
    k = epsilon(b^2/3+b epsilon/3+2 epsilon^2/15).

Fix D>0 from the actual original Gram stencil. If eta_star(t) is a prescribed instantaneous equilibrium and w=eta-eta_star satisfies

    m w_ddot+(k+D)w = -m eta_star_ddot,

then

    sqrt(m w_dot^2+(k+D)w^2)(t)
       <= initial_error_norm + sqrt(m) integral_0^t |eta_star_ddot| ds.

For bounded driving acceleration, well-prepared initial energy and m=O(epsilon^3), this provides an explicit small-error route. With w0=1,w_dot0=0 and no drive, however, w=cos(sqrt((k+D)/m)t): its amplitude does not decay as the frequency diverges. There is no automatic relaxation of an undamped fast mode.

Six thicknesses use the sourced finite coefficient D=0.07002660590277227. The prepared scalar bound decreases as expected, while the unprepared amplitude remains1. This scalar trial reduction is not the full coupled dynamics or the mechanical source force. The full-feedback criterion and output sensitivity must still be satisfied; the scalar scaling cannot replace them.

## 9. What carries over to the moving problem

The prior same-state potential-removal force law remains valid:

    |DeltaF_same| <= A eV+B sqrt(eV),   eV=DeltaV.

All27 saved moving states satisfy it numerically. At257,t=0.4, A=1.24709, B=11.85196 and eV=1.06682e-12 give bound1.22416e-5. A sufficient potential gap for a2e-7 SAME-STATE budget is2.84760e-16. The actual trajectory-feedback term is still1.81017e-5; it is not erased by satisfying an instantaneous condition elsewhere.

For a genuine moving comparison, write the full first-order flows as f_old,f_new on a smooth convex state tube with positive coupled inertia and admissible source speed/position. In a fixed positive norm P, put d(y)=f_new(y)-f_old(y). For these two potential-related actions its acceleration block is H(y)^-1 grad(DeltaV), with zero same-state position-rate defect. If lambda(t) bounds the logarithmic norm of Df_new throughout the tube, then

    Rstate(t) = exp(integral_0^t lambda) Rstate(0)
                + integral_0^t exp(integral_s^t lambda) ||d(y_old(s))||P ds

bounds the state separation as long as both trajectories and their joining segments stay in that tube. If LF bounds the force gradient there, a sufficient evolved-force criterion is

    A eV+B sqrt(eV)+LF Rstate <= force_budget.

This follows by the mean-Jacobian error equation and the norm differential inequality. It is conditional, not a computed certificate: the required tube, stability bound, output bound and continuous-time defect control have NOT been established from nine saved samples.

There is also a direct action-level route for carrying the modal construction to a moving b. For a smooth full mass-normalized basis u=U(b)a,

    u_dot=U a_dot+V U_b a,
    A_modal=U^T M U_b+U^T A U,
    B_modal=U_b^T M U_b+U_b^T A U+U^T A^T U_b+U^T B U,
    L=|a_dot|^2/2+V a_dot^T A_modal a
       +V^2 a^T B_modal a/2-a^T Omega^2 a/2-S sqrt(1-V^2).

These expressions follow by substitution, not by inventing a coupling. The source canonical momentum in these coordinates gains p_u^T U_b a; it must not be silently identified with the old fixed-u source momentum. With all modes this is a coordinate change. With a subset, the moving connection can drive omitted modes and the frozen envelope is no longer enough.

For simple separated eigenvalues lambda_j=omega_j^2, differentiation gives

    lambda_j,b = Uj^T (K_b-lambda_j M_b) Uj,
    Ui^T M Uj,b = Ui^T(K_b-lambda_j M_b)Uj/(lambda_j-lambda_i), i!=j,
    Uj^T M Uj,b = -Uj^T M_b Uj/2.

Near degeneracy requires a cluster/projector treatment, not division by a vanishing gap. These moving-basis formulas are derived here but not implemented or numerically qualified in this turn.

## 10. Decision and next bounded target

Keep the original branch and all its memory. Do not adopt the static relaxed candidate, impose trace equilibrium, or change force gates. The real advance is a full-feedback bound plus a constructive, source-observable-aware finite reduction, and an explicit derivation of the moving connection it must inherit.

NEXT qualify that moving-basis connection against the unchanged full action and canonical source momentum on both branches. Then bound the omitted-mode drive generated by source motion, before any reduced moving run or claim of joint-refinement convergence. Preserve eigenvalue clusters and the full source-current transformation. This is a specific derivation/implementation target, not a request for invented parent numbers.

## Evidence, limits and reproducibility

Successful current suites: dynamic reduction217, prepared-data criterion36, retained local modes83, invariant modal bound26, force-aware selection7; total369 checks. These are algebra/implementation checks, not369 physics validations. One new failed attempt is preserved in addition to14 inherited failures.

All-time statements refer to the displayed exact-arithmetic finite frozen theorems. Sampled errors, matrix residuals and numerical envelope values are floating-point diagnostics; no interval-certified continuum theorem is claimed. No freely moving source pass, full GR limit, live geometry closure or new parent ownership follows. Existing measured GR discrepancies remain exactly as previously recorded.

- Shared new mathematics: `scripts/annular_dynamic_reduction_bound_20260916.py`.
- Full-feedback controls: `scripts/verify_annular_dynamic_reduction_20260916.py`.
- Prepared-data/moving instantaneous checks: `scripts/derive_annular_prepared_data_20260916.py`.
- Preserved failed enrichment: `scripts/verify_annular_retained_boundary_modes_20260916.py`.
- Correctly scaled enrichment qualification: `scripts/verify_annular_retained_boundary_modes_20260916_v2.py`.
- Invariant modal envelope: `scripts/verify_annular_invariant_modal_force_bound_20260916.py`.
- Force-aware constructive selection: `scripts/verify_annular_force_aware_modes_20260916.py`.
- Prior seal: `source-intake/navier-stokes/20260914/annular-relaxed-branch-final-integrity.json`.
- Current seal, complete only if its state says so: `source-intake/navier-stokes/20260914/annular-dynamic-reduction-final-integrity.json`.

Only post-checkpoint-work is written. No GitHub, subagents, changes to the protected workbench, deleted failures, hidden damping, or revised physical thresholds. All own computations finished; integrity sealing follows.
