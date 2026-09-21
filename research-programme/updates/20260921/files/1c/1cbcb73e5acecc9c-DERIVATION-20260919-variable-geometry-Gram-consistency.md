# Variable-geometry consistency of the explicit Gram source force

Private continuation of `DERIVATION-20260919-localized-Gram-reaction-and-force-mesh-law.md`. This stage extends the force-consistency argument to positive variable kinetic/spatial coefficients, the actual non-rigid source map, and the WHOLE explicit Gram drive. It does not establish the full GR limit. No new live trajectory is evolved; the preceding 13.58% instantaneous MTS endpoint discrepancy is unchanged.

## 1. Result and precise scope

Let h be the uniform base-grid spacing, with source-fitted, possibly highly graded P2 elements that retain the base vertices and have maximum element length at most h. Let delta_L/delta_R be the two source-adjacent lengths. Assume:

1. The source is separated from both outer boundaries and the map is nondegenerate. On each side, R(x,b) is the inherited affine map, J=R_x>0 and c=R_b. The bounds on A=c/J and A_x are uniform.
2. The positive kinetic weight K=J R^4/C varies by at most epsilon=0.05 relative to a positive reference value WITHIN EACH element. That reference value may vary between elements. Positive quadrature is exact for the constant-weight P2 mass products.
3. The Gram row weights W_i=C_i/h are positive with C_i<=C0 and |partial_b W_i|<=beta W_i. Their derivative here holds the actual metric provider fixed, as in the existing explicit-drive split.
4. The source-zero target field u is continuous, piecewise W^(2,infinity) on the two sides, with |u'|<=U and |u''|<=M. A source derivative jump is allowed. There is no requirement of a continuous second derivative or that each wave front be fitted by the scalar mesh.
5. The source is sufficiently far from the outer Gram closures for the finite source-stencil bound to apply. All closure rows are otherwise retained and have the fixed bounded-support, bounded-coefficient properties of the inherited rule.

For the nodal interpolant u_h=I_h u, using the SAME mass, Gram and source-map rules as the existing action, the derivation below gives

    |J_G(u_h)| <= A1 h + A2 h^2(1/delta_L+1/delta_R) + A3 h^2,

with constants independent of the number of source bisections. Consequently h -> 0 and h^2/delta_min -> 0 suffice for the ENTIRE explicit Gram contribution to vanish under these hypotheses, not merely its seven source rows. The shape term is included.

This is a consistency theorem for interpolated regular fields at bounded geometry. It is NOT a theorem that the actual nonlinear trajectory stays close to those interpolants, that the metric feedback is stable, or that the complete MTS source/metric equations reduce to GR. Those distinctions are essential. A finite nonzero reaction in a weaker limit would need its own derivation rather than being declared equivalent to GR traction.

## 2. Uniform weighted P2 mass projection on graded meshes

For the unit-cell basis phi=((1-s)(1-2s),4s(1-s),s(2s-1)), exact integration gives

    M0 = [[4,2,-1],[2,16,2],[-1,2,4]]/30.

The sum of absolute basis functions is at most 5/4. For endpoint basis functions, Cauchy gives integral |phi| <= sqrt(2/15); for the midpoint the integral is 2/3. These bounds also hold for the stated positive quadrature. Thus relative weight variation epsilon bounds the endpoint and midpoint diagonal margins below by K_ref times cell length times

    d_end = 1/30 - epsilon*(5/4)*sqrt(2/15),
    d_mid = 2/5 - epsilon*5/6.

Shared-vertex assembly adds positive margins, and deleting the source degree of freedom cannot reduce them. With D_m=diag(M), the row norm of T=D_m^(-1)(M-D_m) is bounded by

    rho = max{[1/10+epsilon*((5/4)sqrt(2/15)-2/15)]/[(1-epsilon)2/15],
              [2/15+epsilon*(5/6-8/15)]/[(1-epsilon)8/15]} < 1.

The maximum-component argument applied to the projection load gives a nodal infinity-norm stability constant

    C_P = max{(1+epsilon)sqrt(2/15)/d_end,
              (1+epsilon)(2/3)/d_mid}.

At epsilon=0.05, rho=0.9170139992 and C_P=36.47467992. These constants are conservative; they are not fitted to the actual trajectories. Crucially, no ratio between adjacent element widths appears. The argument is elementary matrix control, not an imported unproved assertion of projection stability on arbitrary meshes.

## 3. The source projection defect remains localized in total mass

Define eta_L/eta_R as the weighted mass-minimizing defects with extended source value one on their own half and zero prescribed source value removed from the free coordinates. They solve M eta_side=-m_side, where m_side is the corresponding source column of the uneliminated mass matrix. Their loads touch only the two free nodes next to the source on each side; the two halves are uncoupled in this scalar mass block.

Writing M=D_m(I+T), the inverse Neumann series is valid because rho<1. The normalized source load is bounded by rho. After n band-matrix multiplications, a load initially supported on four consecutive free nodes reaches at most 4+4n nodes. Therefore

    ||eta_L||_1+||eta_R||_1
       <= sum_(n>=0) (4+4n) rho^(n+1)
       = 4rho/(1-rho)^2.

This bound is independent of source-cell width and mesh grading depth. It is about the TOTAL nodal defect, not a claim of decay with physical distance at a mesh-independent physical rate. The conservative numerical bound is 532.6308. The actual saved states give about 0.7294.

## 4. Control the complete projected force

Set B=D-r j^T, r=D(x-b)_+, as before. Let the uniform constants d0,d1,d2 bound the row absolute sum, first scaled absolute moment, and half the second scaled absolute moment of D; let d_col bound its column absolute sum and r0=max|r_i|/h. The fixed stencil/closure construction bounds these independently of resolution. It annihilates constants and affine functions in exact arithmetic. Numerical tests retain, rather than zero out, floating-point moment and hinge tails.

### Field factor

Subtract the TRUE derivative hinge from u. The resulting field has a continuous first derivative and second derivative bounded by M across the source. On either source cell, the endpoint derivative of its quadratic interpolant differs from the true derivative by at most M delta. Hence

    |j^T I_h u - Delta| <= M(delta_L+delta_R),
    |B I_h u|_infinity <= C_F M h^2,     C_F=d2+2r0.

This bound does not assume the wider stencil already lies inside a wave front. It is less sharp than the preceding exact local phase formula, but applies to piecewise W^(2,infinity) fields even where a bounded second derivative jumps inside an element.

### Projected transport

The actual transport load uses w_h=-A(I_h u)' and v=P_K w_h. Put w=-A u', with sidewise Lipschitz bound L=A1 U+A0 M, where A0 bounds |A| and A1 bounds |A_x|. The P2 derivative interpolation error is at most 3Mh on each element. Let z_h be the extended, sidewise P2 interpolant of w, retaining its two source traces w_L/w_R. Then

    v = z_free - w_L eta_L - w_R eta_R + e_h,
    ||e_h||_infinity <= C_P h[3A0 M+(5/4)L].

This follows by projecting w_h-z_h; it is not an assumed decomposition of the dynamics. Also ||v||_infinity <= C_P A0(U+3Mh) and

    |j^T v| <= 5(1/delta_L+1/delta_R)||v||_infinity.

On the finitely many source-straddling rows, these estimates and |r_i|<=r0 h give a contribution bounded by a constant times h+h^2(1/delta_L+1/delta_R).

For remaining rows, r_i=0 in exact arithmetic and the whole original stencil lies on one side. The z term is bounded by d1 Lh, the e term by d0 C_P h[3A0 M+(5/4)L]. Summing the source-defect term uses the COLUMN bound d_col and the total nodal defect from section 3, rather than multiplying its global maximum by all rows. Since the number of rows times h stays bounded on the fixed interval, the remaining projected work is O(h).

### Shape term

The bound on partial_b W_i gives

    |F_shape| <= beta C0 N_rows (C_F M h^2)^2/(2h) = O(h^2).

For the actual non-rigid map with prescribed C(R), one may use beta >= sup |C_R/C| |c| + sup |J_b/J|. Positivity and these bounds must be verified, not inferred from one sampled point. The combined estimates prove section 1. If all hypotheses and the trajectory approximation hold uniformly in time, the constants can be uniform; the present result does not supply those dynamical hypotheses.

Implementation: `scripts/annular_P2_weighted_projection_bounds_20260919.py`.

## 5. Tests with genuinely variable coefficients and a non-rigid map

`scripts/derive_annular_P2_weighted_consistency_20260919.py` uses the unchanged action formulas with a PRESCRIBED analytic metric

    U=sqrt(1-1.4/R),   N=U[1+0.02 sin(2(R-6))],

and source displacements -0.02/+0.015. It analytically bounds the positive coefficient, its logarithmic derivative, map Jacobians and kinetic-weight cell variation. The profile is the previous two-front response with s=0.77,V=0.03,D0=0.002,t=0.04, plus gradient 0.01. No fronts are inserted into the mesh. Coefficients are selected as a bounded test fixture, not fitted to a live discrepancy.

Thirty cases cover 33 through 2049 base vertices, two source-cap powers, two source positions and two reference controls. All 216 checks pass, including the weighted projection decomposition, source-defect locality, field interpolation bound, source/remaining contributions and the explicit shape term. The operator and geometry bounds are evaluated independently of the measured force.

For displacement -0.02, the h-scaled source cap gives total explicit drives -2.65041e-4 at 33, -3.27906e-7 at 513, and +7.98881e-8 at 2049. The h-squared cap gives -4.23921e-3, -8.42123e-5 and +5.66374e-5 respectively. Phase changes prevent interpreting these few values as a simple fitted order. The h-scaled sequence satisfies the derived sufficient condition; the h-squared sequence does not. Failure to satisfy a sufficient condition is not itself a proof that a particular sequence cannot converge.

The a-priori constants are deliberately loose: the 2049 h-scaled bound is about 0.0128, much larger than the actual 8e-8 drive. Their role is to establish a uniform rate under stated hypotheses, NOT to certify the parent's current force tolerance. The much sharper saved-state row bounds remain a separate diagnostic. Source: `source-intake/navier-stokes/20260914/annular-P2-variable-geometry-consistency-attempt01/status.json`.

## 6. Check the assumptions and regularity structure on actual saved states

`scripts/derive_annular_P2_live_weighted_projection_v4_20260919.py` reconstructs the existing 257/513 reference and MTS endpoint geometries. It does not replace them by the fixture metric or evolve them again. Actual finite-quadrature relative weight variation is about 0.000997/0.000502; the mass contraction is 0.750062/0.750031; the nodal projection stability bound is 7.50953/7.50769. All are comfortably within the derived sufficient bounds. These certify properties of the IMPLEMENTED quadrature mass matrix, not an unsampled continuous supremum or all future times.

The script also derives an independent Peano decomposition. For each original row define K_i(s)=sum_j D_ij(x_j-s)_+. With the source derivative hinge removed, the field has regular element curvature and ordinary derivative-jump atoms. Its row factor is the integral of K_i against those two pieces, plus the retained polynomial-moment residual. The left-endpoint atom is EXCLUDED because the initial derivative is already the RIGHT trace. Counting it again double-counts that jump when floating-point first moments are nonzero.

|Actual source-row work|257 MTS|513 MTS|
|---|---:|---:|
|Regular element-curvature contribution|+6.92109233e-6|+3.24052924e-6|
|Ordinary derivative-jump contribution|-6.96836413e-6|-3.29817810e-6|
|Polynomial-moment residual|-4.50781e-14|+8.02005e-14|
|Retained net source work|-4.72718529e-8|-5.76487736e-8|

Thus the small source factor contains a substantial cancellation between regular curvature and ordinary inter-element gradient jumps. These atoms cannot be discarded by assuming the computed P2 field is C1. The Peano absolute bound is looser than the direct row-product bound precisely because it does not use that cancellation.

The same geometric source window is used for both branches, even when reference Gram work is zero:

|Source-window diagnostic|reference257|reference513|MTS257|MTS513|
|---|---:|---:|---:|---:|
|Maximum element curvature|0.00360477|0.00348632|0.00560500|0.02152284|
|Ordinary gradient-jump variation|2.72654e-8|3.42262e-8|1.34729e-7|1.34916e-7|

MTS's source-window jump variation does not decrease between these two states, and its local curvature increases. Two levels are insufficient to infer divergence: its GLOBAL maximum curvature remains about 0.2012, essentially unchanged and above the source-window value. The correct conclusion is that the interpolant consistency result does not automatically prove stability/regularity of the computed trajectory. The reference controls are not exempt from that distinction.

All 28 checks in the final live audit pass. Three failed executions are preserved: an initial syntax error, then two failed reconstructions caused by the left-endpoint atom issue. A preliminary expansion of the floating arithmetic budget did not cure that issue; removing the double-counted endpoint atom at the root did. On the diagnostic failing row, its erroneous contribution was about 4.099e-21. No old force or live state was changed. These are validator failures, not new physical rejection tests. Source: `source-intake/navier-stokes/20260914/annular-P2-live-weighted-projection-attempt04/status.json`.

## 7. What the evolving-state gap requires

At FIXED geometry and source position, let T_h map field coordinates to their kinetic projection. Since T_h is linear and the Gram drive is quadratic, for a field defect e the exact change is

    J_G(u+e)-J_G(u)
      = -(Be)^T W_b Bu - (Be)^T W_b Be/2
        + (BT_h e)^T W Bu + (BT_h u)^T W Be
        + (BT_h e)^T W Be.

Local Cauchy bounds on these FIVE retained terms give a concrete force-controlling error criterion. Small nodal/L2 waveform error alone need not control BT_h e, because the source projection amplifies derivatives. Nor does the fixed-geometry identity include the difference between two independently evolved metric solutions; that is another part of the full stability argument.

`scripts/derive_annular_P2_Gram_trajectory_defect_20260919.py` applies this identity to the fine saved field and the coarse saved field embedded in the fine reference mesh, both evaluated at the SAME actual fine geometry and source position. This is a hierarchical diagnostic, not an estimate of the unknown exact continuum error or a separately evolved counterfactual theory. Both reference and MTS receive the same test. Its results are recorded in `source-intake/navier-stokes/20260914/annular-P2-Gram-trajectory-defect-attempt01/status.json`.

All 12 checks pass. In MTS, a maximum nodal field difference of 1.35656e-8 changes the fixed-fine-geometry explicit Gram drive by -2.97016e-8; about -2.83495e-8 comes from source-straddling rows. The source-local absolute-row bound on that difference is 2.83496e-8, so the source sensitivity is directly resolved rather than hidden inside a large global norm. The source derivative-jump difference is 9.27193e-10. Reference's comparable nodal difference of 1.35641e-8 produces zero Gram contribution, as required. These are not differences between the two actual total forces, since the diagnostic intentionally freezes the fine geometry and operator.

The next substantial target is a stable, force-controlled trajectory approximation with metric feedback, using the derived consistency and polarization bounds rather than silently imposing a smooth-source closure. No front-fitted prescribed fixture, sampled regularity value, or passed implementation check substitutes for that result. No GR/Newton/Maxwell or observational completion follows from this stage.

## 8. Preservation

The three successful validators contain 256 implementation checks. The three new failed executions remain alongside them, bringing the inherited failed-execution total from 37 to 40. None is silently edited into a success. `scripts/seal_annular_P2_weighted_consistency_20260919.py` rehashes the preceding seal and this evidence, validates the compact result table and source paths, and snapshots the resume. Its protected-workbench check is an mtime scan since 06:10:38UTC, not a claimed pre-turn whole-tree hash baseline. All work remains private, with no GitHub action, subagents, discarded modes or altered live trajectories.
