> Public reading copy: local links are mapped to released material or marked unavailable. Machine-specific passages, where present, have been omitted. See the inventory for the original digest.

# The first-period current keeps both gravity rates below 0.5% in period two

The source restarted at 89.2415903205 conformal Mpc and reached 89.3345657494. On the fine grid, the second-period rate errors were **0.198416% (momentum)** and **0.198334% (density)**; measured cumulatively from the original switch they were **0.196082%** and **0.196043%**. Both routes also passed on the coarse grid and with both step subdivisions. The error rose slightly from period one, so the cumulative pass is not hiding a failing second period.

| Gravity grid / route | Period two: no stress | Period two: with stress | Two periods: no stress | Two periods: with stress |
|---|---:|---:|---:|---:|
| Coarse / momentum | 0.765655% | 0.198419% | 0.761628% | 0.196084% |
| Coarse / density | 0.191128% | 0.198337% | 0.187298% | 0.196045% |
| Fine / momentum | 0.765650% | 0.198416% | 0.761623% | 0.196082% |
| Fine / density | 0.191125% | 0.198334% | 0.187296% | 0.196043% |

Four subdivisions shown, with full precision in [results.json](evidence-001.zip) (archive member: `results.json`). “No stress” means **no complementary correction**; the wave and all other existing stress sources are still present. The fine density route was already below tolerance and got slightly worse with the correction. The momentum route changed from failing to passing. Neither corrected route crossed 0.5% at any saved second-period sample. The fine second-period peaks were 0.319965% and 0.319609% of the respective RMS rates.

## Why period two is a different test

For each route we evolved its own trailing mean according to m′ = θ′[j_live − j_leaving]/π. For positive outgoing phase, j_leaving comes from the same route's saved first-period instantaneous wave current, not its mean, not the other route, and not the earlier resolved-wave comparison. The saved first source corner precedes precisely π in the reconstruction by about 4.74×10⁻⁷ radians. The first 1.40×10⁻⁸ conformal Mpc of the interval therefore still uses the incoming prefix for the outgoing sample. We split that internal step at the actual phase crossing rather than rounding the corner, adjusting the mean or changing the output grid. By the end the original pre-switch samples have left the averaging window. An inherited integration constant, if present, was not removed.

We reused each saved final ordinary/field state, integrated curvature, all 77 bin states with their 69 angular orders, spectral state, mean and complementary density. Start-state checks are exact. The density-driven route reads its algebraic metric without resetting its independent momentum integration; neither the integrated curvature nor the algebraic energy curvature showed a jump at the join. We kept the same exchange and stress equations: only ρ(m−j_live) and ρe_c are added to the explicit wave. There is no second fluid current or new matter sector.

## Scoring and numerical checks

Each rate error is the time-weighted complex RMS difference between the derivative of the energy-constraint curvature and the rate from the momentum equation, divided by the RMS momentum rate on that trajectory. Cumulative scoring adds the numerator and denominator integrals from the two intervals **before** taking the square root. Derivatives are evaluated separately on each side of the source corner. The corrected fine cumulative curvature drift, after subtracting the original switch offset, is 0.017410% of actual motion on the momentum route and 0.017958% on the density route.

We checked the sliding mean by directly integrating the phase histories, the pressure and density balances, the single addition of the heavy current, and the disabled trajectories against the original uncorrected solver. The largest numerical control was 0.00000125% or less. Between coarse and fine grids at four subdivisions, the second-period rate-error histories differed by less than 0.000233% of the fine residual; the complementary current, density and pressure each differed by less than 0.000610% of their respective fine signals.

**Restart:** The four second-period packets contain both corrected routes and their disabled controls, final matter, bins and spectral shape, final complementary mean and density, global phase, and each route’s current history. They end at the second source corner (left limit). Start the third period on its right side from those final states, using period two for the delayed current once its phase enters that history and period one's tail until then. Keep the last partial cycle separate when eventually scoring the entire saved interval to 89.6. No third period, new fit or photon calculation was run here.

[Protocol](PROTOCOL.md) · [All scores and controls](evidence-001.zip) (archive member: `results.json`) · [First-period source and restart](../mts-first-period-companion-joint-89p24/RESULTS.md). Reproduce sequentially using single-threaded Python 3.13 with -B in a fresh sibling stage: second.py init, second.py run, score_second.py and verify_second.py. Source and output checksums are in seal.json.
