# A microscopic replay finds the right averaging clock for the matched wave

**Result.** Starting only from the pre-switch field and its velocity, density and momentum are recoverable on the averaged branch's own saved metric. The old projection appeared to reject the pressure of every mode. Enforcing the *existing* phase equation on that same metric removes the bulk of the discrepancy. A stricter comparison still distinguishes the reconstructed wave from its approximate fluid pressure for 43 of 782 modes. No new current was fed to photons.

## What was predicted and frozen

The launch was η=88.4 conformal Mpc; no reset at η=89.1485038. The resolved and matched trajectories have effectively identical pre-switch initial fields (maximum difference 3.56e−8% of their preparation scales), but use their own metric, expansion and mass histories thereafter. Metric forcing came from the constraint, not the later heavy stress. All ten driving/diagnostic metric columns agree exactly across the early/late cache overlap. The cold-tracer derivative recovers the independent metric forcing to 0.000152% or better. The worst time-step change across the four evolved variables was 0.000027%. One-sided interpolation at the switch was retained. The matched and resolved tags here are two heavy-field descriptions, not two new fits or a replacement for the baseline cosmology.

On the resolved control, all 782 later fields and conformal velocities reproduce their native histories within 0.000017% of the per-mode peaks. The independent bilinear current on five output wavenumbers is within 0.000403% and its rate within 0.000392%. The matched conditional current changes by at most 0.00570% of the corresponding resolved-current peak over 89.65–90.4, **not** a percentage of the photon gap. The matched bank's post-switch field columns really are blank. No blank was used as a physical state. Homogeneous replay differs from the interpolated table on the matched route by up to 0.00652%, on the resolved route by 0.000133%.

## Why the pressure changed

The background generator defines dθ/d ln a=m/H_phys. Therefore θ′=am in conformal time. Evaluating a phase table prepared on a different expansion history does not in general obey that same equation. On the matched branch the rate discrepancy is only 0.00640%, but pressure is a small difference between two large oscillating terms. We kept the same microscopic fields and integrated am from the saved pre-switch clock, with no adjustable phase. This clock comparison was proposed after seeing the original pressure failure, then frozen before scoring; it is a mechanism test on existing data, not a held-out observational result.

All 31 fully supported post-switch six-π centers span 89.70625–89.89375 Mpc. There is **no** centered pressure measurement at 90.4 in this packet. The resolved projection at the switch itself agrees with the retained table in density, pressure and current to 7.77e−7, 1.70e−8 and 1.49e−8 of the inherited mode norm respectively. A centered projection *at* the switch mixes pre/post histories and is kept separate from the 31 centers wholly on the new branch.

| Test on the matched branch | Phase table evaluated at matched scale | Phase integrated on matched branch |
|---|---:|---:|
| Worst density error, per-mode peak | 0.02422% | 0.02456% |
| Worst momentum error, per-mode peak | 0.02524% | 0.00520% |
| Median pressure error, per-mode peak | 28.31% | 0.07283% |
| Worst rest-pressure residual, fraction of inherited mode norm (gate 2e−6) | 5.26e−5 | 2.47e−7 |
| Modes missing the rest-pressure gate | 782 | 0 |
| Modes missing the independent pressure-on-its-own-peak gate (0.5%) | 782 | 43 |

All four width/degree/sampling variants select the same 43 pressure failures. Worst is k=1.79619257 Mpc⁻¹, at 89.70625: projected microscopic pressure 6.40548e−6 versus fluid pressure 5.96877e−6 in matching-density units, a 7.317% discrepancy on this mode's native pressure peak. The RMS difference between the two branches' projected pressures with their own clocks is 0.0522% of the difference found with the old clocks. This is not a 99.95% reduction of the photon error.

## An independent check on the surviving discrepancy

Differentiating the mixed field–velocity product gives the pressure identity in PRESSURE.md. Its ninth-degree numerical derivative reproduces the directly projected kinetic-minus-potential pressure within 0.0510% on every matched mode (resolved: 0.00163%); degree seven misses two small-pressure modes. The original fluid pressure itself is reproduced from its own density and momentum to 5.13e−8%. On the 43 failing modes, substituting the reconstructed density and momentum into the *unchanged* fluid law changes pressure by just 0.049% of the RMS discrepancy. The residual therefore is not fixed by better initial density or momentum alone. The mixed-envelope derivative, expansion, rest-frame and metric-work terms partly cancel; their signed contributions are in pressure-scores.json. This is a decomposition conditional on these histories, not a measurement of a new coupling.

**Next test:** evolve the slow mixed-field envelope and the metric-work term from an early center, rather than reading their derivatives from later microscopic samples. Freeze the predicted pressure correction on both preparations and check later supported centers, including the same 43 modes. The older joint photon result at 90.4 remains 0.65971% of the original small correction against 0.5%; it was not rerun. Do not use the conditional bilinear current as a signed matched source until the stress gate is resolved.

## Reproduction

The previous energy-stage seal is pinned in state_io.py. The local order is predict.py, replay_score.py, branch_clock.py, pressure_balance.py, verify.py. The first scorer stopped on Python list absolute-value bookkeeping, after both forecasts had already been frozen; replay_score.py changes only that one expression to elementwise array absolute value without touching the original scorer or rerunning the forecasts. forecast.json, clock-forecast.json and pressure-forecast.json identify the frozen products. mode-pressure-ledger.csv provides all mode-level pressure exceptions and successes. All results are private calculations using the existing bank and thresholds, not telescope data.
