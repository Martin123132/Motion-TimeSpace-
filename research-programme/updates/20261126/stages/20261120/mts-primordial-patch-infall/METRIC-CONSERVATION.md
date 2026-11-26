> Public reading copy: local links are mapped to released material or marked unavailable. Machine-specific passages, where present, have been omitted. See the inventory for the original digest.

# Which stress sources the Newtonian acceleration?

**Question.** Why did an independent small-amplitude Newtonian integration agree much less well with the archived heavy cosmology than with its paired cold branch? No force normalization, empirical offset, growth amplitude or time axis was adjusted.

Use a spatially flat scalar perturbation in the retained native synchronous chart. Prime denotes conformal time, ℋ=aH, ηk denotes k times the synchronous curvature. Write D, p, Q and Π for the total perturbed density, pressure, momentum and anisotropic stress in the native 8πGa² normalization; R and P are the similarly scaled homogeneous density and pressure. These are not the dimensionless comoving contrast D in the infall derivation. In the native flat constraints

    ℋ z = D/(2k) + kη,      (kη)' = Q/2,
    kα = z + 3Q/(2k²),      Φ = η − ℋα,
    k² W = −(D+3ℋQ/k+Π)/2,      Ψ_W = 2W−Φ.

A freely falling cold particle has θ_N=k²α and infers Ψ_E=α′+ℋα. Differentiate the constraints and eliminate D′ and Q′ using the *residuals*, without setting either to zero:

    E = D′+ℋ(D+3p)+kQ+kz(R+P),
    M = Q′+2ℋQ−k(p−2Π/3),
    k²(Ψ_E−Ψ_W) = E/(2ℋ)+3M/(2k).

This last equality uses ℋ²−ℋ′=(R+P)/2. If the background fails that equation, add kz[ℋ²−ℋ′−(R+P)/2]/ℋ. Thus equality of the two accelerations is a consequence of compatible stress evolution and constraints, not a second choice of Newton's constant. This is a conditional consistency identity of the retained weak-field equations, not an independent derivation of the microscopic matter action.

**Mechanism in this implementation.** In the saved native source (not bundled here), the late radiation replacement first computes z_m=(D_m/(2k)+kη)/ℋ using ordinary CDM, baryons and massive neutrinos. Heavy scalar perturbations arrive through the custom stress callback *after* the algebraic photon and massless-neutrino replacement. Their density is present in the final constraint for z, not in z_m. This is a mismatch when a component accounted for outside the native matter list clusters like matter. It is not a general objection to the [radiation streaming approximation](https://arxiv.org/abs/1104.2933).

For the truncated massless neutrinos, δ_r=4(D_m/k²+η), q_r=−4z_m/3, π_r=0. Photons have the same momentum, with the archived opacity correction in δ_γ. The source-side continuity defect is δ_i′+k(q_i+4z/3); the leading term from the missing heavy density is 2D_h/(3ℋ). After including the opposite baryon drag, the common radiation momentum defect is q_r′−kδ_r/3: the opacity term in δ_γ cancels the Thomson momentum term. Multiplying by the appropriate radiation densities gives the **signed** prediction in [constraint_residual.py](evidence-001.zip) (archive member: `constraint_residual.py`). To leading order k²(Ψ_E−Ψ_W)≈Ω_(γ+massless ν)D_h. Do not add this term when the radiation hierarchy is explicitly evolved.

**Decisive intervention.** The original matching table, compiled binary, expansion, primordial realization, mode selection, chronological output and accuracy settings were held fixed. Only DoLateRadTruncation changed. The time-evolution entry point sets its initial time from its batch's largest k: a first naive five-mode batch failed to reproduce the archive and was discarded. Each replay now includes the original chunk maximum and checks *all* original-column values for selected modes against the archive at rtol=2e−5, atol=1e−12 before comparison. Both the five preselected modes and the full 99-mode band were run both ways in both models. “Full hierarchy” here means the late radiation truncation is off, **not** that every hierarchy, discretization or massive-neutrino approximation was removed.

At z=10 the signed radiation residual accounts for the heavy acceleration discrepancy: 0.26792% before subtraction, 0.000813% after. The paired switch-off run returns 0.000740% using the wider derivative stencil. Across the four late times the radiation-subtracted original residual and the switch-off wider-stencil residual are each below 2e−5 in the weighted norm; narrower derivatives of the finite-precision outputs marginally exceed that line at two times. Independently integrating only the nonrelativistic linear density and momentum from each run's own z=99 data yields a final heavy contrast error of 0.00434% with truncation off versus 1.24458% on. The cold final errors are 0.00377% off and 0.00376% on. The reduced late error is not zero and is above the inherited 2e−5 target; the linear Newtonian model omits radiation perturbations, perturbations of massive neutrinos and other relativistic contributions.

**Scope for downstream uses.** For this same frozen primordial selector the native heavy z=0 linear contrast itself changes from 1.22363 to 1.25339, about +2.43%, and peculiar velocity from −19.8141 to −20.3003 km/s. These are formal linear values, not nonlinear galaxy contrasts. This matters for absolute growth, primordial state and any downstream claim sensitive to them. It does not by itself revise H(z), a survey fit, or an entire transfer grid outside these 99 modes. Keep the archived results intact; use explicit late radiation evolution as the reference for subsequent population or growth work on this branch.
