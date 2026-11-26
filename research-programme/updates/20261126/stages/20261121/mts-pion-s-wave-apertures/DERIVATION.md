> Public reading copy: local links are mapped to released material or marked unavailable. Machine-specific passages, where present, have been omitted. See the inventory for the original digest.

# What the two-photon angular bins can tell the gravitational matching calculation

## S and D in the same physical convention

Write the normalized physical helicity amplitudes as \(M/(2e^2)\), \(z=|\cos\theta|\), \(W=\sqrt{s}\) in GeV. Call the like-helicity D projections \(h_j=\int_0^1 P_2 A_{++,j}\,dz\) for the physical charged and neutral channels \(j=c,n\). The retained signed gravity integrand uses \(H=h_c+h_n/2\), not an angular cross section. Isospin symmetry and the common charged pion mass are retained here. The rate is \(y_j=K_j(|A_{++}|^2+|A_{+-}|^2)\), \(K_c=2\pi\alpha^2\beta\,{\rm nb/GeV^{-2}}/W^2\), \(K_n=K_c/2\). Here the unit conversion is approximately 389379 nb per GeV⁻². All angular integrals in this note are over the folded variable. The geometry is that of each actual published bin.

Use the complex isoscalar and isotensor S waves of [Dai & Pennington, solution I, Fig. 22, Eqs. 1–7](https://arxiv.org/abs/1404.7524v2). Reading marked points, not fitting the curves to cross sections, gives both real and imaginary parts. Increasing energy follows the labels, not arc length. In our physical convention the S amplitudes are \(s_c=-(\sqrt2 S_0+S_2)/\sqrt3,\ s_n=\sqrt{2/3}(-S_0+\sqrt2 S_2)\). The extra neutral \(\sqrt2\) undoes the identical normalization already used by those authors. As sign and normalization controls a pure charged Born S wave \(b\) corresponds to \((-\sqrt{2/3}b,-b/\sqrt3)\) and produces \((b,0)\); the two isospin moduli independently reproduce the source's Fig. 16 S components. The figure comparison is a convention check within one paper, not a second experimental data set.

For the fixed-wave comparison \(B\) denotes the charged Born D projection, \(B(z)=(1-\beta^2)/(1-\beta^2 z^2)\), \(B_0=(1-\beta^2){\rm atanh}(\beta)/\beta\). Take
\[
 A_{++,j}=s_j+\mathbf1_c[B(z)-B_0]+(10/3)(H_{\rm ref}-B)P_2(z).
\]
This keeps the original isotensor D and all like-helicity higher waves. Integrating gives \(h_c=B+(2/3)(H_{\rm ref}-B)\), \(h_n=(2/3)(H_{\rm ref}-B)\). Opposite helicity is the scalar-QED Born amplitude for charged and zero for neutral **in this diagnostic only**. Rates are integrated uniformly in \(W,z\) within published, corrected bins; a detector response or alternative within-bin luminosity distribution is not known here. Using the real S in place of its *complex* value or dropping the S–D interference on a cut aperture is not this test. PCHIP fits no observations. The model-labelled sign reversal is an algebraic control on this window, not another globally admissible dispersive solution.

## Outer bound with unknown S and opposite helicity

On \(T=[.60,.75]\) put \(Q=2[\alpha/(4\pi)]\beta^3/W^3\), \(A=(1-.01W^2)\Omega(W^2)\) in the parent stress convention (not bundled here). Bound \(I_T=\int_T Q\,{\rm Re}(HA^*)\,dW\) in GeV⁻². This is one contribution to the hadronic two-pion cut, not a bound on the local subtraction, complete dispersion integral, or gravitational force. The stress and its continuation above the four-pion threshold are retained inputs.

Write \(A_{++,j}=s_j+5h_jP_2+R_j\), with arbitrary complex charge S,D waves. The essential *like-helicity higher-wave* assumption is \(R_c=B(z)-B_0-5BP_2,\ R_n=0\). No size, phase, angular momentum cutoff or shape for the opposite-helicity wave is needed for the outer bound. On a published W window of full width \(\Delta\), integrate over its intersection \(E\) with \(T\); define \(\widehat f=\int_E Q\,{\rm Re}(A^*f)dW\) and \(J=\int_E Q^2 |A|^2/K_j\,dW\). By positivity and Cauchy–Schwarz in energy, for each angular bin \(a\),
\[
 \left\langle(\widehat s+5\widehat h P_2+\widehat R)^2\right\rangle_a
 \le L_a=\Delta\,J\,y_a .
\]
On a partially overlapping energy bin, the full published count is an upper bound on the count in the overlap: **do not** prorate the observed count. Each charge separately covers \(T\) once. Multiply the projected neutral interval by 1/2 only when adding the intervals; the neutral rate already uses \(K_n\).

There are two checks. (i) Average over the measured aperture \([0,Z]\); \(p=P_2-\langle P_2\rangle,\ V=\langle p^2\rangle=Z^4/5\). Projecting out the unknown S gives center \(-\langle p\widehat R\rangle/(5V)\) and radius \(\sqrt{\langle L\rangle/V}/5\) for \(\widehat h\). This bound weakens when angular coverage shrinks, as it should. (ii) Simultaneously use **all** bin inequalities at a trial \(d=\widehat h\). With \(f=5dP_2+\widehat R\), each bin admits \(\widehat s=-\langle f\rangle_a\ \pm\sqrt{L_a-{\rm Var}_a(f)}\). Require every radicand nonnegative and the intervals to intersect. Projection of these convex constraints is an interval; bracket its extremes by bisection and round to the outside. Sum the resulting intervals across bins of energy and charge. This is an outer bound, not a claim that every endpoint is attainable; in particular energy Cauchy–Schwarz is an inequality. Both extractions are numerical quadratures for the assumed input functions, not interval arithmetic on the published form factors.

One can see why the higher-wave assumption matters: if \(R\) has an additional unknown component with rms across the aperture at most \(r(W)\), the radius of the continuous projection bound grows by at most \(\int_E Q |A|r\,dW/(5\sqrt V)\), before the channel weight. Without information about the angular region not measured or the higher waves there, a finite-aperture bound should not be advertised as model independent. Error-box repeats use all reported central values plus quoted stat and sys errors on the upper side, not a likelihood; Mark II's angular table lacks a quoted systematic per point.

## Constructive ambiguity: not just an interval that happens to cover zero

Keep the isotensor D and \(R\) above. Vary only the candidate isoscalar D by \(H=\nu H_{\rm ref}\). For any charge, start with zero S; a second construction subtracts the angular mean of its like-helicity amplitude over **one fixed** aperture \([0,.6]\) at every energy, including in the wider Belle bins. This gives a legitimate angle-independent complex S, constructed without selecting signs, errors or amplitudes from any observed MTS data. It is *not* the dispersively reconstructed S wave. For either construction, the predicted same-helicity intensity in each published bin is \(a\nu^2+b\nu+c\). Solve its inequality against the measured intensity and intersect the real roots over all 148 bins.

Inside that intersection the deficit \(d_a=y_a-\overline{K|A_{++}|^2}\) is nonnegative. An explicit opposite-helicity amplitude within that bin is \(\sqrt{d_a/K(W)}\,b(u)b(v)\), with \(u,v\) the bin-local affine coordinates in W and z and \(b(t)=\sqrt{630}\,t^2(1-t)^2\) on \([0,1]\), zero outside. Its mean square on the unit interval is one. Adjacent amplitudes and first derivatives join at zero, and their intensities add without interference. Fold symmetrically in \(z\) and extend by zero outside the aperture. Thus the entire unpolarized measurement can be reproduced with the specified \(H\) without changing the like-helicity isotensor/higher terms. These are mathematical counterexamples to *identification by intensities alone*: the witness nuisance powers intentionally depend on the observed bins. They are neither physical fits, new MTS predictions nor arguments that crossing, analyticity, two-body unitarity or threshold behavior of a global amplitude will allow these examples.

## Can opposite helicity limited to D already hide the sign?

For the **neutral** channel only, impose \(A_{++}=s+dP_2\), \(A_{+-}=b(1-z^2)\), with \(d=(10/3)(\nu H_{\rm ref}-B)\) fixed. Let energy averages include the positive weight \(K_n\). After angular bin averaging,
\[
 y^{\rm pred}_a=S+U p_a+D q_a+L(1-2p_a+q_a),\qquad p_a=\langle P_2\rangle_a,\ q_a=\langle P_2^2\rangle_a .
\]
Here \(D=\overline{K_n|d|^2}\) is fixed, \(L=(4/9)\overline{K_n|b|^2}\ge0,\ S=\overline{K_n|s|^2}\ge U^2/(4D)\), \(U=2\,{\rm Re}\,\overline{K_n s^*d}\). These conditions are necessary **and sufficient** for arbitrary energy dependence of the two nuisance waves on this energy bin, when \(D>0\). Indeed \(s/d=U/(2D)+i\sqrt{S/D-(U/2D)^2}\), \(b/d=(3/2)\sqrt{L/D}\) realize the moments. Different energy bins need not share phases or a smooth boundary value in this check. It does not impose a common charged/neutral dispersive solution. The simpler S-independent coefficient of \(P_2^2\) projects out the first two powers but can measure only \(D+L\) in this truncation, not \(D\) alone.

Minimize the maximum bin discrepancy divided by its stated error-box width \(e_a\). The upper bound is an actual realizable amplitude and the lower bound is a signed data contrast: for any weights \(w\) with \(\sum w<0,\sum w(1-2p+q)\le0\), set
\[
 \lambda_{\min}\ \ge\ {w\cdot(y-Dq)-D(w\cdot p)^2/(-\sum w)\over |w|\cdot e}.
\]
This follows by maximizing the weighted predicted nuisance term over the cone, not by trusting a solver status. Supporting planes to the quadratic constraint find weights and candidate amplitudes; both bounds are independently evaluated. A synthetic exactly feasible angular distribution and an incompatible pair of identical-angle measurements with known minimum budget 2 test both sides. A free quadratic intensity gives the common unconstrained lower benchmark, not a competing physics model. Quoted error boxes and energy windows are not assigned independent probabilities; there is no chi-square or statistical preference extracted here.
