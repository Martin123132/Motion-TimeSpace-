> Public reading copy: local links are mapped to released material or marked unavailable. Machine-specific passages, where present, have been omitted. See the inventory for the original digest.

# A scalar phase on an observer-normalized weak gravitational ray

## Observable and order

We follow the saved real-field shell experiment (not bundled here) at the original 8.3-kpc fixed observer, with the same scalar mass, two prepared axisymmetric host grounds and six LMC histories. A screen is specified by an affine length normalized by the local observer, not by coordinate height, luminosity distance, redshift or measured pulse arrival time. The new calculation transports the **fast phase** consistently to first order in metric potentials; it retains the previous Newtonian wave and amplitude prefactors. It does not claim a full second-order optical area including amplitude remapping, post-Born lensing, or nonlinear response of the halo.

Write x⁰=ct, lengths in L₀, τ=εx⁰, ε=V₀/c, φ=Φ/c²=ε²U, where U is the ordinary negative Newtonian potential in V₀². Use the common metric ds²=−(1+2φ)(dx⁰)²+(1−2φ)dx² with negligible slip on this branch. Take a static observer tetrad and denote the past-directed affine distance by z. The initial covariant time momentum of the *past*-directed ray is p₀=1+φₒ. Its equation dp₀/dz=(∂₀g_ab)kᵃkᵇ/2 gives −2∂₀φ on the zeroth-order past ray. This yields

    p₀(z) = 1+φₒ−2∫₀ᶻ ∂₀φ(s) ds,
    x⁰ₒ−x⁰ₑ = z+φₒz−2∫₀ᶻ φ(s) ds−2∫₀ᶻ (z−s)∂₀φ(s) ds.

The sources in these integrals are evaluated at τ=τₒ−εs; ∂₀φ is a *partial time derivative*, not a total derivative along the ray. A spatial gradient changes the propagation direction, but it does not feed this time solution at first order about a fixed direction and affine distance. Its action on a nonuniform source amplitude is a different, higher-order optical contribution. For the observer's clock, dx⁰ₒ=(1−φₒ)c dT/L₀, with T=0 synchronized to the archived present. Local tetrad normalization and the integrated time-derivative term are standard weak-field results; see [Schmidt & Jeong, Cosmic Rulers](https://arxiv.org/abs/1204.3625). The finite-shell calculations here use the LMC field, not cosmological data from that paper.

## Separating a real gravitational effect from a reference convention

The original double-carrier coordinate frequency is 2(ε⁻²+E) in native time, E the ground chemical energy in V₀². Ignoring products of post-Newtonian corrections, the host proper frequency and spatial carrier wavenumber are set by the single factor 1+ε²(E−U_H,o). At fixed local proper reception time, the remaining host phase in the projected spatial integral is

    χ_H(z) = −4ε ∫₀ᶻ [U_H(s)−U_H,o] ds.

Neither the difference E−U_H,o nor χ_H changes if the zero of host potential and chemical energy shift together. A static spatial phase change alone can rotate a signal but cannot detune a stationary temporal tone. The proper period uses the same invariant difference; the drift of the oscillator sampled in two different gauges is not a new clock signal.

For a first-order disturbance U_d (prescribed tide plus induced self-potential) use τ_T=T·year_native with T in Julian years. The additional double phase is

    δχ = 2∫₀^τ_T U_d,o(u)du + 2ε [U_d,o(τ_T) z −2∫₀ᶻ U_d(s)ds]
         −4ε²∫₀ᶻ (z−s)∂τ U_d(s)ds.

For a constant added to the external potential, U_d→U_d+C gives δχ→δχ+2C(τ_T−εz). The Schrödinger wave transforms by exp(−iCτ) up to the initial phase convention. Its double phase cancels the change at the emission event. Transform the preparation phase as well when comparing different time origins: an unconstrained **physical** initial scalar phase is not a change of coordinates. We inject a nonzero C into the numerical ray fields and exercise both cancellations. A second test integrates the actual metric Hamilton equations in a manufactured smooth, time-dependent potential; halving its amplitude reduces the first-order coordinate-time discrepancy by a factor of 4. There is no reason for a time-*varying* spatially uniform perturbation of both Newtonian-gauge potentials to be pure gauge in an arbitrary solution.

The wave's common phase in the original potential convention was already restored from the matter equation. Do not add it twice. With the previous unperturbed null derivative A₀ and wave perturbation dA, the carrier envelope that multiplies the corrected host plane wave and exp(iχ_H) is A₀² for the ground and 2A₀ dA+iδχ A₀² for the induced **difference**. The latter term is the undisturbed carrier transported on the changed ray. The common absolute phase is swept, not tuned. For this restricted calculation retain the old slow drift as a comparison target. Exact gauge statements here concern the leading phase, not an assertion of all-order covariance for the retained Newtonian mode amplitudes.

## What was integrated

The host uses the archived ordinary-plus-wave Hamiltonian potential (not the chemical potential) with the Poisson correction for the refined ground. The external drive comes from the original even m=0 radial-harmonic LMC panels; the induced potential solves Lδw=−2B†x at the saved retarded mode states. The archive supplies a quartic terminal drive; on the actual crossing interval we reconstruct the dynamical potential at Chebyshev times and differentiate at fixed position. Integrals of U and its time derivative use separate cumulative panel primitives on the radial-element-split ray, tested with both time and spatial refinement. The rapidly oscillatory outer shell integral uses oscillatory Legendre moments, not an unresolved ordinary sine sum. Replacing the new phase by the old one recovers the saved complex coefficient. The time fit is an interpolant through three computed reception epochs, independently checked at two withheld times. Cases and histories are paired throughout.

## Measuring how the foreground gets through

Keep four equally spaced one-year exposures centered between −20.5 and −0.5 years. For spacing d=20/3 years and nominal frequency Ω the weights are (−1,1+2cos(Ωd),−1−2cos(Ωd),1)/[2d(1−cos(Ωd))]. The normalized leakage for an actual stationary tone of angular frequency ω is

    |H| = |sinc(ω/2) · 2 sin(ωd/2) [cos(ωd)−cos(Ωd)] / [d(1−cos(Ωd))]|.

Nearest frequency thresholds are roots of |C_ground H|=|saved slow slope| on either side of the notch. They are **filter-mismatch thresholds at fixed amplitude**, not errors on the particle mass: changing the physical mass would also require recomputing occupation, wave shape and spatial phasor. A common time shift rotates the tone without spoiling an exact zero. For individual exposure-clock errors |δt_i|≤J, the triangle inequality gives the sufficient all-phase condition 2|C_ground| |sinc(Ω/2)| sin(ΩJ/2) Σ|w_i| < |slow| in the small-jitter interval. Also enumerate all 16 sign patterns of the linearized phase errors for a sharp first-order bound. The jitter calculation does not address a changing source distance.

At leading weak-field order for the slow ground source S=|A₀|², the fixed-screen formula is κ(D)=ε²∫₀ᴰ z(1−z/D)S(z)dz in native lengths. Hence

    ∂κ/∂D = ε² ∫₀ᴰ (z/D)² S(z)dz.

The moving upper edge contributes zero to the first derivative. Check by backward differences. Convert this derivative to per kpc, multiply by the original (20,−70,50)/15 weights, and compare with the **same** secular slope. This tests an uncorrected change of affine range only, not the velocity of an observed object or a model of all kinematic effects. A frequency notch that preserves a linear time trend necessarily preserves this contamination.

**Frozen four-screen stress test:** insert one screen at 42.5 kpc, the midpoint between 35 and 50, without optimizing it. On the undisturbed reference host only, solve four linear equations for coefficients a: Σa=Σa/D=0 to preserve cancellation below 20 kpc; Σa ∂κ_ground/∂D=0 for a *shared additive* range shift; ΣaD² equal to the original value to preserve response to a uniform Ricci source. Freeze and transfer exactly those coefficients to the other host and all histories. For unrelated screen motions there is an obstruction: nulling each independently requires a_j κ′_j=0 for every screen. Every retained κ′_j is strictly positive, so the only such combination is identically zero. The fourth screen is a diagnostic, not a source discovered on the sky.
