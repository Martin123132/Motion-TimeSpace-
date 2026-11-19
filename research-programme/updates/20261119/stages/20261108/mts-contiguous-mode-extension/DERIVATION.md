# Contiguous propagation of the same original perturbation

Parent: ../mts-derived-correlated-transport-remainder-20261108/DERIVATION.md and its sealed numerical results. All fields, gauge maps, G192 tails, opacity/thermal tables, physical phase and baseline control are retained. The present change is the time domain, not a new action, fitted coupling, unit mode or altered tolerance.

## Exact joining data

At N_b the incoming state is the preceding candidate's corrected y_b = y0_b + delta_b. Its physical phase theta_b is also the preceding candidate's value. The saved invariant normalization, slow background and clock histories are global; none is re-anchored to the reference. The source coefficient M, full primitive C and slow derivative C_N at N_b are the same operators as before. The forcing R(N_b,theta_b) y_b must be re-applied to y_b: reusing a saved vector R y0_b would omit R delta_b.

Boundary reuse reconstructs A = M + Omega C_theta on the unchanged discrete Fourier phase representation. Three independent full source evaluations check this reconstruction; the original vector's force is reproduced separately. The inherited C_N remains its previously qualified derivative, not a newly asserted exact zero. New interior nodes rederive C_N and the background-path coordinate defect as previously.

## New interval response

On the next approximately .02 e-fold interval:
    
    y0_N = M y0,                    y0(N_b) = y_b
    delta_N = M delta + R y0,        delta(N_b) = 0
    y_candidate = y0 + delta
    z_candidate = (I+C) y_candidate.

This zero initial NEW correction does not erase the old correction or reset the physical perturbation. It restarts the variation-of-constants expansion from the inherited candidate. The omitted term on this interval is R delta; old numerical/approximation error is still in the incoming data. Normal-form and background-map forcing are propagated separately with the same exact collision split. Fine/coarse maximum time steps are doubled with the interval length, retaining the preceding physical maximum step. The independent physical phase is integrated from theta_b.

## What error is carried

For the exact generator K=M+R on the chosen background and an approximate trajectory y_a whose defect is d=y_a'-K y_a, the exact error e=y_a-y obeys

    e(N) = U_K(N,N_b)e(N_b) + integral[U_K(N,s)d(s) ds].

With exact first-response evolution, d=-R delta. Coefficient interpolation, time integration and phase reconstruction contribute further defects. Difference between the chosen and original physical background contributes a separate source term when comparing with the original equation. Consequently the previous measured discrepancy and numerical controls cannot be dropped or simply equated to a final bound.

The inherited-error records carry prior channel/state discrepancies and both leading/correction controls. The new comparison uses the SAME original reference from its original preparation. It measures accumulated discrepancy across the join, not a locally reset test. A rigorous uniform upper bound would additionally require a controlled propagator gain and integrated remainder/background defects; this stage does not manufacture those from the measured comparison. Invariant drift, slow-history, clock and higher-response errors remain named separately.

## Frozen tests

The 33 source epochs, 17 coefficient nodes and 16 independent interpolation probes are selected from the original time grid before opening the new reference perturbation values. Five physical probe epochs are frozen in advance. Compare both models, all three original wavenumbers and both GR and spatial-Poisson branches across ten original channels. Verify the physical readout at the join matches the previous candidate. Retain ALGEBRA=1e-10 and GATE=2e-5. This is an internal equation/approximation test, not a new observational holdout or a claim that the whole path to the cold entrance is already transported.

