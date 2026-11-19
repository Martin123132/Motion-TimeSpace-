# Exchange balance checked; pressure readout gap isolated

16 November 2026. Local, bounded continuation of the retained cosmological
window. Authoritative status is verification.json, with matching
verification-replay.json. The exchange checks pass; a separate proposed
canonical-to-Hilbert pressure correction DOES NOT fit the saved allowance.
Do not collapse these two findings into an unqualified all-pass result.

## 1. The saved exchange balance closes

Reused all33 reports through epoch2924, the902 signed preparation nodes,
both32/64 saved evolutions and their full/quadratic/independent-difference
states. No new physical evolution, source bank, coefficients, frequencies,
initial state or fitted parameter was introduced. Source/refinement gates
remain2e-5; local algebra gate remains1e-10.

The derived balance now explicitly accounts for:

- own-field flux and expansion;
- surrounding-density work and the live metric response carrying Q_o;
- actual clock/background interpolation defects;
- the known quadratic-source error, e_approx=-B(S_full-S_quadratic);
- the separate diagnostic state-interpolation Euler residual.

For baseline and MTS, native right-edge packets independently check the
source-rate identity at all33 epochs. Quintic interpolation is only a
diagnostic between existing states; its Euler defect is measured, never
silently set to zero. Integrated work/flux is checked against the actual
saved endpoint changes, with8/16 quadrature refinement included. No all-species
stress closure or certified continuum error bound is inferred.

| Fine-history balance, including quadrature allowance | Baseline | MTS |
|---|---:|---:|
| Density residual / original source scale |1.5286e-17|4.9840e-11|
| Current residual / original source scale |exact zero|7.4807e-11|
| Difference-history density residual / its own correction scale |8.8118e-17|2.1928e-11|
| Difference-history current residual / its own correction scale |exact zero|1.2994e-11|

These are numerical balance checks, not chi-square scores or a new
observational comparison. Both cases use the same rules and the original
case-specific normalizations. The source-channel magnitudes are not directly
comparable between the two models.

There are122 exchange checks (61 per case),30 actual-derivative stress
identity checks and27 final verification checks. All these checks pass.
The separate pressure-correction diagnostic below fails its existing gate.
All report/array replays agree exactly.354 frozen input paths are verified.

## 2. What drives the small approximation correction

For the independently evolved full-minus-quadratic difference, the final
density-source changes are -3.09149950e-10 (baseline) and -2.02555584e-10
(MTS), in their respective saved readout units.

The surrounding-density work contributes -3.13508482e-10 and -2.05407430e-10.
The live-metric term contributes +4.34085839e-12 and +2.55278754e-12.
Own-field/flux/background terms close the remaining difference. This
accounts for the response instead of merely reporting that two spectra
look similar. Q_o is retained through eta_k evolution; it is not discarded
because it does not appear as a separate instantaneous density-work term.

The quadratic positive bath is already diagonalized in the retained mode
basis. Adding an extra g psi X stress in this basis would count its mixing
twice. The external work here is geometric, not a newly fitted force or
an electric charge. Quantum measure remains separate.

## 3. A concrete pressure-readout problem, not hidden

The saved background independently interpolates field b and velocity v.
For f_b=b'-v, the existing action implies a difference between the
canonical/native source and stress formed from the actual field derivative:

    Delta Y_D=Delta Y_P=(a/R0) f_b w,
    Delta Y_Q=(a/R0) k f_b u.

HILBERT-READOUT.md derives the accompanying off-shell identities. They pass,
but identity closure does not make the source correction negligible.
We measured its signed weighted increment relative to the SAME original
matched initial epoch, without changing the history.

| MTS full-history increment | Maximum / original source scale | Existing gate |
|---|---:|---|
| Density |1.55197236e-7|passes2e-5|
| Current |2.05365650e-8|passes2e-5|
| Pressure |2.87618488e-5|FAILS2e-5|

The maximum pressure increment is7.299990787e-9 at report2904.
The original absolute pressure allowance is5.076162418e-9: the increment
is about1.44 times that allowance, not a percent-level observational
discrepancy. Even the final increment5.132305791e-9 exceeds the final
remaining allowance5.076079333e-9 after the saved source uncertainty.
Baseline's own cold subsystem has no scalar velocity substitution and
its correction is exactly zero; other baseline fields are not asserted
to have zero defects.

This is a SOURCE-REPRESENTATION diagnostic, not a new solution or a rejection
of the physical theory. It cannot be repaired consistently by adding the
pressure term alone. The density/current changes also alter the metric
constraint and metric evolution. The reported partial fixed-H shifts reach
2.29779e-9 in z and1.32622e-11 in eta_k'; they hold the stored background
fixed and therefore are not the complete feedback response. A consistent
repair must also account for the background density and H changes.

The canonical histories and their earlier successful tests are retained
unchanged. No corrected source or model is promoted. The next constructive
target is the coupled defect-response calculation in NEXT.md.

## Outputs and preservation

- cold/heavy-result.json and cold/heavy-balance.npz: balances and work terms.
- hilbert-result.json and hilbert-readout.npz: correction and failed budget.
- summary.csv: paired checks and separately labelled readout diagnostics.
- protocol.json and inputs.json: frozen scope, tolerances and provenance.
- closeout.json and CLEANUP-VERIFIED.json: artifact hashes and exact exits.

Everything is local. No GitHub, browser, handoff, subagent, native rebuild
or other-chat process changes. Persistent goal remains paused.
