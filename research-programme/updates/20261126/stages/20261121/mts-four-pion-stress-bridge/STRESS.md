> Public reading copy: local links are mapped to released material or marked unavailable. Machine-specific passages, where present, have been omitted. See the inventory for the original digest.

# Four-pion stress from the same minimally coupled pion action

This is a **tree-level low-energy QCD estimate**, made with the physical charged mass for all three pion species and \(F=0.0924\) GeV. We import the leading massive two-flavor chiral action, not a new fundamental MTS degree of freedom. See [Bijnens & Husek, massive nonlinear sigma model and four-pion amplitude](https://doi.org/10.1103/PhysRevD.104.054046) and [effective pion action with an external metric](https://doi.org/10.1103/PhysRevD.102.076023). What is calculated here is its vacuum-to-four-pion spin-two matrix element, inclusive flavor sum and phase space in the normalization of the matching test. No gravitational width or four-pion vertex was fitted.

In mostly-minus particle conventions set the fourth embedding coordinate to \(\sqrt{F^2-\pi^2}\). The interaction through four fields is
\[
 {\cal L}_4=\big[(\partial_\mu(\pi^2))^2-m^2(\pi^2)^2\big]/(8F^2).
\]
Label four outgoing momenta \(p_i\), \(Q=\sum p_i\). For each unordered partition \(ab|cd\) multiply by \(\delta_{a b}\delta_{c d}\) on **flavor** indices. Write \(P=p_a+p_b,\ R=p_c+p_d,\ k_i=Q-p_i\), and
\(K^{\mu\nu}(u,v)=-u^\mu v^\nu-v^\mu u^\nu+g^{\mu\nu}(u\cdot v+m^2)\).
The matrix element for this partition, before spin projection, is
\[
 T^{\mu\nu}_{ab|cd}={1\over F^2}\left[K^{\mu\nu}(P,R)
 -\sum_i K^{\mu\nu}(p_i,k_i)\,{s_{\text{opposite pair to }i}-m^2\over k_i^2-m^2}\right].
\]
The first term is the metric variation of the four-field contact. For the second, attach the quadratic stress to a pion leg and join the internal propagator to the strong four-point vertex. The minus is from the propagator times the strong vertex. \(Q_\mu K^{\mu\nu}(u,v)=-(u^2-m^2)v^\nu-(v^2-m^2)u^\nu\): the divergence of the pole terms cancels the contact *for each partition*. The contact alone fails. The spatial trace-free two-pion element for back-to-back momenta is \(2[p_i p_j]_{\rm TF}\), fixing the stress sign against the parent.

**Independent field-coordinate check.** Restrict to four neutral external pions. In the angle coordinate the kinetic term is exactly quadratic and the mass potential is proportional to \(\cos(\varphi/F)\). The only strong four-field vertex is then \(+m^2/F^2\) (vertex without \(i\)). The spatial trace-free stress is \(-2m^2\sum_i [\mathbf p_i\mathbf p_i]_{\rm TF}/[F^2(k_i^2-m^2)]\). This agrees with the sum of the three Cartesian partition tensors, although the Cartesian formulation has a large contact absent in the angle coordinate. This check is of the all-neutral amplitude, not permission to discard the other charge channels.

**Flux-normalized norms.** Fix one unit spatial, symmetric trace-free polarization in the overall CM. Rotational averaging gives \(\langle |e:T|^2\rangle=\|T_{\rm TF}\|^2/5\). For the Cartesian flavor sum the three partition tensors \(T_j\) have Gram matrix 9 on the diagonal and 3 off it. Consequently \(\sum_{\rm flavors}|T|^2=6\sum_j\|T_j\|^2+3\|\sum_j T_j\|^2\) for the trace-free tensors. Integrate with \(1/4!\), since all labeled momenta/flavors are summed. The corresponding point two-pion norm is \((3/2!)\beta/(8\pi) (not bundled here)|\mathbf p|^4/5\); the dispersive reference multiplies this by \(|A_\pi(s)|^2\). Only like normalizations may be divided to obtain \(r_T\).

The four-body integral factorizes with \(ds_{12}\,ds_{34}/(2\pi)^2\) and three two-body phase spaces \(\lambda^{1/2}(s,a,b)/(8\pi s)\) integrated over orientation. Retain both pair decay polar angles and their relative azimuth; integrate over global orientation by the spin average, not by assuming independent pion directions. The implementation checks both momentum conservation and on-shellness. For a constant massless integrand the unsymmetrized phase volume is \(s^2/[24(4\pi)^5]\). The numerical check differs by \(6.6\times10^{-13}\) relatively.

**Threshold law, including its coefficient.** Write \(\epsilon=W-4m\) and take it positive and small. Each pole ratio tends to \(3/8\). On the nine-dimensional CM momentum sphere define the three orthogonal Jacobi vectors \(\mathbf u_j=\mathbf p_1+\mathbf p_{j+1}\), \(j=1,2,3\); \(\sum_j u_j^2=\sum_i p_i^2=2m\epsilon\). Put \(U_j=[\mathbf u_j\mathbf u_j]_{\rm TF}\) and \(S=\sum U_j\). Then \(T_j=2(U_j-3S/8)/F^2+O(\epsilon^2)\). Sphere averaging gives \(\langle U_j:U_k\rangle=0\) for \(j\ne k\) and \(\sum\langle U_j:U_j\rangle=(10/33)(2m\epsilon)^2\). The flavor sum, polarization average and identical-particle factor therefore give
\[
 \rho_{T,4}={29\over704}{(2m\epsilon)^2\over F^4}\Phi_{4,\rm NR}
  [1+O(\epsilon/m)],\quad
 \Phi_{4,\rm NR}={m\over8(2\pi)^8(2m)^4}
 {2\pi^{9/2}\over\Gamma(9/2)}(2m\epsilon)^{7/2}.
\]
Thus the leading spectral norm **squared** is \(1.77704\times10^{-5}\ {\rm GeV}^{-3/2}\,\epsilon^{11/2}\); it has units GeV⁴, with no additional optical-theorem factor in this phase-space-norm definition. Extrapolating the two finest excess energies to zero reproduces this coefficient within \(10^{-6}\) relatively. The calculation at 0.8 GeV uses the **relativistic** momenta, propagators and phase space, not this power law. Chiral loops, higher operators, mass splitting, electromagnetic final-state effects and multipion rescattering are not part of that estimate.
