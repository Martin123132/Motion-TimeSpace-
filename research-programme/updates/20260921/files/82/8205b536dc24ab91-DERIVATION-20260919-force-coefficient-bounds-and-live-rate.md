# Force-coefficient bounds and the live rate law

Private continuation of `DERIVATION-20260919-source-trace-projection-and-force-law.md`. This stage measures the proposed force-sensitive field bound, derives a geometry-response estimate from the existing mass equations, and tests the coefficient rate along the full canonical direction. It does not establish the full GR limit. The existing 12.5718% integrated and 13.58% instantaneous MTS/continuum discrepancies are unchanged.

## 1. Precisely what is being bounded

The preceding finite model gives

    J_G = S + k^T s + J_reg,
    k_sigma = (B R_sigma)^T W f,
    R_sigma = P e_sigma,

where e_sigma is the piecewise constant on one side of the source, P is the unchanged mass projection with the existing zero-source scalar condition, B is the lifted Gram operator, W its positive row weights and f the lifted field factor. All physical modes remain. These are diagnostic coefficients, not new fitted parent couplings or a two-degree-of-freedom replacement theory.

The actual 257/513 hierarchy is nonnested and uses unequal time steps. The final time is T=4e-5 in normalized annular units, not calibrated SI. The following hierarchy differences are not unknown continuum errors. Both reference and MTS, initial and final saved states, all rows, and full all-label geometry are retained.

## 2. A sharp field-functional bound, not a broad energy norm

At fixed fine geometry, comparing the actual fine field and the original off-space coarse field,

    Delta k_sigma = (B R_sigma)^T W Delta f,
    s_bar^T Delta k = sum_i g_i Delta f_i,
    g_i = W_i (B R s_bar)_i.

Hence

    |s_bar^T Delta k| <= sum_i |g_i Delta f_i|,

with a distinct, usually looser weighted Cauchy bound. The off-space coarse field uses its original gradient/source jump, not an assumed exact embedding.

### Actual final MTS comparison

| Quantity | Value |
|---|---:|
| Measured coefficient channel | -2.83308619487e-8 |
| Rowwise absolute bound | 2.83308619496e-8 |
| Weighted energy bound | 5.26423325e-7 |

The rowwise bound is essentially sharp for this particular saved difference; it is not a uniform bound on every possible perturbation. It controls the same coefficient channel that accounted for about 95.4% of the preceding fixed-geometry field comparison, not 95.4% of the full physical continuum discrepancy.

### Curvature and ordinary gradient jumps cannot be separated away

The off-space Peano representation is evaluated on the union of coarse polynomial breaks and fine stencil knots. The source gradient atom is removed exactly by the original hinge lift; ordinary interior gradient atoms remain. The left endpoint atom is excluded because the initial slope is its right trace. Floating polynomial moments are retained.

For the final weighted coefficient difference:

    regular curvature contribution = -8.81956737e-7,
    ordinary gradient-jump contribution = +8.53625874e-7,
    polynomial-moment contribution = 3.85e-23.

Their cancellation leaves the observed -2.83309e-8. A separated absolute Peano bound is 1.73558e-6 and is much less useful. Discarding the gradient jumps would badly misidentify the response. An independent piecewise-quadratic, nonnested ordinary-knot fixture explicitly detects that omission.

The floating reconstruction discrepancy is 5.88e-16, but its conservative arithmetic allowance is 2.27e-10. That allowance is about 0.8% of the final channel and exceeds the much smaller INITIAL coefficient channel. Thus this test does not certify the tiny initial curvature/jump allocation to many digits. The sharper rowwise bound uses direct field factors and does not depend on that separated allocation.

## 3. Geometry response from the mass equations

Let Phi evaluate free scalar basis functions at the original fixed reference quadrature nodes, omega be the positive kinetic quadrature weights, and

    M = Phi^T diag(omega) Phi,
    M R_sigma = Phi^T diag(omega) e_sigma.

For two geometries on the SAME reference mesh,

    M_1 (R_1-R_0)
       = Phi^T diag(omega_1-omega_0) (e-Phi R_0).

This identity retains the full coefficient change, rather than declaring the geometry fixed in the actual evolution. For any force covector a_1, set z_1=M_1^-1 a_1 and epsilon_0=e-Phi R_0. Then

    a_1^T (R_1-R_0)
      = sum_q (omega_1-omega_0)_q (Phi z_1)_q epsilon_0,q,
    |a_1^T (R_1-R_0)|
      <= ||a_1||_(M_1^-1)
         ||[(omega_1-omega_0)/omega_1] epsilon_0||_(omega_1).

A localized sum of the absolute quadrature products is also available. The projection defect epsilon is essential: bounding by a whole constant field throws away the projection cancellation.

For a field factor f held fixed, the COMPLETE finite geometry change of k is

    Delta k_sigma = (B Delta R_sigma)^T W_1 f
                    + (B R_0,sigma)^T (W_1-W_0) f.

In the actual final MTS geometry pair, the left/right coefficient changes are approximately 3.47563e-16 and 2.61106e-16. Their direct-versus-split differences are approximately 2.22e-23 and 4.68e-23. Gram-weight variation dominates these particular changes. These small numbers describe this comparison only; they do not establish general metric decoupling, and are floating evaluations rather than interval certificates.

## 4. Exact rate law along the unchanged equations

With fixed reference topology and differentiable positive weights, differentiating the SAME mass equation gives

    M dot(R_sigma) = Phi^T diag(dot(omega)) epsilon_sigma,
    epsilon_sigma = e_sigma-Phi R_sigma.

Since B and the reference basis are fixed, let f_dot=B u_dot for a field in that space, a=B^T W f and z=M^-1 a. The exact coefficient rate is

    dot(k_sigma)
      = (B R_sigma)^T W B u_dot
        + sum_q dot(omega)_q (Phi z)_q epsilon_sigma,q
        + (B R_sigma)^T dot(W) f.

The terms are respectively field evolution, mass-projection geometry response, and Gram-weight geometry response. The central field is not assumed dynamically closed: u_dot and geometry belong to the full coupled all-label canonical state.

If gamma bounds |dot(omega)/omega| and eta bounds |dot(W)/W| on the finite quadrature/rows, then

    |dot(k_sigma)|
      <= sum_i |W_i (B R_sigma)_i (B u_dot)_i|
         + gamma ||a||_(M^-1) ||epsilon_sigma||_omega
         + eta ||f||_W ||B R_sigma||_W.

This is a conditional rate inequality. Controlling its ingredients over a time interval, with preserved geometry positivity and canonical solvability, is still required for an evolution/stability certificate. A finite set of endpoint measurements does not supply those uniform hypotheses.

### Canonical tangent tests

The entire saved fine endpoint state is perturbed as y +/- h F(y), using the actual full canonical RHS, not a selected central component. Geometry is re-solved at each probe. The probes are not evolved trajectories. Step sizes are 2e-7, 1e-7, 5e-8 and 2.5e-8; all scalar modes remain.

For total MTS left/right coefficients at the smallest probe:

| Term | Left | Right |
|---|---:|---:|
| Field rate | -0.562943695 | -0.422945533 |
| Mass-response rate estimate | 2.24e-14 | 3.08e-14 |
| Gram-weight rate estimate | 9.43795e-8 | 7.11254e-8 |
| Total predicted rate | -0.562943601 | -0.422945462 |
| Conditional rate bound | 0.602893751 | 0.452960589 |

Direct differences of k agree with the rate formula within 1.19e-7 and 8.86e-8 over the four total-coefficient probes. The errors are NOT monotone under step halving; subtraction/reconstruction sensitivity prevents claiming derivative convergence from that sequence. Checks use the explicitly recorded tolerance 3e-5 times the rate scale plus 3e-9. Geometry rates remain finite-difference estimates, not certified derivatives. The tiny mass rates fluctuate by several percent across probe sizes and should not be quoted as high-precision physical predictions.

Independent dense nonzero fixtures verify the differentiated mass law, rate decomposition, positive-weight bound, second-order difference convergence, and a negative control which fails when geometry terms are dropped. A target already in the finite-element span has zero geometry response, as required. Reference Gram rates vanish by construction; this is disclosed rather than treated as a nonzero physical test.

## 5. A useful exact cancellation: uniform weight scaling cannot drive the projection

Galerkin orthogonality gives

    Phi^T diag(omega) epsilon_sigma = 0,
    sum_q omega_q (Phi z)_q epsilon_sigma,q = 0.

Writing chi=dot(omega)/omega, any constant chi_0 can therefore be subtracted:

    mass_rate = sum_q omega_q (chi_q-chi_0) (Phi z)_q epsilon_sigma,q.

If chi is spatially constant, dot(R)=0: uniform scaling of the mass and its load cannot change their projection. This is a derived property of the existing weighted projection, not a new physical symmetry postulate.

For a practical upper bound, choose chi_0 as the weighted median of chi with weights |omega(Phi z)epsilon|. It minimizes the centered absolute sum. This is mathematical optimization of a bound, not fitting a coupling or modifying data. Numerically, retain the nonzero orthogonality residual r instead of silently replacing it by zero:

    mass_rate = sum_q omega_q (chi_q-chi_0) (Phi z)_q epsilon_q + chi_0 r,
    |mass_rate| <= sum_q |omega_q (chi_q-chi_0) (Phi z)_q epsilon_q| + |chi_0 r|.

All terms, including small tails, remain. A uniform-weight control gives zero centered bound despite a nonzero uncentered absolute sum; a nearly uniform control demonstrates why discarding this cancellation is misleading.

### Actual saved rate estimates

| Smallest-probe MTS mass term | Left | Right |
|---|---:|---:|
| Estimated signed rate | 2.24239e-14 | 3.07993e-14 |
| Uncentered absolute bound | 4.55791e-8 | 2.34025e-8 |
| Centered absolute bound | 2.24745e-14 | 3.08488e-14 |
| Retained floating orthogonality correction | 4.41e-23 | 1.83e-23 |

The large improvement is in the bound on an unchanged estimated quantity. It is NOT an improvement by those factors in MTS's physical agreement. The input-rate uncertainty from the probe study remains; centering does not turn finite differences into a certified continuum derivative.

## 6. What follows and what does not

We now have a sharp observed field-functional bound, a non-vacuous geometry-response law, a tested instantaneous canonical rate decomposition, and a substantially sharper mass-response bound using orthogonality. None alone proves that the force-sensitive field difference remains small over time. Curvature/jump cancellation and rapid field evolution are still central.

The actual final fixed-geometry hierarchy driver s_bar^T R^T B^T W Delta(f_dot) is about +0.01607, while the coefficient difference is about -2.83e-8. This is an instantaneous driver, not the full time derivative of that weighted comparison. It cannot be multiplied by the whole interval to predict error growth; phase cancellation and changing geometry/source values matter.

The next derivation should control that field driver through the canonical momentum residual rather than merely tighten geometry bounds. For actual scalar velocities v, source velocity V, kinetic cross-load b and scalar momentum p,

    p_h = M_h v_h + b_h V_h + r_h,
    rho_h = p_h-b_h V_h-M_h I_h v_H,
    v_h-I_h v_H = M_h^-1(rho_h-r_h),

where r_h is the actual inverse-momentum residual, retained explicitly. Nonnested transfer also contributes to the lifted gradient:

    Delta(f_dot) = B_h(v_h-I_h v_H)
                   + r_lift,h (jump_H(v_H)-jump_h(I_h v_H)).

Thus for the fixed force-row covector g the exact driver has the residual representation

    g^T Delta(f_dot)
       = (B_h^T g)^T M_h^-1(rho_h-r_h)
         + (g^T r_lift,h) [jump_H(v_H)-jump_h(I_h v_H)].

The coarse velocity retains its own live geometry; it is not silently recomputed on the fine geometry. This law is derived here but its useful numerical bound has not yet been tested. It identifies the next measurable dynamical quantity, including the transfer-jump and inverse-solve terms, before a new expensive evolution or any claim of nonlinear stability.

## 7. Reproducibility and limits

Successful runs complete 359 implementation checks: 22 independent algebra/Peano controls, 127 actual field/geometry checks, 52 canonical tangent checks per branch, and 106 centered-bound checks. These counts are software/mathematical checks, not independent experiments supporting MTS. One new failed execution is preserved: the first actual-bound runner used max(empty) when the reference Gram sector correctly had no rows. Its successor uses the neutral empty reduction without changing any MTS formula or tolerance. The historical failure count becomes 43.

Sources:

- `scripts/annular_force_coefficient_bounds_20260919.py`
- `scripts/validate_annular_coefficient_geometry_law_20260919.py`
- `scripts/derive_annular_live_coefficient_bounds_20260919.py` (failed attempt retained)
- `scripts/derive_annular_live_coefficient_bounds_v2_20260919.py`
- `scripts/derive_annular_live_coefficient_rate_20260919.py`
- `scripts/derive_annular_centered_geometry_bound_20260919.py`

Evidence:

- `source-intake/navier-stokes/20260914/annular-coefficient-geometry-algebra-attempt01/status.json`
- `source-intake/navier-stokes/20260914/annular-live-coefficient-bounds-attempt01/status.json`
- `source-intake/navier-stokes/20260914/annular-live-coefficient-bounds-attempt02/status.json`
- `source-intake/navier-stokes/20260914/annular-live-coefficient-rate-MTS-attempt01/status.json`
- `source-intake/navier-stokes/20260914/annular-live-coefficient-rate-reference-attempt01/status.json`
- `source-intake/navier-stokes/20260914/annular-centered-geometry-bound-attempt01/status.json`

All outputs remain private and non-claim. No public push, source action alteration, removed mode, subagent, protected-workbench edit or new long trajectory is performed. The final seal checks inherited hashes, compilation, sourced tables and a protected-directory modification-time scan; the latter is not a pre-turn whole-tree hash baseline.
