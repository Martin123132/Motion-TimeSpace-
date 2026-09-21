# Original weighted action on information-preserving common cells

Private checkpoint, September 20, 2026 local time. No new evolution, parameter adjustment, deleted mode, altered source condition, GitHub action or full-GR claim.

## Result and scope

The exact common reference mesh now carries the ORIGINAL frozen mass and gradient weights, not merely the unit-weight validation forms. The original Gram functionals are also retained. Both reference and MTS pass the inherited numerical thresholds under integration-order refinement and independent direct integration.

For these force-derived test fields, the old weak coarse/fine comparison is largely affected by nodal representation loss. The same continuous fields, compared with each reconstructed physical geometry, have much smaller geometry-weight differences. This is useful evidence about the comparison procedure, NOT proof that the physical source-force mismatch has disappeared.

The tested fields are the coarse initial displacement/velocity and the previously derived coarse Riesz representers of the terminal-force-weighted frozen commutator. They are not a new trajectory and not the complete time-dependent source-force residual. Only the frozen principal mass/stiffness blocks are evaluated here; moving-source cross terms, time derivatives and the full source Schur force are not newly evaluated.

Predecessor: `DERIVATION-20260919-rank-safe-spatial-commutator-and-common-overlay.md`.
Inherited seal: `source-intake/navier-stokes/20260914/annular-rank-safe-commutator-final-integrity.json`.

## 1. Original weights and comparison space

For native level L, reference coordinate xi, physical radius r_L(xi), mapping Jacobian J_L and original coefficient k_L, define

    m_L(p,v) = integral [J_L r_L^4/k_L] p v dxi,
    a_grad,L(a,u) = integral [k_L/J_L] a' u' dxi,
    a_Gram,L(a,u) = (H_L a_nodes)^T W_H,L (H_L u_nodes).

The coefficients are reconstructed from the saved original canonical states and live geometry, without evolving them. All four reconstructed mass arrays and Gram weight arrays match their saved counterparts exactly. Gradient-weight reconstruction differs only at about 1.74e-18 in the recorded normalisation; the saved arrays remain the baseline for native-form comparisons.

The common mesh has 1,094 free P2 coefficients and 547 elements, retains both native spaces, and keeps the source trace zero. Integration additionally splits at the mapped geometry breakpoints of BOTH levels, giving 1,635 positive segments. No integration cut is discarded. Orders 16, 32 and 64 use 26,160, 52,320 and 104,640 points respectively.

Let E_c,E_f embed native functions in the common space, with exact left inverses R_c,R_f. For the coarse test/trial field vector z, distinguish:

    true common field:       E_c z,
    canonical fine sample:   E_f R_f E_c z,
    legacy fine sample:      E_f I z.

The canonical sampler is exact evaluation at canonical fine nodes, but still cannot preserve all coarse functions. The legacy sampler additionally contains the earlier binary64 shape-evaluation arithmetic. Separating these two avoids calling floating-point interpolation differences a physical effect.

The Gram extension is explicit: evaluate the common field with R_L, then apply the SAME native H_L and W_H,L. This agrees with the original discrete Gram action on the native space. It does not introduce a new continuum Gram operator or assume that nodal functionals see every common-space component.

## 2. Derive cancellation-preserving weighted moments

On each common element, express each P2 function in the local coordinate t in [0,1]. Products of fields have degree four; products of their derivatives have degree two. Compute

    mu_L,e,k = integral_element w_L(xi) t^k dxi,
    weak_form = sum_elements sum_k polynomial_product_e,k * mu_L,e,k.

Cell coordinates, polynomial coefficients, contractions and sums use 64-digit Decimal arithmetic. Geometry and metric coefficient evaluations remain binary64 parent inputs. High-precision accumulation does not imply high-precision physical coefficients.

Geometry differences contract the SAME field-product coefficients against mu_f-mu_c. Representation differences contract the difference of polynomial products against the SAME fine moments. Thus signed cancellation is preserved before any absolute values are taken.

For each frozen weak sector the exact finite-input telescope is

    fine_native(legacy sample) - coarse_native
      = fine native quadrature/basis closure
        + legacy-sampler arithmetic
        + canonical representation alias
        + geometry-weight difference
        + Gram-stencil difference
        + coarse native quadrature/basis closure.

For mass and gradient, a common continuous field with fixed geometry has no remaining grid-stencil term. For Gram, retain the native finite functionals: separate fine-versus-coarse geometry weights from fine-versus-coarse stencils at the SAME coarse geometry. Neither closure is silently set to zero just because it is inconvenient.

## 3. Numerical results

All values are signed, normalised code-unit weak probes. They are NOT new measured physical force discrepancies.

| Sector | Old native weak difference | Representation alias | Geometry-weight difference |
|---|---:|---:|---:|
| Reference mass | -4.812653609e-9 | -4.812653609e-9 | +5.90045e-26 |
| Reference gradient | -8.724429696e-10 | -8.724517841e-10 | -4.38205e-21 |
| MTS mass | +4.992963309e-7 | +4.992963311e-7 | -1.29922e-20 |
| MTS gradient | -1.450272372e-8 | -1.441820679e-8 | +2.91764e-15 |

The remaining columns of the telescope are recorded, not hidden:

- MTS gradient: coarse native quadrature/basis closure -8.63549e-11; fine closure +1.74819e-12; legacy-sampler arithmetic +8.68206e-14. This checkpoint does not further identify how much of each combined closure is quadrature versus basis arithmetic.
- Reference gradient legacy-sampler arithmetic: +8.81478e-15. Reference is not exempted from this effect.
- MTS Gram native weak difference: -1.81083e-11. It splits into legacy-sampler arithmetic -1.64804e-11, same-geometry stencil difference -1.62791e-12 and geometry-weight difference -1.85922e-22. Canonical representation alias is zero for this specified Gram extension because it uses the same canonical nodal values. That does NOT show that the full Gram dynamics are irrelevant.
- Reference has no Gram rows; its Gram terms remain zero.

For the MTS mass probe, +4.96153e-7 of the +4.99296e-7 representation term lies in the four common cells supporting the formerly erased coarse basis components. In the gradient probe, that region contributes -8.05947e-7 and the rest contributes +7.91529e-7: signed cancellation matters, and local terms are not causal percentages.

The two common cells touching the source itself have zero canonical representation-alias contribution for these probes. This does not license discarding any surrounding cells, source-motion term or Gram row.

## 4. Independent checks and what they establish

- Unit-weight moment polynomials match independent exact-rational polarisation integrals.
- Original parent masses and Gram weights are reproduced from the saved canonical geometry.
- Every 16/32 and 32/64 channel-refinement comparison passes the LITERAL predecessor threshold: 3.002e-16 for reference and about 3.064e-16 for MTS. The largest 32/64 change is 4.533e-18; the largest 16/32 change is 4.970e-17.
- A separate integrator evaluates unexpanded P2 shapes and derivatives directly at every order-16 integration point. It agrees with moment contraction to better than 1.14e-63 for these fixed inputs. This is algebraic/numerical consistency, not physical precision.
- The original coarse Riesz force pairing is recovered, including its saved residual. This checks that the actual force-derived probes, rather than arbitrary substituted fields, were used.
- Shared linear and quadratic functions survive the canonical common/fine comparison; maximum coefficient discrepancy is 1e-66 in the chosen arithmetic.
- The formerly erased basis vector 265 now has positive physical-weighted mass about 0.0157760 and gradient form about 237,639.654 on the common space for BOTH branches. Its canonical fine sample is zero. This demonstrates the information loss with the actual weights, not only a Euclidean norm.

These checks qualify the fixed, weighted weak-probe computation. They do NOT enclose all binary64 parent-coefficient errors, prove uniform spatial convergence, or certify the nonlinear physical source force. The independent very-small reconstruction errors are conditional on the same saved input data.

## 5. Rank-safe route into the actual force commutator

This stage supplies the common-cell moment representation needed for mixed weak matrices. Let B_fc be the fine-test/coarse-trial mass matrix evaluated on common cells using the fine physical weight, and S_fc the corresponding gradient-plus-original-Gram mixed stiffness. Keep the original native M_f, K_f, M_c, K_c, and set A_c=M_c^-1 K_c.

For the OLD nodal-transfer commutator, the exact identity is

    M_f I A_c - K_f I
      = (M_f I - B_fc) A_c
        - (K_f I - S_fc)
        + (B_fc A_c - S_fc).

This separates the mass transfer/assembly defect, stiffness transfer/assembly defect, and true mixed weak defect WITHOUT inverting the singular I^T M_f I. No injectivity of I is required. The individual terms retain signed cancellations and must not be turned into separate physical causes without the full sum.

With the already qualified adjoint lambda(s)=exp((T-s)L_f)^T c, set z_f=M_f^-1 lambda_v. The original force commutator equals

    integral_0^T z_f(s)^T [M_f I A_c - K_f I] u_c(s) ds.

The next substantive target is to assemble B_fc and S_fc from these common moments, verify the above operator identity, then integrate the three contributions against the actual frozen primal/adjoint paths. That step has NOT been done here. The current same-field Riesz probes must not be substituted for it.

Native quadrature/basis closures must remain explicit when comparing the common mixed matrices with native arrays. Any improved bound must exploit consistency and moment cancellations before taking absolute norms; the previous very loose Cauchy bound is not retrospectively promoted to a pass.

## Unchanged physics and saved evidence

The 12.5718% impulse, 13.5770% fine/continuum endpoint and 32.5535% coarse64/fine endpoint discrepancies are unchanged; these are different comparisons. No R10, PPN, clock, orbital, local-GR or full-GR pass follows.

- Acquisition: `scripts/acquire_annular_common_action_weights_20260920.py`.
- Moment helper: `scripts/annular_common_weighted_moments_20260920.py`.
- Actual weak comparison: `scripts/derive_annular_common_weak_action_20260920.py`.
- Independent controls: `scripts/validate_annular_common_weak_action_20260920.py`.
- Data: `source-intake/navier-stokes/20260914/annular-common-action-weights-attempt01/status.json`.
- Results: `source-intake/navier-stokes/20260914/annular-common-weak-action-attempt01/status.json`.
- Controls: `source-intake/navier-stokes/20260914/annular-common-weak-controls-attempt01/status.json`.

All three runs complete: 30, 49 and 29 scoped implementation/source checks, no new failed run. No subagent or concurrent heavy worker was used. The protected workbench, galaxy work and prior immutable evidence are untouched.
