# From the common metric to a nonlinear gas sightline

## What is carried from the parent
The mass m, heavy abundance, homogeneous cosmology, perturbation phase, and density and momentum at z=99 are inherited from the sealed early-field run, not from a forest fit. The pressure-off arm starts with the *same* state; all-cold transfers are those of their own cosmology. k is comoving Mpc⁻¹; conformal time τ is in Mpc and Hc=a'/a; c=1 until conversion to km/s. Initial transfer numbers are per unit primordial curvature. The scale chosen for a controlled cosine and the covariance of a stochastic Fourier coefficient are different things.

Write U_i=−div(v_i)/Hc in longitudinal gauge, v_i the peculiar velocity, θ_i the canonical velocity potential (a v_i=∇θ_i, so U_i=k²θ_i/(aHc)). Separate coordinate mass contrast C_i=δ_i,N−3Φ from the proper Newtonian-gauge density. For nonrelativistic clustered species at linear order C_i=δ_i,sync−3 etak/k. A prime denotes d/dτ. With g_i=4πG a²ρ_i, the flat Einstein constraints imply

    (k²+3Σg_i) Φ = −Σg_i(C_i−3Hc θ_i/a) − E_other ,
    Ψ = Φ − S_other/k²,      F = −k²Ψ.

The common seed uses k times the synchronous relative heavy momentum to undo the CDM frame. E_other is the sum of nonclustered comoving density sources, including the rolling field; S_other is total shear in native units. These are read from the photon, massless and massive neutrino and scalar variables, **not obtained by subtracting a fitted gas or gravitational force residual**. observer.diff records the readout-only changes; no trajectory equations changed. The other species are linear external inputs in the box, not an additional invisible nonlinear component. The potential eliminates a linear relativistic density correction; it is not a nonlinear Einstein solver.

## Why the counterfactual initially missed
The photon's synchronous dipole qγ and the synchronous baryon velocity v_b appear only through qγ−4v_b/3 in Thomson drag. Replacing the heavy wave with dust changes the synchronous observer's velocity. Importing qγ,sync from the wave run while moving v_b,sync to the dust run therefore imports the *old frame* as well as the radiation. Since qγ,N=qγ,sync+4σ/3 and σ=−Hc U_c/k, take qγ,N across and form the scattering slip with the **live** Newtonian gas velocity. This predicts the dust intervention from the wave environmental history; no pressure-off photon or gas history supplies the new input. At linear order

    C_b'=k²θ_b/a,
    θ_b'=−a[ Ψ + cs²(C_b+3η) + s_T
                + (ργ/ρb) opacity (qγ,N/k+4θ_b/(3a)) ] ,
    η=Φ−Hc θ_c/a,       s_T=(δp_b/ρ_b)_sync−cs²δ_b,sync.

s_T is explicitly read, even when the retained branch returns zero. For the heavy exact fluid there is also a −3Hc Π in C_h'; its Euler pressure is Π=c_s,h²(C_h+3Φ−3Hc θ_h/a). The simpler Newtonian leading pressure k² C_h/(4m²a²), with conserved wave number, is separately tested rather than asserted to give the same transfers. The scalar potential treatment assumes irrotational peculiar velocities.

## Evolving at finite amplitude
For ordinary smooth material n=1+C,
    
    n' = −div(n∇θ)/a,
    θ' = −|∇θ|²/(2a) − a(Ψ + gas enthalpy + external terms).

CDM and pressure-off heavy material have zero gas enthalpy and no scattering drag. In the wave arm instead evolve

    i ψ' = −∇²ψ/(2ma) + ma Ψ ψ,       n_h=|ψ|²,
    a j_h= Im(ψ*∇ψ)/m.

The code uses mass-weighted longitudinal currents for the weak-field velocity correction; it never divides a wave current by a vanishing density. Newtonian clustering is live across all massive species. The Poisson mean is removed in each periodic box. The parent-background gas enthalpy uses a 5/3 polytropic continuation whose tangent is native cs²; this is a controlled barotropic approximation. An explicitly separate photoheated arm adds a 3/2 polytrope with μ=0.61 and T₀=10,000 K, smoothly switched on from z=9 to z=7. The native pre-existing thermal perturbation and opacity terms are kept, not refit. Neither this heat input nor the neutral-hydrogen abundance is derived from MTS. No shocks, cooling network, external UV spatial fluctuations or shell crossing are modeled. Native transfer validation is for the unheated prescription, not for a claim that primordial gas stays at the native temperature after reionization.

Periodic Fourier derivatives, strict two-thirds mode mask, fourth-order interaction-picture integration and exact free-wave phase exp[−i k² Δ∫dτ/a /(2m)]. A repeated scale step and grid test checks truncation; there is no force softening, density clipping, imposed late amplitude or evolving renormalization. Nonlinear tests include planar Einstein–de Sitter dust before shell crossing, plus free dispersing interference with a density node. Plane waves and added transverse waves are not sampled velocities of actual absorbers.

## A neutral-hydrogen readout, with its units
Use optically thin photoionization equilibrium at uniform photoionization rate and T=T₀ n_b^(γ−1). The local weight is proportional to n_b²(T/T₀)^−0.7. This conditional approximation and its range of applicability are discussed by [Bolton et al.](https://academic.oup.com/mnras/article/357/4/1178/1051501). For a sightline period L_v=2π aH c / k_x in km/s (aH=Hc), add gas peculiar velocities in km/s and integrate the periodic Doppler profile with b²=2k_BT/m_H (proton mass approximation). In Fourier space,

    τ_l = A ⟨ n_b² (T/T₀)^−0.7
             exp[−2π i l (x/L_x + v_b/L_v)]
             exp[−(π l b/L_v)²] ⟩_x .
    F=exp(−τ),   δ_F=F/⟨F⟩_all−1,
    P₁D(l)=L_v ⟨|δ_F,l|²⟩_transverse .

This is the two-sided Fourier convention evaluated at positive l; P₁D has units km/s and k_v=2πl/L_v has units s/km. Average powers of separate sightlines, not the squared mean Fourier coefficient. A=0.65 is a fixed optical depth scale for the diagnostic, not adjusted to measured mean flux. Neutral column is conserved under the frequency transformation. We test analytic linear density and velocity responses, translation, total column, Parseval and the velocity-grid resolution.

## Finite transverse support versus a converged forest
Take k_x=7.052308884 Mpc⁻¹, choose orthogonal transverse spacings so (1,±1,0) has length 7.305207289 and (1,0,±1) has length 7.790917156 Mpc⁻¹. These are directly prepared magnitudes; no transfer interpolation. Add those pairs cumulatively while retaining all numerically resolved harmonics produced by nonlinear evolution. This fixes the periodic volume throughout the transverse test. The broadband cosmological source is **not** populated outside these pairs. At z=4.2 the fundamental corresponds to the high HIRES/MIKE bin; at other epochs this coherent box still uses the same comoving k_x and must not be relabeled the exact high velocity bin.

For a fixed-modulus pair use |R_K|²=P_R(K)/V with P_R(K)=2π² A_s (K/k*)^(n_s−1)/K³, Hermitian conjugate at −K, uniform random phases. This fixes the variance normalization from the parent; it is not a Gaussian-amplitude ensemble, and two paired phase draws are not a survey covariance. At linear order let d=(k_x b₀/(2 Hc c))² and μ=k_x/K. The independent prediction on these actual discrete modes is

    P₁D(k_x) = L_v A² exp(−2d) Σ_{K_x=k_x} (P_R(K)/V)
               × [(2−0.7(γ−1)−d(γ−1)) D_b(K) + μ² U_b(K)]².

D_b and U_b here are the independently integrated warm linear gas transfers, not the nonlinear box's output. The thermal exponential depends on **radial** k_x, not total K: by itself it cannot bound the high-transverse-k tail at fixed observed velocity scale. The actual gas susceptibility and matter spectrum at larger K, plus nonlinear mode coupling, must do that work. A numerical spatial resolution pass at fixed inputs is consequently not a physical tail convergence test.

