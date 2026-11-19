# The physical right-edge state and its causal history

## 1. The actual initial value problem

The retained native preparation has a fixed ordered set of16 heavy-branch modes and4 cold-baseline modes. The target is k=5/Mpc. Capture the complete native vector, active hierarchy, regime signature, caches, background/thermodynamic owner and source callback at original index2892. The heavy right edge is tau_b=89.70491681253633, a_b=0.0002266254582732105. Keep the original center label a0=0.00022501566262210325 on the historical projected quantity.

Only the private capture selector changes: select original mode15 in the heavy batch or mode4 in the cold batch and ignore capture callbacks for the other modes. The modes, evolution equations, clock, original background tables and numerical boosts are unaltered. The complete4253-output comparison is a separate gate. No quintic candidate background or custom clock table is inserted.

The captured numerical vector has400 allocated slots and185 active equations in the heavy branch; the cold baseline has397/182. Inactive allocations are retained but are not new physical degrees of freedom. The native owner is recreated from the original parameters; an NPZ alone is not a portable live native process or a substitute for that owner.

## 2. Exact current-state coordinate change

For each retained scalar let b,v be its background, u,w its perturbation, mu=a*m, omega=sqrt(mu²+k²), H the physical conformal Hubble rate, and r=d(log a)/d tau from the actual native scale-factor interpolant. Define

    B=(b,v/omega), U=(u,w/omega), J=B outer U.

Keep every nonscalar active native variable, including the live metric and other species. Replace the scalar pair by the four entries of J on the coherent subspace. The inverse is U=J^T B/(B^T B), regular when B^T B>0. This is an injective constrained coordinate chart, not four new independent scalar perturbations. The coherent-subspace remainder is checked during evolution.

The physical source contributions are

    D=mu² J11+omega² J22,
    Q=k*omega*J21,
    P=-mu² J11+omega² J22.

These enter the native metric constraints and rest equations directly. In the flat retained background,

    z=(D_total/(2k)+eta_k)/H,
    eta_k'=Q_total/2,
    delta_cdm'=-k*z.

Consequently a CDM density perturbation changes z by R_c*Delta(delta_cdm)/(2kH). Rescaling the heavy moment changes z by Delta(D_h)/(2kH) and eta_k' by Delta(Q_h)/2. These general-k factors, including k=5 rather than the old k=1 probe, are tested independently.

Differentiating J gives J'=B' outer U+B outer U'. B' uses the actual background interpolant and native clock. U' includes -k*z*v forcing from the CURRENT metric. No future native metric or other-species trajectory is supplied as a forcing series.

## 3. Connect this chart to the saved memory equations

For the old normalization beta=a/R0, R0=2.479342985570997e-8, the saved cross-coordinate is

    j=beta*(J11,omega*J12,omega*J21,omega²*J22).

On the actual native clock, define Ef=r*b_N-v and Eb=r*v_N+2H*v+mu²*b. With aB=b²+v²/mu², the recovery rows are

    l_u=(b,0,v/mu²,0)/aB,
    l_w=(0,b,0,v/mu²)/aB.

Then the exact coherent-state operator is

    A_free=[[r,1,1,0],[-(mu²+k²),r-2H,0,1],
            [-mu²,0,r-2H,1],[0,-mu²,-(mu²+k²),r-4H]],
    A_defect=rows(Ef*l_u,Ef*l_w,Eb*l_u,Eb*l_w),
    G=(0,beta*b*v,0,beta*v²), o_D=(mu²,0,0,1),
    zeta=z-(o_D*j)/(2kHbeta),
    j'=[A_free+A_defect-G outer o_D/(2Hbeta)]j-k*zeta*G.

Physical normalized source rows are O=((mu²,0,0,1),(0,0,k,0),(-mu²,0,0,1)). Their nonzero derivatives are O'11=2rmu² and O'31=-2rmu². Hence Y'=O'j+Oj'. This is checked against both the current native product chart and direct differentiation of b,v,u,w on the integrated solution. The native r/H-1 is small, not identically zero; using r here retains the original interpolant rather than silently changing H in the physics.

At the right edge, the saved history endpoint agrees with this recovered j, its primitive pair and the retained phase-corrected carrier y=P^-1(M(u,w),zeta). In particular

    y_b=y_mean+delta_y_last,
    j_b=j_mean+h_last.

These identities connect the current state to the nonzero initial memory already derived. They do not equate current sources with the historical weighted average.

## 4. Causal continuation without inventing902 fields

The native full perturbation state obeys a current-state linear equation X'=F(t)X on the tested fixed regime. Let U(t,s) be its fundamental propagator, including all native rest/metric equations. On the finite interval where this initial-value problem is well-defined, X(t_i)=U(t_i,t_b)X_b. Thus the old source average can formally be written sum_i weight_i O(t_i)U(t_i,t_b)X_b. This identity is not a numerical prescription to integrate a dissipative hierarchy backwards, nor a proof that a three-component averaged carrier alone is invertible. The saved history avoids that unstable reconstruction.

A constructive forward representation is a delay record xi(t,ell)=X(t-ell), with

    partial_t xi+partial_ell xi=0,
    xi(t,0)=X(t),
    xi(t_b,ell)=the prepared past trajectory.

The source record can likewise store S(t,ell)=O(t-ell)X(t-ell); it obeys the same advection identity with new values injected from the current coupled solution. The historical readout is sum_i weight_i S(t,lag_i), lag_i=t_b-t_i>=0. Old weights remain signed and fixed, not occupation probabilities. Holding the lags fixed is NOT the same operation as shifting indices in a nonuniform time grid.

For the moment representation m=sum_i weight_i j(t-lag_i), h_i=j(t-lag_i)-m, the existing nonzero source memory C=sum_i weight_i O_i h_i is retained. Advection and the live right-edge boundary enforce that delayed nodes are samples of ONE trajectory rather than902 independently prepared physical fields. The previous formal retarded elimination remains available, but a compact numerical approximation to its kernel is a subsequent step.

This stage numerically establishes the physical boundary, its history-endpoint consistency, the live moment generator and a short coupled continuation. The delay-record readout across the advancing window is derived here but is not yet numerically propagated or compressed. That is the next bounded test.
