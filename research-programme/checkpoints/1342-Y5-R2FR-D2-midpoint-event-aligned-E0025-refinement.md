# 5326 - D2 midpoint event-aligned E0025 refinement

## Method

The complete 5325 pole census identifies seven support crossings in
topology panels 1, 7, 8, and 10.  Their coordinates are solved from the
signed pole-to-support margin.  Each crossing is integrated in squared
event coordinates; all other regions use direct coordinates.  Q4/Q8
outer comparison and recursive local refinement replace the coarse Q2/Q4
smoke rule.  A pole lying just outside a moving support endpoint is
subtracted with a one-sided Laurent fit evaluated entirely on the active
support branch; scale stability, pole-order suppression, and masked versus
unmasked identity are all required before its analytic logarithm is used.

## Result

- completed full run: `True`;
- encountered nodes: `372`;
- failed inner nodes: `0`;
- adaptive leaves: `26`;
- fixed-decay value: `36.4368093277` `+4.04408116584 i`;
- conservative relative error: `0.00245252283808`;
- decision: **D2_EVENT_ALIGNED_E0025_ACCEPTED__BUILD_D2_REGULATOR_LADDER**;
- validation: **PASS**.

## Claim boundary

A passing result closes only E0025 at D2_MID.  No epsilon-zero, angular
endpoint, full phase-space, UV, local-GR, or full-MTS claim follows.
