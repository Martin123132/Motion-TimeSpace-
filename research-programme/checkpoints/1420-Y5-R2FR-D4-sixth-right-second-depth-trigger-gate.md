# 5404 — Sixth-right second depth-trigger gate

## Purpose

Checkpoint 5404 tests the second depth-fourteen transition on the sixth-support right connector. It uses the unchanged production evaluator first, then the path-addressed derivative and factorized-angle audits, before allowing the leaf back into production.

## Result

- The exact path `RDLDRDRDLDLDRU` covers `x in [0.287293254204984, 0.287431332070181]` and `t in [0.0078125, 0.015625]`.
- The ordinary production evaluator certifies the leaf with amplitude-denominator lower bound `0.0010154847978798421` and collision-Jacobian lower bound `0.07480940521750942`.
- All `108` centred-derivative comparisons pass with maximum relative error `5.851378006985454e-16`.
- Every closed factorized-angle scheme passes. The weakest certified positive-imaginary lower bound is `0.0013575974869823363`; the `32 x 32` cover proves modulus lower bound `0.004676133928216189`.
- A confirming bounded production resume commits the leaf, advances the connector `264 -> 272` accepted boxes, and returns the pending frontier to `7` boxes at maximum depth `10`.
- Accepted parameter area is `0.00956189216486214`, or `0.5410156250000006` of the complete connector rectangle. Accepted plus pending area remains exact within floating-point outward tolerance.

## Decision

The second right-connector trigger is a finite conservative transition, not an observed physical zero. Revision v40 may continue from the preserved shallow frontier. This does not prove global univalence, regular-away `W3`, regulator removal, local GR, or full MTS.

Machine-readable validation is stored in `source-intake/functional_rg/5404/P8_Y5_BRR5396_5404_VALIDATION.csv` and `source-intake/functional_rg/5404/sixth_right_second_depth_trigger_gate_result.json`.
