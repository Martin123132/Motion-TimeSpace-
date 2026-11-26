> Public reading copy: local links are mapped to released material or marked unavailable. Machine-specific passages, where present, have been omitted. See the inventory for the original digest.

# Where the matched 77-bin evolution first disagrees

At the switch (89.1485038031 conformal Mpc), the retained matched preparation determines a wave state without copying the resolved control’s launch. With the saved microscopic forcing, the two ways of computing curvature agree to the original 0.5% RMS criterion through 89.6 Mpc. Their rates are more discriminating: the momentum-driven trajectory fails its own rate check on both clocks. The discrepancy can be traced back to the change from averaged to instantaneous heavy current at the switch.

## What was supplied and what was predicted

The input was the matched nonzero ordinary-matter launch, homogeneous oscillator phase, instantaneous heavy density, and the preceding half-turn (π of background phase) used to construct the saved mean-current quadrature. Using the mean and density together gives an observation-matrix condition number of 2.00 rather than 10.57 million for the instantaneous-only pair near the velocity turning point. On the fine clock the recovered wave reproduces density at the actual matched metric to 0.001484% and the de-averaged current to 0.00001686%. Density and current were not both set equal to their averages. [Launch checks](evidence-001.zip) (archive member: `entry-tests.csv`).

The ordinary sources, U, Q, Fq, heavy shear and incoming bin states came from the matched side. Four microscopic source functions (hfield, hmoment, henergy, hJ) still come from the sealed wave forcing bank: the averaged bank does not supply them. This is a conditional test, not an independent derivation of those functions. All 77 momentum bins and their 69 angular orders advanced with ordinary matter, waves and gravity. No post-switch reference state drove their evolution. The predicted histories were frozen before comparing to the [resolved control](../mts-prepared-joint-77-switch-89p6/RESULTS.md). No photon projection or fit was performed.

## What passed and what missed

Fine gravity clock, four subdivisions; time-weighted complex RMS. Each row compares the curvature reconstructed from energy to an independently integrated momentum history on that same trajectory. Drift subtracts the initial offset and is normalized to actual curvature motion; rate compares the smooth energy-constraint derivative with the momentum-equation rate. The threshold remains 0.5% for each, not their average.

| Gravity used for evolution | Full curvature | Drift since switch | Rate | First sampled rate crossing (Mpc) |
|---|---:|---:|---:|---|
| Momentum equation | 0.343252% | 0.220818% | **0.769540%** | 89.154296875 |
| Energy-density constraint | 0.344743% | 0.015310% | 0.190707% | None |

The same pass/fail pattern and first sampled crossing appear on both clocks with both subdivision counts. Neither source corner produces a measured curvature jump. The worst sampled momentum-route rate discrepancy is 1.3942% of the RMS rate. [All eight runs](evidence-001.zip) (archive member: `constraint-tests.csv`).

Comparisons to the corresponding *resolved trajectory* answer a different question. On the fine momentum trajectory the total current differs by 0.002212%, and the curvature rate by 0.133647%; neither number cancels the failed internal rate check. The four integrated bin stress differences are each below 0.0011% of the corresponding resolved stress. Four coarse-to-fine tests of very small energy/shear differences fail when normalized to those differences themselves (0.527–0.873%). Do not claim their small amplitudes are precisely resolved. [Control comparisons](evidence-001.zip) (archive member: `versus-resolved.csv`) · [Refinement tests](evidence-001.zip) (archive member: `refinement.csv`).

## Why the rate separates

At fixed incoming curvature Φ and identical ordinary and bin state, write the constraint residual as R = BΦ + Ecan/2 + 3HJ/(2k²) − U. The exact difference between wave and fluid residuals is ΔR = ΔD_h/2 + 3HΔJ_h/(2k²), where ΔD_h is the change in heavy density evaluated at that same Φ, including its volume term. The fluid launch satisfies the constraint to about 1.8 × 10⁻¹²%; substituting the phase-resolved wave leaves 0.342660% of the launch curvature scale. The heavy-current change accounts for 99.779% of this **signed projected offset**, and the heavy-density change for 0.221%. [Switch balance](evidence-001.zip) (archive member: `seam-budget.csv`).

A separate diagnostic takes the derivative of the rate residual with respect to Φ, at fixed other state variables, directly from the matter, metric and bin equations. A unit-Φ check against their numerical right-hand sides agrees within 3.8 × 10⁻¹⁴%. Multiplying that coefficient by the **switch offset alone**, with no fitted amplitude, predicts the difference between the two trajectories’ rate residuals with **0.50102% RMS error relative to that difference** (signed projection 100.458%; slight overprediction). This is 0.003734% of the momentum-rate scale. Using their recorded instantaneous Φ difference instead leaves 0.16076% of the route difference; this second check is diagnostic, not a forecast. Neither comparison is a repaired evolution or a pass for the 0.76954% residual. [Rate attribution](evidence-001.zip) (archive member: `rate-origin.csv`) · [Coefficient checks](evidence-001.zip) (archive member: `rate-jacobian-controls.csv`).

## Next test

Derive the compensating stress or metric term when phase-resolved current replaces the fluid mean. At continuous Φ the companion contribution to R must be −ΔR. If only the metric is changed instead, the accounting identity is B_wave δΦ = −ΔR; imposing that reset by hand would not explain why the physical switch selects it. Predict the compensation from the saved preparation or parent exchange law first, then repeat both gravity routes without moving the switch or changing the tolerance. If no such term follows, retain the junction failure rather than repairing it by fit.

[Protocol](PROTOCOL.md). Reproduction order in a fresh stage copy with the pinned upstream stages: prepare, evolve, score, then the seam and rate diagnostics. The sealed stage can be audited without launching those runs by checking the hashes listed in seal.json. No earlier histories were overwritten.
