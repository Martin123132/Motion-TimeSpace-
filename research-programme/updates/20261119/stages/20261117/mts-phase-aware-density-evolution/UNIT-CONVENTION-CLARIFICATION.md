# Dimensional correction to the retained metric documentation

The numerical equations and variable names are unchanged. There is a dimensional
wording error in the sealed mts-coupled-metric-consistency-20261117/DERIVATION.md:
it assigns Mpc^-1 to z and sigma alongside eta_k. The equations written in that
same file instead require z and sigma to be dimensionless in c=1 conformal units.
Keep the sealed original intact; use this explicit correction when citing it.

With tau in Mpc, k,H in Mpc^-1 and D,Q,T in Mpc^-2,

    Hz = D/(2k)+eta_k

requires eta_k in Mpc^-1 and z dimensionless. Likewise

    sigma=z+3Q/(2k^2)

requires sigma dimensionless. The trace relation then consistently has Mpc^-1
on every term: z'+2Hz-eta_k+3T/(2k). eta_k'=Q/2 has Mpc^-2.

For the retained dimensionless homogeneous/perturbation fields Phi,f, their
velocities V,g have Mpc^-1, so the scalar forcing kVz has Mpc^-2 as required
by g'. This also gives D,P,Q in Mpc^-2, J and W in Mpc^-1, beta=a/rho0 in
Mpc^2, and d_star,w dimensionless. The new kappa=3Hs/2 has Mpc^-1 and is a
local notation for the boundary coefficient, not Newton's gravitational coupling.

This is a documentation correction inferred directly from the retained constraints
and evolution equations. No data, fit, physical constant, numerical source or
acceptance threshold is changed.
