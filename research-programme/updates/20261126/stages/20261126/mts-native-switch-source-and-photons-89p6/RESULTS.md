# Direct switch source brings both photon routes inside 0.5%
At 89.14850380306666 conformal Mpc the directly evaluated heavy quadratic sources of the retained Fourier probe are E = -1.3319828061215036e-14 - 6.599022181216298e-13 i and J = 2.856286553545417e-16 - 2.644114474183047e-15 i, in the saved bank normalization. They are identical in the incoming state inversion and outgoing force evaluation, on both gravity grids and on the resolved-wave control. These are mode amplitudes, not a homogeneous energy density and not an observed flux.

The total reconstructed, normalized instantaneous heavy density/current at entry are in matched-switch-p16.npz and matched-switch-p32.npz. For p32 they are 6.16678124454e-10 + 6.98610309471e-10 i and 2.59149128269e-12 - 2.40038903871e-11 i respectively. This is a re-solution for the heavy coordinates, with curvature, ordinary matter, bin populations and initial angular state retained; it is not a photon-level subtraction. See METHOD.md.

| Full window to 89.6, primary transfer, four subdivisions | p16 | p32 |
|---|---:|---:|
| Previous joint route gap, % of original small correction | 1.567398 | 1.567329 |
| New energy gap, same channel normalization (%) | 0.175538 | 0.175505 |
| New longitudinal-current gap (%) | 0.175464 | 0.175431 |
| New joint gap (limit 0.5%) | **0.175522** | **0.175488** |
| Momentum-route correction, % of full joint launch | 0.019019 | 0.019019 |
| Density-route correction, % of full joint launch | 0.019014 | 0.019014 |
| Joint gap with compensating stress disabled, original small-correction units (%) | 513.8775 | 513.8800 |

The joint discrepancy dropped by about 88.8%. Both absolute corrections also pass the separate 0.163% size limit. The stress-disabled control fails the inter-route test: sharing the source does not by itself make the two routes agree. On p32 the entry and subsequent continuous contributions to the joint gap have norms of 0.06171% and 0.23182% respectively; combine the signed vectors before taking a norm. No readout was adjusted to force agreement.

**Controls.** The shared-process attempt failed its source check and remains saved. In two independently initialized repeats the largest change in the directly computed switch source was 0.00000784% of the old interpolation split. The largest difference at the two adjacent bank knots was 0.00005484% on that same scale. Of the 60 replay and refinement checks, 60 passed: worst photon refinement 0.13482%, gravity refinement 0.04508%, inner subdivision 0.02906%. Across all three transfer settings and both subdivisions the largest stress-on route discrepancy in any channel was 0.17565%. Cold baseline and original heavy launch readouts are byte-for-byte equal as arrays to the previously saved ones, before adding the new correction. All signed predictions were frozen in prediction-freeze.json before comparison.

**Interpretation and next test.** The off-grid source mismatch explains most of the earlier numerical disagreement in this window. This does not measure cosmological fit. The useful independent test now is a new time window: carry both histories out of 89.6 without resetting them, freeze the two photon routes on the same normalization, and check whether they stay within 0.5%. If the necessary native sources are absent, acquire them before scoring; do not extrapolate the present correction.

Files: native-check.json (first failed repeat), fresh-check.json (new independent repeats), native-standard.npz, preparation-checks.json, interface-*.json, gravity-freeze.json, prediction-freeze.json, scores.json, result.json and seal.json. run_checked.ps1 runs downstream stages only once the native input is frozen. No public or Galaxy Lab files changed.
