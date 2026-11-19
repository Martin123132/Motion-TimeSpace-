# Clock-weighted forcing primitive and derivative

Retained numerical source: f(N,theta)=sum_j B_j(theta) F_j(N), where B is the COMPLETE real representation of the saved 256-point complex forcing, including both Nyquist sine and cosine terms. F_j are the already accepted CubicSpline coefficients of normal-form and coordinate-map forcing applied to the original leading state. No source or fit is replaced. The source period is pi, as confirmed by the original phase grid and factors exp(2 i k theta).

Let w=1/Omega, W=integral w, mu_j=integral w B_j/W. Define K_j by
    partial_theta K_j=w(B_j-mu_j),    integral w K_j=0.
The periodic primitive exists because its right-hand side has zero angular integral. It is unique after the clock-weighted normalization. Then
    J=sum_j K_j F_j,    fbar=sum_j mu_j F_j.

Derivatives at FIXED theta:
    w_N=-Omega_N/Omega^2,
    mu_j,N=integral w_N(B_j-mu_j)/W,
    (K_j,N)_theta=w_N(B_j-mu_j)-w mu_j,N,
    integral(w K_j,N+w_N K_j)=0,
    J_N=sum_j K_j,N F_j + K_j F_j,N.
This last term carries the derivative of the complete retained forcing, not merely its frozen operator.

For the retained rho reconstruction log(rho/rhobar)=g and rhobar_N=-rhobar:
    rho_N|theta=rho[-1+g_N|rho,theta]/[1-g_logrho],
    H_N|theta=(E_N+coordinate coordinate_N+velocity velocity_N+rho_N)/(6H),
    Omega_N|theta=(omega/H)(1-H_N/H).
The code uses the already derived directional source laws and this implicit derivative. H is conformal expansion, omega=a m.

At each queried N, rho in rhobar exp([-.02,.02]) gives explicit bounds on H, |g| and |g_logrho|. An interval mapped strictly into itself with contraction less than one gives the unique reconstructed phase branch. Omega >= omega/H_max-1.5>0 uniformly in theta on that branch. These are fixed-N bounds, not an asserted enclosure of unsampled N.

The exact transformed response is
    eta_N=M eta+fbar+M J-J_N,    delta=eta+J,
    eta(N_b)=delta(N_b)-J(N_b,theta_b).
No residual averaging is assumed. Baseline has no phase and takes J=0,fbar=f, reproducing its original equation.

Auxiliary odd phase quadrature resolves the retained source without deleting a Nyquist mode; clock weighting generates additional harmonics, so its convergence is tested separately. Auxiliary Hermite interpolation uses the derived K_N and mu_N; its derivative is taken consistently from that same interpolant and tested off-grid. Original physical/source banks and tolerances are unchanged.

Scope of f_N: exact derivative of the accepted retained forcing interpolant. This is not a claim that an independent microscopic derivative R_N has already been computed at every N. Source interpolation uncertainty, omitted R delta and reconstructed-background mismatch remain separate inherited errors. The purpose is a faithful derived transformation of the saved response, followed by physical-source and gain control, not substitution of an easier physical model.
