# A derived projection response and pressure relation

This continues the retained real-scalar/CDM branch and the original a225-w6-d8 temporal extraction. The background, k=1 Mpc^-1, gravitational normalization, initial seeds, 902 output times and signed weights are unchanged. No observational fit or pressure fit is performed.

## Coupled source block, not a prescribed total metric

The block is x=(u_s,w_s,delta_c) for the baseline and x=(u_s,w_s,u_h,w_h,delta_c) for MTS. It carries ALL retained real scalars AND the synchronous CDM density, not just a heavy scalar with frozen self-gravity. The remaining baryon/photon/neutrino densities and eta_k are supplied from the saved reference history in this operator test.

Define D_block=d(t)x, where each scalar contributes (mu_j^2*b_j,v_j) in its pair of columns and CDM contributes R_c in its column. Then

    z_rest=(D_rest/(2k)+eta_k)/H
    z=z_rest+d*x/(2kH)
    x'=A0*x+B*z = [A0+B*d/(2kH)]*x+B*z_rest.

A0 contains each KG block [[0,1],[-(k^2+mu_j^2),-2H]] and a zero CDM density diagonal. B has scalar entries (0,-k*v_j) and CDM entry -k. Thus CDM self-gravity, scalar self-gravity and scalar–CDM density feedback are included in A. The other metric/species history is still supplied; this is not a new fully reduced coupled cosmology.

D_rest is calculated from the other species' own density contrasts and homogeneous densities, not inferred by subtracting a desired scalar result. Eta remains part of the rest system and must respond to scalar/current stress in a future fully coupled implementation. The pressure/current source rows are C_P=(-mu2*b,v), C_Q=(k*v,0); synchronous CDM current/pressure remain zero. The same-state block RHS and source rows are checked against the actual native derivatives/readout.

For clarity, the block trace is invariant under fixed numerical similarity scaling:

    tr(A)=-2H*N_scalar-(R_c+sum_j v_j^2)/(2H).

## Evaluate the retarded solution instead of fitting a closure

With T'=A*T and T(t0)=I, standard variation of constants gives

    x(t)=T(t)[x0+integral_(t0)^t T(s)^(-1) B(s) z_rest(s) ds].

Here and in the implementation T(t) means T(t,t0). Fundamental integration, retarded quadrature and driving-history interpolation are refined separately. The numerical state scaling is a constant similarity transformation based on coordinate peaks; it is not a fitted physical parameter and does not change x or its source rows.

Let beta=a/rho0 use the historical normalization and let wi be the unchanged signed extraction weights. For all projected source rows:

    projected_sources = L*x0 + source_forcing
    L=sum_i wi*beta_i*C_source(t_i)*T(t_i).

This retains the initial-state contribution and the entire specified forcing history. It does not assume positive phase occupation, stationary averaging or a universal local sound speed.

## Identify the actual unknown physical block

For MTS the reconstruction target is only the TWO heavy initial coordinates. The retained slow-scalar and CDM initial values are known and are propagated, not zeroed physically. Write their contribution plus the retarded forcing as h. Select the original heavy density/current rows:

    y=(projected_D_h,projected_Q_h)
    y=L_unknown*x_h0+h_DQ.

The baseline is a one-dimensional CDM reconstruction from its projected density. It is not subjected to an artificial2x2 inversion with an identically zero current row. Baseline slow-scalar evolution and pressure remain checked in the forward/inverse trajectories.

Before inversion, measure the rank and condition of L_unknown. Rows are scaled by their maximum absolute response, columns use the already-declared numerical state units. Both this dimensionless condition and the raw matrix condition are retained. The forcing subtraction is assessed separately: a well-conditioned matrix alone would not rule out catastrophic cancellation in y-h.

The resulting MTS matrix has rank2 and scaled condition about1.00131769 in this window; the right-hand-side cancellation ratios are about1 and1.00144. This supports a stable conditional reconstruction HERE. It is neither a general theorem for all windows/k nor a determination of unknown external histories/populations.

## Eliminate the reconstructed coordinates to predict pressure

The pressure row is NOT used in the inversion. Eliminating the heavy seed gives

    projected_P_h = h_P+L_P*L_unknown^(-1)*(y-h_DQ)
                  = a_D*projected_D_h+a_Q*projected_Q_h+h_effective.

At the finest saved configuration, in the original source normalization:

    a_D = 2.1985207325650542e-4
    a_Q = 1.3854484743668138e-5
    h_effective = -5.949823326616946e-7.

These numbers are computed from the retained action/background response and specified other-species/known-seed history. They are NOT regression coefficients fitted to pressure. They belong to this finite temporal extraction, not instantaneous D/Q at arbitrary time or a reusable cosmology-independent fluid law. The history offset must not be dropped: doing so gives about0.2644% pressure error on the saved case.

The fine prediction is -2.2500624054861969e-4 versus the saved projected pressure -2.2500624054007335e-4. Its pressure-relative discrepancy is about3.80e-11. A coarser driving history gives a larger discrepancy; all retained tests use their original gates. These are internal numerical comparisons, not measured cosmological precision.

The same response maps the reconstructed seed to the full block's endpoint, including the induced slow-scalar/CDM evolution. Thus a next native continuation can start from an action-derived reconstructed endpoint rather than choosing a new D0. Its accuracy must be tested in live evolution; the algebra alone does not authorize changing a distinct positive-ensemble late branch.

## Finite-refinement sensitivity attribution

For fine response A_f,h_f and a changed numerical representation A_c,h_c, with the SAME measured projected pair y, the reconstructed seed difference obeys exactly

    A_f*(x_c-x_f) = -(A_c-A_f)*x_c-(h_c-h_f).

If epsilon=||A_f^(-1)*(A_c-A_f)||_inf<1, then

    ||x_c-x_f||_inf <=
      [||A_f^(-1)*(h_c-h_f)||_inf
       +||A_f^(-1)*(A_c-A_f)*x_f||_inf]/(1-epsilon).

The check includes an explicit floating-point allowance for subtracting nearly identical seeds. This bounds the OBSERVED finite refinement, conditional on its measured operator/history differences; it is not a certified bound on an unknown continuum solution. Independent source-column perturbations test the linear pressure elimination algebra without fitting pressure.
