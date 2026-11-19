# Source-complete leading radiation approximation: frozen comparison

Continue from b637369aae96427cca2f2911fe152e97db3a2cac3619b78519bf64276d0e841b.
Previous goal turn made verified progress: derived live preparation and
identified a failed physical gate, not merely a missing-input list.
No outstanding worker. Keep the retained action, G, background, source
bank, physical grids, k=5/Mpc, z=10 short window and 2e-5 gate.

Implement the derived missing-scalar-density/pressure correction in a
separate native-source port. Four externally supplied radiation increments
are inserted before radiation stress is added, so the native metric,
other-species RHS and baryon drag all receive the SAME corrected sources.
With the port disabled the copied library must reproduce the original
capture/RHS/observer; no original source, object or DLL is overwritten.

The increments come from the existing action stress and leading RSA trace
equation, not fitting the measured defect. Include slow and heavy scalar
stress, pressure and photon opacity. For the canonical heavy state derive
the pressure gauge transformation and solve the resulting linear metric
feedback, rather than holding metric-dependent pressure fixed.

Test original/corrected native heavy and cold controls and canonical
MTS. Derive the canonical initial forced response with the new operator.
Use independent differentiated metric/energy diagnostics, not the native
observer's momentum-law expression. Keep the finite-time/source-order
limitations of RSA explicit; a passing short-window test is not a complete
radiation hierarchy or broad cosmological validation. Preserve failures.

One numerical worker/thread, CPU4 below-normal, -B,900sec per worker.
Compiler children tracked individually; temporary mappings removed only
if still owned. Safe check-in before14:38UTC. No GitHub, Galaxy edits,
subagents, browser, relay/timers or other-worker actions.
