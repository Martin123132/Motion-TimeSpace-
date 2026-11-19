# Completed frozen third-cell source and three-cell accumulation

Date: 2026-11-10. Private numerical checkpoint; no publishing.

## What finished

The originally frozen third source cell, saved indices 8--12, is complete: 158/158 MTS dense-output segments and 2750/2750 nodes. The completion reused the inherited segment catalogues and the deliberately paused worker; no completed node was restarted. Independent audit covers 44,000 scalar contractions, with exact agreement after rounding to the production binary representation. The independent forward-map discrepancy is 1.059272396363778e-15 and the integrated absolute-scale discrepancy is 2.219234912718689e-16.

The full source includes the derived dense-output flow-defect coupling. It was not discarded or replaced by an evolution-equation derivative. Integration uses direct dN and exact moments on the frozen segments. The original physical bank, histories, physical grids, arithmetic and acceptance thresholds remain unchanged: algebra 1e-10, numerical comparison 2e-5.

## Matched-model outcome

Each full-source comparison contains two metric branches and ten output channels. These are numerical accuracy checks, not observational fit scores.

| Check | MTS heavy branch | Cold baseline |
|---|---:|---:|
| Complete third-cell source | 20/20 | 0/20 |
| Independent flow/nonflow reconstruction, four sensitive outputs | 4/4 | 0/4 |
| Accumulated first three source cells | 20/20 | 0/20 |
| Individual-cell pass counts in accumulation | 20, 20, 20 | 0, 0, 0 |

The old retained three-cell MTS comparison had 16/20 passing outputs. The new 20/20 result comes from completing the frozen segment-aligned integration, not relaxing a threshold. Full third-cell MTS source magnitude is at most 2.903823473765343e-7 of the retained channel reference; baseline is at most 1.3590630188878761e-14.

For the independent reconstruction, the identity tested was:

Q_new(S) - [Q_old(S-F) + Q_new(F)] = Q_new(S-F) - Q_old(S-F).

The maximum MTS difference/original budget is 1.7566491471670867e-6, below 2e-5. For cold it is 0.07773841345366103, above the unchanged gate. Expressed relative to the physical channel reference, the corresponding maximum differences are 8.327579370095838e-15 and 2.862210040978517e-16. Thus the cold flags concern a very small correction with an especially small normalization; they do not establish a failure of GR or a physical advantage for MTS.

## Accumulated contribution

Authoritative result: balanced/accumulation-03/result.json and its two referenced NPZ packets. Start from the sealed TWO-cell total and add this third cell exactly once. Shared source, phase, physical-state and measure endpoints and terminal-adjoint reference scales were checked.

All following values are dimensionless fractions of each retained channel reference, with maxima taken across channels; maxima need not occur in the same channel.

| Three-cell quantity | MTS heavy branch | Cold baseline |
|---|---:|---:|
| Maximum absolute signed contribution/reference | 8.308366802140394e-7 | 1.156826671203949e-13 |
| Maximum triangle budget/reference | 8.312254409100439e-7 | 1.2163252927174022e-13 |
| Maximum summed quadrature-change indicator/reference | 2.2289414800984588e-13 | 3.730512349279596e-17 |
| Maximum change from the prior three-cell result/reference | 6.312838678229057e-14 | 2.862210040978542e-16 |

These are finite-resolution comparisons and conditional triangle budgets for the balanced family and the first three source cells. A quadrature-change indicator is not a rigorous continuum error bound. This is not an entire-history qualification.

All inherited current, phase, mixed, adjoint interpolation and adjoint-step controls are retained, using sums of absolute cell changes so cancellations cannot hide a failed cell. Earlier clock-measure controls are carried unchanged. The new third-cell calculation has no approximate phase-to-N Jacobian, so that particular measure control is inapplicable; physical phase and current effects remain present.

## Diagnosed implementation failures, preserved rather than hidden

1. accumulate-01 exited 1 in its independent addition checker, before publishing model packets. A 90-digit decimal intermediate can double-round an exact binary midpoint. The production binary64 additions were correct. The independent exact-rational audit checked 720 scalar pairs with zero disagreements; all 35 decimal-oracle discrepancies were diagnosed as adjacent-float midpoint cases. Only the checker was corrected.
2. accumulate-02 exited 1 before publishing model packets because retained metadata names the second branch poisson-spatial while direct projection names it poisson. The versioned third script uses an explicit mapping, checks the branch ordering, and checks the mapped pass flag and signed source against the unchanged arrays.
3. accumulate-03 exits 0. Failed attempts, their empty output directories, scripts and logs are retained. No failed calculation is relabelled as a success. See ADDITION-ORACLE-REPAIR.md and ACCUMULATION-BRANCH-LABEL-ADAPTER.md.

## Execution and evidence

The original supervisor completed batches17--18 after the owner-authorized in-place resume. Its conservative forecast counted the intentional pause as compute time and stopped safely. A separately recorded continuation ran only previously unattempted batch19 within the original 05:35 UTC cutoff. No duplicated batch18 and no extra research direction.

Primary evidence:
- completed-audit/result.json: complete frozen coverage and independent contractions.
- balanced/all-source-projection-01/result.json: full-source baseline/MTS comparisons.
- balanced/component-comparison-01/result.json: reconstruction identity.
- balanced/addition-oracle-01/result.json: exact addition audit.
- balanced/accumulation-03/result.json: authoritative three-cell total.
- ACCUMULATION-DERIVATION.md: measure, additive response and control accounting.
- CLEANUP.json and closeout.json, generated by seal_complete_stage.ps1: terminal receipts, immutable input checks and final artifact hashes.

The seal verifies sixteen numerical worker receipts: fourteen exit0 and two explicitly diagnosed exit1. The resume receipt is process control, not a numerical attempt. No unrelated processes, user applications, bank files or GitHub state are changed.
