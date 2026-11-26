# What the saved wave determines

The working quantities are the retained conformally normalized longitudinal momentum \(j=J/\rho\), energy \(e=E/\rho\), \(d=e-3\Phi\), pressure \(p=P/\rho\), and shear. The common time is conformal distance \(\eta\) in Mpc. The microscopic stress contains the induced second-order field and the quadratic products of linear fields. On the saved trajectory its balance laws give independent rates:
\[
 W_j=-\mathcal H j+k^2p+k^2\Psi+s_j,\qquad W_d=-j-3\mathcal H p+s_e .
\]
Here \(s_j,s_e\) are the inhomogeneous source terms in this normalization, including metric and quadratic-field terms; their presence is not a measured dissipation rate. The four signed integrals of \(W_j\) for each cycle and both seeds are in the impulse tables.

**A finite-time, causal average with no fitted period.** Put \(u=\theta(\eta)-\theta(\eta_s)\), where the phase is recovered from the saved wave background. The leading quadratic carrier has period \(L=\pi\) in this phase (not a fixed duration in Mpc). At entry set \(\widetilde X(u<0)=X(0)\), use the measured \(X(u)\) at positive phase, and define
\[
 A_L X(u)=L^{-1}\int_{u-L}^u\widetilde X(v)\,dv .
\]
This preparation preserves the entry value. Holding the not-yet-filled portion at its entry value is an explicit convention, not something the field equations select. In conformal time,
\[
 (A_Lj)'=\frac{\theta'}{L}\left[j(u)-j(\max(0,u-L))\right]
 =\frac{\theta'}{L}\int_{\max(0,u-L)}^u
       \frac{W_j(\eta(v))}{\theta'(\eta(v))}\,dv .
\]
The first expression uses stress samples. The second uses the force terms and the varying phase speed. Their agreement is a test, not a fit. The remaining current obeys \(j_{\rm osc}'=W_j-(A_Lj)'\); its initial value is zero in this preparation, not in a pre-existing periodic average. Integrating both rates independently reconstructs the measured current throughout the overlap. After filling, a stationary harmonic \(e^{2inu}\) averages to zero for nonzero integer \(n\); its microscopic amplitude need not decay. A varying envelope and secular forces leave a slowly changing mean.

The two-period control uses \(2\pi\). Another start uses only the elapsed support until one cycle is available; its derivative during filling is \(\theta'(j-Aj)/u\), with the regular half-slope limit at entry. It is not allowed to shift the event to improve agreement. Four complete cycles **before** and four **after** were scored from actual wave samples. The pre-event data are used for this persistence test, not presented as hidden history of the entry-filled average.

**Pressure and gravity cannot be filtered independently without a check.** The simple filtered implementation carries the equation-derived rates into the effective density and momentum equations, with the measured filtered pressure and shear. It keeps the other species on their actual matched histories. An independent test computes the curvature rate both from the momentum constraint and by differentiating the curvature from the energy constraint. Simultaneously smoothing each heavy stress component need not preserve that identity when the other sources are not smoothed the same way.

The companion construction instead prescribes only the one-cycle current change \(\Delta j=A_L j-j\). In the saved reference geometry hold the original inhomogeneous work and shear fixed. Subtracting the unsmoothed conservation equations fixes
\[
 k^2\Delta p=\Delta j'+\mathcal H\Delta j,\qquad
 \Delta d'=-\Delta j-3\mathcal H\Delta p,\qquad \Delta d(\eta_s)=0 .
\]
There is no adjustable coefficient here. The resulting pressure is **required under those assumptions**, not the measured phase-averaged pressure. On the finer step for the photon launch the difference between them reaches 81.2% of the peak raw wave pressure, whereas the required energy differs from the directly averaged energy by 0.121% of its peak. The coupled solve then responds to the actual lapse and curvature, rather than imposing the saved geometry. A matched surrounding-source run, a wave surrounding-source control, and a one-sided interpolation control separate conservation of the reference redistribution from consistency of the whole joined metric.

**Photon observable.** The original transfer propagates any \(4[\Phi]\) monopole at the entry and the subsequent curvature-rate and lapse sources until 89.6. After that only scattering and free propagation act on this interval's correction. The cold baseline is identical on the two sides. For each gravity step compute the full-window visibility-weighted RMS of the **complex vector difference** (photon energy, current) of the modified and explicit-wave results, divided by the original joint launch norm \(1.8923589891767267\,10^{-12}\), times 100. The 0.163% criterion is not a difference of RMS magnitudes, a likelihood, or a percentage of the observed sky. Both metric-rate routes and the inherited time, angular and gravity controls are reported separately.
