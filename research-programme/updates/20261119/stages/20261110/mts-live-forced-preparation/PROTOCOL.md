# Live forced preparation and off-shell metric test

Previous goal turn: verified progress, sealed gauge-source bridge
b38c7a30eca992eab70d20d86c2579d5a19fbac7b83a1381065ddaecd8a18588.
No outstanding worker. Retain the existing 95-state canonical model,
background, couplings, k=5/Mpc, z=10, Delta ln a=.001 and 2e-5 physical /
numerical gate. Algebraic identities use 1e-10. No galaxy state selection.

Derive the initial D0 and D0+D1 response using derivatives of the LIVE
operator and metric source rows, not native-fluid metric derivatives or
future perturbation trajectories. Keep the two physical initial sources
and all rest-species states fixed. Record conditioning and any failure of
the derivative expansion rather than assuming D1 must improve matters.

The exact derivation is a row-operator identity. Numerical native operator
coefficient derivatives use nested five-point one-sided stencils INSIDE
the captured regime, with long-double accumulation of double-input rows.
These are background/operator samples, never supplied future perturbation
states. Compare three stencil spacings before accepting preparation.
This is a numerical realization of derived derivatives, not an assertion
that the native DLL supplies exact symbolic time jets. The scalar carrier
jets use the retained background equations where available.

Independently evaluate the metric momentum residual, rather than declaring
it zero from the observer's native momentum formula. Derive the generalized
constraint-defect identity retaining that residual. Evaluate scalar energy
and current defects separately and the pressure-independent total budget.
Run identical metric checks on the retained heavy and cold controls.

One CPU4/below-normal numerical worker/thread, -B, 900 seconds per worker;
safe handoff before 14:15 UTC. Do not rerun full historical archive or
change original sources. No subagents, GitHub, Galaxy edits, relay/timer,
new browser/server, or other-agent process actions. Preserve failures.
