> Public reading copy: local links are mapped to released material or marked unavailable. Machine-specific passages, where present, have been omitted. See the inventory for the original digest.

# The peak energy cancellation is real, but it is not the full-window result

24 November 2026 · local research · physical scattering · one retained mode, k = 0.3368801156 per conformal Mpc.

**Question.** Compared with the first two post-64 matter intervals (64–76.8 Mpc), what changes when the measured third interval (76.8–83.2 Mpc) is added? At the visibility peak it reduces the magnitude of the photon energy contrast and increases the current contrast. Over the finite emission window the MTS-minus-baseline **RMS magnitudes both grow**.

| MTS minus baseline, finer gravity step | First two (% of launch) | Third alone (% of launch) | All three (% of launch) | All three / first two, window | Same ratio, peak |
|---|---:|---:|---:|---:|---:|
| Energy | 2.54808 | 1.60898 | 2.76158 | 1.08379 | 0.44340 |
| Current | 1.36672 | 0.86414 | 1.50097 | 1.09822 | 14.04973 |
| Joint | 2.89147 | 1.82635 | 3.14312 | 1.08703 | 0.65906 |

Each percentage uses the same original paired joint launch norm (1.8923589892e-12); it is not a percent of sky power, an observed CMB discrepancy, or a full prediction with all sources. The baseline and MTS were evolved separately with their own physical scattering coefficients. For the baseline alone the ratios (energy, current, joint) are 1.25032, 1.26289, 1.25316; for MTS alone they are 1.28841, 1.30039, 1.29112. Subtracting these ratios would not give the paired result.

**Why the sign changes.** The third energy response is nearly opposite the earlier response at the peak, but their normalized real inner product across the window is only −0.17747 (current −0.15315). The negative cross term therefore takes away less power than the third interval adds. In visibility-weighted measure, energy is reduced 47.11% of the time, current is increased 54.95%, and **both happen together on 32.81%**. Current exceeds energy in magnitude after adding the third interval on 43.95% of the weight, but energy is larger by RMS. Current growth and current dominance are different statements. The 14-fold peak current ratio used a particularly small first-two current denominator.

**Calculation.** On the original common scale-factor grid we add the complex contributions of the two forcing channels and the selected intervals. We form the heavy-minus-cold difference at equal scale factor before taking magnitudes. We then use the archived baseline visibility measure (normalized over 750 ≤ z ≤ 1500), not a separately retimed peak for each branch. RMS² is the integral of squared modulus against that measure; joint RMS² is the sum of energy and current RMS². Fractions of the window integrate visibility weight, splitting cells at interpolated sign changes. The common peak is at z = 1089.17. Contributions outside the three source intervals are excluded to isolate their response; this does not set physical gravity to zero there.

**Checks.** All 1,245 comparisons passed the original 0.5% gate (absolute probability for support fractions). The p16/p32 shift in the complex all-three paired history is 0.00556% of its joint RMS; the worst gravity comparison over channels, spans and branches is 0.02673%. Earlier peak values are reproduced against the sealed adjoints to within 1.02e-11 relative. Doubling the visibility quadrature from 8,193 to 16,385 points changes RMS by at most 1.10e-14 relative and support by at most 0.00076 percentage points. The signed-interference identity and independent archived norm implementation agree as well. [Readouts](evidence-001.zip) (archive member: `window-rms.csv`) · [Peak versus window](evidence-001.zip) (archive member: `peak-vs-window.csv`) · [Weighted support](evidence-001.zip) (archive member: `visibility-support.csv`) · [Checks](evidence-001.zip) (archive member: `checks.csv`) · [Previous peak result](../mts-photon-peak-post64-three/RESULTS.md).

**Next:** combine the three saved histories at each epoch with the already saved photon history through 64 Mpc, held fixed and identified as such (not recomputed at p32). Compare the finite-window result before and after adding the three intervals. This tests whether the 8.70% isolated joint increase matters against the earlier background, without another matter integration. Physical matter coverage still ends at 83.2 Mpc.
