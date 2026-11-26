> Public reading copy: local links are mapped to released material or marked unavailable. Machine-specific passages, where present, have been omitted. See the inventory for the original digest.

# Where the centre term enters, and what determines the replacement equation

Local calculation, 21 November 2026. The predecessor is [the recovered Cartesian curvature operator](../mts-cartesian-origin-transport/RESULTS.md). The object studied here is the quadrupole of the **controlled cosmological formation**, not a new Milky Way occupation model. The original state files are read-only.

## From matter to the launch constraint

The q=1024 preparation uses the conformal factor u=1+χ₀, its quadrupole x=χ₂, rest-density weights ρᵢ, spherical number nᵢ, signed quadrupole Dᵢ, radial speed pᵢ and quadrupole speed Pᵢ. Its monopole source is u⁵ E/4+3b²/(16u⁷). For a dust species w=√(1+p²/u⁴)−1. For the retained massive-wave branch, w=(p²+εG²)/(2u⁴) and G=(∂ᵣn)/n−6∂ᵣu/u. Differentiating the same source gives, for each species, three distinct quadrupole contributions:

    number: ρ D/(4u)
    kinetic: ρ (D w+n δw)/(4u)
    volume: −6 ρ n(1+w)x/(4u²).

The remaining terms are 5u⁴xE/4, the surrounding and normal-graph quadrupoles times u⁵/4, and 3b b₂/(8u⁷)−21b²x/(16u⁸). [Independent differentiation](evidence-001.zip) (archive member: `sector_source.py`) uses these expressions, rather than the parent’s complex directional derivative. The two external terms are split at the original, uncorrected surrounding-source value. The original solve is rebuilt and checked against the saved packets before attributing the contamination.

The first-element slope can also be predicted **without** the rebuilt metric: multiply each signed *native formation density* polynomial’s derivative at zero by ρᵢ/4, and sum. Incoming spherical-Bessel quadrupoles have no linear power; neither total occupation nor a coupling was fitted to infer this coefficient. Comparing formation on two meshes and two outer domains distinguishes the first-element representation from the remote boundary.

## The continuity equation gives an independent physical check

Use the original log-scale-factor clock, with conformal Hubble rate H. At the start the local angular density and phase increments vanish. C(r) is the spherical fractional number excess; v is the radial derivative of the spherical velocity potential. D★ and P★ are the incoming density and phase quadrupoles. Inside the collar the launch monopoles are sums of j₀(kr), the quadrupoles sums of j₂(kr). The continuum rate is

    H Ḋ = −C Δ₂P★ − C′P★′ − v D★′ − (v′+2v/r)D★.

It follows by expanding the divergence of the radial flux C P★′+v D★ and adding its angular part 6 C P★/r². If C=C₀+C₂r²+…, v=v₁r+…, D★=d₂r²+…, and P★=p₂r²+p₄r⁴+…, then H Ḋ/r² tends to −14C₀p₄−4C₂p₂−5v₁d₂. In particular the **linear coefficient is zero at this physical launch**, and the quadratic coefficient is independently known and generally nonzero. [Launch test](evidence-001.zip) (archive member: `first_flux.py`) evaluates it from the saved mode weights, from the strong equation at nonzero radius, and from the native weak equations. Inserting the exact analytic fluxes into the old lumped quadrature isolates what the old weak divergence produces without any interpolated matter gradients.

## A conservative alternative to editing the source

For a smooth Cartesian degree-two perturbation, D and the velocity potential w have the form r² f(r²); a stored reduced spherical field has the form r f(r²). On the *first* formation element take the subspaces t²,t⁴,t⁶ and t,t³,t⁵ respectively, t=r/h. They are the regular subspaces of the original degree-six polynomial space, not a smooth fit to the saved endpoint. Use the original incident history and original start; project the starting monopoles with the native nodal mass so their radial mass moments are retained. The endpoint belongs to both elements. Do not fix its value at launch or suppress it when differentiating.

Let B denote the angular test functions, n=1+C, and D,w the subsequently evolving local angular perturbations. The weak continuity load in the first element is

    H M α̇ = ∫ [r² B′ (n w′ + v D + C P★′ + v D★) + 6 B (n w + C P★)] dr
            + B(h) × (native neighbouring element's interface load),
    M = ∫ r² B Bᵀ dr + m_neighbour B(h)B(h)ᵀ.

Here α are the three unknown coefficients; both terms come from the original flux law. We integrate the first element at 20 Gaussian points, retain its full mass matrix, and leave the neighbouring test space and the exterior unchanged. The reduced spherical and phase rates use their native mass-orthogonal projections. Since r and r² are respectively admissible test functions, the spherical mass moment and the tested quadrupole flux moment are not discarded. The latter is a **balance** with incoming, angular, and interface work, not a conserved enclosed quadrupole. This is not a proof that every sector of the discrete parent is globally conservative. The implementation (not bundled here) changes no particle mass, initial host sign, source calibration, surrounding history, or physical aperture.

The zero slope of the new basis is not the accuracy test. The tests are its *nonzero* r² coefficient versus the independent continuum value, the signed integrated flux with separately evaluated fields, agreement across genuinely re-evolved meshes at finite radii, the reconstructed Hamiltonian source, and the wave-minus-cold proper tides. The source and transport controls use no new sky data.
