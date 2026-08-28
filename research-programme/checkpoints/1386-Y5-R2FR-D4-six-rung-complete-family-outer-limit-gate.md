# 5370 - D4 six-rung complete-family outer-limit gate

## Decision

`D4_SIX_RUNG_COMPLETE_FAMILY_GATE_FAILS__OUTER_REGULATOR_ZERO_LIMIT_REMAINS_BLOCKED`

The gate was frozen before the E0003125 measurement. It tests both the checkpoint-5345 free-A complete second-order family and the stronger checkpoint-5360 source-constrained fixed-A family.

- fixed-A maximum normalized residual: `0.0053121389449495779`;
- free-A maximum normalized residual: `0.0046782515571801601`;
- source-A compatibility: `True`;
- fixed/free intercept compatibility: `True`;
- relative conservative intercept envelope: `0.028292189199063279`;
- full frozen gate passes: `False`.

## Claim boundary

A passing result is a conditional numerical D4_OUTER regulator-zero extrapolation under the parent normal-form hypotheses. The separate uniform numerical M_D4 remainder constant, decay-angle limit, full phase-space coefficient, UV result, local GR, and full MTS theory remain unclaimed.

The frozen gate first completed its mathematics but exposed NumPy boolean scalars to the standard JSON writer. The recorded adapter verifies the preregistered script hash and converts only scalar representation; no fit, threshold, gate, or claim rule changed.
