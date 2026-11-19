# Third source interval carried through; two integration flags localized

Completed locally on2026-11-09. This extends the retained balanced-family calculation from original source8 to12, with both baseline and MTS, the existing GR/Poisson-spatial branches and10 terminal output channels. Original preparation, physics, bank, physical grids and tolerances are unchanged. The previous sealed stages are retained.

## Measured result

| Quantity | MTS | Baseline |
|---|---:|---:|
| Third-cell numerical cases passing |18/20|0/20|
| Three-cell cumulative cases passing |18/20|0/20|
| Largest third-cell contribution/reference |2.903823403934019e-7|1.335712582227464e-14|
| Largest three-cell contribution/reference |8.308366732309069e-7|1.1544294451714895e-13|
| Largest cumulative conditional Cauchy budget/reference |8.312254336148809e-7|1.2138286027541308e-13|
| Largest cumulative sum of measured absolute quadrature changes/reference |3.3697377568345453e-13|6.664391369695005e-17|

The largest accumulated MTS contribution is about0.830837ppm on the existing terminal comparison normalization. This is the isolated background-generator source contribution, not a fit score. The two failing cell flags are retained in the cumulative result; no cancellation-based promotion. The first two MTS cells remain20/20 independently.

## What the remaining two flags actually are

Both occur in the GR output branch: Pi and delta_massless. Their source-relative signed quadrature changes are2.6434527265082145e-5 and2.946886806024891e-5, above the unchanged2e-5 gate. Their conditional-budget changes are8.487937155010104e-5 and8.571153770071806e-5. All current, source-phase, cross-term, adjoint and clock-measure controls pass. The largest source-phase control is2.0638876557717252e-7, current8.099968359783855e-15, adjoint interpolation6.409200027258359e-11.

The saved129/257/513-point MTS results show shrinking changes, not a claim of convergence:

| GR channel | Latest/previous signed change | Latest/previous budget change | Physical signed change/reference |
|---|---:|---:|---:|
|Pi|0.2496242885918107|0.629986068593544|1.2531084853976604e-13|
|delta_massless|0.2557491800211604|0.6750387506759754|1.1976382393137867e-13|

The diagnosis decomposes refinement differences over the saved panels without a new physical evaluation.90 of128 panels carry90% of the absolute signed difference in either channel;75/78 panels carry90% of the second-moment difference. This is distributed integration uncertainty, not evidence for repairing one isolated bad node. Panel sums reproduce the global signed/second-moment differences within1.634e-15/1.069e-15 relative to the relevant numerical budgets. Baseline is tested by the same decomposition, with identities within2.775e-15. These ratios do not justify extrapolating an assumed formal convergence order or promising the next grid will pass.

Decision: one paired source-quadrature refinement of this cell, retaining every old point, before advancing to source16. No new native calculation was launched by this diagnostic.

## Continuity and preserved physics

The accepted four histories inherit their OWN parent endpoints without a reset. Incoming-state/reference agreement is<=3.380e-15; saved-current agreement over the cell<=4.229e-15. Source sampling is513 MTS points and509 baseline points, determined independently by the inherited no-coarser phase/N spacing. There are1020 new source points and2 reused boundaries, with1022 phase controls. Baseline/MTS may have different node counts because their original physical phase/time histories differ; the sampling rule and accuracy gates are the same.

MTS N domain[-8.348285951253436,-8.33846283728409]; baseline[-8.341414745260776,-8.328010779574203]. Both shared source vectors and phase measures are bitwise inherited. The same original terminal adjoints and reference scales are used. Signed contributions add to the TWO-CELL cumulative result exactly once; already accumulated absolute control changes and all three cell flags are preserved. The adjoint additivity proof and conditional Cauchy inequality are retained in the sealed second-cell DERIVATION.md.

The256-angle primitive, G192 hierarchy, physical source bank, ALGEBRA1e-10/GATE2e-5 and DOP853 rtol2e-12/atol2e-14 are unchanged. Native source mapping residuals are<=6.467e-16, phase-frame<=5.689e-16; adjoint contractions reproduce exactly. Primitive refinement<=4.363e-13, closure<=2.878e-13. Stored-polynomial MTS phase derivative bounds are positive2875.7857044533935..2926.5206949249477; physical-clock versus stored-polynomial derivative differences stay<=8.029e-13. The polynomial certificate and numerically evaluated conditional budgets retain their earlier scope.

The baseline source remains small and nonzero. Its worst relative quadrature/budget changes are0.025954619350181386/0.010432310050450845. The0/20 relative-accuracy flags remain visible rather than being excused by small physical size.

## Repaired implementation failure

The first history attempt stopped before any numerical history packet was accepted because one leading-reference slice still selected the previous cell. REFERENCE-REPAIR.md preserves that failed script, freeze, identity and exit1. The accepted continue_current_v2.py uses one epoch_slice for every reference component and checks incoming agreement BEFORE integration. The measured stale leading mismatches were0.15985(MTS) and0.29229(baseline), versus correct incoming errors around1.8e-15 to3.4e-15. The RHS and tolerances were not changed. Only the rejected unsaved history solve was repeated from the verified parent.

## Verification and files

audit/result.json passes the independent artifact/equation-consistency audit:4 history controls,1020 new points,2 reused boundary points,1022 phase controls,40 cell outputs and40 cumulative outputs. It directly verifies that every stored reference component belongs to the same original physical epochs, preserves the failed attempt, recompiles stage Python without bytecode caches, and checks exact worker identities. Audit success does not turn the18/20 numerical result into20/20.

- Accepted history: balanced/history-02/result.json.
- Frozen grid/probes: balanced/grid-01/result.json and balanced/probe-verification/result.json.
- Source/projection: balanced/points-01/cell03-result.json and balanced/projection-cell03/result.json.
- Accumulation: balanced/accumulation-01/result.json.
- Saved-only diagnosis: balanced/quadrature-diagnosis-01/result.json and model panel-difference packets.
- Accepted auditor: audit_third_cell_v3.py. Accepted final sealer: seal_stage_v2.ps1, which additionally checks the diagnosis inputs and includes its decision.
- Final immutable inventory and process receipts: closeout.json and CLEANUP.json.

All14 task-owned numerical attempts are terminal:13 exit0 and the preserved rejected reference check exit1. One numerical worker/thread at a time, below-normal CPU4. No GitHub, subagents, compiler, application launch or intervention in another chat. PLAN.md steps are complete; measured integration flags determine the next step in NEXT.md. Goal remains active and unmet.
