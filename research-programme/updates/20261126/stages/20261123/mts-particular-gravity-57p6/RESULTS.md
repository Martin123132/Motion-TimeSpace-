> Public reading copy: local links are mapped to released material or marked unavailable. Machine-specific passages, where present, have been omitted. See the inventory for the original digest.

# 51.2–57.6 conformal Mpc: the window rises while the peak keeps falling

23 November 2026 · Private · Longest frozen wave (4,2,1), k = 0.3368801156243423 per comoving Mpc. The fifth source interval reverses the last interval's direction for the **total** last-scattering window RMS, but not at the visibility peak. On its own it produces a slightly larger window response than the fourth (1.4338% vs 1.3769% of launch). No phase, amplitude or window was fitted.

| Joint photon energy/current, MTS minus cold baseline | Window RMS | Common visibility peak |
|---|---:|---:|
| Previous signed sum, particular gravity through 51.2 | 3.4519% | 1.2727% |
| Fifth interval alone | 1.4338% | 0.5724% |
| New signed sum, particular gravity through 57.6 | **3.8103%** | **1.1147%** |
| Change (percentage points) | **+0.3584** | **−0.1580** |

All percentages in this table refer to the original joint energy/current **launch difference** (norm 1.8923589891767267e-12). Energy and current are compared at equal scale factors for the two models. The window spans 750 ≤ z ≤ 1500 and uses the same normalized cold visibility times the conformal-time weight. The source coverage ends at 57.6, not the photon readout. These are predictions for one mode; they are not percentages of observed microwave sky power.

## Two different cancellations

- **Against the full signal** already present, the new interval is almost orthogonal across the window (alignment +0.0553) and partly opposed at the peak (−0.4838). Adding the complex energy and current before taking their magnitude explains the two different signs.
- **Against the previous four matter-source intervals alone**, the fifth points strongly the other way: −0.9135 across the window, −0.8102 at peak. Their window sum falls from 1.9580% to 0.8722% of launch even while the total signal rises. The five individual magnitudes sum to 6.6245%, so their signed sum retains just **13.17%** of that value (12.20% at peak). This is cancellation of field amplitudes, not an energy-loss fraction. The calculation reproduces the sealed four-interval result before adding the fifth.
- Subtracting freely propagated photons from the entire history, which leaves the regular drive as well as the five particular intervals, gives a net driven contrast of 0.9527% of launch across the window and 0.6060% at peak. A small net value does not bound uncomputed later forcing.

## What was checked

1. Continued the two saved -p4 material states, the common incident histories and all 154 finite-momentum endpoints with the original angular and momentum grids. Reused the 17 overlapping native time samples; they are not independent checks. Source joins agreed below 2.7e-16 relative; direct incident-flight/projection controls agreed within 7e-16 on three test bins per model.
2. Tested gravity **before opening photon scores**. Doubling the inner step from 0.0015625 to 0.003125 conformal Mpc at fixed converged stress changed the signed potential, lapse and potential derivative by 0.4047%, 0.3954% and 0.0855% of their respective peaks. The independently differentiated potential agreed with the signed constraint derivative to 0.2003%. The potential step check has increased from 0.1202% to 0.2370% to 0.4047% over three intervals; the preset gate is still 0.5%.
3. All 27 propagation comparisons plus six fixed-stress end-to-end comparisons passed at window and peak. The isolated fifth signal was zero before its source interval. Under five matched settings assembled across all intervals, the signed window change was +0.3567 to +0.3584 percentage points and the peak change −0.1590 to −0.1580 (rounded). The maximum sensitivity of the total signed history to these joint variants was 0.0234% RMS and 0.0331% at peak. Previous cumulative results were reproduced for every numerical setting before scoring its increment. These ranges test the numerical implementation, not observational uncertainty.

[Per-model results](evidence-001.zip) (archive member: `results-p4.csv`) · [full-signal alignment](evidence-001.zip) (archive member: `interference-p4.csv`) · [fifth vs earlier four](evidence-001.zip) (archive member: `fifth-versus-four.csv`) · [five-interval coherence](evidence-001.zip) (archive member: `five-interval-coherence.csv`) · [total minus free](evidence-001.zip) (archive member: `net-drive-versus-free.csv`) · [control signs](evidence-001.zip) (archive member: `direction-under-paired-controls.csv`) · [all-interval sensitivity](evidence-001.zip) (archive member: `all-five-blocks-control.csv`) · [gravity gate](evidence-001.zip) (archive member: `pre-transport-gate.json`) · [photon controls](evidence-001.zip) (archive member: `controls-p4.csv`) · [material step propagated](evidence-001.zip) (archive member: `frozen-stress-step-propagated.csv`) · [frozen protocol](PROTOCOL.md).

**Next manual test:** isolate 57.6–64.0 Mpc using the new particular-cold-p4.npz, particular-heavy-p4.npz, common and per-bin endpoints. Start with half the current inner step for both models (0.00078125 Mpc) and check it against 0.0015625 at fixed stress before scoring photons. Keep the bank, physical source sampling, phases and tolerances unchanged. No background job, fit or publication. Use verify57.py with Python 3.13 and bytecode disabled to verify the saved stage.
