# From a released stellar population model to gravity

## What was taken from the sky

The input is the 39-column density-parameter FITS accompanying [Imig et al., ApJ 990, 203](https://doi.org/10.3847/1538-4357/adf723). The archive receipt and exact table live in the preceding sealed stage. These are red-giant-count-derived population models, not 186 independent gravitating point objects or direct measurements of acceleration. The survey footprint, extrapolation, stellar-evolution mass conversion and poorly sampled populations matter.

For population i, let d_i(R) be the continuous broken exponential with the two tabulated inverse scale lengths and break radius, normalized to d_i(8.122 kpc)=1. Let h_i(R)=h_i0+A_i(R−8.122 kpc). Use the tabulated median parameters. Then rho_i=C_i d_i exp(−|z|/h_i); its two-sided column to height H is C_i d_i 2h_i[1−exp(−H/h_i)]. These forms reproduce the released profile *shapes* on their grids. We retain the same finite reconstruction domain, R≤30 kpc, |z|≤10 kpc, with no new velocity-selected boundary. The integrals include the model beyond the directly sampled giants; that truncation is not evidence for a physical edge.

Catalogue reconstruction: choose C_i to make the full cylindrical integral 2π∫R dR ∫rho_i dz equal to the published surviving mass (AGED_LOG_STELLAR_MASS, including remnants). Column reconstruction: instead impose the local SMD_0 interpreted as a two-sided column through ±5 kpc, multiplied by AGED_MASS_FRACTION once. Both positive prescriptions use exactly the same 186 populated cells; they are two interpretations, not the ends of a statistical confidence interval. The scaled shape-only variant multiplies every catalogue density by a single factor 1.84245 to give the original analytic disk mass; it is not a measured stellar mass.

## Normalization provenance and a reproducible warning

[Pinned results notebook](https://github.com/astrojimig/mw_density_imig2025/blob/06ae695be167cb45bf5499e0752ec93aca41c059/results/make_results_file.ipynb), SHA-256 aa1057bff75a7bc607c8dd07f23b200dd09996aabd1f3e0c1a82ed8670a39468. [Pinned density model](https://github.com/astrojimig/mw_density_imig2025/blob/06ae695be167cb45bf5499e0752ec93aca41c059/mw_density/density_profiles.py), SHA-256 fe2892af1781933662685af93c7c05ff33b8621d908fdf9af7d61b0ae5b30fcb. The implementation is cited, not redistributed or executed here.

In this notebook the local-column calculation integrates the maximum-parameter solar profile on a positive-z mesh. The released total-mass calculation integrates the median-parameter shape on a symmetric z mesh and then in dR; that particular radial integral has no cylindrical 2πR factor. It also multiplies by ln(10) times the released NU_0 and the population count-to-mass factor. The latter factor is common and can be eliminated using SMD_0. With kpc and solar masses, the direct replay is

    M_i,aged = f_i [10^6 SMD_0 / I_z,max,positive] [ln(10) NU_0] I_Rz,median.

I denotes the release's discrete trapezoids, not the physical 3D volume integral. This identity recovers the released masses to roundoff, independently of the local cylindrical normalization we use to solve Poisson's equation. It is not a unit-based argument to multiply the reported Galaxy mass by 2π, nor a new measurement of the true mass. Settling which absolute density to use requires the selection-function normalization, geometry and isochrone mass conversion, or an independent spatial mass constraint.

## Gravity from this source

Use ∇²Φ=4πGρ, Φ→0 at infinity and g=−∇Φ. For axisymmetry and reflection symmetry, write J_l(r)=∫_0^1 ρ(r,μ)P_l(μ)dμ for even l. The coefficient multiplying P_l(μ) in Φ is −4πG times [r^(−l−1)∫_0^r s^(l+2)J_l ds + r^l ∫_r^∞ s^(1−l)J_l ds]. Inner and outer recurrences avoid high floating-point powers; outside the last matter shell retain the decaying exterior solution. Potentials supplied to the wave operator use these multipoles. The direct force on reported sky positions instead uses an independent azimuthal elliptic ring integral (no effective softening). Radial changes of variable on panels adjacent to an evaluation point and a height change of variable resolve the ring singularity. Ring-order checks, a truncated analytic Plummer sphere, and agreement of mass from boundary flux and direct cylindrical integration test different parts of the calculation. Do not substitute the multipole truncation's worst near-plane *force* for the better resolved direct rings.

## Matched nonlinear test

Let t vary from zero to one. Replace the original MN disk potential by Φ_MN+t(cΦ_star−Φ_MN), and do the same for disk forces. The originally specified bulge and compact source remain fixed. This is a controlled shared potential, not identification of a distinct bulge in the photometry. The retained heavy field solves its stationary Schrödinger–Poisson equations in this new potential at each step. The fixed-occupation experiment holds its old particle number; the matched experiment recalibrates only that number so that R g_in=(224.03 km/s)^2 at 17.58 kpc. The comparator uses exactly the same ordinary field and data point, varying only the amplitude of a fixed-scale 16-kpc NFW profile; its fixed-amplitude control keeps the old normalization. A match is neither a formation prediction nor an independent test at that radius.

Before the finite response was solved, the existing calibrated adjoint applied its saved interior potential weights and direct acceleration weights to each source difference. A centered nonlinear solve at ±1/64 and ±1/128 tests the derivative at zero; full-strength endpoints are *not* approximated by this linearization. Slope denotes dV_c/dR near 8.3 kpc, not a stellar streaming-speed gradient. Kz is signed upward at (8.3,1.5) kpc, in (km/s)^2/kpc.

## A geometry-only null for spherical gravity

At the same off-plane point define T=g_z+(z/R)g_in and μ=z/r. For an axisymmetric potential, T=−(1/r)∂Φ/∂μ at fixed r: the terms containing ∂Φ/∂r cancel exactly. Any spherical potential therefore contributes zero T, irrespective of its radial density law or amplitude. Superposition is linear for gravitational forces; subtracting the *same* ordinary-source contribution leaves zero for a spherical halo but not necessarily for the disk-loaded wave. We evaluate the wave result both by direct forces and by a fourth-order angular difference of the independently integrated wave potential at constant spherical radius, dropping its constant monopole analytically. Ordinary disk gravity itself gives a much larger T. Without independent constraints on that foreground and on both force components at matched positions this is a conditional prediction, not an observational detection, and it is not a null for flattened dark halos.

