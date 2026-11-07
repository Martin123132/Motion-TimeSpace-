# Stage222: same-seed incident-history refinement

Frozen before calculation. Reuse Stage221's complete panel and preserve all failures.

- Evolve a new eighth-grid incident history for BOTH heavy and cold backgrounds.
- Use the EXACT same saved initial and previous states used by the half/quarter histories.
- Recompute the whole post-seed candidate interval, not only the final injection interval.
- Keep the original scattering bank untouched; reuse the same smooth local candidate and its already qualified bridge.
- Use 80-digit state evolution with 100-digit first/final-step checks and existing 1e-10 identities.
- Keep existing source/response 1% gates; assess baseline, MTS increment AND cancelling total.
- No refit, new frequency node, new virtual integral, global curve change, or response-grid change.
- Shared native seed error remains common and unbounded; this tests conditional post-seed discretization only.
- Checkpoint every eight updates, two one-thread workers maximum, report within four hours.
- Numerical failures are retained, not normalized away. No GitHub or subagents.

