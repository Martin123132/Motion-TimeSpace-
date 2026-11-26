> Public reading copy: local links are mapped to released material or marked unavailable. Machine-specific passages, where present, have been omitted. See the inventory for the original digest.

# The current–gravity feedback preserves the curvature improvement and passes the heavy-density test

The switch-launched wave now supplies the **only** heavy current in the metric equation. The updated metric acts back on the wave within each integration step; the old fluid current is neither carried nor added. The ordinary species and their angular responses evolve with the new metric. We did not retune the wave, alter the external stress, advance the production history, or use the native wave to set the prediction. This is a phase-resolved replacement inside the matched background, not a claim that a phase-blind fluid predicts its missing oscillations.

| Full 89.1485038031–89.6 conformal Mpc window; fine gravity / four subdivisions | Fine stress input | Coarse stress control |
|---|---:|---:|
| Previous averaged fluid: curvature RMS error vs resolved native response | 0.007816% | 0.009632% |
| Previous one-way current replacement: curvature error | 0.00092309% | 0.00122943% |
| **Recoupled curvature error** | **0.00092309%** | **0.00122943%** |
| Induced lapse error (shared supplied shear removed) | 0.00092435% | 0.00123137% |
| Previous averaged fluid: heavy-current error | 49.930% | 49.444% |
| **Recoupled heavy-current error** | **0.00002437%** | **0.00002441%** |
| Canonical heavy energy error | 0.02687% | 0.02719% |
| **Physical heavy-density perturbation error** (a²-weighted) | **0.04504%** | **0.04406%** |
| Physical heavy-pressure perturbation error (a²-weighted) | 0.00002712% | 0.00002783% |

The one-way and recoupled curvature histories differ by only 2.01 × 10⁻⁹% of the native curvature response on the primary run. This was not a convergence assumption. With both directions of feedback active the histories actually agree to that level. The two frozen stress inputs are numerical controls, not independent observations. All 192 source/clock/subdivision/window/channel comparisons pass the unchanged 0.5% gate (largest error 0.04506% rounded upward). No last-scattering or galaxy observable was rescored.

## The independent energy check

Writing A=(am)², v=b′, J=k²vf, and u=f′−v(Ψ+3Φ), the canonical E=v u+Ab f is not the physical density variable. The a²-weighted density and pressure perturbations are D=v(u+3vΦ)+Ab f and p=v(u+3vΦ)−Ab f. From the retained wave equations and background oscillator one obtains
- D′+H(D+3p)+J = 3v²Φ′,
- J′+2HJ = k²(p+v²Ψ).

Starting at zero, we integrated these two equations using the saved pressure, gravity and current as appropriate, **without using the later density as a source of its own prediction**. An integrating factor removes the target on the left. An alternative quadrature uses metric increments directly; a separate manufactured example checks sign and normalization. On primary fine stress the density balance reconstructs the recoupled density to 4.71 × 10⁻⁸%; the same test on the independently replayed native reference gives 0.01617%. Dropping metric work increases the full-window error to 92.59% on the primary forecast and 79.55% on the coarse-stress control. Across the 48 balance cases the two quadratures differ by at most 0.00174%. The forecast/reference density comparison is a separate, harder test; its 0.04504% error is not the balance residual.

## What remains in the reference and the curvature

A post-score diagnostic checked the background oscillator rather than treating the native residual as zero. For stored background functions define r_v=v′+2Hv+Ab and r_V=(Ab)′−2HAb−Av. Differentiating the actual products adds r_v(u+6vΦ)+r_V f to the density rate and k²r_v f to the current rate. Using these measured residuals only after scoring reduces the fine native density-balance discrepancy from 0.01617% to 1.58 × 10⁻⁷% (coarse stress: 0.01588% to 1.46 × 10⁻⁷%). The diagnostic reconstructed f using both current and potential energy without division by a crossed zero of v or b. The tiny matched residual is not improved by this correction. This identifies a mismatch between the stored native background functions and the ideal homogeneous-oscillator identities; it does not identify which upstream approximation produced it or change any primary score.

Separately, the curvature-budget attribution uses the native lapse only **after** the prediction is frozen. Integrating −(H_matched−H_native)Ψ_native with the matched damping explains 99.9994% of the projection along the remaining fine-source curvature error; subtracting that diagnostic leaves 0.00249% of the *error's own* RMS. The corresponding coarse-stress residual is 0.00217%. There is little reason to tune the heavy current to chase this remainder.

## Controls and restart

All 96 fixed-stress refinement comparisons pass (largest discrepancy 0.00001122%). A separate adaptive two-variable native replay on the sealed native metric reproduces the archived full-system native current to better than 3.4 × 10⁻⁹% on every grid and input. It provides the reference density; this is a numerical cross-check within the same field equations, not an external density measurement. Both nonzero histories and the exact-zero control used the same sealed input packets for corresponding runs. The first attempted protocol initialization encountered a local module-name collision before running any comparison; its receipt was retained and the executable names made unique before the successful freeze.

**Next:** test the other gravitational equation on these same histories: reconstruct the total energy and momentum source of the time-time Einstein constraint on each branch with a consistent density convention, including the imposed stress and ordinary matter. Compare its residual with the momentum-driven metric, and with the native residual, before extending the time window. That checks whether what now moves the metric correctly also sources it correctly.

[Predeclared protocol](PROTOCOL.md) · Frozen forecast (not bundled here) · [All response scores](evidence-001.zip) (archive member: `response-scores.csv`) · [Energy and current balances](evidence-001.zip) (archive member: `balance-checks.csv`) · [One-way vs recoupled](evidence-001.zip) (archive member: `curvature-comparison.csv`) · [Curvature attribution](evidence-001.zip) (archive member: `curvature-attribution.csv`) · [Native-background diagnostic](evidence-001.zip) (archive member: `background-residual.csv`) · [Fixed-input refinement](evidence-001.zip) (archive member: `clock-tests.csv`).

Reproduction with the same verified parent and a fresh sibling folder: recouple_stage.py, recouple_forecast.py, recouple_reference.py, recouple_score.py, background_residual.py, recouple_verify.py. Use the retained Python with -B and one numerical thread. Internal results only.
