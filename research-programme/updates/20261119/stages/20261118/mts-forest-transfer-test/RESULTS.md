# Forest test: the retained heavy branch has a cutoff sharper than the calibrated simulations

The illustrative heavy preparation (about half the clustered matter, fixed field mass and primordial spectrum) has a real, testable problem of **scale dependence**. Its overall clustering amplitude is within the range of the published forest likelihood; its spectral slope is nowhere near that range at the reference scale. No absorption-data rejection or preference for this branch is inferred. Its parameters have not been changed.

## Where the difference is generated

At redshift 3 the reference velocity wavenumber 0.009 s/km corresponds to 0.708505/Mpc for both MTS backgrounds and 0.706450/Mpc for conventional ΛCDM. Direct logarithmic slopes of *total* linear matter power (including massive neutrinos):

| Fixed branch | σ8 today | d ln P / d ln k at its pivot |
|---|---:|---:|
| Conventional ΛCDM | 0.84221 | −2.29926 |
| All-cold, retained background | 0.82886 | −2.29990 |
| Retained mixed heavy | 0.82312 | **−7.16791** |

The release accepts slopes from −2.6 to −2.0 and σ8 from 0.5 to 1.5. Changing just the primordial amplitude multiplies the linear power and **cannot** repair its slope. At fixed all-cold slope, entry into the calibrated region would require the heavy/cold logarithmic power-ratio slope to be at least −0.30010 instead of −4.86801 (a shift of +4.56791). That is a requirement **for this emulator**, not an observational bound on how nature may behave.

The heavy solver rejected an attempted unsourced off-grid mode. Rather than turning off its guard, we evolved the early field at seven additional wavenumbers and projected its oscillations into matching density and momentum. Two original knots checked both projections to within 1.7e−7 relative; their late power replayed within 8.9e−8. Across the 40 earlier shared clustered-power predictions per branch the largest difference is 1.46e−7. At the heavy pivot, three centered differences and the independent coarse spline span −7.171 to −7.162; this resolution dependence cannot explain the failure.

At the **common comoving** pivot the heavy/cold power ratio goes from 0.31779 at z=3999 to 0.24794 at 1100, 0.22238 at 99 and 0.22002 at 3. The excess slope is already −4.82932 at 99 versus −4.86801 at 3. At z=3 the matter-gravity Jeans wavenumber is 4.858/Mpc; the heavy pressure coefficient relative to the matter-gravity coefficient at the pivot is just 0.000452. This is a coefficient comparison, not the ratio of the actual total forces. It explains why an early cutoff can survive with little *new* pressure at this scale. At higher wavenumbers evolution is not negligible: at k=1.981/Mpc the power ratio falls from 0.01926 at z=99 to 0.01363 at z=4.2; at k=5/Mpc, from 0.008834 to 0.001764. A single redshift-independent rescaling is not a demonstrated forest forward model.

## Independent simulation-grid obstruction

Using the actual 109 ABG, 83 ABD, eight thermal and one cold templates, we asked for the *best possible* normalized nonnegative mixture, not just a nearest-neighbour match. At z=0 the heavy/cold power ratio is 0.90273 at 0.3425/Mpc and 0.09838 at 0.83536/Mpc. Those two knots alone witness the impossibility of matching the cutoff accurately. Across trusted overlap the minimum achievable **maximum absolute power-ratio error** lies between 0.2272567 and 0.2272587. Against conventional ΛCDM the corresponding minimum is 0.21742; the cold/cold and ΛCDM/ΛCDM identity templates are exact. No assumptions about k>5/Mpc are required for the lower bounds. Comparing each knot separately would only prove a 0.02274 error and would miss the main effect. This is a simulation-library limitation, not a 22.7% observational discrepancy.

## Actual absorption controls

[Hooper et al.](https://arxiv.org/abs/2206.08188) and the [pinned MontePython release](https://github.com/brinckmann/montepython_public/tree/5b365b093982099b926a0c0c169697c9dc6cbbc4/montepython/likelihoods/Lya_abgd). Seventeen source/code/data assets, 13,914,101 bytes, matched upstream Git blob identities; local SHA-256, URLs and sizes in release.json. Downloaded actual observations, inverse covariances, astrophysical grid and hydro responses. Only HIRES (28 bins) plus MIKE (21); no XQ-100, no CMB combination and no claim of independent holdout. The observed powers are not ratios of matter spectra.

- Released reference flux: χ² = **57.9924** on 49 bins, HIRES 25.9220 + MIKE 32.0704; independently whitened. Recovered the same reference flux through the astrophysical interpolation. This is a pipeline check, not a fit.
- With the release's fiducial gas history, our conventional cosmology as an identity-transfer control gives **92.6684**. Matched all-cold gives **90.4176** as a *conditional* identity-transfer approximation. These are not best fits, a fitted comparison or a substitute for a dedicated hydro run in the retained expansion. Both use the same gas treatment. No inference from their score difference.
- In the published example parameter file the gas temperature-density slope evolves with exponent −1.93, whereas the code fallback is +1.93. The example gives fixed-control scores 103.69 and 103.65; the fallback leaves the supplied gas-slope scaling range in at least one bin and is diagnostic only. None of these choices affects the heavy slope veto.
- **No χ² for heavy MTS.** Do not clip its slope, fit it to the grid, interpret a solver boundary value as a data exclusion, or use the reference score as its own.

**Next test:** initialize the same linear gravitational calculation at z=99 with the actual species densities *and velocities*. Propagate the heavy field with and without its dispersive pressure, holding initial perturbations, matter abundance and background fixed. Compare gravitational forcing and baryon response across k=0.34–5/Mpc through the forest epochs, with a true all-cold and solver-resolution control. This tests whether a pressureless particle simulation with the correct initial transfer can be used at any of those scales, or whether an explicit wave calculation is necessary. Even a linear pass would still need a nonlinear gas/absorption calibration against the observed flux.

