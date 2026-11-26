> Public reading copy: local links are mapped to released material or marked unavailable. Machine-specific passages, where present, have been omitted. See the inventory for the original digest.

# A necessary change in wave gradients for a local Newtonian force
       
**Question.** The saved LMC response in azimuthal sectors 0, 2 and 3 missed the inner force bands. Can a different shape give the missing acceleration *at the same gradient distance from the prepared ground*? Work in the retained weak-field Poisson limit on ordinary three-dimensional space. A pure mass-amplitude ψ has density |ψ|², not number density; divide its squared norm by the particle mass to obtain particle number. The bound below is independent of angular truncation, small-amplitude perturbation theory and the phase of the external tide. Its numerical application still depends on the two specified hosts and the stationary-plus-direct force baseline.
       
## 1. Directional point-force form
       
For displacement y from a probe and any unit force direction e, put k(y)=e·ŷ/|y|². Up to the gravitational constant, the measured wave acceleration in that direction is the quadratic form of k. It is signed: replacing it by 1/|y|² unnecessarily throws away angular cancellation. In spherical coordinates centred on the probe, the numerator for a field u is ∫ dr dΩ cosθ |u|². The denominator D[u]=∫ |∇u|² d³y obeys
       
    D[u] ≥ ∫ dr dΩ ( |∇Ω u|² + |u|²/4 ).
       
This follows by integrating the radial square |r ∂ᵣu + u/2|². Prove it first for smooth compactly supported fields away from the origin, then pass to the finite-energy form domain. Translate and rotate to any site and direction.
       
The best possible dimensionless form constant is the operator norm of (L²+1/4)^(−1/2) cosθ (L²+1/4)^(−1/2) on the unit sphere. In the normalized spherical harmonics this is a real Jacobi matrix coupling adjacent degrees. The m=0 block dominates all |m|>0 blocks, since its links are largest and taking componentwise absolute values increases the upper Rayleigh estimate. The signs of the eigenvalues pair by parity. Its squared link between degrees ℓ and ℓ+1 is
       
    tℓ² = 16(ℓ+1)² / [(2ℓ+1)³(2ℓ+3)³].
       
Truncation gives a lower bound. For an upper bound after degree L the rest of the tridiagonal matrix has norm at most 2/[(L+3/2)(L+5/2)] by its row sums. Test that xI−J is positive: eliminate the leading block by scalar LDL and allow a worst-case subtraction of tL²/(x−tail_bound) from its final pivot. [Exact rational certificate](evidence-001.zip) (archive member: `sharp_certificate.py`) brackets the infinite result without depending on a floating eigenvalue:
       
    0.782087227798 < C < 0.782087227800.
       
Sharpness for the unconstrained whole-space form follows by taking u=r^(−1/2) sin(π log(r/r₀)/T) times the angular trial function on a finite log-radial interval of width T, extended by zero. Increasing T sends the extra radial penalty π²/T² to zero. This does **not** say a galaxy has such an optimizing field. Finite-width controls (not bundled here). By self-adjointness of the bounded form in the gradient inner product, the same C bounds the mixed form: |〈u,kv〉|≤C√(D[u]D[v]).
       
## 2. Finite changes, not just a tangent
       
Let ψ=g+h. Regardless of phase or shape,
       
    |aψ (not bundled here)−ag (not bundled here)| ≤ GC [2√(D[g] D[h]) + D[h]].
       
Choose e in the direction of the vector change; no independent factor per force component is needed. A global phase is unobservable, so minimize D[h] over a constant phase of ψ. The reference and actual comparison fields are normalized to the same occupation. Norm preservation does not imply equal gradients. The term quadratic in h includes interference of all its modes. This also bounds finite mixtures: write the mass density as Σ|Ψⱼ|², compare to the columns cⱼg with Σ|cⱼ|²=1, and apply Cauchy–Schwarz over the columns. The minimal gradient distance is D[Ψ]+D[g]−2(Σ|〈∇g,∇Ψⱼ〉|²)^(1/2). It is unchanged by a constant unitary mixing of the columns. A reference ground of different profile or mass must be tested separately.
       
For each radius and hemisphere, take b to be the Euclidean distance of the stationary-plus-direct radial/polar vector to its rectangular pair of signed intervals. Any force that enters that rectangle must move by ≥b, even if its azimuthal component is free. In the saved dimensionless convention the acceleration scale is a*=v²/L since the mass unit is v²L/G, with harmonics normalized in the angular average; the physical density contains the compensating 1/(4π). Set s=b/(C a*). Then
       
    D[h] ≥ [s/(√(D[g]+s)+√D[g])]².
       
Use an **upper** endpoint for D[g] and C to obtain a conservative lower bound. The maximum across four sites is necessary, not their sum, and not a joint likelihood. The retained unit calibration (not bundled here) gives κ=ℏ/m=vL, N=g†g. The reported specific gradient energy is v²D[h]/(2N), in (km/s)²: the kinetic seminorm of a *field difference per unit prepared wave mass*. It is not the kinetic energy difference K[ψ]−K[g], orbit energy, minimum work from a particular source, or a bound on excitation in other matter.
       
## 3. Check on the actual saved fields
       
Use the degree-seven radial element representation for rψ, continuous across element boundaries, zero at both wave endpoints. Its zero extension is admissible for the whole-space inequality. Radial differentiation gives ∫|u′|² for u=rψ. The angular contribution is ℓ(ℓ+1)∫|u/r|². Mass and radial derivative use polynomial-exact Gauss integration. On the first element u/r is a polynomial because u(0)=0. Elsewhere enclose 1/r² on 64 subintervals per element times the integrated positive |u|². Compare the native kinetic matrix with those brackets. This encloses integration on the interpolated wave, not uncertainty in the physical boundary of the Milky Way.
       
In sectors 2 and 3 reconstruct both d and canonical p, not just the density displacement: the retained reduced waves W are H⁻¹-orthonormal, hence p is lifted from W⁻ᵀċ. The two azimuthal coefficients are (d+ip)/2 and (d*+ip*)/2 in the common real angular basis. Keep the archived complex m=0 displacement as well. Retain all terms in the normalized endpoint density: its square generates orders 0 through 6, not just 0,2,3. For the exact-density readout convolve the Fourier coefficients, put back the real partner once, sum **both** exterior and interior Newton multipoles at the original negative-x meridian, and check against the restricted linear readout. Densities here are exact squares of the available reconstructed fields, not new solutions of a nonlinear evolution.
       
A second control averages the same wave over axial rotations, **without** rotating the external satellite. It erases coherence between angular orders while preserving the occupation, kinetic norm and the gradient distance to the invariant reference (as a mixture). An independent discrete average over 16 angles reproduces the Fourier-diagonal density. This is a test of what the bound measures, not a claim that the specified orbit produces the mixture.
       
## 4. Why not infer a mass fraction from a point force?
       
In unrestricted three-dimensional data a force at a point cannot alone require a positive amount of redistributed mass. For a constructive example use disjoint compact spherical densities. Remove a fraction ε from a distant smooth source and put it in a spherical packet of radius d/4 whose centre is d=d₀√ε from the probe. Its force there is exactly GεM/d²=GM/d₀²; the lost distant force vanishes with ε. Smooth square roots give fixed-number trial waves; the packet's gradient cost scales as ε/d² and **does not vanish**. This is a reason to distinguish a number claim from the gradient claim above, not a proposed Galactic formation mechanism.
       
A *uniform spherical volume average* of the acceleration over an aperture of radius a has a bounded kernel: by Newton's shell theorem its force per unit source mass is at most G/a² inside or outside the aperture. For two equal-mass densities the positive and negative parts of their difference each integrate to the moved mass. Therefore M_moved≥a²|Δa_avg|/(2G). Applying this to observational data requires the actual survey weighting, the correspondingly averaged baseline and an averaged force discrepancy. No point interval here has been reinterpreted as a measured spherical aperture.
