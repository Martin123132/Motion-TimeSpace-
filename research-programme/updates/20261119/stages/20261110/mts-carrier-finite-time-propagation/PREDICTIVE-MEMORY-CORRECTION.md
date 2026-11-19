# Derived next correction without using the exact trajectory as input

This derives a concrete follow-on from the defect transport. It is not a report that the follow-on has been run. The current error channel uses the exact conditional reference for diagnosis; that channel must not be presented as a prediction.

Write the exact conditional transformed two-component equation as

    y'=(B+R)*y+f+g,

where B is the proposed first effective generator, R is its explicit operator remainder, f is the retained approximate forcing, and g is the corresponding forcing remainder. Both R and g follow from the current background, exact coordinate maps and prescribed rest-source history. They must be evaluated from those equations, not from future exact heavy perturbations. Keeping g is important: the augmented third coordinate z_rest introduces a remainder in the forcing column as well as in the 2x2 operator.

Let the existing forward prediction y0 solve

    y0'=B*y0+f

with the frozen original initial data. The FIRST PREDICTIVE memory response is

    delta1'=B*delta1+R*y0+g, delta1(t0)=0,
    y1=y0+delta1.

Its source contains the approximate y0, not the exact reference. Equivalently it is the first variation-of-constants correction with the propagator of B. No coefficient or output residual is fitted.

An exact subtraction then gives

    y1'=(B+R)*y1+f+g-R*delta1,
    e1'= (B+R)*e1+R*delta1, e1(t0)=0,

where e1=y_exact-y1. Thus the next residual is explicitly R*delta1, computable without access to y_exact. A componentwise comparison system with the same diagonal and absolute off-diagonal entries of B+R, driven by abs(R*delta1), supplies a conditional error-envelope route. Any numerical bound still needs integration/refinement checks before a certified-bound claim.

## Explicit current-coefficient construction

In the saved implementation let p=(u,w), X=M*p, and X=T*y+h*zeta, where T=P[:2,:2], h=P[:2,2], and zeta is the retained rest-source history. The last row of the retained augmented P is (0,0,1). Let the primitive equation be p'=A_p*p+f_p; f_p already contains the prescribed rest-source factor. All of M, M', P, P', A_p, f_p, zeta and zeta' are returned by the existing History.evaluate operation, without an exact heavy perturbation argument.

Define

    A_X=(M'+M*A_p)*M^-1,
    A_exact=T^-1*(A_X*T-T'),
    f_exact=T^-1*((A_X*h-h')*zeta+M*f_p-h*zeta'),
    R=A_exact-B, g=f_exact-f.

These expressions follow by differentiating M*p=T*y+h*zeta and substituting the primitive equation. Use matrix solves, not stored fitted coefficients. They give the actual operator and forcing remainders needed above. In particular, g need not vanish when R is small; a correction that silently omits g is a different equation. The next implementation must check this algebraic map against the existing exact_reduced_rate for arbitrary instantaneous test vectors before propagation.

## Concrete test

Use the original frozen initial data and histories. Integrate y0 and delta1 without feeding in the exact reference; run the reference only as a separately checked comparator. Apply the unchanged exact source reconstruction to y1. Test both instantaneous native stresses and their original signed projections, especially pressure, with all gates retained. Mutation checks must demonstrate that changing the comparator does not change y0 or delta1.

This is an explicit parent-derived memory correction, not a new adjustable local fluid law. If it closes a discrepancy only when exact-reference values are supplied, it has failed the predictive test. A fully coupled version must lift R,g and the source response to the current rest-species state using LIVE-FEEDBACK-LIFT.md rather than treat future rest histories as a new physical input.
