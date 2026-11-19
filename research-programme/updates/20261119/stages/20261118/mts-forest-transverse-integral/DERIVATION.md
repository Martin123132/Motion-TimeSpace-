# What the shared gravitational field predicts here

All comparisons hold the retained adiabatic population, mass, gas heating prescription and primordial normalization fixed. No observed velocity or absorption power sets a transfer amplitude. The pressure-off intervention removes only heavy perturbation pressure at z=99; it does not turn the earlier cosmology into cold dark matter. The all-cold control has its own early history.

## Continuing the microscopic field without reselecting a population
Write N=ln a, x=mt and u=dφ/dx. For a positive quadratic homogeneous scalar, φ_x=u and u_x=−φ−3hu with h=H_phys/m. Thus ζ=exp[3(N−N_s)/2+i(x−x_s)](φ+iu) satisfies ζ_x=(3h/2) exp[2i(x−x_s)] ζ*, N_x=h. Friedmann sources the same h from standard species, slow energy and |ζ|² exp[−3(N−N_s)]. The slow energy in this early carrier extension is frozen at its saved initial potential; the subsequent slow background is independently integrated and checked for flatness. This is the saved separated early-background approximation, not a fit to a new matter fraction. Matching at a continuous-density crossing solves a(φ′²+a²m²φ²)/2=ρ⋆, not φ=0 or a preferred perturbation phase. An arbitrary interpolated restart is demonstrably worse than a retained integrator knot (homogeneous.json). We also compare step-halving, original-field overlap, alternative phase windows, thinning and polynomial orders, independent switching surfaces, the force constraint, gas time steps and external-source sampling. These are numerical tests, not analytic uniform error bounds.

The native, unaveraged common-metric perturbation is evolved independently at each new k. It has δφ″+2ℋδφ′+(k²+a²m²)δφ=−kZφ′. Its microscopic conformal density, current and pressure are φ′δφ′±a²m²φδφ and kφ′δφ (plus for density). Projection removes carrier harmonics, not an adjustable force. The envelope law tested at the crossing is P=[k/(am+√(a²m²+k²))]²(D+3ℋQ/k). A local pressure pass is necessary, not sufficient: changing the crossing can still change the much later relative density and velocity. On the early, low-k overlap, trace_control.py independently drives the retained metric trace with external density plus three times pressure and the returning heavy stress; no late direct D,Q enters that control.

## A reduced gravitational prediction that does not depend on the split into two dusts
Use the saved canonical variables C_i, θ_i with C_{i,N}=k²θ_i/(aℋ) and, for a pressureless geodesic, θ_{i,N}=−(a/ℋ)Ψ. Heavy and ordinary cold matter use the SAME Ψ. Consequently θ_h−θ_c is constant, and C_h−C_c equals its initial value plus k²(θ_h−θ_c) times ∫dN/(aℋ). Their homogeneous dust fraction w=g_h/(g_c+g_h) is constant. The metric therefore needs only D=(1−w)C_c+wC_h and T=(1−w)θ_c+wθ_h: D_N=k²T/(aℋ), T_N=−aΨ/ℋ. Let g_d=g_c+g_h. The existing constraints give

    Φ = [−g_d D−g_b C_b+3ℋ(g_d T+g_b θ_b)/a−E_ext]/[k²+3(g_d+g_b)]
    Ψ = Φ−S_slip/k²,   η = Φ−(ℋ/a)[T−w(θ_h−θ_c)].

The η term is retained in the baryonic pressure/thermal gauge conversion; erasing the initial relative velocity there is not the reduction. Evolving just D,T,C_b,θ_b with independent adaptive DOP853 and the saved radiation, entropy and photon dipole tests the six-variable Gauss solution, not merely its initial conditions. For the independent unheated intervention a different native run actually switches the heavy stress off, allowing its photon/other-species history to respond. Heating in the separate linear gas calculation is still prescribed; these two tests validate different things.

## A conservation identity separates a solver clock error from pressure physics
Let f be the homogeneous heavy scalar, v=f′, F=δf, V=δf′, and primes denote conformal time. The raw conformal pressure is p_c=vV−(am)²fF. J_h=aQ=k a²vF/ρ⋆, P=a p_c/ρ⋆. Direct differentiation gives J_h′=akP: the terms proportional to 2ℋv cancel by the homogeneous Klein–Gordon equation. This is independent of the approximation used to describe slowly varying pressure. The native averaged law independently has Q′=−ℋQ+kP. Comparing early-fluid evolution with the second, directly projected microscopic endpoint gives a *required* impulse difference; it is not an independent measurement of its entire microscopic integrand.

On the solver's interpolated scale-factor clock ℓ=d ln a/dτ_lookup, the background table v(N) need not satisfy that equation in the solver's τ. Its predicted extra source in J_h′ is

    k a² F/ρ⋆ × [(v_N+2v)ℓ+(am)²f].

With phase-clock rate hφ=am/(d phase/dN), the bracket splits into (v_N+2v)(ℓ−hφ) and the homogeneous KG remainder evaluated with hφ. The first needs the lookup derivative and the independently calculated background, not a measured current derivative. The perturbation F can be recovered without division by either f or v at a node: solve the two scaled identities (am)²fF=(δρ_c−δp_c)/2 and am vF=am q_c/k together. Comparing the integrated predicted source with J_h(end)−J_h(start)−∫akP dτ across the stored carrier windows tests the clock explanation.

For an actual dynamics repair, rather than subtracting that predicted residual, clock_transport.py uses N as the independent variable, the same initial F,V and metric expansion perturbation J, and the same sampled other-species Einstein trace. In (F,V,J), the conformal right hand side is [V,−2ℋV−(k²+a²m²)F+vJ,−ℋJ+(δρ_c+3δp_c)/2+trace_other]. Divide ALL THREE right hand sides and the independently integrated pressure impulse by the same Friedmann rate ℋ, instead of by ℓ. Both versions return the heavy density and pressure into the metric expansion. Other species remain a supplied driver over these short windows; the full hierarchy and late spatial spectrum have **not** been rerun with this clock replacement. Refining the old lookup spacing alone is a separate control.

## The spectral minimum is not an absence of gravity
At fixed radial k_x, the linear response before squaring is R=B D_b+(k_x/k)² U_b, B=2−(0.7+d)(γ−1), d=(k_x b₀/(2ℋc))². The finite contribution is ∫d ln k W R² with positive W=ℋc A² exp(−2d)k² P_R/(2π). A cancellation R=0 at one 3D k is NOT a zero of the measured 1D power. Doppler damping alone multiplies all transverse wavenumbers equally in this bin. Density-only and no-added-heating replays distinguish velocity cancellation from a gas acoustic sign change. Four-point Gauss quadrature on each log interval integrates products of two cubic signed amplitudes exactly for those interpolants; the primary integral retains the original shape-preserving interpolation of the positive integrand. Sign changes, held-out errors and differences between interpolants are kept separately. None bounds the unseen tail.

## What is changing between two matching surfaces?
With the external histories fixed, the late system is affine. A single matrix propagation splits each response into six initial canonical coordinates plus the driven term. Linearity does not turn these bookkeeping components into independently preparable universes. For two histories A,B, the exact identity is

    R_A−R_B = L_A(X_A−X_B) + (L_A−L_B)X_B + (r_A−r_B).

Here L maps initial coordinates to a final observable and r is the driven response. matching_origin.py evaluates the middle terms by actually transporting the second initial vector on the first operator, for every saved epoch and each mode. It compares corresponding epoch labels and the reconstructed physical metric/gas outputs on each arm. This distinguishes trouble inherited by z=99 from trouble introduced by the late pressureless limit. It does not repair a failed interface by reweighting terms.

