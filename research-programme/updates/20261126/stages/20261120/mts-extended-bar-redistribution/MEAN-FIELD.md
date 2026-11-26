> Public reading copy: local links are mapped to released material or marked unavailable. Machine-specific passages, where present, have been omitted. See the inventory for the original digest.

# Derived forcing for the next fixed-occupation calculation

The sky sees the full bar. The axisymmetric part of the stationary wave sees only its azimuthal mean. Write that mean as Δρ₀(R,z) = Σ_i a_i B_i(R)[p_i(z)−Σ_j f_j(R)p_j(z)], where f_j are the proportional donor fractions in the actual admissible source. Since each profile integrates to one, ∫dz Δρ₀(R,z)=0 **at every radius**. Were the heights unchanged as well, an azimuth-only reallocation would leave the axisymmetric ordinary potential exactly unchanged. One must not drive the mean wave with the full near-side bar force or add another monopole. Even with the height change, the total mass perturbation and dipole vanish.

For the exterior axisymmetric moments in the usual Legendre convention, Q_l=∫r^l P_l(z/r)Δρ₀ d³x. The ring constraint cancels the terms depending only on R:

    Q₂ = ∫ 2πR dR Σ_i a_i B_i [⟨z²⟩_i − ⟨z²⟩_donor]
    Q₄ = ∫ 2πR dR Σ_i a_i B_i [Δ⟨z⁴⟩ − 3R² Δ⟨z²⟩].

For a normalized two-sided exponential the two moments are 2h² and 24h⁴. For sech²(z/h)/(2h) they are π²h²/12 and 7π⁴h⁴/240. The original donors use the saved tabulated heights and the analytic moments of their exponential tails, not a replacement thin-disk approximation.

**Check before re-solving.** For the source-admissible whole-disk S22 transfer (0.4), ΔQ₂ = **−5.62103×10⁸ M☉ kpc²** and ΔQ₄ = **+1.17565×10¹⁰ M☉ kpc⁴**. It flattens the vertically averaged mass distribution in the quadrupole sense. On the north axis the independently integrated change in ordinary potential at 50, 100 and 200 kpc is +0.01918053, +0.00241252 and +0.00030204 (km/s)². The two predicted terms −G(Q₂/r³+Q₄/r⁵) miss by 9.67×10⁻⁵, 6.06×10⁻⁶ and 3.79×10⁻⁷ relative: the omitted relative term falls about sixteenfold per doubling as expected. These are large-radius checks, not a multipole approximation at 6 kpc. The localized height distributions have tails; no infinite series convergence outside a compact support is presumed. Saved control (not bundled here).

**Use in the parent equation.** Build δΦ_ord,0 from this signed density with the same Poisson normalization and matching as the E3 ground, check the polar far-field moments above, and project δΦ_ord,0 g onto the fixed-number tangent space of each saved wave ground. Solve the self-gravitating tangent equation there (including its induced potential), or re-solve the finite source with exactly the old norm. Check a small-amplitude central difference against that tangent before interpreting the finite 0.4 result. The aspherical remainder of the *ordinary* field contributes directly at the probe. A changing rotating source can also induce nonaxisymmetric wave modes; this far-field calculation supplies neither their amplitude nor their initial state. Compare the final predicted force with the [residual metric target](evidence-001.zip) (archive member: `metric-residual-contract.csv`), not vice versa.
