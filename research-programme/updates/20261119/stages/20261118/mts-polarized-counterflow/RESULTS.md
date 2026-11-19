# Radiation and gravitating heavy stress through the matching window

**The retained scalar's longitudinal stress predicts a real momentum transfer in the calculation.** Between a=0.00015 and a=0.000225016 the field equations give a weighted momentum change of +0.204674. Direct stress supplies +0.105240 and work by the geometry supplies +0.099474. Dropping stress misses +0.105200; retaining both leaves −0.0000401. This is an internal test against the resolved field, not a measurement of cosmic pressure.

## What now reaches the match

We joined polarized finite-opacity scattering, its return force on the gas and both free-streaming neutrino populations to the evolving nonlinear geometry and matter, for the same Gaussian growing pair of waves in both backgrounds. The earlier active radiation calculation ended at kτ=20. Both histories now pass the matching centre at kτ≈176.599 (z≈4443) and extend to the top of its phase window at kτ≈177.717.

| Centre coefficient, synchronous slices | Heavy + CDM | All-cold control |
|---|---:|---:|
| CDM density at the centre | 910.66996 | 1487.83434 |
| Phase-averaged heavy energy | 16.98090 | 0 (no heavy field) |
| Phase-averaged heavy covariant momentum | 1.01404 | 0 (no heavy field) |
| Heavy energy minus own CDM density | −893.68906 | not applicable |

The old short-window projection gave −899.396 for the relative coefficient. The change of +5.707 is from extending the active sources **and** replacing the tight photon fluid, not an isolation of photon scattering alone. These are per-primordial-amplitude-product response coefficients on one triangle, not observed densities. The tabulated CDM entry is an instantaneous centre value; the phase-smoothed CDM readout in the separate junction replay differs by 0.000040 on the heavy branch.

## Can the slowly varying fields carry their own stress?

Starting at a=0.00015, we advanced the heavy energy, momentum, CDM density and volume expansion together. Their initial values were taken once. Subsequent second-order scalar/CDM values are comparison targets, not drivers; radiation/baryon active stress and the incoming first-order waves still come from the reference history. The scalar pressure feeds back into gravity. No pressure coefficient or initial condition was optimized against later samples.

| Refined energy/momentum replay at the final centre | Heavy energy | Heavy momentum |
|---|---:|---:|
| Direct phase projection of the oscillating field | 16.980901 | 1.014042 |
| Derived stress and coherent metric work | 16.982850 | 1.014377 |
| Error from suppressing the generated stress (same prepared state, leading work) | −4.36696 | −0.10520 |

The derived-stress endpoint errors are 0.0115% of energy and 0.0330% of momentum. Absolute energy errors at the two intermediate checks are 0.00358 and 0.00473; avoid a percentage near the energy zero crossing. The all-cold model generates no scalar response and reproduces its nonzero CDM control to 0.000041 at the endpoint. An independent signed-work check predicts 0.00133444 versus 0.00133334 measured for the narrow phase correlation between expansion and scalar kinetic energy (0.0822% difference). Including it slightly *increases* the aggregate endpoint error relative to omitting it; other errors partially cancel. The pressureless control also fails with the same covariance omitted on both sides (errors +0.00132 versus −4.36696 in heavy energy). These are approximation tests on this window, not accuracy guarantees at later times.

## Checks that distinguish numerical effects from physics

- Both branches pass the frozen 1e−8 absolute momentum-return and photon-energy checks. Full versus refined grids change the heavy relative coefficient by 0.00079 and cold CDM by less than 0.000001. Starting finite-opacity propagation at kτ=20 instead of 10 shifts them by +0.00295 and −0.00062 on the primary grid. Independent retarded integration differs from the refined direct relative density by +0.000209. The refined Hamiltonian residual over the peak term sum is 3.84e−5 (heavy), 4.70e−5 (cold); later-start controls reach 1.6e−4.
- The native linear neutrino reference initially differed by up to 3.9% of peak. Raising only its angular accuracy, delaying its approximate high-frequency hierarchy, reduces the independently evolved density/flux errors to at most 2.41e−5 of peak. The heavy/cold production histories retain the original first-order metric: the high-resolution reference also changes some leading metric/flow inputs by up to 6.9e−5 of peak. That is a sensitivity, not a rigorous nonlinear error bound.
- Finite-difference parallel transport of an independent polarized screen tensor agrees with the angular operator within 2.46e−11. Coarse/fine angular maps need not match on individual unphysical polarization basis vectors; on the actual saved waves the geometric and per-opacity collision sources differ by under 2e−13 and 7e−14. Truncating the outgoing photon hierarchy from 12 to 8 leaves the full-window matching relative coefficient unchanged within 1e−10. Massless plus 36 massive momentum shells remain active.
- Changing only the additional proper electron-fraction perturbation changes the heavy relative coefficient by 3.4e−6; the single extra gas-pressure term changes it by 4.3e−8. Neither test establishes a bound on omitted thermal physics. The early helium response reproduces the native Saha-era background log-derivative to ≲1.4e−5 of peak.
- Projector widths/degree, conservation subintervals, two source grids, two field grids, prescribed-metric and active-metric replays and the zero-stress controls are saved. The four direct longitudinal stresses on the refined 6π projector are −0.016090, −0.000293, +0.007929 and +0.013691. This sign change would be lost in a single positive fitted pressure constant. The coefficient is quadratic; its sign is not the sign of the total physical pressure.
- Both complete angular terminal restarts replay bit-for-bit from kτ=160. Exact instantaneous and separately smoothed centre packets are retained for the next evolution, with interpolation sensitivity recorded. No catalogues opened, no galaxy occupation assigned, no added couplings and no GitHub changes.

**Next physical calculation:** switch the scalar and its gravitating source to the derived averaged equations while evolving the surrounding photon, baryon and neutrino perturbations rather than replaying their trace. Use an overlapping window to test the full energy/momentum constraint and switch-time dependence before extending toward z=99. Include or bound the omitted rolling-scalar source, recombination/thermal assumptions and second-order gauge conversion before using these seeds for an observational prediction. The present signal is the transfer of stress to momentum; no new bispectrum or rotation-curve score is reported.

Numerical records: validation.json, junction-refined.json, stress-refined.json, averaged-refined.json, coherent-work-refined.json and junction-restart-check.json. The heavy/cold full and refined NPZs are raw histories. matching-restart-heavy.npz and matching-restart-cold.npz contain both exact and phase-filtered radiation states. EQUATIONS.md defines every reported stress and source.

