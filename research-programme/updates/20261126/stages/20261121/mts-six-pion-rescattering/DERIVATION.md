> Public reading copy: local links are mapped to released material or marked unavailable. Machine-specific passages, where present, have been omitted. See the inventory for the original digest.

# Four pions back into two: crossed source unitarity

Natural units; four initially labeled intermediate pions, one identical-particle division by \(4!\), equal masses \(m=0.1395704\) GeV and \(F=0.0924\) GeV. Keep the same square-root pion coordinates, metric and production conventions as the previous stage (not bundled here). This uses ordinary two-flavor chiral matter within the common-metric matching, not an MTS-specific modification to pion scattering.

## Which terms actually enter spin two?

Use all momenta incoming: four physical on-shell \(p_i\), followed by \(-k_+\) and \(-k_-\) with \(k_\pm=(W/2,\pm p\,t)\), \(p^2=W^2/4-m^2\), \(|t|=1\). For each perfect matching of the six real Cartesian isospin labels into three pairs \(A,B,C\) attach the product of their Kronecker deltas. Define \(p_A\) to be the pair sum and \(v_A=p_A^2-m^2\). In the square-root coordinates the sextic Lagrangian is \(\pi^2(\partial\pi^2)^2/(8F^4)-m^2(\pi^2)^3/(16F^4)\). Its contact gives \(\sum v_A/F^4\). Joining two quartic vertices gives the following coefficient for each matching:
\[
 F^4 {\cal M}_{A|B|C}=v_A+v_B+v_C-
 \sum_{\text{choice of remaining pair }C}v_Av_B\sum_{c\in C}
 \frac{1}{(p_A+p_c)^2-m^2}.
\]
There are 15 matchings and ten unlabeled three-against-three pole partitions. This is the leading part of [Bijnens & Husek, Eqs. 28–34](https://arxiv.org/abs/2107.06291); in their **own** mass, decay and three-to-three configuration we recover both Table I numbers \(+15.99\) and \(-319.00\), separately. Returning to the retained constants, crossing, pion permutations, reversing all momenta, and all-neutral equivalence to the cosine mass potential are checked before projection. The all-neutral amplitude in angle coordinates is \(-[m^2+m^4\sum_{\text{ten triples}}1/(p_{abc}^2-m^2)]/F^4\); dropping the contact would not reproduce it.

Trace over the two external isospins and divide by three; let the resulting singlet-average kernel on the intermediate labels be \(\sum_jD_j K_j(t)\), with the same three four-pion singlet tensors and Gram matrix as previously. Tracing a term pairs \(k_+\) directly to \(k_-\) with weight one, or joins their two internal partners with weight \(1/3\). For the \(D\) wave keep \(S_j=\langle(tt-I/3)K_j(t)\rangle_t\). The sextic contact is at most linear in \(t\) and integrates to zero. So do the four exchange partitions having three intermediate pions on one side: their denominators are constant, and at most one numerator factor is linear. **Only the six \((ij,-k_+)|(kl,-k_-)\) exchange poles survive the spin projection.** They are not physical singularities in this channel: \(q=p_i+p_j-k_+\) cannot be future or past timelike or null since either \(k_-=p_k+p_l+q\) or \(k_+=p_i+p_j-q\) would then have mass at least \(2m\). Hence \(q^2-m^2\le -m^2\).

For each such pole write the denominator as \(d_0+d\cdot t\) and numerator factors as \(a_0+a\cdot t,b_0+b\cdot t\). Subtracting terms at most linear in \(t\) leaves the **exact** projected numerator \([(a-a_0d/d_0)\cdot t][(b-b_0d/d_0)\cdot t]\) over the same denominator. No near-threshold subtraction of two large numerical contact amplitudes is necessary. Align the angular axis with \(d\), average the transverse azimuth exactly (rank four at most), and use \(\int_0^1 z^{2n}/(1-r^2z^2)\,dz\), \(n=0,1,2\), \(r=|d/d_0|<1\). The first moment is \(\operatorname{atanh}(r)/r\); higher ones follow by division or a convergent series near zero. Independently integrating the entire six-leg amplitude over directions, with contacts and all poles present, checks the analytic projection.

## Production factors and reciprocity

Use \(S=1+i{\cal T}\) in invariant amplitude conventions and \(2\,\mathrm{Im}\,F_2=\sum_X\int d\Phi_X\,{\cal M}^*_{2\leftarrow X}F_X/S_X\) on the complete right cut. The terms below are the tree four-pion contributions to the discontinuity divided by \(2i\); this component is real at this order. Full coupled-channel summands need not separately be real at higher orders. Let \(C_j\) be the previous photon angular moment summed against \(D_j\), \(T_j\) the spatial trace-free stress coefficients, and \(G_{jk}=6\delta_{jk}+3\). For the external singlet-average two-pion wave, the \(P_2\) moments are \(2H/3\) for photons and \(4p^2 A/(5\sqrt6)\) for stress. The angular kernel is \(P_2(t\cdot n)=3(tt-I/3):(nn-I/3)/2\). Consequently
\[
 u_H=\mathrm{Im}_4 H=\frac{3}{64}\int d\Phi_4\, S_j:C_j,\qquad
 u_A=\mathrm{Im}_4 A=\frac{3}{192p^2}\int d\Phi_4\,G_{jk}S_j:T_k.
\]
Repeated partition indices are summed. For the normalized isospin-zero scattering state the strong source is \(\sqrt3\sum D_j K_j\), rather than the trace average. With \({\cal M}^0=32\pi\sum_J(2J+1)t_JP_J\) and \(S_J=1+2i\beta t_J\), the leading four-pion transition probability is
\[
 P_4=(1-|S_2^0|^2)_{4\pi,\rm leading}
 =\frac{3\beta}{256\pi}\int d\Phi_4\,G_{jk}S_j:S_k .
\]
The same incoming flux gives the pure isoscalar, \(J=2\) identical-pion cross section \(10\pi P_4/p^2\); this is not the total cross section of a charged pion beam. The two-pion elastic control explicitly recovers \(\mathrm{Im}F=\beta t_2 F\) for real trial sources. Each ratio \(|u_F/F_2|\) is bounded by \(\sqrt{P_4}\,r_F/2\) for these matched leading kernels and source norms. In a separate event calculation we send the two-pion Born photon and unit stress sources **back into four**, using angular quadrature on the full crossed tensor; the imaginary pieces of the two- and four-body mixed products cancel to \(8.3\times10^{-12}\) relative. This tests the sign and multiplicities without fitting.

Near the new threshold put \(\epsilon=W-4m,\ R^2=2m\epsilon\) and use the three earlier Jacobi vectors \(u_j\). In the quadratic part of \(K_j(t)\), the coefficient of \(tt\) is \(F^{-4}[(5/4)\sum_b u_bu_b-(11/8)u_ju_j]_{\rm TF}\). To see the coefficient, at threshold \(d_0=-4m^2\), \(d=2\sqrt3m(p_i+p_j)\); the pair constants are \(3m^2\) for internal-internal and \(-3m^2\) for mixed. Apply the reduced-numerator identity above to the nine products at each of the six poles. The [Jacobi matrices and rational contractions](evidence-001.zip) (archive member: `checks.json`) are retained. With \(\Phi_{4,\rm NR}\) as in the prior threshold derivation (not bundled here), the leading terms are
\[
 (u_H,u_A)=\frac{\Phi_{4,\rm NR}R^4}{m^2 F^6}
  \left(-\frac{161}{126720},-\frac{149}{50688}\right),\qquad
 P_4=\frac{\Phi_{4,\rm NR}R^4}{F^8}\frac{\sqrt{3/4}}{\pi}\frac{763}{337920}.
\]
The \(11/2\) power is phase space \(7/2\) plus two powers from the source and scattering spin-two factors. The analytic coefficients are nonzero. Two near-threshold extrapolation points recover all three independently within 14 ppm. Away from threshold the calculation uses the full relativistic kernel and phase space.

For real leading \(H=H_{\rm Born}, A=1\), the four-pion part of the **first variation** of their relative phase is \(u_H/H_{\rm Born}-u_A\). It is not appropriate to call the same quotient with complex reconstructed amplitudes a measured phase: a dressed calculation needs a consistent elastic phase and inelastic kernel. We report separate magnitude-normalized source terms for comparison. Similarly one cannot deduce the real part from an imaginary part at the same energy. The finite-window dispersion test is [separate](DISPERSION.md).

