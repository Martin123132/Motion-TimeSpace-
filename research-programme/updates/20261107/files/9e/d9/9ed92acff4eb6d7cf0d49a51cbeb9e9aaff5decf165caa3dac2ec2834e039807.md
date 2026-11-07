# Stage139: corrected source evolution through forty-eight original intervals

Private/local. Stage138 is preserved;both backgrounds now carry the corrected solution continuously through global step30720.

## Larger continuous extension

Each background advances5120 additional steps from the corrected25600 restart with both BDF and outer time levels. The accepted trajectory is never reset to the original history. Baseline and both MTS columns are evolved together.
The original5265 frequency grid,40960 global inner spacing,2048 response steps,physical boundary prescription and external driver are unchanged. One hundred twenty-eight new hashed restarts retain both time levels.
The new257-knot coefficient bank evaluates248missing physical temperatures and reuses9original coarse endpoints. Both backgrounds share the verified thermal parameter. No normalization or physical coefficient is fitted.
The entire-band finite-principal-grid symbol bound remains <= -1.44594843e-05. It has an analytic between-sample remainder and a conservative floating allowance,not a formal interval-arithmetic certificate.

- heavy: weighted norm-budget residual1.48478911e-13;total-field boundary equation residual2.81894883e-16;257new-block saved sites.
- cold: weighted norm-budget residual1.41644067e-13;total-field boundary equation residual3.30336965e-16;257new-block saved sites.

The norm budget is numerical stability accounting,not physical radiation-energy conservation. The inherited control/restart tests remain evidence;no new original-law trajectory is relabelled as a control.

## Full new-block source comparison

Stage133 unit-shift source matrices are reused exactly. Independent physical-event sources are evaluated at every257new-block knot in BOTH matching windows,not just at endpoints. Seventeen direct common-kernel checks per window also test the cache independently.
Maximum common-versus-physical weak relative error: 1.82003495e-06.
The continuous prefix has1537dense source sites over forty-eight original intervals (forty-nine of65original coarse saved epochs). Later forcing is restored at30740 for this bounded feedback comparison. The corrected30720 state remains saved for continuous extension.

## Gas-response changes

Fractions refer to the small saved gas correction,not total gas temperature. Extension increments and common/physical source differences are propagated separately to avoid relying on subtraction of nearly equal responses.

| Background/window | Extension endpoint fraction: baseline, MTS1, MTS2 | Source-discretization endpoint fraction: baseline, MTS1, MTS2 |
|---|---|---|
| feedback-heavy-m20 | 0.00656800736, 1.71977706e-05, 1.71969661e-05 | 2.18587449e-05, 7.14147705e-05, 7.14114608e-05 |
| feedback-heavy-m40 | 0.00847461759, 0.000120465913, 0.000120457277 | 1.92048777e-05, 0.00012175926, 0.000121750623 |
| feedback-cold-m20 | 0.0066076107, 1.69870564e-05, 1.69862602e-05 | 2.19306792e-05, 7.15043454e-05, 7.15010186e-05 |
| feedback-cold-m40 | 0.00851753255, 0.000124690535, 0.000124681375 | 1.9239924e-05, 0.00012232418, 0.000122315441 |

## New-block source discrepancy

The newest contribution is small enough to require separating its own source discrepancy from errors accumulated over earlier intervals. The unchanged response solver propagates (C-P)-(C0-P0),where previous sources are expanded onto the same grid. This forcing vanishes outside the new sites and outside the Compton component.
The table gives the measured source-discrepancy contribution as a PERCENT of this block's independently propagated gas addition,not as a percent of the total correction. It does not bound all numerical or physical error. See BLOCK-SOURCE-ERROR.md.

| Background/window | Percent of block addition: baseline, MTS1, MTS2 |
|---|---|
| heavy-m20 | 0.00398141122, 0.0168816907, 0.0168817021 |
| heavy-m40 | 0.0024307184, 0.00276752662, 0.00276752562 |
| cold-m20 | 0.00398562534, 0.01699281, 0.0169928118 |
| cold-m40 | 0.00243598391, 0.00263569049, 0.00263569274 |

Stage133 attributed its earlier large MTS change predominantly to source reconstruction. This extension does not assume that earlier attribution quantitatively applies to all new intervals. Large sensitivity flags must remain visible.

## Retained diagnostics

5084scientific checks:5075pass,9retained failures. No thresholds changed.
- feedback-heavy-m20: Response:physical:gas; Response:cubic:gas
- feedback-heavy-m40: Response:physical:gas; Response:cubic:gas
- feedback-cold-m20: Response:physical:gas; Response:cubic:gas; Response:continuation:gas
- feedback-cold-m40: Response:physical:gas; Response:cubic:gas

All prior failed checks remain sealed separately. No parent output is overwritten. Coverage refers to the saved time-coordinate span,not necessarily elapsed physical time or response weight.

## Next

Continue the same corrected two-level trajectory from30720 to35840 in another eight-interval resumable block,using the verified cached common source and independent physical-event comparisons. Track cumulative gas/radiation response and source-error budget before interpreting a full-history physical amplitude.

This is a numerical extension of the existing framework,not an observational preference or completion of the remaining thermal history.
