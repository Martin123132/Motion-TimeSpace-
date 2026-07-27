# 5231 - Local double-residue identity and pooled A00 tail decomposition

## Result

Decision: `ADOPT_LOCAL_DOUBLE_RESIDUE_IDENTITY_AND_DERIVE_OUTER_MOMENTS`.

The safe reciprocal topological correction has been reduced from a repeated
nested-contour diagnosis to a local coefficient identity.  Near one
cross-source collision,

```text
F(zeta,u) = C / [(u-r1(zeta))(u-r2(zeta))] + less-singular,

R_pair = sigma C
         / [zeta_* u_* partial_zeta(r1-r2)|_*].
```

`sigma` is fixed by causal ownership: `+1` when the first labelled pole is
owned and `-1` when the second is owned.  A safe reciprocal pair then
contributes `(w_rep-w_partner) R_rep`.

## Stored identity test

- Stored safe entries audited: `1028`.
- Material entries (`|R| >= 1.0`):
  `492`.
- Median material relative residual:
  `1.22738979e-08`.
- Maximum material relative residual:
  `0.00195933031`.
- Material higher-than-double-pole cases: `0`.

## Pooled reconstruction

- Events: `48` =
  `24` old + `24` fresh.
- Correlation between observed A00 and the safe local-identity reconstruction:
  `0.999999988157`.
- RMS residual: `0.0745277981`.
- Maximum absolute residual:
  `0.494110841`.

The omitted remainder is the pre-existing unsafe additive cross-source family.
It is numerically negligible in the E020/E040 physical A00 extrapolation at
the frozen tolerance, but it is not silently reclassified as safe.

## Tail localization

The two opposite-sign extremes are symmetry-related members of the same
soft-leg collision class:

- Old seed `522115`:
  A00 `-2017.20139`, dominated by
  `direct:g2:plus/direct:g3:minus` at
  `-2070.5409`.
- Fresh seed `731942010`:
  A00 `2073.33142`, dominated by
  `direct:g1:plus/direct:g3:minus` at
  `1760.47838`.

This replaces the vague statement that the sample is merely “heavy-tailed.”
The tail is carried by explicit local double-residue families.  Its moment
existence is controlled by the outer-event scaling of
`C/[zeta_* u_* partial_zeta(r1-r2)]` and by the winding-activation regions.

## Consequence

Median-of-means is not frozen yet.  A finite-variance theorem cannot be
assumed before the outer zero-set codimension and pole order are derived.
The next checkpoint must derive those scalings for the leading families and
decide whether the ordinary mean, a principal-value construction, or a
different finite observable is mathematically licensed.

## Claim boundary

This checkpoint is an exact reduction and numerical cross-check of the A00
topological tail.  It does not establish a numerical ultraviolet coefficient,
local GR, the galaxy branch, or full MTS.

## Evidence

- Event decomposition: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\functional_rg\5231\pooled_A00_tail_event_decomposition.csv`
- Family decomposition: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\functional_rg\5231\pooled_A00_tail_family_decomposition.csv`
- Stored identity audit: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\functional_rg\5231\stored_safe_pair_identity_audit.csv`
- Result: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\functional_rg\5231\local_double_residue_tail_decomposition.json`
- Validation: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_BRR545_5231_VALIDATION.csv`
