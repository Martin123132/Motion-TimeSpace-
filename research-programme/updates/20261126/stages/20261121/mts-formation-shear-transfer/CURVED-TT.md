> Public reading copy: local links are mapped to released material or marked unavailable. Machine-specific passages, where present, have been omitted. See the inventory for the original digest.

# A curved-slice continuation with a nonzero, calculable curvature source

Use a spherically symmetric spatial metric dρ²+B(ρ)²dΩ², with ρ proper radial distance. Keep the same tensor harmonic and the same orthonormal amplitudes as in [the flat calculation](TENSOR-CHANNEL.md). Angular derivatives are those on the unit sphere. The divergence of the trace-free tensor has radial coefficient 2 ∂ρL +(4L−4b) B′/B −6v/B and tangential coefficient ∂ρv +[3B′v+2b−2d]/B. Consequently an arbitrary regular radial amplitude defines a transverse-traceless spatial tensor by

    b=−L/2,       v=B L′/3+B′L,       d=Bv′/2+3B′v/2−L/2 .

This is a *specific completion* of L, not a requirement that the actual matter or all metric perturbations be transverse-traceless. At linear order the scalar curvature variation is ∇ᵢ∇ⱼhⁱʲ−∇² tr(h)−Ric:h. Only the last term survives for a TT perturbation. With λr=−2B″/B and λt=(1−B′²−BB″)/B² the radial and tangential background Ricci eigenvalues, the result is

    δR⁽³⁾ = 2(λt−λr) L Y = 2 (1−B′²+BB″) L Y / B².

Constant-sectional-curvature backgrounds give zero, not so an arbitrary matter background. A smooth regular centre with B=ρ+aρ³+b₅ρ⁵+O(ρ⁷) has (1−B′²+BB″)/B²=(10b₅−3a²)ρ²+O(ρ⁴). Hence this *spatial curvature source* for regular bounded L starts at order ρ²; this derivation does not assume that the entire constrained solution or the numerical first-cell profile vanishes.

As a separate check, differentiate the metric, inverse metric, Christoffel symbols and Ricci tensor directly at rational off-axis points in (ρ,cos θ,φ), once with B=ρ and once with B=ρ+ρ³/13+ρ⁵/37. The curved case has a nonzero answer. Also apply independent conformal perturbations with nonzero δR, without reusing the TT formula. [Twelve exact metric-variation cases](evidence-001.zip) (archive member: `curved-slice-tests.csv`).

For the actual saved spherical backgrounds, B=r exp(b₀) and dρ=exp(ℓ₀) dr. The coefficient 2(λt−λr) admits two calculations from the retained monopole geometry:

    −3X − R⁽³⁾/2,
    2e⁻²ℓ₀ [expm1(2(ℓ₀−b₀))/r² − ∂rℓ₀/r − (∂rb₀)(∂rℓ₀) + ∂r²b₀].

Here X is the radial eigenvalue of the spatial Einstein tensor. Compute the response from the measured ΔL profile for the **hypothetical curved TT completion**, adding the shared and signed parts as a product, then bound it by coefficient sup norms times profile norms. This is not an upper bound on the actual whole constraint: the non-TT part, extrinsic-curvature variation δ(K²−KᵢⱼKⁱʲ), and matter energy must be calculated separately. The clock forecasts and cutoff were not refit. The construction gives a concrete test for a future curved tensor evolution: predict its driven tidal field as well as its scalar constraint, rather than projecting away a mode because its continuum flat constraint vanishes.
