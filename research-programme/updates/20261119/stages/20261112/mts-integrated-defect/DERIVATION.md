# Integrated representation-defect contribution

This stage implements the preceding exact identity on the retained background, not a fitted pressure correction or a changed field equation. Native source authority is the preceding mts-equation-curvature-20261112 checkpoint; old files remain unchanged. Its folded-generator derivation of metric/rest and self-gravity derivatives is retained.

## Actual background, not a replacement clock

The new private native export saves the existing thermo interpolation knots S=a/tau, their x-derivatives, tau_min, dlntau and background density/mass constants. The original preparation/readout values are bit-identical to the preceding 902-node packets. All original standard-output parity checks pass. No physical sample grid is changed.

With x=log(tau/tau_min)/dlntau+1 and the original piecewise cubic S:

    a=tau*S(x)
    r=1/tau+S_x/(dlntau*a)
    r'=(S_x/dlntau+S_xx/dlntau^2)/(tau*a)-r^2.

H and H' are evaluated from the actual matter, radiation, massive-neutrino and scalar background representation. The unchanged natural-cubic scalar tables supply b,v and their derivatives. No r=H substitution is made. The Python reconstruction agrees with the native a,r,r',H,H' at the unchanged algebra gate for both branches.

## Coefficient evolution from the equations

Retain beta=a/R0, m2=(a*m_h)^2, u'=w and the coupled w',w'' already derived. The defect coefficients are

    C_b=beta*(m2*u,0,-m2*u)
    C_v=beta*(w,k*u,w).

For the nonzero C_b entries, their first and second derivatives are beta*m2 times

    3r*u+u'
    (3r'+9r^2)*u+6r*u'+u''.

For beta*w, the derivatives are beta*(r*w+w') and beta*((r'+r^2)*w+2r*w'+w''); for beta*k*u replace w with k*u. The frozen primary coefficient representation is C(t)=C0+t*C0'+t^2*C0''/2. A linear representation is retained as a numerical approximation control, not fitted to the source target.

For E_b=b'-v and E_v=v'+2Hv+m2*b, compute E(t) from the original background, then evaluate

    I(s)=-s*C0*E0 + integral_0^s [C(t)-(s-t)C'(t)]E(t) dt.

This equals integral_0^s(s-t)C(t)E'(t)dt for the same chosen C(t). Direct E' quadrature is an independent check, not the implementation used for the prediction. Integration is split at the exact background/thermo interpolation knots. Orders8/16 refine quadrature only, not the physical grids. The maximum absolute-weighted integration-by-parts discrepancy is about2.24e-16 and quadrature discrepancy3.90e-17 in retained source units, across density/current/pressure.

The frozen primary prediction is

    Y_pred(s)=Y0+s*F1+(s^2/2)*sum_i(weight_i*R_i0)+sum_i(weight_i*I_i(s)),
    R=Y''-C_b E_b'-C_v E_v'.

The original nonzero history, source normalization, signed weights, source-map terms and initial metric/rest derivative are preserved. Only R is frozen; it is an algebraic remainder, not a demonstrated slow variable. Cold has no heavy defect correction and remains the existing equation-owned quadratic control.

## Finite correction versus local curvature

At the final saved offset, the integrated heavy defect contribution (D,Q,P) is

    (-3.398199741955805e-11, 3.50036133300526e-11, -8.440854043936155e-10).

That pressure contribution is opposite in sign to extending its positive initial defect curvature as a constant. This explains why the actual integrated prediction can improve despite retaining, rather than deleting, the representation defect. It does not establish that all remaining error is a background artifact.

## Remainder controls and their limits

The predeclared6/8-knot derivative estimates of R disagree enough to fail the pressure gate after propagation. Their inferred cubic corrections are not promoted. A separate direct-integral diagnostic then acquires R at the eight already-saved continuation epochs, keeping the original reporting grid. This diagnostic uses the reference trajectory, not a new predictive input or observational holdout.

Natural-cubic, PCHIP and linear representations of R are integrated analytically in local polynomial coordinates. Twelve degree0..3 analytic integral controls pass. The natural-cubic signed pressure-variation contribution is small, but PCHIP differs and the absolute-weighted representation envelope is large. Signed weighted sums cancel strongly; a small net value alone cannot certify an error allowance. Equally, the deliberately absolute-weighted envelope is NOT a measured physical error or a confidence interval. Neither this check nor the failed derivative estimate justifies rejecting the retained theory; both block certifying the frozen-R approximation at this precision.

## Constructive route for the next bounded check

Avoid another derivative stencil or unconstrained interpolation of cancelling R. Reuse the saved background and each node's primitive initial state. At a fixed node, separate the actual metric into its heavy scalar source and rest:

    z=zeta+(m2*b*u+v*w)/(2kH).

This gives the two-component short-interval equation

    u'=w
    w'=-(m2+k^2+v*m2*b/(2H))*u
        -(2H+v^2/(2H))*w-k*v*zeta.

Both self-gravity coefficients follow from the existing constraint; no new coupling is introduced. zeta0 and zeta0' are already derived in the prior stage, so a first-order rest expansion can be frozen before comparing against the reference, with a constant-rest control explicitly labelled approximate. Background coefficients stay time-dependent. Propagating these primitive pairs preserves their coherent cancellation before forming Y and summing the fixed weights, instead of interpolating a high-amplitude stress remainder component by component.

This is a proposed local predictive test, not a completed calculation or a replacement for the full coupled rest hierarchy. Step refinement and the rest-expansion control are required. No guaranteed pass is asserted. The original full-rest short evolution and first-order accepted source prediction remain the references.
