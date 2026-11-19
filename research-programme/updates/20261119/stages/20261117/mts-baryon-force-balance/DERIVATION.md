# Accumulated baryon force on retained metric histories

This stage reuses the sealed 32/64 histories, not a new scattering bank or evolution.
Native equations.f90:2458 supplies v_b'=-H v_b+k pi_b-Gamma_b S_v,
where pi_b=delta_p_b/rho_b, Gamma_b=4 B_gamma opacity/(3 B_b),
S_v=v_b-3 q_gamma/4, B_i=kappa a^2 rho_i, and r=a'/a.
Primes differentiate conformal time in Mpc; k,H,r,opacity have units Mpc^-1;
a,v_b,q_gamma,sigma,pi_b are dimensionless. Native transfer is -k(v_b+sigma)/H.

With u_N=v_b+sigma and k Psi_kin=sigma'+r sigma:

    (a u_N)' = a[k Psi_kin+k pi_b-Gamma_b S_v+(r-H)v_b].
    a u_N - a0 u_N0 = a sigma-a0 sigma0 + integral F d tau,
    F = a[k pi_b-Gamma_b S_v+(r-H)v_b].

Thus reconstructed u_N is sigma+(a0 v_b0+integral F)/a. Initial matching is
carried exactly once at the earliest time, not independently reset for each
overlapping preparation window. The metric endpoint is retained exactly; it
is not omitted and is not an independently predicted force history.

Source derivatives read independently from saved baryon stress are
v_b'=(Q_b'+r Q_b)/B_b and (a v_b)'=a[Q_b'/B_b+2r v_b]. These check the
Euler identity but do NOT provide interpolant derivatives for the force
integral. The integral uses pressure, photon drag and background contact only.

For responses, use exact quotient and product differences before quadrature:
Delta(N/D)=[Delta N-(N_old/D_old)Delta D]/D_new;
Delta(XY)=Delta X Y_old+X_new Delta Y. No tiny baseline change is declared
resolved merely because the much larger full velocity converges.

Original scale-clock and field-table corners define piecewise integration
regions. No invented corner sample: an interval spanning a missing corner uses
a recorded linear bridge. Within regions use PCHIP primitives, with the fixed
decimation and independent trapezoid checks in protocol.json. These provide a
working numerical estimate, not a rigorous continuum bound or new observation.
Every corner bridge is reported; closure against saved velocity is an
independent endpoint check on the summed force, not proof of each term's
accuracy. The native stress Weyl potential remains distinct from Psi_kin.

Quantum measure and prior full-source pressure budget remain separate. This
stage does not transport that complete uncertainty into an observed sky.
