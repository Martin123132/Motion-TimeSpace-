# What actually feeds back into gravity

The matched original control is the sealed two-way scalar/stream solution. The initial hot distribution is uniform and isotropic in the local orthonormal frame, so it adds **no perturbed energy, current, radial pressure or anisotropy at the starting instant**. Its homogeneous energy is already in the expansion history; it is not inserted into the excess Hamiltonian source a second time. The original canonical material labels and both scalar fields still evolve. On each new half/full slice the thermal state supplies δE, j=ℓF, Π to the common constraints. The independent trace readout explicitly includes δP_r. Dust face quadrature sees only dust pressure; it does not inadvertently remove or double-count hot pressure. The lapse and metric expansion from the solve supply the next force and redshift to the particles. No measured trace residual or frozen forecast appears in this update. The coupled thermal transport is weak-field linear collisionless transport on this metric; retaining the nonlinear old solver does not promote the thermal sector itself to fully nonlinear kinetics.

Direct interpolation of the angular distribution at its previous position gives a simple live control. Its integrated momentum can be much more accurate than its small local pressure. A separate representation follows from the same transport equation: write s=∫₀ᵗ v dη, choose the actual initial gravitational potential U₀ and speed v₀, and split off

    Θ_B(x,n,q,t) = [U₀(|x−sn|)−U₀(r)]/v₀².

Along a free thermal characteristic the first term is constant. The residual brightness therefore obeys the original equation with spatial forcing −n·∇[U(t)−(v(t)/v₀)² U₀]/v(t). When the potential and the speed are constant this residual vanishes identically for Vdot=0. Nothing has been fitted or discarded: add Θ_B back for the measured and gravitating stress. This avoids repeatedly interpolating the dominant dipole into much smaller even moments. The recalculation at new radii uses a separate causal integration on the old metric, including the original U and V, and does not know the new material trajectories.

The 24 Mpc boundary keeps the original normalizations for the metric. On the small extension needed by an incoming ray the main calculation continues the initial gravitational gradient with its exterior 1/r² form; the live stored redshift rate is set to zero outside. The independent test-field control also compares a zero extension with a time-dependent matched derivative. Neither is a measured boundary. The full-radius four-case replay reproduces the original metric, trace, event, restart and (when applicable) wave-energy packet arrays before the on/off comparisons.

## Independent homogeneous evolution

A piecewise log-linear H accurately interpolates its *value* but its derivative can bias the small enthalpy left after subtracting the dominant matter and slow field. The source-based alternative keeps exactly the old H and scalar field/normal velocity at the starting slice. In N=ln a it evolves

    dH²/dN = −[ρ_b+ρ_c+ρ_wave,rest + W_s² + (E+p)_photons,ν],
    dφ_s/dN = W_s/H,                 dW_s/dN = −3W_s − m_s² φ_s/H.

Here ρ and p include 8πG, and the heavy homogeneous source uses the retained late-time matched rest background (not the exact instantaneous fast-phase pressure). No adjusted vacuum term is needed. The cosmological clock can now be evolved without inferring the remaining hot enthalpy by subtracting nearly equal numbers. The ODE is checked against the unchanged independently integrated native expansion at ten offsets per branch/epoch, not just the starting anchor. The source version is used in the local solver only after this check passes. A cubic through exactly the old table is a separate numerical control, not a competing field equation.

## Shell energy test: distinct from radial momentum

To first order in the metric and the thermal perturbation, p=δP_r−2Π/3 and F=j/a. For a comoving shell [l,h], not including the angular factor 4π,

    ∆[a³∫ δE r²dr] = ∫{−a³[r²F]ₗʰ − 3a⁴H∫δp r²dr + 3a³(E+p)_bg∫Vdot r²dr}dη.

Test both species groups and all four shells, each on the larger of actual change, expected change and largest individual work/flux. Never infer energy conservation solely from a correct integrated dipole.

An especially sharp problem for a slowly moving species is that a very narrow streaming shift probes the second derivative of the initial potential. Pointwise density can undersample this structure even when the current is correct. For the static reference its volume integral can be calculated without that derivative. The spherical mean of U₀ translated by a distance d, integrated over a ball of radius r, is the integral over source shell u of u²U₀(u) times the fraction of shell inside the translated ball:

    K = clip([(r−u+|d|)(r+u−|d|)]/[4u|d|], 0, 1).

Subtract the untranslated indicator 1[u<r]; equal volumes allow U₀(r) to be subtracted from the integrand too. The integral has support only from max(0,r−|d|) to r+|d| and equals the exact enclosed reference monopole times v₀². In the volume-based variant the cumulative energy and isotropic pressure at each grid knot and their angularly measured derivatives determine a Hermite reconstruction; its derivative, not a new mass assignment, sources the finite gravity mesh. The first interval uses a regular even central density. The anisotropy and transported residual keep their own moments. An independent spherical-Bessel test includes both signs of elapsed time, sites inside and outside the displacement, and the small-displacement limit.

## The residual distribution, not another free density term

Testing the initial-potential volume independently separates two errors: interpolation of its analytic monopole onto gravity cells, and transport of the much smaller *remaining* monopole. Correcting only the former need not repair the latter. For each massive-neutrino comoving momentum the angle average of the kinetic equation gives

    ∂η F₀ + v r⁻²∂r(r²F₁) = ∂η V.

The radial gravitational force is a dipole, so it has zero angle average even after removing Θ_B. Consequently the enclosed residual brightness C(q,R)=∫₀ᴿ r²〈Θ−Θ_B〉dr has a derived evolution: Cdot=∫₀ᴿr²Vdot dr − v R²〈μ(Θ−Θ_B)〉 at R. Level 6 evolves this quantity with the other matter using the measured angular flux at the actual substeps. Its regular radial derivative supplies the residual monopole for subsequent transport, gravity and pressure. Higher angular moments and the massless calculation are not set by an energy fit. A passed check using the same flux is not by itself independent evidence of accuracy.

The independent shell test instead begins again with the *old metric* and the microscopic unperturbed distribution. Angular monopole transport over a shell source Vdot uses its untranslated volume plus the signed cap correction. For the force source its primitive is even simpler: ∫₀ᴿr²∂s S_s U dr = −R²〈μU(R−sn)〉, from differentiating a translated ball. Integrating these two actual sources through past light cones, over momentum and signed time, predicts shell energy without ever reading a live residual, fitted local pressure, or the energy needed to close a budget. Compare this with the simulated shell energy as well as with its independent current/work readouts.
