# 5265 — Piecewise outer-coefficient reassembly

## Construction

The decay-cosine integral is no longer forced through a single global polynomial. Six topology-uniform intervals use nested one-panel/two-panel Simpson rules. I01 and I06 are split at the four checkpoint-5264 certified boundary brackets and integrated chamber by chamber.

The transition estimate is the mean of shape-preserving PCHIP and Akima integrals. Its internal error ledger adds half their spread, the generation-8 to final-boundary shift, and the independently certified boundary-location error. This numerical ledger is conservative but is not promoted to a theorem-level interpolation bound.

## Endpoint analytic repair

The first generation-11 attempt exposed a real implementation defect rather than a failed residue: endpoint geometry replaced the complex outer coordinate by its real part during Newton refinement. That approximately doubled the regulator displacement of the `MC14` pole. The corrected endpoint map retains the full complex coordinate in the event geometry and root rationals.

With no gate relaxed, all four endpoint fits then recover simple-pole slopes between `-1.0148` and `-0.9857`, against the existing `0.12` tolerance. Their normalized root shifts are below `7.5e-11` of the fit radius and their root residuals are at machine precision. A 24-point complex contour audit independently gives nested residue spreads below `7.4e-11` and scaled double-pole leakage below `2.0e-10`.

## Result

- Validation passed: `True`.
- Order-512 coefficient: `-2.2499270271471357 -16.163056513555603i`.
- Order-512 magnitude: `16.318902153266297`.
- Total error estimate: `2.6284280512494713`.
- Relative error estimate: `0.16106647534027774`.
- Inner 128/512 relative difference: `0.000134864992246929`.
- Fixed-soft outer coefficient accepted: `True`.
- Decision: `ADOPT_FIXED_SOFT_PIECEWISE_OUTER_COEFFICIENT__HANDOFF_TO_SOFT_ENERGY_RULE`.

## Claim boundary

This locks one fixed-soft-energy two-angular coefficient. The final soft-energy integration, endpoint subtraction across that variable, and source-pool replication remain required before a numeric UV coefficient can be claimed. No local-GR or full-MTS claim follows from this checkpoint.
