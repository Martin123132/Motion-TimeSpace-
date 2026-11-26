> Public reading copy: local links are mapped to released material or marked unavailable. Machine-specific passages, where present, have been omitted. See the inventory for the original digest.

# A signed, fixed-occupation test of the three-lobed LMC wave
       
Start with the two prepared, real axisymmetric ground states of the saved Schrödinger–Poisson branch. The host is stationary in this calculation; the applied satellite tide is not. Use the archived six alternatives and the same force intervals and units as the two-lobed calculation (not bundled here). No sky force determines the initial state. This is an azimuthal order, **not** a single spherical multipole: for m=3 and even reflection in z the allowed degrees are 3,5,7,…. Multiplying a ground of maximum degree L by a trial wave of maximum degree L+3 requires incident degrees through 2L+3, here 39 and 71. Orthogonality in azimuth gives zero first-order change in total occupation without requiring a new normalization. Azimuthally uniform timing shifts and uniform accelerations cannot drive m=3 at linear order.
       
## From the external potential to the measured signs
       
Write the real external potential as the sum of complex azimuthal harmonics paired with their conjugates. The incoming +3 projection uses exp(−3iφ). The translated native satellite field includes all its own archived degrees 0–6, not merely its intrinsic m=3 component: even a displaced spherical satellite can drive a three-lobed response about the host centre. Integrate the translated source in a frame aligned with the satellite-centre displacement, split radial integration at each native knot, retain both cosine and sine quadratures, and compute the force on the earlier negative-x observing meridian (not bundled here). An m=2 test by itself cannot distinguish the positive and negative x axes; an odd m can.
       
Let H be the stationary wave Hessian, Lp the positive Poisson operator with vacuum exterior matching, B multiplication by the ground, and M=H−2 B Lp⁻¹ Bᵀ. All these matrices carry the new azimuthal order in their angular kinetic, gravity and overlap terms. For the summed conjugate displacement d and its momentum p in the original time units, linearizing the pair gives
       
    d′ = H p,     p′ = −M d − 2 F(t),     F = project_m(g Vsat) / v_unit².
       
The no-added-wave solution starts with d=p=0. In H⁻¹-orthonormal modes vⱼ satisfying M vⱼ=σⱼ² H⁻¹vⱼ, d=Σ vⱼ cⱼ, with
       
    cⱼ(T) = −2 ∫ [sin(σⱼ(T−t))/σⱼ] vⱼᵀ F(t) dt.
       
We integrate the original local quartic time interpolant against the oscillator kernel, not an instantaneous equilibrium. The density's +3 coefficient is proportional to the ground times d, with the conjugate coefficient supplied once by reality. If S maps this product through Poisson to the northern spherical radial and polar components, the real field is 2 Re[exp(3iφ) S d]. At φ=π it is **−2 Re(Sd)**; at the mirror in z, only its polar component changes sign. Do not reflect the nonsymmetric direct satellite force. The old subtotal already contains the stationary host, direct tide, m=0 and **all** retained m=2; m=3 is added once. Static NFW receives no fictitious wave. Units for every signed force table are 10⁻¹⁰ m/s². There is no fitted orientation or incoming free wave.
       
## Can a better shape at the same available excitation do it?
       
For the new complex sector, E=(d† M d+p† H p)/2 is the dimensionless perturbation energy in the inherited normalization. After subtracting the instantaneous static displacement −2 M⁻¹F, use the energy norm and the fact that free propagation preserves it. If M≥λI on the **full discrete sector**,
       
    E(T) ≤ 2 [‖F(t₀)‖ + ‖F(T)‖ + TV(F)]² / λ.
       
The positive-shift test uses the Schur complement of the full, gravity-augmented stiffness with checked symmetric factorization and positive pivots. The total variation on each time panel is bounded above by the sum of distances between adjacent vector Bernstein controls of the quartic: its derivative is a convex combination of those increments times four. This bounds all modes of that spatial grid, not just the detected or propagated modes. It is a numerical certificate on represented inputs, not a theorem for every possible interpolant of unmeasured satellite motion.
       
Take the original four-component signed witness w from before this calculation. Let b be the least projection demanded after removing the stationary and direct field. For m=0,2 denote the verified old force supports by √(E₀ n₀), √(E₂ n₂). For the full complex m=3 sector, define n₃=8 wᵀ S M⁻¹ Sᵀ w. Cauchy–Schwarz then gives
       
    w·a_driven ≤ √(E₀ n₀) + √(E₂ n₂) + √(E₃ n₃) = U,
       
using the three separate energy ceilings. The sign at the observing meridian changes the predicted force but not this upper bound. If b>U, the **three sectors together** cannot reach the signed requirements with the represented satellite input starting from rest. This remains a meaningful test if the unused hemispheric odd part is allowed to repair the north–south differences for free: in that case use the earlier even average interval, not a reflected copy of the northern observation. It does not give a bound on the untested even-in-height m=1 or higher azimuthal sectors.
       
For an independent incoming free oscillation, linear superposition plus Cauchy–Schwarz gives a necessary preparation budget:
       
    E_free,0+E_free,2+E_free,3 ≥ max(b−U,0)² / (n₀+n₂+n₃).
       
This uses the conserved positive **free** energy, so it constrains initial preparation as well as the endpoint, even for phases optimally aligned with the tide. It is a lower bound, not a fitted initial state, particle count, unique population, or conversion into orbital energy.
       
## Reproduction
       
From this folder with the retained Python and NumPy/SciPy: build the small projection library with `build.cmd`. Run `python -B sources.py control`, `python -B sources.py`, `python -B evolution.py`, then `python -B complete.py`. The complete-degree challenge uses a separate 48-node quadrature on the nested radial grid, with four and eight time subdivisions; it never substitutes the reduced propagated energy for an upper bound. Spatial grid, initial occupations, comparison bands and tolerances are inherited. `python -B field_check.py` independently differentiates the reconstructed density potential at both meridians and checks a wider finite domain. `python -B refine.py midpoints` and `python -B refine.py` test fresh physical half-steps and larger trial spaces. Runs are single-threaded, local and keep their own output separate.
