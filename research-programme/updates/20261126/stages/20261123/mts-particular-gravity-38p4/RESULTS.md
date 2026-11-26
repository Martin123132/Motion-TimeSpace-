> Public reading copy: local links are mapped to released material or marked unavailable. Machine-specific passages, where present, have been omitted. See the inventory for the original digest.

# A second interval pulls the peak and the wider window in different directions

23 November 2026. Private numerical continuation; longest frozen output wave (4,2,1), k=0.3368801156243423 per comoving Mpc. Only the added matter-sourced gravitational force from 32 to 38.4 conformal Mpc is measured here. The original launch amplitudes, 77 momentum bins, background preparations, comparison window and 0.5% numerical tolerance are unchanged.

| MTS minus cold baseline | Joint photon energy/current RMS, 750 ≤ z ≤ 1500 | At the common visibility peak |
|---|---:|---:|
| Previous sum through 32 | 4.4323% | 1.6222% |
| New 32–38.4 source alone | 1.3049% | 0.7175% |
| Signed sum through 38.4 | **4.3884%** | **2.0307%** |
| Change in the sum (percentage points) | **−0.0439** | **+0.4085** |

Every entry is normalized to the same magnitude of the original joint MTS-minus-cold launch difference (1.8923589891767267e-12), **not** to the observed microwave background. The common window uses the normalized cold visibility weighted by conformal time at matched scale factors. This is a prediction for one wave with the particular driving included only through the specified time, not an observed sky spectrum.

## Why the signs differ

The phase and sign of the complex energy and current were retained before taking the magnitude. On its own the new interval has energy RMS 1.1514% and current RMS 0.6142% of launch, combined in quadrature. Its alignment with the **entire preceding signal** is −0.1807 across the window but +0.4200 at peak; hence partial cancellation in the first reading and reinforcement in the second. With **just the preceding matter-sourced block** its alignment is positive in both readings (+0.5009 and +0.8789). These statements can coexist because the entire earlier signal also includes the launched photons and regular gravitational driving. The aperture and phases were not moved. Each branch alone grows slightly across the window (cold 4.1364% → 4.1959%, MTS 4.1318% → 4.1987%, each relative to its own launch).

## Checks and coverage

- Restarted both coupled fields, spectral shape and all 154 finite-momentum incident histories from their individually verified 32 Mpc endpoints. Reused the 17 overlapping padded native samples instead of counting copied values as independent evidence. The incident source joins differ by less than 2e-16 of their references. Independent evolution and contraction for the slow, middle and fast check bins agree within 7e-16.
- Returned four stresses to the two gravity solutions. Both converged at the second evaluation. The two ways of obtaining the signed curvature derivative agree to 0.0818% of its own peak on a shared scale-factor grid. Doubling the inner material step at fixed stress changes the signed potential, lapse and potential derivative by 0.4813%, 0.4606% and 0.0658%. The first is close to the **unchanged 0.5% gate**; no increasing-step extrapolation is justified.
- The new force acts only on 32–38.4. The new photon response vanishes at saved readouts before this interval, and the verifier checks that the old complex sum is included exactly once. All 27 propagation comparisons and six further fixed-stress step comparisons pass for cold, MTS and their difference at both window and peak. The largest fixed-stress step shift in the isolated contrast is 0.221% RMS, 0.218% at peak.
- As a separate sign check, repeated the comparison using like-for-like variants of **both** adjacent intervals, keeping the still earlier photon and regular component fixed. Across the five numerical settings the window change ranges from −0.04392 to −0.04231 percentage points, the peak from +0.40853 to +0.40989. These ranges are numerical sensitivities, not confidence intervals or independent observations.

[By branch and component](evidence-001.zip) (archive member: `results-p2.csv`) · [adjacent blocks](evidence-001.zip) (archive member: `adjacent-blocks.csv`) · [alignment with previous total](evidence-001.zip) (archive member: `interference-p2.csv`) · [paired sign sensitivity](evidence-001.zip) (archive member: `direction-under-paired-controls.csv`) · [metric time-step comparisons](evidence-001.zip) (archive member: `matched-step-check.csv`) · [transport checks](evidence-001.zip) (archive member: `controls-p2.csv`) · [propagated material-step checks](evidence-001.zip) (archive member: `frozen-stress-step-propagated.csv`) · [frozen scope](PROTOCOL.md)

**Next manual test:** start both preparations at the saved 38.4 endpoint and isolate 38.4–44.8. Check the material time step against its half-step on the signed contrast first, then score the isolated interval and its contribution to the whole signal. Do not assume either sign repeats. The verified restarts are particular-cold-p2.npz and particular-heavy-p2.npz plus the per-bin micro-* and common-* endpoints. Use verify38.py with Python 3.13 and bytecode disabled to check the saved manifest.
