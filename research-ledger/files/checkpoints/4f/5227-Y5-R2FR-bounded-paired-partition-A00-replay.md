# 5227 - Bounded paired-partition A00 replay

## Result

The unit source-family control rejected at checkpoint 5225 has been replaced
by an exact bounded channel pullback, not by a fitted coefficient.

Decision: `REJECT_PAIRED_PARTITION_SCALE_WITHOUT_NEW_DERIVATION`.

All `48/48` replay jobs converged.

## Derived estimator

The original direct channel is

`W3 = 3 w3`.

Checkpoint 5226 supplies the measure-preserving `g1<->g3` involution.
Pulling the slot-1 channel back into the working slot-3 chart gives `3 w1`.
Their arithmetic mean is therefore

`W13 = 3 (w3+w1)/2`.

This is unbiased by identical-graviton symmetry. On real phase space,
`0 <= W13 <= 3/2`, so it cannot reproduce the unbounded `w1/w3`
importance ratio. Because `W3` and `W13` have the same partition
denominator, no new topology poles are introduced.

The plus-distribution endpoint is also derived: as `x3->0`, `w3->1` and
`w1->0`, so the paired endpoint subtraction is exactly one half of the
original endpoint.

## Retrospective test

- Events: `24`.
- Mean paired-minus-raw difference:
  `504.662354` with
  `1.3094` standard errors.
- A00 real SD ratio:
  `4.05545962`.
- Local topological real SD ratio:
  `1.88662303`.
- Raw/paired local maximum event shares:
  `0.301936811` /
  `0.350790981`.
- Raw/paired local maximum leave-one-out shifts:
  `0.800443357` /
  `0.834736426`.

## Interpretation

This sample was already exposed during estimator development. A passing
variance result can authorize a genuinely new blind pilot, but cannot be
promoted to a numerical ultraviolet coefficient. A failed result rejects
this estimator without post-hoc multiplier tuning.

## Claim boundary

The calculation concerns only the crossed-`hhh` A00 contribution. It does
not close the other cut classes, a canonical UV coefficient, local GR, the
galaxy branch, or full MTS.

## Evidence

- Manifest: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\functional_rg\5227\frozen_bounded_paired_partition_manifest.json`
- Protocol lock: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\functional_rg\5227\frozen_bounded_paired_partition_protocol_lock.json`
- Topology reuse: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\functional_rg\5227\topology_reuse_audit.json`
- Event rows: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\functional_rg\5227\bounded_paired_partition_A00_event_rows.csv`
- Result: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\functional_rg\5227\bounded_paired_partition_A00_results.json`
- Validation: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_BRR545_5227_VALIDATION.csv`
