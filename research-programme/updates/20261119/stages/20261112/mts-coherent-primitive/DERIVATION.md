# Coherent primitive evolution and rest-curvature response

## Retained model and scope

This calculation starts from the existing902-node prepared history, original signed weights, native clocks, background splines and source normalization. It is a short-window prediction at the same nine original reporting epochs, not a new cosmological fit, a galaxy occupation prescription or a replacement action. Inputs and their hashes are in frozen-inputs.json. No native preparation is rerun: the preceding clock and derivative readouts are reused directly.

H is the retained Friedmann rate and r=(log a)' the actual native interpolation rate; neither is substituted for the other. Background fields b,v and their derivatives come from the existing natural-cubic tables. Time is native conformal Mpc with c=1.

## Heavy pair with live self-gravity

Let m2=(a*m_h)^2 and D_h=v*w+m2*b*u, without the historical source normalization. The existing constraint gives

    z=zeta_h+D_h/(2kH).

Substitution into the original perturbation equations yields

    u'=w
    w'=-(m2+k^2+v*m2*b/(2H))*u
        -(2H+v^2/(2H))*w-k*v*zeta_h.

The self-gravity terms evolve with the actual state and time-dependent background. They are not frozen forces or new fitted couplings. Initial rest coefficients follow from the coupled native readout:

    zeta_h0=z0-D_h0/(2kH0)
    zeta_h0'=z0'-[D_h0'-D_h0*H0'/H0]/(2kH0).

The primary rest approximation is zeta_h(s)=zeta_h0+s*zeta_h0'. A constant-rest control retains zeta_h0 only. Both are explicitly local approximations to the other matter, metric and field variables. The full rest hierarchy is not integrated in these reduced runs.

The physical normalized sources are formed only AFTER evolving the pair:

    Y_h=(a/R0)*(v*w+m2*b*u, k*v*u, v*w-m2*b*u).

There is no independent pressure fit, sampled pressure-curvature interpolation or deletion of background representation defects. The pair retains the common phase from which density, current and pressure are constructed.

## Baseline receives the corresponding control

For cold CDM perturbation delta_c, the native equation is delta_c'=-k*z. Let R_c=background_CDM_constant/a. Separate its live density contribution:

    z=zeta_c+R_c*delta_c/(2kH)
    delta_c'=-R_c*delta_c/(2H)-k*zeta_c
    zeta_c0'=z0'-R_c0*[delta_c0'-(r0+H0'/H0)*delta_c0]/(2kH0).

Its primary/control rest expansions use the same linear/constant rule, with its own background, clock and initial state. The source is the retained normalization times(delta_c,0,0); no fictitious heavy field is added to the baseline. Zero dust current and pressure are properties of this retained-frame source readout, not a claim that all baseline matter stresses vanish.

## Initial and numerical checks

The first AND second primitive derivatives obtained by differentiating the reduced equations match the original coupled readout at1e-10. That includes the time-dependent self-gravity coefficients and zeta0'. Background a,r,r',H,H' reconstruction passes the same gate. Three independent matrix-exponential controls test affine forcing. These are numerical/algebraic controls, not new observations.

DOP853 uses rtol1e-10 and normalized atol1e-12, with32/64maximum-step subdivisions. The physical grids and reporting epochs are unchanged. Each heavy pair is numerically scaled by its initial phase amplitude and corresponding velocity amplitude; cold is scaled by its initial density amplitude. These scales do not change the equations or fit parameters.

To retain the previously saved initial historical source, predictions use

    Ybar_pred(s)=Ybar_saved(0)+sum_i weight_i*[Y_i(s)-Y_i(0)].

The raw initial recapture discrepancy is separately recorded and included in the working numerical allowance. This is initial-state matching rather than fitting an offset. Both increment summation and direct weighted readout are checked. All trajectories are frozen before target-source comparisons.

## Why constant-versus-linear is not a missing-error bound

Heavy pressure fails with constant rest but passes with linear rest. Their difference measures the already-included first-order physical response. It does NOT bound the next, omitted rest-curvature term. The predeclared stricter sensitivity envelope is reported and fails; it is not reinterpreted as a demonstrated failure of the linear-rest prediction. Nor is the linear prediction declared accurate for arbitrary histories merely because it matches this exposed reference window.

## Derived response to the remaining rest curvature

For either reduced system write x'=A(s)x+B(s)zeta(s), and terminal source Y_j=L_j(s)x(s). If the initial matching and linear coefficient are correct and the unknown remainder satisfies a uniform bound |zeta''|<=K, then

    |delta_zeta(t)| <= K*t^2/2
    delta_x(s)=integral_0^s Phi(s,t)B(t)delta_zeta(t)dt.

Solve the adjoint lambda_j'=-A^T*lambda_j backward with lambda_j(s)=L_j(s)^T. The resulting source response obeys the conditional inequality

    |delta_Ybar_j(s)| <= K*G_j(s)
    G_j(s)=sum_i |weight_i|*integral_0^s |lambda_ij(t)^T*B_i(t)|*t^2/2 dt.

The absolute values allow unrelated signs across nodes; no cancellation is assumed in this bound. It is conditional on the actual uniform curvature bound, which this stage does not establish.

check_response.py evaluates these gains numerically at the FINAL saved epoch, with32/64refinement, and checks the signed adjoint response against an independent forward response to unit quadratic rest forcing. Boundary primitive states are also checked against the saved full native reference. These checks pass. Numerical gains are not certified interval enclosures.

Heavy final gains(D,Q,P) are approximately

    (1.2557834093e-6,1.5278831495e-8,1.2412515406e-6).

After the observed residual and numerical allowance, the conditional uniform curvature ceilings are approximately(0.748785,45.1992,0.00356303) in native rest-variable/Mpc^2 units; pressure is restrictive. The cold density ceiling is812.762 in its own rest-variable convention. These numbers are requirements for a later bound, not measured curvatures, fitted parameters, or a certificate covering all intermediate epochs.

## Next derivation can use the existing coupled equations

For the heavy split, let D_rest exclude the heavy scalar density but retain all other perturbed densities. Then

    H*zeta_h=D_rest/(2k)+eta_k
    zeta_h''=[D_rest''/(2k)+eta_k'']/H
              -2*(H'/H)*zeta_h'-(H''/H)*zeta_h
    eta_k''=Q_total'/2  (retained flat convention).

H'' comes from the actual background representation. D_rest'' and Q_total' must come from the coupled matter/radiation/neutrino/slow-field equations, retaining interpolation and approximation conventions, rather than another blind high-order difference of cancelling source arrays. The cold split has the analogous equation excluding its own CDM density. This identifies the quantities to derive/read out next. A bound must cover the interval, not just the maximum at saved nodes. A quadratic-rest predictor can be frozen and tested once its coefficient is genuinely supplied by those equations.
