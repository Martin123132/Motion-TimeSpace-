> Public reading copy: local links are mapped to released material or marked unavailable. Machine-specific passages, where present, have been omitted. See the inventory for the original digest.

# The frozen cycle drifts predict the signed photon readout on both gravity clocks

The equation-predicted net changes from cycles 2–4 account for **71.849% of the late joint photon discrepancy** on the fine gravity grid, measured by signed projection along that late discrepancy. Individually and together, their photon energy and current agree with the archived drift readouts within the unchanged 0.5% tolerance. This locates the origin of part of a saved simulation discrepancy; it does not remove it.

## Prediction versus saved readout

Energy, current and joint magnitudes are expressed in percent of their corresponding original momentum-route signal (not percent of the total light). The last column instead compares the magnitude of the *complex vector error* with the archived drift's own magnitude, so a phase error is visible. Four source substeps, primary photon setting:

| Gravity grid | Predicted energy / current (% of corresponding common signal) | Predicted joint (%) | Saved joint (%) | Joint vector error (%) |
|---|---:|---:|---:|---:|
| Coarse | 0.37345930 / 0.37284515 | 0.37332220 | 0.37331956 | 0.00171188 |
| Fine | 0.37346017 / 0.37284695 | 0.37332327 | 0.37332412 | 0.00030531 |

| Cycle | Predicted joint, fine (% common signal) | Signed share of late vector, fine | Joint vector error, coarse / fine |
|---|---:|---:|---:|
| 2 | 0.13913793 | +27.0504% | 0.002363% / 0.000897% |
| 3 | 0.17682467 | +34.5449% | 0.002636% / 0.000833% |
| 4 | 0.08740096 | +10.2535% | 0.010611% / 0.003785% |

The signed shares add; the joint magnitudes need not. The joint prediction changes by 0.00038439% of its own magnitude between gravity grids.

## What was predicted and what was carried separately

For a complete cycle of duration Δτ the frozen forcing in each active source cell is (ΔC_matched/D_matched − ΔC_wave/D_wave)/Δτ. Here ΔC is the branch's *full* equation-predicted raw work including ordinary matter and the prescribed geometric work, not just the heavy–metric pair. Each D is evaluated at its own original right-cell convention; the separate preparation grid has the same right endpoint throughout the active cells. The common cold baseline, medium, scattering, mode and visibility weighting were retained. Both complex components were carried through the linear scattering equations without fitting and without using archived endpoint changes to set amplitudes. The forecast is exactly zero in the first and final partial cycles before propagation. The source and photon predictions for all three cycles were sealed before the scoring code opened the comparison readouts. No new gravity interval or observations were used.

On the fine grid the saved **zero-net oscillatory remainder** contributes 0.00069869% on the common scale, with a signed late share of −0.00393%. The **incomplete fifth cycle** contributes 0.16076716% (+28.15492% along the late result). Its 0.86145-cycle duration was not padded or counted as drift. The first cycle, a separate control outside the late window, contributes 0.08989314% on the common scale. The three late contributions close to 100% using archived vectors; substituting the prediction instead gives 99.99981%.

Replacing *only* the complete-cycle drift and retaining the other three saved pieces gives a fine full-window joint gap of **0.57636074%** versus the saved **0.57636165%** (coarse: 0.57635278% versus 0.57635063%). This hybrid is a cross-check, not a prediction of the omitted pieces. The 0.5% full-window criterion is still exceeded, distinct from the passed 0.5% drift-prediction accuracy test.

## Checks and next step

All 48 drift comparisons and 18 hybrid checks pass at both source subdivisions where applicable; all 96 numerical checks pass. Worst component across the comparisons: 0.06428% or less; across the controls: 0.01046% or less. The primary and angular-check photon arrays are byte-identical at the saved precision and are not independent evidence. Source-subdivision, photon-time, gravity-step, branch-subtraction and cycle-superposition comparisons are recorded separately.

**Next:** forecast the actual time-dependent work over the last 0.86145 cycle from its own left state, freeze the photon vector on each gravity grid and compare with the archived partial-cycle readout. Do not extrapolate a complete-cycle mean or reuse its archived amplitude.

[Protocol](PROTOCOL.md) · [frozen inputs](evidence-001.zip) (archive member: `inputs.csv`) · source freeze (not bundled here) · photon prediction freeze (not bundled here) · [vector comparisons](evidence-001.zip) (archive member: `comparisons.csv`) · [numerical checks](evidence-001.zip) (archive member: `checks.csv`) · [signed and magnitude readouts](evidence-001.zip) (archive member: `readout.csv`).
