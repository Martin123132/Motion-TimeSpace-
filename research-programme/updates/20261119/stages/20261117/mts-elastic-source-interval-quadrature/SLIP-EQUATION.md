# A scalar balance for the source, without subtracting two collision rates

On the retained flat branch outside tight coupling, let s=v_b-3q_gamma/4, w=4 B_gamma/(3 B_b), chi=conformal opacity and c_b^2 the native baryon sound-speed coefficient. The saved non-magnetic Euler rows in `../mts-coupled-metric-consistency-20261117/native/fortran/equations.f90` give

    v_b'=-H v_b+k c_b^2 delta_b-w chi s,
    3 q_gamma'/4=chi s+k delta_gamma/4-k Pi_gamma/2,
    s'=F-L s,  F=-H v_b+k c_b^2 delta_b-k delta_gamma/4+k Pi_gamma/2,  L=chi(1+w).

Pi_gamma here is the dimensionless native photon quadrupole, not the background-weighted species stress. These are conformal-time rates at the same branch clock. No fitted transfer coefficient. The slip equation is not autonomous: F still depends on the coupled history.

For g=(1+alpha)^-1, fixed ionization gives chi1=chi0 g², c1²=c0² g, w1=w0 g. Write d=s1-s0. Then

    d'=-L1 d + Delta F - Delta L s0,
    Delta F=-H1 Delta v_b-Delta H v_b0+k c0²(g Delta delta_b+(g-1)delta_b0)-k Delta delta_gamma/4+k Delta Pi_gamma/2,
    Delta L=chi0[(g²-1)+w0(g³-1)].

Use g-1=-alpha/(1+alpha), g²-1=(g-1)(1+g), g³-1=(g-1)(1+g+g²); use small saved state changes directly, not differences of two large packet rates. The native Hubble pair still enters: if Delta H itself is unresolved, this rearrangement does not magically recover it. Native and represented original scales may also differ at roundoff; keep the actual 32/64 flags. The scalar equation gives a prospective integrating-factor route: d(r)=exp[-integral_l^r L1]d(l)+integral_l^r exp[-integral_t^r L1](Delta F-Delta L s0)dt. It cannot assume that endpoint force values resolve the forcing between knots. Test against direct interior evolution first.

Independent integral identity: for W=4/[3(1+w)], the elastic fractional radiation source R=4chi s²/3=W s(F-s'). Consequently integral R=integral(W s F+W' s²/2)-[W s²/2], with W'=4 w (a'/a)/[3(1+w)^2] when w is proportional to1/a. Apply separately on each branch, with its own rate, or form a cancellation-safe finite difference. Retain the boundary term and work on the same mode. This may improve or worsen conditioning; it is not a certified replacement quadrature or a full gas heat law. The present check tests the Euler identities against the saved packet and native terminal RHS; it does not claim this alternate time integral was verified.
