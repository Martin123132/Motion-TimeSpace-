# Exact-clock localized Legendre current for the moving-source action

Private continuation of `DERIVATION-20260921-independent-Ward-source-and-mass-current.md`. Numerical results will be recorded in a separate immutable results report. No action, state, coefficient, or empirical fit is changed here.

## 1. General derivation, including nonquadratic velocities

Let q collect every retained field and source coefficient, v=qdot, and let L(q,v;t) be the matter action with the metric treated as a specified time-dependent background when taking partial derivatives. Define

    p=L_v, M=L_vv, B=L_q-p_q v-p_t,
    E=L_q-d_t p=B-M a.

Assume the velocity Hessian M is invertible on this chart. Localize the SAME action at a fixed physical radius R, including moving interfaces: L_R. Set

    p_R=(L_R)_v, M_R=(L_R)_vv,
    H_R=v^T p_R-L_R,
    B_R=(L_R)_q-(p_R)_q v-(p_R)_t.

Then H_R,v=M_R v and the chain rule gives

    d_t H_R = -v^T B_R + v^T M_R a - (L_R)_t.

Consequently the following current and balance are derived, not fitted:

    a_0=M^-1 B,
    J_R=v^T(B_R-M_R a_0),
    d_t H_R+J_R=Q_R-v^T M_R M^-1 E,  Q_R=-(L_R)_t.

Equivalently, with D_0=v.d_q+d_t at fixed velocity,

    J_R=Q_R-D_0 H_R-v^T M_R a_0.

This last form permits evaluation without differentiating every localized force component. At the whole-domain cut, M_R=M and B_R=B, hence J_R=0 identically. At the empty cut it is also zero. For the fixed-spatial quadratic Lagrangian it reduces to the formula derived in the previous checkpoint. No assumption of quadratic dust energy is made.

This is a semidiscrete energy current selected by the actual localized action and its Legendre map. M^-1 can couple distant degrees of freedom. A covariant parent mixed stress does not follow merely by naming this current: its shift variation and locality/continuum correspondence are the next compatibility calculation. The background derivative here uses the archived metric tangent; it is not a new independently evolved geometry or a claim that the fixed-background Hessian equals the reduced gravity-matter Hessian.

## 2. Actual wave/source Hessian and proper clock

At fixed material label, use the existing map r=chi(x,b,z), J=chi_x, d=chi_b, V=bdot, g_ref=u_x, eta=-d*g_ref/J, T=u_t+V*eta. Write k=J*r^2/(N*sqrt(F)) and h=r^2*N*sqrt(F)/J. The wave Lagrangian is (k*T^2-h*g_ref^2)/2. Its velocity Hessian is the positive rank-one density k Z Z^T with Z=(field shape functions,eta), followed by the unchanged material-cardinal projection.

For dust, s=sqrt(N^2-V^2/F), L_d=-m*s. Exactly,

    p_d=m*V/(F*s), H_d=m*N^2/s,
    (M_d)_bb=m*N^2/(F*s^3),
    (H_d)_V=V*(M_d)_bb.

The field-source cross terms k*shape*eta and the source inertia k*eta^2 are retained. Positivity follows from positive quadrature, k>0 and the timelike clock, with invertibility checked on all 16,425 retained components. No mode deletion or mass-lumping is allowed.

## 3. Explicit convective and metric terms

Here nu_t=N_t/N and F_t are at fixed physical radius; radial gradients and map motion are separate. At fixed v,

    D_0 eta=-d*(u_t)_x/J-eta*J_b*V/J,
    D_0 T=V*D_0 eta,
    D_0 k=k_b*V+k*(-nu_t-F_t/(2F)),
    D_0 h=h_b*V+h*(nu_t+F_t/(2F)).

Thus wave D_0 H density is (D_0 k)*T^2/2+k*T*D_0 T+(D_0 h)*g_ref^2/2+h*g_ref*(u_t)_x. Its explicit exchange is Q_wave=-k*(-nu_t-F_t/(2F))*T^2/2+h*(nu_t+F_t/(2F))*g_ref^2/2.

For dust evaluated at r=b, use total nu_0=nu_t+V*nu_r, F_0=F_t+V*F_r and s_0=(N^2*nu_0+V^2*F_0/(2F^2))/s. Then D_0 p_d=p_d*(-F_0/F-s_0/s), D_0 H_d=H_d*(2*nu_0-s_0/s), and Q_d=m*(N^2*nu_t+V^2*F_t/(2F^2))/s.

For the unchanged Gram potential, y=D u, load=S^T(y^2/2), h_i=gamma_i*load_i. D and S stay fixed. Then D_0 h_i=(gamma_b*V+gamma*(nu_t+F_t/(2F)))*load_i+gamma*(S^T(y*D v))_i and Q_i=h_i*(nu_t+F_t/(2F)).

## 4. A fixed physical cut moves through reference coordinates

Differentiating the actual mask gives D_0 1_(r<R)=-W*delta(R-r), W=d*V. Therefore D_0 H_R includes minus the wave mesh-advection flux W*e at the cut and minus each moving Gram-node crossing W*h_i*delta(R-r_i). Material-label root Jacobians are retained when averaging nodal deltas. The five inherited cuts avoid the dust support; no dust crossing delta is silently discarded at a cut through that support. Extra empty/whole cuts test normalization and boundary silence.

## 5. Independent connection to the preceding Ward result

Let J_old be the previously computed wave+dust+Gram energy current and W_R the independently computed integral of I*r^2*div(T)_t. The established energy identity reads

    W_R=Q_R-d_t H_R-J_old.

The new derivation therefore predicts

    J_R-J_old = W_R - v^T M_R M^-1 E.

This comparison is diagnostic, not a definition used to calculate J_R. Calculate J_R from B, the positive Hessian, localized energy derivatives and explicit metric exchange FIRST; only then compare with the sealed Ward-source data. Both reference and both MTS variants receive the same calculation and omissions. Any residual acceleration/EL contribution is retained rather than assumed zero. The corresponding conditional mass current is kappa*sqrt(F)/N times J_R. No fitted boundary constant is introduced.

## 6. Predeclared numerical checks

- Reuse the endpoint-wide states, six phase probes, and radial archives; retain all degrees of freedom and the exact clock.
- Assemble the full fixed-metric Hessian with reference order12/material order48. Check symmetry, positive banded Cholesky/Schur pivots, and inverse residual. Compare analytic momentum/Hessian contractions with archived phase derivatives.
- Use both Richardson metric/velocity tangents and physically split local orders8/12, matching the previous five diagnostic cuts. Add empty and whole-domain cuts outside every support.
- Compare current-difference plus the computed EL projection to independently sealed Ward integrals, with energy-unit tolerance 2e-11+0.05*max(abs(W_R)). Record failures rather than change the gate.
- Require whole-domain current magnitude below 2e-11, paired local-quadrature change below 2e-11, and finite values. Record moving-cut and source-inertia omission effects without treating an insensitive control as success.
- Keep model implications separate from implementation identities. Source hashes, fresh run artifacts, and a compact independent checker accompany the result. Preserve every earlier execution unchanged.
