# Canonical heavy variables and a phase partner for the driven field

Use the canonical second-order variables F and W in the retained solver, not a time derivative mislabeled W. On either supplied second-order metric history, with omega=ma, H=a'/a and K=k_out², the real-orientation equations in conformal time are

    F' = W + A,                       A = v (Psi + 3 Phi) + Qf,
    W' = -2 H W -(omega²+K) F + B,   B = -omega² b (Psi - 3 Phi) + Qw.

Here b'=v, v'=-2Hv-omega²b. The pair Qf,Qw is linear in the common heavy phase at fixed first-order metric. The scalar stress contractions Qe,Qt,Qj,Qs are quadratic in it. For each virtual orientation use its *own* drives and contractions, not a rotated final current. The same physical second-order potentials are supplied in both orientations. This is a test of a conditional matter response, not a derivation that the metric is phase independent.

At the common cutoff write the heavy and driven fields as real parts of slowly varying amplitudes times exp(i theta), theta'=omega. Eliminating W gives a forced oscillator with RHS B+A'+2HA. Keeping the first resonant transport terms gives Famp'=(-d+i K/(2omega))Famp+Aamp/2+Bamp/(2i omega), d=3H/2. A quarter-turn converts an amplitude to i times itself. Therefore, writing nu=omega+K/(2omega),

    Fq = (W + d F + A/2 + Bq/(2omega))/nu,
    Wq = -nu F - d Fq - Aq/2 + B/(2omega).

Subscript q here means the orthogonal *phase*, not an adjustable source. This map squares to minus the identity when applied jointly with the earlier transported first-order phase and the drives. It is an adiabatic preparation prescription at the cutoff, not a proof that the exact incoming second-order state has this orthogonal partner. Evolve the real and quarter fields independently from there; for the diagonal orientation linearity gives their sum divided by sqrt(2).

The complete microscopic conformally scaled heavy density, isotropic pressure, longitudinal current and shear on a given metric are

    E = v W + omega² b F + 3 v² Phi + Qe
    P = v W - omega² b F + 3 v² Phi + (Qe-Qt)/3
    J = K v F + Qj,                   shear = Qs.

This is the stress *before* the legacy effective retarded compensator. It is not legitimate to add both to gravity as new independent sources. Define Ec, Pc, Jc by omitting the explicit Qe,Qp,Qj terms. Direct differentiation and the two wave equations give

    Ec' = -H(Ec+3Pc)-Jc + 3 v² Phi' + v Qw + omega² b Qf
    Jc' = -2 H Jc + K(Pc + v² Psi + v Qf).

Add Qe' and Qj' to return to total derivatives. In particular the pressure and work terms include correlations of the background velocity with the driven field; replacing these by products of individual means is not conservation. Phi' is the derivative of the actual route's Phi, not automatically the momentum shadow on the density route. For an integrated check add the measured *change* in the explicit quadratic stress rather than differentiating a noisy small number. The ensemble mean is the half-sum of real and quarter stresses; the mean of the single real solution across time is a separately computed check. Neither equality nor agreement to tolerance is assumed.
