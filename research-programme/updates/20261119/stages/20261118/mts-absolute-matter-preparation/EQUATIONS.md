# From the radiation-era state to a weak-field matter experiment

Use the conventions in ../mts-recombination-counterflow-20261118/EQUATIONS.md and the inherited ../mts-active-stress-junction-20261118/EQUATIONS.md. k=1.98095677855 comoving Mpc⁻¹, |p|=|q|=|p+q|, μ=−1/2; no factor of two on a sum-mode cosine. The input is the same regular adiabatic Gaussian two-wave realization in both branches, not a galaxy population. Density/velocity coefficients multiply the small external primordial wave amplitudes. The heavy component is 0.50218 of clustered matter on this example. The cold comparison replaces it by ordinary cold matter, not by an independent fitted ΛCDM background.

## Live propagation before the interface

Restart the earlier forecast-carried-fine core and the recombination checkpoint's resolved incident/spectral/generated angular skies. Implement the previously tested local Einstein/averaged-scalar equations with Raychaudhuri, baryon number, baryon momentum, the scalar momentum constraint and the virial pressure/longitudinal stress. Return the active and momentum sources at every Runge–Kutta stage. Include all retained quadratic photon and neutrino transport terms (not just perturbed opacity); massless plus the original 36 massive thermal shells. Use independent native first-order metric and baryon histories and evolved incident photon multipoles; photons, gas, neutrino distribution and metric of the generated wave are *not* input histories. Thomson transport is elastic and polarized. Include the derived perturbation of hydrogen/neutral-helium chemistry and previously fitted atomic inputs of RECFAST. Dust-like gas in the generated momentum equation is the inherited approximation; compare a separate native c_b²δb₂ term. Before last scattering diffusion matters; do not replace the radiation by a pressureless fluid there. This is scalar about K, not a solution for arbitrary vector/tensor, entropy or primordial non-Gaussian excitations.

The same-input history uses native angular setting 4 from the z=3999 checkpoint, not a new cosmology. The fine angular solver for the generated modes is separate (2704 to z=99; 4080 over the extension to z=49). Keep setting 16 as a numerical sensitivity, and do not combine its different initial first wave with a second wave from setting 4 without reporting the discontinuity. Kinetics continue from their actual z=99 terminal state in the extension. No astrophysical reionization history is used to score a flux observable. The slow field enters the background and first-order waves. Its omitted direct second-order source is bounded, conditional on the old regular state and supplied interpolants, by continuing the positive oscillator energy estimate from its original bound through each interval; not a global error theorem.

## A constraint that can be evaluated without catastrophic cancellation

D is the synchronous CDM first wave, η the first log-metric curvature, t its scalar shear; 3η′=D′+t. Write Z=η₂−3D²/32+9Dη/16+45η²/32. The scalar spatial Ricci at K is exactly −4k²Z at this order. In the momentum equation the purely geometric flux equals −k(3D+η)t/8 for this triangle. With J the remaining physical longitudinal covariant momentum (including the tetrad-to-coordinate corrections for the radiation),
```
Z′ = J/(2k) + η(12D′+7t)/8 .
```
Evolve from the *same* initial Z. This removes a subtraction of order D² but does not use the Hamiltonian constraint to set any integration constant. Diagnose −4k²Z−4ℋK_e+2D′²/3−(μ²−1/3)t²−2δE independently, where δE carries the inherited 8πG a² normalization. constraint-directions.json propagates alternate initial displacements that would remove the inherited residual using just one channel at a time. These are sensitivities only; none were used to construct the prediction.

## Which density enters the late solver?

First take the independently checked second-order coordinate/normal transformation (absolute_slicing.py in the preceding stage). Use T=t/k², first displacement L=(−2D+6η)/(2k²), the derived second-order T₂,L₂, and the native Weyl transfer Ψ+Φ=η+T′. Use normal-frame first density d and longitudinal sine velocity v and second normal energy E₂ and energy-frame velocity v₂ in what follows. All clustered components are homogeneous dust at the averaging order. For dust, mass measured by the slice normal is E/Γ; its second coefficient is E₂+μv²/2. For comoving-coordinate mass multiply by the induced spatial volume, not by an invented extra force. To quadratic order:
```
V₁=−3Φ,
V₂=3ℋT₂+(3/2)ℋ′T²−C₂−TD′+μk²LD−k²L₂
     −(μ²/2)k⁴L²+(μ/2)(kT)²+V₁²/2.
D_coord,2=D_mass,2+V₁ D_mass,1+V₂;
v_coord,2=v_phys,2+(Ψ+Φ)v_phys,1/2 .
```
This follows independently from the determinant of the induced metric, (a_S/a)³ det(J) sqrt(det γ_S)/Γ_observer. At z=99 and 49 the CDM coordinate mass must also equal the Jacobian of its fixed synchronous labels: −k²L₂+(1−μ²)k⁴L²/2. Its coordinate trajectory requires v_coord,2=kL₂′+μk³LT/2. The baryon number four-current gives the independent number result D_c,coord,2+β₂−C₂+(β₁−D)²/2+T(β₁′−D′)−(1+μ)k²L(β₁−D)−μkT v_b,S. Compare proper and coordinate definitions with the corresponding first-order density choices throughout the late calculation. The Cartesian late solver drops relativistic forces; the coordinate variant is a weak-field sensitivity, not exact nonlinear GR in every gauge.

## Local positive-frequency heavy wave

On a fixed locally inertial slice, remove the homogeneous carrier and use the positive-frequency canonical envelope ψ. Write r=k/(am), ω=sqrt(1+r²); a nonzero Fourier component of the scalar field and its local time derivative uses factors 1/sqrt(ω) and −i sqrt(ω), respectively, in units of m. This nonrelativistic construction has a literature precedent ([Namjoo, Guth & Kaiser](https://arxiv.org/abs/1712.00445)); the equal-triangle inverse and tests here apply it to the retained branch. The stress-normalized pair kernels are e_ij=(ω_iω_j+1+p_i·p_j)/(2 sqrt(ω_iω_j)), j_ij=(ω_i p_j+ω_j p_i)/(2 sqrt(ω_iω_j)), with dimensionless physical momenta. Let e=(ω+1)/(2 sqrt(ω)), c=[2+(1−μ)r²]/(2ω). In ψ/ψ₀ the first-wave cosine has real and imaginary parts a₁=d/(2e), b₁=−sqrt(ω)v/r. The equal-wave crossed flux at K cancels by symmetry. From |ψ|² and ∇argψ/(am) the second-order proper-envelope result is
```
n₂=E₂/e + (1−c/e)(a₁²+b₁²)
vψ₂=sqrt(ω)[v₂+((d+p₁)/2−a₁)v].
```
The first-wave phase speed and number are sqrt(ω)v and d/e. controls.py checks this inversion against direct Fourier analysis of finite scalar fields, their stress, number and phase, including non-small r to expose sign/normalization errors. This is a local positive-frequency/slow-background map, not an exact conserved Noether charge for a real scalar in general curved spacetime. At z=99, r=0.001322 and ℋ/(am)=8.69e−7. Spatial variation of the local frame, relativistic gravity forces and higher carrier corrections are not assigned an invented statistical uncertainty. The overlap evolution directly probes the aggregate matching error in the retained example.

## Independent late readouts

For D (mass coefficient), U=−k v/ℋ and derivatives in ln a, the equivalent Newtonian sum-mode equations are
```
D₂′ = U₂ + D₁U₁/2,
U₂′ = (Σ_i 4πGρ_i D₂,i/H²) − (2+d ln H/d ln a)U₂
       − W k⁴D₂ − U₁²/4 + (3/4)W k⁴D₁² ,
W = 1/(4a⁴m²H²) for the heavy species, 0 for dust.
```
The coefficients apply to this equilateral triangle. Read out Q=2(Σf_iD₂,i)/(Σf_iD₁,i)² and B=3QP² with each model's own linear power. Use the primordial spectrum and matched normalization of the earlier two-mode experiment. Compare its frozen adjoint row plus retarded forcing with a forward ODE; independently evolve density, dust velocity potentials and the complex Schrödinger wave on an oblique periodic grid with their common Poisson force. The real-space and autonomously evolved Fourier comparison does not use native later linear modes as imposed forces. No observed spectrum, fitted three-point coefficient, loop correction, survey window, stochastic galaxy bias, or flux-temperature model is included.

