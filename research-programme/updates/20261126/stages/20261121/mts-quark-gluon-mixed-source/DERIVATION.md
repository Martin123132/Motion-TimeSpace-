> Public reading copy: local links are mapped to released material or marked unavailable. Machine-specific passages, where present, have been omitted. See the inventory for the original digest.

# The stress of the sea and the two currents

Write S=S_g−Σ_f log det D_f and W=−log∫exp(−S). Subscripts mean independent source derivatives h,p,k, including when momenta coincide. Expanding the **normalized** measure gives, with connected cumulants κ,

    W_hpk = <S_hpk> − cov(S_h,S_pk) − cov(S_p,S_hk) − cov(S_k,S_hp) + κ₃(S_h,S_p,S_k).

This follows from ∂<O>=<∂O>−cov(O,∂S). No stochastic or factorization assumption. On a translation-invariant measure every single-source mean at our nonzero wavevectors vanishes; all three legs together conserve momentum. Thus the covariances and third cumulant here are ordinary closed products (no conjugation on the designated Fourier legs). One cannot set the individual-configuration singles to zero just because their means vanish. This is why a fixed-background triangle, or the average of the full single-configuration derivative, does not suffice.

For R=D⁻¹ the third derivative of the negative log determinant is

    −Tr(R D_hpk)
    +Tr(R D_hp R D_k + R D_pk R D_h + R D_kh R D_p)
    −Tr(R D_h R D_p R D_k + R D_h R D_k R D_p).

The first two lines are contacts on a single quark loop. The first and second derivatives per flavor are −Tr(R D_i) and −Tr(R D_ij)+Tr(R D_i R D_j). Add the gluon stress to S_h before taking cumulants; the gluon action itself has no direct photon derivative in this regulator. Sum the sea flavors before forming products: different quark loops may carry different flavors.

**Finite action used.** Positive Euclidean weight. At spatial shear g_yy=eʰ, g_zz=e⁻ʰ the volume element is one. Take η=(0,0,−1,+1), w_μ=e^(η_μ h), b_μ=e^(η_μ h/2). In lattice units the Wilson matrix acts as

    D = m + Σμ [ w_μ (1−(T_μ+T_μ†)/2) + b_μ γ_μ (T_μ−T_μ†)/2 ].

The color link in T carries exp(i Q A_link); the reversed link carries its inverse. The determinant calculation at complex sources analytically continues the negative phase, **not** the conjugate of a complex source. Here h varies only in time, the time hopping coefficient is unchanged, and h commutes with the y,z hops; this shorthand is not an arbitrary-position curved spin-connection prescription. Plaquettes use S_g=βΣ(1−Re tr P/3)exp[(η_μ+η_ν)h_face]. At first h_face is the arithmetic mean of its four corners. Both the fermion and gluon stress are variations of specified actions, not stress ansätze independently adjusted to the two banks. Standard ingredients: [Wilson quarks with color and external EM links](https://doi.org/10.1103/PhysRevD.97.034505); [bare versus renormalized gauge anisotropy](https://arxiv.org/abs/hep-lat/9803010). Our metric interpolation and finite orbit measure are explicit control choices; no renormalized stress normalization is imported.

**Independent route.** The analytic calculation uses spatial momentum shifts and temporal inverse blocks. The direct code assembles in coordinate time and x, sums four transverse sectors, and varies finite actions including both determinants and the glue. On a normalized orbit measure W_hpk=−Z_hpk/Z at these momenta. The coefficient of the triple variation in each configuration's density ratio is unchanged under translating that configuration (q+p+k=0), and is even under simultaneous reversal of both photon sources. This allows a single orbit representative in the numerical density-ratio difference, not in arbitrary lower derivatives. Independently for n=0 we sum the eight translated real-source partition weights **before taking their logarithm**. Translation by four sites includes the opposite photon field at the same real shear. A cosine/sine shear against two cosine currents gives respectively Re/Im of the plane-wave answer divided by four. Periodicity and the time extent exclude other signed triples. Tested finite color and electromagnetic gauge transformations, charge conjugation, longitudinal replacement of either photon, neutral matter, and interchange of photon insertions. Time reversal was not enforced on the three chosen histories, so the unaveraged-with-reflections response can be complex; a reflection pair would select its real part. Neither component is a physical vacuum measurement.

## Which disconnected terms really vanish?

For isospin-symmetric u,d and strange, take the same mass-additive Wilson operator for each, no dynamical QED, charges (2,−1,−1)/3. For a unit-charge single-current loop J_i=−Tr(R V_i), the physical flavor sum **on each configuration** is [J_i(m_l)−J_i(m_s)]/3. This familiar flavor cancellation is used in [physical-point disconnected HVP work](https://arxiv.org/abs/1512.09054). It survives differentiating the conditional loop in a common metric. In particular B_hi=−Tr(R V_hi)+Tr(R V_h R V_i) is a one-current loop, not a two-current loop. Set Δ=m_s−m_l, C=R_l R_s. The exact resolvent identity R_l−R_s=Δ C yields the stripped differences:

    (J_i(l)−J_i(s))/Δ = −Tr(C V_i),
    (B_hi(l)−B_hi(s))/Δ = −Tr(C V_hi)
                      +Tr(C V_h R_l V_i + R_s V_h C V_i).

In the two covariances with *separate* currents and in the third cumulant, both current factors therefore carry Δ/3. This group is exactly Δ²/9 times the corresponding cumulants of the stripped operators. That factorization holds even if the normalized sea measure itself depends on mass. A quadratic leading law near degeneracy requires finite resolvents and moments; the prefactor need not stay small at the physical masses or in a different order of chiral/volume limits. **The covariance of total stress with a two-current loop survives the equal-mass limit**: its photon charges are squared, not summed linearly. Heavy flavors, isospin breaking, or changing the mass dependence of the lattice action require their own version of the identity. This is not a bound on the whole QCD coupling.

An additional 5×3×2×2 background has different, noncommuting SU(3) links at every site. No Fourier block reduction in its inverse. Both nonzero-spatial-momentum single-current loops are active here. Eight splittings including zero compare explicit charge-weighted traces with the divided resolvent formula. At equal masses the separate-current contribution vanishes even though the magnitude of the stress/two-current product is 0.10951 per site on this fixture. At Δ=0.005 the analytic zero-splitting coefficient predicts the stripped result to 0.50%, without fitting that coefficient. See numbers (not bundled here); magnitudes are in lattice units, not vacuum coefficients.
