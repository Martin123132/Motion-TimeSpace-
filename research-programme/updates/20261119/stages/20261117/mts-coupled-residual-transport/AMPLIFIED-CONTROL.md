# Independent finite-amplitude control of the error equation

The original frozen replay score FAILED its error-relative precision gate.
It stays failed: no tolerance or existing result is changed. In particular,
native velocity's total comparison allowance is about0.26% of the predicted
tiny error, versus the unchanged0.002% gate. Full-physics/source gates passed.
Rounding of large cancelling primitives dominates this readout's allowance;
independent trajectory integration differences also contribute. This diagnosis
does not prove the error prediction correct merely because it is plausible.

At a fixed common live background the SAME retained linear operator gives
p_plus'=A p_plus+c-a*r and p_minus'=A p_minus+c+a*r,
with identical parent initial state at3040. Subtracting derives
d=(p_plus-p_minus)/(2a), d'=A d-r, d(t0)=0.
Therefore d=e in exact arithmetic. Each probe is independently integrated
through its physical perturbation coordinates and full native metric/species
coupling. It is NOT reconstructed from the transported error. The forcing r
is computed from the concurrently evolving, unamplified physical approximation,
not fitted to a discrepancy or changed to depend on the probe.

Use both signs of a=16384 and65536, frozen BEFORE these controls, and the SAME
32/64 max steps, clocks, bank, native binary, physical units and tolerances.
The positive and negative probes are numerical tests, not alternative physical
MTS predictions or added parameters. Homogeneity/additivity and zero-offset
native preflights have already passed in this fixed-selector regime. Inactive
seeds are equal and the selector stays zero.

For every value readout B(t)y, compare [B p_plus-B p_minus]/(2a) with B e.
Carry the primitive rounding envelope divided by2a, both step refinements and
the unamplified transported-error rounding into the unchanged2e-5 relative
gate. Test agreement between the TWO amplitudes separately. The average of
the probes should independently recover the concurrently evolved parent;
also check that enlarged controls do not change the unamplified solution
beyond the frozen full-output tolerances. Keep baseline's already verified
zero/linearity controls and earlier raw physics results explicitly separate.

This is a diagnostic of small-error transport with improved signal-to-rounding
ratio, NOT a certified bound on the full physical error, nonlinear response,
or an excuse to rename the original failed gate as passed. No new epoch is
authorized by this supplemental test alone; complete3041 states are retained
for the next controlled continuation decision.
