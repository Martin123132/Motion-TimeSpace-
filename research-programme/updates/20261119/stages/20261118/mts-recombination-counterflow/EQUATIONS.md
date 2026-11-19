# From the local electron perturbation to the later matter response

Same CDM-comoving synchronous convention, k = 1.98095677855 Mpc⁻¹, K=p+q, |K|=|p|=|q| and μ=−1/2 as ../mts-active-stress-junction-20261118/EQUATIONS.md. All numbers are transfer coefficients, not measured overdensities. κ>0 is conformal Thomson opacity.

## Perturbing the material, not fitting the opacity

Integrate in N=ln a. At linear probe amplitude ε take n_H=n̄_H(1+εδ_b), T_r=T̄_r(1+εF₀/4), and H_escape/H=1+ε(k v_b−D′)/(3ℋ); H without a script denotes the proper background expansion. Synchronous CDM time has no lapse correction. Solve for x_H, x_He (singly ionized helium fraction) and y=T_m/T̄_r, with x_e=x_H+f_He x_He. Use early algebraic ionization equilibrium with continuous state transfer to kinetic evolution. The kinetic equations are the imported hydrogen effective-atom and helium singlet/triplet rate/escape laws, not MTS-derived atomic coefficients. In particular H dx_H/dN = C_H[β_B(1−x_H) exp(−E_Lyα/kT_photo)−n_H α_B x_H x_e]. Use the explicit saved source code for helium continuum absorption, escape factors and RECFAST corrections. The temperature equation is dy/dN=−[1+2ε(kv_b−D′)/(3ℋ)]y + (Γ_C/H)(1+εF₀/4−y), Γ_C ∝ T_r⁴ x_e/(1+f_He+x_e). The switch times are fixed background times; helium kinetics freezes at z=1250 once the remaining ionized abundance is negligible. Primary reverse Boltzmann factors are evaluated at T_r, capture coefficients at T_m; testing the T_m prescription is a model sensitivity, not an independent atomic calculation.

For rate vector f, solve Y₁′=f_Y Y₁+f_ε. Check by solving four independent nonlinear, perturbed histories using a different integrator. The opacity increment **in addition to** the known gas density is e_x=δx_e/x_e. Use the native background opacity even when testing alternate perturbed chemistry. [RECFAST physics](https://arxiv.org/abs/0711.1357), [perturbed recombination](https://arxiv.org/abs/0812.3652), [nonlocal transport at small scales](https://arxiv.org/abs/1409.1240). The first perturbation paper's quoted effective-atom sufficiency is for k<1/Mpc; the latter paper's strong nonlocal effects at much larger k do not prove a precision bound here.

## Optical forcing and shared gravity

Difference two calculations with identical primordial, linear and z=3999 data and identical quadratic sources, except e_x C₁. Every quadratic geometric term cancels in this difference, but the *generated* gravity and its backreaction do not. Use scalar intensity moments I_l and polarization P_l expanded in normalized associated Legendre functions B_l^s=sqrt[(l−s)!/(l+s)!] P_l^s(u), s=0 or 2; coefficients in the sky are (2l+1)(−i)^l times stored moments. Rotation to the scalar about K multiplies the incoming l-th coefficient by R_l=P_l(1/2), also for polarization with its screen transported. The source is κ e_x R_l C₁,l; for intensity the elastic rest-frame C₁ is zero at l=0, 4v_b/3−I₁ at l=1, (I₂−sqrt(6)P₂)/10−I₂ at l=2, and −I_l otherwise. The only polarization gain is −sqrt(6)(I₂−sqrt(6)P₂)/10. Multiply the returned dipole force by −ρ_γ/ρ_b in the baryon equation, using exactly the same source as the photons. Stream with k[sqrt(l²−s²)F_(l−1)−sqrt((l+1)²−s²)F_(l+1)]/(2l+1). First-order radiation is evolved from the saved incoming sky on the native metric and gas velocity, not read off from the output difference.

CDM, log baryon number, baryon current, averaged heavy energy/current, and spatial curvature obey the homogeneous linearization in the generated state of the previously tested Einstein/virial equations. Generate thermal neutrino skies by K_e/3−t₂(u²−1/3) and return both energy and longitudinal momentum to Einstein gravity. Thus photons do not heat gas in this elastic calculation; the relative energy-frame momenta exchange. As an independent check, a neutrino's zeroth/first moments are the time integrals of [K_e j₀(x)+2t₂ j₂(x)]/3 and [K_e j₁(x)−2t₂ j₂′(x)]/3, x=k∫v(q,τ)dτ. This does not use a truncated Legendre hierarchy.

## Absolute scalar gauge map on the retained triangle

Let γ_S=exp(s), with s₁=(A n nᵀ+B I)cos for each wave, A=−2D+6η, B=−2η. Pull back from Newtonian coordinates with τ_S=τ+T₁+T₂ and x_S=x+∇L₁+∇L₂ (the symbols on the right denote perturbations including their spatial harmonics). First order L=A/(2k²), T=L′=t/k². Write J=∇∇L₁. At the sum mode, apart from the unknown scalar spatial correction, the quadratic spatial metric is
M=T₁s₁′+∇L₁·∇s₁+s₁²/2+Js₁+s₁J+J²−∇T₁⊗∇T₁.
The scalar anisotropy projection 3(ẑẑ−I/3):M/2 on the cosine gives 3A²/64+3k²T²/8. The quadratic non-generator shift on the sine, divided by k, is T[T′−B+A/4]/2 from −T₁′∇T₁+(s₁+J)∇T₁. Therefore the zero scalar anisotropy and shift conditions give
```
L₂ = (A₂ + 3A²/64 + 3k²T²/8)/(2k²)
T₂ = L₂′ − T[T′−B+A/4]/2 = t₂/k² + T(B/2−A/32−T′/8).
```
Here A₂′=2t₂ for the log metric, A₂=−2C₂+6η₂ in the saved labels (a time-independent relabeling changes L₂ but not T₂). No equal Newtonian potentials required. This computes the **scalar projection** only; it does not discard generated tensor modes from the full universe by assertion.

For zero background pressure on the retained species, denote its synchronous density, rest pressure and longitudinal momentum at first order by d,p,v, normal energy at second order by E₂, and covariant current by J₂. Set l=(μA+B)/4. Directly transporting its density and boosting its stress tensor into the Newtonian slice normal gives
```
d₂,N = E₂ + T(d′−3ℋd) − μ k² L d − 3ℋ T₂
        + (9ℋ²−3ℋ′)T²/2 − 2μ kT v − μ(kT)²
v₂,N = J₂ − [l+(d+p)/2]v + (T v′−μ k² L v)/2
        + kT₂ − kTB/4 .
```
Use E₂=C₂+D²/2 for CDM, E₂=β₂+β₁²/2−μv_b²/2 for cold baryons, and Y for the averaged heavy field; J₂=0,P_b,Q respectively. These are normal-frame energy and energy-frame velocity, not an assumption that every relativistic species is a Newtonian dust. The fixture reconstructs the full unexpanded spatial matrix exponential, finite coordinate Jacobian and normal from orthogonality, Lorentz-transforms each stress tensor, and Fourier-extracts both metric and matter. Its local Taylor histories use the same retained first-order equations: it is an independent check of the transformation, not an independent solution for gravity.

For the ionization-driven *difference*, all first waves are identical: ΔT₂=Δt₂/k², Δd₂,N=ΔE₂−3ℋΔT₂, ΔU₂,N=−k(ΔJ₂+kΔT₂)/ℋ. Because quadratic first-order corrections to rest/normal/conserved densities also cancel, this difference avoids an ambiguity in matching absolute matter density to the nonrelativistic solver. Divide the seed by the squared *un-normalized* total matter transfer of the corresponding branch at z=99. Apply the saved z=8 row, and independently integrate the homogeneous Newtonian multispecies system forward with these same seeds. This is the contribution entering via the initial matter state, not additional radiative evolution between z=99 and 8.

## Lifting the actual incoming angular data

For functions in the normalized spin basis, let X multiply by u, D=(1−u²)∂_u, R be the diagonal azimuthal rotation. Before the Fourier phases are restored, azimuthal projections of w, w², (μ−wξ)∂_ξ and w(μ−wξ)∂_ξ acting on the incoming sky have matrices W=XR−RX, W²_projected=X²R−2XRX+RX², E=DR−RD and XE−EX+μR−XRX+RX², respectively (ξ=n·q̂, w=n·p̂=u−ξ). D acts in the meridional parallel screen for spin 2. W²_projected is **not** the square of W. Only five diagonals are needed for geometry; Thomson gain adds finite low multipoles. angular_lift.py tests the signs, phases and screen rotation against direct angular quadrature. Re-evolve incident, spectral-derivative and generated neutrino skies from the resolved kτ=10 packet; apply the very same nontrivial phase projection at a=0.00015, then the saved coupled pre/post-match metric histories. Preserve the original 36 momentum nodes; do not infer high multipoles by padding the 144-direction late packet.

