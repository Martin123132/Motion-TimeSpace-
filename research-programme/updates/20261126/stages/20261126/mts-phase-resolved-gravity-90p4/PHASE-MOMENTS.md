# Which phase harmonics can actually drive the mean heavy stress?
For the retained coherent probe on a common conformal clock, write e=(cos gamma,sin gamma), b_gamma=e·b, v_gamma=e·v. The observed quadratures of b and v are not assumed equal in magnitude. For a scalar metric M let M0=<M>, Mc=2<M cos(2 gamma)>, Ms=2<M sin(2 gamma)>. Angle brackets are uniform on [0,pi), pairing unsigned stress under a sign reversal. The tensor
    T(M) = 2 < e e^T M > = M0 I + [[Mc,Ms],[Ms,-Mc]]/2
is an identity, including for the equally spaced rule used here. No assumption about the size of higher metric harmonics is required.

Write f=2<e F>, w=2<e W> for the first odd harmonics of the driven field and its canonical momentum. Projecting the *equations* gives
    f' = w + T(Psi+3Phi) v + q_f,
    w' = -2 H w - (K+omega²) f - omega² T(Psi-3Phi) b + q_w.
Here q_f and q_w are the corresponding first odd source harmonics. At the same clock the exact readouts are
    <P> = (v·w - omega² b·f + 3 v^T T(Phi) v)/2 + <Qp>,
    <E> = (v·w + omega² b·f + 3 v^T T(Phi) v)/2 + <Qe>,
    <J> = K v·f/2 + <Qj>.
Thus a fourth harmonic may corrupt a two-angle *measurement* of mean stress, but it need not be propagated as an independent driver of the continuum mean-pressure equation. It can still matter indirectly by acting back on the lower metric harmonics in the gravitational evolution. This is a reduction of the probe/readout, not a closed replacement for that evolution. It also depends on the common metric-independent H and omega in this retained probe. A sector in which those quantities acquire their own phase variation requires further moments.

Implement the reduced evolution directly, evolving the homogeneous incoming term, odd microscopic forcing, mean-metric forcing and second-harmonic metric forcing separately. This tests both the total and its signed cancellation without integrating 16 tracer states. Score against both the independent sixteen-state solver and the physical temporal reference. Neither a good reconstruction of the first nor an algebraic identity is evidence of agreement with the second.
