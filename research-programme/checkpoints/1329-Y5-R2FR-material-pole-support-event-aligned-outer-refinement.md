# 5313 — Material-pole support events and outer refinement

## Result

The 5312 outer failure is traced to panel `9`, not to the inner energy
quadrature.  The `MC04_SM_DM` material branch `direct:shared:s13` enters and
leaves contract `29` over a narrow soft-angle interval.  Those two support
events are derived by geometric pole scans and bisection before outer
quadrature; they are not fitted from the final integral values.

- support entry: `0.398477172386`;
- support exit: `0.42816813973`;
- maximum event bracket width: `1.48120824273e-07`;
- event-aligned initial panels: `3`;
- final adaptive leaves: `14`;
- completed inner-node shards: `150`;
- maximum leaf Q2/Q4 change:
  `inf`;
- second-order Laurent preflight nodes:
  `3`;
- maximum double-Laurent fit residual:
  `1.17083455269e-07`;
- maximum `R2` scale change:
  `0.00024115143567`;
- panel-nine summed error budget:
  `inf`;
- reassembled `E0025` fixed-decay integral:
  `0`
  `+0 i`.

The failed in-support nodes are not repaired by loosening a simple-pole
threshold.  A derived `R2/(E-p)^2 + R1/(E-p)` model reduces their residuals
by roughly three orders of magnitude and supplies the exact primitive
`-R2/(E-p)+R1 log(E-p)`.  The next runner must apply that subtraction inside
the support and in a controlled one-sided collar at the entry/exit events.

Decision: **SHARED_BRANCH_SECOND_ORDER_LAURENT_TERM_DERIVED__BUILD_DOUBLE_POLE_AND_ENDPOINT_COLLAR_SUBTRACTION**.

Validation: **PASS**.

## Claim boundary

Even a passing result is one regulator at one fixed absolute decay angle.
It does not establish the five-regulator zero limit, decay-angle integration,
a full phase-space coefficient, a UV prediction, local GR, or full MTS.
