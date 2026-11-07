# Derivative primitive from the retained GR constraint

All sources below are evaluated on the fixed GR reference. The candidate
operator and adjoint remain those independently evolved previously.
A prime is conformal time; a subscript N is d/d ln a.

Let chi=1 (Poisson-spatial) or0 (dust-force), L=1+3chi Wq/(2k^2),
g=3H W/(2k^2), M=3H Qg/(2k^3), S=Pi_g/k^2, P=-Dg/(2k^2).
The retained constraint gives Phi_g=P-M exactly. Hence

    J=Phi_g-chi P = (1-chi)Phi_g-chi M
    T=3H J_N/(k L)
    Y=-3(H+chi g)/(k L)
    r=b_alpha(M+S)+b_z[T+Y(M+S)].

J=-M for Poisson-spatial is an exact physical primitive of the troublesome
time derivative, not an empirically chosen oscillation amplitude.
For dust-force, J=Phi_g. Both are tested as controls.

Define F=b_alpha+Y b_z and d=3H b_z/(k L).
The already-derived error equation becomes

    e_N=An e+F(M+S)+d J_N.

The source transformation w=e-d J is exact:

    w_N=An w+F(M+S)+(An d-d_N)J
    w(initial)=-d(initial)J(initial).

That nonzero transformed initial condition is essential; setting it to zero
would incorrectly discard a real boundary contribution.

For lambda_N=-An^T lambda, lambda(final)=ell, let C=lambda^T d.
Then C_N=lambda^T(d_N-An d), including all coupling/phase effects, and

    ell e(final)=[C J]_initial^final
                  +integral [lambda^T F(M+S)-C_N J] dN.

Consequently the absolute value is bounded by

    |[C J]_initial^final|
       +integral |lambda^T F(M+S)-C_N J| dN.

A separate metric-time budget is |[C J]|+integral |C_N J|.
The two endpoint values may be combined exactly; a more conservative
sum of their separate absolute values is also recorded.
These are bounds on known reference sources propagated through the fully
coupled candidate; no unknown DeltaD or target trajectory is supplied.

## Full derivative, including the fast scalar

In fixed normalized coordinates U,

    d=3 R_z/(k L U).

The H in b_z cancels exactly. For constant native material source rows,
d_N=-d L_N/L. For each scalar's unrotated velocity row,
R_z=-k v and (R_z)_N=-k v_N.

For the heavy carrier B=a(sqrt(omega)d_h+i u_h/sqrt(omega))exp(i theta),
the complex injection is

    d_B=-3i a v exp(i theta)/(L sqrt(omega) U_B)
    (d_B)_N=-3i a exp(i theta)/(L sqrt(omega) U_B)
             [v_N+(1/2+i mu-L_N/L)v],

where omega=a m, mu=theta_N. No v division at its zeros, no dropped mu term.
L_N=3chi(Wq)_N/(2k^2); Wq_N retains the actual quadrature/background
representation and is independently checked rather than replaced by a
pressureless approximation.

The core-to-massive-tail injection is through quadrupoles. d has zero
entries in those five quadrupoles, so An d has zero tail. This is verified
before contracting only the saved adjoint core traces. The full hierarchy
still influenced those traces in their earlier backward evolution.

The method is not predicated on the derivative commutator being small.
A failure to improve the bound is a physical/mathematical result, not a
reason to fit d or change the gate. In particular rapid phase in the
adjoint remains in An d and may obstruct a naive slow-response estimate.

