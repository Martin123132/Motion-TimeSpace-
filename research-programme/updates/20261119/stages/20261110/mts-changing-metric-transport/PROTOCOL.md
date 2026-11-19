# Changing-metric transport: fixed contract

2026-11-10. Continue the completed background-derivative stage. Reuse its
z=10 interval s=ln(a/a_center) in[0,.001],399modes per model and original
seven source knots. No new mass, coupling, population, branch fit or data.

First enclose the retained homogeneous ODE with an explicit local Picard
box about its saved initial state. Use outward-rounded rational interval
arithmetic, not maxima sampled at33points. Bound H,H',H'',H''' and the
previous91-term W2 residual over that whole box. The resulting certificate
is conditional on the stored initial values, original background interpolant
and retained matched-dust branch; it excludes initial-data and model error.
The old constant-H enclosure is not an input to the new bound.

Use source-derived W2 and W2' with distinct Phi/Psi. Keep the full
counter-rotating canonical forcing integral. Source interpolation is a
not-a-knot cubic through the seven original knots; a separately labelled
five-knot control uses indices[0,1,3,5,6]. Both are supplied-history probes,
not an independently predicted metric. Never differentiate raw float32
values to supply a physical background derivative.

Heavy numerical controls:2048,4096,8192panels,16Gauss nodes, eight panels
per batch. Preserve the same canonical initial data and both explicitly
prepared carrier quadratures. Check background/phase interpolation and
source interpolation separately. Direct field controls at k=.03,.1,1,5,
two quadratures, DOP853 rtol2e-11/2e-12, atol1/100 on declared fixed scales.
Run the first mode as a bounded timing/control batch before the remaining
three; retain all declared modes. Numerical gate2e-5, algebra gate1e-10.

Cold control follows its physical Euler/density equations with its own
changing H,Phi,Psi. No diagnostic WKB mass enters the cold matter law.
Compare endpoint density/current with each retained native chart, and report
pressure discrepancies on a declared energy-block scale separately from
relative pressure errors. Explicitly distinguish microscopic phase ensemble
from time averaging and inherited averaged background from a derived state.

Separate implementation controls from agreement with the retained native
closure. A native discrepancy is scientific evidence to preserve, not a
reason to loosen a gate or drop a mode. Preserve outputs before declaring
such a discrepancy. Do not call it a failed numerical implementation if its
independent field and baseline controls pass.

Each worker is one numerical thread on CPU4, below-normal, bounded900seconds.
Four-hour maximum check-in; do not restart an unobserved but live process.
One worker at a time. No native rebuild, GitHub, browser, Galaxy Lab edits,
new timers, or other-agent process changes. Exclusive outputs and receipts.
