# Selected longer-window test completed — 16 November 2026

Epochs2917..2924 completed for baseline and MTS, finishing the preselected horizon. All25 prior control reports and source cells are preserved;33 reports are now saved. No later evolution was started.

## Frozen-source and evolution checks

- Only11 new baseline and14 new MTS one-sided source cells were constructed. All22+28 fresh sixth/five-sixths probes pass, with numerical predictions frozen before validation capture.
- Original926 native packets are byte-identical; all934 current packets agree between construction and validation captures. Earlier source readouts agree exactly. The retained DLL and physical bank were reused unchanged.
- Full, original-quadratic, independent-difference and nine-term response states were continued separately. Original902 signed preparation nodes, physical grids, parameters, normalizations, original quadratic origin and2e-5/1e-10 tolerances remain fixed. Physical32/64 maximum steps remain those of the original shortest window.
- The original25 reference rows and uncertainty budgets were retained. New native references use902 shifted-time readouts per new report with the original matching anchor; no source or old uncertainty was extrapolated.

## Derived response at the larger horizon

Elapsed durations are0.03945017660593919 (baseline) and0.03944843281006172 (MTS), nearly twice the16-interval horizon selected for this test.

Maximum correction-relative discrepancy INCLUDING numerical working allowance against the separately evolved difference:

| Case/channel | Relative discrepancy | Fixed gate |
|---|---:|---:|
| Baseline density | 1.786515e-15 | 2e-5 |
| MTS density | 3.297820e-8 | 2e-5 |
| MTS current | 1.489650e-7 | 2e-5 |
| MTS pressure | 5.335516e-8 | 2e-5 |

Baseline current and pressure remain zero. All original observable-scale, native-boundary, source and weighted-superposition checks pass. Whole-history maxima retain the earlier pressure working allowance; no earlier error was discarded. This checks the time-dependent, corner-aware integral response, not a fitted power exponent or a new observational fit.

## Recomputed endpoint bounds

All60 forward/adjoint/refinement checks pass at the new endpoint.

| Case/channel | Resolved correction | New envelope | Used |
|---|---:|---:|---:|
| Baseline density | -3.091499495840423e-10 | 1.750649769025407e-9 | 17.6592% |
| MTS density | -2.0255558410387042e-10 | 1.090790537086831e-9 | 18.5696% |
| MTS current | -6.928411827241568e-12 | 4.5971460373966513e-11 | 15.0711% |
| MTS pressure | -1.644977254537612e-10 | 9.864066757553953e-10 | 16.6765% |

These remain numerical working bounds, not certified continuum estimates.

## Restart identity included from the outset

The previously derived E'=A E transport was frozen before this batch. No zero initial mismatch was presumed. The old raw failure remains in the retained prefix; one additional raw zero-seed diagnostic would fail at epoch2919/node796/u. Its known seed predicts9.058733683418862e-20 of the9.320751813668317e-20 raw mismatch. Remaining2.620181302494546e-21 fits the unchanged4.552560105992919e-20 allowance.

All transported identities pass for both cases. Maximum remaining fractions of the original node allowance are10.5170% (baseline) and16.7232% (MTS). No history, coefficient, prediction or threshold was changed after seeing this diagnostic. Prior prefix acceptance uses its sealed reconciled identity and exact state preservation, not a renewed zero-seed assumption.

Authoritative overall result: batch-result.json. result.json retains raw zero-seed diagnostics. No failed worker or new post-check repair was needed in this batch.

## Next

The selected horizon is complete. Stop numerical evolution here, verify cleanup, then conduct the separately requested matter-sector compatibility review. That review cannot change this sealed calculation. No GitHub, relay, subagent or new observational fit. Persistent goal remains paused.
