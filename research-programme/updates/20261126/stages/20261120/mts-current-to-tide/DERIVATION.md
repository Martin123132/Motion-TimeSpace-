> Public reading copy: local links are mapped to released material or marked unavailable. Machine-specific passages, where present, have been omitted. See the inventory for the original digest.

# From a prepared wave number current to the finite-ruler tide

Use the retained positive-quadratic matter branch, CMC launch, even quadrupole to first order in angle, and Gaussian proper clock from the preceding source calculation (not bundled here). This is an *additional* wave-normal momentum density beyond the coordinate phase current. Removing it does not remove the ordinary matter or its gravity.

## The current that enters the constraints

Let n be the coordinate number profile, u=1+χ the conformal factor, μ the rest frequency in launch units, D the positive-frequency correction and d the real normal drift. At fixed n the logarithmic wave amplitude is (log n−log(1+D))/2−3 log u. The common kinetic stress tensor therefore adds the conformal momentum source

    ΔJ_i = −ρ★ n d / [2μ(1+D)] · ∂ᵢ[log n − 6 log u − log(1+D)].

Here the angular gradient coefficient carries 1/r and the spherical and quadrupole radial coefficients are kept separately. Metric volume factors are those of the saved *constraint source*, not extra factors to apply to the force afterward. Deriving it by the log-amplitude formula reproduces all three saved preparation source components. Introduce a bookkeeping strength λ multiplying only ΔJ. Differentiating at zero gives ΔJ of the unperturbed preparation exactly at first order, even if J is a function of the field being solved for: d(λJ[Y(λ)])/dλ at zero is J[Y(0)]. No arbitrary coupling is estimated in this construction.

## Elliptic response and external field

For the monopole, δB₀ = r⁻³∫₀ʳ s³ ΔJ₀(s)ds. For the quadrupole longitudinal field write δW_r=w, δW_t=v, and use radial shear B=(4/3)(w'−w/r)+4v/r, mixed shear C=v'+(w−v)/r, and angular shear A=2v/r. The two divergence equations are

    B' + (3B−6C)/r = ΔJ_r,
    C' + (3C−B/2−2A)/r = ΔJ_t.

One solver uses the inherited finite elements. An independent propagator uses Q=(w,v,rB,rC) and the log-radius equation dQ/d ln r = M Q + r²(0,0,ΔJ_r,ΔJ_t), with

    M = [[1,−3,3/4,0], [−1,1,0,1], [0,0,−2,6], [0,4,1/2,−2]].

Its homogeneous powers are −4, −2, 1 and 3. For a left-eigenvector projection h of the source, each mode equals r^p times an integral of s^(1−p) h(s) ds. Negative powers get an interior integral starting at zero (regular centre); positive powers get an exterior integral starting at the outer radius. Fix the two remaining regular coefficients by the two outer values of w,v. In the response the variations of these data are **zero**, but their baseline values stay in the preparation. This gives a nontrivial exterior contribution without adding a free external tide. In particular an independent nonzero homogeneous wall fixture returns (B,C,A)=(4,2,2): setting the physical variation of a boundary value to zero is not discarding its solution space.

The scalar constraint is −Δχ=S(u,u',B), S=u⁵E/4+3B²/(16u⁷). At fixed sources except ΔJ the scalar tangent obeys

    [−Δ−S_u−S_{u'}∂r] δχ = 3B δB/(8u⁷).

Use the same matched Robin and centre conditions for both harmonics. Solve the monopole first: the angular variations of the coefficients multiply it on the right of the quadrupole equation. The sparse tangent solve acts on the correction itself, not the difference of two metric solutions. A trial fixed-point implementation did not reliably settle for very small exterior-only inputs; using the assembled linear operator avoids that conditioning issue. Differentiate the implicit positive-frequency graph, both initial surrounding-frame currents and the metric-to-proper-distance mapping. The number derivative at launch, 2δRe L + δell+2δB_area + δD/(1+D), vanishes (B_area is the angular log scale, not the shear above). Only then propagate the original closed first response for the same proper time and take its proper-ruler derivative. The derivative of the final measurement is a centred numerical derivative **along this analytically solved direction**; multiple gains test its stability. It is not a second fit or a second complete initial constraint solve.

## A weak-field source with no solved relativistic wave graph

At fixed physical mass and occupation, let ε scale as 1/c, geometric densities as ε², H and the coordinate velocity potential V as ε, and μ as ε⁻¹. Keep the aperture in length units fixed. In these units u−1 and D are order ε², d is order ε². At leading order write g=∇log n, B_V=ΔV+g·∇V and d₀=−(3H+B_V)/(2μ); the source is −ρ★ n d₀ g/(2μ), order ε⁵. This is a source-order statement under these assumptions, not a statement that an observed acceleration is order ε⁵.

The next correction uses Q₀=Δ√n/√n and D₂=(|∇V|²−Q₀/μ²)/2. Determine χ₂ from the scalar Poisson constraint with the coordinate number-density source and the supplied external density and boundary data. The first drift change is d₁=(4χ₂ B_V+4∇χ₂·∇V)/(2μ). Relative to the common factor −ρ★n/(2μ), the predicted added terms are

    d₁ g − d₀ D₂ g − 6d₀∇χ₂ − d₀∇D₂.

The derivative of log u accounts for the factor 6; replacing the amplitude by a fixed proper density would miss it. This construction uses the formation-stage number, phase, H, explicit surrounding source and boundary potential. It does **not** read the relativistic normal graph or solved conformal metric to build the correction. Its downstream transfer to the detector still uses the constrained relativistic background. Interchanging these two claims would overstate the Newtonian limit.

## Precision and coverage

Source partitions and gains were fixed in [the initial protocol](PREDICTION.md). Partitioning the current before solving is important: integrating only the interior monopole would lose an angular exterior field. Projections are conditional diagnostics in the fixed gauge/ruler; neither the angular components nor the radial partitions are separately observable forces. The switch diagnosis (not bundled here) uses complete nonlinear preparations only as controls after prediction. [The compensated unit switch](evidence-001.zip) (archive member: `unit_switch.py`) differentiates the shear of the small vector solution before adding the background shear, re-solves both scalar harmonics and the normal graph, and propagates the finite switch without first differencing total vector solutions. All signed dust cases have zero added-source response; their physical dust currents are not set to zero. No observational data have been added.
