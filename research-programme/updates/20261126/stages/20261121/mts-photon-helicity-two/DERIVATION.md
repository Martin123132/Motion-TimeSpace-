> Public reading copy: local links are mapped to released material or marked unavailable. Machine-specific passages, where present, have been omitted. See the inventory for the original digest.

# Isolating the helicity-two matter wave

Use real incoming photons and the original isospin-limit pion mass. \(W=\sqrt{s}\) in GeV, \(a=4m_\pi^2,\ v=\sqrt{1-a/s},\ z=|\cos\theta|\). The charged folded rate is \(K(|A_{++}|^2+|A_{+-}|^2)\) with \(K=2\pi\alpha^2\beta\,({\rm nb/GeV^{-2}})/s,\ \beta=v\); the physical neutral rate has \(K/2\). The normalized amplitudes are \(M/(2e^2)\). Do not confuse helicity-two \(D_2\), which contributes to the opposite-helicity data, with the helicity-zero \(J=2\) projection \(D_0\) in the signed pion stress cut.

### 1. Project before replacing

Suppress the common azimuthal phase. The normalized basis \(U=\sqrt{15/8}(1-z^2)=\sqrt5\,d^2_{20}\) has \(\int_0^1 U^2dz=1\). Project the charged opposite-helicity Born wave \(A_B=v^2(1-z^2)/(1-v^2z^2)\):
\[
 b=\int_0^1UA_B\,dz=\sqrt{15/8}\{(1-v^2)^2\,{\rm atanh}(v)/v^3+5/3-1/v^2\}.
\]
For small \(v\) use the convergent expansion with coefficients \(8/[(2k+1)(2k+3)(2k+5)]\) multiplying \(v^{2k+2}\) inside the braces. Write \(R=A_B-bU\). It is orthogonal to \(U\) on the full folded range, **not on the experimental aperture**. If \(F=(F_0,F_2)\) are the two isospin waves in Dai–Pennington units, the physical charge amplitudes are
\[
 (A_c,A_n/\sqrt2)^T=U O F+(R,0)^T,\quad
 O=\begin{pmatrix}-\sqrt{2/3}&-1/\sqrt3\\-1/\sqrt3&\sqrt{2/3}\end{pmatrix}.
\]
Decoupled Born means \(F=O^T(b,0)\). The photon S and like-helicity D waves, including their interference, are carried forward from the byte-verified prior bins. Changing \(A_{+-}\) alone cannot change the signed \(-F_3\) cut.

### 2. Signed reconstruction rather than a sign chosen on the data

Use the opposite-helicity dispersion equation in [García-Martín & Moussallam](https://arxiv.org/abs/1006.5373v1) (sections on D waves, left cuts, sum rules and polarizabilities). Their physical charged partial wave is \(2b/\sqrt5\); their isospin vector acts on \((\sqrt2 h_c,h_n)\). Thus \(B_I=O_{cI}\sqrt2(2b/\sqrt5)\) and their isospin amplitude \(f_I\) converts to \(F_I=\sqrt{5/8}\,f_I\). There is no extra identical-particle factor in a partial wave after this conversion.

Let \(k_I(t)=-{\rm Im}(1/\Omega_I(t))B_I(t)/[t^2(t-a)]\) and \(l_I(t)=({\rm Im}\,h_I^{Res}/\pi)/[\Omega_I(t)t^2(t-a)]\). After canceling the absorptive term in \(B_I/\Omega_I\), the real reduced amplitude on the upper rim is
\[
 \frac{f_I}{\Omega_I}=B_I\,{\rm Re}(1/\Omega_I)
   +s(s-a)\left[d^I+s\int_L\frac{l_I(t)}{t-s}dt
                   +\frac{s}{\pi}{\rm PV}\int_R\frac{k_I(t)}{t-s}dt\right].
\]
Equivalently, when unsubtracted at this order the sum rule gives \(d^I=\int_L l_I+\int_R k_I/\pi\). The physical pole prescription produces \(+i k_I(s)\) in the right term after division by \(\pi\), canceling the imaginary part of \(B_I/\Omega_I\) exactly. This fixes the signs before any experiment comparison.

For a vector or axial-vector resonance with \(t_R=(m_R^2-m_\pi^2)^2/m_R^2\), use the charge coefficient of the saved table times \((\sqrt6/4)t\sqrt{1-a/t}\,[4m_R^2(t+t_R)/(t(t-a))]^2\) on \(t<-t_R\). Axial and vector have the **same** sign for this helicity, unlike the like-helicity wave. Tensor exchange has the extra factor \(4t+t_R\), not the like-helicity \(4t+3t_R\). Rotate \((\sqrt2 C_c,C_n)\) into isospin at the start. These are narrow-resonance approximations; no assumed absent contribution is converted to an error bar.

- Isoscalar: keep the existing tensor Omnès input, high-energy continuation and spacelike prescription from the retained signed matter reconstruction (not bundled here); use the published fitted \(d^0=-0.48\ {\rm GeV}^{-4}\). This is a hybrid, **not a numerical replication of the authors' fit**. Our corresponding sum rule with 5 GeV² left cutoff gives −0.5580, versus their tabulated −0.54. The \(I=0\) subtraction is not derived from the MTS action.
- Isotensor: take the lower phase curve of GM Fig. 6. The horizontal axis in the plot says MeV; 0.4–2 and the paper's energy convention are GeV. Extrapolate from the first point at 0.4 GeV to threshold as \(k_\pi^5\); beyond 2 GeV smoothly in value bring the phase to zero linearly in \(s\) at 9 GeV², with 16 GeV² as a sensitivity. The phase between the sampled knots is linear in \(s\). For each segment slope \(c_j\), integration by parts gives \({\rm Re}\log\Omega(s)=-\sum_j c_j[(t-s)\log|t-s|-t\log t]_{t_j}^{t_{j+1}}/\pi\); the upper-rim phase is \(\delta(s)\). This also supplies spacelike values without extrapolating a real-axis modulus. The sum rule gives \(d^2=0.42053+0.02517=+0.44570\ {\rm GeV}^{-4}\). Inverting the two *same paper's* rounded polarizability sums gives \(d^0=-0.48191,d^2=+0.43873\), a convention/size cross-check, not independent validation. Cutoffs of 3 and 5 GeV² and the subtraction alternatives are retained separately.
- Second input: [Dai & Pennington, Solution I](https://arxiv.org/abs/1404.7524v2). The blue isospin curves in Fig. 16 give \(m_I=\sqrt{\sigma_{I,D2}/K}\); Fig. 2 gives the D phases, with a real production factor below the effective inelastic thresholds of their parametrization. Fig. 3 independently checks both magnitudes in their covered range. Use the branch \(F_I=-m_Ie^{i\phi_I}\) continuous with the signed low-energy Born-dominated calculation in each channel. A **modulus plot by itself cannot fix this sign**, and the physical four-pion threshold lies below part of the tested region. The signed GM construction is the separate input; the DP comparison is conditional. Calculations include all four constant sign choices and continuous arbitrary-phase bounds. Digitization resolution in the near-zero plotted isotensor phase is not a physical phase measurement. A source curve given at its native fit normalization is not a renormalized pure MTS prediction.

### 3. What survives unknown phases on the actual measured aperture

Let \(N=\int U^2dz,\ C=\int UR\,dz,\ B_R=\int R^2dz\) on one aperture. For a single charge of coefficient modulus \(d\), the integrated intensity ranges between \(B_R+Nd^2\mp2|C|d\) (omit \(R\) for a neutral-only bin and use the symmetric neutral state in this paragraph). The accessible \(d\) is the interval between the difference and sum of the two magnitudes multiplied by the appropriate \(|O_{jI}|\). Minimize at \(|C|/N\) clipped to that interval. These extrema are only marginal across different bins.

For **both** physical charges on the same aperture at the same W, the unpolarized opposite-helicity *sum* is a different observable. Neutral phase space cancels its wave normalization, and orthogonality of \(O\) removes the unknown interference between the two isospins exactly. Dividing by \(K\), the sharp lower bound at that W is
\[
 B_R+N(m_0^2+m_2^2)-2|C|(|O_{c0}|m_0+|O_{c2}|m_2).
\]
One cannot evade it by transferring strength from charged to neutral through a relative phase. Combine whole, potentially overlapping energy histograms by splitting **theory only** at their edges and summing appropriate single- or two-charge minima; never subdivide an observed count. The summed quantities in the joint table are integrated over W in **nb GeV**, not nb or counts of independent events. Like-helicity power can only raise each total. Negative excess is inconclusive, not proof of a solution. The quoted error boxes are deterministic. Mark II's primary table provides a 7% shared scale; Belle's pointwise quoted systematic is included once, not supplemented by another independently varied normalization absent a covariance decomposition. Energy bin means are uniform on each published interval as in the original work.

### 4. Bringing the correction back to the gravitational form factor

The two photons are on shell. Write \(f(x)=-F_3(-x)\) with spacelike momentum transferred to the common metric, \(x\ge0\). The retained real two-pion cut in a W window has the zero-transfer integrand \(dI_0=[\alpha/(2\pi)]\beta^3\,{\rm Re}[(h_c+h_n/2)A_\pi^*]\,dW/W^3\); both \(h\)'s here are **like helicity**. From the dispersion kernel \(1/(s+x)\), the *window* contributes \(\int s/(s+x)\,dI_0\) to \(f(x)\). Thus \(f(0)-f(u)\) weights it by \(u/(s+u)\), and \(f(0)-2f(u)+f(2u)\) by \(2u^2/[(s+u)(s+2u)]\). The latter kills both an arbitrary constant and an arbitrary linear local subtraction. It does not kill quadratic or higher local terms, nor constrain unobserved spectral channels. We use \(u=4m_\pi^2\), a specified scale, not a fitted one.

Apply each kernel inside both factors of the previous angular moment bound (not bundled here), carrying Mark II's shared normalization in the upper envelope. Uncertain opposite helicity is **not subtracted from data to tighten a gravity bound**. A direct combination of the three separately integrated \(f(x)\)'s checks signs and cancellations. These are conditional spectrally resolved parts of a metric response; the angular measurements do not measure gravity directly.
