# From a collective-action limit to a bound on actual perturbation mass

The first (absolute-frequency-floor) bound in DERIVATION.md is valid on the tested stable discretizations but gives the sharp central spatial gradients of F excessive weight. A relative form inequality removes that weakness. With H and M as in DERIVATION.md, test the single fixed number η=1/2, without optimizing it:

    η H ≤ M = H−2 B L⁻¹ B† ≤ H.

The upper inequality uses the sign of attractive gravity and L>0; the lower is equivalent to positivity of the Schur block with (1−η)H, √2 B, and L. This second test includes all represented meridional directions for each harmonic, not only the lowest sampled eigenmode. The following implication is analytic; the operator inequalities for this galaxy are checked numerically on finite meshes.

Let C=H¹ᐟ² M H¹ᐟ². Then η H²≤C≤H². The positive square root is operator monotone; inversion reverses order. Consequently

    √η H ≤ C¹ᐟ² ≤ H,     H⁻¹ ≤ C⁻¹ᐟ² ≤ η⁻¹ᐟ² H⁻¹.

In the complete orthonormal oscillator basis the sum/integral of |⟨U,F⟩|²/σ is ⟨H¹ᐟ²F,C⁻¹ᐟ²H¹ᐟ²F⟩ ≤ ||F||²/√η. Restriction to the closed band can only lower this positive sum. Thus the closed collective action at switch-off is bounded by the frozen single-harmonic strength times [K_co²+K_counter²]/√η. This is stronger than using ⟨F,HF⟩/σ_min; it does not equate a dressed mode with a single-particle orbital.

For a reconstructed state (u,v), including one formed from only the closed spectral projector in the oscillator coordinates, its action and actual positive sideband norm are

    J = [⟨H⁻¹ᐟ²u,C¹ᐟ²H⁻¹ᐟ²u⟩ + ⟨H¹ᐟ²v,C⁻¹ᐟ²H¹ᐟ²v⟩]/2,
    N_side = (||u||²+||v||²)/2 = ||a||²+||b||².

The inequalities give J ≥ (√η||u||²+||v||²)/2 ≥ √η N_side. Combining both results bounds the *actual* mass norm of the reconstructed subthreshold component at **every subsequent unforced time**, with at most 1/η times the corresponding uniform frozen Fourier-strength bound. This is not obtained by treating oscillator action as particle number. It does not bound above-threshold response, the signed ground-density deformation, their interference in a local density, an incoming density matrix, or a pattern whose speed or source varies differently. At a single turn the absolute mass ceiling is loose; it becomes useful when a smooth pulse is long relative to the detuning. The asymptotic eighth power is an envelope for this sin⁴ family, not a universal law for real galaxies.

The relative-coercivity tables record the checked pivots and backward residuals for all sixteen m and both backgrounds. These are finite-precision matrix tests backed by a mesh comparison, not interval-arithmetic or an infinite-dimensional positivity proof.
