> Public reading copy: local links are mapped to released material or marked unavailable. Machine-specific passages, where present, have been omitted. See the inventory for the original digest.

# How the new discontinuities affect the matching moment

**Question:** can the four-pion change to the *dominant two-pion channel* be bigger than the direct four-pion term? A discontinuity at one energy does not answer this. Here we isolate, and actually integrate, the portion driven by the leading four-pion source on the finite interval \(b=(4m)^2\) to \(c=(0.8\,\mathrm{GeV})^2\). Set \(a=(2m)^2\). Other cuts and local terms are not set to zero as physical claims.

For source \(F=H,A\) define the window contribution, with specified zeros at its matching points, as
\[
 \Delta_L F(s)=\frac{L(s)}{\pi}\int_b^c\frac{u_F(v)\,dv}{L(v)(v-s-i0)} .
\]
The prescriptions are H3: \(L=s^2(s-a)\); H4: \(s^3(s-a)\); A1: \(s\); A2: \(s^2\). H3 fixes the assigned photonic shift and slope at zero and its value at two-pion threshold; H4 additionally fixes the second derivative at zero. A1 leaves the total-stress normalization at zero alone; A2 also keeps its slope. These assignments hold the same constants fixed in each prescription. A physical comparison of differently subtracted representations would transform the subtraction coefficients: the computed differences are explicitly **polynomials**, not four independent physical predictions. Interactions can affect those coefficients. An independent bare local photon–curvature term in the final matching is yet another issue.

To isolate the order with a single feedback insertion use the real leading sources \(H_{\rm Born}\) and \(A=1\). The linear change to the signed matching moment is
\[
 \delta I=\int \frac{\alpha}{4\pi}\frac{\beta^3\,ds}{s^2}
 [\mathrm{Re}\Delta H+H_{\rm Born}\mathrm{Re}\Delta A].
\]
Dressings from two-pion strong interactions cannot be included consistently just by replacing the denominators of phase ratios by their observed moduli. The direct cut and this feedback are at different orders in the chiral expansion; their sum does not include every term through the higher order.

**In the same window** as the direct four-pion result, \(b<s<c\), use the principal value, not just the absorptive term or its modulus. The table gives GeV⁻².

| Term | Principal-value moment | Fraction of the positive direct term |
|---|---:|---:|
| H3 | −3.3953 × 10⁻¹¹ | −7.53% |
| H4 | −2.2489 × 10⁻¹¹ | −4.98% |
| A1 | −1.0896 × 10⁻¹¹ | −2.42% |
| A2 | −8.0739 × 10⁻¹² | −1.79% |

**Two independent evaluations.** First exchange the order of the two Cauchy integrals. For a weight \(f(s)=w(s)L(s)\), including the real Born factor for the stress term, use
\[
 {\rm PV}\int_b^c\frac{f(s)\,ds}{v-s}
 =\int_b^c\frac{f(s)-f(v)}{v-s}\,ds+f(v)\log\frac{v-b}{c-v}.
\]
After multiplying by \(u_F(v)/L(v)\), subtract the linear interpolation of the endpoint coefficient from the logarithmic integrand and add it back analytically, using \(\int_0^1 t\log[t/(1-t)]\,dt=1/2\). The lower coefficient is zero by the threshold law. Second, interpolate only the smooth threshold-divided source with its independent analytic endpoint and a calculated upper endpoint. Treat the Cauchy singularity in the *original* inner integral with weighted quadrature; integrate the endpoint-logarithmic outer response adaptively. Their largest fractional disagreement on the fine grid is 0.036%. Artificial endpoint logarithms are integrable and reflect isolating a sharp window; they are not pion resonances. Grid and integration comparisons (not bundled here).

**Below the four-pion opening.** In the already referenced 0.281–0.540 GeV two-pion window the H3/A1 allocation yields −5.52 × 10⁻¹² GeV⁻² from the same four-body source, H4/A2 yields −2.16 × 10⁻¹². These are assigned corrections on the Born/unit reference, not a new fit of the earlier reconstructed elastic wave. Real source shifts at three energies (not bundled here).

**One polynomial-independent shape check.** For five distinct \(s_i\) below \(b\), a fourth divided difference annihilates *all* polynomial ambiguities through degree three and for this right-cut piece equals \(\pi^{-1}\int_b^c u_F(v)dv/\prod_i(v-s_i)\). Use \(W_i=0.30,0.36,0.42,0.48,0.54\) GeV and \(s_i=W_i^2\). The values are \(-2.497\times10^{-6}\) and \(-6.003\times10^{-6}\) GeV⁻⁸ for photon and stress. Explicit differences of the subtracted values reproduce them with all four prescriptions. Unlike the window's allocated absolute shift, these shape contributions are unchanged by the subtraction choices tested. Spectral weight outside the window, additional cuts, or higher local derivatives are not removed. Numbers (not bundled here).

**Back to the parent observable.** The previously matched mostly-plus optical action has \(c_W^{\rm opt}=-(\hbar c)^2 I\) for these contributions in GeV⁻². Multiply by the [saved finite-endpoint GR-ray transfer at conjunction](../mts-binary-polarization-rays/RESULTS.md); same central binary and polarization labeling, reception at infinity. The direct four-pion piece corresponds to −9.97 × 10⁻⁶³ s of differential travel time; the two feedback examples separately give +0.99 or +0.68 × 10⁻⁶³ s. These are microscopic *pieces* of an optical coefficient, not forecasts for the total observed timing residual. No coupling was inferred from the pulsar. Signed conversions and transfer (not bundled here).

