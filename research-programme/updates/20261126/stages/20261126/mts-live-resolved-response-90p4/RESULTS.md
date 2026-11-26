> Public reading copy: local links are mapped to released material or marked unavailable. Machine-specific passages, where present, have been omitted. See the inventory for the original digest.

# Predicting the two gravity routes’ photon disagreement from the incoming state

**Window:** 89.65–90.4 conformal Mpc. This is a comparison against saved numerical histories, not an observational fit. The question was whether repairing the first-order forcing alone made the two existing gravity routes agree on the later photons, and, if not, whether their disagreement could be predicted from the equations.

## Physical test

Both grids carried their own incoming resolved states through 15 adjoining tiles. Radiation, ordinary species, gravity, both scalar sectors, 77 bins and the spectral shape responded together. Only the specified repaired-minus-original first-order driving terms changed; the homogeneous coefficients of the second-order evolution did not. The matched solution remained independently prepared. The original-forcing controls reproduced the archived histories. See [protocol](PROTOCOL.md) and [photon transfer](TRANSFER.md).

| Fine forcing, primary photon transfer | p16 | p32 |
|---|---:|---:|
| Energy gap, % of original small correction | 0.655258 | 0.655268 |
| Current gap, same scale | 0.654699 | 0.654711 |
| Joint gap, same scale (target 0.5%) | 0.655133 | 0.655144 |
| Frozen diagnostic error, % of actual joint gap vector | 0.008674 | 0.010821 |

The original p32 joint gap was 0.659708%. The repaired p32 routes are only 0.018391% and 0.018381% on the separate full-launch scale (limit 0.163%). Passing that limit does not erase the small-correction miss. Including the optional complex entry term gives 0.655239% on p32. The direct seven-way source/state decomposition and the resolution variants are in [scores](evidence-001.zip) (archive member: `scores.json`). This intervention’s bin response has a very small direct photon projection, not evidence that bins can be removed.

## What explains the miss?

On the momentum-route orbit, let r be the stored curvature potential minus the density-constraint reconstruction on that *same* state. An equation for r using the given sources alone predicts the **change** under the repair accurately but misses the **absolute** drift. The missing state-dependent term has an explicit [transverse row](HEAVY-ROW.md). Two measured defects of the archived homogeneous heavy field, the difference between its tabulated derivative and velocity and the residual of its velocity equation, account for approximately 45.6% and 54.5% of the omitted signed work on the p32 control. Those are shares of the missing constraint work, **not** of the photon gap. Small terms have opposing signs. [Full work accounting](evidence-001.zip) (archive member: `work-scores.json`).

A reduced forecast evolved the heavy field, velocity and stored curvature from their incoming values. Continuing the other variables to first order from launch predicted the measured constraint drift to within 0.0081% across all six histories. This uses the time-dependent forcing and coefficients of the experiment; it is not a prediction without those inputs. [Test](THREE-STATE.md) · [scores](evidence-001.zip) (archive member: `three-scores.json`).

Next, the [two-route response identity](RESPONSE-IDENTITY.md) propagates this predicted residual into the difference of the density and momentum orbits and then through scattering. Absolute tests retain the inherited route difference; repaired-minus-control tests start from zero change. No later resolved state is supplied to this diagnostic forecast. On p32, the fine-table joint photon gap was predicted as **0.655142%** versus **0.655144%** measured. The error in the energy-and-current vector, not just its magnitude, was **0.010821% of the measured gap**; across all six absolute cases it was below 0.011%. The four repaired-minus-control joint vectors were predicted to within 0.00024% of their own sizes. [Frozen predictions and comparisons](evidence-001.zip) (archive member: `gap-photon-scores.json`). These tests locate a numerical/theoretical inconsistency inside the retained calculation; predicting it is not fixing it.

**Next physical test:** carry the independently evolved heavy homogeneous field and velocity into the second-order coefficients on both grids. Construct the corresponding common-metric background terms consistently, quantify any remaining clock/enthalpy residuals rather than setting them to zero, and predict the photon energy and current again. Keep the same incoming states, matched control, normalization and thresholds; do not subtract the diagnosed gap by hand.
