# How a slowly varying source enters the finite-speed tidal prediction

This auxiliary calculation is distinct from the prospective frozen-source comparison. The source is the spatial tensor stress of the independently evolved Newton preparation, not an inversion of the curved detector. It tests the *linear mechanical tensor particular solution*, not scalar feedback or arbitrary free radiation.

For an ordinary tensor perturbation h on the homogeneous common metric, let ξ be the background conformal time from launch, b=a/a★, u=√q ξ, and A=−r⁻⁶∂ᵣ(r⁶∂ᵣ) on the regular radial TT quadrupole. The linear tensor equation in the existing source units is

    hᵤᵤ + 2 Hᵤ hᵤ + A h = 2 S(ξ)/q²,       Hᵤ = (d ln b/dξ)/√q .

Here S includes the conformal background density proportional to b⁻¹, the matter velocity products, and the additional wave density-gradient term with coefficient 1/(4 a²m²). These are stresses on the common Newton history, not the total source of the full Einstein equations. The trace's normal-frame background and initial velocities are anchored to the original native inputs. The code also evolves both signed clouds and the zero preparation at the changing scale factor. It does not infer the local wave occupation from the resulting force.

Take h and hᵤ initially zero for this particular term only; independent free gravitational data are not thereby ruled out. Set X=q² h/2 and Y=b X. Then

    Yᵤᵤ + A Y = b S + (bᵤᵤ/b)Y .

For a freely falling infinitesimal separation with physical length proportional to b(1+h/2), the anisotropic proper relative acceleration is proportional to (hᵤᵤ+Hᵤhᵤ)/(2 b²). After applying the unchanged signed aperture, the normalized increment in this component is

    [ b⁻² ⟨W_b, S−A X−Hᵤ Xᵤ⟩ − ⟨W_1,S(0)⟩ ]/q,
      W_b(r)=b W(br),  X=Y/b,  Xᵤ=Yᵤ/b−Hᵤ X.

A homogeneous expansion rate alone cannot be counted as anisotropic tidal response. Moving W is necessary for a fixed proper aperture. This formula does not model quadratic metric corrections or the change of the local physical ruler due to the signed clouds.

**Independent error controls.** On each time panel integrate the spectral cosine/sine Green functions against an affine forcing exactly, treating bᵤᵤY/b at both ends consistently (one scalar denominator per mode). At zero eigenfrequency the position weights are 1/2 and 1/6; do not divide by zero or discard a constant mode in a time-dependent source. A constant source and unit scale factor must reproduce the independent frozen wave experiment. A ramp source at finite frequency has an exact closed-form solution. A uniform mode at b=1+αu, driven by S=1+2αu/b, has X=u²/2 even with expansion and is a separate check. Temporal and spatial refinements, and the same evolution with the source, expansion or proper clock held fixed, distinguish a changing source from a propagation or clock effect. All methods use the same normalization and keep the original frozen forecast intact.

**Conditional analytic bound.** For b=1, Duhamel and one integration by parts give, on the same zero-free-wave initial data,

    q ΔE(τ) = ⟨W,[cos(√A √q τ)−I]S(0)⟩
              + ∫ from 0 to τ of ⟨W,cos(√A √q (τ−s)) dS(s)⟩ .

Thus at a fixed physical clock the evolving-source contribution is at most ‖W‖* TV(S)/q. In the declared finite spatial model, a sharper bound is Σⱼ |Wⱼ| TV(Sⱼ)/q in the mass-orthonormal modes, with the variation over the actual time interval. A uniform finite variation plus finite initial source is sufficient for this *tensor term* to disappear in the Newton limit. Sampled history differences bound the variation of their specified affine interpolant, not of every continuum trajectory through those points. This argument neither bounds an unspecified incoming wave nor derives an arbitrary galaxy's initial state.

