> Public reading copy: local links are mapped to released material or marked unavailable. Machine-specific passages, where present, have been omitted. See the inventory for the original digest.

# The occupied galactic wave has a calculable pulsar signal; most of it looks like ordinary clock or spin drift

21 November 2026 · Private forecast with real sightlines, observing times, timing designs and noise settings · No measured timing residuals opened for scoring

**What changed.** The LMC wave is no longer being tested only on hypothetical light screens. We derived its leading timing signal from its oscillatory pressure and the free-falling Earth and pulsar clocks, integrated the curvature down all 26 saved binary-pulsar directions, and projected the result through two actual observing programs. The original force bands, occupations and couplings are unchanged. GR with the same scalar and preparation is an exact matched control at this order; comparison with a stationary smooth host tests the presence of coherent oscillating stress, not the name of the gravitational theory.

**Field scale.** The two specific prepared grounds imply a cycle-averaged scalar density at the saved Solar position of **0.595–0.598 GeV/cm³**, a terrestrial spatial-metric potential amplitude of approximately **1.05 × 10⁻¹³**, and an Earth-only timing amplitude of **36.0–36.2 μs** at a **68.36-year** period. These quantities follow from the saved wave normalization. They are not a measurement of Galactic occupation or a universal MTS prediction for every halo. The clock and line terms of a uniform lapse cancel, but a real oscillating pressure has curvature and is sampled at different events.

**Across the 26 real directions**, nominal coherent total peak amplitudes are **4.38–79.20 μs** over the two grounds and six history alternatives, including the undriven ground. The LMC-driven difference alone is **0.110–2.835 μs** before timing fits. The complete curvature integral differs from the Earth-minus-pulsar endpoint approximation by **1.16–32.33 ns** in the complex total residual (up to 0.0472%). The largest uncertainty is not this correction: one quoted distance error corresponds to **0.30–420 radians** of emission phase across the sample. The light wavelength is 20.96 pc; do not tune an emission phase to match an observed residual.

### Two actual timing designs

These packaged EPTA series are distinct from the earlier 24.46-year cadence-only J1713 test. Numbers below use the reference ground at the nominal catalogue distance and RMS over the unknown starting phase. Nanoseconds after the fit are physical waveform RMS using the same formal-uncertainty weights for readability; the final S/N uses the correlated covariance itself.

| Pulsar | Data span / arrival times / fit rank | Before fit | Formal-error-only fit | Fixed correlated-noise fit | Conditional optimal S/N, phase RMS |
|---|---:|---:|---:|---:|---:|
| J1713+0747 | 10.11 yr / 4,539 / 66 | 32.59 μs | 46.2 ns | 149.0 ns | 1.54 |
| J0613−0200 | 11.01 yr / 2,260 / 73 | 41.33 μs | 76.4 ns | 327.1 ns | 0.51 |

The timing design contains offset, spin and spin-down as well as the other released columns. Correlated-noise weighting can leave *more* physical signal while assigning it *less* statistical weight. The LMC-driven change by itself leaves only **3.5–5.3 ns** for J1713 and **7.9–11.9 ns** for J0613 in the correlated fit. A number-diagonal ensemble has no coherent mean waveform to which those numbers could be applied.

### The test that matters most

Allow both pulsars one common absolute phase, not two separately optimized phases. At the nominal distances the most favorable two-pulsar conditional S/N is **2.17–2.20** across the total preparations. If an arbitrary common terrestrial sine/cosine at the same frequency is also allowed, that drops to **0.851–0.864**, even for the most favorable phase. A pure common Earth tone disappears in that control. The LMC-induced difference alone has a best-phase S/N of only **0.021–0.031** after clock removal. Scanning the two distance-error intervals produces 25,315 distance pairs per state; the **phase-RMS** total clock-cleaned S/N ranges from 0.078 to 0.620 on that grid. This last range is a sensitivity scan, not an observational posterior bound or a maximum over the absolute phase.

**Verdict:** these two short-baseline series on their own are a poor discriminator of the LMC-induced wave. The prepared *whole* halo is the more promising falsification target. Its high occupation deserves scrutiny: [Smarra et al.](https://arxiv.org/abs/2306.16228) report density constraints in a nearby mass range beginning at approximately 10⁻²⁴ eV. Our retained 9.586 × 10⁻²⁵ eV pole is about 4.14% below that quoted lower edge. The published headline neither excludes nor clears this preparation. A test at this mass must also match the assumed coherence, noise and spatial profile. Nothing here has been fitted or detected in the timing residuals.

### Verification and next test

- 728/728 nominal complex timing-amplitude comparisons pass the original 20-ppm gate under spatial refinement and independent modal-basis/time refinement; worst difference is 0.239 ppm. An analytic finite-momentum relativistic stress check and a separate clock/Doppler/line-integral identity check fix the curvature normalization and signs.
- Distance averages are not silently accepted: the first trapezoidal half-grid check exceeds 20 ppm for 196/364 summaries. Simpson integration on the same saved evaluations passes all **364/364**, worst 14.78 ppm. The reported sampled extrema are not certified continuum extrema.
- Each pilot has 256 synthetic signal/noise recovery trials. Nominal 95% ellipse coverage was **93.36%** and **95.31%**, respectively; noiseless quadrature recovery error is below 4.3 × 10⁻¹⁶ s. Dense submatrix inversion independently checks whitening to 2.6 × 10⁻¹³ relative. These checks validate a *fixed* noise model, not uncertainty in those noise parameters or unmodelled correlated signals.
- [Derivation, conventions and limitations](DERIVATION.md) · pressure scale (not bundled here) · 26 sightlines (not bundled here) · distance scan (not bundled here) · actual fit transfer (not bundled here) · correlated single-pulsar forecasts (not bundled here) · [two-pulsar clock control](evidence-001.zip) (archive member: `clock-control.csv`) · injection recovery (not bundled here). Provenance: geometry acquisition (not bundled here) and design-only input receipt (not bundled here). Run `python -B verify_timing.py` for read-only, single-worker offline replay; no fetching or telescope residual files required.

**Next:** before reading real residuals, freeze a wider array test at the retained pole using *every* overlap with the saved geometry, not the pair with the highest expected S/N. Compare long and short baselines without double-counting shared observations. Test coherent MTS, identical GR-plus-scalar, incoherent-mean and pure terrestrial-clock injections against common red noise and realistic distance uncertainty. If the clock-cleaned array has appreciable sensitivity, carry that predeclared comparison to the actual residuals; if it does not, report the achievable occupation sensitivity rather than fitting the halo to noise.
