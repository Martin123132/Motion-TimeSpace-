# 5252 - Q01/Q07 paired transport and full order-9 gate

## Calculation

Q01 and Q07 receive the same reciprocal-projective collision and chamber-boundary transport used for the accepted Q00-Q08 backbone. All nine corrected node values are then assembled under the original order-3/5/9 weights and the original 0.2 convergence and Chebyshev-tail thresholds.

## Corrected node profile

- Q00: `(-0.0016047463806135056-0.0002760343617074112j)`, source checkpoint `5251`, relative correction `6.88878818888e-06`.
- Q01: `(2310.4652308335662+0.0028306205656028725j)`, source checkpoint `5252`, relative correction `8.27266894838e-05`.
- Q02: `(-400.35272689381867+7.318107568452313e-05j)`, source checkpoint `5251`, relative correction `0.00215061104371`.
- Q03: `(252.15977839895186+0.0006007742174577774j)`, source checkpoint `5247`, relative correction `0.0829953383953`.
- Q04: `(37.37905668096878-5.7636408751943105j)`, source checkpoint `5251`, relative correction `0.00320014710782`.
- Q05: `(-160.8231942911625-0.0006217358495971361j)`, source checkpoint `5249`, relative correction `0.136739785311`.
- Q06: `(610.0633126183284-0.0007455163215144661j)`, source checkpoint `5251`, relative correction `0.000234035298486`.
- Q07: `(-2624.339198839262-0.0031190341631583208j)`, source checkpoint `5252`, relative correction `0.000441012167393`.
- Q08: `(-0.0016047463806134657-0.000276034361707373j)`, source checkpoint `5251`, relative correction `6.88878818887e-06`.

## Full corrected cubature

- Order 3: `(12.397121012079863-1.911653332637763j)`.
- Order 5: `(35.259983428209416-1.147062885779279j)`.
- Order 9: `(15.035421321258777-0.5644406519310965j)`.
- Order 3 to 5 relative difference: `0.648427662939`.
- Order 5 to 9 relative difference: `1.34473851875`.
- Degree 5 to 8 Chebyshev-tail fraction: `0.76758127348`.
- Order-9 inner 128/512 relative difference: `7.19380699071e-07`.

## Decision

`HOLD_FULL_ORDER9_CUBATURE__LOCALIZE_CORRECTED_OUTER_PROFILE`

Failed acceptance gates: `OUTER_ORDER_3_TO_5_CONVERGENCE|OUTER_ORDER_5_TO_9_CONVERGENCE|ORDER9_CHEBYSHEV_TAIL_DECAY`.

## Protection and claim boundary

- Formal-workbench files changed during 5252: `0`.
- No numeric UV coefficient, local-GR extension, or full-MTS claim follows from this one angular slice.

## Next exact target

Localize the corrected decay-angle profile by interval and build a piecewise/adaptive outer rule before increasing the global order; do not promote this slice.
