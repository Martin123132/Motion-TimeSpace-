> Public reading copy: local links are mapped to released material or marked unavailable. Machine-specific passages, where present, have been omitted. See the inventory for the original digest.

# When the retained heavy-wave pressure first gravitates

**Conventions.** This stage uses the common, minimally coupled Einstein-metric branch that is already in the model. It derives its weak-field response, not the metric action or the value of Newton's constant. Work in flat FLRW, with conformal time τ and c=1. Distances are comoving Mpc; H here means a'/a, not the physical Hubble rate. R, P, D, Q and Π include 8πGa² (the Q sign is CAMB's); S=R+P. The line element is a²[−(1+2Ψ)dτ²+(1−2Φ)dx²]. For the gauge conventions and perturbation equations see [Ma & Bertschinger](https://arxiv.org/abs/astro-ph/9506072). The calibrated mass, Fourier weights, initial phases and cosmological hypotheses all come from the [predecessor](../mts-transmitted-formation-tide/RESULTS.md).

## 1. Check the metric before subtracting two solutions

The native synchronous clock shift is α=σ/k. Thus Φ=η−Hα, Ψ=(σ'+Hσ)/k, Φ−Ψ=Π/k², W=(Φ+Ψ)/2. The total compensated coordinate-density source and Newtonian energy current are D*=D_sync−3Sη and Q_N=Q_sync+Sσ. The flat Hamiltonian and momentum constraints give

    (2k²+3S)Φ = −D*−3H Q_N/k,        Φ'+HΨ= Q_N/(2k).

The factor 3S is not a Yukawa modification to GR: it is what appears when *every* density is expressed on this volume convention. In synchronous variables the same answer is −(D_sync+3H Q_sync/k)/(2k²). For a dust-background species d=δ_N−3Φ and V=−θ_N/k². Newtonian matter-only Φ from the archived d, all-species lapse and Weyl are three different numbers. The radial force reads −∂rΨ on the symmetry axis; the polar force at θ=π/4 is +3Ψ₂/(2r) for a P₂ mode. The trace-free axial tide is −(∂r²−∇²/3)Ψ on axis. These are rescaled conformal readouts, not the entire observed light-cone lensing or line-of-sight acceleration.

## 2. A matched switch predicts **two** coefficients

After recording the native state at a=0.01, set only the averaged heavy pressure perturbation to zero in a control. The same equation computes both its stress diagnostic and its density and current derivatives; neither the mean density nor the gravitational coupling is switched. The two branches restart their integrator at the identical saved-time boundary in the same way. All other species evolve in their respective metric. This counterfactual heavy control is different from the independently evolved cosmology with no heavy component.

Let Δ denote retained minus switched. At matching all field values, Φ, Ψ and Φ' agree. For dust background R_h=S_h=C_h/a, θ_h=−k²V and π=δp_h/ρ_h in Newtonian coordinates,

    B = d+3Φ−3HV,       u=k/(am),       s=u²/(1+√(1+u²))²,
    π=sB,               d'=k²V−3Hπ,     V'=−HV−Ψ−π.

Rest-frame pressure is the retained **matched effective model**, not a new choice fitted here. At launch Δd'=−3Hπ and ΔV'=−π: their contributions to Δ(d−3HV)' cancel exactly. Treating d alone as gravitating mass gives the wrong onset. The momentum equation above then gives ΔΦ''=R_hπ/2. Independently the trace of the spatial Einstein equation reads

    Φ'' + H(2Φ'+Ψ') + (2H'+H²)Ψ + k²(Φ−Ψ)/3 = (8πGa²/2) δp_N.

At launch the heavy fluid has no linear anisotropic stress; other species have identical state, lapse and curvature rate. Their density and pressure perturbations therefore have identical first derivatives. In Newtonian coordinates the free-streaming quadrupole is driven by neighbouring angular moments; their first derivatives are unchanged at launch. Thus the difference in the slip and its first **two** derivatives vanishes there on this late, free-streaming branch. This is not an assumption that the subsequent slip stays zero. Differentiate the trace, use R_h'/R_h=−H, s'/s=−2H/√(1+u²), and H²−H'=S/2:

    B'=(k²+3S/2)V+3Q_N/(2k)
    A=ΔΦ''(0)=R_h s B/2
    J=ΔΦ'''(0)=R_h s [B'−(4+2/√(1+u²)) H B]/2.

Consequently ΔΦ=A Δτ²/2+J Δτ³/6+O(Δτ⁴). Both numbers are obtained from the original pressure-on launch state, not by fitting the differences. Independent checks use the measured *later* native differences, including Φ'=Q_N/(2k)−HΨ, measured Weyl derivative and evolving stress. The Newtonian quadratic coefficient from the separately evolved matched model is R_h k²d/[8(am)²]. It approaches the GR coefficient only where the comoving density shift and the finite k/(am) dispersion correction are small. The cosmological test covers 99 modes, not an arbitrary window around one wavenumber.

## 3. What stress is actually present on the two spherical preparations?

The nonlinear archived clouds are weak-field matter solutions; no nonlinear metric time slice is supplied. A useful exactly local geometric identity, with geodesic deviation written as −Rᵢ₀ⱼ₀, is

    (−Rᵢ₀ⱼ₀ + Cᵢ₀ⱼ₀)^TF = + Rᵢⱼ^TF/2 = 4πG Tᵢⱼ^TF

in an orthonormal observer frame. It isolates anisotropic matter stress, without inferring the freely determined Weyl tensor. For the nonrelativistic envelope of a minimally coupled canonical massive field, write ψ=√n exp(iamV). The spatial gradient part of its Hilbert stress in units 8πGa² is R_h[n ∂ᵢV ∂ⱼV + ε ∂ᵢn ∂ⱼn/n]^TF, ε=1/[4(am)²]; the traces from mass, pressure, time derivatives and the metric term drop out. The dust species have just the streaming term. The Schrödinger–Poisson limit is discussed by [Hui et al.](https://arxiv.org/abs/1610.08297); here it is evaluated on the retained calibrated states, not a fit to a halo. The estimate uses leading proper mass density and peculiar velocity in the cosmological normal frame. Coordinate-to-proper and post-Newtonian corrections to this estimate are not being bounded by numerical mesh agreement.

Write n=n₀+λDP₂ and V=V₀+λvP₂ with u₀=V₀'. Here D and v are the **total** quadrupole including the noncompact reference and the localized excess. At λ=0 the rr streaming coefficient before trace removal is DU₀²+2n₀U₀v' (U₀=u₀); the gradient term is ε[2n₀'D'/n₀−(n₀'/n₀)²D]. Multiply by 2/3 on axis and by R_species/2. At π/4 the rθ coefficient uses n₀U₀v/r and ε n₀'D/(n₀r), times −3R_species/4. Physical differential acceleration per separation in s⁻² multiplies this output by c²/(a Mpc)². A Cartesian field-gradient calculation and an independent radial mesh check these tensor components.

The two angular evolutions live on the *same* archived spherical background in each preparation. Report separately (i) the change of streaming, (ii) the explicit canonical gradient stress evaluated on the pressure-on state, and (iii) their sum against a pressureless angular comparator. That comparator is not a separately evolved pressureless nonlinear background. The Newtonian **host-only** trace-free tide used for scale comes from its localized quadrupolar potential: −(2/3)∇²Φ−2g_r/r−6Φ/r², g_r=−∂rΦ. This is not division by the total cosmological tide.

## 4. Momentum is not a bare phase

Subtract the unperturbed homogeneous quadrupole reference, denoting the saved excess density and phase by δD and w. In the same leading local frame the excess number flux for each species has a radial coefficient (n₀−1)Vref' + n₀ w' + U₀(Dref+δD) and tangential coefficient [(n₀−1)Vref+n₀w]/r multiplying ∂θP₂. Weight each by R_species, sum, and call the result (jᵣ,jₜ). It need not be a gradient. Project vⱼ via ∇²vⱼ=div j, regular at the origin with decaying exterior. For the contribution from the flux *inside* b, extend that contribution by zero, retaining the jump in its divergence at b. Shell integration by parts gives, for r<b,

    5vⱼ(r)=∫₀ʳ(s/r)³(2jᵣ+6jₜ)ds + ∫ᵣᵇ(r/s)²(−3jᵣ+6jₜ)ds.

A compact pure gradient is recovered; a compact divergence-free current gives zero; an independent variational Poisson solve with exterior Robin condition measures the same quantity. Report b=96 and 120 Mpc separately. This bounds sensitivity to the *measured shell*, not to an unknown exterior. In the linear momentum constraint at fixed slicing the scalar term from this current is −vⱼ/2. Substituting it alone does not solve nonlinear Einstein constraints: metric products, the observer clock, other species' mixed response and any unconstrained free data must be treated on the same slice.
