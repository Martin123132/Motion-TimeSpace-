# Original preparation, relative phase and mean-coordinate matching

## Scope and fixed parent
This calculation continues the retained two-field MTS branch and its cold control, using the accepted GR and spatial-Poisson G192 preparations. It does not replace the action, choose a new perturbation amplitude, or reset a mode at the cold boundary. Parent evidence is ../mts-cold-coupled-background-envelope-20261108/closeout.json. Wavenumbers remain 0.32497672865575244, 0.6499534573115049 and 1.2999069146230098 Mpc^-1.

The native convention uses conformal time and N=ln(a); H in the source code is the conformal expansion rate. The physical background heavy phase is theta=atan2(-V_h,U_h), with U_h=a*m_h*phi_h and V_h=phi_h'. It is not the arbitrary carrier-coordinate angle, whose initial value is zero.

## 1. Relative phase follows from the original scalar perturbation
At a fixed background, set r²=U_h²+V_h²=2*rho_h. The retained gauge-corrected scalar perturbations are

    delta_U_h = omega_h*(delta_phi_h + V_h*alpha_gauge),
    delta_V_h = delta_phi_h' + H*(V_h,N - V_h)*alpha_gauge,
    V_h,N = -2*V_h - omega_h*U_h/H.

These plus signs are the existing native-to-physical gauge convention, not a change of gauge made here. Differentiate the scalar density and angle:

    delta = delta_rho_h/rho_h
          = (U_h*delta_U_h + V_h*delta_V_h)/rho_h,
    delta_theta = (V_h*delta_U_h - U_h*delta_V_h)/(2*rho_h),
    W = alpha_wave*delta_theta,
    alpha_wave = k²/(omega_h*H).

Thus the second relative variable is a scaled physical phase perturbation, not a freely chosen extra initial condition. Its two-by-two map has determinant -2*alpha_wave/r²; it is invertible on this nonzero-density, positive-k branch. The physical norm uses y_h=h*(delta,W), h=sqrt(rho_h)*H/k. Five symbolic identities and an independent 70-digit differentiation of rho and atan2 check the signs and factors. The cold control has no heavy phase: no division by rho_h=0 is attempted.

## 2. Full initial-state map
Let u_original be the complete original, normalized PoissonDriver state: gauge variable, fluid and scalar core, and all 190 retained tail multipoles at each of five massive nodes. B_phys maps it to physical relative coordinates. Its core is the inherited adapted energy/gauge map followed by relative rotation and h weighting; its full tail is the inherited diagonal physical weight. No hierarchy coefficient is discarded.

The exact closed metric map is R_phys; S_phys=R_phys^-1. At a frozen background and physical phase,

    y_0 = B_phys*u_original,
    z_0 = R_phys*y_0.

Both gravity branches use the SAME u_original within each model, but have their own metric-dependent R_phys. Baseline and MTS retain their own original preparations rather than being forced into the same numerical state.

For the derived closed source A(theta), the continuous frozen-clock definitions are

    Abar = integral A(theta)/omega_theta dtheta / integral 1/omega_theta dtheta,
    C_theta = (A-Abar)/omega_theta,  integral C dtheta = 0,
    omega_theta = mu - 1.5*sin(2*theta).

The retained implementation uses its existing 256-node Fourier grid. Subtracting the constant A(0) BEFORE the weighted average and then adding it back is algebraically identical and prevents a large phase-independent collision coefficient from contaminating the small phase primitive by rounding. It changes no equations, nodes or tolerances.

The correct prepared mean coordinate is therefore

    bar_z_0 = [I+C(theta_0)]^-1 R_phys(theta_0) B_phys(theta_0) u_original.

Reconstruction applies these maps in reverse. Ignoring C(theta_0), choosing theta_0=0 because the carrier chart starts at zero, or replacing u_original by a convenient late unit vector would change the initial-value problem. The saved restart packets explicitly retain each factor.

## 3. Why the full hierarchy need not be replicated for every phase
The original full G192 state is retained. For the frozen source, remote tail streaming and damping depend on the fixed background density, H, speeds and clock, not the heavy phase. Metric readout L and forcing F live in the core. The map correction lives only in the heavy rows; the product L*G reaches only the first tail through the quadrupole. Consequently the phase-dependent correction is supported within the inherited core-plus-ten block. The remote phase primitive is exactly zero in these retained equations, not a small-tail approximation. Sparse full-G192 evaluations at four phases independently test this support statement. They do not truncate the propagating hierarchy.

For the computed finite Fourier polynomial,

    sup_theta ||C(theta)||_2 <= sum_modes ||C_hat_mode||_F.

A sum below one guarantees its endpoint inverse at every phase by the Neumann bound. This is a bound for the computed polynomial; it is not a new proof that all continuum Fourier truncation error is zero. Existing 128-node subset comparisons, periodic derivative/closure tests and frozen off-grid source predictions assess the unchanged 256-node evaluation.

## 4. Exact and mean backgrounds must not be identified at preparation
The saved heavy background invariant gives

    rho_mean(N0) = rho_exact(N0)*exp(invariant_initial),
    invariant_initial = -first_corrector(N0)-second_corrector(N0).

Its nonzero initial shift is derived from the saved original phase, not an extra fit. Both maps are evaluated on the SAME original encoded vector, producing bar_z_exact,0 and bar_z_mean,0. The packets store their signed difference in every coordinate. Baseline has zero heavy-background replacement shift.

A future approximate transport can either use the mapped mean-background preparation and propagate its initial mismatch, or use a common transformed initial vector and account for the resulting reconstruction mismatch. These choices must not be mixed. The intended comparison here keeps raw preparation fixed, so it carries

    delta_bar_z_0 = bar_z_mean,0 - bar_z_exact,0

as an explicit initial error term. With a controlled reference solution and growth bound,

    ||delta_bar_z(N)|| <= growth(N,N0)*||delta_bar_z_0||
                         + integral growth(N,s)*||delta_Abar(s)*bar_z_reference(s)|| ds
                         + averaging/integration terms.

Use the actual mode-weighted forcing and both final physical maps. The previously saved cold source envelope applies only to its cold interval; it is NOT silently extended across the early-to-cold gap.

## 5. Evidence scope
The original early solution is reused, not refitted. Preparation checks compare source-derived coordinates with the native calculation, check both inverse maps over all G192 entries, and validate the early closed generator against the native source. The new mean-coordinate packets are restart-ready INITIAL data, not a propagated cold perturbation. The useful next calculation is a bounded early reference/mean evolution comparison using the already saved early trajectories, before extending across the unsolved intervening epochs.

