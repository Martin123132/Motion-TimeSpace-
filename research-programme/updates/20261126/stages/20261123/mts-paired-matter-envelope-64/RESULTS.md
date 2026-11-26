> Public reading copy: local links are mapped to released material or marked unavailable. Machine-specific passages, where present, have been omitted. See the inventory for the original digest.

# Can the saved matter equations bound the remaining photon driving to 0.5%?
**Decision: not with these bounds.** At 64 conformal Mpc the signed MTS-minus-baseline potential is much better constrained than the two branches taken separately. Beyond the cut, the equations give an explicit bound in terms of paired momentum and shear. Discarding their relative phase already costs more than the photon budget; preserving phase gives a quantitative target, not evidence that it is met. The size of the actual late signal remains undetermined. No matter or photon interval was started.

## What the saved states establish
Baseline is the saved cold branch; MTS is the saved heavy branch. Results refer to the retained longest mode, \(k=0.3368801\ {\rm Mpc}^{-1}\), the 77-bin calculation, the two original media, and the previous scoring conventions. A percent here is a fraction of the retained signed photon contrast, *not* a fraction of the gravitational potential or of launch amplitude.

| At the two native 64-Mpc endpoints | Magnitude |
|---|---:|
| Potential difference, \(|\delta\Phi_0|\) | \(1.99335\,10^{-13}\) |
| Lapse difference, \(|\delta\Psi_0|\) | \(2.02750\,10^{-13}\) |
| Paired algebraic upper bound on the lapse difference | \(2.19991\,10^{-13}\) |
| Adding individual lapse magnitudes instead | \(1.33003\,10^{-12}\) |

The endpoint energy term contributes \(2.07\,10^{-13}\) in magnitude; the net longitudinal momentum term contributes \(8.48\,10^{-15}\). By sector, the cold matter and heavy scalar contributions to the lapse contrast are \(5.26\,10^{-13}\) and \(4.54\,10^{-13}\), largely opposed in phase. Keeping that cancellation tightened the endpoint bound by a factor of 6.05. These are components of the same calculation, not two observational measurements.

Energy, momentum and shear reconstructed the individual saved endpoints and their signed differences at all six cuts. The integrating-factor replay of both potentials on each stored interval, for baseline, MTS and their difference at common scale factor, passed **36/36** comparisons. Worst discrepancy: **0.06815%** of the relevant potential's own interval peak (gate 0.5%). The rate and slip inputs here come from the saved evolution: this is an internal equation check, not an independent prediction or an error bar for late times. [Endpoint decomposition](evidence-001.zip) (archive member: `signed-matter-constraints.csv`), [sectors](evidence-001.zip) (archive member: `matter-sectors.csv`), [replays](evidence-001.zip) (archive member: `momentum-replay.csv`).

## Derivation of the divergence bound
Write \(A=U-E/2,\ S=\Pi-Q,\ d=k^2+{\rm Jac}/2\), including the quadratic sources and finite-bin stress. With \(\delta=h-c\), \(H\) the matter conformal expansion rate, and \(\alpha=3/(2k^2)\), the exact retained constraint gives
\[
d_h\delta\Phi=\delta A-\alpha(H_h\delta J+\delta H\,J_c)-\delta d\,\Phi_c,\qquad
\delta\Psi=\delta\Phi+\delta S/k^2 .
\]
It applies on native paired endpoints or at two states matched in scale factor, as specified. Do not identify the two native cut scales: baseline starts at 0.000154917050404564, MTS at 0.00015491688273726336. All forward bounds switch the branches on separately and compare them at common scale factor.

The momentum equation gives \(\Phi'+H_r\Phi=b\), where
\[
b=J/(2k^2)+F_q-H_r S/k^2+(H_r-H)\Psi .
\]
Prime denotes the native conformal-time derivative. \(H_r\) is the positive interpolated reference expansion; the last term is required if the input matter history uses a slightly different expansion. It is not set to zero in the bound. With \(\beta_j=d\eta_j/da\), \(\chi_j=1_{\eta_j\ge64}\), \(p_j=\exp[-\int_{64}^{\eta_j}H_{r,j}d\eta]\) after cut, write \(\Phi_j=p_j\Phi_j^0+u_j\). Here \(u_j\) is the causal integral of \(\chi_j\beta_j b_j\) with the positive integrating factor. Since its kernel is at most one, and \(\exp(-x)\) is 1-Lipschitz for \(x\ge0\),
\[
\begin{split}
 B&=\int|\delta(\chi\beta b)|da+\mu\int\chi_c\beta_c|b_c|da,\quad
 \mu\le2.454\,10^{-5},\\
 |\delta\Phi|&\le|p_h\Phi_h^0-p_c\Phi_c^0|+B,\qquad
 |\delta\Psi|\le|p_h\Phi_h^0-p_c\Phi_c^0|+B+|\delta S|/k^2 .
\end{split}
\]
The potential inequalities are shown on the both-active region; the implementation also includes the short single-branch segment. The kernel mismatch is bounded by integrating the difference of the two reference expansion rates expressed in the common clock, using polynomial bounds on the saved medium. This is a **conditional full-range envelope**, not a numerical cap obtained by extrapolating the last measured momentum or shear.

## Two tests of the photon budget
**1. Separate magnitudes.** Removing the derivative monopole drive and restoring the boundary value puts \(4\delta[\chi(\Phi-\Phi^0)]\) back into the photon monopole. Its known integrating-factor component is \(4[(p_h-1)\Phi_h^0-(p_c-1)\Phi_c^0]\) (zero on each inactive branch). We evaluated it on the original scale-factor nodes and scored with the original cubic interpolation and visibility weights.

| Statistic | Absolute 0.5% allowance | Known component's norm | Ratio |
|---|---:|---:|---:|
| Window RMS | \(4.27604\,10^{-16}\) | \(6.67008\,10^{-13}\) | 1,560 |
| Visibility peak | \(1.40134\,10^{-16}\) | \(6.62679\,10^{-13}\) | 4,729 |

A sufficient bound **adding separate norms** for this component, the compensating matter contribution, and acceleration cannot pass even before the other positive terms enter. These ratios are **not lower bounds on the observed or predicted photon residual**. The signed contributions can cancel. [Inputs and scores](evidence-001.zip) (archive member: `surface-certificate-floor.csv`), [full conservative gains](evidence-001.zip) (archive member: `residual-gains.csv`), [complex momentum cancellation targets](evidence-001.zip) (archive member: `momentum-cancellation-target.csv`). The gains include the retained scoring-spline and medium-mismatch allowances. They concern the continuous constraint solution; any future calculation using independently interpolated \(\Phi'\) and \(\Phi\) must also charge their derivative defect as in the predecessor.

**2. Keep phase and test what the direct sufficient criterion would require.** Let \(D_s=\int\|\delta s\|_{W_h}da,\ I_c^\gamma=\int\|s_c\|_{W_c}da\) for the original, untransformed photon sources. The previous criterion is \(D_s+\epsilon I_c^\gamma\le\tau\) with \(\epsilon=0.0550911\); \(\tau\) includes the scoring-spline allowance. In the continuum equations the energy slot gives \(|\delta[\chi(\Phi-\Phi^0)]|\le D_s/4\). On the overlap, \(\delta\Phi\) would therefore have to remain within \(\tau/4\) of \(D_0=\Phi_h^0-\Phi_c^0\); equivalently, the numerator of the energy constraint above must stay that close to \(d_hD_0\) after multiplication by \(d_h\).

The acceleration slot also gives \(\int|\delta(\chi\beta\Psi)|da\le\sqrt3 D_s/(4k)\). Let \(L=\int\beta_h da\) on the both-active region up to the desired readout, \(\rho=\sup|\beta_h/\beta_c-1|\le2.841\,10^{-5}\), and take the mean with weight \(\beta_h/L\). As \(\delta\Psi=D_0+\delta[\chi(\Phi-\Phi^0)]+\delta S/k^2\) there, the signed mean slip must obey
\[
|\overline{\delta S/k^2}+D_0|\le
\tau\max\{1/4+\sqrt3/(4kL),\;(\rho/\epsilon)\sqrt3/(4kL)\}.
\]
At peak this is a disk in the complex plane centered at \(1.12086\,10^{-13}-1.64837\,10^{-13}i\) with radius \(1.196\,10^{-17}\). The implied mean slip magnitude must exceed \(1.9932\,10^{-13}\), **12.12 times** the largest sampled paired slip in the six saved intervals (\(1.6445\,10^{-14}\)). The window result is similar. This comparison does not assume that the past maximum bounds the future. It is a necessary condition for this particular *sufficient* certificate, not a requirement on every way the photons could cancel. A retrospective test with the known 57.6–64 source gives a center distance \(1.889\,10^{-13}\) inside its \(6.229\,10^{-13}\) bound. [Thresholds](evidence-001.zip) (archive member: `necessary-shear-target.csv`), [sampled history](evidence-001.zip) (archive member: `saved-paired-shear.csv`), [backtest](evidence-001.zip) (archive member: `shear-target-backtest.csv`).

## Why the three moments alone do not close; next step
At 64 we applied the evolution operator once to a photon intensity octupole direction, with all other state components, the finite-bin input, and external forcing held fixed. The instantaneous energy, momentum, shear and both potentials are unchanged, but \(\partial I'_2/\partial I_3=-3k/5=-0.2021281\) for both models; consequently the time derivative of effective shear **is changed**. [Operator check](evidence-001.zip) (archive member: `projected-closure.csv`). This is an algebraic test of what the projection loses, not a change to the saved initial conditions or evidence for two allowable histories from the same full state.

**Recommended next step (no new matter interval):** use the saved photon transport operator to weight signed energy and acceleration forcing by their response at the visibility peak; test that weighting on the known six intervals against their saved readouts before applying it to late-source bounds. This attacks the sign information lost by the absolute-value test. It will still need an envelope for the later matter source, including the higher moments that feed shear. No later particular matter history, new galaxy fit, or observational detection is claimed here.

[Original 64-Mpc result and unchanged tolerance](../mts-particular-gravity-64-tail/RESULTS.md) · original transport bounds (not bundled here) · [machine-readable decision](evidence-001.zip) (archive member: `decision.json`).
