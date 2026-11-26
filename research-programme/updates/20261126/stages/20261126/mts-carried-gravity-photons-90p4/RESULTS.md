# What the photons retain through 90.4 conformal Mpc

**The added 89.65–90.4 interval passes on its own, but the cumulative prediction misses the unchanged 0.5% consistency threshold on both gravity grids.** The finer-grid joint difference is **0.46224%** for the new interval and **0.65971%** for the full history from the switch. The earlier 89.65 result stands. This is a comparison of two ways of computing gravity for the matched-minus-resolved MTS correction, not an observation that MTS misses the sky by 0.66%. The cold comparator, switch preparation and photon normalization did not change.

| Primary transfer, four inner subdivisions | New energy | New current | New joint | Cumulative energy | Cumulative current | Cumulative joint |
|---|---:|---:|---:|---:|---:|---:|
| p16 | 0.462353% | 0.461817% | 0.462234% | 0.659846% | 0.659269% | 0.659717% |
| p32 | 0.462363% | 0.461827% | 0.462243% | 0.659837% | 0.659262% | 0.659708% |

Each denominator is the original visibility-weighted reference correction in the same channel. The two cumulative corrections separately remain small on the full-launch scale: 0.018391% and 0.018378% on p32, below the separate 0.163% size limit. Small amplitude is not agreement between the routes. With compensating stress switched off, the finer-grid joint gaps are 79.54% incremental and 534.02% cumulative on the original small-correction scale.

## What produced the difference

On a density-route trajectory call the potential calculated from energy Φ_E and the time derivative predicted from its *own* current and lapse P_J. The discrepancy R = dΦ_E/dη − P_J can be measured separately for the matched state and resolved wave. The source driving the energy/current route difference splits identically into the difference of their R values, the change in P_J between trajectories, and the separate lapse difference. We transported each contribution through the unchanged scattering equations over the full visibility distribution, not just to its peak. This is a diagnostic of frozen predictions, not a new correction applied to the histories.

| Contribution projected along the full joint discrepancy, percentage points of original correction | p16 | p32 |
|---|---:|---:|
| Incoming photon difference at 89.65 | +0.202222 | +0.202222 |
| Matched density residual | +0.375425 | +0.375377 |
| Minus resolved-wave density residual | +0.076636 | +0.076674 |
| Change in momentum rate between gravitational trajectories | −0.003935 | −0.003935 |
| Difference in lapse driving | +0.009369 | +0.009370 |
| **Sum** | **0.659717** | **0.659708** |

The subtraction sign on the resolved residual matters: its contribution to the projected gap is positive, not a claim that both raw residuals have the same sign. These are signed projections, not norms added as scalars. On p32 the net density residual contributes **+0.45205 percentage points** and reinforces the inherited photon difference. The signed full-spectrum reconstruction closes to less than 9e-12% of the original reference on both grids. The result identifies an equation to investigate; it does not establish which physical stress term is wrong.

## Controls and restart

- Fifteen contiguous 0.05-Mpc pieces on each of eight physical continuations; each started from its own exact saved tensors. Both final perturbation banks retain all 77 × 69 bin moments. No state resets, amplitude changes, repeated previous cycle, or extra photon kick. The matched driver used the prior frozen U restoration, not the independently computed native test value.
- Once a full phase period had elapsed, the delayed physical current came entirely from that route's new history. Direct integration of the preceding π of phase reproduced the carried mean (up to its inherited integration constant) to within 5.8e-8% of the segment mean-current peak across routes. All 14 seam readouts on every continuation agreed within 2e-12% of their preceding endpoint values.
- The complete signed photon predictions and hierarchies were frozen before scoring. All 144 replay, grid, inner-step, time and angular comparisons passed; worst 0.003375% on the original scale. Across settings the cumulative joint gap ranged from 0.65970% to 0.65979%. Refining the grids does not remove the miss. The primary forward readout and adjoint at the visibility peak agreed to 8.3e-12% or better.
- Read **restart90.json** for the field, photon and incident populations, oscillator and delayed-current history at 90.4. **scores.json** is the frozen-forecast comparison; **balance.json** and **balance-vectors.npz** retain the post-score decomposition. **peak-attribution.npz** additionally divides the peak driving into fifteen time intervals. **verify90.py** checks receipts, links, signed reconstruction and restarts. No new data fit or publication.

**Next physical test.** Stay within these saved histories. Differentiate the energy constraint on each density trajectory, rather than choosing a corrective force from the photon residual. In the retained convention, with κ = k², DΦ_E = U − E/2 − 3ℋJ/(2κ) and P_J = J/(2κ) − ℋΨ + Fq. Therefore D R = U′ − E′/2 − 3(ℋJ)′/(2κ) − D′Φ_E − D P_J. Use the matter continuity and momentum equations to compute the derivative terms independently on the matched and resolved histories. Compare signed terms, their cancellations and their projections through scattering on both grids, including a differentiation control. To recover the present gate, a change would need to remove at least 0.15971 percentage points in joint norm on p32; this is a diagnostic scale, not a fitting target. No further interval or relaxed tolerance is needed to perform that test.
