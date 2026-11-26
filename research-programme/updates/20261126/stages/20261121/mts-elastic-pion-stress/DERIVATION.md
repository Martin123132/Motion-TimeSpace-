> Public reading copy: local links are mapped to released material or marked unavailable. Machine-specific passages, where present, have been omitted. See the inventory for the original digest.

# Matching two real photons to the total pion stress

Use the retained normalization in the parent cut (not bundled here). Set \(s=W^2,\ a=4m_\pi^2,\ \beta=\sqrt{1-a/s}\). \(m_\pi=0.1395704\) GeV (the charged mass, including for neutral pions in this isospin-limit calculation). For each physical charge channel \(h_i=(2e^2)^{-1}\int_0^1 P_2 M_{++}^{i}\,dz\). Write \(H=h_c+h_n/2\). The factor \(1/2\) is neutral identical-particle phase space, not a missing neutral force. The physical quantity integrated is
\[
 I_{[l,u]}={\alpha\over4\pi}\int_{l^2}^{u^2}{\beta^3\over s^2}
       \operatorname{Re}[H(s)A_\pi^*(s)]\,ds.
\]
This is a linear interference, not the integral of an intensity. Only the spin-two part of the total pion stress contributes; the independent scalar trace or pion D-term is not inserted here. One-loop charged-scalar Born production with \(A=1\) gives \(I_{[2m,\infty]}=\alpha/(720\pi m^2)\), checked independently by angular integration.

## Removing the normalization ambiguities

- In the [Dai–Pennington convention](https://arxiv.org/abs/1404.7524v2), the spherical harmonics of Eq. (3) imply \(h_c=F^{+-}_{20}/\sqrt5\). Their neutral amplitude absorbs identical-particle normalization, so \(h_n=\sqrt{2/5}F^{00}_{20}\). Their isospin rotation therefore gives \(H=-\sqrt{3/10}\,F^0_{20}\) and **annihilates \(I=2\)**. Their Appendix A charged Born wave divided by \(\sqrt5\) matches the direct angular integral including sign. Their Fig. 3 displays \(|F|\): only its magnitude is used. Black is the solution and green the dispersive constraint; they need not coincide. The Born comparator in this work is the analytic D wave, not the unrelated dashed curve marked B.
- In [García-Martín & Moussallam](https://arxiv.org/abs/1006.5373v1), partial waves of the helicity amplitude expand with \(2J+1\). The charged Born wave in their normalization is twice our \(B=h_c^{\rm Born}\). Their isospin rotation acts on \((\sqrt2 h^c_{\rm GM},h^n_{\rm GM})\). It follows that \(H=-\sqrt3 h^0_{2,++}/4\). Both conversions are verified on the full Born angular response at 45 energies. No overall sign was chosen by comparing fit quality.
- [Cao, Guo, Li & Yao](https://arxiv.org/abs/2411.13398v2), supplementary D-wave construction, give \(A_\pi=P\Omega,\ P\simeq 1-0.01s\) (with \(s\) in GeV²), normalized to the **total** stress at \(s=0\). The source estimates its slope by tensor resonance saturation. The two real-valued curves for the complex \(\Omega\) are read separately; the spacelike \(A_\pi\) figure is reserved for checking, not for determining the timelike normalization.

## Signed photon wave

Employ the one-channel, subtracted \(I=0,J=2,++\) representation of García-Martín & Moussallam with their fitted \(c^{(0)}=0.22\ \mathrm{GeV}^{-6}\) and the updated common \(\Omega\) above. This **hybrid evaluation** is not a reproduction or refit of either paper's set of parameters. For \(D=s^2(s-a)\), \(\Omega=|\Omega|e^{i\phi}\), and \(c_H=-\sqrt3\,c^{(0)}/4\),
\[
 {H\over\Omega}
 = B\,{\operatorname{Re}\Omega\over|\Omega|^2}
 +D\left[c_H+s\,L(s)+{s\over\pi}\operatorname{PV}\!
            \int_a^\infty {K(v)\over v-s}\,dv\right],
 \qquad K(v)={B(v)\operatorname{Im}\Omega(v)\over|\Omega(v)|^2 v^3(v-a)}.
\]
On the upper rim \(1/(v-s-i0)\) adds \(+i\pi K(s)\) inside the unprojected integral. It cancels the imaginary part of \(B/\Omega\); hence \(H/\Omega\) is real in the elastic region but **not necessarily positive**. The product used in the integral is \(P|\Omega|^2 H/\Omega\). Its sampled sign is an output. This identity also explains why no division by a tiny threshold phase or measured imaginary part is needed. The Coulomb and charged/neutral mass-splitting corrections are not included; \(0.540<4m_\pi\) under the stated equal-mass convention.

Here \(L(s)=\int_{-\Lambda}^{-s_R}[\operatorname{Im}H_R(v)/\pi]/[\Omega(v)v^3(v-a)(v-s)]\,dv\), summed over the retained crossings. For \(s_R=(m_R^2-m_\pi^2)^2/m_R^2,\ X^2=1+4m_R^2(v+s_R)/[v(v-a)]\), the vector numerator is \(-(\widetilde C_c+\widetilde C_n/2)m_R^2(3X^2-1)/\beta(v)\); reverse its sign for axial vector, multiply the vector expression by \(4v+3s_R\) with the tensor's own coupling for tensor exchange. Applied here to \(\rho,\omega,\phi,a_1,b_1,h_1,a_2\); numerical couplings are the published central entries/estimates, with rounded resonance masses listed in the script. Unknown or higher resonances, including unmeasured axial tensors, are not asserted absent. Tensor coupling units are GeV⁻⁴ as follows from the radiative width, vector and axial-vector units GeV⁻². The cutoff is \(\Lambda=5\) GeV² centrally, with 3 tested separately. The finite resonance sum and sharp left-cut cutoff are modeling choices.

For negative \(v\), evaluate \(\log\Omega(v)=(v/\pi)\int_a^\infty\phi(t)\,dt/[t(t-v)]\). Read \(\phi=\arg\Omega\) from the two plotted curves to \(W=2\) GeV. Above that, continue the **phase itself** to \(\pi\) as \(2/[1+(W/2)^p]\) times its endpoint deviation, \(p=3\) (also 2,5); for the small right-cut tail take \(|\Omega|=|\Omega(4)|4/t\). These are our explicit tail prescriptions, not the source's continuation of phase *shift and inelasticity* separately. The reconstruction gives \(\Omega'(0)=0.62855\ \mathrm{GeV}^{-2}\); the source's approximate polynomial and tensor mass imply about \(0.625\). At the lower endpoint only, from \(2m_\pi\) to the first plotted stress knot, hold the real part fixed and the imaginary part zero. It affects the separately reported threshold sliver, not the choice of sign. Interpolation of pinned figure coordinates is piecewise linear in \(W\); fine steps in the smallest imaginary part reflect plotting resolution.

## Distinguishing sensitivities

Changing only \(c^{(0)}\) leaves an exactly affine change:
\[
 {\partial I\over\partial c^{(0)}}=
 -{\sqrt3\over4}{\alpha\over4\pi}\int ds\,
 {\beta^3\over s^2} P|\Omega|^2 s^2(s-a).
\]
On the specified interval this is \(-3.97\times10^{-6}\ \mathrm{GeV}^4\); the independent finite difference at fixed cutoff agrees. Varying just this subtraction is not varying a local curvature contact in the parent action: the two coefficients have different dimensions, operators, and observational roles. The values 0.10 and 0.19 in the checks are the source's sum-rule alternatives at their **respective** left-cut cutoffs, not independent standard deviations.

The alternate pole calculation isolates the singular source panel, applies a Cauchy quadrature there, and independently integrates both unsubtracted sides. The main calculation instead removes \(K(s)\) globally and integrates its logarithm analytically. Refining panels next to sharp digitized corners was necessary for their agreement. The separate spacelike stress check does not establish a precise confidence interval for the timelike form factor. This work uses imported low-energy amplitudes to improve the matching calculation; it proves no new existence theorem, mass gap or microscopic contact normalization.
