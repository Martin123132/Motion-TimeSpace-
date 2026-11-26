> Public reading copy: local links are mapped to released material or marked unavailable. Machine-specific passages, where present, have been omitted. See the inventory for the original digest.

# Cycles 2 and 4: the heavy current opposes the metric work

Both equation-based forecasts reproduced the saved net drift at both gravity steps with the original 0.5% tolerance. The heavy–metric cancellation recurs without using cycle 3 to choose a coefficient, amplitude or phase. The two terms alone do not predict the complete drift to that accuracy.

## What was frozen

Each matched and native-wave forecast starts from its own left state, reconstructed from the switch, on the same common cold baseline. Cycle 2 spans 89.24159032–89.33456575 and cycle 4 spans 89.42743046–89.52018481 conformal Mpc. The two gravity grids and two source subdivisions give 16 launches. All predictions were frozen together before scoring. The forecast retains the original source bank, grids, forcing and tolerances. See [protocol](PROTOCOL.md), launch record (not bundled here) and prediction record (not bundled here).

## Compare with the saved endpoint drift

Errors below are percentages of the magnitude of each row's own complex reference. The main comparison uses four source substeps and phase-crossing endpoints. Coarse and fine refer to the gravity step. “Difference” means matched minus native wave, subtracted before taking a magnitude.

| Predicted change | Cycle 2 coarse | Cycle 2 fine | Cycle 4 coarse | Cycle 4 fine |
|---|---:|---:|---:|---:|
| Matched total | 0.000601% | 0.000252% | 0.011249% | 0.003669% |
| Native-wave total | 0.011741% | 0.004308% | 0.010797% | 0.003045% |
| Difference of totals | 0.002363% | 0.000897% | 0.010611% | 0.003785% |
| Heavy + metric difference, against field-variable replay | 0.000629% | 0.000298% | 0.002474% | 0.000228% |

The last row is a change-of-variables check against a separate replay, not an independently archived measurement of sector work. The first three use the archived total. On the fine grid the predicted complex differences (real, imaginary, in units of 10⁻²⁰ of the raw constraint) are (+4.98769, −6.78885) and (+5.23569, −0.73848) for cycles 2 and 4. The paired differences change by 0.000710% and 0.001429% between gravity grids.

## What actually cancels

The heavy work splits exactly into E/2 and 3HJ/(2k²). Together with the metric work it enters the constraint with a minus sign. The [derivation](DERIVATION.md) shows which pressure terms cancel, and retains the actual background interpolation errors. The following fine-grid percentages project each *signed* contribution along its own cycle’s net complex branch difference; they are not ratios of absolute magnitudes.

| Contribution to matched-minus-native drift | Cycle 2 | Cycle 4 |
|---|---:|---:|
| Complementary metric work | +455.76% | +450.53% |
| Heavy energy contribution | +363.37% | +482.02% |
| Heavy weighted current contribution | −716.90% | −832.68% |
| Heavy subtotal | −353.52% | −350.65% |
| Heavy + metric subtotal | +102.24% | +99.88% |

The current more than cancels the reinforcing heavy energy on each cycle. A projected subtotal near 100% is not enough: it can still miss a component perpendicular to the net drift. Against the archived complex difference, keeping only heavy and metric misses by **2.25048%** and **0.99735%** (fine grid). Restoring ordinary work reduces those errors to 0.04550% and 0.15143%; restoring the prescribed geometric contribution as well gives the full forecast in the table. No term was selected or refitted after scoring.

## Checks and next use

All 48 archived endpoint comparisons, 72 field-basis replay comparisons, 192 numerical controls and 48 rate-identity checks pass. Over both boundary conventions and both subdivisions the largest endpoint error is 0.11087%; the largest numerical-control error is 0.10017%. Detailed outputs: [comparisons](evidence-001.zip) (archive member: `gates.csv`), [numerical controls](evidence-001.zip) (archive member: `controls.csv`), [rate identities](evidence-001.zip) (archive member: `rate-identities.csv`), [signed contributions](evidence-001.zip) (archive member: `contributions.csv`), [term-removal diagnostic](evidence-001.zip) (archive member: `pair-only-diagnostic.csv`).

This measures drift on saved histories, not its transfer to observed light. Next: project the frozen complete-cycle drifts (2, 3, 4) through the saved photon weighting with each branch's own normalization, and compare with the saved signed photon contribution at both gravity steps. Keep the first cycle, within-cycle oscillations and the incomplete final cycle separate; do not tune an amplitude or alter the existing photon result.
