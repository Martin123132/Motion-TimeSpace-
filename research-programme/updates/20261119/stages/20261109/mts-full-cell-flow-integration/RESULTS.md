# Full-cell continuation: verified first coverage and complete-source test

## Outcome
The first40consecutive MTS background segments are complete. Including the three already verified later panels gives **43of158segments**, covering **26.45977158770772%** of the original third source cell's N-length. This is795verified source nodes:132inherited and663new. The remaining115segments require1955of the already-frozen nodes.

The identified heavy-flow contribution passes the unchanged comparison on every completed segment. More importantly, the saved packets also let us check the **entire10-output coupled source** without another native calculation. On the completed MTS domain, all20branch/output comparisons pass the original2e-5protocol. The full cell is still unfinished, so the old complete-cell source has not been replaced.

## Bounded execution
- Turn starts2026-11-09 16:53UTC; cutoff20:45UTC.
- All158segments and2750nodes were frozen before new evaluation; four inherited33node panels retained, new segments nested9/17nodes.
- One new17node segment was independently qualified before production.
- Batches00..04 each cover eight consecutive segments and pass their numerical screen.
- The campaign stops normally at19:31:28UTC in state safe-check-in-boundary, retaining time for independent validation, full-source projection and cleanup.
- One below-normal CPU4 numerical worker/thread at a time. No history reintegration, physical bank/grid/tolerance change, compiler, subagent, GitHub action or interference with other work.
- Outputs are sharded by segment; no single new packet directory needs thousands of files.

## Heavy-flow checks
All43completed segments pass all four branch/channel comparisons under the unchanged gate. Summing the absolute per-segment numerical-control indicators gives:

| Branch | Pi / original budget | delta_massless / original budget |
|---|---:|---:|
| GR |5.586792024428902e-9|7.349279811492088e-9|
| Poisson-spatial |3.4829061905229544e-9|4.359049296603271e-9|

These include quadrature, current, phase, phase/current cross and both adjoint controls. They are numerical refinement indicators, not rigorous continuum enclosures. They cover only the completed union.

Independent checks cover12720scalar-field cases at90-digit arithmetic. Results agree when rounded to binary64; forward versus transpose observable-map differences are<=1.059272396363778e-15. Independent quadrature error is<=2.2108290459872574e-16 relative to the absolute weighted sum.

## Full source, not just two selected outputs
ALL-SOURCE-DERIVATION.md explains why the saved source/control packets support direct dN integration of all ten outputs: Phi,Psi,D,Q,Pi,theta_c,delta_c,delta_b,delta_gamma,delta_massless. No new physics or component deletion is involved. The physical clock and phase history remain; a second phase-coordinate Jacobian is not part of a direct dN integral.

Original acceptance criteria are retained, including refinement of the signed integral and Cauchy scale, current/phase/cross/combined controls, both adjoint comparisons, volume and the discrete Cauchy check. Extra triangle indicators are recorded separately.

| Largest diagnostic on completed MTS domain | Value |
|---|---:|
| Signed-integral quadrature refinement |1.8040459342785281e-6|
| Cauchy-scale refinement |1.5824301708295708e-6|
| Current-history control |7.223977114782823e-15|
| Phase-history control |7.521409333130656e-8|
| Phase/current cross |2.632593963553251e-22|
| Combined current and phase |7.521409369233091e-8|
| Adjoint interpolation |7.927518586471481e-11|
| Adjoint steps |3.680687774695494e-14|

All20comparisons pass2e-5 on this completed, partly disconnected domain. Its largest signed contribution is7.496944791088345e-8 of the existing physical reference scale; its Cauchy scale is7.499138856630102e-8. These are partial source contributions, not full-history totals or observational improvements.

All-source adjoint contractions were independently recomputed for every saved source/control point; maximum normalized discrepancy1.978978956396609e-15. Independent segment quadrature discrepancy<=2.2198386140116518e-16 on the absolute weighted scale.

## Baseline kept equally visible
The same direct full-source procedure reuses the baseline's66saved nodes across both complete baseline segments. Its heavy field is absent, but the full coupled source is not replaced by zero.

Baseline remains0/20strict relative comparisons: largest signed-integral refinement0.03854239926015293 and Cauchy-scale refinement0.16258192921150677. The largest signed contribution is1.3590630188878761e-14 of the physical reference scale; the aggregate triangle indicator is1.2922693724365293e-16. Those small absolute scales do not turn the failed relative tests into passes or establish a physical failure of GR. Independent contraction and quadrature arithmetic still pass (<=1.3175335514196428e-15 and2.068734174983479e-16).

This is a numerical source-consistency comparison, not a model-selection score.

## Provenance and next decision
Read balanced/freeze-01/result.json, balanced/batches/batch00..04-result.json, balanced/screens, completed-audit/result.json and balanced/all-source-projection-01/result.json. All consumed evidence has absolute paths and hashes. The prior selected-segment seal is03eb20dbdac990b6e9061a637f6434f04684ded30ea9865f770d0b669c7f7d59.

ADAPTER-NOTE.md records a pre-execution inherited-index assembly correction. The corrected completed-audit adapter ran successfully; no physical input or tolerance changed. Fifteen numerical workers finish exit0; exact dispatcher/worker cleanup and artifact seal are recorded separately.

Next is batch05, segment ordinals40..47, using this same complete-cell freeze. Finish all158segments before testing/promoting a full-source replacement or updating the three-cell total. The full MTS goal remains active and unmet; this turn produces verified progress toward its coupled-source/GR-limit calculation, not a redefinition of the goal.

