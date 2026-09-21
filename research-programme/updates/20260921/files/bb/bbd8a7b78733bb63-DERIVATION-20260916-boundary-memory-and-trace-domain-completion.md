# Boundary memory, trace domain, and a conditional relaxed action

Private continuation of `DERIVATION-20260916-boundary-capacity-and-local-source-refinement.md`.
Turn start: 2026-09-16T08:58:15Z. Four-hour check-in deadline: 12:58:15Z.

## Result in plain language

The boundary coupling is no longer represented only by a static target. Its finite-dimensional dynamic response is derived below, with its inertia, memory, initial-state contribution, and moving-source momentum retained. It reproduces the saved equations for both reference and MTS.

The trace penalty has a genuine domain issue under a specific limit: hold the original sampling stencil fixed and allow arbitrarily narrow layers. The associated positive energy form is not closable in the bare bulk kinetic L2 space. This is not a rejection of MTS or of every stronger/augmented parent domain. It rules out treating that particular bare-space completion as automatic.

A conditional, parameter-free static relaxation can nevertheless be derived explicitly. It is a new candidate branch, not a silently repaired version of the old trajectories. Neither dynamic convergence to that branch nor improved force accuracy has been demonstrated here. The previous MTS final-force failures remain unchanged.

## 1. Exact moving-source decomposition of the existing finite action

Use the previous flat spherical benchmark, with source position b, velocity V, material mass S, and the same fixed reference basis. Write u for field coordinates, B0 for the value basis and B1 for its reference derivative. Let J be the map Jacobian and k its displacement derivative with respect to b. At quadrature points define T=-(k/J) B1. Define

    M = B0^T W_t B0,
    A = B0^T W_t T,
    B = T^T W_t T,
    K = K_bulk + L_Gram^T W_Gram L_Gram.

Here W_t contains the positive kinetic quadrature measure. A is a transport matrix, not an additional coupling constant. These matrices depend on b; the prescribed metric in this checkpoint is flat and time independent. The full finite action is exactly

    L = udot^T M udot/2 + V udot^T A u
        + V^2 u^T B u/2 - u^T K u/2 - S sqrt(1-V^2).

Consequently

    p_u = M udot + V A u,
    p_b = S V/sqrt(1-V^2) + zeta,
    zeta = udot^T A u + V u^T B u.

Let a_b=bddot and let a subscript b denote a partial derivative at fixed field coordinates. The field equation is

    M uddot + C udot + F u = 0,
    C = V(M_b + A - A^T),
    F = K + a_b A + V^2(A_b-B).

The mechanical source law is

    S a_b/(1-V^2)^(3/2) + d(zeta)/dt
       = udot^T M_b udot/2 + V udot^T A_b u
         + V^2 u^T B_b u/2 - u^T K_b u/2.

No global field-momentum derivative has been discarded. In particular,

    d(zeta)/dt = uddot^T A u + udot^T A udot
        + V udot^T A_b u + a_b u^T B u
        + 2 V udot^T B u + V^2 u^T B_b u.

These identities are tested at all nine saved times for both branches at base257/splits8 and base513/splits4. Maximum field-equation residual is 1.148e-13; source-law residual is 7.611e-16. This checks an exact rewriting of the same finite equations, not agreement with GR to those tolerances.

## 2. Separate the genuinely added local modes

Write u=E x+Z z. E is the previously qualified exact quadratic embedding, x contains the retained old quadratic nodal values, and Z contains unit vectors at newly inserted nodes. There are28 local coordinates at257/splits8 and12 at513/splits4. The full field, its rates, and its acceleration can all be reconstructed this way.

Let G be the original sampled stencil, h the sampled reference hinge, W its positive weights, and r the local derivative-jump row. Then

    G Z = 0,
    L_Gram Z = -h r,
    D = h^T W h > 0,
    j_star(x) = h^T W G E x / D,
    ell x = (j E)x - j_star(x).

Thus the local Gram-dependent part of the potential is exactly

    D (ell x + r z)^2/2,

in addition to the projected vertex energy. In particular K_zz=K_bulk,zz+D r^T r and K_zx=K_bulk,zx+D r^T ell. No new coefficient has been fitted. This rank-one structure is algebraic, even though the local dynamics has many modes.

For a moving source the exact local equation is

    M_zz zddot + C_zz zdot + F_zz z
       = -(M_zx xddot + C_zx xdot + F_zx x).

Direct reconstruction of this equation agrees with the saved local accelerations within5.434e-12. A small local coordinate is not evidence that its derivative trace or acceleration is negligible.

## 3. The derived memory response

First prescribe a stationary source. Then C=0 and F=K. With generalized eigenvectors U normalized by U^T M_zz U=I and U^T K_zz U=Omega^2, define

    R(t) = U diag(sin(omega_n t)/omega_n) U^T,
    z_hom(t) = U cos(Omega t) U^T M_zz z(0)
             + U sin(Omega t) Omega^-1 U^T M_zz zdot(0).

The exact causal local solution is

    z(t) = z_hom(t)
        - integral_0^t R(t-s)[M_zx xddot(s)+K_zx x(s)] ds.

Substitution into the x equation gives memory; it does not justify instantaneous static elimination. In Laplace space the zero-initial-data operator is the Schur complement of P(s)=s^2 M+K:

    P_eff(s) = P_xx(s)-P_xz(s) P_zz(s)^-1 P_zx(s).

Nonzero local initial data produce an additional forcing term and must not be dropped. Eight independent frozen-source controls reproduce the causal solution within2.071e-15 in state. Omitting the homogeneous part in the manufactured controls produces errors between6.56e-5 and3.45e-4. These are solver-identity controls, not observed physical deviations.

For a prescribed moving b(t), the local first-order state (z,zdot) instead has the time-dependent generator

    H(t) = [[0,I],[-M_zz^-1 F_zz,-M_zz^-1 C_zz]].

Its retarded propagator Phi(t,s), together with the same coarse forcing, provides the exact time-ordered analogue of the displayed convolution. In the coupled problem b(t) and x(t) are themselves unknown; this is an implicit reduction, not a separately closed moving-source solver. The complete source equation in section1 still applies. No such reduced moving-source integration is claimed in this checkpoint.

### An explicit scalar feedback law for the trace

Let P0(s)=s^2 M_zz+K_bulk,zz and use zero local initial data for the following transfer relation. Define

    z_free(s) = -P0(s)^-1 (s^2 M_zx+K_bulk,zx) x(s),
    chi(s) = r P0(s)^-1 r^T,
    delta_free(s) = ell x(s)+r z_free(s).

Then the actual trace mismatch and local response satisfy exactly

    delta(s) = delta_free(s)/(1+D chi(s)),
    z(s) = z_free(s)-D P0(s)^-1 r^T delta(s).

The free generalized modes give chi(s)=sum_n a_n^2/(s^2+omega_0n^2), with nonnegative residues. Static attenuation is strictly between0 and1. It is not a constant attenuation at every frequency: resonant response and phase are retained, and the transfer tends to1 at sufficiently large |s| in a non-pole direction. This is a finite benchmark response, not a derived universal physical screening coefficient.

At final saved source positions, static attenuation is0.0644516 for257/splits8 and0.301350 for513/splits4. Direct finite solves and this formula agree in local state within6.60e-20 for the sampled complex frequencies and frozen positions. The actual evolving trace is not assumed to be static, and neither attenuation number measures the error relative to GR.

## 4. Why narrowing the layer creates fast modes

For a stationary flat source, place the quadratic layer u_epsilon=epsilon*s*(1-s) on the first right-hand cell, where s=(r-b)/epsilon, and set it to zero elsewhere. Its reference derivative jump is1 and every original sampled vertex value is unchanged. Its exact scalar-coordinate mass and bulk stiffness are

    m_epsilon = epsilon^3 (b^2/30+b epsilon/30+epsilon^2/105),
    k_epsilon = epsilon (b^2/3+b epsilon/3+2 epsilon^2/15).

The unchanged Gram stiffness of this direction is D. Therefore its Rayleigh frequency obeys

    omega_trial^2 = (k_epsilon+D)/m_epsilon,
    reference: epsilon^2 omega_trial^2 -> 10,
    fixed D>0: epsilon^3 omega_trial^2 -> 30D/b^2.

The maximum local eigenfrequency is at least this trial frequency. For the MTS257/splits8 control, the trial is64,864.8 and the maximum local frequency77,535.5; the corresponding reference maximum is45,107.3. These are fixed-source numerical units, not new particle frequencies. Frequency growth means stiffness, not by itself an exponentially growing instability: the frozen mass and stiffness are positive.

Both branches, two original base grids, and six subdivision counts are tested. These are algebraic spectral calculations, not additional expensive full trajectory integrations.

## 5. A conditional domain obstruction, with its proof

Fix the original stencil G, hinge h, positive W, source location, and finite one-dimensional annulus. Assume positive bounded bulk weights A_kin and C_bulk. Use the kinetic space H=L2(A_kin dr), and a dense piecewise smooth form domain with u(b)=0 and a defined one-sided derivative jump j(u). Set Q=2*potential:

    Q(u) = integral C_bulk |u'|^2 dr + ||G u-h j(u)||_W^2.

The original samples stay a positive distance from the source. Choose a smooth-cutoff layer on the right,

    v_epsilon(r)=epsilon*eta((r-b)/epsilon),
    eta(s)=s(1-s)^2 on[0,1], zero outside.

It is C1 at the outer cutoff, has j(v_epsilon)=1, and G v_epsilon=0 once epsilon is small enough. Its squared kinetic norm is O(epsilon^3); its bulk derivative energy is O(epsilon). The constants for frozen weights are integral eta^2=1/105 and integral (eta')^2=2/15.

For any two sufficiently small widths, j(v_epsilon-v_delta)=0 and G(v_epsilon-v_delta)=0. The bulk triangle inequality gives Q(v_epsilon-v_delta)<=2 Q_bulk(v_epsilon)+2 Q_bulk(v_delta), tending to zero. Thus a decreasing sequence is Q-Cauchy and tends to zero in H. But Q(v_epsilon)->D>0. This contradicts the defining closability criterion. The positive form is therefore **not closable in this bare H space under these hypotheses**.

This is stronger than merely saying bulk error fails to bound a derivative trace. It is also strictly limited: D and the original stencil are held fixed. The proof neither analyzes a simultaneous base-grid limit in which D changes nor excludes a stronger topology, an explicitly augmented trace state, or a parent-derived physical regularization. It does not reject the full parent theory.

### What direct stationarity would require

In the unrelaxed continuum variational model admitting the above arbitrarily narrow layers, vary u by g(t) v_epsilon, with g compactly supported in time. Under finite bulk kinetic/gradient norms, the bulk variation tends to zero, whereas the Gram variation tends to minus integral g(t) D[j(u)-j_star(u)] dt. A prescribed smooth timelike moving map adds transport variations supported in the same shrinking region; their norms also tend to zero. Consequently any sufficiently regular stationary path in this unrestricted variation class must satisfy

    D[j(u)-j_star(u)] = 0

in time-distributional form. This is a necessary condition from the stated action and domain, not a sufficient well-posedness theorem or permission to impose it on finite-grid solutions whose admissible variations differ.

## 6. Derive the static relaxation instead of inventing one

For the same fixed-stencil hypotheses, the lower-semicontinuous envelope in bulk H has domain H1 with the source Dirichlet condition and is

    Q_bar(u) = integral C_bulk |u'|^2 dr
             + (G u)^T [W-W h h^T W/D] (G u).

**Lower bound.** Bounded Q and the source Dirichlet condition bound the H1 norm by the one-dimensional Poincare inequality. A subsequence converges uniformly while derivatives converge weakly, so all original sampled values converge. Completing the Gram square bounds every original Q below the displayed projected term plus bulk energy. Weak lower semicontinuity supplies the lower bound.

**Recovery.** Approximate any admissible H1 function by piecewise smooth functions. For each approximation, add a sufficiently narrow layer with amplitude j_star-j(original), retaining every sampled value. Choose the width so that amplitude squared times width tends to zero. The derivative jump attains j_star while the added bulk and kinetic norms vanish. This yields the displayed upper bound. No finite amplitude bound on the approximating derivative jumps is needed because the widths can be chosen accordingly.

The projected Gram term is nonnegative and continuous on H1 in one dimension. Together with the coercive bulk part it defines a closed relaxed form. These lower/recovery arguments identify its envelope under the stated topology, not a unique fundamental parent action.

Equivalently, the energy completion admits an independent auxiliary trace eta:

    V_aug(u,eta;b)=V_bulk(u;b)+(G u-h eta)^T W(b)(G u-h eta)/2.

With no independently supplied trace kinetic term, variation in eta gives eta=j_star(u;b). The resulting conditional action uses V_bar=Q_bar/2 and the original bulk/source kinetic terms. **The auxiliary eta is not automatically the derivative trace of the limiting bulk field.** The recovery sequence illustrates exactly why those can differ. This distinction prevents disguising the relaxed model as the old finite equation with j forcibly overwritten.

Let y=Gu and rho=y-h eta_star. Envelope differentiation gives

    partial_u V_bar,Gram = G^T W rho,
    partial_b V_bar,Gram = rho^T W_b rho/2,
    partial_W V_bar,Gram = rho rho^T/2.

Terms involving derivatives of eta_star cancel because h^T W rho=0. The source covector includes minus the b derivative; the entire kinetic source current zeta remains. Numerical complex-step checks verify the field, source, and coefficient-weight derivatives. Twelve kinematic recovery sequences attain the relaxed Gram energy without deleting original rows; their remaining bulk correction tends down with layer width. They are NOT dynamically evolved solutions.

Static relaxation alone does not prove convergence of the finite Hamiltonian trajectories. High-frequency energy can survive in a vanishing-mass layer; prepared initial data and dynamical control are still needed. No physical trace inertia or damping is introduced by fiat here.

## 7. Checks, failed attempts, and decision

| Suite | Successful checks | Scope |
| --- | ---: | --- |
| Moving-source decomposition and frozen memory | 93 | Both branches; saved equations; causal controls |
| Trace-domain algebra and layer spectra | 82 | Symbolic identities and conditional spectral checks |
| Rank-one trace susceptibility | 38 | Exact feedback and finite frequency-domain comparison |
| Relaxed action and recovery | 44 | Static envelope derivatives and kinematic sequences |

Total257 implementation/algebra checks. Counts are not independent physical confirmations or machine-checked proofs of the analytical domain lemmas.

Three initial attempts are preserved: empty reference Gram arrays exposed a reduction bug; coordinate subtraction on the narrowest cell exceeded an analytic quadrature check; a symbolic positivity query returned unknown until its rational expression was factored. The corrected versions preserve the stated numerical tolerances. In the layer diagnostic only, shape values are evaluated directly at known reference Gauss fractions; no old evolution action is modified. At64 subdivisions the original coordinate-recovery mass/stiffness relative differences are about3.39e-11 and5.95e-11, recorded rather than hidden.

**Next practical step:** implement the explicitly labelled relaxed-trace candidate as a separate variational branch, retaining its derived source covector, coefficient dual, and kinetic source current. Qualify its derivatives, then run a small paired reference/MTS test under the unchanged force gates. Preserve the unrelaxed branch as the comparison. In parallel with interpretation, establish what initial-data and joint-refinement conditions would connect the finite unrelaxed dynamics to that candidate. Neither a pass nor adoption of this completion is predetermined.

This is not a full GR limit, a black-hole result, or an observational claim. The previous benchmark force failures are not relabelled. No GitHub changes, subagents, or formalization-workbench edits.

## Evidence and general mathematical context

- Exact matrix construction: `scripts/annular_boundary_response_20260916.py`.
- Dynamic response: `scripts/verify_annular_boundary_response_20260916_v2.py`.
- Domain/layer qualification: `scripts/derive_annular_trace_domain_20260916_v2.py`.
- Trace susceptibility: `scripts/derive_annular_trace_susceptibility_20260916_v2.py`.
- Relaxed-action checks: `scripts/verify_annular_relaxed_trace_action_20260916.py`.
- Dynamic evidence: `source-intake/navier-stokes/20260914/annular-boundary-dynamic-response-attempt02/status.json`.
- Domain evidence: `source-intake/navier-stokes/20260914/annular-trace-domain-and-inertia-attempt02/status.json`.
- Susceptibility evidence: `source-intake/navier-stokes/20260914/annular-trace-susceptibility-attempt02/status.json`.
- Relaxation evidence: `source-intake/navier-stokes/20260914/annular-relaxed-trace-action-attempt01/status.json`.
- Previous seal: `source-intake/navier-stokes/20260914/annular-boundary-capacity-final-integrity.json`.
- Current seal, only complete when its recorded state says so: `source-intake/navier-stokes/20260914/annular-boundary-response-final-integrity.json`.

For general context, [Jesse Peterson's operator-algebra notes](https://www.math.vanderbilt.edu/peters10/teaching/spring2020/OperatorAlgebras.pdf) discuss closed/closable positive forms, and [Chorin, Hald and Kupferman, PNAS 2000](https://www.ma.huji.ac.il/~razk/Publications/PDF/CHK00.pdf) discuss memory under elimination of unresolved variables. Search excerpts were accessible on2026-09-16; direct PDF opens timed out. Neither is represented as having been read in full or as proving any MTS-specific statement. All model-specific formulas and arguments used here are given explicitly above.
