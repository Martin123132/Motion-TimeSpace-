# Rank-safe spatial commutator and an information-preserving common mesh

Private derivation checkpoint, September 19, 2026. This contains a constructive repair to the comparison space, an exact transfer obstruction, and an attempted force bound. No live evolution, action modification, mode deletion, parameter fitting, GitHub action, or full-GR claim.

## Outcome in plain language

1. The old coarse-to-fine nodal sampler is not injective: it completely erases six genuine coarse P2 components in BOTH reference and MTS. More fine nodes did not mean finer cells everywhere. Any proposed inverse of its pulled-back fine mass is invalid.
2. A 1,094-component common P2 mesh now contains both original spaces without losing information. Exact rational left inverses and exact unweighted field/gradient integrals verify this construction. It retains all saved edges, including the original source trace, without snapping or regularisation.
3. The previously precision-qualified force commutator is reproduced from independently propagated adjoints. The lost-mode contributions participate in very large cancellations; they cannot be removed or labelled the sole cause of the final mismatch.
4. A rank-safe action-factor force bound has been derived and evaluated. It is valid as a finite-input algebraic inequality but numerically too loose: it does NOT close the local-GR/continuum force gate.

Predecessor: `DERIVATION-20260919-cancellation-preserving-source-force-transport.md`.
Inherited evidence: `source-intake/navier-stokes/20260914/annular-decimal-transport-final-integrity.json`.

## 1. The inverse we must not introduce

Let I be the saved 1072-by-558 coarse-to-fine nodal interpolation. The candidate Galerkin split would introduce

    M_g = I^T M_f I,
    K_g = I^T K_f I,
    P = I M_g^-1 I^T M_f.

If I were injective, this could split the coarse-subspace mass/stiffness mismatch and its fine complement. It is NOT injective here. Its exact zero columns are

    265, 266, 267, 271, 272, 273.

Their reference coordinates run from 6.0253125 to 6.0278125, just inside the source at 6.03. Two further columns, 268 and 270, have very small nonzero norms; no claim of their exact nullity is made. No rank cutoff is needed to prove the six exact null directions.

For each listed index j, I e_j=0 while e_j is a nonzero native finite-element function. Therefore M_g e_j=0, independently of the positive fine mass. No positive lower transfer-coercivity constant can hold for every coarse field. Neither a pseudoinverse nor a ridge term would restore the discarded functions; either would introduce a new choice requiring its own justification.

The zero columns are reproduced directly from the original basis evaluator. Eleven coarse edges are absent from the fine mesh. This is a nonnested-grid sampling obstruction, not evidence that either physical theory has failed. The old force telescopes and adjoint identities remain algebraically valid for this I; they did not require this new, invalid inverse. The earlier high-precision pass is not revoked.

## 2. Constructive common-mesh repair

Take the exact union of both sets of saved binary64 element edges, interpreted as rational numbers. Put canonical P2 nodes at each union edge and exact midpoint, retaining the existing zero scalar trace at the source. This gives 1,094 free coefficients, compared with 558 coarse and 1,072 fine coefficients. There are no sub-1e-12 cells in this union; the smallest width is about 4.8828125e-6. No edge has been merged or dropped.

Let E_c and E_f evaluate each native polynomial field at the common canonical nodes. Let R_c and R_f evaluate common polynomials at the corresponding native canonical nodes. Exact rational arithmetic establishes

    R_c E_c = identity_558,
    R_f E_f = identity_1072.

The union contains every native breakpoint. A quadratic on any native element is therefore reproduced as the same quadratic on every common subelement. This proves equality of the represented function and its derivative almost everywhere, not just agreement on a few plotted points. The source is a shared breakpoint and its original trace is retained. The left-inverse identities prove injectivity without a numerical singular-value threshold.

For random rational coefficient fixtures, a source hinge, and each erased basis vector, the native/common values of

    integral u(r)^2 dr,       integral [du(r)/dr]^2 dr

agree EXACTLY as fractions. For example the erased column-265 function has positive unweighted squared norm about 3.3333333e-4 and positive gradient form about 8.5333333e3. Its old nodal image is zero; its common-mesh image preserves both integrals.

These integrals are independent representation controls with unit reference weight. They are NOT substitutes for the physical action's metric-dependent mass, gradient, Gram or moving-source terms. Canonical midpoint arithmetic is exact on the stored edge geometry; it is not a claim that all earlier binary64 basis evaluations were themselves exact. Physical weighted forms still need the mixed/native-basis evaluation on common cells.

## 3. Exact force-weighted localisation of the old commutator

Keep the original saved phase, force covector c and original I. For Y=(u,v), let L=[[0,1],[-M^-1K,0]], E=exp(TL), T=4e-5. Define

    w = I^T E_f^T c - E_c^T I^T c,
    C_force = w_u . u_c0 + w_v . v_c0.

This is exactly c.[(E_f I-I E_c)Y_c0]. The independent 48-digit adjoints from the preceding checkpoint provide w; accumulation uses 64 decimal digits. The reconstruction error is at most 1.009e-45 for all four reference/MTS spatial32/spatial64 comparisons. The original predecessor precision thresholds are replayed during sealing; no previously failed gate is relaxed.

For a zero column of I, the corresponding pulled fine adjoint vanishes, leaving exactly minus the coarse backward-adjoint contribution. This yields the following signed coarse64/fine split in normalised code units:

| Initial-coordinate group | Reference | MTS |
|---|---:|---:|
| Six exactly erased columns | +4.388219204e-9 | +1.745929787e-3 |
| Two near-zero columns | -6.742635954e-10 | -1.869116939e-4 |
| All remaining columns | -2.452409149e-9 | -1.559048091e-3 |
| Total operator commutator | +1.261546460e-9 | -2.999829819e-8 |

**These are signed, cancelling terms, not causal percentages.** The MTS erased-mode subtotal is about 58,201 times the signed net magnitude. It would be wrong to say that removing those modes fixes 58,201 times the discrepancy. Doing so would destroy the cancellations and change the problem. The same warning applies to reference, whose erased subtotal also exceeds its net value.

Cumulative windows around the reference source are exported separately, not summed as disjoint partitions. Local nodal pieces can be large and cancel against their complement; this localisation does not justify discarding exterior rows.

## 4. A derived bound that avoids the singular projected mass

The native coarse action remains positive and invertible under its existing source condition. Use ONLY its original K_c and M_c, not M_g. Solve

    K_c a = w_u - r_u,       M_c b = w_v - r_v.

Then, without an injectivity assumption on I,

    C_force = a^T K_c u_c0 + b^T M_c v_c0
              + r_u . u_c0 + r_v . v_c0.

Use the original positive factorisation

    K_c = G^T W_G G + H^T W_H H,      M_c = L_M D_M L_M^T.

The signed terms are the weighted gradient, original lifted-Gram and kinetic-factor pairings. Cauchy-Schwarz on any exhaustive, declared row partition gives

    |C_force| <= sum_over_blocks sqrt(sum w_i a_i^2) sqrt(sum w_i u_i^2)
                 + sum_i |r_u,i u_c0,i| + sum_i |r_v,i v_c0,i|.

For the kinetic block replace the factor vectors by L_M^T b and L_M^T v_c0. The corresponding unpartitioned action-energy bound follows by combining the block norms. Every residual is retained; neither the stiffness inversion nor the mass inversion is treated as numerically exact.

The stiffness solve uses a double-precision preconditioner with 64-digit residual corrections. Three corrections reduce the relative residual to 9.18e-46 (reference) and 9.56e-45 (MTS). The original lower-triangle mass convention is preserved. The reconstructed signed force agrees to below 7e-63; this is algebraic reconstruction conditional on the saved inputs, not comparable physical accuracy.

### Numerical outcome: the bound is not useful yet

| Coarse64/fine quantity | Reference | MTS |
|---|---:|---:|
| Signed commutator | +1.26155e-9 | -2.99983e-8 |
| Nodal absolute bound | 0.0257592 | 11.9044 |
| Partitioned action-factor bound | 0.0189048 | 26.6439 |
| Action bound / absolute signed value | 1.499e7 | 8.882e8 |

The reference bound improves modestly; the MTS action bound is WORSE than the nodal bound. Both remain many orders too large. These failures of sharpness are reported, not converted into stability evidence.

The gradient factors alone include MTS source-window and remaining signed terms about +0.07146940825 and -0.07146943825. Their near cancellation carries almost the entire signed remainder. Small direct Gram pairing in this Riesz decomposition does not show that the Gram action is dynamically irrelevant: the representer a and adjoints already depend on the full Gram-inclusive action.

This is a finite-input algebraic bound with evaluated residuals. It is neither an interval-arithmetic enclosure nor a uniform continuum theorem. Any claim of a sharp local-GR force bound remains blocked.

## 5. What changes next

Do not invert I^T M_f I, add a ridge, delete erased modes or run another blind time refinement. The next substantive calculation is the ORIGINAL weighted weak mass/gradient/Gram comparison on the common cells, evaluating each native function in its own basis. It must retain geometry/source differences and quantify cancellation-preserving moment/consistency defects BEFORE absolute values are taken.

The exact common mesh and its left inverses are ready for that calculation. They are not yet a new evolution grid, and the present work has not recomputed physical force predictions on it. The previously recorded 12.5718% impulse, 13.5770% fine/continuum endpoint, and 32.5535% coarse64/fine endpoint discrepancies remain unchanged and refer to different comparisons.

## Reproducibility and limits

- Exact common-space helper: `scripts/annular_common_P2_overlay_20260919.py`.
- Kernel proof, construction and adjoint localisation: `scripts/derive_annular_transfer_kernel_and_common_overlay_20260919.py`.
- Residual-inclusive action-factor bound: `scripts/derive_annular_commutator_riesz_bound_20260919.py`.
- First result: `source-intake/navier-stokes/20260914/annular-transfer-kernel-overlay-attempt01/status.json`.
- Second result: `source-intake/navier-stokes/20260914/annular-commutator-riesz-bound-attempt01/status.json`.

Both runs completed with 97 and 43 scoped implementation/source checks respectively, with no new failed run. Those counts are not independent tests of a fundamental theory. The new proof concerns the saved discrete comparison spaces and their force functional. Original evidence and both model branches are preserved; no full GR/local-GR/continuum pass is claimed.
