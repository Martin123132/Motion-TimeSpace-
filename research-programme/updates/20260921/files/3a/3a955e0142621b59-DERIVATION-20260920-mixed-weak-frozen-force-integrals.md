# Mixed weak matrices carried into the frozen source-force commutator

Private continuation of `DERIVATION-20260920-original-weighted-action-on-common-cells.md`.

Status: COMPLETE, including independent adjoints and separated refinement checks. No new live evolution, physical parameter adjustment, or public claim. The original binary64 parent coefficients and source-force covector are unchanged.

## 1. What is actually being computed

The preceding stage used initial-field/Riesz weak probes. Those probes do not establish how much of the time-integrated force comparison comes from transfer. This stage instead uses the original coarse initial phase, the actual saved spatial64 source-force covector, and both original frozen principal actions over the same saved duration T=the exact binary64 value of 4e-5.

This is the homogeneous frozen-operator contribution to the existing comparison. It is not the complete nonlinear moving-source force budget; source forcing, time-dependent action changes, geometry paths and initial representation differences are not silently included.

## 2. Mixed matrices without a singular inverse

Let E_c,E_f embed both native P2 fields into the exact common space. The mass matrix B and gradient stiffness S_grad pair fine tests with coarse trials using the fine physical weight and the stored common-cell moments. They are rectangular, 1072 by 558. Coarse and fine fields are preserved, not resampled for these integrals.

The Gram extension is precisely the previously declared original discrete extension, not a proposed continuum action:

    J = R_f E_c,
    S_Gram = H_f^T W_f H_f J,
    S = S_grad + S_Gram.

This retains the original Gram stencil's limitations; it must not be advertised as an injective representation of every coarse function. The reference branch has zero Gram contribution.

Keep the native positive mass matrices, original stiffness matrices and legacy transfer I. With A_c=M_c^-1 K_c and A_f=M_f^-1 K_f, define

    D_mass = (M_f I - B) A_c,
    D_stiffness = S - K_f I,
    D_weak = B A_c - S.

Then the exact finite-input operator identity is

    D_mass + D_stiffness + D_weak = M_f I A_c - K_f I.

No inverse of I^T M_f I, B, or any projected mass is used. All coarse components, including the six previously erased nodal-transfer components, remain in the coarse dynamics. The first two terms combine representation and native-assembly effects; neither is pure interpolation error. D_weak is a finite-element consistency residual under finer tests, not automatically a physical inconsistency or a continuum error.

This attribution depends on the explicitly fixed common-integral and Gram-extension convention. Another comparison convention can redistribute the three contributions while leaving their sum unchanged. Their signed values are therefore not unique causal percentages of a physical discrepancy.

## 3. Integrating actual paths instead of substituting probes

Let x_c=(u_c,v_c), L_c=[[0,Id],[-A_c,0]], and L_f analogously. The coarse path satisfies x_c'=L_c x_c from the original initial state. For each of the three independently propagated response channels,

    r_j'' + A_f r_j = M_f^-1 D_j u_c,
    r_j(0) = r_j'(0) = 0.

For the original terminal covector c, the channel output is exactly

    F_j = c^T (r_j(T),r_j'(T))
        = integral_0^T lambda_v(s)^T M_f^-1 D_j u_c(s) ds,
    lambda(s) = exp((T-s)L_f^T)c.

Consequently the sum is the previously qualified frozen operator commutator. Equality of the sum is necessary but insufficient: each channel is independently checked with the transpose augmented evolution.

In reverse time tau=T-s, the fine adjoint source eta'=L_f^T eta starts at c. For each coarse response p_j, initialized at zero,

    p_j' = L_c^T p_j + (D_j^T M_f^-1 eta_v, 0).

Then F_j=p_j(T)^T x_c(0). The implemented independent forcing uses

    D_mass^T z = A_c^T (I^T M_f z - B^T z),
    D_stiffness^T z = S^T z - I^T K_f z,
    D_weak^T z = A_c^T B^T z - S^T z.

The order of mass solve and stiffness multiplication in A_c^T is retained. M_f z=eta_v uses the same original symmetric lower-triangle mass convention as the predecessor.

The augmented frozen exponential is evaluated by scaled, substepped Taylor action at 32 digits/order48 and 48 digits/order64. No modes are truncated. A separate dense mpmath exponential on a small noncommuting-mass fixture, including rank-deficient I, verifies all three channels and their adjoints. A sign-reversed stiffness-channel control is detectably wrong.

## 4. Results and validation

All entries below are signed contributions to the SAME frozen spatial64 source-force commutator, in its saved code-unit normalization. They are not percentages of the physical force and are not absolute error bounds.

| Branch | Mass transfer / assembly | Stiffness transfer / assembly | Mixed weak remainder | Sum / original commutator |
|---|---:|---:|---:|---:|
| Reference | -9.38180216544e-11 | +4.02856726926e-12 | +1.35133591391e-9 | +1.26154645952e-9 |
| MTS | +4.16606060049e-10 | -1.38638612462e-10 | -3.02762656364e-8 | -2.99982981888e-8 |

The MTS transfer/assembly terms together contribute +2.77967447588e-10, opposing the negative weak remainder. Removing those terms as an accounting exercise would make the remaining magnitude slightly larger, not cure the discrepancy. For reference the analogous sum is -8.97894543851e-11, likewise opposing its positive weak remainder. Such removal would be a decomposition, not a demonstrated corrected evolution.

Both branches reproduce their original frozen commutators under the unchanged literal gates: 3.002e-16 for reference and approximately 3.064e-16 for MTS. Every individual channel agrees between forward and independently formulated adjoint propagation; the largest discrepancy is 5.338e-46 for these fixed input arrays. This tiny arithmetic discrepancy is not physical accuracy.

Combined arithmetic/time-order/moment-order refinement changes no channel by more than 5.995e-19. The additional run separates arithmetic/time-order changes at fixed spatial moment order32 from moment32-to64 changes at fixed 48-digit/order64 evolution:

- At fixed spatial moment order32, increasing arithmetic precision/time order changes no channel by more than 1.998e-30.
- At fixed 48-digit/order64 evolution, changing spatial moment order32 to64 changes no channel by more than 5.995e-19.
- Every separated comparison passes the same literal predecessor gate; no threshold was relaxed.
- The independent fine-adjoint terminal arrays reproduce the original 48-digit spatial64 arrays exactly at the recorded precision for both branches. The original force covector/path was not substituted for a more convenient test.

Four successful runs contain 132 scoped implementation/source checks: matrix assembly54, corrected dense controls9, forward/adjoint integration34 and separated refinement35. These counts describe implementation checks, not independent experiments or evidence that MTS is correct. The main integral run took about20.9 minutes and the separated refinement about7.5 minutes on one actual single-core worker, run sequentially.

Mixed matrices reproduce independent common-field polynomial pairings and the original Gram extension; transpose and pointwise operator identities also pass. The small dense exponential fixture checks each nonzero channel separately with noncommuting mass/stiffness and a singular transfer. No inverse or regularization of that transfer is used.

## 5. Interpretation and next calculation

The stronger, time-integrated test does NOT support extrapolating the preceding initial-field probe result into a claim that nodal transfer explains the force discrepancy. The mass/stiffness probes were legitimate, but their relative importance does not survive unchanged under the actual evolving force weighting.

The dominant term in this particular decomposition is the mixed weak remainder for BOTH branches. Its value has now been calculated and independently checked; it is not an unspecified missing input. However, coarse finite-element equations only enforce their weak equations against coarse tests. A finer test can see a nonzero residual even if the underlying continuum equations are consistent. Calling the entire remainder a new physical defect, or declaring the pipeline broken because the reference also has one, would both be premature.

The next useful calculation is therefore the derived finer-test/closure/geometry/stencil split below. It directly interrogates the nonzero term actually found, rather than retesting the eliminated simple-transfer explanation or changing physical coefficients to hide it.

### Exact next identity: the finer-test residual is not automatically new physics

There is a further algebraic split that does not modify the action. Let C=R_c E_f map a fine test to its canonical coarse nodal values. Define B_c and S_c by pairing the same fine test/coarse trial with the COARSE geometry weights; extend the original coarse Gram form using R_c. Let M_c^*,K_c^* be those common-integrated coarse/coarse forms, including the original coarse Gram term.

Then

    B_f A_c - S_f = D_closure + D_test + D_geometry_stencil,

    D_closure = C^T [(M_c^* - M_c) A_c - (K_c^* - K_c)],
    D_test = (B_c - C^T M_c^*) A_c - (S_c - C^T K_c^*),
    D_geometry_stencil = (B_f - B_c) A_c - (S_f - S_c).

Proof: expand the right side. Everything cancels except B_f A_c-S_f and C^T(K_c-M_c A_c); the latter is exactly zero by the original A_c=M_c^-1 K_c. No rank assumption on I or C, extra equation or vanishing physical coupling has been inserted.

For a fine test t=E_f z, its unresolved part is t_perp=t-E_c C z. Exact R_c E_c=Id gives R_c t_perp=0. Consequently the specified coarse Gram extension annihilates t_perp, while its mass and gradient pairings can remain nonzero between coarse nodes. D_test therefore measures a genuine finer-test discretization residual even for a consistent continuum equation. It is not an orthogonal projection and no norm bound is inferred.

The remaining Gram difference can itself be split using the already sourced fine Gram weights evaluated on coarse geometry: a weight-change term H_f^T(W_f-W_f|coarse)H_f J and a same-geometry stencil term H_f^T W_f|coarse H_f J-C^T K_Gram,c. This prevents calling a stencil difference a geometric physical effect.

This identity is derived here; its additional matrices and channel integrals have NOT been evaluated in this checkpoint. Their evaluation is the next targeted calculation if the mixed weak remainder is material. It uses existing source-backed moments and keeps original native quadrature/basis closures explicit, rather than requiring a new fitted parameter.

The 12.5718% impulse, 13.5770% fine/continuum endpoint and 32.5535% coarse64/fine endpoint differences are unchanged and describe different comparisons. No local-GR, full-GR, continuum-error-bound or observational pass is inferred. Decimal accumulation is conditional on saved binary64 physical inputs, not a new precision claim for the parent theory.

## Evidence

- Mixed matrix assembly: `scripts/derive_annular_mixed_weak_matrices_20260920.py`.
- Independent augmented-integrator fixture: `scripts/validate_annular_mixed_force_cascade_v2_20260920.py`.
- Frozen forward/adjoint integrals: `scripts/derive_annular_mixed_force_integrals_20260920.py`.
- Separated integration-refinement checks: `scripts/validate_annular_mixed_force_refinement_20260920.py`.
- Matrix run: `source-intake/navier-stokes/20260914/annular-mixed-weak-matrices-attempt01/status.json`.
- Control run: `source-intake/navier-stokes/20260914/annular-mixed-force-controls-attempt02/status.json`.
- Force integrals: `source-intake/navier-stokes/20260914/annular-mixed-force-integrals-attempt01/status.json`.
- Refinement: `source-intake/navier-stokes/20260914/annular-mixed-force-refinement-attempt01/status.json`.

The first control attempt is preserved as failed: the legacy lower-band adapter does not support a two-DOF fixture because it takes a maximum over an empty second off-diagonal. The corrected fixture uses the already-existing exactly symmetric-band implementation for its exactly symmetric small matrices; production native actions still use the original lower-triangle adapter. No scientific threshold or production action was changed to fix that fixture setup error.
