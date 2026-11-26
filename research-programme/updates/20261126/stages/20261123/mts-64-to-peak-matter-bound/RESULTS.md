> Public reading copy: local links are mapped to released material or marked unavailable. Machine-specific passages, where present, have been omitted. See the inventory for the original digest.

# What the 64 Mpc state bounds at 273.33232 Mpc
**Decision.** The retained state fixes the signed restart contribution to the current and lapse at the target and gives conditional upper bounds for both their magnitudes and their rates of change. It does **not** by itself fix the physical late values. The missing contributions are two specific signed integrals of longitudinal momentum production and shear/clock work. Adding magnitudes cannot certify 0.5%; the full forced solution could still satisfy the tolerance. No late particular matter state was calculated, no regular solution substituted, and no fit or observational data used.

## Results for the paired contrast
Baseline is cold; MTS is heavy. Differences compare at equal saved scale factor, not equal native conformal times. The common launch has MTS time 64, baseline time 63.9999375288 (interpolated **inside** its saved final block). The window is 268.81660–277.84791 in the baseline clock. The midpoint in the MTS clock is \(s_*=273.33232136\) Mpc. The measured cut gives \(\delta C_0=(-6.43486+17.68913i)10^{-15}\ {\rm Mpc}^{-1}\) and \(\delta Y_0=(-1.14750+1.67150i)10^{-13}\).

| Quantity | Known signed contribution from the restart | Additional signed integral required |
|---|---:|---|
| Effective current at midpoint | \((-1.91899+5.27521i)10^{-16}\ {\rm Mpc}^{-1}\) | Weighted longitudinal impulse \(I_C\) |
| Lapse at midpoint | \((-1.11378+2.80563i)10^{-13}\) | Weighted current plus shear/clock work \(I_Y\) |

These are **terms of a decomposition**, not a zero-forcing model prediction or lower bounds on the actual signals. For the inherited positive midpoint-and-slope photon test, even spending the entire peak allowance on one term would require \(I_C\) to be within \(5.5061\,10^{-18}\ {\rm Mpc}^{-1}\) of the negative of the first entry, or \(I_Y\) within \(3.0434\,10^{-17}\) of the negative of the second. Their centers are roughly **102** and **9,919** such radii from zero. The four terms actually **share** one budget. [Signed target disks](evidence-001.zip) (archive member: `required-signed-impulses.csv`) · [baseline, MTS and paired propagated terms](evidence-001.zip) (archive member: `transported-cut.csv`).

Put \(p=\sup_{64\le s\le s_*}|\mathcal P|\), \(v=\sup_{64\le s\le s_*}|\mathcal V|\), using MTS conformal distances in Mpc. The midpoint upper bounds are
\[
|\delta C_*|\le 5.614\,10^{-16}+75.966p,\qquad
|\delta Y_*|\le 3.019\,10^{-13}+6224.75p+115.728v .
\]
For **the entire hot window** use \(p,v\) taken through its right edge. Then
\[
\sup|\delta C'|\le5.949\,10^{-18}+1.782p,\qquad
\sup|\delta Y'|\le2.112\,10^{-15}+109.151p+1.587v .
\]
Here \(\delta C'\) and \(\mathcal P\) have units \({\rm Mpc}^{-2}\), \(\delta Y'\) and \(\mathcal V\) have units \({\rm Mpc}^{-1}\); coefficients carry the appropriate powers of Mpc. Values rounded **up**. These inequalities are conditional on physical envelopes; the large nonnegative terms show why unsigned extrapolation is insufficient. [All 18 bounds, including the two individual models](evidence-001.zip) (archive member: `conditional-bounds.csv`).

**A constraint on when the work must occur.** For the same positive test to pass, the peak production magnitude before the hot window must be at least \(7.61\,10^{-18}\ {\rm Mpc}^{-2}\), while throughout the window it must be at most \(2.50\,10^{-18}\ {\rm Mpc}^{-2}\). This is a necessary, not sufficient, contrast of at least **3.04 to one**. The early *signed integral* must reach the requisite disk: a large instantaneous cut value is not evidence of that area. Eliminating any constant longitudinal production between the two moment equations gives a second independent condition. If the shear/clock work vanished, the maximum departure of production from any constant would have to be at least \(5.41\,10^{-17}\ {\rm Mpc}^{-2}\); if production were constant, the shear/clock term would need to reach at least \(2.20\,10^{-15}\ {\rm Mpc}^{-1}\) somewhere on the bridge. Neither assumption was used as a closure. See [necessary conditions](evidence-001.zip) (archive member: `necessary-production.json`).

## Equations used
Keep the original \(Y=\Psi,\ L=\Psi-\Phi=(\Pi-Q)/k^2\) and \(C=J/(2k^2)+F_q+(H_r-H_m)Y=\Phi'_{\rm native}+H_rY\). \(H_r\) is the saved reference conformal expansion, \(H_m\) that of the matter calculation. Set \(s=\eta_h,\ r=d\eta_c/ds,\ g=d\ln a/ds\), using both original scale-factor clocks; a prime below means \(d/ds\). With \(D=\delta C,\ Z=\delta Y\) the exact reduced equations are
\[
 D'=-2gD+\mathcal P,\qquad Z'=D-H_{r,h}Z+\mathcal V,
\]
\[
 \mathcal P=a^{-2}(a^2\delta C)',\qquad
 \mathcal V=(\delta L)'+(1-r)C_c+(rH_{r,c}-H_{r,h})Y_c .
\]
The \(a^2\) weight removes the ordinary free redshifting of longitudinal momentum in the dust piece. For the total it is an integrating factor **with all production retained**; it is not a dilution law imposed on the heavy field. In particular \(\mathcal P\) includes the derivative of \(a^2\delta J/(2k^2)\), the quadratic metric rate, and the reference-expansion correction. The individual equations use \(\mathcal P_j=a^{-2}(a^2 C_j)'\) and \(Y_j'=r_j(C_j-H_{r,j}Y_j)+L_j'\). This is why subtracting the two separately transported restart terms need not exactly reproduce the chosen paired restart term: in the paired decomposition the clock mismatch sits in \(\mathcal V\).

With \(w(t,u)=[a(u)/a(t)]^2,\ G(t,u)=\exp[-\int_u^t H_{r,h} ds]\) and \(T(t,u)=\int_u^t G(t,x)w(x,u)dx\), the pair satisfies
\[
 D(t)=w(t,0)D_0+\int w(t,u)\mathcal P(u)du,\quad
 Z(t)=G(t,0)Z_0+T(t,0)D_0+\int[T(t,u)\mathcal P(u)+G(t,u)\mathcal V(u)]du.
\]
Index 0 denotes the **matched 64 Mpc cut**, not time zero. At midpoint \(w=0.02982175,\ G=0.17268915,\ T=14.2289780\) Mpc. Positive integrals bound unknown work; monotone factor endpoints bracket the kernel gains cell by cell. The tight midpoint calculation also bounds composite-trapezoid error by a second-derivative envelope for \(G(t,u)w(u,0)d\eta_j/da\). This limits numerical centering error on the paired lapse to \(5.49\,10^{-21}\), **0.019%** of its one-term radius. All are numerical bounds on the retained interpolants, not a formal roundoff proof.

For the inherited paired photon criterion the four nonnegative terms have weights 25.45065, 58.63587, 4.60457 and 11.42571 on \(|D_*|,\sup|D'|,|Z_*|,\sup|Z'|\), respectively (rounded; exact values in the parent). Budget \(=1.4013360277896485\,10^{-16}\), unchanged. Bounding \(D,Z\) within half-window distance of their midpoint gives the necessary hot-window ceilings in [window conditions](evidence-001.zip) (archive member: `window-conditions.csv`). Subtract the largest possible hot contribution from the disk requirement on \(I_C\) to obtain the pre-window production minimum. For the constant-production elimination subtract \(\alpha I_C\) from \(I_Y\) with \(\alpha=\int T/\int w=81.93946\) Mpc; \(\int(T-\alpha w)=0\) by construction. The numerical inequalities include the bracketing uncertainty in \(\alpha\). These conditions concern this sufficient paired-source certificate; failure would not prove that the actual photons exceed 0.5%. Other windows and medium leakage still require their own allowance.

## Validation, precision and what remains
- **72/72 historical comparisons** passed for current, lapse and their slopes: six completed intervals, baseline/MTS/signed difference. Worst discrepancy was **0.0655%** of the respective interval peak. The momentum inputs come from stored flux, quadratic sources and background correction; the lapse equation uses stored shear. This checks the equations against the saved trajectory; it does not independently constrain future forcing. [Replays](evidence-001.zip) (archive member: `real-history-checks.csv`).
- **12/12** cut value and slope comparisons passed against the saved larger matter step. Despite those passes, its signed change in the transported lapse term is \(2.8563\,10^{-17}\), **93.85% of the entire one-term midpoint lapse radius**. This is sensitivity to that historical refinement, not a measured physical error or a budget charge to be silently discarded. Current centering moves by only 0.41% of its corresponding radius. [Cut control](evidence-001.zip) (archive member: `cut-step-check.csv`) · [slope control](evidence-001.zip) (archive member: `endpoint-slope-step.csv`) · [tight integration check](evidence-001.zip) (archive member: `tight-midpoint-bracket.csv`).
- At the cut, longitudinal momentum supplies essentially all of the paired production, \(|\mathcal P_J|=3.26\,10^{-13}\ {\rm Mpc}^{-2}\); the quadratic metric-rate piece is \(3.06\,10^{-16}\). The shear-rate term dominates \(\mathcal V\) there. **Do not hold these cut rates fixed** for the next 209 Mpc. [Physical source decomposition](evidence-001.zip) (archive member: `cut-source-decomposition.csv`).
- In the verified source chain the dynamically matched 77-bin state and common incident source end at **64**. The padded quadratic forcing ends at **64.05**, not at recombination. The long saved medium supplies the clocks and \(H_r\), not longitudinal momentum or anisotropic stress. The late regular-mode and different two-wave histories cannot substitute for this particular solution. Input coverage and distinctions (not bundled here).
- Four smooth, compact mathematical source changes leave the entire early state and its derivatives unchanged, yet can move either midpoint value or either local slope independently in the **projected** equations. [Checks](evidence-001.zip) (archive member: `projection-freedom-controls.csv`). These are demonstrations of the insufficiency of the reduced inputs, **not alternative solutions of the full MTS initial-value problem**. The full matter dynamics select the actual impulses.

**Next physical calculation:** carry the two *signed* weighted integrals of longitudinal momentum and shear forward from the verified 64 Mpc restart, retaining baseline and MTS separately and checking the matter step. Use the same primary and tighter start control before claiming a cancellation on the scale of the lapse disk. No fitted state at 273 Mpc and no late test on a different curvature branch.
