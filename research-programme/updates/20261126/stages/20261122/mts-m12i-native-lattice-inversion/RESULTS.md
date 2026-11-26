> Public reading copy: local links are mapped to released material or marked unavailable. Machine-specific passages, where present, have been omitted. See the inventory for the original digest.

# The same-host wave seed recovered, without choosing phases from a galaxy
**The archived FIRE m12i generator and its first-order particle displacement give the same large-scale pattern.** The generator is a source for a specific simulated realization, not another fitted halo. Both routes start before galaxy formation. Neither uses rotation curves, stream positions, a fitted occupation, or the old compact stationary wave to select a state.

| Maximum k (comoving Mpc⁻¹) | Native first-order vs generating seed, relative rms | Earlier Eulerian density vs seed | Earlier Eulerian momentum vs seed |
|---:|---:|---:|---:|
| 0.75 | 0.0841% | 2.879% | 7.153% |
| 1.5 | 0.1988% | 5.099% | 12.034% |
| 2.4 | 0.7692% | 7.616% | 17.312% |

The common lower screen is 0.2925 Mpc⁻¹ (first available box mode 0.29405). At the largest cutoff the signed correlation is 0.9999745 over 145,346 modes counting conjugates. This is not 145,346 independent measurements. The domain-shift negative control has correlation 0.00471 with the reference seed; no translation was fitted. The generator supplies the band phases without estimating them from displaced density or momentum. This does not certify all continuum approximations to 0.5%: the point-sampled displacement differs from the generator by more than that across the widest band. A piecewise-constant volume reconstruction, a deliberately different discretization, differs by 4.92% rms there.

**Independent evolution check.** All 146,541,875 original records have been assigned to their generator lattice, including the gas stagger and merged coarse material. Gas and fine dark matter have identical cell keys; all seven levels tile the periodic domain once when gas is paired with dark. The maximum discrepancy of the ballistic lattice estimate from the prescribed centre is 0.102 cells in any coordinate. The two recovered displacement orders were propagated in the simulation's own dust background to z≈19 and compared with the 137,744 distinct dark particle IDs saved from four later simulation shards. The pooled three-dimensional position error drops from **4.730 to 0.898 comoving kpc**, and peculiar velocity error from **1.971 to 0.620 km/s**, against the previous velocity-as-linear prescription. Both improve in each shard. This tests the inversion against a later simulation output, not observations or the MTS wave propagation.

**What it does for MTS.** The private packet supplies the curvature realization, wave coordinate number density, spatial phase, velocity divergence, and paired cold coordinate number density at z=99. It retains the original mass, metric coupling, normalization, starting time, and transfer screens. Assigning the generator realization to the retained MTS primordial spectrum is an *explicit matched-initial-conditions comparison* of cosmologies; FIRE did not simulate MTS. The same independent simulation seed can now be used in both.

| z=99, full tested band, 192-grid drifted window | Generator replay | Native particle inversion |
|---|---:|---:|
| Initial mean wave density contrast on tags ending inside 13.96 kpc | 1.97301% | 1.97323% |
| Initial change in inner share if classical destinations are kept, percentage points | −0.20737 | −0.20345 |
| Initial relative current contribution per e-fold to inner share, fraction units | −0.00014948 | −0.00014525 |

The old stationary wave would instead require **+46.03 percentage points** versus uniform classical tracing in that aperture. The source-recovered initial weighting does not explain that concentration. Neither that concentration nor today's force is imposed here. The core-change and relative-current estimates differ by 1.89% and 2.83% between seed and native reconstructions: the sign agrees while those particular precision gates stay open. Of the 27 earlier-style observable comparisons **10** clear 0.5% across source choice, cell quadrature, grid and clock; **0** clear 0.002%. These are numerical sensitivities, not confidence intervals or probabilities for a theory. The distinct quadratic displacement and transport terms, and even the undisplaced multiresolution lattice, contribute to the old density/momentum split; the measured cubic expansion leaves 0.07–6.17% of that split on the four frozen modes. See decomposition (not bundled here) and [all source comparisons](evidence-001.zip) (archive member: `independent-seed-comparison.csv`).

**Next physical calculation:** advance heavy and ordinary cold perturbations from the *same recovered seed* through the common metric, with the derived wave pressure/current, starting at z=99. Use z≈19 as the first simulation-side cold and baryonic check; do not interpret matching particle labels as wave trajectories. Bound finite-band and environment errors before conditioning any present-day galactic force. The old Pal 5 and GD-1 comparisons stay downstream, not calibration targets.

Derivation and replay (not bundled here) · wave and cold packet (not bundled here) · later dynamics (not bundled here) · [unchanged window checks](evidence-001.zip) (archive member: `window-gates.csv`). All private.
