# Second source cell completed; first two cells accumulated

Completed locally on2026-11-09. Scope: the original balanced-wave family, baseline and MTS, both saved GR and Poisson-spatial output branches,10 terminal channels each. This is an extension of the prepared original calculation, not a new theory, fit or physical bank. The previous sealed first-cell result is preserved.

## Main result

| Quantity | MTS | Baseline |
|---|---:|---:|
| Second-cell numerical cases passing |20/20|0/20|
| Two-cell cumulative numerical cases passing |20/20|0/20|
| Largest second-cell contribution/reference |2.770641364909232e-7|5.044223486751953e-14|
| Largest two-cell contribution/reference |5.404543328375052e-7|1.0212775272936754e-13|
| Largest two-cell conditional Cauchy budget/reference |5.407050720235631e-7|1.0304774512690233e-13|
| Largest sum of measured absolute quadrature changes/reference |2.116629271436885e-13|2.2394006346320987e-17|

The MTS contribution is about0.277064ppm from this cell and0.540454ppm cumulatively, on the saved comparison normalization. Those are contributions from the isolated background-generator source, not observational fit improvements. First-cell and second-cell signed contributions add using the same final-epoch adjoint. The sum retains independent error terms and cannot hide a failed cell by cancellation. DERIVATION.md gives the adjoint identity and conditional inequality.

## What was actually continued

- Original source indices4 to8, using intermediate index6 for comparison. Four carried histories: fine/coarse for both models. Each inherits its OWN complete phase and five-channel endpoint bitwise. No late-state reset, changed normalization or replacement of the coarse state with the fine state.
- MTS e-fold domain[-8.358284040677821,-8.348285951253436]; baseline[-8.354944155828964,-8.341414745260776]. Each follows its own original physical history.
-513 source points per model, with the shared left endpoint reused.1024 new paired-model source points,1026 phase controls. Both source vectors and the shared phase measure match the preceding cell bitwise.
- The same accepted integration spacing sets each new panel from its solved phase span, before source sampling. Eight distributed checks, including both original index8 endpoint maps, qualified before four sequential bulk batches.
- Original action/bank, physical grids, G192 hierarchy,256-angle primitive, numerical gate2e-5, algebra gate1e-10 and DOP853 rtol2e-12/atol2e-14 remain unchanged.

## Accuracy and independent verification

MTS worst second-cell source-relative quadrature change3.295011904194638e-6 and conditional-budget change3.252062404688275e-6 are both below2e-5. Current/source-phase/cross-term, adjoint interpolation/time-step and clock-measure controls also pass. The largest phase-source control is1.8355562746829127e-7; current control5.8870474097405844e-15; adjoint interpolation5.020497566451021e-11. Integration volume relative error2.822760932887026e-12.

The baseline has a very small nonzero source, but its worst source-relative quadrature and budget changes remain0.026990582696650767 and0.021521336782763363. Its0/20 flags are preserved on the same rules as MTS. The earlier conditioning diagnosis remains relevant; tiny physical size is not silently converted into a numerical pass.

audit/result.json independently verifies inherited endpoints, immutable inputs, both complete panels, source/map identities, native difference sign, source-phase/current cross controls, terminal-adjoint contractions, integration, cumulative arithmetic and pass flags. Maximum map residuals are6.050823271044862e-16 and6.073596404675282e-16; adjoint contractions reproduce exactly. Primitive refinement<=2.9147692043038457e-13 and closure<=2.0718565748307572e-13. It checks40 cell and40 cumulative output cases and compiles all stage Python sources without bytecode caches.

The saved MTS phase polynomial has a positive derivative throughout this cell:2824.828226171616 to2875.8185428291054, established with exact rational Bernstein bounds on the stored polynomials. This is not a certificate for the continuum ODE. Cauchy budgets are numerically evaluated conditional expressions; bridge/output-map/other residual terms remain separate in the existing full identity.

## Evidence and operation

- balanced/history-01/result.json: four inherited histories and original-node comparisons.
- balanced/grid-01/result.json and balanced/probe-verification/result.json: frozen spacing, boundary reuse and probes.
- balanced/points-01/cell02-result.json: complete paired source panel.
- balanced/projection-cell02/result.json: per-cell outputs and all separate controls.
- balanced/accumulation-01/result.json: first-plus-second-cell signed contributions and conservative control sums.
- audit/result.json: accepted verification. closeout.json and CLEANUP.json contain artifact hashes and exact terminal worker receipts after sealing.

All12 numerical workers exit normally; each uses one numerical thread on CPU4 at below-normal priority. No subagents, new compiler, temporary application, GitHub operation or other-chat process intervention. Existing source files are not edited after being hash-recorded. The accepted projection wrapper is project_cell_v2.py; its only extra change is correcting the copied first-cell metadata label. ADAPTER.md documents the retained unused predecessors.

All five steps of PLAN.md are completed. Next: extend to original source index12 using the saved endpoint at8, retaining both control histories and accumulating against the same terminal adjoint. Do not refine this accepted second MTS cell automatically.
