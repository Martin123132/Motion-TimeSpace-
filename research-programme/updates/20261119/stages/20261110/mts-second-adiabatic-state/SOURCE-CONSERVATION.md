# Source conservation with an explicit oscillator remainder

The source map is not accepted merely because its trajectory looks smooth.
This derives its conservation remainder from the original scalar field equation.

For q0 and qk let R0 and Rk denote their oscillator residual coefficients,
qj''+Omega_j^2 qj=Rj qj. Use the same projected amplitudes R,I, frequencies
W0,Wk, slopes L0,Lk and denominator D as DERIVATION.md. Let

    Ebg = 2 L0 R0/D,
    w = (W0^2+L0^2-mu^2)/D.

The background continuity remainder is exactly

    rho'/rho +3H(1+w)=Ebg.

For the projected linear sources the exact off-shell identities are

    delta' + k u +3H(Pi-w delta)
      = 2[(L0 R-W0 I)Rk+(Lk R+Wk I)R0]/D -delta Ebg,

    S' -3H w S +mu Pi = -2mu R0 R/D -S Ebg.

These are the scalar stress-divergence identity specialized to the retained
normalizations and carrier projection. They do not assume a dust background
after retaining a nonzero second-order pressure. They also do not identify
u=q_momentum/rho with theta/k when w is nonzero.

The script verifies these rational identities for arbitrary frequency
functions, their first/second derivatives, H and H'. They therefore separate
an exact source identity from the approximate choice of W2.

For the constant-H certificate domain, let Rmax bound both |R0|,|Rk|,
Lmax bound |L0|,|Lk|, Wmax bound |W0|,|Wk| and Dmin=1490^2.
With N=max(|R|,|I|,|delta|,|S|), the two perturbation remainders obey

    |energy-continuity remainder|/N
        <= 2 Rmax(3Lmax+2Wmax)/Dmin,
    |phase/current remainder|/N
        <= 2 Rmax(1510+Lmax)/Dmin.

Divide by Hmin=.0012 for e-fold derivative units. These are explicit
instantaneous source-residual bounds, not terminal perturbation-error bounds.
The rigorous oscillator propagation bound and these source identities are
different statements; near-zero individual observables still need their
conditioning propagated.

No arbitrary compensating source was added to make continuity pass.
The remainder comes from the declared oscillator truncation itself.
