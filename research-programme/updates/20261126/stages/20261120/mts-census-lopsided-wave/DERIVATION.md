# Relative wave and ordinary matter in the satellite field

## State and frame

Use the retained Newtonian Schrödinger–Poisson limit on each of the three actual saved central-speed equilibria. Keep its norm N, chosen previously at 224.03 km/s and 17.58 kpc, and the ordinary foreground fraction (0, 0.23097, or 0.47861) fixed during the drive. Do not copy a perturbation from a different ground. The ordinary density translates as one body; stellar/gas bending, compression and a deformable stellar bar are not included. There is no independent galaxy-formation claim for these occupations.

Let X be the complex plane-even m=1 density-amplitude variable (sum of conjugate perturbations), measured about the centre of the ordinary matter. Its first-order density integrates to zero by the azimuthal integral. In stationary wave units write H for the ground-shifted single-particle Hamiltonian, B for multiplication by the real ground and projection onto Poisson sources, and L for the vacuum Poisson stiffness. Then M=H−2BL⁻¹Bᵀ is the density stiffness. Multiplication and projection are done anew on each saved equilibrium; the factor two follows from the conjugate wave equation, not a fitted disk coupling. Numerically the stationary residual, factorization without negative pivots, uniform translation and full-versus-reduced static compliance are checked.

Use fixed-ordinary canonical mode coordinates c (H¹ᐟ² M H¹ᐟ² normal modes), natural frequencies σ, and row mᵀ such that the relative planar centre is mᵀc, expressed as x−iy in units of the ground length. A translated profile is the tangent N H times the full-mesh centre row, divided by its measured unit-displacement response. Multiplying this profile by the *evolved* centroid, rather than fitting a shift, separates a rigid translation from the rest of the wave. The centroid kinetic sum N mᵀm must be one up to the saved numerical tolerance.

Compute the external acceleration on the extended baryons by integrating −∇Φ_LMC against the actual ordinary mass. This includes the four-population census, gas, mass-normalized E3 bulge, signed 0.4 bar redistribution, and the native component at the saved mixing fraction. A signed transfer is not added as extra mass. The second force integral averages the same field against the squared wave ground, independently of the modal forcing. Azimuthal averaging of a harmonic V_j(r)Y_j1 gives coefficients for V'_j and V_j. For μ=z/r and p=P_j(μ), they are respectively
    α = sqrt[(2j+1)/(j(j+1))] j [P_(j−1)−μp],
    β = [α + sqrt[(2j+1)/(j(j+1))] j(j+1) μp]/r.
Use the same radial spline for the force and the potential; integrate its value and derivative rather than differentiating a noisily differenced force. Uniform and cubic Cartesian test potentials check the two coefficients and their normalization. Exterior truncations and the assumed shape of the ordinary matter belong to the preparation, not measurement errors. A spatial constant has no m=1 component.

Let F be the complex modal forcing by the finite satellite field after subtracting its uniform gradient at the origin, and δ_b the ordinary external acceleration minus that point acceleration in units v²/L₀. Write γ=M_wave/M_ordinary. Newton's third law gives the opposite reaction of ordinary matter to the wave restoring acceleration. In the translated frame,
    c'' + (I + γ N m mᵀ) diag(σ²) c = −F − N m δ_b .
With q=diag(σ)c the stiffness becomes symmetric:
    q'' + K q = −diag(σ)(F+N m δ_b),
    K=diag(σ²)+γN (σm)(σm)ᵀ .
Start the relative perturbation and its velocity at zero at the first saved epoch. Use both real quadratures of the actual satellite orbit, not a fitted offset or a quasi-static response. A uniform external potential gradient makes the raw modal and ordinary forces cancel. Recompute the restoring acceleration independently by integrating the ordinary potential gradient against the wave density, and compare to the evolved relative motion. The near-disk material readout replaces the archived reference by site-minus-point first, then subtracts the ordinary external-minus-point and induced ordinary reaction. Only the planar reference changes; this stage does not introduce vertical recoil. The static NFW control receives the same specified external tide and external reference shift, but no invented live-halo mode.

## Isolating intrinsic shape

At a site with cylindrical coordinates R,z let a_z=(z a_r−R a_θ)/sqrt(R²+z²). For each R form the azimuthal cosine of the vertical-odd acceleration:
    V(R)=mean_φ cos(φ) [a_z(R,+h,φ)−a_z(R,−h,φ)],   h=1.5 kpc.
Here φ=0 points along the tested negative-x meridian. A pure cosine perturbation gives its northern amplitude. Any uniform acceleration cancels, and m=0, the bar's m=2 and other azimuthal orders integrate to zero. The measured *one-meridian* bands do not measure V. For a small rigid displacement of the wave in +x, V(R)=d_x ∂_R a_z,ground(R,h). Obtain the derivative on each ground by independently differencing its stationary Poisson field, not by fitting either dynamical readout. Then
    S = V(6) − [∂_R a_z(6)/∂_R a_z(8.3)] V(8.3)
also removes rigid wave translation to first order. Save the small discrete leakage by comparison with the translation tangent. For the external satellite and archived live-halo comparison, extract the same coefficient at 128 then 256 azimuths using both hemispheres. A live halo has its own foreground and initial fluctuations: report both its final harmonic and final-minus-initial, separately from the static baseline.

## A lower energy bound that does not assume the driven shape

At the single matched meridian form v(R)=[a_z(+h)−a_z(−h)]/2. Propagate the rectangular signed intervals into two intervals for v and subtract the original local background plus direct point-relative satellite and m=0 wave. This is a *necessary*, not sufficient, condition for all original components. It remains necessary after any uniform reference subtraction and in particular after ordinary recoil.

For the m=1 sector only its real quadrature contributes. If A maps full-mesh real displacement to these two vertical forces, the least potential energy for a given increment d is dᵀ(AM⁻¹Aᵀ)⁻¹d/2. Compute the compliance by full sparse Poisson/field elimination, not just the retained dynamical basis. Minimize this positive quadratic over the two-dimensional rectangle: check the interior origin, then the four edges with the other coordinate clipped to its allowed interval. Check the variational sign at the selected point. This is not a parameter fit or a replacement physical state.

In the canonical c normalization, eliminating common translational momentum gives the relative inertia
    T = (I+γN mmᵀ)⁻¹ = I − γN mmᵀ/(1+γN mᵀm).
Thus the actual driving energy in the same units is [c'†Tc'+||σc||²]/2 including *both* complex quadratures. This reduced kinetic form follows also by multiplying the unforced relative equation by T. In normal coordinates Q of K the very same energy is [||Q||²+||Q'/ω||²]/2. Factor K as a squared matrix and use its singular values to avoid losing relative accuracy on its soft modes against its stiffest frequencies. Check this second energy and free conservation through a nonzero propagation time to 1e−10 before using an energy ratio. Common positive unit factors cancel in the ratio. A lower bound above the driven energy concerns this linear excitation on these grounds only, not the LMC's total orbital energy, arbitrary initial waves, or nonlinear field evolution.

Because the energy's square root is a norm, an additional homogeneous initial perturbation can help only if its conserved energy is at least [max(0,sqrt(E_min)−sqrt(E_driven))]². This allows maximally constructive interference; it does not assume the satellite actually prepared that state.

## Off-disk continuation

At the two saved stream sites, reconstruct the stationary force and the m=0 disturbance on the same ground. The latter is exactly half the force difference of g+x and g−x since Newtonian gravity is linear in density and density quadratic in the wave. Cross-check the same procedure against the known mode readouts on the inner meridian. Rotate the complex m=1 spherical force into cylindrical R and z, add the archived present satellite force evaluated at the actual site minus its origin value, and apply the ordinary planar material correction once. Use the azimuth sweep for the unknown sky orientation, not an angle selected to favor one model. Both MTS and the static halo use the same direct field; only MTS has the prepared wave and its reaction. Compute the previously defined total force ratio q=sqrt[(z/R)F_R/F_z] and linear strength using the two published reference offsets and widths from the saved comparison. These present force samples do not model a stream's past orbit or assign its stars an observational likelihood.
