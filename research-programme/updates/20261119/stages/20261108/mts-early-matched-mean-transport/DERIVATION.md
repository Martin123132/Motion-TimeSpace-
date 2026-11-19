# Short early transport: exact retained collision rate

## Purpose and approximation under test
The previous stage derived the original full G192 preparation in physical, metric-closed and phase-mean coordinates. This stage tests a short first interval against the already saved original early solution, not against new observations. Initial data, histories, both gravity branches and both baseline/MTS controls remain fixed.

For the physical closed variable z, the retained instantaneous equation is z_N=A(sigma,theta)z. Let C_theta=(A-Abar)/omega_theta with zero phase mean, as in the preceding stage. Setting z=(I+C)bar_z along the ACTUAL background gives exactly

    bar_z,N = Abar*bar_z + Remainder*bar_z,
    Remainder = (I+C)^-1 [A*C-C*Abar-C_slow,N].

Here C_slow,N includes every non-phase source/background/clock derivative; it cannot be set to zero merely because C has zero phase mean. The present candidate evolves Abar on the saved mean background, so both this remainder and the background/phase replacement are approximations being tested. Source interpolation and solver error are separately controlled. The cold-interval error envelope is not used to certify this earlier interval.

The initial mapped mean state is reused exactly. Its signed mismatch from the original-background mapped state is evolved as a second linear response under the SAME candidate operator. Subtracting that contribution is diagnostic, not an accepted retuning of the initial amplitude.

## Why whole-matrix interpolation failed
The frozen first half-k held-out source test found an absolute error0.133218100256272 in the fine interpolant at the baryon-velocity diagonal. The coarse error was0.20017947400174307. The original table's scattering contribution accounts for that discrepancy: removing it leaves only2.191904e-11/3.290554e-11 in the rest of the matrix. The original failing attempt and predictions remain untouched.

This is a time-interpolation error in a stiff retained scattering coefficient, not evidence against MTS or an excuse to smooth the bank. Repair the representation by evaluating the scattering rate from the original source at every requested time.

## Exact source split
Let chi=kappa/H, where kappa is the retained conformal Thomson opacity and H is the conformal expansion rate. At fixed background, the physical free generator is

    G = G_without_collision + chi*C_unit.

The inherited physical collision matrix C_unit acts only on photon/baryon/polarization entries; its heavy-scalar columns vanish. Neither the physical closed maps R_phys,S_phys nor their retained background derivatives depend on kappa (sound speed is a separate retained source). Since S_phys-I has only heavy rows,

    C_unit*S_phys = C_unit,
    A_collision = chi*R_phys*C_unit.

The phase clock and averaging weight also do not depend on kappa. Therefore

    Abar = Abar_without_collision + chi*Bbar_collision,
    Bbar_collision = <R_phys*C_unit>_clock.

This retains the small induced heavy-row collision feedback; it does NOT assume Bbar_collision=C_unit. The unit matrix and noncollision remainder are interpolated; chi(N) is read directly through the original thermal cubic's scale inversion. The same decomposition is used for the baseline. No source tables, collision physics, threshold or phase nodes change.

An independent finite coefficient change (original kappa versus zero kappa in the derived source, for algebra validation only) checks this identity at both endpoints, both models, all wavelengths, multiple physical phases and both gravity branches. Zero-opacity checks are not replacement physical models.

## Frozen experiment and honest acceptance
The first saved epoch at or before N0+0.01 defines the end. Thirty-three original epoch indices define the source tests:17 even nodes for the finer interpolant,9 nested nodes for the coarser control,16 odd nodes held out. Predictions are frozen before their full source evaluations. Five original epochs at indices0,8,16,24,32 supply physical readouts.

The full G192 remote streaming/damping remains present. Its phase-independent entries are shared by the gravity branches and never replaced by zero tails. DOP853 uses original rtol2e-12/atol2e-14 with the state scaled numerically by its original physical norm, not a changed physical amplitude. Coarse/fine time steps and source interpolants are compared separately before reference performance is inspected.

The physical phase is integrated from the actual original initial angle on the candidate mean background. Reconstruction uses C(theta), S_phys and the physical/gauge inverse, then the native observable readout. The original carrier phase is used only as an encoding chart, not as the physical heavy phase or a fitted source.

The ten retained observables are Phi, Psi, D, Q, Pi, theta_c, delta_c, delta_b, delta_gamma and delta_massless. Each discrepancy is divided by its own maximum reference magnitude over the five original epochs, using the same relative-comparison convention as the original evolution. GATE=2e-5 is unchanged. Comparison results must distinguish numerical validation from a failed or successful physical approximation test. A failed physical comparison remains a valid completed test and determines the next derivation; it is never relabelled as a pass.

