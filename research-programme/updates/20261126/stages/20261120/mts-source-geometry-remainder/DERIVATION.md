# A prediction from the initial mass and geometry, not the final tide

**Scope.** Use the previous positive-quadratic, minimally coupled massive wave (or its matched dust control), in the local Gaussian proper-time frame, on the same signed cloud preparations. This is an initial-value calculation inside that classical theory. It does not determine its gravitational constant or a galaxy's occupation. Factors of the launch scale factor and the chosen gravitational-density units are already in the prior operators. All absolute tides are in launch-conformal Mpc⁻²; ppm below refers to the *signed Newtonian secular change*, not to the entire background gravitational field.

### Eliminate the rapid normal variable from the mass flux

Let the complex logarithmic wave be L and its rest-frequency-subtracted normal momentum be z; k is the trace of the extrinsic curvature. In the inherited time units the equations are

    L' = k/2 + μ z
    z' = 2iμ z + [ΔL + (∇L)² − k'/2 + k²/4]/μ − μ z².

The square here is bilinear, not an absolute square. Write A = ρ★ exp(2 Re L), b = Im z and ρw = A(1−b), the time component of the conserved wave number current times the mass. Taking the imaginary part and differentiating the density cancels both terms proportional to μ Re z (including the product with b):

    ρw' = k ρw − A Im[ΔL + (∇L)²]/μ
         = k ρw − div[A ∇ Im L / μ]     (continuum).

The implemented first line uses the inherited discrete radial Laplacian and gradient separately; the continuum product rule is not imposed on a finite mesh. This identity preserves the nonzero mass flux, rather than discarding the normal mode by averaging. It is checked against the unsimplified derivative in both harmonics around the detector. For dust species j, ρj = ρ★j n_j exp(−ell−2B), where n_j is the conserved coordinate number and (ell+2B)'=−k. Hence ρj' = kρj + ρ★j exp(−ell−2B)n_j'. The staggered-face dust current gives n_j'. These formulas separate compression from transport without a new coupling.

### The same mass, surface and ruler as the comparison

After excluding local kinetic/spatial stress and the surrounding matter's explicit tide, the retained Gauss readout is

    C = −(Σρj + ρw)/3 + (R_surface − κ²/2)/2 + (k/3 − σr/2)².

R_surface is the scalar curvature of the coordinate two-surface, κ its spatial mean curvature, and σr the radial shear. This is a scalar tidal *component in the specified frame*, not a generic stress-free field equation. Differentiate the two geometry terms with the metric and extrinsic evolution. On a diagonal test geometry with log areal factor B and quadrupole Q, the intrinsic half-gap can independently be formed as [exp(−2B)(1−ΔΩB) − exp(−2ell)(1+r∂r B)²]/r² through first order in Q. The independent complex-amplitude check includes a nonzero angular mode. For the real clouds the full expressions also include tilt and angular metric shear.

Integrate the quadrupole over the two compact proper-distance windows from the archived test. Differentiating the measurement includes both change of the fields and change of radial proper length at fixed detector position; a coordinate window would not give this test. Integrate the rate *before* subtracting signed hosts, unhosted controls and pressure switches. No endpoint subtraction of the large absolute tidal fields.

### Predict from preparation

The prepared 120-Mpc constraint solution supplies the incoming quadrupole and common-metric momenta; the six-unit propagation domain does not replace it with an isolated source. The incoming stress is frozen at launch, but the surrounding *density and flux* respond through their original local conservation equations. Its launch value, normal graph, pressure and derivatives are supplied by the prior preparation, not inferred from the tidal target. The separate global-constraint test starts from the formation-stage inputs, reconstructs the wave normal graph with the Hamiltonian and momentum sources and evaluates the first analytic response without reading any archived tide. Twenty launch quantities per full case are then compared to the archived inputs. The diagnostic source deletions affect the **added normal-graph corrections** in the constraints, not all gravitating density or all momentum. The homogeneous expansion change and subsequent coupled dynamics are kept identical in prescription.

For an initial state Y★ with slope F★ and constant incident stress, define the increment u. The exactly integrable linear block A has A[L,z]=μ and A[z,z]=iω with ω=2μ; it is zero for the dust preparation. Set u₀=0 and construct successive causal source integrals:

    S_j(s) = F(Y★ + u_j(s)) − A u_j(s)
    u_{j+1}(s) = ∫₀ˢ exp[(s−v)A] S_j(v) dv.

In particular, all slow components of u₁ are just s F★. For the wave, Q(s)=expm1(iωs)/(iω) gives u₁,z = Q F★z and u₁,L = s F★L + (Q−s)F★z/(2i). This first estimate needs **one set of launch slopes**, not a measured field history. When reading the tide we evaluate its physical rate at the predicted fields (a source-rate approximation, not an assertion that a truncated trajectory is exact). Four further levels including this first return were specified in advance. The full higher levels are a new approximate solution of the *same* field equations, not independent theoretical evidence. Causal integrals interpolate the smooth source in Chebyshev polynomials; Gauss quadrature integrates the exposed fast phase against those sources. Constant, linear and quadratic drives have an analytic integral for comparison.

### What is and isn't a prediction

The GR-side forecast uses no archived evolved metric/tide. The rest and geometry **excesses** subtract the separately saved, matched Newtonian prediction (total and local rest/density parts). The summed excess is invariant to how that local Newtonian split is allocated; the separately quoted pieces are conditional on this convention and on the fixed ruler/frame. A further comparison adds the preceding independently computed weak-field motion-stress forecast and the launch-stress surroundings forecast; neither is fitted to the combined answer. The two signs of one cloud and two overlapping rulers are controls, not four independent astronomical measurements. The inherited other curvature readout and pointwise disagreements are retained separately. Do not transfer sub-ppm reproducibility of one finite-mesh readout to continuum GR, to the LMC force bands, or to an empirical test.
