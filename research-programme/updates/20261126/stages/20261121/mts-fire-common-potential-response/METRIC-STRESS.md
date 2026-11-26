> Public reading copy: local links are mapped to released material or marked unavailable. Machine-specific passages, where present, have been omitted. See the inventory for the original digest.

# What these same waves source beyond the Newtonian density term

**Scope.** This is the spherical part of the *linear metric contribution of the heavy wave's anisotropic stress*, at the two existing probe radii. It is calculated from the retained quadratic matter action and common Einstein metric term, not from a fitted ratio of lensing to dynamics. The FIRE history and the ordinary foreground used for evolution are unchanged. This is distinct from re-integrating the halo through a post-Newtonian metric.

For ds²=−(1+2Φ/c²)c²dt²+(1−2Ψ/c²)d𝐱², define S=Ψ−Φ. The trace-free, scalar part of the linear spatial Einstein equation is DᵢⱼS=8πG Πᵢⱼ/c², where Dᵢⱼ=∂ᵢ∂ⱼ−δᵢⱼ∇²/3 and Π is the scalar part of the anisotropic stress in pressure units. This sign follows by substituting h₀₀=−2Φ/c² and hᵢⱼ=−2Ψδᵢⱼ/c² in the linear Ricci tensor; the trace drops out. Take the spherical projection of the *tensor*, not the anisotropic stress of a sphericalized density. The radial–tangential pressure difference is the angular average Δp=⟨T_rr−(T_θθ+T_φφ)/2⟩ in an orthonormal frame, not a time average over galactic orbits. No transverse vector or tensor monopole contributes for a regular localized source.

For the retained minimally coupled real heavy scalar, the mass term and the isotropic parts of the Hilbert stress cancel in Δp. Averaging the fast carrier oscillations, and normalizing the complex envelope so that |a|² is **mass** density, gives the leading spatial trace-free stress κ² Re(∂ᵢa*∂ⱼa)ᵀᶠ, κ=ℏ/m. No fluid shear law is imposed. In particular a density gradient can source stress even for an envelope with no coherent radial velocity. The spherical equations become

    S″−S′/r = 8πG Δp/c²,
    −S′(r) = (8πG/c²) r ∫ᵣ^∞ Δp(t)/t dt,
    S(r) = (4πG/c²) ∫ᵣ^∞ [(t²−r²)/t] Δp(t) dt.

The spatially constant solution is fixed by S(∞)=0 and the growing r² mode by isolation. Thus a compact anisotropic source gives zero **exterior monopole force difference** outside its entire support at this order; its force difference *inside* samples pressure outside the probe. This is not the enclosed-mass law for the ordinary Newtonian force.

Let y=r/L, M*=v²L/G, κ=vL. The code's reduced modes are u_l(y), with angular functions of unit norm over the sphere and a mass unit M*. Then 4π L³Δp/(M*v²) is

    B(y) = Σ_l { |u_l′−u_l/y|²/y² − l(l+1)|u_l|²/(2y⁴) }.

Consequently S/v²=(v²/c²)∫B(t)(t²−y²)/t dt and −L S′/v²=(2v²/c²)y∫B(t)/t dt. The separately computed monopole Newtonian acceleration in the same units is −Σ∫₀ʸ|u_l|²dt/y². Evaluate the differentiated radial finite elements directly; retain both gradient terms through the maximum wave degree. Two compact polynomial profiles (l=0,2 with the edge at an element boundary) check signs, radial scaling, angular factors and normalization against analytic integral polynomials, in addition to quadrature refinement. For the passive branch the table describes what its density and stress *would* source, not a different metric actually applied to transport it.

**Reading the result.** −S′ is the difference between the radial gradients of the two metric potentials, not a second force to add to stellar accelerations. This is only the heavy matter term linear in the metric perturbations. Nonlinear gravity from the Newtonian potential can be of the same post-Newtonian order; ordinary stresses, stresses of any other sectors, other multipoles and boundary/propagation effects are not included. No total Galactic slip, PPN γ, lensing constraint or violation of GR follows. A static NFW density without its stress tensor does not specify the same stress observable and is not silently scored as having zero slip. A GR metric supplied with the identical matter stress has the identical contribution.

## Matched finite-shell constraint with the geometric term

Use logarithmic potentials for this separate post-Newtonian diagnostic: g₀₀=−exp(2ν), gᵢⱼ=exp(2λ)δᵢⱼ, Φ=c²ν and Ψ=−c²λ. At Newtonian order Φ=Ψ=U. In the prescribed scalar metric with zero shift the trace-free spatial Ricci tensor is the trace-free part of

    −∂ᵢ∂ⱼ(λ+ν) + λᵢλⱼ − νᵢνⱼ + λᵢνⱼ + λⱼνᵢ .

Time derivatives are pure trace in this metric, not discarded by identifying a nonstationary wave as static. The result is checked independently by contracting Christoffel symbols with arbitrary functions of time and all three coordinates and, separately, for a radial isotropic metric. At the first order beyond equal Newtonian potentials this gives DᵢⱼS = [8πG Πᵢⱼ + 2(∂ᵢU∂ⱼU)ᵀᶠ]/c² for this scalar source. The geometric sign and normalization reproduce the exact isotropic Schwarzschild vacuum: −c²(λ+ν)=−c² log[1−(GM/2rc²)²]. Do not substitute metric potentials defined by a different quadratic expansion for these logarithmic ones. Eight exact checks (not bundled here).

Evaluate the finite-shell combination A₁₂=−S′(r₁)+(r₁/r₂)S′(r₂). The homogeneous r² solution and all exterior integration constants cancel. Its heavy-stress contribution is the restriction of the previous pressure integral to [r₁,r₂]. Its geometric contribution is (2r₁/c²)∫[⟨Uᵣ²−|∇ΩU|²/(2r²)⟩/r]dr on the same shell. For orthonormally expanded potentials this angular average is Σ(|U_l′|²−l(l+1)|U_l|²/(2r²)). Only the degrees present in the wave potential enter its cross term with a prescribed ordinary potential; ordinary-ordinary terms cancel. Wave potentials use the actual retained Poisson operator rather than the longer density series used for the diagnostic force. Two radial quadratures and interpolation of either U or rU check the shell integration.

Difference the sources of the coupled and reset states at the final snapshot, or separately the would-source tracer and reset. In addition to the wave stress this retains the wave–wave geometric difference and **twice the cross term with the ordinary gravitational field**. The full 3D angular dependence in the retained axisymmetric potential basis is included before averaging; this is not the field of a sphericalized mass distribution. A pure quadrupolar manufactured potential checks the gradient term's angular contribution. The snapshot-600 ordinary assembly potential is the same for the two branches; ordinary stresses are explicitly held fixed in this source comparison. There is no live ordinary post-Newtonian response, independent vector/tensor preparation, or imposed direct LMC field in this axisymmetric evolution. The six direct alternatives appear only in the separate force-band readout. The shell table (not bundled here) is a boundary-independent prediction of the retained scalar constraint **under those conditions**, not the absolute metric of the Milky Way. It needs no universal slip parameter.
