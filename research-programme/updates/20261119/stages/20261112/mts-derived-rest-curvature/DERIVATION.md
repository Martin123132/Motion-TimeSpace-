# Rest curvature from the retained coupled equations

## Conventions and authority

Primes mean derivatives in the original native conformal clock (Mpc, c=1). Use the actual interpolated scale factor rate r=a'/a, which need not equal the independently reconstructed conformal H at machine precision. Keep H, H', r and r' distinct. The original field splines and neutrino quadrature/approximations are retained, not replaced by ideal continuum identities.

Authority: ../mts-integrated-defect-20261112/native/fortran/equations.f90 (derivs, Nu_Integrate_L012), massive_neutrinos.f90 (actual rho_P), MTSTwoField.f90 (FieldJet, perturbation evolution), and the sealed 96-column preparation readouts. The only native modification here is the private read-only mts_curvature_hook.inc export. Original evolution sources are byte-identical; all original 910 readout rows agree byte-for-byte for each case.

Let D=sum D_j, Q=sum Q_j, R=sum R_j. In the retained flat branch,

    H²=R/3,  z=(D/(2k)+eta_k)/H,  eta_k'=Q/2.
    H'=R'/(6H),  H''=R''/(6H)-(H')²/H.

Exclude the heavy scalar density for MTS, or CDM density for baseline; write the remaining density as D_o. The rest forcing is

    zeta=(D_o/(2k)+eta_k)/H,
    zeta'=(D_o'/(2k)+Q/2)/H-(H'/H)zeta,
    zeta''=(D_o''/(2k)+Q'/2)/H
            -2(H'/H)zeta'-(H''/H)zeta.

This is an algebraic derivative identity of the actual retained equations, not a fit or a sampled finite difference. Excluding heavy density does NOT exclude the heavy contribution to Q or H. That distinction matters numerically.

## Matter and radiation

For a component with R_j proportional to a^(-p), D_j=R_j delta_j:

    D_j''=R_j[delta_j''-2p r delta_j'+(p²r²-p r')delta_j],
    Q_j'=R_j[q_j'-p r q_j],
    R_j''=(p²r²-p r')R_j.

p=1 for CDM/baryons, p=2 for photons/massless neutrinos. Native CDM current is zero. Directly differentiating the retained monopole equations gives

    delta_c''=-k z',
    delta_b''=-k(z'+v_b'),
    delta_gamma,nu0''=-k(4z'/3+q_gamma,nu0').

Use the actual native v_b',q_gamma',q_nu0', including the retained photon approximation where applicable. No collision term is discarded, and no new time or frequency grid is introduced.

## Massive neutrinos

For each quadrature momentum, v_q=[1+(am/q)²]^(-1/2), v_q'=-r v_q(1-v_q²). For a resolved monopole F_0:

    F_0''=-k[4z'/3+v_q' F_1+v_q F_1'].

Its density weight W=A kernel/v_q, A=grhormass/a², obeys

    g=W'/W=-r(1+v_q²),
    g'=-r'(1+v_q²)+2r²v_q²(1-v_q²),
    (W F_0)''=W[F_0''+2g F_0'+(g²+g')F_0].

The current uses A kernel F_1, hence its derivative is A kernel(F_1'-2r F_1). Preserve the native perturbatively relativistic high-q tail: F_0=delta_nu0+c delta_corr, c=(m/q)²/2, with

    delta_corr''=k a²(2r q_nu0+q_nu0')-k q_corr'.

The tail is not set to zero or replaced by an independent massless species. Unsupported massive-fluid or omitted-multipole regimes are rejected by the capture gate.

For the background A rho(am), with N=ln a:

    (A rho)''=A[r²(rho_NN-4rho_N+4rho)+r'(rho_N-2rho)].

Use derivatives of the exact small-am rho_P formula in the retained native branch. With c2=5/(7 pi²), A4=.01099926669, B4=.003492416767, C5=.005866275571, for am>=.01:

    rho=1+c2 am²+am⁴(A4 ln(am)-B4-C5 am),
    rho_NN=4c2 am²+am⁴[A4(16ln(am)+8)-16B4-25C5 am].

Below .01 only the quadratic term is retained, exactly as in native rho_P. No independent legacy drho approximation is substituted.

## Scalar terms, including the slow field

For each scalar, M=(am)², b=background field, v=background velocity, u=perturbation, w=u'. The native background independently interpolates b and v, so calculate b'=r b_N, b''=r' b_N+r²b_NN, and similarly for v. Do not impose b'=v to erase interpolation defects.

    M'=2rM,  M''=(2r'+4r²)M,
    w'=-(M+k²)u-2Hw-kvz,
    w''=-M'u-(M+k²)w-2H'w-2Hw'-k(v'z+vz'),
    D=v w+M b u,
    D''=v''w+2v'w'+v w''+M''bu
         +2M'(b'u+bw)+M(b''u+2b'w+bw'),
    Q'=k(v'u+vw),
    R''=v'²+vv''+M''b²/2+2M'bb'+M(b'²+bb'').

The independently retained source-jet implementation agrees after removing its a/R0 normalization and normalization derivatives. Eleven independent 80-digit differentiation controls check the quotient, scalar product and neutrino weight/background identities.

## Frozen prediction and response test

Use zeta_i(s)=zeta_i(0)+s zeta_i'(0)+s² zeta_i''(0)/2 at each of the original 902 preparation nodes. The new coefficient is read from the coupled equations before target scoring. Evolve the same coherent primitive subsystem, actual background and live own-density metric coupling as the previous stage, with the original solver tolerances and reporting epochs.

For the previously saved signed adjoint gain g_ij, the linear subsystem predicts the quadratic-minus-linear final source change exactly in arithmetic:

    Delta Ybar_j=sum_i weight_i g_ij zeta_i''(0).

The independently evolved change agrees within its explicit numerical working allowance for both cases. The absolute-node-gain sum bounds the effect of THIS frozen quadratic forcing; it is not a bound on uncomputed time variation of zeta''.

## What the threshold actually says

The previous pressure ceiling .0035630317480616954 is a sufficient, final-epoch, uniform-curvature condition. MTS has a computed initial-node magnitude .00668191679964326, 1.87535 times that ceiling. Thus this sufficient condition cannot be satisfied over all the original trajectories including their initial points. A sampled maximum is not an upper bound between samples, and no such upper bound is claimed. The failure of this sufficient condition does not imply failure of the signed physical response; the direct quadratic prediction improves and passes.

At the largest-curvature node, the heavy background term -zeta R_heavy''/(6H²) is -.00555814458218, and the heavy current term Q_heavy'/(2H) is -.00112197108620. The maximum of the full rest curvature is negative at that node. Other terms are retained in the saved decomposition, not dropped as small.

## Constructive next system: promote eta_k

The decomposition gives a specific next representation, not another interpolant search. Let D_o and Q_o exclude the heavy scalar. Keep eta_k as a live state:

    u'=w,
    w'=-(M+k²+vMb/(2H))u-(2H+v²/(2H))w
         -(kv/H)[D_o/(2k)+eta_k],
    eta_k'=(kvu+Q_o)/2.

This follows directly from the original constraint and current equation. It propagates the heavy current feedback instead of burying it in frozen rest coefficients, and retains the full saved H(t) denominator rather than Taylor-expanding its rapidly varying second derivative. It is not a new coupling or new field theory. Baseline CDM counterpart:

    delta_c'=-(R_c delta_c+D_o)/(2H)-k eta_k/H,
    eta_k'=Q_o/2.

Initial D_o,D_o',D_o'',Q_o,Q_o' are already available in this stage's seven-component readout. Native initial RHS checks for this enlarged system are included in validation; its time evolution is the next manual stage. External-sector continuation still needs an explicit frozen approximation/error check rather than being silently declared exact.
