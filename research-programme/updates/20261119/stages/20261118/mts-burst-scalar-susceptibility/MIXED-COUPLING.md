# Resolving the discrepancy instead of changing the tolerance

Within the tested two-current subspace write the ruler as L(z,v)=vᵀK(z)v, the two early magnetic readings as D(z)v=d, and z=A². Define u(z)=(v(z)−v₀)/z and u₀=−D₀⁻¹D'₀v₀. Relative to the leading magnetic-matched scalar susceptibility, the exact finite excess per z is

    [L(z,v(z))−L(0,v₀)]/z − S_matched
    = {[L(z,v₀)−L(0,v₀)]/z − S_fixed}
      + 2[u(z)−u₀]ᵀ K₀ v₀
      + 2u(z)ᵀ[K(z)−K₀]v₀
      + z u(z)ᵀ K(z) u(z).

This splits a nonlinear discrepancy into four distinct contributions. It uses the ordinary and scalar solutions for the two fixed unit currents and their known opposing mixture via polarization, not coefficients fitted to the late discrepancy. The archived directly evolved full calibrated ruler supplies an independent left-hand side. Assess closure on the **remainder itself** as well as on the larger scalar signal.

**Additional zero-amplitude prediction.** Differentiate the same evolving equations for each unit current, giving K'₀ by polarization and D'₀ directly from the two early field readings. From D(z)v(z)=d the part of the z² weight correction caused by changing source identification in a changing magnetic map is w_mix=−D₀⁻¹D'₀u₀. Thus the explicit mixed part of the A⁴ ruler coefficient is

    C_mix=2u₀ᵀK'₀v₀ + u₀ᵀK₀u₀ + 2w_mixᵀK₀v₀.

Predict the correction as z S_matched+z² C_mix. This is **not the entire fourth-order prediction**: with K₂ and D₂ denoting half the pure second z derivatives, the missing terms are v₀ᵀK₂v₀−2(D₀⁻¹D₂v₀)ᵀK₀v₀. They represent intrinsic curvature of the fixed-current gravity and magnetic responses. In contrast C_mix is completely fixed at zero, uses neither finite-amplitude waveforms nor the measured discrepancy, and requires no extra coupling. Perform the two new derivative solves on the original coarse grid; compare its prediction against both archived full and newly executed smaller-amplitude tests. This diagnostic was motivated by the disclosed full-arm remainder, not selected on a genuinely held-out dataset.
