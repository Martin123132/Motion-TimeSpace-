# From the resolved gas drive to a tide that cannot be removed by changing frames

## Inputs and scope
Start with the sealed ordinary-centre recoil stage and its 12 wave/ordinary histories. Only replace the external differential force on the two specified gas components. Keep the parent metric coupling, stellar calibration, gas densities, chosen fixed wave occupation, odds/even sector split, common-frame convention and fixed signed bands. Reuse the six [Vasiliev simulated histories](https://doi.org/10.5281/zenodo.8015660), not six statistically independent observed trajectories. The ordinary density is still rigidly translated, the wave can deform, and NFW is the retained static control.

## Resolving hydrogen without a Galactic angular expansion
For each gas component use its saved surface density Σ(R)=Σ₀ exp(−R_m/R−R/R_d) and even, normalized vertical profile. For the planar complex vector x−iy integrate by parts:

    a_g − a_point = M_g⁻¹ ∫ d³x  [Φ_s(x−D)−Φ_s(−D)−x⋅∇Φ_s(−D)] e^(−iφ) ∂Rρ_g .

This is the negative potential gradient averaged over the gas, with the shared acceleration removed. In the integrand ∂Rρ_g=ρ_g (R_m/R²−1/R_d). The z part of the subtracted linear potential integrates to zero in this planar component. No Galactic spherical-harmonic cutoff is used for this replacement. Keep all 49 original satellite coefficients through degree six and the same radial interpolation.

Use u=|z|/h. The folded density is 2 exp(−u)/(1+exp(−u))². Its even moments are 2(2j)!(1−2^(1−2j))ζ(2j) for j≥1, with unit zeroth moment. Build positive Gaussian quadrature for u² and verify these moments. Split the radial integral also at every appearance/disappearance of a satellite radial knot on an azimuthal ring, separately for both signs of z. For a knot k these boundaries are |D_R−sqrt(k²−(D_z±z)²)| and D_R+sqrt(k²−(D_z±z)²) when the square root is real. The retained full-azimuth integrator separately splits the angular variable at the knots. Reuse the tested 240-kpc radial integration limit. Three vertical/radial/azimuthal orders and the previous uncompressed vertical integrator check this reduction. A synthetic cubic is checked against analytic cylindrical gas moments, not against the same quadrature.

Evaluate on the **entire** archived source-time grid, not just at present and not by interpolating six endpoint repairs. At the old points the original projected body accelerations are cached. For the additional half-steps of L2M11 the old source is calculated from the already saved midpoint shell bank and the original weights. For each ordinary foreground, with its original mass M_b, the only new source is

    e(t) = Σ_g (M_g/M_b) [a_g,direct(t) − a_g,projected(t)] .

The wave-minus-ordinary external drive changes by −e, not +e. All comparisons are complex vector comparisons. The superseded projected gas must not also be added to the new source.

## Exact propagation of the saved source representation
Let ω,W be the saved coupled-mode frequencies and positive centroid residues, τ=tV/L, u=V²/L and K=sin(ωΔτ)/ω. Each scalar channel solves q''+ω²q=−e/u with zero initial data. The added centroid is L ΣWq; additional sky readouts use their saved signed residues. Only the material-frame sky readout includes the instantaneous projection of e. A shared external acceleration changes neither the relative wave–matter driver nor the site-minus-point baseline. The static NFW control has no induced wave, but receives the same foreground convention.

Use exact Legendre–spherical-Bessel convolution of the piecewise quartic source as in the original response. A second, final-time calculation uses monomials and integration by parts against exp(−iωt), with low-frequency Gaussian integration to avoid cancellation. Map back into the original spatial modes, check the independent body-force integral and both observing-frame projections. The second calculation does not run the original forced wave a second time.

On each interval write the complex acceleration as a fourth-degree Bernstein polynomial with coefficients b_j. Nonnegative basis functions integrate to Δt/5, hence

    Δt |Σ b_j/5| ≤ ∫ |e(t)| dt ≤ Δt Σ |b_j|/5 .

Subdivide the represented polynomial for tighter bounds; this is **not** generating physical data or presuming a phase. The time coordinate is kpc/(km/s), so the impulse is in km/s. The bound on any centroid change is (1000 L/V) Σ W/ω times this upper impulse, in pc. The analogous sky bound uses absolute signed readout residues, plus a separately evaluated instantaneous shift for the material frame. The inequalities apply rigorously to the adopted polynomial up to numerical rounding, not to arbitrary unknown variation between source evaluations. Test variation separately on nested time samplings and with frozen predictions at one independent non-grid time in every archive interval. In the latter choose the test panel by the greatest original projected HI fourth difference in that interval, not by the performance of the replacement. These are numerical controls on simulated histories, not observational holdout tests.

## A source-independent geometric diagnostic
Use the original traced outer bands from [Lim et al., Figure 9](https://arxiv.org/html/2305.13358v3#S3.F9), for spherical a_r and a_θ at the same azimuth, R=6 and 8.3 kpc, z=±h=±1.5 kpc. They are acceleration reconstructions assuming approximate tracer equilibrium. Combine the **actual separate north and south values**, not a reflected copy. Set r=(R²+z²)^(1/2); a_z=(z/r)a_r−(R/r)a_θ. The observable

    K(R)=[a_z(R,−h)−a_z(R,+h)]/(2h)

is invariant under *every uniform vector acceleration*. It measures the vertical Hessian of the potential averaged across the slab, not the midplane value or a vertical oscillator frequency measured in isolation. In the weak, slowly varying Newtonian metric and the geodesic-deviation convention d²ξ_z/dt²=−c²R_(0z0z) ξ_z, K/c² is the associated mean tidal curvature. No relativistic or strong-field completion is inferred from two Galactic radii.

Project the cartesian product of the four original component intervals exactly with sign-aware interval arithmetic. With unknown covariance this is a conservative **conditional envelope if all component intervals are met**; it is not a joint 95% interval or a new significance. For each prepared prediction let I_R=[K_low−K_model,K_high−K_model]. Every allowed correction must lie in I_R. If inf I₆ > sup I₈.₃, even adding any constant tidal tensor plus any uniform acceleration is insufficient. The extra slab-averaged vertical curvature must *decrease* by at least inf I₆−sup I₈.₃; for a smooth correction its radial derivative must be at most minus that gap/2.3 kpc somewhere. This is a bound on an averaged third potential derivative, not on the Newtonian constant. Compute both marginal envelopes and test an arbitrary symmetric affine force field against **all eight** original inequalities as an additional feasibility control, not an MTS fit.

For clarity the integrated Poisson identity is K=4πG ρ̄ + mean[div_horizontal a_horizontal]. A surface-density equivalent requires a separately stated condition on the horizontal divergence correction. Neither K nor its radial difference alone measures a disk mass. A supplementary contrast of the north–south polar differences, weighted by r/h and differenced between radii, annihilates both a uniform acceleration and any centred spherical addition. Agreement with that looser contrast alone cannot establish a successful mass law.
