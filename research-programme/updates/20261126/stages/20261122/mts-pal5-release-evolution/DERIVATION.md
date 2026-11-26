> Public reading copy: local links are mapped to released material or marked unavailable. Machine-specific passages, where present, have been omitted. See the inventory for the original digest.

# A mass-sourced tide, a moving stellar population, and the response of the wave

## Ordinary field and trajectories

Use exactly the retained positive ordinary density law, its original shell/angular mass transfers at snapshots 586 and 590, the terminal exterior law and the same linear interpolation in *source time*. Keep the original finite spatial extent of the continuous Newton quadrature (160 kpc), not a new inferred outer Galaxy. Whole-aperture transferred masses match the saved −1.5803457934e9 and +3.2140649715e8 solar masses. These are prescribed ordinary histories, not a live baryonic response. Linearity of Newton gravity commutes with time interpolation in this representation. No change to G.

Write x=log(r/r0), y=galactocentric latitude, R=r cos y. In axisymmetry, r²∇²Φ=Φ_xx+Φ_x+Φ_yy−tan(y)Φ_y. The short orbit crosses the angular matter-transfer face y=−arcsin(1/32). Use separate spectral intervals on either side, continuity of Φ and Φ_y, and the isolated Newton potential on the *outer* computational boundary. A finite density jump is allowed; there is no surface delta-function mass sheet. Eliminate the shared interface value using equality of physical first derivatives. Solve the remaining separable system. For conditioning, solve for F=Φ−Φ0+aR0(R−R0)+az0(z−z0), adding r² aR0/R to the right-hand side. Restore the linear contribution to the force; this is a coordinate conditioning, not external matter or a fitted boundary. A manufactured solution continuous in value and slope with a jump in second derivative checks the transmission solve. Real forces at the moving centre and four offsets are checked against separate 3-D Newton force integrals, including a sample on the interface. [Independent comparisons](evidence-001.zip) (archive member: `newton-checks.csv`).

The 72 archived stellar probes are the shells of *circular* initial velocities, not the equilibrium Plummer distribution used in the separate initial-curvature check. Let ξ, v be star position and velocity relative to the moving cluster and b_j=a_j(X+ξ)−a_j(X). For a fixed Plummer cluster potential,
    
    d[ |v|²/2 + Φ_cluster(ξ) ]/dt = v·b_ordinary + v·b_wave.

Advance each centre and its associated stars simultaneously. Integrate both powers separately; evaluate the left side from states. Preserve the native-cell crossing solver for the old ordinary-field comparison. In the smooth potential, value and acceleration are continuous at the density break; use step refinement as well as independent comparisons through it. The cluster feels each field and moves, it is not held at its initial coordinates. The **same** initial centre and all stellar positions/velocities are supplied to all cases. Replaying a different frozen state at that centre is deliberate experimental matching, not a claim that each historical orbit actually started there.

## Response neglected when reusing the waves

For each of the four saved states at 586, compare evolution with corrected and original ordinary potential, **with identical initial wavefunction, mass normalization and wave self-gravity for this pair**. Denote corrected minus original by Δ; compare physical times, not instantaneous replacements of a wave by its conjugate. In the retained scalar Schrödinger–Poisson weak-field branch with universal potential coupling, write the physical mass flux as j. Continuity gives ∂tρ=−div j. The momentum equation gives ∂t j = ρ a_total − div Π, where Π includes the gradient/quantum and transport stress of the wave. Initially j, Π, ρ and wave self-gravity coincide within each pair. Hence

    Δρ(0) = Δ∂tρ(0) = 0,
    Δ∂t j(0) = ρ Δa_ordinary,
    Δ∂t²ρ(0) = −div(ρ Δa_ordinary).

This is a continuum variation within the retained Newtonian branch; it does not assume the later nonlinear wave states are equal. In a ball translating with the cluster, the two centres share their initial position and velocity, but their accelerations differ by Δa_ordinary(X). Transforming the continuity equation to this frame gives

    ΔM_wave''(0) = −∮ ρ(X+ξ) [Δa_ordinary(X+ξ)−Δa_ordinary(X)]·n dS .

A uniform acceleration cancels exactly. A useful independent decomposition is 4πG ρ(X) ΔM_ordinary(<A) minus the surface integral of [ρ(X+ξ)−ρ(X)] times the relative acceleration change. The independent positive ordinary-source mass, the old effective Newton mass (not baryons that have physically disappeared), and the surface quadrature give separate checks. The actual positive wave density is reconstructed from the saved complex finite-element states, not by taking a second derivative of an interpolated wave potential. With dimensionless radius r/L and normalized angular basis sqrt(2l+1)P_l, it is m_scale |Σu_l(r/L)sqrt(2l+1)P_l(μ)|² / (4π L r²). Twenty-four enclosed-mass comparisons check the normalization against the archived profiles. The surface quadrature splits wherever it meets a native radial interface, including in the wave elements.

Gauss's law maps this to the *mean inward* normal wave acceleration: Δ〈g_wave,in〉''=G ΔM_wave''/A². This is not the pointwise acceleration of a star. The negative value in this experiment describes an initial **difference in curvature** compared with the old field, not a loss of total wave occupation, a present-day observed local mass change, or even a measured outward flux. A separately solvable Gaussian wave in two quadratic potentials, with expanding, static-width-at-launch and contracting initial phase choices, gives the same surface law when differentiated in time. [Analytic evolution test](evidence-001.zip) (archive member: `independent-quantum-control.csv`).

The initial response is local and derivable without a fitted susceptibility. The corrected wave potential at later times is nonlocal; these local coefficients cannot be advanced for 0.927 Myr by assuming constant curvature or patched to zero outside the numerical domain. A complete live-wave replay needs the corrected source potential throughout the supported initial wave (the same source model), then the original Hermitian evolution and self-gravity solve. This is the next physically different test.
