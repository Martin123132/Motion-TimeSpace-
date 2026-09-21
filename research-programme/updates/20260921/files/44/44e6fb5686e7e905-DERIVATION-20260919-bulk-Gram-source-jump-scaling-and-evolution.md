# Bulk Gram refinement and the source-jump stiffness law

Private continuation of `DERIVATION-20260919-live-canonical-exponential-step.md`. The previous evolved source-cell refinement reduced the reference discrepancy but not the MTS discrepancy. The evaluated force split placed most of the latter in the remaining drive J, not the explicit source projection inertia Q. This stage changes spatial resolution, not the action rule, physical force, matter coupling, initial profile, or retained Gram modes. It does not establish the full GR limit.

Headline: actual joint refinement reduces the MTS short-endpoint force discrepancy by41.87%, after a further time check; it remains13.58% of the instantaneous continuum force and changes sign across the spatial refinement. The new derivations identify separate source-cell and bulk-Gram scales, a provable frozen scalar frequency lower bound, and an unresolved-front mechanism in an exact local fixture. The live MTS drive is still dominated by explicit projected Gram work, not the GR pressure trace. This is measurable progress and a sharper recovery target, not completed GR recovery.

## 1. Two distinct spatial scales

The scalar P2 mesh has fine source-adjacent lengths delta_left/right. The Gram stencil still samples the original uniformly spaced base vertices, spacing h. Source-cell subdivision at fixed base_count leaves the original Gram stencil and its hinge support unchanged. Increasing base_count changes the grid-dependent finite Gram matrix according to its existing definition; this is NOT exact equality of the two finite matrices, and no such nested-action claim is made for a changing base grid.

The actual source-adjacent lengths matter, not merely the requested cap. For257/cap2e-5 both are1.953125e-5. For513/cap1e-5 they are7.32421875e-6 and9.765625e-6. The bulk spacing halves from0.00625 to0.003125. Anchor location within its bulk cell also changes, from phase0.8 to0.6.

## 2. Exact lifted Gram block

Let D be the existing Gram factor on base-vertex samples, j the source derivative-jump functional, r=D applied to the unit hinge max(R-b,0), and W the existing positive row coefficient divided by h. The actual lifted factor is B=D-r j^T. Therefore, without discarding any term,

    K_Gram=B^T W B=A-b_mix j^T-j b_mix^T+mu j j^T,
    A=D^T W D,    b_mix=D^T W r,    mu=r^T W r >= 0.

For scalar coordinates u, with Delta=j^T u,

    E_Gram=1/2 u^T A u-Delta b_mix^T u+1/2 mu Delta^2.

The two mixed terms are essential. The isolated dyad mu j j^T is NOT the full Gram operator and supplies no general coercivity bound on it: D u=r Delta can cancel the entire Gram factor. For the same reason a frequency computed from that dyad alone is not automatically a bound on the full spectrum. All physical runs retain the complete B, geometry dependence, and source variation.

## 3. Derive the exact interior hinge coefficient

For an interior anchor at phase theta in a uniform bulk cell,0<=theta<=1, the three nonzero third differences of the hinge, divided by h, are

    (1-theta, 2theta-1, -theta).

The already derived compatible unit Gram has diagonal5/72 and neighbouring entries-1/144 in this interior block. Consequently, for a constant positive row coefficient C,

    mu=C h kappa(theta),
    kappa(theta)=(34theta^2-34theta+11)/72,
    5/144 <= kappa(theta) <= 11/72.

This is an exact finite-stencil identity, not a fit. With varying positive row coefficients between C_min and C_max, the same sum-of-squares construction gives C_min h kappa <= mu <= C_max h kappa. These coefficient bounds must be justified on the actual relevant rows; sampled physical coefficients are not promoted to continuum supremum bounds.

The phase change is not negligible. At theta0.8 and0.6, kappa is5.56/72 and2.84/72. Halving h thus predicts a coefficient ratio0.255396 for constant C, not simply one half. The actual initial curved-geometry values are0.013470879355 and0.003439276236, following that prediction closely. Source-cap halving at fixed h does not supply this reduction.

## 4. Derive the source trace scale, including a genuine spectral lower bound

On one source-adjacent P2 cell of length delta with the source value fixed to zero, the remaining vertex/midpoint mass matrix is delta/30 times[[4,2],[2,16]]. The source derivative functional is(1,-4)/delta up to orientation. Its exact unit-weight dual norm squared is48/delta^3. Restricting to the midpoint bubble alone gives30/delta^3. For kinetic density0<K_min<=K<=K_max on each adjacent cell, and nonnegative mass contributions elsewhere,

    30 sum_sides[1/(K_max,side delta_side^3)]
      <= j^T M^-1 j
      <=48 sum_sides[1/(K_min,side delta_side^3)].

The lower bound uses two independent midpoint bubbles; the upper bound applies the local trace inequality to the full energy. Together with mu=O(h), the isolated dyad frequency has squared scale h/delta^3 when the other coefficients and relative source-cell lengths are uniformly controlled. This explains why refining only tiny source cells can increase high-frequency stiffness without shrinking the bulk Gram correction.

There is also a true LOWER bound for the frozen scalar pencil, under a checkable condition. If those two midpoint bubbles are not base-vertex samples, D annihilates their span. On that span the mixed terms vanish exactly and the full Gram energy equals its dyad energy. Let M_bb be the two-bubble mass submatrix and j_b the restricted jump. A Rayleigh trial then gives

    lambda_max(M^-1 K_scalar) >= mu j_b^T M_bb^-1 j_b,

provided the remaining frozen scalar stiffness is nonnegative. This does NOT prove stability of the nonlinear source/metric system, and is not a lower bound for every scalar mode. The numerical validator checks the actual bubble support, its full Rayleigh quotient and the largest generalized eigenvalue without dropping modes.

Implementation: `scripts/annular_P2_bulk_refinement_20260919.py`, `scripts/derive_annular_P2_Gram_jump_scale_20260919.py`. All43 validation checks pass, including the exact phase polynomial, unit-cell trace constants and12 variable-source-cap fixtures. The actual initial MTS scalar pencils give:

|Bulk/source cap|Bubble lower frequency|Full Rayleigh trial frequency|Largest scalar frequency|
|---|---:|---:|---:|
|257/2e-5|1512840.02|1517929.98|1738425.00|
|513/1e-5|2806709.41|2823663.81|3239623.78|

These are angular frequencies in the existing test normalization, not SI predictions. The lower-bound trial genuinely captures much of the high-frequency scale despite the smaller hinge coefficient. The finer source derivative functional grows faster than that coefficient shrinks. This supplies an action-based explanation of the stiffness, not a new instability claim or a nonlinear convergence theorem. Evidence: `source-intake/navier-stokes/20260914/annular-P2-Gram-jump-scale-attempt01/status.json`.

## 5. Qualification and actual paired evolution

`scripts/probe_annular_P2_bulk_refinement_20260919.py` qualifies513 bulk vertices,1072 scalar nodes and15 material labels at source cap1e-5 in both branches. Its new indexed initial constructor performs the SAME analytic preparation without constructing discarded legacy dense intermediates. Against the original saved257/cap2e-5 states, coordinate and momentum differences are zero at reported precision; rate differences are at most1.39e-17. This is an initialization efficiency change, not new initial data.

Both initial force gates and canonical/radial/current/force identities pass. Initial forces are-1.6940482605e-9/reference and-1.2005239119e-9/MTS against the existing zero initial continuum force. Central frozen maximum angular frequencies are635478.7103 and3239623.7838; all scalar modes are retained. Observed initial RHS evaluations take9.75 and20.11seconds under shared laptop load. These are cost probes, not guaranteed future runtimes.

`scripts/run_annular_P2_bulk_refinement_20260919.py` runs paired32/64-step live exponential evolutions to4e-5, each with a6000second safety allowance and every accepted step saved. The nonlinear remainder recomputes the full canonical flow, radial geometry, source motion and Gram contributions. It compares with the same independently discretized continuum512 endpoint and the saved257/cap2e-5 branch endpoints. The time-force diagnostic remains2e-9; the inherited peak-scaled endpoint force target remains2.7005981227e-8. Neither is silently tightened or relaxed after seeing the answer.

The paired evolutions complete in2849seconds/reference and3810seconds/MTS. The MTS32-to64 force difference is9.9698935598e-10. Although below the existing2e-9 diagnostic budget, it is appreciable beside the remaining discrepancy, so `scripts/refine_annular_P2_bulk_MTS_time_20260919.py` performs a fresh run from the unchanged initial data with128 exponential steps. It completes in3505seconds, retaining all modes and terms. Its64-to128 force difference is1.7365318114e-10, with a successive force-difference ratio5.7413. This shows a smaller observed time-step change, not a proof of asymptotic order or a rigorous truncation-error bound.

|Endpoint at4e-5|reference513/cap1e-5,64steps|MTS513/cap1e-5,128steps|
|---|---:|---:|
|Reduced wave force|-5.3358521533e-8|-6.1099388847e-8|
|Common continuum512 force|-5.3795549953e-8|-5.3795549953e-8|
|Absolute force discrepancy|4.3702842009e-10|7.3038388937e-9|
|Discrepancy / instantaneous force|0.812%|13.577%|
|Previous257/cap2e-5 discrepancy|4.4374602378e-10|1.2563915300e-8|
|New/previous discrepancy|0.984862|0.581335|
|Waveform relative norm discrepancy|7.3332268705e-5|7.3335037096e-5|
|Last force time-step change|2.5633351778e-12|1.7365318114e-10|
|Last relative field time-step change|2.3057e-12|6.2442e-12|
|Conforming force identity residual|6.7064e-12|6.7064e-12|

MTS's discrepancy falls about41.87%, but changes sign under spatial refinement; it is NOT a demonstrated monotone or asymptotic convergence sequence. The remaining13.6% instantaneous discrepancy is substantial and is not hidden behind the inherited peak-scaled short-endpoint pass. Reference's1.5% improvement in its already much smaller discrepancy is below the6.3296e-11 continuum384/512 difference, so no resolved large force improvement is claimed there. Both waveform errors fall approximately fourfold, yet that norm alone does not certify the source force. Final source, velocity, clock, canonical, radial and current checks pass. No action coefficient, initial profile or force was adjusted to obtain these numbers.

At the final MTS state, the pressure trace is only-5.2028e-10, while conforming bulk-lift and combined Gram work are-1.4990e-8 and-4.5596e-8. Thus approximate agreement of the total force is not yet a derivation of the GR pressure mechanism. The remaining drive is-6.1240225509e-8 and projection inertia9.5522e-9; the explicit inertia correction stays much smaller than the drive discrepancy.

Sources: `source-intake/navier-stokes/20260914/annular-P2-bulk513-evolution-reference-attempt01/status.json`, `source-intake/navier-stokes/20260914/annular-P2-bulk513-evolution-MTS-attempt01/status.json`, `source-intake/navier-stokes/20260914/annular-P2-bulk513-MTS-time128-attempt01/status.json`.

This interval remains only1% of the previous.004 horizon; no full-interval force pass, joint convergence theorem, local-GR recovery, or observational preference follows from a short endpoint result.

## 6. Derive the explicit Gram contribution to the actual drive J

The exact Schur drive is J=f_b-r_b-a^T M^-1(f_u-r_u). Define v=M^-1 a, using the full kinetic mass matrix and source cross term. With the ACTUAL live geometry and its tangent held fixed for this algebraic split, the Gram potential has no velocity dependence. Its explicit covectors are f_u,Gram=-B^T W B u and f_b,Gram=-partial_b E_Gram. Hence

    J_Gram=f_b,Gram+v^T B^T W B u,
    J=J_Gram+J_remaining.

The positive sign on the projected variation follows from the minus sign in the Schur projection of the negative potential gradient. This kinetic projection is not the previous conforming P2 lift; their Gram ledgers need not agree term by term. The remainder still contains the actual geometry/tangent response to the Gram sector, so it must not be labelled a separately evolved Gram-free theory. Subtracting J_Gram is not permission to alter the force or state.

Positive W also gives the exact conditional estimate

    |J_Gram| <= |f_b,Gram|+2 sqrt(E_Gram(u) E_Gram(v)).

Thus a small Gram energy of the field alone is insufficient: the kinetically projected transport direction v must also be controlled. Vanishing source-shape work and vanishing product E_Gram(u)E_Gram(v) suffice for this explicit drive term to vanish, but not for the entire self-consistent GR limit. Uniform bounds for the actual evolving states, geometry response and time interval would still be required. The saved-state runner evaluates this bound; it does not replace those requirements by an assumption or a sampled maximum.

`scripts/derive_annular_P2_Gram_projected_drive_20260919.py` evaluates this identity on the existing coarse and fine evolved states in BOTH branches. It checks the source force by complex differentiation of the same Gram energy and the scalar projection by both the explicit covector and an independent energy directional derivative. All27 checks pass, including zero-Gram reference controls and MTS omitted-projection negative controls. The64-to128 field difference is also recomputed from physical states in one sealed modal basis, so this diagnostic does not rely on eigenvector orientations matching across separate factorizations.

|Actual evolved MTS state|257/cap2e-5,32steps|513/cap1e-5,128steps|
|---|---:|---:|
|Total J|-4.1553572308e-8|-6.1240225509e-8|
|Explicit Gram shape force|-2.3237730040e-9|-1.4802046168e-10|
|Kinetic-projected Gram variation|-3.6260869864e-8|-5.7026012605e-8|
|Total explicit J_Gram|-3.8584642868e-8|-5.7174033067e-8|
|Remaining drive|-2.9689294403e-9|-4.0661924419e-9|
|E_Gram(u)|5.4616561279e-9|3.4803133462e-10|
|E_Gram(v)|99574.95|138412.31|
|Global absolute J_Gram bound|0.046640934|0.013881185|

Both reference explicit Gram contributions are zero as required. In MTS, smaller field Gram energy and smaller explicit shape force do NOT imply that the projected Gram drive is disappearing: its magnitude increases here, and dominates J. The derived global Cauchy bound is valid as a saved-state inequality but far too large to certify smallness. We do not conceal this by calling a passed bound check a physical pass. Its excessive size motivates localizing the row products by source support before seeking a uniform bound; it does not justify deleting the projected term. Evidence: `source-intake/navier-stokes/20260914/annular-P2-Gram-projected-drive-attempt01/status.json`.

## 7. Why resolving the source cell need not resolve its wavefront

There is an exact diagnostic in the CONSTANT-COEFFICIENT local corner fixture, not a substitute for the live parent solution. For speed s>|V|, constant forcing D0 and comoving coordinate x, the source response derived in the preceding corner note is

    u(x,t)=D0/2 [t^2-max(t-crossing_time,0)^2],
    crossing_time=-x/(s+V) on the left, x/(s-V) on the right,
    Delta=u_x(0+)-u_x(0-)=D0 t [1/(s-V)+1/(s+V)].

Suppose the two fine source cells lie inside the respective fronts, but each front lies short of the nearest BASE vertex. P2 then reproduces the quadratic source trace exactly, while every base vertex sees the SAME exterior value D0 t^2/2. Hence D u=0 but j^T u=Delta, and the existing repaired Gram factor is EXACTLY-r Delta:

    E_Gram=mu Delta^2/2.

This is not cured by further subdividing source cells without changing the base stencil. With uniform coefficient C, the local continuum gradient energy of this response is

    E_gradient=C D0^2 t^3 [1/(s-V)+1/(s+V)]/6,
    E_Gram/E_gradient=3 h kappa(theta) [1/(s-V)+1/(s+V)]/t.

For V=0 this becomes6 kappa h/(s t). It is a comparison of gradient and Gram energies for a specified local response, NOT of total conserved energy or measured force errors. A globally small Gram energy can nevertheless dominate this very young local response when its front has not reached the base vertices.

Conversely, once that fixed-time front is resolved, subtracting the exact source hinge leaves a C1 piecewise-quadratic function. Its third differences vanish except in finitely many stencils crossing second-derivative jumps; those differences are O(h^2). Bounded compatible Gram weights therefore give E_Gram=O(h^3) for this fixture. This proves an energy scaling for the prescribed constant-coefficient response, not convergence of the self-consistent force. The projected-direction energy in section6, the live geometry and a uniform time argument still matter.

`scripts/derive_annular_P2_unresolved_front_Gram_20260919.py` checks both actual graded mesh layouts with explicitly prescribed fixture coefficients s=.77,V=.03,D0=1,t=4e-5, and a separate constant-phase resolved-front sweep. These coefficients are not fitted to the live force results. It uses exact-rational natural P2 node locations solely to avoid tiny-cell midpoint roundoff in this analytic fixture; no live state is altered. All13 checks pass.

The fixture fronts extend3.20e-5/2.96e-5, so both source meshes resolve their adjacent quadratic response, yet the nearest base vertices are much farther away:0.005/0.00125 on257 and0.001875/0.00125 on513. The exact unresolved-front energy identity holds on both. Gram energy divided by that local continuum gradient energy is94.16 and24.05 respectively. Those are fixture energy ratios, not live force-error predictions. In a separate unit-coefficient constant-phase sweep, E_Gram/h^3 is0.03805 at4,16 and64 front-lengths per bulk cell, consistent with the derived resolved-front scaling. Source: `source-intake/navier-stokes/20260914/annular-P2-unresolved-front-Gram-attempt01/status.json`.

This exhibits a concrete mechanism by which refining the source while its wider Gram stencil still misses the front can leave a persistent early-time discrepancy. It does not prove that ALL of the live discrepancy comes from that mechanism. A matched resolved-front test of the full dynamics, or a justified uniform force bound, remains necessary before promoting the local-GR limit.

## 8. Independent first-step algorithm control

`scripts/check_annular_P2_bulk_first_step_20260919.py` uses physical-space DOP853 without the modal split at the original64-step scheme's first endpoint6.25e-7. Both maximum step and tolerance are tightened; this is not a tolerance-only rerun that silently takes an identical step. Results:

|Branch|RK step-refinement force difference|Exponential/RK force difference|Predeclared first-step control|
|---|---:|---:|---|
|reference|3.2526e-17|1.3473e-14|pass|
|MTS|1.9525e-13|2.0099e-10|pass|

The executions take729/1074seconds. These checks do NOT independently integrate the entire4e-5 interval or qualify every point of the subsequent128-step MTS trajectory. The whole-interval empirical time differences and first-step independent checks have separate scopes; neither is a certified continuous-defect enclosure.

## 9. Next physical/mathematical target and checkpoint boundary

The next target is FRONT-RESOLVED force recovery, not another blind source-cap halving or a claim based only on the total force being near the reference. First localize the explicit projected Gram work into source-support and remaining stencil rows to obtain a useful bound without relying on unrelated distant energy. Use the derived front-to-base-spacing criterion to design a matched local-limit test and verify its runtime/stability before extending the live interval. The full Gram/source/metric feedback must remain present; a prescribed local fixture cannot replace that test.

No full.004 evolution, unrestricted GR limit, Newton/Maxwell completion or observational claim is established here. All owned numerical jobs for this checkpoint finish before the final integrity seal. Historical failures remain preserved, all work stays private inside post-checkpoint-work, and no GitHub action or subagent is used. The protected-workbench check is an mtime scan since this turn began, not a claimed pre-turn whole-tree hash baseline.
