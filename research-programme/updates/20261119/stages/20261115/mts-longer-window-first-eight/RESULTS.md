# Longer-window first eight-epoch batch — 2026-11-15

## Outcome

Original epochs2909..2916 completed for baseline and MTS. Both pass source, native-reference, endpoint-response and derived-expansion checks, with an explicitly documented correction to the restarted numerical cancellation identity. The17 prior reports and source cells remain unchanged;25 reports are now saved. The second batch2917..2924 has NOT started.

Authoritative overall result: batch-result.json. The original raw state-cancellation failure remains in result.json; read RESTART-DEFECT.md rather than treating that file as overwritten or silently waived.

## Frozen source predictions

Only10 new baseline and15 new MTS one-sided source cells were constructed. Predictions were frozen before all20 baseline and30 MTS fresh sixth/five-sixths probes. All50 probes pass the unchanged2e-5 gate.

Maximum fresh curvature discrepancy relative to the retained scale:
- Baseline D/Q:1.94369e-14 /6.50303e-14.
- MTS D/Q:1.43139e-9 /4.43043e-12.

All918 prior native main packets are byte-identical; all926 current main packets agree between construction and validation captures. Earlier source-history readouts agree exactly. Native owner state was cleared/released after every capture. The DLL was reused unchanged, not rebuilt.

## Evolution and numerical reference

Elapsed durations from the original matching origin:
- Baseline0.02958948359840008.
- MTS0.029588188156409956.

The full, original-quadratic and independently conditioned difference histories continue from2908, retaining original902 signed preparation nodes and both32/64 runs. Maximum physical steps remain the ORIGINAL short-window duration/32 or/64. Physical bank, grids, parameters, normalization and tolerances are unchanged.

Eight new902-shifted-time numerical readouts use the original matching anchor. Prior17 reference rows and budgets are preserved, not extrapolated. Maximum relative residual including numerical working allowance over the NEW eight reports:
- Baseline density2.54391e-10; current/pressure zero.
- MTS density5.08762e-11, current7.08385e-12, pressure3.31195e-10.
The original observable-scale gate remains2e-5. Whole-history maxima retain the previously saved values.

## Derived response expansion

The nine saved terms Y0..Y8 were continued without resetting them. Outputs were frozen before scoring. Maximum relative discrepancy INCLUDING working numerical uncertainty versus the independently evolved correction:
- Baseline density9.86776e-16; current/pressure zero.
- MTS density2.06494e-9, current1.79454e-8, pressure3.16675e-9.
All pass2e-5 on the correction's own amplitude scale. The previous17 series rows are preserved byte-for-byte. No time exponent was fitted.

## New endpoint allowance

All60 forward/adjoint/refinement checks pass for gains recomputed through2916.

| Case/channel | Resolved correction | New absolute envelope | Fraction used |
|---|---:|---:|---:|
| Baseline density | -9.784023888592092e-11 | 5.483432874947581e-10 | 17.8429% |
| MTS density | -6.353854491448408e-11 | 3.304490121928455e-10 | 19.2279% |
| MTS current | -1.7432944398451532e-12 | 1.1120623711457737e-11 | 15.6762% |
| MTS pressure | -5.7596318232761303e-11 | 3.1497602462547667e-10 | 18.2859% |

These are conditional numerical working envelopes, not continuum certificates.

## Restart identity repair, not a relaxed gate

One raw MTS nodewise cancellation entry exceeded its allowance by12.0536%. It assumed three independently stored float states had exactly zero initial mismatch at the restart. The saved mismatch is nonzero and its equation is E'=A E.

Transporting that known seed for every node and both cases predicts the failed entry's error without fitting it. The remaining discrepancy is7.7359e-21 against the SAME7.5560e-20 allowance. All corrected node identities pass; the maximum remaining fraction of the old allowance is10.0642% for baseline and19.4335% for MTS. No source, physical trajectory, prediction or threshold was altered. The raw failure and first gate-blocked scorer are retained.

This accounting repair is an explicit post-check correction, not a pre-registered raw pass. It is distinct from the successfully frozen source predictions and response calculations.

## Next and scope

Proceed only on Martin's next manual instruction with2917..2924, retaining all25 control reports, current source cells and separate state/series restarts. Recompute that endpoint's gains and account for its saved restart defect. No source extrapolation or pure-power replacement.

Everything stays local. No new observational fit, GitHub action, subagent, unrelated process change or next-batch job. The persistent goal remains paused. Validation and CLEANUP-VERIFIED.json record final checks and exact worker exits.
