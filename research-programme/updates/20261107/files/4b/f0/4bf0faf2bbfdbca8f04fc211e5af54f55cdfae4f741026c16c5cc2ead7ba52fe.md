# Angular refinement of the combined source

At fixed incoming event, histories, spectral domain and radial rules, replace
only the quadrature of the real soft direction and the virtual bath-cut
direction. Reuse the Stage236 exact amplitude/statistical integrand unchanged.
New real grids are candidates, not edits of the retained scattering bank.

For a virtual ray, retain the source-owned decomposition

    A_r = C0_r I0_r + sum_p Cp_r Ip_r.

Hard unpolarized interference is a real-linear functional:

    kappa_r = 2 Re sum(conj(M0) A_r) / sum(abs(M0)^2).

Thus scalar-intensity response coefficients can be contracted with the exact
tree before the spectral moments are applied. Keep complex coefficients and
the absorptive pole signs; taking their real part before multiplying Ip is
not equivalent. Directional Dirac tensors are retained for provenance and
future polarization use. The scalar shortcut must replay the old full-tensor
Mueller intensity map at the original eight rays.

Recalculate the Planck thermal scalar K0 for each candidate angular rule.
The vacuum term is unchanged. With B the actual saved background and W the
perturbation, the mixed virtual block remains

    Jv = (weight/2) [K0 Jmixed + delta_kappa_B Jequilibrium
                   + Dlinear_B L (kappa_wave,0gas)^T/(2l+1)].

Update the first term by the candidate-minus-original thermal scalar; rebuild
both medium terms with the candidate angular spectral map. Keep lab-frame
angular features and independent gas recoil. The state block is unchanged:
its scalar pole-mass functional has an exact angular reduction already proved
and tested in Stage235, rather than an untested finite-ray approximation.

For each angular rule report separately

    baseline = real_leading,
    MTS_correction = real_difference + virtual + state,
    combined = baseline + MTS_correction.

This baseline is the retained leading real-process control in this collision
sector, not an independently refitted cosmological model. Original-to-final
differences and successive angular refinements answer different questions.
Matrix norms are numerical diagnostics in the retained coordinates; eventual
wave/gravity response must still use the physical source and response norms.
