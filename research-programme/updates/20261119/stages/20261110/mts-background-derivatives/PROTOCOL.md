# Real background derivatives before forced cosmological transport

2026-11-10. Continue the sealed metric-forcing calibration. The constant-H
probe is finished; no new force coefficient or replacement action.

Derive conformal H',H'',H''' from the retained Einstein/background stress
and its species equations. Derive W2 and its residual with those terms,
including their pressure origin. Verify exact dust and constant-H limits.
Do not finite-difference float32 metric transfers to supply these derivatives.

Use the first saved late-time fine window, centred on z=10. Freeze the
interval ln(a/a_center) in[0,.001], already present in both saved histories,
with all399retained k<=5modes. Retain all seven surrounding source knots
[-.004,-.002,-.001,0,.001,.002,.004] as inputs for the next forced evolution.
No new observed data, branch selection or primordial realization is chosen.

Backgrounds are the existing matched heavy a225-w6-d8 packet and its cold
control, each with its own slow field and matter fraction. At these late
times the retained heavy background is the already-matched dust branch;
it must not be silently replaced by a newly invented coherent population.
The quadratic heavy perturbation map remains the explicit interface under test.

Reuse the original StandardSpecies generator only to evaluate its homogeneous
standard-species table, with the same native library and parameters. Do not
recompute perturbation spectra, fit data, rerun the early shooting, or alter
the original tables. Massive-neutrino pressure derivatives are derivatives
of that owner's smooth background table, not newly proven kinetic accuracy.

Evolve the slow field, conformal H and elapsed conformal time independently
from the original interval's first slice. Use the derived Raychaudhuri
equation and check its Friedmann constraint, the saved background and the
two original endpoint clocks. Test DOP853 tolerances2e-11/2e-12, atols1/100
on fixed initial-value scales. Keep algebra gate1e-10 and numerical gate2e-5.
Do not normalize errors by near-zero final values. Preserve failures.

Evaluate the new jets and stable W2 residual on33fixed interval points,
all399heavy modes; keep cold background diagnostics alongside. Such sampled
residuals are diagnostics, not a rigorous interval enclosure. The previous
constant-H certificate cannot be reused for a variable-H history.

The stage must supply actual background evolution and a frozen, sourced
real-history packet, not only equations or a missing-input list. Full forced
field transport and a real-history error enclosure follow using this packet;
no intermediate background check is promoted to that result.

One worker/thread on CPU4, below-normal, <=900seconds per job. Respect
STOP-REQUESTED. No GitHub, browser, galaxy edits, other-agent interference,
new timers, or native library modification. All outputs stay in this stage;
all workers must exit before closeout.
