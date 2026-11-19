# What the repaired clock changes in the forest calculation

**Result.** The clock repair removes the sensitivity to where the microscopic scalar is handed over to its averaged evolution throughout the tested 37-mode band, at the original numerical tolerances. It does **not** remove the physical response to heavy-field pressure. At redshift 4.2, holding the initial state and thermal model fixed, removing that pressure gives **2.400 times** the wave-on partial linear flux power. No observed spectrum, galaxy velocity or free thermal fit entered this comparison.

## Independent controls

| Test | Result | Meaning |
|---|---:|---|
| Maximum microscopic current imbalance, clock spacings 0.24 / 0.12 / 0.06 radians | 4.83e-6 / 2.84e-7 / 8.01e-8 | Four modes, 150,561 readouts, independent pressure integral; the quadrature change at the tightest spacing is 1.08e-9. |
| Early state propagated to later microscopic state, both meshes and all 37 unique modes | 1.67e-5 density / 8.72e-6 current / 5.36e-8 pressure | All within the unchanged scaled 2e-5 / 2e-5 / 2e-6 gates. The second acquisition repeats k=37; it is checked, never counted twice. |
| Integrated action work, fine → finer | density 1.82e-5 → 4.11e-6; current 2.26e-7 → 6.43e-8 | Twelve comparisons (four modes × three later centers) on each mesh. The independent ordinary-cold-matter metric-work check is below 9.0e-9. |
| Replayed other-species and metric readouts, peak-normalized | 4.34e-6 then 1.75e-6 | Seven diagnostic channels, separately evolved. This is not a uniform relative error at channel zeros. |

The stress formula fixes the instantaneous metric-work coefficient to the heavy enthalpy, not a unit multiplier. Omitting its oscillatory contribution gives worst density errors of 2.17e-5 on the fine replay but **8.28e-7** on the finer replay, smaller than the correct formula's finite-mesh discrepancy there. Thus the identity follows from the action; these numerical errors do **not** independently discriminate the coefficient. Metric work and current transport nearly cancel. In particular one should not select the coefficient that happens to leave the smaller numerical remainder.

## Where the extra gravitational force comes from

Taking the difference between native pressure-off and pressure-on solutions with the same initial state, **75.11–75.33%** of the final force increase on the four diagnostic modes comes from changed *heavy comoving density*, and **24.68–24.89%** from the response of ordinary baryons and cold matter. These are signed fractions of the **change**, not fractions of the universe's mass. Both matching surfaces give this result. An independent pressure-on sum of the stored external stresses and slip checks the scalar constraint to 8.28e-8 of each mode's peak force. The off-arm external remainder is inferred by subtraction and has no independent species decomposition here. This identifies a common-metric gravity mechanism; it does not assign a heavy population to a particular galaxy.

## Which numerical uncertainty is now dominant?

Fixed radial mode 0.0794328 s/km; integrated total wavenumbers 7.05231–37 Mpc⁻¹; conditional 10,000 K heating normalization. Earlier and revised columns count pointwise source/solver checks, not observed successes.

| Branch | Earlier → revised passing knots | Partial linear power (km/s) | Change with denser wavenumber sampling |
|---|---:|---:|---:|
| MTS with leading wave pressure | 33 → 37 of 37 | 0.02795430 | −0.01914% |
| Same state, pressure off from z=99 | 18 → 37 of 37 | 0.06708754 | −0.03985% |
| Rolling all-cold control | 37 → 37 of 37 | 10.18596647 | −0.01678% |

The retained exact averaged pressure instead of its leading term gives 0.02795430 (37/37). Moving the matching surface changes either heavy full-band integral by less than 4.9e-8 relative. The cold control was checked against its original bank and does not use a heavy matching surface. The wave/cold partial ratio is 0.0027444; **unlike wave/off, those branches have different cosmological preparations**. The wavenumber-sampling changes exceed 2e-5 relative, so passing 37 point checks does not certify the finite integral to that precision.

For a tail above 37 contributing at most 1% of its own partial power, a sufficient weighted density/velocity RMS ceiling is 0.01216 wave, 0.01883 off, or 0.23203 cold. The unmeasured RMS is not set to its last-band value. Conversely, even ignoring *all* unseen cold power, bringing the wave total to half of cold would require at least about 5.065 km/s of unseen wave power, roughly 181 times its computed partial power. Parity would require about 10.158 km/s, or 363 times the partial power. These are necessary amounts conditional on the finite quadratures, not upper bounds on what lies beyond the cutoff.

**Next physical test:** separate the signature of wave pressure from gas heating. Use the response derivative in EQUATIONS.md to freeze shifts of the three signed density/velocity cancellations at 10,000 K before testing 9,000 and 11,000 K with unchanged source histories on each branch. Keep the broadening-only and dynamical gas-pressure contributions separate. Then extend the total-wavenumber coverage beyond 37 into the next acoustic lobe; do not score observed flux data with an assumed zero tail.

Machine-readable comparisons: full-grid-gates.csv, full-grid-bands.csv, bridge-state-gates.csv, repeat-anchor.csv, gravitating-source-response.csv, impulse-finer.csv, retarded-work-finer.csv, missing-tail-budget.csv and tail-parity-requirement.csv.
