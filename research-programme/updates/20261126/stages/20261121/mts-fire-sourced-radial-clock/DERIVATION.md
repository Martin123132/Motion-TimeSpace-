> Public reading copy: local links are mapped to released material or marked unavailable. Machine-specific passages, where present, have been omitted. See the inventory for the original digest.

# A radial lapse from the two Einstein constraints

The retarded tangent and its adjoint (not bundled here) distinguish the clock potential left out of the driving Hamiltonian from the Poisson response of the changing wave density. Only the former belongs here. Use the normal-energy construction (not bundled here) and the original fast-carrier-averaged, real heavy matter stress. This is a scalar weak-field calculation within the retained common Einstein metric, not an independent derivation of the Einstein action. All state-dependent products are computed *before* taking the spherical average.

## Radial inverses and their integration constants

Let \(y=r/L,\ \epsilon=v^2/c^2,\ U/v^2=V=V_o+h,\ \Psi/v^2=V+\epsilon P,\ \Phi/v^2=V+\epsilon Q,\ Z=P-Q\), with \(h\) the Newtonian potential of the wave. In the parent's Poisson and wave normalization set
\[
 W=\langle V^2\rangle/2,\qquad f=(\langle|\nabla a|^2\rangle-\langle|\nabla V|^2\rangle)/2,\qquad
 T=\langle |a_y|^2-|\nabla_\Omega a|^2/(2y^2)+V_y^2-|\nabla_\Omega V|^2/(2y^2)\rangle .
\]
Here \(a\) is the leading wave. For the canonical radial source, holding the remaining ordinary first-order densitized energy and stress terms out of the drive, \(\Delta_0(P-W)=f,\ Z''-Z'/y=2T\). The ordinary *Newtonian* potential and its cross terms remain in both. For the edge \(R\) of the wave mesh and \(M_f(y)=\int_0^y s^2 f(s)\,ds\),
\[
 Q(y)=W(y)-M_f(y)/y-\int_y^R s f(s)\,ds
       -\int_y^R (s^2-y^2)T(s)\,ds/s + C-m_0/y+I y^2 .
\]
The solution finite at the origin with no extra unresolved point mass has \(m_0=0\). A phase convention removes \(C\) from the wave readout. For an isolated continuation the exterior source fixes \(I=\int_R^\infty T(s)ds/s\). Without that information it is a separate coefficient. In particular the value of \(Q\) on the outermost saved node is **not** set to zero. For the compensated *direct* three-radius statistic the two homogeneous force modes cancel; for the *propagated wave* their effects need not cancel. See the two homogeneous-mode budgets (not bundled here).

Use even orthonormal Legendre modes on the northern hemisphere with reflection symmetry. For a density coefficient \(\rho_l\), the regular open Green function is \(-[A_l+B_l]/(2l+1)\), with \(A_l=y^{-1}\int_0^y(s/y)^l s^2\rho_l\,ds,\ B_l=\int_y^R (y/s)^l s\rho_l\,ds\). Scale inside/outside recurrences by the *local* radius; no huge powers or artificial outer-wall potential are required. Reconstruct through \(l=68\) for the square of the \(l\le34\) wave. Reconstruct the ordinary foreground from its archived angular samples; extrapolate \(yV_o\) one node at the outer edge rather than setting it to zero there. Check both the native gravity solver and the angular reconstruction through \(l=150\). Integrate half-shell controls and the entire wave domain with finite-element Gauss quadrature, testing different radial orders. Time-center sources by averaging **evaluated endpoint profiles**, also checked with separately evolved half-step waves.

For the alternative in which the ordinary *proper*, not densitized, first-order normal energy is held fixed, the extra Poisson source is \(-3\langle V\Delta V_o\rangle\). Avoid differentiating noisy foreground data twice for this solution: \(X=\langle\nabla V\cdot\nabla V_o\rangle,\ A=\langle V V_{o,y}\rangle\) give the extra radial derivative \(-3(A-M_X/y^2)\). Integrating gives \(3[\int_y^R A\,ds-M_X/y-\int_y^R sX\,ds]\) up to a constant. Apply this change consistently **during transport and at readout**. The baseline drive excludes ordinary intrinsic first-order energy and anisotropic stress that the archive does not supply. Common intrinsic terms can still act on the difference of the two wave kernels. Neither convention purports to evolve stellar or gas stress.

## Outside the mesh

For a harmonic vacuum continuation, \(V_l(y)=v_l(R)(R/y)^{l+1}\) gives \(I=\sum_l(l+1)v_l(R)^2/(4R^2)\). Neither exterior vacuum nor vanishing exterior matter stress is inferred from the data. Keep the alternative \(I=0\) and the gain for unrestricted \(I\) in the results. For an explicit *conditional* bound on the omitted ordinary Newtonian continuation assume only \(\|\nabla(V_o-V_{o,\rm harm})\|_{\rm angular\,RMS}\le B(R/y)^2\) outside the box, with the **archived finite-support wave**. Each harmonic field obeys \(\|\nabla h(y)\|\le (R/y)^2 g_h(R)\), \(g_h(R)=\sqrt{\sum(l+1)(2l+1)h_l(R)^2}/R\). Cauchy–Schwarz on the radial-minus-half-tangential quadratic form and \(\int_R^\infty (R/y)^4 dy/y=1/4\) give
\[
 |\Delta I_{\rm mean}|\le (2B g_{\rm mean}+B^2)/4,\qquad
 |\Delta I_{\rm difference}|\le B\,g_{h_c-h_r}/2.
\]
Contract these envelopes with the absolute time-resolved kernel acting on \(y^2\); the mean and difference are distinct. This bound applies neither to unknown PN ordinary stresses nor to extra wave occupation outside the archive. A common lapse constant is checked separately and has no resolved response.

## What enters the wave

Take the incident field, occupations, static foreground and saved FIRE changes unchanged at 590. Add the source above as an extra \(Q_{\rm ext}(t,y)\) in the derived first-order wave equation, not a modifiable galaxy coupling. Run the source through the prior tangent and separately form
\[
 \delta A=\sum (G_c-G_r)\bar Q+\sum (G_c+G_r)(Q_c-Q_r)/2 ,
\]
where the angular sum is performed on the previously retained kernels, not by discarding angular structure in the underlying waves. The new state-density contribution enters the two scalar gradients equally. Adding this \(Q_{\rm ext}\) to endpoint metric forces *again* would double count the earlier canonical constraint calculation. With the alternative ordinary conversion only, the extra direct conversion must also be included once. Purely radial transport is not a solution of all nonspherical lapse multipoles or of the shift.
