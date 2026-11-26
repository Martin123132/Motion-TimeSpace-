> Public reading copy: local links are mapped to released material or marked unavailable. Machine-specific passages, where present, have been omitted. See the inventory for the original digest.

# The full-window photon discrepancy is predictable from the switch states and frozen later work

The first-cycle photon contribution accounts for **+12.10867%** along the saved fine-grid full discrepancy. Both branches start at 89.1485038031 conformal Mpc in their own switch states, and the first source ends at 89.2415903205. We kept the prehistory change in the matched initial condition but did not count the common kick as instantaneous work in the route difference. The full prediction through 89.6 Mpc contains no archived first-cycle or oscillatory photon contribution.

## What was frozen and tested

Both predictions include the newly predicted first cycle, the previously frozen drifts from cycles 2–4, and the previously frozen final partial-cycle source. The second prediction also includes a separate calculation of the zero-net oscillations in cycles 2–4. For that calculation, we evolved through the phase crossings without resetting either branch. On every complete later cycle we subtracted that branch's own raw mean work before applying its constraint denominator. That convention leaves the older frozen drifts unchanged. There is no mean subtraction or padding at either end of the window. Both full photon vectors on both gravity steps and all numerical settings were sealed before reading the comparison arrays. These are new calculations on retained histories with shared inputs, not a blind observational holdout.

| Joint readout | Predicted magnitude, coarse | Saved magnitude, coarse | Coarse vector error | Predicted magnitude, fine | Saved magnitude, fine | Fine vector error |
|---|---:|---:|---:|---:|---:|---:|
| First cycle | 0.08989224% | 0.08989123% | 0.00180448% | 0.08989317% | 0.08989314% | 0.00074192% |
| Entire window, without later oscillations | 0.57637635% | 0.57635063% | 0.12124145% | 0.57637979% | 0.57636165% | 0.12122223% |
| Entire window, including predicted oscillations | 0.57635796% | 0.57635063% | 0.00140805% | 0.57636149% | 0.57636165% | 0.00003215% |

Magnitudes use the original small momentum-route signal as the common scale. Errors subtract complex energy and current vectors before applying the visibility-weighted norm, then divide by the corresponding saved vector's magnitude. The fine full-window **energy** and **current** vector errors are 0.00003218% and 0.00003206% respectively. The full prediction differs by 0.000738% between the two gravity steps. Even the small complete-cycle oscillation signal passes on its own scale: 0.0008863% fine vector error. At the fine step its joint magnitude is 0.00069868% of the common scale; its signed projection along the full gap is only −0.00310% of that gap. This explains why adding the oscillations helps the vector prediction much more than it changes the magnitude.

## Common entry kick and physical checks

The change in matched starting potential from prehistory is already in the launch state. The matched-minus-wave potential offset agrees with original plus preparation kick to better than 1e−11% on both gravity grids. Kept as a separate photon contribution, the common kick has a fine joint magnitude of 0.01864446% of the original launch. Adding it equally to the momentum and differentiated routes and then subtracting recovers the predicted discrepancy within 7e−12% on the primary grids. This cancellation does not mean the starting states or their subsequent dynamics are equal.

The two fine physical route sizes are 0.01901930% and 0.01904003% of the original launch, both within their separate 0.163% size gate. But the fine full gap itself is **0.57636149%** of the original momentum-route signal, above the unchanged **0.5%** physical agreement criterion. Successful reconstruction and actual route agreement answer different questions.

## Verification and next target

All 48 archived photon-vector comparisons, 153 numerical checks and eight branch raw first-cycle endpoint checks pass the 0.5% accuracy tolerance. The primary and angular-check photon arrays are byte-identical here; do not count them as independent evidence. The controls also check that the same frozen drift and partial-cycle photons add linearly to the new first-cycle photon vector. No fit, new interval, restart promotion or publication.

**Next:** use the heavy-current and metric work equations to derive a correction to the averaged branch, using only inputs available to that branch; freeze it before comparison with the native wave. The necessary joint change on the fine grid is at least 0.07636 percentage points on the original common scale (13.25% of the current gap); a correction of that magnitude in the wrong direction will not suffice. Keep the first-cycle and late-window readouts separate to show where a proposed correction helps or harms. Do not use the measured residual as the correction.

[Protocol](PROTOCOL.md) · [switch inputs](evidence-001.zip) (archive member: `launches.csv`) · source freeze (not bundled here) · full photon freeze (not bundled here) · [energy/current comparisons](evidence-001.zip) (archive member: `comparisons.csv`) · raw branch endpoints (not bundled here) · [signed contributions](evidence-001.zip) (archive member: `readouts.csv`) · [kick audit](evidence-001.zip) (archive member: `common-kick.csv`) · [physical gates](evidence-001.zip) (archive member: `physical-gates.csv`) · [numerical checks](evidence-001.zip) (archive member: `numerics.csv`).
