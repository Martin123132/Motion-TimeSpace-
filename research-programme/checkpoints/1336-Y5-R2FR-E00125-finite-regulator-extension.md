# 5320 - E00125 finite-regulator extension

## Method

The 5319 complete logarithmic remainder envelope missed the inherited
one-percent zero-limit gate by a narrow margin.  This checkpoint therefore
computes the requested `epsilon=0.00125` value directly.  Panels 1-8 use
adaptive Q8/Q12 outer quadrature; panel 9 derives its own support-entry,
support-exit, and branch-death geometry and uses exact squared-event Jacobians.
Every inner integral uses the normalized Laurent/raw-contour contract from 5318.

## Result

- encountered nodes: `380`;
- completed nodes: `380`;
- failed inner nodes: `0`;
- fixed-decay value: `104.52780834` `-19.8686401484 i`;
- conservative relative error: `0.000613775664825`;
- decision: **E00125_FINITE_REGULATOR_CONVERGED__REFIT_ZERO_LIMIT**;
- validation: **PASS**.

## Claim boundary

A passing result adds one finite-regulator fixed-decay point only.  It does not
itself establish the regulator-zero limit, decay-angle integration, full
phase-space coefficient, UV behavior, local GR, or the full MTS theory.
