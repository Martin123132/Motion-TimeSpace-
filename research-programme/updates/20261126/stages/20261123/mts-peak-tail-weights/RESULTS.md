> Public reading copy: local links are mapped to released material or marked unavailable. Machine-specific passages, where present, have been omitted. See the inventory for the original digest.

# Where late gravitational forcing could change the photon visibility peak
**Result: prioritize 256.00–277.85 conformal Mpc, particularly 268.82–277.85** (baseline clock, approximately redshift 1216 down to 1089). The saved visibility peak is at 277.89763 Mpc. For the retained longest mode and equal bounds on the magnitude of an unknown source in each time bin, the two main bins immediately before peak carry **60.13%** of the paired effective-current sensitivity and **59.50%** of the lapse sensitivity. The first bin after 64 carries only **1.19%** and **1.02%**, respectively. This ranks the response to a possible source, not when a physical MTS–baseline signal has already been found. A sufficiently large earlier source could still dominate.

| Baseline conformal Mpc | Effective current: share of whole paired gain | Lapse incl. shear: share |
|---|---:|---:|
| 64.00–76.85 | 1.19% | 1.02% |
| 243.22–256.00 | 7.93% | 10.83% |
| 256.00–268.82 | 18.27% | 25.61% |
| 268.82–277.85 | 41.87% | 33.89% |
| Cell containing peak plus later scoring-spline support | 0.39% | 0.18% |

The primary energy-rate and acceleration-potential kernels give similar rankings; the raw acceleration shares for the two leading bins are 25.78% and 33.64%. The sensitivity median is at 263.52–263.54 Mpc for effective current and 263.94–263.96 for lapse. The small post-peak weights belong to the archived cubic **score**, not propagation backward in physical time.

## What the 0.5% budget asks of matter
The unchanged absolute allowance is \(1.4013360\times10^{-16}\), i.e. 0.005 of the retained two-component peak contrast \(2.8026721\times10^{-14}\). On the existing matter branch define
\[
Y=\Psi=(U-E/2-3{\cal H}_m J/(2k^2))/d+(\Pi-Q)/k^2,\qquad
C=J/(2k^2)+F_q+({\cal H}_r-{\cal H}_m)\Psi,\qquad
\Phi'=C-{\cal H}_rY .
\]
Here \(d=k^2+\mathrm{Jac}/2\), including the finite-bin stress and susceptibility; \({\cal H}_r\) is the saved reference expansion on each native clock, not a replacement for \({\cal H}_m\). Thus the photon response to matter has weights \(K_C=K_E,\ K_Y=K_M-{\cal H}_rK_E\), with both measured photon components retained and the subtraction performed *before* taking magnitudes.

Over the entire both-active range, the largest gains across the three tested settings are **63.39212 Mpc** for \(\delta C\) and **15.26100** for \(\delta Y\). For example, the paired-contrast term alone is bounded by \(63.39212\sup|\delta C|+15.26100\sup|\delta Y|\) (coefficients rounded up). If the whole budget were assigned to just one of these and all other terms vanished, the uniform limits would be approximately \(2.21\times10^{-18}\ {\rm Mpc}^{-1}\) or \(9.18\times10^{-18}\), respectively. **Do not spend the whole budget twice.** Cold-source leakage from slightly different transfer kernels, clock matching, and the brief earlier MTS switch are separate expenses. The [eight-term allocations](evidence-001.zip) (archive member: `uniform-matter-and-source-caps.csv`) give one simultaneous sufficient option for the tested settings. They are targets, not measured late source amplitudes.

**A more useful target for the most sensitive bin:** take the complex contrast at its midpoint (\(\eta_h\simeq273.33\) Mpc) and an upper bound on its rate of change there **throughout the bin**. The signed constant part of each kernel can then be summed before taking its magnitude. The paired part of this bin's peak response is bounded by
\[
25.451\,|\delta C_*|+58.636\,\sup|d\delta C/d\eta_h|
+4.605\,|\delta Y_*|+11.426\,\sup|d\delta Y/d\eta_h|.
\]
Coefficients are rounded up across settings; the slopes use the MTS native clock along equal scale factor. To obtain this inequality, subtract the midpoint source at each stage and bound the remainder by slope times elapsed time. No fitted phase or smoothness assumption is needed **if** the slope bound is derived. If one cannot control the slope, the ordinary binwise supremum weights remain valid. Other bins and the three leakage/switch expenses must still be added. [Exact coefficients for both priority windows](evidence-001.zip) (archive member: `priority-matter-targets.csv`).

## How the comparison and checks work
- Reused the sealed adjoint for each native medium. No post-64 matter input or physical source was evolved. The primary, time, and angular settings reuse the original scale nodes; insert only the two physical switches. The reporting windows snap to original grid nodes and do not change integration. Use the native stage times and retain the entire scoring-spline support through the saved endpoint.
- At an overlapping stage let \(X\) be either source, \(a_h,a_c\) its two sampled scale factors, and \(K_j\) each branch's two-component gain including the step. Split the difference exactly into \(K_h\delta X(a_h)+(K_h-K_c)X_c(a_c)+K_h[X_c(a_h)-X_c(a_c)]\). On a single-branch stage use \(K_h X_h\) directly. Summing Euclidean norms gives the positive paired, medium, clock and switch coefficients per bin. The cold-source derivative in the clock expense is per *cold* conformal Mpc, not per scale factor.
- For the first Radau stage the difference of matched cold times is a linear-interpolation defect of \(\eta_c\circ\eta_h^{-1}\). Bound it by \((\Delta\eta_h)^2\sup|(\eta_c\circ\eta_h^{-1})''|/9\) with positive cubic-clock derivative bounds and numerical slack. The end-stage clocks correspond to the same scale node. Clock allowance close to quadruples when doubling the step, as a quadratic spacing bound should; **its per-step coefficient is not resolution invariant**. An independent, more conservative bound using the original (undivided) scale cells changes by less than 0.03% across the controls. It can replace the clock coefficient, not be added to it. See [common-cell bounds](evidence-001.zip) (archive member: `common-cell-clock-gain.csv`). These are numerical enclosures for the sampled transfer, not a formal continuum or floating-point proof.
- **18/18** independent forward-versus-backward synthetic peak tests passed (worst relative error \(3.92\times10^{-9}\), allowance 0.005). **24/24** paired source-envelope controls passed across the two source bases, including an exactly common source and a phased contrast. The midpoint bound encloses all four real archived channel readouts from the **57.6–64** block; it is relatively loose for the rapidly varying MTS energy source. The branch and source-basis algebra was checked separately.
- The top two bins rank in the same order for both branches' paired comparison on all three settings. Whole paired gains change by at most \(2.07\times10^{-8}\) relative, well inside the 0.005 gate. Some tiny medium-difference terms in the peak scoring cell and after it vary by more than 0.5% of *themselves*; they remain included, not promoted to stable fractional predictions or set to zero. For a per-window budget use the largest coefficient for that window across settings. The prior **0.532%** fourth-block energy-step discrepancy remains recorded; it is not extrapolated as a late uncertainty.

**Next:** seek an independently constrained midpoint value and slope for \(C\) and \(Y\) in 268.82–277.85, with the neighbouring 256.00–268.82 bin second. Start from the retained current, energy and shear equations and input coverage; do not seed the late state by fitting a peak or extending the measured 12% cancellation. If historical matter inputs do not reach this range, a bound must connect it to the 64-Mpc restart or to independently derived late data. The physical late response is still unmeasured; the new evidence is where a matter calculation will have leverage.

[Full window weights](evidence-001.zip) (archive member: `per-window-gains.csv`) · [quantiles](evidence-001.zip) (archive member: `cumulative-sensitivity.csv`) · [window value-and-slope gains](evidence-001.zip) (archive member: `signed-local-matter-targets.csv`) · [resolution checks](evidence-001.zip) (archive member: `gain-resolution.csv`) · [forward tests](evidence-001.zip) (archive member: `direct-forward-controls.csv`) · [paired source controls](evidence-001.zip) (archive member: `paired-envelope-controls.csv`) · [historical bound test](evidence-001.zip) (archive member: `saved-block-bound-check.csv`) · [parent peak reconstruction](../mts-signed-photon-peak-six/RESULTS.md).
