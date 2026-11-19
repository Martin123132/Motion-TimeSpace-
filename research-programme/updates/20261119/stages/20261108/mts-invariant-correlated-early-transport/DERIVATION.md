# Invariant-correlated density and full-hierarchy transport

This is a correction within the retained two-field action and original mode preparation. It is not a new model, a new fit or a reset at a late epoch. The frozen plan in PLAN.md and the preceding sealed density theorem specify its scope.

## 1. Reconstruct the physical density, not a mean substituted into physical stress

At fixed slow data let rho_bar = rho_initial exp[-(N-N_initial)+I_initial]. Write rho = rho_bar exp(delta), u = H/omega_h, f = rho/(3H^2), and

    H^2 = [R_ext + (U_s^2 + V_s^2)/2 + rho]/3
    eta_0 = [R_ext,N + U_s^2 - 2 V_s^2 - rho]/(6H^2)
    A = 3(1-eta_0)/2, B = 9(2-f)/8
    g = 3u sin(2theta)/2 - A u^2 cos(2theta)/2 - B u^2 cos(4theta)/4.

The candidate solves delta = g(rho_bar exp(delta),theta). The exact invariant relation instead contains +Delta_I. Setting that remainder to zero specifies an approximation, not a newly asserted conservation law. The preceding proof gives a unique positive fixed point within |delta| <= .02, with contraction below .000759 under its positive-source and u < .001 hypotheses. This box is an existence region, not a changed physical tolerance.

The derivatives used to test the implementation are

    g_x = 3 f u sin(2theta)/4 - 9 f u^2 cos(2theta)/8
          - 9 f u^2 cos(4theta)/32
    g_theta = 3u cos(2theta) + A u^2 sin(2theta) + B u^2 sin(4theta)
    delta_theta = g_theta/(1-g_x).

All derivatives here hold the slow invariant data fixed; x = ln(rho). Independent high-precision roots and differentiation test the floating-point implementation. The bound |Delta ln(rho)| <= |Delta_I|/(1-q) addresses invariant drift alone. Errors in retained slow-scalar and conformal-clock histories are separate terms.

## 2. Evolve an independent physical phase

    theta_N = omega_h/H(rho_rec(theta)) - 3 sin(2theta)/2.

Use the ORIGINAL initial physical phase, not the carrier angle used by the native perturbation representation, and not an interpolated original phase trajectory. The saved slow scalar and conformal clock are retained for this isolated comparison. The preceding implicit derivative shows the rapid omega/H cancels from the phase Lipschitz estimate; its bound is below 4.504551 on the stated box. Actual phase-step refinement is still checked.

## 3. Correlated phase average and the complete periodic map

Freeze the invariant and slow data, NOT instantaneous rho. For Omega(theta) = theta_N > 0,

    <F>_clock = integral F(theta)/Omega(theta) dtheta
               / integral 1/Omega(theta) dtheta.

H now varies with theta. The older closed-form period for constant omega/H must not be reused. Use the retained 256-node phase quadrature, its 128-node control and independent off-grid checks. A computed Fourier-polynomial norm bound is not a continuum quadrature error theorem.

Outside the compact core plus ten retained tail coordinates, full G192 has

    A_remote(theta) = D_remote + S_remote/H(theta).

The diagonal drift and off-diagonal streaming factor are independent of theta at fixed slow data, including the couplings crossing the compact boundary. Therefore

    Abar_remote = D_remote + S_remote <1/H>_clock
    (p_H)_theta = [1/H - <1/H>_clock]/Omega(theta)
    C_full = embed(C_compact) + p_H S_remote.

Choose zero phase mean for each primitive. All 190 tail levels at each of five massive nodes remain. Their phase correction is not discarded merely because the older fixed-rho construction had a phase-independent remote hierarchy. Four grid phases and independent off-grid phases test the exact sparse decomposition. Bound the Fourier polynomial by the sum of compact coefficient Frobenius norms plus sum|p_H_mode| ||S_remote||_F. A bound below one gives invertibility of I+C_full for that polynomial.

## 4. Preserve the exact collision-rate dependence

At fixed N the original opacity kappa is phase-independent, but H is not. The unit physical collision matrix C_unit has zero heavy input columns; the first physical shear S_phys differs from identity only in heavy rows. Thus C_unit S_phys = C_unit and

    partial_kappa A = R_phys C_unit/H
    Abar_collision = kappa <R_phys C_unit/H>_clock.

Retain the induced heavy-row feedback in R_phys. Interpolate the smooth noncollision source and averaged coefficient separately; evaluate kappa from the ORIGINAL thermal cubic at every RHS. Do not interpolate the old stiff whole matrix, change the table or silently replace <1/H> by 1/<H>. Independent opacity-zero differences test this identity for both baseline and MTS.

## 5. Original preparation and physical output maps

Let B_phys map the original normalized native vector into physical energy coordinates. Then

    y_initial = [I+C_full(theta_initial)]^-1 R_phys B_phys u_original
    u_predicted = B_phys^-1 S_phys [I+C_full(theta)] y.

The full sparse inverse is used at the initial endpoint. At output times the native carrier chart is restored separately from the predicted physical phase. Both gravity branches start from the SAME original prepared vector for a given model. No amplitude is fitted, no unit perturbation is injected at the cold entrance, and no initial mismatch is subtracted from the final results to force acceptance.

## 6. What the transport tests, and the next remainder

The candidate evolution here is y_N = Abar y over the same original approximately .01 e-fold interval with five fixed physical readout epochs, three wavenumbers, baseline/MTS, and GR/spatial-Poisson. Source interpolation has 17-node and 9-node controls plus 16 independently evaluated held-out times; propagation has 128-step and 64-step maximum-step controls. ALGEBRA = 1e-10 and GATE = 2e-5 remain unchanged. Frozen outputs precede opening the original perturbation reference for comparison. Background reference data used for matching and diagnostics are explicitly distinguished from those perturbation outputs.

For a source A on a chosen background, z = (I+C)y and Omega C_theta = A-Abar imply the exact residual

    y_N = Abar y + R y
    R = (I+C)^-1 [A C - C Abar - D_slow C].

Here D_slow differentiates the frozen source coefficients along their retained slow histories, excluding the already-accounted-for phase derivative. This term is NOT included in the leading mean evolution. Physical background-substitution errors, including derivative-map consistency with that substituted history, must also be carried when comparing to the original physical system. Numerical agreement at five times is a controlled local test, not a bound on those terms along an uncomputed long trajectory. Use the measured residuals to decide whether the next step is its mode-weighted remainder or a background-history correction; do not refit the unchanged target or borrow the reference phase.

## Provenance

Parent: ../mts-early-matched-mean-transport-20261108/closeout.json, SHA256 ba7c097d8015ca0bad8594b4e6be1dffa7b110edbe7d85523392433590d868db. Its DENSITY-RECONSTRUCTION.md supplies the fixed-point theorem; its failed frozen-rho physical comparison remains intact. Each phase saves input/source hashes; audit/result.json and closeout.json inventory the accepted outputs and any preserved failed attempts.
