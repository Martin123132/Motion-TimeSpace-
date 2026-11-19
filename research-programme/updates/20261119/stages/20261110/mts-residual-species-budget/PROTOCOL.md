# Remaining species budget: frozen saved-trajectory calculation

Previous goal turn: verified progress. The derived leading radiation source
correction was applied and passed the independent sampled metric gate. Start
from its seal 0a86b2f000bc55519d823f60034a8a204d81117184468cab04f689398e670197.
No worker is outstanding. Safe check-in before 15:14 UTC, 2026-11-10.

Reuse all four completed original/corrected fine trajectories and their nine
probe times. Do not evolve again or change the action, background, G, physical
inputs, radiation bank, grids or tolerances. Build a source-by-source budget
with synchronous and Newtonian decompositions, keeping common gauge/metric
derivative defects separate from individual species defects. Diagnose rather
than assume that the remaining total error is still radiation dominated.

Derive the budget identities algebraically and compare measured native RHS
terms, including baryon pressure and equal-and-opposite Thomson momentum
exchange. Compare identical diagnostics for cold, native heavy, D0 and D01.
Keep both 16/32 derivative stencils. If a native approximation explains an
error, test its analytic prediction and a zero-term ablation; do not tune it
to the observed residual or quietly modify the saved trajectories.

One numerical worker/thread, CPU4 below-normal, -B, 900sec deadline and owner
holds. No new library build, subagent, GitHub action, Galaxy edits, relay,
timer, background server or unrelated process intervention.
