# A longitudinal metric response with an experimental normalization

**Observable.** Use a covariant metric source, the canonical electromagnetic potential, Euclidean \(W=-\log Z\), Fourier derivative \(+ip_\mu\), and the vertex \(\Gamma=\delta^3W/\delta g_{00}\delta A_y\delta A_y\) (no stress factor of two). Let the photons carry \(p=(p_0,\mathbf r), k=(k_0,-\mathbf r)\), with no momentum in \(y\); \(q_0=-p_0-k_0\ne0\), \(L=p^2, H=k^2\). A time displacement \(\xi^0(q)\) gives \(\delta g_{00}=2iq_0\xi^0\) and \(\delta A_y=\xi^0\partial_0 A_y\). Two photon derivatives of coordinate invariance give

\[
2q_0\Gamma=-p_0\Pi_{yy}(k)-k_0\Pi_{yy}(p),\qquad
\Pi_{yy}(p)=L[Z-\Delta\alpha(-L)] .
\]

The contact terms from varying the photons are essential. This uses a common covariant metric and a flat rotation-invariant vacuum; it is not an identity of an arbitrary finite lattice at fixed spacing. For the hadronic part alone \(Z\) may include any chosen local Maxwell contact. A metric perturbation that is purely a coordinate change has zero linear curvature: adding an arbitrary finite \(C_{\mu\nu\rho\sigma}F^{\mu\nu}F^{\rho\sigma}\) leaves this measurement unchanged.

**Exact kinematics.** Choose \(p_0=-L/\sqrt{H+L},\ k_0=H/\sqrt{H+L},\ |\mathbf r|^2=LH/(H+L)\). Then \(p_0 H+k_0 L=0\). In particular the charge renormalization cancels without choosing its value:
\[
\Gamma=\frac{LH}{2(H-L)}[\Delta\alpha(-H)-\Delta\alpha(-L)] .
\]
For \(L=1.81,H=6.07\ {\rm GeV}^2\) the factor is \(1.28951878\ {\rm GeV}^2\). [OPAL](https://arxiv.org/abs/hep-ex/0505072) measured the running using small-angle Bhabha scattering; use its **lepton-subtracted difference**, not the quoted total. The implied hadronic metric vertex is \(0.0030562\ {\rm GeV}^2\) with separate errors \(0.000748,\ 0.000554,\ 0.000387\ {\rm GeV}^2\) (statistical, experimental systematic, theoretical). OPAL did not measure a graviton. The step between its two-current result and this vertex is a prediction of the conservation identity, shared with conventional covariant matter. The calculation tests the retained MTS source normalization, not a preference over GR.

**Verification without a gravity fit.** The analytic massive-vector mixing control in empirical.py and charge_free.py independently varies the kinetic and mass stresses. At the exact kinematics the kinetic cross term vanishes, leaving \(M^2b(L)b(H)/2\), \(b(x)=-g x/(M^2+x)\). Away from that condition both terms survive and agree with the source-subtracted expression below. For a unitary diagonal current with \(\Delta\alpha(-x)=e^2\int x\rho(s)/[s(s+x)]ds\), the exact-kinematics result is \(e^2 LH/2\int\rho(s)/[(s+H)(s+L)]ds\). The sign is nonnegative in this convention. This argument says nothing about positivity of a *transverse stress* spectral density.

**What lattice data give.** [Cè et al.](https://arxiv.org/abs/2203.08676) give \(0.0033313(438)\ {\rm GeV}^2\) for four flavors (absolute propagated uncertainty 0.0000438). The [connected-bottom moments](https://arxiv.org/abs/2101.08103) yield a small positive addition: expand \(1/[(1+Lu)(1+Hu)]\) for \(u=1/s\), using the integral remainder, not an assumption of series convergence on all support. Alternating derivatives have fixed sign on \(u\ge0\); the degree-three and degree-two polynomials bracket the kernel. The central bottom difference in running is \(1.4200\)–\(1.4202\) times \(10^{-5}\); its moment uncertainties are larger. With this term the older central metric result is 0.0033496. The bottom-only correction is not a bound on omitted disconnected or isospin-breaking effects.

The [updated calculation, Eqs. 5.67–68](https://arxiv.org/html/2511.01623v2#S5.SS1) gives \(0.00333551\pm0.00001389\ {\rm GeV}^2\) using its Padé as published, no extra bottom added, no isospin-breaking correction. This error propagates its *full covariance*, including correlation between the two momenta. It does not include unknown interpolation bias. The older and newer lattice analyses are related, not independent discoveries. Both are continuum comparisons, not correlators measured on the D450 chain alone.

**Independent-of-interpolating-form check.** Use the updated work's final five-flavor, isospin-symmetric table, in units of \(10^{-5}\). For \(f_s(x)=x/(s+x)\), let \(P\) interpolate at \(n\) knots \(x_i\). Subtract the interpolant and factor its numerator to get exactly
\[
 f_s(x)-P(x)=(-1)^{n+1}\frac{s}{s+x}\prod_i\frac{x-x_i}{s+x_i}.
\]
Its sign is independent of \(s>0\); integration against the positive spectral measure preserves the bound. For each endpoint use all two-, three-, and four-knot subsets of the five nearest knots (zero is an exact available knot). Subtract opposite-side bounds, **collect coefficients of shared knots first**, then bound linear errors by \(\sum |w_i|\sigma_i\). The tightest of these valid bounds is still valid; no kernel or MTS parameters are learned. Treating the central knots as exact gives necessary bounds [0.00331109, 0.00335304]. Allowing each knot to vary anywhere within its own quoted total error gives [0.00323141, 0.00342911] GeV². These are outer bounds conditional on the simultaneous error box and positivity, **not** a confidence interval or proof that every point is attainable. The published Padé estimate lies within both. Exact rational witness weights are in spectral-anchor.json.

**Periodic momenta without retuning the charge.** At arbitrary momenta the unit Maxwell vertex is \(G_0=(p_0k_0+|\mathbf r|^2)/2\). Subtract a multiple of the lower-momentum current response:
\[
\Gamma_*=\Gamma-G_0\,\Pi(p)/L
 = \frac{p_0H}{2q_0}[\Delta\alpha(-H)-\Delta\alpha(-L)].
\]
On a lattice let \((S_0,K_p,K_k)\) be the explicitly computed *unit* Maxwell template for a displacement and two currents, with \((S,P_p,P_k)\) the ensemble values in the same conventions. The combination
\[
 S_* = S-S_0P_p/K_p,\quad P_*=P_k-K_k P_p/K_p,\quad D_*=S_*+ip_0P_*
\]
is **exactly invariant** under adding any multiple of that Maxwell template, even when the template itself fails the continuum identity. In the continuum \(S_*/(2iq_0)=\Gamma_*\) and \(D_*=0\). This subtraction removes a known contact, not every regulator effect. On the coarse noncommuting fixture \(D_*\) has absolute magnitude 1.505 per site, not zero. No coefficient was tuned to cancel it.

Using the [D450 scale and geometry, Table I](https://doi.org/10.1103/qh7q-9nyy) (\(a\simeq0.0756\) fm, temporal extent twice the spatial extent), enumerate periodic current momenta of the specified opposite-time-sign family with \(0.25\le L<H\le12\ {\rm GeV}^2\). Minimize squared log-distance to the two OPAL virtualities using *only kinematics*. For \(p_t=-2\pi m/128,\ k_t=2\pi n/128\) the continuum Maxwell zero requires \(mn=4(n_x^2+n_z^2)\). Two useful choices:

| Choice | \((m,n;n_x,n_z)\) | \((L,H)\), GeV² | Continuum \(\Gamma_*\), GeV² |
|---|---:|---:|---:|
| Closest in virtualities | (10,19;1,1) | (1.773,6.058) | 0.008828 ± 0.000037 |
| Closest with continuum Maxwell vertex zero | (5,16;4,2) | (1.724,5.516) | 0.0030934 ± 0.0000126 |

Errors here are only the updated Padé parameter uncertainty at the nominal momenta. These target *different tensor kinematics*, not discrepant measurements of one number. Even on the second choice the particular lattice Maxwell template gives a nonzero metric vertex \(-0.0002990\ {\rm GeV}^2\) per unit coefficient. The larger finite-spacing Ward defect of that control is separately recorded. D450 has a roughly 219 MeV pion; do not demand physical five-flavor answers on one finite, heavier-mass, 2+1 ensemble. These are measurement designs, not new D450 data.
