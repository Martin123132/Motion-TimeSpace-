# Coupled phase-memory budget and regular source coordinates

This is a derivation within the retained positive quadratic real-scalar branch, not a new action or fitted fluid. It uses the physical source normalization and signed temporal extraction already saved. Symbols follow the preceding live-continuation stage: b,v background field/velocity, u,w perturbation/velocity, mu=a*m, H conformal Hubble rate, r=actual thermal d ln a/d tau, beta=a/R0, and k>0. Numerical evaluation remains at the retained k=1/Mpc.

## 1. The two coupled remainders

    YD=beta*(v*w+mu²*b*u), YQ=beta*k*v*u,
    YP=beta*(v*w-mu²*b*u),
    PA=cs²*(YD+3H*YQ/k), RP=YP-PA,
    cs²=(k/mu)²/(sqrt(1+(k/mu)²)+1)².

Retain E_f=r*b_N-v and E_b=r*v_N+2H*v+mu²*b as representation defects of the saved background tables. The exact same-background coherent equations give

    YD' = BD + RD,  BD=-3H*PA-k*YQ-k*z,
    YQ' = BQ + RQ,  BQ=-H*YQ+k*PA,
    RD=-3H*RP-k*z*(beta*v²-1)+ID,
    RQ=k*RP+IQ,
    ID=(r-H)*YD+beta*E_b*w+beta*mu²*E_f*u
       +2*beta*(r-H)*mu²*b*u,
    IQ=(r-H)*YQ+beta*k*E_b*u.

The full RD/RQ are evaluated, not fitted to endpoint residuals. The baseline is actual synchronous CDM: Yc=F_c*delta_c with constant F_c=a*R_c/R0, Yc'=-F_c*k*z, and no invented heavy pressure or occupation.

## 2. Remove the fast derivatives analytically, not by assuming zero means

Define background and perturbation virials

    J=beta*b*v,
    S=beta*(b*w+v*u),
    E=beta*(v²+mu²*b²)/2,
    F=beta*(E_f*v+E_b*b),
    G=beta*(E_f*w+E_b*u).

Direct field-equation differentiation yields

    beta*v²-1=(E-1)+J'/2+(2H-r)*J/2-F/2,
    RP=S'/2+T,
    T=((2H-r)*S+beta*k²*b*u+k*z*J-G)/2-PA.

Hence the density remainder consists of a derivative boundary part and a history part:

    RD=-(3H*S+k*z*J)'/2 + HD,
    HD=3H'*S/2-3H*T-k*z*(E-1)
       +k*z'*J/2-k*(2H-r)*z*J/2+k*z*F/2+ID,
    RQ=k*S'/2+HQ,  HQ=k*T+IQ.

No step discards phase, assumes random occupation, fits a pressure, or changes the homogeneous background. In particular HD includes the changing metric and normalization terms; cancellation of one endpoint alone is insufficient.

## 3. Original signed weights and their boundary jumps

On each original interval let C_j be the cumulative extraction weight; for the short continuation C_j=1. For any X,

    sum_j C_j integral_j X' = sum_i d_i X_i,
    d_0=-C_0, d_i=C_(i-1)-C_i, d_N=C_(N-1).

Thus integrated RD has boundary -sum_i d_i*(3H_i*S_i+k*z_i*J_i)/2 plus sum_j C_j integral_j HD. Integrated RQ has boundary k*sum_i d_i*S_i/2 plus sum_j C_j integral_j HQ. For the original extraction sum_i w_i=1, this is the exact endpoint-minus-projection identity, including internal weight jumps. The 429 negative weights are retained; no positive averaging interpretation is introduced.

The code compares this decomposition against direct integration of the original field-equation remainders AND the actual saved endpoint. Merely checking the algebra against itself would not establish the latter.

## 4. Metric derivative, with a numerical qualification

At native flat k=1 the retained equations give Hz=D_total/2+eta and eta'=Q_total/2. Also3H²=R_total. The implementation uses

    H'=R_total'/(6H),
    z'=(D_total'/2+eta_native')/H-z*H'/H.

R_total' and D_total' here differentiate fixed-degree interpolants of the saved physical source history. They are NOT a newly exposed exact native derivative routine. Degree5/7, retained-node stride1/2 and Gaussian order4/8 are frozen comparison variants. Independent derivatives of the saved z,H,eta representations check the constraint derivative and native eta equation. The maximum discrepancy over all variants is about2.21e-6, below the unchanged2e-5 gate. This is validated numerical differentiation on saved histories, not an exact new live RHS port. A future independent live-coordinate evolution must replace history access with present-state/background derivatives.

## 5. Conditional energy bounds

For beta>0 and mu>0 let Eu=beta*(w²+mu²*u²)/2. Two exact square identities imply

    |J|<=E/mu,
    |S|<=2*sqrt(E*Eu)/mu.

For example E²/mu²-J²=beta²*(v²-mu²*b²)²/(4mu²), and4E*Eu/mu²-S²=beta²*(v*w-mu²*b*u)²/mu². The implementation bounds T by the sum of its explicitly sourced absolute terms, then bounds HD/HQ and the weighted boundaries using |C_j| and |d_i|. These are valid conditional analytic inequalities. Their numerical quadrature evaluation is not a rigorous interval-arithmetic continuum certificate, nor a bound on every possible initial population. The evaluated bounds are too loose to authorize dropping the remainder at our existing tolerance.

## 6. A regular boundary-adapted source state

The same identities suggest an EXACT reversible coordinate choice:

    WD=YD+(3H*S+k*z*J)/2,
    WQ=YQ-k*S/2,
    WD'=BD+HD, WQ'=BQ+HQ.

These equations retain HD/HQ; setting them to zero is an additional approximation not established here. Also BD/BQ still refer to the physical Y sources, not blindly to W. The new coordinates retain the original two heavy perturbation degrees, and can remove a coordinate singularity without selecting a population or changing the action.

Split the metric constraint using independently sourced rest density:

    z=z_rest+(mu²*b*u+v*w)/(2kH),
    t=b*v/(4H),
    [WD-k*J*z_rest/2, WQ]^T = A [u,w]^T,
    A=beta * [[(1+t)*mu²*b+3H*v/2, (1+t)*v+3H*b/2],
              [k*v/2, -k*b/2]],
    det(A)=-beta²*k/2 * [(1+t)*(mu²*b²+v²)+3H*b*v].

This map never divides by v. For a nonzero positive heavy energy rho_h=(v²+mu²b²)/2, flat positive total density rho_h<=3H², H>0 and k>0, the bracket divided by2rho_h is bounded below by

    1 - 9H/(4mu).

Indeed |b*v|<=rho_h/mu bounds |t| by3H/(4mu), and |3H*b*v/(2rho_h)| by3H/(2mu). Thus mu>9H/4 is a sufficient, not necessary, all-phase regularity condition. This is a local algebraic theorem under those assumptions; finite sampled checks of them are not a global continuum background proof. At k=0 the current coordinate degenerates and this statement does not apply.

The saved heavy histories satisfy the sampled sufficient margin above0.99913, with energy-scaled row-normalized condition below1.00058. Both forward and inverse maps are tested against independently sourced rest density and the actual native state. The cold control requires no invented heavy transform. These W coordinates are not silently equated with the old late averaged selector1, its positive ensemble, or its fitted/extracted initial density/current; their state and source transfer must be explicit.

## 7. What the next physical test is

Implement WD/WQ as retained coordinates in the live parent interface, keeping the exact pressure/kinetic/representation tails and the rest species. Derive the necessary present-state/background derivatives, verify the exact inverse and feedback, then evolve independently against the saved coherent start. Only after that should an approximation discard tails, and only with an error bound in the actual source/observable norm. The old late background/selector matching remains a distinct physical transfer, not something this coordinate identity proves automatically.
