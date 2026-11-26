> Public reading copy: local links are mapped to released material or marked unavailable. Machine-specific passages, where present, have been omitted. See the inventory for the original digest.

# Real photons: the signed vector threshold and the first hadronic input

The external photons here satisfy \(p^2=k^2=0\). This is a different measurement from the off-shell momentum difference in [TRANSVERSE.md](TRANSVERSE.md). The same **local** full-index Weyl coefficient must match after fixing the action and sign convention. The finite-momentum shapes need not coincide.

## Scalar angular cut and known spin thresholds

[Bellazzini, Isabella, Lewandowski & Sgarlata](https://arxiv.org/abs/2108.05896) express the photon gravitational matrix element in three form factors. For real photons, same helicities and a trace-free spin-two source isolate the helicity-flip structure \(F_3\): the opposite-helicity Maxwell tensor and the spin-zero trace structure do not contribute. For their minimally sourced one-loop calculation, Eq. 1.11 gives an **unsubtracted** inverse moment for \(F_3(0)\); their Eq. 1.12/Table 3 convention is \(\alpha_3=-F_3(0)\). The scalar and Dirac entries fix the translation to the retained Euclidean and mostly-plus optical actions. This does not impose the same subtraction prescription on a microscopic parent CFF operator.

For a charged point scalar, \(\beta=\sqrt{1-4m^2/s}\), \(z=\cos\theta\), and the Born equal-helicity amplitude is \(M_{++}=2e^2(1-\beta^2)/(1-\beta^2 z^2)\) in the selected phase convention. Project on \(P_2\) and define \(h=(2e^2)^{-1}\int_0^1 P_2 M_{++}\,dz\). Then \(h=(1-\beta^2)H_2\), with
\[
H_2=\int_0^1\frac{P_2(z)\,dz}{1-\beta^2z^2}
=\frac{(3-\beta^2)\operatorname{atanh}\beta-3\beta}{2\beta^3}.
\]
The scalar Appendix-D cut divided by \(i\alpha\) equals \(-2m^2\beta^3 H_2/s^2=-\beta^3 h/(2s)\). In this **on-shell** channel the Dirac and gauge-vector cuts at the same mass are exactly −2 and +3 times the scalar one, respectively, from the published pair-production amplitudes and cuts. This is not a rule for arbitrary spins or the off-shell banks.

For \(w=Q^2/m^2\), the normalized Euclidean-matched scalar reading \(-4\pi m^2 F_3(-Q^2)/\alpha\) becomes
\[
 \int_0^1 \frac{2\beta^4 H_2(\beta)}{4/(1-\beta^2)+w}\,d\beta.
\]
Independent angular quadrature checks \(H_2\). Expand the last denominator; integrating the terms uses
\(\int_0^1 \beta^{2k+1}\operatorname{atanh}\beta\,d\beta=\sum_{j=0}^{k}(2j+1)^{-1}/(2k+2)\), obtained by summing the absolutely integrable positive series. The scalar starts \(1/180-w/2520+w^2/25200\). All 15 exact spin/moment entries reproduce numerical cut integrals. The two old signs \(+1/180\) and \(-1/90\) in \(W_E\) are recovered **before** applying the vector result to the optical action. Pure trace improvement or Higgs–trace mixing in this decomposition is not an additional \(F_3\) term.

**Signed update.** The minimally coupled SM charged gauge W (including its longitudinal mode, not an arbitrary Proca matter prescription) gives \(+1/60\) in Euclidean loop units, hence
\[
 c_W^{\rm optical}=-\frac{\alpha}{240\pi}\left(\frac{\hbar c}{m_W c^2}\right)^2
 =-5.8344\times10^{-41}\ {\rm m}^2 .
\]
The mass in energy units is the retained 80.3692 ± 0.0133 GeV (not bundled here); its propagated uncertainty alone is \(1.93\times10^{-44}\ {\rm m}^2\), not an all-orders theory error. The old \(3.50065\times10^{-38}\ {\rm m}^2\) was an absolute envelope, **not** the old central estimate. This one-loop magnitude is 1/600 of that ceiling. In the curvature convention of the older 4944 scalar-positive/Dirac-negative register the sign would instead be positive. In the saved optical screen labeling it contributes \(-3.31\times10^{-62}\) s to the central binary example. The lepton plus W subtotal is \(+9.6217944230\times10^{-31}\ {\rm m}^2\); parent and hadronic terms are separate. No existing stage was overwritten. The W loop is published electroweak physics matched into the retained MTS matter choice, not a new MTS prediction of the W mass or the loop itself.

## Where actual hadron data enter

Use the timelike crossed **total** pion energy-momentum form factor \(A_\pi(s)\), normalized \(A_\pi(0)=1\) in the charge-independent isospin limit. The spatial traceless matrix element for a pion pair is \(2(k^ik^j-\delta^{ij}\mathbf k^2/3) A_\pi(s)\); the independent scalar pion D-term drops out. The two-body phase space gives one power of \(\beta\), this tensor supplies two, and its angular projection selects the equal-helicity D wave. Calibrating the overall normalization on the point scalar cut gives the charged-channel term
\[
 \frac{\mathrm{Disc}\,F_3(s)|_{\pi^+\pi^-}}{i\alpha}
 =-\frac{\beta^3}{2s}\, h_{20}^{+-}(s) A_{\pi^+\pi^-}^*(s)
\]
in a common scattering-state phase convention, with \(h_{20}\) defined as above. This is the product on the unitarity right-hand side, **not** a squared amplitude; it is the real spectral sum over complete channels that enters the dispersive integral. The neutral channel has identical-particle phase-space factor 1/2 when using physical amplitudes with the same normalization and full angular integration. It cannot be represented by doubling the charged channel. Isospin projection, conventions for the neutral states, final-state phases and inelastic channels must all match in a signed evaluation. A particularly large helicity-two tensor-resonance signal cannot be substituted for the helicity-zero D wave. An additive local subtraction has no absorptive part.

**What Belle bounds without a partial-wave fit.** Use the [Belle charged-pion measurement](https://arxiv.org/abs/0704.3538), [HEPData release v1](https://doi.org/10.17182/hepdata.51842.v1): all 140 Table 1 energy bins from 0.8 to 1.5 GeV and the 12 angular bins in each of Tables 2, 96, 141. For distinguishable charged pions, parity, Bose exchange and angular folding give \(d\sigma/d|z|=\beta(|M_{++}|^2+|M_{+-}|^2)/(32\pi s)\). Cauchy–Schwarz bounds the contribution of the measured interval \(I=[0,0.6]\) to \(h_{20}\):
\[
 |h_I|\le \frac{\sqrt{32\pi s/\beta}}{2e^2}
 \sqrt{\sigma_I\int_I P_2^2\,dz} .
\]
This uses corrected *intensities*, not a helicity assignment. Integrating the absolute two-pion cut with weight \(ds/s\) now gives, conditional on the tabulated values being bin means,
\[
 |\delta F_3(0)|_{\text{charged, window and aperture}}
 \le 1.6612\times10^{-4}\ {\rm GeV}^{-2}
 \sup_{0.8<W<1.5\,{\rm GeV}} |A_\pi(W^2)| .
\]
Here the left side means the **magnitude of the specified part** of the inverse moment, not the full coefficient or a bound on it. In each energy bin the factor \(\beta^{5/2}/W^2\) decreases for \(W>3m_\pi\), so take its value at the lower edge and use Jensen's inequality on \(\sqrt{\sigma}\). No assumption of flat cross section inside a bin. Shifting all measured intensities upward by their stated upper systematic plus statistical errors gives 1.7665×10⁻⁴ in the same units per unit supremum; this is a simultaneous sensitivity box, not a confidence level. No bound on \(\sup |A_\pi|\) was assumed. The bin-mean interpretation and residual experimental resolution/efficiency corrections are conditions of this data exercise; it is not a rigorous bound on unknown true rates with probability one.

In three energy bins the angular tables allow a more selective bound by applying Cauchy–Schwarz separately in each angular bin. Their integrals reproduce the tabulated total within 0.0046%. Tables 96 and 141 have a generic energy field reading zero; the other qualifier gives 1.2725 and 1.4975 GeV respectively, consistent with the ordered Table 1 bins. Raw metadata are preserved rather than silently relabeled.

**Failure control:** even with a strictly pointlike charged scalar and \(A_\pi=1\), the Belle-window *central-angle* contribution to the Euclidean inverse moment is **negative**, −9.11×10⁻⁶ GeV⁻²; the omitted angles contribute +3.78×10⁻⁵. The full angular result in that window is +2.87×10⁻⁵. About 79.5% of the full point-scalar inverse moment lies **below** Belle's lower energy edge. These figures measure coverage in a solvable control, not fractions inferred for QCD. This is why neither a positive cross section nor a precise resonance peak settles the sign.

**Next independent inputs:** [Cao et al.](https://doi.org/10.1038/s41467-025-62278-9) construct the timelike pion spin-two response dispersively; their datasets are listed as available on request. [Dai & Pennington](https://doi.org/10.1103/PhysRevD.90.036004) analyze charged and neutral two-photon partial waves with isospin/helicity separation. Use the threshold and overlapping elastic window first. Match the phase and full-EMT normalizations to the analytic Born test; distinguish reconstructed amplitudes from observations, and take correlated uncertainty and continuation through inelastic channels seriously. Spacelike pion gravitational radii or OPAL running are not substitutes. No external contact was made.
