# Frozen live test of the derived boundary-adapted source state

Previous turn: verified progress, completing the coupled memory budget and deriving an invertible source map. This stage actually evolves that map, retaining all physical modes and source corrections.

Use the original65 times2892..2956, native captures, projected-source reconstructed endpoint, library, mass/background/normalization, physical bank and2e-5/1e-10 tolerances. Baseline remains actual CDM plus its retained slow scalar. MTS replaces four constrained heavy phase entries with two WD/WQ coordinates; the slow phase and every other active native species/cache remain live. Both captured and reconstructed starts are tested. Do not activate the old averaged selector or drop the derived history tails.

The existing C API has no explicit H'/z' output. Use the permitted local derivative fallback without a rebuild: at the CURRENT phase state, evaluate the existing native RHS/readout at nearby times, holding that current state fixed. Take a five-point derivative of H,z, subtracting the central value before differencing. Add z(t,phase_rhs) to the partial-time z derivative; z is linear in the phase/rest state, so this is its exact state-direction term. H is background-only. No saved future metric or species history enters the evolved RHS.

Freeze time offsets of window_duration/4096 and /8192, centered interior and one-sided near the owner boundaries. Preflight both against the earlier independent source-history derivative control and against local directional differentiation of the actual coordinate map. The directional coordinate test covers the TWO changed heavy coordinates; baseline covers its CDM density. Unchanged rest coordinates use their direct native derivatives and are tested by full evolution, not unnecessary finite-difference subtraction on tiny unrelated components. Their identity mapping is exact by construction.

For each start run step128-h1, step256-h1, step256-h2, with DOP853 rtol1e-10/scaledatol1e-12. Scaling uses initial state/RHS only. Keep all step and derivative refinements separate. Compare state, native observables/derivatives, source coordinates, physical phase and active caches. All comparisons use original gates, and failures stay visible. The source-coordinate RHS is evaluated both by product differentiation and the independently derived tail expression.

Explicit controls: exact zero/sign behavior, rest-to-metric feedback, heavy-to-metric feedback, source-map inverse, and regularity condition. A future state-space reduction or late-background match requires additional physical work; this exact coordinate change does not silently authorize one.

One worker/thread, CPU4 below-normal,900s guard and four-hour check-in. No native build, subagent, new browser/relay/timer, download, Galaxy edit or GitHub. Record exact process and native owner cleanup.
