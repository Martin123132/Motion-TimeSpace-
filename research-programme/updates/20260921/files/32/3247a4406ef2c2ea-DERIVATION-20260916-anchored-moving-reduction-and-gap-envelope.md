# A smooth retained chart and the first paired moving reduction

Private continuation of `DERIVATION-20260916-moving-spectral-connection-and-omitted-force.md`.

## Status and scope

The original prescribed-background finite action is unchanged. Its restriction to a derived moving subspace is now an actual reduced dynamical model, not a collection of frozen snapshots. This is a numerical approximation to the finite action, not a newly established parent action or a full GR limit. The original GR-oracle failures remain unchanged.

Implementation qualification, paired moving evolution and tighter-time-step controls are complete. Both branches pass the prespecified short, sampled reduction-force budget. This is not a full GR limit, an all-time certificate, or a replacement for the earlier GR-oracle comparison.

## 1. The first mask really did fail

The previous single-position cluster completion retained271/286 reference modes and273/286 MTS modes. Those fixed eigenvalue-index sets do not give a usable chart throughout the proposed moving interval. The first qualification attempt reached a reference finite-difference point outside the chart's overlap guard. The second attempt adapted the derivative stencil but then failed at the actual MTS qualification position b=6.0303. Neither failure was deleted or reclassified as a success.

This is a numerical subspace-tracking problem, not a physical MTS-versus-GR result. A near crossing between retained and omitted modes cannot be repaired by silently relabelling an eigenvector or dropping its coupling.

The constructive repair uses the same, trajectory-independent rule for both branches: take the transitive union of entire spectral clusters over201 prespecified positions in b in[6.029,6.031]. The adjacent relative cluster threshold is1e-3; all original force-aware retained modes stay retained. This gives273/286 reference and278/286 MTS modes. It is modest dimension reduction, not a performance breakthrough. No force data or fitted physical coefficient selects these extra modes.

The source interval, gap guard1e-4, and positive-overlap guard remain explicit. An exit triggers a stop, not extrapolation or a hidden change of chart. Internal crossings are allowed; a retained/omitted crossing is not. The initial survey alone is not a continuous-gap proof; section5 supplies a separate analytic criterion and qualified numerical evaluation.

## 2. Projector-anchored coordinates

At each b, let K U=M U Lambda and U^T M U=I. For a retained spectral set R separated from its complement,

    P(b)=U_R(b) U_R(b)^T M(b),
    W(b)=P(b) U_R(b0),
    G(b)=W(b)^T M(b) W(b)=L(b)L(b)^T,
    T(b)=W(b)L(b)^(-T).

The Cholesky factor L has positive diagonal. Thus T^T M T=I. If P is smooth and G stays positive definite, T is a smooth, anchored chart even if individual eigenvectors rotate, change sign, or exchange order inside R. It is not a repeated diagonalization convention for the reduced coordinates.

Compute P',P'' using local frame jets, but treat R and its complement as two invariant blocks. The local gauge C=U^T M U' is -N/2 within either block, N=U^T M' U. Only cross-block entries divide by eigenvalue gaps:

    C_ij=(Q_ij-lambda_j N_ij)/(lambda_j-lambda_i),
    Q=U^T K' U,  i and j in different blocks.

The earlier analytic second-frame law applies with that block partition. It differentiates an invariant block frame, not individual diagonal eigenvectors. Consequently arbitrary internal near-degenerate denominators never enter the projector derivatives.

Writing S=U_R U_R^T gives

    P'=S'M+SM',
    P''=S''M+2S'M'+SM''.

For the normalization, define low(X) as its strictly lower triangular part plus half its diagonal. Then

    L'=L low(L^-1 G' L^-T),
    L''=L low(L^-1 (G''-2L'L'^T) L^-T).

For F=L^-T,

    F'=-F L'^T F,
    F''=2F L'^T F L'^T F-F L''^T F,
    T'=W'F+WF',
    T''=W''F+2W'F'+WF''.

These are analytic derivatives of the actual anchored chart. They are not a local polynomial frame being passed off as a globally evolved coordinate system. A local quadratic jet is used only for independent complex-step checks of the equations.

## 3. Reduced action, source momentum and equations

With physical field u=T(b)x and speed V=b_dot,

    u_dot=T x_dot+V T' x.

Use the unchanged original matrices M,A,B,K. Define

    Acal=T^T M T'+T^T A T,
    Bcal=T'^T M T'+T'^T A T+T^T A^T T'+T^T B T,
    H=T^T K T.

Unlike a pointwise diagonal modal coordinate, H generally is not diagonal. The exact restricted action is

    Lred=|x_dot|^2/2+V x_dot^T Acal x
         +V^2 x^T Bcal x/2-x^T H x/2+Lm(b,V).

Its momenta are

    p_x=x_dot+V Acal x=T^T p_u,
    p_b,new=p_b,old+p_u^T T' x.

The source shift is mandatory coordinate bookkeeping, not a force correction. Energy is invariant under this time-independent coordinate restriction and pullback.

Let c=Acal x, h=Lm_VV+x^T Bcal x and s_R=h-c^T c. The equations are the coupled system

    x_ddot+c b_ddot=r_x,
    c^T x_ddot+h b_ddot=r_b,

where

    r_x=-V(Acal-Acal^T)x_dot-Hx-V^2(Acal'-Bcal)x,
    r_b=-x_dot^T Acal x_dot-2V x_dot^T Bcal x
        -V^2 x^T Bcal' x/2-x^T H' x/2
        +Lm_b-V Lm_Vb.

Thus b_ddot=(r_b-c^T r_x)/s_R. The derivatives of Acal,Bcal,H use T,T',T'' and the analytically differentiated original matrices. Source acceleration, transport, V^2 terms, and material-current derivatives all remain. No pressure-only replacement, damping, imposed trace, or subtracted force is present.

For the prescribed Schwarzschild-form background g=1-2m_bg/b, c=1 units,

    clock=sqrt(g-V^2/g),
    Lm=-S clock,  p_material=S V/(g clock),
    Lm_VV=S/clock^3.

The qualification includes m_bg=0 and0.7. The paired moving smoke uses m_bg=0, as the inherited finite-action comparison did. This is not a live-geometry variation.

## 4. Preparation and the moving defect

Keep original full initialization on the full side. On the reduced side,

    x0=T0^T M0 u0,
    x_dot0=T0^T p_u0-V0 Acal0 x0.

This preserves retained canonical field momentum. It does not preserve all omitted field data or impose equality of canonical source momentum while also fixing b,V. Record the initial preparation error; do not reset it to zero.

At each reduced state, lift the reduced acceleration back into the full original coordinates and evaluate the original coupled acceleration independently. Write delta_a=full_acceleration_at_lifted_state-lifted_reduced_acceleration. If e_u is the original field Euler-Lagrange residual of the lifted reduced trajectory and U_O is a mass-orthonormal omitted basis, define

    f_O=-U_O^T e_u,
    c_O=U_O^T(M T' x+A u),
    s=s_R-|c_O|^2.

The previously derived block law now applies along the evolving trajectory:

    DeltaF_same=-mu_material c_O^T f_O/s,
    |DeltaF_same|<=mu_material |c_O| |f_O|/s,
    ||delta_a||_Hkin^2=|f_O|^2+(c_O^T f_O)^2/s.

The last identity follows by solving the full versus constrained block acceleration system. It includes both the omitted-field acceleration and the induced retained/source acceleration, not just an omitted-tail norm.

Two scalar integrals are evolved with the reduced ODE: integral|f_O|dt and integral||delta_a||_Hkin dt. These are solver-controlled defect diagnostics, NOT a rigorous trajectory-error bound. Variable-metric stability/observable constants and a controlled tube are still needed to propagate them into an all-time force guarantee.

The actual paired force difference is separately split into same-state omission and trajectory/preparation contribution. This prevents the direct Schur-complement bound from being mistaken for a bound on two different evolved states. The reported field phase error at different b uses common reference-coordinate nodal values and the reduced-position quadratic form; it is not advertised as an Eulerian physical-field norm.

## 5. An analytic source-window gap criterion

For positive prescribed coefficient C=r(r-alpha), alpha=2m_bg, and the existing affine map, each stiffness weight is proportional to r(r-alpha)/J, or a nonnegative sampling combination of such weights. Each mass weight is proportional to J r^3/(r-alpha). The basis and Gram rows do not depend on b in reference coordinates.

Let r_min be the fixed inner radius, d_min the minimum distance from the source window to either endpoint, and assume r_min>alpha. Since 0<=k=dr/db<=1,

    |d log(w_mass)/db| <= gamma_M = 1/d_min+3/r_min+1/(r_min-alpha),
    |d log(w_stiffness)/db| <= gamma_K = 1/d_min+1/r_min+1/(r_min-alpha).

For alpha=0, both sharpen to1/d_min+2/r_min. Positive sums preserve these relative bounds. Therefore, as quadratic forms,

    exp(-gamma_M|d|) M(b0) <= M(b0+d) <= exp(gamma_M|d|) M(b0),

and similarly for K. The generalized Rayleigh quotient and min-max characterization then give, for every ordered eigenvalue,

    exp(-gamma|d|)lambda_i(b0) <= lambda_i(b0+d)
                                           <= exp(gamma|d|)lambda_i(b0),
    gamma=gamma_M+gamma_K.

If a center eigenvalue has enclosure radius delta, a sufficient gap condition for every retained/omitted index boundary i in its radius-h cell is

    (lambda_(i+1)-delta)exp(-gamma h)
       -(lambda_i+delta)exp(gamma h) > 0.

Covering the whole source interval with these cells excludes external crossings throughout the interval, conditional on valid eigenvalue enclosures. Internal crossings do not matter. This adds control between sampled positions rather than assuming a survey is a proof.

The checker derives a posteriori eigenvalue-radius estimates from the whitened residual and mass-orthogonality defect. If Q^T Q=G, ||G-I||<=epsilon<1, C Q=Q Lambda+E and C is the whitened symmetric pencil, polar orthonormalization gives the bound

    delta <= 2 epsilon ||Lambda||/[sqrt(1-epsilon)(1+sqrt(1-epsilon))]
             +||E||/sqrt(1-epsilon).

The implementation evaluates this in ordinary floating point and adds128*n*machine_epsilon*max|lambda| as a conservative numerical allowance. That allowance is NOT a directed-rounding error proof. Thus the exact analytic criterion is derived and its margin can be tested, but a rigorous interval certificate is still false. Do not conflate the conditional theorem with a machine-certified continuum result.

## 6. Prespecified moving comparison

- Original locally refined quadratic mesh: base129, source_splits8, full286 degrees.
- Original reference and MTS actions and full initialization unchanged; reduced masks from section1.
- Final time T=.005 with41 saved comparison times and8 accepted intervals. This is only1/80 of the earlier T=.4 benchmark, deliberately a first moving smoke test.
- DOP853 standard tolerances rtol2e-10, atol2e-12, maximum step1/omega_max.
- Independent temporal control: rtol2e-12, atol2e-14 and half the maximum step, on both branches.
- Numerical reduction-force budget2e-7 compares reduced with unchanged full finite action, NOT with a GR oracle. Success at41 samples is not an all-time bound.
- Save accepted intervals, nonzero preparation error, force decomposition, both integrated drives, source position/velocity/clock, energy drift, gap and overlap diagnostics.
- All physical failure flags remain in the evidence even if implementation checks pass.

## 7. Evidence and result table

Standard moving-run results (all41 sampled force-budget flags pass, on each branch):

| Quantity | Reference | MTS |
| --- | ---: | ---: |
| Retained/full field dimension |273/286|278/286|
| Maximum sampled reduced/full force difference |3.3163857833e-8|3.9748964208e-8|
| Initial preparation energy norm |1.0166737856e-7|2.7433948865e-8|
| Final reference-coordinate phase error |1.3965210629e-7|5.5503189420e-8|
| Integrated omitted drive |1.1303699731e-7|8.8523977809e-8|
| Integrated kinetic defect |1.1303716656e-7|8.8523991866e-8|
| Maximum source-position difference |3.9523939677e-13|4.6362913508e-13|
| Maximum source-speed difference |2.8169425126e-10|3.4198206766e-10|
| Maximum clock difference |2.3819488049e-14|2.7788535362e-14|

Full and reduced autonomous energies drift by at most6.94e-18 in each branch at the saved times. This is near floating-point resolution and not a rigorous error bar. The phase error is not erased just because the source errors are small. Each reduced RHS retains original source coupling and independently accumulates the actual moving omission defect.

Whole-window gap evaluation gives minimum relative margins0.00230899766/reference and0.00597934026/MTS. Minimum absolute margins473.5651 and2172.0262 exceed the maximum estimated floating eigenvalue radii0.00119416 and0.00138700 by large factors. The analytic criterion covers between survey points; its numerical implementation remains non-interval and conditional, as section5 states.

The tighter paired control completes with the same41/41 force flags for each branch. Its maximum sampled force differences are3.3163857833e-8/reference and3.9750722899e-8/MTS. Compared with the standard run, the largest change in the reduced/full force difference is7.8221e-14/reference and2.2770e-12/MTS, far below the2e-7 numerical reduction budget. The initial states and retained masks are identical; tolerances tighten100-fold and the maximum step halves. Integrated-drive, field-error, source and clock controls also pass their prespecified numerical tolerances.

There are199 successful current algebra/implementation checks across chart qualification141, gap envelope8, standard evolution17, tight evolution17, and precision comparison16. These counts measure implementation validation, not independent confirmations of MTS physics. Two failed first chart attempts are preserved; neither is used as an MTS/GR performance failure.

Primary outputs:

- `source-intake/navier-stokes/20260914/annular-anchored-chart-qualification-attempt03/status.json`
- `source-intake/navier-stokes/20260914/annular-anchored-moving-smoke-attempt01/status.json`
- `source-intake/navier-stokes/20260914/annular-chart-window-gap-attempt01/status.json`
- `source-intake/navier-stokes/20260914/annular-anchored-moving-tight-attempt01/status.json`
- `source-intake/navier-stokes/20260914/annular-anchored-moving-precision-attempt01/status.json`

Implementation and qualification:

- `scripts/annular_anchored_projector_chart_20260916.py`
- `scripts/annular_windowed_projector_chart_20260916.py`
- `scripts/verify_annular_anchored_chart_20260916.py`
- `scripts/verify_annular_anchored_chart_20260916_v2.py`
- `scripts/verify_annular_anchored_chart_20260916_v3.py`
- `scripts/run_annular_anchored_moving_smoke_20260916.py`
- `scripts/derive_annular_chart_window_gap_20260916.py`
- `scripts/verify_annular_anchored_moving_precision_20260916.py`

The first two qualification attempts are preserved failures. The third completes141 algebra/implementation checks including independent action/momenta/EL/Hessian tests, first and second finite differences, full-rank coordinate equivalence, exact synthetic internal crossings, and rejection of an external degeneracy.

## 8. Next mathematical target, not another missing-input inventory

There is a concrete output-specific identity to implement next, rather than another unspecified residual hunt. Let z be the original finite position/rate/clock state, F its full first-order vector field, z_tilde the lifted reduced solution, and d=F(z_tilde)-z_tilde_dot. Here d has only acceleration components; those are exactly delta_a in section4. Position and clock components vanish at the same lifted state.

Write e=z_full-z_tilde, A(t)=DF(z_tilde(t)), and

    e_dot=A(t)e+d+R_F,
    R_F=F(z_tilde+e)-F(z_tilde)-A(t)e.

For endpoint observable h(z)=the original finite material source force, let ell=Dh(z_tilde(t_final)) and solve the nominal adjoint

    -psi_dot=A(t)^T psi,  psi(t_final)=ell^T.

Differentiating psi^T e and integrating gives the exact identity

    h(z_full(t_final))-h(z_tilde(t_final))
       =psi(0)^T e(0)+integral psi^T d dt
        +integral psi^T R_F dt+R_h,

where R_h=h(z_tilde+e)-h(z_tilde)-ell e at the endpoint. Add the separately measured same-state omission force to obtain the total reduced/full force difference. Initial preparation has an explicit, nonzero term, and the defect is weighted by its actual force sensitivity instead of a global worst-case operator norm.

On a valid state tube, bounds ||D^2 F||<=M_F(t), ||D^2 h||<=M_h imply

    |nonlinear remainder| <= integral ||psi|| M_F ||e||^2/2 dt
                            +M_h ||e(t_final)||^2/2.

This is a derived identity and conditional remainder bound, not an implemented or certified adjoint result in this checkpoint. It needs the full coupled Jacobian, not just the wave block. At the velocity-defect contraction one may use

    |psi_velocity^T delta_a|
       <=||Hkin^(-1/2)psi_velocity|| ||delta_a||_Hkin,

which connects directly to the measured kinetic defect without pretending that its unweighted integral is already a force bound. An adjoint approximation without the remainder control would be a diagnostic, not a proof.

Next compute this endpoint force response for both branches on the saved short trajectories, compare its prediction with the actual discrepancy, and bound or explicitly measure the nonlinear remainder. Extend the paired interval only with explicit chart-window and cluster control; rechart/enrich conservatively if needed. Avoid building an indefinitely longer run that merely assumes the frozen budget persists.

Even a successful finite reduced/full comparison does not repair the inherited continuum/GR force discrepancy. A dynamic joint-refinement argument, treatment of the trace/memory domain, and connection to the parent/live geometry remain separate obligations. No proof of full GR, new empirical test pass, or public claim follows from this checkpoint.
