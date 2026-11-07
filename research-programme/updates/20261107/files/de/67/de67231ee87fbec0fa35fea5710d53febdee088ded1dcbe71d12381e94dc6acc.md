# Stage135: extend the source test through one quarter of the saved history

Started 14 October 2026, 15:41:08 UTC. Private/local; Stage134 sealed and immutable.
- Continue the accepted corrected two-level state from 5120 to 10240 for both
  backgrounds, baseline and both MTS columns together. No trajectory reset.
- Keep 5265 frequency nodes, 40960 global inner steps and 2048 response steps.
  Keep the physical ghost prescription, clock, DC/BR inputs and external history.
- Derive cubic coefficients at all 257 new-block source sites; reuse nine
  original endpoint event sets and evaluate 248 missing physical temperatures.
- Independently evaluate physical-event weak sources at every new site in both
  matching windows; retain the Stage133 exact unit-shift cache for common sources.
- Save both BDF and outer levels every 80 steps. No more than one below-normal
  CPU2 worker, with BLAS/OMP/MKL threads set to one. No subagents or GitHub.
- Join all four corrected blocks without duplicate endpoints: 513 dense sites,
  16 original intervals, 17 of the 65 original saved epochs.
- Recompute the final radiation/gas response with 2048 steps unchanged.
  Preserve the earlier source prefix bitwise; restore inherited later forcing
  at step10260 for this bounded comparison, not the corrected inner endpoint.
- Propagate source-discretization and extension increments independently.
  Retain existing sensitivity and numerical residual diagnostics without
  relaxing thresholds. A percentage of a small correction is not total gas energy.
- Verify parent/consumed hashes, all restart and weak-source records, finite
  arrays, exact source differences and protected-workbench modification count.
- Only this child and the two resume heads may change; no sealed-parent edits.

Safe-work deadline 19:20 UTC; report by 19:41 UTC, even if work remains.
An incomplete source bank remains resumable and is not sealed as complete.
