# Independent angular/phase diagnostic (frozen before wide-run analysis)

Reuse the saved64-node baseline/MTS metric histories as imposed sources. Solve the collisionless neutrino hierarchy by its exact angular characteristics, not by increasing the full coupled matrix. This is a conditional response to a frozen metric, NOT a replacement coupled prediction. Do not change any forward packets, action, tolerance or saved state.

The retained hierarchy has only metric source multipoles S0=-4kz/3 and S2=8ksigma/15. With F(mu)=sum_l(-i)^l(2l+1)F_l P_l(mu), it obeys

    partial_tau F + ikv mu F = -4kz/3 - (8k sigma/3)P2(mu).

Define s(q,tau)=k integral v(q,tau)dtau and Delta s=s(tau)-s(t). Exact low multipoles for the saved monopole-only thermal seed are

    F_l(q,tau)=4Theta j_l(s)+integral[-4kz j_l(Delta s)/3 - 8k sigma K_l(Delta s)/3]dt,
    K0=-j2,
    K1=2j1/5-3j3/5,
    K2=2j2/7-18j4/35-j0/5.

The K factors follow by multiplying P_l by P2 and projecting the plane wave; verify their signs and coefficients against independent angular quadrature. Atzero delayK2=-1/5, reproducing S2=8ksigma/15. Test the free initial condition and these kernel projections independently.

Read the actual fine trajectory's z=-delta_c'/k and sigma from the live source-consistent operator. Sample at every saved256-step boundary. Compare source interpolation using128/256knots, and time quadrature6/10points per segment. Momentum rules64/128/256 all represent the same FD derivative on fixedq[0,60] with unchanged amplitude/mass;64must match the saved rule. These extra rules are passive diagnostics, NOT newly integrated parent backgrounds.

Atninecommon scale-factor probes, compare characteristics at64momenta with the retained lmax16 low moments to diagnose angular closure. Separately compare64/128/256momentum readouts for the SAME64-node metric, avoiding confusion between momentum quadrature and backreaction. Use absolute differences and each field's peak amplitude across the paired probes; gate2e-5unchanged. A nonzero conditional discrepancy identifies a numerical approximation to repair; it is not a fitted observational preference or a self-consistent corrected solution.
