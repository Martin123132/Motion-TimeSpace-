> Public reading copy: local links are mapped to released material or marked unavailable. Machine-specific passages, where present, have been omitted. See the inventory for the original digest.

# Ten pulsars: sensitivity of the saved clock experiment

Private design-only check, 21 November 2026. No observed timing residuals were inspected. The [frozen protocol](PROTOCOL.md) uses all ten catalogue matches to the pinned EPTA release, 27,144 arrival times over an 11.016-year array span. Two designs were previously used in the pilot. The coherent scalar period is about 68 years.

| Primary reference ground + L2M10 | Result |
|---|---:|
| Independent simulated null trigger rate | 4.94% |
| Trigger rate with retained signal | 8.49% (Monte Carlo SE 0.15 percentage points) |
| Optimal benchmark supplied the signal phase and distances | 21.08% mean power |
| Analytic ceiling at 5% false alarms under these assumptions | 21.20% |
| Minimum information multiplier necessary for 80% oracle power | 8.65 |

The fixed-template test would need a 5.08-fold signal amplitude for 80% power; this is a sensitivity diagnostic, not permission to rescale the field or refit the occupation. See models and controls (not bundled here), [sharper analytic bound](evidence-001.zip) (archive member: `any-test-bound.csv`), and [derivation](DERIVATION.md). The LMC increment alone is much less accessible than the total prepared field. GR supplied with the identical minimally coupled scalar gives the same clock signal.

Sensitivity to the common red noise matters: at the upper modelled amplitude the nominal threshold falsely triggers about 11.7% of the time. A single conservative threshold of 1.98116 keeps the calculated false-alarm rate at or below 5% over the specified amplitude interval with other noise properties fixed. At nominal noise this gives 3.23% detection versus 1.60% false alarms; see noise interval (not bundled here). This does not establish calibration for arbitrary noise.

The independently simulated raw-arrival controls trigger on 9/192 nulls and 18/192 injected signals. The numerical comparison after halving the distance grid changes the signal by 1.38e-7 relative. For the two ground controls, coherently transported endpoint phases and independent endpoint phases differ by about 1.31e-6 in the whitened second moment with catalogue distance errors, but by about 46% with hypothetical 3.93 pc errors. This does not equate the full signal likelihoods. See raw injections (not bundled here), numerical controls (not bundled here) and [phase comparison](evidence-001.zip) (archive member: `coherence-control.csv`).

**Decision:** keep the measured residuals blind. A longer, independently evaluated timing design is a useful next sensitivity test; do not add overlapping releases as independent data. These results neither detect a field nor exclude it.
