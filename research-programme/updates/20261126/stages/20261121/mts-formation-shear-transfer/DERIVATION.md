> Public reading copy: local links are mapped to released material or marked unavailable. Machine-specific passages, where present, have been omitted. See the inventory for the original digest.

# What changing the angular shear flux can and cannot change

The matched preparation, wave and cold sources, earlier Newton-plus-propagating-stress forecast, proper apertures and all tolerances are fixed. Only the difference operator for the angular increment L is changed: A_p L = r⁻⁶ D_back,p [r_f⁶ D_face,p L]. The rest of the angular curvature, the mass chart, material source, initial spatial Ricci tensor and both original observers are unchanged. This is a candidate change to the numerical representation of the same retained common-metric field equations, not a new force or an alteration to a matter coupling.

## Central accuracy versus energy

For an even smooth L the regular continuum operator is L″+6L′/r. At the innermost cell r=h/2, the flux of a monomial rⁿ has degree n+5 before its final derivative. Using the actual staggered pair and both origin reflections gives an exact rational folded row h⁻² Σ wⱼ L((j+1/2)h). Its leading truncation errors, numerical minus continuum, are

    p=12:   −(343035/1024) h⁶ L⁽⁸⁾(0) + O(h⁸)
    p=20:   −(671357115/33554432) h¹⁴ L⁽¹⁶⁾(0) + O(h¹⁶).

These are local expansions assuming bounded higher derivatives of the same even physical profile as h decreases, not bounds on a numerical sequence with grid-scale features. The exact row has ℓ¹ norm 5,747.24 for order 12 and 16,714.46 for order 20 before dividing by h². A uniformly bounded independent sample perturbation can therefore have up to 2.91 times the worst-case gain. This ratio is a bound, not an observed physical amplification. Exact rows, monomial controls and an exact decomposition into centred second differences (the change starts at the fourth such difference) are in [the stencil calculation](evidence-001.zip) (archive member: `stencil.py`). High terms may cancel; the leading smooth moment alone does not describe an arbitrary saved state.

With reflecting boundaries and zero normal gradient at both endpoints, the staggered interior divergence is the negative adjoint of its matching gradient. Multiplication by h r⁶ and summation therefore gives

    h Σ r⁶ L A_p L = − h Σ r_f⁶ (D_face,p L)².

This forbids positive self-work for that isolated scalar spatial block. It does not bound a pointwise Hamiltonian or prove stability of the entire coupled evolution. At a fixed full state only the angular shear rate changes: ΔK̇_shear = −exp(−2ℓ₀) (A₂₀−A₁₂)L. The signed perturbation of the *product* includes shared-background factors; taking only the signed factor of L would not be exact. The full RHS is tested on each slot, for both stored and new trajectories, instead of assuming energy stability transfers to the constraint.

## An independently testable cancellation

In the flat linear geometry set the increments of trace, radial mass and polar chart variable to zero, but leave L(r) arbitrary. The continuum map to physical metric amplitudes on this one channel is

    b = −L/2,       v = L+rL′/3,       d = rv′/2+3v/2−L/2.

Substitution into the independently derived scalar curvature gives

    H = −4b″ + (4L′−12b′−12v′)/r + (16L+8b−24v+12d)/r²
      = 2L″+(10L′−6v′)/r + 6(L−v)/r² = 0.

For the pure shear velocity U=−δK_shear, the corresponding continuum momentum cancellation is −r[(v_U)′−(v_U)′]/2=0. These are statements about a specific angular channel, not all perturbed solutions, physical curvature tensors, or the curved matter system. This need not be a pure gauge mode. On the saved mesh, tilts are built on *faces*, then observed at *cells*. The corresponding two numerical derivatives need not commute. We decode only the measured change in L and U, using neither constraint as an input, and predict the change that the **unchanged independent physical observer** should report. We score the full signed fields including the innermost cell, core and bulk. No output is projected to zero; the difference from the forecast remains a diagnostic including other metric channels, curved-background and matter terms. See [separate-channel calculation](evidence-001.zip) (archive member: `null_channel.py`).

A second test avoids differentiating the physical metric samples altogether for the flat part of the Hamiltonian. Pair the observed physical angular fields with W=(1−r²/e²)⁶ on 0≤r≤e. Integration by parts puts derivatives on the *known test function*, giving the numerator

    ∫ [ (−4(rW)′+16W)L + (−4(r²W)″+12(rW)′+8W)b
        + (12(rW)′−24W)v + 12Wd ] dr.

Both endpoint terms vanish for regular fields and this window. We divide by ∫r²W dr. This uses the independently obtained four physical components, **not** the three functions reconstructed from L by assumption. For the curved result the separate full-minus-flat remainder is carried from the unchanged pointwise readout; it is not an independent weak solution of the entire curved problem. Compare linear and cubic interpolants, 8 and 16 nodes per cell, two meshes, and known nonzero test residuals before interpreting any cancellation. A small weak average does not certify the raw centre.

## Memory and time-step controls

At tick 960 subtract the original angular state from the continuously modified state, leaving the common evolving monopoles unchanged. In the retained linear angular sector this difference should then propagate with the modified **homogeneous** equations: the common preparation and surrounding angular drive cancel. Integrate that signal directly (no new added pulse) and compare to the independently saved full continuous minus late-switch endpoints. Repeat with half steps; separately propagate the full forced matched state at half steps for just this last interval. This distinguishes a change inherited from earlier history from the immediate effect of late forcing and from readout subtraction errors. It does not determine the time-step error of the first 960 ticks.

All diagnostics retain the original raw data. Numerical comparisons here refer to the saved conditional weak-field host-minus-zero, wave-minus-cold experiment, not to additional astronomical observations.
