# What produced the first photon discrepancy?

The incoming MTS wave, the retained phase-average table and the Einstein constraints predict the sign and nearly the entire size of the exposed first-cell photon signal. The immediate cause is a change in the heavy **stress used by gravity** when the code swaps descriptions at a fixed scale factor. No microscopic kick to the wave or coupling inferred from photon data is needed to reproduce that signal. This is a diagnostic of a numerical model transition, not evidence for a new radiation component in the sky.

## First predict the switch, then sample it

At 89.1485038031 conformal Mpc, use the incoming field and normal momentum and the independently prepared mean density/current. Reconstruct the change of shear and spatial potential from the scalar Einstein constraints. Propagate that change through the same quadratic heavy energy/current operator on the five original output modes. See DYNAMICS.md, PROTOCOL.md and forecast-freeze.json. Fresh native samples on both sides came **after** the first freeze.

- All ten signed complex energy/current jumps pass 0.5% on their own magnitudes. Worst energy error 0.0899%, worst current error 0.3653%. Using just the density or just the momentum misses their cancellation.
- The switch leaves the other evolution slots untouched. The gauge-invariant spatial potential changes by only 0.001095% of its incoming peak; the trace-free curvature jump clears ten times the sampling spread on 782/782 inputs. Two-sided estimates at the same scale and time give consistent results. The saved cold control, which has no heavy switch, shows apparent potential and shear/time-shift jumps below 0.000007% of the corresponding MTS peaks.
- The initial forecast misses the smallest individual shear/curvature jumps on 100/782 modes. A **diagnostic follow-up**, using only pre-switch rows from the same native matched integration and the specified scale instead of borrowing the resolved incoming state, passes all 782: worst shear error 0.05173%, worst spatial-potential error 0.000362%. This follow-up clarifies preparation sensitivity; it is not a new blind event test. Matched post-switch zeros in the field output are a storage convention, not evidence that the wave disappeared. Post-switch quadratic stress in this comparison is conditional on continuing the coherent field.
- The abrupt change is not removable by simply choosing a new time label on one side of a no-layer physical junction. The published matching conditions and the scope of this inference are given in DYNAMICS.md. It is the literal instantaneous interpretation with fixed surrounding data which fails, not every effective averaging procedure.

## The first cell and the photons

Carry the mean and the **conserved omitted moments** from the same incoming state to the next two saved times. The associated background residual is included. On both common-metric routes the separate residual evolution reproduces the coherent energy/current identities to better than 3e−10% of the corresponding residual peak. This is an identity check, not an autonomous fluid closure. Surrounding sources for the new short prediction are continued from the left only. Compare against the stored, independently evolved conditional sources, not a nonexistent post-switch native microscopic measurement.

| Test | 89.15000 Mpc | 89.15625 Mpc |
|---|---:|---:|
| Largest energy error on the matched-minus-wave contrast, five outputs | 0.18332% | 0.14798% |
| Largest current error on that contrast | **0.74925% (one miss)** | 0.11709% |
| Peak error of shear/time-shift contrast | **0.73468%** | 0.10356% |

Small individual metric contrasts have additional failures; see cell-tests.json. Changing the degree of the incoming surrounding-source extrapolation barely changes the quadratic result. Using the older moment-inverted initial fields leaves the first-knot current miss in place (0.73123%). It should not be rounded into a pass.

Freeze the endpoint potential amplitudes from gravity and the new source calculation, then propagate a unit impulse through the unchanged scattering equation. Freeze the signed photon energy/current spectra **before** comparing with the saved first-cell history. The project was already aware of the old discrepancy. This is a prospective amplitude calculation within an exposed case, not a held-out observation. The two gravity grids share the endpoint amplitude; their saved distributed drives differ slightly.

| Gravity grid | Actual signed first-cell points | Predicted from the surface alone | Error on joint first-cell photon vector | With short source evolution |
|---|---:|---:|---:|---:|
| p16 | +32.50421 | +32.44642 | 0.19719% | 0.21921% |
| p32 | +32.49761 | +32.44615 | 0.18051% | 0.20196% |

Points are measured on the earlier small joint launch, with the original sign and projection; the percentages in the last two columns use the first-cell vector's own norm. All separate photon energy/current checks pass 0.5%, including the inverse-preparation control. Nothing was subtracted from the complete history: the exposed direct-substitution gap through 90.4 Mpc is still 35.27039% / 35.26530% (p16 / p32). Do not debit 32.50 signed points from a norm as though that were a corrected physical solution.

## A conservation condition and a way forward

Can we merely fade the oscillating energy and current into the mean together? **Not near this switch if only an isotropic pressure is free.** FADE.md derives the necessary condition W′D=0 on a common metric. D contains the normally omitted background enthalpy correction. Its peak contribution from that background term grows from negligible at the join to 22.1% and 93.8% of the total D peak at the next two times on the conserved route. At the join 780/782 modes exceed ten times both the preparation variation and sampling spread. These perturbation checks are not statistical confidence bounds.

If we relax just the fixed-current assumption, conservation predicts a causal equation for an extra current I, without fitting its sign, a coupling or a decay coefficient. For a prescribed weight and geometry, I′+(2H+k²/(3H))I=−k W′D/(3H). See CURRENT-CHANNEL.md. The required entry coefficient per unit change in weight agrees in sign on all 782 modes and in magnitude within 0.05176% of the independent sharp-switch shear inference with same-run incoming data. This tests the coefficient identity, **not the existence of this extra microscopic current**. The 36 manufactured conservation controls are checks of analytic moment rates on specified geometry, not simulations of a transition field.

**Next calculation:** use the *retained phase projector and its actual weights* on saved, resolved energy, pressure, current and metric forcing. Derive its commutator with the time derivative and the projected work correlations, including the scale/density normalization used by the matching table. Freeze their signed contributions on the first fully supported oscillation before checking the projected continuity/momentum residuals. The original centered preparation uses both sides of its phase center: label this test as reconstruction, not causal forecasting. Only if the source balance survives should a past-only realization be carried back through gravity and photons. Do not insert a freely chosen fade, compensating photon kick, or new galaxy parameter.

## Reproduction

forecast.py → event_capture.py (dedicated matched samples) and cell_prediction.py (incoming-only prediction) → score_event.py. photon_forecast.py → photon_test.py freezes the new spectra before scoring. incoming_only.py → score_cell.py; fade_test.py → current_channel.py; verify.py checks the receipts and outcome gates. Reuse the checked archives by default. Native capture is not required to verify the checkpoint. No change to the original bank, grids, tolerances, other research agents, or GitHub.
