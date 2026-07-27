# 5219 - General grouped owned-direct classifier

## Derived scope

For a nonzero relative collision row whose every collision pair
is direct-only and has exactly one chamber-owned `direct:g1` or
`direct:g2` pole, linearity permits the pair residues to be
evaluated separately and summed point-by-point.

The classifier uses frozen `L32` and `L48` grids. A finite
nonzero requires radius stability and cross-level agreement.
A zero candidate additionally requires rapid `L32 -> L48`
suppression and an `L64` value below the unchanged `1e-20` gate.
Unknown scopes, cancellation-only grouped zeros and failed
precision tests remain unresolved.

## Witness

- Grouped rows resolved: `3/3`.
- Stable nonzero summands: `3`.
- Event-local zero summands: `2`.
- Validation: `7/7`.

## Status

- General classifier authorized: `True`.
- Current outcome-exposed pilot scale decision: `not allowed`.
- Next: freeze a new independent pilot with this classifier
  declared before topology or residue outcomes.

## Evidence

- Gate: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\functional_rg\5219\general_grouped_owned_direct_classifier_gate.json`
- Witness audit: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\functional_rg\5219\S521509_grouped_classifier_witness_audit.csv`
- Validation: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_BRR545_5219_VALIDATION.csv`
