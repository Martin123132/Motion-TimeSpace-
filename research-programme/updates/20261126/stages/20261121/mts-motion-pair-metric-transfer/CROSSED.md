> Public reading copy: local links are mapped to released material or marked unavailable. Machine-specific passages, where present, have been omitted. See the inventory for the original digest.

# Can the two retained contacts generate a genuine angular change together?

Yes if **both** contacts are present, at the next crossed-channel loop order. This is separate from dressing a graviton propagator with a scalar pair. The result is proportional to the *product of existing coefficients*, not a fitted number. The minimally factorized branch has no tree constitutive portal \(\eta\), so this term vanishes there. Do not set a positive vacuum value of \(\eta\) from a bound on a rolling background.

## Cut and crossing

Use the retained on-shell contact vertex definitions (not bundled here). Cross one photon and one scalar into physical Compton scattering at invariant \(v>m^2\). Let \(p=(v-m^2)/(2\sqrt v)\) and \(z\) be the cosine between incoming and outgoing photon directions. Contracting the two field strengths and scalar momenta gives a helicity-flip amplitude \(-\eta p^2(1-z)\) and a physical helicity-preserving amplitude \(\lambda v p^2(1+z)\). The other helicity at each vertex is zero. Here the photon gauge-kinetic seagull is normalized as \(\eta F_1:F_2/2\). All polarizations are referred to their own momenta; the sign phases in physical Compton and all-incoming pair kinematics are not interchangeable.

Both contact amplitudes have **only \(J=1\) in this crossed channel**, since \(d^1_{\pm1,\pm1}=(1+z)/2\), \(d^1_{\pm1,\mp1}=(1-z)/2\) in the chosen helicity phases. In the \(16\pi(2J+1)t_J d^J\) normalization,
\[
 t_1={p^2\over24\pi}
 \begin{pmatrix}\lambda v&-\eta\\-\eta&\lambda v\end{pmatrix},\qquad
 {\rm Im}\,t_1\big|_{\gamma\phi}=(1-m^2/v)t_1t_1^\dagger .
\]
The on-shell \(\gamma\phi\) pair is distinguishable. The helicity-flip discontinuity vanishes at both \(\eta^2\) alone and \(\lambda^2\) alone; the off-diagonal term is from the two mixed orderings. Strip \(F_1:F_2/2=-p^2(1-z)\) from the Compton amplitude. Its invariant coefficient has
\[
 {\rm Im}\,C(v)\big|_{\eta\lambda}={\eta\lambda\over48\pi}
       {(v-m^2)^3\over v}\,\theta(v-m^2).
\]
The physical equal-helicity two-photon amplitude has this coefficient in the two crossed channels \(C(t)+C(u)\). The scalar is real and the two orderings add. Here \(s=W^2,\ t,u=m^2-s/2\pm s\beta z/2\le0\). The cut is not being taken at a negative physical pair invariant. This isolates the specified two-contact monomial and intermediate state, not mixed Einstein/portal, charged-particle, graviton or other cuts at the same external kinematics.

## The local ambiguity and how to remove it

For two on-shell equal-helicity photons the local parity-even scalar-pair amplitude is their field-strength spinor factor (dimension two) times a symmetric polynomial in \(t,u\). Up to a linear polynomial, \(t+u=2m^2-s\) is angle independent. Degree two is the first local possibility for a D wave, i.e. dimension ten in four dimensions. An explicit on-shell example is \(d(F_1:F_2)[(p_3k_1)(p_4k_2)+(p_3k_2)(p_4k_1)]\), obtainable from two differentiated scalar and two differentiated field-strength factors. Its D coefficient has magnitude \(|d|s^3\beta^2/12\). This is a nuisance direction, **not** a new assumed MTS coupling.

Define \({\cal B}(s)=15\langle P_2[C(t)+C(u)]\rangle/(s^2\beta^2)\), with \(\langle\cdot\rangle=\tfrac12\int_{-1}^1dz\). A subtraction \(C(v)\mapsto C(v)+c_0+c_1v+c_2v^2\) shifts this by **exactly \(c_2\)**. It cannot change \({\cal B}(s_2)-{\cal B}(s_1)\). In the local EFT the mixed discontinuity increases as \(v^2\); an absolute D normalization cannot be inferred by extending an unsubtracted dispersion integral to infinity.

For \(h=s\beta/2,\ A=v-m^2+s/2\), the projected resolvent is \(L(v,s)=15 Q_2(A/h)/(2h^3)\). Its asymptotic \(1/v^3\) explains the logarithmic matching ambiguity. Over any specified crossed interval the signed contribution to the difference is \(\pi^{-1}\int {\rm Im}C(v)[L(v,s_2)-L(v,s_1)]dv\). Direct three-subtraction dispersion followed by angular integration, both with zero and with nonzero arbitrary subtraction coefficients, verifies this independently. Example: \(s_1=5m^2,s_2=12m^2,v_{\max}=16m^2\) yields \(-0.000721707\,\eta\lambda\). All nine checks (not bundled here).

## Propagate into the finite-distance response

Use only \(m^2<v<\Lambda^2,\ 4m^2<s<\Lambda^2\) with \(\Lambda=10^{-3}\) eV, the old low-energy witness, not a claimed hard boundary of the Universe. For the direct finite-window calculation choose the twice-subtracted representative
\[
 C(v)={\eta\lambda v^2\over48\pi^2}
   \int_{m^2}^{\Lambda^2}{(1-m^2/w)^3\over w-v}\,dw,\qquad v=t,u .
\]
Any third-subtraction change is a quadratic polynomial on this window. The identical-real-scalar final-state factor and canonical traceless stress give \(dI_{\eta\lambda}/ds=s\beta^5{\cal B}(s)/(1920\pi^2)\) in the prior Born-positive pair convention (\(F_1:F_2/2=s/2\) there). This is the two-scalar cut fed by the crossed \(\gamma\phi\) discontinuity; other discontinuities of the full higher-order amplitude have not been counted. No nonzero local \(c_2\) has been smuggled into the signed table as a prediction.

For \(k_b=U(Wb)-U(2Wb)\), let \(I_b=\int s\beta^5 k_b\,ds\) over the fixed pair interval and \(\widehat B_b=1920\pi^2 D_{\eta\lambda}(b,2b)/I_b\). It is the weighted mean of \(\mathcal B\). A common quadratic subtraction in \(C\) therefore cancels **exactly** from \(\widehat B_{2b}-\widehat B_b\). The three distances use the same matter, spectral intervals and polarization conventions. The reducible metric piece must first be removed with the matched [common transfer](METRIC.md); this is not a null for arbitrary metric, medium, UV form factors or higher-derivative operators. Band-limited moments are calculational contributions, not an experimental energy cut on virtual pairs.

For \(m\ll W\ll\Lambda\), \(C(v)=-\eta\lambda v^2\ln(-v/\Lambda^2)/(48\pi^2)\) up to a quadratic subtraction and higher derivative orders. Thus the logarithmic slope of \(\mathcal B(s)\) is \(-\eta\lambda/(48\pi^2)\). When \(mb\ll1\ll\Lambda b\), \(I_b\to90/b^4\); rescaling \(Wb\) shows that the difference of the two normalized moments tends to \(+\eta\lambda\ln2/(24\pi^2)\). This identifies a nonanalytic shape, not the absolute strength of the unknown portal. At \(b=1\) cm, using the fixed window and the fast pole, the calculated multiplier is 0.00289571; at 10 cm it is 0.00292596 versus the scaling limit 0.00292627. For the frozen 3/6/12-fm distances the same low-energy window gives only \(1.35\times10^{-24}\) times the product in the **normalized difference**. Naively subtracting two floating-point averages would print zero. We evaluate the covariance with the analytic small-argument difference of the normalized weights there. Finite-window spectra, raw representative and shape (not bundled here).

Mass dimensions: \(\eta\lambda\) and \(\widehat B\) have units energy⁻⁶; \(D\) has units energy⁻². The raw finite-window column is in eV⁴ per \(\eta\lambda\) expressed in eV⁻⁶, with the representative above; the two-mean difference divided by \(\eta\lambda\) is dimensionless. The medium with nonzero occupation or truly spacetime-dependent coefficients is not represented by this vacuum cut.
