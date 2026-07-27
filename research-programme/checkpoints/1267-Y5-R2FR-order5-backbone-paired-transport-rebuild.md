# 5251 - Order-5 backbone paired-transport rebuild

## Calculation

The reciprocal-projective collision and chamber-boundary transport accepted at checkpoints 5245-5249 is applied to every nested order-5 node: Q00/Q02/Q04/Q06/Q08. Each node has an independent resumable state/job cache. Its corrected inner slice is then recomputed under the same residue, coverage, and regulator-extrapolation gates as Q03/Q05.

## Endpoint-resolution derivation

Q00 exposed a resolution failure rather than a failed physical gate. For Y00_E040_MC07 at soft cosine -0.995, the winding pair remained (-1,+1) while the maximum paired projective step fell through 0.387743, 0.232171, 0.121320, 0.061304, and 0.030760. The locked 0.05 gate therefore closed at base resolution 262144. Q08 independently required the same maximum resolution at the reflected endpoint. No acceptance threshold was relaxed.

## Per-node results

- Q00: changed maps `0/12`, corrected `(-0.0016047463806135056-0.0002760343617074112j)`, relative change `0.00424840076167`, acceptance `True`.
- Q02: changed maps `4/12`, corrected `(-400.35272689381867+7.318107568452313e-05j)`, relative change `0.00215061104371`, acceptance `True`.
- Q04: changed maps `8/12`, corrected `(37.37905668096878-5.7636408751943105j)`, relative change `0.00320014710782`, acceptance `True`.
- Q06: changed maps `4/12`, corrected `(610.0633126183284-0.0007455163215144661j)`, relative change `0.000234035298486`, acceptance `True`.
- Q08: changed maps `0/12`, corrected `(-0.0016047463806134657-0.000276034361707373j)`, relative change `0.00424840076167`, acceptance `True`.

## Corrected cubature

- Corrected order-3 value: `(12.397121012079863-1.911653332637763j)`.
- Corrected order-5 value: `(35.259983428209416-1.147062885779279j)`.
- Corrected order-3/order-5 relative difference: `0.648427662939`.
- Corrected order-5 inner 128/512 relative difference: `4.84559258372e-07`.
- Backbone+Q03/Q05 partial order-9 diagnostic: `(15.070546891172082-0.564440652709619j)`.
- Corrected order-5/partial-order-9 relative difference: `1.33928053215`.
- Formal-workbench files changed during 5251: `0`.
- Historical protected digest matched at start: `False` (a false value is retained as a provenance warning, not silently relabelled).

## Decision

`ADOPT_CORRECTED_ORDER5_BACKBONE__REBUILD_Q01_Q07_FOR_FULL_ORDER9`

## Interpretation

The order-5 baseline is now like-for-like only if all five node gates pass. The partial order-9 value remains a diagnostic because Q01 and Q07 still retain inherited topology; it is not a coefficient.

## Claim boundary

No numeric UV coefficient, local-GR extension, or full-MTS claim follows from this checkpoint. The selected local two-derivative GR+SM+Maxwell theorem is unchanged.

## Next exact target

Apply the same paired reciprocal-projective transport to Q01 and Q07, then recompute the fully corrected order-9 cubature and only then test the locked outer-convergence and Chebyshev-tail gates.
