> Public reading copy: local links are mapped to released material or marked unavailable. Machine-specific passages, where present, have been omitted. See the inventory for the original digest.

# How signed gravitational forcing reaches the photon visibility peak
**Decision:** The signed projection reproduces the archived photon density and current at the common visibility peak for the baseline, MTS and their difference on all six saved source intervals. Momentum forcing gives the larger share of the six-block contrast; its direction varies between intervals, so adding unsigned pushes badly overstates the result. One small energy-channel contribution is not individually converged to the unchanged 0.5% criterion.

## Peak result
For the retained longest mode, the entries below are percentages of the corresponding two-component launch norm. The difference row uses the signed MTS-minus-baseline launch norm, not either branch's launch. The energy and momentum columns are magnitudes of complex response vectors; they are **not** percentages to be added. Their signed sum retains both photon density and longitudinal current.

| 25.6–64 conformal Mpc, at peak | Energy forcing | Momentum forcing | Signed sum | Sum / two channel magnitudes |
|---|---:|---:|---:|---:|
| Baseline | 0.16045% | 0.13512% | 0.29503% | 99.82% |
| MTS | 0.16133% | 0.13092% | 0.29180% | 99.85% |
| MTS minus baseline | 0.18430% | 0.45885% | **0.57286%** | 89.07% |

The two channel sums reinforce each other in both branches (alignment +0.9927 and +0.9938). In the **difference** they also reinforce overall, though less strongly (+0.4946); their signed projections on the final vector are 23.10% energy and **76.90% momentum**. The larger cancellation is *between intervals*. Just **12.00%** of the six separate momentum-contrast magnitudes survives their signed sum, versus **58.54%** for energy. Of all twelve separate channel-by-interval magnitudes, **13.85%** survives. Counting every kick as if it pointed in the same direction loses that distinction.

The six-block signal is an addition to the pre-existing photon history. Restoring that history reproduces the previously saved full **1.48105%** peak contrast of launch. Neither 0.57286% nor 1.48105% is a reconstruction error; the **0.5% tolerance** is applied to differences between calculations, not to the size of the signal.

## Checks and the one exception
- **105/105** saved peak comparisons passed: six intervals and their coherent sum, three model combinations, five original numerical settings. Worst relative complex-vector difference was 5.42e-13; worst single-component difference was 2.37e-12 (rounded up). These are numerical reproduction errors, not physical uncertainty.
- **6/6** independent forward checks passed for the two forcing channels in the prespecified 32–38.4 interval, including the signed model difference (worst relative difference 7.06e-13). **6/6** checks also recovered the archived cumulative readouts with and without the incoming history.
- **251/252** resolution comparisons passed. The only exception was the **energy-forcing contrast on 44.8–51.2**, differing by **0.53217%** under the saved alternative matter step. Evaluating both source histories at the same knots on the *same photon kernel* gives **0.53221%**; changing only knot sampling gives 0.0000041%, and changing only the photon mesh gives 0.0000601%. This identifies the numerical origin, not which matter history is exact.
- The magnitude of that energy-channel shift is **0.00491% of the whole interval's peak contrast**: small in the total, but still outside tolerance for that channel. All six-interval sums pass the resolution tests; their largest single-channel change is **0.14036%** (momentum contrast), and the largest change in the combined six-block contrast is **0.11333%**. No failing row was dropped.

## Where this leads
Use the same peak response weights on the *already saved background* beyond 64 to find which times and which signed source need the tightest matter bounds. Carry the small matter-step sensitivity separately. Do not assume that 12% momentum survival continues into an uncalculated interval: that number was measured on the six known blocks alone. No new matter interval, observational fit, or change to either restart was made.

Derivation and input conventions (not bundled here) · [signed contributions by interval, including both output components](evidence-001.zip) (archive member: `signed-contributions.csv`) · [within-channel cancellation](evidence-001.zip) (archive member: `within-channel-cancellation.csv`) · [saved readout checks](evidence-001.zip) (archive member: `peak-comparisons.csv`) · [separate forward tests](evidence-001.zip) (archive member: `independent-split.csv`) · [resolution checks](evidence-001.zip) (archive member: `channel-sensitivity.csv`) · [source of the fourth-block discrepancy](evidence-001.zip) (archive member: `fourth-block-step-isolation.csv`) · [cumulative readout](evidence-001.zip) (archive member: `cumulative-readout.csv`) · [machine-readable summary](evidence-001.zip) (archive member: `outcome.json`).
