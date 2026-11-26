> Public reading copy: local links are mapped to released material or marked unavailable. Machine-specific passages, where present, have been omitted. See the inventory for the original digest.

# From two real photon insertions to the four-pion stress cut

Natural units, mostly-minus metric. Use the same positive-energy, equal-mass, two-flavor pion effective theory, physical electric charge, and common metric as the four-pion stress calculation (not bundled here). These are low-energy matter inputs to the parent matching, not a derivation of QCD from MTS. No sign or coefficient is obtained by fitting a cross section.

## Gauge the action, not the answer

In square-root coordinates the quartic action is \([(\partial\pi^2)^2-m^2(\pi^2)^2]/(8F^2)\). The electromagnetic rotation leaves \(\pi^2\) invariant. In these coordinates the only one- and two-photon insertions at this order are on the quadratic charged-pion kinetic term. In another field parametrization one cannot simply omit the corresponding contact vertices. The strong quartic vertex for a partition \(h=(ab|cd)\) is \(iD_h V\), with \(D_h=\delta_{q_a+q_b,0}\delta_{q_c+q_d,0}\), using charges \(q_i=0,\pm1\). Sum over the three distinct partitions. For photon 1 on leg \(i\) and photon 2 on leg \(j\),
\[
 V_{ij}=\{[p_a+p_b-{\bf 1}_{i\in ab} k_1-{\bf 1}_{j\in ab}k_2]^2-m^2\}/F^2.
\]
The total outgoing momentum is \(Q=k_1+k_2\); \(d_{ir}=-2p_i\cdot k_r,\ d_{iQ}=Q^2-2p_i\cdot Q\). Write \(a_{ir}=2p_i-k_r\). For each partition, multiply the following by \(D_h e^2\):
\[
\sum_i {q_i^2 V_{ii}\over d_{iQ}}\left[
 {a_{i1}^{\mu}(a_{i2}-2k_1)^\nu\over d_{i1}}+
 {(a_{i1}-2k_2)^\mu a_{i2}^\nu\over d_{i2}}-2g^{\mu\nu}\right]
+\sum_{i\ne j} {q_iq_j V_{ij}a_{i1}^\mu a_{j2}^\nu\over d_{i1}d_{j2}} .
\]
At a pair-production subpole the bracket is minus the charged two-pion Born tensor with the second pion momentum \(Q-p_i\): the extra \(iV\) and \(i/d\) account for the minus sign. With the retained polarizations the pair gives \(M_{++}/(2e^2)=(1-\beta^2)/(1-\beta^2 z^2)\), not its negative. At four-pion threshold only the contact survives in a transverse polarization: \(M_{++}^{+-00}/(2e^2)=-3/(4F^2)\). Four neutral pions have no tree photon source.

Contracting photon 1 into the bracket gives \(-d_{iQ}a_{i2}^\nu/d_{i2}\). Including the different-leg terms leaves a multiple of \(\sum_i q_i V_{ij}\) for each charged \(j\); it vanishes since \(V_{ij}\) is constant within each of the two neutral pairs. Interchanging the two photons proves the second Ward identity. The covariant implementation tests both, Bose interchange, pion permutation, the opposite-sign pole factor, the full angular pair Born result and its projected D wave. Removing the contact is a deliberate failing control. See [checks](evidence-001.zip) (archive member: `checks.json`).

## Signed projection and normalization

For unit beam direction \(n\) in the four-body CM, \(b(n)=-(\delta_{ij}-n_i n_j)M^{ij}/(4e^2)\) is the parity-even equal-helicity source. The orthogonal isospin-singlet projector is essential for a norm, though the stress already selects that sector in a mixed product. Let \(G_{ab}=\sum_q D_a D_b=6\delta_{ab}+3\). At fixed internal momenta form
\[
 C_{a,ij}=\langle \sum_q D_a b(n)(n_i n_j-\delta_{ij}/3)\rangle_n .
\]
The spin-two projection of a function with this moment is \(15 C_{ij}n_i n_j/2\), by the fourth angular moment. With \(T_a\) the saved spatial trace-free stress for each partition and \(e=(3nn-I)/\sqrt6\) its unit polarization, the phase-space weights for the mixed product and two squared norms are
\[
 J_4=\int {d\Phi_4\over24}{3\over\sqrt6}\sum_a C_a:T_a,\quad
 N_\gamma=\int {d\Phi_4\over24}{15\over2}\sum_{ab}(G^{-1})_{ab}C_a:C_b,\quad
 N_T=\int {d\Phi_4\over120}\sum_{ab}G_{ab} T_a:T_b .
\]
The 24 divides the labeled momentum/flavor sum. Measured \(\pi^+\pi^-\pi^0\pi^0\) instead uses a specified charge assignment, both photon polarizations averaged, and only \(2!\) in the final state. Never insert that positive rate in place of \(J_4\). At fixed event and after integration \(|J_4|^2\le N_\gamma N_T\) with matched measures.

Match the normalization on **two** pions: \(\Phi_2=\beta/(8\pi)\), \(p=W\beta/2\);
\(J_2=\Phi_2(4p^2/\sqrt6)\operatorname{Re}(H A_\pi^*)\), with \(H=h_c+h_n/2\) as in the elastic derivation (not bundled here). This follows by projecting \(2p_ip_j\) on \(e\) and integrating the charged and half-weighted neutral angular amplitudes. Their two squared singlet norms are \(\Phi_2(10/3)|H|^2\) and \(\Phi_2(4/5)p^4|A_\pi|^2\). The universal real-cut conversion, recovered on that channel, is
\[
 {d I_4\over dW}={4\sqrt6\,\alpha\over W^5}J_4,\qquad I=-F_3(0)\ \text{(window contribution)} .
\]
\(J_4\) has units GeV², \(N_T\) GeV⁴, \(N_\gamma\) is dimensionless. The tree amplitudes here are real. This direct product is not a calculation of the change of \(H A_\pi^*\) in the two-pion channel.

## Independent threshold sign and power

Let \(R^2=2m\epsilon\), \(\epsilon=W-4m\). To order \(R^2\) the angular spin-two part of the photon source at fixed charges is \(B:nn\),
\[
 B={1\over16 m^2 F^2}\sum_h D_h
 [-3\sum_i q_i^2\,p_i p_i+\sum_{i\ne j}q_iq_j\,c_{ij}\,p_i p_j]_{\rm TF}.
\]
Here the \(p\)'s are spatial vectors; \(c_{ij}=3\) for legs in the same pair and \(-5\) otherwise. The coefficients follow by expanding the transverse denominators: \(d_{i1,2}\to-4m^2,\ d_{iQ}\to8m^2\) while the strong numerator is respectively \(3m^2\) or \(-5m^2\). The surviving direction-independent terms cannot interfere with spin-two stress. On the nine-dimensional momentum sphere use three orthogonal Jacobi vectors \(u_a\) as in the preceding stage. The average STF contraction of quadratic tensors with Jacobi matrices \(A,B'\) is \(10R^4\operatorname{tr}(AB')/99\). Combining charge, angular and identical-particle weights with \(T_a=2[u_a u_a-(3/8)\sum_b u_b u_b]_{\rm TF}/F^2\) gives
\[
 (J_4,N_\gamma,N_T)={\Phi_{4,\rm NR} R^4\over F^4}
 \left({53\over3168\sqrt6\,m^2},\ {7\over4752 m^4},\ {29\over704}\right)[1+O(\epsilon/m)] ,
\]
with the relative corrections separately for each component, and \(\Phi_{4,\rm NR}\propto\epsilon^{7/2}\) as in the stress stage. Thus all three start as \(\epsilon^{11/2}\), with a **positive mixed coefficient**. Extrapolation from 0.5 and 1 MeV excess gives relative errors of −2.52, −10.2 and −0.91 parts per million for these three leading coefficients. This is an independent low-energy check, not an extrapolation to 0.8 GeV: the latter uses full relativistic kinematics, propagators and phase space.

