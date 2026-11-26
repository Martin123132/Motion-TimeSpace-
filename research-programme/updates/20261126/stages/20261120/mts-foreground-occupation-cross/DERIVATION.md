# One source of gravity, two directions to test it

## Crossing source and occupation

Use the same positive quadratic weak-field branch and wave particle mass. In the mass-weighted basis solve (T+V_b+U[g²])g=μg. U is the attractive Newton potential, N=gᵀg is particle number in the saved normalization. The direct ordinary readout includes the nonaxisymmetric stars on the observational meridian; only the induced sector here is restricted to the azimuthal mean and even vertical parity. The spectral solver, vacuum gravity, retained six time histories and zero-start convention are unchanged.

Let D(F,N) be a freshly equilibrated stationary dark force for foreground F and occupation N. Four corners AH, AL, BH, BL suffice. Attribute half the sum of the two source differences (BH−AH and BL−AL) to the ordinary potential's effect on the wave, and half the sum of the two number differences (AL−AH and BL−BH) to occupation. The interaction BL−BH−AL+AH is reported separately but is already split between these two totals. This is symmetric accounting, not a new physical independence assumption. Add the pure direct ordinary-force difference once and the separately propagated LMC wave-force difference once. The same direct satellite acceleration cancels between cases. For the spherical NFW control match the dark force at 17.58 kpc after each preparation. No continuous inner-fit amplitude.

For the continuous interpolation V_b(f)=V_A+f(V_B−V_A), constrain the total inward outer force to v²/R₀. Let Gₐ and Dₐ be the direct ordinary and dark inward forces there. Use the bordered tangent of the stationary equation and number constraint: the derivative with respect to f has source −(V_B−V_A)g and gᵀg_f=0; the derivative with respect to N has zero source and gᵀg_N=1/2. Poisson differentiation supplies the self-gravity terms. Then

    dN/df |v = −(Gₐ,f + Dₐ,f|N) / Dₐ,N .
    dD_j/df |v = D_j,f|N + D_j,N dN/df |v .
    dN/dv |f = (2v/R₀) / Dₐ,N .

Use common acceleration units throughout. At the one-width endpoint the fixed-number inner radial wave derivative is −0.43923 per unit f, but after maintaining the outer speed it becomes +0.02486: the response actually changes sign. Five force derivatives check against independent neighboring constrained solves. speed_response.py checks the second calibration direction against ±0.05 km/s solves; anchor_width.py tests the much wider, actual ±1.91 km/s calibration endpoints nonlinearly.

## A local direction requirement without fitting a halo

For each hemisphere subtract its own direct ordinary and satellite accelerations from the corresponding upper and lower bands. Combine the two radial residuals by half their sum, the two polar ones by half their north-minus-south difference. This gives intervals for the mirror-symmetric sector even if the other parity is arbitrary. Correlations between marginal observational limits are not known; the resulting rectangular set is deliberately permissive. Averaging the two bounds for each component supplies *necessary* bounds, not a simultaneous likelihood test.

For fixed f the interval box is affine in f. Write u=−aᵣ>0 for inward radial force and t=aθ for polar force in the northern meridian. The tilt toward the plane relative to the inward radial direction is arctan(t/u). The extrema over the entire census-admissible mixture interval occur on its endpoint boxes: t/u is a ratio of affine functions with positive denominator along each connecting edge; it cannot exceed its vertex extremes. Separately verify the result on an interior grid. This bounds the direction of **the required remaining force**, not necessarily the wave's direction throughout the interval. For a locally axisymmetric equipotential with inward cylindrical and downward vertical gravity, the equivalent force axis ratio is

    q_force² = (Z/R)(R aᵣ + Z aθ)/(Z aᵣ − R aθ).

It is 1 in a spherical potential. It describes the local slope of an equipotential, not the mass-density axis ratio. The same identity applies to the *total* field at a stellar stream, with the ordinary field added rather than subtracted. The dark-force tilt bound at 6 kpc and the observed total force directions high above the plane are not interchangeable.

## What a nonnegative halo can do between the speed anchor and Pal 5

Use forces in km/s/Myr; C converts (km/s)²/kpc to these units. For the Pal 5 normalization combination set p=(0.94², Z/R), e=(R,Z)/r, k=p·e, η=(R₀/r)², with R₀=17.58 kpc and r=√(8.4²+16.8²) kpc. D₀ is the positive dark inward radial force at the outer *midplane* calibration. S_b is the published linear force combination evaluated using ordinary gravity including its additive zero-point terms. For any nonnegative **spherical** halo the best possible (least negative) combination is S_b−kηD₀; any mass in the shell makes it more negative. No NFW scale, density slope or concentration is needed. This is an upper bound, not a sufficient joint test of both stream observables.

For a nonspherical positive wave the identity is more informative. Put A₀=D₀−CGM(<R₀)/R₀², Aₚ=p·(F_dark−F_monopole) at the stream, and ΔM=M(<r)−M(<R₀). Then

    S = S_b − kηD₀ + [Aₚ+kηA₀] − kCGΔM/r² .

The bracket measures the change from nonspherical gravity at both sites. The equation is exact for the stationary weak-field readouts with the stored units. shell_budget.py integrates enclosed mass by splitting the finite elements at both radii. Independent monopole gravitational gradients reproduce those masses to <10⁻⁹ relative. The paper's adopted stationary force summaries are a model-dependent observational interface: this identity does not reconstruct a stream track and does not add a live LMC tide to an equilibrium inference.

Allowing just the census, speed and Pal 5 strength to move jointly by w times their individual printed widths gives a conservative necessary condition on a spherical halo. To maximize S, minimize v for a given w and maximize over the permissible endpoints in f (S is affine in f at fixed v²). Invert this 1D condition. The threshold w=1.079 is **not a 1.079-sigma exclusion**: there is no joint covariance, no selection model and no assertion that this necessary condition is sufficient. It shows precisely why the small shell tension alone would be weak evidence.
