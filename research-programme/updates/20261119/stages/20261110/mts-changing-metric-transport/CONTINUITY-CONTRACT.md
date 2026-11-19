# Diagnose the saved-history interface without a new fit

Frozen after the conditional preparation result, before this diagnostic.
The seven surviving failures are density discrepancies at k between
0.00013335 and0.00048697 inverseMpc. Their current discrepancies are below
the original gate. No new physical profile or coefficient will be fitted.

For the retained averaged background w=0, linear conservation in the actual
Newtonian gauge and velocity convention gives

    delta'=-k v+3 Phi'-3 H Pi,
    v'=-H v+k(Psi+Pi),
    S=-mu v/k,  S'=-mu(Psi+Pi),
    Pi=delta_p/rho_background, mu=am.

Here the native heavy background is the retained averaged dust budget, not
the pressure of an unaveraged coherent carrier. This probes the consistency
of that existing averaged history; it does not replace the microscopic
transport calculation or assume its next-order effective action is derived.

Integrate the equations without differentiating saved potentials:

    delta_f=delta_i+3(Phi_f-Phi_i)
             +integral[-k v/H-3 Pi] ds,
    S_f=S_i-integral[mu(Psi+Pi)/H] ds.

Use the seven original source knots for v and Pi, and the same supplied
H/Phi/Psi. Native cold uses Pi=0. Check every399modes in both histories with
8/16/32Gauss nodes over the same short interval and the original fixed
normalizers and2e-5 gate. Keep signed density residuals, flux components,
and the difference from the conditional microscopic endpoint residual.

This is an internal consistency localization, NOT a held-out test or proof
that a specific native routine is wrong. Source/output rounding, interpolation
and the approximation used for the retained closure remain possible causes.
If it reproduces the discrepancy, investigate that interface rather than
fitting the microscopic pressure or increasing already-converged quadrature.
If it does not, retain the explicit disagreement and inspect the reduction.
