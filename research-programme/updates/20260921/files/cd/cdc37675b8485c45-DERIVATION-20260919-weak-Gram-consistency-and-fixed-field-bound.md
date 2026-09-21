# Weak Gram consistency and a fixed-field refinement bound

Private continuation,19 September2026. No action, coupling, source condition or evolved trajectory is changed. All scalar modes and Gram rows remain present. This stage does not establish the full GR limit or resolve the prior12.5718% impulse /13.58% instantaneous hierarchy discrepancy.

## Main result

The actual final Gram-force transfer work is4.059355910156905e-10. Only2.871096169355907e-14, about0.00707%, belongs to source-straddling rows. A source-only repair would therefore miss almost all of this particular diagnostic. The remaining contribution is dominated by comparing the same coarse trial/test fields with the two Gram operators and weights.

We derived a count-independent bound for the existing positive Gram template and a refinement bound for any **fixed compensated continuous piecewise-quadratic trial and test fields**. Under a bounded coefficient, their Gram pairing tends to zero as the bulk spacing tends to zero. This is a consistency statement for fixed fields, not uniform convergence of the actual evolving hierarchy.

The actual frozen-field scan is not monotone and does not justify fitting a single convergence order. Local derivative-jump bounds improve the very loose global bound, but remain considerably above the measured signed work. These limitations are retained rather than converted into a pass.

## 1. The mass-adjoint weak identity

With fixed reference interpolation I, positive scalar masses M_H,M_h, actual velocity difference d=v_h-Iv_H and T=M_h I M_H^(-1),

    S_G = T K_G,H u_H - K_G,h Iu_H,
    K_G,a = B_a^T W_a B_a,
    eta_H = M_H^(-1) I^T M_h d.

Mass symmetry gives exactly

    d^T S_G = (B_H eta_H)^T W_H (B_H u_H)
            - (B_h d)^T W_h (B_h Iu_H).

This was checked against the direct load on both actual initial/final pairs and against the previous saved final work. It uses the mass-adjoint test, not I^T d, a raw momentum interpolation or an assumed orthogonal projection. Independent nonsymmetric/nonnested fixtures reject the wrong adjoint and omitted jump terms. Reference Gram is identically absent; its zeros are not treated as independent physical validation of this sector.

## 2. Split the remaining mismatch without losing the lift

Write B_a=D_a-r_a j_a, with D the original row operator, r its hinge response and j the one-sided source-gradient jump. On fine rows define the off-space coarse extensions

    F_u = D_h Iu_H - r_h j_H u_H,
    F_eta = D_h Ieta_H - r_h j_H eta_H,
    delta_j_u = j_H u_H - j_h Iu_H,
    delta_j_eta = j_H eta_H - j_h Ieta_H.

Then the weak work splits into four terms:

    operator/weight = (B_H eta_H)^T W_H B_H u_H - F_eta^T W_h F_u,
    test-range      = [B_h(Ieta_H-d)]^T W_h F_u,
    test-jump       = -delta_j_eta r_h^T W_h F_u,
    trial-jump      = -delta_j_u (B_h d)^T W_h r_h.

The operator/weight term includes stencil, sampling, live geometry and source-map coefficient differences. It is not labeled pure quadrature error. The source partition uses each grid's actual straddling stencils; the physical widths differ. All remaining rows, including small hinge tails, are retained.

### Final MTS values

| Quantity | Normalized work |
|---|---:|
| Coarse weak pairing | +4.403423232748186e-10 |
| Fine weak pairing | +3.440673225912818e-11 |
| Difference | +4.059355910156905e-10 |
| Operator/weight term | +3.909642724505665e-10 |
| Test-range term | +1.497131965080567e-11 |
| Test-jump term | -1.142585276613665e-24 |
| Trial-jump term | -1.085847156229241e-18 |
| Source-straddling difference | +2.871096169355907e-14 |
| All-row absolute bound | 1.943049454154916e-9 |
| Separate-pairing Cauchy bound | 2.856069732159903e-8 |
| Four-channel reconstruction error | 1.66633e-22 |

There are7straddling rows on each grid, versus509/1021total rows. The jump corrections are retained but numerically negligible for this work. That does not prove source traces irrelevant to other observables or identify the whole physical force discrepancy with these weak-work numbers.

## 3. A uniform template constant derived from the existing coefficients

The original extra Gram rows factor the sourced positive third-difference form. For base-grid nodal values w,

    ||D w||_W^2 <= (q_max/h) (Delta^3 w)^T G (Delta^3 w),

where q_max=max_r(h W_r) and G is the unit-coefficient template. Its diagonal, adjacent and extra coefficients are explicitly sourced, not fitted. Each row has at most two adjacent entries and one extra entry. Their rational bounds give

    lambda_max(G) <= C_* = 59097/573104 + 2*(3/392) + 1/392
                        = 0.12097455261174238.

The actual row-sum bound on these grids is0.11067159421908299. C_* holds for every supported count>=17, with separated boundary closures, by the coefficient pattern—not by extrapolating four numerical observations.

For the lifted operator let

    w(x) = u(x) - j(u)*(x-anchor)_+.

Define S3_h(w)^2=sum_i |Delta^3 w_i|^2/h^5. Then

    ||B u||_W <= h^2 sqrt(C_* q_max) S3_h(w).

Also Delta^3=[1,-2,1]*Delta and the convolution l1 norm is4, so continuity and Cauchy on each base interval give

    ||B u||_W <= 4 sqrt(C_* q_max) ||w'||_L2.

Floating differences between the lifted matrix application, detrended application and positive-template factorization are measured and added to the numerical bounds. These measurements are not interval-arithmetic error certificates. The displayed mathematical bounds refer to ideal arithmetic with the stated operators.

Both bounds pass for all actual trial/test vectors, on both branches and both endpoints. A bound for the weak work follows by summing the products of coarse trial/test and fine trial/test bounds. For final MTS the discrete-third bound is6.97452e-8 and the mixed third/H1 bound is3.00895e-6: both are valid but much less sharp than the observed work.

Crucially, writing h^2 does NOT prove an evolving convergence rate. The measured third seminorms and mass-adjoint test norms may grow as h decreases or time evolves. The lifted H1 norm contains the source trace: ||u'-j(u)H|| is not interchangeable with ||u'||. The final coarse test has raw H1 norm1.39024e-5 but lifted H1 norm.00192793, so silently dropping that distinction would be unsound.

## 4. Derive an actual refinement bound for fixed P2 fields

A compensated continuous piecewise-quadratic field w has the representation

    w(x) = p2(x) + sum_k a_k (x-x_k)_+
                   + (1/2) sum_k b_k (x-x_k)_+^2,

where a_k are jumps of its first derivative, b_k jumps of its piecewise second derivative, and p2 is a polynomial of degree<=2. The removed source jump is subtracted at the source atom; remaining numerical mismatch is retained.

For a uniform grid,

    ||Delta^3 (x-x_k)_+||_(l2/h) <= sqrt(2h),
    ||Delta^3 [(x-x_k)_+^2/2]||_(l2/h) <= sqrt(3h^3).

The first follows from the three nonzero coefficients h*(1-theta,2theta-1,-theta), whose squared sum is at most2h^2. The second follows because at most three third differences are nonzero and each is at most h^2. Third differences annihilate p2.

Set A1=sum|a_k| and A2=sum|b_k|. Minkowski and the sourced template bound yield

    ||B u||_W <= sqrt(C_* q_max) [sqrt(2h) A1 + sqrt(3h^3) A2].

For two fixed compensated P2 fields with finite A1,A2 and bounded coefficients, the product bound tends to zero. Its general leading order is O(h); if both first-derivative jump totals vanish, the bound improves to O(h^3). This is not an O(h^4) theorem for arbitrary P2 fields, nor a theorem that actual evolving jump budgets stay bounded across discretizations.

## 5. Actual frozen-field refinement experiment

Hold the actual final257-grid trial u_H, its mass-adjoint eta_H, source position and live coarse geometry fixed. Sample these same coarse P2 functions with257,513,1025,2049base nodes. Retain the ORIGINAL coarse jump in every lift; do not silently replace it by the derivative of a new interpolant. The source cap remains2e-5. These are evaluations of a fixed bilinear form, not new evolved systems or a rerun of the force/impulse test.

| Base nodes | Signed work | Absolute row sum | Ratio to preceding magnitude |
|---:|---:|---:|---:|
|257|4.40342323e-10|1.45446862e-9|—|
|513|4.93780508e-11|4.99221019e-10|0.11214|
|1025|6.06918438e-11|1.47385615e-10|1.22913|
|2049|3.35564176e-11|5.08017023e-11|0.55290|

The apparent signed-work orders are3.16,-.30,.85: NOT monotone. No single measured order or uniform evolving convergence is claimed. The row-absolute magnitudes do decrease on these four grids. The mathematical fixed-field bound supplies the limited consistency result independently of that nonmonotone signed sequence, conditional on its stated coefficient and field assumptions.

The broad fixed-P2 product bound decreases from.00105306 to2.26818e-6 but is grossly pessimistic. A further local-kernel calculation improves it without changing fields or action.

## 6. Local derivative-jump bound, including cancellation and arithmetic

For a row with coefficients c_j and leftmost node a, expand w locally about a. Keep all polynomial moments, the gradient-jump kernel sum c_j(x_j-x_k)_+, and the curvature-jump kernel sum c_j(x_j-x_k)_+^2/2. Taking absolute values only over atoms within that row gives a localized factor majorant. The actual reconstruction residual is retained as an explicit numerical allowance; it is not renamed physical closure or assumed zero.

Multiply the trial and test majorants row by row before summing positive weights. All16products of gradient/curvature/polynomial/residual components reconstruct the signed pairing.

| Base nodes | Local atom work bound | Bound / abs(work) |
|---:|---:|---:|
|257|1.01219e-6|2298.64|
|513|1.40243e-7|2840.19|
|1025|1.61322e-8|265.81|
|2049|2.26450e-9|67.48|

This improves the global jump-total bound by roughly three orders of magnitude, but it is still not a sharp practical prediction. At2049the measured reconstruction allowance contributes3.74e-21 to the bound. The remaining looseness is largely from discarding signed cancellation between derivative-jump contributions, not from that measured arithmetic remainder. These a posteriori allowances are not a rigorous interval error budget.

## Next substantive target

The new bound identifies the exact quantities that must stay controlled: the compensated trial jump budgets and the mass-adjoint test's regularity. Next measure their evolution using saved states and derive how the mass-adjoint transfer changes those budgets. Preserve the signed local gradient/curvature cancellation rather than applying the very loose total-variation bound indiscriminately. A source-only fix, claiming fourth-order convergence from the first refinement pair, or launching a blind longer trajectory is not supported.

This Gram term is a sourced discrete third-difference remainder. Its vanishing on fixed regular fields must not be relabeled a resolution-independent new physical effect. Neither this limited consistency result nor the opposite claim that the full MTS framework vanishes follows for the complete parent theory without its continuum identification.

## Evidence and scope

Successful new implementation checks:146 (20 independent weak/template controls,52 actual weak/norm checks,37 frozen refinement checks,37 local-atom checks). They are implementation checks, not146 independent physical validations. No new failed execution; all43historical failed executions remain preserved.

- Previous seal: `source-intake/navier-stokes/20260914/annular-wave-energy-final-integrity.json`
- Independent controls: `source-intake/navier-stokes/20260914/annular-weak-Gram-algebra-attempt01/status.json`
- Actual weak split: `source-intake/navier-stokes/20260914/annular-live-weak-Gram-transfer-attempt01/status.json`
- Frozen refinement: `source-intake/navier-stokes/20260914/annular-frozen-Gram-refinement-attempt01/status.json`
- Local bounds: `source-intake/navier-stokes/20260914/annular-local-atom-Gram-bounds-attempt01/status.json`
- Sourced template: `scripts/sbp4_compatible_second_operator_20260909.py`
- Source coefficient table: `source-intake/navier-stokes/20260909/sbp4-second-derivative-derived/coefficients.json`
- Weak helper: `scripts/annular_weak_Gram_transfer_20260919.py`
- Frozen runner: `scripts/derive_annular_frozen_Gram_refinement_20260919.py`
- Local atom runner: `scripts/derive_annular_local_atom_Gram_bounds_20260919.py`

Only post-checkpoint-work is used, no GitHub or subagents. One actual single-core BelowNormal computation at a time. Protected-workbench verification is an mtime scan since14:39:53UTC, not a pre-turn whole-tree hash baseline. No claim of full GR, time-uniform stability or resolved empirical force agreement is made.
