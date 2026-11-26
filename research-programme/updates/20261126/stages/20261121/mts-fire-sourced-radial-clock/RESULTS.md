> Public reading copy: local links are mapped to released material or marked unavailable. Machine-specific passages, where present, have been omitted. See the inventory for the original digest.

# The sourced radial clock preserves the reversal; the ordinary matter must respond

**Private · 21 November 2026.** The previous stage transported the prepared wave without the still-unknown radial part of its relativistic clock potential. Here we calculated the part set by the saved wave and Newtonian geometry, applied it for the full 22.190427 Myr interval, and tested the ordinary foreground as matter rather than just as a fixed source. No rotation curve, force target, new coupling or occupation was fitted.

## What happened to the metric?

All numbers are self-gravitating inherited wave minus reset, on the original **three-radius compensated metric-force combination**, not accelerations measured at a single radius.

| Fine-grid result in m/s² | Before radial clock transport | With sourced radial clock |
|---|---:|---:|
| First relativistic spatial correction | +1.5400e−19 | **+1.5806e−19** |
| First relativistic time correction | +2.3946e−19 | **+2.4352e−19** |
| Spatial minus time | −8.5461e−20 | −8.5461e−20 |

The coupled-minus-reset radial clock difference adds **+5.5640e−21** through wave evolution; the component shared between histories subtracts **1.5054e−21**, leaving **+4.0586e−21** net. The direct time evolution and the independent saved response kernels reproduce that shift to about 1.1e−11 relative. The previous reversal of the spatial correction therefore survives *this derived radial source*: the older endpoint-only value was −5.016e−20. The new fine time result shifts by about **1.7%** from the previous retarded calculation. This is a correction to the propagated state, not another copy of its direct endpoint clock term.

The net is a cancellation: +1.791e−20 from the wave gradients and stress, about −7.107e−21 from self geometry, −5.630e−21 from ordinary–wave geometry and −1.111e−21 from ordinary geometry. Nine versus eighteen time steps give +4.1032e−21 versus +4.0586e−21 (1.1% spread on the small increment). A separately evolved midpoint changes it by 0.0050%; independent gravity solver, higher angular cutoff and higher radial quadrature leave the sign unchanged. The earlier endpoint constraint is recovered at all three weighted probes taken together. If ordinary **proper** rather than densitized first-order energy is fixed, transport and endpoint conversion give spatial +1.982e−19 and time +2.836e−19. Neither is a measurement of ordinary relativistic stress. Source split (not bundled here) · matched result (not bundled here) · [radial derivation](DERIVATION.md)

**Boundary accounting.** The finite wave box reaches 388.41 kpc. A harmonic exterior changes the matched result by only +5.85e−27 m/s² relative to dropping the exterior integral. This is *not* a declaration of empty space. The alternate continuation has an explicit gradient-dependent bound; if its discrepancy outside falls no slower than inverse square with edge amplitude equal to that of the ordinary harmonic continuation, its matched effect is bounded by 2.04e−27 m/s². Separately, a freely supplied static *differential* central mass term would need an equivalent 7.31e3 solar masses at this order, or an independent differential quadratic lapse term an edge acceleration of 1.27e−15 m/s², to match the conditional time term by changing wave evolution. These are sensitivities, not inferred missing masses, tidal fields or allowances. Exterior remainder (not bundled here) · unknown boundary modes (not bundled here)

## The ordinary-matter test

If the stars/gas start in the same phase-space state in the two gravitational fields at 590, their instantaneous ordinary density and momentum agree. Their **next acceleration does not**. Conservation gives an initial ordinary density curvature without knowing a stellar velocity dispersion. This is Newtonian-order feedback, separate from the tiny relativistic correction above.

| Common launch at 590, fine grid | Inner half, 6.185–7.310 kpc | Outer half, 7.310–8.434 kpc |
|---|---:|---:|
| Foreground mass under the compact radial weight | 1.593e9 solar masses | 1.497e9 solar masses |
| Difference in acceleration on that matter (outward positive) | +8.675e−13 m/s² | +8.768e−13 m/s² |
| Initial curvature of weighted ordinary mass | +6,543 solar masses/Myr² | +10,513 solar masses/Myr² |
| Initial curvature of the ordinary matter's own radial gravity, volume-weighted | +2.653e−16 m/s²/Myr² | +1.851e−16 m/s²/Myr² |
| Minimum ordinary stress difference to maintain identical radial momentum histories instead | 2.34e−15 Pa | 1.65e−15 Pa |

These are two smoothly weighted windows, **not total masses in unweighted shells**. At common launch the live response starts as half the curvature times elapsed time squared. Do not extrapolate that law for all 22 Myr. Direct displacements of the same foreground with two different shared velocity controls recover both curvatures within the unchanged 2e−5 fractional threshold. Strong and weak force-density integrations agree when finite-element faces are retained. The local density is inferred from the archive's Newtonian potential; positive mass in the weighted windows does not establish pointwise positivity or turn this into an observed stellar mass map. [Ordinary balance](evidence-001.zip) (archive member: `ordinary-balance-64.csv`) · displaced mass (not bundled here) · its gravitational effect (not bundled here)

**What is actually missing at cubic order?** For the collisionless shared-state test it is not an entire velocity distribution. Azimuthal streaming and velocity dispersion drop out at this order. Continuity plus the saved density slope eliminate polar current and fix the angular mean of radial current. Just one weighted correlation of **radial mass flow with angle** per window/observable remains. For the mass observable the upper-bound coefficient per km/s drops from 3,474 to **7.42** in the inner half and from 3,332 to **9.84** in the outer half, in solar masses/Myr³. Those are reductions of 468 and 339 times in the sensitivity to unknown flow, **not** claimed observational error reductions.

The density slope still matters: the determined mass third derivatives on the retained right-hand interpolation are −149 and −686 solar masses/Myr³, versus −37 and −85 using the preceding interval. An admissible divergence-free meridional flow can change them without changing that density slope. The residual cannot be set to zero merely because snapshots lack velocities. Characteristic Taylor coefficients verify the jerk formula; ordinary finite differences near compact-window edges do not all reach 2e−5, and their errors remain in the record. Current reduction (not bundled here) · [non-uniqueness controls](evidence-001.zip) (archive member: `current-controls-64.csv`) · [moment derivation](ORDINARY-RESPONSE.md)

**Next:** test the ordinary response with an independent, source-matched radial-current moment and a shorter source-time interval near 590. Distinguish simulated FIRE baryons from the static observed foreground in this hybrid forcing: a simulation velocity is not automatically the Milky Way's velocity. Where a current is unavailable, propagate the explicit residual bound rather than assuming zero flow. This is how to move from an initial response toward a live gravitational comparison. Nonradial clock terms, intrinsic ordinary post-Newtonian energy/stress and earlier first-order wave preparation remain separate.

Validation (not bundled here) · replay and hashes (not bundled here). From this folder, with the original local Python/NumPy/SciPy and the previous bank in place, use Python -B with no save flag. For each of 32 and 64, run radial_history.py with the step count and main; then ordinary_momentum.py, exterior.py, ordinary_kick.py, ordinary_jerk.py and current_reduction.py each with the step count. Additional fine radial_history.py variants are quadrature, angles, native and half. Run manufactured.py and verify.py without a count. Default executions compare saved outputs. No public or Galaxy Lab files changed.
