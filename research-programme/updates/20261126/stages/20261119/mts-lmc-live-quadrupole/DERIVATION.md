# Quadrupole response without counting the trapped wave twice

Use the inherited mass-weighted radial fields. For m=2 define the complex density displacement d=a₊+a₋* and p=H⁻¹ d′. Here H is the sector wave Hamiltonian measured from the ground chemical potential, L the positive Poisson matrix with exterior vacuum matching, and B the ground–potential multiplication. The quadratic positive stiffness on the spatial mesh is M=H−2 B L⁻¹ Bᵀ. Linearizing the two conjugate Schrödinger equations and eliminating gravity gives

    d′=Hp,       p′=−Md−2F,       F=g V₂ (projected and in ground velocity units).

A uniform acceleration has no m=2 projection. Angular integration of the first-order density vanishes in this sector, so no background occupation is changed. The complex Fourier convention is V₂ ∝ ∫exp(−2iφ) V dφ. Translation uses the archive’s complete l≤6 satellite potential. In a frame aligned to its Galactocentric position, the target and translated source share an azimuth. Integrate their cosine and sine terms up to azimuthal order six; integrate the remaining polar angle with distance as variable, splitting at the satellite's radial knots. The rotation coefficients are determined by exact Fourier extraction for these bandlimited angular functions (64 azimuths, host l≤48). At the probe φ=π the reality partner contributes a factor two, not an azimuthal RMS. At mirrored heights z, radial and azimuthal are even, polar odd. This parity applies only to the new wave, not to the earlier direct satellite force.

For an H⁻¹-normalized displacement eigenvector vⱼ, M vⱼ=σⱼ² H⁻¹ vⱼ, and d=Σ vⱼ cⱼ. Each complex cⱼ obeys cⱼ′′+σⱼ² cⱼ=−2 vⱼᵀ F. We evolve both real components against the exact oscillator kernel for a local quartic representation of the source. The finite radial trial spaces include the old v₁ and H⁻¹v₁ and independent static and shifted force readouts. Reconstruct the *entire* m=2 field, project out c₁ from the sum, and add only j>1 to the previous sky subtotal. Compare c₁, c₁′ and the complex forcing to the old independently transformed tidal histories. The original m=0 and direct LMC forces are never reapplied.

## Sharp force requirement and a conservative external ceiling

For the real radial and polar readings at φ=π, let S map the mass-weighted displacement to the single complex-harmonic accelerations on the north probes. The physical readings are 2 S Re(d). Normalize the free excitation energy as E=(d†Md+p†Hp)/2. Its minimum for four prescribed additional readings b, with v₁ absent, is bᵀG⁻¹b/2 where

    G = 4 S [M⁻¹ − v₁ v₁ᵀ/σ₁²] Sᵀ.

This is the full finite spatial mesh's inverse, not the inverse of a truncated set of propagated modes. The positive matrix and its inverse are accessed through the joint wave–Poisson system. Minimize over the original signed hemisphere bands by active faces and check feasibility and the dual signs. In the strict test, north/south requirements must intersect after applying parity; a separate conservative test lets an arbitrary reflection-odd field cover the hemispheric difference at zero cost. Ratios use the same complex-amplitude energy normalization throughout.

For initially unperturbed remaining waves, set F⊥=F−(H⁻¹v₁)(v₁ᵀF). The moving static equilibrium is dₑ=−2 M⁻¹ F⊥. Free evolution preserves the energy norm of (d,p). Shift by (dₑ,0), apply the triangle inequality to the initial shift, the variation of the shift during evolution, and the final shift. On the full mesh, irrespective of the number of modes resolved in time,

    √(2 E_final) ≤ 2 [ ||F⊥(start)||_* + ||F⊥(end)||_* + ∫||F⊥′||_* dt ],
    ||h||_*² = h† M⁻¹ h.

For each local quartic curve with Bernstein control vectors b₀,…,b₄, its derivative is a convex combination of forward differences multiplied by 4/Δt. Its integrated norm is at most Σ||bⱼ₊₁−bⱼ||_*; bins avoid archived shape breaks. This is a bound for the represented source, not an observational uncertainty or an upper bound on arbitrary free incoming waves. It intentionally discards phase cancellation. If the ceiling exceeds the minimum it is inconclusive, never evidence for a fit.

To bound the dual norm without thousands of full sparse solves, choose an orthonormal source span Q from input histories only, set a=Qᵀh, r=h−Qa, W=M⁻¹Q. Then ||h||_*² equals a†(QᵀW)a+2 Re[(Wa)†r]+r†M⁻¹r. A positive shift M−λI certified by symmetric factorization of its gravity-augmented system puts the last term between 0 and ||r||²/λ. Include both complex quadratures. This controls the contribution **outside** the source span and the propagated wave basis on this mesh. Direct solves on additional epochs check the enclosure. No target force is used to estimate the externally available energy.
