# From galaxy velocities to a direct test of the common metric

The small-scale motion forecast improves individual mock galaxy velocities, but its full survey-power correction does not transfer consistently. The retained parent independently predicts a weak lensing spectrum from the metric. The difference attributable specifically to the heavy component is much smaller than the full difference from matched flat ΛCDM on the controlled angular scales.

## Frozen higher-redshift forecast

No new parameter fit. The six forecasts for all four catalogues at 0.5 ≤ z_obs < 0.6 were jointly locked before scoring. Redshift selection and central velocities are inputs; satellite velocity is not. A second reader denied access to every satellite velocity and reproduced the saved object ordering, galaxy types, host velocities, relative-flow fields, local scatter and leverage arrays exactly. This is a transfer within exposed Uchuu simulations, not four independent observational measurements. The two northern catalogues share 99.73% of families.

Primary mean absolute residual across monopole and quadrupole at 0.025 and 0.050 h/Mpc, in the estimator's sum-of-squared-weights normalization (smaller is better):

| Catalogue | Host only | Independent velocities | Pooled residual | Pooled + mean flow | Local scatter only | Mean flow + local scatter |
|---|---:|---:|---:|---:|---:|---:|
| South 0 | .01508 | .05507 | .04782 | .06276 | .05612 | .07114 |
| North 0 | .04141 | .03372 | .02728 | .03193 | .03575 | .04179 |
| South 1 | .03354 | .03467 | .02797 | .02725 | .03381 | .03420 |
| North 1 | .03985 | .03786 | .03138 | .03515 | .03973 | .04356 |

In both satellite classes in every catalogue, adding the predicted mean reduces the single-object velocity RMS; e.g. 532→501 km/s for matched hosts and 504→488 km/s for unmatched hosts in South 0. But adding that same mean to an otherwise identical pooled power forecast **worsens three catalogues out of four**. Adding local scatter to the mean forecast worsens all four. The whole-catalogue autocorrelation, with the independent self-pair variance restored, gives the same direction in each comparison. The worst analytic bound on its omitted angular-series terms is 1.31e-6. No evidence here for promoting the tracer correction to a universal parent coupling. See transfer-scores.csv (including 0.075 and 0.10 stress bands), attribution.json and protected-replay.json.

## Field tests independent of satellite occupation

1. **Velocity.** Project out the window-convolved constant-density, density–velocity and noise nuisance templates of all three models using the DR12 z≈0.38 covariance, without reading the observed bandpowers. The heavy versus same-background cold contrast is 0.000325 covariance standard deviations (monopole and quadrupole) or 0.000496 including the hexadecapole. This measures the accessibility of this particular nuisance-independent statistic, not all cosmological information. See FIELD-TEST.md and field-accessibility.json.
2. **Light bending.** Use the retained native Weyl transfer, not a rotation law or assumed local halo abundance. The potential convention is described in [the CAMB transfer definitions](https://camb.readthedocs.io/en/latest/transfer_variables.html). For a source at z=1 and L=100 the ordinary linear lens power shifts by −0.530% (heavy versus cold); the part satisfying a common matter-power nonlinearity cut Δ²<0.2 shifts by only −0.0875%. At L=400 the apparently larger signal has no contribution satisfying that conservative cut. The curves outside it are linear extrapolations, not nonlinear predictions. See source-plane-lensing.csv.
3. **Remove the foreground at map level.** Apply the existing [three-plane geometric null](https://arxiv.org/abs/1312.0430) to the parent's three thin source planes z=(0.51,1,2); weights (0.5071642,−1.5071642,1) fixed by source distances alone. Use the identical weights for each cosmology; ΛCDM has a small, explicitly retained foreground leakage. All source-plane cross terms are included. This is a constructible ideal combination, not a measured galaxy shear catalogue.

| Angular multipole | Heavy vs same-background cold | Heavy vs matched ΛCDM |
|---:|---:|---:|
| 30 | −0.00408% | −1.4390% |
| 100 | −0.03290% | −3.0579% |
| 188 | −0.09408% | −3.8166% |

These are dense-time, spherical-Bessel, linear convergence power ratios on the computed band ending at k=0.25/Mpc. They do **not** bound the tail above that wavenumber. No galaxy occupation enters. At L=100, the earlier fixed-weight Limber decomposition of the heavy-to-ΛCDM log ratio gives −0.01845 from geometry, −0.01230 from cold/background Weyl evolution and −0.000329 from the heavy addition. The decomposition is a symmetric diagnostic, not three independently measurable terms.

For this one null-map auto spectrum, ideal full-sky Gaussian variance alone over L=30–188 yields heavy/cold separation 0.0762σ; heavy/ΛCDM 4.1254σ if all amplitudes are fixed, but only 0.5508σ after allowing one amplitude. The earlier amplitude-and-tilt check gives 0.2424σ for ΛCDM. These are forecasts, not observed significances. The source weighting multiplies the shape-noise power by 3.53 for ideal equal, independent source-map noise.

## Precision and reuse

The three native backgrounds now have 305 k modes and 124 redshift epochs each, including 78 new times. At the three tabulated multipoles thinning the new grid changes the Limber null power by at most 2.7e-8 fractionally. Densification changes the finite-band Bessel power by at most 6.9e-6. The absolute spherical-Bessel correction relative to dense Limber ranges from about −2.2% at L=30 to −0.093% at L=188; it largely cancels in the heavy/cold contrast. Although the integrated statistic is stable, the old ΛCDM transfer differs from the untruncated native replay by up to 2.0172e-5 at original epochs, just outside the 2e-5 pointwise gate. Do **not** claim that all old transfer values meet that gate. Dense production values are in dense-lensing.json and exact-null-lensing.csv. Hashes, masking, ordering and score reconstruction are checked by audit.py.

**Next empirical bridge:** use published [KiDS-1000 source distributions and bandpower information](https://kids.strw.leidenuniv.nl/DR4/KiDS-1000_cosmicshear.php) rather than treating ideal planes as observed galaxies. Freeze the distributions, masks, angular response, calibration freedom and model-validity cuts before inspecting measured powers. Test whether any real combination retains controlled-scale heavy/cold signal; if the accessible difference is mainly on nonlinear scales, derive the heavy-field nonlinear stress rather than adjusting satellite scatter. None of the KiDS measurements were scored here.
