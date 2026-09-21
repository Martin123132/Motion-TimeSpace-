# Moving spectral connection and the force from omitted modes

Private continuation of `DERIVATION-20260916-dynamic-boundary-reduction-and-force-aware-memory.md`.
Started2026-09-16T12:41:39Z; four-hour check-in deadline16:41:39Z.

## Outcome

The moving-coordinate connection is now implemented and checked against the unchanged full action, canonical momenta, velocity Hessian, energy and off-shell Euler-Lagrange equations. We also derive analytic spectral curvature, a cluster-safe derivative rule, the source-force change caused by omitted moving modes, and a canonical-momentum-preserving preparation rule.

This is an advance from the frozen-source construction. It is NOT yet a freely evolved reduced solution or a GR-limit proof. No original action, original trajectory, physical threshold or public repository is changed.

The source-force fixture comparison is deliberately symmetric. With cluster-complete retained masks and the derived preparation, MTS satisfies the2e-7 instantaneous comparison budget at all six fixtures; the reference exceeds it at the final moving fixture by about10.5%. A numerical reduction can fail on either branch. This is not evidence that GR fails or that MTS beats GR: the comparison is reduced-versus-full finite action, not either theory against an independent GR oracle.

## 1. Exact moving-coordinate action

Retain the previous prescribed-metric action, with b the moving source and V=b_dot:

    L = u_dot^T M u_dot/2 + V u_dot^T A u
        + V^2 u^T B u/2 - u^T K u/2 + L_material(b,V).

All original Gram rows remain in K. The full mass-normalized spectral frame satisfies K U=M U H, U^T M U=I. At the chosen expansion point H is diagonal with entries lambda_j=omega_j^2. Within transported spectral clusters it need not stay diagonal nearby.

For u=U(b)a,

    u_dot = U a_dot+V U_b a,
    Acal = U^T M U_b+U^T A U,
    Bcal = U_b^T M U_b+U_b^T A U+U^T A^T U_b+U^T B U,
    Lnew = |a_dot|^2/2+V a_dot^T Acal a
           +V^2 a^T Bcal a/2-a^T H a/2+L_material.

In the flat controls L_material=-S sqrt(1-V^2). For the prescribed curved controls the existing lapse/root clock and its derivatives are retained, not replaced by the flat expression.

The transformed canonical momenta are

    p_a = U^T p_u = a_dot+V Acal a,
    p_b,new = p_b,old+p_u^T U_b a
            = p_b,material+a_dot^T Acal a+V a^T Bcal a.

The added term is a coordinate-connection contribution, not a new physical source force. Identifying the transformed source momentum with the old one without this term is incorrect. In the16 qualification states its absolute size reaches1.38072e-5 in benchmark units.

With J=[[U,U_b a],[0,1]], the velocity Hessian obeys Hkin,new=J^T Hkin,old J and the energy is unchanged. The EL residuals obey, even off shell,

    EL_a,new = U^T EL_u,old,
    EL_b,new = EL_b,old+(U_b a)^T EL_u,old.

Second-frame terms cancel from this transformation identity. The first qualification uses a local polynomial frame jet and therefore verifies the coordinate law without pretending its numerical second jet is a certified spectral curvature. The later derivation supplies the analytic curvature separately.

Sixteen states span base33/splits2 and base65/splits4, both branches, prescribed background masses0 and0.7, b=6.03/6.035 and V=0.06. The193 successful checks include independent complex-step action/source derivatives, full coupled inertia and on-/off-shell residual controls. Maximum EL covariance discrepancy is9.854e-16. These are finite-action checks, not live-geometry qualification.

## 2. Cluster-safe first derivatives

Define N=U^T M_b U, Q=U^T K_b U and C=U^T M U_b. For indices in different spectral clusters,

    Cij = (Qij-lambda_j Nij)/(lambda_j-lambda_i).

Inside each cluster choose Cij=-Nij/2. This is a mass-normalized parallel gauge at the expansion point, not an assertion that each degenerate eigenvector has a unique derivative. Then

    U_b=U C,
    H_b=Q+C^T Lambda+Lambda C.

H_b is block diagonal across clusters, but its internal cluster blocks generally are dense. This avoids division by internal zero or small gaps.

For a cluster I the physical subspace projector is

    P_I=U_I U_I^T M,
    P_I,b=U_I,b U_I^T M+U_I U_I,b^T M+U_I U_I^T M_b.

It is independent of orthogonal frame rotations within the cluster. An exact-degeneracy synthetic control verifies the projector derivative and the differentiated identity P_b P+P P_b=P_b, including a splitting pair. This is an algebra control, not additional physical evidence.

A truncation must retain a whole near-degenerate cluster or none of it. An individual mode label is not a robust physical object at a crossing. The finite numerical cluster policy used for curvature/motion fixtures merges adjacent eigenvalues separated by at most1e-3 times their local scale. This is a coordinate-conditioning setting, not a physical coupling or fit to observations. The same rule is applied to both branches. No uniform-in-b spectral-gap proof is claimed from a few tested positions.

## 3. Analytic second derivatives, not a guessed curvature

For the qualified prescribed constant-mass metric, let alpha=2 m_background. The actual coefficient is r(r-alpha), with r=r_ref+k(b-b_anchor) and J affine in b. Put

    f(r)=r^3/(r-alpha),
    f'(r)=2r+alpha-alpha^3/(r-alpha)^2,
    f''(r)=2+2alpha^3/(r-alpha)^3.

The mass quadrature weight is w J f; hence its first/second b derivatives are

    w(J_b f+J k f'),
    w(2 J_b k f'+J k^2 f'').

The transport weight is -w k f, the transport-square weight is w k^2 f/J, and the spatial/Gram nodal weight is r(r-alpha)/J. Differentiating these expressions gives M_b,M_bb,A_b,A_bb,B_b,B_bb,K_b,K_bb without differencing neighboring matrices. The code rejects an unqualified metric coefficient or background_mass=None rather than silently using these formulas for live/time-dependent geometry.

The analytic first derivatives agree with the existing complex-step derivatives, and the analytic second derivatives agree with complex-stepping the independently written first-derivative expressions. All four matrix families are tested on both branches and both prescribed backgrounds.

For the spectral second derivative, set N2=U^T M_bb U and Q2=U^T K_bb U. Write U_bb=U D and define

    R2 = Q2+2 Q C-N2 Lambda-2 N C Lambda-2(N+C)H_b,
    S2 = -2 C^T C-2 C^T N-2 N C-N2.

In different clusters use Dij=R2ij/(lambda_j-lambda_i). Within a cluster use Dij=S2ij/2, choosing a local polar-alignment gauge for the second jet. Then

    H_bb = R2+Lambda D-D Lambda,
    D+D^T=S2.

These follow by differentiating K U=M U H and U^T M U=I twice. Block stiffness remains symmetric and block diagonal across clusters. The gauge is local; this is not yet a global mode-tracking implementation.

Independent aligned-frame finite differences check the analytic curvature. The curvature is NOT taken from those finite differences. The62-check suite also includes the synthetic exact-degeneracy and projector tests.

### Numerical failures preserved

Three failed attempts are retained, not overwritten:

- The first moving-frame qualification used a fixed2e-6/1e-6 difference pair. A rapidly changing MTS pair needed further refinement; two consecutive smaller controls pass the unchanged2e-4 relative derivative tolerance.
- The first curvature check used steps too small for a second finite difference, amplifying roundoff. Widening the step ladder exposed the competing issue of mode-label swaps.
- The second curvature attempt still treated close reference modes separately. Completing their clusters allowed accurate aligned comparisons without dividing by tiny internal gaps. The final run keeps the3e-3 curvature-control tolerance and requires two consecutive acceptable steps.

Thus both under-resolution and overly small finite-difference steps can mislead. The failures concern numerical derivative controls, not failures of the parent physics. No physical force gate was loosened.

## 4. Derive the omitted-mode drive

Mass normalization makes the exact full modal field equation

    a_ddot+V(Acal-Acal^T)a_dot
      +[H+b_ddot Acal+V^2(Acal_b-Bcal)]a=0.

The new implementation derives Acal_b using the analytic U_bb and matrix derivatives. There are three separate motion-driven sources for otherwise omitted modes: a velocity term, a speed-squared term, and a source-acceleration term. Even V=0 does not make a freely accelerating source equivalent to an externally held source.

At a state with a_O=a_dot,O=0, let R/O denote retained/omitted indices, c=Acal a, h the full source inertia, and r the EL force minus the convective momentum derivative, so

    [[I,c],[c^T,h]] [a_ddot,b_ddot]^T = [r_a,r_b]^T.

Define s=h-c^T c and s_R=h-c_R^T c_R. The variationally reduced source acceleration is

    b_ddot,R=(r_b-c_R^T r_R)/s_R,
    f_O=r_O-c_O b_ddot,R.

f_O is the omitted field-equation residual left by the reduced acceleration. Exact Schur elimination gives

    b_ddot,full-b_ddot,R = -c_O^T f_O/s,
    DeltaF_same = -mu_material c_O^T f_O/s,
    |DeltaF_same| <= mu_material ||c_O|| ||f_O||/s.

For the flat source mu_material=S/(1-V^2)^(3/2). The same-state material momentum-rate difference has no extra metric-position contribution because position and speed are held equal in that comparison.

This is the derived instantaneous force effect of omitted motion-driven modes, not a correction subtracted from a result. The full transformed source acceleration is also checked against the unchanged original-coordinate solver.

The full acceleration defect is available, not just its source component:

    delta b_ddot=-c_O^T f_O/s,
    delta a_ddot,R=-c_R delta b_ddot,
    delta a_ddot,O=f_O-c_O delta b_ddot,
    ||delta acceleration||Hkin^2=||f_O||^2+(c_O^T f_O)^2/s.

This supplies the driving defect for a propagated state-error estimate. It does NOT remove the need to bound its accumulation and the nonlinear response along an actual trajectory.

## 5. Preserve canonical momenta when preparing the reduced state

Simply discarding a_dot,O is not the correct kinetic projection in a moving frame. Because p_a=a_dot+V Acal a, preserving a_R and p_R at fixed b,V requires

    a_dot,R,prepared = a_dot,R,full+V Acal_RO a_O,full.

This is also the minimizer of the positive physical field kinetic-error norm at fixed retained position. In original coordinates it gives

    U_R^T [M delta u_dot+V A delta u]=0.

The discarded initial state is not reset to zero in the error accounting. Its measured positive field error norm is

    Eprep^2=delta u_dot^T M delta u_dot
        +2V delta u_dot^T A delta u+V^2 delta u^T B delta u
        +delta u^T K delta u.

Retained field momenta are preserved; total source canonical momentum is not additionally imposed, since b,V are held fixed for this comparison. The physical initial fine state remains the reference, and its projection discrepancy is recorded explicitly.

The original frozen tail envelope is NOT automatically a bound on this moving preparation. We therefore separate

    F_full(original)-F_reduced(projected)
      = [F_full(original)-F_full(projected)]
        +[F_full(projected)-F_reduced(projected)].

Only the second bracket is controlled by the instantaneous omitted-drive law above. The first is the preparation effect and cannot be silently discarded. A preliminary coordinate-rate-projection diagnostic is preserved; the canonical-momentum projection is the current qualified preparation.

## 6. Paired finite fixtures and honest outcome

Use the same129/splits8 full field (286 degrees of freedom) as the prior frozen comparison. Completing the frozen masks under the curvature-safe cluster policy retains271 reference modes and273 MTS modes, rather than268/269. Retaining more modes lowers the old frozen envelope to1.65524e-7/reference and1.59219e-7/MTS; those remain frozen bounds only.

Fixtures are exact frozen full-field states at phases0,0.2,0.4, each assigned source speed0 or0.06 at b=6.03. They are legitimate states for testing the moving action, but are NOT samples from a freely moving reduced trajectory. Each is projected using the derived canonical-momentum rule. No empirical data, independent GR oracle, fitted coupling or new damping enters this test.

| Branch | Phase | V | Same-state force bound | Total observed preparation+omission force difference |
| --- | ---: | ---: | ---: | ---: |
| Reference | 0 | 0 | 2.79601e-12 | +2.84770e-8 |
| Reference | 0 | .06 | 5.96334e-10 | +2.83892e-8 |
| Reference | .2 | 0 | 3.87920e-9 | -2.02853e-9 |
| Reference | .2 | .06 | 3.98101e-8 | -2.55812e-8 |
| Reference | .4 | 0 | 1.33231e-8 | -8.55386e-9 |
| Reference | .4 | .06 | 2.30598e-7 | +2.21013e-7 |
| MTS | 0 | 0 | 6.83383e-13 | +2.69684e-8 |
| MTS | 0 | .06 | 4.70369e-10 | +2.70203e-8 |
| MTS | .2 | 0 | 1.26489e-9 | -6.51231e-9 |
| MTS | .2 | .06 | 1.56364e-8 | -1.45905e-8 |
| MTS | .4 | 0 | 4.30670e-9 | +2.36694e-10 |
| MTS | .4 | .06 | 8.63625e-8 | +8.49183e-8 |

The reference final moving fixture fails the2e-7 budget in both sufficient bound and observed total discrepancy. MTS has no failure among these six fixtures. This supports investigating the reduction, not ranking the fundamental theories. The masks are only frozen-qualified numerical approximations, so failure on the reference is a warning not to mistake approximation error for new physics.

At the final MTS moving fixture, the norms of the separate velocity, speed-squared and source-acceleration drives are1.64031e-4,7.68490e-6 and7.96808e-6. The total omitted drive is1.60992e-4: cancellation and signs matter. A source-held calculation would miss these contributions.

The source-force difference induced by projection is explicitly included in the table; the corresponding field preparation norm is about2.925e-7/reference and1.105e-6/MTS. Neither quantity has been uniformly propagated in time. A same-state success is not an evolved-error certificate.

## 7. Next implementation, now with explicit equations

The next bounded target is a smoothly transported, cluster-complete retained subspace and a short paired reduced/full moving evolution. A practical local chart is W(b)=P_R(b)U_R(b0), followed by M(b)-orthonormalization while its Gram matrix remains nonsingular. That avoids identifying near-crossing individual mode labels as physical objects. Its first/second derivatives and source momentum must follow the same pullback rules verified here; abruptly re-diagonalizing and discarding the connection is not an allowed shortcut.

Use the derived omitted residual f_O to drive the error estimate and to request numerical enrichment when needed. A frozen force budget alone is inadequate, as the reference fixture demonstrates. Initial projection, integrated defect, full source momentum, spectral-cluster crossings, and time-integration error must all remain in the accounting. Do not declare the original GR gate passed from these state fixtures or tune an added physical coefficient to suppress their force differences.

This is not a full GR limit, live metric variation, global spectral-gap theorem or completed moving reduced solver. All original parent-action and continuum claims remain at their prior status.

## Evidence and reproducibility

Successful suites: moving connection193, clustered curvature62, preliminary coordinate-rate projection78, canonical-momentum projection102; total435 implementation/algebra checks. These are not435 independent physical successes. Three new failed numerical attempts and one failed literal-wording integrity check are preserved in addition to15 inherited failures. The first sealer looked for “NOT a freely evolved reduced solution” while this note says “NOT yet a freely evolved reduced solution”; the versioned correction changes that wording check, not the scientific scope or evidence.

- Frame/projectors and local pullback: `scripts/annular_moving_spectral_frame_20260916.py`.
- Preserved failed moving qualification: `scripts/verify_annular_moving_spectral_connection_20260916.py`.
- Converged qualification: `scripts/verify_annular_moving_spectral_connection_20260916_v2.py`.
- Analytic matrix/basis curvature: `scripts/annular_moving_spectral_curvature_20260916.py`.
- Preserved curvature attempts: `scripts/verify_annular_spectral_clusters_20260916.py`, `scripts/verify_annular_spectral_clusters_20260916_v2.py`.
- Qualified cluster/curvature controls: `scripts/verify_annular_spectral_clusters_20260916_v3.py`.
- Preliminary force law: `scripts/derive_annular_motion_driven_mode_force_20260916.py`.
- Current force law and canonical preparation: `scripts/derive_annular_motion_driven_mode_force_20260916_v2.py`.
- Prior seal: `source-intake/navier-stokes/20260914/annular-dynamic-reduction-final-integrity.json`.
- Failed wording-check seal: `source-intake/navier-stokes/20260914/annular-moving-spectral-final-integrity.json`.
- Current seal, complete only if its state says so: `source-intake/navier-stokes/20260914/annular-moving-spectral-final-integrity-v2.json`.

Only post-checkpoint-work writes; no GitHub, subagents, original-action changes, removed failures or modified protected workbench. One single-core numerical worker at a time. All own numerical calculations finished; integrity sealing follows.
