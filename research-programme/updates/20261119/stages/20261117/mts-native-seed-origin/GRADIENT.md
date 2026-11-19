# The gradient of the regular scalar mode, before comparing trajectories

Use the expanding flat branch, synchronous CDM rest frame and the regular adiabatic growing mode. Work to first order in the matter loading and separately in x²=(kτ)². At gradient order the background is pure radiation, photons are tightly coupled, neutrinos freely stream and are ultrarelativistic. R denotes their fractional radiation energy, including still-relativistic massive species. This is a calculation within the retained GR/matter limit. The radiation hierarchy is imported, not a new MTS law; cf. [Ma & Bertschinger, eqs. 21, 42, 51 and 96](https://arxiv.org/html/astro-ph/9506072v1). The scalar is the retained canonical MTS field with no independent isocurvature amplitude.

Normalize c=δ_c=C x²(1+b x²); hence h=-2c, with residual synchronous gauge modes removed. Write θ_j/k=C V_j x³, σ_ν=C S x² and V=(1-R)V_γ+R V_ν. Radiation momentum conservation gives 3V_γ=1/3 and 3V_ν=1/3-S. The Einstein momentum constraint gives η_x=2 C V x. The neutrino quadrupole equation gives 2S=-8/15+8V/5. Consequently S=-8/[3(15+4R)], and V=(15+12R)/[9(15+4R)]. This keeps the neutrino quadrupole while deriving the coefficient; setting the neutrino velocity equal to the photon velocity would lose its R dependence.

Radiation continuity integrates to δ_rad=4c/3-C V x⁴/3. The trace Einstein equation, c_xx+c_x/x=3 δ_rad/x², then gives 16b=4b-V, or

    b=-(5+4R)/[36(15+4R)].

The canonical scalar perturbation obeys δφ''+2Hδφ'+[k²+(am)²]δφ=c'φ'. With the regular radiation-era background velocity and the leading scalar normalization of the preceding stage, the gradient balance is 72e+1=84b. The field gradient coefficient relative to its leading τ⁶ term is e=(84b-1)/72. The velocity coefficient relative to its leading τ⁵ term is 4e/3. The +1 on the left comes from propagation of the scalar itself, not from the CDM forcing.

**Comparisons use the same normalization.** The retained native CDM seed includes -ωτ/5 but not b x². Relative to the original native scalar seed evaluated with that CDM, the first-order multipliers are 1-23ωτ/70+e x² (field) and 1-ωτ/3+(4e/3)x² (velocity). If a caller supplies CDM that ALREADY includes b x², subtract b from each gradient multiplier; do not count the density correction twice.

Test these frozen coefficients against the Hamiltonian constraint and an independently integrated radiation hierarchy with scalar wave propagation. Check pure fluid and pure free-streaming limits as well as both native compositions. Test the mixed matter-plus-gradient prediction at the retained mode start, including the native pre-table velocity convention. Report the error on the small correction, not just on the leading field. This is a short independent initial-mode calculation, not a new native CAMB run; the original table, tolerances and material checkpoint remain unchanged.
