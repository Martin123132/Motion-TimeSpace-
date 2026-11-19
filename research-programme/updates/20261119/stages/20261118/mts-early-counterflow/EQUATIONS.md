# Primordial curvature to the scalar matching slice

**Convention.** Flat common-Einstein-metric branch, geodesic irrotational CDM; conformal time τ (Mpc), primes d/dτ. Spatial metric is a²γ. CDM labels and synchronous slicing are those of the native solver. Use the cosine at K=p+q for two distinct unit-curvature incoming waves: |p|=|q|=|K|=k, μ=p·q/k²=−1/2. No extra factorial. Every second-order number below multiplies the product of two small primordial amplitudes. Velocities and density transfers are not physical order-one disturbances. MTS's real heavy field f uses the original canonical normalization 8πG absorbed into f; write m_a²=a²m² and g_s=8πG a²ρ_s. [Ma & Bertschinger](https://arxiv.org/abs/astro-ph/9506072) gives the linear synchronous convention, not the nonlinear matching prescription here.

**CDM and heavy field evolve together, before the switch.** Set C=ln(ρ_c/ρ̄_c); the expansion scalar obeys aθ=3ℋ−C'. The covariant Raychaudhuri equation and the scalar action give
```
C''+ℋ C' = C'²/3 + a²σᵢⱼσⁱʲ + 4πG a² δ(E+S),
f''+2ℋ f'−Δγ f + m_a² f = C' f'.
```
Here E is normal-frame energy density and S the spatial stress trace. For this canonical scalar, 8πG a²(E+S)=2 f'²−m_a² f² exactly; spatial-gradient terms cancel in the trace, not in its energy density. This uses the retained common metric, not a new dark force. Let D=C₁, s=kσ_CAMB=−ℋ U_c, η=etak/k, v_b the synchronous baryon velocity sine coefficient. The synchronous spatial perturbation is (h+6η)nᵢnⱼ−2ηδᵢⱼ, h=−2D. Compute D' independently of differentiating a float32 density: D'=ℋ growth[(1−f_b)D+f_b δ_b]+f_b k v_b with f_b=ρ_b/(ρ_c+ρ_b).

For X=(C₂,C₂',f₂,f₂') the nontrivial equations are
```
C₂''=−ℋ C₂' + g_c C₂/2 + 2f₀'f₂'−m_a²f₀ f₂
      + D'²/3+(μ²−1/3)s²+g_c D²/4 + f₁'²−m_a²f₁²/2
      −μ g_b v_b² + ℋ² u_ext .
f₂''=−2ℋ f₂'−(k²+m_a²)f₂ + f₀' C₂' + D'f₁'−(5/2)k²η f₁ .
```
Drop the heavy entries in the ordinary cold control, not the baryons from the native gravity. The shear contraction follows by taking the trace of the two traceless directional tensors. The curved Laplacian follows by expanding (det γ)^−1/2 ∂ᵢ[(det γ)^1/2 γⁱʲ∂ⱼf]. At general μ its bilinear coefficient is k²f₁[(μ²+μ/2)h+(6μ²+4μ−2)η]; the trace h cancels at this triangle. u_ext is the *second-order* omitted active gravitational stress in units ℋ²/(4πG a²), after displaying the cold baryon bulk term. A constant unit u does not represent a cosmological model. At linear order the independent full-history replay includes photons, baryons, massless neutrinos, the slow scalar and the massive-neutrino trace in its relativistic approximation. The accuracy of this independent replay is measured, not assumed.

**Matching candidate.** Read out CDM density C₂+D²/2 and C₂'/ℋ at the matching centre. For the heavy sector apply the saved oscillation-projector P (6π half-width, degree 8, same nodes and centre) to these two coefficients:
```
δh₂=P{ a [ f₀' f₂' + m_a² f₀ f₂ + ( f₁'²+(m_a²−μ k²) f₁² )/2 ] / ρ_match }
qh₂=P{ a k [f₀' f₂ + f₁'f₁/2] / ρ_match } .
```
q is the longitudinal normal momentum with its spatial index down, in the native sign; it is not the second-order velocity divided by enthalpy. These expressions follow from the unaveraged normal energy and momentum tensors. Applying this particular *linear* averaging functional to the nonlinear tensors defines a diagnostic. A nonlinear distributional/junction or effective-fluid matching argument (and a second-order gauge transformation to compare with the late Newtonian variables) is still necessary. Specifying the error in C₂ at a later Newtonian slice by the difference found here would be incorrect.

**The acoustic gravity source.** Within the tightly coupled adiabatic sector define β=ln(n_E/n̄), n_E=Γ n_rest the baryon number per unit normal proper volume. The rest photon density is ρ̄γ[exp(β)/Γ]^(4/3). Define covariant fluid momentum Pᵢ=T⁰ᵢ/(ρ̄_b+4ρ̄γ/3), r=(4ρ̄γ/3)/(ρ̄_b+4ρ̄γ/3), c²=r/3. Then to second order, suppressing the explicitly excluded pressure slip, diffusion, and intrinsic quadrupole:
```
β₂'= C₂'−k P₂ + k v_b[(1+r/6)β₁−5η/2]
P₂'=−(1−r)ℋ P₂ + k c² β₂ + D'v_b/2
      +k c²[2β₁²/3 + μ v_b²/2]−k v_b²/4 .
4πG a² δ(E+S)_bγ,2
    =(g_b/2)[β₂+β₁²/2−3μ v_b²/2]
      +g_γ[4β₂/3+8β₁²/9−2μ v_b²/3] .
```
Use β₁=δ_b from the full native solution. Replace, do not add to, the isolated baryon kinetic term on the chosen window. For the derivation use baryon number conservation β'=C'−∂ᵢvⁱ+vⁱ∂ᵢ(C−β) and total covariant momentum conservation. To second order vᵢ₂=Pᵢ₂−(1+r/3)β₁ vᵢ₁; raise with the perturbed γⁱʲ. Isotropic pressure contributes −∂ᵢp_rest/(ρ̄_b+4ρ̄γ/3), with δp₂/W=c²(β₂+2β₁²/3−[v²]₂/2). Momentum transport also contributes −∂ⱼ(vʲvᵢ). The cosine coefficient of [v²]₂ is −μ v_b². The periodic fixture separately computes these terms from the exact current and stress on a curved metric without inputting the quadratic formula. This is adiabatic true tight coupling, not a guarantee of tight coupling for the entire matching epoch.

**Physical initial datum in the growing, adiabatic subfamily.** Write the long-wavelength primordial spatial metric e^(2ζ)δᵢⱼ in its conformally flat labels, including an explicit possible ζ₂. At leading two-gradient order, the Hamiltonian constraint gives R[γ]−4ℋ C'=16πG a²δE; radiation dominance and uniform entropy give δE_r=(4/3)ρ̄_r C to this gradient order. Regularity removes the decaying solution, leaving C=τ²R[γ]/16. R=e^(−2ζ)[−4Δζ−2(∇ζ)²]. A coordinate change matters: to the native h→0 labels x_conformal=x_native−3Σ n ζ₁ sin(k·x)/k at first order. Curvature is a scalar, so pull it back before taking the sum mode. The quadratic curvature coefficient for two identical amplitudes ζ₁ is (−8+2μ−12μ)k²ζ₁²+4K²ζ₂, i.e. −3k²ζ₁²+4k²ζ₂ here. Missing this pullback would give −9 rather than −3.
```
C₂ ≈ (kτ)²(ζ₂/4 −3ζ₁²/16),  C₂'≈2 C₂/τ,
β₂≈C₂,  P₂≈ kτ C₂/9,
f₂≈−f₀(a m τ)² C₂/105,  f₂'≈6 f₂/τ .
```
The last relation integrates KG with the regular frozen-field background and its incoming homogeneous isocurvature set to zero. The coefficient applies in the same radiation-dominated, leading-gradient expansion as the native scalar seed. These are not identities at arbitrary finite kτ. Corrections include higher gradients, departures from radiation domination, entropy/decaying modes and any primordial non-Gaussian preparation; the integrated quadratic sources are subsequently required. Four native starting times test the leading regular *linear* expansion, not a previously unavailable exact native nonlinear solution.

**A direction that propagates exactly.** At order two, varying only an adiabatic primordial sum-mode amplitude while holding both incoming waves fixed is governed by the *linear* full species system (the quadratic sources do not vary). Thus in the same Newtonian density convention at z=8, dQ/dζ₂=2/T_m(K,z) for an equilateral tree amplitude, where T_m is the unnormalized total clustered linear transfer for unit ζ. Compute the heavy-minus-cold derivative, and independently contract the older z=99 response row with the corresponding multi-species density and velocity direction. This is a constraint on one direction; geometric nonlinear propagation is not identical to adding a primordial mode of −3/4 for all species. The Planck number is a separately labelled published template illustration, not a new likelihood, and does not constrain scale-dependent or heavy-isocurvature data here.
